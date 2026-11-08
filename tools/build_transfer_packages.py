"""Build two reviewable ZIPs, retain old scientific bytes, never delete sources."""
from datetime import datetime,timezone
import argparse
import hashlib
import io
import json
from pathlib import Path,PurePosixPath
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DAY='20261102'
DEV_ROOT='ARC2_Global_Development_'+DAY
DEV=Path('D:/ARC2-Global_Development_'+DAY+'.zip')
OVER=Path('D:/ARC2-Global_Overleaf_'+DAY+'.zip')
R3=Path('D:/DASFAA-2027-paper-release-20261101-r3-paper-story/DASFAA-2027-paper-release')
WORK=ROOT/('tmp/handoff_'+DAY)
ASSETS=ROOT/'handoff_20261102'


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def safe(name):
    if not name or '\\' in name or ':' in name or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts:
        raise ValueError('Unsafe archive path: '+name)
    return name


def write_json(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def supplement():
    summary=json.loads((ROOT/'results/tc1l_local_r1_20261102/full/scoring/summary.json').read_text())
    rows={r['method']:r for r in summary['means']}
    text=[r'\begin{table}[t]',r'\centering',r'\caption{Matched-initialization ablation on FiQA development, MiniLM to DistilRoBERTa, at 50\% anchor-inclusive exposure (1,024 fitted anchors; five seeds).}',
          r'\label{tab:tc1l-matched}',r'\begin{tabular}{lrr}',r'\toprule',r'Method & nDCG@10 & Recall@100 \\',r'\midrule']
    for name,label in [('procrustes','Procrustes initialization'),('euclidean2','Euclidean residual, two steps'),('chordal2','Norm-scaled chordal, two steps'),('tangent2','ARC2-Global, two tangent steps')]:
        a,b=f"{rows[name]['ndcg10']:.5f}",f"{rows[name]['recall100']:.5f}"
        if name=='tangent2':label=r'\textbf{'+label+'}';a=r'\textbf{'+a+'}';b=r'\textbf{'+b+'}'
        text.append(label+' & '+a+' & '+b+r' \\')
    text += [r'\bottomrule',r'\end{tabular}',r'\par\smallskip',r'\begin{tabular}{lr}',r'\toprule',r'ARC2 minus control & $\Delta$ nDCG@10 [98.75\% interval] \\',r'\midrule']
    for c in summary['primary_contrasts']:
        label='Norm-scaled chordal' if c['right']=='chordal2' else 'Euclidean residual'
        text.append(label+f" & {c['delta_ndcg10']:+.5f} [{c['lower']:+.5f}, {c['upper']:+.5f}]"+r' \\')
    text += [r'\bottomrule',r'\end{tabular}',r'\par\smallskip',r'\begin{minipage}{0.96\linewidth}\small',
             r'Intervals retain the original four-contrast family (two E5 contrasts pending). These are inspected development results; the initialization, anchors, regularization and two-update count are shared across controls.',
             r'\end{minipage}',r'\end{table}','']
    return '\n'.join(text).encode()


class Registry:
    def __init__(self):self.entries={};self.omitted=[]
    def add(self,name,source,origin):
        name=safe(name)
        if name in self.entries:raise ValueError('Duplicate package member '+name)
        if isinstance(source,bytes):h=hashlib.sha256(source).hexdigest();size=len(source)
        else:source=Path(source);h=sha(source);size=source.stat().st_size
        self.entries[name]={'source':source,'sha256':h,'bytes':size,'origin':origin}
    def content(self,name):
        source=self.entries[name]['source'];return source if isinstance(source,bytes) else source.read_bytes()
    def manifest(self):return {k:{s:v for s,v in spec.items() if s!='source'} for k,spec in sorted(self.entries.items())}


def credential_check(registry):
    findings=[]
    key=re.compile(rb'^-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----',re.M)
    assignment=re.compile(rb'''(?i)(?:password|passphrase|api[_-]?key|secret[_-]?key)\s*[:=]\s*['"]([^'"\r\n]{6,})['"]''')
    for name,row in registry.entries.items():
        lower=name.lower()
        if any(x in PurePosixPath(lower).parts for x in ['.ssh','.env']) or lower.endswith(('.key','.pem','.p12')):
            findings.append({'path':name,'kind':'credential_filename'});continue
        if Path(name).suffix.lower() not in ['.py','.md','.json','.txt','.yaml','.yml','.toml','.sh']:continue
        data=registry.content(name)
        if key.search(data):findings.append({'path':name,'kind':'private_key_payload'})
        if assignment.search(data):findings.append({'path':name,'kind':'review_literal_assignment'})
    if findings:
        write_json(WORK/'credential_review.json',findings)
        fatal=[r for r in findings if r['kind']!='review_literal_assignment']
        if fatal:raise ValueError('Credential payload/filename excluded only after explicit review; see receipt')
    return findings


def write_zip(registry,target,prefix,manifest_name):
    manifest=registry.manifest()
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True,strict_timestamps=False) as archive:
        for name,row in sorted(registry.entries.items()):
            source=row['source'];member=prefix+name
            if isinstance(source,bytes):archive.writestr(member,source)
            else:archive.write(source,member,compress_type=zipfile.ZIP_STORED if name.endswith('.bundle') else zipfile.ZIP_DEFLATED)
        archive.writestr(prefix+manifest_name,json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'files':manifest},indent=2,ensure_ascii=False)+'\n')
    with zipfile.ZipFile(target) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate ZIP members')
        for name,row in registry.entries.items():
            h=hashlib.sha256()
            with archive.open(prefix+name) as stream:
                for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
            if h.hexdigest()!=row['sha256']:raise ValueError('ZIP hash mismatch '+name)
    return {'file_count':len(manifest),'uncompressed_bytes':sum(r['bytes'] for r in manifest.values()),'bytes':target.stat().st_size,'sha256':sha(target),'all_members_hash_verified':True}


def build_overleaf():
    registry=Registry()
    old=ROOT/'paper/ARC2_Global_DASFAA2027_source.zip'
    with zipfile.ZipFile(old) as archive:
        previous=json.loads(archive.read('SOURCE_MANIFEST.json'))
        for name,h in previous.items():
            data=archive.read(name)
            if hashlib.sha256(data).hexdigest()!=h:raise ValueError('Original manuscript ZIP corrupted')
            if sha(ROOT/'paper'/name)!=h:raise ValueError('Manuscript source newer than export: '+name)
            registry.add(name,data,'Current frozen manuscript source, unchanged')
    registry.add('additional_material/tc1l_minilm_ablation.tex',supplement(),'Generated from sealed TC1L means/intervals')
    registry.add('additional_material/tc1l_minilm_effects.pdf',ROOT/'results/tc1l_local_r1_20261102/report/fig_tangent_controls.pdf','Current verified TC1L vector figure')
    readme=('Anonymous LNCS manuscript source. Select main.tex on Overleaf.\n'
            'Compiler: pdfLaTeX; bibliography: BibTeX.\n'
            'The main paper remains the current16-page draft; no new experiment is automatically included.\n'
            'additional_material/tc1l_minilm_ablation.tex and tc1l_minilm_effects.pdf are ready for integration.\n'
            'The supplement is a matched-initialization MiniLM FiQA development result; E5 controls pending.\n'
            'Add published GCPA positioning and arrange supervisor/anonymity/artifact review before submission.\n'
            'This ZIP contains no operational logs, raw research bundles, keys or private review reports.\n')
    registry.add('README_OVERLEAF.txt',readme.encode(),'New export instructions')
    registry.add('SOURCE_MANIFEST.json',(json.dumps({k:v['sha256'] for k,v in registry.entries.items()},indent=2)+'\n').encode(),'Derived anonymous source hashes')
    part=WORK/'overleaf.zip.partial'
    record=write_zip(registry,part,'','EXPORT_MANIFEST.json')
    return registry,part,record


def build_development(bundle):
    registry=Registry();tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    allowed={'src','ops','configs','protocols','licenses','refine-logs','tools','provenance','results','paper','figures','handoff_20261102'}
    for name in tracked:
        if not name:continue
        p=PurePosixPath(name);parts=p.parts;source=ROOT/name
        if not source.is_file():continue
        if parts[0] not in allowed and len(parts)!=1:continue
        omit=('__pycache__' in parts or (parts[0]=='paper' and ('build' in parts or 'render_paper' in parts or 'primary_sources' in parts))
              or (name.startswith('paper/review/') and source.suffix.lower() in ['.png','.jpg','.jpeg'])
              or (name.startswith('results/b1g_r1_review_20261027/') and len(parts)>2 and parts[2] in ['main','mini','smoke','transport'])
              or source.suffix.lower() in ['.zip','.bundle'] or name.endswith(('.tar','.tar.gz','.tar.zst'))
              or parts[0] in ['.aris','.git','manuscript'])
        if omit:
            registry.omitted.append({'path':name,'bytes':source.stat().st_size,'reason':'Regenerable build/render, redundant container, or large G replay source; original kept on disk/backups'});continue
        if name in ['README.md','AGENTS.md']:
            registry.add('archive/current_project/'+name,source,'Verbatim original project navigation/instructions');continue
        registry.add(name,source,'Current project snapshot '+SNAPSHOT)
    # Merge every manifested R3 byte, sharing identical entries and archiving
    # conflicting old versions. This retains historical/negative evidence.
    manifest=json.loads((R3/'RELEASE_MANIFEST.json').read_text());mapping={}
    science_dirs={'src','ops','configs','protocols','licenses','results','appendix','reproduce','tools','provenance'}
    for name,spec in manifest['files'].items():
        safe(name);source=R3/name
        if sha(source)!=spec['sha256'] or source.stat().st_size!=spec['bytes']:raise ValueError('R3 file differs '+name)
        if name in registry.entries and registry.entries[name]['sha256']==spec['sha256']:target=name
        else:
            target=name if PurePosixPath(name).parts[0] in science_dirs and name not in registry.entries else 'archive/r3/'+name
            if target not in registry.entries:registry.add(target,source,'Original R3 manifested file '+name)
        mapping[name]=target
    registry.add('archive/r3/RELEASE_MANIFEST.json',R3/'RELEASE_MANIFEST.json','Original immutable R3 manifest')
    registry.add('archive/r3/CHECKSUMS.sha256',R3/'CHECKSUMS.sha256','Original immutable R3 checksums')
    registry.add('handoff/R3_MAPPING.json',(json.dumps(mapping,indent=2)+'\n').encode(),'Exact original R3 path -> delivered member mapping')
    registry.add('START_HERE.md',ASSETS/'START_HERE.md','Current finite development handoff')
    registry.add('README.md',ASSETS/'START_HERE.md','Current portable entry point')
    registry.add('AGENTS.md',ASSETS/'AGENTS_PORTABLE.md','Current portable agent contract')
    for name in ['verify_package.py','reconstruct_r3.py','prepare_local_draft.py']:
        registry.add('handoff/'+name,ASSETS/name,'Portable handoff helper')
    vectors=json.loads((ROOT/'configs/tc1l_minilm_local_20261102_lock.json').read_text())
    for role,filename in [('old_docs','old_docs.npy'),('new_docs','new_docs.npy'),('new_queries','new_queries.npy')]:
        spec=vectors['data'][role];source=Path(spec['path']);source=source if source.is_absolute() else ROOT/source
        if sha(source)!=spec['sha256']:raise ValueError('MiniLM input changed')
        registry.add('inputs/minilm_fiqa/'+filename,source,'Verified byte-identical TC1L '+role)
    registry.add('inputs/minilm_fiqa/fiqa_dev.tsv',ROOT/'results/tc1l_local_r1_20261102/full/scoring/fiqa_dev.tsv','Already-inspected development labels; no new test access')
    registry.add('paper/additional_material/tc1l_minilm_ablation.tex',supplement(),'Generated current TC1L table fragment')
    registry.add('paper/additional_material/tc1l_minilm_effects.pdf',ROOT/'results/tc1l_local_r1_20261102/report/fig_tangent_controls.pdf','Verified TC1L figure')
    registry.add('provenance/source_history.bundle',bundle,'Original complete Git history '+SNAPSHOT)
    skills=Path('D:/DASFAA-2027-MixIndex/.agents/skills')
    for p in skills.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:registry.add('research_skills/ARIS/'+p.relative_to(skills).as_posix(),p,'Existing local ARIS skill snapshot; optional')
    aris=Path('C:/Users/Gia Huy/aris_repo')
    for name in ['LICENSE','LICENSE.md','tools/evidence_check.py']:
        if (aris/name).is_file():registry.add('research_skills/ARIS_upstream/'+name,aris/name,'Upstream ARIS license/helper snapshot')
    registry.add('handoff/PACKAGE_SCOPE.json',(json.dumps({'source_commit':SNAPSHOT,'client_date':'2026-11-02',
         'R3_manifested_files_preserved':len(mapping),'original_R3_manifest_sha256':sha(R3/'RELEASE_MANIFEST.json'),
         'scope':'Private paper/code/compact-evidence development; MiniLM inputs included. Full server backups/weights/E5 cache not included.',
         'paper_main_unchanged':True,'TC1L_not_yet_integrated_into_manuscript':True,'new_scientific_runs':False,
         'original_scientific_inputs_and_results_unchanged':True,'omitted_current_paths':registry.omitted},indent=2)+'\n').encode(),'Export scope and omissions')
    findings=credential_check(registry)
    write_json(WORK/'credential_scan_receipt.json',{'fatal_private_key_payloads':0,'literal_assignment_candidates':findings,'scope':'Exported current text/filenames; Git bundle separately checked for credential filenames'})
    record=write_zip(registry,WORK/'development.zip.partial',DEV_ROOT+'/','PACKAGE_MANIFEST.json')
    record['R3_files_preserved']=len(mapping);record['literal_assignment_candidates']=len(findings)
    return registry,WORK/'development.zip.partial',record


def main():
    global SNAPSHOT,WORK
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attempt',default='r1')
    args=parser.parse_args()
    if not re.fullmatch(r'r[1-9][0-9]*',args.attempt):raise ValueError('Expected named build attempt rN')
    if args.attempt!='r1':WORK=ROOT/('tmp/handoff_'+DAY+'_'+args.attempt)
    SNAPSHOT=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    for path in [DEV,OVER]:
        if path.exists():raise FileExistsError('Preserve existing deliverable '+str(path))
    WORK.mkdir(parents=True,exist_ok=False)
    # The bundle includes only repository history; no external SSH home is read.
    objects=subprocess.check_output(['git','rev-list','--objects','--all'],cwd=ROOT,text=True)
    bad=[line.split(' ',1)[1] for line in objects.splitlines() if ' ' in line and re.search(r'(?i)(?:^|/)(?:\.ssh|id_rsa|lxbach\.key|bachdylan-key|\.env)(?:$|/)',line.split(' ',1)[1])]
    if bad:raise ValueError('Credential-like historical filename; bundle requires review')
    bundle=WORK/'source_history.bundle'
    subprocess.run(['git','-c','pack.threads=2','-c','pack.windowMemory=32m','-c','pack.deltaCacheSize=16m','bundle','create',str(bundle),'--all'],cwd=ROOT,check=True)
    subprocess.run(['git','bundle','verify',str(bundle)],cwd=ROOT,check=True)
    print('SOURCE_HISTORY_BUNDLED',flush=True)
    _,overpart,overrecord=build_overleaf();print('OVERLEAF_SOURCE_PACKED',json.dumps(overrecord),flush=True)
    _,devpart,devrecord=build_development(bundle);print('DEVELOPMENT_PACKED',json.dumps(devrecord),flush=True)
    record={'source_commit':SNAPSHOT,'development':{**devrecord,'partial_path':str(devpart),'final_path':str(DEV)},
            'overleaf':{**overrecord,'partial_path':str(overpart),'final_path':str(OVER)},
            'status':'HASH_VERIFIED_PENDING_ISOLATED_SMOKES','no_original_deletion':True}
    write_json(ROOT/'provenance/qa/handoff_packages_preliminary_20261102.json',record)
    print(json.dumps(record,indent=2),flush=True)


if __name__=='__main__':main()
