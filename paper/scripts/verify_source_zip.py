"""Compile the manuscript ZIP in isolation and compare it with the built PDF."""
from pathlib import Path
from datetime import datetime, timezone
from zipfile import ZipFile
import hashlib
import json
import subprocess
from pypdf import PdfReader

PAPER=Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    now=datetime.now(timezone.utc)
    work=PAPER/'build'/('zip_smoke_'+now.strftime('%Y%m%dT%H%M%S%f'))
    work.mkdir(parents=True)
    archive=PAPER/'ARC2_Global_DASFAA2027_source.zip'
    with ZipFile(archive) as zipped:
        for member in zipped.namelist():
            assert not Path(member).is_absolute() and '..' not in Path(member).parts
        zipped.extractall(work)
    commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],
              ['bibtex','main'],
              ['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],
              ['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex']]
    for index,argv in enumerate(commands):
        result=subprocess.run(argv,cwd=work,capture_output=True,text=True,encoding='utf8',errors='replace')
        (work/f'pass{index}.txt').write_text(result.stdout+result.stderr,encoding='utf8')
        assert result.returncode==0,result.stdout[-2000:]
    build=json.loads((PAPER/'review/build_receipt.json').read_text(encoding='utf8'))
    pdf=PAPER/build['output']
    reference,isolated=PdfReader(pdf),PdfReader(work/'main.pdf')
    assert len(reference.pages)==len(isolated.pages)<=16
    assert '\n'.join(p.extract_text() for p in reference.pages)=='\n'.join(p.extract_text() for p in isolated.pages)
    log=(work/'main.log').read_text(encoding='utf8',errors='replace')
    assert 'Overfull \\hbox' not in log and 'There were undefined references' not in log
    result={'status':'PASS','checked_at_utc':now.isoformat(),'pages':len(reference.pages),
            'isolated_source_zip_build':True,'text_identical_to_current_draft':True,
            'network_or_research_data_required':False,'compiled_entrypoint':'main.tex',
            'archive_sha256':sha(archive),'pdf_sha256':sha(pdf),
            'build_directory':work.relative_to(PAPER).as_posix()}
    (PAPER/'review/SOURCE_ZIP_SMOKE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
