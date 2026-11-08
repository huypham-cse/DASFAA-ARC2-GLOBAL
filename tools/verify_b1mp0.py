"""Verify synchronized B1-M/P0 review artifacts without opening qrels."""
import argparse,hashlib,importlib.util,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def close(a,b):
    if isinstance(a,dict):
        assert set(a)==set(b)
        for k in a:close(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):close(x,y)
    elif isinstance(a,float):assert np.isclose(a,b,rtol=0,atol=1e-12),(a,b)
    else:assert a==b,(a,b)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    assert not a.output.exists();base=a.root.resolve();run=base/'b1m_full_r1_20261026';p0=base/'b1p0_full_r1_20261026'
    m=read(run/'metadata.json');p=read(p0/'metadata.json')
    assert m['status']=='FAILED_PRESERVED' and not m['TREC_access']
    assert m['ranking_count']==736 and (run/'scoring/failure.json').exists()
    assert p['status']=='B1P0_FULL_PASS' and not p['failures'] and len(p['checks'])==31
    committed=subprocess.check_output(['git','show',m['code_commit']+':configs/b1m_lock.json'],cwd=ROOT)
    assert hashlib.sha256(committed).hexdigest()==m['lock_sha256']
    assert sha(run/'ranking_seal.json')==m['ranking_seal_sha256']
    seal=read(run/'ranking_seal.json');assert len(seal['cells'])==736
    for rel,digest in seal['inputs'].items():assert sha(run/rel)==digest,rel
    for c in seal['cells']:
        path=run/c['ranking_path'];assert sha(path)==c['ranking_sha256'],path
        ids=read(run/'inputs'/c['dataset']/'ids.json');r=np.load(path,allow_pickle=False)
        assert r.shape==(len(ids['query_ids']),100) and r.dtype.kind in 'iu'
        assert r.min()>=0 and r.max()<len(ids['doc_ids'])
        assert all(len(set(row))==100 for row in r)
    p0real=read(run/'p0_real_checks.json');assert len(p0real)==120
    for row in p0real:
        assert row['coefficient_maxabs']<=1e-6 and row['proxy_maxabs']<=1e-6
        assert row['ranking_drift']['score_maxabs']<=1e-6
        assert row['ranking_drift']['unexplained_inversion_count']==0
    for case in p['checks']:
        assert case['status']=='PASS'
        for step in case['steps']:
            assert step['float64_allclose'] and step['coefficient_maxabs']<=1e-6
            assert step['normalized_proxy_maxabs']<=1e-6 and step['score_maxabs']<=1e-6
            assert all(r['unexplained_inversion_count']==0 for r in step['ranking'])
    score=run/'scoring_r2_binary';done=read(score/'completed.json');assert done['status']=='DEV_SCORED'
    repair_lock=subprocess.check_output(['git','show',done['scorer_code_commit']+':configs/b1m_score_r2_lock.json'],cwd=ROOT)
    started=read(score/'started.json')
    assert hashlib.sha256(repair_lock).hexdigest()==started['lock_sha256']
    assert read(run/'scoring/failure.json')['dev_qrel_access_started']
    assert done['rescore_context']['ranking_seal_sha256']==m['ranking_seal_sha256']
    for rel,digest in done['artifact_sha256'].items():assert sha(score/rel)==digest,rel
    assert read(score/'first_dev_qrel_open.json')['all_736_rankings_and_ids_verified']
    # Reproduce means and bootstrap CIs from per-query outputs only, not labels.
    spec=importlib.util.spec_from_file_location('saved_dev_scorer',ROOT/'ops/b1m_score.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    arrays={};cells=[];ids={}
    for dataset in module.DATASETS:
        index=read(score/dataset/'cell_index.json');cells.extend(index['cells'])
        arrays[dataset]=np.load(score/dataset/'per_query.npy',allow_pickle=False)
        assert np.isfinite(arrays[dataset]).all()
        i=read(run/'inputs'/dataset/'ids.json');ids[dataset]=(i['doc_ids'],i['query_ids'])
    means,contrasts,encoder,overall=module.summaries(cells,arrays,ids)
    summary=read(score/'results_summary.json')
    for key,value in [('means',means),('contrasts',contrasts),('per_encoder_macro',encoder),('overall_macro',overall)]:close(summary[key],value)
    extraction=read(ROOT/'provenance/implementation_extraction.json')
    for rel,digest in extraction['canonical_lf_hashes'].items():assert hashlib.sha256((ROOT/rel).read_text(encoding='utf-8').encode()).hexdigest()==digest
    result={'status':'PASS','scope':'local synchronized rankings, input hashes, per-query means/CI arithmetic and saved P0 receipts; no qrels read; not claim audit','rankings':736,'synthetic_P0_cases':31,'real_P0_budget_checks':120,'frozen_ARC2_unchanged':True,'backend_ranking_identity':all(r['ranking_drift']['queries_with_difference']==0 for r in p0real),'raw_coefficients_vectors_and_synthetic_arrays':'retained on H100 with full manifest; omitted from compact local review bundle','next':'STOP before B1-P/B1-G/TREC/systems pending next user instruction'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
