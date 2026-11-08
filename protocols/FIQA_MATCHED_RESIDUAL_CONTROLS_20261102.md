# FiQA matched residual controls — immutable execution protocol

Date: 2 November 2026. Stage TC1. Pre-run commit is the commit first containing
this protocol, its JSON lock and scientific runner/scorer sources; record that
commit in the deployment receipt before synthetic, real smoke or full runs.
This finite DEV addition is authorized by the user's request to run the proposed
tangent ablation. Older writing/experiment STOPs are released for TC1 only.

## Question and scope

Does the tangent projection itself help compared with a norm-matched chordal
residual, and does the complete tangent refinement help compared with ordinary
Euclidean residual refinement under identical initialization and supervision?
This is already-inspected FiQA development data, not an independent test or a
method-selection opportunity. Do not change ARC2, manuscript or earlier runs.

Use exactly FiQA's 57,638 documents and 500 development queries, the existing
MiniLM-L6 -> DistilRoBERTa and E5-small-v2 -> E5-base-v2 vector caches, dimensions
384 -> 768, seeds 17,29,41,53,67, original ordered 1,024 anchors and original
50% paid selections. Each paid set has 28,819 distinct documents including all
anchors. IDs, selections, cache bytes and encoder revisions are pinned by
`configs/tangent_control_20261102_lock.json`. No new encodings are performed.

## Locked computations

For augmented source anchor design X, paired unit destination Y and raw
coefficient B, let Z=XB, r=||Z|| by row, u=Z/r, c=<u,Y>. All update trajectories
begin at exactly the same raw centered rectangular Procrustes affine B0.

| Output | Recomputed target R at each of exactly two steps |
|---|---|
| ARC2 Tangent2 | r (Y - c u) |
| Chordal2 matched-norm control | r (Y - u) |
| EuclideanResidual2 ordinary control | Y - Z |
| B0 Procrustes context | No updates; descriptive only |

Each update solves min_D ||XD-R||_F^2 + 10||D||_F^2, then B <- B+D.
Use the same dual float64 Cholesky solve X.T solve(XX.T+10I,R) for every arm;
intercept is regularized. Retain float64 between steps, export float32 only
for final inference. No line search, scale fit, per-arm prior, tuning, residual
weight, hyperparameter sweep or between-step normalization. Original frozen
ARC2 code is unchanged and its two exported steps must match this trajectory.

At a common state, C-T=r(c-1)u is radial and P_u C=T. Thus T-versus-C isolates
including that radial component in the norm-matched target, conditional on the
ridge fitting and evolving trajectories. T-versus-E also changes norm scaling.
It does not alone isolate projection, initialization or all possible residual
algorithms. A positive result is not a global optimization/convergence result.

Map all old documents by the same float32 augmented affine application with
512-row blocks and row L2 normalization, then replace exactly paid50 with the
same real destination vectors. No query translation. Exact float32 inner
product, query batches16, top100, score descending / document-row ascending
ties; exclude identical query/document string IDs before ranking. No ANN.

## Matrix and target access

Four fresh rows x two pairs x five seeds = **40 full rankings**, each500x100.
There are30 update trajectories and10 descriptive B0 outputs. Fresh rows avoid
cross-runtime historical ranking substitutions. No third encoder or dataset.
Retain all historical baselines; TC1 is a mechanism control, not a replacement
main baseline panel.

The retained75% target cache may be opened only to obtain exact paid50 rows by
sorted document index; discard the cache reference before fit/map diagnostics.
Fit sees only the1,024 paired anchors from that paid50 slice. No diagnostics,
fit, scoring threshold or case selection may inspect the withheld25% target
rows. Physical cache storage is not the logical exposure. Record28,819 logical
paid encodings per deployment scenario, but **zero physical encodings this run**.

## Runtime, artifacts and cost interpretation

Execute CPU linear algebra and exact retrieval on reachable H100 Mini .201;
the endpoint reports a four-CPU cgroup quota, so use four BLAS threads. Pin
NumPy2.4.6/SciPy1.17.1; record Python, OpenBLAS, host, load, versions, wall
times, CPU time, peak RSS and resource samples every2s. GPU exclusivity is not
required and no GPU/physical-encoding/serving latency savings claim is made.
Shared Procrustes/factor timing and per-trajectory update/map/search timing are
diagnostic phase measurements, not independent end-to-end fit-cost trials.
No artificial elapsed-time, RAM, VRAM or headroom STOP thresholds.

Create one unique campaign directory with sibling synthetic/, smoke/, full/;
never overwrite or resume a failed scientific output. Save coefficients,
float64 step snapshots, diagnostics, exact rankings, hashes, IDs, selections,
versions, logs and resource traces. Failures remain FAILED_PRESERVED with
traceback/available outputs; an interrupted process retains its last progress.
Recovery needs a separately recorded immutable amendment; do not silently
overwrite this protocol or lock. Source/input identity mismatches are STOPs.

## Smoke and gates

Before full: run committed deterministic synthetic tests for frozen ARC2
bitwise coefficient parity; target/radial projection identities; independent
primal/dual solve/normal equations (1e-10 synthetic tolerance); scale
equivariance of tangent/chordal; Euclidean second-step recurrence; aligned,
antipodal and least-squares-stationary behavior; nontrivial held-out effect;
stable tie order; zero-direction rejection; existing graded/binary metric
synthetic checks. Zero/nonfinite raw direction<=1e-12 is a preserved failure.

Then qrel-free real smoke uses both pairs, seed17, same full corpus/query
paths, all four outputs:8 rankings. Inspect per-step radii/cosines, radial and
tangent energies, X.T R, solve residuals, coefficient changes, unpaid proxy
changes and ranking changes. Exact unpaid-proxy identity between T and either
control stops for degeneracy interpretation before full/scoring. Legitimate
stationarity/near-zero effect is retained, never repaired to create a win.
No smoke quality scoring or arm selection. Full requires matching successful
synthetic and smoke receipts with identical lock SHA.

## Separate scoring and fixed inference

Only after all40 full rankings are sealed: a separate process rejects changed
lock/source/input/artifact/ranking hashes and validates the full matrix, IDs,
shape, bounds, unique hits and identical-ID exclusion before DEV labels open.
Use the existing FiQA dev.tsv SHA
03b27e547cd29dc721c3b93ce8ddd70df6b2d0ce954d8ef3659d386e8cd72c11;
record this campaign's label access, explicitly not first-ever access.
Reuse existing graded nDCG@10 (2^rel-1) and Recall@100 implementation, with
complete positive-qrel denominator and unjudged=0. Keep all500 queries.

Four primary two-sided contrasts: T-C and T-E for each of two pairs.
Average paired per-query metrics over the five fixed seeds first. Bootstrap
queries jointly across all four contrasts with20,000 draws, RNG20261102,
percentile linear quantiles. Bonferroni individual coverage98.75%, quantiles
.00625/.99375, approximate family coverage95%. Positive iff lower>0, negative
iff upper<0, otherwise unresolved. These intervals condition on fixed seeds,
FiQA, pairs and prior development selection; no seed/population generality.
Recall, seed SD and B0 are descriptive, no hidden extra primary hypotheses.
No quality threshold, practical margin, noninferiority or equivalence claim.

If T beats E but not C, do not attribute an isolated projection benefit.
If T beats C but not E, do not claim ordinary-residual superiority. Retain
negative/unresolved outcomes. Even four positive contrasts remain DEV evidence.

## Finite completion

Download the complete new compact run and verify hashes locally. Recompute
means/intervals from saved per-query outputs; make one comparison table and
figure. Record outcome in experiment log, findings and single tracker, followed
by ARIS interpretation. **STOP** before manuscript changes, a score regrade,
algorithm changes, new data, independent confirmation or systems experiments.
