# treccovid2020 — FIX (same-family/provisional)

Existence: **VERIFIED**. Bibliographic metadata: **MATCH**. Context: **WEAK**, with a supported collection-background use.

The nine authors and their order, full title, DOI `10.1145/3451964.3451965`, ACM SIGIR Forum 54(1), and pages 1–12 match the entry. Live [Crossref metadata](https://api.crossref.org/works/10.1145/3451964.3451965) gives June 2020 as the print/issue date and February 19, 2021 as the online date. Keep **2020**: the [official author PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=930360) also identifies June 2020. The [NIST landing record](https://www.nist.gov/publications/trec-covid-constructing-pandemic-information-retrieval-test-collection) uses the online year. This is a 12-page journal article, distinct from the [10-page arXiv v1 record](https://arxiv.org/abs/2005.04474), submitted May 9, 2020. No bibliography repair is required.

| Use | Verdict | Reason |
|---|---|---|
| `sections/experimental-setup.tex:16`: TREC-COVID identity/background | SUPPORTS | The article describes construction and motivation of the pandemic retrieval collection. |
| Same context: all 171,332 documents and 50 queries | WEAK | The cited article is an early Round 1/2 snapshot, discussing 51K/60K document releases and 30 Round 1 topics. It does not establish the later exact BEIR packaging or the authors' pinned files. |
| Same context: frozen confirmation, closed labels, sealed rankings/endpoints and separate verification | WEAK | These are claims about this study's protocol and execution. Collection literature cannot verify them; no contradiction is inferred and local provenance was outside this audit. |

The exact counts agree with live [BEIR dataset metadata](https://datasets-server.huggingface.co/info?dataset=BeIR%2Ftrec-covid): 171,332 corpus examples and 50 query examples. The [benchmark-maintainer README](https://raw.githubusercontent.com/beir-cellar/beir/main/README.md) lists 50 queries and 171K documents. The [official final collection documentation](https://ir.nist.gov/covidSubmit/data.html) identifies the July 16 CORD-19 release and final 50 topics after five rounds. These corroborate public collection dimensions, not the identity or use of the authors' pinned local files. Only documentation/metadata were read; no relevance-judgment files were accessed.

**Fix:** Keep this citation for original collection background. Specify the BEIR release and add `beir2021` to the packaging statement. Attach the actual local pinned manifest to exact counts/file identity, and the immutable protocol/seal audit to the study-specific label-access chronology. Suggested opening:

> We subsequently froze a separate confirmation using the BEIR release of TREC-COVID\cite{treccovid2020,beir2021}, with all 171,332 documents and 50 queries in our pinned input manifest.

Do not insert the suggested manifest/seal reference until its actual artifact is identified. This audit did not inspect those artifacts.

Confidence: **high** for existence, metadata and source scope; local study provenance remains unaudited. Live checks performed November 1, 2026. ACM returned HTTP 403, so publisher-deposited Crossref metadata and the official author PDF supplied verification. No prior reviews, other agents/models, experiments or qrels were consulted; no manuscript/bibliography edits made. This is a **same-family/provisional** review.
