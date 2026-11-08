# B2: prospective TREC-COVID fixed-anchor confirmation

This protocol is immutable once committed and before acquisition/encoding smoke
or any scientific run. Its pre-run Git commit, `configs/b2_lock.json` and the
source hashes in that lock define execution authority. Later live status belongs
in the experiment tracker, never by editing this protocol or old raw attempts.

## Authorization and finite scope

The user released the completed B1c/D1 STOP on 31 October 2026 with “ok làm đi,
chừa lại phần cập nhật manuscript”. This authorizes B2 preparation, matching
smoke, the complete independent comparison, separate verification/scoring,
local result verification, figures and ARIS claim review. **Do not edit
`manuscript/`. Do not launch B3/B4, another dataset, a new method or retuning.**

The previous D1 is a narrow GO-C1 for fixed-supervision quality. B1-P's E5
all-paid losses and the unresolved MiniLM/ridge comparison remain evidence.
The original team non-exposure statement is
`provenance/trec_exposure_attestation.json`; B1c did not access TREC labels.

## Claim and complete comparison

Test whether frozen ARC2-Global improves target-query mixed-gallery retrieval
against the five declared external configurations with exactly 1,024 fitting
pairs, conditional on the specified encoder migration. No universal-win,
native-reference superiority, optimum-supervision, physical-cost, ANN, SLO or
live-traffic claim is tested here.

- Dataset: full TREC-COVID, 171,332 documents and all 50 queries.
- Pairs: MiniLM-L6-v2 (384) to all-distilroberta-v1 (768); e5-small-v2 (384)
  to e5-base-v2 (768), with the exact B1-M revisions and model-file SHA256s.
- Methods: `arc2_global_tangent2_r1`, centered `procrustes_global`,
  `la2m20_integration_script_adaptation`,
  `simplelinear_official_final50_mlp5`,
  `ridge_affine_l10_bias_regularized`, `embedding_converter_paper_spec`.
- Seeds: 17, 29, 41, 53, 67. Paid budgets: 25%, 50%, 75%.
- Exactly 180 partial rankings and four deterministic native Full-X/Full-Y
  reference rankings: **184 rankings from 60 fitted galleries**.

ARC2 remains centered rectangular Procrustes initialization, lambda10 and
exactly two tangent updates, no local residual/neural mapper. Use the already
validated primal backend through the unchanged `b1p_stage.cpu_fit`; this is a
declared numerical backend, not a post-test algorithm change. All other CPU
adapters and the paired neural worker remain frozen. LA2M has 20 source-anchor
clusters, n_init4 and the original singleton fallback. SimpleLinear uses pinned
official code, final50 epochs, batch4028 and its locked loss/defaults. Converter
uses the locked paper-spec adaptation: 50,000 selection iterations, batch64,
k100, paired validation MAE/earliest minimum, followed by a fresh selected-length
refit on all 1,024 anchors. Original papers' broader training settings are not
claimed reproduced. No final relevance labels select checkpoint or model.

## Inputs, identity and acquisition

`configs/b2_acquisition.json`, copied verbatim into the lock, pins corpus/query
HF revision7e16fde3016c639c7f856e803f4bab92645562c4, explicit Parquet paths,
file sizes and SHA256s. Preserve original Parquet row order; reject duplicate
or empty IDs. Documents use `(title + " " + text).strip()`, queries use the text
unchanged. This full-BEIR document composition is declared in advance; Nano
corpora had their own pinned text-only format.

All four model revisions, allowed paths and file SHA256s are copied from
`configs/b1m_lock.json`. Downloads are explicitly allowlisted; no implicit
hub access, remote code, label loader or unrestricted snapshot download is
permitted in acquisition/encoding. Model-native length settings are recorded
but overridden to the same B1-M maximum128 tokens for all four models.
Batch32, float32, normalized output, eval/inference mode, seed17, deterministic
Torch and disabled TF32 are fixed. Encoder runtime is separately installed with
SentenceTransformers4.1.0/Transformers4.51.3/Torch2.6.0+cu124/NumPy2.2.6;
it does not modify the baseline GPU runtime. Versions, module identities,
runtime install logs and all model/input/output hashes are retained.

Acquisition first verifies every raw file hash. Encoding writes unique outputs,
per-4,096-row flushed chunk journals, physical document/query encode counts,
timing/RSS/device/progress/failures and a completed encoding manifest. The
manifest binds the predeclared procedure and generated vector SHA256s before
any fitting. No changed revision, guessed missing cache, batch/precision/length
fallback or unverified embedding reuse is allowed.

The qrels source is pinned by metadata only: BeIR/trec-covid-qrels revision
532ac68ee6756ac22c9346eebf65bd3c6a042e10, `test.tsv`, 980,831 bytes, Git blob SHA1
9cb5167175d7cdbf9d85ea828c6a3da943fe7053. Upstream does not provide an LFS SHA256
for this small Git file; the scorer must verify `SHA1("blob <length>\0"+bytes)`
and record SHA256 before parsing. Acquisition/encoding never download qrels.

## Paid documents, fitting exposure and exact search

For each seed, use independent NumPy SeedSequence streams `[seed,0]` for
1,024 unique anchors and `[seed,1]` for a permutation of all document rows.
`select_for_budget` retains the frozen DEV rule: anchors plus earliest remaining
order rows to exactly floor(fraction*N), with nested sets. Each method and pair
uses the same ordered anchors and paid sets. Every fit sees only the 1,024
paired anchor vectors; paid nonanchors are not extra training examples.

Charge unique destination exposure as `|A union S|`, anchors included: 42,833,
85,666, 128,499 documents at the three budgets. Full-Y is 171,332, Full-X uses
the native incumbent query/document encoder. Full destination caches are
prepared for representation evaluation/reference access, not billed as fresh
partial-deployment encoding. Record physical corpus encoding separately;
no deployment dollar saving follows from these cache-based rankings.

Normalize proxies to unit float32 and replace exactly the paid rows by true
destination vectors. Queries use the destination encoder. Exact float32 inner
product, query batch16, top100; ties use ascending original document row index,
and identical query/document IDs are excluded. Full references use native
queries and documents. Keep every query, seed, budget and method.

## Held endpoints and pre-label verification

Serialize all184 **exact-search endpoints** using `b2_exact_endpoint_v1`:
native matrix or base proxy plus paid-index patch into a frozen destination
matrix, query vectors, ordered IDs, dimensions and explicit score/tie/exclusion
settings. Bind every referenced file by SHA256. A proxy is stored once per fit
and referenced across its three endpoint budgets. These reconstructable exact
endpoints are not approximate ANN or a measured serving deployment.

Seal all rankings, endpoint descriptors, parameters/fit receipts, ordered IDs,
selections, source/model/encoding identities and failures before labels. The
separate `ops/b2_verify.py` independently reloads and reconstructs every
endpoint, computes its float32 scores and stable top100, and compares all
ordered document IDs against the sealed rankings. It verifies exact prescribed
184-cell identities, complete hashes and named encoder bindings. Any mismatch
is preserved, fails verification and prohibits qrel access. An approximate
top-k agreement tolerance is not a gate for this exact claim.

## Separate one-shot final scoring and interpretation

Only after matching code/lock, all184 sealed rankings and the successful
separate verifier seal are unchanged may `ops/b2_score.py` request qrels. An
exclusive, fsynced first-final-opening receipt at the canonical run root is
written **before** the network request. A separate output alias cannot bypass
this receipt. Preserve source bytes, Git blob verification and SHA256, parsing
records, all raw per-query metrics, all means, seed SD/range and failures.

nDCG@10 is primary, with graded gain `2^rel-1`; Recall@100 is secondary with
all positive judgments in its denominator. Reject duplicate judgments and
nonfinite grades; include zero-positive queries as zeros. Unjudged documents
are nonrelevant. Do not filter queries based on method results or query/corpus
coverage.

Primary family is the **30** ARC2-minus-baseline nDCG contrasts: five external
configurations x two pairs x three budgets. Average five mapping seeds before
paired query resampling. Use 20,000 PCG64/default_rng draws, seed20261031, sharing
each query resample across every method, pair, budget and metric. Individual
percentile coverage is `1-0.05/30`, for approximate95% Bonferroni family coverage.
Recall intervals and condition mean intervals are nominal95% descriptive.
Store bootstrap outputs for reproducibility. There are 50 independent queries,
not250 independent observations from multiplying mapping seeds.

An interval strictly above0 supports improvement for that condition; strictly
below0 supports worse performance; crossing or touching0 is unresolved.
No post-hoc margin, noninferiority/equivalence declaration, cell filtering or
winner selection is permitted. All negative/unresolved outcomes remain in
tables/figures and ARIS interpretation. No second collection is selected to
rescue a failed claim, and independent second-step/all-paid necessity is not
silently added to this fixed-anchor test.

## Run order, resources and failures

Deploy a clean exact pre-run Git commit on Mini `.201:62161`, H100 MIG20GB.
Keep code/assets/outputs under `/home/jovyan/arc2_b2_20261031`; never move them
while input identities are cached. Existing CPU/GPU/upstream runtime paths
remain explicit in the lock. Do not change other jobs, MIG configuration,
priorities or cgroup quotas. Record shared load; shared execution time does
not establish isolated GPU performance. No artificial walltime, VRAM/RAM
headroom or restored120h cap is imposed.

Finite campaign order:

1. Allowlisted acquisition with all byte/hash checks.
2. Qrel-free encoder smoke, fixed first64 documents/eight queries, all models.
3. All-six-method synthetic CPU/GPU smoke: 2,048 synthetic documents, eight
   queries, 128 anchor pairs, one synthetic pair/seed17, all three budgets;
   20 rankings including two native references. Converter smoke500 iterations.
4. Separate smoke endpoint verification; distinct smoke status cannot release
   final labels.
5. Full qrel-free corpus encoding, then the complete60-fit/184-ranking run.
6. Separate full endpoint verifier, then one-shot final scorer.
7. Local computational verification, full result tables/figures and ARIS
   result-to-claim. No manuscript update.

Fresh directories only. Preserve failed smokes, interrupted workers, partial
checkpoints, manifests, stderr, resource traces and all negative evidence.
Actual OS/I/O/model-download/numerical failures stop the corresponding
campaign; no silent rerun, partial-matrix scoring or parameter fallback.
Infrastructure repair before labels needs recorded source/runtime identity
and a new matching smoke when code changes; final-label exposure cannot be
undone. A scorer failure after first opening remains an exposed failed
attempt and cannot be retried as a fresh independent confirmation.

Maintain incremental local backup of completed evidence to D, with whole-file
hashes and a separate terminal coverage receipt; mutable partial files are
never accepted as verified final evidence. Record corpus/model caches as
reproducible inputs, not model-fit provenance that can be guessed after reset.

**STOP after B2's verified results, figures and ARIS review. Leave manuscript
unchanged. No automatic B3/B4, new dataset, algorithm revision or retuning.**
