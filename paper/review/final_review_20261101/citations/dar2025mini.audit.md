# dar2025mini — KEEP

Fresh live-primary audit, 2026-11-01. **Same-family/provisional; high confidence.**

Existence verified. Author: **Guy Dar**. Title: **mini-vec2vec: Scaling Universal Geometry Alignment with Linear Transformations**. The supplied `misc` entry matches the [current arXiv BibTeX export](https://arxiv.org/bibtex/2510.02348), including **2026**, identifier `2510.02348`, and `cs.CL`. No conference/journal venue is verified or should be invented.

The [original submission](https://arxiv.org/abs/2510.02348v1) is **v1, 27 September 2025**; the [latest record](https://arxiv.org/abs/2510.02348) is **v4, 17 February 2026**. Thus 2026 is correct for the supplied latest-version entry. The internal key `dar2025mini` need not change. DOI: `10.48550/arXiv.2510.02348`.

| Use | Verdict | Evidence and reason |
| --- | --- | --- |
| `sections/related-work.tex:23` — pseudo-pairs, Procrustes, matching and clustering refinements | **SUPPORTS** | [Latest primary method, sections 3.2–3.4 and Listings 1–2](https://arxiv.org/html/2510.02348v4): cluster-based relative representations construct pseudo-pairs; Procrustes fits the map; nearest-neighbor matching and smoothed Procrustes updates iterate; clustering refinement follows. |

**Required fix: none.** Optional precision: write “iterative matching refinement, and a clustering-based refinement.” The latter is one pass in v4, not a repeatedly iterated stage.

Only the supplied entry/context and live primary sources were audited. This citation establishes method ingredients, not evidence for ARC2's empirical claims. No manuscript edits or experiments were performed.
