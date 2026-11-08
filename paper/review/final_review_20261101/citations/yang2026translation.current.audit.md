# yang2026translation ? current citation audit

**Verdict: KEEP.** All three audit axes pass for the current frozen wording. No manuscript change is requested.

## Current inputs

| File | SHA-256 (original bytes) |
|---|---|
| `paper/references.bib` | `c04d2e03b5df17f3e6e026bd7f8e7c942905055de4174c9a45f1fddeb7941de2` |
| `paper/sections/related-work.tex` | `c2908b8289c07214f10cf548acbd4436da970fdd0a487b62669b115ab492167b` |
| `paper/sections/method.tex` | `ceb05f7d9303ea5560b646fe9b25f81f7a6b772557fb7b747ae89190d98530fc` |

The JSON also records the actual extracted BibTeX entry, citing paragraph and tangent subsection, with individual hashes. No earlier citation/research opinion was read.

## Three-axis decision

- **bibliographic_accuracy ? KEEP:** Current authors, title, ICML 43 booktitle, PMLR volume 306, pages 144275--144302, year 2026 and canonical URL match the live publisher record. Optional series/publisher fields are not required corrections.
- **claim_support ? KEEP:** All technical attributions in the frozen citing paragraph are supported by the publisher abstract and author PDF; the per-anchor tangent comparison matches the current method equations.
- **citation_use_and_scope ? KEEP:** HMoE is relevant context for document embedding translation and geometric residual control. The text does not present an HMoE reproduction or performance comparison. The five-configuration panel is this study's metadata, not an assertion sourced to HMoE.

## Technical checks

- **hierarchical mixture of experts and localized expert structure ? KEEP:** Section 3, PDF pp. 4--6: a binary source-space hierarchy selects local experts; node-specific LoRA adapts a shared neural translator.
- **out-of-distribution translation, multi-model mixing and chaining ? KEEP:** Abstract and Sections 4--5: cross-dataset OOD, common-target mixing and composed multi-hop translation are explicit settings.
- **residual regularization along target principal directions versus per-anchor tangent targets ? KEEP:** Sections 4.1--4.2, PDF pp. 6--7: target-training PCA supplies PC1/PC2; projection penalties shape mixing and chaining residuals. Current Eq. tangent-target instead projects each target onto the plane orthogonal to its own current prediction and scales by its norm. Both fitted ARC2 corrections accumulate into B2.

The distinction is structural, not a claim of priority over all geometric methods. HMoE belongs in related work; the paragraph explicitly treats the evaluated five configurations as local study metadata. No HMoE superiority or reproduction is claimed.

## Primary evidence and access

- [Publisher record](https://proceedings.mlr.press/v306/yang26e.html), accessed 2026-11-01; metadata and abstract available live.
- [Publisher-linked author paper](https://raw.githubusercontent.com/mlresearch/v306/main/assets/yang26e/yang26e.pdf), directly downloaded: 1,698,281 bytes; SHA-256 `38b35ae4755468e2619731e527d216792b936008e343c09e229c8e4f04856c05`. Section 3 supports the expert structure; Sections 4.1--4.2 and Fig. 6 support PCA-direction residual control.
- The web PDF parser rejected the octet-stream content type; direct HTTPS download succeeded. Extraction warned about an XObject limit, but the relevant prose and equations were recovered. OpenReview presented browser verification and was not used as evidence.

No new wording, experiments, delegation, manuscript edits, local result audit, or standalone novelty judgment. The full structured record is `yang2026translation.current.audit.json`.
