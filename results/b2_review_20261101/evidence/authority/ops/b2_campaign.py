"""Finite B2 campaign: pinned inputs -> matching smokes ->184 ->verify ->score."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def dump(path, obj):
    tmp = path.with_suffix('.writing')
    with tmp.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(obj, stream, indent=2, allow_nan=False)
        stream.flush(); os.fsync(stream.fileno())
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    if not args.name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_' for c in args.name):
        raise ValueError('Use a unique safe campaign name')
    lockpath = args.lock.resolve(strict=True)
    lock = json.loads(lockpath.read_text())
    paths = {kind: ROOT / 'results' / ('b2_' + kind + '_' + args.name)
             for kind in ['schedule', 'assets', 'encode_smoke', 'smoke', 'encode_full', 'full']}
    if any(path.exists() for path in paths.values()):
        raise FileExistsError('Preserve all existing attempt directories')
    paths['schedule'].mkdir(parents=True)
    out = paths['schedule']
    meta = {'status': 'RUNNING', 'stage': 'B2', 'code_commit': args.code_commit,
            'lock_sha256': sha(lockpath), 'paths': {k: str(v) for k, v in paths.items()},
            'started_utc': datetime.now(timezone.utc).isoformat(), 'jobs': [],
            'manuscript_updates': False, 'next_scientific_phase_auto_launch': False}
    dump(out / 'metadata.json', meta)
    cpu, encode = lock['cpu_python'], lock['encoder_python']
    common = ['--lock', str(lockpath), '--code-commit', args.code_commit]
    stages = [
        ('acquire', [cpu, '-u', str(ROOT / 'ops/b2_inputs.py'), '--stage', 'acquire', *common,
                     '--out', str(paths['assets'])], paths['assets'] / 'acquisition_manifest.json', 'ACQUISITION_PASS'),
        ('encode_smoke', [encode, '-u', str(ROOT / 'ops/b2_inputs.py'), '--stage', 'smoke', *common,
                          '--assets', str(paths['assets']), '--out', str(paths['encode_smoke'])],
                         paths['encode_smoke'] / 'encoding_manifest.json', 'SMOKE_ENCODING_PASS'),
        ('smoke', [cpu, '-u', str(ROOT / 'ops/b2_stage.py'), '--stage', 'smoke', *common,
                   '--output', str(paths['smoke'])], paths['smoke'] / 'metadata.json', 'B2_SMOKE_PASS'),
        ('verify_smoke', [cpu, '-u', str(ROOT / 'ops/b2_verify.py'), '--lock', str(lockpath),
                          '--run', str(paths['smoke']), '--smoke'],
                         paths['smoke'] / 'verification/verification_seal.json', 'B2_ENDPOINT_SMOKE_PASS'),
        ('encode_full', [encode, '-u', str(ROOT / 'ops/b2_inputs.py'), '--stage', 'encode', *common,
                         '--assets', str(paths['assets']), '--out', str(paths['encode_full'])],
                        paths['encode_full'] / 'encoding_manifest.json', 'ENCODING_PASS'),
        ('full', [cpu, '-u', str(ROOT / 'ops/b2_stage.py'), '--stage', 'full', *common,
                  '--output', str(paths['full']), '--encoding', str(paths['encode_full']),
                  '--smoke', str(paths['smoke'])], paths['full'] / 'metadata.json', 'B2_RANKINGS_SEALED_STOP'),
        ('verify', [cpu, '-u', str(ROOT / 'ops/b2_verify.py'), '--lock', str(lockpath),
                    '--run', str(paths['full'])], paths['full'] / 'verification/verification_seal.json',
                   'ENDPOINTS_INDEPENDENTLY_VERIFIED'),
        ('score', [cpu, '-u', str(ROOT / 'ops/b2_score.py'), '--lock', str(lockpath),
                   '--run', str(paths['full'])], paths['full'] / 'scoring/completed.json', 'FINAL_SCORED'),
    ]
    env = {**os.environ, **lock['environment'], 'PYTHONNOUSERSITE': '1',
           'TOKENIZERS_PARALLELISM': 'false', 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1'}
    child = None
    def interrupted(sig, frame):
        if child is not None and child.poll() is None:
            child.terminate()
        raise RuntimeError('Campaign interrupted by signal ' + str(sig))
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != args.code_commit:
            raise ValueError('Deployment commit drift')
        for name, argv, receipt_path, expected in stages:
            job = {'stage': name, 'argv': argv, 'started_utc': datetime.now(timezone.utc).isoformat()}
            meta['jobs'].append(job); meta['current_stage'] = name
            dump(out / 'metadata.json', meta)
            with (out / (name + '.stdout.log')).open('xb') as stdout, (out / (name + '.stderr.log')).open('xb') as stderr:
                child = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
                job['pid'] = child.pid; dump(out / 'metadata.json', meta)
                job['returncode'] = child.wait()
            job['ended_utc'] = datetime.now(timezone.utc).isoformat()
            dump(out / 'metadata.json', meta)
            if job['returncode']:
                raise RuntimeError('Preserved failed stage ' + name)
            receipt = json.loads(receipt_path.read_text())
            if receipt.get('status') != expected:
                raise ValueError('Unexpected stage receipt: ' + name)
            if sha(lockpath) != meta['lock_sha256']:
                raise ValueError('Lock changed during campaign')
            job['receipt_path'] = str(receipt_path); job['receipt_sha256'] = sha(receipt_path)
            dump(out / 'metadata.json', meta)
        meta.update(status='B2_SCORED_STOP_FOR_REVIEW', current_stage='STOP',
                    next_action='Retrieve/verify results, figures and ARIS review; leave manuscript untouched; no systems')
    except BaseException as error:
        meta.update(status='FAILED_PRESERVED', error=repr(error), traceback=traceback.format_exc(),
                    final_labels_opened=(paths['full'] / 'first_final_qrel_open.json').exists())
    finally:
        meta['ended_utc'] = datetime.now(timezone.utc).isoformat()
        dump(out / 'metadata.json', meta)
    return 0 if meta['status'] == 'B2_SCORED_STOP_FOR_REVIEW' else 1


if __name__ == '__main__':
    raise SystemExit(main())
