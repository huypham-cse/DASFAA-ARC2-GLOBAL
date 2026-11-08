# Current citation audit: minilm2020

Decision: **KEEP**. This is a citation-level decision, not a manuscript-wide PASS.

Audited current files on 2026-11-01T14:06:09.653752+00:00. Reviewer: gpt-6.1-sol, high; same-family review. No manuscript edits or scientific experiments were performed. No prior reviewer reports or old citation-context bundles were used as evidence.

| Axis | Finding | Decision |
|---|---|---|
| Existence | The live NeurIPS 2020 proceedings page identifies the paper and six authors. | KEEP |
| Metadata | The current entry matches the publisher BibTeX in author order, title, venue, volume 33, pages 5776?5788 and year 2020. Optional omitted fields are not errors. | KEEP |
| Context | The sole use is broad encoder-family/training background, supported by the paper's self-attention-distillation contribution. | KEEP |

The current entry is at `paper/references.bib:125?132`. Scanning every current `paper/sections/*.tex` file found exactly one use, at `related-work.tex:32`:

> Sentence-BERT, MiniLM, and E5 supply established encoder families and training approaches relevant to our model transitions.

The [NeurIPS primary page](https://proceedings.neurips.cc/paper/2020/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) and [publisher BibTeX](https://proceedings.neurips.cc/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Bibtex.bib) support the paper identity and architectural background. MiniLM's original compression method should be distinguished from later sentence-transformer fine-tuning. It does not itself establish the exact `all-MiniLM-L6-v2` sentence checkpoint.

`experimental-setup.tex:20?26` now names the exact migration and supplies pinned maintainer cards. The [MiniLM card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md) describes a 384-dimensional sentence encoder, initialized from `nreimers/MiniLM-L6-H384-uncased` and later contrastively fine-tuned on sentence pairs. The [destination card](https://huggingface.co/sentence-transformers/all-distilroberta-v1/resolve/842eaed40bee4d61673a81c92d5689a8fed7a09f/README.md) documents the 768-dimensional `all-distilroberta-v1` sentence encoder based on `distilroberta-base`. Thus the present wording has separate primary support for architecture background and checkpoint provenance. No required correction is identified.

Access limits: browser retrieval succeeded for the NeurIPS abstract and MiniLM blob page. Publisher BibTeX was rejected by the browser's content-type handler, and the destination blob/raw URLs returned browser access errors; direct HTTPS retrieval of the exact publisher/pinned resolve URLs succeeded (HTTP 200). Source retrieval hashes and timestamps are in the JSON. The full NeurIPS PDF was not inspected; the abstract and publisher BibTeX suffice for this limited background use.

Unverified scope: this audit does not compare experimental manifests or downloaded weight bytes with model revisions, validate runtime encoding settings, or audit empirical results. E5 cards were outside this single-entry audit. A maintainer card documents a model; it does not prove which bytes a scientific run loaded.

Current SHA256 hashes (all scanned section files included so the one-use count is bounded to these bytes):

| File | SHA256 |
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
