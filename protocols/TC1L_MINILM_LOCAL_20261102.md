# TC1L — immutable MiniLM local execution amendment

Date: 2 November 2026 (Asia/Saigon). The user explicitly authorized running
the MiniLM branch locally after SSH .201/.225 became unreachable. This releases
the earlier no-duplicate-launch limitation for this **separately named local
measurement only**. Remote TC1 status remains unknown; never overwrite, cancel,
relabel or combine its records as if byte-identical to this Windows run.

## Fixed question and matrix

Carry forward all mathematical definitions, frozen ARC2 code, two control
targets, lambda10, exactlytwo updates, dual float64 solve, bias penalty,
float64 between-step state, float32 inference, and interpretation boundaries
from `FIQA_MATCHED_RESIDUAL_CONTROLS_20261102.md` and the ARIS design.
Change only execution environment and available pair coverage.

MiniLM-L6 -> DistilRoBERTa only, FiQA DEV57,638docs/500queries; original
1,024ordered anchors and paid50 sets, seeds17,29,41,53,67. Four rows:
B0 Procrustes (descriptive), ARC2 Tangent2, norm-matched Chordal2 and ordinary
EuclideanResidual2. Exactly20fresh full rankings and15update trajectories.
E5 is unavailable locally and remains pending, not discarded based on quality.
No new datasets, neural training, document encoding, method tuning or paper edit.

## Cache recovery and exposure

Recover the old/source and full destination MiniLM document NPYs by byte
transport from existing `local_transport_20261030.tar`. Expected SHA256s:

- old:59b14828cfe583d279c6cd2f79365c169b573e8331dbf4c1f4ee241214c35782
- destination:a0d10483e5c02ddadee94aeb44da717d6fb068473702caac63249ee33a89ff56
- destination queries:826911a012bb37e0b117f0929517ee3c21345dc9f402cda71c47cf677a550375

This recovers previously measured bytes, not a new encoding. Source/query/
target/ID/selection hashes and model revisions are pinned in the local JSON
lock. Full target bytes may be hashed and its NPY metadata inspected; numeric
access is restricted to the original28,819paid50 rows (including allanchors).
Fit reads only1,024anchor target rows; gallery overwrite reads paid blocks;
unpaid diagnostics read source vectors and map coefficients only.

## Local environment and bounded memory

Windows Python3.12, NumPy2.5.3, SciPy1.18.1; record complete actual versions,
BLAS, host, resource/load, walltime, CPUtime and sampled peakRSS. Use4BLAS
threads, sequential seeds and arms. These are computational environment
differences from Linux TC1, not a new algorithm or a cross-platform byte-match
claim. No artificial elapsed/RAM/VRAM/headroom stop thresholds.

Each arm maps source rows in512-row blocks using the original float32 affine
expression and normalization. Put the one current gallery in a disk-backed
NPY mmap; insert the exact paid destination rows with blockwise validation.
Retrieval uses the original full-document float32 query-batch16 matmul and
stable argsort: score descending, document-row ascending ties; exclude equal
query/document string IDs. Do not replace this with document-block score
accumulation, reduced precision, approximate retrieval or top-k partitioning.

Avoid whole-gallery `_vectors` temporaries and arrays of all unpaid proxies.
Calculate diagnostics by small source blocks, retaining only scalar summaries
and cosine samples. The gallery is explicitly temporary scratch, not a raw
measurement artifact: close its mmap, verify its resolved path belongs to this
run's scratch directory and unlink only that single successful arm's file
after rankings are saved. Preserve failed scratch and all failure metadata.
Never delete any old inputs, outputs, raw rankings or unknown remote process.

## Required execution gates

Commit this protocol, local lock, code and pre-run review before any synthetic
or real-data numerical experiment. Use one unique local campaign directory.
Static review is same-family/provisional gpt-6.1-sol/high.

1. Deterministic synthetic checks from TC1, including exported tangent bitwise
   parity to frozen code and independent solve/target identities; additionally
   compare mmap-vs-memory q16 rankings with identical-ID exclusion/duplicate
   ties, and reject negative/duplicate/out-of-range indices.
2. Qrel-free seed17 smoke on full corpus/500queries, allfour rows. Record
   target energies, norms, normal-equation residuals, unpaid proxy/ranking
   changes, map/search times and RSS. Exact unpaid T/C or T/E identity stops
   for interpretation. Do not score smoke quality or select cases by outcomes.
3. Full allfive seeds only after matching synthetic and smoke PASS receipts.
   Hash/seal all20rankings, coefficients, float64 snapshots, diagnostics,
   IDs, selections and all inputs. Failure outputs remain FAILED_PRESERVED;
   no silent resume, overwrite or automatic science retry.
4. A separate scorer process checks exact20cell identities/distinct contained
   paths, complete locked input hashes, source versions, original IDs/order,
   hit shapes/ranges/uniqueness and identical-ID exclusion before labels.

## Labels and statistical family

Recover only FiQA dev.tsv from the old transport archive **after the full
ranking gate**, record campaign label access and require SHA256
03b27e547cd29dc721c3b93ce8ddd70df6b2d0ce954d8ef3659d386e8cd72c11.
These are already-inspected DEV labels, not a first-ever independent opening.
No TREC-COVID/Physics/Mathematica labels or final-test tuning.

Reuse existing graded nDCG@10/Recall@100 and all500queries. Average per-query
metrics over the five paired seeds before query bootstrap20,000draws,
RNG20261102. Observe T-C and T-E for MiniLM, but **retain the original four
contrast family**, with two E5 contrasts pending: individual98.75% percentile
intervals, linear quantiles.00625/.99375, approximate95% original-family
coverage. Do not shrink K to2 to obtain narrower intervals. Positive iff lower
>0, negative iff upper<0, otherwise unresolved. Recall, B0 and seed SD remain
descriptive. No noninferiority/equivalence or quality-matching margin.

All mechanism claims stay conditional on this MiniLM DEV configuration and
declared arithmetic. T>E without T>C does not isolate tangent projection.
T>C without T>E does not establish ordinary-residual superiority. Keep all
negative/unresolved observations and distinguish local from remote results.

## Finite completion and STOP

Independently recompute all20rankings'20,000per-query metric values from saved
raw IDs/qrels, saved means and the locked bootstrap. Generate one comparison
table and a vector figure, visually inspect it, update current log/findings/
tracker and obtain ARIS interpretation. Shared initialization/factor and mmap
map/search times are diagnostic phases, not physical deployment-cost savings.
**STOP before manuscript edits, algorithm changes, regrading, E5 cache
acquisition/rerun, new datasets or systems experiments.**
