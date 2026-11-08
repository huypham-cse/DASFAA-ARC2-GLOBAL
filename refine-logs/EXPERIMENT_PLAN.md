# ARC2-Global experiment and paper plan

<!-- B2_CURRENT_BEGIN -->
1 November 2026: **B2 COMPLETE**, all 184rankings/60fits, endpoint replay before labels, FINAL_SCORED03:12:54+07. Local QA PASS (results\b2_review_20261101\qa_completed_20261101T020214554697Z.json); all 1,138 compact files/181,895,786bytes verified. Primary family: 11 positive / 19 unresolved / 0 negative; all 6 Procrustes point differences negative, all Procrustes/LA2M family intervals unresolved. ARIS claim_supported=partial, same-family/provisional. Complete report/figures at results/b2_review_20261101; root REPORT/CLAIMS current. Backup: 1,330 files / 58,977,150,839 bytes complete 03:16:10+07, zero pending; no owned remote B2 job remains. Manuscript: 20 files unchanged. STOP before manuscript changes, B3/B4, retuning or new datasets. Earlier execution entries below are historical.
<!-- B2_CURRENT_END -->

Date: 2026-10-25. Revision: 2 (scientific controls before systems spending).
Status: proposed finite roadmap, not an immutable execution
protocol. Fixed method: `arc2_global_tangent2_r1`. User selected MS MARCO
Documents **100K**. Notify the user before H100/scientific runs or claim audit.

Liveexecution31Oct13:57+07: B2started onMini.201 underpre-run26feef1,
all61sourcepinsandlockverified. Acquisition,4encodersmoke,6methodsmoke20cells
andseparateendpointsmokePASS. FullTREC-COVIDencodingrunning; firstmodel106496/
171332docs. Labelsclosed. Frozen60fits/184rankings andseparateverifier/one-shot
scorer followautomatically; thenlocalQA/figures/ARIS, STOP. Manuscriptunchanged.
See singletracker andprovenance/qa/b2_r1_startup_verified_20261031.json.

Executionrelease31Oct2026: user authorized B2 through independentresults,
verification,figures andARISreview, excludingmanuscriptupdates. Thecompleted
B1c/D1 STOP below is released forB2only. Use the new immutable
B2_TREC_COVID_CONFIRMATION_20261031.md andconfigs/b2_lock.json;
184rankings/60fits/30primarycontrasts. No extra dataset/method/systems.
CurrentpreparationPASS:27synthetictests,61sourcepins,pre-runreview002samefamily
provisional. Commitbeforeanyscience; qrelsremaincloseduntilall184rankingsand
separateendpointverificationPASS. STOPafterB2review, manuscriptunchanged.

Current31Oct2026: **B1c-R3 COMPLETE**,358newrankings sealed+736cells DEVscored,
local metric/bootstrapverificationPASS, complete six-methodreport andthreefigures
visualQA PASS. ARISfinalD1 narrowGO-C1 for plannedfixed1024confirmation only;
overallpartial/samefamilyprovisional, systemsnotadmitted. Preserve original320/R2
interruptedattempts and38displacedhistoricalFiQAcells. Currentmainmatrix736=
378retained+358new;118fresh+2savedfits. No method/scoringchanges afterlabels.
**STOPbeforeB2/TREC/systems** until user reviews. The next finite scientificitem,
ifreleased, is existingB2:184rankings/30contrasts under a newimmutableprotocol;
then interpret, integrate/write mapperpaper and audit. B3/B4 conditional.
[Currentreport](../REPORT.md), [sixmethodfigures/tables](../results/b1c_r3_review_20261031/SUMMARY.md),
[finalD1](../CLAIMS_FROM_RESULTS.md). CurrentcampaignoutputbackupCOMPLETE13:05+07,64.48GB/2484files,0pending;
see provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json (relative to root).

Revision 2 makes tangent ablations, an unconstrained ridge baseline and a
FiQA all-paid-pairs comparison mandatory; specifies the random paid sets and
mixed-gallery diagnostics; predeclares uncertainty interpretation; and makes
systems experiments conditional on a written development/independent decision.
No algorithm, existing result, test exposure, or scientific protocol is changed.

Execution update27Oct2026: B1-M, B1-P0 and B1-P complete. All124 B1-P rankings
are scored/locally verified; original failed scoring attempt is preserved with
separate successful recovery. See the single live tracker and
results/b1p_r5_review_20261027/SUMMARY.md. The user released the B1-P STOP for
finite B1-G diagnostics and ARIS/D1 interpretation on27Oct. B1-G protocol/code
515b3d10 was committed before execution; both full shards and separate DEV
scoring passed. Local QA verified210galleries/450cases/90conditions with zero
discrepancy; figure QA passed. ARIS is partial overall and recommends narrow
GO-C1 for the frozen fixed-supervision quality question only, no systems
admission. REPORT.md and CLAIMS_FROM_RESULTS.md record the current evidence.
STOP for user review before remaining breadth/TREC/systems or formal claim audit.
Roadmap scope is unchanged; no later scientific phase has started.

Execution authorization28Oct2026: the user released B1c preparation, matching
smoke and exactly320 missing DEV rankings, separate scoring/report/final D1.
The immutable execution protocol is B1C_MAIN_MATRIX_COMPLETION_20261028.md;
its pre-run commit must precede smoke. Execution committed585b8b8; R1 runtime
amendment74c6a75 selects MINI20GB, deployment snapshot19f3f0e. Both MAIN and
MINI matching synthetic smokes passed, but only MINI is queued for full after
its required453-file transfer and final source hash verification. See tracker.
Historical review STOPs above remain
provenance; current STOP is after B1c/report/final D1 and before B2. No method,
dataset, all-paid regime or systems expansion is authorized by this release.

## Current critical path after the 27 October file review

This clarification preserves revision2's datasets, methods, budgets and maximum
cell count. It does not authorize a scientific launch. B1-M/P0/P/G are complete,
at that checkpoint **B1c was416/736 main DEVcells**. R3 now completes the same736-cell matrix with378retained+358new, preserving38displaced historicalcells. FinalD1 has been refreshed; the former breadthgap is closed. The next scientificphase remainsB2 only afteruserrelease.

| Order | Work and finite deliverable | Current state |
|---|---|---|
| 1 | Correct stale navigation and report regeneration; verify preservation on temporary copies | DONE in this file review; live report/raw evidence unchanged |
| 2 | Complete the locked six-method DEV matrix, preserving interrupted attempts | COMPLETE31Oct via prospective R3:358new+378retained=736scored; localQA PASS. Original320/R2 interrupted,38historicalcells preserved |
| 3 | Update six-method comparison, curves and final D1 from complete B1c+M/P/G | COMPLETE31Oct; every encoder/budget/sign retained; narrowGO-C1 recommendation, STOPforuserreview |
| 4 | If admitted, freeze and execute B2's existing184 rankings/30 external-baseline contrasts; separate scorer after seals | CONDITIONAL; TREC labels closed |
| 5 | Interpret B2, write the mapper-focused paper, review claims/citations, compile/render and freeze release | Finite paper closure; formal claim audit needs its planned notification |
| 6 | B3/B4 only if a later D2 supports a distinct, testable C2 contribution | CONDITIONAL, not required to close the mapper paper |

### Historical deficit before R3 (now completed)

| Collection / methods | Missing rankings | Fitting work |
|---|---:|---|
| NanoNQ, NanoHotpotQA, NanoFEVER: LA2M, SimpleLinear, converter; two pairs, five seeds,25/50/75% |270|90 method fits, each shared across its three budgets |
| FiQA: LA2M and SimpleLinear at25/75% |40|20 fixed1024 fitted galleries already have saved artifacts and50% parity evidence |
| FiQA: converter at75% |10|10 fixed1024 pristine proxy galleries already have saved artifacts and50% parity evidence |
| **Total** |**320**|**90 potential new Nano fits;30 FiQA fit artifacts with a reuse path** |

These are the missing cells in the existing matrix, not320 new training jobs.
The local index inventory verifies416 existing main identities,320 missing
identities and no conflicting hashes for duplicate identities. FiQA reuse is
conditional on checking the actual source files, model/input/order/parameter
identity and committed runtime; new25/75 rankings have not yet been generated.
All-paid fits are not substitutes for the fixed1024 regime. No existing ranking
needs rerunning solely for completeness or renaming. Record new fit/map/RSS and
shared-load observations; reused work has historical timing, not zero-cost fitting.

The bounded historical metadata check also found older NanoHotpotQA/NanoFEVER
results in MixIndex's `u1_six_task_replay/u1_r1_full_20261019T2236` and
`e4_nanobeir_breadth/e4_full_20261018T072414`. These are inventory leads, not
newly accepted reuse: LA2M4 differs from the current LA2M20 and the inspected
vector hashes/runtime differ; matching ordered anchors is unverified. Old
SimpleLinear is a lead for the source inventory. No matching local NanoNQ/E5/
converter cache was established; absence locally does not establish absence
on a server. Keep90 as potential new Nano method fits until that inventory.

After B1c: completed unique planned quality cells become1156 =836+320.
If B2 is admitted,184 further cells reach the unchanged maximum1340.
B1-G's diagnostic counterfactuals are separately counted, not added to this matrix.
Measure an ETA from the relevant smoke/first worker before promising a duration;
old all-paid timings are not a validated estimate for these Nano fits.

Execute the planned cells in three finite chunks: first the50 FiQA endpoints
with verified reuse, then180 Nano LA2M/SimpleLinear rankings (up to60 fits),
then90 Nano converter rankings (up to30 fit workers with selection/refit).
This order produces useful tables early without changing the matrix, training
policies or final decision point. One fit worker is not one gradient update.

### Improvements to make with the evidence already available

- **Align the paper with the real question.** Given a required destination-space
  migration, measure retained fixed-target retrieval quality at a matched paid
  document budget. Motivate compatibility requirements as scenarios/assumptions
  unless actually supplied or measured. All24 fixed1024 ARC2 partial mean nDCGs
  are below both native references in the current DEV matrix. Full-Y is lower
  than Full-X on both NanoHotpotQA/NanoFEVER encoder pairs. Therefore neither
  an immediate cutover-quality win nor a uniform quality-upgrade claim is supported.
  Full-X uses its native query encoder; it is operational context, not a mapper
  under the same target-query condition. Full-Y is a reference, not an upper bound.
- **Integrate completed evidence into the manuscript.** The current scaffold
  still describes only the imported FiQA subset, calls learned baselines future
  work and omits the new mechanism/all-paid/mixed-gallery studies. Use generated
  tables and the existing figures; distinguish the complete M/P/G controls from
  pending B1c breadth. Retain E5/Recall losses and the unresolved MiniLM ridge
  comparison. Write the existing evidence sections while B1c executes, then add
  its table and the independent section after their results exist.
- **Explain the tangent update rather than claim an unproved theorem.** For
  a nonzero prediction z with direction u and norm r, normalization has Jacobian
  J=(I-uu^T)/r. The current target t=r(I-uu^T)y satisfies Jt=(I-uu^T)y. This is
  local geometric intuition for an angular correction; global ridge projection
  and a finite update do not guarantee monotone ranking, cosine improvement on
  every example, or convergence. Numerical source and two-step/lambda10 identity stay fixed.
- **Make efficiency comparisons specific.** For 384 source and 768 target dimensions the final
  ARC2 affine coefficient has 295,680 float32 entries, about 1.128 MiB; the specified
  converter has 33,927,168 weights/biases, about 129.422 MiB. This is static algebra
  for the final map, not measured runtime/RSS/dollar cost; ARC2's retained training
  objects are excluded. Ridge has the same final coefficient size as ARC2 and
  Procrustes is similarly compact. Do not turn neural compactness into a claim
  of cost superiority over every baseline. Use planned component measurements
  to substantiate any additional fitting/mapping-efficiency statement.
- **Match independent wording to B2.** The existing184-cell/30-contrast matrix
  tests fixed-anchor ARC2 against five external configurations. It does not
  independently test the necessity of the second step versus one step. Default:
  keep that mechanism attribution as DEV evidence and independently confirm
  quality against external baselines. A new one-step test would be an optional,
  explicitly chosen prospective protocol extension before labels, not an
  automatic new requirement or a post-test change to the comparison family.

The highest-motivation optional algorithm direction is proxy/native score
compatibility, based on the E5 mixed-transition finding. It is not a proven
constant-bias repair and is not required by this completion plan. If the user
chooses to investigate it, use a separately named development candidate with
non-leaking calibration design and a new protocol before touching TREC; preserve
the frozen method and all old results. No algorithm change, calibration pilot,
new dataset, anchor sweep or extra confirmation collection is launched here.

For the mapper-only B2 route, the new protocol must name the exact endpoint
claims being confirmed. Verify the intended exact rankings/ID/tie/reload rules
before labels. Any intended ANN endpoint must also be sealed/verified before
labels, but an unclaimed full serving deployment does not become a prerequisite
to exact-retrieval confirmation. The24-deployment C2 campaign remains behind D2.

Review/evidence: `.aris/traces/research-review/2026-10-27_next_steps/`, including
`dev_matrix_inventory.json` and `reference_and_storage_review.json`.
Renderer regression: `provenance/qa/next_steps_render_regression_20261027.json`.
ARIS review is same-family/provisional; this is roadmap review, not a formal
paper-claim audit. Scientific protocols, sources, results and label exposure remain unchanged.

## Problem and claim map

Problem: given a destination-encoder migration, preserve fixed-target retrieval
quality while full corpus re-encoding is expensive; measure the effect of forward
proxies and partial backfill, with incumbent and full-target service as context.
The destination encoder is not assumed to improve relevance on every collection.

Method thesis: start from a centered rectangular Procrustes map, refine its
angular direction with two closed-form tangent ridge updates, and serve one
target-space gallery where paid true vectors replace proxies.

| Claim | Minimum evidence | Current status |
|---|---|---|
| C1: ARC2-Global is a useful simple non-neural mapper at matched encoding budgets | exact mixed-index retrieval vs credible external methods, matched anchors/IDs/seeds, retained failures, independent TREC confirmation | DEV mechanism and all-paid benchmark evidence; encoder-dependent strengths/limits; independent confirmation pending |
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

B1b policy resolution (2026-10-26, before new quality runs): LA2M uses20
clusters, n_init4 and source-only routing, selected as the first non-global
value in the pinned integration-script CLI grid, not claimed optimal. Official
SimpleLinear retains its actual five affine layers/SELU, fixed50 final epochs,
batch4028, AdamW/MSE+0.5cosine and no validation/early stopping. Ridge uses
lambda10 including bias. configs/baselines.json and the B1b protocol record
exact source/runtime adaptations. These resolve existing six-system rows;
no extra main ranking cells or new scientific claim is introduced.

Full-X and full-Y are always visible references. No method gets hidden full-Y
vectors in fit, routing, selection, threshold calibration or scheduler decisions.

## Five experiment blocks

### B0 â€” package and numerical identity (local, current task)

Extract the existing global path only; retain selected raw rows, original seals
and source hashes. Verify exact coefficient/proxy/mixed-gallery parity on
synthetic same/cross dimensions and copied-result arithmetic. Reuse the LNCS
template/bibliography/section layout, never old placeholder values. No scientific
benchmark or GPU run. Output: clean code, measured report, compact paper scaffold.

### B1 â€” exact retrieval breadth and mechanism (must-run, H100 after notification)

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

### B2 â€” one prospective TREC-COVID confirmation (must-run, no retuning)

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

### B3 â€” physical migration cost and serving (conditional on C2 admission, H100)

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

### B4 â€” held-out traffic benefit and paper closure (conditional on C2 route)

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

The full main matrix represents 300 nominal method/collection/pair/seed fits:
240 DEV and 60 conditional TREC. The current completed DEV matrix has 150 fitted
main-method galleries represented; up to 90 further Nano method fits remain,
pending any additional identity-verified historical reuse. FiQA's remaining 50
rankings have30 existing fitted-gallery reuse paths. Extra ablations represent
120 configuration fits and all-paid represents60, both already completed;
shared factors/one-step coefficients can avoid separate physical fitting.
Do not count each budget as another MLP fit. Potential converter workers now
remaining are 30 Nano plus 10 TREC only if B2 is admitted; the 10 all-paid converter
workers are complete. Data/model/backend differences can prevent reuse; report
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

1. **Completed:** B0, baseline-adapter validation and B1-M/P0/P/G controls.
   Use the current report and tracker; their historical pre-run STOP markers are
   provenance, not today's execution instructions.
2. **Completed31Oct:** prospective B1c-R3 recovery sealed358newrankings and scored736cells. LocalQA, six-methodtables, figures and finalD1 complete; old320/R2 interruptedattempts preserved.
3. **Completed31Oct:** finalD1 narrowGO-C1 fromcomplete B1c+M/P/G; TREC staysclosed pendinguserrelease.
   Freeze supported method/scope and comparison family. Integrate completed DEV
   evidence into the manuscript; no algorithm/threshold tuning on final labels.
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
