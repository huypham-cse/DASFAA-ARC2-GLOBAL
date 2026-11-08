# Fresh experiment-integrity audit

**Verdict: PASS.** gpt-6.1-sol, high, fresh same-family reviewer; acceptance is provisional. No qrel files were opened, no scientific experiments or network requests were executed.

## A. gt_provenance: PASS

FiQA grades are loaded from pinned BEIR DEV TSV; Nano positive pairs from pinned dataset parquet become explicitly declared binary grade1; TREC labels come from pinned BEIR test.tsv, Git blob/size checked before parsing. These are relevance judgments, not destination-model rankings. Custom graded nDCG/Recall scorer is used, not a claimed official-library invocation. This audit checks code and saved provenance receipts without opening or rehashing qrel contents.

Evidence: `ops/b1m_score.py:235`, `ops/b1m_score.py:246`, `ops/b1m_score.py:274`, `ops/b2_score.py:94`, `ops/b2_score.py:225`, `configs/b1m_score_r2_lock.json:scoring`, `configs/b2_lock.json:scoring`, `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/qrel_verified.json`.

## B. score_normalization: PASS

nDCG divides DCG by ideal DCG computed from dataset relevance grades; Recall divides retrieved-positive count by all positive judgments. Neither denominator depends on model score max/mean. Auxiliary full_y_retention fields exist in raw summaries, alongside raw metric means; paper tables, figures and cited effects use raw means and differences, not those ratios. Unit-normalized embeddings are retrieval geometry, not metric score normalization.

Evidence: `ops/b1m_score.py:130`, `ops/b1m_score.py:149`, `ops/b1m_score.py:153`, `ops/b1c_r3_score.py:497`, `ops/b1p_score.py:231`, `paper/generated/dev_macro.tex`, `paper/generated/trec_means.tex`.

## C. result_existence: PASS

353 ledger entries reconcile to saved scientific files. Main-matrix, ablation, all-paid and prospective mean values and four bootstrap families independently recomputed from saved per-query arrays. Saved B2 bootstrap arrays and all184 ranking hashes verified. Raw scoring statuses are complete/DEV_SCORED/FINAL_SCORED; no tracker prose was consulted.

Evidence: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`, `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`, `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`, `results/b1p_r5_review_20261027/scoring/results_summary.json`, `results/b1g_r1_review_20261027/scoring/results_summary.json`, `paper/review/final_review_20261101/RAW_AUDIT.json`.

## D. dead_code: PASS

All five evaluated scientific scoring paths call the shared metrics_for implementation and save its outputs. Matrix and prospective code flow from sealed ranking loads to metrics_for to per_query arrays to summaries. Gallery before/after paths use the same judged metric. No static-only metric is presented as executed. Audit does not claim an exhaustive dead-code scan of every unrelated utility.

Evidence: `ops/b1m_score.py:486`, `ops/b1c_r3_score.py:734`, `ops/b1p_score_recovery.py:270`, `ops/b2_score.py:239`, `ops/b1g_score.py:325`, `ops/b1g_score.py:332`, `ops/b1c_r3_score.py:741`, `ops/b2_score.py:244`.

## E. scope: PASS

Four development collections x2 migrations x3 budgets x6 methods x5 mapping seeds, plus native references; one prospective171332-document/50-query collection. FiQA inspected-development status, query-level inference conditional on observed seeds and fixed collections, TREC geometric-baseline non-wins, no ANN/traffic/physical-cost claim and cached exposure semantics are disclosed. Unresolved intervals are not labeled equivalence.

Evidence: `paper/sections/experimental-setup.tex`, `paper/sections/results.tex`, `paper/sections/discussion.tex`, `results/b1c_r3_review_20261031/evidence/run/scoring/cell_index.json`, `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/cell_index.json`.

## F. evaluation_type: PASS

Reported nDCG and Recall for main matrix, ablations, all-paid, gallery diagnostics and prospective confirmation use real dataset judgments. Paid returned share is a deterministic label-free diagnostic of gallery composition. Synthetic smoke/metric sanity checks and the toy mechanism are expressly separate from scientific retrieval results.

Evidence: `ops/b1m_score.py:130`, `ops/b1g_score.py:325`, `paper/sections/introduction.tex:mechanism caption`.

## Action items

No integrity correction required for this snapshot. Preserve the existing qualifiers and refresh both audits after substantive manuscript changes.

This result verifies source paths, saved provenance, numeric artifacts and scope; it does not replace fresh qrel rescoring or certify all historical environments. `RAW_AUDIT.json` contains the detailed 353-entry empirical ledger, independent recomputation checks and input fingerprints.
