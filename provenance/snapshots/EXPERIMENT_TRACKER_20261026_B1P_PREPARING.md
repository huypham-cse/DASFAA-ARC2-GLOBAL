# ARC2-Global tracker

Revision 2, updated 2026-10-26T08:08:18+07:00. **B1-M COMPLETE; B1-P0 PASS; B1-P IN PROGRESS.**
The user authorized B1-P on2026-10-26. Protocol/runner/scorer preparation and
ARIS readiness review are in progress; no B1-P scientific full run has launched.
B1-M/P0 remain complete:736 scored rankings,31 synthetic and120 real P0 checks.
B1-P includes60 new all-paid cells and20 missing fixed1024 baseline support
cells already belonging to the main matrix;40 fixed cells +4 refs are reused.
STOP after B1-P; B1-G/main breadth/TREC/systems or claim audit remain unauthorized.
See the single live EXPERIMENT_PLAN.md for the complete definitions and routing.

| ID | Block | Deliverable | State | Evidence / next action |
|---|---|---|---|---|
| B0a | package | global-only standalone API | PASS - exact parity | src/arc2_global |
| B0b | package | 64 selected FiQA rankings, metrics, seals | PASS - hashes/metrics | results/fiqa_development |
| B0c | package | exact parity and hash/arithmetic checks | PASS | provenance/qa |
| B0d | paper | reused template; measured report/scaffold | PASS - 5 pages | manuscript; REPORT.md |
| B1a | DEV | protocol/data/model/environment lock + smoke; random paid-set rule | PASS - H100 + local verification | results/b1a_r1_20261025/SUMMARY.md; first failure retained |
| B1b | DEV | genuine LA2M, official SimpleLinear, standard affine ridge | PASS - synthetic H100 + local verification | results/b1b_20261026/SUMMARY.md; adapters ready, no benchmark result |
| B1-M | DEV MUST | 0/1/2 tangent; lambda=1/10/100; ridge control | COMPLETE - scored/local verification | results/b1mp0_r1_review_20261026/SUMMARY.md; fixed two/lambda10 preserved |
| B1-P0 | DEV MUST | identified all-paid solver backend + parity/drift checks | PASS - numerical readiness | 31 synthetic +120 real budget checks; exact ordered top100 identity; no all-paid fit |
| B1-P | DEV MUST | FiQA 50%, all paid pairs, all six methods, two pairs/five seeds | IN PROGRESS - protocol/runner preparation | user authorized2026-10-26;60 all-paid +20 preplanned fixed counterpart cells; full not launched |
| B1-G | DEV MUST | proxy/true score and ranking diagnostics | NOT STARTED | analyzer cannot feed full-target values into fit |
| B1c | DEV | four development collections, fixed six-system matrix | PARTIAL - 396/736 DEV main cells | Procrustes/Global/ridge plus16 refs complete;20 imported converter cells;340 remaining main cells |
| D1 | decision | GO-C1 / CONFIRMATION-ONLY / NO-GO-FOR-SYSTEMS | NOT EVALUATED | after B1-M/P/G; before TREC or systems spending |
| B2a | independent | separate protocol, 30 contrasts, sealed TREC rankings/endpoints | CONDITIONAL / NOT STARTED | keep labels closed; D1 route required |
| B2b | independent | one TREC score; CI interpretation fixed before labels | CONDITIONAL / NOT STARTED | crossing zero is unresolved, not equivalence |
| D2 | decision | C2 hypothesis and quality/cost target justify case study | NOT EVALUATED | after B2 interpretation; no automatic campaign |
| B3a | systems | physical runner, event ledger, failures, actual-method smoke | CONDITIONAL / NOT STARTED | D2 first; no cache billed as fresh encoding |
| B3b | systems | 100K, four strategies, two pairs/three paired trials | CONDITIONAL / NOT STARTED | 24 deployments /36h nominal observation if admitted |
| B4a | traffic | held-out ORCAS random/frequency/coverage replay | CONDITIONAL / NOT STARTED | agreement is proxy; judged relevance if applicable |
| P1 | writing | evidence-selected route, figures and complete paper | NOT STARTED | optional systems route does not block mapper paper |
| P2 | audit | ARIS result-to-claim and fresh paper/raw audit | NOT STARTED | notify user before audit |
| P3 | release | build/render/provenance/reproduction freeze | NOT STARTED | finite completion; no automatic extra dataset |

Maximum if every stage is admitted: 920 main rankings (900 partial +20 refs),
360 extra DEV ablations and 60 all-paid DEV rankings = 1,340. The 64 imported
rankings may be reused on verified identity; at most 1,276 additional cells.
Before TREC: 1,156 DEV cells, of which 64 imported; TREC adds 184 only if admitted.
Ranking counts are not numbers of learned fits or newly physically encoded docs.

Completed unique planned quality cells:756 =64 imported +692 new. The736-cell
mechanism study includes44 reused FiQA rankings,360 new ablation cells, and
matched main rows/references. P0 diagnostic comparisons are not extra scored cells.
Maximum remaining:584 =340 DEV main +60 all-paid +184 conditional TREC.
The R1 compute run's original FAILED_PRESERVED status records the Nano parser
failure; scoring_r2_binary separately completed on the same unchanged seal.
Both that failure and the earlier Windows/Git byte-check stop are retained.
