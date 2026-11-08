# Current ARC2-Global claim assessment

1 November 2026. B1-M/P0/P/G/B1c development studies and independent B2 are complete. Overall `claim_supported: partial`; `review_independence: same-family`; `acceptance_status: provisional`. Computational QA is separate from semantic assurance; no formal paper integrity audit was run.

| ARC2 minus declared baseline configuration | Positive family intervals | Unresolved | Negative family intervals |
|---|---:|---:|---:|
| A2M / Procrustes adaptation | 0/6 | 6/6 | 0/6 |
| LA2M20 adaptation | 0/6 | 6/6 | 0/6 |
| SimpleLinear official code, locked policy | 2/6 | 4/6 | 0/6 |
| Affine ridge, lambda10 | 4/6 | 2/6 | 0/6 |
| Embedding-Converter paper-spec adaptation | 5/6 | 1/6 | 0/6 |

On the prospective TREC-COVID test, the family-adjusted nDCG evidence supports 11 specific improvements. The 19 unresolved comparisons establish neither equivalence nor noninferiority. All six Procrustes point differences are negative; none has a negative family interval. The original DEV macro gains over all five baselines remain valid inspected DEV evidence, but broad Procrustes/LA2M advantage did not receive independent confirmation.

ARC2-Global is a compact closed-form forward adapter requiring no neural training. Under the declared 1,024-anchor protocol it improves aggregate DEV nDCG and shows independent advantages over specified Converter, affine-ridge and SimpleLinear configurations. Which alternative to use remains encoder-, budget- and metric-dependent. The two-step mechanism attribution remains DEV; B2 tested frozen external comparisons rather than one-step ablation.

Do not claim best use of every paid pair, guaranteed superiority over native incumbents, general equivalence, isolated efficiency/dollar savings, serving SLO, ANN or real traffic. Prior all-paid E5 losses and the mixed-gallery reversal remain material; partial backfill document counts are logical exposure, not measured deployment cost.

[Full fresh reviewer response](.aris/traces/result-to-claim/2026-11-01_b2/001-claim-review.response.md) | [Structured verdict](.aris/traces/result-to-claim/2026-11-01_b2/verdict.json) | [All numerical results](REPORT.md) | [All independent comparisons](results/b2_review_20261101/SUMMARY.md) | [Prior DEV assessment, preserved](.aris/traces/result-to-claim/2026-11-01_b2/prior_claim_assessment_20261031.md).

**Finite route:** complete the current result package and STOP. The next paper work is evidence integration and manuscript claim audit when authorized. Manuscript is unchanged; no automatic new experiments or model selection.
