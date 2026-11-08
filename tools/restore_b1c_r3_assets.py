"""Operator-only, opaque B1c R3 asset restoration; Python standard library only.

Local: --plan-only --allocation allocation.json
Remote: --cloud-only --allocation allocation.json
Upload local sources separately using allocation.sources[*].local_path. This
program has no SSH, array loading, encoding, fitting, ranking or label parser.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
import time
import urllib.parse
import urllib.request
import uuid

BASE = Path(__file__).resolve().parents[1]
QA = BASE / 'provenance/qa/cloud_backup_20261030'
DEFAULT_ROOT = '/network-volume/arc2_recovery_20261030'
MANIFEST_MEMBER = '__ARC2_BACKUP__/manifest.json'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def atomic_json(path, value):
    """Identical existing records are idempotent; conflicting records survive."""
    path = Path(path)
    data = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError('Conflicting existing JSON: ' + str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + '.part-' + uuid.uuid4().hex)
    with partial.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.rename(partial, path)


def original_path(value):
    if not isinstance(value, str) or '\\' in value:
        raise ValueError('Invalid original source path')
    parts = PurePosixPath(value).parts
    if (not value.startswith('/root/') or '..' in parts
            or str(PurePosixPath(value)) != value):
        raise ValueError('Noncanonical or escaping original source path: ' + value)
    return value


def restored_path(root, original):
    return str(PurePosixPath(root) / original_path(original).lstrip('/'))


def source_record(path, sha256, size, root, acquisition, **extra):
    original_path(path)
    if not re.fullmatch('[0-9a-f]{64}', sha256):
        raise ValueError('Invalid source SHA256: ' + path)
    if not isinstance(size, int) or size < 0:
        raise ValueError('Invalid source byte count: ' + path)
    return dict(path=path, sha256=sha256, bytes=size,
                restored_path=restored_path(root, path),
                acquisition=acquisition, **extra)


def build_allocation(args):
    additional = read_json(args.manifest)
    matches = read_json(args.local_matches)
    selected = read_json(args.selected_input_plan)
    excluded = {r['original_path'] for r in additional['excluded_unmatched_original_files']}
    original = {}
    for archive in selected['archives']:
        for row in archive['required_files']:
            old = original.setdefault(row['path'], row)
            if old != row:
                raise ValueError('Conflicting original source: ' + row['path'])
    if len(original) != 565 or len(excluded) != 29:
        raise ValueError('Unexpected historical source/exclusion count')
    sources = {}
    # Resolve paths only; the transport must verify bytes before accepting them.
    # The original exact-match inventory remains the authority for local aliases.
    for path, row in original.items():
        if path in excluded:
            continue
        candidates = matches['matches'].get(row['sha256'], [])
        if candidates:
            source = next((p for p in candidates if Path(p).is_file()), None)
            if source is None:
                raise FileNotFoundError('No local alias remains for ' + path)
            sources[path] = source_record(path, row['sha256'], row['bytes'],
                                          args.restore_root, 'local_upload',
                                          local_path=source)
    if len(sources) != 514:
        raise ValueError('Expected exactly514 local source allocations')
    for row in additional['restore_files']:
        path = row['original_path']
        if path in excluded or path in sources:
            raise ValueError('Duplicate or excluded cloud allocation: ' + path)
        sources[path] = source_record(path, row['expected_sha256'], row['expected_bytes'],
                                      args.restore_root, 'cloud_archive',
                                      host=row['host'], chunk=row['chunk'],
                                      archive_name=row['expected_archive_name'])
        if path in original and (sources[path]['sha256'], sources[path]['bytes']) != (
                original[path]['sha256'], original[path]['bytes']):
            raise ValueError('Original source identity drift: ' + path)
    if len(sources) != 629 or set(original) - excluded - set(sources):
        raise ValueError('Incomplete or unexpected629-source acquisition')
    root = PurePosixPath(args.restore_root)
    if not root.is_absolute() or '..' in root.parts:
        raise ValueError('Restore root must be an absolute POSIX path')
    allocation = {
        'schema': 'ARC2_B1C_R3_OPAQUE_ALLOCATION_V1',
        'scope': 'Acquisition only; local uploads are separate. No array derivation or scientific execution.',
        'review_independence': 'same-family', 'acceptance_status': 'provisional',
        'restore_root': args.restore_root,
        'input_manifests': {str(p): digest(p) for p in (
            args.manifest, args.local_matches, args.selected_input_plan)},
        'archives': additional['archives'],
        'counts': {'local_upload': 514, 'cloud_archive': 115, 'sources': 629},
        'sources': sorted(sources.values(), key=lambda r: r['path']),
        'excluded_original_paths': sorted(excluded),
        'derived_slices_pending_committed_preflight': additional['derived_slice_preflight'],
    }
    atomic_json(args.allocation, allocation)
    return allocation


def verify_file(path, expected_hash, expected_bytes):
    path = Path(path)
    if (not path.is_file() or path.is_symlink() or path.stat().st_size != expected_bytes
            or digest(path) != expected_hash):
        raise ValueError('Missing or conflicting existing bytes: ' + str(path))


def destination(root, original):
    root = Path(root).resolve()
    path = root / original_path(original).lstrip('/')
    if not path.resolve().is_relative_to(root):
        raise ValueError('Destination escapes restore root')
    return path


def download(drive_id, target):
    if not re.fullmatch('[A-Za-z0-9_-]+', drive_id):
        raise ValueError('Invalid Drive file ID')
    target = Path(target)
    if target.exists():
        if not target.is_file() or target.is_symlink():
            raise ValueError('Invalid existing download: ' + str(target))
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + '.part-' + uuid.uuid4().hex)
    url = 'https://drive.usercontent.google.com/download?' + urllib.parse.urlencode(
        {'id': drive_id, 'export': 'download', 'confirm': 't'})
    with urllib.request.urlopen(url, timeout=60) as response, partial.open('xb') as stream:
        for data in iter(lambda: response.read(1024 * 1024), b''):
            stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.rename(partial, target)


def safe_member(name):
    if (not name or '\\' in name or name.startswith('/')
            or '..' in PurePosixPath(name).parts
            or str(PurePosixPath(name)) != name.rstrip('/')):
        raise ValueError('Unsafe/noncanonical archive member: ' + name)
    return name.rstrip('/')


def extract_whitelist(archive_path, receipt, wanted, root):
    """Hash-verified archive; stage only whitelisted regular-file payloads."""
    verify_file(archive_path, receipt['archive_sha256'], receipt['archive_bytes'])
    staged = []
    found = set()
    headers = {}
    embedded = None
    with tarfile.open(archive_path, mode='r|gz') as archive:
        for member in archive:
            name = safe_member(member.name)
            if name in headers or (name == MANIFEST_MEMBER and embedded is not None):
                raise ValueError('Duplicate archive member: ' + name)
            if name == MANIFEST_MEMBER:
                if not member.isfile():
                    raise ValueError('Embedded manifest is not a regular file')
                embedded = archive.extractfile(member).read()
                continue
            path = '/' + name
            kind = 'file' if member.isfile() else 'dir' if member.isdir() else 'link' if member.issym() else 'unsupported'
            headers[name] = (kind, member.size)
            if path not in wanted:
                continue
            row = wanted[path]
            if not member.isfile() or member.size != row['bytes']:
                raise ValueError('Whitelisted member type/size mismatch: ' + path)
            found.add(path)
            target = destination(root, path)
            if target.exists():
                verify_file(target, row['sha256'], row['bytes'])
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            partial = target.with_name(target.name + '.part-' + uuid.uuid4().hex)
            h = hashlib.sha256()
            size = 0
            with archive.extractfile(member) as source, partial.open('xb') as stream:
                for data in iter(lambda: source.read(1024 * 1024), b''):
                    stream.write(data)
                    h.update(data)
                    size += len(data)
                stream.flush()
                os.fsync(stream.fileno())
            if size != row['bytes'] or h.hexdigest() != row['sha256']:
                raise ValueError('Whitelisted member SHA256/size mismatch: ' + path)
            staged.append((partial, target, row))
    if embedded is None or hashlib.sha256(embedded).hexdigest() != receipt['manifest_sha256']:
        raise ValueError('Embedded source manifest hash mismatch')
    entries = json.loads(embedded)['entries']
    if len(entries) != receipt['entries'] or len(headers) != len(entries):
        raise ValueError('Embedded source manifest/member count mismatch')
    declared = {}
    for entry in entries:
        path = original_path(entry['path'])
        if path in declared:
            raise ValueError('Duplicate embedded source path')
        declared[path] = entry
        if headers.get(path.lstrip('/')) != (entry['kind'], entry['bytes'] if entry['kind'] == 'file' else 0):
            raise ValueError('Embedded source manifest/header mismatch: ' + path)
    if found != set(wanted):
        raise ValueError('Missing whitelisted archive sources: ' + repr(sorted(set(wanted) - found)))
    for path, row in wanted.items():
        entry = declared[path]
        if (entry['kind'], entry.get('sha256'), entry['bytes']) != ('file', row['sha256'], row['bytes']):
            raise ValueError('Whitelist differs from embedded source manifest: ' + path)
    for partial, target, row in staged:
        if target.exists():
            verify_file(target, row['sha256'], row['bytes'])
            partial.unlink()
        else:
            os.rename(partial, target)
    return len(found)


def cloud_restore(args):
    allocation = read_json(args.allocation)
    if allocation.get('schema') != 'ARC2_B1C_R3_OPAQUE_ALLOCATION_V1':
        raise ValueError('Unsupported allocation')
    root = allocation['restore_root']
    if root != args.restore_root:
        raise ValueError('Allocation/CLI restore-root mismatch')
    cloud = [r for r in allocation['sources'] if r['acquisition'] == 'cloud_archive']
    if len(cloud) != 115 or len({r['path'] for r in cloud}) != 115:
        raise ValueError('Expected115 unique cloud sources')
    for row in cloud:
        source_record(row['path'], row['sha256'], row['bytes'], root, 'cloud_archive')
        if row['restored_path'] != restored_path(root, row['path']):
            raise ValueError('Restored alias drift')
    archive_names = [a['expected_archive_name'] for a in allocation['archives']]
    if (len(archive_names) != 11 or len(set(archive_names)) != 11
            or {r['archive_name'] for r in cloud} != set(archive_names)):
        raise ValueError('Cloud archive allocation mismatch')
    allocation_sha = digest(args.allocation)
    successes = 0
    for archive in allocation['archives']:
        name = archive['expected_archive_name']
        if not re.fullmatch('chunk_[0-9]{4}_[0-9a-f]{16}\\.tar\\.gz', name):
            raise ValueError('Invalid archive name')
        wanted = {r['path']: r for r in cloud if r['archive_name'] == name}
        success_path = args.receipt_dir / (name + '.restore_verified.json')
        event = {'archive': name, 'allocation_sha256': allocation_sha, 'time_unix': time.time()}
        try:
            if success_path.exists():
                prior = read_json(success_path)
                if prior['allocation_sha256'] != allocation_sha or prior['sources'] != sorted(wanted):
                    raise ValueError('Conflicting existing restore receipt')
                for path, row in wanted.items():
                    verify_file(destination(root, path), row['sha256'], row['bytes'])
                event.update(status='ALREADY_VERIFIED', files=len(wanted))
            else:
                receipt_path = args.cache_root / (name + '.verified.json')
                if archive['expected_receipt_name'] != receipt_path.name:
                    raise ValueError('Unexpected original receipt name')
                download(archive['receipt_drive_id'], receipt_path)
                receipt = read_json(receipt_path)
                if receipt.get('status') != 'BACKUP_VERIFIED':
                    raise ValueError('Original archive receipt is not BACKUP_VERIFIED')
                for key in ('archive_sha256', 'manifest_sha256'):
                    if not re.fullmatch('[0-9a-f]{64}', receipt[key]):
                        raise ValueError('Invalid original receipt digest')
                if not all(type(receipt[k]) is int and receipt[k] > 0 for k in ('archive_bytes', 'entries')):
                    raise ValueError('Invalid original receipt counts')
                archive_path = args.cache_root / name
                download(archive['drive_id'], archive_path)
                count = extract_whitelist(archive_path, receipt, wanted, root)
                atomic_json(success_path, {'status': 'RESTORE_VERIFIED', 'allocation_sha256': allocation_sha,
                    'archive': name, 'archive_sha256': receipt['archive_sha256'],
                    'archive_bytes': receipt['archive_bytes'], 'original_receipt_sha256': digest(receipt_path),
                    'embedded_manifest_sha256': receipt['manifest_sha256'], 'sources': sorted(wanted)})
                event.update(status='RESTORE_VERIFIED', files=count)
            successes += 1
        except Exception as error:
            event.update(status='FAILED_PRESERVED', error=type(error).__name__ + ': ' + str(error))
            raise
        finally:
            atomic_json(args.receipt_dir / ('attempt_%s_%s.json' % (time.time_ns(), uuid.uuid4().hex)), event)
            print(json.dumps(event), flush=True)
    return {'status': 'CLOUD_ASSETS_VERIFIED', 'archives': successes, 'cloud_files': len(cloud),
            'local_uploads': 'Separate transport; not verified or performed by --cloud-only',
            'allocation_sha256': allocation_sha}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--plan-only', action='store_true')
    mode.add_argument('--cloud-only', action='store_true')
    parser.add_argument('--allocation', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, default=QA / 'r3_additional_recovery_sources.json')
    parser.add_argument('--local-matches', type=Path, default=QA / 'local_source_matches.json')
    parser.add_argument('--selected-input-plan', type=Path, default=QA / 'selected_input_recovery_plan.json')
    parser.add_argument('--restore-root', default=DEFAULT_ROOT + '/restored')
    parser.add_argument('--cache-root', type=Path, default=Path(DEFAULT_ROOT + '/downloads'))
    parser.add_argument('--receipt-dir', type=Path, default=Path(DEFAULT_ROOT + '/receipts'))
    args = parser.parse_args()
    if args.plan_only:
        allocation = build_allocation(args)
        print(json.dumps({'status': 'PLAN_ONLY', 'allocation': str(args.allocation),
                          'counts': allocation['counts'], 'downloads_performed': False}), flush=True)
        return 0
    if os.name != 'posix':
        parser.error('--cloud-only runs on the remote POSIX filesystem')
    print(json.dumps(cloud_restore(args)), flush=True)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({'status': 'FAILED_PRESERVED', 'error': type(error).__name__ + ': ' + str(error)}), file=sys.stderr)
        raise SystemExit(1)
