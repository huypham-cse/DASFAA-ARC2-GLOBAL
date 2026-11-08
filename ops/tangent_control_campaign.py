"""Finite synthetic -> smoke -> full -> separate DEV score; preserve failures."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
from tangent_control_run import sha, dump, utc, verify_code, ROOT


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lock',required=True); ap.add_argument('--output',required=True)
    args=ap.parse_args(); lock=json.loads((ROOT/args.lock).read_text());verify_code(lock)
    root=Path(args.output).resolve();root.mkdir(parents=True,exist_ok=False)
    state={'status':'RUNNING','utc_start':utc(),'lock_sha256':sha(ROOT/args.lock),
           'stages':[],'pid':os.getpid(),'scope':'FiQA matched-residual DEV only'}
    env={**os.environ,'OPENBLAS_NUM_THREADS':str(lock['blas_threads']),
         'OMP_NUM_THREADS':str(lock['blas_threads']),'MKL_NUM_THREADS':str(lock['blas_threads'])}
    try:
        for stage in ('synthetic','smoke','full','score'):
            if stage=='score':
                seal=sha(root/'full/ranking_seal.json')
                command=[sys.executable,'-u',str(ROOT/'ops/tangent_control_score.py'),
                         '--lock',args.lock,'--run',str(root/'full'),'--seal-sha256',seal]
            else:
                command=[sys.executable,'-u',str(ROOT/'ops/tangent_control_run.py'),
                         '--lock',args.lock,'--output',str(root/stage),'--stage',stage]
                if stage=='full':command.extend(['--smoke',str(root/'smoke')])
            record={'stage':stage,'utc_start':utc(),'argv':command}
            state['stages'].append(record);dump(root/'campaign.json',state)
            print(json.dumps({'stage':stage,'utc':utc()}),flush=True)
            with (root/(stage+'.stdout.log')).open('x') as out,(root/(stage+'.stderr.log')).open('x') as err:
                child=subprocess.run(command,cwd=ROOT,env=env,stdout=out,stderr=err)
            record.update(exit_code=child.returncode,utc_end=utc());dump(root/'campaign.json',state)
            if child.returncode:raise RuntimeError(stage+' failed; all attempts retained')
        state.update(status='COMPLETE_STOP_FOR_REVIEW',utc_end=utc())
    except BaseException as exc:
        state.update(status='FAILED_PRESERVED',utc_end=utc(),error=repr(exc),traceback=traceback.format_exc());raise
    finally:
        dump(root/'campaign.json',state);print(json.dumps(state),flush=True)


if __name__=='__main__':main()
