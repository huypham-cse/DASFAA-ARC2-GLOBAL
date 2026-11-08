"""Export a small anonymous manuscript-source ZIP, separate from research evidence."""
from pathlib import Path
import hashlib
import json
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]

def main():
    receipt=json.loads((ROOT/'review'/'build_receipt.json').read_text())
    pdf=ROOT/receipt['output']
    files=[ROOT/'main.tex',ROOT/'references.bib',ROOT/'llncs.cls',ROOT/'splncs04.bst',pdf]
    files+=sorted((ROOT/'sections').glob('*.tex'))
    files += [ROOT/'generated'/f for f in ['dev_macro.tex','trec_means.tex','allpaid.tex','budget_leverage.tex','trec_recall.tex']]
    files += [ROOT/'figures'/f for f in ['mechanism.pdf','mechanism.tex','dev_quality.pdf','dev_ablation.pdf','trec_quality.pdf']]
    out=ROOT/'ARC2_Global_DASFAA2027_source.zip'
    manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    readme=('Anonymous LNCS manuscript-source draft.\n'
            'Select main.tex as the main document on Overleaf.\n'
            'Local build: pdflatex main; bibtex main; pdflatex main; pdflatex main.\n'
            'Prebuilt vector figures are included. mechanism.tex is editable TikZ.\n'
            'The complete descriptive TREC Recall table is generated/trec_recall.tex; the main paper also plots all its values.\n'
            'This is the manuscript source, not the full research-reproduction artifact.\n'
            'Internal author paths, review logs, server records and raw research bundles are excluded.\n')
    with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,p.relative_to(ROOT).as_posix())
        z.writestr('README_SOURCE.txt',readme)
        z.writestr('SOURCE_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
    with ZipFile(out) as z:
        for name,expected in manifest.items():
            assert hashlib.sha256(z.read(name)).hexdigest()==expected
        assert not any(n.startswith(('review/','build/')) for n in z.namelist())
    record={'archive':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
            'files':len(files),'manifest_members_verified':True,'scope':'anonymous manuscript-source export; no research-evidence deletion'}
    (ROOT/'review'/'source_archive_receipt.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    out.with_suffix('.zip.sha256').write_text(record['sha256']+'  '+out.name+'\n',encoding='ascii')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
