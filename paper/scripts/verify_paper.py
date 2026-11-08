"""Deterministic final-draft QA, with hash-scoped semantic review status."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def claim_audit_status():
    reports = ROOT/'review'/'final_review_20261101'
    history = []
    candidates=[reports/name for name in ('RAW_AUDIT.json', 'RAW_AUDIT_R2.json', 'FINAL_POLISHED_AUDIT.json')]
    candidates.append(ROOT/'PAPER_CLAIM_AUDIT.json')
    for path in candidates:
        if not path.is_file():
            continue
        report = json.loads(path.read_text(encoding='utf-8'))
        hashes = report.get('audited_input_hashes', {})
        checked, changed = [], []
        for relative, expected in hashes.items():
            if relative.startswith(('sections/', 'generated/', 'figures/')) or relative in ('main.tex', 'references.bib'):
                target = ROOT/relative
                checked.append(relative)
                if not target.is_file() or sha(target) != expected.removeprefix('sha256:'):
                    changed.append(relative)
        history.append({'report':path.relative_to(ROOT).as_posix(),
                        'verdict':report.get('verdict'),
                        'review_independence':report.get('review_independence'),
                        'acceptance_status':report.get('acceptance_status'),
                        'manuscript_inputs_checked':len(checked),
                        'changed_manuscript_inputs':changed,
                        'matches_current_manuscript':bool(checked) and not changed})
    current = [item for item in history if item['matches_current_manuscript']]
    return {'current_snapshot':current[-1] if current else 'PENDING: no hash-matching fresh report',
            'history':history}

def main():
    build=json.loads((ROOT/'review'/'build_receipt.json').read_text())
    pdf=ROOT/build['output']
    reader=PdfReader(pdf)
    text='\n'.join(p.extract_text() or '' for p in reader.pages)
    log=(ROOT/'build'/'main.log').read_text(encoding='utf-8',errors='replace')
    abstract=(ROOT/'sections'/'abstract.tex').read_text().split('\\keywords')[0]
    abstract=re.sub(r'\\begin\{abstract\}','',abstract)
    word_count=len(abstract.split())
    assert word_count<=200,word_count
    assert len(reader.pages)<=16,len(reader.pages)
    assert 'Overfull \\hbox' not in log
    assert not re.search(r'(Citation|Reference) .*undefined|There were undefined references',log)
    alltex='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'sections').glob('*.tex'))
    bib=(ROOT/'references.bib').read_text(encoding='utf-8')
    used={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',alltex) for k in group.split(',')}
    keys=set(re.findall(r'@\w+\{([^,]+),',bib))
    assert used<=keys,used-keys
    bad=re.findall(r'Gia Huy|bachdylan|103\.73\.232|[CD]:\\|/root/|ARC2-server-backup',text,re.I)
    assert not bad,bad
    assert 'Anonymous' in str(reader.metadata.author)
    assert (ROOT/'generated'/'trec_means.tex').read_text().count(r'^{\dagger}')==11
    data=json.loads((ROOT/'generated'/'numeric_claims.json').read_text())
    converted=[c['ndcg10']['delta'] for c in data['prospective'] if c['pair']=='e5_small_base' and c['right']=='embedding_converter_paper_spec']
    assert f'{min(converted):.4f}'=='0.2000' and f'{max(converted):.4f}'=='0.2572'
    affine=(384+1)*768
    hidden=5*768
    widths=(384,hidden,hidden,hidden,768)
    converter=sum((a+1)*b for a,b in zip(widths[:-1],widths[1:]))
    assert converter==33927168 and affine==295680
    assert f'{converter/affine:.1f}'=='114.7'
    assert f'{affine*4/2**20:.2f}'=='1.13'
    scientific=subprocess.run(['git','diff','--name-only','--','src','ops','configs','protocols','results','manuscript'],cwd=PROJECT,capture_output=True,text=True,check=True).stdout.strip()
    assert not scientific,scientific
    figure_source=(ROOT/'figures'/'mechanism.tex').read_text()
    assert 'Centered Procrustes' in figure_source and 'Two tangent corrections' in figure_source
    assert 'Local residual' not in figure_source
    assert 'Illustrative corpus' in figure_source
    paths=[ROOT/'main.tex',ROOT/'references.bib']+list((ROOT/'sections').glob('*.tex'))+list((ROOT/'generated').glob('*.tex'))+list((ROOT/'figures').glob('*.pdf'))+[ROOT/'figures'/'mechanism.tex']
    out={'checked_at_utc':datetime.now(timezone.utc).isoformat(),
         'verification_kind':'deterministic parent QA, not independent semantic review',
         'status':'PASS','pdf':pdf.name,'pages':len(reader.pages),'abstract_words':word_count,
         'citations':len(used),'bibliography_entries':len(keys),'unresolved_citations_or_references':0,
         'overfull_hboxes':0,'known_identity_strings_in_pdf':bad,'anonymous_pdf_author':str(reader.metadata.author),
         'trec_positive_markers':11,'displayed_E5_Converter_delta_range':[min(converted),max(converted)],
         'coefficient_count':affine,'converter_parameter_count':converter,
         'parameter_ratio':converter/affine,'coefficient_MiB':affine*4/2**20,
         'scientific_tracked_changes':[],
         'paper_input_hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)},
         'pdf_sha256':sha(pdf),'fresh_final_claim_audit':claim_audit_status()}
    (ROOT/'review'/'FINAL_QA.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='paper_input_hashes'},indent=2))

if __name__=='__main__':main()
