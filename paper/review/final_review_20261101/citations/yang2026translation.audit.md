# yang2026translation ? KEEP

Existence: **YES**. Confidence: **high**. Same-family review; acceptance status: **provisional**. Reviewer: gpt-6.1-sol, high.

The [publisher record](https://proceedings.mlr.press/v306/yang26e.html) and its BibTeX confirm both authors, title, 2026, ICML 43, PMLR 306 and pages 144275?144302. The supplied entry matches. It cites the published proceedings version. No DOI is supplied or listed in that record; no correction is required.

| Occurrence | Verdict | Reason |
|---|---|---|
| `sections/related-work.tex:8` | SUPPORTS | The sentence accurately covers OOD translation, mixing/chaining, hierarchical experts and directional residual regularization. |

The [publisher PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/yang26e/yang26e.pdf), ?4.1?4.2 and Fig. 6 (PDF pp. 6?7), defines directions by PCA of target training embeddings. Mixing penalizes residual components orthogonal to PC1; chaining encourages propagated upstream error along PC1 and downstream residual along PC2. This is shared principal-direction residual shaping, not a per-anchor tangent target. The present sentence makes no contrary claim.

The PDF was downloaded live and matched the local fulltext PDF byte-for-byte: SHA-256 `38b35ae4755468e2619731e527d216792b936008e343c09e229c8e4f04856c05`. The relevant pages were extracted directly with pypdf. The web renderer could not parse the octet-stream PDF, but direct download succeeded.

Exact correction: **none**. Neighboring citations were outside this one-key audit. No bibliography/manuscript edits.
