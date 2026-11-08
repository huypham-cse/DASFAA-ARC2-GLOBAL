# B1-M mechanism and B1-P0 numerical backend protocol

Immutable after the pre-run commit. Authorization: on2026-10-26 the user
requested B1-M and B1-P0 together. Complete these two items, report, then STOP.
B1-P all-paid fits, B1-G, the remaining learned-baseline breadth matrix, D1,
TREC-COVID, independent scoring, systems deployments and claim audit are not
authorized by this protocol. No elapsed-time, RAM, VRAM or shared-load cutoff.
Preserve actual failures and all signed/negative observations.

## Fixed computation and populations

Primary ARC2-Global stays `arc2_global_tangent2_r1`, unchanged source files:
centered rectangular Procrustes raw affine initialization, two tangent updates,
lambda10, bias regularized, float64 updates and float32 stored coefficients,
normalized document proxies, destination queries and paid-vector replacement.
Fit sees only ordered source/target anchor pairs, not relevance/query data or
unpaid target rows. The float64 coefficient continues between updates; the
stored float32 one-step snapshot is never fed back into step2.

Exactly six mechanism rows: authors' normalized Procrustes zero-step control,
one step/lambda10, fixed two/lambda10, two/lambda1, two/lambda100, unconstrained
affine ridge/lambda10 including bias. `mechanism_ablation.py` is a named DEV
implementation; its lambda10 snapshots must equal the unchanged frozen API.
Do not substitute affine-expanded B0 for authors' float32 Procrustes apply.
Alternative lambdas remain named ablations, never replacement method selection.

Collections: NanoNQ5035/50 queries, NanoHotpotQA5090/50, NanoFEVER4996/50,
FiQA57638/500 already-inspected DEV. Both pinned encoder pairs: MiniLM-L6-v2
to all-distilroberta-v1 and e5-small-v2 to e5-base-v2,384->768. Seeds17,29,41,53,67;
1024 fitting anchors; budgets25/50/75%, floor(b*N) unique encodings |A union S|,
anchors included. Reuse exact B1a Nano sorted IDs, anchor/order/paid arrays;
FiQA retains historical order/anchors and derives75% from the same permutation.
Paid sets are shared by every row and nested. No traffic/label-based selection.

The complete mechanism matrix is720 partial rankings and16 full-X/full-Y refs.
Existing40 FiQA Procrustes/primary partial rows and four refs may be reused only
after vector/model/ID/source identities and qrel-free ranked-ID comparison pass.
Compatibility search is logged separately. Equal ranks copy original raw bytes;
non-identity retains old outputs and records changed-query counts, and the fresh
common-arithmetic measurement is used. No scoring selects reuse. No converter,
LA2M or SimpleLinear quality campaign is included in this item.

## Inputs, encoding and exact search

`configs/b1m_lock.json` pins B1a metadata/input files, model revisions and every
model file hash, FiQA vector manifest, code and qrel sources. Canonical-LF hashes
describe source; actual Linux lock-byte hash and pre-run commit enter metadata.
No model download, package upgrade or shared-environment mutation is needed.

Nano corpus/query strings are their published `text` columns, with no invented
title concatenation, sorted by string `_id` as in B1a. Encode each Nano document
and query once per model using the pinned existing SentenceTransformer model,
float32 eval/inference, max_seq_length128, batch32, normalized embeddings and
unchanged packaged pooling/tokenizer. E5 prefixes are `passage: ` and `query: `;
MiniLM/DistilRoBERTa have empty prefixes. Torch2.6.0+cu124, NumPy2.2.6,
sentence-transformers4.1.0, transformers4.51.3, TF32 disabled, deterministic
algorithms, seed17, CUBLAS_WORKSPACE_CONFIG=:4096:8. Log physical preparation
encodes; a reusable vector cache is not a fresh deployment cost measurement.
FiQA's eight hash-matched cached vectors preserve their historical encoding
regime; this is not a new encoder reproduction. Keep the preparation distinction.

CPU environment is the existing NumPy2.4.6/SciPy1.17.1 runtime with Haswell
OpenBLAS and four OMP/BLAS threads. Record actual library origins/BLAS settings.
Mapping blocks512; exact float32 query batch16 @ gallery.T; stable descending
score, ascending original document row on ties; exclude identical query/doc IDs.
Top100 IDs, all selections, vector/input hashes and code/runtime identity are
sealed before the separate scorer opens any DEV relevance content. Full-X uses
source queries/source docs; full-Y uses target queries/target docs.

## B1-P0, separately identified backend

`arc2_global_tangent2_primal_float64_r1` is an opt-in backend, not a silent API
replacement. With augmented X, it solves (X.T X+lambda I) delta=X.T T using
Cholesky/solve; bias, B0, tangent targets, two updates and storage are unchanged.
No28,819-pair real fit or all-paid ranking occurs. `configs/b1p0_lock.json`
enumerates finite synthetic smoke/full fixtures: same/cross dimensions,
384->768 with1024 and2048 anchors, nonzero intercept, near-collinear/duplicate
source rows, five fixed seeds, exact-tie toy. Full has31 fixtures; smoke has6.
The2048 fixture is synthetic scaling readiness, not an all-paid experiment.

Before interpreting backend readiness require float64 per-update allclose
atol=rtol=1e-9; exported coefficient, normalized proxy/gallery and exact-score
maxabs<=1e-6; finite/unit rows and paid overwrite equality. Preserve raw arrays,
errors, timings/RSS, coefficient relative/Frobenius and rank drift where produced.
Validate real1024-anchor fits within B1-M too:40 collection/pair/seed fits and
120 corresponding budget comparisons. Primary rankings continue to use frozen
dual even if primal passes. Fit/selection is not changed by relevance scores.

Report top10/top100 ordered/set identity, changed query counts and every rank
discrepancy. Exact synthetic ties must follow the unchanged row rule. Numerical
near-tie drift is distinguished from byte/ranked-ID identity: for each query,
epsilon=max absolute dual/primal score difference; every inversion among the
union of returned IDs must have dual score gap<=2epsilon. Any unexplained
larger-gap inversion or exceeded tolerance fails readiness; never loosen a
tolerance after quality inspection. Keep failed/drifted outputs. The main
study uses frozen dual and does not depend on a favorable primal quality score.

## DEV scoring and interpretation

Separate `ops/b1m_score.py` rejects incomplete/changed inputs and all collections
outside the four named DEV tasks. It verifies exactly736 sealed cells, IDs and
source hashes before label access, tests a serialized synthetic graded scorer,
and writes the first-access receipt before downloading/opening DEV qrels. Nano
qrel file URLs, revisions, bytes and SHA256 come from repository metadata only,
not opened labels; FiQA uses the historical locked DEV TSV. TREC remains closed.
Verify again before final output; preserve every failure and partial result.

Primary nDCG@10 uses gain2^rel-1 and log2 discount; Recall@100 uses all positive
qrels for each query as denominator. Unjudged hits count zero. Every registered
query remains in the mean; zero-positive/unjudged queries score zero. Record
judgments outside the sealed corpus without silently shrinking the denominator.

Five ordered contrasts: fixed primary minus Procrustes, primary minus one-step,
primary minus ridge, lambda1 minus primary, lambda100 minus primary. Report
every24 collection/pair/budget cell, nDCG and Recall, all five seed values/SD/range,
full refs and retention. Macro averages weight the24 cells equally; each encoder
macro weights its12 cells equally. FiQA does not get tenfold collection weight.

Paired query bootstrap20000 draws, seed20261026, SeedSequence.spawn(4) in order
NanoNQ,NanoHotpotQA,NanoFEVER,FiQA, each child default_rng/PCG64, int32 sampled
indices shape(draws,Q), shared across methods/pairs/budgets/seeds within collection.
Average the five locked mapping seeds before resampling. Percentiles use linear
quantiles. Report nominal95% descriptive intervals; only the five overall macro
nDCG contrasts receive99% Bonferroni percentile intervals for approximate95%
family coverage. Per-cell/encoder/Recall intervals are descriptive, not part of
that family. No justified practical equivalence/noninferiority margin is set.
Crossing zero is unresolved; bootstrap cannot remove development exposure.
No replacement-method selection, universal-win claim or D1 decision is made.

## Execution and preservation

Commit source, both locks and this protocol before any new scientific run.
New unique clean checkout and output paths; run P0 synthetic smoke and B1-M
synthetic smoke first. Only after they pass run P0 full synthetic and B1-M full
preparation/rankings, real P0 diagnostics and separate DEV scorer. Record SVD,
Gram/factor, tangent target/solve phases, mapping/retrieval, raw wall/RSS and
shared GPU traces. Shared/recomputed one-step phases are not standalone timings.
Timings on a loaded host are engineering observations, not deployment cost.
No next-stage daemon or automatic B1-P launch. STOP after both reports, update
the one live tracker and wait for the next user instruction.
