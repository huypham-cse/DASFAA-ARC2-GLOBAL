"""Fetch primary bibliography and reading evidence; no scientific data access."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, re
import requests

ROOT = Path(__file__).resolve().parent
SOURCES = {
 'vejendla2025drift': ('acl', 'https://aclanthology.org/2025.emnlp-main.805.bib', 'https://aclanthology.org/2025.emnlp-main.805.pdf'),
 'yoon2025converter': ('acl', 'https://aclanthology.org/2025.acl-long.1237.bib', 'https://aclanthology.org/2025.acl-long.1237.pdf'),
 'yang2026translation': ('pmlr', 'https://proceedings.mlr.press/v306/yang26e.bib', 'https://raw.githubusercontent.com/mlresearch/v306/main/assets/yang26e/yang26e.pdf'),
 'jha2025geometry': ('arxiv', 'https://arxiv.org/bibtex/2505.12540', 'https://arxiv.org/html/2505.12540v4'),
 'dar2025mini': ('arxiv', 'https://arxiv.org/bibtex/2510.02348', 'https://arxiv.org/html/2510.02348v2'),
 'maystre2025procrustes': ('arxiv', 'https://arxiv.org/bibtex/2510.13406', 'https://arxiv.org/html/2510.13406v1'),
 'byun2026mkp': ('arxiv', 'https://arxiv.org/bibtex/2609.16875', 'https://arxiv.org/html/2609.16875v1'),
 'gao2023vec2vec': ('arxiv', 'https://arxiv.org/bibtex/2306.12689', 'https://arxiv.org/abs/2306.12689'),
 'schonemann1966procrustes': ('doi', 'https://doi.org/10.1007/BF02289451', 'https://doi.org/10.1007/BF02289451'),
 'shen2020backward': ('cvf', 'https://openaccess.thecvf.com/content_CVPR_2020/html/Shen_Towards_Backward-Compatible_Representation_Learning_CVPR_2020_paper.html', None),
 'thakur2021beir': ('neurips', 'https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Bibtex.bib', 'https://arxiv.org/abs/2104.08663'),
 'reimers2019sentencebert': ('acl', 'https://aclanthology.org/D19-1410.bib', 'https://aclanthology.org/D19-1410/'),
 'wang2020minilm': ('neurips', 'https://proceedings.neurips.cc/paper_files/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Bibtex.bib', 'https://proceedings.neurips.cc/paper/2020/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html'),
 'wang2022e5': ('arxiv', 'https://arxiv.org/bibtex/2212.03533', 'https://arxiv.org/abs/2212.03533'),
}

def fetch_one(item):
    key, (kind, bib_url, read_url) = item
    record = {'key': key, 'kind': kind, 'bib_url': bib_url, 'reading_url': read_url, 'responses': []}
    for label, url in [('metadata', bib_url), ('reading', read_url)]:
        if not url: continue
        try:
            headers = {'User-Agent': 'ARC2-literature-verification/1.0'}
            if kind == 'doi' and label == 'metadata': headers['Accept'] = 'application/x-bibtex'
            response = requests.get(url, headers=headers, timeout=50)
            suffix = '.pdf' if response.content.startswith(b'%PDF') else '.txt'
            path = ROOT / (key + '_' + label + suffix)
            path.write_bytes(response.content)
            record['responses'].append({'role': label, 'url': url, 'final_url': response.url, 'status': response.status_code, 'path': path.name, 'sha256': hashlib.sha256(response.content).hexdigest(), 'bytes': len(response.content), 'content_type': response.headers.get('Content-Type')})
        except Exception as exc:
            record['responses'].append({'role': label, 'url': url, 'error': str(exc)})
    return record

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(fetch_one, SOURCES.items()))
    (ROOT / 'fetch_receipt.json').write_text(json.dumps({'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'sources': records}, indent=2), encoding='utf-8')
    for record in records:
        print(record['key'], [(r['role'], r.get('status'), r.get('bytes'), r.get('error')) for r in record['responses']])
