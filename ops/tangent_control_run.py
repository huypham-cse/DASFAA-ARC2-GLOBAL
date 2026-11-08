"""Qrel-free, unique-directory FiQA matched-residual development experiment."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def save(path, value):
    import numpy as np
    with Path(path).open('xb') as stream:
        np.save(stream, value, allow_pickle=False)


def utc():
    return datetime.now(timezone.utc).isoformat()


def verify_code(lock):
    for name, digest in lock['source_sha256'].items():
        if sha(ROOT / name) != digest:
            raise ValueError('Changed locked source: '+name)


def synthetic():
    import numpy as np
    from scipy.linalg import cho_factor, cho_solve
    from arc2_global.residual_ablation import fit_controls, residual_target, METHODS
    from arc2_global.numerics import normalize_rows, apply_affine
    from arc2_global.model import _tangent2
    from arc2_global.retrieval import exact_topk
    rng = np.random.default_rng(20261102)
    old = normalize_rows(rng.normal(size=(47, 9)).astype(np.float32))
    y = normalize_rows(rng.normal(size=(47, 13)).astype(np.float32))
    fitted = fit_controls(old, y)
    frozen = _tangent2(old, y, fitted['base_float64'])
    for step in range(2):
        np.testing.assert_array_equal(frozen[step], fitted['float64_steps']['tangent2'][step].astype(np.float32))
    x = np.c_[old.astype(np.float64), np.ones(len(old))]
    base = fitted['base_float64']
    z = x @ base
    t, r, u, c = residual_target(z, y.astype(np.float64), 'tangent2')
    chord = residual_target(z, y.astype(np.float64), 'chordal2')[0]
    euclid = residual_target(z, y.astype(np.float64), 'euclidean2')[0]
    np.testing.assert_allclose(chord-t, r*(c-1)*u, atol=1e-10, rtol=1e-10)
    np.testing.assert_allclose(np.sum(t*u, axis=1), 0, atol=1e-10)
    np.testing.assert_allclose(euclid-np.sum(euclid*u, axis=1, keepdims=True)*u, t/r, atol=1e-10)
    primal = cho_factor(x.T@x+10*np.eye(x.shape[1]), lower=True)
    for method in METHODS:
        coef = base.copy()
        for expected in fitted['float64_steps'][method]:
            target = residual_target(x@coef, y.astype(np.float64), method)[0]
            coef += cho_solve(primal, x.T@target)
            np.testing.assert_allclose(coef, expected, atol=1e-10, rtol=1e-10)
        assert max(s['normal_equation_relative_residual'] for s in fitted['trajectories'][method]['steps']) < 1e-10
    for method in ('tangent2', 'chordal2'):
        coef, scaled = base.copy(), 3.7*base
        for _ in range(2):
            coef += cho_solve(primal, x.T@residual_target(x@coef,y,method)[0])
            scaled += cho_solve(primal, x.T@residual_target(x@scaled,y,method)[0])
        np.testing.assert_allclose(scaled, 3.7*coef, atol=1e-10, rtol=1e-10)
    e1, e2 = fitted['float64_steps']['euclidean2']
    np.testing.assert_allclose(e2-e1, 10*cho_solve(primal,e1-base), atol=1e-10, rtol=1e-10)
    aligned=np.array([[2.,0.], [0.,3.]])
    unit=np.array([[1.,0.], [0.,1.]])
    for method in ('tangent2','chordal2'):
        np.testing.assert_allclose(residual_target(aligned,unit,method)[0], 0, atol=1e-10)
    assert np.linalg.norm(residual_target(aligned,unit,'euclidean2')[0]) > 0
    np.testing.assert_allclose(residual_target(aligned,-unit,'tangent2')[0],0,atol=1e-10)
    assert np.linalg.norm(residual_target(aligned,-unit,'chordal2')[0]) > 0
    # A least-squares-stationary prediction has no Euclidean update.
    least= np.linalg.lstsq(x,y,rcond=None)[0]
    np.testing.assert_allclose(x.T@(y-x@least),0,atol=1e-10)
    np.testing.assert_allclose(cho_solve(primal,x.T@(y-x@least)),0,atol=1e-10)
    held=normalize_rows(rng.normal(size=(11,9)).astype(np.float32))
    assert np.max(np.abs(apply_affine(held,fitted['coefficients']['tangent2'])-
                         apply_affine(held,fitted['coefficients']['chordal2']))) > 1e-6
    docs=np.array([[1,0],[1,0],[0,1],[0,1]],dtype=np.float32)
    np.testing.assert_array_equal(exact_topk(docs[:1],docs,k=4),[[0,1,2,3]])
    try:
        residual_target(np.zeros((1,2)),unit[:1],'tangent2')
        raise AssertionError('Zero direction was accepted')
    except ValueError:
        pass
    from b1m_score import synthetic_checks
    metric_checks=synthetic_checks()
    return {'status':'SYNTHETIC_PASS','checks':[
        'frozen_tangent_bitwise','target_projection_identity','radial_identity',
        'primal_dual_independent_solve','normal_equations','scale_equivariance',
        'euclidean_second_step_recurrence','aligned_and_antipodal',
        'least_squares_stationarity','heldout_nontrivial_effect','stable_ties',
        'zero_direction_rejection'],'metric_synthetic_checks':metric_checks}


class Resources:
    def __init__(self, output):
        self.output=output; self.stop=threading.Event(); self.peak=0
    def sample(self):
        import psutil
        proc=psutil.Process(); rss=proc.memory_info().rss; self.peak=max(self.peak,rss)
        row={'utc':utc(),'rss_bytes':rss,'cpu_seconds':sum(proc.cpu_times()[:2]),
             'host_available_bytes':psutil.virtual_memory().available,
             'loadavg':list(os.getloadavg()) if hasattr(os,'getloadavg') else None}
        with (self.output/'resources.jsonl').open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(row)+'\n')
    def run(self):
        while not self.stop.wait(2):
            self.sample()
    def begin(self):
        self.sample(); self.thread=threading.Thread(target=self.run,daemon=True); self.thread.start()
    def end(self):
        self.stop.set(); self.thread.join(); self.sample()


def full(lock, output, stage):
    import numpy as np
    from arc2_global.residual_ablation import fit_controls
    from arc2_global.numerics import apply_affine, _indices, _vectors
    from arc2_global.model import _tangent2
    from arc2_global.retrieval import exact_topk
    ids=json.loads((ROOT/lock['ids']['path']).read_text())
    if sha(ROOT/lock['ids']['path']) != lock['ids']['sha256']:
        raise ValueError('Changed IDs')
    shutil.copyfile(ROOT/lock['ids']['path'],output/'ids.json')
    registry={}
    # Validate the complete physical-cache inputs before computation.
    specs=[spec for g in lock['groups'] for k,spec in g.items() if isinstance(spec,dict) and 'sha256' in spec and k!='full_target_reference']
    for spec in specs:
        path=ROOT/spec['path'] if not Path(spec['path']).is_absolute() else Path(spec['path'])
        if str(path) not in registry:
            if sha(path)!=spec['sha256']: raise ValueError('Changed input: '+str(path))
            registry[str(path)]=spec['sha256']
    dump(output/'verified_inputs.json',registry)
    cells=[]
    groups=lock['groups'] if stage=='full' else [g for g in lock['groups'] if g['seed']==17]
    for g in groups:
        label=g['pair']+'_seed'+str(g['seed'])
        folder=output/label; folder.mkdir()
        def load(key):
            p=Path(g[key]['path']); return np.load(p if p.is_absolute() else ROOT/p,mmap_mode='r',allow_pickle=False)
        old,q=load('old_docs'),load('new_queries')
        anchors=_indices('anchors',np.asarray(load('anchors')),len(old))
        paid=_indices('paid50',np.asarray(load('paid50')),len(old))
        paid75=_indices('paid75',np.asarray(load('paid75')),len(old))
        if old.shape != (57638,384) or q.shape != (500,768): raise ValueError('Unexpected vectors')
        if len(anchors)!=1024 or len(paid)!=28819 or len(paid75)!=43228:
            raise ValueError('Unexpected exposure')
        if not np.array_equal(paid,np.unique(paid)) or not np.array_equal(paid75,np.unique(paid75)):
            raise ValueError('Paid row order must be sorted unique')
        pos=np.searchsorted(paid75,paid)
        if np.any(pos>=len(paid75)) or not np.array_equal(paid75[pos],paid): raise ValueError('Paid50 not subset of cached75')
        # Expose only paid50 target rows beyond this point, never withheld25%.
        cached=load('targets75')
        if cached.shape!=(43228,768) or cached.dtype!=np.float32:raise ValueError('Invalid cached target shape/dtype')
        selected=np.array(cached[pos],dtype=np.float32); del cached
        _vectors('queries',q,dim=768); _vectors('paid50_targets',selected,dim=768)
        ap=np.searchsorted(paid,anchors)
        if np.any(ap>=len(paid)) or not np.array_equal(paid[ap],anchors): raise ValueError('Anchors not paid')
        target_anchors=selected[ap]
        save(folder/'paid50.npy',paid); save(folder/'anchors.npy',anchors)
        fitted=fit_controls(np.asarray(old[anchors]),target_anchors)
        frozen=_tangent2(np.asarray(old[anchors]),target_anchors,fitted['base_float64'])
        np.testing.assert_array_equal(frozen[1],fitted['coefficients']['tangent2'])
        arrays={**fitted['coefficients'],'base_float64':fitted['base_float64']}
        for method,states in fitted['float64_steps'].items():
            for i,state in enumerate(states,1): arrays[method+'_step'+str(i)+'_float64']=state
        with (folder/'parameters.npz').open('xb') as stream: np.savez(stream,**arrays)
        diagnostics={k:v for k,v in fitted.items() if k in ['shared_procrustes_seconds','shared_dual_factor_seconds','trajectories']}
        diagnostics.update({'paid_unique_encodings_logical':len(paid),'fit_pairs':len(anchors),
                            'physical_encodings_this_run':0,'cache_only':True,'methods':{}})
        galleries={}
        for method,coef in fitted['coefficients'].items():
            started=time.perf_counter()
            gallery=np.empty((len(old),768),dtype=np.float32)
            for start in range(0,len(old),512): gallery[start:start+512]=apply_affine(old[start:start+512],coef)
            map_seconds=time.perf_counter()-started
            # Continuous diagnostics on unpaid rows; do not threshold-select results.
            unpaid=np.ones(len(old),dtype=bool); unpaid[paid]=False
            galleries[method]=gallery[unpaid].copy()
            gallery[paid]=selected
            np.testing.assert_array_equal(gallery[paid],selected)
            started=time.perf_counter()
            ranks=exact_topk(q,gallery,k=100,batch_rows=16,query_ids=ids['query_ids'],document_ids=ids['doc_ids'],exclude_identical_ids=True)
            search_seconds=time.perf_counter()-started
            rp=folder/(method+'_rankings.npy'); save(rp,ranks)
            cells.append({'pair':g['pair'],'seed':g['seed'],'method':method,'budget':'50pct',
                          'ranking_path':rp.relative_to(output).as_posix(),'sha256':sha(rp),
                          'shape':list(ranks.shape),'map_seconds':map_seconds,'search_seconds':search_seconds})
            diagnostics['methods'][method]={'map_seconds':map_seconds,'search_seconds':search_seconds}
            dump(output/'progress.json',{'stage':stage,'rankings':len(cells),'expected':40 if stage=='full' else 8,'latest':label+'/'+method,'utc':utc()})
            print(json.dumps({'rankings':len(cells),'latest':label+'/'+method}),flush=True)
        for method in ('tangent2','chordal2','euclidean2'):
            cos=np.sum(galleries['procrustes'].astype(np.float64)*galleries[method],axis=1)
            diagnostics['methods'][method]['unpaid_proxy_cosine_to_B0_quantiles']=np.quantile(cos,[0,.25,.5,.75,1]).tolist()
            diagnostics['methods'][method]['unpaid_proxy_maxabs_to_B0']=float(np.max(np.abs(galleries[method]-galleries['procrustes'])))
        for other in ('chordal2','euclidean2','procrustes'):
            diagnostics['methods'][other]['unpaid_proxy_maxabs_vs_tangent']=float(np.max(np.abs(galleries[other]-galleries['tangent2'])))
            a=np.load(folder/'tangent2_rankings.npy'); b=np.load(folder/(other+'_rankings.npy'))
            diagnostics['methods'][other]['queries_changed_top100_vs_tangent']=int(np.any(a!=b,axis=1).sum())
            diagnostics['methods'][other]['queries_changed_top10_vs_tangent']=int(np.any(a[:,:10]!=b[:,:10],axis=1).sum())
        dump(folder/'diagnostics.json',diagnostics)
        if stage=='smoke' and any(np.array_equal(galleries['tangent2'],galleries[m]) for m in ('chordal2','euclidean2')):
            raise RuntimeError('SMOKE_DEGENERATE_STOP: exact unpaid proxy identity; preserve and interpret before scoring')
        del galleries
    expected=40 if stage=='full' else 8
    if len(cells)!=expected: raise ValueError('Incomplete ranking matrix')
    dump(output/'ranking_seal.json',{'utc':utc(),'stage':stage,'lock_sha256':sha(ROOT/lock['_lock_path']),
         'cells':cells,'input_hashes':registry,'artifacts':{
             p.relative_to(output).as_posix():sha(p) for p in output.rglob('*')
             if p.is_file() and p.name not in ['metadata.json','resources.jsonl','progress.json']}})
    return {'status':stage.upper()+'_SEALED','rankings':len(cells),'qrels_opened':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lock',required=True); ap.add_argument('--output',required=True)
    ap.add_argument('--stage',choices=['synthetic','smoke','full'],required=True)
    ap.add_argument('--smoke',help='Required matching successful smoke directory for full')
    args=ap.parse_args(); lock=json.loads((ROOT/args.lock).read_text()); verify_code(lock)
    lock['_lock_path']=args.lock
    output=Path(args.output).resolve(); output.mkdir(parents=True,exist_ok=False)
    meta={'status':'RUNNING','utc_start':utc(),'stage':args.stage,'lock_sha256':sha(ROOT/args.lock),
          'host':platform.node(),'python':sys.version,'platform':platform.platform(),'pid':os.getpid(),
          'qrels_opened':False,'method_unchanged':True}
    resource=Resources(output); began=time.perf_counter()
    try:
        import numpy,scipy
        from threadpoolctl import threadpool_limits,threadpool_info
        meta.update(numpy=numpy.__version__,scipy=scipy.__version__)
        if meta['numpy']!=lock['runtime']['numpy'] or meta['scipy']!=lock['runtime']['scipy']:
            raise ValueError('Runtime version mismatch')
        if args.stage=='full':
            if not args.smoke: raise ValueError('Full requires smoke')
            smoke=json.loads((Path(args.smoke)/'metadata.json').read_text())
            if smoke['status']!='SMOKE_SEALED' or smoke['lock_sha256']!=meta['lock_sha256']:
                raise ValueError('Matching smoke not passed')
            synthetic_path=Path(args.smoke).parent/'synthetic'
            syn=json.loads((synthetic_path/'metadata.json').read_text())
            if syn['status']!='SYNTHETIC_PASS' or syn['lock_sha256']!=meta['lock_sha256']:
                raise ValueError('Matching synthetic checks not passed')
        resource.begin()
        with threadpool_limits(limits=lock['blas_threads']):
            meta['blas']=threadpool_info(); dump(output/'metadata.json',meta)
            result=synthetic() if args.stage=='synthetic' else full(lock,output,args.stage)
        meta.update(result)
    except BaseException as exc:
        meta.update(status='FAILED_PRESERVED',error=repr(exc),traceback=traceback.format_exc())
        raise
    finally:
        if hasattr(resource,'thread'):resource.end()
        meta.update(utc_end=utc(),elapsed_seconds=time.perf_counter()-began,peak_rss_bytes=resource.peak)
        dump(output/'metadata.json',meta)
        print(json.dumps({k:meta[k] for k in ['status','elapsed_seconds','peak_rss_bytes']}),flush=True)


if __name__=='__main__': main()
