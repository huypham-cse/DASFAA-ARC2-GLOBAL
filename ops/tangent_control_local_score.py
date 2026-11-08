"""Separate TC1L20-ranking scorer; original four-contrast family retained."""
import argparse
import csv
import json
import hashlib
import platform
from pathlib import Path
import shutil
import sys
import tarfile
import time
import traceback
import numpy as np
import scipy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ops'))
from tangent_control_run import sha,dump,utc,verify_code
from tangent_control_local_run import checked_inputs
from b1m_score import metrics_for,parse_qrel_rows


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lock',required=True)
    ap.add_argument('--run',required=True);ap.add_argument('--seal-sha256',required=True)
    args=ap.parse_args();lock=json.loads((ROOT/args.lock).read_text());verify_code(lock)
    runtime={'python':sys.version,'platform':platform.system(),'numpy':np.__version__,'scipy':scipy.__version__}
    if runtime!=lock['runtime']:raise ValueError('Scorer local runtime mismatch before labels')
    run=Path(args.run).resolve();sealpath=run/'ranking_seal.json'
    if sha(sealpath)!=args.seal_sha256:raise ValueError('Changed local seal')
    meta=json.loads((run/'metadata.json').read_text());seal=json.loads(sealpath.read_text())
    locksha=sha(ROOT/args.lock)
    if meta['status']!='FULL_SEALED' or seal['stage']!='full' or seal['lock_sha256']!=locksha or meta['lock_sha256']!=locksha:
        raise ValueError('Require matching full sealed local run')
    cells=seal['cells'];expected={('minilm_distilroberta',s,m,'50pct') for s in lock['seeds'] for m in lock['methods']}
    actual=[(c['pair'],c['seed'],c['method'],c['budget']) for c in cells]
    if len(cells)!=20 or len(set(actual))!=20 or set(actual)!=expected:raise ValueError('Incomplete20-cell matrix')
    if len({c['ranking_path'] for c in cells})!=20:raise ValueError('Duplicate ranking paths')
    registry=checked_inputs(lock)
    if seal['input_hashes']!=registry:raise ValueError('Input registry differs from complete lock')
    for relative,h in seal['artifacts'].items():
        p=(run/relative).resolve()
        if not p.is_relative_to(run) or sha(p)!=h:raise ValueError('Changed local artifact: '+relative)
    if sha(run/'ids.json')!=lock['ids']['sha256']:raise ValueError('Changed locked ID ordering')
    ids=json.loads((run/'ids.json').read_text())
    for name,count in [('doc_ids',57638),('query_ids',500)]:
        row=ids[name]
        if len(row)!=count or len(set(row))!=count or any(not isinstance(v,str) or not v for v in row):raise ValueError('Invalid IDs')
    ranks=[]
    for c in cells:
        p=(run/c['ranking_path']).resolve()
        if not p.is_relative_to(run) or sha(p)!=c['sha256']:raise ValueError('Changed ranking')
        r=np.load(p,allow_pickle=False)
        if r.shape!=(500,100) or r.dtype.kind not in 'iu' or np.any(r<0) or np.any(r>=57638):raise ValueError('Malformed rankings')
        if np.any(np.diff(np.sort(r,axis=1),axis=1)==0):raise ValueError('Duplicate hit')
        for i,q in enumerate(ids['query_ids']):
            if q in [ids['doc_ids'][int(v)] for v in r[i]]:raise ValueError('Identical ID returned')
        ranks.append(r)
    out=run/'scoring';out.mkdir(exist_ok=False)
    status={'status':'SCORING','utc_start':utc(),'scope':'MiniLM-only local FiQA DEV; E5 pending','lock_sha256':locksha,'seal_sha256':args.seal_sha256,'runtime':runtime}
    began=time.perf_counter()
    try:
        dump(out/'dev_label_access.json',{'utc':utc(),'source':lock['qrels'],
             'already_inspected_development_labels':True,'all20rankings_sealed':True})
        # Byte recovery of the original labels occurs only after the gate above.
        qp=out/'fiqa_dev.tsv'
        with tarfile.open(ROOT/lock['qrels']['archive']) as archive:
            member=archive.getmember(lock['qrels']['member'])
            if not member.isfile() or member.size!=18327:raise ValueError('Unexpected DEV label member')
            with archive.extractfile(member) as source,qp.open('xb') as destination:shutil.copyfileobj(source,destination)
        if sha(qp)!=lock['qrels']['sha256']:raise ValueError('Recovered DEV label hash mismatch')
        with qp.open(encoding='utf-8') as stream:
            reader=csv.DictReader(stream,delimiter='\t');columns=reader.fieldnames;rows=list(reader)
        labels,_=parse_qrel_rows(rows,columns,'tsv')
        values=np.stack([metrics_for(r,ids['doc_ids'],ids['query_ids'],labels) for r in ranks])
        np.save(out/'per_query.npy',values,allow_pickle=False);dump(out/'cell_index.json',cells)
        means=[];method_arrays={}
        for method in lock['methods']:
            a=np.stack([values[i] for i,c in enumerate(cells) if c['method']==method])
            if a.shape!=(5,500,2):raise ValueError('Expected five seed arrays')
            method_arrays[method]=a.mean(axis=0)
            means.append({'pair':'minilm_distilroberta','method':method,'ndcg10':float(a[:,:,0].mean()),
                          'recall100':float(a[:,:,1].mean()),'ndcg10_seed_std':float(a[:,:,0].mean(axis=1).std(ddof=1))})
        others=['chordal2','euclidean2']
        difference=np.stack([method_arrays['tangent2'][:,0]-method_arrays[m][:,0] for m in others],axis=1)
        rng=np.random.default_rng(20261102)
        draw_chunks=[];index_hash=hashlib.sha256()
        for _ in range(100):
            idx=rng.integers(0,500,size=(200,500));index_hash.update(idx.astype('<i8',copy=False).tobytes())
            draw_chunks.append(difference[idx].mean(axis=1))
        draws=np.concatenate(draw_chunks)
        np.save(out/'bootstrap_draws.npy',draws,allow_pickle=False)
        contrasts=[]
        for j,other in enumerate(others):
            lo,hi=np.quantile(draws[:,j],[.00625,.99375])
            contrasts.append({'pair':'minilm_distilroberta','left':'tangent2','right':other,'delta_ndcg10':float(difference[:,j].mean()),
                              'lower':float(lo),'upper':float(hi),'verdict':'positive' if lo>0 else 'negative' if hi<0 else 'unresolved'})
        summary={'status':'DEV_SCORED','scope':status['scope'],'means':means,'primary_contrasts':contrasts,
                 'bootstrap':{'draws':20000,'seed':20261102,'unit':'query after five-seed averaging',
                 'family_size':4,'observed_contrasts':2,'pending_E5_contrasts':2,'individual_coverage':.9875,
                 'approx_original_family_coverage':.95,'quantile_method':'linear','query_indices_sha256_le_int64':index_hash.hexdigest()},
                 'independent_test_claim':False,'physical_cost_claim':False,'original_two_pair_campaign_complete':False}
        dump(out/'summary.json',summary)
        with (out/'means.csv').open('w',newline='',encoding='utf-8') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(means[0]));writer.writeheader();writer.writerows(means)
        status['status']='DEV_SCORED';print(json.dumps(summary,indent=2),flush=True)
    except BaseException as exc:
        status.update(status='FAILED_PRESERVED',error=repr(exc),traceback=traceback.format_exc());raise
    finally:
        status.update(utc_end=utc(),elapsed_seconds=time.perf_counter()-began);dump(out/'metadata.json',status)


if __name__=='__main__':main()
