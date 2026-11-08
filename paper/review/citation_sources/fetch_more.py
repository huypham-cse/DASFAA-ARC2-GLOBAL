from pathlib import Path
import concurrent.futures, datetime, hashlib, html, json, re
import requests
ROOT=Path(__file__).resolve().parent
JOBS={
 'yang2026translation_page':'https://proceedings.mlr.press/v306/yang26e.html',
 'jha2025geometry_conference_bib':'https://proceedings.neurips.cc/paper_files/paper/28820-/bibtex',
 'thakur2021beir_round2_page':'https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html',
 'la2m_doi_bib':'https://doi.org/10.1145/3769803',
 'la2m_crossref':'https://api.crossref.org/works/10.1145/3769803',
 'la2m_publisher':'https://dl.acm.org/doi/10.1145/3769803',
 'la2m_pdf':'https://dl.acm.org/doi/pdf/10.1145/3769803',
 'treccovid_doi_bib':'https://doi.org/10.1145/3451964.3451965',
 'nanobeir_card':'https://huggingface.co/datasets/zeta-alpha-ai/NanoFiQA2018/raw/main/README.md',
 'nanobeir_api':'https://huggingface.co/api/datasets/zeta-alpha-ai/NanoFiQA2018',
 'nanobeir_collection':'https://huggingface.co/collections/zeta-alpha-ai/nanobeir',
 'minilm_card':'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/raw/main/README.md',
 'e5_card':'https://huggingface.co/intfloat/e5-small-v2/raw/main/README.md',
 'official_code_readme':'https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/README.md',
 'official_code_la2m':'https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/reproduce-scripts/la2m/exp_la2m.py',
 'official_code_tree':'https://api.github.com/repos/DBgroup-Edinburgh/embedding-translation/git/trees/5e62baf1544264847ce3d8feeabd1ded6499b064?recursive=1',
 'arxiv_recent_search':'https://export.arxiv.org/api/query?search_query=all%3A%22embedding%20translation%22%20AND%20submittedDate%3A%5B202605010000%20TO%202611012359%5D&max_results=30&sortBy=submittedDate&sortOrder=descending',
}
def fetch(item):
 key,url=item
 headers={'User-Agent':'ARC2-literature-verification/1.0'}
 if key.endswith('doi_bib'): headers['Accept']='application/x-bibtex'
 try:
  r=requests.get(url,headers=headers,timeout=50)
  suffix='.pdf' if r.content.startswith(b'%PDF') else '.txt'
  path=ROOT/(key+suffix);path.write_bytes(r.content)
  return {'id':key,'url':url,'final_url':r.url,'status':r.status_code,'path':path.name,'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content)}
 except Exception as e:return {'id':key,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as p: records=list(p.map(fetch,JOBS.items()))
(ROOT/'fetch_more_receipt.json').write_text(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':records},indent=2),encoding='utf8')
for r in records:print(r['id'],r.get('status'),r.get('bytes'),r.get('error'))
for key in ('yang2026translation_page','thakur2021beir_round2_page'):
 s=(ROOT/(key+'.txt')).read_text(encoding='utf8')
 print(key,'links',re.findall(r'href=[\"\x27]([^\"\x27]*[Bb]ib[^\"\x27]*)',s))
 if key=='yang2026translation_page':
  m=re.search(r'(@InProceedings\{.*?)</code>',s,re.S)
  if m:(ROOT/'yang2026translation_verified.bib').write_text(html.unescape(re.sub('<[^>]*>','',m.group(1))),encoding='utf8')
