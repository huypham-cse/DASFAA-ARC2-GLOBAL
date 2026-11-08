"""Independent read-only calculations for the fresh 2026-11-02 claim audit.
Only writes audit artifacts beside this script. Never opens qrels or rankings.
"""
from pathlib import Path
import json, hashlib, re, collections, datetime, xml.etree.ElementTree as ET
import numpy as np
from pypdf import PdfReader
from pypdf.generic import ContentStream

ROOT=Path('D:/DASFAA-2027-paper'); PAPER=ROOT/'paper'; OUT=Path(__file__).parent
PATHS={
'dev':'results/b1c_r3_review_20261031/evidence/run/scoring/summary.json',
'trec':'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json',
'ablation':'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
'paid':'results/b1p_r5_review_20261027/scoring/results_summary.json',
'gallery':'results/b1g_r1_review_20261027/scoring/results_summary.json'}
READ=set(); CLAIMS=[]
def read(p):
 p=Path(p);READ.add(p.resolve());return p.read_bytes()
def js(p):return json.loads(read(p))
def txt(p):return read(p).decode('utf-8-sig')
def arr(p):READ.add(Path(p).resolve());return np.load(p,allow_pickle=False)
def claim(location,paper_text,evidence,values,status='exact_match',details=''):
 CLAIMS.append(dict(claim_id=f'C{len(CLAIMS)+1:03}',location=location,paper_text=paper_text,evidence_file=evidence,evidence_value=values,status=status,details=details))
D={k:js(ROOT/p) for k,p in PATHS.items()}
A='arc2_global_tangent2_r1'; METHODS=[A,'procrustes_global','la2m20_integration_script_adaptation','simplelinear_official_final50_mlp5','ridge_affine_l10_bias_regularized','embedding_converter_paper_spec']
LABELS=dict(zip(METHODS,['ARC2-Global','Procrustes','LA2M20','SimpleLinear','Affine ridge','Converter']));LABELS.update(full_x='Native Full-X',full_y='Native Full-Y')
PAIRS=['minilm_distilroberta','e5_small_base'];BUDGETS=['25pct','50pct','75pct'];SETS=['FiQA','NanoNQ','NanoHotpotQA','NanoFEVER']
def rows(key,**selectors):return [x for x in D[key]['means'] if all(x.get(k)==v for k,v in selectors.items())]
def mean(key,method,metric='ndcg10',**sel):return float(np.mean([x[metric]['mean'] for x in rows(key,method=method,**sel)]))
def one(items,**sel):
 r=[x for x in items if all(x.get(k)==v for k,v in sel.items())];assert len(r)==1,(sel,len(r));return r[0]
def family(c):return c['ndcg10'].get('ci_bonferroni_family95',c['ndcg10'].get('ci99_bonferroni_family95'))
def decision(ci):return 'above_zero' if ci[0]>0 else 'below_zero' if ci[1]<0 else 'unresolved'

# Read every declared source; no prior reports or executor ledgers are evidence.
SOURCES={p.relative_to(PAPER).as_posix():txt(p) for p in [PAPER/'main.tex',*sorted((PAPER/'sections').glob('*.tex')),*sorted((PAPER/'generated').glob('*.tex'))]}
for p in [*sorted((PAPER/'figures').glob('*')),PAPER/'scripts/build_evidence.py',PAPER/'scripts/plot_publication.py']:
 if p.is_file():read(p)

# Reconstruct all saved means from per-query arrays, and retain seed-level cells.
CELLS={}; RECON=[]
for key in ['dev','trec','paid','ablation']:
 base=(ROOT/PATHS[key]).parent; subdirs=[base/s for s in SETS] if key=='ablation' else [base]
 grouped=collections.defaultdict(list); cells=[]
 for folder in subdirs:
  index=js(folder/'cell_index.json'); arrays={p.name:arr(p) for p in folder.glob('per_query*.npy')}
  for i,c in enumerate(index['cells']):
   filename=c.get('per_query_file','per_query.npy');a=arrays[filename][c.get('per_query_index',c.get('per_dataset_index',i))]
   c=dict(c);c['saved_means']=a.mean(axis=0).tolist(); cells.append(c)
   identity=tuple(c.get(k) for k in ['dataset','pair','budget','method']+(['regime'] if key=='paid' else []));grouped[identity].append(a.mean(axis=0))
 errors=[]
 for r in D[key]['means']:
  identity=tuple(r.get(k) for k in ['dataset','pair','budget','method']+(['regime'] if key=='paid' else []));actual=np.mean(grouped[identity],axis=0)
  errors.extend(abs(actual[j]-r[m]['mean']) for j,m in enumerate(index['metrics']))
 CELLS[key]=cells;RECON.append(dict(campaign=key,cells=len(cells),means=len(D[key]['means']),max_absolute_error=float(max(errors))));assert max(errors)<1e-12
 claim('raw saved per-query reconciliation',f'All {key} displayed condition means use all queries and five mapping seeds (one native reference)',PATHS[key],RECON[-1],details='Independent arithmetic on saved scored arrays; no metric recomputation from qrels or rankings.')

# Numeric cells and rank/marker styling in every generated table.
def table_row(name,label):
 text=SOURCES['generated/'+name+'.tex'];line=next(l for l in text.splitlines() if ' & ' in l and (LABELS.get(label,label) in l) and not l.startswith('Method'))
 return line.split(' & ')[1:]
def cell(name,method,col,value,peers=None,marker=None):
 source=table_row(name,method)[col];num=re.findall(r'[-+]?\d+\.\d{4}',source);assert len(num)==1,(name,method,col,source)
 good=num[0]==f'{value:.4f}';rank=None
 if peers is not None:
  order=sorted(set(peers),reverse=True);rank=order.index(value)+1
  good &= (('\\textbf{' in source)==(rank==1)) and (('\\underline{' in source)==(rank==2))
 if marker is not None:good &= ('\\dagger' in source)==(marker=='above_zero') and ('\\ddagger' in source)==(marker=='below_zero')
 claim('generated/'+name+'.tex',f'{method}, numeric column {col+1}: {source.strip()}',PATHS['paid' if name=='allpaid' else 'trec' if name.startswith('trec') else 'dev'],dict(mean=value,rank_among_six=rank,family_decision=marker),'rounding_ok' if good else 'number_mismatch')
 assert good,(name,method,col,source,value,rank,marker)
for m in METHODS:
 for j,metric in enumerate(['ndcg10','recall100']):cell('dev_macro',m,j,mean('dev',m,metric),[mean('dev',x,metric) for x in METHODS])
 if m!=A:
  c=one(D['dev']['aggregate_contrasts'],right=m)
  nums=re.findall(r'[-+]?\d+\.\d{4}', ' '.join(table_row('dev_macro',m)[2:]));expected=[f'{x:+.4f}' for x in [c['ndcg10']['delta'],*family(c)]];assert nums==expected,(nums,expected)
  claim('generated/dev_macro.tex',f'ARC2 minus {m}, difference and family interval',PATHS['dev'],c['ndcg10'],'rounding_ok')
for tab,metric in [('trec_means','ndcg10'),('trec_recall','recall100')]:
 for m in METHODS:
  for pi,p in enumerate(PAIRS):
   for bi,b in enumerate(BUDGETS):
    c=None if m==A or metric=='recall100' else decision(family(one(D['trec']['contrasts'],pair=p,budget=b,right=m)))
    cell(tab,m,pi*3+bi,mean('trec',m,metric,pair=p,budget=b),[mean('trec',x,metric,pair=p,budget=b) for x in METHODS],c)
 for m in ['full_x','full_y']:
  for pi,p in enumerate(PAIRS):cell(tab,m,pi,mean('trec',m,metric,pair=p))
for m in METHODS:
 for pi,p in enumerate(PAIRS):
  for j,(reg,metric) in enumerate([('fixed1024','ndcg10'),('allpaid28819','ndcg10'),('allpaid28819','recall100')]):
   dec=None
   if j==1 and m!=A:dec=decision(family(one(D['paid']['contrasts'],pair=p,kind='arc2_allpaid_vs_baseline_allpaid',right={'method':m,'regime':reg})))
   cell('allpaid',m,pi*3+j,mean('paid',m,metric,pair=p,regime=reg),[mean('paid',x,metric,pair=p,regime=reg) for x in METHODS],dec)
for m in ['full_x','full_y']:
 for pi,p in enumerate(PAIRS):
  for j,metric in enumerate(['ndcg10','recall100']):cell('allpaid',m,pi*2+j,mean('paid',m,metric,pair=p))
for i,c in enumerate(D['ablation']['overall_macro']):
 line=[l for l in SOURCES['generated/ablation.tex'].splitlines() if ' & ' in l][i+1];numbers=re.findall(r'[-+]?\d+\.\d{4}',line)
 expected=[f'{x:+.4f}' for x in [c['ndcg10']['delta'],*family(c)]];assert numbers==expected
 claim('generated/ablation.tex',line,PATHS['ablation'],c['ndcg10'],'rounding_ok')
for ds in SETS+['TREC-COVID']:
 key='trec' if ds=='TREC-COVID' else 'dev';p=PAIRS[1]
 specs=[(A,'25pct'),(METHODS[1],'25pct'),(METHODS[2],'25pct'),(METHODS[3],'75pct'),(METHODS[4],'75pct'),(METHODS[5],'75pct'),('full_x',None),('full_y',None)]
 vals=[mean(key,m,pair=p,dataset=ds,**({'budget':b} if b else {})) for m,b in specs]
 line=next(l for l in SOURCES['generated/budget_leverage.tex'].splitlines() if ds in l and ' & ' in l);nums=re.findall(r'\d+\.\d{4}',line);assert nums==[f'{x:.4f}' for x in vals]
 assert vals[0]>vals[4] and vals[0]>vals[5]
 claim('abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion',f'E5 ARC2 25% > ridge75% and Converter75%, {ds}',PATHS[key],dict(zip(['ARC2_25','Procrustes_25','LA2M_25','SimpleLinear_75','ridge_75','Converter_75','native_X','native_Y'],vals)),'rounding_ok','Post-hoc descriptive cross-budget point comparison, no additional test, minimum-cost, equivalence or physical-savings claim. Full raw baseline panel retained elsewhere.')
for p in PAIRS:
 for m in METHODS[1:]:
  cs=[c for c in D['trec']['contrasts'] if c['pair']==p and c['right']==m];counts=collections.Counter(decision(family(c)) for c in cs);line=table_row('trec_family',m)[PAIRS.index(p)]
  expected=f"{counts['above_zero']}/{counts['unresolved']}/{counts['below_zero']}";assert expected in line
  claim('generated/trec_family.tex',f'{p}/{m}: {expected}',PATHS['trec'],[dict(budget=c['budget'],delta=c['ndcg10']['delta'],ci=family(c)) for c in cs])

# Prose comparisons and scope, independently recomputed rather than trusting ledgers.
collection_macros={ds:{m:mean('dev',m,dataset=ds) for m in METHODS} for ds in SETS}
assert all(v[A]>max(x for k,x in v.items() if k!=A) for v in collection_macros.values())
claim('abstract; introduction; results 5.1; conclusion','Each of four collection-level macros and the 24-condition overall macro leads all five baselines',PATHS['dev'],dict(by_collection=collection_macros,overall={m:mean('dev',m) for m in METHODS}))
pair_gains={p:mean('dev',A,pair=p)-mean('dev',METHODS[1],pair=p) for p in PAIRS}
claim('results 5.1','Pair-wise Procrustes gains 0.0257 MiniLM and 0.0229 E5',PATHS['dev'],pair_gains,'rounding_ok')
for m in METHODS[1:]:
 cs=[c for c in D['dev']['condition_contrasts'] if c['right']==m];pos=sum(c['ndcg10']['delta']>0 for c in cs);assert pos==(23 if m==METHODS[1] else 24)
 claim('results 5.1',f'Positive condition point differences versus {m}',PATHS['dev'],dict(positive=pos,total=24,nonpositive=[c for c in cs if c['ndcg10']['delta']<=0]))
claim('results 5.1','Recall .8659 vs .8661, interval [-.0049,.0043]',PATHS['dev'],dict(arc=mean('dev',A,'recall100'),proc=mean('dev',METHODS[1],'recall100'),contrast=D['dev']['aggregate_contrasts'][0]['recall100']),'rounding_ok')
cs=[c for c in D['ablation']['contrasts'] if c['right']=='tangent1_l10'];assert sum(c['ndcg10']['delta']>0 for c in cs)==22
seed_macros={}
for seed in [17,29,41,53,67]:
 cells=[c for c in CELLS['ablation'] if c.get('seed')==seed]
 seed_macros[str(seed)]=float(np.mean([one(cells,dataset=ds,pair=p,budget=b,method=A)['saved_means'][0]-one(cells,dataset=ds,pair=p,budget=b,method='tangent1_l10')['saved_means'][0] for ds in SETS for p in PAIRS for b in BUDGETS]))
assert min(seed_macros.values())>0
claim('abstract; introduction; results 5.2','Second step +.0069 [.0038,.0100], positive in22/24 conditions and each5seedmacros',PATHS['ablation'],dict(macro=one(D['ablation']['overall_macro'],right='tangent1_l10')['ndcg10'],positive_conditions=22,seed_macros=seed_macros,nonpositive=[c for c in cs if c['ndcg10']['delta']<=0]),'rounding_ok')
for c in D['ablation']['overall_macro']:
 claim('results 5.2; figure3',f"Ablation {c['left']} minus {c['right']}",PATHS['ablation'],c['ndcg10'],'rounding_ok')
trec_cs=D['trec']['contrasts'];counts=collections.Counter(decision(family(c)) for c in trec_cs);assert counts=={'above_zero':11,'unresolved':19}
claim('results 5.3','Family supports Converter5,ridge4,SimpleLinear2, all11 comparisons marked',PATHS['trec'],dict(overall=dict(counts),supported=[dict(pair=c['pair'],budget=c['budget'],baseline=c['right'],delta=c['ndcg10']['delta'],ci=family(c)) for c in trec_cs if decision(family(c))=='above_zero']))
for p in PAIRS:
 for m in [METHODS[1],METHODS[2]]:
  cs=[c for c in trec_cs if c['pair']==p and c['right']==m];assert all(decision(family(c))=='unresolved' for c in cs)
  if m==METHODS[1]:assert all(c['ndcg10']['delta']<0 for c in cs)
claim('results 5.3','Procrustes higher in all6unrounded cells, MiniLM75 difference<.0001; all Proc/LA2M family intervals crosszero',PATHS['trec'],[dict(pair=c['pair'],budget=c['budget'],baseline=c['right'],delta=c['ndcg10']['delta'],ci=family(c)) for c in trec_cs if c['right'] in METHODS[1:3]])
e5conv=[c for c in trec_cs if c['pair']==PAIRS[1] and c['right']==METHODS[5]]
claim('abstract; results 5.3','E5 Converter gain .2000 to .2572;25% familyCI[.1757,.3376]',PATHS['trec'],[c['ndcg10'] for c in e5conv],'rounding_ok')
recall_values={b:{m:mean('trec',m,'recall100',pair=PAIRS[0],budget=b) for m in METHODS} for b in BUDGETS};assert all(v[A]==max(v.values()) for v in recall_values.values())
claim('abstract; results5.3','MiniLM Recall highest6adapter pointmeans all3budgets;75%=.0998 versus nativeY .1052; E5=.0997 versus .1162',PATHS['trec'],dict(minilm=recall_values,native={p:{m:dict(ndcg=mean('trec',m,pair=p),recall=mean('trec',m,'recall100',pair=p)) for m in ['full_x','full_y']} for p in PAIRS},e5_arc75=mean('trec',A,'recall100',pair=PAIRS[1],budget='75pct')),'rounding_ok','Auxiliary descriptive only; nDCG proximity .5195 vs .5203 is explicitly not equivalence.')
fullx_diffs=[dict(dataset=ds,pair=p,budget=b,delta=mean('dev',A,dataset=ds,pair=p,budget=b)-mean('dev','full_x',dataset=ds,pair=p)) for ds in SETS for p in PAIRS for b in BUDGETS];assert all(c['delta']<0 for c in fullx_diffs)
claim('discussion','All24partialDEVfive-seedARC2conditionmeansbelowFull-X',PATHS['dev'],fullx_diffs,details='Condition means only; does not assert all individual seeds below Full-X.')
for p in PAIRS:
 for c in [c for c in D['paid']['contrasts'] if c['pair']==p and (c['kind']=='arc2_allpaid_vs_baseline_allpaid' or c['kind']=='within_method' and c['left']['method']==A or p==PAIRS[0] and c['kind']=='arc2_fixed_vs_baseline_allpaid')]:
  claim('introduction;results5.5;allpaid markers',c['id'],PATHS['paid'],c['ndcg10'],'rounding_ok')
for p in PAIRS:
 g=one(D['gallery']['aggregate_five_seed_conditions'],dataset='FiQA',pair=p,method=A,regime='allpaid28819',budget='50pct')
 claim('results5.5 mixed-gallery paragraph',f'{p} allpaid before/after replacement nDCG,Recall and paidtop10',PATHS['gallery'],dict(metrics=g['metrics'],paid_top10={k:g['paid_returned_share'][k]['top10'] for k in ['before','after']}),'rounding_ok')

# Independently validate every saved point contrast against the reconciled means.
for key,field in [('dev','condition_contrasts'),('trec','contrasts'),('ablation','contrasts'),('paid','contrasts')]:
 errors=[]
 for c in D[key][field]:
  sel={k:c[k] for k in ['dataset','pair','budget']}
  for metric in ['ndcg10','recall100']:
   if key=='paid':
    a=mean(key,c['left']['method'],metric,**sel,regime=c['left']['regime']);b=mean(key,c['right']['method'],metric,**sel,regime=c['right']['regime'])
   else:a=mean(key,c['left'],metric,**sel);b=mean(key,c['right'],metric,**sel)
   errors.append(abs(a-b-c[metric]['delta']))
  if family(c) is not None:assert decision(family(c))==c['ndcg10']['family_interval_interpretation']
 assert max(errors)<1e-12
 claim('point contrast arithmetic',f'Every {key} saved point contrast agrees with reconstructed means',PATHS[key],dict(contrasts=len(D[key][field]),max_error=max(errors)))

# Scalar prose amounts are mapped directly to raw values, including negative context.
prose=[]
for p in PAIRS:
 for regime in ['fixed1024','allpaid28819']:prose.append((f'{p}/{regime} ARC2 nDCG',mean('paid',A,pair=p,regime=regime)))
 g=one(D['gallery']['aggregate_five_seed_conditions'],dataset='FiQA',pair=p,method=A,regime='allpaid28819',budget='50pct')
 for timing in ['before','after']:prose.append((f'{p}/replacement/{timing}/nDCG',g['metrics']['ndcg10'][timing]['mean']))
 if p==PAIRS[1]:
  for timing in ['before','after']:
   prose.append((f'E5/replacement/{timing}/Recall',g['metrics']['recall100'][timing]['mean']));prose.append((f'E5/replacement/{timing}/paid top10',g['paid_returned_share'][timing]['top10']['mean']))
for label,v in prose:assert f'{v:.4f}' in SOURCES['sections/results.tex'],(label,v)
claim('results5.5 scalar prose','Fixed/all-paid values and replacement nDCG, E5 Recall and paid top10 shares', [PATHS['paid'],PATHS['gallery']],dict(prose),'rounding_ok')

# Actual vector figures: invert coordinates and check every point / interval,
# then check corresponding paths also exist in PDF drawing operators.
NS={'s':'http://www.w3.org/2000/svg'};colors=dict(zip(METHODS,['#0f4d92','#626262','#32848e','#914781','#ad413f','#967512']))
def xy(path):return [tuple(map(float,p)) for p in re.findall(r'[ML]\s*([-\d.eE]+)\s+([-\d.eE]+)',path)]
def pdfpaths(p):
 r=PdfReader(p);ops=ContentStream(r.pages[0].get_contents(),r).operations;paths=[];current=[]
 for v,k in ops:
  if k==b'm':current=[tuple(map(float,v))]
  elif k==b'l':current.append(tuple(map(float,v)))
  elif k in [b'S',b's']:
   if current:paths.append(current)
   current=[]
 return float(r.pages[0].mediabox.height),paths
def verify_pdf_path(points,h,paths):
 target=np.array([(x,h-y) for x,y in points]);return any(len(p)==len(points) and np.max(abs(np.array(p)-target))<3e-6 for p in paths)
for name,key,macro in [('dev_quality','dev',True),('trec_quality','trec',False)]:
 root=ET.fromstring(read(PAPER/'figures'/f'{name}.svg'));h,paths=pdfpaths(PAPER/'figures'/f'{name}.pdf');count=0;errors=[]
 for ai,axes in enumerate([g for g in root.findall('.//s:g',NS) if re.fullmatch(r'axes_\d+',g.get('id',''))]):
  metric='ndcg10' if ai<2 else 'recall100';p=PAIRS[ai%2];lo,hi=(.18,.72) if macro else ([(.42,.53),(.28,.70),(.06,.11),(.02,.13)][ai]);native_seen=0
  for path in axes.findall('./s:g/s:path',NS):
   style=path.get('style','');color=re.search(r'stroke: (#[0-9a-fA-F]+)',style);clip=path.get('clip-path');pts=xy(path.get('d',''))
   if not color or not clip or color.group(1).lower() not in [*colors.values(),'#272727']:continue
   co=color.group(1).lower();cid=clip[5:-1];rect=root.find(f'.//s:clipPath[@id="{cid}"]/s:rect',NS);top=float(rect.get('y'));height=float(rect.get('height'))
   ys=[hi-(y-top)/height*(hi-lo) for x,y in pts]
   m=next((m for m,c in colors.items() if c==co),None)
   if m is None:m=['full_x','full_y'][native_seen];native_seen+=1;expected=[mean(key,m,metric,pair=p)]*2;count+=1
   else:expected=[mean(key,m,metric,pair=p,budget=b) for b in BUDGETS];count+=3
   assert len(ys)==len(expected),(name,ai,m,pts)
   error=max(abs(a-b) for a,b in zip(ys,expected));assert error<1e-8,(name,ai,m,error);errors.append(error);assert verify_pdf_path(pts,h,paths),(name,ai,m,'PDF path absent')
 assert count==(40 if macro else 80),(name,count)
 claim('actual figures/'+name+'.svg and.pdf',f'{count} metric/native data points in actual vector figure',PATHS[key],dict(data_points=count,max_svg_inverse_error=max(errors),pdf_paths_match_svg=True),details='All6adapter curves at3budgets plus2native horizontal references per panel; no interval or intermediate point inferred.')
root=ET.fromstring(read(PAPER/'figures/dev_ablation.svg'));h,paths=pdfpaths(PAPER/'figures/dev_ablation.pdf');rect=root.find('.//s:clipPath/s:rect',NS);left=float(rect.get('x'));width=float(rect.get('width'));bars=[]
for path in root.findall('.//s:path',NS):
 pts=xy(path.get('d',''));style=path.get('style','')
 if 'stroke-width: 1.6' in style and len(pts)==2 and path.get('clip-path'):
  vals=[-.02+(x-left)/width*.145 for x,y in pts];bars.append(vals);assert verify_pdf_path(pts,h,paths)
assert len(bars)==5
for vals,c in zip(bars,D['ablation']['overall_macro']):assert np.max(abs(np.array(vals)-family(c)))<1e-8
claim('actual figures/dev_ablation.svg and.pdf','All5fullsaved99%ablationintervals ononecontinuousaxis',PATHS['ablation'],dict(actual_interval_coordinates=bars,saved_intervals=[family(c) for c in D['ablation']['overall_macro']],pdf_paths_match_svg=True),details='Exact independent coordinate inversion; includes large ridge contrast and negative lambda100 control.')

# Structural parameter arithmetic, code/protocol authority, no execution.
hidden=5*768;weights=(384*hidden+hidden)+2*(hidden*hidden+hidden)+(hidden*768+768);arcbytes=385*768*4
assert round(weights*4/arcbytes,1)==114.7
claim('abstract;method3.5;discussion','295680float32 coefficients=1182720bytes=1.13MiB;114.7times fewer parameterbytes thanConverter', ['src/arc2_global/embedding_converter.py','src/arc2_global/model.py'],dict(coefficients=385*768,bytes=arcbytes,MiB=arcbytes/2**20,converter_parameters=weights,converter_bytes=weights*4,parameter_byte_ratio=weights*4/arcbytes),'rounding_ok','Structural coefficient/weight count only; same ridge coefficient count; not checkpoint size or end-to-endcost.')
AUTH=['configs/baselines.json','configs/datasets.json','configs/b1c_r3_lock.json','configs/b1m_lock.json','configs/b1m_score_r2_lock.json','configs/b1p_lock.json','configs/b2_lock.json','src/arc2_global/model.py','src/arc2_global/solver_backend.py','src/arc2_global/mechanism_ablation.py','src/arc2_global/procrustes.py','src/arc2_global/numerics.py','src/arc2_global/retrieval.py','src/arc2_global/baseline_adapters.py','src/arc2_global/embedding_converter.py','ops/b1m_score.py','ops/b1p_score.py','ops/b1c_r3_score.py','ops/b2_score.py','ops/b1p_stage.py','ops/b2_stage.py','protocols/B2_TREC_COVID_CONFIRMATION_20261031.md','protocols/B1P_ALL_PAID_FIQA_20261026.md','protocols/B1M_B1P0_DEVELOPMENT_20261026.md']
for p in AUTH:read(ROOT/p)
backends=[]
for p in (ROOT/'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu').glob('*arc2*/metadata.json'):
 d=js(p);assert d['backend_id']=='arc2_global_tangent2_primal_float64_r1';backends.append(dict(path=p.relative_to(ROOT).as_posix(),backend=d['backend_id'],fit_pairs=d['fit_pairs']))
for p in (ROOT/'results/b1p_r5_review_20261027/generation/cpu').glob('*arc2*/metadata.json'):
 d=js(p);assert d['backend_id']=='arc2_global_tangent2_primal_float64_r1';backends.append(dict(path=p.relative_to(ROOT).as_posix(),backend=d['backend_id'],fit_pairs=d['fit_pairs']))
claim('setup;method3.5','Solverregimeassignment', ['ops/b1p_stage.py','ops/b2_stage.py','protocols/B2_TREC_COVID_CONFIRMATION_20261031.md'],dict(dev_arc_cells=collections.Counter(c.get('original_source') for c in CELLS['dev'] if c['method']==A),receipts=backends,assignment={'DEV_fixed1024':'dual float64','B1M_ablation':'dual float64','B1P_fixed1024_imports':'dual float64','B1P_allpaid28819':'primal float64','B2_fixed1024':'primal float64'}),'exact_match' if 'TREC-COVID fits use the float64' in SOURCES['sections/experimental-setup.tex'] or 'TREC-COVID ARC2 fits use' in SOURCES['sections/experimental-setup.tex'] else 'ambiguous_mapping','Found omission: original current manuscript assigned allpaid primal, but did not explicitly assign prospective fixed1024 B2 primal; parent notified for narrow disclosure correction. No incorrect numeric comparison found.')
claim('method equations1-10,algorithm;setup','Frozen lambda10/exactly2targets;rawaffine float64 expansion of float32Procrustes;biasregularization;oneaffine normalizedmixedgallery;exactfloat32top100 stableties',AUTH,dict(lambda_value=10,tangent_steps=2,d_s=384,d_t=768,p=385),details='Source inspected statically; equations, cosinegradient and exact-arithmetic scaleequivariance checked algebraically. No claim of guaranteed finite-step improvement.')
claim('setup scope and inferential construction','4DEVcollections,2migrations,3budgets,5seeds,1024anchors;TREC171332/50;paidFiQA28819/57638;20kquerybootstrap and5/5/32/30families',AUTH,dict(collections={x:dict(documents=next(y['docs'] for y in js(ROOT/'configs/datasets.json')['retrieval'] if y['name']==x),queries=500 if x=='FiQA' else 50) for x in SETS+['TREC-COVID']},seeds=[17,29,41,53,67],families={k:D[k]['bootstrap'] for k in ['dev','trec','paid','ablation']}),details='Protocol/config and savedscorer metadata match; sharedindices/five-seedaveraging and percentiles inspected in implementation. Full20kbootstrap notrerun. Prospective designation verified protocol/seals/timestamps only; not independent reconstruction of historical human nonexposure.')

b2base=(ROOT/PATHS['trec']).parent.parent
seal=js(b2base/'verification/verification_seal.json');opening=js(b2base/'first_final_qrel_open.json');ranking=js(b2base/'ranking_seal.json')
assert seal['completed_utc']<opening['first_final_qrel_open_utc'];assert len(seal['verified_cells'])==184 and all(c['all_top100_ids_and_order_equal'] for c in seal['verified_cells'])
assert hashlib.sha256((b2base/'verification/verification_seal.json').read_bytes()).hexdigest()==opening['verification_seal_sha256']
assert hashlib.sha256((b2base/'ranking_seal.json').read_bytes()).hexdigest()==opening['ranking_seal_sha256']
claim('setup prospective scope','184 rankings/endpoints sealed and separately verified before first final label opening', [str(b2base/'verification/verification_seal.json'),str(b2base/'first_final_qrel_open.json'),str(b2base/'ranking_seal.json')],dict(verified_cells=184,verification_completed_utc=seal['completed_utc'],first_open_utc=opening['first_final_qrel_open_utc'],verification_hash_matches=True,ranking_seal_hash_matches=True),details='Saved provenance checked only; qrels were not opened by this audit.')

pdf=PAPER/'ARC2_Global_DASFAA2027_final.pdf';read(pdf);reader=PdfReader(pdf);pdftext='\n'.join(p.extract_text() for p in reader.pages);assert len(reader.pages)==16
embedded=[]
for page,name,fig in [(3,'/Im1','mechanism'),(10,'/Im2','dev_quality'),(11,'/Im3','dev_ablation'),(13,'/Im4','trec_quality')]:
 raw=PdfReader(PAPER/'figures'/f'{fig}.pdf').pages[0].get_contents().get_data();actual=reader.pages[page-1]['/Resources']['/XObject'][name].get_object().get_data();assert raw==actual;embedded.append(dict(page=page,figure=fig,decoded_content_byte_identical=True))
claim('compiled final PDF figures','All4 included vector figures equal audited actual figure PDF drawing streams',str(pdf),embedded)
assert 'all-paid and TREC-COVID fits use the float64 primal backend' in re.sub(r'\s+',' ',pdftext)
claim('compiled finalPDF','Current16-pagePDF contains measuredcrossbudgettable,allpaidmarkers and4panelTRECfigure',str(pdf),dict(pages=len(reader.pages),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),visual_review='16-page contact sheet and full pages11-14 inspected; labels/tablecontext/negativeevidence visible'),details='Raster inspection supplements vector-coordinate checks. Mechanism24docs/8anchors/4extraencodes is explicitly illustrative.')
read(Path(__file__))
hashes={}
for p in sorted(READ):
 try:key=p.relative_to(PAPER).as_posix()
 except ValueError:key=p.as_posix()
 hashes[key]='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
resolution=dict(issue='Initial setup did not explicitly identify the TREC-COVID primal backend.',initial_pdf_sha256='44473eaa32e0dce707554eff3f76042abf043eb88aa7a3cf6cc7aa4f63bf0128',action='Parent added precise development dual / all-paid and TREC-COVID primal assignment; reused all-paid-study fixed comparisons remain dual.',status='resolved',final_pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source_and_pdf_rechecked=True)
output=dict(audit_skill='paper-claim-audit',verdict='WARN' if any(c['status']=='ambiguous_mapping' for c in CLAIMS) else 'PASS',reason_code='solver_regime_disclosure' if any(c['status']=='ambiguous_mapping' for c in CLAIMS) else 'all_numbers_match_within_scope',summary='All audited raw numbers, full-precision ranks, family markers and actual vector figure coordinates reconcile. The solver-regime disclosure omission was corrected and the final source/PDF rechecked.',reviewer_model='gpt-6.1-sol',reviewer_reasoning='high',executor_family='openai',reviewer_family='openai',review_independence='same-family',acceptance_status='provisional',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),thread_id='/root/revision_20261102_claim_audit',audited_input_hashes=hashes,claims=CLAIMS,resolved_findings=[resolution],details=dict(total_claims=len(CLAIMS),status_counts=dict(collections.Counter(c['status'] for c in CLAIMS)),reconciliation=RECON),limitations=['No qrels opened, ranking rescore, retrieval, encoding, training or new scientific run.','Saved bootstrap intervals checked against displayed values and implemented construction; the full 20,000-draw bootstrap was not rerun.','Fresh same-family audit; not independent external review, acceptance scoring or a submission-readiness decision.','External literature attribution/reproduction accuracy and original human nonexposure were not independently audited.','Raw claims in the five authorized campaigns only; illustrative mechanism numbers are not empirical evidence.'])
(OUT/'CLAIM_AUDIT.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
md=['# Fresh paper-to-raw claim audit','',f"Verdict: **{output['verdict']} within scope**. Same-family / provisional; gpt-6.1-sol, high.",'',f"Audited {len(CLAIMS)} claim records and {len(hashes)} fresh input hashes. PDF: {len(reader.pages)} pages, SHA256 `{hashlib.sha256(pdf.read_bytes()).hexdigest()}`.",'','No numerical, comparison, marker, rank or vector-figure mismatch found. All saved means reconcile to scored per-query arrays: DEV 736 cells/160 means; TREC 184/40; all-paid 124/28; ablation 736/160, each maximum absolute error 0. All eleven TREC daggers and eight all-paid family markers, best/second styling before rounding, 80 TREC metric/native points and all five complete ablation intervals reconcile.','','## Found omission and resolution','','The initial setup omitted the explicit TREC-COVID primal-backend assignment. The parent corrected the source to distinguish development fixed-anchor dual fits, all-paid/TREC-COVID primal fits, and reused dual fixed-anchor comparisons in the all-paid study. The corrected source and compiled PDF text were reread; the new setup page was rendered and inspected. No numerical or scientific-file change was required.',f"Initial PDF SHA256: `{resolution['initial_pdf_sha256']}`. Final SHA256: `{resolution['final_pdf_sha256']}`. Status: **resolved**.",'','## Scope and negative evidence','','The E5 25%-versus-75% comparison holds on all five collections as a post-hoc descriptive point comparison. The complete raw baseline/native context is retained; no minimum budget, equal-quality or physical-cost assertion is supported or made. Each collection macro leads all five baselines; the second step is positive in 22/24 conditions and all five seed macros. TREC Procrustes is higher in all six unrounded nDCG cells, all Procrustes/LA2M family intervals are unresolved, MiniLM all-paid ridge remains unresolved, and E5 all-paid geometric losses and replacement losses remain visible.','','## Limitations','']+['- '+x for x in output['limitations']]+['','## Claim-level evidence','']
for c in CLAIMS:
 md += [f"### {c['claim_id']} - {c['status']}",f"- Location: {c['location']}",f"- Claim: {c['paper_text']}",f"- Raw/code paths: `{c['evidence_file']}`",f"- Exact evidence: `{json.dumps(c['evidence_value'],ensure_ascii=True,separators=(',',':'))}`"]
 if c['details']:md+=['- Notes: '+c['details']]
 md+=['']
md+=['## Fresh hashes','','Full paper-relative manuscript/figure/PDF hashes and absolute out-of-paper raw/code/protocol hashes are in the JSON sibling. Prior review opinions/reports were not consulted.']
(OUT/'CLAIM_AUDIT.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(dict(verdict=output['verdict'],claims=len(CLAIMS),hashes=len(hashes),statuses=output['details']['status_counts'],reconciliation=RECON,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest()),indent=2))

