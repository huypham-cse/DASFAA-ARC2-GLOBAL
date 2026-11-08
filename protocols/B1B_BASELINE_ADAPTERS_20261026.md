# B1b: external baseline adapters and synthetic validation

Immutable after pre-run commit. User confirmed continuation on 2026-10-26
(Asia/Saigon). Authorized item: B1b only. Report results and wait for confirmation
before B1-M or another tracker item. No real collection, encoder, qrel, TREC
file, quality scoring, ablation campaign, all-paid fit or systems trial is read
or launched by this stage. Frozen ARC2-Global remains unchanged.

## External source and adaptation identity

Use the existing clean upstream checkout at revision
`5e62baf1544264847ce3d8feeabd1ded6499b064` from
https://github.com/DBgroup-Edinburgh/embedding-translation.
The lock contains all 83 relevant Python raw-byte SHA256 values measured on
Linux before this stage. Reject source drift, wrong revision or dirty upstream.
Do not use historical Windows CRLF hashes for the Linux checkout.

**LA2M:** adapt the actual integration-script algorithm in
`reproduce-scripts/la2m/exp_la2m.py`: source-anchor KMeans, n_init=4, fixed seed,
local centered rectangular Procrustes when a cluster has at least two paired
rows, otherwise all-pair global fallback, and nearest-source-centroid routing.
Do not load that script normally: extract only the three exact numerical
definitions for the test oracle, omitting harness imports, answer-balanced
partitioning, evaluation and main. The usable adapter stores fitted centroids
and local maps, accepts only paired arrays for fit and only source rows for
transform; normalized proxies are a shared gallery convention.

Pin **20 clusters** for the future main LA2M baseline: this is the first
non-global value in the pinned script's CLI grid [1,20,50,100,200], chosen before
new quality results. It is not asserted to be the published optimum, recommended
setting or best attainable LA2M. Counts1/2/4 below are synthetic correctness
fixtures only. 1,024 fitting pairs give roughly51 pairs/cluster against384
source dimensions: local maps can be underdetermined, which must remain a
stated limitation of this matched-budget adaptation. This is distinct from the
upstream package's PCA/same-dimension implementation and from local8 residuals.

**SimpleLinear:** execute the unmodified package class
`embedding_translation.mapper.simple_linear.strategy.SimpleLinearMapper` and
its actual configuration. Pin the upstream defaults: nominal layer_num=4,
hidden512, SELU, **five actual affine layers**, fixed50 epochs, batch4028,
AdamW lr1e-4/weight_decay1e-5, gradient clip1, ReduceLROnPlateau patience5/factor.5,
MSE + hard-coded0.5 cosine loss, local distillation disabled. Declared early
stopping/validation/loss/output config knobs unused by this class do not become
active features. Final model after the fixed50 epochs is used; no validation,
checkpoint selection or relevance-based refit policy is invented. Train on
all supplied allowed paired rows. Upstream outputs raw vectors; normalization
and true-vector replacement are adapter/gallery operations.

Use the existing GPU environment (Torch2.6.0+cu124/NumPy2.2.6). Official package
imports require missing dependency modules: append the two existing dependency
directories in the lock after the GPU-native search paths. Do not install or
upgrade any shared environment. Record actual module origins and versions;
Torch/NumPy must remain GPU-native. This is an explicit runtime/anchor-budget
adaptation, not a full original-paper or original-requirements reproduction.

**Affine ridge:** standard unconstrained forward affine regression, normalized
paired inputs/targets, lambda10 on every augmented coordinate **including bias**.
Solve the float64 primal normal equations by Cholesky, store coefficient float32,
then normalize predictions. This is a standard baseline, not a new ARC2 revision.

## Meaningful CPU checks

Use seeds17/29/41/53/67, all synthetic normalized float32 source/target pairs.
CPU runtime is NumPy2.4.6/SciPy1.17.1/sklearn1.5.1 with Haswell and four BLAS/OMP
threads, as inventoried. No source/target model is encoded in this stage.

- For each seed compare LA2M raw outputs with the exact authors' translate_o1
  oracle at24->40 and40->24 for1 and4 clusters, plus384->768 with1,024 paired
  anchors/20 clusters. Require absolute output delta<=1e-6 (rtol0), several
  active local maps for multi-cluster cases, and source-only transform routing.
- Give the oracle NaN non-reference targets, then arbitrary alternative
  non-reference targets; require exact output invariance. The adapter fit API
  itself accepts paired arrays only, never a corpus-sized target cache.
- Verify a separate7+1 source-cluster fixture uses global fallback for its
  singleton cluster, matching the global Procrustes kernel exactly.
- Compare ridge coefficients with an independent augmented least-squares solve
  [X_aug;sqrt(10)I], [Y;0], cast tofloat32, at absolute tolerance1e-6 (rtol0).
  Check finite normalized proxies and absence of an orthogonality constraint.
- Shared gallery must include all fitted pairs in the paid set, preserve their
  target values, overwrite paid IDs exactly and leave unpaid proxies exactly
  unchanged. Reject missing fitted IDs, changed fitted targets and duplicate
  paid IDs. Full target matrices are used only for synthetic oracle checks.

## Official SimpleLinear CUDA checks

Fixture:96 normalized synthetic384-dimensional source rows,768-dimensional
targets generated by a fixed random projection,32 paired fitting rows. For each
of the five seeds, use the actual default50-epoch official adapter and a separate
direct invocation of the exact same upstream class, config and allowed rows.
Reset Torch seed for identical initialization; deterministic algorithms,
TF32 disabled, CUBLAS_WORKSPACE_CONFIG=:4096:8, four Torch/BLAS threads.

Require actual five Linear layers/SELU, official class origin, full default-config
identity, CUDA device, finite nonzero gradients and changed parameters, and
lower synthetic training loss than the corresponding initial model. A gradient
probe after fitting must not apply an extra optimizer update. The adapter's
raw predictions must agree with the official-direct outputs within1e-6, and
the same-seed final parameter hashes must match exactly. Save both raw output
arrays, fixture arrays, configs, model-state hashes and loss/gradient receipts.
This demonstrates adapter behavior and synthetic learning, not generalization
or superiority on retrieval datasets. No50,000-step converter run occurs.

## Execution, preservation and completion

Commit protocol, lock, registry, source and runner before the new H100 attempt.
Use a new code checkout and unique `results/b1b_*` directory; record commit,
lock/source hashes, runtime/module origins, raw arrays, partial CPU/GPU receipts,
wall time, process-tree RSS, own CUDA peak allocation and shared-GPU samples.
Observe shared load; do not require an idle GPU or impose resource/time cutoffs.
Do not signal anyone else's process. Preserve stdout/stderr, actual errors,
interrupted/failed attempts and any externally observed lost process. No daemon
or automatic next-stage launch is installed.

PASS requires all25 LA2M oracle cases,15 ridge cases, singleton fallback, shared
gallery rejection checks and five official/direct CUDA seed comparisons. Save
and synchronize full receipts; verify transfer hashes and saved array comparisons
locally. Correctness PASS establishes readiness of these fixed adaptations only.
Then STOP, report B1b and wait for user confirmation before B1-M. Existing FiQA
results, numerical ARC2-Global, dataset scope and future matrix counts are unchanged.
