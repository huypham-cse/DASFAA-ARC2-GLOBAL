"""Locked six-configuration DEV mechanism study and real fixed-anchor P0 checks."""
import argparse,hashlib,json,os,shutil,signal,subprocess,sys,time,traceback
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import scipy
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src'),str(ROOT/'ops')]
from b1a_stage import Observations,dump,sha,check_sources,read_parquet
from arc2_global import fit_arc2_global,transform_old_docs,normalize_rows,select_for_budget
from arc2_global.numerics import apply_affine
from arc2_global.procrustes import procrustes_apply
from arc2_global.retrieval import exact_topk
from arc2_global.baseline_adapters import fit_ridge
from arc2_global.mechanism_ablation import fit_tangent_path

PRIMARY='arc2_global_tangent2_r1'
METHODS=['procrustes_global','tangent1_l10',PRIMARY,'tangent2_l1','tangent2_l100','ridge_affine_l10_bias_regularized']
PAIRS={'minilm_distilroberta':('minilm_x','distilroberta_y'),'e5_small_base':('e5_small_x','e5_base_y')}
BUDGETS=[('25pct',.25),('50pct',.5),('75pct',.75)]

def save(path,array):
    path.parent.mkdir(parents=True,exist_ok=True);np.save(path,array,allow_pickle=False)
    return sha(path)

def map_blocks(old,fn):
    return np.concatenate([fn(old[s:s+512]) for s in range(0,len(old),512)])

def fit_paths(x,y,anchors):
    began=time.perf_counter();frozen=fit_arc2_global(x,anchors,y)
    phases={'frozen_fit_seconds':time.perf_counter()-began}
    diagnostic=fit_tangent_path(x[anchors],y,ridge_lambda=10.)
    np.testing.assert_array_equal(diagnostic['one'],frozen.one_step_coef)
    np.testing.assert_array_equal(diagnostic['two'],frozen.arc2_coef)
    paths={PRIMARY:lambda b:apply_affine(b,frozen.arc2_coef),
           'tangent1_l10':lambda b:apply_affine(b,frozen.one_step_coef),
           'procrustes_global':lambda b:normalize_rows(procrustes_apply(b,frozen.source_mean,frozen.target_mean,frozen.matrix))}
    phases['tangent_l10_diagnostic']=diagnostic['phases']
    parameters={'procrustes_source_mean':frozen.source_mean,'procrustes_target_mean':frozen.target_mean,'procrustes_matrix':frozen.matrix,'base_float64':frozen.base_coef,'frozen_two':frozen.arc2_coef,'one_l10':frozen.one_step_coef,'dual_first_float64':diagnostic['float64_steps'][0],'dual_final_float64':diagnostic['float64_steps'][1]}
    for lam,name in [(1.,'tangent2_l1'),(100.,'tangent2_l100')]:
        a=fit_tangent_path(x[anchors],y,ridge_lambda=lam)
        paths[name]=lambda b,c=a['two']:apply_affine(b,c)
        phases[name]=a['phases']
        parameters[name]=a['two']
    began=time.perf_counter();ridge=fit_ridge(x[anchors],y)
    phases['ridge_fit_seconds']=time.perf_counter()-began
    paths['ridge_affine_l10_bias_regularized']=ridge.transform
    parameters['ridge_affine_l10_bias_regularized']=ridge.coefficient
    diagnostic['parameters']=parameters
    return frozen,diagnostic,paths,phases

def synthetic_smoke(out):
    from b1m_score import synthetic_checks
    rng=np.random.default_rng(17)
    x=normalize_rows(rng.normal(size=(192,384)).astype(np.float32))
    y=normalize_rows((x@rng.normal(size=(384,768)).astype(np.float32)+.1).astype(np.float32))
    anchors=np.arange(64);f,d,paths,phases=fit_paths(x,y[anchors],anchors)
    q=normalize_rows(rng.normal(size=(8,768)).astype(np.float32));records={}
    paid=select_for_budget(anchors,np.arange(192),n_docs=192,fraction=.5)
    for name,fn in paths.items():
        proxy=map_blocks(x,fn);gallery=proxy.copy();gallery[paid]=y[paid]
        ranking=exact_topk(q,gallery,k=100)
        assert np.isfinite(proxy).all() and np.array_equal(gallery[paid],y[paid])
        save(out/(name+'.npy'),ranking);records[name]=list(ranking.shape)
    mapped=map_blocks(x,lambda b:apply_affine(b,f.arc2_coef))
    np.testing.assert_array_equal(mapped,transform_old_docs(x,f))
    check=synthetic_checks()
    return {'status':'B1M_SYNTHETIC_SMOKE_PASS','configurations':records,'scorer_checks':check,'phases':phases}

def prepare_inputs(lock,out):
    b1a=Path(lock['b1a_run']);metadata=json.loads((b1a/'metadata.json').read_text())
    assert sha(b1a/'metadata.json')==lock['b1a_metadata_sha256']
    for dataset in lock['nano_datasets']:
        src=b1a/'inputs'/dataset;dst=out/'inputs'/dataset;dst.mkdir(parents=True)
        for rec in metadata['nano'][dataset]['files'].values():assert sha(Path(rec['path']))==rec['sha256']
        docs=read_parquet(src/'corpus/train-00000-of-00001.parquet')
        queries=read_parquet(src/'queries/train-00000-of-00001.parquet')
        ids={'doc_ids':[r['_id'] for r in docs],'query_ids':[r['_id'] for r in queries],'row_order':'lexicographic string IDs'}
        assert ids==json.loads((src/'ids.json').read_text())
        dump(dst/'ids.json',ids);dump(dst/'texts.json',{'docs':[r['text'] for r in docs],'queries':[r['text'] for r in queries]})
        for recs in ['anchor_order_files','paid_sets']:
            for name,rec in metadata['nano'][dataset][recs].items():
                assert sha(src/name)==rec['sha256'];shutil.copyfile(src/name,dst/name)
    dst=out/'inputs/FiQA';dst.mkdir(parents=True)
    manifest_path=Path(lock['fiqa']['manifest_path']);assert sha(manifest_path)==lock['fiqa']['manifest_sha256']
    manifest=json.loads(manifest_path.read_text());source=ROOT/'results/fiqa_development'
    assert sha(Path(manifest['ids']['path']))==manifest['ids']['sha256']
    assert json.loads((source/'ids.json').read_text())==json.loads(Path(manifest['ids']['path']).read_text())
    shutil.copyfile(source/'ids.json',dst/'ids.json')
    order=np.load(source/'backfill_order.npy',allow_pickle=False)
    for seed in lock['seeds']:
        anchors=np.load(source/f'selections/anchors_seed_{seed}.npy',allow_pickle=False)
        save(dst/f'anchors_seed{seed}.npy',anchors);save(dst/f'order_seed{seed}.npy',order)
        for budget,fraction in BUDGETS:
            selected=select_for_budget(anchors,order,n_docs=57638,fraction=fraction)
            if fraction<.75:np.testing.assert_array_equal(selected,np.load(source/f'selections/seed{seed}_{budget}.npy',allow_pickle=False))
            save(dst/f'paid_seed{seed}_{budget}.npy',selected)
    for pair,roles in manifest['vectors'].items():
        for role,rec in roles.items():
            assert sha(Path(rec['path']))==rec['sha256']
            arr=np.load(rec['path'],mmap_mode='r',allow_pickle=False)
            assert list(arr.shape)==rec['shape'] and arr.dtype==np.float32
    return manifest

def run_full(lock,out,meta):
    from arc2_global.solver_backend import tangent2_primal,compare_ranking_drift,BACKEND_ID
    manifest=prepare_inputs(lock,out)
    env={**os.environ,'CUBLAS_WORKSPACE_CONFIG':':4096:8','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
    dump(out/'progress.json',{'stage':'NANO_ENCODING','cells':0})
    with (out/'encode.stdout.log').open('w') as stdout,(out/'encode.stderr.log').open('w') as stderr:
        child=subprocess.run([lock['gpu_python'],'-u',str(ROOT/'ops/b1m_encode.py'),'--lock',str(ROOT/'configs/b1m_lock.json'),'--run',str(out)],env=env,stdout=stdout,stderr=stderr)
    if child.returncode:raise RuntimeError('Nano encoding failed; logs preserved')
    encoding=json.loads((out/'encoding/metadata.json').read_text());assert encoding['status']=='ENCODING_PASS'
    meta['encoding']=encoding;dump(out/'metadata.json',meta)
    source_index=json.loads((ROOT/'results/fiqa_development/metric_index.json').read_text())['cells']
    reusable={}
    for c in source_index:
        method={ 'procrustes_tangent2_global':PRIMARY}.get(c['method'],c['method'])
        if method in ['procrustes_global',PRIMARY,'full_x','full_y']:
            key=(c['pair'],method,c['seed'],'full' if c['seed'] is None else c['budget'])
            reusable[key]=c
    cells=[];p0=[];fitrows=[];reuse_receipts=[]
    def rank(dataset,pair,method,seed,budget,q,g,ids,**extra):
        began=time.perf_counter();ranking=exact_topk(q,g,k=100,batch_rows=16,query_ids=ids['query_ids'],document_ids=ids['doc_ids'],exclude_identical_ids=True)
        seconds=time.perf_counter()-began
        rel=f'rankings/{dataset}_{pair}_{method}_seed{seed}_{budget}.npy';path=out/rel;reused=False
        prior=reusable.get((pair,method,seed,budget)) if dataset=='FiQA' else None
        if prior:
            p=ROOT/'results/fiqa_development'/prior['ranking_path'];assert sha(p)==prior['ranking_sha256']
            previous=np.load(p,allow_pickle=False);reused=np.array_equal(ranking,previous)
            reuse_receipts.append({'pair':pair,'method':method,'seed':seed,'budget':budget,'ranked_ids_exact':reused,'changed_queries':int(np.any(ranking!=previous,axis=1).sum()),'source_ranking_sha256':sha(p)})
            if reused:path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,path)
        if not reused:save(path,ranking)
        cells.append({'dataset':dataset,'pair':pair,'method':method,'seed':seed,'budget':budget,'ranking_path':rel,'ranking_sha256':sha(path),'search_seconds':seconds,'reused_after_qrel_free_identity_check':reused,**extra})
        dump(out/'cells_pre_qrels.json',cells);dump(out/'progress.json',{'stage':'RANKING','cells':len(cells),'total':736,'dataset':dataset,'pair':pair,'method':method,'seed':seed})
    for dataset in [*lock['nano_datasets'],'FiQA']:
        ids=json.loads((out/'inputs'/dataset/'ids.json').read_text())
        for pair,(oldlabel,newlabel) in PAIRS.items():
            if dataset=='FiQA':
                arrays={role:np.load(rec['path'],mmap_mode='r',allow_pickle=False) for role,rec in manifest['vectors'][pair].items()}
            else:
                folder=out/'vectors'/dataset
                arrays={role:np.load(folder/f'{label}_{kind}.npy',mmap_mode='r',allow_pickle=False) for role,label,kind in [('old_docs',oldlabel,'docs'),('old_queries',oldlabel,'queries'),('new_docs',newlabel,'docs'),('new_queries',newlabel,'queries')]}
            old,new,q=arrays['old_docs'],arrays['new_docs'],arrays['new_queries']
            rank(dataset,pair,'full_x',None,'full',arrays['old_queries'],old,ids,unique_destination_encodings=0)
            rank(dataset,pair,'full_y',None,'full',q,new,ids,unique_destination_encodings=len(old))
            for seed in lock['seeds']:
                folder=out/'inputs'/dataset;anchors=np.load(folder/f'anchors_seed{seed}.npy',allow_pickle=False)
                fitted,diag,paths,phases=fit_paths(old,new[anchors],anchors)
                start=time.perf_counter();primal64=tangent2_primal(old[anchors],new[anchors],fitted.base_coef,return_float64=True)
                primal_seconds=time.perf_counter()-start
                for i,(a,b) in enumerate(zip(primal64,diag['float64_steps'])):
                    assert np.allclose(a,b,atol=1e-9,rtol=1e-9),('primal64',dataset,pair,seed,i)
                began=time.perf_counter();primary=map_blocks(old,paths[PRIMARY]);primary_mapping_seconds=time.perf_counter()-began
                primal=map_blocks(old,lambda b:apply_affine(b,primal64[1].astype(np.float32)))
                delta=float(np.max(np.abs(primary-primal)));assert delta<=1e-6
                base_record={'dataset':dataset,'pair':pair,'seed':seed,'backend_id':BACKEND_ID,'anchors':1024,'proxy_maxabs':delta,'coefficient_maxabs':float(np.max(np.abs(fitted.arc2_coef-primal64[1].astype(np.float32)))),'float64_step_maxabs':[float(np.max(np.abs(a-b))) for a,b in zip(primal64,diag['float64_steps'])],'float64_step_relative_frobenius':[float(np.linalg.norm(a-b)/np.linalg.norm(b)) for a,b in zip(primal64,diag['float64_steps'])],'primal_fit_seconds':primal_seconds}
                assert base_record['coefficient_maxabs']<=1e-6
                coefdir=out/'coefficients'/f'{dataset}_{pair}_seed{seed}';coefdir.mkdir(parents=True)
                np.savez_compressed(coefdir/'parameters.npz',**diag['parameters'],primal_first_float64=primal64[0],primal_final_float64=primal64[1],primal_two=primal64[1].astype(np.float32))
                base_record['parameters_path']=(coefdir/'parameters.npz').relative_to(out).as_posix();base_record['parameters_sha256']=sha(coefdir/'parameters.npz')
                fitrows.append({'dataset':dataset,'pair':pair,'seed':seed,'phases':phases,'note':'one-step shares frozen two-step work; diagnostic recomputation recorded separately'})
                for method in METHODS:
                    began=time.perf_counter();proxy=primary if method==PRIMARY else map_blocks(old,paths[method]);mapping=primary_mapping_seconds if method==PRIMARY else time.perf_counter()-began
                    for budget,fraction in BUDGETS:
                        paid=np.load(folder/f'paid_seed{seed}_{budget}.npy',allow_pickle=False)
                        assert len(paid)==int(fraction*len(old)) and set(anchors)<=set(paid)
                        gallery=proxy.copy();gallery[paid]=new[paid]
                        rank(dataset,pair,method,seed,budget,q,gallery,ids,unique_destination_encodings=len(paid),anchor_count=1024,mapping_seconds=mapping)
                        if method==PRIMARY:
                            candidate=primal.copy();candidate[paid]=new[paid]
                            drift=compare_ranking_drift(q,gallery,candidate,k=100,batch_rows=16,query_ids=ids['query_ids'],document_ids=ids['doc_ids'],exclude_identical_ids=True)
                            drift['top10_queries_with_difference']=sum(r['reference_top_ids'][:10]!=r['actual_top_ids'][:10] for r in drift['mismatches'])
                            drift['top10_queries_with_membership_difference']=sum(set(r['reference_top_ids'][:10])!=set(r['actual_top_ids'][:10]) for r in drift['mismatches'])
                            # Unexplained rank differences are retained and fail readiness.
                            p0.append({**base_record,'budget':budget,'ranking_drift':drift})
                            dump(out/'p0_real_checks.json',p0)
                            if drift['score_maxabs']>1e-6 or drift['unexplained_inversion_count']!=0:raise AssertionError('Primal ranking drift gate failed')
                dump(out/'fit_phases.json',fitrows);dump(out/'reuse_checks.json',reuse_receipts)
    assert len(cells)==736 and len(p0)==120
    inputs={p.relative_to(out).as_posix():sha(p) for p in (out/'inputs').rglob('*') if p.is_file()}
    vector_hashes={p.relative_to(out).as_posix():sha(p) for p in (out/'vectors').rglob('*.npy')}
    seal={'status':'RANKINGS_SEALED','sealed_unix':time.time(),'cells':cells,'inputs':inputs,'vector_hashes':vector_hashes,'qrels_opened':False,'primary_method':PRIMARY}
    dump(out/'ranking_seal.json',seal)
    meta.update(status='RANKINGS_SEALED',ranking_seal_sha256=sha(out/'ranking_seal.json'),ranking_count=736,p0_real_checks=120,reused_rankings=sum(c['reused_after_qrel_free_identity_check'] for c in cells),new_qrel_reads=0)
    dump(out/'metadata.json',meta)
    with (out/'scorer.stdout.log').open('w') as stdout,(out/'scorer.stderr.log').open('w') as stderr:
        child=subprocess.run([sys.executable,str(ROOT/'ops/b1m_score.py'),'--lock',str(ROOT/'configs/b1m_lock.json'),'--run',str(out)],stdout=stdout,stderr=stderr)
    if child.returncode:raise RuntimeError('DEV scoring failed; preserve sealed rankings and logs')
    meta.update(status='B1M_AND_REAL_P0_PASS',new_qrel_reads=4,scoring_directory='scoring',next_action='STOP before B1-P/B1-G/main breadth/TREC; report both authorized items')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['smoke','full'],required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--code-commit',required=True);ap.add_argument('--smoke',type=Path);ap.add_argument('--p0-smoke',type=Path);a=ap.parse_args()
    out=a.output.resolve();assert out.parent==(ROOT/'results').resolve() and out.name.startswith('b1m_');out.mkdir(exist_ok=False)
    lock=json.loads((ROOT/'configs/b1m_lock.json').read_text());began=time.perf_counter();monitor=Observations(out);monitor.begin()
    meta={'status':'RUNNING','stage':a.stage,'code_commit':a.code_commit,'lock_sha256':sha(ROOT/'configs/b1m_lock.json'),'started_utc':datetime.now(timezone.utc).isoformat(),'failures':[],'new_qrel_reads':0,'TREC_access':False,'artificial_caps':None};dump(out/'metadata.json',meta)
    def interrupted(sig,frame):raise RuntimeError(f'Received signal {sig}')
    signal.signal(signal.SIGTERM,interrupted)
    try:
        check_sources(lock,a.code_commit)
        for rel,digest in lock['packaged_file_sha256'].items():assert sha(ROOT/rel)==digest,rel
        assert {'numpy':np.__version__,'scipy':scipy.__version__}==lock['cpu_versions']
        assert {k:os.environ.get(k) for k in lock['cpu_environment']}==lock['cpu_environment']
        from threadpoolctl import threadpool_info
        meta['runtime']={'numpy':np.__version__,'scipy':scipy.__version__,'executable':sys.executable,'environment':lock['cpu_environment'],'module_origins':{'numpy':np.__file__,'scipy':scipy.__file__},'blas':threadpool_info()}
        if a.stage=='smoke':meta.update(synthetic=synthetic_smoke(out),status='B1M_SMOKE_PASS')
        else:
            assert a.smoke and json.loads((a.smoke/'metadata.json').read_text())['status']=='B1M_SMOKE_PASS'
            assert a.p0_smoke and json.loads((a.p0_smoke/'metadata.json').read_text())['status']=='B1P0_SMOKE_PASS'
            run_full(lock,out,meta)
    except BaseException as exc:meta.update(status='FAILED_PRESERVED',failures=[repr(exc)],traceback=traceback.format_exc())
    finally:
        monitor.end();meta.update(ended_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.perf_counter()-began,peak_process_tree_rss_bytes=monitor.peak);dump(out/'metadata.json',meta)
    print(json.dumps({'status':meta['status'],'failures':meta['failures']}));return 0 if meta['status'] in ['B1M_SMOKE_PASS','B1M_AND_REAL_P0_PASS'] else 1
if __name__=='__main__':raise SystemExit(main())
