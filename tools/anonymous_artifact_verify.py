"""Offline frozen-output verification; no fitting, vector search or qrel access."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def arr(p):return np.load(ROOT/p,allow_pickle=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def equal(a,b):
    error=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    if error>1e-12:raise ValueError(('Numerical mismatch',error,a,b))
    return error
def resolve(name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts or ':' in name or '\\' in name:raise ValueError('Unsafe manifest path')
    return ROOT/p
def main():
    manifest=read('MANIFEST.json')
    for name,spec in manifest['files'].items():
        p=resolve(name)
        if not p.is_file() or p.stat().st_size!=spec['bytes'] or sha(p)!=spec['sha256']:raise ValueError('Manifest mismatch: '+name)
    counters={};maximum=0.0
    for family in ['development','mechanism','allpaid','prospective','matched_targets']:
        base=Path('evidence')/family;summary=read(base/'summary.json');cells=[];arrays=[]
        for p in sorted((ROOT/base).rglob('cell_index.json')):
            relative=p.parent.relative_to(ROOT);ix=read(p.relative_to(ROOT))
            cc=ix if isinstance(ix,list) else ix['cells']
            for i,c in enumerate(cc):
                if family=='development':a=arr(relative/c['per_query_file'])[c['per_query_index']]
                elif family=='mechanism':a=arr(relative/'per_query.npy')[c['per_dataset_index']]
                else:a=arr(relative/'per_query.npy')[c.get('per_query_index',i)]
                cells.append(c);arrays.append(a)
        checked=0
        for row in summary['means']:
            identity={k:row[k] for k in ['dataset','pair','budget','method','regime'] if k in row}
            selected=[a for c,a in zip(cells,arrays) if all(c.get(k)==v for k,v in identity.items())]
            if not selected:raise ValueError(('Missing condition',family,identity))
            # Native reference cells occur once; adapters retain every fixed seed.
            for j,m in enumerate(['ndcg10','recall100']):
                value=row[m];v=value['mean'] if isinstance(value,dict) else value
                maximum=max(maximum,equal(np.mean(selected,axis=(0,1))[j],v));checked+=1
                if isinstance(value,dict) and len(selected)==5:
                    per_seed=np.mean(selected,axis=1)[:,j]
                    if 'seed_std' in value:maximum=max(maximum,equal(per_seed.std(ddof=1),value['seed_std']))
            # Each non-reference condition must have all five seeds.
            if row['method'] not in ['full_x','full_y'] and len(selected)!=5:raise ValueError(('Incomplete seeds',family,identity))
        counters[family]={'cells':len(cells),'means_checked':checked}
        if family=='matched_targets':
            lookup={(c['seed'],c['method']):a for c,a in zip(cells,arrays)}
            indices=np.random.default_rng(summary['bootstrap']['seed']).integers(0,500,size=(20000,500),dtype=np.int64)
            digest=hashlib.sha256(indices.astype('<i8').tobytes()).hexdigest()
            if digest!=summary['bootstrap']['query_indices_sha256_le_int64']:raise ValueError('Bootstrap query indices changed')
            computed=[]
            for contrast in summary['primary_contrasts']:
                delta=np.stack([lookup[(s,'tangent2')][:,0]-lookup[(s,contrast['right'])][:,0] for s in [17,29,41,53,67]])
                draw=delta.mean(axis=0)[indices].mean(axis=1);computed.append(draw)
                maximum=max(maximum,equal(delta.mean(),contrast['delta_ndcg10']),equal(np.quantile(draw,[.00625,.99375]),[contrast['lower'],contrast['upper']]))
                if not np.all(delta.mean(axis=1)>0):raise ValueError('Seed sign mismatch')
            maximum=max(maximum,equal(np.stack(computed,axis=1),arr(base/'bootstrap_draws.npy')))
            counters[family]['bootstrap_draws_recomputed']=20000
    # Independent arithmetic checks on the retained mixed-gallery score arrays.
    base=Path('evidence/gallery');g=read(base/'summary.json');case_results={r['case_id']:r for r in g['case_diagnostics_and_metrics']};lookup={}
    cases=0
    for p in sorted((ROOT/base).rglob('cell_index.json')):
        folder=p.parent.relative_to(ROOT);ix=read(p.relative_to(ROOT))
        before=arr(folder/'before_per_query.npy');after=arr(folder/'after_per_query.npy');delta=arr(folder/'delta_per_query.npy')
        for c in ix['partial_cases']:
            b,a=before[c['before_index']],after[c['after_delta_index']];d=delta[c['after_delta_index']]
            maximum=max(maximum,equal(a-b,d));row=case_results[c['case_id']]
            for j,m in enumerate(['ndcg10','recall100']):
                maximum=max(maximum,equal(b[:,j].mean(),row['metrics'][m]['before']),equal(a[:,j].mean(),row['metrics'][m]['after']),equal(d[:,j].mean(),row['metrics'][m]['delta']['mean']))
            lookup[tuple(c[k] for k in ['dataset','pair','method','regime','budget','seed'])]=(b,a,d);cases+=1
    for row in g['aggregate_five_seed_conditions']:
        values=[lookup[tuple(row[k] for k in ['dataset','pair','method','regime','budget'])+(s,)] for s in [17,29,41,53,67]]
        for j,m in enumerate(['ndcg10','recall100']):
            for i,key in enumerate(['before','after','delta_of_query_means']):maximum=max(maximum,equal(np.mean([v[i][:,j].mean() for v in values]),row['metrics'][m][key]['mean']))
    counters['gallery']={'partial_cases':cases,'five_seed_conditions':len(g['aggregate_five_seed_conditions'])}
    index=read('evidence/ranking_index.json');unique=set()
    for row in index['cells']:
        p=resolve(row['path'])
        if sha(p)!=row['sha256']:raise ValueError('Ranking mismatch')
        if row['sha256'] in unique:continue
        unique.add(row['sha256']);a=arr(row['path'])
        if a.ndim!=2 or a.shape[1]!=100 or not np.issubdtype(a.dtype,np.integer) or a.min()<0:raise ValueError('Invalid ranking array')
        if not all(len(np.unique(v))==100 for v in a):raise ValueError('Duplicate document within ranking')
    result={'status':'PASS','manifest_files':len(manifest['files']),'ranking_cells':len(index['cells']),'unique_raw_ranking_arrays':len(unique),'ranking_family_counts':dict(Counter(r['family'] for r in index['cells'])),'max_metric_arithmetic_error':maximum,'families':counters,'offline':True,'qrels_opened':False,'new_fit_or_vector_search':False,'scope':'Frozen means, seed counts, gallery arithmetic, matched-control bootstrap and all packaged bytes; other original saved intervals are retained, not independently recomputed by this verifier.'}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
