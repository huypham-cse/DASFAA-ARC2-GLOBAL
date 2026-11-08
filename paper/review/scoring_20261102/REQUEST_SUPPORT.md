# Fresh ARIS result-to-claim scoring

Use gpt-6.1-sol/high only, no delegation. Workspace D:/DASFAA-2027-paper.
Read-only scoring: no manuscript/scientific-file edits, qrel opening, scoring
labels anew, fitting, retrieval, new experiments or publication.

Read current paper/sections/*.tex and paper/generated/*.tex, actual 16-page
paper/ARC2_Global_DASFAA2027_final.pdf (SHA256
e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc).
Use raw scientific evidence:
- results/b1c_r3_review_20261031/evidence/run/scoring/summary.json
- results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json
- results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json
- results/b1p_r5_review_20261027/scoring/results_summary.json
- results/b1g_r1_review_20261027/scoring/results_summary.json
Their existing per-query arrays/configs/protocols/code are available. Read-only
calculations are allowed. Do not read old scores/reviewer interpretations or
author summaries. Applicable frozen/read-only instructions are supplied here;
any accidentally exposed old opinion must be disclosed, not treated as evidence.

Read paper/review/scoring_20261102/EVIDENCE_PRECHECK.json. It only establishes
that selected exact values occur in the cited files; it does not establish
semantic support. Use raw evidence for your judgment.

Extract intended claims from the current paper itself. For each, judge
yes/partial/no with positive evidence, scope limits, precise sources and a
strongest supported wording. Distinguish development breadth, independent
matched-budget confirmation, post-hoc cross-budget descriptions, auxiliary
Recall point means and structural storage from physical deployment cost.
Judge the exact current bounded paper, not universal best-method dominance.
Identify only actual unsupported claims and useful missing evidence; separate
current-claim necessities from optional extensions. Do not run any extension.

Score empirical support (1-10), fairness/rigor (1-10), practical value under the
stated scenario (1-10), and claim calibration (1-10), with anchors/reasons.
These dimension scores are not an acceptance probability or a holistic venue
score. Give claim_supported=yes/partial/no and confidence high/medium/low.

Write RESULT_TO_CLAIM_SCORE.md/.json in paper/review/scoring_20261102/.
Record model gpt-6.1-sol/high, same-family/provisional, exact current input
hashes and explicit unverified scope. No other model/agent or new experiment.
