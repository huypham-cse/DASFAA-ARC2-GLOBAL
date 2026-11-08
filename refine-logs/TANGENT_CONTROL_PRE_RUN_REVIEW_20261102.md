# TC1 static pre-run review

Date: 2026-11-02. Verdict: **PASS_TO_COMMIT_AND_SMOKE**. No remaining must-fix finding in the reviewed snapshot. This is internal same-family/provisional review, not independent external validation or evidence that runtime smoke has passed.

Reviewed lock SHA256: `c48679786a8216e18fcdd61fe7cae366b7c9b0383c7a3da35293c1a10e78c30b`. All 17 pinned local source/protocol hashes matched this lock at review. The precise protocol, sources and lock must be committed and deployed with that identity before synthetic or real-data smoke. Full remains conditional on successful matching synthetic and real smoke receipts; scoring remains conditional on a complete full seal. Any subsequent scientific-source/lock change needs refreshed review/pins before execution.

This review read source, protocol, lock and prior design only. No Python/scientific tests, fitting, retrieval, label-file reading/hashing, remote execution, manuscript changes or agent delegation occurred. Static source SHA checks are not a verification of remote caches or labels.

## Scientific computation: pass by inspection

`residual_ablation.py` uses exactly T=r(Y-cu), C=r(Y-u), and E=Y-Z. Each trajectory starts from the same raw centered Procrustes B0, recomputes its own target, and performs exactly two dual Cholesky ridge corrections with lambda10, including the intercept. Float64 is retained between updates, followed by a single float32 coefficient export and the common normalized inference path. No zero-centered direct-ridge substitution, normalization between steps, neural fit or control-specific tuning appears.

The tangent computation retains `_tangent2`'s array dtypes, Gram expression, Cholesky defaults, target arithmetic and update ordering; separating `cho_solve` into an intermediate variable does not change the numerical operation. The synthetic suite compares both exported snapshots exactly to frozen `_tangent2`; each real group additionally requires exact final coefficient equality. Actual bitwise identity remains a runtime assertion, not a claim made by static inspection.

Forty fresh rankings correctly comprise four rows x two pairs x five seeds, with B0 descriptive and only three update trajectories per pair/seed. All arms share inputs, paid replacements, native destination queries, mapping blocks512, exact float32 search batches16 and stable row-index ties. Current protocol confines findings to already-inspected FiQA development; negative/no-op outcomes cannot trigger a method change.

## Paid exposure and scoring gates: pass after fixes

The current runner validates anchor/paid indices with `_indices`, exact counts1024/28819/43228, sorted paid50/paid75 sets, subset membership, cached target shape/dtype and paid50/query unit vectors. `searchsorted` obtains exactly the paid50 slice and then releases the paid75 mapping reference. Fit receives only selected anchor rows. Withheld25 target rows do not enter fitting, selection or diagnostics; whole-cache byte hashing establishes identity only. Report28819 logical paid destination vectors and zero physical encodings this run, without a physical-cost claim.

The separate scorer now checks source hashes; full status/stage and matching metadata/seal lock hashes; all40 expected pair/seed/method identities and distinct paths;50pct budgets; the complete lock-derived input registry and its hashes; all sealed artifact hashes; original ID-file SHA plus ID lengths/types/uniqueness; and ranking bounds, shape, unique hits and identical-ID exclusion. These gates run before the DEV label-access receipt and qrel opening. Existing graded nDCG/Recall rules preserve all500 queries and the full positive-qrel denominator. Unique output/scoring directories and preserved failure traces avoid silent retry/overwrite.

Resolved findings during review: scorer ID validation and distinct ranking paths; complete input-manifest comparison; stage/budget/metadata-lock checks; negative/out-of-range index rejection and cache shape checks. The runner now **copies original ID bytes** rather than reserializing JSON, preventing an otherwise avoidable locked-SHA failure. No unresolved arithmetic or input-gate bug was identified in the final reviewed snapshot.

## Inference and synthetic coverage: pass by inspection

For every method/pair the scorer first averages the five seed-specific per-query arrays. It forms exactly T-C and T-E for both pairs, then resamples the same query indices across the four columns.100 batches of200 draws give20,000 paired draws with default_rng seed20261102. Default linear quantiles.00625/.99375 correctly give98.75% individual Bonferroni intervals for K4 and approximate95% family coverage. Strict lower>0 / upper<0 rules preserve unresolved contrasts. B0/Recall/seed dispersion remain descriptive. Saved per-query arrays and bootstrap draws support independent local recomputation and additional descriptive tables without new primary tests.

Synthetic fixtures are appropriately nontrivial: random coupled anchors with a held-out source set; independent primal/dual updates and normal equations; common-state radial/tangent identities; positive-scale equivariance; Euclidean second-step recurrence; aligned unequal-radius and antipodal targets; a least-squares-stationary Euclidean no-op; stable ties; zero-direction rejection; and existing graded/binary metric fixtures. Their tight tolerances apply to small well-conditioned synthetic matrices. The real smoke records continuous energies, radii, solve residuals and unpaid proxy/ranking changes, and stops on exact T/control unpaid-proxy identity for interpretation. It does not score quality or repair a legitimate no-op. Runtime success and resource requirements still need the committed smoke.

## Bounded follow-through

Proceed only through the existing finite campaign after commit/deployment verification: synthetic -> both-pair seed17 smoke ->40 full rankings -> separate DEV scoring -> local raw-output verification/table/figure -> ARIS interpretation -> STOP. No arbitrary time/RAM/VRAM cutoff, result-dependent selection, manuscript edit or new scope is introduced.

Minor reporting note, not a launch blocker: call C the **prediction-norm-scaled chordal control** or explicitly define “matched norm” as matching factor r. Its target length is not matched to T. A T-versus-E win alone cannot isolate projection; a T-versus-C win alone cannot establish ordinary-Euclidean superiority. Conditional query intervals cannot remove prior development selection or establish independent-test/general-population superiority.

Inspected: `src/arc2_global/residual_ablation.py`; `ops/tangent_control_{run,score,campaign}.py`; `protocols/FIQA_MATCHED_RESIDUAL_CONTROLS_20261102.md`; lock/builder; relevant frozen model/numerics/retrieval/metric dependencies; previous design. Reviewed source identity is recorded in the companion JSON.
