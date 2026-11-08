# minilm2020 citation audit

**Recommendation: FIX the checkpoint attribution; keep the paper.** Confidence: high. Status: **same-family/provisional** (gpt-6.1-sol, high reasoning; fresh single-entry review). Live primary-source checks performed on 2026-11-01.

## Existence and metadata

Verified in the [official NeurIPS proceedings](https://proceedings.neurips.cc/paper/2020/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) and [publisher BibTeX](https://proceedings.neurips.cc/paper_files/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Bibtex.bib). The supplied entry is correct:

- Authors, in order: Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan Yang, Ming Zhou.
- Title: *MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers*.
- Venue/year: *Advances in Neural Information Processing Systems*, volume 33, 2020, pages 5776–5788.
- Version: published NeurIPS 2020 proceedings paper, a 13-page [official PDF](https://proceedings.neurips.cc/paper_files/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf). Publisher: Curran Associates, Inc.

No bibliographic correction is required. The live BibTeX was retrieved through `Invoke-WebRequest` after the web reader rejected its MIME type. Editor, publisher, and URL fields may be added but are optional.

## Context judgments

| Use | Verdict | Action | Reason |
| --- | --- | --- | --- |
| `sections/experimental-setup.tex:21` | **WEAK** | **FIX** | Valid background for the MiniLM family, but the 2020 paper does not establish the exact `all-MiniLM-L6-v2` sentence-embedding checkpoint. |
| `sections/related-work.tex:31` | **SUPPORTS** | **KEEP** | The sentence explicitly discusses encoder families and training approaches; MiniLM's architecture/distillation paper directly fits that scope. |

The published paper describes distillation using attention distributions and value relations (Sections 1 and 3); Table 3 includes a six-layer model with hidden dimension 384. That architecture fact is distinct from identifying a subsequently fine-tuned sentence encoder. The [official `all-MiniLM-L6-v2` model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) establishes the named checkpoint's 384-dimensional output and describes contrastive fine-tuning from `nreimers/MiniLM-L6-H384-uncased`.

For the experimental-setup use, retain `minilm2020` and add a checkpoint-specific model-card reference beside `all-MiniLM-L6-v2`, including the actual pinned revision from the experiment manifest. No revision was supplied or audited here, so none is proposed. The MiniLM paper cannot substantiate the destination checkpoint, the E5 pair, a migration's complete dimensional specification, local hash/revision pins, or the study's encoding settings. Those are separate attribution or reproducibility questions, outside this entry's support.

One possible minimal wording adjustment is to identify `all-MiniLM-L6-v2` with its official model-card reference, then retain the MiniLM paper where discussing the underlying model family. Do not replace the family paper with a model card throughout related work.

This is a same-family/provisional citation audit, not an independent cross-model review. It covers only the supplied entry and two contexts; no experiments, qrels, prior reviews, or other manuscript entries were inspected.
