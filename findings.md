# Current research findings

<!-- TC1L_RESULT_BEGIN -->
2 November 2026: **Matched-initialization tangent control is positive on
FiQA development for MiniLM-L6 -> DistilRoBERTa at50% inclusive exposure.**
The frozen ARC2 two-step tangent target improves nDCG@10 over both the
prediction-norm-scaled chordal control (+0.013999, corrected interval
[0.009704,0.018621]) and ordinary Euclidean residual refinement (+0.011589,
[0.007821,0.015656]). Both controls start from the same Procrustes coefficient,
use the same1,024anchors, lambda10, two updates, float64 dual solve and
float32 exact retrieval; gains are positive in allfive fixed seed means.
This directly addresses the initialization/prior confound for this configuration.
Chordal tests removing the radial target component under a common scaling rule;
it does not fix later states or target norms. Euclidean also changes norm scaling.
E5 is pending and this inspected DEV study is not independent confirmation.
All20rankings, coefficients, diagnostics, negative-query cases and saved metrics
are retained at [results/tc1l_local_r1_20261102](results/tc1l_local_r1_20261102/report/SUMMARY.md).
LocalQA PASS; ARIS yes/high/same-family/provisional. No additional experiment
required for the exact bounded claim; no paper/method change or regrade made.
<!-- TC1L_RESULT_END -->

<!-- B2_CURRENT_BEGIN -->
1 November 2026. B2 prospective TREC-COVID confirmation is complete and locally verified: 184 rankings / 60 fits, all source and chronology bindings PASS; 18,400 metric values and 2.8 million bootstrap values independently reproduced. Primary family: 11 positive / 19 unresolved / 0 negative intervals. Independent confirmed improvements: Converter 5/6, ridge 4/6, SimpleLinear 2/6; Procrustes and LA2M 0/6 each. All six Procrustes nDCG point differences are negative; unresolved is not equivalence. MiniLM Recall improves relative to Procrustes; E5 Recall falls (descriptive intervals). All native references and negatives remain reported.

The DEV aggregate benefit remains supported, while transfer is baseline/encoder/budget dependent. No physical cost/SLO/traffic conclusion follows from this representation experiment. B1-P all-paid losses and B1-G mixed-gallery reversal remain material. ARIS final review is same-family/provisional; full verdict and exact effects are in [CLAIMS_FROM_RESULTS.md](CLAIMS_FROM_RESULTS.md) and [REPORT.md](REPORT.md).

Full B2 backup: 1,330 files / 58,977,150,839 bytes complete 03:16:10+07. Compact evidence: 1,138 files / 181,895,786 bytes verified. All 20 manuscript file hashes unchanged. Current finite phase ends after results/QA/figures/ARIS; STOP before manuscript edits, B3/B4, new datasets or retuning. Earlier DEV checkpoints below are historical.
<!-- B2_CURRENT_END -->

31 October 2026. **B1-M/P0/P/G and the complete B1c-R3 six-method DEV matrix are finished.** See [REPORT.md](REPORT.md), [all B1c tables/figures](results/b1c_r3_review_20261031/SUMMARY.md) and [current claim assessment](CLAIMS_FROM_RESULTS.md).

B1c scored736cells (378retained+358new). Local verification rescored every ranking from locked DEVqrels;239,200metric values agree within3.33e-16; locked20,000-draw summaries agree within4.44e-16. All five macro nDCG comparisons favor ARC2 with positive99% per-comparison intervals in the predeclared five-comparison family. Against Procrustes, delta+0.024325, interval[+0.018132,+0.030792]; means higher in23/24conditions. The four other declared configurations have higher ARC2 means in24/24conditions each. These are inspected development results, not independent confirmation or120family-tested wins.

The new breadth closes the old missing-external-baseline gap. It does not remove the material limitations: overall Recall versus Procrustes unresolved; E5Recall lower on average; FiQA/E5/75%nDCG point difference negative with a descriptive interval crossing zero; all24partialARC2nDCG means below both native references. B1-P all-paid E5 loses to Procrustes/LA2M; MiniLM ridge remains unresolved. B1-G mixed replacement can reverse pure-proxy ordering; score-bias causality and a repair are unproved.

ARIS final D1: **narrow GO-C1 recommendation** for the planned frozen fixed-anchor B2 question. Boundedfixed-anchorquality=yes; mechanism=partial (empirical contribution supported, no optimality/general guarantee); generaldeployment/cost=no; descriptivemixed-gallerylimit=yes. Overallpartial, same-family/provisional. No new audit, method switch, parameter tuning or new experiment family was added.

**Current STOP:** authorized DEV generation, scoring, verification, report/figures and finalD1 are complete. Await user release before B2/TREC/systems. If released, the next finite scientific item is the existing184-ranking/30-contrast TREC-COVID confirmation under a new committed protocol. B3/B4 remain conditional; manuscript integration and final paper audit follow the admitted route. No additional dataset or algorithm search was made mandatory.

R3 recovered after filesystem loss without relabeling original320/R2 interrupted attempts.118fresh+2savedfitgroups,38displacedhistoricalFiQAcells preserved. Full generation took93,144.895s shared-load walltime, including the recorded output relocation pause; this is not isolated GPU-hours or physical deployment cost. Cached exposure counts|A union S| includinganchors; physicalnewdocumentencodes=0.

Backup current B1c-R3 complete31Oct13:05+07:2,484files/64,478,738,712bytes (~64.48GB),120groups,0pending/0unstable; watcher exited after terminal coverage. Data at D:/ARC2-B1c-R3-backup-20261030; proof provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json. Scope is current campaign outputs, not every historical project/cache.

## Historical27October checkpoint (superseded for completion status)

27 October 2026. B1-M/P0/P/G are complete. The consolidated numerical report is [REPORT.md](REPORT.md); the fresh semantic review is [CLAIMS_FROM_RESULTS.md](CLAIMS_FROM_RESULTS.md).

ARIS verdict: partial overall, same-family provisional. Fixed-supervision angular-refinement quality contribution: supported in inspected DEV. General strongest-baseline/physical-cost/SLO superiority: unsupported. Mixed replacement can reverse proxy-quality ordering: supported descriptively; score-bias causality remains unproven. MiniLM all-paid wins over four baseline configurations remain positive evidence; ridge is unresolved and E5 losses remain retained.

D1 recommendation: narrow GO-C1 for the frozen fixed-supervision confirmation question; no systems admission. STOP for user review before any next scientific phase. TREC stays closed; no retuning, new CI family or method selection occurred. All failures, including the first local path-check failure and successful separate R2 QA, are preserved.

Careful file review27Oct: this is a scoped provisional D1, not completion of
B1c. Actual local indices verify416/736 main DEV cells and320 missing. Finish
existing breadth, refresh final D1, then consider the unchanged184-cell B2.
FiQA's50 missing endpoints have concrete existing fit artifacts; Nano270 needs
up to 90 fits pending further compatible-cache inventory. The manuscript still
needs M/P/G integration. The legacy report renderer's overwrite of B1P/G was
reproduced/fixed in temporary copies, with preservation/idempotence PASS; live
REPORT/raw evidence remain unchanged. Full review/finite next steps are composed
into the existing experiment plan, with ARIS trace under
.aris/traces/research-review/2026-10-27_next_steps/. No new scientific run occurred.
