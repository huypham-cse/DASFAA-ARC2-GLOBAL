"""Build the anonymous LNCS draft without altering scientific evidence."""
from pathlib import Path
import argparse
import subprocess
import shutil
import json
import hashlib
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def run(argv, name, build_dir):
    p = subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (build_dir/f'{name}.txt').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
    if p.returncode:
        print((p.stdout+'\n'+p.stderr)[-6500:])
        raise SystemExit(f'{name} failed, exit {p.returncode}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--engine',default='pdflatex')
    ap.add_argument('--output',default='ARC2_Global_DASFAA2027_final.pdf')
    args=ap.parse_args()
    build_dir=ROOT/'build'/('latex_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
    build_dir.mkdir(parents=True)
    rel_build=build_dir.relative_to(ROOT).as_posix()
    opts=[args.engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+rel_build,'main.tex']
    run(opts,'latex_pass1',build_dir)
    run(['bibtex',rel_build+'/main'],'bibtex',build_dir)
    run(opts,'latex_pass2',build_dir)
    run(opts,'latex_pass3',build_dir)
    dest=ROOT/args.output
    try:
        shutil.copy2(build_dir/'main.pdf',dest)
    except PermissionError:
        dest=ROOT/(Path(args.output).stem+'_'+datetime.now(timezone.utc).strftime('%H%M%S')+'.pdf')
        shutil.copy2(build_dir/'main.pdf',dest)
    for suffix in ('log','bbl','blg'):
        shutil.copy2(build_dir/('main.'+suffix),ROOT/'build'/('main.'+suffix))
    from pypdf import PdfReader
    pdf=PdfReader(dest)
    receipt={'built_at_utc':datetime.now(timezone.utc).isoformat(), 'pages':len(pdf.pages),
             'page_limit':16,'within_page_limit':len(pdf.pages)<=16,
             'pdf_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(), 'output':dest.name,
             'engine':args.engine,'anonymous_authors':True,'build_directory':rel_build,
             'review_status':'draft; see review artifacts for actual review status'}
    (ROOT/'review'/'build_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))
    if not receipt['within_page_limit']:
        raise SystemExit('Page limit exceeded: edit prose/layout, do not compress LNCS margins/font.')

if __name__=='__main__':
    main()
