"""Interactive SSH helper. Credentials stay in memory; trust existing host keys.

Set ARC2_SSH_DEPS only if Paramiko is installed in a separate local directory.
Requests are JSON lines on stdin. This is an operator tool, not a job daemon.
"""
import argparse
import getpass
import json
import os
from pathlib import Path
import posixpath
import shlex
import sys

if os.environ.get('ARC2_SSH_DEPS'):
    sys.path.insert(0,os.environ['ARC2_SSH_DEPS'])
import paramiko

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--host',default='103.73.232.225')
    ap.add_argument('--port',type=int,default=52194)
    ap.add_argument('--key',type=Path,default=Path.home()/'.ssh/lxbach.key')
    ap.add_argument('--passphrase-stdin',action='store_true',
                    help='Read one passphrase line from stdin; never save it')
    ap.add_argument('--transfer-root',default='/root/arc2_global_paper_20261025',
                    choices=['/root/arc2_global_paper_20261025','/network-volume/arc2_recovery_20261030'])
    args=ap.parse_args()
    if args.passphrase_stdin:
        print('SSH_PASSPHRASE_STDIN_READY',flush=True)
        password=sys.stdin.readline().rstrip('\r\n')
    else:
        password=getpass.getpass('SSH key passphrase (not saved): ')
    client=paramiko.SSHClient()
    client.load_host_keys(str(Path.home()/'.ssh/known_hosts'))
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(args.host,port=args.port,username='root',key_filename=str(args.key),
                   passphrase=password,look_for_keys=False,allow_agent=False,timeout=20)
    del password
    client.get_transport().set_keepalive(30)
    print(json.dumps({'status':'SSH_CONNECTED','host':args.host,'port':args.port}),flush=True)
    try:
        for line in sys.stdin:
            try:
                req=json.loads(line)
                action=req['action']
                if action=='close':break
                if action=='python':
                    argv=[req.get('python','python3'),'-u','-c',req['code']]
                elif action=='argv':argv=req['argv']
                elif action in ('upload','download'):
                    remote=posixpath.normpath(req['remote'])
                    if not remote.startswith(args.transfer_root.rstrip('/')+'/'):
                        raise ValueError('Transfer target outside current project')
                    # This server disables SFTP; use the authenticated SSH channel.
                    if action=='upload':
                        code='import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); p.open("xb").write(sys.stdin.buffer.read())'
                        inp,out,err=client.exec_command(shlex.join(['python3','-c',code,remote]))
                        with Path(req['local']).open('rb') as source:
                            for block in iter(lambda:source.read(1024*1024),b''):
                                inp.write(block)
                        inp.channel.shutdown_write()
                        output=out.read();error=err.read()
                        if out.channel.recv_exit_status()!=0:raise RuntimeError(error.decode())
                    else:
                        local=Path(req['local'])
                        if local.exists():raise FileExistsError('Preserve local result')
                        code='import pathlib,sys; sys.stdout.buffer.write(pathlib.Path(sys.argv[1]).read_bytes())'
                        _,out,err=client.exec_command(shlex.join(['python3','-c',code,remote]))
                        data=out.read();error=err.read()
                        if out.channel.recv_exit_status()!=0:raise RuntimeError(error.decode())
                        local.parent.mkdir(parents=True,exist_ok=True)
                        local.write_bytes(data)
                    print(json.dumps({'id':req.get('id'),'status':'TRANSFER_OK'}),flush=True)
                    continue
                else:raise ValueError('Unknown request')
                _,stdout,stderr=client.exec_command(shlex.join(argv))
                output=stdout.read().decode('utf-8',errors='replace')
                error=stderr.read().decode('utf-8',errors='replace')
                status=stdout.channel.recv_exit_status()
                print(json.dumps({'id':req.get('id'),'exit_code':status,'stdout':output,'stderr':error}),flush=True)
            except Exception as e:
                print(json.dumps({'id':locals().get('req',{}).get('id'),'error':str(e)}),flush=True)
    finally:client.close()

if __name__=='__main__':main()
