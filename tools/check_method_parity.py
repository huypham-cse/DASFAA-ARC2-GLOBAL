"""Synthetic-only parity against the already evaluated reference; no GPU/qrels."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import arc2_global as method
from arc2_global import procrustes as kernel

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reference',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists(): raise FileExistsError('Preserve existing QA receipt')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    record={'scope':'synthetic packaging verification only','new_qrel_reads':0,
            'new_benchmark_rankings':0,'platform':platform.platform(),'python':sys.version,
            'pre_check_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'checks':[],'status':'RUNNING'}
    started=time.perf_counter()
    try:
        extraction=json.loads((ROOT/'provenance/implementation_extraction.json').read_text())
        for r in extraction['sources']:
            if hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()!=r['sha256']:
                raise AssertionError('Reference source changed since extraction')
        sys.path.insert(1,str(args.reference.resolve()/'artifact/src'))
        from mixindex_arc2 import p8_procrustes_geometry as reference
        with threadpool_limits(limits=4):
            for case,(dx,dy) in enumerate([(24,24),(24,40),(40,24),(384,768)]):
                rng=np.random.default_rng(17+case)
                old=method.normalize_rows(rng.normal(size=(80,dx)).astype(np.float32))
                new=method.normalize_rows((old@rng.normal(size=(dx,dy)).astype(np.float32)+
                       .02*rng.normal(size=(80,dy))).astype(np.float32))
                anchors=rng.choice(80,24,replace=False).astype(np.int64)
                actual=method.fit_arc2_global(old,anchors,new[anchors])
                expected=reference.fit_procrustes_arc2(old,anchors,new[anchors],kernel=kernel)
                for field in ['source_mean','target_mean','matrix','base_coef','one_step_coef','arc2_coef']:
                    np.testing.assert_array_equal(getattr(actual,field),getattr(expected,field))
                for block in [1,13,512]:
                    np.testing.assert_array_equal(method.transform_old_docs(old,actual,block_rows=block),
                        reference.transform_old_docs(old,expected,method='procrustes_tangent2_global',block_rows=block))
                selected=method.select_for_budget(anchors,np.arange(80),n_docs=80,fraction=.5)
                assert len(selected)==40 and set(anchors)<=set(selected)
                mixed=method.build_mixed_gallery(old,actual,selected,new[selected],block_rows=13)
                np.testing.assert_array_equal(mixed,reference.build_mixed_gallery(old,expected,
                    selected,new[selected],method='procrustes_tangent2_global',block_rows=13))
                np.testing.assert_array_equal(mixed[selected],new[selected])
                record['checks'].append({'source_dim':dx,'target_dim':dy,'coefficient_proxy_mixed_exact':True,
                                         'blocks':[1,13,512],'anchor_inclusive_selected':40})
            for label,call in [
                ('budget_below_anchors',lambda:method.select_for_budget(anchors,np.arange(80),n_docs=80,fraction=.1)),
                ('missing_anchor',lambda:method.build_mixed_gallery(old,actual,np.array([],dtype=np.int64),new[:0])),
                ('changed_anchor',lambda:method.build_mixed_gallery(old,actual,anchors,new[anchors][::-1])),
                ('invalid_block',lambda:method.transform_old_docs(old,actual,block_rows=0)),
            ]:
                try: call()
                except ValueError: record['checks'].append({'rejection':label,'passed':True})
                else: raise AssertionError(f'Failed to reject {label}')
        record['status']='PASS'
    except Exception:
        record['status']='FAIL';record['failure']=traceback.format_exc()
    finally:
        record['wall_seconds']=time.perf_counter()-started
        args.output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))
    return 0 if record['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
