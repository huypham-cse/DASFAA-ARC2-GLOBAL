# Current citation audit: `treccovid2020`

Decision: **KEEP**. Required changes: **none**. Fresh single-entry audit of the current bibliography and section sources, using live primary records. Requested reviewer configuration: gpt-6.1-sol / high.

| Axis | Verdict | Finding |
|---|---|---|
| Existence | PASS / KEEP | NIST hosts the matching article and Crossref returns ACM-deposited metadata for DOI `10.1145/3451964.3451965`. |
| Bibliographic accuracy | PASS / KEEP | Nine authors and their order, title, journal, 54(1), pages 1?12 and DOI match. The issue year is 2020; the online date is 19 February 2021. |
| Contextual support | PASS, scoped / KEEP | The one citation occurrence identifies TREC-COVID and co-cites BEIR for the benchmark release. Current wording separates external collection identity from this study's input manifest and chronology. |

## Current context and source scope

The only `treccovid2020` citation is at `paper/sections/experimental-setup.tex:16`, with `beir2021`. Lines 15?19 name the BEIR release, attribute 171,332 documents and 50 queries to its input manifest, then state this study's label/seal chronology separately.

The [NIST article](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=930360), pp. 1?2, establishes the collection's origin and biomedical retrieval task and explicitly describes an early-round snapshot. It need not verify a later study's execution chronology. Its [NIST record](https://www.nist.gov/publications/trec-covid-constructing-pandemic-information-retrieval-test-collection) records the online date; the PDF footer and [ACM-deposited Crossref metadata](https://api.crossref.org/works/10.1145/3451964.3451965) support the 2020 issue year. Crossref stores the full title in title/subtitle fields.

The co-cited [BEIR paper](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Paper-round2.pdf), Table 1, and [maintainer dataset metadata](https://huggingface.co/datasets/BeIR/trec-covid/raw/main/README.md) identify the BEIR collection and report 171,332 documents / 50 queries. The [maintainer repository](https://github.com/beir-cellar/beir) agrees on release identity. These records corroborate the declared release size; local manifest completeness was not audited.

All other TREC-COVID mentions in abstract, introduction, setup, results and discussion concern this study's design or outcomes. They are not presented as results from the cited 2020 article. No external citation mismatch was found. This verdict does **not** certify the local prospective chronology or numerical findings.

## Access and audit limits

The ACM landing page returned HTTP 403. Crossref was read successfully through direct Python HTTPS after web-tool access failed; the full NIST PDF was accessible. The dataset card was likewise retrieved through direct HTTPS. No actual qrels/relevance-label file was opened, no local study records or result arrays were audited, and no experiments or manuscript edits were performed. No previous citation audits informed this judgment. Required workspace README/handoff were read for repository instructions only.

The companion JSON contains every detected TREC-COVID context, the exact citation paragraph, primary-source retrieval details and scope boundaries. This is citation review, not execution review.

## Final input hashes (SHA-256)

- `paper/references.bib`: `c04d2e03b5df17f3e6e026bd7f8e7c942905055de4174c9a45f1fddeb7941de2`
- `paper/sections/abstract.tex`: `c75dc88657f9b538f314b1787e75b08f9b3864f000a0f7e8b729effbe5f7d3d4`
- `paper/sections/conclusion.tex`: `5ab2f71361be86ad2ddc5d4d21e00cc0a1ac869c900ef6546edba72be0b572b7`
- `paper/sections/discussion.tex`: `834323c766a49b3b3874b660b9e6fdad3b660e8b5d93a5afeeae0c22fea01240`
- `paper/sections/experimental-setup.tex`: `c6dfc7e773e6f448118013e5f11ec35eed6f849f7fb475bb1d690b1e07220828`
- `paper/sections/introduction.tex`: `d67c836c50b51760cb279b62c1096a4b4a3e4498fa9e6b547df72d79cc27945f`
- `paper/sections/method.tex`: `c4babc62dd94e8c6e2ccd6b921ea9d82db762ddf73df5c6efe71a3f022ce0e37`
- `paper/sections/related-work.tex`: `bb47d22e21547ef1e96f4eb3634cda7039d2d6078082bae302d6507380a2b10f`
- `paper/sections/results.tex`: `a8d76c0bc6ffcd14af3d461baf406837e3cd34a371585cd1e9754c28a64bafd3`

Citation-entry hash (UTF-8 text, LF): `e06635ce3f6bd28150987026ab1c7da0bae53a1c2387bdb629da85532260b3af`.
