# TC1L local pre-run static review

Date: 2026-11-02. Reviewer: secondary Codex gpt-6.1-sol/high using ARIS ablation-planner, same-family/provisional. **Final verdict: PASS_TO_COMMIT_AND_SYNTHETIC.** No scientific stage, qrels, or label member was opened by this review. No implementation/manuscript changes were made by the reviewer.

Final reviewed lock SHA256: `82c54141f70c451ab7d90833a8c78f9e14d765aa7e19ca4cbccded50b6a2dbd6`.

The finite scientific design and numeric implementation are sound on static inspection. Both required corrections from the first draft are resolved. This is permission to proceed through the already authorized committed protocol gates, not a claim that synthetic, real smoke, full execution, or scoring has passed. Commit the final protocol/lock/code/review before synthetic.

## Resolved first-draft corrections

1. **Prior-stage integrity: resolved.** Campaign records successful synthetic/smoke metadata SHA256s and the smoke seal SHA256 in `stage_receipts.json`. The next runner verifies each metadata digest/status/local-lock identity. Before full, it additionally checks the receipt-bound smoke seal, four-cell count, local-lock identity, path containment and every sealed smoke artifact digest. The synthetic success metadata is now explicitly hash-bound by the campaign receipt. A missing or altered retained stage artifact stops progression rather than being silently recreated.
2. **Runtime provenance: resolved.** Runner enforces full pinned Python version, platform system, NumPy and SciPy before computation. Scorer constructs and checks the same runtime dictionary before label access and includes it in scoring metadata. Runner records actual BLAS details under the four-thread limit. No historical Linux byte-parity claim is made. The scorer carries its runtime dictionary in memory before labels and writes it in its final/failure metadata; label access is durably recorded separately before opening the archive member.

The updated scorer also hashes the exact bootstrap query indices as concatenated little-endian int64 bytes while retaining the original draw stream. Refreshed lock pins and AST parsing passed. The earlier draft review used an incorrect source-count total: the verified current counts are18 total source pins, including11 unchanged scientific-module pins; the pass/fail checks themselves had no mismatches.

## Verified static properties

- All18 source pins currently match. All11 `src/arc2_global/*.py` pins are identical to the original TC1 lock, including frozen model, procrustes, residual targets, numerical application, and retrieval. No frozen API or computation was changed.
- All14 locked input files match their current SHA256s by independent byte-stream hashing: old/new documents, destination queries, five anchor files, five paid50 files, and IDs. The recovered document hashes and destination-query hash match the original protocol. This check performs no target numerical scan.
- IDs use the actual `doc_ids` and `query_ids` keys: 57,638 unique document strings and500 unique development query strings. Original ID SHA matches the parent lock. All five original ordered-anchor and paid-selection SHA values match the parent. Query vector bytes retain the original declared ordering provenance; this review does not infer semantic row order from values.
- Fit reads `new[a]` for only1,024 anchors after validating all anchors belong to the28,819 paid rows. Mapping reads destination numerics only at each block's paid indices; no withheld-target numerical validation, normalization, or diagnostics occur. Whole-file target hashing is byte-only. Anchors retain their input order.
- `fit_controls` preserves common B0, float64 dual Cholesky solve, lambda10, two own-state residual updates, regularized intercept and float32 final export. Both exported frozen tangent steps are checked for array equality in each real cell. No historical cross-runtime byte claim is made.
- Only one full disk-backed float32 gallery is created per arm. Small-block unpaid diagnostics retain scalar summaries/cosine samples. Mapping keeps the original512-row augmented float32 affine expression and normalization; paid rows are inserted exactly, without renormalizing target vectors. Retrieval retains full-document query-batch16 matmul and stable descending sort with identical-ID exclusion.
- Successful scratch is flushed, closed, path-contained and unlinked per arm; failed scratch is preserved. Input maps remain open only for the process lifetime and are never deleted. No previous outputs are overwritten. There is no automatic retry.
- Synthetic scaffolding retains all original mechanism/metric checks and adds mmap-versus-memory rank equality with duplicates, identical-ID exclusion, and a partial final batch. The four reviewed Python files parse successfully via AST. No synthetic numerical checks have yet run.
- Scoring requires20 distinct exact pair/seed/method/budget cells, lock/input/source/artifact hashes, original IDs,500x100 integer ranks, bounds, unique hits and exclusion before extracting only the expected18,327-byte DEV member. It then checks the original qrel SHA. The primary contrasts average five seed metrics per query before jointly resampling20,000 query draws with default_rng20261102. K=4,98.75% individual linear percentile CIs are preserved, and E5 is pending. B0 and Recall remain descriptive.

## Completion requirements to retain

The current scorer writes raw per-query values, bootstrap contrast draws and query-index SHA256, enabling a separate report to reproduce the fixed results. The executor explicitly retained corrected-only primary decisions; nominal95% intervals are unnecessary for this local report. Per-seed paired summaries/ranges and exact query win/tie/loss counts can be descriptive post-analysis from the sealed raw arrays without introducing a new hypothesis. Do not call the current abbreviated summary the final comparison table/figure/independent-verification report. The local amendment explicitly treats full galleries as scratch rather than retained raw artifacts; coefficients, inference source, locked inputs and rankings remain retained for reproducibility. No claim of a saved or historically byte-identical gallery is supported.

The three scientific stages must remain qrel-free; smoke rows do not replace fresh full rows. STOP on exact unpaid T/C or T/E proxy identity for interpretation. A complete local MiniLM campaign does not complete original two-pair TC1, establish independent confirmation, or authorize manuscript/method changes. Original remote status stays unknown.

## Files reviewed

`ops/tangent_control_local_{run,score,campaign}.py`; `tools/build_tc1l_lock.py`; `protocols/TC1L_MINILM_LOCAL_20261102.md`; `configs/tc1l_minilm_local_20261102_lock.json`; original TC1 source/protocol/lock; `ops/b1m_score.py` metric/parser definitions; `tools/recover_tc1l_inputs.py` and its recovery receipt; ID metadata. The qrels archive member was not read.
