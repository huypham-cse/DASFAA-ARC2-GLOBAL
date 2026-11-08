"""Fresh offline release audit. Reads raw evidence only; writes own trace."""
from pathlib import Path
import collections, csv, hashlib, json, math, sys
import numpy as np
import pyarrow.parquet as pq

ROOT=Path('D:/DASFAA-2027-paper-release')
OUT=Path(__file__).resolve().parent
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
ma={};mc=[];maximum=0
for d in DATASETS:
    sc=M/f'scoring_r2_binary/{d}'
    ix=read(sc/'cell_index.json');saved=arr(sc/'per_query.npy')
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
    for j,m in enumerate(['ndcg10','recall100']):
        error(np.quantile(draw[:,j],[.025,.975]),r[m]['ci95'])
        if r['scope']=='overall' and j==0:error(np.quantile(draw[:,j],[.005,.995]),r[m]['ci99_bonferroni_family95'])
result['B1M']={'cells':len(mc),'metric_values':sum(x.size for x in ma.values()),'max_metric_error':maximum,'means':len(ms['means']),'condition_contrasts':len(ms['contrasts']),'encoder_macros':len(ms['per_encoder_macro']),'overall_macros':ms['overall_macro'],'census':census(mc),'status':'PASS'}
pi=read(P/'scoring/cell_index.json');pc=pi['cells'];pa=arr(P/'scoring/per_query.npy');computed=np.empty_like(pa)
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
result['B1G']={'partial_cases':len(cases),'pure_galleries':sum(v['before_shape'][0] for v in gcounts.values()),'array_values':gvalues,'conditions':len(gs['aggregate_five_seed_conditions']),'shapes':gcounts,'negative_condition_delta_counts':{m:sum(r['metrics'][m]['delta_of_query_means']['mean']<0 for r in gs['aggregate_five_seed_conditions']) for m in ['ndcg10','recall100']},'status':'PASS_scored_arrays_only_no_vector_replay'}
for family in ['B1M','B1P','B1G']:print(family,{k:v for k,v in result[family].items() if k not in ['census','contrasts','overall_macros','shapes']},flush=True)
(OUT/'numeric_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
(OUT/'numeric_input_hashes.json').write_text(json.dumps(HASHES,indent=2)+'\n',encoding='utf8')
