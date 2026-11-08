# B2: independent TREC-COVID fixed-anchor confirmation

Completed one-shot final scoring: `FINAL_SCORED`; **11/30 primary contrasts support improvement, 19/30 remain unresolved, 0/30 support worse performance** under the locked family intervals.

Confirmed improvements occur against Converter (5/6), affine ridge (4/6), and SimpleLinear (2/6) under the locked configurations. All six ARC2-minus-Procrustes nDCG means are negative and all six family intervals cross zero. These unresolved comparisons do not demonstrate equality, noninferiority or equivalence. The result remains conditional on the declared configurations; no method switch follows automatically.

## Evidence and scope

- Full TREC-COVID: 171,332 documents, all 50 queries, two encoder migrations, seeds 17/29/41/53/67, six methods, three paid budgets.
- Complete 184 exact-search rankings: 180 partial endpoints from 60 fits plus four native Full-X/Full-Y references. Exactly 1,024 paired anchors per fit.
- Charge unique destination documents as |A ∪ S|, including anchors: 42,833 / 85,666 / 128,499 (25/50/75%). Nonanchor paid rows add no fitting pairs.
- nDCG@10 uses graded gain 2^rel−1; Recall@100 includes all positive judgments in its denominator; unjudged documents are nonrelevant. No query filtering.
- The locked 30 primary nDCG contrasts use 20,000 paired query bootstrap draws, PCG64 seed 20261031, with five mapping seeds averaged first. Each percentile interval has ~99.8333% individual coverage for approximate 95% Bonferroni family coverage. There are 50 query units, not 250 independent observations.
- Recall intervals and condition-mean intervals are nominal 95% descriptive. No new interval, post-hoc macro test, p-value or equivalence margin is introduced by this report.
- Full native references use their own native queries and documents; mixed-gallery methods use destination queries. They are contextual references, not extra primary contrasts.

## Primary results by declared baseline

| Migration | Baseline configuration | Above zero | Unresolved | Below zero | Negative nDCG means |
|---|---|---:|---:|---:|---:|
| MiniLM → DistilRoBERTa | A2M / centered Procrustes adaptation | 0 | 3 | 0 | 3 |
| MiniLM → DistilRoBERTa | LA2M20 integration-script adaptation | 0 | 3 | 0 | 2 |
| MiniLM → DistilRoBERTa | SimpleLinear official code, final50, 5-layer MLP | 0 | 3 | 0 | 1 |
| MiniLM → DistilRoBERTa | Affine ridge, lambda10, regularized bias | 1 | 2 | 0 | 0 |
| MiniLM → DistilRoBERTa | Embedding-Converter paper-spec adaptation | 2 | 1 | 0 | 0 |
| E5-small → E5-base | A2M / centered Procrustes adaptation | 0 | 3 | 0 | 3 |
| E5-small → E5-base | LA2M20 integration-script adaptation | 0 | 3 | 0 | 1 |
| E5-small → E5-base | SimpleLinear official code, final50, 5-layer MLP | 2 | 1 | 0 | 0 |
| E5-small → E5-base | Affine ridge, lambda10, regularized bias | 3 | 0 | 0 | 0 |
| E5-small → E5-base | Embedding-Converter paper-spec adaptation | 3 | 0 | 0 | 0 |

All negative and unresolved outcomes are retained below and in the CSV files. Above/below zero refer only to the primary family interval, not a mean sign.

## All 40 condition means and native references

Values are mean ± mapping-seed sample SD; native references have one deterministic ranking and no mapping-seed SD. Nominal 95% query-bootstrap intervals, seed min/max, native-reference differences and Full-Y retention are in [all_means.csv](tables/all_means.csv). ARC2 is numerically below native Full-Y in all six conditions on both metrics; these reference differences are descriptive and have no new inferential test.

### MiniLM → DistilRoBERTa

| Budget | Method | nDCG@10 ± seed SD | Recall@100 ± seed SD |
|---|---|---:|---:|
| 25% | ARC2-Global | 0.46191 ± 0.01286 | 0.08963 ± 0.00093 |
| 25% | A2M / centered Procrustes adaptation | 0.46196 ± 0.01871 | 0.08657 ± 0.00150 |
| 25% | LA2M20 integration-script adaptation | 0.46342 ± 0.02098 | 0.07357 ± 0.00145 |
| 25% | SimpleLinear official code, final50, 5-layer MLP | 0.46104 ± 0.02184 | 0.06257 ± 0.00129 |
| 25% | Affine ridge, lambda10, regularized bias | 0.43217 ± 0.02285 | 0.06890 ± 0.00068 |
| 25% | Embedding-Converter paper-spec adaptation | 0.42237 ± 0.02646 | 0.06512 ± 0.00187 |
| 50% | ARC2-Global | 0.49996 ± 0.01179 | 0.09529 ± 0.00121 |
| 50% | A2M / centered Procrustes adaptation | 0.50462 ± 0.01516 | 0.09349 ± 0.00143 |
| 50% | LA2M20 integration-script adaptation | 0.50728 ± 0.01666 | 0.08842 ± 0.00154 |
| 50% | SimpleLinear official code, final50, 5-layer MLP | 0.50759 ± 0.01648 | 0.08448 ± 0.00142 |
| 50% | Affine ridge, lambda10, regularized bias | 0.48544 ± 0.01676 | 0.07799 ± 0.00106 |
| 50% | Embedding-Converter paper-spec adaptation | 0.47805 ± 0.01919 | 0.07717 ± 0.00129 |
| 75% | ARC2-Global | 0.51951 ± 0.01352 | 0.09984 ± 0.00050 |
| 75% | A2M / centered Procrustes adaptation | 0.51954 ± 0.01441 | 0.09943 ± 0.00061 |
| 75% | LA2M20 integration-script adaptation | 0.51856 ± 0.01323 | 0.09827 ± 0.00088 |
| 75% | SimpleLinear official code, final50, 5-layer MLP | 0.51930 ± 0.01386 | 0.09702 ± 0.00077 |
| 75% | Affine ridge, lambda10, regularized bias | 0.50122 ± 0.01400 | 0.08564 ± 0.00071 |
| 75% | Embedding-Converter paper-spec adaptation | 0.50325 ± 0.01554 | 0.08920 ± 0.00145 |
| full | Full-X | 0.49348 (native) | 0.09355 (native) |
| full | Full-Y | 0.52027 (native) | 0.10521 (native) |

### E5-small → E5-base

| Budget | Method | nDCG@10 ± seed SD | Recall@100 ± seed SD |
|---|---|---:|---:|
| 25% | ARC2-Global | 0.56280 ± 0.01796 | 0.08658 ± 0.00193 |
| 25% | A2M / centered Procrustes adaptation | 0.56604 ± 0.01724 | 0.08857 ± 0.00189 |
| 25% | LA2M20 integration-script adaptation | 0.52059 ± 0.01915 | 0.05933 ± 0.00168 |
| 25% | SimpleLinear official code, final50, 5-layer MLP | 0.42993 ± 0.03475 | 0.02964 ± 0.00298 |
| 25% | Affine ridge, lambda10, regularized bias | 0.29862 ± 0.01041 | 0.03726 ± 0.00085 |
| 25% | Embedding-Converter paper-spec adaptation | 0.30557 ± 0.01606 | 0.04225 ± 0.00107 |
| 50% | ARC2-Global | 0.59041 ± 0.01707 | 0.09284 ± 0.00151 |
| 50% | A2M / centered Procrustes adaptation | 0.60673 ± 0.01133 | 0.09758 ± 0.00107 |
| 50% | LA2M20 integration-script adaptation | 0.58981 ± 0.01129 | 0.08234 ± 0.00111 |
| 50% | SimpleLinear official code, final50, 5-layer MLP | 0.52868 ± 0.01613 | 0.05097 ± 0.00349 |
| 50% | Affine ridge, lambda10, regularized bias | 0.32814 ± 0.00923 | 0.03822 ± 0.00090 |
| 50% | Embedding-Converter paper-spec adaptation | 0.35902 ± 0.01652 | 0.04951 ± 0.00088 |
| 75% | ARC2-Global | 0.60978 ± 0.01352 | 0.09967 ± 0.00124 |
| 75% | A2M / centered Procrustes adaptation | 0.61979 ± 0.01365 | 0.10606 ± 0.00067 |
| 75% | LA2M20 integration-script adaptation | 0.61878 ± 0.01414 | 0.10159 ± 0.00068 |
| 75% | SimpleLinear official code, final50, 5-layer MLP | 0.57849 ± 0.01383 | 0.06928 ± 0.00366 |
| 75% | Affine ridge, lambda10, regularized bias | 0.32778 ± 0.01405 | 0.03657 ± 0.00121 |
| 75% | Embedding-Converter paper-spec adaptation | 0.40983 ± 0.01073 | 0.05824 ± 0.00094 |
| full | Full-X | 0.68054 (native) | 0.12353 (native) |
| full | Full-Y | 0.64211 (native) | 0.11624 (native) |

## All 30 ARC2-minus-baseline contrasts

nDCG intervals below are the primary ~99.8333% individual intervals (approximate 95% 30-comparison family). Recall intervals are nominal 95% descriptive. Seed delta SD/range and nominal nDCG intervals are retained in [all_contrasts.csv](tables/all_contrasts.csv).

### MiniLM → DistilRoBERTa

| Budget | Baseline | Δ nDCG@10 | Primary interval | Decision | Δ Recall@100 | Descriptive 95% interval |
|---|---|---:|---|---|---:|---|
| 25% | Procrustes adaptation | -0.00005 | [-0.01469, +0.01321] | unresolved | +0.00306 | [+0.00173, +0.00455] |
| 25% | LA2M20 adaptation | -0.00150 | [-0.03431, +0.02908] | unresolved | +0.01606 | [+0.01031, +0.02296] |
| 25% | SimpleLinear (official code) | +0.00087 | [-0.03294, +0.03255] | unresolved | +0.02706 | [+0.01950, +0.03586] |
| 25% | Affine ridge | +0.02974 | [-0.00448, +0.06833] | unresolved | +0.02073 | [+0.01528, +0.02665] |
| 25% | Converter adaptation | +0.03954 | [+0.00063, +0.07561] | above_zero | +0.02451 | [+0.01893, +0.03073] |
| 50% | Procrustes adaptation | -0.00467 | [-0.01862, +0.00610] | unresolved | +0.00181 | [+0.00067, +0.00299] |
| 50% | LA2M20 adaptation | -0.00732 | [-0.02668, +0.00714] | unresolved | +0.00687 | [+0.00384, +0.01015] |
| 50% | SimpleLinear (official code) | -0.00764 | [-0.02740, +0.00692] | unresolved | +0.01081 | [+0.00728, +0.01473] |
| 50% | Affine ridge | +0.01452 | [-0.01080, +0.04210] | unresolved | +0.01730 | [+0.01246, +0.02312] |
| 50% | Converter adaptation | +0.02191 | [+0.00052, +0.04264] | above_zero | +0.01812 | [+0.01431, +0.02237] |
| 75% | Procrustes adaptation | -0.00002 | [-0.00450, +0.00438] | unresolved | +0.00041 | [-0.00046, +0.00130] |
| 75% | LA2M20 adaptation | +0.00095 | [-0.00612, +0.00878] | unresolved | +0.00157 | [+0.00029, +0.00293] |
| 75% | SimpleLinear (official code) | +0.00021 | [-0.00683, +0.00802] | unresolved | +0.00282 | [+0.00153, +0.00422] |
| 75% | Affine ridge | +0.01829 | [+0.00044, +0.04492] | above_zero | +0.01420 | [+0.01026, +0.01886] |
| 75% | Converter adaptation | +0.01626 | [-0.00004, +0.03208] | unresolved | +0.01064 | [+0.00856, +0.01288] |

### E5-small → E5-base

| Budget | Baseline | Δ nDCG@10 | Primary interval | Decision | Δ Recall@100 | Descriptive 95% interval |
|---|---|---:|---|---|---:|---|
| 25% | Procrustes adaptation | -0.00324 | [-0.02162, +0.01432] | unresolved | -0.00199 | [-0.00329, -0.00068] |
| 25% | LA2M20 adaptation | +0.04221 | [-0.00642, +0.09332] | unresolved | +0.02725 | [+0.01989, +0.03546] |
| 25% | SimpleLinear (official code) | +0.13287 | [+0.06330, +0.20514] | above_zero | +0.05694 | [+0.04632, +0.06839] |
| 25% | Affine ridge | +0.26418 | [+0.15726, +0.37676] | above_zero | +0.04932 | [+0.03746, +0.06252] |
| 25% | Converter adaptation | +0.25723 | [+0.17573, +0.33757] | above_zero | +0.04433 | [+0.03449, +0.05524] |
| 50% | Procrustes adaptation | -0.01632 | [-0.03982, +0.00230] | unresolved | -0.00473 | [-0.00644, -0.00312] |
| 50% | LA2M20 adaptation | +0.00059 | [-0.03551, +0.03600] | unresolved | +0.01050 | [+0.00667, +0.01476] |
| 50% | SimpleLinear (official code) | +0.06173 | [+0.01356, +0.11446] | above_zero | +0.04187 | [+0.03310, +0.05164] |
| 50% | Affine ridge | +0.26227 | [+0.15796, +0.37285] | above_zero | +0.05463 | [+0.04210, +0.06822] |
| 50% | Converter adaptation | +0.23138 | [+0.15672, +0.30851] | above_zero | +0.04333 | [+0.03441, +0.05292] |
| 75% | Procrustes adaptation | -0.01001 | [-0.02601, +0.00363] | unresolved | -0.00639 | [-0.00876, -0.00432] |
| 75% | LA2M20 adaptation | -0.00900 | [-0.03578, +0.01565] | unresolved | -0.00192 | [-0.00453, +0.00048] |
| 75% | SimpleLinear (official code) | +0.03129 | [-0.00383, +0.07170] | unresolved | +0.03038 | [+0.02219, +0.03986] |
| 75% | Affine ridge | +0.28200 | [+0.17480, +0.39733] | above_zero | +0.06310 | [+0.05016, +0.07663] |
| 75% | Converter adaptation | +0.19995 | [+0.13925, +0.26422] | above_zero | +0.04143 | [+0.03301, +0.05060] |

## Figures and reproducibility

- [nDCG@10 versus paid destination coverage](figures/b2_ndcg10_vs_budget.pdf) ([PNG](figures/b2_ndcg10_vs_budget.png), [SVG](figures/b2_ndcg10_vs_budget.svg)).
- [Recall@100 versus paid destination coverage](figures/b2_recall100_vs_budget.pdf) ([PNG](figures/b2_recall100_vs_budget.png), [SVG](figures/b2_recall100_vs_budget.svg)).
- [All 30 primary contrasts](figures/b2_all30_primary_contrasts.pdf) ([PNG](figures/b2_all30_primary_contrasts.png), [SVG](figures/b2_all30_primary_contrasts.svg)).
- [All 184 ranking-level seed means](tables/seed_means.csv), [primary sign/interval counts](tables/primary_counts.csv), [all negative contrasts](tables/negative_contrasts.csv).
- Exact saved summary SHA256: `646b1f535db1138dc51a2d8d1296b97de89ba8354ead9f88e45080c9cb5f18c7`.
- Independent computational QA: [qa_completed_20261101T020214554697Z.json](qa_completed_20261101T020214554697Z.json), SHA256 `cdd654c401cd51efc3177fc8b6a40bbc60d346768417a9db2cd8699298110e42`. This compact verification does not claim regeneration of the remote encoder outputs, fit checkpoints or exact endpoints.
- Rendering provenance and artifact hashes: [render_provenance.json](render_provenance.json). Visual inspection is recorded separately in [visual_qa.json](visual_qa.json).

## Baseline qualifications and limits

ARC2 is the frozen centered rectangular Procrustes initialization, lambda10 and exactly two tangent updates; there is no local residual or neural mapper. A2M/Procrustes is the centered affine adaptation. LA2M20 uses 20 source-anchor clusters and the integration-script singleton fallback. SimpleLinear uses pinned official code, a five-layer MLP and final50 epochs. Ridge regularizes the affine bias at lambda10. Embedding-Converter is the locked paper-spec adaptation with 50,000 selection iterations and a fresh selected-length refit on all 1,024 anchors; anchor validation MAE, never final qrels, selected training length. These labels do not claim full original-paper reproduction.

The independent test is conditional on this dataset, the two pinned encoder migrations, the fixed 1,024-anchor fitting regime and 128-token encoder setting. It does not test one-versus-two tangent necessity, all-paid supervision, an optimal anchor budget, ANN behavior, measured deployment cost, isolated hardware speed, SLOs or real traffic. Full destination caches were physically prepared for evaluation; the charged partial exposure does not demonstrate physical encoding savings. Shared execution timing is not an isolated performance benchmark.

**STOP after the authorized B2 result review and ARIS analysis. Manuscript unchanged; no automatic systems run, new dataset, retuning or submission-facing method switch.**
