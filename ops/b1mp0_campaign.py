"""Finite authorized B1-M/P0 schedule, smoke first, no time/resource cutoff."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'ops'))
from b1a_stage import dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--code-commit',required=True);ap.add_argument('--name',required=True);a=ap.parse_args()
    assert a.name.replace('_','').isalnum()
    schedule=ROOT/'results'/('b1mp0_schedule_'+a.name);schedule.mkdir(exist_ok=False)
    results=ROOT/'results';smoke=results/('b1m_smoke_'+a.name);p0smoke=results/('b1p0_smoke_'+a.name)
    p0full=results/('b1p0_full_'+a.name);full=results/('b1m_full_'+a.name)
    jobs=[('p0_smoke',[sys.executable,str(ROOT/'ops/b1p0_worker.py'),'--lock',str(ROOT/'configs/b1p0_lock.json'),'--stage','smoke','--output',str(p0smoke),'--code-commit',a.code_commit]),
          ('mechanism_smoke',[sys.executable,str(ROOT/'ops/b1m_stage.py'),'--stage','smoke','--output',str(smoke),'--code-commit',a.code_commit]),
          ('p0_full',[sys.executable,str(ROOT/'ops/b1p0_worker.py'),'--lock',str(ROOT/'configs/b1p0_lock.json'),'--stage','full','--output',str(p0full),'--code-commit',a.code_commit]),
          ('mechanism_full',[sys.executable,str(ROOT/'ops/b1m_stage.py'),'--stage','full','--output',str(full),'--code-commit',a.code_commit,'--smoke',str(smoke),'--p0-smoke',str(p0smoke)])]
    receipt={'status':'RUNNING','code_commit':a.code_commit,'authorized_items':['B1-M','B1-P0'],'automatic_next_stage':False,'jobs':[]}
    dump(schedule/'metadata.json',receipt)
    for name,argv in jobs:
        row={'job':name,'started_unix':time.time(),'argv':argv};receipt['jobs'].append(row);dump(schedule/'metadata.json',receipt)
        with (schedule/(name+'.stdout.log')).open('x') as stdout,(schedule/(name+'.stderr.log')).open('x') as stderr:
            process=subprocess.run(argv,cwd=ROOT,stdout=stdout,stderr=stderr)
        row.update(exit_code=process.returncode,ended_unix=time.time());dump(schedule/'metadata.json',receipt)
        if process.returncode:
            receipt['status']='FAILED_PRESERVED';dump(schedule/'metadata.json',receipt);return 1
    receipt['status']='B1M_P0_COMPLETE_STOP';dump(schedule/'metadata.json',receipt);return 0
if __name__=='__main__':raise SystemExit(main())
