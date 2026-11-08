# B2 result-to-claim review

Overall verdict: **partial**, with high confidence in the narrow numerical interpretation. Semantic review is **same-family / provisional**. `integrity_status: unavailable`: no formal `EXPERIMENT_AUDIT.json` was found. Computational QA is separately PASS and does not upgrade this status.

Suggested central claim: ARC2-Global is a compact forward document-space adapter that applies two closed-form tangent corrections to a centered Procrustes map. With 1,024 fitting pairs, it improves aggregate nDCG@10 across four inspected development collections. A prospective TREC-COVID test confirms gains in 11 of 30 declared comparisons against the specified ridge, SimpleLinear and Converter configurations, while its incremental nDCG advantage over Procrustes and LA2M remains unresolved.

The evidence supports a bounded representation-quality contribution and an explicit boundary on transfer. It does not support a general state-of-the-art claim or an independent win over the Procrustes initializer. The broad independent superiority claim should be narrowed now; further experiments are not needed to make that narrower statement truthful.

I read the immutable B2 protocol, frozen lock, raw scoring summary and completion/opening/verification receipts, deterministic precheck, final local QA, source implementation, consolidated DEV report, B1c report, B1-P all-paid report, B1-G diagnostics and the B1-M raw macro summary. The deterministic precheck found six cited values; that establishes existence only. I derived the primary outcomes directly from every saved family interval rather than accepting reported outcome counts.

The complete test contains 180 partial rankings and four native references, two encoder pairs, five mapping seeds, three budgets, 171,332 documents and all 50 queries. Its statistical units are 50 queries, not 250 seed-query observations. Five-seed averages precede the shared 20,000-draw PCG64 paired-query bootstrap (seed20261031). The 30 primary nDCG intervals use approximate 95% Bonferroni family coverage; Recall intervals are nominal 95% descriptive. A family interval strictly above zero supports improvement, strictly below zero supports worse performance, and touching/crossing zero is unresolved. I retain these frozen thresholds and introduce no margin, subset, new test or post-test selection rule.

Across all 30 primary contrasts, **11 improve and 19 remain unresolved; none is family-negative**. There are 20 positive and 10 negative point deltas. Confirmed gains comprise MiniLM Converter at 25/50% and ridge at 75%; E5 SimpleLinear at 25/50%, ridge at 25/50/75%, and Converter at 25/50/75%. Procrustes and LA2M have zero confirmed gains out of six each. The fact that no family interval is wholly negative does not establish safety, noninferiority or equivalence. In particular all six Procrustes point deltas favor Procrustes. E5/50% versus Procrustes is -0.016322 [-0.039820,+0.002298]. E5/75% versus LA2M is -0.008995 [-0.035779,+0.015646]. MiniLM/75% versus Converter is unresolved despite a positive point mean (+0.016258 [-0.000045,+0.032084]); it must not be rounded into a win.

All primary effects below are absolute nDCG units. Baseline labels mean the locked configurations, including their documented adaptations, not unrestricted original-paper methods or verified published-setting reproductions.

| Pair | Budget | Baseline | Delta nDCG [family interval] | Decision |
|---|---|---|---:|---|
| minilm_distilroberta | 25pct | Procrustes | -0.000051 [-0.014695, +0.013214] | unresolved |
| minilm_distilroberta | 25pct | LA2M20 | -0.001504 [-0.034306, +0.029079] | unresolved |
| minilm_distilroberta | 25pct | SimpleLinear | +0.000873 [-0.032945, +0.032548] | unresolved |
| minilm_distilroberta | 25pct | Ridge | +0.029743 [-0.004478, +0.068326] | unresolved |
| minilm_distilroberta | 25pct | Converter | +0.039540 [+0.000630, +0.075613] | above_zero |
| minilm_distilroberta | 50pct | Procrustes | -0.004667 [-0.018618, +0.006099] | unresolved |
| minilm_distilroberta | 50pct | LA2M20 | -0.007321 [-0.026683, +0.007138] | unresolved |
| minilm_distilroberta | 50pct | SimpleLinear | -0.007635 [-0.027398, +0.006922] | unresolved |
| minilm_distilroberta | 50pct | Ridge | +0.014517 [-0.010799, +0.042098] | unresolved |
| minilm_distilroberta | 50pct | Converter | +0.021908 [+0.000518, +0.042639] | above_zero |
| minilm_distilroberta | 75pct | Procrustes | -0.000024 [-0.004505, +0.004384] | unresolved |
| minilm_distilroberta | 75pct | LA2M20 | +0.000951 [-0.006116, +0.008781] | unresolved |
| minilm_distilroberta | 75pct | SimpleLinear | +0.000211 [-0.006828, +0.008019] | unresolved |
| minilm_distilroberta | 75pct | Ridge | +0.018294 [+0.000440, +0.044923] | above_zero |
| minilm_distilroberta | 75pct | Converter | +0.016258 [-0.000045, +0.032084] | unresolved |
| e5_small_base | 25pct | Procrustes | -0.003240 [-0.021621, +0.014325] | unresolved |
| e5_small_base | 25pct | LA2M20 | +0.042211 [-0.006417, +0.093325] | unresolved |
| e5_small_base | 25pct | SimpleLinear | +0.132873 [+0.063300, +0.205137] | above_zero |
| e5_small_base | 25pct | Ridge | +0.264181 [+0.157265, +0.376758] | above_zero |
| e5_small_base | 25pct | Converter | +0.257234 [+0.175731, +0.337569] | above_zero |
| e5_small_base | 50pct | Procrustes | -0.016322 [-0.039820, +0.002298] | unresolved |
| e5_small_base | 50pct | LA2M20 | +0.000594 [-0.035513, +0.035996] | unresolved |
| e5_small_base | 50pct | SimpleLinear | +0.061730 [+0.013560, +0.114461] | above_zero |
| e5_small_base | 50pct | Ridge | +0.262267 [+0.157959, +0.372850] | above_zero |
| e5_small_base | 50pct | Converter | +0.231385 [+0.156717, +0.308507] | above_zero |
| e5_small_base | 75pct | Procrustes | -0.010012 [-0.026005, +0.003631] | unresolved |
| e5_small_base | 75pct | LA2M20 | -0.008995 [-0.035779, +0.015646] | unresolved |
| e5_small_base | 75pct | SimpleLinear | +0.031288 [-0.003830, +0.071705] | unresolved |
| e5_small_base | 75pct | Ridge | +0.281997 [+0.174800, +0.397330] | above_zero |
| e5_small_base | 75pct | Converter | +0.199954 [+0.139250, +0.264222] | above_zero |

Native-reference point means and ARC2 point means (no new reference contrasts or tests):

| Pair | Full-X nDCG | Full-Y nDCG | ARC2 25% | ARC2 50% | ARC2 75% |
|---|---:|---:|---:|---:|---:|
| minilm_distilroberta | 0.493478 | 0.520273 | 0.461913 | 0.499955 | 0.519513 |
| e5_small_base | 0.680542 | 0.642113 | 0.562802 | 0.590406 | 0.609782 |

Full-Y is a reference, not an upper bound. These points show that destination migration itself is not assured to improve relevance: E5 Full-X exceeds Full-Y. All six ARC2 Recall point means are also below Full-Y; four are below Full-X. The two MiniLM nDCG points above Full-X do not carry a prospective reference-superiority conclusion under the declared primary family.

B2 Recall provides a metric-dependent boundary: its E5-minus-Procrustes deltas are -0.001991 [-0.003292,-0.000680], -0.004733 [-0.006442,-0.003115], and -0.006389 [-0.008764,-0.004324] at 25/50/75%. These are nominal descriptive intervals, not additional primary discoveries. B2 does not erase the earlier all-paid losses or the overall DEV unresolved Recall difference versus Procrustes.

Individual claims are evaluated as follows:

- **compact_frozen_adapter: yes**. Source implements a centered raw affine Procrustes expansion followed by two ridge-solved tangent updates; inference applies the final affine coefficient and row normalization. For 384-to-768 dimensions, 385*768 float32 coefficients require 1,182,720 bytes. This is coefficient storage, not total runtime memory or a unique advantage over ridge/Procrustes. Closed-form describes each correction, not a globally optimal angular solution.

- **fixed_anchor_dev_macro: yes**. B1c five macro deltas are +0.024325, +0.104055, +0.172100, +0.095653 and +0.161162; all saved family intervals are positive. This remains inspected DEV, not independent validation or all-condition dominance.

- **independent_transfer_all_external: partial**. 11/30 family contrasts are positive, 19 unresolved, none family-negative. Gains occur versus Converter in 5/6 conditions, ridge in 4/6 and SimpleLinear in 2/6; none versus Procrustes or LA2M.

- **independent_procrustes_advantage: no**. All six B2 point deltas versus Procrustes are negative and all six family intervals cross zero. This demonstrates neither improvement, inferiority at the family criterion, noninferiority nor equivalence.

- **independent_la2m_advantage: no**. All six family intervals cross zero, with both positive and negative point deltas.

- **two_step_mechanism: partial**. DEV B1-M two-minus-one macro delta +0.006924 has family interval [+0.003809,+0.009959]; two-minus-Procrustes is +0.024325. This supports an average DEV contribution, not independent necessity or optimality. B2 contains no one-step arm, and does not confirm incremental improvement over Procrustes.

- **all_paid_dominance: no**. B1-P E5 all-paid loses nDCG to Procrustes (-0.044335, family interval [-0.079696,-0.009272]) and LA2M (-0.037474, [-0.070583,-0.003758]); MiniLM versus all-paid ridge is unresolved. MiniLM fixed-anchor also trails every all-paid baseline in the locked cross-regime comparisons.

- **mixed_gallery_causal_explanation: partial**. B1-G establishes that actual true-vector replacement can reverse pure-proxy ordering; all-paid FiQA/E5 ARC2 changes 0.314908 to 0.291867, versus Procrustes 0.286096 to 0.336202. It does not isolate a unique causal explanation or validate a calibration repair.

- **native_reference_superiority: no**. All six B2 ARC2 nDCG point means are below Full-Y; four are below Full-X. E5 Full-X exceeds Full-Y, and all three E5 ARC2 points are below both. The two MiniLM point means above Full-X are descriptive comparisons outside the 30-contrast primary family.

- **uniform_recall_advantage: no**. B2 has 25 positive, three negative and two unresolved nominal descriptive Recall intervals. All three E5-vs-Procrustes Recall differences are negative; DEV overall Recall versus Procrustes is unresolved.

- **systems_cost_traffic_ann: no**. B2 exact cache-based representation comparisons count logical unique destination exposure, not a physically measured partial-deployment cost. Shared-load receipts and endpoint replay establish neither serving performance nor cost savings. No ANN or real-traffic experiment is present.

- **recorded_prospective_sequence: yes**. Final QA verifies the locked 184-cell identities, 60 fit groups, pinned sources and ordered recorded events; all rankings sealed 19:56:09 UTC, replay seal completed 20:11:42 UTC, opening receipt 20:12:17 UTC. This is recorded provenance and computational QA, not a formal audit of every possible human access.

The positive contribution can be stated as a fixed affine adapter with two closed-form angular corrections, a complete matched-supervision development comparison, and a prospective test showing both transferable gains against specified configurations and the boundary at stronger geometric baselines. Keep the method frozen. Report the aggregate DEV improvement and the full independent table together. Do not present eleven favorable cells as a newly selected deployment policy, or claim that the test established the second correction's independent value.

The supported use case is a migration already required for reasons outside these relevance results, with a declared 1,024-pair fitting set and partial native backfill. ARC2 is a candidate to evaluate at the actual mixed endpoint, alongside Procrustes and LA2M. Relevance priorities may favor retaining the incumbent, and Recall priorities may favor another mapper. This is a conditional candidate-use statement; the study supplies no dollar, latency, memory-budget or cutover threshold for choosing it. Logical destination exposure is |A union S|, anchors included: 42,833/85,666/128,499 documents, while physical corpus encoding was separately performed for the evaluation caches. The approximately 1.128 MiB final coefficient array is a transparent structural property, not measured end-to-end memory efficiency.

Final computational QA receipt `results/b2_review_20261101/qa_completed_20261101T020214554697Z.json` is PASS: 61 source pins, 62 pre-run Git objects, 184 prescribed cells, 60 fit groups and 1,138 compact files verified; 18,400 metric values agree within 2.22e-16, 2.8 million independently recomputed bootstrap values within 7.77e-16, and 1,106 summary numbers within 4.44e-16. The remote pre-label verifier separately replayed every ordered exact top100. Recorded seals/opening times are consistent with the prospective protocol. Large vectors/checkpoints are bound by transport-coverage hashes/sizes, not independently rehashed or regenerated in local QA; the receipt does not audit every possible human/data access. Retained stderr warnings and historical failed attempts must remain visible. No formal integrity audit or cross-family semantic acceptance is implied.

Missing evidence for broader claims is independent improvement over Procrustes/LA2M, independent zero/one/two-step mechanism tests, broad encoder/domain generalization, independent all-paid comparisons, and any actual deployment cost/serving evidence. These are limitations, not a requirement to keep expanding this finite campaign. If a future claim requires one of them, it needs a new explicit authorization and immutable protocol; B2 is exposed and cannot become a fresh test through retuning.

The next authorized action is to finish the existing B2 tables/figures, record the narrowed claim and limitations in the report/notes, and STOP. Leave `manuscript/` unchanged. No automatic B3/B4, new dataset, calibration variant, algorithm revision, further relevance test or formal claim audit is authorized by this result. A future manuscript update or broader scientific phase requires the user's separate instruction. No novelty or venue-acceptance judgment is made here.
