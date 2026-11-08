# ARC2-Global: current consolidated results

<!-- B2_CURRENT_BEGIN -->
Updated 1 November 2026. **B2 independent TREC-COVID confirmation is complete:** 171,332 documents, 50 queries, two frozen encoder pairs, five seeds, 25/50/75% budgets; all 184 rankings and 60 fit groups. Rankings sealed at 02:56:09+07, separate exact endpoint replay finished 03:11:42, first final-label receipt 03:12:17, scoring completed 03:12:54. No scientific failures or postlabel changes.

The locked 30-comparison nDCG@10 family has **11 positive intervals, 19 unresolved, 0 negative intervals**. This is a condition-specific independent result. It does not establish equivalence or noninferiority in the unresolved comparisons.

| ARC2 minus declared baseline configuration | Positive family intervals | Unresolved | Negative family intervals |
|---|---:|---:|---:|
| A2M / Procrustes adaptation | 0/6 | 6/6 | 0/6 |
| LA2M20 adaptation | 0/6 | 6/6 | 0/6 |
| SimpleLinear official code, locked policy | 2/6 | 4/6 | 0/6 |
| Affine ridge, lambda10 | 4/6 | 2/6 | 0/6 |
| Embedding-Converter paper-spec adaptation | 5/6 | 1/6 | 0/6 |

All six nDCG point differences against Procrustes are negative (-0.016322 to -0.000024), with family intervals crossing zero. All six LA2M comparisons are also unresolved. Independent broad superiority over these baselines is unconfirmed. Recall is descriptive: against Procrustes, ARC2 gains for MiniLM and loses for E5; these intervals were not corrected as the primary family.

MiniLM ARC2 nDCG at 25/50/75% is 0.461913/0.499955/0.519513, versus native Full-X 0.493478 and Full-Y 0.520273. E5 ARC2 is 0.562802/0.590406/0.609782 versus Full-X 0.680542 and Full-Y 0.642113. Retaining an incumbent can therefore be the appropriate quality choice. Full-Y is a native reference, not an upper bound.

[All B2 results, tables and figures](results/b2_review_20261101/SUMMARY.md) | [Raw independent summary](results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json) | [Current ARIS claim review](CLAIMS_FROM_RESULTS.md).

Independent local QA recomputed all 184 rankings/18,400 metric values (maximum difference 2.22e-16) and 2.8 million saved bootstrap values. This validates the saved evidence, not fresh local regeneration of large vector endpoints. The remote separate verifier replayed every ordered top100 endpoint before labels. Full backup: 1,330 files/58,977,150,839 verified bytes on D, zero pending. All 20 manuscript file hashes remain unchanged.

The current result is a compact, neural-training-free forward adapter with clear fixed-anchor DEV benefits and a narrower independent advantage over specified baseline configurations. It has no measured isolated cost, serving SLO, ANN or real-traffic benefit. B2 encoded all four full-corpus model caches for representation evaluation; it did not measure actual partial-migration deployment savings.

**STOP:** B2 results/QA/figures/ARIS are complete. Manuscript editing, new datasets, retuning and B3/B4 were not performed. The remaining paper work is to integrate this bounded evidence and audit the resulting manuscript when authorized; no additional benchmark is automatically required.

The following sections retain the completed inspected DEV evidence and its limitations.
<!-- B2_CURRENT_END -->

Updated 31 October 2026. **The complete B1c-R3 DEV matrix is scored and locally verified.**

With 1,024 shared fitting anchors, ARC2-Global has higher aggregate nDCG@10 than all five declared external baseline configurations across four inspected development collections. All five predeclared macro comparison intervals exclude zero in its favor. This supports a bounded quality claim; the all-paid and Recall results below define its limits.

[Complete six-method report and figures](results/b1c_r3_review_20261031/SUMMARY.md) | [Raw scored summary](results/b1c_r3_review_20261031/evidence/run/scoring/summary.json) | [Current claim review](CLAIMS_FROM_RESULTS.md) | [Execution tracker](refine-logs/EXPERIMENT_TRACKER.md).

## Complete fixed-anchor comparison

NanoNQ (5,035 documents, 50 queries), NanoHotpotQA (5,090/50), NanoFEVER (4,996/50), FiQA (57,638/500); two encoder pairs, five seeds and 25/50/75% paid-document budgets. Both pairs map 384 to 768 dimensions: MiniLM to DistilRoBERTa and E5-small to E5-base. The method is frozen at two tangent updates and lambda10; no local residual or neural training.

All 736 cells are present: 378 retained and 358 new rankings, with 118 fresh fit groups and two saved-fit reuse groups. The 38 displaced historical FiQA cells and earlier interrupted attempts remain provenance. R3 completion does not relabel those old attempts as successful.

Each contrast below equally weights the 24 dataset/pair/budget strata after averaging five seeds. The locked 20,000-draw query bootstrap uses 99% intervals per nDCG comparison, giving approximate 95% coverage for the five-comparison family. Per-condition and Recall intervals are descriptive. Higher mean counts are not counts of statistically significant wins.

| ARC2 minus baseline | Absolute nDCG@10 delta | 99% interval | Higher/lower/tied means, out of24 |
|---|---:|---|---:|
| A2M / Procrustes adaptation | +0.024325 | [+0.018132, +0.030792] | 23/1/0 |
| LA2M20 adaptation | +0.104055 | [+0.086070, +0.122915] | 24/0/0 |
| SimpleLinear official code, 5-layer MLP | +0.172100 | [+0.149862, +0.194703] | 24/0/0 |
| Affine ridge, lambda10 | +0.095653 | [+0.075405, +0.116427] | 24/0/0 |
| Embedding-Converter paper-spec adaptation | +0.161162 | [+0.142686, +0.179916] | 24/0/0 |

The overall Recall@100 difference against Procrustes is -0.000239 (descriptive95% interval [-0.004944, +0.004336]), which is unresolved. The sole lower nDCG condition mean against Procrustes is FiQA/E5 at75%; E5 Recall also has losses. All24 partial ARC2 nDCG means are below both native Full-X and Full-Y references. This statement concerns nDCG: Recall is above Full-X in8/24 conditions and above Full-Y in1/24.

Procrustes/A2M and LA2M20 are the declared adaptations; SimpleLinear uses official upstream code with the locked five-layer/final50-epoch training policy. Embedding-Converter is a paper-spec adaptation with 50,000 selection steps and a selected-length fresh refit, trained on the same1,024 paired anchors. These results do not reproduce its published multi-corpus training setting. Full-X uses its native query/document encoder and is an incumbent reference; Full-Y is the destination-native reference, not a mathematical upper bound.

## Mechanism and supervision controls

B1-M ablations are a separate completed DEV study. Its five-comparison interval family differs from the B1c external-baseline family, so their intervals must not be interchanged.

| B1-M contrast | Absolute nDCG@10 delta | 99% family interval |
|---|---:|---|
| ARC2-Global minus Procrustes | +0.024325 | [+0.018015, +0.031021] |
| ARC2-Global minus one tangent step | +0.006924 | [+0.003809, +0.009959] |
| ARC2-Global minus affine ridge | +0.095653 | [+0.075353, +0.116631] |
| two steps, lambda1 minus ARC2-Global | +0.003197 | [-0.001890, +0.008304] |
| two steps, lambda100 minus ARC2-Global | -0.009255 | [-0.013214, -0.005510] |

B1-P0 verified the all-paid numerical backend against the frozen reference. B1-P then gave every method all28,819 already-paid pairs on FiQA50%, removing the withheld-supervision objection at that operating point. The outcome is encoder-dependent:

| All-paid FiQA50% method | MiniLM nDCG@10 | E5 nDCG@10 |
|---|---:|---:|
| ARC2-Global | 0.367146 | 0.291867 |
| A2M / Procrustes adaptation | 0.333386 | 0.336202 |
| LA2M20 adaptation | 0.338923 | 0.329341 |
| SimpleLinear official code, 5-layer MLP | 0.332316 | 0.167949 |
| Affine ridge, lambda10 | 0.367263 | 0.227015 |
| Embedding-Converter paper-spec adaptation | 0.325761 | 0.262519 |

MiniLM ARC2 has positive family-adjusted nDCG comparisons against four configurations; the ridge comparison is unresolved. E5 ARC2 is below Procrustes and LA2M with all paid pairs. The fixed-anchor result does not establish best use of every available paid pair.

[All-paid report, all32 contrasts and retained failures](results/b1p_r5_review_20261027/SUMMARY.md).

## Mixed-gallery behavior

B1-G reused frozen galleries to compare pure proxies with actual mixed endpoints. For all-paid FiQA/E5 at50%, five-seed nDCG means are:

| Method | Pure-proxy diagnostic | Mixed endpoint | Mixed minus proxy |
|---|---:|---:|---:|
| ARC2-Global | 0.314908 | 0.291867 | -0.023041 |
| A2M / Procrustes adaptation | 0.286096 | 0.336202 | +0.050106 |
| Affine ridge, lambda10 | 0.270585 | 0.227015 | -0.043570 |

Thus better pure-proxy quality can reverse after true-vector replacement. The score/share diagnostics suggest a compatibility hypothesis; they do not prove a unique cause or a calibration fix. The pure-proxy endpoint is a diagnostic counterfactual, not a zero-encoding deployment.

[Complete mixed-gallery evidence](results/b1g_r1_review_20261027/SUMMARY.md).

## Use case, efficiency and limits

The supported use case is a required destination-space migration with a small declared fitting set and partial native backfill. ARC2 offers a simple affine forward map with empirical aggregate nDCG gains over the declared fixed-anchor alternatives. Evaluate the actual mixed endpoint before cutover, especially when more paired data or E5 encoders are available. A relevance/Recall target can favor a different method or retaining the incumbent.

For384-to768 dimensions, the final affine map has295,680 float32 coefficients including bias (1,182,720 bytes, approximately1.128MiB). This is algebraic coefficient storage only, excluding fitting objects; ridge is equally compact and Procrustes similarly compact. No neural training is required for ARC2. Cached destination exposure counts unique documents as|A union S|, anchors included. Those cached DEV measurements performed zero new physical document encodings. No dollar saving, isolated H100 cost, serving SLO or real-traffic gain is established.

## Verification and finite next step

All736 compact rankings were rescored locally using a separate metric implementation and the locked DEV qrels;239,200 metric values agree within3.33e-16. The locked20,000-draw means/intervals agree within4.44e-16. The compact bundle verifies scoring evidence, not regeneration from all model checkpoints/vectors; full backup has a separate completion receipt.

The full six-method DEV comparison is finished. Its historical D1 led to the now-completed B2 above. The current STOP is after B2 review; B3/B4 remain conditional and were not run.

Raw results, negative outcomes and failed/interrupted runs remain authoritative; the manuscript still needs the completed DEV evidence integrated before it can be treated as a current paper.

The current B1c-R3 full/smoke/schedule output backup is complete on D: 2,484 files, 64,478,738,712 verified bytes (approximately64.48GB), zero pending files. This backup scope does not include every historical project or source/runtime cache. [Terminal backup receipt](provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json).
