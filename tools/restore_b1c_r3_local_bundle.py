"""Restore only the 515 hash-pinned local byte copies; never parse labels."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allocation', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    expected = '9be3f215050b133b0839041dd12c5f8228401d0fc8395e3293793785e649c489'
    if args.archive.stat().st_size != 327864320 or sha(args.archive) != expected:
        raise ValueError('Local transfer container differs from original pinned bytes')
    allocation = json.loads(args.allocation.read_text())
    root = Path(allocation['restore_root']).resolve()
    if str(root) != '/network-volume/arc2_recovery_20261030/restored':
        raise ValueError('Unexpected restoration root')
    rows = {r['path'].lstrip('/'): r for r in allocation['sources'] if 'local_path' in r}
    if len(rows) != 515:
        raise ValueError('Expected 515 local source files')
    seen, published = set(), []
    with tarfile.open(args.archive, 'r|') as archive:
        for member in archive:
            if member.name not in rows or member.name in seen or not member.isfile():
                raise ValueError('Unexpected or duplicated archive member')
            row = rows[member.name]
            target = (root / member.name).resolve()
            if not target.is_relative_to(root) or str(target) != row['restored_path']:
                raise ValueError('Restored alias differs from the acquisition allocation')
            if member.size != row['bytes']:
                raise ValueError('Source size differs: ' + member.name)
            seen.add(member.name)
            if target.exists():
                if target.is_symlink() or target.stat().st_size != row['bytes'] or sha(target) != row['sha256']:
                    raise ValueError('Existing source conflict: ' + str(target))
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + '.local-restore.part')
            with archive.extractfile(member) as source, temporary.open('xb') as out:
                for chunk in iter(lambda: source.read(4 * 1024 * 1024), b''):
                    out.write(chunk)
            if temporary.stat().st_size != row['bytes'] or sha(temporary) != row['sha256']:
                raise ValueError('Restored source failed identity: ' + str(target))
            temporary.rename(target)
            published.append(str(target))
    if seen != set(rows):
        raise ValueError('Incomplete source transfer')
    receipt = {'status': 'LOCAL_ASSETS_VERIFIED', 'files': len(seen), 'newly_published': len(published),
               'archive_sha256': expected, 'allocation_sha256': sha(args.allocation),
               'opaque_dev_label_transport': True, 'labels_parsed': False, 'fits': 0}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open('x') as out:
        json.dump(receipt, out, indent=2)
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
