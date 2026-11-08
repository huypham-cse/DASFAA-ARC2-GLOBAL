# Completed-result depth audit

Audit date: 1 November 2026. Read-only comparison of `D:/DASFAA-2027-paper` and `D:/DASFAA-2027-paper-release`. Scope follows the paper workspace's current AGENTS.md: ARC2-Global only, fixed lambda10 and two tangent updates, no local residual. No manuscript or scientific artifact was changed; no new run, scoring, bootstrap, threshold, tuning or method selection was performed.

## Finding

The release preserves the five substantive result families M/P/G/B1c/B2. Their five raw scorer summary JSONs are byte-identical to the workspace copies. The weakness is the executive presentation: START_HERE shows two studies visually (DEV main quality and independent B2), while three completed studies are reduced to a sentence and selected limitations. A supervisor can miss both material positive all-paid evidence and the strongest qualifications. This is underreporting, not evidence that the M/P/G raw results were deleted.

I independently recomputed every reported mean in M, P, B1c and B2 from saved `per_query.npy` arrays plus their cell indexes: 776 metric mean values, maximum absolute difference exactly zero. Saved scorer intervals were read directly; no new intervals were constructed. The companion JSON retains exact source paths/hashes and the raw relevant contrasts.

## Completed evidence ledger and correct counts

| Study | Completed measurement unit | Means / contrasts | Increment to logical unique quality matrix | Executive visibility |
|---|---|---|---|---|
| B1c main DEV | 736 rankings =720 partial seed endpoints +16 native refs |144 partial condition means +16 refs;120 matched condition contrasts;5 macro family contrasts |736 |Prominent chart; only five-sign outcome in prose |
| B1-M mechanism |736 rankings =720 partial +16 refs; zero/one/two-step, lambda1/10/100 and ridge controls |144 partial means +16 refs;120 condition contrasts;10 pair macros;5 overall family contrasts |360 additional one-step/lambda1/lambda100 seed endpoints;376 identities overlap B1c |One retention sentence in START_HERE; CLAIM_LOCK quantifies step2 only |
| B1-P all-paid |124 rankings =120 partial +4 refs;51 reused +73 generated |24 partial means +4 refs;32 declared nDCG contrasts:12 within-method +10 allpaid ARC2/baseline +10 fixed ARC2/allpaid baseline |60 allpaid seed endpoints;64 fixed/reference identities overlap main |Negatives mentioned; MiniLM four wins absent from front page |
| B1-G mixed diagnostics |450 paired cases,210 saved pristine galleries,90 five-seed conditions |Before/after nDCG and Recall, score errors, returned shares;450 historical mixed arrays replay exactly |No added main quality identity, fit or embedding; counterfactual diagnostics |Reversal asserted without numbers; existing detailed figure unshown |
| B2 independent |184 rankings =180 partial +4 native refs,60 fits |36 partial condition means +4 refs;30 primary family contrasts |184 |Prominent complete family decisions |
| P0 backend validation |31 synthetic fixtures/62 update comparisons;40 real1024-anchor fit identities/120 budget comparisons |Correctness drift checks, not relevance contrasts |0 |Inside M/P0 subsidiary summary |
| B1a preparation/smoke |4 reference dimension cases;4 encoder repeat checks;2 toy mixed galleries;60 nested paid sets |Readiness/correctness, no benchmark scoring |0 |No standalone result folder in release |
| B1b baseline validation |25 LA2M oracle fixtures,15 ridge cases,5 official SimpleLinear adapter/direct comparisons |Raw prediction/coefficient differences0.0 |0 |No standalone result folder in release |
| Imported FiQA |64 rankings,60 partial +4 refs,12 partial means +4 refs |Historical inspected DEV import, no original candidate-specific CIs |0 beyond the later identity matrix |No separate imported folder in release; compatible evidence reused |

**Union is1,340 logical quality cells =1,320 partial +20 native reference cells**, verified by building identities `(dataset,pair,method,budget,fit_regime,seed)` from raw cell indexes. It is736 main +360 ablation +60 allpaid +184 independent. It is not736+736+124+450+184, and it is not the count of newly executed fits or physically unique saved ranking files. R3's38 displaced historical FiQA outcomes, interrupted attempts and newer replacement artifacts must remain distinct provenance even when their logical condition identity repeats. Counts of mean signs, family contrasts, ranking seeds, queries, fits, and diagnostic counterfactuals must remain separate.

The two studies'736 counts mean different method panels. M's six partial methods are Procrustes, ARC2, one-step, lambda1, lambda100 and ridge. Main B1c's are Procrustes, ARC2, LA2M, SimpleLinear, ridge and Converter. Reusing the number736 without naming the panel is especially easy to misread.

## Material positives and negatives worth surfacing

### 1. MiniLM all-paid evidence is stronger than the front-page narrative suggests

At the same50% paid-document budget and the same28,819 fitting pairs for all methods, MiniLM ARC2 nDCG is0.367146, compared with Procrustes0.333386, LA2M0.338923, SimpleLinear0.332316, ridge0.367263 and Converter0.325761. These are five-seed means read from P's raw scorer JSON and independently reproduced from per-query arrays.

| Allpaid ARC2 minus allpaid baseline | MiniLM delta nDCG [saved family interval] | E5 delta nDCG [saved family interval] |
|---|---|---|
| Procrustes |+0.033760 [+0.018645,+0.050408] |-0.044335 [-0.079696,-0.009272] |
| LA2M20 |+0.028223 [+0.010129,+0.047297] |-0.037474 [-0.070583,-0.003758] |
| SimpleLinear |+0.034830 [+0.023544,+0.047191] |+0.123918 [+0.093821,+0.156724] |
| Ridge |-0.000117 [-0.007540,+0.006532] |+0.064852 [+0.043521,+0.089349] |
| Converter |+0.041385 [+0.023614,+0.060969] |+0.029348 [-0.015573,+0.074762] |

These intervals belong to the locked32-contrast family, approximately95% family coverage, not a new10-contrast correction. Four MiniLM matched family comparisons favor ARC2; ridge is unresolved. E5 has two confirmed losses, two gains and one unresolved contrast. This encoder dependence is a substantive scientific result and should be summarized symmetrically. The detailed P summary already does this; START_HERE and CLAIM_LOCK emphasize the limits without stating the four positive comparisons.

### 2. Additional supervision is beneficial for MiniLM but not uniformly beneficial

For ARC2 fixed1024 to allpaid28819, MiniLM nDCG increases0.307505 to0.367146: delta+0.059641, family interval[+0.039341,+0.080604]. Recall delta+0.015631, descriptive95%[+0.002193,+0.029359]. E5 nDCG decreases0.311635 to0.291867: delta-0.019768, family interval[-0.056330,+0.016637], unresolved; Recall delta-0.061435, descriptive95%[-0.083203,-0.040108]. Do not call the E5 nDCG decrease a family-confirmed degradation.

A further limit is easy to miss: **MiniLM fixed1024 ARC2 loses against every allpaid baseline in all five locked cross-regime nDCG comparisons.** Deltas are-0.025882 vs Procrustes,-0.031419 vs LA2M,-0.024811 vs SimpleLinear,-0.059758 vs ridge,-0.018257 vs Converter; all five family intervals are below zero. Fixed-supervision main-matrix gains do not establish the best use of all already-paid target pairs. All32 P decisions, including within-method and cross-regime comparisons, total19 above-zero,9 below-zero,4 unresolved; these must not be advertised as32 same-regime superiority comparisons.

### 3. Mechanism work supports the two-step design, with locked sensitivity caveats

| Saved M contrast | Macro nDCG delta | Saved99% family interval |
|---|---:|---|
| ARC2 minus zero-step Procrustes |+0.024325 |[+0.018015,+0.031021] |
| ARC2 minus one tangent step |+0.006924 |[+0.003809,+0.009959] |
| ARC2 minus ordinary affine ridge |+0.095653 |[+0.075353,+0.116631] |
| Lambda1 two-step minus locked lambda10 |+0.003197 |[-0.001890,+0.008304] |
| Lambda100 two-step minus locked lambda10 |-0.009255 |[-0.013214,-0.005510] |

These are equal-weight macros across24 dataset/pair/budget conditions, five seeds averaged first. Two-step exceeds zero-step in23/24 mean conditions and one-step in22/24; those counts are descriptive, not23 or22 family-confirmed wins. The lambda1 interval is unresolved, so this is neither evidence that lambda10 is optimal nor permission to select lambda1 after inspection. Lambda100's family-negative result supplies useful sensitivity evidence. No independent one-versus-two experiment exists in B2.

M and B1c repeat the same Procrustes/ridge point deltas but have different bootstrap families/draw contexts. For example Procrustes M family interval is[0.018015,0.031021], whereas B1c is[0.018132,0.030792]. These are not contradictory and must not be interchanged. B1c primary comparisons are five external configurations; M includes lambda/step controls.

### 4. Main fixed-anchor results have metric limits in addition to a positive macro

Raw B1c macros favor ARC2 in all five nDCG families: Procrustes+0.024325, LA2M+0.104055, SimpleLinear+0.172100, ridge+0.095653, Converter+0.161162. All family intervals are positive. Against Procrustes, nDCG mean signs are23 higher/1 lower; Recall signs are11 higher/12 lower/1 tied, with overall Recall delta-0.000239 and descriptive95%[-0.004944,+0.004336]. E5's descriptive Recall macro delta is-0.007654. The sole negative nDCG point condition is FiQA/E5/75%:-0.003583.

ARC2 partial nDCG is below native Full-X and Full-Y in24/24 conditions each. Recall exceeds Full-X in8/24 and Full-Y in1/24, so native references are contextual operating points rather than mathematical upper bounds. The existing quality and Recall figures retain these facts; the executive page currently displays only quality.

### 5. Mixed replacement reverses an actual relative ordering

For allpaid FiQA/E5 at50%, G's saved five-seed metrics are:

| Method | Proxy-only nDCG | Actual mixed nDCG | After-before | Proxy-only Recall | Actual mixed Recall | After-before |
|---|---:|---:|---:|---:|---:|---:|
| ARC2 |0.314908 |0.291867 |-0.023041 |0.654164 |0.559490 |-0.094674 |
| Procrustes |0.286096 |0.336202 |+0.050106 |0.605397 |0.653389 |+0.047992 |
| Ridge |0.270585 |0.227015 |-0.043570 |0.602436 |0.424511 |-0.177925 |

ARC2 is above Procrustes in proxy-only nDCG, below it after actual paid-row replacement. ARC2's nDCG and Recall after-before deltas are negative in all five saved seeds. Its paid top10 share changes0.491640 to0.064720, with sampled unpaid proxy-minus-true score bias+0.039684. Procrustes paid top10 share changes0.497480 to0.370720, unpaid bias+0.017429. These are descriptive measurements; returned-share imbalance and bias do not establish miscalibration or causally explain the quality reversal.

The before gallery predicts every document including anchors; after replaces the original exact anchor-inclusive paid set. The fitting exposure is held fixed. An allpaid mapper already saw its paid pairs when fitting, so the before endpoint is a counterfactual without replacement, not a no-target-supervision regime. This distinction should accompany the small reversal table. A sentence alone loses that mechanism relevance.

### 6. B2 is correctly bounded, but Recall and native-reference boundaries can be clearer

The raw30-contrast family is11 above-zero/19 unresolved/0 below-zero: Converter5/6, ridge4/6, SimpleLinear2/6; Procrustes/LA2M0/6 each. All six Procrustes point differences are negative. Unresolved is not equivalence or noninferiority.

Against Procrustes, MiniLM Recall deltas at25/50/75% are+0.003062,+0.001806,+0.000407; first two descriptive intervals exclude zero, third crosses. E5 Recall deltas are-0.001991,-0.004733,-0.006389, with all three nominal95% intervals below zero. This metric tradeoff reinforces the encoder-dependent boundary. No new multiple-comparison inference should be implied.

E5 native Full-X nDCG0.680542 exceeds Full-Y0.642113 and every ARC2 endpoint0.562802/0.590406/0.609782. MiniLM native Full-X0.493478 is below ARC2 at50/75% but above ARC2 at25%; Full-Y0.520273 remains above all three ARC2 means. The current claim lock mentions the E5 boundary correctly.

## Correctness evidence and actual packaging gaps

P0 is retained within the M/P0 release folder and deserves a correctness ledger row:31 synthetic fixtures,62 update comparisons;40 real1024-anchor fits,120 budget comparisons;zero changed ordered top100 query comparisons. Maximum stored-coefficient difference7.27595761418e-12 and normalized proxy difference3.72529029846e-09. This is ranking/numerical compatibility, not bit identity or a cost benchmark. The primal backend is explicitly identified and opt-in; fixed primary rankings use the frozen dual. The earlier P0 study did not itself benchmark real28819-pair fits; later P did.

The release does not contain standalone `results/b1a_r1_20261025`, `results/b1b_20261026`, `results/b1a_first_failure_20261025`, or `results/fiqa_development` result directories. It does include B1a/B1b protocols, locks and runnable code, which establish intended procedures but are not substitutes for completed receipts. If the desired release is a complete review archive, add a small `provenance/preparatory_validation/` appendix with:

- B1a SUMMARY, metadata, synthetic_checks and first-attempt failure receipt; input manifest/hash receipt and GPU-worker smoke metadata. It establishes4 exact reference-parity dimension cases,4 deterministic toy encoder repeats,2 toy mixed galleries and60 nested anchor-inclusive paid sets, not retrieval quality.
- B1b SUMMARY, metadata, cpu_checks and official SimpleLinear GPU metadata:25 LA2M author-oracle fixtures,15 independent ridge checks,5 official-code adapter/direct comparisons, all prediction/coefficient differences0.0. Preserve qualifications: LA2M20 is script-guided adaptation; SimpleLinear is five affine layers/final50, not a single linear map.
- Imported FiQA summary/metric_index/import manifest and selection/extraction mapping as provenance, with an explicit reused identity map. It is inspected DEV selected after scores;64 imported rankings are not64 extra independent observations. Candidate-specific intervals came from subsequent locked controls, not the original import.

This appendix is a provenance recommendation, not a reason to pull older scientific methods into the active result set. The current release's main results are already reviewable without their larger old artifacts. Failure/negative preservation and claim provenance improve with the small appendix.

## Reviewer-facing presentation from saved evidence only

1. Add an executive evidence ledger with main DEV, M, P, G, P0 and B2, separating completed units, question, saved effect and limitation. Label B1a/b as preparatory correctness in an appendix. Link each row directly to its subsidiary SUMMARY and raw JSON.
2. Add the ten-row allpaid contrast table above, or a two-panel forest plot copied from saved P deltas/family intervals. Show both encoder pairs, all five baselines, all signs and both native references. This is the highest-value missing visual; there is no saved P figure in the release.
3. Add the five-row mechanism table/forest plot from M's saved overall_macro intervals, retaining lambda1 unresolved and lambda100 negative. No M publication figure currently exists in the release.
4. Show the already-generated `b1g_mixed_gallery_diagnostics.pdf/png` beside a concise explanation of its frozen-fit before/after endpoint. Keep the predeclared overview subset and link all90 conditions; do not select a new subset based on favorable outcomes.
5. Link/show the existing B1c Recall counterpart and B2 Recall figure, or provide the short metric-limit row. Do not add a composite significance claim across nDCG/Recall.
6. If showing efficiency structure, diagram one1024-pair fit reused across budgets and logical paid sets versus unmeasured physical costs. Use actual paid counts from locked IDs. No random-paid-set method beats a selected active strategy here; random/nested paid sets are a fixed protocol design, not a demonstrated sample-efficiency/cost win. Existing full-corpus caches and shared-host wall/RSS receipts cannot establish deployment dollars, isolated H100 throughput or SLO benefits.

All proposed numbers/plots can be taken directly from saved JSON/CSV arrays; none requires a new experiment or uncertainty calculation. The current claim lock can remain scientifically narrow while the review page becomes more complete.

## Method-scope guard

Current identity is `arc2_global_tangent2_r1`: centered rectangular Procrustes expanded as a raw affine map, lambda10, exactly2 tangent corrections, normalized proxy gallery, anchor-inclusive true-vector replacement, no learned local residual. Historical ARC2/local-k8, P5/P8 variants and original mixed-index experiments are not this method. They may be linked as discovery/history, but their quality gains, costs or negative verdicts must not be relabeled as current ARC2-Global results. The Global import explicitly excludes old local8 as independent LA2M evidence. Current LA2M means come from the separately pinned clustered adaptation. No critical current-release local/Global substitution was found in this scope.
