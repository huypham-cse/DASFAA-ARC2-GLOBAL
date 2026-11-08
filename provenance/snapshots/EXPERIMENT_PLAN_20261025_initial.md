# ARC2-Global experiment and paper plan

Date: 2026-10-25. Status: proposed finite roadmap, not an immutable execution
protocol. Fixed method: `arc2_global_tangent2_r1`. User selected MS MARCO
Documents **100K**. Notify the user before H100/scientific runs or claim audit.

## Problem and claim map

Problem: upgrade independently trained retrieval encoders when full corpus
re-encoding is expensive; measure when forward proxies plus partial backfill
offer a useful operating point and when keeping the incumbent is better.

Method thesis: start from a centered rectangular Procrustes map, refine its
angular direction with two closed-form tangent ridge updates, and serve one
target-space gallery where paid true vectors replace proxies.

| Claim | Minimum evidence | Current status |
|---|---|---|
| C1: ARC2-Global is a useful simple non-neural mapper at matched encoding budgets | exact mixed-index retrieval vs credible external methods, matched anchors/IDs/seeds, retained failures, independent TREC confirmation | descriptive FiQA means only; favorable nDCG, mixed Recall |
| C2: it offers a practical quality/cost migration operating point under specified workload conditions | fresh physical deployment accounting and held-out ORCAS backfill comparison vs full rebuild/dual index/incumbent and a strong external mapper | unmeasured |

Anti-claims to rule out: extra paid anchors; hidden cached encoding savings;
weak or misnamed baselines; wins caused by fewer candidate documents; reporting
only favorable encoders/budgets; treating Nano scores as full BEIR results.
No universal dominance, production-SLO guarantee, zero-downtime theorem, or
novel scheduler claim. Strong paper wording depends on observed results, not
the ideal draft's numbers. More GPU hours alone do not prove novelty.

## Fixed scope

| Collection | Docs | Queries | Exposure / use |
|---|---:|---:|---|
| NanoNQ | 5,035 | 50 | development by default; no independent label |
| NanoHotpotQA | 5,090 | 50 | development; earlier Nano conditions inspected |
| NanoFEVER | 4,996 | 50 | development; earlier Nano conditions inspected |
| FiQA | 57,638 | existing 500 DEV | inspected; reuse compatible existing cells |
| TREC-COVID | 171,332 | 50 | user attested uninspected; keep labels closed |
| MS MARCO Documents v1 subset | 100,000 | ID/log preparation determines count | systems study with ORCAS |
| **Total** | **344,091** | | 244,091 retrieval + 100,000 systems |

Datasets are evaluation collections, not algorithms. No additional datasets,
encoder sweeps, custom Medium variants or 1M run are required by this plan.
The Nano corpora are published smaller retrieval tasks; they cannot establish
full-collection performance. TREC has only 50 queries: report uncertainty.

Pairs remain MiniLM-L6-v2 -> all-distilroberta-v1 (384->768) and e5-small-v2 ->
e5-base-v2 (384->768). Pin exact revisions, tokenizer/pooling, query/document
prefixes, text construction, truncation, precision and normalization before
execution; copy the old settings only where input/model hashes match. E5 prompt
handling and pooling are explicit checks. Do not silently change MiniLM's target
to MPNet from the historical draft.

Method constants: lambda=10, two tangent steps, no local correction; 1,024
anchors; seeds 17,29,41,53,67. Destination budgets 25%,50%,75%, plus full-Y
100% as one reference per pair (identical gallery need not be rerun per method).
The 25% NanoFEVER budget is floor(.25*4996)=1,249, so all 1,024 anchors fit.
Anchors count; never call an anchor-only fit zero total encoding cost.

## External baseline registry

Three families, with explicit adaptations:

1. Alignment: A2M / centered Procrustes, and actual clustered LA2M from the
   pinned authors' implementation. LA2M is per-cluster Procrustes, not the
   earlier Procrustes+local8 matched control. Fix cluster count/routing/fallback
   using published guidance or development-only selection before TREC.
2. Simple learned map: official-code SimpleLinear, pinned upstream revision,
   documented architecture/loss/training/selection. No old score imported under
   a different encoder or API. It is a baseline, not an independent test dataset.
3. Neural converter: existing Embedding-Converter paper-spec anchor1024
   adaptation; retain its exact validation/refit policy. Distinguish this from
   official code and the original multi-corpus training regime. Verify losses,
   gradients and anchor/generalization diagnostics before using new results.

All five systems (ARC2-Global plus four external configurations) receive the
same documents, ordered anchor pairs, paid destination IDs, queries, seeds,
and exact tie rule. Main comparison uses fixed 1,024 fitting anchors; paid
backfill vectors only overwrite gallery rows, for every method. Therefore
claim fixed-anchor performance, not the best use of all available supervision.
Run a single 50%-budget sensitivity where all paid pairs are offered to every
mapper only if the fixed-anchor restriction becomes a decisive reviewer issue;
it is appendix/optional, not a precondition for the core story.

Full-X and full-Y are always visible references. No method gets hidden full-Y
vectors in fit, routing, selection, threshold calibration or scheduler decisions.

## Five experiment blocks

### B0 — package and numerical identity (local, current task)

Extract the existing global path only; retain selected raw rows, original seals
and source hashes. Verify exact coefficient/proxy/mixed-gallery parity on
synthetic same/cross dimensions and copied-result arithmetic. Reuse the LNCS
template/bibliography/section layout, never old placeholder values. No scientific
benchmark or GPU run. Output: clean code, measured report, compact paper scaffold.

### B1 — exact retrieval breadth and mechanism (must-run, H100 after notification)

Claim: C1. Run NanoNQ, NanoHotpotQA, NanoFEVER, FiQA DEV, leaving TREC closed.
Compare all five systems at 25/50/75%, five seeds and two pairs; full-X/Y refs.
Report nDCG@10 (primary), Recall@100 (secondary), absolute deltas, full-Y retention,
and per-seed/per-query data. The A2M comparator isolates the added tangent
updates; no historical internal methods need enter the active paper matrix.
Representational results use exact search. Lock score arithmetic, row/ID tie
order, numerical environment and top-100 IDs; verify the serialized scorer on
synthetic ties before new rankings. Retain small Recall losses as well as nDCG gains.

Reuse the 60 compatible FiQA partial rankings and four full references already
imported; do not rerun them just to rename the method. New FiQA cells cover
75% and the two new baselines. Regenerate a complete condition only when model,
data, method or environment identity prevents fair reuse; retain its old result
and name the new measurement. No checkpoint/cluster tuning on TREC labels.

Success evidence: paired improvements against a credible alignment baseline in
more than a single development corner, with visible size and variability, and
an understandable operating tradeoff against neural fitting. A small or negative
effect narrows the result; it is reported, not deleted or repaired with final labels.
Figures: quality vs budget, paired deltas, encoder-dependent Recall tradeoffs.

### B2 — one prospective TREC-COVID confirmation (must-run, no retuning)

After development decisions are final, commit one immutable protocol containing
all dataset/model/code/file hashes, all five systems, two pairs, five seeds,
25/50/75% budgets, full refs, tie rules, metrics, bootstrap draws/seed and fixed
comparison family. Primary family: ARC2-Global minus each of four external
methods over two pairs and three budgets (24 nDCG contrasts); report simultaneous
95% paired query intervals with five-seed averaging, plus seed sensitivity and
descriptive Recall. No universal-win admission threshold or silent method switch.

Before first TREC label opening, generate and seal **all** intended rankings and
serialize/hash every intended held-index ANN endpoint. A separate qrel-free
verifier checks IDs, settings, retrieval/tie rules, reload behavior and top-k
agreement against their sealed reference. Preserve all mismatches. ANN agreement
is not a replacement for representation-quality evidence.

A separate scorer accepts only sealed unchanged inputs, logs first label access
and scores once. No qrels are copied into this package. The pre-existing exposure
attestation is provenance, not permission to skip the new protocol. Subsequent
debugging may fix infrastructure, but after label access any method adjustment
becomes development and cannot reuse this collection as a fresh confirmation.
Output: independent results table, all contrasts, failures and claim scope.

### B3 — physical migration cost and serving (must-run for C2, H100)

Corpus: deterministic 100,000-document subset of MS MARCO Documents v1, with
ORCAS IDs mapped to that document corpus. Do not substitute NanoMSMARCO passages.
Freeze ID-based document sampling before loading judged results. Prepare/split
ORCAS by normalized query string into scheduling and held-out halves; remove
overlap with other evaluation queries. Publish surviving docs/queries/click
pairs; do not assume the full ORCAS counts remain after filtering.

Use two fixed pairs and one 25% destination budget (25,000 unique docs, including
1,024 anchors). Compare four deployment strategies: ARC2-Global, one strongest
eligible external mapper, full rebuild and dual index. External mapper choice
is locked from development aggregate nDCG/full-Y retention across B1 collections,
pairs and budgets, with lower fit complexity breaking ties; never use TREC or
systems outcomes to pick it. Keep the incumbent X service as a visible reference
and available until a verified cutover. If the method cannot meet the fixed
quality target, keep incumbent service and record no eligible cutover.

Three paired randomized blocks per encoder, all four strategies in each block:
24 fresh deployments total. Every deployment physically encodes its own unique
destination set once, anchors included, fits/maps proxies, builds its own index,
verifies it and then cuts over atomically when eligible. Full rebuild physically
encodes all 100K. Count duplicate work, retries, failed attempts, index writes,
model loading, mapping, fitting, search service, CPU/GPU seconds, RAM-byte-seconds,
storage-byte-seconds, I/O and transferred bytes. A full-vector scientific cache
is not billable physical deployment work. Separate old-index sunk cost from
new migration cost; include new queries for all applicable service strategies.

Scientific observation schedule: D=60 min migration checkpoint, H=90 min workload
window. These are measurement checkpoints, not automatic process kill caps.
If build/encode exceeds a checkpoint, report failure-to-cut-over there and
continue preserving work to completion unless an actual host/runtime failure
occurs. Predeclare endpoint quality eligibility and a labeled **experimental**
latency/error target before trials using a separate calibration workload; no
claim these targets are a real user's contractual SLO. No arbitrary free-VRAM,
RAM or elapsed-time admission rejection is reintroduced.

Use open-loop scheduled arrivals (record scheduled arrival, enqueue, start and
finish; unfinished/error requests remain in denominators) to avoid coordinated
omission. Record raw latencies, queue, errors, endpoint identity, cutover events
and continuous CPU/GPU/shared-load traces. Shared load does not force endless
waiting: run with telemetry, keep contaminated attempts, analyze paired loaded
conditions separately from isolated performance. Capture pre-block machine
state; do not kill other users' jobs. Include synthetic failures for encoding,
fit, index creation/reload, query exceptions, interrupted cutover and signals.

Nominal observation work is 24*90min = **36 server-hours**, plus preparation,
calibration and any unfinished deployment work. This is a workload estimate,
not a GPU-compute bill, guarantee, deadline, or restored 120h cap. Measure cost
units first; apply explicit rates only if supplied/verified and label scenarios.
Output: component-time breakdown, cost vs achieved quality, p50/p95/p99,
errors/queue and cutover timeline, with all three trials rather than best trial.

### B4 — held-out traffic benefit and paper closure (bounded, must-run if traffic-driven title)

On the same 100K corpus, compare random, static query-frequency priority and
the fixed coverage scheduler with the same ARC2-Global proxy and paid budgets.
Use five mapping seeds, two pairs, 25/50/75% snapshots; split traffic by query ID
before deriving the policy. Primary metric: held-out traffic-weighted agreement
with full-Y top-10; report unweighted agreement and coverage of the log as well.
ORCAS lacks timestamps: this is held-out click-log replay, not chronological
or live-production traffic. Cached replay is quality/scheduler evidence only,
not a fresh physical-cost measurement. No new mapper or scheduler tuning here.

If traffic priority gives no benefit, report it and use a migration/quality-cost
title without a traffic-driven superiority claim. AOL-IA/chronological replay
and 1M docs are optional future work, not required to close this paper.

## Matrix and compute accounting

Main retrieval maximum: 5 collections * 2 pairs * 5 seeds * 3 partial budgets *
5 systems = **750 partial rankings**, plus **20 full references**, total **770**.
The imported FiQA 60 partial +4 refs can satisfy 64 of these; **706 additional
ranking cells** remain if all inputs/environments pass compatibility checks.
This is not 706 independent MLP fits: one fit is reused over three budgets.
At most 250 method/collection/pair/seed fits, 30 compatible fits represented by
the imported FiQA cells. About 40 new converter selection/refit workers remain
if all original ten FiQA workers are verified and reused; data/pair/baseline
differences may prevent reuse and must be recorded, never guessed.

Do not promise a precise H100 duration now. The completed earlier development
run took ~4h27m with seven fresh converter fits plus overhead/reused workers on
a shared server, so use a conservative planning envelope of **1-3 days for
retrieval preparation/comparisons**, then **36h nominal systems observation**,
plus measured replay/render/write time. These are provisional estimates, not
new measurements or stop limits. Replace them with a stage-wise ETA after smoke
measures corpus encoding, one learned fit and one endpoint build. Peak load,
text length, compilation and downloads can materially alter time.

Report hardware utilization separately from elapsed server time. Existing FiQA
vectors may be reused only on matching hashes/revisions; fresh physical trials
never charge the cache as new encoding. No heavy corpus/model/embedding files
are copied to the laptop as part of this package. H100 runners are future code,
not implemented or launched by the roadmap.

## End-to-end execution and writing order

1. **Now:** finish B0, build this development paper scaffold and report paths to
   user. STOP before H100/scoring/audit as requested.
2. **After notification:** write/commit exact data/source/environment protocols;
   implement only external adapters, sealed exact runner and separate scorer;
   H100 qrel-free input preparation/smoke. Check E5 prompts and actual LA2M.
3. Complete B1 development table; freeze baselines and planned case selection.
   Develop deployment runner/failure checks and intended held-index endpoints
   qrel-free; write/commit distinct actual-method smoke protocol and pass it.
4. Commit B2 independent protocol; generate all TREC rankings/endpoints, verify,
   seal, score once. No method tuning after this. Report positive and negative.
5. Run the fixed B3 physical paired case study and B4 held-out scheduler replay;
   retain shared-load traces, failed attempts and identity receipts.
6. Generate all tables/figures from raw files: mechanism, quality-budget, paired
   deltas, physical cost breakdown/Pareto, traffic/cutover timeline. Include a
   when-to-use/not-use analysis from measured tradeoffs and failure conditions.
7. Write the final paper using the reused LNCS structure. Method explains the
   actual tangent update; related work compares mechanisms and assumptions;
   experiments distinguish DEV/independent/physical replay. Replace provisional
   abstract/title only with supported findings. Verify citations/venue rules.
8. Notify the user before ARIS result-to-claim and paper-claim-audit. Then give a
   fresh reviewer only paper + raw numeric evidence for number/scope audit;
   retain review independence/status truthfully. Fix prose/data plumbing, not
   test performance. Compile/render/check layout, references and reproducibility.
9. Freeze paper/code/data manifests and release instructions. No extra benchmark
   campaign unless an audit identifies a concrete unresolved issue or user asks.

## Completion criteria and fallback

Core research ends when the fixed retrieval matrix, one sealed independent test,
one 100K physical case study and held-out traffic replay are reported, including
negative results, and paper claims match evidence. Optional appendix ideas do
not keep the project open indefinitely. Failure to demonstrate C2 leads to a
mapper-focused paper with C2 removed, not invented cost/SLO or automatic reruns.
Failure on independent C1 is reported and changes framing; it does not authorize
silently redefining the algorithm or harvesting another untouched test.

Paper acceptance cannot be promised. The highest risks are incremental novelty,
small E5 gains, limited Nano query counts, few training anchors for a large MLP,
and loaded-server cost interpretation. The plan addresses these through a
correct strong baseline, independent uncertainty, explicit assumptions and
physical accounting, rather than adding datasets without a purpose.

## Source links and reuse

- [Published Nano datasets](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)
- [BEIR](https://github.com/beir-cellar/beir)
- [MS MARCO Documents v1](https://github.com/microsoft/msmarco/blob/master/Datasets.md)
- [ORCAS](https://microsoft.github.io/msmarco/ORCAS.html)
- [Alignment and SimpleLinear source](https://github.com/DBgroup-Edinburgh/embedding-translation)
- [Embedding-Converter paper](https://aclanthology.org/2025.acl-long.1237/)

The previous draft provides organization and references, not numerical evidence
or a requirement to implement its unused regional/calibration mechanisms. The
active method remains ARC2-Global. Historical literature notes/reviews remain
in the archive; verify before citation. No new ARIS claim audit was run here.
