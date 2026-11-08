"""Install isolated B2 encoder dependencies; never mutate the baseline runtime."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import subprocess
import sys
import traceback

BASE = Path('/network-volume/arc2_recovery_20261030')
WORK = Path('/home/jovyan/arc2_b2_20261031')
PINS = ['sentence-transformers==4.1.0', 'transformers==4.51.3',
        'huggingface-hub==0.30.2', 'tokenizers==0.21.1', 'safetensors==0.5.3',
        'requests==2.32.3', 'urllib3==2.4.0', 'certifi==2025.1.31',
        'idna==3.10', 'charset-normalizer==3.4.1', 'packaging==25.0',
        'regex==2024.11.6', 'Pillow==11.2.1', 'PyYAML==6.0.3']


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / 'encode_runtime_install'
    out.mkdir(exist_ok=False)
    meta = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'Infrastructure only; no encoder, dataset or qrels invocation',
            'pins': PINS, 'commands': [], 'baseline_runtime_mutated': False}
    def dump():
        (out / 'metadata.json').write_text(json.dumps(meta, indent=2))
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(('UV_', 'PIP_')) and k not in
           ('PYTHONPATH', 'PYTHONHOME', 'CONDA_PREFIX', 'VIRTUAL_ENV')}
    env.update(PYTHONPATH=str(BASE / 'bootstrap'), PYTHONNOUSERSITE='1',
               UV_CACHE_DIR=str(WORK / 'uv_cache'), TMPDIR=str(WORK / 'tmp'),
               PIP_CONFIG_FILE=os.devnull)
    (WORK / 'tmp').mkdir(exist_ok=True)
    uv = [sys.executable, '-m', 'uv', '--no-config']
    def command(name, argv):
        with (out / (name + '.stdout.log')).open('wb') as stdout, (out / (name + '.stderr.log')).open('wb') as stderr:
            r = subprocess.run(argv, env=env, stdout=stdout, stderr=stderr)
        meta['commands'].append({'name': name, 'argv': argv, 'returncode': r.returncode})
        dump()
        if r.returncode:
            raise RuntimeError(name + ' failed')
    try:
        target = WORK / 'envs/encode'
        if target.exists():
            raise FileExistsError('Preserve existing encoder environment')
        command('venv', uv + ['venv', '--python', str(BASE / 'envs/gpu/bin/python'), str(target)])
        site = target / 'lib/python3.11/site-packages'
        (site / 'b2_frozen_runtime.pth').write_text(
            str(BASE / 'envs/gpu/lib/python3.11/site-packages') + '\n' +
            str(BASE / 'envs/cpu/lib/python3.11/site-packages') + '\n')
        command('install', uv + ['pip', 'install', '--python', str(target / 'bin/python'),
                                 '--index-url', 'https://pypi.org/simple', '--no-deps', *PINS])
        code = """import json,importlib,sys,torch
from sentence_transformers import SentenceTransformer
import transformers,numpy,pyarrow
expected={'numpy':'2.2.6','torch':'2.6.0+cu124','sentence_transformers':'4.1.0','transformers':'4.51.3'}
seen={k:importlib.import_module(k).__version__ for k in expected}
assert seen==expected,(seen,expected)
print(json.dumps({'versions':seen,'executable':sys.executable,'cuda':torch.cuda.is_available(),'pyarrow':pyarrow.__version__}))
"""
        command('import_validation', [str(target / 'bin/python'), '-c', code])
        command('freeze', uv + ['pip', 'freeze', '--python', str(target / 'bin/python')])
        meta.update(status='ENCODE_RUNTIME_READY', python=str(target / 'bin/python'))
    except BaseException as error:
        meta.update(status='FAILED_PRESERVED', error=repr(error), traceback=traceback.format_exc())
        raise
    finally:
        meta['ended_utc'] = datetime.now(timezone.utc).isoformat()
        dump()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
