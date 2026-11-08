"""Finite smoke-to-full B1-P schedule; no further item is auto-launched."""
import argparse,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'ops'))
from b1a_stage import dump
def main():
    p=argparse.ArgumentParser();p.add_argument('--code-commit',required=True);p.add_argument('--name',required=True);a=p.parse_args();assert a.name.replace('_','').isalnum()
    out=ROOT/'results'/('b1p_schedule_'+a.name);out.mkdir(exist_ok=False);smoke=ROOT/'results'/('b1p_smoke_'+a.name);full=ROOT/'results'/('b1p_full_'+a.name)
    meta={'status':'RUNNING','code_commit':a.code_commit,'jobs':[],'next_item_auto_launch':False};dump(out/'metadata.json',meta)
    for stage,dest in [('smoke',smoke),('full',full)]:
        cmd=[sys.executable,'-u',str(ROOT/'ops/b1p_stage.py'),'--stage',stage,'--output',str(dest),'--code-commit',a.code_commit]
        if stage=='full':cmd+=['--smoke',str(smoke)]
        row={'stage':stage,'argv':cmd,'started_unix':time.time()};meta['jobs'].append(row);dump(out/'metadata.json',meta)
        with (out/(stage+'.stdout.log')).open('x') as stdout,(out/(stage+'.stderr.log')).open('x') as stderr:process=subprocess.run(cmd,cwd=ROOT,stdout=stdout,stderr=stderr)
        row.update(exit_code=process.returncode,ended_unix=time.time());dump(out/'metadata.json',meta)
        if process.returncode:meta['status']='FAILED_PRESERVED';dump(out/'metadata.json',meta);return 1
    meta['status']='B1P_COMPLETE_STOP';dump(out/'metadata.json',meta);return 0
if __name__=='__main__':raise SystemExit(main())
