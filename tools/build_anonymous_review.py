"""Whitelisted anonymous export; original runs and private handoffs stay intact.

This packages existing numerical evidence. It never fits, ranks or opens qrels.
Public metadata are explicitly derivative copies, not replacement protocol seals.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, zipfile

ROOT=Path(__file__).resolve().parents[1]
R3=Path('D:/DASFAA-2027-paper-release-20261101-r3-paper-story/DASFAA-2027-paper-release')
OUT=Path('D:/ARC2-Global_Anonymous_Artifact_20261102')
QA=ROOT/'provenance/qa/anonymous_review_20261102'
FAMILIES={
 'development':'results/b1c_r3_review_20261031/evidence/run/scoring/summary.json',
 'mechanism':'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
 'allpaid':'results/b1p_r5_review_20261027/scoring/results_summary.json',
 'gallery':'results/b1g_r1_review_20261027/scoring/results_summary.json',
 'prospective':'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json',
 'matched_targets':'results/tc1l_local_r1_20261102/full/scoring/summary.json',
}
LOCKS={'dev_lock':'b1c_r3_lock.json','trec_lock':'b2_lock.json','paid_lock':'b1p_lock.json',
       'matched_lock':'tc1l_minilm_local_20261102_lock.json','dataset_registry':'datasets.json'}
KEYS={'development':'dev','mechanism':'mechanism','allpaid':'allpaid','gallery':'gallery','prospective':'trec','matched_targets':'matched'}
BAD=re.compile(r'Gia\s*Huy|bachdylan|103\.73\.232|(?<![A-Za-z])[A-Za-z]:[\\/]|/root/|/home/|/network-volume/|ARC2-server-backup|nb-[0-9a-f]{8}',re.I)
TRANSFORMS=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def clean(v,key=''):
    if isinstance(v,dict):
        return {k:clean(x,k) for k,x in v.items() if not re.search(r'(^|_)(hostname|username|ssh|passphrase|private_key|code_commit|scorer_code_commit|git_commit|commit)$',k)}
    if isinstance(v,list):return [clean(x,key) for x in v]
    if isinstance(v,str):
        if BAD.search(v):return '[private operational location omitted]'
    return v
def copied(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def public_json(src,dst):
    data=read(src);pub=clean(data);write(dst,pub)
    TRANSFORMS.append({'source':str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else str(src),'source_sha256':sha(src),'public':dst.relative_to(OUT).as_posix(),'public_sha256':sha(dst),'metadata_derivative':True})
    return pub
def main():
    if (OUT/'MANIFEST.json').exists():raise RuntimeError('Refuse overwrite of finalized artifact: '+str(OUT))
    OUT.mkdir(exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
    for p in (ROOT/'src/arc2_global').glob('*.py'):copied(p,OUT/'src/arc2_global'/p.name)
    for p in (ROOT/'licenses').glob('*'):copied(p,OUT/'licenses'/p.name)
    copied(ROOT/'pyproject.toml',OUT/'pyproject.toml')
    copied(ROOT/'tools/anonymous_artifact_verify.py',OUT/'verify.py')
    copied(ROOT/'tools/anonymous_artifact_map.py',OUT/'map_documents.py')
    (OUT/'requirements.txt').write_text('numpy>=1.26\nscipy>=1.11\nmatplotlib>=3.8\nthreadpoolctl>=3\n',encoding='ascii')
    layout={'paths':{KEYS[k]:'evidence/'+k+'/summary.json' for k in FAMILIES}}
    specs=[]
    # Every scored row is retained, including native references and negative results.
    for family,relative in FAMILIES.items():
        base=(ROOT/relative).parent;dest=OUT/'evidence'/family
        public_json(ROOT/relative,dest/'summary.json')
        for p in base.rglob('*.npy'):copied(p,dest/p.relative_to(base))
        for p in base.rglob('cell_index.json'):
            index=public_json(p,dest/p.relative_to(base));cells=index if isinstance(index,list) else index.get('cells',index.get('pure_cells',[]))+index.get('partial_cases',[])
            for row in cells:
                h=row.get('ranking_sha256',row.get('sha256',row.get('ranking',{}).get('sha256')))
                if h and family!='gallery':specs.append({'family':family,'cell':{k:row[k] for k in ('dataset','pair','seed','budget','regime','method','case_id','group_id','before_index','after_delta_index','per_query_index','per_dataset_index') if k in row},'sha256':h})
    for key,name in LOCKS.items():
        target=OUT/'configs'/name;public_json(ROOT/'configs'/name,target);layout['paths'][key]=target.relative_to(OUT).as_posix()
    write(OUT/'artifact_layout.json',layout)
    for name in ['build_evidence.py','plot_publication.py']:
        copied(ROOT/'paper/scripts'/name,OUT/'paper/scripts'/name)
    for name in ['main.tex','references.bib','llncs.cls','splncs04.bst']:
        copied(ROOT/'paper'/name,OUT/'paper'/name)
    for folder,extensions in [('sections',{'.tex'}),('generated',{'.tex','.csv','.json'}),('figures',{'.tex','.pdf','.png','.svg'})]:
        for p in (ROOT/'paper'/folder).iterdir():
            if p.suffix in extensions:copied(p,OUT/'paper'/folder/p.name)
    copied(ROOT/'paper/ARC2_Global_DASFAA2027_supervisor_20261102.pdf',OUT/'paper/paper.pdf')
    # Content-addressed raw ranking bytes. No old metadata/hash is rewritten.
    objects={}
    for base in [R3/'results',ROOT/'results/tc1l_local_r1_20261102/full']:
        for p in base.rglob('*.npy'):
            if p.is_file():objects.setdefault(sha(p),p)
    gallery=R3/'results/b1g_r1_review_20261027/portable_rankings/ranking_index.json'
    for r in read(gallery)['files']:
        specs.append({'family':'gallery','cell':{k:r[k] for k in ('dataset','group_id','case_id','kind') if k in r},'sha256':r['sha256']})
    missing=[]
    for spec in specs:
        h=spec['sha256'];spec['path']='rankings/'+h+'.npy'
        if h not in objects:missing.append(spec);continue
        target=OUT/spec['path']
        if not target.exists():copied(objects[h],target)
    if missing:raise ValueError('Missing raw rankings: '+json.dumps(missing[:4]))
    write(OUT/'evidence/ranking_index.json',{'description':'All referenced top-100 ranking arrays, unchanged bytes, content-addressed; repeated cells share objects.','cells':specs})
    # Public ordered IDs allow optional re-scoring against separately obtained judgments.
    for dataset in ['FiQA','NanoNQ','NanoHotpotQA','NanoFEVER']:
        public_json(R3/f'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/inputs/{dataset}/ids.json',OUT/f'ids/{dataset}.json')
    public_json(ROOT/'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/inputs/ids.json',OUT/'ids/TREC-COVID.json')
    public_json(ROOT/'results/tc1l_local_r1_20261102/full/ids.json',OUT/'ids/FiQA_matched_targets.json')
    notices='''# Third-party notices\n\nThe Procrustes functions in `src/arc2_global/procrustes.py` retain the upstream Apache-2.0 attribution and license in `licenses/`. Source: https://github.com/DBgroup-Edinburgh/embedding-translation at revision 5e62baf1544264847ce3d8feeabd1ded6499b064. SimpleLinear and LA2M configurations are declared adaptations of that upstream implementation.\n\nSpringer LNCS class and bibliography style retain their embedded notices. Bibliographic citations identify other work, including GCPA; GCPA has not been reproduced in this artifact. No encoder weights, corpus text or qrels are redistributed. Obtain datasets and models from their maintainers under their own terms. This anonymous review copy grants evaluation use of the project code and outputs; it does not relicense third-party material.\n'''
    (OUT/'THIRD_PARTY_NOTICES.md').write_text(notices,encoding='utf8')
    readme='''# ARC2-Global: anonymous numerical artifact\n\nThis review artifact accompanies **ARC2-Global: Tangent-Corrected Alignment for Embedding-Index Migration**. It provides the frozen mapper, declared baseline configurations, completed per-query arrays, all indexed raw ranking arrays and manuscript table/figure generation. Negative and unresolved comparisons and native Full-X/Full-Y references remain included.\n\n## Quick start\n\nUse Python 3.10+ (verification tested with Python 3.12). From this folder:\n\n```sh\npython -m pip install -r requirements.txt\npython verify.py\npython paper/scripts/build_evidence.py\n```\n\n`verify.py` checks every manifest digest, all per-query condition means, gallery before/after differences, and the matched-control 20,000-draw bootstrap. It does not contact a server or open qrels. The evidence builder regenerates tables and vector figures from the packaged saved results; LaTeX (`latex`, `dvipng`, Computer Modern) is required for figure rendering. Compile `paper/main.tex` using pdflatex/BibTeX to rebuild the manuscript.\n\n## Fit the frozen method on your own paired vectors\n\n```sh\npython map_documents.py --old-docs old.npy --anchor-indices anchors.npy --target-anchors target_anchors.npy --output proxies.npy\n```\n\nRows of `target_anchors.npy` must match the order in `anchors.npy`; all input vectors must be unit normalized. The numerical method remains centered rectangular Procrustes, lambda=10 and exactly two tangent ridge updates. The output is a document-proxy array; insert paid true destination vectors in the gallery and query it using the destination encoder. Count all unique paid rows, including anchors.\n\n## Evidence structure\n\n- `development`: four inspected collections, both migrations, three budgets, six adapters and native references.\n- `mechanism`: all original 0/1/2-step and regularization controls, including unfavorable ones.\n- `allpaid`: all fixed-anchor and all-paid FiQA comparisons.\n- `gallery`: all saved before/after mixed-gallery diagnostics.\n- `prospective`: completed TREC-COVID confirmation with its locked 30-contrast family.\n- `matched_targets`: separate Windows FiQA/MiniLM development measurement; both positive controls retain the original four-contrast family; the two planned E5 contrasts are pending.\n- `rankings/`: byte-identical content-addressed ranking NPY files; `evidence/ranking_index.json` maps all exported cells to them.\n- `ids/`: ordered public document/query IDs associated with ranking rows.\n\n## Reproducibility scope and provenance\n\nThis compact artifact verifies completed numerical outputs; it is not a cached-vector physical deployment benchmark. Model weights, corpus vectors, full training checkpoints and qrels are not included. Ranking metrics can be independently re-scored after obtaining the original BEIR/NanoBEIR judgments and checking their frozen hashes/configurations. No end-to-end cost or SLO reproduction is claimed. Inspect `configs/` for pinned models, source file hashes, seeds, policies and versions.\n\nJSON metadata in this copy are **anonymized derivatives**: private machine locations and operational commit fields are omitted. Scientific results, method names, model revisions, seeds, stored interval endpoints and numerical array bytes are retained. Their new manifest hashes identify this public copy; original protocol/ranking seal hashes in source fields refer to unchanged private archives, not to these derived JSON files. No Git history, server credentials or author-identifying logs are included.\n\nThere is no public hosting link yet. This folder can be uploaded to a blind-review host after checking the venue's current supplementary-material policy.\n'''
    (OUT/'README.md').write_text(readme,encoding='utf8')
    write(QA/'metadata_transform_private.json',TRANSFORMS)
    # Fail closed on names, personal filesystem paths and host identifiers.
    issues=[]
    for p in OUT.rglob('*'):
        if p.is_file() and p.suffix in {'.json','.md','.py','.toml','.txt','.tex','.bib','.svg'}:
            for line_no,line in enumerate(p.read_text(encoding='utf8',errors='replace').splitlines(),1):
                if BAD.search(line):issues.append({'file':p.relative_to(OUT).as_posix(),'line':line_no,'match':BAD.search(line).group()})
    if issues:write(QA/'privacy_issues.json',issues);raise ValueError('Privacy scan failed: '+str(issues[:6]))
    files={p.relative_to(OUT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()}
    write(OUT/'MANIFEST.json',{'schema':'arc2-anonymous-artifact-v1','files':files,'ranking_cells':len(specs),'unique_ranking_arrays':len({r['sha256'] for r in specs}),'policy':'Public derivative metadata; unchanged numerical arrays; no original run overwritten.'})
    write(QA/'build.json',{'utc':datetime.now(timezone.utc).isoformat(),'folder':str(OUT),'files':len(files),'ranking_cells':len(specs),'unique_ranking_arrays':len({r['sha256'] for r in specs}),'private_patterns_found':[],'original_scientific_files_changed':False})
    print(json.dumps(read(QA/'build.json'),indent=2))
if __name__=='__main__':main()
