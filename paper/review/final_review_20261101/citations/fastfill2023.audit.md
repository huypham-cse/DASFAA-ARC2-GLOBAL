# fastfill2023

**KEEP — existence verified; confidence high.** Review independence: same-family. Acceptance status: provisional. Live checks performed 2026-11-01.

The supplied author order, title, 2023 year, ICLR venue and `inproceedings` type match the [official authors' citation block](https://raw.githubusercontent.com/apple/ml-fct/main/README.md). The [Apple research page](https://machinelearning.apple.com/research/fastfill) independently confirms the authors, title and publication context.

The [primary arXiv record](https://arxiv.org/abs/2303.04766) lists v1, submitted 8 March 2023, and DOI `10.48550/arXiv.2303.04766`. This is an arXiv DOI; no conference DOI or proceedings page range was established. The PDF contains 24 pages, not an assigned proceedings range.

| Use | Verdict | Reason |
| --- | --- | --- |
| `sections/related-work.tex:9` | SUPPORTS | [Primary text](https://arxiv.org/pdf/2303.04766), pp. 5–6, supports visual alignment with uncertainty-ordered partial backfilling. Introduction p. 2 explicitly identifies an initial drop for earlier losses with random ordering (FCT-Random, Figure 2a). Thus replacement **can** initially reduce retrieval performance; the sentence does not claim that all policies or FastFill itself must decline. |

No required fix. [OpenReview](https://openreview.net/forum?id=rnRiiHw8Vy) returned a browser-verification challenge; no inaccessible metadata was guessed. The accompanying JSON records source-level verified facts and explicit checks for partial backfilling and initial retrieval decline. Only this key's supplied input and live primary sources were examined.
