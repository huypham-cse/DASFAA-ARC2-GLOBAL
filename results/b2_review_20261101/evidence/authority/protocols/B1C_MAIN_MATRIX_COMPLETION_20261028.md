# B1c: immutable completion of the six-method DEV matrix

Date: 28 October 2026, Asia/Saigon. This document, its lock, registries and
executable sources must be committed before smoke or scientific execution.
The pre-run commit is recorded by the deployment/launch receipts and passed
to every worker. Editing any scientific source after launch requires a new
protocol/revision and directory; it never changes a historical run.

## Authorization, question and stopping point

The user authorized careful execution of the existing B1c plan on28Oct after
reviewing its finite scope. The earlier B1-G user-review STOP is released for
this completion and its report/final D1 interpretation only. No B2, TREC-COVID
label opening, new algorithm, calibration, dataset sweep or systems campaign
is authorized. STOP after the complete DEV report and final D1 for user review.

Question: under matched fixed1024 fitting supervision and paid replacement
budgets, how does frozen ARC2-Global compare with the five declared external
configurations across the four already-inspected DEV collections? This is a
completion of the existing matrix, not independent confirmation or a search
for a favorable algorithm/configuration. All negative and failed evidence stays.

## Fixed matrix and identities

Collections and ordered query counts: NanoNQ5035/50, NanoHotpotQA5090/50,
NanoFEVER4996/50 and FiQA57638/500 (documents/queries). Two frozen encoder
pairs: all-MiniLM-L6-v2→all-distilroberta-v1 and e5-small-v2→e5-base-v2,
384→768. Exact model revisions and encoder source manifests are copied into
the lock from the historical B1-M input lock. No encoder is invoked in B1c;
reuse the exact previously sealed embedding bytes, query IDs and document order.
The registry binds each vector file and each input/selection file by SHA256.
No unverified historical Nano learned fit is substituted for a current fit.

Seeds17,29,41,53,67; budgets25%,50%,75%. Reuse the original ordered1024
anchors and paid-ID arrays from B1-M verbatim, including FiQA's historical
selection rule. Paid count is floor(fraction*N), anchors are included and paid
sets are nested. No qrels, frequencies or relevance-based sampling enter fit.
Charge unique destination document vectors as |A union S|, equal to the paid
count here; this is cached logical exposure, not fresh physical encoding cost.

The six method IDs are:

- `arc2_global_tangent2_r1`: centered rectangular Procrustes initialization,
  lambda10, exactly two tangent ridge updates; no local residual or neural fit.
- `procrustes_global`: centered Procrustes alignment adaptation.
- `la2m20_integration_script_adaptation`:20 clusters,n_init4, source routing,
  unchanged fallback and centering from the B1b adapter.
- `simplelinear_official_final50_mlp5`: pinned upstream official five-affine-layer
  MLP/SELU, final50 epochs,batch4028, original AdamW/MSE+0.5cosine; no qrel
  validation or early stopping. Its name does not imply a linear model.
- `ridge_affine_l10_bias_regularized`: augmented affine ridge, lambda10
  including bias, unchanged normalization.
- `embedding_converter_paper_spec`: unchanged paper-spec adaptation, full-width
  50000 selection updates,batch64,k100; paired-vector validation split
  default_rng(seed+20261025), firstfloor(N/8) validation; earliest minimum
  coordinate MAE at250-update checkpoints; fresh all-anchor refit for exactly
  selected_iteration updates. Preserve dense float32 neighbor scores, stable
  rowwise neighbor ties and existing optimizer/loss/RNG/checkpoint policies.

These are declared baseline configurations/adaptations, not reproductions of
each paper's complete original setting. Full-X and Full-Y remain visible
native references, not an assertion that the destination always improves quality.

`configs/b1c_existing.json` identifies416 immutable existing main rankings;
`configs/b1c_sources.json` identifies precisely320 missing rankings in120groups:

| Execution phase | New endpoints | Fitting |
|---|---:|---|
| FiQA LA2M/SimpleLinear25/75 and converter75 |50|30 existing fixed1024 galleries; no new fit |
| Three Nano collections, LA2M/SimpleLinear, both pairs/five seeds/three budgets |180|60 new fits shared across budgets |
| Same Nano matrix, converter |90|30 new selection/refit workers shared across budgets |

Canonical complete matrix is720partial cells+16native refs=736. Do not confuse
this with B1-M's736-cell mechanism matrix. Do not launch the old B1-M/B1-P
campaign entry points. All-paid fits never replace fixed1024 fits. Existing
source aliases, source hashes and timings remain in provenance.

## Saved-fit reuse and source preparation

FiQA uses the30 fixed1024 sources from the two sealed B1-G registries. Before
each reused group's new endpoints, reconstruct its pristine proxy using the
unchanged B1-G reconstruction helper and reproduce its original ordered50%
top100 exactly. Preserve a mismatch and stop; do not silently refit/relabel.
Saved LA2M parameters require the pinned sklearn1.5.1 routing runtime.

The preparation inventory found47 required files absent from MAIN but present
on MINI, with518 other explicit source files already matching on MAIN. This
is a location distinction, not evidence of deletion. Copy only those47 listed
qrel-free files through the verified transport manifest, preserving source
paths/hashes and existing matching files. Verify all565 explicit source files
after transport. No source file is overwritten with differing content.
The independent labels remain untouched. Backups on D are separate artifacts.

## Deployment and arithmetic

Primary host103.73.232.225:52194, NVIDIA H10080GB HBM3;
GPU UUID and actual byte memory capacity are in the lock. CPU Python and GPU
Python paths/versions, Haswell OpenBLAS, four BLAS/OMP threads, upstream raw
source hashes, deterministic Torch and CUBLAS_WORKSPACE_CONFIG=:4096:8 are
pinned in `configs/b1c_lock.json`. TF32 stays disabled. Record host identity,
versions, process-tree RSS, own CUDA allocations, GPU sharing and stage times.
This is a shared-host quality campaign; its wall times are not isolated-H100
cost, dollars, fresh-encoding savings or SLO evidence. Do not modify other jobs,
guards, priority or GPU partitioning. No artificial elapsed/RAM/VRAM caps.

Only the materializer reads the full destination cache to select paid slices.
CPU fitting receives a paired-only target guard. Neural workers receive only
ordered source/target anchor pairs and the full source gallery; they receive
no full target cache, queries or qrels. Fit once per dataset/pair/seed/method.
Preserve pristine proxies and copy before each paid overwrite.

Exact top100 uses the unchanged `exact_topk`:float32 query batches16 @ gallery.T,
stable original document-row ties and identical-ID exclusion. Rank over the
entire collection, serialize integer positions against original IDs, reload
and verify. No ANN approximation or query mapping is introduced.

## Required smoke and execution

Run a unique matching committed smoke before the full directory. Smoke uses
synthetic256-source/128-anchor384→768 vectors, LA2M20 and both neural workers;
converter smoke uses500 selection updates with its otherwise unchanged
architecture/loss/k/validation/refit. Tests cover saved LA2M reconstruction,
finite losses/gradients, parameter updates, proxy shape/norm, stable exact ties,
identical-ID exclusion, serialization, paired-target access, nonzero child exits,
SIGTERM preservation, matrix completeness and scorer tamper/parser checks.
It is readiness evidence, not a scientific benchmark.

Only matching code/lock/registry/existing-registry smoke PASS permits full.
Execute the50/180/90 phases serially, without a new user stop between them.
Estimate duration from observed smoke/first-worker timings, explicitly allowing
shared-load and refit variation; an estimate is not a time limit or guarantee.
Each run has a unique directory, input IDs/hashes, parameters/checkpoints,
rankings, resources, timings and process exits. Original source runs are read-only.

Before any current scorer label access, finish all320new endpoints and the30
FiQA parity checks, seal every generated input/rank/fit/request/checkpoint
artifact, bind the frozen416-source registry, and record the complete seal.
The separately launched scorer verifies those artifacts and all736 rankings,
IDs/source files and code before DEV labels; it repeats verification at the end.

## Scoring and interpretation fixed before execution

Use only the exact four historical DEV qrel specifications from
`configs/b1m_score_r2_lock.json`, including the repaired implicit grade1 for
Nano positive-pair parquet. Record the first opening in this attempt before
reading/downloading/hashing labels. Prior inspection is explicitly retained:
this is not first-ever independent exposure. No TREC source is accepted.

Primary nDCG@10 uses graded2^rel-1 gain; secondary Recall@100 divides by all
positive qrels, including positives outside the Nano corpus. Unjudged items
are zero; all original evaluation queries count, including zero-positive queries.
Save736 per-query records,160condition/ref means and120condition contrasts.
Report five-seed means/SD/range, all baselines/native refs and signs. These
condition means/intervals and Recall results are descriptive.

The only inferential family is five ARC2-minus-external **macro nDCG contrasts**,
equal-weight over all24dataset/pair/budget strata. Average the five mapping
seeds first. Use20000 query-bootstrap draws, NumPy PCG64 default_rng seed20261028,
datasets in NanoNQ,NanoHotpotQA,NanoFEVER,FiQA order. Resample queries independently
between datasets; within a dataset share query draws across all methods,
encoders,budgets and seeds. Thus seed-query rows are not treated as iid.
Bonferroni nominal family95% gives individual99% percentile intervals
(quantiles0.005,0.995); coverage remains approximate. Nominal95% percentile
intervals for individual conditions and macro Recall are descriptive. The120
condition contrasts do not become120 family-tested wins.

An interval touching/crossing zero is unresolved, not equivalence or noninferiority.
A positive macro contrast supports only the declared inspected-DEV aggregate,
not every encoder/budget or an independent result. Preserve E5/Recall losses,
strong all-paid comparisons and mixed-gallery failures in final D1. No margin,
threshold, method, encoder exclusion, alternative seed or test dataset is
selected after these outcomes. No cost/SLO/traffic/causal claim follows.

## Failure preservation and finite closure

Any input/runtime/source/ID/parity/matrix mismatch, nonfinite computation,
CUDA/OS/I/O error or child failure is recorded with partial artifacts, logs,
exit signal and observations. The campaign stops rather than swallowing a
failed cell, changing parameters or silently reusing an incompatible fit.
SIGKILL can prevent a final Python receipt; preserve parent/process/checkpoint
evidence. Any actual recovery must preserve that attempt and use a distinct
documented compatible recovery/directory, not edit its status to PASS.

After separate successful scoring, retrieve raw rankings, per-query arrays,
IDs, fits/log evidence and seals; verify locally, update the single tracker,
generate full comparison/quality-budget figures, and refresh D1 through ARIS.
ARIS same-family review is provisional, not an external acceptance guarantee.
STOP for the user after B1c/report/D1. B2 requires its separate committed
protocol and user release; C2/physical/traffic work remains conditional.
