# Independent DASFAA-style review R2

Date: 2026-11-01. Reviewer: gpt-6.1-sol, high reasoning. Anonymous paper: *ARC2-Global: Tangent-Corrected Alignment for Embedding-Index Migration*.

**Score: 6/10 — Weak accept. Confidence: 4/5.**

Internal senior-reviewer simulation only; not an official DASFAA rubric or acceptance probability. The local scale uses 6 for weak accept and 7 for accept. Scores below are holistic judgments, not an arithmetic scoring formula.

## Judgment

Technically sound and useful incremental work with strong development evidence and a well-defined deployment representation. The independent collection confirms advantages over selected evaluated neural/regression configurations, not over Procrustes or LA2M. This bounded contribution clears a weak-accept threshold but lacks the novelty and closest-baseline confirmation for a confident accept.

The contribution is exactly two affine ridge fits to raw-norm-scaled negative cosine-gradient targets, initialized by centered rectangular Procrustes, yield one normalized affine document adapter for anchor-inclusive staged destination-space migration. This is a useful small-method contribution: an explicit computation that improves normalized document adaptation while keeping the inference artifact simple. It does not require a sweeping new compatibility framework or a convergence theorem to be worthwhile.

The development evidence is convincing for the stated evaluation panel. A 0.0243 macro nDCG gain over the closest baseline, 23/24 positive condition means, and a supported 0.0069 gain from the second step are meaningful together. The prospective evaluation materially strengthens the paper through large E5 gains over the evaluated Converter and ridge configurations. It does not establish an independent gain over Procrustes: all six prospective point differences favor Procrustes, with unresolved family intervals. The manuscript reports this distinction accurately. I would retain the complete results and current confident wording of the supported claims.

I lean weak accept for a focused data-management/retrieval paper. The main reason to stop below a confident accept is the combination of incremental algorithmic novelty and lack of independent superiority over the strongest compact geometric alternative. These are scientific limits on impact, not evidence that the method or reported result is invalid.

## Dimension scores

| Dimension | Score / 10 | Rationale |
|---|---:|---|
| novelty | 5 | A specific, plausible refinement of established alignment/regression ingredients; the exact norm-scaled tangent ridge composition is distinct, while affine inference and partial backfill are established. |
| technical | 7 | The formulation, gradient, current-map prior, rectangular alignment and common-scale reasoning are correct; the finite method is empirical rather than a convergence theorem. |
| experimental | 7 | Strong matched development panel, mechanism controls, all-paid comparison and prospectively sealed test with paired multiplicity-aware intervals; independent benefit over the closest geometric baseline remains unestablished. |
| practical | 6 | Concrete destination-query/single-gallery operating scenario and very small adapter; the gains are encoder dependent and parameter storage is the measured structural efficiency quantity. |
| clarity | 8 | Coherent result-led narrative, precise equations, readable tables and four useful figures, with balanced complete comparisons. |
| reproducibility | 6 | Method, budgets, seeds, revisions, retrieval rules and statistical units are unusually clear; artifact access and some baseline configuration details are not discoverable from the paper itself. |
| venuefit | 8 | Relevant to vector data management, migration budgets and mixed-index quality; a representation/evaluation paper with practical database relevance rather than a serving-systems contribution. |

## Strengths

- Exact compact algorithm and three correct central mathematical claims.
- Matched five-baseline panel, same anchors and paid replacement rows, full native references, graded relevance retrieval and transparent multiplicity-aware query intervals.
- Development gain over Procrustes of 0.0243 across the macro and 23/24 positive condition means; second-step gain of 0.0069.
- Prospective E5 gains against evaluated Converter/ridge at every budget, plus informative encoder-dependent all-paid and mixed-gallery behavior.
- Clean 15-page PDF with all four figures and negative/competitive outcomes retained.

The budget definition is particularly clear: anchors are paid destination encodings and are replaced by native vectors in the gallery. The distinction between fitting supervision and true-vector replacement avoids an easy source of unfair comparison. The method also describes the current-map prior rather than presenting the entire affine-ridge difference as an isolated tangent effect. Native Full-X and Full-Y, all-paid E5 behavior and competitive prospective geometric baselines remain visible.

## Main concerns and their implications

- Independent TREC-COVID results have higher Procrustes point means in all six cells and unresolved Procrustes/LA2M adjusted intervals.
- Novelty is incremental; the experiments do not isolate tangent targeting from a retained-current-map prior in the affine-ridge contrast.
- Only two 384-to-768 migrations and one independent collection; three Nano development collections have 50 queries each.
- HMoE is cited but untested; comparison is to declared configurations rather than every recent method or original-paper reproduction.
- Parameter count supports storage and affine inference claims; no measured end-to-end encoding/serving efficiency result.

These concerns do not warrant adding repeated cautionary paragraphs. The paper already distinguishes development from prospective evidence, parameter storage from end-to-end cost, and point proximity from equivalence. Keep that calibration and use the available space to sharpen the mechanism and relation to the closest recent work.

## Independent mathematical check

### Cosine gradient: correct

For u=z/r and ||y||=1, D N(z)=(I-u^T u)/r. Thus grad_z[1-y N(z)^T]=-[y-(uy^T)u]/r and T=r[y-(uy^T)u]=-r^2 grad. This is a scaled negative gradient target, not the gradient itself.

### Current-map prior: correct

Substituting Delta=C-B_t in ||Xtilde Delta-T||_F^2+lambda||Delta||_F^2 gives Eq. (8) exactly. The prior center is the current map at each update, not a fixed B0 or a zero-centered fit onto Y.

### Positive common-scale equivariance: correct under the stated conditions

For c>0, z(cB)=cz, r(cB)=cr and u(cB)=u, so T(cB)=cT(B). The fixed linear ridge operator yields Delta(cB)=cDelta(B); induction gives scaled iterates and unchanged normalized predictions. It is not row-wise scale invariance or a finite-step improvement guarantee.

### Rectangular Procrustes and affine expansion: correct for evaluated ds<=dt

Thin SVD of Yc^T Xc has U of shape dt x ds and V of shape ds x ds. W=UV^T has orthonormal columns; W^T maps source rows into destination coordinates. The bias mu_t-mu_s W^T gives the stated centered raw prediction.

### Ridge solve, storage and costs: consistent

lambda>0 makes the dual/primal ridge systems positive definite; both are equivalent in exact arithmetic. 385*768=295680 float32 coefficients, 1182720 bytes, about 1.128 MiB; 33927168/295680 is about 114.7. The displayed complexity expressions are consistent.

### Tangent fitted corrections and descent: appropriately bounded

The targets are tangent but shared ridge-fitted row corrections need not be. The manuscript correctly makes no monotone finite-step cosine/retrieval improvement claim.

The gradient interpretation explains what the target does. It does not by itself prove that two steps are universally preferable or that retrieval improves on every new corpus. The paper's finite-procedure evidence is the appropriate justification for those measured gains. No mathematical correction to the three requested core claims is necessary.

## Citation positioning

The literature coverage is substantively relevant rather than decorative. The paper distinguishes paired document translation, query-side backward adaptation, train-time compatibility, unpaired pseudo-correspondence methods and partial backfill. It explicitly credits earlier ingredients and does not claim mixed galleries or Procrustes initialization as new.

Selective primary-source checks support the key distinctions. [Embedding-Converter](https://aclanthology.org/2025.acl-long.1237.pdf) uses document conversion with regression/global/local losses and retrieval-based validation, making the declared MAE-based adaptation consequential and appropriately disclosed. [Yang and Cao's HMoE paper](https://proceedings.mlr.press/v306/yang26e.html) explicitly studies OOD, mixing and chaining with localized experts; its presence in related work raises a natural comparison question. [Spherical interpolation](https://arxiv.org/abs/2609.39836) concerns aligned query directions, while [mini-vec2vec](https://arxiv.org/abs/2510.02348) obtains linear translation through pseudo-pairing and refinement. These checks support the current conceptual distinctions; they are not an exhaustive novelty certificate.

The most useful writing change is to explain why the present global two-step map is a different design point from HMoE and state its status as contextual, untested related work. A new HMoE experiment is an optional extension, separate from the required writing edits.

## Visual and narrative review

The actual 15-page reviewed PDF was rendered and every page inspected. All four figures were inspected in their page context; pages 3 and 11 also received 150-dpi inspection.

| Figure | PDF page | Assessment |
|---|---:|---|
| 1 | 3 | Readable and informative native-style mechanism with illustrative accounting and explicit toy-data caption; small pale labels can be strengthened. |
| 2 | 10 | Clear two-migration development curves with complete methods/native references; legend and markers distinguish methods. |
| 3 | 11 | Readable five-contrast interval plot including zero and negative controls; ridge scale compresses small effects somewhat but their labels remain clear. |
| 4 | 12 | Clear prospective curves with complete panel and native references; different vertical ranges are stated in caption. |

No clipping, broken math, unreadable tables, missing figures, overlapping elements or anonymity defect observed. Some floats precede their section text, which is acceptable in the present readable layout. Figure 1 correctly marks its corpus, anchors and displayed hits as illustrative. The main data figures retain every method and both native references. Tables are compact but readable. No visual redesign is required.

The narrative moves from a concrete staged-index problem to the algorithm and then development, ablation, prospective and all-paid evidence. The result-led framing is effective. The paper is more persuasive when the exact update and measured gain remain the main story than when novelty is expressed in generic directional-language terms.

## Ranked required text-only fixes

**Critical: none.** No mandatory new experiment is attached to the writing revisions.

1. **MAJOR — Sections 1, 2 and 3.3.** The exact algorithmic novelty can be stated more sharply than 'directional refinement'. Add a compact interpretation after Eq. (8): each step fits norm-scaled cosine descent targets under an affine correction penalty centered on the current map; the new object is this finite two-step computation, not Procrustes, affine folding, or mixed galleries. Explain that two is the selected fixed procedure, with the measured incremental gain in Section 5.2, rather than a universally optimal iteration count.

2. **MAJOR — Section 2, first paragraph.** The recent HMoE paper is cited but its relationship to the evaluated panel remains implicit. Add two sentences contrasting its localized/expert routing and mixing/OOD objective with the single global affine refinement here, and state that HMoE is contextual related work rather than an evaluated baseline. Keep the paper's existing 'five evaluated configurations' language. Do not imply a state-of-the-art comparison that was not run.

3. **MAJOR — End of Section 4 or a short artifact footnote.** The paper says revisions and input hashes are pinned but does not tell a reader where those artifacts/configurations can be obtained. Add a concise anonymous artifact-availability statement pointing to the existing release if it is available for review, including the configuration/manifest entry point. Identify the baseline optimizer, learning rate, layer widths/loss weights, validation split and solver backend in that existing configuration rather than expanding the main paper into a protocol log. If unavailable, accurately state availability instead of suggesting the paper alone specifies these settings.

4. **MINOR — Section 5.4.** 'the two-pair comparison' can be read as two training pairs rather than two encoder migrations. Replace it with 'the two-migration comparison'.

5. **MINOR — Section 4 bootstrap paragraph.** Pairing across repeated conditions is implied but not fully explicit. Add one sentence saying whether the same sampled query indices are reused across methods, budgets and migrations for each collection, matching the locked analysis. This makes the macro interval construction independently interpretable without changing the statistics.

6. **MINOR — Section 3.3 and Figure 1.** Normalization notation is used before an explicit mathematical definition, and the smallest pale annotations in the mechanism are less legible than the rest of the paper. Define N(z)=z/||z|| for nonzero z at first use. If revising figure text, darken the pale annotations or shorten them; preserve the working example, accounting and all four figures.

These revisions should preserve the frozen two-step, lambda=10 method, measured negative outcomes and full comparison panel.

## Optional scientific extensions, separate from writing edits

1. On a newly locked independent setting, compare the frozen procedure with the strongest geometric comparator and, where feasible, HMoE. Purpose: Test incremental independent value over the closest geometric alternative and modern coverage.

2. A separately named/protocolled control retaining the same initialization and correction penalty but using a non-tangent target. Purpose: Separate directional targeting from the current-map prior without changing the frozen method.

Neither is required to fix the present prose. No experiment was run for this review, and this review does not release any protocol STOP or authorize retuning.

## Scope, independence and limitations

- Read all requested manuscript source: main.tex, eight section files, five generated TeX files and references.bib. The generated ablation.tex and trec_family.tex were read even though main.tex does not insert them.
- Inspected the actual reviewed PDF, not an earlier or similarly named revision: 15 pages, 812,677 bytes, SHA-256 `de820e58315443262fda1bea48fea73206e5d8fc04c15b808c7c1bb3be4465ed`.
- Read AGENTS.md only for scope rules. Its embedded prior review opinions and status claims were not used as scientific evidence. No paper/review content or prior score was opened.
- No other agent/model was consulted. No scientific run, source-code audit, ranking reconstruction, new statistical calculation or manuscript edit was performed.
- This is a paper review and mathematical consistency check, not an independent audit of raw results, leakage controls, implementation identity, hash provenance, or empirical significance reconstruction. Author-reported tables/intervals are evaluated as presented. Source-to-PDF build identity was not independently rebuilt.
- Selective primary-source positioning checks, not an exhaustive novelty search or full verification of all 18 references. The HMoE PDF and ACM DOI page could not be read through the web tool. An inaccessible attempted OpenReview URL was not used.
- The input hashes below identify exactly the locally read material. They establish review input identity; they do not certify the underlying results.
- Only these review outputs and temporary PDF page PNGs were created. Temporary renderings reside under tmp/pdfs/r2_review_20261101/.

## Read-input SHA-256 manifest

| Relative path | Bytes | SHA-256 |
|---|---:|---|
| AGENTS.md | 17606 | `300cedb59f460fa7fec3472d1fbbfee87987c197d369addc3e854d18381e96ee` |
| paper/main.tex | 1078 | `f8278687f7db8ce72b6142713f3c10d56b89ae29cb8032386baa84dae151b98f` |
| paper/sections/abstract.tex | 1309 | `c75dc88657f9b538f314b1787e75b08f9b3864f000a0f7e8b729effbe5f7d3d4` |
| paper/sections/conclusion.tex | 614 | `5ab2f71361be86ad2ddc5d4d21e00cc0a1ac869c900ef6546edba72be0b572b7` |
| paper/sections/discussion.tex | 2167 | `834323c766a49b3b3874b660b9e6fdad3b660e8b5d93a5afeeae0c22fea01240` |
| paper/sections/experimental-setup.tex | 5698 | `c6dfc7e773e6f448118013e5f11ec35eed6f849f7fb475bb1d690b1e07220828` |
| paper/sections/introduction.tex | 3978 | `d67c836c50b51760cb279b62c1096a4b4a3e4498fa9e6b547df72d79cc27945f` |
| paper/sections/method.tex | 10129 | `c4babc62dd94e8c6e2ccd6b921ea9d82db762ddf73df5c6efe71a3f022ce0e37` |
| paper/sections/related-work.tex | 4381 | `bb47d22e21547ef1e96f4eb3634cda7039d2d6078082bae302d6507380a2b10f` |
| paper/sections/results.tex | 6518 | `a8d76c0bc6ffcd14af3d461baf406837e3cd34a371585cd1e9754c28a64bafd3` |
| paper/generated/ablation.tex | 836 | `024435422d3cd2e5c977fa680365e1a7983e763ad813c91a4d65eb4db847571e` |
| paper/generated/allpaid.tex | 1285 | `8df4a96cb9a4e5c9bf7c2e501f0bcd3009c38183d874417d013b956fcec8a561` |
| paper/generated/dev_macro.tex | 964 | `163f3ff6de42e4d0e60f3014e04864b4c48ebd08766995134bde4c22f84e2878` |
| paper/generated/trec_family.tex | 655 | `b249a6c58e87792b9bed0dee93e631e66d65c7f0381fb38d3c03f0a19ed4fc9e` |
| paper/generated/trec_means.tex | 1465 | `2d6fe4761d377eb66da068072310dcfd893e67fdcbf43b4186160182b8fc0c19` |
| paper/references.bib | 6442 | `c04d2e03b5df17f3e6e026bd7f8e7c942905055de4174c9a45f1fddeb7941de2` |
| paper/ARC2_Global_DASFAA2027_reviewed.pdf | 812677 | `de820e58315443262fda1bea48fea73206e5d8fc04c15b808c7c1bb3be4465ed` |

The companion DASFAA_REVIEW_R2.json contains the same scores, fixes, checks, scope and full absolute input paths.

