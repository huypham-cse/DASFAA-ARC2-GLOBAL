from pathlib import Path
import concurrent.futures,hashlib,json,re
import requests
P=Path(__file__).resolve().parent
jobs={
 'fastfill_arxiv_bib':'https://arxiv.org/bibtex/2303.04766',
 'fastfill_author_page':'https://machinelearning.apple.com/research/fastfill',
 'fastfill_official_readme':'https://raw.githubusercontent.com/apple/ml-fct/main/README.md',
 'fastfill_openreview_api':'https://api.openreview.net/notes?id=rnRiiHw8Vy',
 'fastfill_openreview_api2':'https://api2.openreview.net/notes?id=rnRiiHw8Vy',
 'fastfill_primary_pdf':'https://openreview.net/pdf/8d20dc462785f41d1a42a73d5f251100169ec180.pdf',
}
def fetch(item):
 name,url=item
 try:
  r=requests.get(url,timeout=45);suffix='.pdf' if r.content.startswith(b'%PDF') else '.txt'
  f=P/(name+suffix);f.write_bytes(r.content)
  return {'file':f.name,'url':url,'status':r.status_code,'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content)}
 except Exception as e:return {'file':name,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: rows=list(ex.map(fetch,jobs.items()))
(P/'fastfill_receipt.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(rows)
for f in (P/'fastfill_author_page.txt',P/'fastfill_openreview_api.txt',P/'fastfill_openreview_api2.txt'):
 s=f.read_text(encoding='utf8');i=s.lower().find('bibtex');print(f.name,s[max(0,i-100):i+1200].encode('ascii','backslashreplace').decode())
