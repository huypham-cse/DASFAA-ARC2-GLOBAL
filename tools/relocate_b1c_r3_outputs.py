"""Operator-only output relocation; frozen code/inputs/runtime stay on NFS.

Default prints the procedure. --execute pauses only the two owned controllers,
lets their existing GPU worker exit, copies/verifies opaque output bytes, keeps
the old tree, switches the original output alias, and resumes the same PIDs.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time

BASE = Path('/network-volume/arc2_recovery_20261030')
CODE = BASE / 'code_61f7317_b1c_r3'
NAME = 'mini_r3b_20261030t0347'
SOURCE = CODE / 'results' / ('b1c_r3_full_' + NAME)
TARGET = Path('/home/jovyan/arc2_b1c_r3_outputs_20261030') / SOURCE.name
PRESERVED = BASE / 'preserved_before_output_relocation_20261030' / SOURCE.name
COMMIT = '61f73171b1869a186648aadd88f1b6f81a61376b'
LOCK_SHA = 'f567a4b6267baef3c59de1aca750d19ba3479d228109f7d098fd45d26586830d'


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def proc(pid):
    base = Path('/proc') / str(pid)
    try:
        fields = (base / 'stat').read_text().rsplit(')', 1)[1].split()
        argv = (base / 'cmdline').read_bytes().split(b'\0')
        return {'pid': pid, 'state': fields[0], 'ppid': int(fields[1]),
                'start_ticks': int(fields[19]), 'argv': [x.decode() for x in argv if x]}
    except FileNotFoundError:
        return None


def stamp(path):
    s = path.stat()
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns]


def same_process(old):
    current = proc(old['pid'])
    return current and current['start_ticks'] == old['start_ticks']


def immutable_stamps(lock):
    allocation = json.loads((CODE / 'configs/b1c_r3_acquisition.json').read_text())
    paths = {Path(row['restored_path']) for row in allocation['sources']}
    paths.update(CODE / p for p in lock['source_sha256_canonical_lf'])
    paths.update(Path(lock['upstream']) / p for p in lock['upstream_raw_sha256'])
    paths.add(CODE / 'configs/b1c_r3_lock.json')
    return {str(p): stamp(p) for p in sorted(paths)}


def copy_verified_tree(source, target, progress):
    """Source writers have exited/paused; reject mutation and verify every copy."""
    target.mkdir(parents=True, exist_ok=False)
    manifest = {}
    for p in sorted(source.rglob('*')):
        relative = p.relative_to(source)
        destination = target / relative
        if p.is_symlink():
            raise ValueError('Unexpected symlink inside raw run: ' + str(relative))
        if p.is_dir():
            destination.mkdir(exist_ok=True)
            continue
        if not p.is_file():
            raise ValueError('Unexpected output file type')
        before = stamp(p)
        before_mode = p.stat().st_mode
        h, count = hashlib.sha256(), 0
        temporary = destination.with_name(destination.name + '.relocation.part')
        with p.open('rb') as incoming, temporary.open('xb') as outgoing:
            for block in iter(lambda: incoming.read(8 * 1024 * 1024), b''):
                outgoing.write(block); h.update(block); count += len(block)
            outgoing.flush(); os.fsync(outgoing.fileno())
        if stamp(p) != before or count != before[2] or sha(temporary) != h.hexdigest():
            raise ValueError('Source changed or output copy failed: ' + str(relative))
        shutil.copystat(p, temporary)
        if (temporary.stat().st_mode != before_mode or temporary.stat().st_mtime_ns != before[3]
                or p.stat().st_mode != before_mode):
            raise ValueError('Output copy mode/mtime differs: ' + str(relative))
        temporary.rename(destination)
        manifest[relative.as_posix()] = {'sha256': h.hexdigest(), 'bytes': count, 'mode': before_mode, 'source_stat': before}
        if len(manifest) % 25 == 0:
            progress(len(manifest), sum(x['bytes'] for x in manifest.values()))
    expected = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
    if expected != set(manifest):
        raise ValueError('Output tree changed during relocation')
    for relative, row in manifest.items():
        if stamp(source / relative) != row['source_stat']:
            raise ValueError('Source writer remained active')
    return manifest


def execute():
    attempt = BASE / ('storage_relocation_' + str(time.time_ns()))
    attempt.mkdir(exist_ok=False)
    ledger = {'status': 'PREFLIGHT', 'started_utc': now(), 'source': str(SOURCE),
              'target': str(TARGET), 'preserved': str(PRESERVED), 'events': [],
              'scientific_code_commit': COMMIT, 'scientific_lock_sha256': LOCK_SHA,
              'numeric_changes': False, 'new_fits_or_rankings': False}
    paused = []
    switched = False
    def record(status, **extra):
        ledger.update(status=status, **extra)
        ledger['events'].append({'utc': now(), 'status': status})
        temporary = attempt / 'ledger.writing'
        temporary.write_text(json.dumps(ledger, indent=2) + '\n')
        temporary.replace(attempt / 'ledger.json')
        print(json.dumps({'status': status, **extra}), flush=True)
    try:
        if SOURCE.is_symlink() or not SOURCE.resolve().is_relative_to(BASE.resolve()):
            raise ValueError('Source must still be the original owned NFS output tree')
        if TARGET.exists() or TARGET.is_symlink() or PRESERVED.exists():
            raise FileExistsError('Preserve every existing relocation target/snapshot')
        if TARGET.parent.parent.resolve() != Path('/home/jovyan').resolve():
            raise ValueError('Unexpected destination scope')
        if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=CODE, text=True).strip() != COMMIT:
            raise ValueError('Running deployment Git identity changed')
        if sha(CODE / 'configs/b1c_r3_lock.json') != LOCK_SHA:
            raise ValueError('Scientific lock changed')
        lock = json.loads((CODE / 'configs/b1c_r3_lock.json').read_text())
        original_sources = immutable_stamps(lock)
        campaign, controller = proc(2777), proc(2997)
        for row, script in [(campaign, 'b1c_r3_campaign.py'), (controller, 'b1c_r3_stage.py')]:
            if not row or str(CODE / 'ops' / script) not in row['argv']:
                raise ValueError('Owned controller identity differs')
        if controller['ppid'] != campaign['pid'] or str(SOURCE) not in controller['argv']:
            raise ValueError('Unexpected owned process relationship/output')
        children = [proc(int(p.name)) for p in Path('/proc').iterdir() if p.name.isdigit()]
        workers = [p for p in children if p and p['ppid'] == controller['pid']
                   and str(CODE / 'ops/b1p_neural_worker.py') in p['argv']]
        if len(workers) != 1:
            raise ValueError('Require exactly the current owned neural worker at its controller wait')
        worker = workers[0]
        record('PAUSING_OWN_CONTROLLERS', controllers=[campaign, controller], worker=worker)
        for row in (controller, campaign):
            os.kill(row['pid'], signal.SIGSTOP); paused.append(row)
            while same_process(row) and proc(row['pid'])['state'] not in ('T', 't'):
                time.sleep(.05)
            if not same_process(row):
                raise RuntimeError('Owned controller exited during pause')
        # Freeze first, then capture the actual child: the controller could
        # have reaped the initially observed worker and spawned its successor.
        children = [proc(int(p.name)) for p in Path('/proc').iterdir() if p.name.isdigit()]
        live = [p for p in children if p and p['ppid'] == controller['pid'] and p['state'] != 'Z']
        workers = [p for p in live if str(CODE / 'ops/b1p_neural_worker.py') in p['argv']]
        if len(workers) != 1 or len(live) != 1:
            raise ValueError('Require exactly one actual owned neural child after controllers stop')
        worker = workers[0]
        request_path = Path(worker['argv'][worker['argv'].index('--request') + 1]).resolve()
        if not request_path.is_relative_to(SOURCE.resolve()):
            raise ValueError('Worker request is outside the active output tree')
        request = json.loads(request_path.read_text())
        if (request['code_commit'] != COMMIT or request['mode'] != 'full'
                or not Path(request['output']).resolve().is_relative_to(SOURCE.resolve())
                or Path(request['lockpath']).resolve() != (CODE / 'configs/b1c_r3_lock.json').resolve()):
            raise ValueError('Actual worker request differs from owned frozen run')
        ledger['worker'] = worker
        record('WAITING_FOR_EXISTING_WORKER_TO_CLOSE', pause_started_utc=now())
        while same_process(worker) and proc(worker['pid'])['state'] != 'Z':
            time.sleep(5)
        children = [proc(int(p.name)) for p in Path('/proc').iterdir() if p.name.isdigit()]
        if any(p and p['ppid'] == controller['pid'] and p['state'] != 'Z' for p in children):
            raise RuntimeError('An owned child is still active before output copy')
        if any(not same_process(p) or proc(p['pid'])['state'] not in ('T', 't') for p in paused):
            raise RuntimeError('Controller pause changed before output copy')
        # A zombie has no open descriptors. Controller keeps child log FDs open
        # until wait() returns, but cannot write them while stopped.
        forbidden = []
        paused_ids = {row['pid'] for row in paused}
        allowed_logs = {str(request_path.parent / name) for name in ('stdout.log', 'stderr.log')}
        for process in Path('/proc').iterdir():
            if not process.name.isdigit():
                continue
            try:
                descriptors = list((process / 'fd').iterdir())
            except FileNotFoundError:
                continue
            for fd in descriptors:
                try:
                    target = os.readlink(fd)
                    info = process / 'fdinfo' / fd.name
                    flags = next(int(s.split()[1], 8) for s in info.read_text().splitlines() if s.startswith('flags:'))
                except FileNotFoundError:
                    continue
                if flags & os.O_ACCMODE and target.startswith(str(SOURCE) + '/'):
                    if int(process.name) not in paused_ids or target not in allowed_logs:
                        forbidden.append({'pid': int(process.name), 'fd': str(fd), 'target': target})
        if forbidden:
            raise RuntimeError('Controller paused with an unexpected output descriptor: ' + repr(forbidden))
        record('COPYING_VERIFIED_OUTPUTS', worker_closed_utc=now())
        manifest = copy_verified_tree(SOURCE, TARGET, lambda n, b: record('COPYING_VERIFIED_OUTPUTS', files=n, bytes=b))
        (attempt / 'file_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        if immutable_stamps(lock) != original_sources:
            raise ValueError('Immutable source device/inode/bytes/mtime changed')
        PRESERVED.parent.mkdir(exist_ok=True)
        SOURCE.rename(PRESERVED)
        try:
            SOURCE.symlink_to(TARGET, target_is_directory=True)
            switched = True
        except BaseException:
            PRESERVED.rename(SOURCE)
            raise
        if SOURCE.resolve() != TARGET.resolve() or immutable_stamps(lock) != original_sources:
            raise ValueError('Alias/source stamp verification failed')
        if len([p for p in SOURCE.rglob('*') if p.is_file()]) != len(manifest):
            raise ValueError('Relocated root traversal differs')
        record('OUTPUTS_RELOCATED_VERIFIED', files=len(manifest), bytes=sum(x['bytes'] for x in manifest.values()),
               pause_ended_utc=now(), original_source_stamps_unchanged=True,
               raw_snapshot_preserved=True, resource_pause='Include operator pause in wall elapsed; no isolated cost/SLO claim')
    except BaseException as error:
        if switched and SOURCE.is_symlink() and SOURCE.resolve() == TARGET.resolve() and PRESERVED.is_dir():
            SOURCE.unlink()  # Only the alias created above; both raw trees survive.
            PRESERVED.rename(SOURCE)
        record('FAILED_PRESERVED', error=repr(error))
        raise
    finally:
        for row in paused:
            if same_process(row):
                os.kill(row['pid'], signal.SIGCONT)
        record(ledger['status'], controllers_resumed_utc=now())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if args.execute:
        execute()
    else:
        print(json.dumps({'source': str(SOURCE), 'target': str(TARGET), 'preserved': str(PRESERVED),
                          'procedure': 'Pause owned controllers; let worker close; copy/hash outputs only; preserve old tree; switch output alias; resume same PIDs'}))
