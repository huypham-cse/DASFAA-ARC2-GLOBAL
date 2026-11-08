"""Finite committed B1c-R3 smoke ->358 generation -> separate DEV scorer ->STOP."""
import argparse
import json
import hashlib
import traceback
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ops'))
from b1a_stage import dump


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--smoke', type=Path, help='Already completed matching smoke; full stage verifies it')
    parser.add_argument('--restored-root', type=Path, required=True)
    parser.add_argument('--lock', type=Path, default=ROOT / 'configs/b1c_r3_lock.json')
    args = parser.parse_args()
    if not args.name.replace('_', '').isalnum():
        raise ValueError('Invalid campaign name')
    out = ROOT / 'results' / ('b1c_r3_schedule_' + args.name)
    smoke = args.smoke.resolve() if args.smoke else ROOT / 'results' / ('b1c_r3_smoke_' + args.name)
    full = ROOT / 'results' / ('b1c_r3_full_' + args.name)
    out.mkdir(exist_ok=False)
    lock_path = args.lock.resolve(strict=True)
    lock_sha = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    meta = {'status': 'RUNNING', 'stage': 'B1c-R3', 'code_commit': args.code_commit,
            'lock_path': str(lock_path), 'lock_sha256': lock_sha,
            'restored_root': str(args.restored_root.resolve()),
            'started_unix': time.time(), 'jobs': [], 'TREC_access': False,
            'next_scientific_phase_auto_launch': False}
    dump(out / 'metadata.json', meta)
    commands = [
        ('smoke', [sys.executable, '-u', str(ROOT / 'ops/b1c_r3_stage.py'), '--stage', 'smoke',
                   '--output', str(smoke), '--code-commit', args.code_commit]),
        ('full', [sys.executable, '-u', str(ROOT / 'ops/b1c_r3_stage.py'), '--stage', 'full',
                  '--output', str(full), '--code-commit', args.code_commit, '--smoke', str(smoke)]),
        ('score', [sys.executable, '-u', str(ROOT / 'ops/b1c_r3_score.py'), '--lock',
                   str(args.lock.resolve()), '--run', str(full)])]
    for name, argv in commands:
        if name in ('smoke', 'full'):
            argv.extend(['--lock', str(args.lock.resolve()), '--restored-root', str(args.restored_root.resolve())])
    if args.smoke:
        commands = commands[1:]
        meta['precompleted_smoke'] = str(smoke)
    try:
        for name, argv in commands:
            if hashlib.sha256(lock_path.read_bytes()).hexdigest() != lock_sha:
                raise ValueError('R3 lock changed during campaign')
            row = {'stage': name, 'argv': argv, 'started_unix': time.time()}
            meta['jobs'].append(row)
            dump(out / 'metadata.json', meta)
            with (out / (name + '.stdout.log')).open('x') as stdout, (out / (name + '.stderr.log')).open('x') as stderr:
                child = subprocess.Popen(argv, cwd=ROOT, stdout=stdout, stderr=stderr)
                row['pid'] = child.pid
                dump(out / 'metadata.json', meta)
                code = child.wait()
            row.update(returncode=code, ended_unix=time.time())
            if code:
                raise RuntimeError('R3 ' + name + ' failed with exit ' + str(code))
            receipt_path = (smoke if name == 'smoke' else full) / 'metadata.json'
            if name == 'score':
                receipt_path = full / 'scoring' / 'completed.json'
            receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
            expected = {'smoke': 'B1C_R3_SMOKE_PASS', 'full': 'B1C_R3_RANKINGS_SEALED_STOP',
                        'score': 'DEV_SCORED'}[name]
            if receipt.get('status') != expected:
                raise ValueError('Missing matching completion receipt for ' + name)
            if name != 'score' and any(receipt.get(k) != v for k, v in
                                       (('code_commit', args.code_commit), ('lock_sha256', lock_sha))):
                raise ValueError('R3 stage completion has a different code/lock identity')
            if name == 'score':
                summary_path = full / 'scoring' / 'summary.json'
                if hashlib.sha256(summary_path.read_bytes()).hexdigest() != receipt.get('summary_sha256'):
                    raise ValueError('R3 scored summary hash differs from its completion receipt')
                summary = json.loads(summary_path.read_text(encoding='utf-8'))
                if (summary.get('scorer_code_commit') != args.code_commit
                        or summary.get('lock_sha256') != lock_sha
                        or (summary.get('ranking_cells'), summary.get('imported_cells'), summary.get('new_cells')) != (736, 378, 358)):
                    raise ValueError('R3 scored completion has a different code/lock/matrix identity')
            row.update(receipt_path=str(receipt_path), receipt_sha256=hashlib.sha256(receipt_path.read_bytes()).hexdigest())
            dump(out / 'metadata.json', meta)
    except BaseException as error:
        meta.update(status='FAILED_PRESERVED', ended_unix=time.time(),
                    failures=[repr(error)], traceback=traceback.format_exc())
        dump(out / 'metadata.json', meta)
        return 1
    meta.update(status='B1C_R3_SCORED_STOP_FOR_D1', ended_unix=time.time(),
                next_action='Retrieve/verify complete DEV results, report and ARIS final D1; STOP before B2')
    dump(out / 'metadata.json', meta)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
