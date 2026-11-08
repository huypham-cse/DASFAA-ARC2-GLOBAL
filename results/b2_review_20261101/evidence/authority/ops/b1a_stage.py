"""B1a input checks and small smoke only; deliberately has no qrel scorer."""
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
import threading
import time
import traceback
import types
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(obj,indent=2)+'\n');temp.replace(path)

class Observations:
    def __init__(self,out):self.out=out;self.event=threading.Event();self.peak=0
    def sample(self):
        import psutil
        row={'unix':time.time(),'pid':os.getpid()}
        try:
            process=psutil.Process()
            rss=sum(p.memory_info().rss for p in [process]+process.children(recursive=True) if p.is_running())
            self.peak=max(self.peak,rss);row['process_tree_rss_bytes']=rss
            row['host_available_memory_bytes']=psutil.virtual_memory().available
            p=subprocess.run(['nvidia-smi','--query-gpu=uuid,memory.used,utilization.gpu','--format=csv,noheader'],capture_output=True,text=True)
            row['shared_gpu']=p.stdout.strip();row['gpu_query_exit']=p.returncode
        except Exception as e:row['observation_error']=repr(e)
        with (self.out/'resource_trace.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    def run(self):
        while not self.event.is_set():self.sample();self.event.wait(5)
    def begin(self):self.thread=threading.Thread(target=self.run,daemon=True);self.thread.start()
    def end(self):self.event.set();self.thread.join();self.sample()

def check_sources(lock,commit):
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    if head!=commit or dirty:raise ValueError('Deployment commit/worktree mismatch')
    for rel,digest in lock['source_sha256_canonical_lf'].items():
        actual=hashlib.sha256((ROOT/rel).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        if actual!=digest:raise ValueError('Source drift: '+rel)
    for spec in lock['models'].values():
        for rel,digest in spec['file_sha256'].items():
            if sha(Path(spec['path'])/rel)!=digest:raise ValueError('Model drift: '+rel)

def read_parquet(path):
    import pyarrow.parquet as pq
    rows=pq.read_table(path,columns=['_id','text']).to_pylist()
    values=[{'_id':str(r['_id']),'text':str(r['text'])} for r in rows]
    if len({r['_id'] for r in values})!=len(values):raise ValueError('Duplicate dataset IDs')
    return sorted(values,key=lambda r:r['_id'])

def prepare_nano(lock,out):
    import numpy as np
    from arc2_global import select_for_budget
    result={}
    for name,spec in lock['datasets'].items():
        folder=out/'inputs'/name;folder.mkdir(parents=True)
        groups={'corpus':[],'queries':[]};files={}
        for record in spec['files']:
            rel=record['rfilename'];group=rel.split('/')[0]
            if group not in groups or not rel.endswith('.parquet'):
                raise ValueError('Non-whitelisted dataset file')
            path=folder/rel;path.parent.mkdir(parents=True,exist_ok=True)
            url=f"https://huggingface.co/datasets/{spec['repo']}/resolve/{spec['revision']}/{rel}"
            partial=path.with_suffix('.download')
            with urllib.request.urlopen(url,timeout=60) as response,partial.open('xb') as target:
                while True:
                    block=response.read(1024*1024)
                    if not block:break
                    target.write(block)
            if sha(partial)!=record['lfs']['sha256'] or partial.stat().st_size!=record['size']:
                raise ValueError('Dataset download identity mismatch')
            partial.rename(path);files[rel]={'path':str(path),'sha256':sha(path),'bytes':path.stat().st_size}
            groups[group].extend(read_parquet(path))
        n=len(groups['corpus']);q=len(groups['queries'])
        if n!=spec['expected_docs'] or q!=spec['expected_queries']:
            raise ValueError('Dataset count mismatch: '+name)
        doc_ids=[r['_id'] for r in groups['corpus']];qids=[r['_id'] for r in groups['queries']]
        dump(folder/'ids.json',{'doc_ids':doc_ids,'query_ids':qids,'row_order':'lexicographic string IDs'})
        selections={};anchor_order_files={}
        for seed in lock['seeds']:
            anchors=np.random.default_rng(np.random.SeedSequence([seed,0])).choice(n,1024,replace=False).astype(np.int64)
            order=np.random.default_rng(np.random.SeedSequence([seed,1])).permutation(n).astype(np.int64)
            np.save(folder/f'anchors_seed{seed}.npy',anchors,allow_pickle=False)
            np.save(folder/f'order_seed{seed}.npy',order,allow_pickle=False)
            for role,values in [('anchors',anchors),('order',order)]:
                name_in_folder=f'{role}_seed{seed}.npy'
                anchor_order_files[name_in_folder]={'count':len(values),'sha256':sha(folder/name_in_folder)}
            previous=set()
            for budget in [.25,.5,.75]:
                selected=select_for_budget(anchors,order,n_docs=n,fraction=budget)
                if not previous<=set(selected) or not set(anchors)<=set(selected):raise AssertionError('Paid sets not nested')
                previous=set(selected)
                path=folder/f'paid_seed{seed}_{int(budget*100)}pct.npy';np.save(path,selected,allow_pickle=False)
                selections[path.name]={'count':len(selected),'sha256':sha(path)}
        result[name]={'docs':n,'queries':q,'revision':spec['revision'],'files':files,
                      'ids_sha256':sha(folder/'ids.json'),'anchor_order_files':anchor_order_files,
                      'paid_sets':selections,'qrels_requested_or_read':False}
        dump(out/'input_receipts.json',result)
    return result

def verify_fiqa(lock,out):
    import numpy as np
    from arc2_global import select_for_budget
    spec=lock['fiqa'];path=Path(spec['manifest_path'])
    if sha(path)!=spec['manifest_sha256']:raise ValueError('FiQA manifest drift')
    manifest=json.loads(path.read_text());records={}
    for key in ['config','corpus','source_queries','dev_query_ids']:
        r=manifest['source_inputs'][key]
        if sha(Path(r['path']))!=r['sha256']:raise ValueError('FiQA raw input drift: '+key)
    for pair,vectors in manifest['vectors'].items():
        for role,r in vectors.items():
            path=Path(r['path'])
            if sha(path)!=r['sha256']:raise ValueError('FiQA cached vector drift')
            a=np.load(path,mmap_mode='r',allow_pickle=False)
            if list(a.shape)!=r['shape'] or a.dtype!=np.float32:raise ValueError('FiQA vector shape/dtype')
            for start in range(0,len(a),512):
                part=a[start:start+512]
                if not np.isfinite(part).all() or not np.allclose(np.linalg.norm(part,axis=1),1,atol=1e-4,rtol=0):
                    raise ValueError('FiQA vector finite/unit check')
            records[pair+'/'+role]={'path':str(path),'sha256':r['sha256'],'shape':r['shape']}
    ids=Path(manifest['ids']['path'])
    if sha(ids)!=manifest['ids']['sha256']:raise ValueError('FiQA source IDs drift')
    actual=json.loads(ids.read_text());packaged=json.loads((ROOT/'results/fiqa_development/ids.json').read_text())
    if actual!=packaged:raise ValueError('FiQA ID order differs from selected results')
    order=np.load(ROOT/'results/fiqa_development/backfill_order.npy',allow_pickle=False)
    reference=Path(lock['reference_root'])/'artifact/results/p8_full_r10_20261025'
    np.testing.assert_array_equal(order,np.load(reference/'backfill_order.npy',allow_pickle=False))
    paid={}
    for seed in lock['seeds']:
        anchors=np.load(ROOT/f'results/fiqa_development/selections/anchors_seed_{seed}.npy',allow_pickle=False)
        np.testing.assert_array_equal(anchors,np.load(reference/f'selections/anchors_seed_{seed}.npy',allow_pickle=False))
        for budget in [.25,.5,.75]:
            selected=select_for_budget(anchors,order,n_docs=57638,fraction=budget)
            if budget in [.25,.5]:
                np.testing.assert_array_equal(selected,np.load(ROOT/f'results/fiqa_development/selections/seed{seed}_{int(budget*100)}pct.npy',allow_pickle=False))
            path=out/'inputs/FiQA'/f'paid_seed{seed}_{int(budget*100)}pct.npy'
            path.parent.mkdir(parents=True,exist_ok=True);np.save(path,selected,allow_pickle=False)
            paid[path.name]={'count':len(selected),'sha256':sha(path)}
    return {'vectors':records,'docs':57638,'queries':500,'ordered_ids_equal':True,
            'anchors_and_backfill_equal':True,'paid_sets':paid,'new_physical_document_encodes':0,
            'reuse_scope':'hash/ID verified cached representations, not full fresh-encoder reproduction'}

def synthetic_checks(lock,out):
    import numpy as np
    import scipy
    from arc2_global import fit_arc2_global,normalize_rows,transform_old_docs,build_mixed_gallery,select_for_budget
    from arc2_global.retrieval import exact_topk
    if {'numpy':np.__version__,'scipy':scipy.__version__}!=lock['cpu_versions']:
        raise ValueError('CPU numerical runtime drift')
    runtime={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),
             'hostname':platform.node(),'numpy':np.__version__,'scipy':scipy.__version__,
             'environment':{k:os.environ.get(k) for k in ['OPENBLAS_CORETYPE','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS']}}
    reference_root=Path(lock['reference_root'])
    for rel,digest in lock['reference_sha256_canonical_lf'].items():
        if hashlib.sha256((reference_root/rel).read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=digest:
            raise ValueError('Historical numerical source changed')
    upstream=Path(lock['upstream_script'])
    if sha(upstream)!=lock['upstream_sha256']:raise ValueError('Upstream kernel changed')
    upstream_root=upstream.parents[2]
    upstream_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream_root,text=True).strip()
    upstream_dirty=subprocess.check_output(['git','status','--porcelain'],cwd=upstream_root,text=True).strip()
    if upstream_revision!=lock['upstream_revision'] or upstream_dirty:
        raise ValueError('Upstream revision/worktree mismatch')
    runtime['upstream_revision']=upstream_revision;runtime['upstream_raw_sha256']=sha(upstream)
    code=upstream.read_text();tree=ast.parse(code)
    chosen=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['procrustes_fit','procrustes_apply']],type_ignores=[])
    namespace={'np':np};exec(compile(chosen,str(upstream),'exec'),namespace)
    kernel=types.SimpleNamespace(**{k:namespace[k] for k in ['procrustes_fit','procrustes_apply']})
    sys.path.insert(1,str(reference_root/'artifact/src'))
    from mixindex_arc2 import p8_procrustes_geometry as reference
    results=[]
    for case,(dx,dy) in enumerate([(24,24),(24,40),(40,24),(384,768)]):
        rng=np.random.default_rng(17+case)
        old=normalize_rows(rng.normal(size=(80,dx)).astype(np.float32))
        target=normalize_rows((old@rng.normal(size=(dx,dy)).astype(np.float32)+.02*rng.normal(size=(80,dy))).astype(np.float32))
        anchors=rng.choice(80,24,replace=False).astype(np.int64)
        actual=fit_arc2_global(old,anchors,target[anchors]);expected=reference.fit_procrustes_arc2(old,anchors,target[anchors],kernel=kernel)
        for field in ['base_coef','one_step_coef','arc2_coef','matrix']:
            np.testing.assert_array_equal(getattr(actual,field),getattr(expected,field))
        selected=select_for_budget(anchors,np.arange(80),n_docs=80,fraction=.5)
        for block in [1,13,512]:
            np.testing.assert_array_equal(transform_old_docs(old,actual,block_rows=block),reference.transform_old_docs(old,expected,method='procrustes_tangent2_global',block_rows=block))
            np.testing.assert_array_equal(build_mixed_gallery(old,actual,selected,target[selected],block_rows=block),reference.build_mixed_gallery(old,expected,selected,target[selected],method='procrustes_tangent2_global',block_rows=block))
        results.append({'old_dim':dx,'new_dim':dy,'blocks':[1,13,512],'exact_reference_parity':True})
    docs=np.array([[1,0],[1,0],[0,1],[-1,0]],dtype=np.float32);query=np.array([[1,0]],dtype=np.float32)
    got=exact_topk(query,docs,k=3,query_ids=['q0'],document_ids=['d0','d1','q0','d3'],exclude_identical_ids=True)
    np.testing.assert_array_equal(got,[[0,1,3]])
    dump(out/'synthetic_checks.json',{'status':'PASS','runtime':runtime,'reference_parity':results,'tie_and_exclusion_test':True})
    return runtime

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--code-commit',required=True)
    ap.add_argument('--lock',type=Path,default=ROOT/'configs/b1a_lock.json');args=ap.parse_args()
    out=args.output.resolve()
    if out.parent!=(ROOT/'results').resolve() or not out.name.startswith('b1a_'):
        raise ValueError('New results/b1a_* directory required')
    out.mkdir(parents=True,exist_ok=False)
    began=time.perf_counter();lock_path=args.lock.resolve();lock=json.loads(lock_path.read_text())
    meta={'status':'RUNNING','stage':'B1a only','code_commit':args.code_commit,
          'lock_path':str(lock_path),'lock_sha256':sha(lock_path),'started_utc':datetime.now(timezone.utc).isoformat(),
          'new_qrel_reads':0,'benchmark_rankings_generated':False,'independent_scoring':False,
          'artificial_resource_or_time_caps':None,'failures':[],'source_worktree':str(ROOT)}
    monitor=Observations(out);monitor.begin();dump(out/'metadata.json',meta)
    def interrupted(sig,frame):raise RuntimeError(f'Received signal {sig}; preserving attempt')
    signal.signal(signal.SIGTERM,interrupted)
    try:
        check_sources(lock,args.code_commit)
        expected_env={'OPENBLAS_CORETYPE':'Haswell','OMP_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4'}
        if {k:os.environ.get(k) for k in expected_env}!=expected_env:
            raise ValueError('CPU BLAS/thread invocation differs from protocol')
        meta['cpu_runtime']=synthetic_checks(lock,out)
        meta['fiqa']=verify_fiqa(lock,out);dump(out/'metadata.json',meta)
        meta['nano']=prepare_nano(lock,out);dump(out/'metadata.json',meta)
        env={**os.environ,'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1',
             'CUBLAS_WORKSPACE_CONFIG':':4096:8','OMP_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4'}
        with (out/'gpu_worker.stdout.log').open('w') as stdout,(out/'gpu_worker.stderr.log').open('w') as stderr:
            worker=subprocess.run([lock['gpu_python'],'-u',str(ROOT/'ops/b1a_gpu_worker.py'),
                '--lock',str(lock_path),'--output',str(out/'gpu_smoke')],
                env=env,stdout=stdout,stderr=stderr)
        meta['gpu_worker_exit_code']=worker.returncode
        if worker.returncode!=0:raise RuntimeError('GPU smoke failed; preserve worker output')
        gpu=json.loads((out/'gpu_smoke/metadata.json').read_text())
        if gpu['status']!='GPU_SMOKE_PASS' or len(gpu['models'])!=4:raise ValueError('Incomplete GPU smoke')
        meta['gpu_smoke']=gpu
        import numpy as np
        from arc2_global import fit_arc2_global,build_mixed_gallery
        from arc2_global.retrieval import exact_topk
        meta['toy_mixed_gallery_checks']={}
        for name,old_label,new_label in [('minilm_distilroberta','minilm_x','distilroberta_y'),
                                          ('e5_small_base','e5_small_x','e5_base_y')]:
            old=np.load(out/'gpu_smoke'/(old_label+'.npy'),allow_pickle=False)
            target=np.load(out/'gpu_smoke'/(new_label+'.npy'),allow_pickle=False)
            anchors=np.arange(8,dtype=np.int64);paid=np.arange(9,dtype=np.int64)
            model=fit_arc2_global(old[:12],anchors,target[anchors])
            gallery=build_mixed_gallery(old[:12],model,paid,target[paid])
            np.testing.assert_array_equal(gallery[paid],target[paid])
            ranked=exact_topk(target[12:],gallery,k=3)
            if ranked.shape!=(4,3):raise AssertionError('Toy search shape')
            path=out/f'toy_{name}_rankings.npy';np.save(path,ranked,allow_pickle=False)
            meta['toy_mixed_gallery_checks'][name]={'status':'PASS','documents':12,'queries':4,
                'fit_pairs':8,'paid_documents':9,'proxy_documents':3,'top_k':3,
                'ranking_sha256':sha(path),'scope':'synthetic texts; no relevance claim'}
        meta['status']='B1A_INPUTS_AND_GPU_SMOKE_PASS'
        meta['next_action']='STOP: report B1a and wait for user confirmation before B1b'
    except BaseException as e:
        meta.update(status='FAILED_PRESERVED',failures=[repr(e)],traceback=traceback.format_exc())
    finally:
        monitor.end();meta.update(wall_seconds=time.perf_counter()-began,
            peak_process_tree_rss_bytes=monitor.peak,ended_utc=datetime.now(timezone.utc).isoformat())
        dump(out/'metadata.json',meta)
    print(json.dumps({'status':meta['status'],'output':str(out),'failures':meta['failures']}))
    return 0 if meta['status']=='B1A_INPUTS_AND_GPU_SMOKE_PASS' else 1

if __name__=='__main__':raise SystemExit(main())
