"""Copy verified terminal B2 evidence into a portable, compact review bundle.

Original scientific paths stay in the manifest; mutable operator snapshots are
resolved only through terminal coverage. Large tensors/checkpoints remain in
the separately completed local backup. No scientific output is modified.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REMOTE = '/home/jovyan/arc2_b2_20261031/code_26feef1/'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--backup', type=Path, default=Path('D:/ARC2-B2-backup-20261031'))
    ap.add_argument('--output', type=Path, default=ROOT / 'results/b2_review_20261101/evidence')
    args = ap.parse_args()
    backup, out = args.backup.resolve(), args.output.resolve()
    if out.exists():
        raise FileExistsError('Preserve existing evidence bundle')
    state = json.loads((backup / 'operator_state.json').read_text(encoding='utf-8'))
    events = [json.loads(x) for x in (backup / 'operator_events.jsonl').read_text().splitlines()]
    if events[-1]['status'] != 'COMPLETE_CAMPAIGN_BACKED_UP':
        raise ValueError('Terminal verified backup required')
    full = 'results/b2_full_r1_20261031t064859/'
    files, omitted = {}, {}
    out.mkdir(parents=True)

    def publish(source, rel, original, expected=None):
        target = (out / rel).resolve()
        if not target.is_relative_to(out) or target == out:
            raise ValueError('Path escapes review bundle')
        observed = {'bytes': source.stat().st_size, 'sha256': sha(source)}
        if expected and any(observed[k] != expected[k] for k in observed):
            raise ValueError('Backup file hash/size mismatch: ' + rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha(target) != observed['sha256']:
            raise ValueError('Copy hash mismatch: ' + rel)
        files[rel] = dict(path=original, **observed)

    for rel, spec in state['coverage'].items():
        suffix = Path(rel).suffix
        include = (rel.startswith(full) and suffix not in ('.pt', '.npz', '.safetensors', '.parquet')
                   and not (suffix == '.npy' and spec['bytes'] > 32 * 1024 * 1024))
        include |= not rel.startswith(full) and suffix in ('.json', '.log', '.jsonl')
        if not include:
            omitted[rel] = {'bytes': spec['bytes'], 'sha256': spec['sha256'], 'local': spec['local']}
            continue
        source = (backup / spec['local']).resolve()
        if not source.is_relative_to(backup):
            raise ValueError('Backup path escape')
        publish(source, rel, REMOTE + rel, spec)
    authority = ['configs/b2_lock.json', 'configs/b2_acquisition.json',
                 'protocols/B2_TREC_COVID_CONFIRMATION_20261031.md']
    lock = json.loads((ROOT / authority[0]).read_text())
    authority += list(lock['source_sha256_canonical_lf'])
    for rel in dict.fromkeys(authority):
        publish(ROOT / rel, 'authority/' + rel, REMOTE + rel)
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
                'scientific_code_commit': '26feef1026bea610ec7f53d581c3c9064949d004',
                'files': files, 'file_count': len(files),
                'bytes': sum(s['bytes'] for s in files.values()),
                'omitted_large_inputs_and_fit_artifacts': omitted,
                'full_backup': str(backup),
                'coverage_sha256': sha(backup / 'operator_state.json'),
                'terminal_event': events[-1],
                'scope': 'Portable raw rankings, per-query scores, bootstrap draws, seals, IDs, selections, logs and source. Large vector/fit regeneration requires full backup.'}
    (out / 'bundle_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: manifest[k] for k in ['file_count', 'bytes', 'scope']}))


if __name__ == '__main__':
    main()
