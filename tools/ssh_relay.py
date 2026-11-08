"""Stream a hash-listed qrel-free package between two authorized SSH hosts.

Credentials stay in memory; host keys must already be trusted. Existing matching
files are verified and retained. Transfer uses bounded chunks, not laptop RAM
proportional to archive size. No remote private key or network service is created.
"""
import argparse,getpass,hashlib,json,os,shlex,sys,time
from pathlib import Path
if os.environ.get('ARC2_SSH_DEPS'):sys.path.insert(0,os.environ['ARC2_SSH_DEPS'])
import paramiko

SEND='''import json,sys,tarfile
from pathlib import Path
m=json.loads(Path(sys.argv[1]).read_text())
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:
 for name in m['files']:t.add(name,arcname=name.lstrip('/'),recursive=False)
'''
RECEIVE='''import json,sys,tarfile,hashlib,os,time
from pathlib import Path
manifest=Path(sys.argv[1]);m=json.loads(manifest.read_text());expected=m['files'];seen=set();total=0
with tarfile.open(fileobj=sys.stdin.buffer,mode='r|') as tar:
 for member in tar:
  path=Path('/')/member.name;name=str(path)
  assert member.isfile() and name in expected and name not in seen
  assert path.resolve()==path and '..' not in path.parts
  spec=expected[name];assert member.size==spec['bytes']
  source=tar.extractfile(member);path.parent.mkdir(parents=True,exist_ok=True)
  temporary=path.with_name(path.name+'.arc2transfer-'+str(os.getpid()))
  digest=hashlib.sha256();count=0
  with temporary.open('xb') as out:
   while True:
    block=source.read(1024*1024)
    if not block:break
    digest.update(block);count+=len(block);out.write(block)
   out.flush();os.fsync(out.fileno())
  assert count==spec['bytes'] and digest.hexdigest()==spec['sha256'],name
  if path.exists():
   old=hashlib.sha256()
   with path.open('rb') as stream:
    for block in iter(lambda:stream.read(1024*1024),b''):old.update(block)
   assert path.stat().st_size==count and old.hexdigest()==spec['sha256'],name
   temporary.unlink()
  else:temporary.rename(path)
  seen.add(name);total+=count
assert seen==set(expected)
receipt={'status':'TRANSFER_VERIFIED','files':len(seen),'bytes':total,'finished_unix':time.time(),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}
manifest.with_name(manifest.stem+'_received.json').open('x').write(json.dumps(receipt,indent=2)+'\\n')
print(json.dumps(receipt))
'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--receipt',type=Path,required=True)
    a=ap.parse_args();assert not a.receipt.exists()
    data=a.manifest.read_bytes();manifest=json.loads(data)
    for name in manifest['files']:
        assert name.startswith('/root/') and 'qrels' not in Path(name).parts and not Path(name).name.startswith('qrel')
    password=getpass.getpass('SSH key passphrase (not saved): ');clients=[]
    try:
        for host,port in [('103.73.232.225',52194),('103.73.232.201',62161)]:
            c=paramiko.SSHClient();c.load_host_keys(str(Path.home()/'.ssh/known_hosts'));c.set_missing_host_key_policy(paramiko.RejectPolicy())
            c.connect(host,port=port,username='root',key_filename=str(Path.home()/'.ssh/lxbach.key'),passphrase=password,look_for_keys=False,allow_agent=False,timeout=30)
            c.get_transport().set_keepalive(30);clients.append(c)
        del password
        remote='/root/arc2_global_paper_20261025/b1p_mini_transport_manifest_20261026.json'
        dest=clients[1]
        code='from pathlib import Path;import sys;p=Path(sys.argv[1]);p.open("xb").write(sys.stdin.buffer.read())'
        inp,out,err=dest.exec_command(shlex.join(['python3','-c',code,remote]));inp.write(data);inp.channel.shutdown_write()
        output=out.read();error=err.read();assert out.channel.recv_exit_status()==0,error.decode()
        _,source,source_err=clients[0].exec_command(shlex.join(['python3','-u','-c',SEND,remote]))
        sink,result,dest_err=dest.exec_command(shlex.join(['python3','-u','-c',RECEIVE,remote]))
        count=0;last=0;began=time.time()
        while True:
            block=source.read(1024*1024)
            if not block:break
            sink.write(block);count+=len(block)
            if count-last>=100*1024*1024:
                print(json.dumps({'streamed_bytes':count,'elapsed_seconds':time.time()-began}),flush=True);last=count
        sink.channel.shutdown_write()
        source_error=source_err.read().decode();source_exit=source.channel.recv_exit_status()
        output=result.read().decode();error=dest_err.read().decode();dest_exit=result.channel.recv_exit_status()
        receipt={'source_host':'103.73.232.225','destination_host':'103.73.232.201','source_exit':source_exit,'destination_exit':dest_exit,'destination_output':output,'source_error':source_error,'destination_error':error,'stream_bytes':count,'elapsed_seconds':time.time()-began,'manifest_sha256':hashlib.sha256(data).hexdigest()}
        a.receipt.parent.mkdir(parents=True,exist_ok=True);a.receipt.open('x').write(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt),flush=True)
        return 0 if source_exit==dest_exit==0 else 1
    finally:
        for c in clients:c.close()
if __name__=='__main__':raise SystemExit(main())
