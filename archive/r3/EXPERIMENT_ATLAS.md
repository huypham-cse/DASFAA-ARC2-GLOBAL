# Complete experiment atlas â€” ARC2-Global

Revision **r2-completeness**, 1 November 2026. This is a saved-evidence review packet before paper writing. The original r1 ZIP remains unchanged; no numerical method, ranking, label exposure, threshold or scientific protocol changed.

## 1. Exact experiment coverage

**1,340 unique planned logical quality cells =736 main DEV +360 additional ablation cells +60 additional all-paid cells +184 independent cells.** There are 1,320 partial cells and 20 native references. Five seeds, budgets, shared queries and reused historical rankings do not create 1,340 independent statistical observations.

| Block | Completed measurement | Increment to disjoint quality union | Status / location |
|---|---|---:|---|
| B0 historical import |64 inspected FiQA rankings, all original byte versions retained |0, subset of main identities |[Imported evidence](results/fiqa_development/summary.json); source import/extraction manifests in provenance/ |
| B1a input / encoder readiness |60 nested paid sets,4 encoder repeat tests,2 toy galleries,4 dimension parity cases |0 |[Readiness report](results/b1a_r1_20261025/SUMMARY.md) |
| B1b external-adapter correctness |25 LA2M oracle fixtures,15 ridge cases,5 official-code SimpleLinear comparisons |0 |[Baseline validation](results/b1b_20261026/SUMMARY.md) |
| B1c main DEV |736 rankings:720 partial +16 native; six methods, four collections, two pairs, three budgets, five seeds |736 |[All six-method results](results/b1c_r3_review_20261031/SUMMARY.md) |
| B1-M mechanism/sensitivity |736 rankings, including360 extra one-step/lambda1/lambda100 identities |360 |[Mechanism report](results/b1mp0_r1_review_20261026/SUMMARY.md) |
| B1-P0 backend parity |31 synthetic fixtures/62 updates;40 real fit identities/120 budget checks; zero ordered top100 drift |0 |[P0 included with M](results/b1mp0_r1_review_20261026/SUMMARY.md) |
| B1-P paid-pair supervision |124 rankings:60 fixed +60 allpaid +4 native; same FiQA 50% destination budget |60 |[All-paid report](results/b1p_r5_review_20261027/SUMMARY.md) |
| B1-G mixed-gallery diagnostics |450paired replacement cases,210 pure galleries,90 five-seed conditions; no new fits |0; diagnostic counterfactuals counted separately |[All diagnostics](results/b1g_r1_review_20261027/SUMMARY.md) |
| B2 prospective TREC-COVID |184 rankings,60fits, separate prelabel endpoint replay and one-shot scoring |184 |[Independent report](results/b2_review_20261101/SUMMARY.md) |
| B3 / B4 physical100K and traffic replay |Not run; conditional systems route |0 |No cost/SLO/real-traffic claim |

The five source indices I/M/P/C/B have1,844 rows, with504 repeated logical identities. An equivalent chronological union is64+692+80+320+184=1,340. Main-first disjoint counting above is easier to read. Native references are deduplicated across seeds/methods. B1c and M both contain736 rows but compare different method panels; adding the two totals directly would double-count376identities. P overlaps main in64identities.

Collections: NanoNQ5,035 documents/50 queries; NanoHotpotQA5,090/50; NanoFEVER4,996/50; FiQA57,638/500 inspected DEV; TREC-COVID171,332/50 prospective. Sum of corpus entries across collections:244,091, not a claim of globally distinct text documents. MS MARCO100K, ORCAS and AOL replay are unrun conditional work. Both real encoder pairs are384â†’768 (MiniLMâ†’DistilRoBERTa and E5-smallâ†’E5-base).

## 2. Mechanism and sensitivity â€” all five saved macro comparisons

| Left minus right | nDCG delta [saved99% interval; five-comparison family] |
|---|---:|
| arc2_global_tangent2_r1 minus procrustes_global | +0.024325 [+0.018015, +0.031021] |
| arc2_global_tangent2_r1 minus tangent1_l10 | +0.006924 [+0.003809, +0.009959] |
| arc2_global_tangent2_r1 minus ridge_affine_l10_bias_regularized | +0.095653 [+0.075353, +0.116631] |
| tangent2_l1 minus arc2_global_tangent2_r1 | +0.003197 [-0.001890, +0.008304] |
| tangent2_l100 minus arc2_global_tangent2_r1 | -0.009255 [-0.013214, -0.005510] |

The second update contributes about 0.006924 aggregate nDCG beyond one step. Lambda1 is unresolved versus the locked lambda10; lambda100 is worse. The method remains lambda10/two steps, with no post-score parameter selection or independent one-step necessity claim.

![All mechanism controls](results/control_figures/b1m_mechanism_controls.png)

P0 is correctness evidence: stored coefficient difference up to 7.27595761418e-12 and normalized proxy difference 3.72529029846e-09 were recorded; zero ordered top100 changes across 120 real budget checks. This is tolerance-validated numerical parity, not byte-identical coefficients, new quality evidence or physical cost.

## 3. All-paid fitting â€” complete matched external comparisons

FiQA 50% gives 28,819 paid destination pairs to every compared all-paid mapper; fitting only 1,024 of them is a different supervision regime, not the same experiment. The top panels below compare all-paid ARC2 against all-paid baselines. The bottom panels retain fixed ARC2 versus all-paid competitors. All32 original contrasts remain in the detailed report;20are drawn in the figure.

| Pair | All-paid ARC2 minus all-paid baseline | nDCG delta [saved32-comparison family interval] |
|---|---|---:|
| minilm_distilroberta | procrustes_global | +0.033760 [+0.018645, +0.050408] |
| minilm_distilroberta | la2m20_integration_script_adaptation | +0.028223 [+0.010129, +0.047297] |
| minilm_distilroberta | simplelinear_official_final50_mlp5 | +0.034830 [+0.023544, +0.047191] |
| minilm_distilroberta | ridge_affine_l10_bias_regularized | -0.000117 [-0.007540, +0.006532] |
| minilm_distilroberta | embedding_converter_paper_spec | +0.041385 [+0.023614, +0.060969] |
| e5_small_base | procrustes_global | -0.044335 [-0.079696, -0.009272] |
| e5_small_base | la2m20_integration_script_adaptation | -0.037474 [-0.070583, -0.003758] |
| e5_small_base | simplelinear_official_final50_mlp5 | +0.123918 [+0.093821, +0.156724] |
| e5_small_base | ridge_affine_l10_bias_regularized | +0.064852 [+0.043521, +0.089349] |
| e5_small_base | embedding_converter_paper_spec | +0.029348 [-0.015573, +0.074762] |

**MiniLM all-paid ARC2 has four positive family comparisons; ridge is unresolved.** E5 loses to Procrustes/LA2M, beats the declared SimpleLinear/ridge configurations, and is unresolved versus Converter. Fixed1024MiniLM ARC2 is below all five all-paid comparators. Thus the positive result and the supervision limit are both visible.

![All-paid and fixed-fit comparisons](results/control_figures/b1p_allpaid_controls.png)

## 4. Mixed-gallery diagnostics â€” actual replacement can reverse ordering

The original 450 cases reuse 210 fitted galleries. R2 includes unchanged raw top100 outputs for 210 proxy-only galleries and 450 mixed endpoints in a short content-addressed layout, along with all saved metric arrays and90seed-averaged conditions. The verification independently rescores those rankings; it does not rerun full vector search, fit models or regenerate sampled score-error distributions.

![All six methods, both pairs, FiQA 50 all-paid diagnostic](results/control_figures/b1g_proxy_mixed_controls.png)

For all-paid FiQA/E5 at50%, ARC2 proxy-only nDCG0.314908 becomes0.291867; Procrustes0.286096 becomes0.336202; ridge0.270585 becomes0.227015. A better proxy-only ranking can therefore become a worse mixed endpoint. This is descriptive evidence, not proof of a unique calibration cause or a repair. The figure displays all six methods for both pairs in that fixed view; the CSV retains all 90 conditions.

## 5. Full quality includes Recall and native references

| DEV macro ARC2 minus baseline | nDCG mean delta | Recall mean delta [nominal descriptive95%] |
|---|---:|---:|
| procrustes_global | +0.024325 | -0.000239 [-0.004944, +0.004336] |
| la2m20_integration_script_adaptation | +0.104055 | +0.090028 [+0.075394, +0.105760] |
| simplelinear_official_final50_mlp5 | +0.172100 | +0.252882 [+0.236538, +0.269462] |
| ridge_affine_l10_bias_regularized | +0.095653 | +0.121734 [+0.103216, +0.141376] |
| embedding_converter_paper_spec | +0.161162 | +0.101758 [+0.087364, +0.116912] |

All five DEV nDCG macro family comparisons favor ARC2. Overall DEV Recall versus Procrustes is unresolved; E5 Recall losses and the FiQA/E5/75%nDCG negative mean remain reported. In B2, nDCG family decisions are11 positive/19 unresolved/0 negative. Recall versus Procrustes has2positive,3 negative and1unresolved nominal intervals; all three E5 Recall intervals are negative. These nominal Recall decisions are not interchangeable with the30-comparison nDCG family.

Native Full-X exceeds Full-Y on both NanoHotpotQA pairs, both NanoFEVER pairs and TREC/E5. A required migration may still be the operational scenario, but the destination model is not assumed to improve relevance. All native references remain visible; cutover is not automatically warranted.

## 6. What the first release missed, and what is repaired

- **Presentation:** it foregrounded736 main DEV +184 independent rows and hid the360 extra ablation and60all-paid identities in subsidiary reports. Quantitative M/P/G results now have dedicated sections and three new figures.
- **Historical bytes:** ten original Converter25%FiQA rankings were absent, although their logical conditions had current R3 versions. All64 original imported ranking hashes and all38displaced historical byte versions are now preserved. Historical versions are not counted as new logical conditions.
- **Validation/history:** raw B1a/B1b validation, all available compact failed/smoke bundles, import/source seals and supporting QA are added. Old STOP strings inside immutable reports describe their original dates; this atlas is the current coverage guide.
- **G reproducibility:** r1 only provided scored arrays/tables. R2 adds all660 saved raw G ranking records with their hashes and group binding contexts, enabling independent relevance rescoring. Large vectors, model checkpoints, sampled score arrays and new vector-search regeneration remain outside the lightweight scope.

No data was newly tuned or selected, no negative result removed, no final collection reopened over the network, and no manuscript changed. Earlier interrupted runs remain interrupted. Original r1 ZIP is preserved for comparison.

## 7. Verification and review status

Run `python reproduce/verify_review_release.py --root . --mode full` for hashes plus main736 DEV/184B2rankings and their locked bootstrap. Run `python reproduce/verify_control_families.py --root .` for all736M/124Prankings, their declared means/intervals, and all210 pure/450mixed G raw rankings and saved metric arrays. Run `python reproduce/verify_experiment_inventory.py --root .` for the 1,340 logical union and historical coverage.

Saved-control render: `python reproduce/render_release_controls.py --root .` writes fresh figures under checks/. Original source/results remain frozen. See checks/ for final receipts and provenance/completeness_audit/ for the audited source inventory.

The earlier completed B2 semantic verdict remains partial/same-family/provisional. A new zero-context release-claim reviewer completed numerical checks but hit the account usage limit before a final semantic verdict. That fresh review is recorded as REVIEW_UNAVAILABLE, not PASS. This packet is for supervisor fact-checking, not a submission-ready claim-audit certificate. No further scientific experiment is launched.

Audit boundary: the current ARC2-Global paper repository and its exact imported source protocols/results. The64imported FiQA rows include the eligible earlier global-method evidence. Older mixed ARC2/P5/P8 exploration is neither erased nor automatically relabeled as the frozen method; historical source/model/anchor compatibility is required for reuse. No claim is made that every older external project/server cache was recovered.
