# Fresh raw-evidence claim audit R2

**Verdict: PASS for the checked snapshot. Same-family; provisional.**

PASS for the checked local scientific claims: table values, headline comparisons, four saved bootstrap families, frozen-method equations and structural storage arithmetic match the specified raw scores/code. No required manuscript correction found in this bounded audit.

Auditor: gpt-6.1-sol / high, fresh child thread `/root/final_snapshot_audit_r2_20261101`. No delegation. The manuscript and scientific artifacts were left unchanged.

The machine-readable sibling contains 58 claim groups and SHA256 hashes for 520 declared manuscript, figure, score-array, raw ranking/endpoint, protocol, lock, receipt and source inputs. A final rehash found no stale input.

## Evidence and independent computations

| Raw authority | What was checked | Maximum error |
|---|---|---:|
| `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json` + index/arrays | 736 cells, 160 mean rows, all five equal-24-condition macro contrast intervals | means 3.33e-16; intervals 8.33e-17 |
| `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json` + index/arrays | 184 cells, 40 mean rows, all 30 contrasts and saved intervals | means 1.11e-16; contrasts/intervals 1.67e-16 |
| `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json` + four index/array pairs | 736 mechanism-panel cells, 160 mean rows, five macro contrast intervals | means 3.33e-16; intervals 5.55e-17 |
| `results/b1p_r5_review_20261027/scoring/results_summary.json` + index/array | 124 cells, 28 mean rows, all 32 contrasts and intervals | means 2.78e-16; contrasts/intervals 3.33e-16 |
| `results/b1g_r1_review_20261027/scoring/results_summary.json` + FiQA before/after arrays | Two all-paid ARC2 examples, five seeds each; paid top-10 share traced to case records | <1e-12 |

An independent script reconstructs query-bootstrap distributions from saved per-query metrics; it does not import or execute the campaign scorers. It also checks 27 LaTeX table rows, all 30 TREC dagger decisions, both plotted 40-row curve CSVs, collection counts from ordered IDs, five anchor/15 nested paid sets, 184 B2 ranking hashes and 184 endpoint hashes. Scientific source pins match the actual R3/B2/B1-P/B1-M-R2 locks. The old original B1-M scorer lock predates its explicit parser repair; the R2 scoring lock and recorded executed scorer SHA are the appropriate authority.

## Claim findings

- **Development:** all five macro nDCG intervals are positive. Procrustes difference is 0.0243251090, family interval [0.0181321752, 0.0307916403]. Point gains are 23/24 versus Procrustes and 24/24 versus every other baseline. All 24 partial DEV ARC2 means are below native Full-X (and Full-Y). Macro Recall comparison remains unresolved.
- **Second correction:** two-minus-one is 0.006924 with [0.003809, 0.009959] after displayed rounding; lambda controls and the complete-procedure ridge comparison match the separate mechanism family. The paper correctly avoids attributing the entire ridge gap solely to tangent targeting.
- **TREC:** 11 positive / 19 unresolved / 0 negative family intervals; five Converter, four ridge and two SimpleLinear positives. Every Procrustes point comparison favors Procrustes, while Procrustes/LA2M family intervals remain unresolved. MiniLM 75% ARC2 and native Full-Y round to 0.5195 / 0.5203. This is descriptive proximity, not equivalence. E5 Converter gains correctly span 0.2000 to 0.2572.
- **All-paid:** MiniLM ARC2 improves from 0.307505 to 0.367146 and beats four all-paid baselines with ridge unresolved; its fixed-anchor version loses to every all-paid baseline. E5 ARC2 changes from 0.311635 to 0.291867 with the within-method interval unresolved, trails Procrustes/LA2M, beats SimpleLinear/ridge and is unresolved versus Converter. Holding summed-objective lambda=10 means effective averaged-loss penalty changes from 10/1024 to 10/28819; the manuscript accurately states that data quantity is not isolated at fixed effective regularization.
- **Mixed gallery:** E5 all-paid nDCG 0.314908 to 0.291867, Recall 0.654164 to 0.559490 and paid top-10 share 0.491640 to 0.064720 match. MiniLM nDCG 0.350951 to 0.367146 matches.
- **Frozen mathematics:** centered affine expansion, target T = -r^2 grad(1 - y N(z)^T), current-map-centered correction prior, regularized intercept, two updates, reused Cholesky, float64 update arithmetic and float32 export match the executed frozen computation. The stated target is tangent; the fitted affine row correction need not be tangent, as the text correctly says.
- **Scale equivariance:** the existing wording ?In exact arithmetic with nonzero predictions? sufficiently qualifies the analytical identity. No required text correction remains. The actual dual/primal loops and normalization helper reject norms <=1e-12 rather than applying a denominator floor; scaling can cross these guards or finite-range limits, and float32 export/application can change rounding. No execution-wide invariance is inferred.
- **Storage and scope:** 385*768 = 295,680 float32 values = 1,182,720 bytes = 1.1279296875 MiB. Converter widths 384/3840/3840/3840/768 imply 33,927,168 parameters and a 114.74285714285715 ratio, correctly rounded to 114.7. This is parameter storage; the paper explicitly excludes end-to-end cost/runtime claims. Native Full-X/Y use their own query/document encoders. All six methods and native rows remain visible in the main comparison panels.
- **Prospective chronology:** ranking seal 2026-10-31 19:56:09.382605 UTC < independent-verification seal 20:11:42.810083 < first final-label opening 20:12:17.410541 < score completion 20:12:54.081736. Hash relationships and all 184 ranking/endpoint records reconcile.

## Claim-level ledger

Each entry below is a claim group; all exact values and raw references are retained in the JSON sibling. Repeated abstract/introduction/discussion claims share one ledger entry. Table-row groups cover every displayed numeric cell in that row.

| ID | Location / claim | Status |
|---|---|---|
| R2-001 | generated/dev_macro.tex ? ARC2-Global row | rounding_ok |
| R2-002 | generated/trec_means.tex ? ARC2-Global row | rounding_ok |
| R2-003 | generated/allpaid.tex ? ARC2-Global row | rounding_ok |
| R2-004 | generated/dev_macro.tex ? Procrustes row | rounding_ok |
| R2-005 | generated/trec_means.tex ? Procrustes row | rounding_ok |
| R2-006 | generated/allpaid.tex ? Procrustes row | rounding_ok |
| R2-007 | generated/dev_macro.tex ? LA2M20 row | rounding_ok |
| R2-008 | generated/trec_means.tex ? LA2M20 row | rounding_ok |
| R2-009 | generated/allpaid.tex ? LA2M20 row | rounding_ok |
| R2-010 | generated/dev_macro.tex ? SimpleLinear row | rounding_ok |
| R2-011 | generated/trec_means.tex ? SimpleLinear row | rounding_ok |
| R2-012 | generated/allpaid.tex ? SimpleLinear row | rounding_ok |
| R2-013 | generated/dev_macro.tex ? Affine ridge row | rounding_ok |
| R2-014 | generated/trec_means.tex ? Affine ridge row | rounding_ok |
| R2-015 | generated/allpaid.tex ? Affine ridge row | rounding_ok |
| R2-016 | generated/dev_macro.tex ? Converter row | rounding_ok |
| R2-017 | generated/trec_means.tex ? Converter row | rounding_ok |
| R2-018 | generated/allpaid.tex ? Converter row | rounding_ok |
| R2-019 | generated/trec_means.tex ? Native Full-X row | rounding_ok |
| R2-020 | generated/allpaid.tex ? Native Full-X row | rounding_ok |
| R2-021 | generated/trec_means.tex ? Native Full-Y row | rounding_ok |
| R2-022 | generated/allpaid.tex ? Native Full-Y row | rounding_ok |
| R2-023 | generated/ablation.tex; Fig.3 ? arc2_global_tangent2_r1 minus procrustes_global | rounding_ok |
| R2-024 | generated/ablation.tex; Fig.3 ? arc2_global_tangent2_r1 minus tangent1_l10 | rounding_ok |
| R2-025 | generated/ablation.tex; Fig.3 ? arc2_global_tangent2_r1 minus ridge_affine_l10_bias_regularized | rounding_ok |
| R2-026 | generated/ablation.tex; Fig.3 ? tangent2_l1 minus arc2_global_tangent2_r1 | rounding_ok |
| R2-027 | generated/ablation.tex; Fig.3 ? tangent2_l100 minus arc2_global_tangent2_r1 | rounding_ok |
| R2-028 | abstract; introduction; results ? Positive development macro comparison against procrustes_global | exact_match |
| R2-029 | abstract; introduction; results ? Positive development macro comparison against la2m20_integration_script_adaptation | exact_match |
| R2-030 | abstract; introduction; results ? Positive development macro comparison against simplelinear_official_final50_mlp5 | exact_match |
| R2-031 | abstract; introduction; results ? Positive development macro comparison against ridge_affine_l10_bias_regularized | exact_match |
| R2-032 | abstract; introduction; results ? Positive development macro comparison against embedding_converter_paper_spec | exact_match |
| R2-033 | abstract; results ? 23/24 Procrustes point gains; 24/24 each other baseline | exact_match |
| R2-034 | results ? Migration macro differences .025733 / .022917 | rounding_ok |
| R2-035 | results ? FiQA/E5 75% exception -.003583 | rounding_ok |
| R2-036 | discussion ? Every partial DEV ARC2 endpoint below native Full-X | exact_match |
| R2-037 | results; generated/trec_family.tex; dagger markers ? 11 positive / 19 unresolved / 0 negative in 30 contrasts | exact_match |
| R2-038 | abstract; results ? E5 Converter gains .2000 to .2572; 25% .257234 [.175731,.337569] | rounding_ok |
| R2-039 | results ? All six Procrustes point means higher; all Procrustes/LA2M family intervals unresolved | exact_match |
| R2-040 | abstract; results; discussion ? MiniLM 75% .5195 versus native Full-Y .5203 | rounding_ok |
| R2-041 | results all-paid subsection ? minilm_distilroberta all-paid ordering / within-method change / cross-regime ordering | exact_match |
| R2-042 | results all-paid subsection ? e5_small_base all-paid ordering / within-method change / cross-regime ordering | exact_match |
| R2-043 | results mixed-gallery paragraph ? minilm_distilroberta proxy-only to mixed-gallery values | rounding_ok |
| R2-044 | results mixed-gallery paragraph ? e5_small_base proxy-only to mixed-gallery values | rounding_ok |
| R2-045 | method Eqs.2-3 ? Centered rectangular Procrustes; raw affine expansion; float64 from float32 parameters | exact_match |
| R2-046 | abstract; method Eqs.4-5 ? Norm-scaled negative cosine-gradient targets | exact_match |
| R2-047 | method Eqs.6-8 ? Ridge prior centered at current Bt; regularized bias; reused Cholesky; exactly two steps; lambda10 | exact_match |
| R2-048 | method scale-equivariance paragraph ? In exact arithmetic with nonzero predictions, T(cB)=cT(B), c>0 | exact_match |
| R2-049 | method; discussion ? 295680 coefficients;1182720 bytes;1.13 MiB;33927168 Converter parameters;114.7x | rounding_ok |
| R2-050 | results all-paid penalty qualification ? Fixed summed-objective lambda10 does not isolate data quantity at fixed effective penalty | exact_match |
| R2-051 | method complexity subsection ? Dual/primal fitting and application big-O costs | exact_match |
| R2-052 | setup retrieval/native paragraph ? Exact float32 inner product; stable row-index ties; top100; ID exclusion; native references use own query/document encoders | exact_match |
| R2-053 | setup inference paragraph ? 20k query draws; average five seeds first; DEV/ablation five each, paid32, TREC30 families | exact_match |
| R2-054 | setup main matrix/exposure ? Four development collections x two pairs x three budgets x six methods x five seeds; 1024 paired anchors; paid set anchor inclusive | exact_match |
| R2-055 | setup baseline paragraph ? Full five-baseline panel with declared adaptations | exact_match |
| R2-056 | intro/mechanism figure/caption ? 24 illustrative docs;8 anchors;4 further encodings;12 native vectors | exact_match |
| R2-057 | setup collection paragraph ? Five collection document/query counts | exact_match |
| R2-058 | setup prospective-label paragraph ? TREC labels closed until all rankings sealed and endpoints separately verified | exact_match |

## Explicit unverified scope

1. No qrel file was opened or rescored. Existing per-query metric arrays are the lowest numerical authority independently recomputed in this audit; ranking-to-qrel metric correctness was checked by reading scorer code, not by re-execution.
2. No training, encoding, retrieval, endpoint replay, parameter refitting, or scientific source/result modification was performed. All 184 B2 ranking/endpoint file hashes were checked; their existing endpoint verifier records were inspected, not rerun.
3. All 388 summary mean rows were checked (160 DEV, 40 TREC, 28 all-paid, 160 mechanism); these reuse some historical cells and must not be described as 1,780 independent experiments. Four separate locked contrast families (5+5+30+32) were reconstructed from existing scores.
4. Only the two five-seed FiQA all-paid ARC2 gallery examples used by the manuscript were independently checked against before/after per-query arrays; the entire 450-case diagnostic matrix was not independently reconstructed.
5. Local baseline wrappers, frozen configurations, B2 neural fit receipts and pinned source hashes were checked. The remote official SimpleLinear upstream source and every historical DEV neural fit receipt were not independently reread or regenerated. This is not external-method reproduction certification.
6. Bibliographic accuracy, related-work characterizations, novelty, venue compliance, and external-paper theoretical statements were not independently checked against external primary sources. No prior paper/review opinions were used as evidence.
7. Figures: all four supplied PNGs and mechanism TikZ source were visually inspected; the full reviewed PDF text was extracted, and PDF pages 6,10,12,13 were rendered and inspected. Figure values were traced to raw means, plotted CSVs and plotting code. No pixel-by-pixel binary equivalence or complete page-by-page layout audit is claimed.
8. Scale equivariance is an ideal exact-arithmetic identity, as explicitly stated in the manuscript. Runtime norm guards (<=1e-12 rejected), finite-range checks and float32 rounding prevent an unconditional execution-wide or bitwise invariance claim. No scaled execution was performed.
9. Prospective-label closure is supported by committed protocol, source policy and ordered/hash-bound run receipts. This is a local artifact audit, not proof about every possible unrecorded action outside the campaign.
10. PASS applies to the frozen input snapshot identified by hashes. Same-family review remains provisional and is not submission-ready acceptance or authorization for another experiment.

## Reproduction and hashes

Run `python paper/review/final_review_20261101/raw_audit_r2_check.py` from the workspace root to repeat the saved-score checks. The script writes `raw_audit_r2_computed.json`; `RAW_AUDIT_R2.json` is the canonical signed-scope result of this review. Input hashes use paper-relative keys for manuscript files and absolute paths for external results/configs/code. The four page-render PNGs are visual audit outputs, not empirical evidence.

Reviewed PDF SHA256: `sha256:de820e58315443262fda1bea48fea73206e5d8fc04c15b808c7c1bb3be4465ed`.
Main LaTeX SHA256: `sha256:f8278687f7db8ce72b6142713f3c10d56b89ae29cb8032386baa84dae151b98f`.

No required correction was found within the checked scope. This audit does not certify unverified claims or a later manuscript revision.
