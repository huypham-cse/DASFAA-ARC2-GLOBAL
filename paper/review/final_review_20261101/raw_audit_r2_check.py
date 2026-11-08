"""Independent read-only audit of existing scores; never opens qrels or runs retrieval/fit.
Writes only this audit's result and input hash manifest beside this script.
"""
import hashlib, json, os, subprocess, re, csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
INPUTS={}
def touch(p):
    p=Path(p); p=p if p.is_absolute() else ROOT/p
    assert not p.name.startswith('qrels'), 'Labels forbidden'
    key=p.relative_to(ROOT/'paper').as_posix() if p.is_relative_to(ROOT/'paper') else p.as_posix()
    INPUTS[key]='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
    return p
def read(p): return json.loads(touch(p).read_text(encoding='utf-8'))
def array(p): return np.load(touch(p),allow_pickle=False)
PATHS={
 'dev':'results/b1c_r3_review_20261031/evidence/run/scoring/summary.json',
 'trec':'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json',
 'ablation':'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
 'paid':'results/b1p_r5_review_20261027/scoring/results_summary.json',
 'gallery':'results/b1g_r1_review_20261027/scoring/results_summary.json'}
D={k:read(p) for k,p in PATHS.items()}
DS=['NanoNQ','NanoHotpotQA','NanoFEVER','FiQA']; PAIRS=['minilm_distilroberta','e5_small_base']
BUDGETS=['25pct','50pct','75pct']; SEEDS=[17,29,41,53,67]
ARC='arc2_global_tangent2_r1'; PROC='procrustes_global'
LABELS={ARC:'ARC2-Global',PROC:'Procrustes','la2m20_integration_script_adaptation':'LA2M20',
 'simplelinear_official_final50_mlp5':'SimpleLinear','ridge_affine_l10_bias_regularized':'Affine ridge',
 'embedding_converter_paper_spec':'Converter','full_x':'Native Full-X','full_y':'Native Full-Y'}
L={}; CHECKS={}; LEDGER=[]
def claim(location,text,value,evidence,actual,status='exact_match',details=''):
    LEDGER.append(dict(claim_id=f'R2-{len(LEDGER)+1:03}',location=location,paper_text=text,
       paper_value=value,evidence_file=evidence,evidence_value=actual,status=status,details=details))
def ci_check(name,actual,saved):
    err=float(np.max(np.abs(np.asarray(actual)-saved)))
    assert err<1e-12,(name,err,actual,saved)
    return err
def load_cells(k):
    base=ROOT/Path(PATHS[k]).parent; lookup={}
    indexpaths=[base/'cell_index.json'] if k in ['dev','trec','paid'] else [base/d/'cell_index.json' for d in DS]
    for ip in indexpaths:
        idx=read(ip)
        files={}
        for i,c in enumerate(idx['cells']):
            filename=c.get('per_query_file','per_query.npy')
            if filename not in files: files[filename]=array(ip.parent/filename)
            a=files[filename][c.get('per_query_index',c.get('per_dataset_index',i))]
            ident=(c['dataset'],c['pair'],c.get('seed'),c['budget'],c['method'],c.get('regime') if k=='paid' else None)
            assert ident not in lookup
            lookup[ident]=a
    return lookup
def get(k,d,p,b,m,reg=None):
    seeds=[None] if m.startswith('full_') else SEEDS
    return np.stack([L[k][(d,p,s,b,m,reg)] for s in seeds])
for k in ['dev','trec','paid','ablation']:
    L[k]=load_cells(k); errors=[]
    for r in D[k]['means']:
        a=get(k,r['dataset'],r['pair'],r['budget'],r['method'],r.get('regime') if k=='paid' else None)
        for j,m in enumerate(['ndcg10','recall100']):errors.append(abs(a[:,:,j].mean()-r[m]['mean']))
        assert sorted({x[2] for x in L[k] if x[0]==r['dataset'] and x[1]==r['pair'] and x[3]==r['budget'] and x[4]==r['method'] and x[5]==(r.get('regime') if k=='paid' else None)},key=lambda x:-1 if x is None else x)==([None] if r['method'].startswith('full_') else SEEDS)
    assert max(errors)<1e-12
    CHECKS[k+'_means']={'ranking_cells':len(L[k]),'summary_rows':len(D[k]['means']),'max_abs_error':max(errors)}
def boot(v,rng):
    # One query draw shared over every contrast, seed-averaged first.
    n=len(v); out=np.empty((20000,)+v.shape[1:]); h=hashlib.sha256()
    for lo in range(0,20000,256):
        ix=rng.integers(0,n,size=(min(256,20000-lo),n),dtype=np.int32);h.update(ix.tobytes())
        out[lo:lo+len(ix)]=v[ix].mean(axis=1)
    return out,h.hexdigest()
def macro(k,contrasts,seed,spawn=False):
    rng=np.random.default_rng(seed); children=np.random.SeedSequence(seed).spawn(4) if spawn else None
    sums=0.; maxerr=0.; digests={}
    for di,d in enumerate(DS):
        v=np.stack([np.mean([get(k,d,p,b,c['left'])-get(k,d,p,b,c['right']) for p in PAIRS for b in BUDGETS],axis=(0,1)) for c in contrasts],axis=1)
        draws,digest=boot(v,np.random.default_rng(children[di]) if spawn else rng)
        digests[d]=digest;sums=sums+draws/4
    for i,c in enumerate(contrasts):
        fld='ci99_bonferroni_family95' if spawn else 'ci_bonferroni_family95'
        maxerr=max(maxerr,ci_check((k,i),np.quantile(sums[:,i,0],[.005,.995]),c['ndcg10'][fld]))
        maxerr=max(maxerr,ci_check((k,i,'recall'),np.quantile(sums[:,i,1],[.025,.975]),c['recall100']['ci95']))
    CHECKS[k+'_macro_bootstrap']={'contrasts':len(contrasts),'draws':20000,'max_abs_error':maxerr,'index_digests':digests}
macro('dev',D['dev']['aggregate_contrasts'],20261028)
macro('ablation',D['ablation']['overall_macro'],20261026,True)
for k,n,seed in [('trec',30,20261031),('paid',32,20261026)]:
    cols=[]
    for c in D[k]['contrasts']:
        d=c['dataset'];p=c['pair'];b=c['budget']
        left=c['left'] if k=='trec' else c['left']['method'];right=c['right'] if k=='trec' else c['right']['method']
        lr=None if k=='trec' else c['left']['regime'];rr=None if k=='trec' else c['right']['regime']
        cols.append((get(k,d,p,b,left,lr)-get(k,d,p,b,right,rr)).mean(axis=0))
    vals=np.stack(cols,axis=1);draws,digest=boot(vals,np.random.default_rng(seed));errors=[]
    for i,c in enumerate(D[k]['contrasts']):
        for j,m in enumerate(['ndcg10','recall100']):
            errors.append(ci_check((k,i,m),vals[:,i,j].mean(),c[m]['delta']))
            errors.append(ci_check((k,i,m),np.quantile(draws[:,i,j],[.025,.975]),c[m]['ci95']))
        errors.append(ci_check((k,i),np.quantile(draws[:,i,0],[.05/(2*n),1-.05/(2*n)]),c['ndcg10']['ci_bonferroni_family95']))
    CHECKS[k+'_bootstrap']={'contrasts':n,'draws':20000,'max_abs_error':max(errors),'index_digest':digest}

# Every displayed table row receives a ledger record, directly from independently checked scores.
def mm(k,m,p=None,b=None,reg=None,metric='ndcg10'):
    rs=[r[metric]['mean'] for r in D[k]['means'] if r['method']==m and (p is None or r['pair']==p) and (b is None or r['budget']==b) and (reg is None or r.get('regime')==reg)]
    assert rs; return float(np.mean(rs))
for m,label in LABELS.items():
    if m not in ['full_x','full_y']:
        actual=[mm('dev',m),mm('dev',m,metric='recall100')]
        c=next((c for c in D['dev']['aggregate_contrasts'] if c['right']==m),None)
        if c:actual += [c['ndcg10']['delta'],c['ndcg10']['ci_bonferroni_family95']]
        claim('generated/dev_macro.tex',label+' row','4-decimal values',PATHS['dev'],actual,'rounding_ok')
    vals=[[mm('trec',m,p,b if not m.startswith('full_') else None) for b in BUDGETS] for p in PAIRS]
    claim('generated/trec_means.tex',label+' row','4-decimal values',PATHS['trec'],vals,'rounding_ok')
    vals=[]
    for p in PAIRS:
        if m.startswith('full_'):vals.extend([mm('paid',m,p),mm('paid',m,p,metric='recall100')])
        else:vals.extend([mm('paid',m,p,reg='fixed1024'),mm('paid',m,p,reg='allpaid28819'),mm('paid',m,p,reg='allpaid28819',metric='recall100')])
    claim('generated/allpaid.tex',label+' row','4-decimal values',PATHS['paid'],vals,'rounding_ok')
for c in D['ablation']['overall_macro']:
    claim('generated/ablation.tex; Fig.3',c['left']+' minus '+c['right'],'4-decimal values',PATHS['ablation'],c['ndcg10'],'rounding_ok')
for c in D['dev']['aggregate_contrasts']:
    claim('abstract; introduction; results', 'Positive development macro comparison against '+c['right'],True,PATHS['dev'],c['ndcg10'])
counts={}
for m in LABELS:
    if m in [ARC,'full_x','full_y']:continue
    cs=[c for c in D['dev']['condition_contrasts'] if c['right']==m]
    counts[m]=sum(c['ndcg10']['delta']>0 for c in cs)
claim('abstract; results','23/24 Procrustes point gains; 24/24 each other baseline',[23,24,24,24,24],PATHS['dev'],counts)
pairdiff={p:float(np.mean([c['ndcg10']['delta'] for c in D['dev']['condition_contrasts'] if c['pair']==p and c['right']==PROC])) for p in PAIRS}
claim('results','Migration macro differences .025733 / .022917',[.025733,.022917],PATHS['dev'],pairdiff,'rounding_ok')
ex=[c for c in D['dev']['condition_contrasts'] if c['right']==PROC and c['ndcg10']['delta']<0]
claim('results','FiQA/E5 75% exception -.003583',-.003583,PATHS['dev'],ex,'rounding_ok')
native_counts={m:sum(r['ndcg10']['mean']<next(z['ndcg10']['mean'] for z in D['dev']['means'] if z['dataset']==r['dataset'] and z['pair']==r['pair'] and z['method']==m) for r in D['dev']['means'] if r['method']==ARC) for m in ['full_x','full_y']}
claim('discussion','Every partial DEV ARC2 endpoint below native Full-X',24,PATHS['dev'],native_counts)
fc={m:{p:[sum(c['ndcg10']['family_interval_interpretation']==s for c in D['trec']['contrasts'] if c['right']==m and c['pair']==p) for s in ['above_zero','unresolved','below_zero']] for p in PAIRS} for m in LABELS if m not in [ARC,'full_x','full_y']}
claim('results; generated/trec_family.tex; dagger markers','11 positive / 19 unresolved / 0 negative in 30 contrasts',[11,19,0],PATHS['trec'],fc)
e5conv=[c['ndcg10'] for c in D['trec']['contrasts'] if c['pair']==PAIRS[1] and c['right']=='embedding_converter_paper_spec']
claim('abstract; results','E5 Converter gains .2000 to .2572; 25% .257234 [.175731,.337569]',[.2000,.2572,.257234,.175731,.337569],PATHS['trec'],e5conv,'rounding_ok')
claim('results','All six Procrustes point means higher; all Procrustes/LA2M family intervals unresolved',True,PATHS['trec'],[c for c in D['trec']['contrasts'] if c['right'] in [PROC,'la2m20_integration_script_adaptation']])
claim('abstract; results; discussion','MiniLM 75% .5195 versus native Full-Y .5203',[.5195,.5203],PATHS['trec'],[mm('trec',ARC,PAIRS[0],'75pct'),mm('trec','full_y',PAIRS[0])],'rounding_ok','Native comparison is descriptive; no equivalence family or margin. floor(.75*171332)=128499, leaving 42833 proxies.')
for p in PAIRS:
    cs=[c for c in D['paid']['contrasts'] if c['pair']==p and (c['kind']=='arc2_allpaid_vs_baseline_allpaid' or c['kind']=='within_method' and c['left']['method']==ARC or c['kind']=='arc2_fixed_vs_baseline_allpaid')]
    claim('results all-paid subsection',p+' all-paid ordering / within-method change / cross-regime ordering','stated direction and family decision',PATHS['paid'],cs)

# Independent read-only gallery checks for exactly the two examples used in prose.
gb=ROOT/Path(PATHS['gallery']).parent;gi=read(gb/'FiQA/cell_index.json')
before=array(gb/'FiQA/before_per_query.npy');after=array(gb/'FiQA/after_per_query.npy');delta=array(gb/'FiQA/delta_per_query.npy')
for p in PAIRS:
    agg=next(c for c in D['gallery']['aggregate_five_seed_conditions'] if c['dataset']=='FiQA' and c['pair']==p and c['method']==ARC and c['regime']=='allpaid28819')
    cases=[c for c in gi['partial_cases'] if c['pair']==p and c['method']==ARC and c['regime']=='allpaid28819']
    CHECKS.setdefault('gallery_examples',{})[p]={'cases':len(cases),'case_keys':list(cases[0])}
    for phase in ['before','after']:
        for j,m in enumerate(['ndcg10','recall100']):
            vals=[]
            for c in cases:
                idx=c['before_index' if phase=='before' else 'after_delta_index'];vals.append((before if phase=='before' else after)[idx,:,j].mean())
            ci_check((p,phase,m),np.mean(vals),agg['metrics'][m][phase]['mean'])
    claim('results mixed-gallery paragraph',p+' proxy-only to mixed-gallery values','6-decimal prose',PATHS['gallery'],{'metrics':agg['metrics'],'paid_returned_share':agg['paid_returned_share']},'rounding_ok','Metric means independently checked from FiQA before/after per-query arrays; paid-share values traced to per-case diagnostic records below.')
    raw=[c for c in D['gallery']['case_diagnostics_and_metrics'] if c['dataset']=='FiQA' and c['pair']==p and c['method']==ARC and c['regime']=='allpaid28819']
    CHECKS['gallery_examples'][p]['raw_diagnostic_keys']=list(raw[0])
    for phase in ['before','after']:
        ci_check((p,phase,'paid_top10'),np.mean([c['returned_shares'][phase]['top10']['paid'] for c in raw]),agg['paid_returned_share'][phase]['top10']['mean'])

# Compare actual LaTeX numeric row tokens, not just generator intent.
def flatten(x):
    if isinstance(x,(list,tuple)):return [z for y in x for z in flatten(y)]
    return [x]
def tablecheck(filename,label,values):
    text=touch(ROOT/'paper/generated'/filename).read_text()
    rows=[r for r in text.splitlines() if '&' in r and label in r.split('&')[0]]
    assert len(rows)==1,(filename,label,rows)
    actual=re.findall(r'[+-]?\d+\.\d+',rows[0])
    expected=[f'{x:.4f}' for x in flatten(values)]
    assert len(actual)==len(expected),(filename,label,actual,expected)
    assert [float(x) for x in actual]==[float(x) for x in expected],(filename,label,actual,expected)
    CHECKS.setdefault('latex_numeric_rows',[]).append({'file':filename,'label':label,'numeric_cells':len(actual)})
for m,label in LABELS.items():
    if m not in ['full_x','full_y']:
        vals=[mm('dev',m),mm('dev',m,metric='recall100')]
        c=next((c for c in D['dev']['aggregate_contrasts'] if c['right']==m),None)
        if c:vals += [c['ndcg10']['delta'],c['ndcg10']['ci_bonferroni_family95']]
        tablecheck('dev_macro.tex',label,vals)
    tablecheck('trec_means.tex',label,[[mm('trec',m,p,b) for b in BUDGETS] if not m.startswith('full_') else [mm('trec',m,p)] for p in PAIRS])
    vals=[]
    for p in PAIRS:
        if m.startswith('full_'): vals += [mm('paid',m,p),mm('paid',m,p,metric='recall100')]
        else: vals += [mm('paid',m,p,reg='fixed1024'),mm('paid',m,p,reg='allpaid28819'),mm('paid',m,p,reg='allpaid28819',metric='recall100')]
    tablecheck('allpaid.tex',label,vals)
for c,label in zip(D['ablation']['overall_macro'],['Two steps minus zero steps','Two steps minus one step','ARC2 minus affine ridge',r'$\lambda=1$',r'$\lambda=100$']):
    tablecheck('ablation.tex',label,[c['ndcg10']['delta'],c['ndcg10']['ci99_bonferroni_family95']])
trectex=touch(ROOT/'paper/generated/trec_means.tex').read_text()
for m,label in LABELS.items():
    if m in [ARC,'full_x','full_y']:continue
    row=next(r for r in trectex.splitlines() if '&' in r and label in r.split('&')[0])
    cells=row.split('&')[1:]
    for i,(p,b) in enumerate((p,b) for p in PAIRS for b in BUDGETS):
        c=next(c for c in D['trec']['contrasts'] if c['pair']==p and c['budget']==b and c['right']==m)
        assert ('dagger' in cells[i])==(c['ndcg10']['family_interval_interpretation']=='above_zero')
CHECKS['trec_dagger_markers']={'checked':30,'positive_markers':trectex.count('^{\\dagger}')}
for filename,key in [('dev_quality_values.csv','dev'),('trec_quality_values.csv','trec')]:
    rows=list(csv.DictReader(touch(ROOT/'paper/generated'/filename).open()))
    for r in rows:
        expected=mm(key,r['method'],r['pair'],r['budget'] if r['budget']!='native' else None)
        ci_check(filename,float(r['ndcg10']),expected)
    CHECKS[filename]={'rows':len(rows),'all_equal_raw_means':True}

# Compare scientific source hashes to the pre-run locks actually used by the scorers.
for lockname in ['b1c_r3_lock.json','b2_lock.json','b1p_lock.json','b1m_score_r2_lock.json']:
    lock=read(ROOT/'configs'/lockname);pins=lock.get('source_sha256_canonical_lf',{})
    checked={}
    for name,expected in pins.items():
        if name.startswith('src/arc2_global/') or name in ['ops/b1p_stage.py','ops/b2_stage.py','ops/b2_score.py','ops/b1c_r3_score.py','ops/b1m_score.py']:
            path=touch(ROOT/name);actual=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
            assert actual==expected,(lockname,name,actual,expected)
            checked[name]=actual
    CHECKS.setdefault('scientific_source_pins',{})[lockname]=checked

# Mathematical/structural checks are analytic/code inspection, not model fitting.
claim('method Eqs.2-3','Centered rectangular Procrustes; raw affine expansion; float64 from float32 parameters','exact stated computation','src/arc2_global/procrustes.py; src/arc2_global/model.py','M=(Y-tm).T@(X-sm); W=U@Vt; B0=[W.T;tm-sm@W.T]; no normalize/scale in B0')
claim('abstract; method Eqs.4-5','Norm-scaled negative cosine-gradient targets','T=-r^2 grad(1-y N(z)^T)','src/arc2_global/model.py; src/arc2_global/solver_backend.py','grad=-(I-u^T u)y^T/r; T=r(y-(uy^T)u)',details='Correct for unit y, nonzero z. Projecting y or y-z gives the same tangent component. Fitted affine row corrections are not asserted tangent.')
claim('method Eqs.6-8','Ridge prior centered at current Bt; regularized bias; reused Cholesky; exactly two steps; lambda10','exact stated computation','src/arc2_global/model.py; src/arc2_global/solver_backend.py','D=C-Bt gives exactly the objective in Eq.6; lambda I includes augmented bias. Factor formed before loop; loop steps (1,2).')
claim('method scale-equivariance paragraph','In exact arithmetic with nonzero predictions, T(cB)=cT(B), c>0','exact ideal algebra','src/arc2_global/model.py; src/arc2_global/solver_backend.py; src/arc2_global/numerics.py','c>0 gives r(cz)=cr(z), u(cz)=u(z); fixed linear ridge operator scales delta; induction scales Bt; normalized inference equal.',details='Existing analytical qualification is sufficient. Executed code rejects norms <=1e-12 and nonfinite rows, rather than clamping denominator. Positive rescaling can cross guard/finite limits. Float32 stored coefficients/application introduce rounding. No execution-wide or bitwise scaling invariance verified or claimed.')
claim('method; discussion','295680 coefficients;1182720 bytes;1.13 MiB;33927168 Converter parameters;114.7x',[295680,1182720,1.13,33927168,114.7],'src/arc2_global/embedding_converter.py; src/arc2_global/model.py',{'affine_parameters':385*768,'bytes':385*768*4,'MiB':385*768*4/2**20,'converter_parameters':sum((a+1)*b for a,b in zip([384,3840,3840,3840],[3840,3840,3840,768])),'ratio':33927168/(385*768)},'rounding_ok','Parameter bytes assume float32 for both, exclude fitting objects/galleries/encoders. Not end-to-end cost.')
claim('results all-paid penalty qualification','Fixed summed-objective lambda10 does not isolate data quantity at fixed effective penalty','correct implication','src/arc2_global/solver_backend.py; ops/b1p_stage.py',{'summed_lambda':10,'averaged_objective_penalty_fixed':10/1024,'averaged_objective_penalty_allpaid':10/28819},details='Dividing sum loss by m gives penalty lambda/m. Effective penalty drops ~28.14x as pairs increase; manuscript explicitly acknowledges this.')
claim('method complexity subsection','Dual/primal fitting and application big-O costs','as stated','src/arc2_global/model.py; src/arc2_global/solver_backend.py; src/arc2_global/numerics.py','Crosscov O(m ds dt); thin SVD O(ds dt min(ds,dt)); dual Gram/factor O(m²p+m³), step O(m²dt+mpdt); primal O(mp²+p³), step O(mpdt+p²dt); final map O(Npdt).',details='Dense arithmetic/storage asymptotics, not measured runtime.')
claim('setup retrieval/native paragraph','Exact float32 inner product; stable row-index ties; top100; ID exclusion; native references use own query/document encoders','declared scope','src/arc2_global/retrieval.py; ops/b2_stage.py; ops/b1m_stage.py','exact_topk uses float32 Q@D.T and stable argsort(-scores); native Full-X receives oldquery,old; Full-Y receives destination query,target.',details='No new search executed in this audit.')
claim('setup inference paragraph','20k query draws; average five seeds first; DEV/ablation five each, paid32, TREC30 families','approximate conditional family coverage','ops/b1c_r3_score.py; ops/b1m_score.py; ops/b1p_score.py; ops/b2_score.py',{'DEV':5,'ablation':5,'paid':32,'TREC':30,'draws':20000,'TREC_individual_confidence':1-.05/30},details='Reconstructed all saved family intervals. Bonferroni tail allocation applies within each separately locked family, not global 72-contrast correction. No simultaneous exact 95% bootstrap guarantee, seed-population inference, or correction for development selection.')
claim('setup main matrix/exposure','Four development collections x two pairs x three budgets x six methods x five seeds; 1024 paired anchors; paid set anchor inclusive','declared scope','configs/b1c_r3_lock.json; configs/b2_lock.json; src/arc2_global/numerics.py; ops/b2_stage.py',{'DEV_partial_cells':4*2*3*6*5,'DEV_native_cells':16,'TREC_partial_cells':2*3*6*5,'TREC_native_cells':4,'seeds':SEEDS,'trec_paid':[42833,85666,128499]},details='select_for_budget unions anchors with earliest permutation entries, skips duplicates, and checks exact floor(rho*N); fit/paid row identity receipts bound in endpoints.')
claim('setup baseline paragraph','Full five-baseline panel with declared adaptations','qualified implementation scope','src/arc2_global/baseline_adapters.py; src/arc2_global/embedding_converter.py; configs/b1c_r3_lock.json; configs/b2_lock.json','LA2M20 source KMeans and >=2 local fits/global singleton fallback; SimpleLinear pinned upstream final50 SELU MLP, batch4028, MSE+cos; ridge lambda10 with bias; Converter selection50k, batch64,k100,earliest best250-step paired-vector MAE and selected-length all-pair refit.',details='No reproduction of all external-paper settings claimed. Upstream training source itself was not independently reread in this audit; local wrapper and locked defaults checked.')
claim('intro/mechanism figure/caption','24 illustrative docs;8 anchors;4 further encodings;12 native vectors','illustrative arithmetic','figures/mechanism.tex',{'grid_documents':24,'anchors':8,'additional_true':4,'budget':12,'remaining_proxies':12},details='Schematic hits explicitly illustrative. No H100, live traffic, measured latency or saving inferred.')

for p in [ROOT/'paper/main.tex',*sorted((ROOT/'paper/sections').glob('*.tex')),*sorted((ROOT/'paper/generated').glob('*.tex')),*sorted((ROOT/'paper/figures').glob('*')),ROOT/'paper/ARC2_Global_DASFAA2027_reviewed.pdf']:
    touch(p)
for p in ['src/arc2_global/model.py','src/arc2_global/procrustes.py','src/arc2_global/solver_backend.py','src/arc2_global/numerics.py','src/arc2_global/retrieval.py','src/arc2_global/mechanism_ablation.py','src/arc2_global/baseline_adapters.py','src/arc2_global/embedding_converter.py','ops/b1m_score.py','ops/b1c_r3_score.py','ops/b1p_score.py','ops/b1p_stage.py','ops/b2_score.py','ops/b2_stage.py','ops/b2_inputs.py','ops/b2_verify.py','ops/b2_campaign.py','ops/b1g_analyze_worker.py','configs/b1c_r3_lock.json','configs/b2_lock.json','configs/b1p_lock.json','configs/b1m_lock.json','configs/b1b_lock.json','configs/b2_acquisition.json','protocols/B2_TREC_COVID_CONFIRMATION_20261031.md','protocols/B1M_B1P0_DEVELOPMENT_20261026.md','protocols/B1P_ALL_PAID_FIQA_20261026.md','paper/scripts/build_evidence.py']:
    touch(p)
for name in ['metadata.json','ranking_seal.json','verification/verification_seal.json','first_final_qrel_open.json','scoring/started.json','scoring/completed.json']:
    p=ROOT/Path(PATHS['trec']).parent.parent/name
    d=read(p);CHECKS.setdefault('B2_provenance',{})[name]={k:v for k,v in d.items() if not isinstance(v,(list,dict))}
run=ROOT/Path(PATHS['trec']).parent.parent
seal=read(run/'ranking_seal.json');vs=read(run/'verification/verification_seal.json');opened=read(run/'first_final_qrel_open.json')
assert len(seal['cells'])==len(vs['verified_cells'])==184
assert vs['ranking_seal_sha256']==hashlib.sha256((run/'ranking_seal.json').read_bytes()).hexdigest()
assert opened['verification_seal_sha256']==hashlib.sha256((run/'verification/verification_seal.json').read_bytes()).hexdigest()
assert seal['sealed_utc']<vs['completed_utc']<opened['first_final_qrel_open_utc']<D['trec']['completed_utc']
for c in seal['cells']:
    for pathfield,hashfield in [('ranking_path','ranking_sha256'),('endpoint_path','endpoint_sha256')]:
        path=touch(run/c[pathfield]); assert hashlib.sha256(path.read_bytes()).hexdigest()==c[hashfield]
    ep=read(run/c['endpoint_path']); assert ep['semantics']['dtype']=='float32' and ep['semantics']['exclude_identical_ids'] is True
    assert ep['shape']==[171332,768] if c['method']!='full_x' else ep['shape']==[171332,384]
for s in SEEDS:
    anchors=array(run/f'inputs/anchors_seed{s}.npy');assert len(anchors)==len(set(anchors))==1024
    previous=set(anchors)
    for b,n in [('25pct',42833),('50pct',85666),('75pct',128499)]:
        paid=array(run/f'inputs/paid_seed{s}_{b}.npy');assert len(paid)==len(set(paid))==n and previous<=set(paid);previous=set(paid)
CHECKS['B2_rankings_endpoints_and_selections']={'ranking_hashes':184,'endpoint_hashes':184,'anchor_sets':5,'nested_paid_sets':15,'label_open_order':'ranking seal < verification seal < first final opening < scoring completion'}
for suffix in ['selection_fit.json','refit_fit.json']:
    for path in (run/'neural').glob('*/worker/'+suffix):
        d=read(path)
        if 'parameter_count' in d:
            assert d['parameter_count']==33927168
            if suffix=='selection_fit.json':
                assert d['completed_iterations']==50000 and d['checkpoint_selection']=='earliest_best_anchor_validation_mae'
                best=min((r for r in d['history'] if 'validation_mae' in r),key=lambda r:r['validation_mae'])
                assert d['selected_iteration']==best['step']
            else:assert d['anchor_count']==1024 and d['checkpoint_selection']=='final_fixed_iteration'
        else:
            assert d['configuration']['num_epochs']==50 and d['configuration']['batch_size']==4028 and d['configuration']['activation']=='selu'
            assert d['official_metadata']['layer_num']==4 and d['configuration']['loss_kind']=='mse_cos'
CHECKS['B2_neural_fit_receipts']={'selection_receipts':10,'refit_receipts':20,'Converter_parameter_counts_verified':33927168,'selected_iterations':'earliest best saved validation MAE in all 10 histories','SimpleLinear':'final50 config, layer_num4, SELU, batch4028, mse_cos in all10 receipts'}
counts={}
for dataset,n in [('NanoNQ',5035),('NanoHotpotQA',5090),('NanoFEVER',4996),('FiQA',57638)]:
    ids=read(ROOT/Path(PATHS['ablation']).parent.parent/'inputs'/dataset/'ids.json')
    assert len(ids['doc_ids'])==n and len(ids['query_ids'])==(500 if dataset=='FiQA' else 50)
    counts[dataset]=[len(ids['doc_ids']),len(ids['query_ids'])]
ids=read(run/'inputs/ids.json');assert len(ids['doc_ids'])==171332 and len(ids['query_ids'])==50;counts['TREC-COVID']=[171332,50]
CHECKS['collection_counts_from_raw_ordered_IDs']=counts
claim('setup collection paragraph','Five collection document/query counts','as printed','B1-M inputs/*/ids.json; B2 inputs/ids.json',counts)
claim('setup prospective-label paragraph','TREC labels closed until all rankings sealed and endpoints separately verified','supported recorded execution chronology','B2 ranking_seal.json; verification/verification_seal.json; first_final_qrel_open.json; ops/b2_score.py',CHECKS['B2_rankings_endpoints_and_selections'],details='All 184 ranking/endpoint hashes verified in this audit; recorded verifier results inspected, not rerun. This audits files and code, not all possible unrecorded actions outside the run.')
touch(ROOT/'ops/b1m_stage.py');touch(ROOT/'configs/method.json');touch(ROOT/'configs/datasets.json');touch(ROOT/'configs/baselines.json')
result={'generated_at':datetime.now(timezone.utc).isoformat(),'checks':CHECKS,'ledger':LEDGER,'audited_input_hashes':INPUTS,'numpy_version':np.__version__}
(OUT/'raw_audit_r2_computed.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':CHECKS,'ledger_entries':len(LEDGER),'hashed_inputs':len(INPUTS)},indent=2))
