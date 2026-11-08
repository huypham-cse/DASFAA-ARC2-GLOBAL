# ARC2-Global experiment and paper plan

Date: 2026-10-25. Revision: 2 (scientific controls before systems spending).
Status: proposed finite roadmap, not an immutable execution
protocol. Fixed method: `arc2_global_tangent2_r1`. User selected MS MARCO
Documents **100K**. Notify the user before H100/scientific runs or claim audit.

Revision 2 makes tangent ablations, an unconstrained ridge baseline and a
FiQA all-paid-pairs comparison mandatory; specifies the random paid sets and
mixed-gallery diagnostics; predeclares uncertainty interpretation; and makes
systems experiments conditional on a written development/independent decision.
No algorithm, existing result, test exposure, or scientific protocol is changed.

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
   Include an unconstrained affine ridge map with an augmented bias coordinate,
   lambda=10 and the same normalization/paid sets. This is a mandatory standard
   mathematical baseline, not an old internal method or orthogonal map.
3. Neural converter: existing Embedding-Converter paper-spec anchor1024
   adaptation; retain its exact validation/refit policy. Distinguish this from
   official code and the original multi-corpus training regime. Verify losses,
   gradients and anchor/generalization diagnostics before using new results.

All six systems (ARC2-Global plus five external configurations) receive the
same documents, ordered anchor pairs, paid destination IDs, queries, seeds,
and exact tie rule. Main comparison uses fixed 1,024 fitting anchors; paid
backfill vectors only overwrite gallery rows, for every method. Therefore
claim fixed-anchor performance, not the best use of all available supervision.
The fixed-anchor comparison is accompanied by the mandatory all-paid-pairs
experiment below. Do not claim best use of the encoding budget from the
fixed-anchor table alone, or assume that a baseline may not reuse paid pairs.

### Paid-set construction for B1 and B2

For new collections, fix document row order independently of relevance. For
each seed, use separately seeded RNG streams for 1,024 uniformly sampled
anchors without replacement and a full random backfill permutation. Record
the RNG/stream rule, arrays and hashes in the pre-run protocol. Construct each
paid set by taking all anchors and then unseen IDs from the permutation until
floor(budget*N) IDs are reached. The 25/50/75% sets are nested and shared by
every system. Fitting/selection never uses qrels, target non-paid vectors,
query frequencies or judged-document oversampling. FiQA reuses its historical
ordered anchors and backfill permutation exactly; do not relabel that order as
new random sampling or replace it silently. B4's traffic-selected sets are a
separate declared policy experiment.

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
Compare all six systems at 25/50/75%, five seeds and two pairs; full-X/Y refs.
Report nDCG@10 (primary), Recall@100 (secondary), absolute deltas, full-Y retention,
and per-seed/per-query data. The A2M comparator isolates the added tangent
updates; no historical internal methods need enter the active paper matrix.
Representational results use exact search. Lock score arithmetic, row/ID tie
order, numerical environment and top-100 IDs; verify the serialized scorer on
synthetic ties before new rankings. Retain small Recall losses as well as nDCG gains.

Reuse the 60 compatible FiQA partial rankings and four full references already
imported; do not rerun them just to rename the method. New FiQA cells cover
75% and the three new baselines (LA2M, SimpleLinear and affine ridge).
Regenerate a complete condition only when model,
data, method or environment identity prevents fair reuse; retain its old result
and name the new measurement. No checkpoint/cluster tuning on TREC labels.

Success evidence: paired improvements against a credible alignment baseline in
more than a single development corner, with visible size and variability, and
an understandable operating tradeoff against neural fitting. A small or negative
effect narrows the result; it is reported, not deleted or repaired with final labels.
Figures: quality vs budget, paired deltas, encoder-dependent Recall tradeoffs.

#### B1-M: mandatory mechanism controls (development only)

Across the four development collections, both pairs, five seeds and all three
partial budgets, evaluate:

| Configuration | Purpose | Reuse |
|---|---|---|
| Procrustes, zero tangent steps | effect of adding tangent updates | main A2M row |
| one tangent step, lambda=10 | need for the second step | new named ablation |
| two steps, lambda=10 | fixed proposed method | main ARC2-Global row |
| two steps, lambda=1 | regularization sensitivity | new named ablation |
| two steps, lambda=100 | regularization sensitivity | new named ablation |
| unconstrained affine ridge, lambda=10 | angular refinement vs ordinary regression | main ridge row |

Only the three new ablation configurations add ranking cells. Share compatible
factorizations/fits across budgets and reuse the recorded one-step coefficient
where exact input/code/runtime identity permits it. Report quality, Recall,
fit time and RSS. These are explicitly labeled development ablations; no old
method implementations need be restored. The main ARC2-Global stays two steps,
lambda=10. If another configuration is better, report it; changing the proposed
method requires a separate named revision/decision, never silent selection or
an ablation sweep on TREC.

#### B1-P: mandatory all-paid-pairs check (FiQA DEV, 50% budget)

Use both encoder pairs, five seeds and the **same** 28,819 paid IDs already
defined by each seed's 50% set. For each of all six systems, fit using all
28,819 paid source/target pairs, then overwrite those same IDs with true
destination vectors. The corpus and query set do not change. Compare these
results with the corresponding six 1,024-anchor rows, including cross-regime
comparisons such as fixed-anchor ARC2-Global vs all-paid Procrustes/ridge.
This adds 60 rankings, not another dataset or a larger encoding budget.

For the learned methods, use all paid pairs in the final refit. Preserve the
validation/refit procedure through a separately named all-paid configuration:
fixed seeded 7/8 vs 1/8 pair split for converter selection, then final refit on
the entire paid set. Lock official SimpleLinear validation/refit and LA2M
cluster/routing rules in the development protocol before execution. No ranking
labels select checkpoints. Report both fixed-training-policy and data volume;
the all-paid converter is not the historical anchor1024 configuration.

Extra destination **encoding** is zero relative to that paid set, but fitting
is not free. Measure matrix construction/solve, training, mapping, RSS and
wall time. The current tangent solver forms an n-by-n float64 Gram matrix:
for n=28,819, that matrix alone is about 6.19 GiB before Cholesky/workspace.
Do not describe this experiment as negligible compute.

Develop and verify a separately identified primal/streaming solver backend if
needed: the ridge increment can be evaluated using
(X.T X + lambda I)^(-1) X.T T instead of X.T (X X.T + lambda I)^(-1) T.
Use a solve, not an explicit inverse, and preserve bias regularization,
initialization, tangent target, dtype and normalization conventions. The two
forms agree in exact arithmetic but may differ in floating point. Require
synthetic coefficient/proxy/ranking checks and measured drift against the
existing backend before use. Record a new backend implementation ID, all
tolerances and any non-identity; do not silently alter the frozen API or
retroactively call old results byte-identical. An unresolved solver issue is
reported and fixed before this mandatory check, not a reason to omit it.

#### B1-G: mandatory mixed-gallery diagnostics

For each pair/budget, report paid/proxy population shares, their shares in
returned top-10/top-100, predicted-vs-true score errors on a fixed development
diagnostic sample, and rank/metric changes before and after true-vector
replacement. Compare query-score distributions for paired representations of
the **same** sampled documents, since paid/proxy selection alone can confound
an apparent score bias. Reference vectors used by the isolated diagnostic
analyzer must not enter fit, paid-ID selection, ranking construction or cost.
Keep diagnostics descriptive: a returned-share imbalance alone is not proof
of miscalibration. No new score calibration is tuned into ARC2-Global here.

### Decision after B1: method evidence before systems work

Write a decision record covering B1-M, B1-P and B1-G before B2 and before any
24-deployment campaign. Three outcomes are allowed:

| Outcome | Evidence | Next action |
|---|---|---|
| GO-C1 | tangent improves quality in a reproducible declared encoder/condition scope, or reaches a declared quality target with lower measured fitting cost; the all-paid comparison does not reduce the argument to withheld baseline supervision | freeze that scope and run B2 once; B3/B4 still conditional |
| CONFIRMATION-ONLY | favorable development estimates remain statistically unresolved; no demonstrated harm or decisive all-paid failure, and the independent test can answer the fixed question | B2 only; no systems campaign until its result is interpreted |
| NO-GO-FOR-SYSTEMS | Procrustes/ridge with all paid pairs matches or beats the proposed method and no distinct quality/fit-cost advantage remains, or mechanism controls undermine the contribution | keep TREC closed and stop expansion; report the development finding and revise the research direction |

The execution protocol must fix any practical quality/noninferiority margin,
aggregation weights, encoder-specific scope and cost comparison before running
new B1 cells. Existing FiQA exposure is disclosed. A CI containing zero alone
is inconclusive, not automatic proof of failure or equivalence. A migration-cost
story is an alternative only if it has a distinct, testable systems contribution;
partial backfill being cheaper than full rebuild is insufficient by itself.
These decisions route research work; they do not kill an active job or reinstate
elapsed-time/resource caps. Do not run B3/B4 simply because they were listed.

### B2 — one prospective TREC-COVID confirmation (must-run, no retuning)

After development decisions are final, commit one immutable protocol containing
all dataset/model/code/file hashes, all six systems, two pairs, five seeds,
25/50/75% budgets, full refs, tie rules, metrics, bootstrap draws/seed and fixed
comparison family. Primary family: ARC2-Global minus each of five external
methods over two pairs and three budgets (30 nDCG contrasts); report simultaneous
95% paired query intervals with five-seed averaging, plus seed sensitivity and
descriptive Recall. No universal-win admission threshold or silent method switch.

Predeclare interpretation of every contrast: an interval entirely above zero
supports improvement in that condition; entirely below zero supports worse
performance; an interval crossing or touching zero is unresolved. Do not call
the latter a win, loss or equivalence. Noninferiority/equivalence needs a
scientifically justified margin fixed before opening labels and its own stated
test; absence of significance is not that test. Report effect sizes, interval
widths and the 50-query limitation. Five mapping seeds do not create 250
independent test queries. No new independent collection is added after seeing
TREC outcomes to recover a preferred verdict; any extra confirmation requires
a separate prospective exposure check/protocol.

Ridge is newly mandatory in the main table, so the primary family increases
from 24 to **30** contrasts. This change occurs before TREC execution/labels,
not after a failed significance test. Development-only step/lambda ablations
and all-paid sensitivity are outside this independent contrast family. The
independent claim is explicitly limited to the fixed-anchor regime unless a
future preregistered independent all-paid check is added before label access.

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

### B3 — physical migration cost and serving (conditional on C2 admission, H100)

Admission: finish B1's decision and interpret B2 first. Proceed only with a
specific remaining C2 hypothesis and a development-frozen quality/cost target
that can distinguish ARC2-Global from the strongest relevant comparator. If B2
is unresolved, a bounded descriptive case study is possible only with an
explicit recorded rationale, not a new independent quality claim. If there is
no method-specific or systems contribution worth testing, do not spend the
36 nominal server-hours. Notify the user of the chosen route before launch.

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

### B4 — held-out traffic benefit and paper closure (conditional on C2 route)

Run only if B1/B2 and the C2 decision justify the traffic question. Retaining a
traffic-driven benefit claim requires this evidence; a mapper-focused paper
does not automatically require the traffic campaign.

On the same 100K corpus, compare random, static query-frequency priority and
the fixed coverage scheduler with the same ARC2-Global proxy and paid budgets.
Use five mapping seeds, two pairs, 25/50/75% snapshots; split traffic by query ID
before deriving the policy. Primary metric: held-out traffic-weighted agreement
with full-Y top-10; report unweighted agreement and coverage of the log as well.
This is a ranking-agreement **proxy**, not judged relevance. Where applicable
judged qrels exist for the sampled corpus/query population, also report
nDCG@10/Recall and judged coverage without filtering out queries based on method
outcomes. Otherwise label the metric as agreement throughout paper/figures;
click-derived evaluations are reported separately from human relevance labels.
ORCAS lacks timestamps: this is held-out click-log replay, not chronological
or live-production traffic. Cached replay is quality/scheduler evidence only,
not a fresh physical-cost measurement. No new mapper or scheduler tuning here.

If traffic priority gives no benefit, report it and use a migration/quality-cost
title without a traffic-driven superiority claim. AOL-IA/chronological replay
and 1M docs are optional future work, not required to close this paper.

## Matrix and compute accounting

Main retrieval maximum: 5 collections * 2 pairs * 5 seeds * 3 partial budgets *
6 systems = **900 partial rankings**, plus **20 full references**, total **920**.
The imported FiQA 60 partial +4 refs can satisfy 64 of these; **856 additional
main ranking cells** remain if all identities pass compatibility checks.

Mandatory development extras, with zero-step, two-step lambda10 and ridge rows
already counted in the main matrix:
- Three extra step/lambda controls *4 DEV collections *2 pairs *5 seeds *3
  budgets = **360 extra rankings**.
- All-paid at FiQA 50%: six systems *2 pairs *5 seeds = **60 extra rankings**.
- Mixed-gallery diagnostics reuse the fixed rankings/samples; no additional
  scientific ranking cells are assumed for the declared descriptive analyses.

Maximum with B2 admitted: **1,340 rankings**, of which 64 already imported,
thus **1,276 additional cells**. Before the B1 decision/TREC opening: four DEV
main collections give 720 partial +16 references; plus 420 DEV extras = **1,156
cells**, with 64 imported, at most **1,092 new DEV cells**. TREC contributes
180 partial +4 references = **184** cells only if the route admits B2.

The main matrix represents 300 method/collection/pair/seed fits; 30 compatible
FiQA fits are represented by the imported rankings. Extra ablations represent
120 configuration fits and all-paid represents 60 fits; shared factors and
one-step coefficients may avoid physical re-fitting. Do not count each budget
as another MLP fit. About 40 new fixed-anchor converter workers plus **10
all-paid converter workers** remain if the ten existing FiQA workers are
verified/reusable. Data/model/backend differences can prevent reuse; report
that and never substitute an unverified cached model.

Do not promise a precise H100 duration now. The completed earlier development
run took ~4h27m with seven fresh converter fits plus overhead/reused workers on
a shared server. The old **1-3 days** for retrieval was an unmeasured planning
estimate; the new mandatory all-paid learned fits and solver work add cost, so
it is not a validated ETA for revision 2. Profile stage costs during smoke, and
give an updated forecast before the full DEV comparison. Systems work is now
conditional, with **36h nominal observation only if admitted**,
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
3. Complete B1 including mandatory 0/1/2-step/lambda/ridge controls, FiQA all-paid
   comparison and mixed-gallery diagnostics. Do the cheap algebraic controls
   first, then learned all-paid fits and remaining DEV breadth. Record the B1
   decision; keep TREC closed if NO-GO. Freeze method/scope and case selection.
4. If admitted, commit B2 and predeclare its interval interpretations. Prepare
   only the qrel-free endpoint verification needed for that independent claim;
   verify/reload intended held-index endpoints, seal all rankings, score once.
   No full 24-deployment campaign is required merely to open the test labels.
5. After interpreting B2, record C2 admission. Only then implement/finish the
   physical deployment runner, failure tests and short actual-method smoke
   under a separate committed protocol; if justified, run B3/B4 and retain all
   failures/shared-load traces. No automatic systems run on an inconclusive test.
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

The initial scope is B0 plus B1's fixed matrix and mandatory scientific controls.
Its recorded decision determines whether the sealed B2 test and then B3/B4 are
worth doing. A mapper-focused route ends with admitted B1/B2 evidence and paper
audit; the systems route additionally needs the 100K physical case study and
held-out replay. A NO-GO route ends with an honest report/decision and no automatic
new campaign. All completed negative results remain visible. Optional appendix ideas do
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
