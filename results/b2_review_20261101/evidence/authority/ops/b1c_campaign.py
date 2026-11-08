"""Finite committed B1c smoke ->320 generation -> separate DEV scorer ->STOP."""
import argparse
import json
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
    parser.add_argument('--lock', type=Path, default=ROOT / 'configs/b1c_lock.json')
    parser.add_argument('--recovery', type=Path)
    args = parser.parse_args()
    if not args.name.replace('_', '').isalnum():
        raise ValueError('Invalid campaign name')
    out = ROOT / 'results' / ('b1c_schedule_' + args.name)
    smoke = args.smoke.resolve() if args.smoke else ROOT / 'results' / ('b1c_smoke_' + args.name)
    full = ROOT / 'results' / ('b1c_full_' + args.name)
    out.mkdir(exist_ok=False)
    meta = {'status': 'RUNNING', 'code_commit': args.code_commit,
            'started_unix': time.time(), 'jobs': [], 'TREC_access': False,
            'next_scientific_phase_auto_launch': False}
    dump(out / 'metadata.json', meta)
    commands = [
        ('smoke', [sys.executable, '-u', str(ROOT / 'ops/b1c_stage.py'), '--stage', 'smoke',
                   '--output', str(smoke), '--code-commit', args.code_commit]),
        ('full', [sys.executable, '-u', str(ROOT / 'ops/b1c_stage.py'), '--stage', 'full',
                  '--output', str(full), '--code-commit', args.code_commit, '--smoke', str(smoke)]),
        ('score', [sys.executable, '-u', str(ROOT / 'ops/b1c_score.py'), '--lock',
                   str(args.lock.resolve()), '--run', str(full)])]
    for name, argv in commands:
        if name in ('smoke', 'full'):
            argv.extend(['--lock', str(args.lock.resolve())])
            if args.recovery:
                argv.extend(['--recovery', str(args.recovery.resolve())])
    if args.smoke:
        commands = commands[1:]
        meta['precompleted_smoke'] = str(smoke)
    for name, argv in commands:
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
            meta.update(status='FAILED_PRESERVED', ended_unix=time.time())
            dump(out / 'metadata.json', meta)
            return 1
        dump(out / 'metadata.json', meta)
    meta.update(status='B1C_SCORED_STOP_FOR_D1', ended_unix=time.time(),
                next_action='Retrieve/verify complete DEV results, report and ARIS final D1; STOP before B2')
    dump(out / 'metadata.json', meta)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
