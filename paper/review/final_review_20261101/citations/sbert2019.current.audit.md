# Current citation audit: sbert2019

Verdict: **KEEP**. Required action: none. Final read: 2026-11-01T14:08:34.078266+00:00.

Fresh single-entry review using gpt-6.1-sol/high. No prior reviewer opinions, delegation, experiments or manuscript edits.

| Axis | Result | Finding |
|---|---|---|
| Existence | PASS | Primary ACL record and published PDF confirm this is a real EMNLP-IJCNLP 2019 paper. |
| Metadata accuracy | PASS | Authors/order, title, proceedings, pages 3982-3992, 2019 year, entry type and DOI all match ACL canonical BibTeX. Missing optional month/address/publisher/URL/editor fields are not factual errors. |
| Contextual support | PASS | The sole current citation supplies Sentence-BERT family/training background. The primary paper describes sentence embeddings from BERT/RoBERTa using siamese/triplet training and similarity search. It does not document later all-MiniLM-L6-v2 or all-distilroberta-v1 checkpoints; current setup supplies separate pinned maintainer-card provenance. |

## Actual current context

`paper/sections/related-work.tex:32` ? family-level background:

Sentence-BERT, MiniLM, and E5 supply established encoder families and training approaches relevant to our model transitions~\cite{sbert2019,minilm2020,e52022}.

Exactly one `sbert2019` citation occurs in `paper/sections/*.tex`. The combined citation attributes Sentence-BERT, MiniLM and E5 to their corresponding family papers. It does not claim that the 2019 source introduced the later named checkpoints.

`paper/sections/experimental-setup.tex:20-28` separately names the migrations and links pinned maintainer model cards. The two Sentence-Transformers cards identify 384-dimensional MiniLM and 768-dimensional DistilRoBERTa outputs. The 2019 citation remains appropriate family-level background; checkpoint provenance belongs to those cards.

## Live primary sources and access limits

- [primary publisher record](https://aclanthology.org/D19-1410/): Live web fetch succeeded on 2026-11-01. Metadata and abstract inspected.
- [primary publisher BibTeX](https://aclanthology.org/D19-1410.bib): Live web fetch succeeded on 2026-11-01. Canonical export inspected.
- [primary published paper](https://aclanthology.org/D19-1410.pdf): Live web fetch succeeded; 11-page PDF text inspected, especially abstract/introduction and section 3.
- [pinned maintainer model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md): Live web fetch succeeded; identifies the named checkpoint and 384-dimensional outputs.
- [pinned maintainer model card](https://huggingface.co/sentence-transformers/all-distilroberta-v1/raw/842eaed40bee4d61673a81c92d5689a8fed7a09f/README.md): Browser tool failed for blob and raw URLs. Direct Python urllib HTTPS GET succeeded with HTTP 200; README identifies the named checkpoint and 768-dimensional outputs.

The 2019 paper cannot establish later checkpoint provenance. This audit does not verify E5 cards, downloaded weights, encoding code or experimental results. The DistilRoBERTa browser-access failure was resolved by a direct HTTPS read; the returned README SHA-256 is `565f15ef1c8232cf21b91aa9125bd852f54f2f676c662324732ee3d4d3a43a8c`.

## Final input hashes

All section files were scanned for occurrences. Relevant contexts were re-read before this report was written; no relevant content changed during the audit.

| File | SHA-256 |
|---|---|
| `paper/references.bib` | `c04d2e03b5df17f3e6e026bd7f8e7c942905055de4174c9a45f1fddeb7941de2` |
| `paper/sections/abstract.tex` | `c75dc88657f9b538f314b1787e75b08f9b3864f000a0f7e8b729effbe5f7d3d4` |
| `paper/sections/conclusion.tex` | `5ab2f71361be86ad2ddc5d4d21e00cc0a1ac869c900ef6546edba72be0b572b7` |
| `paper/sections/discussion.tex` | `834323c766a49b3b3874b660b9e6fdad3b660e8b5d93a5afeeae0c22fea01240` |
| `paper/sections/experimental-setup.tex` | `c6dfc7e773e6f448118013e5f11ec35eed6f849f7fb475bb1d690b1e07220828` |
| `paper/sections/introduction.tex` | `d67c836c50b51760cb279b62c1096a4b4a3e4498fa9e6b547df72d79cc27945f` |
| `paper/sections/method.tex` | `c4babc62dd94e8c6e2ccd6b921ea9d82db762ddf73df5c6efe71a3f022ce0e37` |
| `paper/sections/related-work.tex` | `bb47d22e21547ef1e96f4eb3634cda7039d2d6078082bae302d6507380a2b10f` |
| `paper/sections/results.tex` | `a8d76c0bc6ffcd14af3d461baf406837e3cd34a371585cd1e9754c28a64bafd3` |

Bibliographic optional fields could be added for completeness, but the current fields contain no correction requiring FIX, REPLACE or REMOVE.
