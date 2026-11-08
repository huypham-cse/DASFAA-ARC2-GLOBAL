"""Fresh offline release audit. Reads raw evidence only; writes own trace."""
from pathlib import Path
import argparse, collections, csv, hashlib, json, math, sys
from datetime import datetime, timezone
import socket, urllib.request
sys.dont_write_bytecode=True
def forbidden(*args,**kwargs): raise RuntimeError("Network forbidden in saved-control verification")
socket.create_connection=forbidden
urllib.request.urlopen=forbidden
import numpy as np
import pyarrow.parquet as pq

parser=argparse.ArgumentParser(description="Offline independent rescoring of all B1-M/P rankings, locked uncertainty, and B1-G saved metric arrays; no vector replay or new scientific run.")
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
parser.add_argument('--output',type=Path)
args=parser.parse_args()
ROOT=args.root.resolve()
output=(args.output if args.output else Path('checks')/('control_families_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json'))
output=output.resolve() if output.is_absolute() else (ROOT/output).resolve()
if not output.is_relative_to(ROOT/'checks') or output.suffix!='.json' or output.exists():
    raise ValueError('Require an exclusive new JSON output below release checks/')
HASHES={}
def bind(p):
    p=Path(p); HASHES[p.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest(); return p
def read(p): return json.loads(bind(p).read_text(encoding='utf8'))
def arr(p): return np.load(bind(p),allow_pickle=False)
def error(a,b):
    e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    assert e<=1e-12,(e,a,b)
    return e
DATASETS=['NanoNQ','NanoHotpotQA','NanoFEVER','FiQA']
SEEDS=[17,29,41,53,67]
M=ROOT/'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026'
P=ROOT/'results/b1p_r5_review_20261027'
G=ROOT/'results/b1g_r1_review_20261027'
C=ROOT/'results/b1c_r3_review_20261031/evidence'
result={}
ids={d:read(M/f'inputs/{d}/ids.json') for d in DATASETS}
qrels={}
for d in DATASETS:
    p=C/('qrels/FiQA.tsv' if d=='FiQA' else f'run/scoring/qrels_{d}.parquet')
    bind(p)
    if d=='FiQA':
        with p.open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
    else: rows=pq.read_table(p).to_pylist()
    qrels[d]={}
    for r in rows:
        q=str(r.get('query-id',r.get('query_id')));doc=str(r.get('corpus-id',r.get('corpus_id')))
        grade=float(r.get('score',r.get('relevance',1)))
        assert doc not in qrels[d].setdefault(q,{})
        qrels[d][q][doc]=grade
def metrics(ranks,d):
    docs,queries=ids[d]['doc_ids'],ids[d]['query_ids']
    assert ranks.shape==(len(queries),100)
    assert np.issubdtype(ranks.dtype,np.integer) and ranks.min()>=0 and ranks.max()<len(docs)
    assert all(len(np.unique(row))==100 for row in ranks)
    out=np.zeros((len(queries),2))
    discounts=1/np.log2(np.arange(10)+2)
    for i,q in enumerate(queries):
        rel={a:b for a,b in qrels[d].get(q,{}).items() if b>0}
        if not rel:continue
        returned=[docs[int(x)] for x in ranks[i]]
        ideal=sorted(rel.values(),reverse=True)[:10]
        num=math.fsum((2**rel.get(doc,0)-1)*float(discounts[k]) for k,doc in enumerate(returned[:10]))
        den=math.fsum((2**v-1)*float(discounts[k]) for k,v in enumerate(ideal))
        out[i]=num/den,len(set(returned)&rel.keys())/len(rel)
    return out
def census(cells):
    return {k:dict(collections.Counter(str(c.get(k)) for c in cells)) for k in ['dataset','pair','method','seed','budget','regime','origin']}
I=ROOT/'results/fiqa_development'
ii=read(I/'metric_index.json');ip=arr(I/'per_query.npy');iid=read(I/'ids.json')
assert iid==ids['FiQA'] and ip.shape==(64,500,2)
ic=np.stack([metrics(arr(I/c['ranking_path']),'FiQA') for c in ii['cells']])
result['imported_FiQA_history']={'status':'PASS','cells':64,'metric_values':ic.size,'max_metric_error':error(ic,ip)}
ma={};mc=[];maximum=0
for d in DATASETS:
    sc=M/f'scoring_r2_binary/{d}'
    ix=read(sc/'cell_index.json');saved=arr(sc/'per_query.npy')
    assert len(ix['cells'])==184 and saved.shape==(184,len(ids[d]['query_ids']),2)
    computed=np.empty_like(saved)
    for c in ix['cells']:
        i=c['per_dataset_index'];computed[i]=metrics(arr(M/c['ranking_path']),d)
        mc.append(c)
    maximum=max(maximum,error(computed,saved));ma[d]=computed
ms=read(M/'scoring_r2_binary/results_summary.json')
ml={(c['dataset'],c['pair'],c['seed'],c['budget'],c['method']):ma[c['dataset']][c['per_dataset_index']] for c in mc}
def check_means(rows,lookup,mode):
    n=0
    for r in rows:
        if mode=='M':
            vals=np.stack([lookup[(r['dataset'],r['pair'],s,r['budget'],r['method'])] for s in (SEEDS if r['budget']!='full' else [None])]).mean(axis=1)
        else:
            vals=np.stack([lookup[(r['pair'],r['method'],r['regime'],s)] for s in (SEEDS if r['regime']!='reference' else [None])]).mean(axis=1)
        for j,m in enumerate(['ndcg10','recall100']):
            error(vals[:,j].mean(),r[m]['mean']);n+=1
            if vals.shape[0]>1:error(vals[:,j].std(ddof=1),r[m]['seed_std']);error([vals[:,j].min(),vals[:,j].max()],r[m]['seed_range'])
    return n
check_means(ms['means'],ml,'M')
indices={d:np.random.default_rng(ch).integers(0,len(ids[d]['query_ids']),size=(20000,len(ids[d]['query_ids'])),dtype=np.int32) for d,ch in zip(DATASETS,np.random.SeedSequence(20261026).spawn(4))}
draws={}
for r in ms['contrasts']:
    d,p,b,l,h=(r[k] for k in ['dataset','pair','budget','left','right'])
    delta=np.stack([ml[(d,p,s,b,l)]-ml[(d,p,s,b,h)] for s in SEEDS]).mean(axis=0)
    draw=np.stack([delta[:,j][indices[d]].mean(axis=1) for j in [0,1]],axis=1)
    draws[(d,p,b,l,h)]=draw
    for j,m in enumerate(['ndcg10','recall100']):error(delta[:,j].mean(),r[m]['delta']);error(np.quantile(draw[:,j],[.025,.975]),r[m]['ci95'])
for r in ms['overall_macro']+ms['per_encoder_macro']:
    subset=[v for (d,p,b,l,h),v in draws.items() if l==r['left'] and h==r['right'] and (r['scope']=='overall' or p==r['scope'])]
    draw=np.mean(subset,axis=0)
    condition_subset=[x for x in ms['contrasts'] if x['left']==r['left'] and x['right']==r['right'] and (r['scope']=='overall' or x['pair']==r['scope'])]
    for metric in ['ndcg10','recall100']:error(np.mean([x[metric]['delta'] for x in condition_subset]),r[metric]['delta'])
    for j,m in enumerate(['ndcg10','recall100']):
        error(np.quantile(draw[:,j],[.025,.975]),r[m]['ci95'])
        if r['scope']=='overall' and j==0:error(np.quantile(draw[:,j],[.005,.995]),r[m]['ci99_bonferroni_family95'])
result['B1M']={'cells':len(mc),'metric_values':sum(x.size for x in ma.values()),'max_metric_error':maximum,'means':len(ms['means']),'condition_contrasts':len(ms['contrasts']),'encoder_macros':len(ms['per_encoder_macro']),'overall_macros':ms['overall_macro'],'census':census(mc),'status':'PASS'}
pi=read(P/'scoring/cell_index.json');pc=pi['cells'];pa=arr(P/'scoring/per_query.npy');computed=np.empty_like(pa)
assert len(pc)==124 and pa.shape==(124,500,2)
for i,c in enumerate(pc):computed[i]=metrics(arr(P/'generation'/c['ranking_path']),'FiQA')
maximum=error(computed,pa);ps=read(P/'scoring/results_summary.json')
pl={(c['pair'],c['method'],c['regime'],c['seed']):computed[i] for i,c in enumerate(pc)}
check_means(ps['means'],pl,'P')
ind=np.random.default_rng(20261026).integers(0,500,size=(20000,500),dtype=np.int32)
for r in ps['contrasts']:
    delta=np.stack([pl[(r['pair'],r['left']['method'],r['left']['regime'],s)]-pl[(r['pair'],r['right']['method'],r['right']['regime'],s)] for s in SEEDS]).mean(axis=0)
    for j,m in enumerate(['ndcg10','recall100']):
        draw=delta[:,j][ind].mean(axis=1);error(delta[:,j].mean(),r[m]['delta']);error(np.quantile(draw,[.025,.975]),r[m]['ci95'])
        if j==0:error(np.quantile(draw,[.05/64,1-.05/64]),r[m]['ci_bonferroni_family95'])
result['B1P']={'cells':len(pc),'metric_values':computed.size,'max_metric_error':maximum,'means':len(ps['means']),'contrasts':ps['contrasts'],'census':census(pc),'status':'PASS'}
gs=read(G/'scoring/results_summary.json');cases={x['case_id']:x for x in gs['case_diagnostics_and_metrics']};lookup={};gvalues=0;gcounts={}
for d in DATASETS:
    sc=G/f'scoring/{d}';gi=read(sc/'cell_index.json');before=arr(sc/'before_per_query.npy');after=arr(sc/'after_per_query.npy');delta=arr(sc/'delta_per_query.npy')
    gcounts[d]={'before_shape':list(before.shape),'after_shape':list(after.shape),'delta_shape':list(delta.shape)}
    gvalues+=before.size+after.size+delta.size
    for c in gi['partial_cases']:
        i,j=c['before_index'],c['after_delta_index'];error(after[j]-before[i],delta[j]);r=cases[c['case_id']]
        for k,m in enumerate(['ndcg10','recall100']):
            error(before[i,:,k].mean(),r['metrics'][m]['before']);error(after[j,:,k].mean(),r['metrics'][m]['after']);error(delta[j,:,k].mean(),r['metrics'][m]['delta']['mean'])
        lookup[(d,c['pair'],c['method'],c['regime'],c['budget'],c['seed'])]=(before[i],after[j],delta[j])
for r in gs['aggregate_five_seed_conditions']:
    vals=[lookup[(r['dataset'],r['pair'],r['method'],r['regime'],r['budget'],s)] for s in SEEDS]
    for k,m in enumerate(['ndcg10','recall100']):
        for n,field in enumerate(['before','after','delta_of_query_means']):error(np.mean([v[n][:,k].mean() for v in vals]),r['metrics'][m][field]['mean'])
assert len(cases)==450 and len(lookup)==450 and len(gs['aggregate_five_seed_conditions'])==90
result['B1G']={'partial_cases':len(cases),'pure_galleries':sum(v['before_shape'][0] for v in gcounts.values()),'array_values':gvalues,'conditions':len(gs['aggregate_five_seed_conditions']),'shapes':gcounts,'negative_condition_delta_counts':{m:sum(r['metrics'][m]['delta_of_query_means']['mean']<0 for r in gs['aggregate_five_seed_conditions']) for m in ['ndcg10','recall100']},'status':'PASS_scored_arrays_only_no_vector_replay'}
# R2 adds unchanged raw top100 G rankings in a short content-addressed layout.
rank_index=read(G/'portable_rankings/ranking_index.json')
by_before={x['group_id']:x for x in rank_index['files'] if x['kind']=='before'}
by_after={x['case_id']:x for x in rank_index['files'] if x['kind']=='after'}
assert len(by_before)==210 and len(by_after)==450
maximum_g=0.0; raw_values_g=0; raw_hashes_g=set()
historical_rank_files={}
for folder in ['b1mp0_r1_review_20261026','b1p_r5_review_20261027','fiqa_development','b1c_r3_review_20261031']:
    for path in (ROOT/'results'/folder).rglob('*.npy'):
        if 'rank' in path.as_posix().lower():
            historical_rank_files.setdefault(hashlib.sha256(bind(path).read_bytes()).hexdigest(),path)
serialized_byte_differences=0

for d in DATASETS:
    sc=G/f'scoring/{d}';gi=read(sc/'cell_index.json')
    before=arr(sc/'before_per_query.npy');after=arr(sc/'after_per_query.npy')
    assert gi['query_ids']==ids[d]['query_ids']
    for cell in gi['pure_cells']:
        spec=by_before[cell['group_id']];path=G/spec['relative_path']
        observed=hashlib.sha256(bind(path).read_bytes()).hexdigest()
        assert observed==spec['sha256']==cell['ranking_sha256']
        recalculated=metrics(arr(path),d)
        maximum_g=max(maximum_g,error(recalculated,before[cell['before_index']]))
        raw_values_g+=recalculated.size;raw_hashes_g.add(observed)
    for cell in gi['partial_cases']:
        spec=by_after[cell['case_id']];path=G/spec['relative_path']
        observed=hashlib.sha256(bind(path).read_bytes()).hexdigest()
        assert observed==spec['sha256']
        original=historical_rank_files[cell['published_ranking_sha256']]
        assert np.array_equal(arr(path),arr(original)),cell['case_id']
        serialized_byte_differences+=int(observed!=cell['published_ranking_sha256'])
        recalculated=metrics(arr(path),d)
        maximum_g=max(maximum_g,error(recalculated,after[cell['after_delta_index']]))
        raw_values_g+=recalculated.size;raw_hashes_g.add(observed)
result['B1G'].update(status='PASS_raw_ranking_metrics_and_arrays_no_vector_search',
    raw_pure_rankings_rescored=210,raw_mixed_rankings_rescored=450,
    raw_metric_values_compared=raw_values_g,raw_metric_max_error=maximum_g,
    unique_raw_ranking_hashes=len(raw_hashes_g), mixed_arrays_equal_historical=450, mixed_npy_byte_differences=serialized_byte_differences, byte_difference_note='Identical ordered ranking arrays may use int32 in historical files and int64 in G. Each original and exported file hash is checked separately; no bytes relabeled.')
for family in ['B1M','B1P','B1G']:print(family,{k:v for k,v in result[family].items() if k not in ['census','contrasts','overall_macros','shapes']},flush=True)
result={'status':'PASS','verified_utc':datetime.now(timezone.utc).isoformat(),'release_root':str(ROOT),'offline':True,'new_fit':False,'new_encoding':False,'new_vector_search':False,'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'versions':{'python':sys.version,'numpy':np.__version__},'families':result,'input_sha256':HASHES,'limitations':['B1-M/P retrieval rankings are independently rescored from packaged IDs/qrels; model fits and vector endpoints are not regenerated.','B1-M/P declared means and 20,000-draw locked percentile intervals are recomputed from saved rankings.','B1-G independently rescores210pure and450mixed saved top100 rankings and verifies before/after/delta arrays and90condition means. Full vector generation, sampled score errors and search are not replayed.','These controls remain inspected development evidence, not unseen confirmation.']}
output.parent.mkdir(parents=True,exist_ok=True)
with output.open('x',encoding='utf8',newline='\n') as stream:
    json.dump(result,stream,indent=2,allow_nan=False)
    stream.write('\n')
print(json.dumps({'status':'PASS','output':str(output)}),flush=True)
