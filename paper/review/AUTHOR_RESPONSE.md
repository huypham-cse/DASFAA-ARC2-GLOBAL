# Applied editorial improvements

This is the writing executor's response, not a replacement reviewer verdict. Earlier reviews and their exact input snapshots remain unchanged.

## Scientific clarity

- FiQA method selection after inspecting scores is explicit in Setup.
- Converter's paired-vector MAE selection is distinguished from the original retrieval-based validation.
- LA2M20's local maps and singleton global fallback are explicit.
- The ridge contrast refers to the initialized correction procedure; the ablation does not attribute its gain uniquely to projection.
- Penalty controls are sensitivity around a frozen setting, not proof against parameter-search effects.
- Query-bootstrap uncertainty is conditional on observed seeds/collections/pairs; inspected development selection is not corrected by that bootstrap.
- The destination-query/single-gallery operating constraint and native Full-X alternative are clear.
- FastFill and spherical-interpolation prior work now locate the exact tangent-update contribution.

## Stronger research presentation requested by the user

- Abstract and contribution bullets lead with directional refinement, all-five development macro gains, 23/24 Procrustes point gains, prospective E5 improvements and compact inference.
- Results lead with what the method achieves. Run-count/status narration is removed. Full baseline panels remain in all main result tables.
- All 30 prospective comparisons remain represented in one absolute-quality table: eleven daggers mark positive family-adjusted ARC2 comparisons; unmarked cells cross zero. The full 11/19/0 count table remains generated for the evidence package rather than occupying main-paper space.
- The matched all-paid result retains both migrations and every baseline. The cross-regime fixed-versus-all-paid limitation remains one sentence rather than a repetitive front-page warning.
- Compactness is explained positively as one affine inference stage and coefficient storage; the 114.7x comparison remains against the evaluated Converter's parameter bytes.
- Numerical source data, hypotheses, algorithm, labels and historical results were not changed.

## Figure redesign

The first draft's generic sans-serif mechanism has been replaced with editable native LaTeX/TikZ, Computer Modern typography and the title-tab/panel visual language of the user's `fig_arc2_mechanism_v2`.

The current figure uses the correct global computation: centered Procrustes, exactly two tangent corrections, one affine coefficient matrix, no local residual. The worked 24-document query and budget illustration is explicitly marked schematic. Numerical plots now use actual LaTeX serif typography with the same data and a complete baseline legend. The previous generic drawing command redirects to the current TikZ builder to avoid regenerating the rejected design.

## Review disposition

Completed result-to-claim: yes for its bounded claim, high confidence, same-family/provisional. Completed substantive review: proceed after identified editorial fixes. Completed fresh novelty review: proceed with a specific defensible delta; not a proof of priority or an acceptance prediction. Final separate zero-context paper audit: unavailable due to quota, not PASS. This is a finished draft for human review, with that last agent audit still pending.
