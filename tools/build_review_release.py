"""Build a clean, read-only scientific review snapshot; no experiments or labels fetched."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEST = Path('D:/DASFAA-2027-paper-release')
RESULTS = ('b1mp0_r1_review_20261026', 'b1p_r5_review_20261027',
           'b1g_r1_review_20261027', 'b1c_r3_review_20261031', 'b2_review_20261101')
TOOLS = ('verify_b1c_r3_completed.py', 'verify_b2_completed.py',
         'render_b1c_r3_report.py', 'render_b2_report.py')
WRAPPERS = ('verify_review_release.py', 'rebuild_review_figures.py', 'smoke_review_method.py')


def extended(p):
    p = str(Path(p).resolve())
    return Path('\\\\?\\' + p) if os.name == 'nt' and not p.startswith('\\\\?\\') else Path(p)


def sha(p):
    h = hashlib.sha256()
    with extended(p).open('rb') as s:
        for b in iter(lambda: s.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def emit(rel, data):
    p = DEST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding='utf-8', newline='\n')


def build():
    DEST.mkdir(exist_ok=True)
    if any(DEST.iterdir()):
        raise FileExistsError('Preserve nonempty release; build into an empty release directory')
    copied, omitted = {}, []

    def copy(p, rel=None):
        rel = rel or p.relative_to(ROOT).as_posix()
        dst = DEST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(extended(p), extended(dst))
        assert sha(p) == sha(dst), rel
        copied[rel] = p.relative_to(ROOT).as_posix()

    for directory in ('src', 'ops', 'configs', 'protocols', 'licenses'):
        for p in (ROOT / directory).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                copy(p)
    for name in ('pyproject.toml', 'THIRD_PARTY_NOTICES.md'):
        copy(ROOT / name)
    for name in TOOLS:
        copy(ROOT / 'tools' / name)
    for name in WRAPPERS:
        copy(ROOT / 'tools' / name, 'reproduce/' + name)
    for name in RESULTS:
        base = ROOT / 'results' / name
        for p in extended(base).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts:
                continue
            relative = p.relative_to(extended(base))
            if name.startswith('b1g') and relative.parts[0] in ('main', 'mini', 'smoke', 'transport'):
                omitted.append({'path': 'results/' + name + '/' + relative.as_posix(),
                                'bytes': p.stat().st_size,
                                'reason': 'B1-G supporting scored diagnostics included; raw sampled-vector galleries and redundant transfer containers remain in original project.'})
                continue
            # Use original spelling rather than Windows extended prefix in provenance.
            copy(base / relative, 'results/' + name + '/' + relative.as_posix())
    # Every original source pin is required even when its path looks like a
    # historical helper or an intermediate. Keep the original bytes.
    for lock_name in ('b1c_r3_lock.json', 'b2_lock.json'):
        lock = json.loads((ROOT / 'configs' / lock_name).read_text())
        for rel in lock['source_sha256_canonical_lf']:
            if rel not in copied:
                copy(ROOT / rel)
    omitted = [record for record in omitted if record['path'] not in copied]
    for name in ('REPORT.md', 'CLAIMS_FROM_RESULTS.md'):
        copy(ROOT / name, 'provenance/current_project_' + name)
    for p in (ROOT / '.aris/traces/result-to-claim/2026-11-01_b2').iterdir():
        if p.is_file():
            copy(p, 'provenance/aris_b2/' + p.name)
    for name in ('b2_completion_stop_receipt_20261101.json', 'b2_terminal_backup_receipt_20261101.json',
                 'b2_deploy_26feef1_receipt.json', 'b2_manuscript_before_20261031.json',
                 'b1c_r3_terminal_backup_receipt_20261031.json'):
        copy(ROOT / 'provenance/qa' / name, 'provenance/' + name)
    source = {'scientific_method': 'arc2_global_tangent2_r1',
              'project_snapshot_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'b2_pre_run_commit': '26feef1026bea610ec7f53d581c3c9064949d004',
              'packaging_created_utc': datetime.now(timezone.utc).isoformat(),
              'copied_files': copied,
              'omitted_scope': 'Large full-corpus vectors/weights are absent from compact B1c/B2 evidence by their original manifests. B1-G sampled-vector replay is not self-contained here; all scored outcomes, diagnostic tables and prior verification report are present. This is an offline review/reproduction release, not a ready-to-launch physical H100 deployment.',
              'additional_package_omissions': omitted,
              'source_project_unchanged': True, 'manuscript_included_or_modified': False}
    emit('provenance/PACKAGE_SCOPE.json', json.dumps(source, indent=2) + '\n')
    print(json.dumps({'status': 'SOURCE_AND_RESULTS_COPIED', 'destination': str(DEST),
                      'files': len(copied), 'omitted_G_files': len(omitted)}, indent=2))


def manifest():
    files = {}
    scope = json.loads((DEST / 'provenance/PACKAGE_SCOPE.json').read_text())
    origins = scope['copied_files']
    for p in DEST.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(DEST).as_posix()
        if rel in ('RELEASE_MANIFEST.json', 'CHECKSUMS.sha256') or rel.startswith(('checks/', '.venv/')) or '__pycache__' in p.parts:
            continue
        files[rel] = {'bytes': p.stat().st_size, 'sha256': sha(p),
                      'origin': origins.get(rel, 'Release documentation or packaging helper; not a new scientific result')}
    value = {'release': 'ARC2-Global supervisor review, 1 November 2026',
             'created_utc': datetime.now(timezone.utc).isoformat(),
             'scientific_method_frozen': 'arc2_global_tangent2_r1',
             'files': files, 'file_count': len(files), 'bytes': sum(x['bytes'] for x in files.values()),
             'excluded_from_manifest': ['RELEASE_MANIFEST.json (self)', 'CHECKSUMS.sha256 (derived)',
                                        'checks/** (regenerable validation outputs)', '.venv/**', '**/__pycache__/**'],
             'scope': scope['omitted_scope']}
    emit('RELEASE_MANIFEST.json', json.dumps(value, indent=2) + '\n')
    checksums = [f"{s['sha256']}  {r}" for r, s in sorted(files.items())]
    checksums.append(sha(DEST / 'RELEASE_MANIFEST.json') + '  RELEASE_MANIFEST.json')
    emit('CHECKSUMS.sha256', '\n'.join(checksums) + '\n')
    print(json.dumps({'status': 'MANIFEST_WRITTEN', 'files': len(files), 'bytes': value['bytes']}))


def archive(archive_path=None):
    import zipfile
    path = Path(archive_path).resolve() if archive_path else DEST.parent / 'DASFAA-2027-paper-release-20261101.zip'
    if path.parent != DEST.parent or path.suffix != '.zip':
        raise ValueError('Release ZIP must be an explicitly named file beside the release folder')
    if path.exists():
        raise FileExistsError('Preserve existing release archive')
    manifest_data = json.loads((DEST / 'RELEASE_MANIFEST.json').read_text())
    paths = [p for p in DEST.rglob('*') if p.is_file() and '__pycache__' not in p.parts
             and '.venv' not in p.parts]
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(paths):
            z.write(p, (Path(DEST.name) / p.relative_to(DEST)).as_posix())
    with zipfile.ZipFile(path) as z:
        for rel, spec in manifest_data['files'].items():
            payload = z.read(DEST.name + '/' + rel)
            if len(payload) != spec['bytes'] or hashlib.sha256(payload).hexdigest() != spec['sha256']:
                raise ValueError('Archive content verification failed: ' + rel)
    digest = sha(path)
    path.with_suffix('.zip.sha256').write_text(digest + '  ' + path.name + '\n', encoding='utf-8', newline='\n')
    receipt = {'status': 'ARCHIVE_CONTENTS_VERIFIED', 'archive': str(path), 'bytes': path.stat().st_size,
               'sha256': digest, 'manifest_sha256': sha(DEST / 'RELEASE_MANIFEST.json'),
               'manifested_files_verified_inside_archive': len(manifest_data['files']),
               'archive_file_count': len(paths), 'created_utc': datetime.now(timezone.utc).isoformat()}
    path.with_suffix('.zip.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest-only', action='store_true')
    ap.add_argument('--archive-only', action='store_true')
    ap.add_argument('--archive-path', type=Path)
    args = ap.parse_args()
    if args.manifest_only and args.archive_only:
        ap.error('Choose one operation')
    archive(args.archive_path) if args.archive_only else manifest() if args.manifest_only else build()
