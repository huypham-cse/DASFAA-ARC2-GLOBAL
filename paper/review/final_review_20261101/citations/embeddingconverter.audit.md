# embeddingconverter

Existence: **YES**. Verdict: **KEEP**. Exact fix: none. Confidence: **high**.

The supplied authors, title, ACL 2025 proceedings, pages 25464–25482 and DOI match the [canonical publisher export](https://aclanthology.org/2025.acl-long.1237.bib). The [publisher record](https://aclanthology.org/2025.acl-long.1237/) and [published PDF](https://aclanthology.org/2025.acl-long.1237.pdf) were opened live on 2026-11-01. Version: published ACL proceedings, 19 pages. BibTeX's unaccented author spelling follows the publisher export.

| Use | Verdict | Reason |
|---|---|---|
| `sections/experimental-setup.tex:44` | SUPPORTS | Appendix B supports the cited training settings; Section 3.3 supports retrieval validation. MAE selection/refitting is explicitly an adaptation, with no reproduction claim. |
| `sections/introduction.tex:7` | SUPPORTS | Section 4.2 supports document-side conversion; query-side adaptation is assigned to the co-citation. |
| `sections/related-work.tex:5` | SUPPORTS | Sections 3.2 and 4.2 support document conversion with pointwise regression plus global and local similarity losses. |

Detailed metadata, evidence locations and scope limits are in `embeddingconverter.audit.json`. This verifies citation support, not execution of the local implementation.

Review independence: **same-family**. Acceptance status: **provisional**. No prior reviews, other models, subagents, experiments or qrels were consulted.
