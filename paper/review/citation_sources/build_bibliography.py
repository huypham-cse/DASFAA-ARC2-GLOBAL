"""Build compact bibliography from saved primary responses (metadata retained)."""
from pathlib import Path
import datetime, hashlib, html, json, re
import requests

P=Path(__file__).resolve().parent
def save_get(name,url):
 r=requests.get(url,timeout=40); (P/name).write_bytes(r.content)
 return {'url':url,'status':r.status_code,'file':name,'sha256':hashlib.sha256(r.content).hexdigest()}
extra=[]
extra.append(save_get('la2m_institutional_page.txt','https://www.research.ed.ac.uk/en/publications/integrating-vector-databases-across-embedding-models/'))
extra.append(save_get('la2m_author_pdf_attempt.txt','https://www.research.ed.ac.uk/files/572061340/main.pdf'))
extra.append(save_get('beir_correct_bib.txt','https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/106-/bibtex'))
extra.append(save_get('simplelinear_source_verified.txt','https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/mapper/simple_linear/strategy.py'))
(P/'extra_receipt.json').write_text(json.dumps(extra,indent=2),encoding='utf8')

def fields(text):
 # Publisher exports use one whole entry. Parse balanced braced/quoted values.
 text=text.strip(); head=re.match(r'@(\w+)\s*\{([^,]+),',text,re.S)
 if not head: raise ValueError(text[:60])
 result={}; i=head.end()
 while i<len(text):
  m=re.match(r'\s*,?\s*([\w-]+)\s*=\s*',text[i:])
  if not m:break
  name=m.group(1).lower(); i+=m.end(); start=i
  if text[i]=='{':
   depth=1;i+=1
   while depth:
    if text[i]=='{' and text[i-1]!='\\':depth+=1
    elif text[i]=='}' and text[i-1]!='\\':depth-=1
    i+=1
  elif text[i]=='"':
   i+=1
   while text[i]!='"' or text[i-1]=='\\':i+=1
   i+=1
  else:
   while i<len(text) and text[i] not in ',}':i+=1
  result[name]=text[start:i].strip()
 return head.group(1).lower(),result

def compact(key,path,source_url,kind='publisher-export'):
 s=(P/path).read_text(encoding='utf8')
 if key=='shen2020backward':
  s=html.unescape(re.search(r'(@InProceedings\{.*?)</div>',s,re.S).group(1))
  s=re.sub('<[^>]*>','',s)
 entry,fs=fields(s)
 wanted=['author','title','journal','booktitle','volume','number','pages','year','eprint','archiveprefix','primaryclass','doi','url']
 # Retain source metadata; strip unused abstracts/editors and use stable aliases.
 lines=['@'+entry+'{'+key+',']
 for k in wanted:
  if k not in fs:continue
  # LNCS prints DOI links itself. Keep publisher exports unchanged on disk,
  # but avoid duplicate links and long PDF-download URLs in the paper.
  if k=='url' and ('doi' in fs or key in ('beir2021','minilm2020')):continue
  v=' '.join(fs[k].split()).replace('–','--')
  v=v.replace('ö',r'{\"o}').replace('Ö',r'{\"O}').replace('é',r"{\'e}").replace('ò',r'{\`o}')
  lines.append('  '+k+' = '+v+',')
 lines.append('}')
 record={'key':key,'source_file':'citation_sources/'+path,'metadata_url':source_url,'verification':kind,'sha256':hashlib.sha256((P/path).read_bytes()).hexdigest(),'metadata_type':entry,'status':'verified'}
 return '\n'.join(lines),record

specs=[
 ('driftadapter','vejendla2025drift_metadata.txt','https://aclanthology.org/2025.emnlp-main.805.bib'),
 ('embeddingconverter','yoon2025converter_metadata.txt','https://aclanthology.org/2025.acl-long.1237.bib'),
 ('la2m','la2m_doi_bib.txt','https://doi.org/10.1145/3769803'),
 ('yang2026translation','yang2026translation_verified.bib','https://proceedings.mlr.press/v306/yang26e.html'),
 ('jha2025geometry','jha2025geometry_conference_bib.txt','https://proceedings.neurips.cc/paper_files/paper/28820-/bibtex'),
 ('dar2025mini','dar2025mini_metadata.txt','https://arxiv.org/bibtex/2510.02348'),
 ('maystre2025procrustes','maystre2025procrustes_metadata.txt','https://arxiv.org/bibtex/2510.13406'),
 ('schonemann1966procrustes','schonemann1966procrustes_metadata.txt','https://doi.org/10.1007/BF02289451'),
 ('shen2020backward','shen2020backward_metadata.txt','https://openaccess.thecvf.com/content_CVPR_2020/html/Shen_Towards_Backward-Compatible_Representation_Learning_CVPR_2020_paper.html'),
 ('fastfill2023','fastfill_verified.bib','https://raw.githubusercontent.com/apple/ml-fct/main/README.md'),
 ('spherical2026','spherical_bib.txt','https://arxiv.org/bibtex/2609.39836'),
 ('beir2021','beir_correct_bib.txt','https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/106-/bibtex'),
 ('sbert2019','reimers2019sentencebert_metadata.txt','https://aclanthology.org/D19-1410.bib'),
 ('minilm2020','wang2020minilm_metadata.txt','https://proceedings.neurips.cc/paper_files/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Bibtex.bib'),
 ('e52022','wang2022e5_metadata.txt','https://arxiv.org/bibtex/2212.03533'),
 ('treccovid2020','treccovid_doi_bib.txt','https://doi.org/10.1145/3451964.3451965'),
]
entries=[]; records=[]
for args in specs:
 e,r=compact(*args);entries.append(e);records.append(r)
entries.append('''@misc{nanobeir,
  author = {{Zeta Alpha}},
  title = {{NanoBEIR}},
  year = {2024},
  howpublished = {Hugging Face dataset collection},
  url = {https://huggingface.co/collections/zeta-alpha-ai/nanobeir},
  note = {Accessed 1 November 2026},
}''')
records.append({'key':'nanobeir','status':'verified-resource','metadata_url':'https://huggingface.co/collections/zeta-alpha-ai/nanobeir','source_file':'citation_sources/nanobeir_collection.txt','verification':'Resource entry synthesized from provider collection and dataset API; no formal paper/DOI invented; 2024 dataset creation is verified by API createdAt.'})
entries.append('''@misc{simplelinear,
  author = {{DBgroup Edinburgh}},
  title = {Embedding Translation: Reference Implementation},
  year = {2026},
  howpublished = {Software repository},
  url = {https://github.com/DBgroup-Edinburgh/embedding-translation},
  note = {Revision 5e62baf15442; SimpleLinear implementation},
}''')
records.append({'key':'simplelinear','status':'verified-software','metadata_url':'https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/mapper/simple_linear/strategy.py','source_file':'citation_sources/simplelinear_source_verified.txt','verification':'Software entry synthesized from official pinned repository; not a separate published algorithm paper. Exact classes and semantics checked.'})
(P.parent.parent/'references.bib').write_text('% Primary-source verified bibliography. Raw exports and receipts: review/citation_sources/.\n\n'+'\n\n'.join(entries)+'\n',encoding='utf8')
out={'schema':'arc2_literature_sources_v1','verified_on':'2026-11-01','scope':'Literature/citation verification only; no empirical results generated or labels accessed.','references':records,'rejected_or_superseded_metadata':[{'file':'citation_sources/thakur2021beir_metadata.txt','reason':'2021 hash collides across conference rounds; generic Bibtex.bib points to Q-Pain. Replaced with round2-linked /paper_files/paper/106-/bibtex and title/author-checked.'},{'file':'citation_sources/yang2026translation_metadata.txt','reason':'Guessed PMLR .bib endpoint returned404; replaced with actual page BibTeX export.'},{'file':'citation_sources/jha2025geometry_metadata.txt','reason':'Latest arXiv export gives2026; use verified NeurIPS2025 proceedings export for conference version.'}], 'access_limits':['ACM publisher page/PDF and Edinburgh author manuscript returned403; LA2M metadata verified via DOI and Crossref; abstract verified via institutional repository and mechanisms via pinned authors code. Do not claim to have read this inaccessible PDF.','No Zotero/Obsidian source requested/configured; no local papers/ or literature/ PDF library found.','This synthesis is not the fresh independent novelty reviewer requested later by the user.']}
(P.parent/'literature_sources.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print('Wrote',len(records),'verified entries:',','.join(r['key'] for r in records))
