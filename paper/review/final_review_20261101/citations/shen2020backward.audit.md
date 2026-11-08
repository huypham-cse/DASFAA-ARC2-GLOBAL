# shen2020backward ? KEEP

Status: **same-family/provisional**. Confidence: **high**. Checked 2026-11-01.

The paper exists. The supplied title, author order (Yantao Shen, Yuanjun Xiong, Wei Xia, Stefano Soatto), CVPR venue, and 2020 year are correct. DOI: **10.1109/CVPR42600.2020.00640**. No required bibliography correction.

Primary pagination differs: [CVF publisher page](https://openaccess.thecvf.com/content_CVPR_2020/html/Shen_Towards_Backward-Compatible_Representation_Learning_CVPR_2020_paper.html) gives **6368?6377**, while the [live publisher-deposited Crossref record](https://api.crossref.org/works/10.1109/CVPR42600.2020.00640) gives **6367?6376**. The supplied entry omits pages and DOI; those omissions are not false metadata. If enriched, retain an explicit edition choice.

| Use | Verdict | Reason |
|---|---|---|
| `sections/related-work.tex:14` ? new encoder remains usable with previously computed gallery features | **SUPPORTS** | The paper trains the new encoder while keeping old gallery embeddings usable. Section 2.2, Eq. (2), explicitly evaluates new-model queries against old-model gallery features. Section 2.4 uses the fixed old classifier in training the new encoder. The direction in the manuscript is correct. |

The [CVF full paper](https://openaccess.thecvf.com/content_CVPR_2020/papers/Shen_Towards_Backward-Compatible_Representation_Learning_CVPR_2020_paper.pdf) was fetched live successfully (HTTP 200) and parsed in memory. Sections 2.1?2.5 (printed pages 6370?6371) directly establish the training and compatibility direction. The publisher page was returned by live search; direct web opens returned 403. Cached publisher HTML was only supplementary. The Crossref API was also queried live successfully for title, authors, year, venue, pages, and DOI.

**Fix if needed:** none. Keep the citation and its current claim.
