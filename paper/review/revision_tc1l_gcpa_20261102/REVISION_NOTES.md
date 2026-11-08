# MiniLM mechanism evidence and anonymous supervisor release

The revision presents the directional-target contribution directly: **two tangent ridge corrections strengthen mixed-gallery retrieval while retaining one affine inference stage**. No numerical method or scientific run has changed.

## Section outline and roles

- Abstract and introduction: compact affine method, broad development effect, matched-control support and held-collection operating points.
- Related work: identify GCPA's directional post-Procrustes correction, then distinguish destination supervision, the current-coefficient prior and finite affine updates.
- Setup: specify common initialization, ordered anchors, penalty, two updates, arithmetic/search environment and the original four-contrast correction.
- Results and Figure 3: show both matched controls alongside all five original macro controls; retain both families and their full intervals on separate axes.
- Conclusion: connect directional evidence to the single-map deployment form.

## Claim-to-evidence map

| Claim | Direct evidence | Scope |
|---|---|---|
| ARC2 0.3075 vs chordal 0.2935 and Euclidean 0.2959 | `results/tc1l_local_r1_20261102/full/scoring/summary.json`, `cell_index.json`, `per_query.npy` | FiQA development, MiniLM, 50% coverage, five seeds |
| Tangent minus chordal +0.0140 [0.0097, 0.0186] | Saved primary contrast and `bootstrap_draws.npy` | Original K4, 98.75% individual interval |
| Tangent minus Euclidean +0.0116 [0.0078, 0.0157] | Same frozen scorer output | Same family, two E5 contrasts pending |
| Both differences positive in five seed means | All 20 per-query cells | Seed means, not every query |
| GCPA trains a consensus-direction residual MLP with an angular trust penalty | [Official ICML/PMLR paper](https://proceedings.mlr.press/v306/achara26a.html), Section 3.4, Eq. 8 | Related work, no empirical GCPA comparison |
| Anonymous numerical evidence is supplied | Separate `ARC2-Global_Anonymous_Artifact_20261102.zip` | Frozen-output verification and mapper use; no physical deployment claim |

## Five-dimension self-review

1. **Contribution:** Is the new control informative beyond Procrustes initialization? Yes: initialization, paid pairs, penalty and update count are shared; both control intervals are positive. Chordal shares a scaling rule, not identical norms or later states.
2. **Writing clarity:** Does each new paragraph have a distinct role? Yes: setup defines the comparison; results state the effect and its interpretation; related work identifies the actual computational distinction. Redundant prose was condensed to retain standard 16-page LNCS layout.
3. **Experimental strength:** Are complete controls and uncertainty included? All four MiniLM arms, all five seeds and both original-K4 intervals are retained. Existing unfavorable regularization controls and baseline wins remain visible.
4. **Evaluation completeness:** Is local development confused with held-collection evidence? No. TC1L is explicitly a separate Windows development measurement; the completed TREC study remains the prospective test. This revision adds no test-label access or new experiment.
5. **Method soundness:** Does the explanation imply stronger guarantees than the computation gives? No. The radial-target interpretation is conditional on these two-step trajectories; no finite-step monotonicity, universal dominance or physical cost reduction is inferred.

The new quantitative audit is `paper/PAPER_CLAIM_AUDIT.md` and `.json`. Historical scorecards concern their original snapshots; this revision assigns no invented acceptance score. User will send the prepared supervisor packet. No public upload, email or conference submission is performed.
