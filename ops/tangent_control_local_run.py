"""TC1L: original fit arithmetic, one disk-backed gallery, no qrel access."""
import argparse
import gc
import json
import os
from pathlib import Path
import platform
import shutil
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from tangent_control_run import sha,dump,save,utc,verify_code,Resources,synthetic


def checked_inputs(lock):
    found={}
    for spec in [*lock['data'].values(),*lock['anchors'].values(),*lock['paid50'].values(),lock['ids']]:
        p=Path(spec['path']);p=p if p.is_absolute() else ROOT/p
        if sha(p)!=spec['sha256']:raise ValueError('Changed local input: '+str(p))
        found[str(p.resolve())]=spec['sha256']
    return found


def rank_mmap(queries,gallery,ids):
    """Same full-document float32 q16 matmul and stable sort as exact_topk."""
    import numpy as np
    from arc2_global.numerics import _vectors
    q=_vectors('queries',queries,dim=gallery.shape[1])
    positions={doc:i for i,doc in enumerate(ids['doc_ids'])}
    ranks=np.empty((len(q),100),dtype=np.int64)
    for start in range(0,len(q),16):
        scores=q[start:start+16]@gallery.T
        for j,qid in enumerate(ids['query_ids'][start:start+len(scores)]):
            if qid in positions:scores[j,positions[qid]]=-np.inf
        if np.any(np.isfinite(scores).sum(axis=1)<100):raise ValueError('Not enough eligible hits')
        ranks[start:start+len(scores)]=np.argsort(-scores,axis=1,kind='stable')[:,:100]
    return ranks


def synthetic_local(out):
    import numpy as np
    from arc2_global.numerics import normalize_rows,_indices
    from arc2_global.retrieval import exact_topk
    result=synthetic()
    rng=np.random.default_rng(20261102)
    docs=normalize_rows(rng.normal(size=(130,7)).astype(np.float32))
    docs[1]=docs[0]  # repeated rows exercise stable exact ties
    q=docs[:19].copy()
    ids={'doc_ids':[str(i) for i in range(130)],'query_ids':[str(i) for i in range(19)]}
    path=out/'synthetic_gallery.npy'
    mm=np.lib.format.open_memmap(path,mode='w+',dtype=np.float32,shape=docs.shape)
    mm[:]=docs;mm.flush()
    actual=rank_mmap(q,mm,ids)
    expected=exact_topk(q,docs,k=100,batch_rows=16,query_ids=ids['query_ids'],document_ids=ids['doc_ids'],exclude_identical_ids=True)
    np.testing.assert_array_equal(actual,expected)
    mm._mmap.close();del mm
    for bad in [np.array([-1]),np.array([0,0]),np.array([130])]:
        try:_indices('bad',bad,130)
        except ValueError:continue
        raise AssertionError('Bad indices accepted')
    result['local_checks']=['mmap_inmemory_rank_bitwise_q16','identical_id_exclusion','stable_duplicate_ties','negative_duplicate_oob_rejection']
    return result


def diagnostics_blocks(old,coefficients,paid):
    import numpy as np
    from arc2_global.numerics import apply_affine
    keys=['tangent2','chordal2','euclidean2']
    cos={k:[] for k in keys};max_b0={k:0. for k in keys};max_t={k:0. for k in ['procrustes','chordal2','euclidean2']}
    for start in range(0,len(old),512):
        stop=min(start+512,len(old));rows=np.arange(start,stop)
        unpaid=~np.isin(rows,paid)
        if not np.any(unpaid):continue
        block={k:apply_affine(old[start:stop],v)[unpaid] for k,v in coefficients.items()}
        for k in keys:
            cos[k].append(np.sum(block[k].astype(np.float64)*block['procrustes'],axis=1))
            max_b0[k]=max(max_b0[k],float(np.max(np.abs(block[k]-block['procrustes']))))
        for k in max_t:max_t[k]=max(max_t[k],float(np.max(np.abs(block[k]-block['tangent2']))))
    return {'unpaid_cosine_to_B0_quantiles':{k:np.quantile(np.concatenate(v),[0,.25,.5,.75,1]).tolist() for k,v in cos.items()},
            'unpaid_maxabs_to_B0':max_b0,'unpaid_maxabs_to_tangent':max_t}


def scientific(lock,out,stage):
    import numpy as np
    from arc2_global.residual_ablation import fit_controls
    from arc2_global.model import _tangent2
    from arc2_global.numerics import _vectors,_indices,apply_affine
    registry=checked_inputs(lock)
    dump(out/'verified_inputs.json',registry)
    idpath=Path(lock['ids']['path']);idpath=idpath if idpath.is_absolute() else ROOT/idpath
    shutil.copyfile(idpath,out/'ids.json');ids=json.loads(idpath.read_text())
    def load(spec):
        p=Path(spec['path']);return np.load(p if p.is_absolute() else ROOT/p,mmap_mode='r',allow_pickle=False)
    old=load(lock['data']['old_docs']);new=load(lock['data']['new_docs']);q=load(lock['data']['new_queries'])
    if old.shape!=(57638,384) or new.shape!=(57638,768) or q.shape!=(500,768):raise ValueError('Unexpected vector shape')
    if any(a.dtype!=np.float32 for a in [old,new,q]):raise ValueError('Expected float32 caches')
    _vectors('destination_queries',q,dim=768)
    cells=[];scratch=out/'scratch';scratch.mkdir()
    seeds=[17] if stage=='smoke' else lock['seeds']
    for seed in seeds:
        folder=out/('minilm_distilroberta_seed'+str(seed));folder.mkdir()
        a=_indices('anchors',np.asarray(load(lock['anchors'][str(seed)])),len(old))
        paid=_indices('paid50',np.asarray(load(lock['paid50'][str(seed)])),len(old))
        if len(a)!=1024 or len(paid)!=28819 or not np.array_equal(paid,np.unique(paid)) or not set(a)<=set(paid):
            raise ValueError('Incorrect anchor-inclusive exposure')
        # Only the paid anchors, and later paid replacement blocks, are read
        # numerically from the full destination document cache.
        target_anchors=np.array(new[a],dtype=np.float32)
        fitted=fit_controls(np.asarray(old[a]),target_anchors)
        one,two=_tangent2(np.asarray(old[a]),target_anchors,fitted['base_float64'])
        np.testing.assert_array_equal(one,fitted['float64_steps']['tangent2'][0].astype(np.float32))
        np.testing.assert_array_equal(two,fitted['coefficients']['tangent2'])
        arrays={**fitted['coefficients'],'base_float64':fitted['base_float64']}
        for m,states in fitted['float64_steps'].items():
            for i,b in enumerate(states,1):arrays[m+'_step'+str(i)+'_float64']=b
        with (folder/'parameters.npz').open('xb') as stream:np.savez(stream,**arrays)
        save(folder/'anchors.npy',a);save(folder/'paid50.npy',paid)
        diag={k:fitted[k] for k in ['shared_procrustes_seconds','shared_dual_factor_seconds','trajectories']}
        diag['unpaid']=diagnostics_blocks(old,fitted['coefficients'],paid)
        if stage=='smoke' and any(diag['unpaid']['unpaid_maxabs_to_tangent'][m]==0 for m in ['chordal2','euclidean2']):
            dump(folder/'diagnostics.json',diag)
            raise RuntimeError('SMOKE_DEGENERATE_STOP; no changing controls to manufacture effects')
        diag.update(physical_encodings_this_run=0,logical_paid_documents=28819,fit_pairs=1024,methods={})
        for method,coef in fitted['coefficients'].items():
            path=scratch/(str(seed)+'_'+method+'_gallery.npy')
            if path.exists():raise FileExistsError('Preserve existing scratch')
            gallery=np.lib.format.open_memmap(path,mode='w+',dtype=np.float32,shape=(57638,768))
            success=False
            try:
                began=time.perf_counter()
                for start in range(0,len(old),512):
                    stop=min(start+512,len(old))
                    _vectors('source_block',old[start:stop],dim=384)
                    block=apply_affine(old[start:stop],coef)
                    p0,p1=np.searchsorted(paid,[start,stop]);selected=paid[p0:p1]
                    if len(selected):
                        exact=np.array(new[selected],dtype=np.float32)
                        _vectors('paid_target_block',exact,dim=768);block[selected-start]=exact
                    gallery[start:stop]=block
                gallery.flush();mapping=time.perf_counter()-began
                began=time.perf_counter();ranks=rank_mmap(q,gallery,ids);search=time.perf_counter()-began
                rp=folder/(method+'_rankings.npy');save(rp,ranks)
                cells.append({'pair':'minilm_distilroberta','seed':seed,'method':method,'budget':'50pct',
                              'ranking_path':rp.relative_to(out).as_posix(),'sha256':sha(rp),'shape':list(ranks.shape),
                              'map_seconds':mapping,'search_seconds':search})
                diag['methods'][method]={'map_seconds_including_mmap_flush':mapping,'search_seconds':search}
                dump(out/'progress.json',{'utc':utc(),'stage':stage,'rankings':len(cells),'expected':4 if stage=='smoke' else 20,'latest':str(seed)+'/'+method})
                print(json.dumps({'rankings':len(cells),'latest':str(seed)+'/'+method}),flush=True)
                success=True
            finally:
                gallery._mmap.close();del gallery;gc.collect()
                if success:
                    if not path.resolve().is_relative_to(scratch.resolve()):raise ValueError('Escaping scratch path')
                    path.unlink()  # only this new, successful arm's documented scratch file
        for method in ['procrustes','chordal2','euclidean2']:
            left=np.load(folder/'tangent2_rankings.npy',allow_pickle=False);right=np.load(folder/(method+'_rankings.npy'),allow_pickle=False)
            diag['methods'][method]['changed_top10_queries_vs_tangent']=int(np.any(left[:,:10]!=right[:,:10],axis=1).sum())
            diag['methods'][method]['changed_top100_queries_vs_tangent']=int(np.any(left!=right,axis=1).sum())
        dump(folder/'diagnostics.json',diag)
        del fitted,arrays;gc.collect()
    expected=4 if stage=='smoke' else 20
    if len(cells)!=expected:raise ValueError('Incomplete local matrix')
    dump(out/'ranking_seal.json',{'utc':utc(),'stage':stage,'lock_sha256':sha(ROOT/lock['_lock_path']),
         'cells':cells,'input_hashes':registry,'artifacts':{p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file() and p.name not in ['metadata.json','progress.json','resources.jsonl']}})
    return {'status':stage.upper()+'_SEALED','rankings':len(cells),'qrels_opened':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lock',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--stage',choices=['synthetic','smoke','full'],required=True)
    args=ap.parse_args();lock=json.loads((ROOT/args.lock).read_text());verify_code(lock);lock['_lock_path']=args.lock
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
    meta={'status':'RUNNING','utc_start':utc(),'stage':args.stage,'lock_sha256':sha(ROOT/args.lock),
          'host':platform.node(),'python':sys.version,'platform':platform.platform(),'pid':os.getpid(),
          'scope':'TC1L MiniLM local development; E5 pending','qrels_opened':False}
    resources=Resources(out);began=time.perf_counter()
    try:
        import numpy,scipy
        from threadpoolctl import threadpool_info,threadpool_limits
        meta.update(numpy=numpy.__version__,scipy=scipy.__version__)
        if (meta['numpy']!=lock['runtime']['numpy'] or meta['scipy']!=lock['runtime']['scipy'] or
                sys.version!=lock['runtime']['python'] or platform.system()!=lock['runtime']['platform']):
            raise ValueError('Local runtime mismatch')
        gates=['synthetic'] if args.stage=='smoke' else ['synthetic','smoke'] if args.stage=='full' else []
        for gate in gates:
            receipts=json.loads((out.parent/'stage_receipts.json').read_text())
            relative=gate+'/metadata.json'
            if sha(out.parent/relative)!=receipts[relative]:raise ValueError('Changed '+gate+' receipt')
            m=json.loads((out.parent/relative).read_text())
            wanted='SYNTHETIC_PASS' if gate=='synthetic' else 'SMOKE_SEALED'
            if m['status']!=wanted or m['lock_sha256']!=meta['lock_sha256']:raise ValueError('Matching '+gate+' not passed')
            if gate=='smoke':
                sealpath=out.parent/'smoke/ranking_seal.json'
                if sha(sealpath)!=receipts['smoke/ranking_seal.json']:raise ValueError('Changed smoke seal')
                seal=json.loads(sealpath.read_text())
                if len(seal['cells'])!=4 or seal['lock_sha256']!=meta['lock_sha256']:raise ValueError('Incomplete smoke seal')
                for relative,h in seal['artifacts'].items():
                    path=(out.parent/'smoke'/relative).resolve()
                    if not path.is_relative_to((out.parent/'smoke').resolve()) or sha(path)!=h:raise ValueError('Changed smoke artifact')
        resources.begin()
        with threadpool_limits(limits=lock['blas_threads']):
            meta['blas']=threadpool_info();dump(out/'metadata.json',meta)
            meta.update(synthetic_local(out) if args.stage=='synthetic' else scientific(lock,out,args.stage))
    except BaseException as exc:
        meta.update(status='FAILED_PRESERVED',error=repr(exc),traceback=traceback.format_exc());raise
    finally:
        if hasattr(resources,'thread'):resources.end()
        meta.update(utc_end=utc(),elapsed_seconds=time.perf_counter()-began,peak_rss_bytes=resources.peak)
        dump(out/'metadata.json',meta);print(json.dumps({k:meta[k] for k in ['status','elapsed_seconds','peak_rss_bytes']}),flush=True)


if __name__=='__main__':main()
