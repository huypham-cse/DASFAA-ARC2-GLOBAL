"""Copy only explicitly listed B1c input files between the two hosts; no qrels."""
import argparse
import getpass
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import time

if os.environ.get('ARC2_SSH_DEPS'):
    sys.path.insert(0, os.environ['ARC2_SSH_DEPS'])
import paramiko
from ssh_relay import SEND, RECEIVE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--reverse', action='store_true', help='MAIN to MINI instead of MINI to MAIN')
    parser.add_argument('--remote-manifest', default='/root/arc2_global_paper_20261025/b1c_prepare_20261028/transfer_manifest_r1.json')
    args = parser.parse_args()
    if args.receipt.exists():
        raise FileExistsError('Preserve existing transfer receipt')
    raw = args.manifest.read_bytes()
    spec = json.loads(raw)
    for name in spec['files']:
        if not name.startswith(('/root/arc2_global_paper_20261025/', '/root/arc2_p3h_20261020/')) or 'qrel' in name.lower():
            raise ValueError('Transfer is limited to explicit qrel-free project inputs')
    password = getpass.getpass('SSH key passphrase (memory only): ')
    clients = []
    began = time.time()
    remote = args.remote_manifest
    if not remote.startswith('/root/arc2_global_paper_20261025/'):
        raise ValueError('Manifest must stay inside the current project')
    endpoints = [('103.73.232.201', 62161), ('103.73.232.225', 52194)]
    if args.reverse:
        endpoints.reverse()
    try:
        for host, port in endpoints:
            c = paramiko.SSHClient()
            c.load_host_keys(str(Path.home() / '.ssh/known_hosts'))
            c.set_missing_host_key_policy(paramiko.RejectPolicy())
            c.connect(host, port=port, username='root', key_filename=str(Path.home() / '.ssh/lxbach.key'),
                      passphrase=password, look_for_keys=False, allow_agent=False, timeout=30)
            c.get_transport().set_keepalive(20)
            clients.append(c)
            create = 'from pathlib import Path;import sys;p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.open("xb").write(sys.stdin.buffer.read())'
            inp, out, err = c.exec_command(shlex.join(['python3', '-c', create, remote]))
            inp.write(raw)
            inp.channel.shutdown_write()
            out.read()
            error = err.read().decode()
            if out.channel.recv_exit_status():
                raise RuntimeError(error)
        del password
        _, source, source_err = clients[0].exec_command(shlex.join(['python3', '-u', '-c', SEND, remote]))
        sink, result, dest_err = clients[1].exec_command(shlex.join(['python3', '-u', '-c', RECEIVE, remote]))
        count = last = 0
        while True:
            data = source.read(1024 * 1024)
            if not data:
                break
            sink.write(data)
            count += len(data)
            if count - last > 100 * 1024 * 1024:
                print(json.dumps({'stream_bytes': count, 'elapsed_seconds': time.time() - began}), flush=True)
                last = count
        sink.channel.shutdown_write()
        source_error = source_err.read().decode()
        source_code = source.channel.recv_exit_status()
        output = result.read().decode()
        destination_error = dest_err.read().decode()
        destination_code = result.channel.recv_exit_status()
        record = {'status': 'TRANSFER_VERIFIED' if source_code == destination_code == 0 else 'FAILED_PRESERVED',
                  'source_host': endpoints[0][0], 'destination_host': endpoints[1][0],
                  'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'source_exit': source_code,
                  'destination_exit': destination_code, 'destination_output': output,
                  'source_error': source_error, 'destination_error': destination_error,
                  'stream_bytes': count, 'elapsed_seconds': time.time() - began}
        with args.receipt.open('x', encoding='utf-8') as f:
            json.dump(record, f, indent=2)
        print(json.dumps(record), flush=True)
        return 0 if record['status'] == 'TRANSFER_VERIFIED' else 1
    finally:
        for client in clients:
            client.close()


if __name__ == '__main__':
    raise SystemExit(main())
