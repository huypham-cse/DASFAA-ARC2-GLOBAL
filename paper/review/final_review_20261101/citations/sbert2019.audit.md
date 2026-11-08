# Citation audit: `sbert2019`

**Recommendation: FIX citation placement/support; retain the entry.** Confidence: high. Status: **same-family/provisional**. Checked 2026-11-01 using live primary sources; no earlier reviews, experiments, or qrels were consulted.

## Existence and metadata

**VERIFIED; supplied metadata CORRECT.** The live [ACL publisher record](https://aclanthology.org/D19-1410/), [BibTeX export](https://aclanthology.org/D19-1410.bib), and [proceedings full text](https://aclanthology.org/D19-1410.pdf) agree:

- Authors, in order: Nils Reimers; Iryna Gurevych.
- Title: Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.
- Year/venue: 2019, Proceedings of EMNLP-IJCNLP (full supplied booktitle matches).
- Pages: 3982–3992. DOI: `10.18653/v1/D19-1410`.
- Version: published proceedings article, ACL Anthology D19-1410; publisher Association for Computational Linguistics.

Optional publisher, month, address, and URL fields may be added but their omission is not an error.

## Context judgments

| File / supplied line | Verdict | Action | Reason |
|---|---|---|---|
| `sections/experimental-setup.tex:21` | **WEAK** | **FIX** | The citation follows exact named checkpoints and a dimensional migration. SBERT supplies methodological lineage, but does not document the later `all-MiniLM-L6-v2` or `all-distilroberta-v1` checkpoints. Their dimensions are independently supported by maintainer cards, so the claim is not contradicted; its attribution is incomplete. |
| `sections/related-work.tex:31` | **SUPPORTS** | **KEEP** | This explicitly attributes generic encoder families and training approaches. SBERT directly supports its own family/method portion, without making a checkpoint-specific or migration-performance claim. |

The proceedings full text, particularly Section 3 and Section 3.1 (printed pages 3984–3985), describes pooling BERT/RoBERTa into sentence vectors and siamese/triplet objectives, with NLI fine-tuning. This is sufficient for generic Sentence-BERT attribution. It is not a source for the later checkpoints' identities, exact configurations, or the study's run settings. [Primary full text](https://aclanthology.org/D19-1410.pdf).

The primary [all-MiniLM-L6-v2 maintainer card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) documents 384-dimensional output and contrastive sentence-pair fine-tuning; the [all-distilroberta-v1 card](https://huggingface.co/sentence-transformers/all-distilroberta-v1) documents 768-dimensional output and its distinct distilroberta initialization. These directly support checkpoint identification and dimensions. The first card distinguishes default 256-word-piece truncation from 128-token training length; the second specifies default truncation at 128 word pieces. Neither card establishes what this study actually executed.

## Concrete fix

Retain `sbert2019` unchanged in the bibliography and retain the related-work attribution. Add checkpoint-specific references or footnotes beside the MiniLM-to-distilroberta migration using the two maintainer cards, ideally at the already pinned experimental revisions. Do not invent a revision or treat the current main-branch card as proof of the experiment's pinned version. If necessary, state explicitly that the 128-token encoding cap is the study's configuration.

Pinned revisions, input hashes, normalization, and actual encoding settings require the authors' run/config evidence. This audit does not validate that evidence or judge the separate E5 citation. The conclusion is a single same-family provisional audit, not independent cross-family validation.
