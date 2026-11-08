"""Validate external baseline adapters, using no benchmark or qrel files."""
from __future__ import annotations
import argparse
import ast
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time
import traceback
import types

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from b1a_stage import Observations,dump,sha

def fixture(seed,dx,dy,n=128):
    import numpy as np
    from arc2_global.numerics import normalize_rows
    rng=np.random.default_rng(seed)
    x=normalize_rows(rng.normal(size=(n,dx)).astype(np.float32))
    y=normalize_rows((x@rng.normal(size=(dx,dy)).astype(np.float32)+.05*rng.normal(size=(1,dy))).astype(np.float32))
    return x,y

def cpu_checks(lock,out,meta):
    import numpy as np
    import scipy
    import sklearn
    from sklearn.cluster import KMeans
    from arc2_global.baseline_adapters import fit_la2m,fit_ridge,mixed_gallery,verify_upstream
    from arc2_global.numerics import normalize_rows
    actual={'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__}
    if actual!=lock['cpu_versions']:raise ValueError('CPU version drift')
    meta['cpu_runtime']={'versions':actual,'python':sys.version,'executable':sys.executable,
                         'module_origins':{'numpy':np.__file__,'scipy':scipy.__file__,'sklearn':sklearn.__file__},
                         'platform':platform.platform(),
                         'host':platform.node(),'environment':{k:os.environ.get(k) for k in lock['cpu_environment']}}
    upstream=verify_upstream(lock['upstream'],lock['upstream_raw_sha256'])
    path=upstream/'reproduce-scripts/la2m/exp_la2m.py';tree=ast.parse(path.read_text())
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['procrustes_fit','procrustes_apply','translate_o1']]
    namespace={'np':np,'KMeans':KMeans};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
    kernel=types.SimpleNamespace(**{k:namespace[k] for k in ['procrustes_fit','procrustes_apply','translate_o1']})
    rows=[];ridge_rows=[]
    # Two small cross-dimensional fixtures plus actual 1024-pair/384->768 shape.
    for seed in lock['seeds']:
        for dx,dy,n,na,clusters in [(24,40,128,64,1),(24,40,128,64,4),
                                     (40,24,128,64,1),(40,24,128,64,4),
                                     (384,768,1152,1024,20)]:
            old,target=fixture(seed,dx,dy,n);x,y=old[:na],target[:na]
            model=fit_la2m(x,y,seed=seed,n_clusters=clusters);raw=model.transform_raw(old)
            compact_x=np.concatenate((x,old),axis=0)
            compact_y=np.full((na+n,dy),np.nan,dtype=np.float32);compact_y[:na]=y
            expected=kernel.translate_o1('la2m',compact_x,compact_y,np.arange(na,na+n),np.arange(na),clusters,seed,center=True)
            delta=float(np.max(np.abs(raw-expected)))
            if not np.allclose(raw,expected,atol=1e-6,rtol=0):raise AssertionError('LA2M upstream parity')
            local_count=sum(v is not None for v in model.local_maps.values())
            if clusters>1 and local_count<2:raise AssertionError('No genuine multiple local maps')
            compact_y[na:]=np.random.default_rng(seed+100).normal(size=(n,dy)).astype(np.float32)
            changed=kernel.translate_o1('la2m',compact_x,compact_y,np.arange(na,na+n),np.arange(na),clusters,seed,center=True)
            np.testing.assert_array_equal(expected,changed)
            proxy=model.transform(old)
            fit_ids=np.arange(na,dtype=np.int64);paid=np.arange(na+(n-na)//2,dtype=np.int64)
            gallery=mixed_gallery(proxy,fit_ids,y,paid,target[paid])
            np.testing.assert_array_equal(gallery[paid],target[paid]);np.testing.assert_array_equal(gallery[len(paid):],proxy[len(paid):])
            if dx==384:
                for name,array in [('source',old),('target',target),('la2m_adapter',raw),('la2m_official',expected)]:
                    np.save(out/f'{name}_seed{seed}.npy',array,allow_pickle=False)
            rows.append({'seed':seed,'dims':[dx,dy],'fit_pairs':na,'clusters':clusters,
                         'local_maps':local_count,'max_raw_delta':delta,'nonanchor_target_invariance':True,
                         'paired_only_fit':True,'paid_overwrite_and_unpaid_identity':True})
            if clusters==1 or dx==384:
                ridge=fit_ridge(x,y)
                aug=np.concatenate((x.astype(np.float64),np.ones((na,1))),axis=1)
                oracle=np.linalg.lstsq(np.vstack((aug,np.sqrt(10.)*np.eye(dx+1))),
                      np.vstack((y.astype(np.float64),np.zeros((dx+1,dy)))),rcond=None)[0].astype(np.float32)
                difference=float(np.max(np.abs(ridge.coefficient-oracle)))
                if not np.allclose(ridge.coefficient,oracle,atol=1e-6,rtol=0):raise AssertionError('Ridge augmented-lstsq parity')
                if np.allclose(ridge.coefficient[:-1]@ridge.coefficient[:-1].T,np.eye(dx),atol=1e-3):
                    raise AssertionError('Ridge baseline unexpectedly constrained orthogonal')
                ridge_proxy=ridge.transform(old)
                result=mixed_gallery(ridge_proxy,fit_ids,y,paid,target[paid])
                np.testing.assert_array_equal(result[paid],target[paid])
                np.testing.assert_array_equal(result[len(paid):],ridge_proxy[len(paid):])
                ridge_rows.append({'seed':seed,'dims':[dx,dy],'fit_pairs':na,'coefficient_max_delta':difference,
                                   'lambda':10,'bias_regularized':True,'nonorthogonal':True})
            dump(out/'cpu_checks.json',{'status':'RUNNING','la2m':rows,'ridge':ridge_rows})
    # A deliberately isolated singleton source cluster must use global fallback.
    rng=np.random.default_rng(17)
    x=np.zeros((8,24),dtype=np.float32);x[:7,0]=1;x[:7]+=.01*rng.normal(size=(7,24)).astype(np.float32);x[7,1]=1
    x=normalize_rows(x);y=normalize_rows(x@rng.normal(size=(24,40)).astype(np.float32))
    m=fit_la2m(x,y,seed=17,n_clusters=2)
    singleton=int(m.anchor_labels[7]);assert np.sum(m.anchor_labels==singleton)==1
    assert m.local_maps[singleton] is None
    got=m.transform_raw(x[7:8]);ref=kernel.procrustes_apply(x[7:8],*m.global_map)
    np.testing.assert_array_equal(got,ref)
    rejects=0;proxy=m.transform(x)
    for call in [lambda:mixed_gallery(proxy,np.arange(8),y,np.arange(7),y[:7]),
                 lambda:mixed_gallery(proxy,np.arange(8),y,np.arange(8),y[::-1]),
                 lambda:mixed_gallery(proxy,np.arange(8),y,np.array([0,0,1,2,3,4,5,6,7]),y[[0,0,1,2,3,4,5,6,7]])]:
        try:call()
        except ValueError:rejects+=1
        else:raise AssertionError('Invalid paid gallery was accepted')
    result={'status':'CPU_BASELINES_PASS','la2m':rows,'ridge':ridge_rows,
            'singleton_global_fallback':True,'invalid_gallery_rejections':rejects}
    dump(out/'cpu_checks.json',result)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--code-commit',required=True);args=ap.parse_args()
    out=args.output.resolve()
    if out.parent!=(ROOT/'results').resolve() or not out.name.startswith('b1b_'):raise ValueError('New results/b1b_* path required')
    out.mkdir(parents=True,exist_ok=False);began=time.perf_counter()
    lock_path=ROOT/'configs/b1b_lock.json';lock=json.loads(lock_path.read_text())
    meta={'status':'RUNNING','stage':'B1b only','code_commit':args.code_commit,'lock_sha256':sha(lock_path),
          'started_utc':datetime.now(timezone.utc).isoformat(),'new_qrel_reads':0,
          'benchmark_quality_scoring':False,'real_dataset_or_encoder_loaded':False,'failures':[],
          'artificial_time_or_memory_caps':None}
    monitor=Observations(out);monitor.begin();dump(out/'metadata.json',meta)
    def interrupted(sig,frame):raise RuntimeError(f'Received signal {sig}')
    signal.signal(signal.SIGTERM,interrupted)
    try:
        if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()!=args.code_commit:
            raise ValueError('Wrong deployment commit')
        if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip():
            raise ValueError('Dirty tracked source')
        for rel,digest in lock['source_sha256_canonical_lf'].items():
            if hashlib.sha256((ROOT/rel).read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=digest:
                raise ValueError('Source drift: '+rel)
        if {k:os.environ.get(k) for k in lock['cpu_environment']}!=lock['cpu_environment']:
            raise ValueError('CPU invocation differs from locked environment')
        meta['cpu_checks']=cpu_checks(lock,out,meta);dump(out/'metadata.json',meta)
        env={**os.environ,'CUBLAS_WORKSPACE_CONFIG':':4096:8','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
        with (out/'gpu.stdout.log').open('w') as stdout,(out/'gpu.stderr.log').open('w') as stderr:
            p=subprocess.run([lock['gpu_python'],'-u',str(ROOT/'ops/b1b_gpu_worker.py'),'--lock',str(lock_path),'--output',str(out/'simplelinear_gpu')],env=env,stdout=stdout,stderr=stderr)
        meta['gpu_worker_exit_code']=p.returncode
        if p.returncode:raise RuntimeError('Official SimpleLinear GPU checks failed; preserve worker logs')
        gpu=json.loads((out/'simplelinear_gpu/metadata.json').read_text())
        if gpu['status']!='SIMPLELINEAR_OFFICIAL_CUDA_CHECKS_PASS':raise ValueError('GPU worker incomplete')
        meta['simplelinear']=gpu;meta['status']='B1B_BASELINE_ADAPTERS_PASS'
        meta['next_action']='STOP - report B1b and wait for confirmation before B1-M'
    except BaseException as exc:
        meta.update(status='FAILED_PRESERVED',failures=[repr(exc)],traceback=traceback.format_exc())
    finally:
        monitor.end();meta.update(wall_seconds=time.perf_counter()-began,peak_process_tree_rss_bytes=monitor.peak,
                                 ended_utc=datetime.now(timezone.utc).isoformat());dump(out/'metadata.json',meta)
    print(json.dumps({'status':meta['status'],'failures':meta['failures']}))
    return 0 if meta['status']=='B1B_BASELINE_ADAPTERS_PASS' else 1

if __name__=='__main__':raise SystemExit(main())
