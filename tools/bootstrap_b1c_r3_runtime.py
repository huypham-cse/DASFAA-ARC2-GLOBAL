"""Operator-only, isolated B1c R3 environment installation; no experiment code.

Print the plan by default. Pass --execute on the Linux server to install.
Every subprocess gets retained stdout/stderr and a durable start/end ledger.
Existing CPU/GPU environments are refused rather than silently replaced.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time
import traceback
import urllib.request
import uuid

ROOT = Path('/network-volume/arc2_recovery_20261030')
PYTHON = '3.11.17'
UV_METADATA_URL = 'https://pypi.org/pypi/uv/json'
TORCH_INDEX = 'https://download.pytorch.org/whl/cu124'
CPU = ('numpy==2.4.6', 'scipy==1.17.1', 'scikit-learn==1.5.1',
       'psutil', 'threadpoolctl', 'pyarrow==25.0.1')
GPU = ('numpy==2.2.6', 'scipy==1.15.3', 'scikit-learn==1.6.1',
       'pydantic==2.14.1', 'faiss-cpu==1.15.1', 'loguru==0.7.3',
       'tqdm==4.70.1', 'psutil', 'threadpoolctl')
TORCH = 'torch==2.6.0+cu124'


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_name(path.name + '.writing')
    with temporary.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def environment():
    # Remove inherited environment/index targeting only for our children.
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(('UV_', 'PIP_'))
           and k not in ('VIRTUAL_ENV', 'CONDA_PREFIX', 'PYTHONHOME', 'PYTHONPATH')}
    env.update(UV_PYTHON_INSTALL_DIR=str(ROOT / 'python'),
               UV_CACHE_DIR=str(ROOT / 'cache'),
               UV_PYTHON_BIN_DIR=str(ROOT / 'bin'),
               UV_MANAGED_PYTHON='1',
               PYTHONPATH=str(ROOT / 'bootstrap'),
               PYTHONNOUSERSITE='1',
               PIP_CACHE_DIR=str(ROOT / 'cache' / 'pip'),
               PIP_CONFIG_FILE=os.devnull,
               TMPDIR=str(ROOT / 'tmp'))
    return env


def command_plan(uv_version='<current PyPI uv version>'):
    uv = [sys.executable, '-m', 'uv', '--no-config']
    cpu_python = str(ROOT / 'envs/cpu/bin/python')
    gpu_python = str(ROOT / 'envs/gpu/bin/python')
    return [
        ('bootstrap_uv', [sys.executable, '-m', 'pip', 'install', '--target',
                          str(ROOT / 'bootstrap'), '--index-url', 'https://pypi.org/simple',
                          'uv==' + uv_version]),
        ('uv_version', uv + ['--version']),
        ('install_python', uv + ['python', 'install', PYTHON]),
        ('cpu_venv', uv + ['venv', '--python', PYTHON, str(ROOT / 'envs/cpu')]),
        ('gpu_venv', uv + ['venv', '--python', PYTHON, str(ROOT / 'envs/gpu')]),
        ('cpu_packages', uv + ['pip', 'install', '--python', cpu_python,
                              '--index-url', 'https://pypi.org/simple', *CPU]),
        ('gpu_packages', uv + ['pip', 'install', '--python', gpu_python,
                              '--index-url', 'https://pypi.org/simple', *GPU]),
        ('gpu_torch', uv + ['pip', 'install', '--python', gpu_python,
                           '--index-url', TORCH_INDEX, TORCH]),
    ]


def metadata_script(packages):
    expected = {p.split('==')[0]: p.split('==')[1] for p in packages if '==' in p}
    names = [p.split('==')[0] for p in packages]
    # importlib.metadata reads installed distribution metadata only. In
    # particular, no NumPy/SciPy/sklearn/torch/faiss package is imported.
    return ('import importlib.metadata as m,json,platform; '
            'v={n:m.version(n) for n in ' + repr(names) + '}; '
            'print(json.dumps({"python":platform.python_version(),"packages":v},sort_keys=True)); '
            'assert platform.python_version()==' + repr(PYTHON) + '; '
            'assert all(v[n]==x for n,x in ' + repr(expected) + '.items())')


def install():
    if sys.platform != 'linux':
        raise RuntimeError('Execution is for the Linux recovery server only')
    ROOT.mkdir(parents=True, exist_ok=True)
    attempt = ROOT / 'install_ledger' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8])
    attempt.mkdir(parents=True, exist_ok=False)
    ledger_path = attempt / 'ledger.json'
    ledger = {'status': 'INSTALLING', 'started_utc': now(), 'root': str(ROOT),
              'operator_python': sys.version, 'platform': platform.platform(),
              'installer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'python_requested': PYTHON, 'commands': [], 'failures': [],
              'algorithm_imports': False, 'scientific_runs': False,
              'numerical_model_probes': False, 'artificial_resource_caps': None,
              'environment_overrides': {k: v for k, v in environment().items()
                                        if k.startswith(('UV_', 'PIP_', 'PYTHON'))}}
    write_json(ledger_path, ledger)

    def run(name, argv):
        index = len(ledger['commands'])
        stdout_path = attempt / (f'{index:02d}_' + name + '.stdout.log')
        stderr_path = attempt / (f'{index:02d}_' + name + '.stderr.log')
        row = {'name': name, 'argv': argv, 'started_utc': now(),
               'status': 'STARTING', 'stdout': str(stdout_path), 'stderr': str(stderr_path)}
        ledger['commands'].append(row)
        write_json(ledger_path, ledger)
        start = time.monotonic()
        with stdout_path.open('xb') as stdout, stderr_path.open('xb') as stderr:
            try:
                child = subprocess.Popen(argv, cwd=ROOT, env=environment(), stdout=stdout, stderr=stderr,
                                         start_new_session=True)
                row.update(pid=child.pid, status='RUNNING')
                write_json(ledger_path, ledger)
                code = child.wait()
            except BaseException as error:
                # Only the subprocess group created by this installer is ours.
                # Record its actual exit without applying time/memory limits.
                if 'child' in locals() and child.poll() is None:
                    os.killpg(child.pid, signal.SIGTERM)
                    row['returncode'] = child.wait()
                row.update(status='FAILED', error=repr(error), ended_utc=now(),
                           elapsed_seconds=time.monotonic() - start)
                write_json(ledger_path, ledger)
                raise
            finally:
                stdout.flush()
                stderr.flush()
                os.fsync(stdout.fileno())
                os.fsync(stderr.fileno())
        row.update(returncode=code, status='PASS' if code == 0 else 'FAILED',
                   ended_utc=now(), elapsed_seconds=time.monotonic() - start)
        write_json(ledger_path, ledger)
        if code:
            raise RuntimeError(name + ' failed with returncode ' + str(code) + '; see ' + str(stderr_path))
        return stdout_path

    try:
        for name in ('cpu', 'gpu'):
            target = ROOT / 'envs' / name
            if target.exists() or target.is_symlink():
                raise FileExistsError('Refuse to replace existing environment: ' + str(target))
        if (ROOT / 'bootstrap').exists() and any((ROOT / 'bootstrap').iterdir()):
            raise FileExistsError('Refuse to merge a new uv installation into a nonempty bootstrap target')
        for name in ('bootstrap', 'envs', 'python', 'cache', 'bin', 'tmp'):
            (ROOT / name).mkdir(exist_ok=True)
        ledger['uv_metadata_request'] = {'url': UV_METADATA_URL, 'started_utc': now()}
        write_json(ledger_path, ledger)
        with urllib.request.urlopen(UV_METADATA_URL) as response:
            payload = response.read()
        (attempt / 'uv_pypi_metadata.json').write_bytes(payload)
        version = json.loads(payload)['info']['version']
        if not isinstance(version, str) or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)+(?:[A-Za-z0-9.+-]*)', version):
            raise ValueError('Unexpected current PyPI uv version: ' + repr(version))
        ledger['uv_metadata_request'].update(completed_utc=now(), resolved_version=version,
                                             sha256=hashlib.sha256(payload).hexdigest())
        write_json(ledger_path, ledger)
        for name, argv in command_plan(version):
            run(name, argv)
        uv = [sys.executable, '-m', 'uv', '--no-config']
        ledger['environment_versions'] = {}
        for name, packages in (('cpu', CPU), ('gpu', (*GPU, TORCH))):
            executable = str(ROOT / 'envs' / name / 'bin/python')
            freeze = run(name + '_pip_freeze', uv + ['pip', 'freeze', '--python', executable])
            frozen_path = attempt / (name + '_pip_freeze.txt')
            frozen_path.write_bytes(freeze.read_bytes())
            versions = run(name + '_metadata_versions', [executable, '-c', metadata_script(packages)])
            ledger['environment_versions'][name] = {**json.loads(versions.read_text(encoding='utf-8')),
                                                    'pip_freeze': str(frozen_path),
                                                    'pip_freeze_sha256': hashlib.sha256(frozen_path.read_bytes()).hexdigest()}
            write_json(ledger_path, ledger)
            run(name + '_pip_check', uv + ['pip', 'check', '--python', executable])
        ledger.update(status='RUNTIME_INSTALLED_METADATA_VERIFIED', completed_utc=now(),
                      next_action='STOP; scientific smoke/full require the separate committed protocol')
        write_json(ledger_path, ledger)
        print(json.dumps({'status': ledger['status'], 'ledger': str(ledger_path)}))
        return 0
    except BaseException as error:
        ledger.update(status='FAILED_PRESERVED', ended_utc=now(), failures=[repr(error)],
                      traceback=traceback.format_exc(), next_action='Inspect retained errors; no fallback version or scientific launch')
        write_json(ledger_path, ledger)
        print(json.dumps({'status': ledger['status'], 'ledger': str(ledger_path), 'error': repr(error)}), file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='Install only into the fixed persistent recovery root')
    args = parser.parse_args()
    if args.execute:
        return install()
    print(json.dumps({'status': 'PLAN_ONLY_NO_INSTALLATION', 'root': str(ROOT),
                      'uv_metadata_url': UV_METADATA_URL,
                      'environment_overrides': {k: v for k, v in environment().items()
                                                if k.startswith(('UV_', 'PIP_', 'PYTHON'))},
                      'commands': command_plan(), 'post_install_checks': 'stdlib distribution versions, uv pip freeze/check; no numerical imports'}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
