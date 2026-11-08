"""Separate sealed-input scorer; FiQA DEV only, no test-set label access."""
import argparse
import csv
import json
from pathlib import Path
import sys
import traceback
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ops'))
from tangent_control_run import sha, dump, utc, verify_code
from b1m_score import metrics_for, parse_qrel_rows


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lock',required=True); ap.add_argument('--run',required=True)
    ap.add_argument('--seal-sha256',required=True)
    args=ap.parse_args(); lock=json.loads((ROOT/args.lock).read_text()); verify_code(lock)
    run=Path(args.run).resolve(); sealpath=run/'ranking_seal.json'
    if sha(sealpath)!=args.seal_sha256: raise ValueError('Seal changed')
    meta=json.loads((run/'metadata.json').read_text())
    seal=json.loads(sealpath.read_text())
    if (meta['status']!='FULL_SEALED' or seal['stage']!='full' or
            seal['lock_sha256']!=sha(ROOT/args.lock) or meta['lock_sha256']!=sha(ROOT/args.lock)):
        raise ValueError('Require full sealed matching run')
    if len(seal['cells'])!=40: raise ValueError('Incomplete matrix')
    expected={(p,s,m) for p in lock['pairs'] for s in lock['seeds'] for m in lock['methods']}
    if {(c['pair'],c['seed'],c['method']) for c in seal['cells']}!=expected:
        raise ValueError('Unexpected cell identities')
    paths=[c['ranking_path'] for c in seal['cells']]
    if len(set(paths))!=40:raise ValueError('Ranking paths must be distinct')
    if any(c['budget']!='50pct' for c in seal['cells']):raise ValueError('Unexpected budget')
    expected_inputs={}
    for g in lock['groups']:
        for key,spec in g.items():
            if key=='full_target_reference' or not isinstance(spec,dict) or 'sha256' not in spec:continue
            path=Path(spec['path'])
            if not path.is_absolute():path=ROOT/path
            expected_inputs[str(path)]=spec['sha256']
    if seal['input_hashes']!=expected_inputs:raise ValueError('Incomplete/changed input registry')
    for rel,h in seal['artifacts'].items():
        p=(run/rel).resolve()
        if not p.is_relative_to(run) or sha(p)!=h: raise ValueError('Changed sealed artifact: '+rel)
    for path,h in seal['input_hashes'].items():
        if sha(path)!=h: raise ValueError('Changed vector/selection input: '+path)
    if sha(run/'ids.json')!=lock['ids']['sha256']:raise ValueError('IDs differ from locked order')
    ids=json.loads((run/'ids.json').read_text()); ranks=[]
    for key,count in [('doc_ids',57638),('query_ids',500)]:
        values=ids[key]
        if len(values)!=count or any(not isinstance(v,str) or not v for v in values) or len(set(values))!=count:
            raise ValueError('Invalid locked ID list: '+key)
    for c in seal['cells']:
        p=(run/c['ranking_path']).resolve()
        if not p.is_relative_to(run) or sha(p)!=c['sha256']:raise ValueError('Changed ranking')
        r=np.load(p,allow_pickle=False)
        if r.shape!=(500,100) or r.dtype.kind not in 'iu' or np.any(r<0) or np.any(r>=57638):
            raise ValueError('Invalid rankings')
        if np.any(np.diff(np.sort(r,axis=1),axis=1)==0):raise ValueError('Duplicate hit')
        for i,qid in enumerate(ids['query_ids']):
            if qid in [ids['doc_ids'][int(j)] for j in r[i]]:raise ValueError('Identical ID not excluded')
        ranks.append(r)
    out=run/'scoring'; out.mkdir(exist_ok=False)
    status={'status':'SCORING','utc_start':utc(),'scope':'inspected FiQA development ablation',
            'seal_sha256':args.seal_sha256,'lock_sha256':sha(ROOT/args.lock)}
    began=time.perf_counter()
    try:
        # Receipt precedes the label file opening. These labels were already
        # inspected historically; this is not a first-ever independent opening.
        dump(out/'dev_label_access.json',{'utc':utc(),'source':lock['qrels'],
             'already_inspected_development_labels':True,'rankings_sealed':40})
        qp=Path(lock['qrels']['path'])
        if sha(qp)!=lock['qrels']['sha256']:raise ValueError('Changed DEV labels')
        with qp.open(encoding='utf-8') as stream:
            reader=csv.DictReader(stream,delimiter='\t'); columns=reader.fieldnames; rows=list(reader)
        qrels,_=parse_qrel_rows(rows,columns,'tsv')
        values=np.stack([metrics_for(r,ids['doc_ids'],ids['query_ids'],qrels) for r in ranks])
        np.save(out/'per_query.npy',values,allow_pickle=False)
        cells=seal['cells']; dump(out/'cell_index.json',cells)
        means=[]; diff=[]; contrast_keys=[]
        for pair in lock['pairs']:
            means_by_method={}
            for method in lock['methods']:
                rows=np.stack([values[i] for i,c in enumerate(cells) if c['pair']==pair and c['method']==method])
                if rows.shape!=(5,500,2): raise ValueError('Wrong five-seed metric shape')
                means_by_method[method]=rows.mean(axis=0)
                means.append({'pair':pair,'method':method,'ndcg10':float(rows[:,:,0].mean()),
                              'recall100':float(rows[:,:,1].mean()),
                              'ndcg10_seed_std':float(rows[:,:,0].mean(axis=1).std(ddof=1))})
            for other in ('chordal2','euclidean2'):
                diff.append(means_by_method['tangent2'][:,0]-means_by_method[other][:,0])
                contrast_keys.append({'pair':pair,'left':'tangent2','right':other})
        difference=np.stack(diff,axis=1)
        rng=np.random.default_rng(20261102); draws=[]
        for _ in range(100):
            idx=rng.integers(0,500,size=(200,500))
            draws.append(difference[idx].mean(axis=1))
        bootstrap=np.concatenate(draws)
        np.save(out/'bootstrap_draws.npy',bootstrap,allow_pickle=False)
        intervals=[]
        for j,key in enumerate(contrast_keys):
            low,high=np.quantile(bootstrap[:,j],[.00625,.99375])
            intervals.append({**key,'delta_ndcg10':float(difference[:,j].mean()),
                 'lower':float(low),'upper':float(high),
                 'verdict':'positive' if low>0 else 'negative' if high<0 else 'unresolved'})
        result={'status':'DEV_SCORED','scope':status['scope'],'means':means,'primary_contrasts':intervals,
                'bootstrap':{'draws':20000,'seed':20261102,'unit':'query after five-seed averaging',
                 'family_size':4,'individual_coverage':.9875,'approx_family_coverage':.95,
                 'queries_shared_across_pairs':True,'quantile_method':'linear'},
                'physical_cost_claim':False,'independent_test_claim':False}
        dump(out/'summary.json',result)
        with (out/'means.csv').open('w',newline='',encoding='utf-8') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(means[0]));writer.writeheader();writer.writerows(means)
        status.update(status='DEV_SCORED')
        print(json.dumps(result,indent=2),flush=True)
    except BaseException as exc:
        status.update(status='FAILED_PRESERVED',error=repr(exc),traceback=traceback.format_exc());raise
    finally:
        status.update(utc_end=utc(),elapsed_seconds=time.perf_counter()-began)
        dump(out/'metadata.json',status)


if __name__=='__main__':main()
