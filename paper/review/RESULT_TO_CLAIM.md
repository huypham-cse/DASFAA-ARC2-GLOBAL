# Result-to-claim review of the new mapper manuscript

- `claim_supported: yes`
- `confidence: high`
- `review_independence: same-family`
- `acceptance_status: provisional`
- `integrity_status: unavailable` (no `EXPERIMENT_AUDIT.json` found; the numerical checks below passed).

The current, bounded central claim is supported: two tangent-residual corrections provide a useful refinement of a compact affine document adapter, with development macro improvements, a development-supported second update, and selective prospective gains. This verdict applies to the manuscript as actually qualified. It does not convert the older, broader universal-superiority claim into a positive result or alter earlier campaign verdicts. The paper can proceed without another scientific run.

## What the results support

1. **The implemented adapter matches the mathematical description.** `src/arc2_global/model.py` expands the raw centered rectangular Procrustes map, fits norm-scaled tangent residuals, regularizes the correction including its intercept, performs exactly two updates at lambda 10, and stores a final float32 coefficient matrix. `solver_backend.py` supplies the separately identified primal solve. The normalization derivative in the manuscript is correct and appropriately limited to a local motivation rather than a retrieval guarantee. Final coefficient storage is exactly 295,680 float32 values, 1,182,720 bytes, or 1.1279296875 MiB. This supports the stated 1.13 MiB coefficient-only compactness.

2. **The fixed-anchor development macro claim is correct.** In B1c-R3 `aggregate_contrasts`, all five saved nDCG family intervals are positive. ARC2 minus Procrustes is 0.0243251090, with interval [0.0181321752, 0.0307916403]. The two migration-specific descriptive effects are 0.0257329362 and 0.0229172818. The 23/24 Procrustes point gains and 24/24 point gains against every other baseline are correct. The paper explicitly distinguishes these point counts from tested wins. The Procrustes Recall effect is -0.0002385904, with descriptive interval [-0.0049436262, 0.0043358500]; the manuscript correctly avoids claiming a Recall gain.

3. **The second correction is supported on development data.** B1-M `overall_macro` gives two minus one step = 0.0069238629, with its separate family interval [0.0038093883, 0.0099591262]. The ridge and lambda-control statements also match their primary fields. These controls establish an aggregate development contribution, not that two steps are optimal or independently necessary on TREC-COVID. The draft does not claim the latter.

4. **The prospective result is reported correctly and at the right scope.** All 30 B2 `contrasts[*].ndcg10.ci_bonferroni_family95` decisions reproduce: 11 positive, 19 unresolved, zero negative. Converter has five confirmed contrasts, ridge four, and SimpleLinear two. E5 improves over the declared Converter and ridge configurations at all three budgets. Every Procrustes point difference is negative; all Procrustes and LA2M family intervals are unresolved. The manuscript explicitly says this neither establishes equivalence nor noninferiority. The endpoint-verification seal completed at 20:11:42 UTC, before the recorded first final-label opening at 20:12:17 UTC, and its hash matches the scorer's declared seal.

5. **The matched all-paid result supports a useful MiniLM operating point.** B1-P's 32-contrast family confirms MiniLM ARC2 above Procrustes, LA2M, SimpleLinear and Converter; ridge is unresolved. The E5 negatives against Procrustes and LA2M, positives against SimpleLinear/ridge, and unresolved Converter comparison are all correctly retained. So are the negative MiniLM fixed-ARC2 versus all-paid-baseline comparisons. The paper correctly treats fixed supervision and equal paid-document exposure as different comparisons.

6. **The mixed-gallery reversal is real and correctly descriptive.** B1-G's five-seed aggregate records reproduce the quoted all-paid E5 ARC2 nDCG drop from 0.3149077504 to 0.2918669821, Recall drop from 0.6541642458 to 0.5594899234, and paid top-10 share drop from 0.491640 to 0.064720. MiniLM nDCG instead rises from 0.3509507352 to 0.3671460214. Holding a fitted mapper fixed isolates the replacement intervention for these endpoints. It does not identify the causal explanation for the score imbalance, which the draft correctly leaves open.

## What the results do not support

They do not establish a general independent win over Procrustes/LA2M, uniformly beneficial all-paid fitting, universal optimality of two updates or lambda 10, monotonic improvement after true-vector replacement, an independent second-step ablation, or deployment latency/cost savings. The current results and discussion already acknowledge these boundaries. The paper is a mapper and representation-quality study; a complete serving-system experiment is not a missing prerequisite for its present contribution. Compactness also holds for other affine mappers, so it should remain an architectural property of this directional refinement rather than an exclusive advantage over all baselines.

## Missing evidence and actionable wording

No additional scientific evidence is necessary for the scoped central claim. No important numerical error was found in the inspected sections or generated tables. Two small editorial refinements would make the evidence boundary more explicit:

- In experimental setup, add that ARC2's frozen form was selected after inspecting FiQA development scores. The existing statement that these collections were inspected during development is directionally correct; this addition states the selection provenance directly, as recorded in `configs/method.json`.
- Replace “The penalty controls also distinguish this effect from an unrestricted parameter search” with “The penalty controls probe sensitivity around the frozen setting.” Three fixed settings do not establish that unrestricted search played no role historically or that lambda 10 is optimal. The surrounding results and the decision to retain lambda 10 are correct.

Suggested central claim: **“ARC2-Global adds two tangent-residual ridge corrections to a centered Procrustes initialization while retaining one compact affine adapter at inference. Under matched fixed-anchor supervision it improves development macro nDCG over the five evaluated baseline configurations; the second correction contributes on development data, and a prospective collection confirms selected gains with encoder-dependent transfer.”**

## Next experiments needed

- **Necessary for the current claim:** none. Preserve the existing qualifications and make the two wording refinements above.
- **Optional extensions only if the claim is later expanded:** independently test one versus two updates to claim prospective second-step necessity; evaluate further prospectively locked collections to claim broader alignment superiority; measure actual encoding/serving workflows to claim physical migration savings. These are distinct future claims, not gates for completing this manuscript, and no run is authorized by this review.

## Verification scope

This review read the seven requested manuscript sections, all generated TeX tables, all five primary scoring JSON files, numerical fitting/application source, relevant locks, statistical implementation, and B2 verification/opening receipts. It did not rely on the legacy `manuscript/` placeholders and did not access network qrels, fit models, encode text, or run retrieval.

Read-only recomputation checked all 160 development means, 40 TREC means and 28 all-paid means against saved per-query arrays, with maximum errors 3.33e-16, 1.67e-16 and 2.78e-16. All five development family intervals, all five mechanism family intervals and all 32 all-paid family intervals were regenerated from their locked query resampling; maximum errors were below 9e-17. All 30 TREC family intervals matched saved bootstrap draws exactly. Details and source hashes are in `RESULT_TO_CLAIM_NUMERIC_CHECKS.json`. These numerical checks do not upgrade this same-family semantic judgment beyond provisional acceptance.
