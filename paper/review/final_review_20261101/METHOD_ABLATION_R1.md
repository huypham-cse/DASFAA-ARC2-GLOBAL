# ARC2-Global method and ablation review, R1

Date: 2026-11-01. Reviewer: gpt-6.1-sol, high, as explicitly requested. Review independence: same-family. Acceptance status: provisional. Skills applied: aris:research-review, aris:ablation-planner, aris:novelty-check; formula-derivation is incorporated below. No further agents, scientific runs, relevance scoring, or manuscript changes were performed. This is an independent reading of current source, current sections, saved results, and primary closest-work texts; older reviews and scores were not read.

## Assessment and scores

The implementation and current method equations agree. ARC2 is a defensible, modest algorithmic contribution: a particular finite directional refinement of an established alignment map, with useful evidence under limited paired supervision and an honest mixed-gallery evaluation. The strongest paper is an empirically supported compact adapter for a required destination-query transition. It is not a general advance over all geometric mappers: prospective TREC-COVID Procrustes point means exceed ARC2 in all six conditions, and their family intervals remain unresolved.

| Dimension | Score / 10 | Reason |
|---|---:|---|
| Novelty | 6 | The two ridge-fitted, norm-scaled tangent targets folded into a single affine document map are a concrete delta. Alignment, cosine geometry, residual refinement, lightweight adapters, and partial backfilling all have clear predecessors. No inspected named paper contains this exact evaluated computation. |
| Technical soundness | 8 | Correct normalization derivative, correctly oriented rectangular initialization, update-only regularization including bias, and exact-arithmetic primal/dual equivalence. The paper already avoids a convergence claim and identifies floating-point distinctions. |
| Mechanism evidence | 6 | Zero/one/two updates, penalty controls, direct ridge, all-paid fitting, and actual mixed-gallery interventions are already substantial. The causal value of tangent projection is not isolated from initialization and the retained prior, and the method is not prospectively superior to Procrustes. |
| Practical significance within stated scope | 7 | One small affine artifact, native destination queries, and prospective E5 wins over the evaluated Converter/ridge configurations make a useful operating point. The current evidence supports choosing an adapter during a mandated transition, not a recommendation to upgrade an otherwise satisfactory source model. |

These are reviewer judgments, not acceptance probabilities or guarantees. Recommendation: **PROCEED WITH CAUTION**, with the caution specifically about mechanism attribution and scope of prospective superiority, not a claim that nearby work invalidates the method.

## Verified implementation and wording

`src/arc2_global/model.py:39` expands the raw centered map into float64 coefficients, without normalizing its output or fitting a scale. At lines 69–81 the design is augmented by ones; a dual Gram plus 10I is factored once; exactly two targets `norms * (y - sum(unit*y)*unit)` are recomputed and added. The final matrix is cast to float32. `solver_backend.py:59–71` implements the same targets with a primal solve. `baseline_adapters.py:39–45` fits direct affine ridge to Y and penalizes the full coefficient, including the bias.

The paper's derivative for a nonzero row vector, `D N(z)[h] = h(I-u^T u)/r`, is correct. Its chosen **target** is tangent at each anchor. However, the regression output `(Xtilde Delta)_j` need not be tangent at anchor j: the shared fit mixes anchor targets. The paper should continue to say that it *fits tangent targets*, rather than claiming the fitted correction eliminates every radial component. The current statement that finite-update benefit is empirical is correct.

For the evaluated 384-to-768 map, W is 768 by 384 and W^T W = I in exact arithmetic; the centered raw linear part preserves source displacements before translation. The refined map is unconstrained. This is appropriately described as a rectangular semiorthogonal initialization, not an orthogonal guarantee for the final model.

The final artifact has `(384+1)*768 = 295,680` float32 coefficients, 1,182,720 bytes, 1.128 MiB rounded to 1.13. Dividing 33,927,168 Converter float32 parameters by 295,680 gives 114.7439, rounded to 114.7. The manuscript correctly restricts this ratio to parameter bytes and excludes galleries, fitting state, encoder weights, index work, and end-to-end cost. “Requires no neural mapper training” is accurate; “requires no training” would obscure fitted anchors and linear solves.

## Ablation coverage from saved evidence

Evidence paths:

- M: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`, especially `overall_macro` and per-condition means.
- P: `results/b1p_r5_review_20261027/scoring/results_summary.json`, including its 32 predeclared contrasts and fixed/all-paid regimes.
- G: `results/b1g_r1_review_20261027/scoring/results_summary.json`, particularly `aggregate_five_seed_conditions` and diagnostic limits.
- T: `results/b2_review_20261101/tables/derived_summary.json`, a descriptive copy of verified saved-score contrasts, and the bundle manifest. No fresh uncertainty calculation was performed for this review.

| Reviewer question | Status | Already available evidence / permissible conclusion |
|---|---|---|
| Does refinement improve its starting map? | supported | M compares zero updates (centered Procrustes) with two; macro nDCG difference +0.024325. The primary baseline-family interval in current results is [0.018132, 0.030792]. The separate M ablation-family draw has [0.018015, 0.031021]; do not interchange independently saved families. |
| Does the second update help beyond one? | supported | M two-minus-one +0.00692386, saved ablation-family interval [0.00380939, 0.00995913]. This establishes incremental development value, not optimality of two updates over every possible count. |
| Is lambda=10 uniquely best or robust? | supported, limited | M lambda=1 minus 10 is +0.00319750, interval [-0.00189038, 0.00830403]; lambda=100 minus 10 is -0.00925534, interval [-0.01321398, -0.00551025]. Already answers local sensitivity. It does not establish broad insensitivity or global optimality. Preserve the frozen 10. |
| Does the initialized procedure beat direct affine ridge? | supported | M +0.09565305, interval [0.07535299, 0.11663127]. This is a full-procedure contrast; direct ridge removes both prior retention and tangent targeting. Current results explicitly acknowledge this. |
| Is tangent projection itself the reason for the gain? | not isolated | No matched Procrustes-initialized radial residual-ridge correction was located in the evaluated panel. No claim that projection alone caused the full ridge gap is justified. A prose scope statement suffices for current claims. |
| Is Procrustes initialization necessary? | not isolated | Zero steps tests the starting map as a comparator, not an alternative initialization for the same tangent procedure. No zero/random/ridge initialization control is present. Such a run is optional unless initialization is claimed necessary or uniquely best. |
| Does the raw-norm multiplier empirically help? | not isolated | Its first-order role is exactly derived; no target-without-norm empirical control isolates its retrieval contribution. Do not conflate analytic motivation with an ablation win. |
| Are baselines handicapped by withholding paid fitting pairs? | supported, scoped | Main comparison matches the same 1,024 pairs and replacement rows across methods. P separately uses every paid pair for all six methods at FiQA 50%. The cross-regime contrast is disclosed, and the paper must keep both regimes visible. |
| Does all-paid fitting preserve the method ordering? | supported; answer is no | MiniLM all-paid ARC2=0.367146, versus fixed=0.307505; all-paid wins over Procrustes, LA2M, SimpleLinear, Converter, while ridge difference -0.000117 is unresolved. Fixed ARC2 loses each all-paid MiniLM baseline. E5 all-paid ARC2 loses to Procrustes and LA2M; its change from fixed has unresolved nDCG interval. |
| Can proxy-only quality select the mixed-gallery operating point? | supported; answer is no | G holds each fitted map and paid set fixed, then replaces proxies. E5 all-paid ARC2 nDCG 0.314908→0.291867, Recall 0.654164→0.559490; MiniLM nDCG 0.350951→0.367146. These directly measure opposite effects. Returned-share imbalance alone is explicitly not proof of calibration error. |
| Does the method generalize beyond development? | supported, comparator-specific | T has 11 family-supported baseline improvements: five Converter, four ridge, two SimpleLinear. E5 gains over Converter and ridge occur at all three budgets. No supported superiority to Procrustes/LA2M; no equivalence inferred from crossing-zero intervals. |
| Are all-paid, tangent-factor, initialization sweeps or many extra step counts mandatory now? | optional future | They would expand attribution/scope, but are not required to sustain the finite procedure and currently qualified claims. Do not tune them using final-test qrels. |
| Does compactness imply actual operational savings? | optional future | Structural coefficient storage and absence of neural fitting are supported. Encoding, serving latency, ANN behavior and deployment savings are different measurements; present paper does not claim them. |

The all-paid intervention increases m while keeping lambda=10 in a summed objective. It therefore changes both available supervision and the effective penalty relative to an average loss. It remains a valid operational comparison of the frozen procedure at larger fitting exposure, but should not be described as an isolated estimate of the causal effect of data quantity at fixed effective regularization.

## Closest work and defensible delta

Primary texts read from `paper/review/citation_sources/`: Yoon/Arik Converter; Yang/Cao 2026 translation; Maystre et al. Procrustes; Ricci et al. spherical interpolation; Vejendla Drift-Adapter; Jha et al. vec2vec; Dar et al. mini-vec2vec; Byun et al. MKP; FastFill. The attempted `la2m_pdf.txt` is a publisher challenge page, so I do not pretend to have read a full LA2M paper there. Its institutional primary abstract and the pinned integration implementation support the narrower local/global alignment description.

| Primary work | Closest overlap | Distinction this paper can defend |
|---|---|---|
| [Embedding-Converter](https://aclanthology.org/2025.acl-long.1237/) | Document-side transformation, regression and relational losses | ARC2 uses a finite sequence of affine ridge corrections rather than a neural converter; the actual evaluated baseline is a declared adaptation. |
| [Generalizable and Composable Multi-Model Embedding Translation](https://proceedings.mlr.press/v306/yang26e.html) | Embedding reuse, mixed target spaces, residual directions | H-MoE routes among local neural experts and regularizes residual directions using target principal components for mixing/chaining. ARC2's tangent plane is anchor-specific at its current prediction; these are different operations. |
| [When Embedding Models Meet](https://arxiv.org/abs/2510.13406) | Procrustes, partial upgrades, interoperable retrieval | ARC2 does not contribute Procrustes or its geometric motivation; it relaxes that starting map through two tangent-target regressions. |
| [Spherical interpolation](https://arxiv.org/abs/2609.39836) | Angular residual after alignment and cosine retrieval | SLERP combines old and aligned new **queries** along a spherical arc. ARC2 estimates one document map from paired anchors; it neither executes per-query interpolation nor requires the old query at serving time. |
| [FastFill](https://arxiv.org/abs/2303.04766) | Alignment plus partial backfilling; replacement may reduce quality | Mixed-gallery evaluation and a nonmonotone replacement effect are not first discoveries here. ARC2 contributes a different finite adapter and measured relevance behavior for these text migrations with anchor-inclusive accounting. |
| Drift-Adapter / MKP-Adapter | Frozen-backbone compatibility and lightweight fitted adapters | Their principal adaptation direction is new representation/query to the existing legacy space. The current paper's operational requirement is native destination queries and a destination-space gallery. |
| vec2vec / mini-vec2vec | Translation, initial alignment and iterative refinement | They infer correspondences from unpaired data; ARC2 uses known document pairs and fits the specific norm-scaled tangent target. “Procrustes plus refinement” alone is not a novelty claim. |

Recent-search coverage on 2026-11-01 included 12 targeted formulations spanning tangent/ridge/Procrustes, angular refinement, paired-budget migration, mixed-gallery affine translation and residual correction, including 2025–2026 constraints. Primary results confirmed the 2026 H-MoE and spherical papers. A newly surfaced [cross-day item-embedding study](https://arxiv.org/abs/2610.36408) is about inherited scale and downstream CTR, not the ARC2 computation. Searches did not identify an exact predecessor; they are not a proof that none exists. This review relies on primary papers/code rather than web review-site opinions.

One-sentence positioning: **ARC2-Global fits two norm-scaled tangent-residual ridge corrections to a centered rectangular Procrustes document map, retains a single affine inference artifact, and evaluates the resulting mapper when its proxies compete with paid native destination vectors.**

## Derivation package: exact interpretation of the existing update

### Target and status

Target: explain the existing update's relationship to cosine loss, the retained map, and arbitrary positive global scale. This is elementary algebra and mechanism interpretation, not a new algorithm or convergence theorem. Status: **COHERENT AS STATED**.

### Invariant object

The organizing object is the existing ridge projection of the state-dependent target `T(B)`. Cosine loss explains that target locally; judged retrieval remains the empirical endpoint. Neither is silently substituted for the other.

### Assumptions and notation

Write H = Xtilde, G = H^T H + lambda I, lambda>0, and B = B_t. Anchors y_j are unit vectors; z_j=h_j B is nonzero; r_j=||z_j||, u_j=z_j/r_j. H and lambda are fixed during both updates; T is recomputed from B. Identities below use real exact arithmetic. Positive-scale equivariance assumes every relevant prediction remains nonzero and both paths remain in the implementation's admissible range; finite-precision casts and the absolute 1e-12 rejection threshold need not preserve it for arbitrary scales.

### Derivation strategy and map

1. Differentiate normalized cosine loss at one current prediction.
2. Substitute its gradient into the exact target.
3. Change variables from Delta to B+Delta in the existing quadratic objective.
4. Propagate a common positive multiplier through the target and linear solve.

Only the normalization perturbation in the paper is first-order. Steps below are exact identities; their interpretation does not prove finite-step improvement.

### Main derivation

**Identity 1: norm-squared cosine-gradient target.** For `ell_j(z)=1-y_j(z/||z||)^T`, its row gradient is

`grad_z ell_j = -(y_j-(u_j y_j^T)u_j)/r_j`.

This follows by substituting `D N(z)[h]=h(I-u_j^T u_j)/r_j` into the directional derivative of ell. Consequently

`T_j(B) = -r_j^2 grad_z ell_j(z_j)`.

Thus the requested raw-space target is a norm-scaled negative cosine gradient. The actual Delta is `G^{-1} H^T T(B)`, so it is ridge-smoothed through the shared affine design. It is not ordinary gradient descent on the unweighted sum of cosine losses, nor the exact minimizer of that nonlinear loss, nor an asserted Gauss–Newton step.

**Identity 2: current-map prior.** Substitute `C=B+Delta` in the implemented objective. Its unique minimizer is

`B_{t+1} = argmin_C ||H C - (H B_t + T(B_t))||_F^2 + lambda ||C-B_t||_F^2`.

Uniqueness follows because the Hessian in each target coordinate is `2G` and lambda>0. This is a quadratic fit of a state-dependent pseudo-target with a penalty centered on the **current** map. It is not a penalty centered at zero and is not literally a fixed B0 prior on each separate step.

To expose the plain-ridge confound, hypothetically replace T by the radial-inclusive raw residual `Y-HB`. Algebra then gives

`B + G^{-1}H^T(Y-HB) = G^{-1}H^T Y + lambda G^{-1}B`.

The second term retains the prior. This identity explains why direct ridge differs even before tangent projection; it is not an evaluated ablation or a newly proposed variant.

**Proposition 3: positive global scale equivariance of the update.** Let c>0 and replace B by cB, with H, Y and lambda unchanged. Then z'_j=cz_j, r'_j=cr_j, u'_j=u_j, hence T(cB)=cT(B). Linearity of the ridge solution gives Delta(cB)=c Delta(B), so `F(cB)=c F(B)` for `F(B)=B+Delta(B)`. Induction gives the same property after both updates; normalized mapped outputs agree whenever defined. This is a global common-scale identity, not invariance to scaling individual anchor rows, changing the source normalization, lambda, or initialization geometry.

### Remarks, boundaries and open risks

The identities explain a geometric design choice and the role of the prior; they add no empirical claim. An individual target is orthogonal to its current direction, but the fitted row correction can have a radial part. Antipodal y=-u also yields a zero tangent target, illustrating why this is not a global convergence guarantee. No current evidence establishes finite-step descent, globally optimal step count, pure tangent causality, or a new retrieval theorem. The identities are checked by the displayed derivative, variable substitution, positive-definite normal equation, and induction; formal proof tooling is unnecessary for this routine algebra.

### Proposed concise LaTeX insert, for author review only

Priority: use the gradient identity and current-map prior in the method. Keep scale equivariance to an appendix or omit it if page space is tight. This snippet changes explanation, not computation:

```latex
For $\ell_j(z)=1-y_j\mathcal N(z)^\top$, the target also satisfies
$T_j^{(t)}=-(r_j^{(t)})^2\nabla_z\ell_j(z_j^{(t)})$.
It therefore requests a norm-scaled negative cosine-gradient correction,
which the shared affine ridge fit smooths across anchors. Equivalently,
\[
B_{t+1}=\arg\min_C
\|\widetilde X C-(\widetilde X B_t+T^{(t)})\|_F^2
+\lambda\|C-B_t\|_F^2.
\]
The penalty retains the current map as the center of each update.
These identities explain the target and regularization; they do not imply
that the fitted finite update decreases cosine loss or retrieval error.
```

Optional appendix sentence:

```latex
In exact arithmetic, for any common $c>0$ with nonzero predictions,
$T(cB)=cT(B)$ and the linear ridge solve gives $F(cB)=cF(B)$,
where $F(B)=B+\Delta(B)$. Thus positive global rescaling of the
initial coefficients leaves the normalized two-update map unchanged.
This algebraic property does not assert identical floating-point behavior.
```

## Minimum feasible edits now

1. Add the concise gradient/prior explanation above. It makes the design more interpretable without repackaging it as an untested optimizer. Preserve the existing normalization derivative and empirical qualification.
2. Add one sentence after the ridge result: “This comparison supports the initialized refinement procedure; it does not isolate tangent projection from retaining the Procrustes prior.” The current prose already says initialization and correction are evaluated together; the extra prior wording is the useful delta.
3. Make the intended operating requirement concrete near the start: destination queries are required and paid native vectors must share one destination gallery with proxies. Existing experiments then answer an actionable product choice even where retaining Full-X would be better if allowed.
4. Keep the positive all-paid MiniLM operating point prominent, while retaining the same-budget all-paid ridge unresolved comparison and E5 reversals. Do not call unresolved differences ties or equivalent quality.
5. Retain explicit comparison with H-MoE, SLERP and FastFill, limiting novelty to the exact finite adapter and measured text mixed-gallery behavior. No claims of being first to study mixing, angular residuals, or harmful backfilling.

No new experiment is mandatory for the present properly scoped factual claims. If a later paper revision wants to assert that tangent targeting itself is superior to ordinary residual fitting with the same prior, the minimal optional next scientific comparison is the prior-matched residual control; it needs a new immutable protocol and should remain outside this editing task. Initialization/norm-factor controls follow only if their unique empirical necessity becomes a claim. Do not spend runs repeating already answered 0/1/2, lambda1/10/100, all-paid, or actual mixed-gallery questions. No compute estimate is invented here.
