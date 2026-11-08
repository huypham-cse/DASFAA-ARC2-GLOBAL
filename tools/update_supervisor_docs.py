"""Update private current pointers, preserve the previous review notes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'paper';B=P/'review/revision_tc1l_gcpa_20261102/before'
def save(name,text):
    p=P/name
    if p.exists() and not (B/name).exists():(B/name).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,B/name)
    p.write_text(text,encoding='utf8')
save('README.md','''# ARC2-Global — current supervisor draft

Open **[the revised PDF](ARC2_Global_DASFAA2027_supervisor_20261102.pdf)**.
`ARC2_Global_DASFAA2027_final.pdf` is an identical convenience alias. This
revision integrates the MiniLM matched-initialization controls into Results
and Figure 3, and positions ARC2 against GCPA in related work.

The document has **16 standard LNCS pages, a 175-word abstract and 19
references**, anonymous author fields and ordinary template dimensions.
No scientific method, raw ranking or original protocol changed.

## Deliverables

- [Supervisor packet](D:/ARC2-Global_Supervisor_Review_20261102.zip): PDF, source ZIP, anonymous artifact and a short review note. User will send it.
- [Updated Overleaf ZIP](D:/ARC2-Global_Overleaf_20261102_r2.zip): select `main.tex`; no large data bundle required to compile.
- [Anonymous numerical artifact](D:/ARC2-Global_Anonymous_Artifact_20261102.zip): frozen mapper, six evidence groups, ranking arrays, verification and table/figure scripts.

The artifact is a prepared local ZIP, not a hosted link. Its README defines
frozen-output verification and mapper use on supplied vectors, separately
from full encoder training or physical deployment reproduction.

## Edit and build

Edit `main.tex`, `sections/*.tex`, `references.bib` and
`figures/mechanism.tex`. From the project root:

```sh
python paper/scripts/build_evidence.py
python paper/scripts/build_paper.py --output ARC2_Global_DASFAA2027_final.pdf
python paper/scripts/verify_paper.py
python paper/scripts/package_source.py
python paper/scripts/verify_source_zip.py
```

These commands read completed results and render the manuscript; they do not
fit, encode, open qrels or launch H100 jobs. Changed paper inputs require a
new hash-scoped audit before being treated as checked.

## Checks and provenance

See [the supervisor handoff](review/SUPERVISOR_HANDOFF.md),
[revision/evidence map](review/revision_tc1l_gcpa_20261102/REVISION_NOTES.md),
[current claim audit](PAPER_CLAIM_AUDIT.md), `review/FINAL_QA.json`,
`review/SOURCE_ZIP_SMOKE.json` and `review/EVIDENCE_MAP.json`.
The current audit is its Markdown/JSON pair; the older audit HTML and
scorecards are historical snapshots. This revision receives no new
acceptance score.

Previous documents are retained under
`review/revision_tc1l_gcpa_20261102/before/`. Original D: delivery ZIPs remain
intact. Full ARIS traces stay private. No email, public upload or conference
submission has been performed.
''')
save('review/SUPERVISOR_HANDOFF.md','''# ARC2-Global — supervisor review, 2 November 2026

**Two tangent ridge corrections improve mixed-gallery retrieval while
retaining one compact affine document adapter.** The intended application
uses destination-model queries during gradual document migration.

Read [the revised PDF](../ARC2_Global_DASFAA2027_supervisor_20261102.pdf).
The [sendable packet](D:/ARC2-Global_Supervisor_Review_20261102.zip) contains
the paper, Overleaf sources, anonymous numerical artifact, verification
summary and draft covering note. The user will send it.

| Evidence | Main message |
|---|---|
| Four-collection development | Best macro nDCG among six adapters: +0.0243 over Procrustes [0.0181,0.0308]. |
| Matched-initialization MiniLM controls — now integrated | ARC2 0.3075 vs chordal 0.2935 and Euclidean 0.2959; gains +0.0140 [0.0097,0.0186] and +0.0116 [0.0078,0.0157]. Both positive in all five seed means. |
| Second update | +0.0069 over one step [0.0038,0.0100], without another inference stage. |
| Prospective TREC-COVID | E5 beats evaluated Converter and ridge at all three budgets. MiniLM/75% reaches 0.5195 nDCG vs native Full-Y 0.5203; Recall point means lead six adapters at each budget. |
| Lower E5 destination exposure | ARC2/25% exceeds Converter and ridge/75% on all five collections; descriptive observed operating points. |
| Already-paid pairs | MiniLM improves +0.0596 [0.0393,0.0806] at unchanged 50% coverage. |
| Compact mapper | 1.13 MiB coefficients, 114.7 times fewer parameter bytes than evaluated Converter; no neural mapper training. |

GCPA is now cited from its official ICML/PMLR publication. Related work
distinguishes its consensus-direction neural corrector from ARC2's paired
destination targets, current-coefficient prior and finite affine updates.

The new ablation is FiQA/MiniLM development evidence. The completed TREC
study supplies prospective evidence, with geometric competitors retained.
Resource advantages concern destination-vector exposure and coefficient bytes;
physical encoding cost and serving SLOs require separate measurement.

## Verification and finite next step

- Current fresh ARIS [claim audit](../PAPER_CLAIM_AUDIT.md): gpt-6.1-sol/high, same-family/provisional.
- Standard LNCS: 16 pages, 175-word abstract, 19 references; no overfull boxes or undefined references; anonymous metadata.
- All 16 pages rendered/inspected; detailed figure/table checks.
- Overleaf ZIP compiled in isolation with identical paper text.
- Anonymous artifact checks 2,460 ranking records / 1,623 distinct arrays, means, gallery arithmetic and matched-control bootstrap; separately regenerates all 16 table/CSV outputs identically.

**Next: supervisor feedback on contribution framing and submission readiness.**
The local artifact is ready to share; choose anonymous hosting when arranging
the actual submission. No additional study, H100 run, retuning, label opening
or new acceptance score is implied by this revision.
''')
state=json.loads((P/'PAPER_IMPROVEMENT_STATE.json').read_text())
state.update(active_revision='TC1L matched-target integration, GCPA positioning and anonymous supervisor delivery',phase='supervisor_review',final_pdf='ARC2_Global_DASFAA2027_supervisor_20261102.pdf',final_pdf_sha256=hashlib.sha256((P/'ARC2_Global_DASFAA2027_supervisor_20261102.pdf').read_bytes()).hexdigest(),pages=16,abstract_words=175,citation_count=19,source_zip_smoke='PASS',render_fidelity='PASS',new_scientific_runs=False,remaining_checkpoint=['Supervisor feedback','Anonymous hosting/upload and actual submission after review'],score_notice='All scores remain historical assessments of their original snapshots; no new score assigned to this revision.',citation_audit='Original 18 single-entry reports retained; GCPA checked against official publication by fresh current claim auditor.')
audit=json.loads((P/'PAPER_CLAIM_AUDIT.json').read_text())
state['final_audit']={'report':'PAPER_CLAIM_AUDIT.json','verdict':audit['verdict'],'claim_records':audit['details']['total_claims'],'declared_hashes_verified':len(audit['audited_input_hashes']),'unresolved_mismatches':0,'review_independence':'same-family','acceptance_status':'provisional'}
state['latest_scoring']['snapshot_notice']='Historical pre-TC1L/GCPA-integration snapshot; not a current-revision grade.'
state['timestamp']=datetime.now(timezone.utc).isoformat()
(P/'PAPER_IMPROVEMENT_STATE.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf8')
