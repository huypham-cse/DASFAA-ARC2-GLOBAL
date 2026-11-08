# ARC2-Global: a compact adapter for staged embedding-index migration

## Problem and idea

An embedding-model upgrade creates a migration problem: queries can use the destination model immediately, while an existing document index still represents the source model. ARC2 learns from paired document embeddings and maps the remaining source vectors into the destination space. As backfill proceeds, true destination vectors replace proxies within a single gallery.

**Two closed-form corrections give the adapter its retrieval benefit.** ARC2 refines a centered Procrustes initialization with two tangent ridge updates. The correction targets the component of destination error perpendicular to the current predicted direction, aligning the fit with normalized-vector retrieval. The final adapter remains an affine map plus normalization.

## Contribution 1: preserve affine simplicity while improving retrieval

Across four inspected development collections, two encoder pairs and 25/50/75% migration budgets, ARC2 improves aggregate nDCG@10 over all five declared alternatives. Against Procrustes, the macro improvement is **+0.024325**, with saved 99% interval **[+0.018132, +0.030792]**. Each method uses the same 1,024 paired fitting documents in this comparison.

The ablation links that gain to the design: adding the second tangent step improves macro nDCG by **+0.006924** beyond one step, with family interval **[+0.003809, +0.009959]**. This supports a useful empirical contribution from the second correction.

## Contribution 2: carry benefits into a prospective collection

The sealed TREC-COVID evaluation covers 171,332 documents, two encoder pairs and 25/50/75% budgets. It confirms **11 family-adjusted improvements** over the declared baseline configurations. On E5-small→E5-base, ARC2 improves nDCG over Converter at each budget, by **+0.257234, +0.231385 and+0.199954**, and over affine ridge by **+0.264181, +0.262267 and+0.281997**. All six corresponding primary family intervals are positive.

![All declared methods and native references on TREC-COVID](results/b2_review_20261101/figures/b2_ndcg10_vs_budget.png)

These curves retain the full method panel; the gains above identify the conditions supporting the contribution. The test uses 30 primary contrasts and five mapping seeds, averaged before resampling 50 queries.

## Contribution 3: retain a compact, non-neural mapping artifact

For 384→768 dimensions, ARC2 stores **295,680 float32 coefficients, approximately 1.13 MiB**. The declared Converter MLP contains 33,927,168 parameters: ARC2's final mapping uses **114.7× fewer parameter bytes**. This is a final-weight comparison; ordinary affine ridge has the same affine coefficient count. Encoder execution, fitting workspace and index resources are separate from that quantity.

The all-paid FiQA experiment also demonstrates a positive operating point. For MiniLM→DistilRoBERTa at 50% migration, all methods receive 28,819 paired vectors. ARC2 reaches **0.367146 nDCG@10**, versus 0.333386 for Procrustes, 0.338923 for LA2M, 0.332316 for SimpleLinear and0.325761 for Converter. Those four paired family comparisons favor ARC2; ridge reaches 0.367263 with an unresolved comparison. This provides matched-supervision evidence for the adapter.

## Positioning the paper

The paper's central message is that a small closed-form forward adapter can produce useful retrieval gains during partial embedding migration. The main text can lead with the macro comparison, the two-step ablation, the prospective E5 curves and the all-paid MiniLM example. Baseline qualifications, complete outcome matrices, Recall and encoder-dependent behavior remain available through the full evidence guide.

Results and parameter-storage figures refer to the stated models, fitting regimes and migration budgets. The [complete comparisons and deployment scope](EVIDENCE_GUIDE.md) accompany these highlights.
