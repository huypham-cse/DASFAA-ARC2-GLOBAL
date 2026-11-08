"""B1-P only: matched fixed/all-paid FiQA fits, exact rankings, separate scoring."""
import argparse,hashlib,json,os,shutil,signal,subprocess,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import scipy
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src'),str(ROOT/'ops')]
from b1a_stage import Observations,dump,sha
from arc2_global import normalize_rows
from arc2_global.model import centered_affine_coefficient,fit_arc2_global
from arc2_global.procrustes import procrustes_fit,procrustes_apply
from arc2_global.numerics import apply_affine
from arc2_global.solver_backend import tangent2_primal,BACKEND_ID
from arc2_global.baseline_adapters import fit_la2m,fit_ridge,mixed_gallery
from arc2_global.retrieval import exact_topk

PRIMARY='arc2_global_tangent2_r1'
PROC='procrustes_global';RIDGE='ridge_affine_l10_bias_regularized';LA2M='la2m20_integration_script_adaptation';SIMPLE='simplelinear_official_final50_mlp5';CONVERTER='embedding_converter_paper_spec'
METHODS=[PROC,PRIMARY,LA2M,SIMPLE,RIDGE,CONVERTER]
PAIRS=['minilm_distilroberta','e5_small_base']

def save(path,values):
    path.parent.mkdir(parents=True,exist_ok=True);np.save(path,values,allow_pickle=False);return sha(path)

def map_blocks(source,fn):
    return np.concatenate([fn(source[s:s+512]) for s in range(0,len(source),512)])


def run_observed_child(argv,env,directory,request_sha256=None):
    directory.mkdir(parents=True,exist_ok=True)
    row={'status':'STARTING','started_utc':datetime.now(timezone.utc).isoformat(),'request_sha256':request_sha256,'argv':argv}
    def events():
        path=Path('/sys/fs/cgroup/memory.events')
        return path.read_text() if path.exists() else None
    row['cgroup_memory_events_before']=events()
    with (directory/'stdout.log').open('x') as stdout,(directory/'stderr.log').open('x') as stderr:
        process=subprocess.Popen(argv,env=env,stdout=stdout,stderr=stderr)
        row.update(status='RUNNING',pid=process.pid);dump(directory/'process_exit.json',row)
        code=process.wait()
    row.update(status='EXITED',returncode=code,signal_number=-code if code<0 else None,
        signal_name=signal.Signals(-code).name if code<0 else None,ended_utc=datetime.now(timezone.utc).isoformat(),
        stdout_sha256=sha(directory/'stdout.log'),stderr_sha256=sha(directory/'stderr.log'),cgroup_memory_events_after=events())
    dump(directory/'process_exit.json',row)
    return row

def check_identity(lock,commit):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==commit
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    assert {'numpy':np.__version__,'scipy':scipy.__version__}==lock['cpu_versions']
    import sklearn
    assert sklearn.__version__==lock['cpu_sklearn_version']
    for k,v in lock['cpu_environment'].items():assert os.environ.get(k)==v,k
    for rel,d in lock['source_sha256_canonical_lf'].items():assert hashlib.sha256((ROOT/rel).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==d,rel

def cpu_fit(method,old,target,fit_ids,seed,output):
    began=time.perf_counter();x=np.asarray(old[fit_ids]);y=np.asarray(target[fit_ids]);params={};phases={}
    if method in [PROC,PRIMARY]:
        t=time.perf_counter();sm,tm,w=procrustes_fit(x,y,center=True);phases['procrustes_seconds']=time.perf_counter()-t
        params.update(source_mean=sm,target_mean=tm,matrix=w)
        if method==PROC:fn=lambda b:normalize_rows(procrustes_apply(b,sm,tm,w))
        else:
            base=centered_affine_coefficient(sm,tm,w);t=time.perf_counter();one,two=tangent2_primal(x,y,base)
            phases['matrix_construction_factor_and_two_updates_seconds']=time.perf_counter()-t
            params.update(base=base,one=one,two=two);fn=lambda b:apply_affine(b,two)
    elif method==RIDGE:
        model=fit_ridge(x,y);params['coefficient']=model.coefficient;fn=model.transform
    elif method==LA2M:
        model=fit_la2m(x,y,seed=seed,n_clusters=20);fn=model.transform
        params.update(centroids=model.kmeans.cluster_centers_,anchor_labels=model.anchor_labels,global_source_mean=model.global_map[0],global_target_mean=model.global_map[1],global_matrix=model.global_map[2])
        for c,v in model.local_maps.items():
            if v is not None:
                for name,value in zip(['source_mean','target_mean','matrix'],v):params[f'cluster{c}_{name}']=value
    else:raise ValueError(method)
    fit_seconds=time.perf_counter()-began;output.mkdir(parents=True,exist_ok=False)
    np.savez_compressed(output/'parameters.npz',**params)
    t=time.perf_counter();proxy=map_blocks(old,fn);mapping_seconds=time.perf_counter()-t
    assert np.isfinite(proxy).all() and np.allclose(np.linalg.norm(proxy,axis=1),1,atol=1e-4,rtol=0)
    record={'status':'CPU_FIT_PASS','method':method,'fit_pairs':len(fit_ids),'fit_seconds':fit_seconds,'mapping_seconds':mapping_seconds,'phases':phases,'parameters_sha256':sha(output/'parameters.npz'),'backend_id':BACKEND_ID if method==PRIMARY else None,'new_physical_document_encodes':0}
    dump(output/'metadata.json',record);return proxy,record

def neural(lock,commit,out,pair,seed,regime,method,old_path,old,paired_ids,target,mode):
    request_dir=out/'neural'/f'{pair}_seed{seed}_{regime}_{method}';request_dir.mkdir(parents=True)
    x=request_dir/'paired_source.npy';y=request_dir/'paired_target.npy'
    save(x,np.asarray(old[paired_ids]));save(y,np.asarray(target[paired_ids]))
    request={'mode':mode,'method':'embedding_converter' if method==CONVERTER else 'simplelinear','regime':'anchors' if regime=='fixed1024' else 'all_paid','seed':seed,'lockpath':str(ROOT/'configs/b1p_lock.json'),'output':str(request_dir/'worker'),'paired_source':str(x),'paired_target':str(y),'full_source':str(old_path),'code_commit':commit,'input_sha256':{'paired_source':sha(x),'paired_target':sha(y),'full_source':sha(old_path)}}
    resume_key=f'{pair}_seed{seed}_{regime}_{method}'
    if mode=='full' and resume_key in lock.get('resume_checkpoints_by_cell',{}):
        assert method==CONVERTER
        request['resume_checkpoints']=lock['resume_checkpoints_by_cell'][resume_key]
        for item in request['resume_checkpoints'].values():assert sha(Path(item['path']))==item['sha256']
    dump(request_dir/'request.json',request)
    env={**os.environ,**lock['environment'],'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
    current=out/'cells_pre_qrels.json'
    dump(out/'progress.json',{'stage':'NEURAL_FIT','cells':len(json.loads(current.read_text())) if current.exists() else 0,'total':124,'pair':pair,'seed':seed,'regime':regime,'method':method,'worker':str(request_dir/'worker')})
    exit_record=run_observed_child([lock['gpu_python'],'-u',str(ROOT/'ops/b1p_neural_worker.py'),'--request',str(request_dir/'request.json')],env,request_dir,sha(request_dir/'request.json'))
    code=exit_record['returncode']
    if code:raise RuntimeError(f'Neural worker failed: returncode={code}, signal={exit_record["signal_name"]}, path={request_dir}')
    receipt=json.loads((request_dir/'worker/metadata.json').read_text());assert receipt['status']=='B1P_NEURAL_'+mode.upper()+'_PASS'
    return np.load(request_dir/'worker/proxy_full.npy',mmap_mode='r',allow_pickle=False),receipt

def smoke(lock,commit,out):
    from b1m_score import synthetic_checks
    exits=[]
    for name,code,expected in [('exit7','raise SystemExit(7)',7),('sigterm','import os,signal;os.kill(os.getpid(),signal.SIGTERM)',-15)]:
        row=run_observed_child([sys.executable,'-c',code],os.environ.copy(),out/'process_tests'/name)
        assert row['returncode']==expected and row['status']=='EXITED';exits.append(row)
    dump(out/'process_failure_checks.json',{'status':'PASS','expected_nonzero_children':exits})
    rng=np.random.default_rng(17);old=normalize_rows(rng.normal(size=(256,384)).astype(np.float32));target=normalize_rows((old@rng.normal(size=(384,768)).astype(np.float32)+.1).astype(np.float32));query=normalize_rows(rng.normal(size=(8,768)).astype(np.float32));fit=np.arange(128);ids={'doc_ids':[f'd{i}' for i in range(256)],'query_ids':[f'q{i}' for i in range(8)]};oldpath=out/'synthetic_old.npy';save(oldpath,old)
    records=[]
    for method in [PROC,RIDGE,PRIMARY,LA2M,SIMPLE,CONVERTER]:
        if method in [SIMPLE,CONVERTER]:proxy,meta=neural(lock,commit,out,'synthetic',17,'allpaid28819',method,oldpath,old,fit,target,'smoke')
        else:proxy,meta=cpu_fit(method,old,target,fit,17,out/'cpu'/method)
        gallery=mixed_gallery(proxy,fit,target[fit],fit,target[fit]);np.testing.assert_array_equal(gallery[fit],target[fit])
        np.testing.assert_array_equal(gallery[128:],proxy[128:]);ranking=exact_topk(query,gallery,k=100,query_ids=ids['query_ids'],document_ids=ids['doc_ids'],exclude_identical_ids=True)
        path=out/'rankings'/(method+'.npy');save(path,ranking);np.testing.assert_array_equal(np.load(path,allow_pickle=False),ranking)
        records.append({'method':method,'worker':meta,'top100_serialization':'PASS'})
        if method==PRIMARY:
            direct=fit_arc2_global(old,fit,target[fit]);assert np.allclose(direct.arc2_coef,np.load(out/'cpu'/method/'parameters.npz')['two'],atol=1e-6,rtol=0)
    dump(out/'synthetic_scorer_checks.json',synthetic_checks());return records

def prepare(lock,out):
    manifest=Path(lock['fiqa']['manifest_path']);assert sha(manifest)==lock['fiqa']['manifest_sha256'];m=json.loads(manifest.read_text())
    for pair,roles in m['vectors'].items():
        for role,r in roles.items():assert sha(Path(r['path']))==r['sha256'],(pair,role)
    src=Path(lock['b1m_run']);assert sha(src/'ranking_seal.json')==lock['b1m_seal_sha256']
    assert sha(src/'scoring_r2_binary/completed.json')==lock['b1m_scoring_completed_sha256']
    assert json.loads((src/'scoring_r2_binary/completed.json').read_text())['status']=='DEV_SCORED'
    sealed_inputs=json.loads((src/'ranking_seal.json').read_text())['inputs']
    dst=out/'inputs';dst.mkdir()
    for f in (src/'inputs/FiQA').iterdir():
        if f.is_file():
            assert sha(f)==sealed_inputs[f'inputs/FiQA/{f.name}'],f.name
            shutil.copyfile(f,dst/f.name)
    for rel,digest in lock['packaged_file_sha256'].items():
        actual=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT)
        assert hashlib.sha256(actual).hexdigest()==digest,rel
    return m,src,json.loads((src/'ranking_seal.json').read_text()),json.loads((dst/'ids.json').read_text())

def full(lock,commit,out,meta):
    m,source,oldseal,ids=prepare(lock,out);cells=[];reused=[]
    def copy_cell(c,regime,method,src):
        path=src/c['ranking_path'];assert sha(path)==c['ranking_sha256']
        rel=f"rankings/{c['pair']}_seed{c['seed']}_{regime}_{method}.npy";dest=out/rel;dest.parent.mkdir(exist_ok=True);shutil.copyfile(path,dest)
        record={'dataset':'FiQA','pair':c['pair'],'method':method,'regime':regime,'seed':c['seed'],'budget':'full' if c['seed'] is None else '50pct','ranking_path':rel,'ranking_sha256':sha(dest),'reused':True,'source_method':c['method'],'source_path':str(path),'fit_timing':'unavailable as new paired measurement','fit_pairs':0 if c['seed'] is None else 1024,'unique_destination_encodings':c.get('unique_destination_encodings',0)}
        cells.append(record);reused.append(record)
    for c in oldseal['cells']:
        if c['dataset']!='FiQA':continue
        if c['seed'] is None:copy_cell(c,'reference',c['method'],source)
        elif c['budget']=='50pct' and c['method'] in [PROC,PRIMARY,RIDGE]:copy_cell(c,'fixed1024',c['method'],source)
    fiqa=ROOT/'results/fiqa_development'
    for c in json.loads((fiqa/'metric_index.json').read_text())['cells']:
        if c['budget']=='50pct' and c['method']=='embedding_converter_paper_spec_anchor1024':copy_cell(c,'fixed1024',CONVERTER,fiqa)
    assert len(cells)==44;dump(out/'reuse_receipts.json',reused);dump(out/'cells_pre_qrels.json',cells)
    recovery=lock.get('recovery_source')
    if recovery:
        recovered=recover_cells(recovery,out,cells)
        cells.extend(recovered);reused.extend(recovered)
        dump(out/'reuse_receipts.json',reused);dump(out/'cells_pre_qrels.json',cells)
        meta['recovered_successful_cells']=len(recovered)
    def rank(pair,seed,regime,method,query,proxy,target,paid,fit_ids,receipt):
        gallery=mixed_gallery(proxy,fit_ids,np.asarray(target[fit_ids]),paid,np.asarray(target[paid]));began=time.perf_counter()
        ranking=exact_topk(query,gallery,k=100,batch_rows=16,query_ids=ids['query_ids'],document_ids=ids['doc_ids'],exclude_identical_ids=True)
        elapsed=time.perf_counter()-began;rel=f'rankings/{pair}_seed{seed}_{regime}_{method}.npy';digest=save(out/rel,ranking)
        cells.append({'dataset':'FiQA','pair':pair,'seed':seed,'regime':regime,'method':method,'budget':'50pct','ranking_path':rel,'ranking_sha256':digest,'reused':False,'fit_pairs':len(fit_ids),'unique_destination_encodings':len(paid),'search_seconds':elapsed,'fit_receipt':receipt})
        dump(out/'cells_pre_qrels.json',cells);dump(out/'progress.json',{'stage':'RANKING','cells':len(cells),'total':124,'pair':pair,'seed':seed,'regime':regime,'method':method})
    # Serial pair/seed schedule. All-paid converter is the final job of each block.
    for pair in PAIRS:
        specs=m['vectors'][pair];oldpath=Path(specs['old_docs']['path']);old=np.load(oldpath,mmap_mode='r',allow_pickle=False);target=np.load(specs['new_docs']['path'],mmap_mode='r',allow_pickle=False);query=np.load(specs['new_queries']['path'],mmap_mode='r',allow_pickle=False)
        for seed in lock['seeds']:
            paid=np.load(out/f'inputs/paid_seed{seed}_50pct.npy',allow_pickle=False);anchors=np.load(out/f'inputs/anchors_seed{seed}.npy',allow_pickle=False)
            assert len(paid)==28819 and len(anchors)==1024 and set(anchors)<=set(paid)
            for method in [PROC,RIDGE,PRIMARY,LA2M,SIMPLE,CONVERTER]:
                regimes=['fixed1024','allpaid28819'] if method in [LA2M,SIMPLE] else ['allpaid28819']
                for regime in regimes:
                    if any(c['pair']==pair and c['seed']==seed and c['regime']==regime and c['method']==method for c in cells):continue
                    fit=anchors if regime=='fixed1024' else paid
                    if method in [SIMPLE,CONVERTER]:proxy,receipt=neural(lock,commit,out,pair,seed,regime,method,oldpath,old,fit,target,'full')
                    else:
                        dump(out/'progress.json',{'stage':'CPU_FIT','cells':len(cells),'pair':pair,'seed':seed,'regime':regime,'method':method})
                        proxy,receipt=cpu_fit(method,old,target,fit,seed,out/'cpu'/f'{pair}_seed{seed}_{regime}_{method}')
                    rank(pair,seed,regime,method,query,proxy,target,paid,fit,receipt);del proxy
    assert len(cells)==124
    seal={'status':'RANKINGS_SEALED','sealed_unix':time.time(),'cells':cells,'inputs':{p.relative_to(out).as_posix():sha(p) for p in (out/'inputs').rglob('*') if p.is_file()},'qrels_opened':bool(lock.get('dev_label_transport')),'ranking_process_qrel_reads':0,'prior_dev_label_transport':lock.get('dev_label_transport'),'scope':'B1-P DEV only; prior opaque label transport is recorded separately'}
    dump(out/'ranking_seal.json',seal);meta.update(status='RANKINGS_SEALED',ranking_count=124,ranking_seal_sha256=sha(out/'ranking_seal.json'));dump(out/'metadata.json',meta)
    dump(out/'progress.json',{'stage':'DEV_SCORING','cells':124,'total':124})
    with (out/'scorer.stdout.log').open('x') as stdout,(out/'scorer.stderr.log').open('x') as stderr:
        p=subprocess.run([sys.executable,str(ROOT/'ops/b1p_score.py'),'--lock',str(ROOT/'configs/b1p_lock.json'),'--run',str(out)],stdout=stdout,stderr=stderr)
    if p.returncode:raise RuntimeError('Scorer failed; preserve all sealed rankings')
    meta.update(status='B1P_COMPLETE_STOP',new_current_dev_qrel_sources_opened=1,next_action='STOP after B1-P; wait for user before B1-G/main breadth/TREC/systems')
    dump(out/'progress.json',{'stage':'COMPLETE_STOP','cells':124,'total':124})


def recover_cells(spec,out,current):
    """Copy only completed ranks; retain immutable failed attempt and original receipts."""
    manifest_path=Path(spec['manifest_path'])
    assert sha(manifest_path)==spec['manifest_sha256']
    manifest=json.loads(manifest_path.read_text());source=Path(manifest['run'])
    assert manifest['status']=='FAILED_PRESERVED' and manifest['cells']==51 and manifest['new_successful_cells']==7
    assert manifest['qrels_opened'] is False and manifest['code_commit']==spec['code_commit']
    assert not (source/'ranking_seal.json').exists() and not (source/'scoring').exists()
    for relative,item in manifest['files'].items():
        path=(source/relative).resolve();assert path.is_relative_to(source.resolve())
        assert path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],relative
    prior_meta=json.loads((source/'metadata.json').read_text());prior_root=source.parent.parent
    assert prior_meta['status']=='FAILED_PRESERVED' and prior_meta['code_commit']==manifest['code_commit']
    assert prior_meta['lock_sha256']==manifest['lock_sha256']==sha(prior_root/'configs/b1p_lock.json')
    prior_lock=json.loads((prior_root/'configs/b1p_lock.json').read_text());current_lock=json.loads((ROOT/'configs/b1p_lock.json').read_text())
    for field in ['fiqa','seeds','converter_config','simplelinear_defaults','scoring','b1m_run','b1m_seal_sha256','b1m_scoring_completed_sha256']:
        assert prior_lock[field]==current_lock[field],field
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=prior_root,text=True).strip()==manifest['code_commit']
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=prior_root,text=True).strip()
    for relative,digest in prior_lock['source_sha256_canonical_lf'].items():
        assert hashlib.sha256((prior_root/relative).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==digest,relative
    for path in (out/'inputs').iterdir():
        if path.is_file():assert sha(path)==sha(source/'inputs'/path.name),path.name
    old=json.loads((source/'cells_pre_qrels.json').read_text())
    assert len(old)==51
    def identity(c):return tuple(c[k] for k in ['pair','seed','regime','method'])
    seen={identity(c):c for c in current};recovered=[]
    for c in old:
        if c['reused']:
            assert identity(c) in seen and c['ranking_sha256']==seen[identity(c)]['ranking_sha256']
            continue
        assert identity(c) not in seen and c['pair']==PAIRS[0] and c['seed']==17
        assert c['method'] in [PROC,RIDGE,PRIMARY,LA2M,SIMPLE] and c['regime'] in ['fixed1024','allpaid28819']
        src=source/c['ranking_path'];assert sha(src)==c['ranking_sha256']
        values=np.load(src,allow_pickle=False);assert values.shape==(500,100) and values.dtype.kind in 'iu'
        dst=out/c['ranking_path'];assert not dst.exists();shutil.copyfile(src,dst)
        row={**c,'reused':True,'recovery_source_path':str(src),'recovery_source_commit':manifest['code_commit'],
            'fit_timing':'preserved original attempt observation, not a new paired measurement'}
        recovered.append(row);seen[identity(c)]=row
    assert len(recovered)==7 and len(seen)==51
    dump(out/'recovery_verification.json',{'status':'PASS','manifest_sha256':sha(manifest_path),
        'verified_files':len(manifest['files']),'copied_successful_cells':7,'retained_reference_or_imported_cells':44,
        'prior_failed_attempt':str(source),'failed_fit_policy':manifest['failed_fit_policy']})
    return recovered

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['smoke','full'],required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--code-commit',required=True);ap.add_argument('--smoke',type=Path);a=ap.parse_args()
    out=a.output.resolve();assert out.parent==(ROOT/'results').resolve() and out.name.startswith('b1p_');out.mkdir(exist_ok=False)
    lockpath=ROOT/'configs/b1p_lock.json';lock=json.loads(lockpath.read_text());began=time.perf_counter();monitor=Observations(out);monitor.begin()
    meta={'status':'RUNNING','stage':a.stage,'code_commit':a.code_commit,'lock_sha256':sha(lockpath),'started_utc':datetime.now(timezone.utc).isoformat(),'failures':[],'TREC_access':False,'new_physical_document_encodes':0,'artificial_time_memory_caps':None,'new_current_dev_qrel_sources_opened':0}
    dump(out/'metadata.json',meta)
    def interrupted(sig,frame):raise RuntimeError(f'Received signal {sig}')
    signal.signal(signal.SIGTERM,interrupted)
    try:
        check_identity(lock,a.code_commit)
        if a.stage=='full' and lock.get('mini_transport_manifest'):
            spec=lock['mini_transport_manifest'];path=Path(spec['path']);assert sha(path)==spec['sha256']
            transported=json.loads(path.read_text())
            for name,item in transported['files'].items():
                p=Path(name);assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],name
            meta['transported_qrel_free_files_verified']=len(transported['files'])
        if a.stage=='full' and lock.get('dev_label_transport'):
            from b1p_score import verify_dev_transport
            transport=verify_dev_transport(lock)
            meta.update(prior_dev_label_transport=transport,new_current_dev_qrel_sources_opened=1,
                ranking_process_qrel_reads=0,qrels_opened=True)
            dump(out/'metadata.json',meta)
        from threadpoolctl import threadpool_info
        import sklearn
        blas=threadpool_info();numerical_blas=[r for r in blas if r.get('internal_api')=='openblas']
        assert numerical_blas and all(r.get('architecture')=='Haswell' and r['num_threads']==4 for r in numerical_blas),blas
        meta['runtime']={'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__,'python':sys.executable,'environment':lock['cpu_environment'],'blas':blas,'verified_openblas_architecture_threads':True}
        if a.stage=='smoke':meta.update(smoke_checks=smoke(lock,a.code_commit,out),status='B1P_SMOKE_PASS')
        else:
            assert a.smoke;sm=json.loads((a.smoke/'metadata.json').read_text());assert sm['status']=='B1P_SMOKE_PASS' and sm['code_commit']==a.code_commit and sm['lock_sha256']==meta['lock_sha256']
            full(lock,a.code_commit,out,meta)
    except BaseException as exc:meta.update(status='FAILED_PRESERVED',failures=[repr(exc)],traceback=traceback.format_exc())
    finally:monitor.end();meta.update(wall_seconds=time.perf_counter()-began,peak_process_tree_rss_bytes=monitor.peak,ended_utc=datetime.now(timezone.utc).isoformat());dump(out/'metadata.json',meta)
    print(json.dumps({'status':meta['status'],'failures':meta['failures']}));return 0 if meta['status'] in ['B1P_SMOKE_PASS','B1P_COMPLETE_STOP'] else 1
if __name__=='__main__':raise SystemExit(main())
