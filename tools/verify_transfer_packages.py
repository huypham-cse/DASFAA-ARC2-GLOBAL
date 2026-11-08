"""Isolated source/package checks only: no model fit, ranking or new scoring."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'tmp/handoff_20261102'


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def emit(path,data):path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')


def main():
    global WORK
    receipt=json.loads((ROOT/'provenance/qa/handoff_packages_preliminary_20261102.json').read_text())
    WORK=Path(receipt['development']['partial_path']).parent
    sourcezip=Path(receipt['overleaf']['partial_path'])
    over=WORK/'overleaf_isolated_smoke';over.mkdir(exist_ok=False)
    with ZipFile(sourcezip) as archive:
        for name in archive.namelist():
            if Path(name).is_absolute() or '..' in Path(name).parts or ':' in name:raise ValueError('Escaping source member')
        archive.extractall(over)
        private=[]
        for name in archive.namelist():
            if Path(name).suffix in ['.tex','.bib','.txt','.json']:
                data=archive.read(name)
                if any(x in data for x in [b'Gia Huy',b'.ssh/',b'103.73.232.',b'C:\\Users\\',b'D:/DASFAA']):private.append(name)
        if private:raise ValueError('Private source marker in anonymous ZIP: '+str(private))
    commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],['bibtex','main'],
              ['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex']]
    for i,argv in enumerate(commands):
        proc=subprocess.run(argv,cwd=over,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (over/('build_pass'+str(i)+'.txt')).write_text(proc.stdout+proc.stderr,encoding='utf-8')
        if proc.returncode:raise RuntimeError('Isolated Overleaf build failed: '+proc.stdout[-2000:])
    reference=PdfReader(ROOT/'paper/ARC2_Global_DASFAA2027_final.pdf');rebuilt=PdfReader(over/'main.pdf')
    assert len(reference.pages)==len(rebuilt.pages)==16
    assert [p.extract_text() for p in reference.pages]==[p.extract_text() for p in rebuilt.pages]
    assert [p.mediabox for p in reference.pages]==[p.mediabox for p in rebuilt.pages]
    log=(over/'main.log').read_text(encoding='utf-8',errors='replace')
    assert 'Overfull \\hbox' not in log and 'There were undefined references' not in log
    assert not any('Gia Huy' in str(v) for v in rebuilt.metadata.values())
    # Compile the new table fragment independently, without inserting it in main.
    wrapper=(r'\documentclass{llncs}'+'\n'+r'\usepackage[T1]{fontenc}'+'\n'+r'\usepackage{booktabs,amsmath}'+'\n'+
             r'\begin{document}'+'\n'+r'\input{additional_material/tc1l_minilm_ablation}'+'\n'+r'\end{document}'+'\n')
    (over/'fragment_smoke.tex').write_text(wrapper,encoding='utf-8')
    proc=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','fragment_smoke.tex'],cwd=over,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (over/'fragment_build.txt').write_text(proc.stdout+proc.stderr,encoding='utf-8')
    if proc.returncode:raise RuntimeError('Supplement table does not compile: '+proc.stdout[-1600:])
    if 'Overfull \\hbox' in (over/'fragment_smoke.log').read_text(errors='replace'):raise ValueError('Supplement table overflows')
    print('OVERLEAF_AND_SUPPLEMENT_COMPILE_PASS',flush=True)
    dev=Path(receipt['development']['partial_path'])
    check=subprocess.run([sys.executable,str(ROOT/'handoff_20261102/verify_package.py'),str(dev)],capture_output=True,text=True,encoding='utf-8')
    if check.returncode:raise RuntimeError('Development archive check failed: '+check.stdout+check.stderr)
    hashes=json.loads(check.stdout)
    isolated=WORK/'development_isolated_smoke';isolated.mkdir(exist_ok=False)
    with ZipFile(dev) as archive:
        prefix=[n[:-len('PACKAGE_MANIFEST.json')] for n in archive.namelist() if n.endswith('/PACKAGE_MANIFEST.json')][0]
        manifest=json.loads(archive.read(prefix+'PACKAGE_MANIFEST.json'))
        needed=[name for name in manifest['files'] if name.startswith(('src/','ops/','tools/','protocols/','configs/','inputs/minilm_fiqa/','handoff/')) or name in ['pyproject.toml','THIRD_PARTY_NOTICES.md']]
        for name in needed:
            target=(isolated/name).resolve()
            if not target.is_relative_to(isolated.resolve()):raise ValueError('Escaping extraction')
            target.parent.mkdir(parents=True,exist_ok=True)
            with archive.open(prefix+name) as inp,target.open('xb') as out:
                for block in iter(lambda:inp.read(8*1024*1024),b''):out.write(block)
        # Original relative ID/selection files are small, needed by draft hash checks.
        for name in manifest['files']:
            if not name.startswith('results/fiqa_development/'):continue
            if name!='results/fiqa_development/ids.json' and '/selections/' not in name:continue
            target=isolated/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(archive.read(prefix+name))
        r3map=json.loads(archive.read(prefix+'handoff/R3_MAPPING.json'))
        r3manifest=json.loads(archive.read(prefix+'archive/r3/RELEASE_MANIFEST.json'))
        for original,spec in r3manifest['files'].items():
            delivered=manifest['files'][r3map[original]]
            if delivered['sha256']!=spec['sha256'] or delivered['bytes']!=spec['bytes']:raise ValueError('R3 evidence omitted or changed')
    before={p.relative_to(isolated).as_posix():sha(p) for p in (isolated/'configs').glob('*.json')}
    draft=subprocess.run([sys.executable,str(isolated/'handoff/prepare_local_draft.py')],cwd=isolated,capture_output=True,text=True,encoding='utf-8')
    (isolated/'draft_smoke.txt').write_text(draft.stdout+draft.stderr,encoding='utf-8')
    if draft.returncode:raise RuntimeError('Relocation draft helper failed: '+draft.stdout+draft.stderr)
    assert all(sha(isolated/p)==h for p,h in before.items()),'Original locks changed by draft helper'
    assert len(list((isolated/'configs').glob('tc1l_relocated_*_DRAFT.json')))==1
    print('DEVELOPMENT_BYTE_AND_RELOCATION_DRAFT_PASS',flush=True)
    result={'status':'PASS','overleaf':{'isolated_compile':True,'pages':16,'text_and_page_geometry_identical':True,
        'overfull_or_undefined_reference_errors':False,'table_fragment_compile':True,'private_text_markers':[]},
        'development':{'all_member_hashes':hashes,'all_R3_manifested_files_preserved':len(r3map),
        'isolated_relocation_draft_smoke':True,'original_locks_unchanged':True},
        'new_model_fits':0,'new_rankings':0,'new_scientific_scoring':0,
        'paper_sha256':sha(ROOT/'paper/ARC2_Global_DASFAA2027_final.pdf')}
    emit(ROOT/'provenance/qa/handoff_packages_verification_20261102.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
