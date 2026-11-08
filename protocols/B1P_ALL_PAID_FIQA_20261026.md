# B1-P: all already-paid pairs on FiQA development

Immutable after the pre-run commit. On2026-10-26 the user requested B1-P.
This authorizes preparation, smoke and the full finite B1-P campaign, then report
and STOP. B1-G, remaining breadth beyond the necessary counterpart rows, D1,
TREC/independent labels, physical deployments, SLO and claim audit stay outside
this run. No artificial wall-time/RAM/VRAM/free-headroom cutoff or forecast gate.
Observe shared load and preserve actual failures and partial training/results.

## Scientific question and exact scope

Does using all28,819 already-paid source/target pairs change the fixed-anchor
comparison? Corpus57,638,500 inspected FiQA DEV queries, both existing384->768
pairs (MiniLM-L6-v2->all-distilroberta-v1, e5-small-v2->e5-base-v2), seeds17,
29,41,53,67. Destination budget is the same historical50% paid set per seed,
including every original1,024 anchor. Keep historical ordered anchors and sorted
paid row arrays, document/query IDs, vectors/prefixes/truncation/pooling intact.
All-paid fitting sees the ordered paid pairs only. Queries/relevance labels and
unpaid target vectors never enter fitting, neighbor selection or model selection.

Six rows in both regimes: Procrustes; ARC2-Global; LA2M20 integration-script
adaptation; official-code SimpleLinear; unconstrained affine ridge; adapted
Embedding-Converter. Fixed regime fits original1,024 ordered anchors; all-paid
regime fits28,819 ordered paid IDs. Both overwrite exactly the same28,819 true
vectors and leave the other28,819 proxy rows searchable. Thus encoding budget
is |A union S|=28,819 in both regimes, not an extra full-corpus paid allowance.
No physical encode is performed; these are hash-verified cached representations,
not a fresh deployment-cost campaign. Fitting/mapping/training work is measured.

Exactly124 sealed rankings:120 partial =6 methods*2 regimes*2 pairs*5 seeds,
plus four full-X/full-Y references. Reuse40 existing compatible fixed rows:
30 Procrustes/Global/ridge50% rows from B1-M and10 converter50% rows from the
imported FiQA run. Reuse four full references. Generate60 all-paid rows and20
missing fixed LA2M/SimpleLinear counterparts; those20 count toward existing B1
main-matrix cells, not extra scientific scope. Retain original method IDs and
source hashes in reuse receipts. Reused timings are not new paired measurements.

## Fixed methods and training policies

Primary default source/API stays frozen: centered rectangular Procrustes raw
affine initialization, lambda10, exactly two tangent updates, float64 updates,
storedfloat32 coefficients and normalized proxies; no local/neural component.
All-paid ARC2 uses explicit backend arc2_global_tangent2_primal_float64_r1,
validated by B1-P0 (31 synthetic and120 real budget checks). Bias is regularized,
same tangent targets/intermediate precision; original default dual code is not
changed or old results relabeled byte-identical. Store B0/one/two coefficients.
Measure SVD and combined Gram/factor/two-update phase separately from mapping.

Procrustes uses authors' normalized subtract/matmul/add path. Ridge uses
unconstrained augmented affine lambda10 including bias. LA2M uses20 clusters,
n_init4, seeded source KMeans, local centered Procrustes when>=2 rows, otherwise
global fallback, nearest-source-centroid routing. Keep this setting identical
across regimes; it is script-guided, not asserted globally optimal.

SimpleLinear executes unchanged official source5e62baf1544264847ce3d8feeabd1ded6499b064,
actual five affine layers/hidden512/SELU, AdamW lr1e-4/weight_decay1e-5,
MSE+0.5cosine, batch4028, exactly50 final epochs, no validation/early stopping.
All supplied pairs enter fit. The different number of optimizer updates is
reported, not described as equal training work. Normalize output in the gallery.

Converter remains a paper-spec anchor-budget adaptation, not official code or
the paper's large multi-corpus setup. Four affine layers, three SELUs, hidden
5*targetdim=3840, normalized final output; regression MAE+.1 global cosine-gap
MAE+.1 target-kNN100 cosine-gap MAE. Adam lr.001/betas(.9,.999)/eps1e-8, no decay,
batch64 centers with replacement,64 independent global endpoints, one sampled
top100 target neighbor per center; gradients through both endpoints. Retain
sampling, reductions, deterministic Torch seeds, precision and optimizer policy.

Explicit all-paid generalization of historical split: rng(seed+20261025),
permutation(N), first floor(N/8) validation, remainder selection training.
For28,819:25,217 train/3,602 validation; original1,024 gives896/128. Selection
always completes50,000 updates; evaluate held-pair coordinate MAE every250
updates and final; choose earliest strictly minimum checkpoint. Fresh same-seed
model/Adam then refit ALL supplied pairs for selected_iteration (<=50,000).
Do not force a50,000-step refit or use retrieval labels for checkpoint selection.
Save both fits/checkpoints/splits and include both passes in fitting cost.

Converter neighbors use separately identified exact row-block implementation,
block256, against the complete per-phase training target population. Preserve
the original defensive unit normalization, float32 cosine, self exclusion and
descending-score/ascending training-row ties. Partition boundary is resolved
using all larger scores and the lowest tied row IDs, then stable sorted top100.
This reduces workspace, never approximates the neighbor population. Before full
fits, require exact ordered equality to dense original calculations on synthetic
duplicate/near-tie fixtures and two1024x768 fixtures; record score drift. This
implementation/generalization is explicit, not a claim of byte reproduction
of the authors' original multi-corpus experiment.

## Input/runtime identities and search

configs/b1p_lock.json pins current source canonical-LF hashes, committed packaged
input bytes, the B1-M ranking seal and successful R2 scoring receipt, cached
FiQA vector manifest/ID hashes, model revision provenance, external upstream83
raw-source hashes, configurations and scorer rules. Verify clean checkout/commit
and every source/cached vector/reused ranking/selection before use. Source locks
use canonicalLF; packaged raw files use exact committed Git bytes on Linux,
avoiding the earlier Windows-derived-JSON checksum mistake.

CPU NumPy2.4.6/SciPy1.17.1/sklearn1.5.1, Haswell and four BLAS/OMP threads;
GPU existing Torch2.6.0+cu124/NumPy2.2.6 environment, verified auxiliary origins
from B1b and append-only dependency fallbacks. No shared package upgrades.
TF32off, deterministic algorithms, CUBLAS_WORKSPACE_CONFIG=:4096:8. Pin all
available runtime versions/origins in metadata. Target-only children receive
paired source, paired target and full old source files, never full-Y or qrels.

Map blocks512 for CPU and256 for neural; normalizedfloat32 proxy gallery.
Exact search float32 query batch16 @ gallery.T, stable score descending then
original document row ascending; exclude identical query/doc IDs. Top100,
every ID/paid array, source/runtime/input provenance are sealed before the
separate current-attempt DEV qrel read. Full-X uses old queries/docs; full-Y
uses new queries/docs. Failures never silently shrink the expected124 cells.

## Smoke, schedule and resources

New clean checkout/output directories, protocol+lock+source committed first.
Synthetic256doc/128paired/8query fixture,384->768, all six methods, exact saved
top100 reload/paid overwrite/unpaid identity; primal-vs-frozen tolerance1e-6.
CUDA smoke keeps converter full width/loss/k with500 selection updates and
selected-step refit; SimpleLinear keeps actual50 epochs. Require initial
nonzero gradients, finite training/parameters, actual parameter changes and
valid outputs. Late converged zero gradients alone do not fail a fit.
Run exact neighbor dense parity and synthetic graded scorer before full.
Smoke is infrastructure/throughput observation, not scientific full baseline.

After smoke PASS execute fixed serial pair, then seed blocks. Per block:
Procrustes, ridge, primal ARC2, fixed/all-paid LA2M, fixed/all-paid SimpleLinear,
all-paid converter. Save progress/checkpoints and stage receipts durably.
Automatic continuation is only within B1-P; no next tracker item is launched.
Observe process-tree RSS, host/GPU shared load, own CUDA peaks, stage wall times
(neighbor construction, selection/refit, solves, mapping/retrieval). Shared-host
timings vs imported historical rows are not an isolated speedup/deployment bill.
No wait-for-idle or machine-time cap; actual numerical/OS/I/O failures stop the
attempt and preserve prior cells. No shorter/failed fit substitutes for full.

## Separate DEV scorer and uncertainty

ops/b1p_score.py verifies exact124-key population, immutable seal/input/ranking
hashes and source/runtime context; test synthetic graded metrics before labels.
Write first current-attempt access receipt before hashing/opening historical
FiQA DEV TSV SHA03b27e547cd29dc721c3b93ce8ddd70df6b2d0ce954d8ef3659d386e8cd72c11.
Preserve original historical exposure; this is DEV, not independent confirmation.
No Nano/TREC loader or network request is used by this scorer.

nDCG@10 primary, gain2^rel-1/log2discount; Recall@100 over all positive qrels.
Count all500 queries, zero-positive/unjudged query metrics zero. Save all
124x500x2 per-query values, all means, five-seed SD/range and full-Y retention.

Predeclare32 pair-specific nDCG contrasts: within each encoder pair, all-paid
minus fixed for each of six methods; all-paid ARC2 minus each of five all-paid
baselines; fixed ARC2 minus each of five all-paid baselines. Pair outer order
MiniLM thenE5; method order in lock. Average five seed-specific query deltas
before pairedquery bootstrap20,000 draws. One shared default_rng(20261026),
PCG64, int32 index array(20000,500), reused across all contrasts/metrics.
Nominal95% intervals descriptive;32-contrast nDCG family95% uses Bonferroni
percentile interval confidence1-.05/32=.9984375 each, linear quantiles.
Coverage is approximate. Recall/retention/reference comparisons are descriptive.
Report all signs and unresolved intervals, never claim equivalence when zero
is crossed. No justified noninferiority/practical margin is invented; this
stage reports supervision sensitivity, not an automatic D1/independent decision.

On completion verify/synchronize paper-relevant raw outputs and update the live
tracker/report. Large checkpoints/proxies remain preserved with a full manifest.
STOP and report B1-P; await user before B1-G, main breadth, TREC or systems.
