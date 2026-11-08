# B1b completed: external baseline adapters

**PASS on H100 and local saved-array verification. STOP: waiting for user confirmation before B1-M.**

Pre-run commit: `180db50f4d2985f2ddc30557fb55c513b8856143`.
Immutable protocol: `../../protocols/B1B_BASELINE_ADAPTERS_20261026.md`.
Run: 2026-10-25T18:16:08.467073+00:00 to 2026-10-25T18:16:41.416826+00:00 (UTC; 2026-10-26 in Asia/Saigon).
Raw metadata, arrays, CPU/GPU receipts, resource trace and stdout/stderr are retained in this directory.

## Correctness outcomes

| Baseline | Checks | Largest observed absolute difference | Outcome |
|---|---|---:|---|
| LA2M script-guided adaptation | 25 author-oracle cases, five seeds | 0.0 raw prediction | PASS |
| Standard unconstrained affine ridge | 15 independent augmented least-squares cases | 0.0 coefficient | PASS |
| Unmodified official SimpleLinear on CUDA | five adapter/direct seed comparisons, 50 epochs each | 0.0 raw prediction | PASS |

LA2M includes 384->768 dimensions, 1,024 fitting pairs and 20 clusters for all five seeds. Smaller rectangular fixtures, source-only routing, exact invariance to non-anchor target values, and singleton global fallback also passed. The 20-cluster setting comes from the pinned integration-script grid; it is not claimed optimal or a full original-paper reproduction. At 1,024 pairs its local fits can be underdetermined.

SimpleLinear uses the official implementation: five actual affine layers, SELU, AdamW, MSE+0.5cosine, final epoch 50 with no validation/early stopping. The synthetic GPU fixture has 96 documents, 32 fitting pairs and 48 paid IDs. Same-seed adapter/direct final parameter hashes match exactly; parameters changed and gradients were finite/nonzero. These are synthetic training losses, not relevance scores:

| Seed | Initial loss | Final evaluation loss | Raw prediction difference |
|---|---:|---:|---:|
| 17 | 0.524310 | 0.087845 | 0.0 |
| 29 | 0.532880 | 0.091564 | 0.0 |
| 41 | 0.521863 | 0.087080 | 0.0 |
| 53 | 0.527781 | 0.090977 | 0.0 |
| 67 | 0.526823 | 0.088526 | 0.0 |

Ridge uses lambda 10 including bias and no orthogonality constraint. Paid-vector replacement and unchanged unpaid proxies passed; invalid missing-fit, changed-fit-target and duplicate-paid inputs were rejected.

## Resources and scope

Recorded stage wall time: **32.95 seconds**; peak observed process-tree RSS **1.66 GiB**; largest worker-owned CUDA allocation **111.72 MiB**. These describe a tiny synthetic correctness run on a shared server, excluding protocol preparation and transfer; they are not physical deployment cost or full-dataset throughput estimates.

No real collection, encoder or qrel was loaded; no document encoding, benchmark ranking/scoring, independent confirmation, all-paid campaign, serving/SLO experiment or claim audit occurred. Frozen ARC2-Global files remain identical to extraction hashes. Existing FiQA quality results and future matrix counts are unchanged.

The archive SHA256/size matched the server-generated receipt; all saved comparison arrays passed local verification. An initial local checksum check used a 65-character value copied from wrapped terminal output and stopped before extraction. We replaced that manual transcription with an authenticated receipt-file transfer, retained `provenance/qa/b1b_local_transfer_attempt1.json`, and changed no H100 output. No failed scientific B1b attempt was recorded.

Definitions/registry/lock stay at their pre-run contents, including the registry's then-pending status. This summary, the verification receipt and the live tracker record completion. ARIS readiness review was same-family/provisional, not an independent paper audit. The B1b tmux session ended; no automatic next stage is installed.

## Next item

**B1-M: development mechanism controls** comparing 0/1/2 tangent steps, lambda 1/10/100 and affine ridge across the four development collections, two encoder pairs, five seeds and 25/50/75% budgets. Reuse compatible main rows; only three new ablation configurations add 360 ranking cells. The proposed method stays exactly two steps/lambda 10. Write/commit the next protocol and smoke before its scientific run. Wait for user confirmation first.
