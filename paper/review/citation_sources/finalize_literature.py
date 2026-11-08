from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent
review=P.parent
data=json.loads((review/'literature_sources.json').read_text(encoding='utf8'))
bib=(review.parent/'references.bib').read_text(encoding='utf8')
entries=re.split(r'(?m)(?=^@\w+\{)',bib)[1:]
bykey={re.match(r'@\w+\{([^,]+),',x).group(1):x for x in entries}
for record in data['references']:
 s=bykey[record['key']]
 def get(name):
  m=re.search(r'(?m)^\s*'+name+r'\s*=\s*(.*),\s*$',s)
  return m.group(1) if m else None
 record['verified_export_fields']={k:get(k) for k in ['author','title','year','journal','booktitle','doi','url'] if get(k) is not None}
 if record['key']=='dar2025mini':
  record['reading_url']='https://arxiv.org/html/2510.02348v4'
  record['reading_file']='citation_sources/dar_latest_reading.txt'
  record['version_note']='Latest v4,17February2026, checked after initially readingv2. Matching-based ICP50--100iterations plus one clustering refinement; not tangent ridge updates.'
data['novelty_search']={
 'assessment':'Local provisional PROCEED WITH CAUTION; not the fresh independent reviewer verdict.',
 'claims':[
  {'id':'C1','claim':'Exact finite centered rectangular Procrustes plus two tangent ridge corrections','queries':['centered Procrustes tangent ridge embedding migration affine normalization','embedding translation tangent residual angular correction ridge Procrustes 2025 2026','cross model embedding alignment two step cosine tangent regression'],'raw_results':'citation_sources/claim_search_0.txt','finding':'No exact computation found among inspected sources; individual ingredients and iterative alignment are established.'},
  {'id':'C2','claim':'Mixed-gallery retrieval findings under paid-document encoding budget','queries':['partial re embedding mixed gallery document migration Procrustes 2025 2026','incremental embedding model migration mixed old new documents retrieval','embedding translation A2M LA2M generalizable composable multi model'],'raw_results':'citation_sources/claim_search_3.txt','finding':'Mixed databases and staged migration are established in LA2M/HMoE; FastFill and SLERP also study partial backfill and replacement harm, so only specific adapter/text evidence can be claimed.'},
  {'id':'C3','claim':'Compact global correction as alternative to learned neural translators','queries':['compact affine adapter document embedding migration anchor budget 2025 2026','embedding conversion Procrustes ridge neural adapter retrieval 2026','document side embedding alignment bounded residual corrections cosine'],'raw_results':'citation_sources/claim_search_6.txt','finding':'Compact adapters and document conversion are prior art; structural affine storage is not a measured end-to-end cost win.'},
 ],
 'freshness':'Web follow-ups included 2025--2026; arXiv API response saved for submittedDate20260501--20261101. September2026 MKP, indexmigration,scorecalibration,memoryportability and vectorlinking leads checked for scope.',
 'prohibited_overclaims':['first document-side converter','first mixed-gallery search','first frozen-backbone adapter','general superiority over HMoE','independent advantage over Procrustes/LA2M without supporting intervals','borrowing published systems gains for our method']
}
data['close_prior_review_addendum']={'origin':'Parent fresh reviewer surfaced these two papers; this agent independently fetched and checked their primary sources.','fastfill2023':{'metadata':'Authors official repository BibTeX plus Apple primary paper page; missing delimiter comma repaired, no field content changed.','primary_reading':'https://arxiv.org/html/2303.04766v1','reading_file':'citation_sources/fastfill_full_html.txt','receipt':'citation_sources/fastfill_receipt.json','finding':'Old-to-new feature alignment, partial backfill, fixed backfill budget, and initial replacement harm are already explicit. Distinguish the exact frozen two-tangent document adapter and text retrieval evidence.'},'spherical2026':{'metadata':'Fetched arXiv BibTeX2609.39836; author spelling from primary export.','primary_reading':'https://arxiv.org/html/2609.39836v1','reading_file':'citation_sources/spherical_full_html.txt','receipt':'citation_sources/close_prior_receipt.json','finding':'Query-side SLERP after Procrustes differs from document-side tangent ridge updates; appendixP.2 already studies mixed-gallery partial backfill and appendixN includes ridge alignment.'},'bibliography_scope':'MKP omitted from compact bibliography after adding these closer priors; primary MKP evidence remains in novelty record.'}
data['validation']={'reference_count':len(bykey),'related_work_word_count':len(re.findall(r'\b[\w-]+\b',re.sub(r'\\cite\{[^}]+\}','',(review.parent/'sections/related-work.tex').read_text(encoding='utf8')))),'missing_citation_keys':sorted({c for f in review.parent.rglob('*.tex') for x in re.findall(r'\\cite\w*\{([^}]+)\}',f.read_text(encoding='utf8')) for c in x.split(',')}-set(bykey))}
(review/'literature_sources.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
files=[]
for f in sorted(P.iterdir()):
 if f.is_file() and f.name!='source_manifest.json':files.append({'path':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(P/'source_manifest.json').write_text(json.dumps({'scope':'Literature evidence and scripts only; includes unsuccessful responses preserved with receipts.','files':files},indent=2),encoding='utf8')
print(data['validation'])
