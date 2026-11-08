"""Opaque, resumable SSH backup; never interprets scientific labels or results.

No credentials are written. Remote files remain unchanged. Each small archive
contains a source SHA256 manifest and is independently checked after download.
"""
import argparse
import concurrent.futures
import getpass
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import sys
import tarfile
import threading
import time
import uuid

if os.environ.get('ARC2_SSH_DEPS'):
    sys.path.insert(0, os.environ['ARC2_SSH_DEPS'])
import paramiko

ROOTS = ['/root/arc2_global_paper_20261025', '/root/arc2_p3h_20261020']
HOSTS = {'main': ('103.73.232.225', 52194), 'mini': ('103.73.232.201', 62161)}
MANIFEST = '__ARC2_BACKUP__/manifest.json'
LOCK = threading.Lock()

SCAN = r'''
import json,os,stat,sys
from pathlib import Path
roots=json.load(sys.stdin); rows=[]; errors=[]
for root in roots:
 if not Path(root).is_dir():
  errors.append({'path':root,'error':'MISSING_ROOT'});continue
 def visit(path):
  try:
   s=path.lstat()
   kind='file' if stat.S_ISREG(s.st_mode) else 'link' if stat.S_ISLNK(s.st_mode) else 'dir' if stat.S_ISDIR(s.st_mode) else 'special'
   row={'path':str(path),'kind':kind,'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'mode':s.st_mode}
   if kind=='link':row['link_target']=os.readlink(path)
   rows.append(row)
   if kind=='dir':
    for child in sorted(path.iterdir()):visit(child)
  except Exception as e:errors.append({'path':str(path),'error':type(e).__name__+': '+str(e)})
 visit(Path(root))
print(json.dumps({'roots':roots,'entries':rows,'errors':errors,'scanned_unix':__import__('time').time()}))
'''

STREAM = r'''
import gzip,hashlib,io,json,os,stat,sys,tarfile
rows=json.load(sys.stdin); records=[]
class Sink:
 def __init__(self):self.sha=hashlib.sha256();self.count=0
 def write(self,b):self.sha.update(b);self.count+=len(b);return sys.stdout.buffer.write(b)
 def flush(self):sys.stdout.buffer.flush()
class Reader:
 def __init__(self,f):self.f=f;self.sha=hashlib.sha256();self.count=0
 def read(self,n):
  b=self.f.read(n);self.sha.update(b);self.count+=len(b);return b
def unchanged(row):
 s=os.lstat(row['path'])
 if (s.st_size,s.st_mtime_ns,s.st_mode)!=(row['bytes'],row['mtime_ns'],row['mode']):
  raise RuntimeError('SOURCE_CHANGED:'+row['path'])
sink=Sink()
with gzip.GzipFile(fileobj=sink,mode='wb',compresslevel=1,mtime=0) as compressed:
 with tarfile.open(fileobj=compressed,mode='w|',format=tarfile.PAX_FORMAT) as tar:
  for row in rows:
   path=row['path']
   if not any(path==r or path.startswith(r+'/') for r in ['/root/arc2_global_paper_20261025','/root/arc2_p3h_20261020']):raise ValueError('OUTSIDE_ROOT')
   unchanged(row)
   # Preserve each ordinary file independently, including source hard links.
   tar.inodes.clear()
   info=tar.gettarinfo(path,arcname=path.lstrip('/'))
   record=dict(row)
   if row['kind']=='file':
    with open(path,'rb') as f:
     reader=Reader(f);tar.addfile(info,reader)
     if reader.count!=row['bytes']:raise RuntimeError('SHORT_SOURCE:'+path)
     record['sha256']=reader.sha.hexdigest()
   elif row['kind'] in ['dir','link']:tar.addfile(info)
   else:raise ValueError('SPECIAL_FILE:'+path)
   unchanged(row);records.append(record)
  data=json.dumps({'schema':'arc2-opaque-backup-v1','entries':records},sort_keys=True).encode()
  info=tarfile.TarInfo('__ARC2_BACKUP__/manifest.json');info.size=len(data)
  tar.addfile(info,io.BytesIO(data))
sink.flush()
sys.stderr.write(json.dumps({'status':'SOURCE_STREAM_COMPLETE','archive_sha256':sink.sha.hexdigest(),'archive_bytes':sink.count,'manifest_sha256':hashlib.sha256(data).hexdigest(),'entries':len(records)}))
'''


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def write_json(path, value):
    temporary = path.with_name(path.name + '.tmp-' + uuid.uuid4().hex)
    temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
    os.replace(temporary, path)


def emit(host, event, **fields):
    with LOCK:
        print(json.dumps({'host': host, 'event': event, **fields}), flush=True)


def connect(host, password, key):
    address, port = HOSTS[host]
    c = paramiko.SSHClient()
    c.load_host_keys(str(Path.home() / '.ssh/known_hosts'))
    c.set_missing_host_key_policy(paramiko.RejectPolicy())
    c.connect(address, port=port, username='root', key_filename=str(key),
              passphrase=password, look_for_keys=False, allow_agent=False, timeout=25)
    c.get_transport().set_keepalive(20)
    return c


def remote(c, code, data):
    inp, out, err = c.exec_command(shlex.join(['python3', '-u', '-c', code]))
    inp.write(json.dumps(data).encode())
    inp.channel.shutdown_write()
    return out, err


def verify_archive(path, expected_rows, source_receipt):
    observed = {}
    raw_manifest = None
    with tarfile.open(path, mode='r|gz') as archive:
        for member in archive:
            if member.name == MANIFEST:
                if raw_manifest is not None:
                    raise ValueError('Duplicate backup manifest')
                raw_manifest = archive.extractfile(member).read()
                continue
            name = '/' + member.name.rstrip('/')
            if name in observed:
                raise ValueError('Duplicate archive member: ' + name)
            item = {'kind': 'file' if member.isfile() else 'dir' if member.isdir() else 'link' if member.issym() else 'unsupported'}
            if member.isfile():
                h = hashlib.sha256()
                total = 0
                f = archive.extractfile(member)
                for b in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(b)
                    total += len(b)
                item.update(bytes=total, sha256=h.hexdigest())
            elif member.issym():
                item['link_target'] = member.linkname
            observed[name] = item
    if raw_manifest is None or hashlib.sha256(raw_manifest).hexdigest() != source_receipt['manifest_sha256']:
        raise ValueError('Manifest hash mismatch')
    entries = json.loads(raw_manifest)['entries']
    expected = {r['path']: r for r in expected_rows}
    if {r['path']: {k: v for k, v in r.items() if k != 'sha256'} for r in entries} != expected:
        raise ValueError('Manifest differs from initial source inventory')
    if set(observed) != set(expected):
        raise ValueError('Archive member set mismatch')
    for row in entries:
        actual = observed[row['path']]
        for key in ['kind'] + (['bytes', 'sha256'] if row['kind'] == 'file' else ['link_target'] if row['kind'] == 'link' else []):
            if actual[key] != row[key]:
                raise ValueError('Archive verification failed: ' + row['path'])
    return {'status': 'BACKUP_VERIFIED', 'entries': len(entries),
            'source_bytes': sum(r['bytes'] for r in entries if r['kind'] == 'file'),
            'manifest_sha256': source_receipt['manifest_sha256']}


def worker(host, password, args):
    folder = args.destination / host
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'archives').mkdir(exist_ok=True)
    c = connect(host, password, args.key)
    emit(host, 'CONNECTED')
    plan_path = folder / 'inventory.json'
    try:
        if plan_path.exists():
            inventory = json.loads(plan_path.read_text(encoding='utf-8'))
        else:
            out, err = remote(c, SCAN, ROOTS)
            data = out.read()
            errors = err.read().decode()
            if out.channel.recv_exit_status() != 0:
                raise RuntimeError(errors)
            inventory = json.loads(data)
            write_json(plan_path, inventory)
        if inventory['errors']:
            raise RuntimeError('Source inventory has errors; preserved in inventory.json')
        prior_path = Path('provenance/qa/server_storage_' + host + '_20261028.json')
        prior = json.loads(prior_path.read_text(encoding='utf-8'))
        current = {r['path']: r for r in inventory['entries']}
        missing = [r for r in prior['large_project_files'] if r['path'] not in current]
        changed = [r for r in prior['large_project_files'] if r['path'] in current and current[r['path']]['bytes'] != r['bytes']]
        write_json(folder / 'prior_inventory_comparison.json', {
            'scope': 'Existence and size only for previously inventoried large current-project files; cannot determine pre-inventory deletion',
            'checked': len(prior['large_project_files']), 'missing': missing, 'size_changed': changed})
        emit(host, 'INVENTORY', entries=len(current), source_bytes=sum(r['bytes'] for r in current.values() if r['kind'] == 'file'), previously_listed_missing=len(missing), previously_listed_size_changed=len(changed))
        # Current project first; deterministic small chunks allow interrupted work to resume.
        rows = sorted(inventory['entries'], key=lambda r: (not r['path'].startswith(ROOTS[0]), r['bytes'] if r['kind'] == 'file' else 0, r['path']))
        chunks = []
        batch, size = [], 0
        for row in rows:
            if row['kind'] == 'special':
                raise ValueError('Special file requires separate preservation: ' + row['path'])
            n = row['bytes'] if row['kind'] == 'file' else 0
            if batch and size + n > 512 * 1024 * 1024:
                chunks.append(batch)
                batch, size = [], 0
            batch.append(row)
            size += n
        if batch:
            chunks.append(batch)
        completed = 0
        source_completed = 0
        status_path = folder / 'status.json'
        for i, batch in enumerate(chunks):
            identity = hashlib.sha256(json.dumps(batch, sort_keys=True).encode()).hexdigest()[:16]
            archive = folder / 'archives' / ('chunk_%04d_%s.tar.gz' % (i, identity))
            receipt = archive.with_suffix(archive.suffix + '.verified.json')
            if receipt.exists():
                old = json.loads(receipt.read_text(encoding='utf-8'))
                if archive.stat().st_size != old['archive_bytes'] or digest(archive) != old['archive_sha256']:
                    raise ValueError('Previously verified local archive changed')
                completed += 1
                source_completed += old['source_bytes']
                continue
            temporary = archive.with_name(archive.name + '.partial-' + uuid.uuid4().hex)
            started = time.time()
            out, err = remote(c, STREAM, batch)
            h = hashlib.sha256()
            downloaded = 0
            last = 0
            with temporary.open('xb') as target:
                while True:
                    b = out.read(1024 * 1024)
                    if not b:
                        break
                    target.write(b)
                    h.update(b)
                    downloaded += len(b)
                    if time.time() - last > 15:
                        write_json(status_path, {'status': 'COPYING', 'host': host,
                            'chunks_complete': completed, 'chunks_total': len(chunks),
                            'verified_source_bytes': source_completed, 'current_chunk': i,
                            'current_downloaded_bytes': downloaded, 'updated_unix': time.time()})
                        last = time.time()
                target.flush()
                os.fsync(target.fileno())
            remote_error = err.read().decode()
            exit_code = out.channel.recv_exit_status()
            if exit_code:
                raise RuntimeError('Remote backup failed; partial preserved: ' + remote_error[-3000:])
            source = json.loads(remote_error)
            if downloaded != source['archive_bytes'] or h.hexdigest() != source['archive_sha256']:
                raise ValueError('Transfer hash mismatch; partial preserved')
            checked = verify_archive(temporary, batch, source)
            if archive.exists():
                raise FileExistsError('Preserve previous archive without receipt')
            temporary.rename(archive)
            checked.update(archive_sha256=h.hexdigest(), archive_bytes=downloaded,
                           completed_unix=time.time(), seconds=time.time()-started)
            write_json(receipt, checked)
            completed += 1
            source_completed += checked['source_bytes']
            emit(host, 'CHUNK_VERIFIED', chunk=i, chunks_complete=completed,
                 chunks_total=len(chunks), verified_source_bytes=source_completed)
        status = {'status': 'SELECTED_ROOTS_BACKUP_VERIFIED', 'host': host, 'roots': ROOTS,
                  'chunks_complete': completed, 'chunks_total': len(chunks),
                  'verified_source_bytes': source_completed, 'completed_unix': time.time(),
                  'not_in_scope': ['/root/p8-a-recompute-20261022'],
                  'labels': 'Opaque byte preservation only; no label interpretation or scientific scoring'}
        write_json(status_path, status)
        emit(host, 'SELECTED_ROOTS_BACKUP_VERIFIED', verified_source_bytes=source_completed)
        return status
    except Exception as e:
        write_json(folder / 'failure_' + str(time.time_ns()) + '.json', {'status': 'FAILED_PRESERVED', 'error': type(e).__name__ + ': ' + str(e), 'time': time.time()})
        emit(host, 'FAILED_PRESERVED', error=type(e).__name__ + ': ' + str(e))
        raise
    finally:
        c.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--destination', type=Path, required=True)
    ap.add_argument('--key', type=Path, default=Path.home() / '.ssh/lxbach.key')
    args = ap.parse_args()
    args.destination.mkdir(parents=True, exist_ok=True)
    password = getpass.getpass('SSH key passphrase (memory only): ')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(worker, host, password, args) for host in HOSTS]
        results = [f.result() for f in futures]
    del password
    write_json(args.destination / 'completion.json', {'status': 'SELECTED_ROOTS_BACKUP_VERIFIED', 'hosts': results})


if __name__ == '__main__':
    main()
