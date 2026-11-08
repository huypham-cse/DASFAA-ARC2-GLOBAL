# Method section: code map and internal self-review

Written 1 November 2026 for `paper/sections/method.tex`. This is an internal
authoring record, not paper prose. Source code, scientific locks, raw runs and
the legacy `manuscript/` were not changed. The current user authorization
releases paper writing only; no scientific run was performed here.

## Section outline and paragraph roles

1. **Opening / overview:** destination-space proxies, mixed gallery, and one global map.
2. **Setting / challenge:** source and destination dimensions; direct destination queries.
3. **Budget / design:** `|A union S|`, charged anchors, nested replacement, supervision versus replacement.
4. **Initialization / design:** centered rectangular Procrustes, expanded raw affine map, arithmetic parity.
5. **Angular correction / motivation:** remove the radial discrepancy; explain the norm factor with a first-order identity.
6. **Fitting / design:** two regularized correction solves, shared factorization, regularized intercept, no neural/local component.
7. **Output / interpretation:** affine collapse, normalization, true-vector overwrite, deterministic exact retrieval.
8. **Cost / scope:** final coefficient storage, backend-dependent fit cost, logical exposure versus physical encoding.

Pipeline sketch: source vectors + paired destination anchors -> centered raw
Procrustes -> tangent target -> shared ridge correction -> recomputed tangent
target -> second correction -> final affine map -> unit proxies -> true-vector
overwrite -> exact search by direct destination queries. The parent author
supplies the visual mechanism figure separately.

## Precise source map

All paths below are relative to `D:/DASFAA-2027-paper`. Ranges are source line
ranges inspected on this date, not citations to manuscript placeholders.

| Paper item / claim | Implementation or locked source | Status / qualification |
|---|---|---|
| Unit float32 paired vectors | `src/arc2_global/numerics.py:6–16`; `model.py:96–103` | Supported; norms checked to absolute tolerance `1e-4`. |
| `384 -> 768` dimensions | `configs/b2_lock.json:233–320`; `ops/b2_stage.py:171–174` | Supported for the two evaluated encoder pairs; method notation allows general positive dimensions. |
| Destination queries are encoded directly | `ops/b2_inputs.py:266–299` encodes document and query roles separately with each encoder's prefixes; `ops/b2_stage.py:230–287` routes destination query matrices to mixed endpoints; `numerics.py:35–41` maps only documents | Supported. The method does not map source queries. |
| Charged unique budget `|A union S|` | `configs/method.json:14`; `numerics.py:44–64` | Supported. Implementation returns an anchor-inclusive paid set, hence manuscript's convention `A subseteq S`. |
| Random anchors and independent backfill stream; nested paid sets | `ops/b2_stage.py:82–103` | Supported: `SeedSequence([seed,0])` for anchor choice, `[seed,1]` for backfill permutation, then charged-budget helper. |
| Fixed 1,024 paired anchors | `configs/method.json:9`; `configs/b2_lock.json:185`; `ops/b2_stage.py:316` | Supported. Constants in early locked files can have stale workflow status; no status string was used as completion evidence. |
| All-paid-pairs is a separate comparison | `ops/b1p_stage.py:170–176` | Supported: fixed1024 uses anchors; all-paid uses paid IDs. |
| Fit needs paired document supervision, no labels or queries | `model.py:89–119`; `solver_backend.py:79–110` | Supported. Reference API also receives full source docs to validate/select anchors; numerical fitting consumes only paired anchor rows. |
| Thin centered rectangular SVD and orientation | `procrustes.py:17–30` | Supported: cross-covariance is destination-by-source, `W=U@Vt`, output uses `W.T`. |
| Raw affine expansion, with intercept | `model.py:39–60` | Supported: top block `W.T`, final row `tm-sm@W.T`; float64 expansion of original float32 means/matrix; no fitted scale and no base-row normalization. |
| Raw and normalized initialization parity check | `model.py:106–116` | Supported at absolute tolerance `1e-6`. |
| Tangent residual target | `model.py:73–81`; `solver_backend.py:63–71` | Supported exactly: norm times target minus current-direction inner product times direction. |
| Lambda 10 and exactly two updates | `model.py:12–16,69–86`; `configs/method.json:5–8` | Supported. No convergence stopping or extra correction. |
| Objective regularizes delta, including delta intercept | `model.py:66–81`; `solver_backend.py:36–38,56–71` | Algebraically supported. `X` includes an all-ones column, and identity ridge covers all `p` coordinates. It is not a penalty on the final `B`. |
| Reference dual, one reused `m x m` factorization | `model.py:69–80` | Supported. Fit cost must include cubic anchor-count factorization; final coefficient storage does not imply constant fit memory. |
| Separate primal backend and exact-arithmetic equivalence | `solver_backend.py:1–5,18,30–76` | Supported. It factors `p x p`, explicitly identified as `arc2_global_tangent2_primal_float64_r1`. |
| Primal is used beyond all-paid | `ops/b1p_stage.py:55–79`; `ops/b2_stage.py:24–25,266–274` | Important: B2 imports `cpu_fit` from B1-P and therefore also uses primal for its fixed1024 ARC2 fits. The paper does not claim all main timing rows use dual. |
| Float64 updates, final float32 storage | `model.py:66–86`; `solver_backend.py:56–76` | Supported. The first-step float32 snapshot is diagnostic; reference second-step arithmetic continues from float64 `coef`. |
| Affine collapse plus one final normalization | `model.py:146–157`; `numerics.py:35–41` | Supported. No intermediate nonlinear inference layers. |
| Selected true vectors overwrite proxies, including anchors | `model.py:127–143` | Supported; exact fitted anchor vector equality checked before overwrite. |
| Exact score arithmetic and deterministic ties | `retrieval.py:5–29`; `ops/b2_stage.py:35–38` | Supported: float32 batch matrix product; stable descending-score argsort preserves ascending document row index at exact ties. This is not lexical ID sorting. |
| Identical-ID exclusions | `retrieval.py:13–27`; `ops/b2_stage.py:35–38` | Supported as an explicit dataset/campaign flag, not an unconditional model component. |
| No local residual or neural mapper training | `configs/method.json:7–8`; `model.py` complete fit/application path | Supported. Frozen encoders are still neural encoders; claim concerns fitting the mapper only. |
| 295,680 coefficients, 1.13 MiB | `(384+1)*768=295680`; `295680*4=1182720`; `1182720/(1024*1024)=1.1279296875` | Exact structural calculation, includes bias. Excludes encoder, gallery, saved fit diagnostics, and model dataclass's retained arrays. |
| Cached exposure differs from physical encodes | `ops/b1p_stage.py:78`; `ops/b2_stage.py:344`; `ops/b2_inputs.py:277–299` | Supported. Fitting/ranking from caches records zero new physical encodes; independent acquisition separately produced full vectors for reference/cache construction. Logical budgets do not claim a partial physical deployment. |

## Algebra checked separately from empirical claims

### Normalization identity

For a fixed nonzero **row** vector `z`, put `r=||z||` and `u=z/r`.
Differentiating `r` in direction `h` gives `Dr[h]=u h^T`. Hence

`DN(z)[h] = h/r - z (u h^T)/r^2 = h(I-u^T u)/r`.

For `v=y-(u y^T)u`, `v u^T=0`; choosing `h=r v` therefore yields
`DN(z)[h]=v`. Taylor expansion at a nonzero `z` gives the displayed paper
identity as epsilon tends to zero. The remainder is local, for fixed `z,h`.
It is not asserted uniformly near `z=0` (the implementation rejects raw
norms at or below `1e-12`). This is elementary differentiation explaining an
implemented target, not a new convergence theorem or an empirical result.

The actual raw perturbations are rows of `X delta`, which share a regressor
and need not equal the prescribed targets. Moreover epsilon is effectively
one in the executed update. Consequently the identity does **not** imply
monotone cosine improvement, lower retrieval loss, convergence, uniqueness
of a final mapping, or a particular nDCG gain. All such claims are excluded.

### Ridge objective and backend equivalence

Strict convexity for positive lambda gives the normal equation
`(X^T X+lambda I_p)delta=X^T T`, including the intercept coordinate. The
identity `(X^T X+lambda I_p)X^T=X^T(XX^T+lambda I_m)` yields
`delta=X^T(XX^T+lambda I_m)^(-1)T`, exactly matching the reference dual code.
This is equivalence of the real-arithmetic equations. Float64 solve pathways
and float32 application can produce different near-tie orders; the paper does
not assert bitwise backend identity.

### Complexity accounting

Let `m` be fitted pair count, `p=d_s+1`, `d_t` destination dimension. Dense
arithmetic costs used in the paper are:

- Cross-covariance: `O(m d_s d_t)`; thin rectangular SVD: `O(d_s d_t min(d_s,d_t))`.
- Reference dual: Gram `O(m^2 p)`, Cholesky `O(m^3)` once, each correction
  `O(m p d_t + m^2 d_t)`, Gram storage `O(m^2)`.
- Identified primal: Gram `O(m p^2)`, Cholesky `O(p^3)` once, each correction
  `O(m p d_t + p^2 d_t)`, Gram storage `O(p^2)`.
- Both additionally retain/read paired inputs, targets, and coefficients;
  Gram storage is not total fitting memory.
- Complete proxy application: `O(N p d_t)`; coefficient-only storage `O(p d_t)`.
- Exact retrieval: ordinary dense query-gallery inner products and stable sort;
  no ANN acceleration claim and no measured physical deployment cost.

The map is affine in raw coordinates and normalized at output. Calling the
whole normalized forward function linear would be imprecise; paper language
uses "affine map" for coefficients and explicitly states normalization.

## Five-dimension self-review

| Dimension | Skeptical question | Answer / resolution |
|---|---|---|
| Contribution | Does compactness alone distinguish ARC2 from ridge or Procrustes? | No. Main design is tangent-residual refinement of a centered initialization for mixed galleries. No exclusive compactness or universal quality claim appears. |
| Writing clarity | Can a reader reconstruct orientation, bias, normalization and updates? | Yes: row-vector convention, dimensions, exact base expansion, objective, target, two-step range, and overwrite rule are explicit. |
| Experimental strength | Does the method section sneak development findings into independent claims? | No performance number or win appears here. Setting and storage numbers are code/structural facts. Empirical scope belongs to results. |
| Evaluation completeness | Does exact search hide arbitrary tie handling or budget-free anchors? | No. Anchor union accounting, true overwrite, descending-score/ascending-row ties, and optional identical-ID exclusion are explicit. |
| Design soundness | Does the first-order identity guarantee finite coupled update improvements? | No; the prose explicitly limits it. Ridge targets are refit, not an asserted global cosine optimizer. |

Additional checks: terminology is stable (source/destination, anchor/paid,
raw affine/proxy/mixed gallery). Every paragraph maps to the overview; the
equations occur in execution order. No unsupported physical speed, dollar,
SLO, real-traffic, universal dominance, or convergence claim remains.

## Verification record

- Draft count: approximately 1,006 alphabetic prose words after stripping
  displayed/inline mathematics and LaTeX commands; 1,141 whitespace tokens
  including equations and pseudocode. Both counts are approximate.
- Source-to-equation inspection completed for the full fit, application,
  replacement and retrieval paths listed above.
- Local standalone LNCS compilation passed twice with `pdflatex` and the
  existing `manuscript/llncs.cls`; all cross-references resolved. No overfull
  or underfull box warnings. The standard LNCS/amsmath `vec` accent warning is
  unrelated to this section. PDF: four standalone pages (about 3.3 pages of
  content); the parent paper controls integrated pagination.
- Rendered all four pages with `pdftoppm` and visually inspected them:
  equations, subscripts, rectangular orientation, piecewise gallery rule and
  six-row pseudocode fit the LNCS column. No clipping or text collisions.
- Temporary QA output is under
  `C:/Users/Gia Huy/AppData/Local/Temp/arc2_method_qa_20261101/` and outside the
  repository. An initial shell attempt hit the environment's unavailable
  short-name TEMP path; rerunning from the resolved long path succeeded.
  Its accidental root `texput.log` was removed.
- No scientific experiment, numerical source edit, lock edit, raw-result
  edit, or legacy manuscript edit was performed.
