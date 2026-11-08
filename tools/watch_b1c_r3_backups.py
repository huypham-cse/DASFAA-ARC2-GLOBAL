"""Operator-only incremental SSH backup while this laptop is awake/connected.

No SFTP, scientific execution, label parsing, or credential persistence. Run in
an interactive terminal; Ctrl-C stops. A failed transfer is preserved as .part.
"""
import argparse
from datetime import datetime, timezone
import getpass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shlex
import sys
import time
import traceback

PROJECT = '/network-volume/arc2_recovery_20261030/code_61f7317_b1c_r3'
CAMPAIGN = 'mini_r3b_20261030t0347'
RELOCATED_FULL = '/home/jovyan/arc2_b1c_r3_outputs_20261030/b1c_r3_full_' + CAMPAIGN
HOST, PORT = '103.73.232.201', 62161
CHUNK_BYTES = 128 * 1024 * 1024
CONNECTION_BYTES = 384 * 1024 * 1024
REMOTE = r'''
import hashlib,json,pathlib,sys
project=pathlib.Path(sys.argv[1]).resolve(); name=sys.argv[2]
relocated=pathlib.Path(sys.argv[3]).resolve()
previous=json.load(sys.stdin); files=[]; groups=[]; terminal=False; failed=False
def read(path,default):
    return json.loads(path.read_text()) if path.exists() else default
registry=read(project/'configs/b1c_r3_sources.json',{'groups':[]})
full=project/'results'/('b1c_r3_full_'+name)
cells=read(full/'cells_pre_qrels.json',[])
done={c['case_id'] for c in cells}
for g in registry['groups']:
    if {c['case_id'] for c in g['cases']} <= done: groups.append(g['group_id'])
schedule=project/'results'/('b1c_r3_schedule_'+name)
status=read(schedule/'metadata.json',{}).get('status')
terminal=bool(status and status!='RUNNING'); failed=terminal and status!='B1C_R3_SCORED_STOP_FOR_D1'
for kind in ('full','smoke','schedule'):
    root=project/'results'/('b1c_r3_'+kind+'_'+name)
    for p in sorted(root.rglob('*')) if root.exists() else []:
        if not p.is_file() or p.is_symlink(): continue
        if not (p.resolve().is_relative_to(project) or p.resolve().is_relative_to(relocated)): raise ValueError('Escaping remote file')
        rel=p.relative_to(project).as_posix(); st=p.stat(); stamp=[st.st_size,st.st_mtime_ns]
        old=previous.get(rel,{}); h=hashlib.sha256()
        if old.get('stat')==stamp: digest=old['sha256']
        else:
            with p.open('rb') as f:
                for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
            digest=h.hexdigest()
        after=p.stat()
        if [after.st_size,after.st_mtime_ns]!=stamp: continue
        complete=any('/groups/'+g+'/' in '/'+rel or '/cpu/'+g.split('_')[0]+'_'+g+'/' in '/'+rel
                     or '/neural/'+g.split('_')[0]+'_'+g+'/' in '/'+rel for g in groups)
        ranked=kind=='full' and p.parent.name=='rankings' and any(p.stem.endswith(c) for c in done)
        inputs=kind=='full' and '/inputs/' in rel
        mutable=p.name.endswith(('.log','.jsonl')) or p.name in ('metadata.json','progress.json','cells_pre_qrels.json','parity_receipts.json','fit_receipts.json','fresh_fiqa_historical_comparisons.json')
        files.append({'path':rel,'stat':stamp,'sha256':digest,'immutable':(complete or ranked or inputs or terminal) and not mutable,'priority':0 if complete or ranked else 1})
print(json.dumps({'files':files,'completed_groups':groups,'campaign_status':status,'terminal':terminal,'failed':failed}))
'''
STREAM = r'''
import pathlib,sys
p=pathlib.Path(sys.argv[1]).resolve(); root=pathlib.Path(sys.argv[2]).resolve()
relocated=pathlib.Path(sys.argv[3]).resolve()
if not (p.is_relative_to(root) or p.is_relative_to(relocated)): raise ValueError('Escaping download')
offset,remaining=int(sys.argv[4]),int(sys.argv[5])
if offset<0 or remaining<0 or offset+remaining>p.stat().st_size: raise ValueError('Invalid byte range')
with p.open('rb') as f:
    f.seek(offset)
    while remaining:
        b=f.read(min(1024*1024,remaining))
        if not b: raise ValueError('File shortened during transfer')
        sys.stdout.buffer.write(b); remaining-=len(b)
'''


def stamp():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def long_path_root(path):
    path = Path(path).resolve()
    if os.name == 'nt' and not str(path).startswith('\\\\?\\'):
        value = str(path)
        path = Path('\\\\?\\UNC\\' + value[2:] if value.startswith('\\\\') else '\\\\?\\' + value)
    return path


def inside(root, relative):
    # Older Windows receipts stored native separators. Accept only relative
    # local paths; keep drive, UNC, traversal and resolved-root guards intact.
    windows = PureWindowsPath(relative)
    if windows.drive or windows.root:
        raise ValueError('Invalid backup relative path')
    relative = relative.replace('\\', '/')
    parts = PurePosixPath(relative).parts
    if not parts or PurePosixPath(relative).is_absolute() or any(p in ('.', '..') or '\\' in p or ':' in p for p in parts):
        raise ValueError('Invalid backup relative path')
    path = (root / Path(*parts)).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Escaping backup path')
    return path


def copy_verified(stream, destination, row):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.stat().st_size != row['stat'][0] or digest(destination) != row['sha256']:
            raise FileExistsError('Preserve conflicting local bytes: ' + str(destination))
        return
    partial = destination.with_name(destination.name + '.part-' + stamp())
    h, count = hashlib.sha256(), 0
    with partial.open('xb') as target:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            target.write(block); h.update(block); count += len(block)
        target.flush(); os.fsync(target.fileno())
    if count != row['stat'][0] or h.hexdigest() != row['sha256']:
        raise ValueError('Remote changed/incomplete transfer; partial preserved: ' + str(partial))
    if destination.exists():
        raise FileExistsError('Concurrent backup conflict; partial preserved')
    partial.rename(destination)


def connect(passphrase):
    if os.environ.get('ARC2_SSH_DEPS'):
        sys.path.insert(0, os.environ['ARC2_SSH_DEPS'])
    import paramiko
    client = paramiko.SSHClient()
    client.load_host_keys(str(Path.home() / '.ssh/known_hosts'))
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(HOST, port=PORT, username='root', key_filename=str(Path.home() / '.ssh/lxbach.key'),
                   passphrase=passphrase, look_for_keys=False, allow_agent=False, timeout=20,
                   banner_timeout=30, auth_timeout=30, channel_timeout=300)
    client.get_transport().set_keepalive(30)
    return client


def inventory(client, previous):
    inp, out, err = client.exec_command(shlex.join(['python3', '-c', REMOTE, PROJECT, CAMPAIGN, RELOCATED_FULL]), timeout=600)
    inp.write(json.dumps(previous).encode()); inp.channel.shutdown_write()
    data, error = out.read(), err.read()
    if out.channel.recv_exit_status():
        raise RuntimeError('Remote inventory failed: ' + error.decode(errors='replace'))
    return json.loads(data)


def download_ranges(client, passphrase, relative, destination, row, transferred):
    """Keep transport sessions below the installed 512MiB rekey threshold.

    Bounds apply only to backup network I/O, never the scientific process.
    Whole-file SHA256 remains the acceptance criterion across all ranges.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + '.part-' + stamp())
    h, offset = hashlib.sha256(), 0
    try:
        with partial.open('xb') as target:
            while offset < row['stat'][0]:
                amount = min(CHUNK_BYTES, row['stat'][0] - offset)
                if transferred + amount > CONNECTION_BYTES:
                    client.close(); client = connect(passphrase); transferred = 0
                argv = ['python3', '-c', STREAM, PROJECT + '/' + relative, PROJECT,
                        RELOCATED_FULL, str(offset), str(amount)]
                inp, out, err = client.exec_command(shlex.join(argv), timeout=300)
                inp.channel.shutdown_write()
                received = 0
                try:
                    while received < amount:
                        block = out.read(min(1024 * 1024, amount - received))
                        if not block: break
                        target.write(block); h.update(block); received += len(block)
                    error = err.read()
                    if out.channel.recv_exit_status() or received != amount:
                        raise RuntimeError('Incomplete backup range: ' + error.decode(errors='replace'))
                finally:
                    out.channel.close()
                offset += received; transferred += received
            target.flush(); os.fsync(target.fileno())
        if offset != row['stat'][0] or h.hexdigest() != row['sha256']:
            raise ValueError('Whole-file backup hash differs; partial preserved: ' + str(partial))
        if destination.exists():
            raise FileExistsError('Preserve concurrent local backup: ' + str(destination))
        partial.rename(destination)
        return client, transferred
    except BaseException:
        client.close()
        raise


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--local-root', type=Path, default=Path('D:/ARC2-B1c-R3-backup-20261030'))
    ap.add_argument('--poll-seconds', type=float, default=60)
    ap.add_argument('--max-consecutive-errors', type=int, default=5)
    args = ap.parse_args()
    if args.poll_seconds <= 0 or args.max_consecutive_errors < 1:
        ap.error('Poll interval and consecutive error limit must be positive')
    root = long_path_root(args.local_root); root.mkdir(parents=True, exist_ok=True)
    passphrase = getpass.getpass('SSH key passphrase (memory only): ')
    client, previous, coverage, errors, transferred = None, {}, {}, 0, 0
    state_path = root / 'operator_state.json'
    if state_path.exists():
        saved = json.loads(state_path.read_text(encoding='utf-8'))
        if saved['remote_project'] != PROJECT or saved['campaign'] != CAMPAIGN:
            raise ValueError('Backup state belongs to a different campaign')
        previous, coverage = saved['previous'], saved['coverage']
    def save_state(current):
        temporary = root / 'operator_state.writing'
        with temporary.open('w', encoding='utf-8') as stream:
            json.dump({'remote_project': PROJECT, 'campaign': CAMPAIGN,
                       'previous': current, 'coverage': coverage}, stream)
        temporary.replace(state_path)
    def event(**row):
        row['utc'] = stamp()
        with (root / 'operator_events.jsonl').open('a', encoding='utf-8') as log:
            log.write(json.dumps(row) + '\n')
        print(json.dumps(row), flush=True)
    try:
        while True:
            try:
                if client is None: client = connect(passphrase); transferred = 0
                current = inventory(client, previous); now = stamp(); skipped = 0
                current_rows = {r['path']: r for r in current['files']}
                save_state(current_rows)
                for row in sorted(current['files'], key=lambda r: (r['priority'], r['path'])):
                    rel = row['path']; old = previous.get(rel)
                    if old is None or (old['stat'], old['sha256']) != (row['stat'], row['sha256']):
                        skipped += 1; continue
                    canonical = row['immutable']
                    prior = coverage.get(rel)
                    if (prior and prior['sha256'] == row['sha256'] and prior['canonical'] == canonical
                            and inside(root, prior['local']).is_file()
                            and inside(root, prior['local']).stat().st_size == row['stat'][0]):
                        continue
                    local = inside(root, ('artifacts/' if canonical else 'snapshots/' + now + '/') + rel)
                    if local.exists():
                        if local.stat().st_size != row['stat'][0] or digest(local) != row['sha256']:
                            raise FileExistsError('Preserve conflicting local bytes: ' + str(local))
                    else:
                        client, transferred = download_ranges(client, passphrase, rel, local, row, transferred)
                    coverage[rel] = {'sha256': row['sha256'], 'bytes': row['stat'][0], 'local': local.relative_to(root).as_posix(), 'canonical': canonical}
                    if len(coverage) % 25 == 0:
                        save_state(current_rows)
                        event(status='FILES_COPIED_VERIFIED', files=len(coverage), bytes=sum(x['bytes'] for x in coverage.values()))
                previous = {r['path']: r for r in current['files']}
                save_state(previous)
                pending = [r['path'] for r in current['files'] if coverage.get(r['path'], {}).get('sha256') != r['sha256']]
                manifest = {'utc': now, 'remote_project': PROJECT, 'campaign': CAMPAIGN, 'status': current['campaign_status'],
                            'completed_groups': current['completed_groups'], 'coverage': coverage, 'pending': pending,
                            'all_current_files_verified': not pending, 'laptop_must_remain_awake_connected': True}
                with (root / ('coverage_' + now + '.json')).open('x', encoding='utf-8') as f: json.dump(manifest, f, indent=2)
                event(status='POLL_VERIFIED', groups=len(current['completed_groups']), files=len(coverage), pending=len(pending), unstable=skipped)
                errors = 0
                if current['terminal'] and not pending and not skipped:
                    event(status='FAILED_CAMPAIGN_BACKED_UP' if current['failed'] else 'COMPLETE_CAMPAIGN_BACKED_UP')
                    return 2 if current['failed'] else 0
            except Exception as exc:
                errors += 1; event(status='BACKUP_ERROR', consecutive_errors=errors, error=repr(exc), traceback=traceback.format_exc())
                if client is not None: client.close(); client = None
                if errors >= args.max_consecutive_errors: return 1
            time.sleep(args.poll_seconds)
    except KeyboardInterrupt:
        event(status='OPERATOR_STOPPED'); return 130
    finally:
        if client is not None: client.close()


if __name__ == '__main__':
    raise SystemExit(main())
