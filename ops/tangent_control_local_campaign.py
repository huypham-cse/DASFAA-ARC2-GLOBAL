"""Finite, sequential TC1L local campaign; no daemon or automatic restart."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
from tangent_control_run import ROOT,sha,dump,utc,verify_code


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lock',required=True);ap.add_argument('--output',required=True)
    args=ap.parse_args();lock=json.loads((ROOT/args.lock).read_text());verify_code(lock)
    root=Path(args.output).resolve();root.mkdir(parents=True,exist_ok=False)
    state={'status':'RUNNING','utc_start':utc(),'pid':os.getpid(),'lock_sha256':sha(ROOT/args.lock),'stages':[],
           'scope':'TC1L MiniLM-only Windows development; original remote status unknown'}
    env={**os.environ,'OPENBLAS_NUM_THREADS':'4','OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4'}
    receipts={}
    try:
        for stage in ['synthetic','smoke','full','score']:
            if stage=='score':
                argv=[sys.executable,'-u',str(ROOT/'ops/tangent_control_local_score.py'),'--lock',args.lock,
                      '--run',str(root/'full'),'--seal-sha256',sha(root/'full/ranking_seal.json')]
            else:
                argv=[sys.executable,'-u',str(ROOT/'ops/tangent_control_local_run.py'),'--lock',args.lock,
                      '--output',str(root/stage),'--stage',stage]
            record={'stage':stage,'utc_start':utc(),'argv':argv};state['stages'].append(record);dump(root/'campaign.json',state)
            print(json.dumps({'stage':stage,'utc':utc()}),flush=True)
            with (root/(stage+'.stdout.log')).open('x') as out,(root/(stage+'.stderr.log')).open('x') as err:
                result=subprocess.run(argv,cwd=ROOT,env=env,stdout=out,stderr=err)
            record.update(exit_code=result.returncode,utc_end=utc());dump(root/'campaign.json',state)
            if result.returncode:raise RuntimeError(stage+' failed; preserve, never auto-retry')
            if stage in ['synthetic','smoke']:
                relative=stage+'/metadata.json';receipts[relative]=sha(root/relative)
                if stage=='smoke':receipts['smoke/ranking_seal.json']=sha(root/'smoke/ranking_seal.json')
                dump(root/'stage_receipts.json',receipts)
        state.update(status='COMPLETE_STOP_FOR_REVIEW',utc_end=utc())
    except BaseException as exc:
        state.update(status='FAILED_PRESERVED',error=repr(exc),traceback=traceback.format_exc(),utc_end=utc());raise
    finally:
        dump(root/'campaign.json',state);print(json.dumps(state),flush=True)


if __name__=='__main__':main()
