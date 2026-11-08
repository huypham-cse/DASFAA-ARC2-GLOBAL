"""Make the finite supervisor delivery; never send or publish it."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'paper'
QA=ROOT/'provenance/qa/anonymous_review_20261102'
DEST=Path('D:/ARC2-Global_Supervisor_Review_20261102')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf8')
def main():
    audit=read(P/'PAPER_CLAIM_AUDIT.json')
    assert audit['verdict']=='PASS'
    for key,h in audit['audited_input_hashes'].items():
        p=Path(key) if Path(key).is_absolute() else P/key
        assert sha(p)==h.removeprefix('sha256:'),key
    subprocess.run([sys.executable,'-X','utf8','paper/scripts/verify_paper.py'],cwd=ROOT,check=True,capture_output=True)
    subprocess.run([sys.executable,'-X','utf8','tools/update_supervisor_docs.py'],cwd=ROOT,check=True)
    qa=read(P/'review/FINAL_QA.json');smoke=read(P/'review/SOURCE_ZIP_SMOKE.json');archive=read(QA/'archives.json');verification=read(QA/'verification.json')
    assert qa['status']=='PASS' and smoke['status']=='PASS' and verification['status']=='PASS'
    assert qa['fresh_final_claim_audit']['current_snapshot']['matches_current_manuscript']
    assert qa['fresh_final_claim_audit']['current_snapshot']['verdict']=='PASS'
    if DEST.exists():raise ValueError('Refuse overwrite of supervisor packet')
    DEST.mkdir()
    pdf=P/'ARC2_Global_DASFAA2027_supervisor_20261102.pdf'
    assert sha(pdf)==sha(P/'ARC2_Global_DASFAA2027_final.pdf')==archive['pdf']['sha256']
    shutil.copyfile(pdf,DEST/'ARC2_Global_DASFAA2027.pdf')
    for key,name in [('overleaf','ARC2_Global_Overleaf.zip'),('anonymous_artifact','ARC2_Global_Anonymous_Artifact.zip')]:
        spec=archive[key];src=Path(spec['file']);assert sha(src)==spec['sha256'];shutil.copyfile(src,DEST/name)
    with zipfile.ZipFile(DEST/'ARC2_Global_Anonymous_Artifact.zip') as z:assert hashlib.sha256(z.read('paper/paper.pdf')).hexdigest()==sha(pdf)
    (DEST/'START_HERE.md').write_text('''# ARC2-Global — supervisor review

Read **ARC2_Global_DASFAA2027.pdf** first. The 16-page anonymous LNCS draft
includes the newly completed MiniLM matched-initialization ablation, a
two-panel mechanism-control figure, and GCPA positioning in related work.

## Research message

Two tangent ridge corrections improve judged retrieval during embedding-index
migration while collapsing into one affine document map. Native destination
queries search true and proxy document vectors together.

| Evidence | Result |
|---|---|
| Development macro | Best among six evaluated adapters; +0.0243 nDCG over Procrustes, corrected interval [0.0181,0.0308]. |
| Matched directional controls | ARC2 0.3075 vs chordal 0.2935 / Euclidean 0.2959. Gains +0.0140 [0.0097,0.0186] and +0.0116 [0.0078,0.0157]; both positive in every fixed seed mean. |
| Second correction | +0.0069 [0.0038,0.0100] over one step, without another inference stage. |
| Prospective collection | E5 beats evaluated Converter and ridge at all three TREC-COVID budgets. MiniLM/75% nDCG 0.5195 vs native Full-Y 0.5203. |
| Lower destination exposure | E5 ARC2/25% exceeds Converter and ridge/75% across all five collections, as a descriptive comparison. |
| Compact form | 1.13 MiB of coefficients; 114.7 times fewer parameter bytes than the evaluated Converter; no neural mapper training. |

The matched-target ablation is FiQA/MiniLM development evidence; prospective
confirmation comes from the completed TREC-COVID study. The paper retains all
external comparison methods and native references. Quality/exposure and
coefficient storage are distinct from physical cost and serving SLOs.

## Package contents

- `ARC2_Global_DASFAA2027.pdf`: current paper.
- `ARC2_Global_Overleaf.zip`: upload to Overleaf and select `main.tex`.
- `ARC2_Global_Anonymous_Artifact.zip`: frozen mapper, all six evidence groups,
  ranking/per-query arrays and verification/figure scripts. Its own README
  defines the reproduction scope and environment.
- `CHECKS.json`: final numerical, format and package checks.
- `COVER_NOTE.txt`: editable covering note, not sent automatically.
- `CHECKSUMS.sha256`: file integrity checks.

The artifact is a locally prepared blind-review copy, not a public URL. Its
2,460 indexed ranking records include reused outputs across studies and map
to 1,623 distinct byte arrays. No experiment count is inferred from this
package census. Frozen-output verification requires only modest CPU memory;
table/figure rendering additionally requires LaTeX.

## Review requested

Please assess the contribution framing, the distinction from geometric and
neural adapters, and whether the evidence presentation is ready for submission.
This packet prepares supervisor review; it has not been submitted or uploaded.
''',encoding='utf8')
    (DEST/'COVER_NOTE.txt').write_text('''Draft covering note — please edit before sending

Subject: ARC2-Global — revised manuscript and reproducibility package for review

Dear Professor,

I am sharing the revised ARC2-Global manuscript and its anonymous numerical
artifact for your review. The main contribution is a compact document adapter:
two tangent ridge corrections improve mixed-gallery retrieval while retaining
a single affine inference map and native destination queries.

The revision integrates the new matched-initialization MiniLM ablation, where
both directional-control comparisons have positive corrected intervals. It
also clarifies the distinction from GCPA and presents the completed prospective
TREC-COVID results alongside the development and paid-pair studies.

The paper fits the standard 16-page LNCS format. The Overleaf source compiles
in isolation, and the separate artifact includes the frozen method, raw ranking
evidence and verification scripts.

I would appreciate your feedback on the contribution framing, technical
positioning and readiness for a DASFAA submission.

Best regards,
[Your name]
''',encoding='utf8')
    checks={'claim_audit':{'verdict':audit['verdict'],'grouped_claims':audit['details']['total_claims'],'input_hashes_verified':len(audit['audited_input_hashes']),'reviewer':'gpt-6.1-sol/high','review_independence':'same-family','acceptance_status':'provisional'},'format':{k:qa[k] for k in ['pages','abstract_words','bibliography_entries','overfull_hboxes','unresolved_citations_or_references','anonymous_pdf_author']},'source_zip':{k:smoke[k] for k in ['status','isolated_source_zip_build','text_identical_to_current_draft']},'artifact':verification,'regeneration':read(QA/'regeneration.json'),'mapper_cli':read(QA/'mapper_cli_smoke.json'),'new_scientific_run':False,'external_send_or_public_upload':False,'new_acceptance_score':None}
    write(DEST/'CHECKS.json',checks)
    files={p.name:sha(p) for p in DEST.iterdir() if p.is_file()}
    (DEST/'CHECKSUMS.sha256').write_text(''.join(h+'  '+n+'\n' for n,h in sorted(files.items())),encoding='ascii')
    out=DEST.with_suffix('.zip')
    if out.exists():raise ValueError('Refuse overwrite')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(DEST.iterdir()):z.write(p,p.name)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for n,h in files.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
    out.with_suffix('.zip.sha256').write_text(sha(out)+'  '+out.name+'\n',encoding='ascii')
    # Original delivered handoffs are immutable historical snapshots.
    old={'D:/ARC2-Global_Development_20261102.zip':'34a628a191e1fd111fffb0476b2078f6951624a30c27dda5a2f229916516d273','D:/ARC2-Global_Overleaf_20261102.zip':'1b817ad70e9bd53988c1a3b576da627415d288fdb50b1a847d9c3a016bb5b926'}
    for p,h in old.items():assert sha(Path(p))==h,p
    result={'status':'COMPLETE','utc':datetime.now(timezone.utc).isoformat(),'supervisor_packet':{'file':str(out),'bytes':out.stat().st_size,'sha256':sha(out),'members':len(files)+1,'all_members_verified':True},'anonymous_artifact':archive['anonymous_artifact'],'overleaf':archive['overleaf'],'paper':{'file':str(pdf),'sha256':sha(pdf)},'checks':checks,'old_handoff_hashes_unchanged':True,'no_send_or_upload':True,'stop':'Await supervisor feedback; no further experiment authorized by packaging.'}
    write(QA/'DELIVERY.json',result);print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
