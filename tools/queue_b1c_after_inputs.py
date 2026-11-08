"""Operator launcher: wait for verified inputs and matching smoke, then B1c only.

This does not fit, rank or score; it invokes the already committed campaign.
No timeout, new experiment, resource policy or later-phase launch is added.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import traceback

BASE = Path('/root/arc2_global_paper_20261025')
ROOT = BASE / 'code_19f3f0e_b1c'
PREP = BASE / 'b1c_prepare_mini_20261028'
SMOKE = ROOT / 'results/b1c_smoke_mini_r1_20261028'
COMMIT = '19f3f0e76255d76012a360477c28ecdea25eec70'
TRANSFER_SHA = 'f64584f096cc89d940880be8e11f7e19ab4640cca1cdf9a7e3fb71fbfa354384'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def status(stage, **fields):
    row = {'status': stage, 'updated_unix': time.time(), 'deployment_commit': COMMIT,
           'TREC_access': False, 'next_phase_auto_launch': False, **fields}
    temporary = PREP / 'after_gate_status.tmp'
    temporary.write_text(json.dumps(row, indent=2))
    temporary.replace(PREP / 'after_gate_status.json')


def main():
    try:
        while True:
            smoke = read(SMOKE / 'metadata.json') if (SMOKE / 'metadata.json').exists() else {}
            failed = PREP / 'smoke_r1.process_exit.json'
            if smoke.get('status') == 'FAILED_PRESERVED' or (failed.exists() and read(failed)['returncode']):
                raise RuntimeError('Actual smoke failure; original smoke remains preserved')
            if smoke.get('status') == 'B1C_SMOKE_PASS':
                break
            status('WAITING_FOR_SMOKE')
            time.sleep(10)
        lock = read(ROOT / 'configs/b1c_lock.json')
        if smoke['code_commit'] != COMMIT or smoke['lock_sha256'] != sha(ROOT / 'configs/b1c_lock.json'):
            raise ValueError('Smoke does not match frozen deployment and lock')
        marker = PREP / 'transfer_r1_received.json'
        while not marker.exists():
            status('WAITING_FOR_VERIFIED_INPUT_TRANSFER', smoke_status=smoke['status'])
            time.sleep(10)
        transport = read(marker)
        if transport['status'] != 'TRANSFER_VERIFIED' or transport['files'] != 453 or transport['manifest_sha256'] != TRANSFER_SHA:
            raise ValueError('Input transport does not match the required453-file manifest')
        specs = {}
        def visit(value):
            if isinstance(value, dict):
                if {'path', 'sha256'} <= set(value):
                    path = Path(value['path'])
                    path = path if path.is_absolute() else ROOT / path
                    if path in specs and specs[path] != value['sha256']:
                        raise ValueError('Conflicting source file declaration')
                    specs[path] = value['sha256']
                else:
                    for item in value.values():
                        visit(item)
            elif isinstance(value, list):
                for item in value:
                    visit(item)
        for name in ['registry', 'existing_cells']:
            spec = lock[name]
            path = ROOT / spec['path']
            if sha(path) != spec['sha256']:
                raise ValueError('Registry changed')
            visit(read(path))
        status('VERIFYING_ALL_PREPARED_SOURCES', source_files=len(specs))
        if len(specs) != 567:
            raise ValueError('Expected565 historical files plus2 committed source registries')
        observed = []
        for path, expected in specs.items():
            if 'qrel' in str(path).lower() or sha(path) != expected:
                raise ValueError('Prepared source differs: ' + str(path))
            observed.append({'path': str(path), 'sha256': expected, 'bytes': path.stat().st_size})
        preflight = {'status': 'PASS', 'checked_unix': time.time(), 'files': observed,
                     'transport': transport, 'smoke_sha256': sha(SMOKE / 'metadata.json'),
                     'new_fits_or_rankings': False, 'qrel_reads': 0}
        with (PREP / 'full_preflight_r1.json').open('x') as stream:
            json.dump(preflight, stream, indent=2)
        env = {**os.environ, **lock['cpu_environment']}
        argv = [lock['cpu_python'], '-u', str(ROOT / 'ops/b1c_campaign.py'),
                '--code-commit', COMMIT, '--name', 'mini_r1_20261028', '--smoke', str(SMOKE)]
        with (PREP / 'full_campaign_r1.stdout.log').open('x') as log:
            child = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
            status('B1C_CAMPAIGN_RUNNING', pid=child.pid, argv=argv,
                   smoke_status=smoke['status'], prepared_source_files=len(observed))
            code = child.wait()
        status('B1C_SCORED_STOP_FOR_D1' if code == 0 else 'FAILED_PRESERVED', returncode=code)
        return code
    except BaseException as error:
        record = {'status': 'FAILED_PRESERVED', 'error': repr(error),
                  'traceback': traceback.format_exc(), 'time': time.time()}
        with (PREP / ('after_gate_failure_' + str(time.time_ns()) + '.json')).open('x') as stream:
            json.dump(record, stream, indent=2)
        status('FAILED_PRESERVED', error=repr(error))
        raise


if __name__ == '__main__':
    raise SystemExit(main())
