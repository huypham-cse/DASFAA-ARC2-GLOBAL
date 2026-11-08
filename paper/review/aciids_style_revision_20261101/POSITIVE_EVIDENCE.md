# Positive evidence for the ACIIDS revision

The draft already includes the strongest prespecified conclusions. Its clearest omitted positive result is a concrete E5 operating-point pattern: ARC2 at 25% coverage exceeds the evaluated Converter and ridge at 75% on all five completed collections. The strongest underused inferential result is the positive all-paid MiniLM within-method gain at an unchanged paid-document set. Prospective MiniLM Recall supplies useful secondary evidence.

This audit read existing scored outputs, saved per-query arrays and actual fit metadata/configurations. REPORT and the release atlas were used for discovery only. No experiment, fit, retrieval, qrel opening, tuning, manuscript/scientific edit, or delegation occurred.

## Verification

All C/B/M/P means were independently recomputed from saved per-query arrays; G before/after and delta arrays were checked. No new confidence interval or inferential family was generated.

- {"study": "C", "rows": 160, "scalar_means": 320, "max_abs_error": 9.43689570931383e-16, "status": "PASS"}
- {"study": "B", "rows": 40, "scalar_means": 80, "max_abs_error": 5.551115123125783e-16, "status": "PASS"}
- {"study": "M", "rows": 160, "scalar_means": 320, "max_abs_error": 1.1102230246251565e-15, "status": "PASS"}
- {"study": "P", "rows": 28, "scalar_means": 56, "max_abs_error": 9.992007221626409e-16, "status": "PASS"}
- {"study": "G", "rows": 90, "scalar_means": 360, "max_abs_error": 0.0, "status": "PASS"}
- {"study": "C/B/M contrasts from saved means", "scalar_contrasts": 80, "max_abs_error": 2.2898349882893854e-16, "status": "PASS", "intervals": "Original intervals retained; no new confidence intervals generated."}

The JSON retains exact source pointers, complete panels and SHA-256 hashes of 99 inspected inputs.

## Complete-context E5 operating points

All methods fit the same 1,024 paired anchors. This intentionally compares 25% ARC2/Procrustes/LA2M with 75% SimpleLinear/ridge/Converter. Native references use their own query/document encoders and full corpus. These are measured, discrete points, not a minimum-encoding test.

| Collection / role | ARC2 25% | Proc. 25% | LA2M 25% | SimpleLinear 75% | Ridge 75% | Converter 75% | Full-X | Full-Y |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NanoNQ / DEV | 0.507123685 | 0.485237046 | 0.364036411 | 0.483877572 | 0.442840999 | 0.402087212 | 0.659510453 | 0.666907899 |
| NanoHotpotQA / DEV | 0.584485656 | 0.551234618 | 0.386898496 | 0.617388084 | 0.505347008 | 0.501633237 | 0.827753243 | 0.819254019 |
| NanoFEVER / DEV | 0.755451273 | 0.714661666 | 0.499050622 | 0.708746011 | 0.728986014 | 0.732576238 | 0.898352761 | 0.896329057 |
| FiQA / DEV | 0.273106842 | 0.271778039 | 0.141573953 | 0.278139782 | 0.160971491 | 0.209533675 | 0.346478290 | 0.389132525 |
| TREC-COVID / prospective | 0.562801573 | 0.566042002 | 0.520590436 | 0.578493722 | 0.327784833 | 0.409827782 | 0.680541649 | 0.642113450 |

`e5_complete_context_table` provides all exact values, role labels, column budgets and stable raw JSON pointers. Each `complete_panel` contains all six adapters at all three budgets plus natives, with nDCG and Recall. Full-X and Full-Y exceed ARC2/25% in every row; prospective Procrustes/25% is also higher. Do not turn this comparison into an inferred threshold or physical encoding-cost saving.

## Ranked candidates

### 1. Strongest overlooked operating-point pattern

**Status:** Descriptive cross-budget comparison; not a predeclared test.

**Current coverage:** Raw endpoints appear in figures/tables; the five-collection 25%-versus-75% pattern is absent.

> Across all five evaluated E5 collections, ARC2 at 25% destination coverage has higher nDCG@10 point means than the evaluated Converter and affine ridge at 75%; on prospective TREC-COVID, the corresponding values are 0.5628, 0.4098 and 0.3278.


Interpretation:
- Use discrete measured points; no tested minimum coverage or interpolated savings.
- All six methods fit 1,024 shared pairs. Full-X/Y exceed ARC2/25% in all five collections.
- Prospective Procrustes/25% exceeds ARC2/25%; Procrustes/LA2M also exceed ARC2 at 75%.

### 2. Strengthen same-paid-set supervision result

**Status:** Original 32-comparison family on inspected development data.

**Current coverage:** Endpoints and four baseline wins present; positive within-ARC2 family interval omitted.

> Using all already-paid MiniLM pairs raises FiQA nDCG@10 from 0.3075 to 0.3671 at the same 50% document coverage, a gain of 0.0596 with family-adjusted interval [0.0393, 0.0806].

Exact saved within-method gain **+0.05964116316462802**, original 32-comparison family interval **[0.03934110686868015,0.08060437708604837]**. MiniLM native Full-X=0.3899614643349381 and Full-Y=0.40473597079469226 exceed all-paid ARC2=0.36714602143626507.

| All-paid method | MiniLM nDCG | E5 nDCG |
|---|---:|---:|
| ARC2 | 0.367146021 | 0.291866982 |
| Procrustes | 0.333386474 | 0.336202461 |
| LA2M20 | 0.338923467 | 0.329341301 |
| SimpleLinear | 0.332316247 | 0.167949407 |
| Affine ridge | 0.367263277 | 0.227014575 |
| Converter | 0.325761439 | 0.262519464 |

All-paid MiniLM ARC2/50%=0.367146021 is also higher than fixed-anchor ARC2/75%=0.350072230 descriptively; fitting exposure differs, so this is not a matched-supervision cost claim. Full locked contrasts and exact pointers are in JSON.

Interpretation:
- All-paid fitting uses 28,819 pairs, fixed uses 1,024. Summed-objective lambda=10 stays fixed, so effective regularization changes.
- MiniLM all-paid ridge is marginally higher, 0.367263277; its comparison is unresolved.
- E5 all-paid ARC2 loses to Procrustes and LA2M. This is encoder dependent.

### 3. Best development macro on every collection

**Status:** Posthoc descriptive equal-condition aggregation.

**Current coverage:** Overall/pair macros and 23/24 count present; collection macros absent.

> ARC2 leads the six-method development panel on each collection macro, improving over Procrustes by 0.0269 on NanoNQ, 0.0316 on NanoHotpotQA, 0.0290 on NanoFEVER and 0.0099 on FiQA.

| Collection | ARC2 macro | Procrustes macro | Difference | Full-X macro | Full-Y macro |
|---|---:|---:|---:|---:|---:|
| NanoNQ | 0.543972498 | 0.517108925 | +0.026863573 | 0.626296159 | 0.672679943 |
| NanoHotpotQA | 0.552674935 | 0.521103205 | +0.031571729 | 0.714158117 | 0.702594303 |
| NanoFEVER | 0.702158691 | 0.673205720 | +0.028952971 | 0.862089400 | 0.822747637 |
| FiQA | 0.311103985 | 0.301191823 | +0.009912162 | 0.368219877 | 0.396934248 |

Interpretation:
- Equal weights over two migrations and three budgets; these are not four newly significant tests.
- All 24 partial DEV five-seed nDCG means remain below native Full-X and Full-Y.

### 4. Robustness of second correction

**Status:** Original five-contrast mechanism family plus descriptive robustness.

**Current coverage:** Macro gain/interval present; 22/24 signs and all-five-seed macro gains omitted.

> The second correction improves 22 of 24 development condition means and adds 0.0069 macro nDCG@10 beyond one step, while both corrections remain absorbed into the same affine inference map.

Exact macro gain **0.006923862939737235**, original family interval **[0.003809388309482942,0.009959126205904258]**. Source: M `/overall_macro/1`; the complete 24 condition contrasts are attached in JSON.

Interpretation:
- Two condition means are negative.
- Saved seed-level overall gains range from 0.003827292 to 0.009036946; seeds are not independent collection replications.
- No prospective one-step ablation. The ridge contrast jointly changes initialization/prior and tangent-target procedure.

### 5. Useful missing secondary prospective Recall result

**Status:** Secondary descriptive Recall; original nominal 95% intervals, not primary-family tests.

**Current coverage:** Prospective Recall values absent from main tables.

> On prospective MiniLM, ARC2 has the highest Recall@100 point mean among all six adapters at every budget: 0.0896, 0.0953 and 0.0998 at 25%, 50% and 75% coverage.


**minilm_distilroberta Recall@100**

| Method | 25% | 50% | 75% |
|---|---:|---:|---:|
| ARC2 | 0.089630885 | 0.095291590 | 0.099836041 |
| Procrustes | 0.086568496 | 0.093485409 | 0.099428764 |
| LA2M20 | 0.073567771 | 0.088422840 | 0.098269540 |
| SimpleLinear | 0.062574705 | 0.084477670 | 0.097016277 |
| Affine ridge | 0.068901341 | 0.077994497 | 0.085637754 |
| Converter | 0.065120507 | 0.077173106 | 0.089200923 |

Native references: Native Full-X=0.093553414, Native Full-Y=0.105213780.

**e5_small_base Recall@100**

| Method | 25% | 50% | 75% |
|---|---:|---:|---:|
| ARC2 | 0.086579816 | 0.092842273 | 0.099666929 |
| Procrustes | 0.088571030 | 0.097575263 | 0.106056381 |
| LA2M20 | 0.059325560 | 0.082341341 | 0.101591631 |
| SimpleLinear | 0.029643592 | 0.050973737 | 0.069282581 |
| Affine ridge | 0.037264260 | 0.038217266 | 0.036570156 |
| Converter | 0.042248049 | 0.049511793 | 0.058240371 |

Native references: Native Full-X=0.123530381, Native Full-Y=0.116243955.

Original ARC2-minus-Procrustes Recall intervals, nominal 95% and descriptive:
- minilm_distilroberta / 25pct: delta +0.003062388410, CI [0.0017318861225867031, 0.004548530715636133]; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json#/contrasts/0`.
- minilm_distilroberta / 50pct: delta +0.001806180351, CI [0.0006734858739983598, 0.0029928393535734415]; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json#/contrasts/5`.
- minilm_distilroberta / 75pct: delta +0.000407276299, CI [-0.00046319614730042097, 0.0012998664306243608]; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json#/contrasts/10`.
- e5_small_base / 25pct: delta -0.001991214482, CI [-0.003291983341906236, -0.0006798521068942913]; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json#/contrasts/15`.
- e5_small_base / 50pct: delta -0.004732990378, CI [-0.006442459861821125, -0.003115103617580042]; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json#/contrasts/20`.
- e5_small_base / 75pct: delta -0.006389451457, CI [-0.008763717298704368, -0.0043236039811896925]; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json#/contrasts/25`.

Interpretation:
- Nominal ARC2-minus-Procrustes intervals positive at 25/50%, unresolved at 75%; no 30-family Recall significance is established.
- Native Full-Y Recall exceeds all ARC2 points. Full-X is exceeded by ARC2 at 50/75% as point estimates.
- E5 Recall loses to Procrustes at all three budgets with negative nominal intervals; LA2M is also higher at 75%.

### 6. Clarify source-versus-destination operating point

**Status:** Posthoc descriptive native-reference comparison.

**Current coverage:** 75% versus destination Full-Y present; 50% versus source Full-X absent.

> For prospective MiniLM migration, ARC2 reaches 0.5000 nDCG@10 at 50% coverage, above native source 0.4935; at 75% it reaches 0.5195 against destination-native 0.5203.


Interpretation:
- Native references use their own query encoders; source queries remain a viable option when permitted.
- Procrustes, LA2M and SimpleLinear have higher 50% nDCG point means than ARC2. No native equivalence or noninferiority test.
- Prospective E5 source Full-X exceeds destination Full-Y. Destination encoders are not automatically relevance upgrades.

### 7. Retain compact-quality anchor

**Status:** Algebraic final storage, corroborated by actual configuration and fit metadata.

**Current coverage:** Already used well in abstract/discussion.

> Two directional corrections compile to one 295,680-coefficient affine map: 1.13 MiB in float32, or 114.7 times fewer parameter bytes than the evaluated Converter.

Exact final coefficient count=295,680; float32 bytes=1,182,720; MiB=1.1279296875. Actual Converter refit metadata records 33,927,168 parameters. Ratio=114.74285714285715. JSON includes the actual configurations and fit receipts.

Interpretation:
- Only final coefficients counted; fitting object/workspace excluded.
- Ridge has the same coefficient count and Procrustes is similarly compact. Mixed gallery still stores full 768-dimensional vectors.
- No end-to-end cost, speedup, dollar, index-memory or serving-SLO claim.

### 8. Optional observational algebraic-fit timing

**Status:** Posthoc shared-load timing; optional supplement only.

**Current coverage:** No explicit durations present; no-neural-training structural result already stated.

> Across ten prospective 1,024-pair fits, recorded ARC2 CPU fitting time ranges from 0.118 to 0.307 seconds; these observations describe the algebraic fitting step.

Observed median CPU fitting time=0.2796211624518037 seconds over ten B2 receipts. No controlled speedup is claimed.

Interpretation:
- Not a controlled CPU/GPU comparison; hardware, runtime and load differ.
- Encoding, mapping, gallery materialization, indexing, query encoding and serving are separate.
- B3/B4 systems studies are unrun.

### 9. Positive MiniLM counterpart to mixed-gallery reversal

**Status:** Paired descriptive diagnostic on saved fitted galleries.

**Current coverage:** MiniLM ARC2 before/after present; comparator behavior omitted.

> On all-paid MiniLM/FiQA, true-vector replacement raises ARC2 nDCG@10 from 0.3510 to 0.3671, whereas Procrustes falls from 0.3496 to 0.3334 and LA2M from 0.3506 to 0.3389.

| Pair | Method | Pure proxy nDCG | Mixed nDCG | Difference |
|---|---|---:|---:|---:|
| e5_small_base | ARC2 | 0.314907750 | 0.291866982 | -0.023040768 |
| e5_small_base | Converter | 0.158650613 | 0.262519464 | +0.103868851 |
| e5_small_base | LA2M20 | 0.298918117 | 0.329341301 | +0.030423184 |
| e5_small_base | Procrustes | 0.286096005 | 0.336202461 | +0.050106456 |
| e5_small_base | Affine ridge | 0.270585008 | 0.227014575 | -0.043570432 |
| e5_small_base | SimpleLinear | 0.115978346 | 0.167949407 | +0.051971061 |
| minilm_distilroberta | ARC2 | 0.350950735 | 0.367146021 | +0.016195286 |
| minilm_distilroberta | Converter | 0.282716029 | 0.325761439 | +0.043045410 |
| minilm_distilroberta | LA2M20 | 0.350643033 | 0.338923467 | -0.011719566 |
| minilm_distilroberta | Procrustes | 0.349558866 | 0.333386474 | -0.016172391 |
| minilm_distilroberta | Affine ridge | 0.342222503 | 0.367263277 | +0.025040774 |
| minilm_distilroberta | SimpleLinear | 0.307119732 | 0.332316247 | +0.025196515 |

Interpretation:
- Retain opposite E5 ARC2 behavior. No unique causal score-bias mechanism or calibration fix proved.
- Proxy-only still requires target fitting pairs; not zero-encoding deployment.
- G reuses older frozen fits; do not mix fresh R3 Converter endpoints.

### 10. Finite engineering validation

**Status:** Finite numerical parity checks only.

**Current coverage:** Not quantified in main paper.

> The primal implementation retains numerical agreement with the frozen reference, with no ordered top-100 changes in 120 real budget checks.

Exact finite parity summary: `{"synthetic_fixtures": 31, "real_budget_checks": 120, "real_fit_identities": 40, "max_coefficient_difference": 7.275957614183426e-12, "max_proxy_difference": 3.725290298461914e-09, "ordered_top100_queries_with_difference": 0}`.

Interpretation:
- Tolerance agreement is not byte-identical coefficients.
- Finite checks are not universal proof or additional relevance evidence.

## Historical positive figures and excluded evidence

Old positive collections were inspected for exact algorithm identity. They are not silently omitted current-Global wins.

- **NanoBEIR E4/E4a:** old runner imports `core.fit_arc2` and `core.transform_old_docs`; the core transform adds k=8 local anchor residuals with the original argpartition weight floor. Current Global explicitly disables local residual. NanoDBPedia/NanoFEVER/NanoHotpotQA plots therefore cannot be imported as current Global results.
- **BRIGHT Economics E6e:** bootstrap delegates to unchanged E6 science, which calls the same local-residual core. The old comparator is LA2M4 rather than current LA2M20. Recorded E6e core hash matches inspected source: True.
- **BRIGHT Physics P7 / P5 / P6:** the immutable P7 protocol explicitly names `arc2_residual_cv_r1` in `mixindex_arc2.current`; it is a different method. Its positive MiniLM outcomes cannot be renamed Global.
- **P8-R10 FiQA `procrustes_tangent2_global`:** exact historical selected global path is eligible and already imported. The 64 preserved ranking byte versions/compatible logical rows are not an independent new study. Other P8 local/residual variants and historical Q14/Q15/R8/M0/M2 outcomes remain separate.

Exact raw paths, source lines and exclusion reasons are in `excluded_evidence_ledger`; inspected historical files are hashed in the input manifest.

## Coverage and real gaps

**1,340 logical quality identities =736 main DEV +360 extra mechanism/sensitivity +60 extra all-paid +184 prospective.** These are not independent statistical observations. B1-G separately contains 450 mixed cases and 210 pure galleries, aggregated into 90 five-seed conditions. B1a/B1b input/baseline validations and B1-P0 parity checks do not add quality results. Historical imports, fixed/native overlaps, 38 displaced records and failed/interrupted attempts remain preserved. B3/B4 physical and traffic studies are unrun.

- No independent superiority over closest Procrustes/LA2M.
- No prospective zero/one/two-step controls.
- No prior-matched control isolates tangent target from initialization/prior.
- No all-paid breadth beyond FiQA.
- No native-reference equivalence/noninferiority test.
- No tested minimum coverage/retention threshold or interpolated saving.
- No physical-100K, traffic replay or serving-SLO measurements.

## Cost and native-reference accounting

- Count unique destination document exposure as |A union S|, anchors included; fitting-pair count differs from paid coverage.
- Fixed fitting uses 1,024 anchors; paid nonanchors supply replacement only. All-paid FiQA/50% fits the same 28,819 paid pairs.
- Coverage is floor(rho*N); TREC 25/50/75% means 42,833/85,666/128,499 unique destination documents.
- Cached fit/rank phases perform zero new physical document encodes. B2 full frozen-vector acquisition is a separate stage; exposure is not total pipeline encoding cost.
- Proxy-only diagnostics still require target fitting pairs.
- Destination query encoding, fitting workspace and full 768-dimensional index storage are outside coefficient-byte/document-exposure metrics.
- Native Full-X uses source queries and may remain viable if allowed; required destination queries change the operating constraint.

## Recommended editing decision

Add the E5 discrete cross-budget operating point, original MiniLM within-ARC2 all-paid interval, and secondary prospective MiniLM Recall context if space permits. Collection breadth is an optional short strengthening sentence. Keep directional quality with compact affine inference central; avoid a study inventory.

Preserve native and strongest-baseline context alongside attractive operating points. Use one compact sentence per selected finding rather than a separate experiment subsection for each block.

## Principal raw sources

- **C**: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- **B**: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- **M**: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- **P**: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- **G**: `results/b1g_r1_review_20261027/scoring/results_summary.json`
