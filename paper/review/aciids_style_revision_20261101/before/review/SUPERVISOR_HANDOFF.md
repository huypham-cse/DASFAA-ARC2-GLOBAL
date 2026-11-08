# ARC2-Global — current supervisor manuscript

Open **[the current PDF](../ARC2_Global_DASFAA2027_final.pdf)**. It contains 15 standard LNCS pages, a 155-word abstract, 18 references and four vector figures. The anonymous [Overleaf/source ZIP](../ARC2_Global_DASFAA2027_source.zip) is 1.13 MiB and compiles independently without research datasets.

## Main contribution

**Two ridge-fitted, norm-scaled cosine targets refine a centered Procrustes alignment while preserving one compact affine document adapter.** This is a specific finite mapping procedure for a required transition to destination-model queries and a single mixed gallery. The paper leads with the method and its strongest measured operating points.

| Evidence | Supported result |
|---|---|
| Broad development quality | Best macro nDCG in the six-method panel; +0.024325 over Procrustes with family-adjusted interval [+0.018132,+0.030792], and 23/24 higher condition means. |
| Mechanism | The second correction adds +0.006924 beyond one step; its separate family interval is positive. |
| Prospective E5 transfer | Gains over the evaluated Converter are +0.199954 to +0.257234 across 25/50/75% coverage; all three family comparisons favor ARC2. Ridge comparisons also favor ARC2 at all three budgets. |
| Partial migration operating point | Prospective MiniLM at 75% coverage reaches 0.5195 nDCG versus native Full-Y 0.5203. These are point estimates, not an equivalence test. |
| All-paid fitting | MiniLM FiQA reaches 0.367146 and beats four of five baselines in its declared family; ridge is unresolved. |
| Compact inference | 295,680 float32 coefficients: 1.13 MiB and 114.7 times fewer parameter bytes than the evaluated Converter; no neural mapper training. |

All six methods, native Full-X/Y, both migrations, all-paid outcomes and the complete prospective panel remain visible. Prospective Procrustes/LA2M differences are unresolved, with Procrustes higher in all six point comparisons. The structural storage ratio is not an end-to-end deployment cost ratio.

## Two fresh scoring rounds

Both context-naive reviewers used **gpt-6.1-sol, high**, as requested. Each returned **6/10, weak accept, confidence 4/5**. These are internal same-family simulations, not an official DASFAA rubric, decision or acceptance probability. The second reviewer scored clarity 8/10 and venue fit 8/10, while identifying incremental novelty and closest-baseline transfer as the main scientific constraints.

The final polish addresses all six second-review writing items: exact update interpretation, HMoE positioning, truthful artifact availability, migration terminology, shared bootstrap indices, and normalization/figure legibility. No third scoring round or higher score is asserted after these edits.

## Verification

| Check | Actual status |
|---|---|
| Final post-polish source-to-raw audit | **PASS** — [fresh report](final_review_20261101/FINAL_POLISHED_AUDIT.md); read its explicit scope and input hashes. |
| Earlier independent raw checks | R1: 353 claim entries/97 checks; R2: 58 claim groups, 388 mean rows and all four saved interval families. Original snapshots and reports retained. |
| Experiment integrity | A–F read-only code/provenance audit PASS for the frozen experiment inputs; no labels reopened. |
| Citation audit | **PASS**, 18 fresh single-entry assessments; repaired checkpoint/TREC contexts and HMoE wording separately rechecked. |
| Numerical/document QA | PASS; no undefined citations/references, no overfull horizontal boxes, anonymous metadata and no known identifying local strings. |
| PDF/source packaging | All 15 pages inspected; isolated ZIP compilation produces identical extracted text. |

Original reviews remain unchanged apart from explicitly documented reviewer-report transcription corrections. See [the loop log](../PAPER_IMPROVEMENT_LOG.md), [citation index](../CITATION_AUDIT.md), [document QA](FINAL_QA.json), and [source ZIP smoke](SOURCE_ZIP_SMOKE.json).

## Before submission

1. Obtain supervisor approval of the contribution, interpretation and final prose.
2. Host an anonymous code/evidence artifact and replace the accurately marked pending public link. The source ZIP is the manuscript; the separate existing R3 research release contains code, configurations, manifests and scored outputs.
3. Recheck the official conference requirements and applicable AI-disclosure wording when preparing the actual submission. No unperformed human approval is asserted.

The current bounded manuscript requires no automatic new experiment. Optional stronger closest-baseline confirmation or prior-matched tangent controls are scientific extensions, not unfinished writing steps. No H100 job, tuning, qrel opening, public upload or conference submission was performed in this loop.
