# ARC2-Global: compact mapping, stronger retrieval

> ARC2-Global combines a compact affine document adapter with two closed-form tangent corrections for staged embedding-index migration. With 1,024 paired fitting documents, it improves aggregate nDCG@10 over five declared baseline configurations on four development collections and achieves prospective TREC-COVID gains over the declared Converter, affine-ridge and SimpleLinear configurations.

Revision: **supervisor-review-20261101-r3-paper-story**. Method: `arc2_global_tangent2_r1`.

## The contribution

ARC2 turns paired old/new document embeddings into a forward adapter for the rest of an index. It starts with a centered Procrustes map and applies exactly two tangent ridge corrections (λ=10). The result is one affine map followed by vector normalization. Queries remain in the native destination space; newly encoded document vectors replace their proxies in the same gallery.

For 384→768 dimensions, the final map occupies **1.13 MiB** in float32. Its 295,680 coefficients are **114.7× smaller in parameter bytes** than the declared 33,927,168-parameter Converter MLP. ARC2 uses no neural training.

## The strongest evidence

| Evidence | Comparison and setting | Δ nDCG@10 | Saved family interval |
|---|---|---:|---|
| Broad development gain | ARC2 − Procrustes; four-collection DEV macro | **+0.024325** | [+0.018132, +0.030792] |
| The second correction contributes | Two tangent steps − one; DEV ablation | **+0.006924** | [+0.003809, +0.009959] |
| Matched all-paid evidence | ARC2 − Procrustes; FiQA/MiniLM, all-paid fitting, 50% budget | **+0.033760** | [+0.018645, +0.050408] |
| Prospective transfer gain | ARC2 − Converter; prospective TREC-COVID/E5, 25% budget | **+0.257234** | [+0.175731, +0.337569] |

The development gain spans NanoNQ, NanoHotpotQA, NanoFEVER and FiQA. The prospective TREC-COVID protocol confirms **11 improvements across 30 declared comparisons**. On E5, ARC2 has positive family intervals over both Converter and affine ridge at **25%, 50% and 75%** destination-document budgets.

The FiQA/MiniLM all-paid study adds a useful result: with the same 28,819 fitting pairs, ARC2 wins **four of five** external comparisons; the ridge comparison is unresolved. The benefit therefore appears beyond the 1,024-pair main setting.

## Why use it

ARC2 is a candidate when an embedding upgrade must be introduced gradually and a compact, non-neural document adapter is valuable. It combines a small final mapping with measured retrieval gains in the stated conditions, while fitting naturally into incremental vector replacement.

Results and parameter-storage figures refer to the stated models, fitting regimes and migration budgets. The [complete comparisons and deployment scope](EVIDENCE_GUIDE.md) accompany these highlights.

[Paper story](RESEARCH_STORY.md) · [Figures and full evidence](EVIDENCE_GUIDE.md) · [Reproduce](REPRODUCE.md)
