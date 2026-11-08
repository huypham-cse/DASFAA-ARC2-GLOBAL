"""Finalize a checked anonymous copy and build portable delivery archives."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
ART=Path('D:/ARC2-Global_Anonymous_Artifact_20261102')
BEFORE=ROOT/'paper/review/revision_tc1l_gcpa_20261102/before'
QA=ROOT/'provenance/qa/anonymous_review_20261102'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf8')
def run(argv,cwd):
    r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,encoding='utf8',errors='replace')
    if r.returncode:raise RuntimeError(r.stdout[-3500:]+r.stderr[-3500:])
    return r.stdout
def archive(folder,out):
    if out.exists():raise ValueError('Refuse overwrite: '+str(out))
    files={p.relative_to(folder).as_posix():sha(p) for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name in sorted(files):z.write(folder/name,name)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(files)
        for name,h in files.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
    out.with_suffix(out.suffix+'.sha256').write_text(sha(out)+'  '+out.name+'\n',encoding='ascii')
    return {'file':str(out),'bytes':out.stat().st_size,'sha256':sha(out),'members':len(files),'all_members_verified':True}
def main():
    audit=json.loads((ROOT/'paper/PAPER_CLAIM_AUDIT.json').read_text(encoding='utf8'))
    if audit['verdict']!='PASS':raise ValueError('Fresh claim audit not PASS')
    for name,expected in audit['audited_input_hashes'].items():
        p=Path(name) if Path(name).is_absolute() else ROOT/'paper'/name
        assert sha(p)==expected.removeprefix('sha256:'),name
    pdf=ROOT/'paper/ARC2_Global_DASFAA2027_supervisor_20261102.pdf'
    # Original PDF already has a byte-identical before snapshot; preserve source ZIP too.
    source=ROOT/'paper/ARC2_Global_DASFAA2027_source.zip'
    if source.exists() and not (BEFORE/source.name).exists():shutil.copyfile(source,BEFORE/source.name)
    shutil.copyfile(pdf,ROOT/'paper/ARC2_Global_DASFAA2027_final.pdf')
    shutil.copyfile(pdf,ART/'paper/paper.pdf')
    manifest=ART/'MANIFEST.json';data=json.loads(manifest.read_text())
    data['files']={p.relative_to(ART).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(ART.rglob('*')) if p.is_file() and p!=manifest and '__pycache__' not in p.parts}
    write(manifest,data)
    verified=run([sys.executable,'-X','utf8','verify.py'],ART)
    (QA/'verification.json').write_text(verified,encoding='utf8')
    run([sys.executable,'-X','utf8','paper/scripts/package_source.py'],ROOT)
    run([sys.executable,'-X','utf8','paper/scripts/verify_source_zip.py'],ROOT)
    over=Path('D:/ARC2-Global_Overleaf_20261102_r2.zip')
    if over.exists():raise ValueError('Refuse overwrite: '+str(over))
    shutil.copyfile(source,over);over.with_suffix('.zip.sha256').write_text(sha(over)+'  '+over.name+'\n',encoding='ascii')
    record={'utc':datetime.now(timezone.utc).isoformat(),'anonymous_artifact':archive(ART,Path('D:/ARC2-Global_Anonymous_Artifact_20261102.zip')),'overleaf':{'file':str(over),'bytes':over.stat().st_size,'sha256':sha(over),'isolated_build_verified':True},'pdf':{'file':str(pdf),'sha256':sha(pdf)},'no_external_send_or_upload':True,'old_packages_preserved':True}
    write(QA/'archives.json',record);print(json.dumps(record,indent=2))
if __name__=='__main__':main()
