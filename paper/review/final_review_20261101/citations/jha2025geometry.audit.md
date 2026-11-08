# Citation audit: jha2025geometry

**Decision: KEEP. Existence: VERIFIED. Use verdict: SUPPORTS.**

Fresh live primary-source audit on 2026-11-01. Same-family/provisional review; no independent model-family validation.

## Metadata

The supplied entry matches the live [NeurIPS BibTeX export](https://proceedings.neurips.cc/paper_files/paper/28820-/bibtex): Rishi Jha, Collin Zhang, Vitaly Shmatikov, John Morris; *Harnessing the Universal Geometry of Embeddings*; *Advances in Neural Information Processing Systems*, volume `38, Main Conference`, 2025, pages 45963–45987, DOI `10.52202/085713-1530`. The export was fetched live using HTTP after the web reader rejected its BibTeX content type.

The [conference landing page](https://proceedings.neurips.cc/paper_files/paper/2025/hash/4175dee33d6145cb8f0323703d138a53-Abstract-Conference.html) confirms title, author order, NeurIPS 2025 main-conference publication, and DOI. The [conference PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/4175dee33d6145cb8f0323703d138a53-Paper-Conference.pdf) spells the last author John X. Morris; the shorter bibliography spelling follows the official export and is not an identity error.

Pagination caveat: the [DOI-linked proceedings vendor record](https://www.proceedings.com/085713-1530.html) instead reports 51335–51359. The supplied 45963–45987 is verified against the conference's own live export, which takes precedence here; the publisher-side pagination conflict remains unresolved. No silent substitution is justified.

Version: cite the published NeurIPS 2025 version. The [arXiv record](https://arxiv.org/abs/2505.12540) identifies preprint 2505.12540, first submitted 18 May 2025, latest v4 revised 26 January 2026. That revision does not change the conference citation year to 2026.

## Use audit

| File / supplied line | Claim | Verdict | Evidence and reason |
|---|---|---|---|
| `sections/related-work.tex:23` | vec2vec learns translation through a shared latent representation without known correspondences | SUPPORTS | Conference PDF §2–3.1, pp. 2–3: the task excludes pairwise correspondence; encoder-specific adapters feed a shared backbone and output adapters decode the common latents. §4.1, p. 5, specifies disjoint training-document sets. Thus both the unpaired supervision description and shared-latent mechanism are directly supported. |

The surrounding distinction from ARC2's known-correspondence setup is appropriate for this citation. Claims about ARC2 or mini-vec2vec are outside this entry's audit scope.

**Fix:** none required. Keep the present conference entry and claim; retain the pagination caveat in the audit record. **Confidence:** high for existence and claim support (0.98); high with an explicit pagination caveat for metadata (0.90).
