# Citation audit: la2m

Existence: **YES**. Verdict: **KEEP**. Confidence: **HIGH**. Review independence: **same-family**; acceptance status: **provisional**.

The input entry matches publisher-deposited metadata: Beining Yang, Yang Cao, and Yang Ren, *Integrating Vector Databases across Embedding Models*, Proceedings of the ACM on Management of Data **3(6)**, pp. 1–28, **2025**, DOI **10.1145/3769803**. Live Crossref gives print publication 4 December 2025 and online publication 5 December 2025. The institutional record supplies article number 338. This is the **2025 PACMMOD journal article**, also presented at **SIGMOD 2026**; the conference presentation does not require changing its journal publication year.

| Cited use | Assessment | Reason |
|---|---|---|
| `sections/experimental-setup.tex:44` | SUPPORTS | The authors' live code implements global centered rectangular Procrustes for A2M and source-reference k-means for LA2M, local fits with at least two references, nearest-centroid routing, and global fallback for singleton clusters. Twenty clusters occurs among supported sweep configurations. The manuscript explicitly declares adaptations. This verifies provenance and suitability, not execution of the manuscript implementation. |
| `sections/introduction.tex:7` | SUPPORTS | LA2M supports the qualitative local-alignment alternative and global orthogonal-alignment context. No quantitative or superiority claim is made. The neighboring neural-regression assertion belongs to the separately cited `simplelinear` entry. |
| `sections/related-work.tex:6` | SUPPORTS | The institutional abstract establishes cross-model database integration rooted in local isometry. The authors' implementation explicitly identifies global A2M and local LA2M, matching the supplied summary. |

Primary sources checked live:

- [Crossref publisher-deposited metadata](https://api.crossref.org/works/10.1145/3769803): retrieved successfully through the live API using PowerShell after browser-tool access failed; confirms title, author order, DOI, journal type, volume, issue, pagination, and dates.
- [University of Edinburgh institutional record](https://www.research.ed.ac.uk/en/publications/integrating-vector-databases-across-embedding-models/): confirms authors, integration/local-isometry scope, article number, series and conference association. Its August 2025 accepted/in-press status is repository metadata, not the final journal publication date.
- [Yang Cao's official publication page](https://homepages.inf.ed.ac.uk/ycao/pub-year.html): confirms this title and author order under SIGMOD 2026.
- [Authors' group implementation, pinned commit](https://github.com/DBgroup-Edinburgh/embedding-translation/blob/5e62baf1544264847ce3d8feeabd1ded6499b064/reproduce-scripts/la2m/exp_la2m.py): live GitHub API resolved the commit and live raw retrieval confirmed the global/local fits and fallback at lines 105–126; the cluster sweep includes 20. This is implementation evidence, without certifying all original-paper settings.
- [Repository README](https://github.com/DBgroup-Edinburgh/embedding-translation/blob/main/README.md): identifies the LA2M reproduction folder with this work and separately states the 2025 journal / SIGMOD 2026 presentation distinction.
- [Institutional accepted manuscript PDF](https://www.research.ed.ac.uk/files/572061340/main.pdf): live access returned **403**. No PDF content, theorem, section detail, or original setting was guessed.

Required exact fix: **none**. Optionally add `note = {Presented at SIGMOD 2026}` while retaining the correct 2025 article entry. No other citation keys, local implementation, experimental results, or earlier reviews were audited.
