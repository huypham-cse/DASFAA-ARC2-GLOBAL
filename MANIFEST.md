# Workspace index

Updated 2026-10-26. One active report and one active plan/tracker.

Plan revision 2 incorporates mandatory mechanism/all-paid controls and conditional
systems admission. B1a input/GPU smoke and B1b external-baseline synthetic checks
are complete. B1-M736-cell DEV mechanism scoring and B1-P0 numerical validation
are complete and locally verified. The primary and imported raw results remain
unchanged. TREC and independent/physical deployment claims remain pending. B1-P R2
smoke was killed by the same guard; R3b Mini20GB smoke PASS, locally verified; full RUNNING.
Both failures are retained. No B1-P quality result yet.

| Artifact | Purpose |
|---|---|
| README.md | start/status/scope/local commands |
| REPORT.md | generated selected development results and qualifications |
| refine-logs/EXPERIMENT_PLAN.md | active experiment, H100 and paper-closure roadmap |
| refine-logs/EXPERIMENT_TRACKER.md | active completion states |
| results/b1p_r5_review_20261027/SUMMARY.md | current completed all-paid comparison and all raw fixed/allpaid results |
| provenance/qa/b1p_r5_completed_verification_20261027.json |124 rankings,28means,32contrasts,96CIs verified; original failure retained |
| protocols/B1P_SCORING_RECOVERY_20261027.md; configs/b1p_score_recovery_lock.json | committed CPU-only recovery context; no refit or metric change |
| src/arc2_global/ | standalone global-only algorithm |
| configs/method.json; datasets.json | fixed method and proposed collection registry |
| provenance/qa/b1p_r1_launch_receipt.json; b1p_r1_live_status.json | B1-P detached full run, source commit/path and observed progress |
| results/b1p_r1_smoke_receipts_20261026/ | verified six-method smoke,38 exact neighbor cases; infrastructure only |
| results/b1p_first_smoke_receipts_20261026/ | preserved blocked-neighbor synthetic failure |
| results/b1mp0_r1_review_20261026/SUMMARY.md | latest measured mechanism/P0 findings, negatives, repairs and next item |
| results/b1mp0_r1_review_20261026/full_raw_manifest.json | complete H100 inventory; local bundle omits large vector/parameter/synthetic arrays |
| results/b1a_r1_20261025/SUMMARY.md | B1a H100 PASS, source/inputs/CUDA checks and next confirmation |
| results/b1a_first_failure_20261025/ | preserved initial source-byte failure |
| results/b1b_20261026/SUMMARY.md | B1b PASS: LA2M/ridge correctness and official SimpleLinear CUDA parity |
| protocols/B1B_BASELINE_ADAPTERS_20261026.md; configs/b1b_lock.json | immutable pre-run B1b policy/source/runtime lock at commit 180db50 |
| results/fiqa_development/ | 64 raw rankings, selected per-query values, IDs and selections |
| manuscript/main.pdf; main.tex; sections/ | five-page working draft; reused LNCS structure |
| manuscript/generated/ | generated actual measured tables and interpretation |
| provenance/source_run/ | original immutable metadata/seal/input manifest |
| provenance/result_import.json | copied file hashes and selected source indices |
| provenance/implementation_extraction.json | source hashes and standalone extraction identity |
| provenance/workspace_migration.json | original paper archive and reused assets |
| provenance/package_files.json | latest working-copy file inventory and SHA256 hashes; not a scientific ranking seal |
| provenance/snapshots/ | timestamped plan/tracker history; use active files above |
| provenance/qa/ | synthetic parity, evidence verification, paper build/preview |
| tools/ | import, render, parity and package verification utilities |

No old numerical placeholders or old internal method rows are presented in the
active report/manuscript. Original history and negative evidence remain preserved
in the source repository and archive; provenance is not a rewritten history.

ARIS experiment-plan conventions were used: two claims, five bounded blocks,
must-run vs optional scope, versioned output then live copy, and this index.
The installed skill's referenced shared output-policy files were absent locally;
no approval or execution requirement was inferred from missing references.
ARIS research-review provided bounded pre-run B1a/R1, B1b and B1-M/P0 readiness reviews
(same-family/provisional). B1-M now adds DEV benchmark measurements and CIs; B1-P0 adds numerical readiness.
B1-P is COMPLETE, scored and locally verified. Latest report:
results/b1p_r5_review_20261027/SUMMARY.md; full fixed/allpaid28means and32contrasts:
results/b1p_r5_review_20261027/scoring/results_summary.md/json. All124 rankings,
per-query124x500x2 arrays,IDs,selections,receipts and logs are in that bundle.
Full manifest preserves759 original raw files/25,539,871,372bytes; large
weights/proxies remain remote. CPU-only recovery protocol/source4062d96 scored
unchanged generation7530c8e after the original pre-parse receipt-write failure.
Original FAILED_PRESERVED metadata and scoring/ remain intact. QA:
provenance/qa/b1p_r5_completed_verification_20261027.json; generation hash check
b1p_r5_generation_verification_20261027.json; STOP b1p_completion_stop_receipt_20261027.json.
No owned experiment running. B1-G/D1 wait for user; no independent claim or paper
audit was performed. Read the single live tracker and REPORT.md for current evidence.
