# Citation audit: driftadapter

Verdict: **KEEP**. Existence verified; supplied metadata matches. Confidence: high. Review independence: same-family. Acceptance status: provisional. Live lookup: 2026-11-01 08:22:58 UTC.

Harshil Vejendla is the sole author of *Drift-Adapter: A Practical Approach to Near Zero-Downtime Embedding Model Upgrades in Vector Databases*, EMNLP 2025 proceedings, pp. 15938–15949, DOI `10.18653/v1/2025.emnlp-main.805`. The cited version is the published main-conference paper (12-page publisher PDF). No bibliographic fix is required.

| Primary source opened live | Verified fact |
|---|---|
| [ACL record](https://aclanthology.org/2025.emnlp-main.805/) | Existence and publication metadata. |
| [Publisher BibTeX](https://aclanthology.org/2025.emnlp-main.805.bib) | All supplied bibliographic fields match; the local key is acceptable. |
| [Publisher PDF](https://aclanthology.org/2025.emnlp-main.805.pdf) | Sections 2.4–3, p. 15940: post-hoc fitting from paired document embeddings; new queries map to the legacy space and search its unchanged ANN index. The three families are Procrustes, low-rank affine, and residual MLP. |

| Citing context | Verdict | Reason |
|---|---|---|
| `sections/introduction.tex:7` | SUPPORTS | Supports the query-side branch of the joint citation. Document conversion is attributed separately to `embeddingconverter`; this audit does not validate that branch or the other citations. |
| `sections/related-work.tex:15` | SUPPORTS | Correct direction and adapter families. Paired document samples train a query-time map, rather than converting stored legacy documents into destination vectors. The paired-embedding/frozen-encoder comparison agrees with the post-hoc setup. |

The ARC2-specific statements require their own evidence and are outside this citation audit. No fix is needed.
