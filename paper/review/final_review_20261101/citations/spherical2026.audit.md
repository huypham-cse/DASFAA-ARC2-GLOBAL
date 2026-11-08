# Citation audit: spherical2026

Decision: **KEEP**. Existence: **verified** by live primary lookup on 2026-11-01. Confidence: **high**. Review independence: **same-family**; acceptance status: **provisional**.

The supplied BibTeX matches the live [arXiv export](https://arxiv.org/bibtex/2609.39836): *Spherical Interpolation for Backward-Compatible Multimodal Representations*, Simone Ricci, Niccolò Biondi, Federico Pernici, 2026, arXiv:2609.39836, cs.CV. The [record](https://arxiv.org/abs/2609.39836) lists v1, submitted September 30, 2026, and reports NeurIPS 2026 acceptance. Proceedings publication was not independently established; the existing arXiv `@misc` entry is accurate. No metadata correction is required.

| Use | Verdict | Reason |
| --- | --- | --- |
| `sections/related-work.tex:16` | **SUPPORTS** | Section 3, Eqs. (1)–(4), maps new queries into old coordinates with Procrustes, then SLERPs old and aligned-new queries. The old gallery stays fixed. Increasing alpha moves old → aligned-new. This supports the manuscript's direction and interpolation description. |

Primary method evidence: [versioned full text, Section 3](https://arxiv.org/html/2609.39836v1#S3). This is endpoint interpolation, not learned tangent regression. The adjacent ARC2 characterization is the manuscript's own method claim, outside what this citation establishes.

Required fix: **none**. Scope: supplied entry and its single supplied context; no prior reviews or cached source text used.
