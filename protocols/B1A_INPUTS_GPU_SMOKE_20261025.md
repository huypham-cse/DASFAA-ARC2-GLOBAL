# B1a: input identity and small H100 smoke

Status: immutable after its pre-run commit. Scope: tracker item B1a only.
Latest user authorizes the full plan on H100 **one item at a time**: finish this
item, report results and wait for confirmation before B1b/another item. No
quality experiment or independent label opening is authorized by this protocol.

## Frozen inputs and environment

`configs/b1a_lock.json` pins metadata resolved before execution: three published
Nano corpus/query parquet filesets, repository commit revisions and individual
LFS SHA256/byte sizes; four existing model snapshots and every weight/tokenizer/
pooling/config hash; FiQA's historical manifest identity; original numerical
reference source and runtime. The lock and all runner sources are committed
before any dataset content preparation, fit or encoder smoke under this protocol.
Public dataset metadata resolution and read-only host/source inventory precede
the run; they are not scientific quality measurements.

- NanoNQ: 5,035 documents, 50 queries; revision
  `77540146379abf95df8326a3c5bb9eb21c7146c3`.
- NanoHotpotQA: 5,090 documents, 50 queries; revision
  `d79c0cdda980aba54842756770928035e1b61a51`.
- NanoFEVER: 4,996 documents, 50 queries; revision
  `a8bfdf1bf15181167a7e22e69cf8754bdea9b4c8`.
- FiQA: existing 57,638-document /500-DEV-query frozen cache; verify eight
  vector files, raw corpus/query/config/DEV IDs, row order and all five
  historical anchors/backfill arrays. Do not newly encode this corpus or read
  its qrels; preserve the existing inspected-development classification.
- MiniLM-L6-v2: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- all-distilroberta-v1: `842eaed40bee4d61673a81c92d5689a8fed7a09f`.
- e5-small-v2: `ffb93f3bd4047442299a41ebb6fa998a38507c52`.
- e5-base-v2: `f52bf8ec8c7124536f0efb74aca902b2995e5bcd`.

CPU numerical worker: existing NumPy 2.4.6 /SciPy 1.17.1 environment, with
OPENBLAS_CORETYPE=Haswell and OMP/OPENBLAS_NUM_THREADS=4. GPU encoder worker:
existing separate NumPy 2.2.6 /Torch 2.6.0+cu124 /SentenceTransformers 4.1.0 /
Transformers 4.51.3 environment. The inventory found that SentenceTransformers
does not import in the CPU numerical environment because of Torch/Transformers
incompatibility. Do not modify that shared environment; use it only for NumPy/
SciPy and use the verified GPU environment for encoding. Preserve this finding.
These are separate roles, not a claim to reproduce every old encoder runtime.

Target host is 103.73.232.225:52194, H100 80GB. Verify/record actual hostname,
GPU UUID, runtime versions and load. Credentials remain outside this project.
No other user's process or host guard is modified. No artificial RAM/VRAM,
idle-GPU or elapsed-time admission threshold is used.

## Source deployment

Pre-run Git commit, clean tracked worktree and canonical-LF source hashes are
checked on H100. Deploy from that committed Git bundle into a new code folder.
The fixed numerical API keeps `arc2_global_tangent2_r1`, lambda=10, exactly two
tangent steps and no local residual. New retrieval utility is tested on toy
ties only; it does not regenerate any historical ranking. Do not modify the
original repositories or append this smoke to an old scientific directory.

## Input preparation, before GPU work

1. Verify pinned source files and all existing model files.
2. Compare standalone ARC2-Global with the **original evaluated** numerical
   implementation on seeded normalized synthetic arrays at 24->24,24->40,
   40->24 and384->768. Require exact base/one-step/final coefficient, proxy
   and mixed-gallery equality, with block sizes1/13/512. Original Procrustes
   functions are extracted only from the SHA-verified upstream file; no upstream
   evaluator, qrel-dependent partitioner or dataset loader is executed.
3. Verify an explicit descending-score, original-document-row tie case and
   identical-ID exclusion case. Scientific score/batch/exclusion policy for
   future collections still requires the B1 full-run protocol; this is a toy
   implementation test, not authority to change old ranking identity.
4. Verify FiQA vector hashes/shapes/float32/unit rows in blocks; verify exact
   ordered IDs/anchors/order against the preserved source and imported package.
   Check that 25/50% selected IDs exactly match; produce the nested 75% set.
5. Download only whitelisted **corpus and queries** parquet objects for the
   three Nano repositories at the frozen revisions; verify LFS SHA256 and bytes.
   Do not request qrels or use a dataset loader that fetches all subsets.
   Preserve UTF-8 text values; sort document/query rows by their string IDs;
   assert uniqueness and expected counts. No qrel-based subsampling.
6. For each new Nano collection and seed17/29/41/53/67, generate anchors with
   default_rng(SeedSequence([seed,0])).choice(N,1024,replace=False) and a separate
   permutation with default_rng(SeedSequence([seed,1])).permutation(N). Prepend
   the anchors logically to paid selection and fill from unseen permutation
   IDs to floor(.25/.50/.75*N). Persist/hash arrays and assert nested budgets
   and anchor inclusion. FiQA retains its historical arrays instead.

## Offline GPU smoke and functional mixed-gallery check

Use only the 12 synthetic document strings and four synthetic query strings in
the committed lock, never benchmark text or labels. Load one cached encoder
at a time, local_files_only=True, no remote code, eval mode and float32. Use
128 tokens, batch4, L2-normalized outputs, explicit E5 `passage: ` and `query: `
prefixes, and empty prefixes for the MiniLM/DistilRoBERTa pair. Disable TF32,
set Torch seed17 and deterministic algorithms; CUBLAS_WORKSPACE_CONFIG=:4096:8.
Encode twice; assert declared dimensions, float32/finite/unit rows and repeat
max absolute difference<=1e-6. Record CUDA model device, model-specific wall
time and own allocated/reserved peak memory. Free only this worker's objects.

The first-pass outputs then exercise the frozen forward mapper on each pair:
12 synthetic docs,8 paired anchors,9 paid IDs,3 remaining proxies and four native
target queries; verify true-row overwrite and an exact top3 output. These toy
rankings are functional artifacts, not benchmark rankings or relevance scores.
Report physical toy encodings including repeats:96 document and32 query encoder
evaluations across all four models. They are preparation overhead, not billable
physical migration savings or full-collection encoding throughput.

## Recording, failure and completion rule

Create exactly one new `results/b1a_*` directory per attempt, with commit,
protocol/lock/source hashes, versions, seeds, input receipts, generated selections,
toy outputs, stdout/stderr, failures, wall time, process-tree RSS and periodic
shared-GPU load. No nDCG, Recall, bootstrap or baseline training occurs.
Partial downloads/failed metadata remain in that attempt. A repair gets a
visible new code/protocol revision and new directory; never overwrite a failure.
SIGTERM records an interruption; SIGKILL cannot be handled, so retain last
heartbeat and externally record a missing process. No automatic retry daemon.

PASS requires all pinned identities/counts/selection checks, four exact-reference
dimension cases, toy tie/exclusion checks, four CUDA encoder checks and both
synthetic mixed-gallery checks. Timings describe a shared-server smoke, not
isolated GPU cost/SLO. A passing tiny smoke does not establish full fresh-FiQA
encoder parity or readiness of unimplemented baselines/full scientific protocol.

After PASS or a preserved unresolved failure: **STOP**, synchronize receipts,
report B1a outcome and ask the user to confirm the next tracker item. In
particular, do not launch B1b, ablations, all-paid fitting, any full matrix,
TREC-COVID access/scoring, systems trials or claim audit automatically.
