# Presentation outline and evidence map

This is an editorial revision inside the release, not a change to scientific results.

## Outline / paragraph roles

1. Opening: staged migration is the problem; vector reuse is the practical motivation.
2. Method: centered initialization, two tangent corrections, affine final artifact.
3. Evidence: DEV macro, mechanism contribution, prospective gains, matched all-paid case.
4. Advantage: compact final weights and no neural training.
5. Scope: comparison conditions are explicit; full results are linked once.

## Claim-to-evidence map

| Highlight | Evidence file | Status |
|---|---|---|
| Broad development gain | results/b1c_r3_review_20261031/evidence/run/scoring/summary.json | Saved positive family interval; condition label preserved |
| The second correction contributes | results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json | Saved positive family interval; condition label preserved |
| Matched all-paid evidence | results/b1p_r5_review_20261027/scoring/results_summary.json | Saved positive family interval; condition label preserved |
| Prospective transfer gain | results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json | Saved positive family interval; condition label preserved |

Parameter storage is derived from the declared source/target dimensions and the frozen ConverterConfig.hidden_multiplier=5 architecture. All affine coefficients and neural weights are compared as float32. Ridge shares the affine coefficient count.

## Editorial self-review

- Contribution: lead with the compact adapter and measured retrieval gains.
- Clarity: one purpose per paragraph; results carry their dataset/encoder/fitting regime.
- Experimental strength: show the strongest observed gains with saved uncertainty.
- Completeness: all locked methods/outcomes remain in full reports and the atlas; no study is represented as unperformed.
- Method design: preserve λ=10/two steps and distinguish final parameter bytes from operational cost.

No new experiment, parameter selection, effect-size calculation from labels, or external-review verdict was introduced. This is a local editorial self-review.
