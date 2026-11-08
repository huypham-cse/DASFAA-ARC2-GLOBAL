# B1-P completed: all-paid fitting at the same 50% encoding budget

**COMPLETE and locally verified, 27 October 2026. STOP after this B1-P report.**

FiQA inspected DEV: 57,638 documents, 500 queries, two encoder pairs and five seeds. Both regimes replace the same 28,819 paid IDs (anchors included); fitting uses either 1,024 anchor pairs or all 28,819 already-paid pairs. No method, lambda10/tangent2, quality threshold or case selection was changed after scoring.

All 124 rankings are sealed: 120 partial cells and four full references. 51 rankings were reused and 73 generated in R5. All ten all-paid converter fits passed. The original scorer failed before TSV parsing on duplicate exclusive receipt creation; its FAILED_PRESERVED metadata and logs remain unchanged. A separately committed, qrel-free-smoked CPU recovery scored the unchanged seal successfully.

## All-paid comparison

Five-seed means. Every partial row below uses the same 50% destination encoding budget and all 28,819 fitting pairs. References are separate operating points: Full-X uses the incumbent query/document encoder; Full-Y uses the target encoder throughout.

| Method | MiniLM to DistilRoBERTa nDCG@10 | Recall@100 | E5-small to E5-base nDCG@10 | Recall@100 |
|---|---:|---:|---:|---:|
| A2M / global Procrustes adaptation | 0.333386 | 0.690495 | 0.336202 | 0.653389 |
| ARC2-Global | 0.367146 | 0.692200 | 0.291867 | 0.559490 |
| LA2M, 20 clusters (adaptation) | 0.338923 | 0.695005 | 0.329341 | 0.647331 |
| SimpleLinear official code (5-layer MLP) | 0.332316 | 0.677789 | 0.167949 | 0.361785 |
| Affine ridge, lambda10 (bias regularized) | 0.367263 | 0.680043 | 0.227015 | 0.424511 |
| Embedding-Converter paper-spec adaptation | 0.325761 | 0.663269 | 0.262519 | 0.578907 |
| Full-X reference | 0.389961 | 0.700184 | 0.346478 | 0.645332 |
| Full-Y reference | 0.404736 | 0.703892 | 0.389133 | 0.696797 |

## Matched all-paid nDCG contrasts

ARC2-Global minus each baseline. Intervals use the predeclared 32-contrast Bonferroni family (approximate 95% family coverage; 99.84375% per interval). An interval crossing zero is unresolved, not equivalence.

| Pair | Baseline | Delta nDCG | Family interval | Interpretation |
|---|---|---:|---|---|
| MiniLM | A2M / global Procrustes adaptation | +0.033760 | [+0.018645, +0.050408] | above_zero |
| MiniLM | LA2M, 20 clusters (adaptation) | +0.028223 | [+0.010129, +0.047297] | above_zero |
| MiniLM | SimpleLinear official code (5-layer MLP) | +0.034830 | [+0.023544, +0.047191] | above_zero |
| MiniLM | Affine ridge, lambda10 (bias regularized) | -0.000117 | [-0.007540, +0.006532] | unresolved |
| MiniLM | Embedding-Converter paper-spec adaptation | +0.041385 | [+0.023614, +0.060969] | above_zero |
| E5 | A2M / global Procrustes adaptation | -0.044335 | [-0.079696, -0.009272] | below_zero |
| E5 | LA2M, 20 clusters (adaptation) | -0.037474 | [-0.070583, -0.003758] | below_zero |
| E5 | SimpleLinear official code (5-layer MLP) | +0.123918 | [+0.093821, +0.156724] | above_zero |
| E5 | Affine ridge, lambda10 (bias regularized) | +0.064852 | [+0.043521, +0.089349] | above_zero |
| E5 | Embedding-Converter paper-spec adaptation | +0.029348 | [-0.015573, +0.074762] | unresolved |

## Effect of additional fitting pairs on ARC2-Global

Encoding budget stays 50%; only the fitting-pair count changes. Recall intervals below are nominal 95% descriptive intervals, outside the nDCG family correction.

| Pair | Fixed1,024 nDCG | All-paid nDCG | Delta nDCG [family interval] | Delta Recall [descriptive95] |
|---|---:|---:|---|---|
| minilm_distilroberta | 0.307505 | 0.367146 | +0.059641 [+0.039341, +0.080604] | +0.015631 [+0.002193, +0.029359] |
| e5_small_base | 0.311635 | 0.291867 | -0.019768 [-0.056330, +0.016637] | -0.061435 [-0.083203, -0.040108] |

## Supported conclusions and limits

- MiniLM: all-paid ARC2 has higher nDCG than Procrustes, LA2M, official-code SimpleLinear and the converter, with all four family intervals above zero. Its nDCG difference from affine ridge is unresolved. Recall is higher than ridge descriptively; this does not establish nDCG equivalence or overall dominance.
- E5: all-paid ARC2 trails Procrustes and LA2M in the nDCG family comparisons, exceeds SimpleLinear/ridge, and is unresolved against the converter. Its all-paid nDCG mean is below fixed-anchor ARC2, with that family interval unresolved; Recall decreases with a negative descriptive interval. More fitting pairs are not uniformly beneficial.
- MiniLM fixed-anchor ARC2 trails every all-paid baseline in the locked cross-regime nDCG comparisons. Thus fixed-anchor comparisons alone do not establish superiority over baselines trained on all already-paid pairs.
- ARC2 means remain below both Full-X and Full-Y on both metrics in both encoder pairs/regimes. All methods, both regimes, references and all 32 contrast signs remain reported.
- This is development evidence with encoder-dependent strengths. It establishes neither an independent paper win nor a dollar saving, physical migration cost, SLO benefit, universal best method or D1 admission. No method switch is selected here.

## Evidence and next action

Generation: `7530c8e`; recovery orchestrator: `4062d96`. Unchanged original metric/bootstrap sources; 20,000 shared query resamples after five-seed averaging. Local QA recomputed all 28 means, 32 contrast deltas and 96 intervals; largest difference was 2.22e-16.

[Complete fixed/all-paid means, seed variation and all 32 nDCG/Recall contrasts](scoring/results_summary.md), [machine-readable results](scoring/results_summary.json), [per-query output](scoring/per_query.npy), [generation inventory](full_manifest.json). Large weights/proxies stay remote; this local bundle contains all rankings, IDs, selections, metrics and logs. Cached-vector encodes are not a physical deployment cost measurement.

B1-P is complete. Next planned item is B1-G mixed-gallery diagnostics, followed by D1. Both await user instruction; no breadth, TREC, systems or claim-audit job was launched.
