# B1c R3 complete six-method development report

**COMPLETE; 736 scored rankings, 144 partial condition means, 16 native references, 120 matched condition contrasts.**

Four inspected DEV collections (FiQA: 57,638 documents / 500 queries; NanoNQ: 5,035 / 50; NanoHotpotQA: 5,090 / 50; NanoFEVER: 4,996 / 50), two encoder pairs, five seeds (17, 29, 41, 53, 67), and 25% / 50% / 75% budgets. All six methods use the same fixed 1,024 anchor pairs. Unique logical destination document exposure is |A ∪ S|; anchors count. No new physical document encoding was performed in this recovery.

R3 retains 378 frozen rankings and adds 358 sealed rankings from 118 fresh fits plus two saved fits. The 38 displaced historical FiQA cells and failed/interrupted attempts remain preserved; the prospective R3 cells consistently replace each affected gallery at all three budgets. The separate scorer opened only the four locked DEV sources after the complete seal. TREC remains closed.

[Quality–budget figure](figures/b1c_r3_quality_budget.pdf) · [PNG](figures/b1c_r3_quality_budget.png) · [SVG](figures/b1c_r3_quality_budget.svg) · [Recall counterpart](figures/b1c_r3_recall_budget.pdf) · [Macro intervals and every condition delta](figures/b1c_r3_macro_and_condition_deltas.pdf)

The quality figure shows all six methods and native Full-X / Full-Y references across all eight dataset/pair panels. Each curve is a five-seed mean; panel y-ranges differ. Native Full-X uses the incumbent query/document encoder; native Full-Y uses the target encoder throughout. These are separate full-corpus reference operating points, and Full-Y is not a mathematical upper bound.

## Predeclared macro comparison

ARC2 minus each baseline, equally weighting all 24 dataset × pair × budget conditions after averaging the five mapping seeds. Every nDCG interval below is the saved 99% percentile interval for the predeclared five-comparison Bonferroni family (approximate 95% family coverage). Recall intervals are nominal 95% descriptive. The 20,000 draws independently resample queries within datasets and share each dataset’s query indices across pairs, budgets, methods and metrics. No p-values or new uncertainty calculations are introduced.

| ARC2 minus baseline | Δ nDCG@10 [99% family interval] | Δ Recall@100 [descriptive 95%] |
|---|---:|---:|
| A2M / Procrustes adaptation | +0.024325 [+0.018132, +0.030792] | -0.000239 [-0.004944, +0.004336] |
| LA2M20 adaptation | +0.104055 [+0.086070, +0.122915] | +0.090028 [+0.075394, +0.105760] |
| SimpleLinear official code (5-layer MLP) | +0.172100 [+0.149862, +0.194703] | +0.252882 [+0.236538, +0.269462] |
| Affine ridge, lambda10 | +0.095653 [+0.075405, +0.116427] | +0.121734 [+0.103216, +0.141376] |
| Embedding-Converter adaptation | +0.161162 [+0.142686, +0.179916] | +0.101758 [+0.087364, +0.116912] |

All five macro nDCG family intervals are above zero. This supports a fixed-supervision development advantage averaged over the locked matrix. It does not imply dominance in each condition, an independent confirmation, or superiority under all-paid supervision.

## All condition signs retained

Counts compare point means across the 24 matched conditions per baseline; they are descriptive higher/lower/tied counts, not 120 family-tested wins. Exact zero defines a tie.

| Baseline | nDCG higher / lower / tied | Recall higher / lower / tied |
|---|---:|---:|
| A2M / Procrustes adaptation | 23 / 1 / 0 | 11 / 12 / 1 |
| LA2M20 adaptation | 24 / 0 / 0 | 24 / 0 / 0 |
| SimpleLinear official code (5-layer MLP) | 24 / 0 / 0 | 24 / 0 / 0 |
| Affine ridge, lambda10 | 24 / 0 / 0 | 24 / 0 / 0 |
| Embedding-Converter adaptation | 24 / 0 / 0 | 24 / 0 / 0 |

### Encoder-pair macro deltas

Equal-weight descriptive averages of the saved condition deltas; no new intervals or tests.

| Scope | Baseline | Δ nDCG@10 | Δ Recall@100 |
|---|---|---:|---:|
| MiniLM → DistilRoBERTa | Procrustes | +0.025733 | +0.007177 |
| E5-small → E5-base | Procrustes | +0.022917 | -0.007654 |
| MiniLM → DistilRoBERTa | LA2M20 | +0.084349 | +0.093043 |
| E5-small → E5-base | LA2M20 | +0.123761 | +0.087012 |
| MiniLM → DistilRoBERTa | SimpleLinear | +0.122800 | +0.110114 |
| E5-small → E5-base | SimpleLinear | +0.221399 | +0.395650 |
| MiniLM → DistilRoBERTa | Ridge | +0.024284 | +0.042623 |
| E5-small → E5-base | Ridge | +0.167022 | +0.200846 |
| MiniLM → DistilRoBERTa | Converter | +0.084113 | +0.073500 |
| E5-small → E5-base | Converter | +0.238212 | +0.130015 |

### Dataset macro deltas

Equal-weight descriptive averages of the saved condition deltas; no new intervals or tests.

| Scope | Baseline | Δ nDCG@10 | Δ Recall@100 |
|---|---|---:|---:|
| NanoNQ | Procrustes | +0.026864 | +0.001333 |
| NanoHotpotQA | Procrustes | +0.031572 | -0.000667 |
| NanoFEVER | Procrustes | +0.028953 | +0.001111 |
| FiQA | Procrustes | +0.009912 | -0.002732 |
| NanoNQ | LA2M20 | +0.102127 | +0.044333 |
| NanoHotpotQA | LA2M20 | +0.106531 | +0.056333 |
| NanoFEVER | LA2M20 | +0.128928 | +0.075000 |
| FiQA | LA2M20 | +0.078633 | +0.184444 |
| NanoNQ | SimpleLinear | +0.197443 | +0.243000 |
| NanoHotpotQA | SimpleLinear | +0.165331 | +0.252000 |
| NanoFEVER | SimpleLinear | +0.228041 | +0.227556 |
| FiQA | SimpleLinear | +0.097585 | +0.288973 |
| NanoNQ | Ridge | +0.088005 | +0.103000 |
| NanoHotpotQA | Ridge | +0.124570 | +0.136667 |
| NanoFEVER | Ridge | +0.078496 | +0.063444 |
| FiQA | Ridge | +0.091542 | +0.183827 |
| NanoNQ | Converter | +0.170441 | +0.063333 |
| NanoHotpotQA | Converter | +0.201368 | +0.069000 |
| NanoFEVER | Converter | +0.158818 | +0.072111 |
| FiQA | Converter | +0.114021 | +0.202586 |

## Interpretation and preserved limits

- ARC2 partial-condition nDCG means are below native Full-X in 24/24 conditions and Full-Y in 24/24. Recall exceeds Full-X in 8/24 conditions and Full-Y in 1/24, so these references are not upper bounds. FiQA / E5 / 75% is the sole negative ARC2-minus-Procrustes nDCG point contrast (-0.003583). The E5 Recall macro difference versus Procrustes is -0.007654; the overall Recall difference is -0.000239 with a descriptive interval crossing zero. Every negative condition contrast remains in the full tables and figure data.
- The existing [FiQA all-paid B1-P experiment](../b1p_r5_review_20261027/SUMMARY.md) remains material: E5 all-paid ARC2 trails Procrustes and LA2M in family nDCG comparisons; MiniLM versus all-paid ridge is unresolved. Additional fitting pairs are not uniformly beneficial. B1c fixed-anchor averages do not erase that evidence.
- Procrustes is a mathematical A2M adaptation; LA2M20 is an integration-script adaptation. SimpleLinear uses pinned official code with the five-layer MLP and final 50 epochs. Embedding-Converter is a paper-spec adaptation with 1,024 paired anchors. These are qualified implementations, not original-paper reproduction claims.
- ARC2 stays centered rectangular Procrustes with lambda=10 and exactly two tangent updates, without local residual or neural fitting. No post-score method, seed, budget or subset selection was performed.
- Fit/map/search resource receipts reflect shared-load execution on the recorded H100 MIG instance. They do not establish isolated accelerator performance, physical dollar savings, real-traffic behavior, SLO improvement or a causal explanation of mixed-gallery effects.

## Complete tables and provenance

[All 144 partial means and 16 references](condition_means.csv) · [All 120 matched condition contrasts](condition_contrasts.csv) · [Five macro contrasts](macro_contrasts.csv) · [Derived descriptive analysis](derived_analysis.json) · [Frozen scorer summary](evidence/run/scoring/summary.json) · [Rendering provenance](figures/b1c_r3_render_provenance.json)

CSV means retain mapping-seed SD/range, saved nominal query-bootstrap intervals, Full-Y retention and deltas. All queries count, including zero-positive queries; nDCG@10 uses graded 2^rel−1 gain, and Recall@100 divides by all positive qrels, including positives outside a Nano corpus. Condition intervals are nominal 95% descriptive, outside the five macro nDCG family. An interval crossing or touching zero is unresolved, not evidence of equivalence.

Scorer commit: `61f73171b1869a186648aadd88f1b6f81a61376b`. Lock SHA256: `f567a4b6267baef3c59de1aca750d19ba3479d228109f7d098fd45d26586830d`. Ranking seal SHA256: `a60b352dd1bb19b4f35783ce5c5172aea6ab3bbc9d4691c740320883dd2bae88`.

**STOP after the separately recorded final D1 review. No B2, TREC, systems campaign or method switch is authorized here.**
