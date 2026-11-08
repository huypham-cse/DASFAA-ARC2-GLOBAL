# B1-G readiness review

Date: 2026-10-27. Verdict: **READY_TO_COMMIT**.

`review_independence: same-family`; `acceptance_status: provisional`.
Reviewer: fresh delegated Codex agent `/root/b1g_readiness_review`, using the
parent's user-authorized inherited review route. This is implementation and
protocol readiness, not cross-family acceptance or a scientific result.

No concrete scientific or execution-order blocker was found. Commit the frozen
protocol, registries, lock and implementation, then run the committed smoke on
each shard before either full shard. Both complete qrel-free seals must precede
the separate DEV scorer. A real parity failure remains a failure; this review
does not pre-approve relaxing it.

## Evidence checked

- Read workspace AGENTS, README, live experiment plan/tracker, B1-G protocol and
  lock, both source registries, staging/ranking/analyzer/scorer code and shared
  diagnostics. Compared reconstruction with original numerical, Procrustes,
  retrieval, baseline adapter, B1-M/B1-P mapping and B1-M scoring code.
- Independently enumerated the complete expected identity matrix from local
  registry JSON: exactly 450 distinct cases and 210 distinct fitted galleries;
  360 B1-M cases, 60 FiQA all-paid cases and 30 extra FiQA fixed baseline cases.
  All four DEV datasets, two pairs, five seeds and declared budgets are present.
  MAIN has 137 groups/377 cases; MINI has 73/73. No duplicate scientific identity
  or omitted expected cell was found.
- Both registry byte digests and every canonical LF source digest match the
  current lock. All registered worker file specifications use the required
  `path`/`sha256` schema. Registry JSON uses LF bytes. All 90 extra FiQA cases
  link by ranking hash to the local historical B1-P cell index.
- Recovered CPU paths preserve centered subtract/matmul/add Procrustes,
  augmented affine multiplication, float32 normalization and mapping blocks of
  512. LA2M reuses saved centroids with pinned `KMeans.predict`, saved local maps
  and original global fallback. Saved neural proxy paths perform no training.
  Exact mixed parity gates all 450 historical rankings before diagnostics can
  count as a completed shard.
- Full reference vectors are read only by materialization of paid slices and
  the fixed hash-ID sample. Worker requests separate ranking from sampled true
  vectors; the rank request whitelist rejects full-target/qrel fields. Sample
  score errors compare the same query and document, with explicit strata,
  counts and null empty strata. The pure endpoint includes anchor predictions
  and is correctly qualified as an exposed-model diagnostic counterfactual.
- The scorer validates both complete portable shard bundles before any DEV
  qrel access receipt/open. It retains unchanged graded nDCG/Recall and requires
  every mixed per-query result to match historical arrays at absolute tolerance
  1e-12, using original ranking hashes and query IDs. MINI vector paths are not
  reopened on MAIN. Only the declared paid-target cache prefix is excluded from
  portable artifact hashing; samples, score arrays, rankings and contexts remain
  mandatory and hash-covered.

## Resolved observation

The first reviewed protocol promised CPU-load records, while the imported
`b1a_stage.Observations` records memory and GPU observations without a separate
CPU-load measurement. The executor narrowed the final protocol to RSS/wall
time and actual failures, with shared-host timing qualifications and no
separate CPU-load profiling claim. The updated protocol canonical hash matches
the final lock; all other canonical source hashes still match. No numerical
code changed. No remaining readiness blocker was found.

## Remaining gates and claims

This audit read local code, protocols, registries and historical index metadata.
It did not access remote artifacts, fit a model, generate scientific diagnostics,
open qrels, run experiments or commit changes. Runtime/pristine-proxy remote
inventory evidence was supplied by the executor; actual committed shard smoke
and all historical parity checks remain required execution gates.

No result has yet been established by B1-G. Completed data may describe
before/after retrieval and sampled same-document score/geometry differences in
the declared DEV scope. It cannot establish calibration, causal root cause,
independent success, ridge equivalence, or deployment cost/SLO. Retain negative
E5 findings and unresolved comparisons. D1 must combine B1-M/P/G evidence and
record a bounded recommendation, then STOP for user review. No additional
breadth, TREC, systems, fitting, calibration or claim audit is authorized by
this readiness verdict.

Trace: `.aris/traces/research-review/2026-10-27_b1g/`.
