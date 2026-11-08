# Current ARC2-Global claim assessment

31 October 2026. Completed B1c-R3 plus M/P/G. The bounded fixed-anchor quality claim is **supported**; the overall research package is **partial**, with independent confirmation and operational claims separate. Same-family ARIS review, provisional.

[Current numerical report](REPORT.md) | [Six-method results and figures](results/b1c_r3_review_20261031/SUMMARY.md) | [Structured verdict](.aris/traces/result-to-claim/2026-10-31_b1c_r3/verdict.json). Historical27October review remains in its original trace directory.

# Final completed B1-M/P/G/B1c-R3 result-to-claim judgment

Overall `claim_supported: partial`. The bounded fixed-anchor DEV quality claim is supported; a practical/general migration or cost claim is not. D1 is a **narrow GO-C1 recommendation for the existing prospective B2 quality question**, with the current STOP retained. This review authorizes no execution. Same-family reviewer `/root/b1c_r3_final_claim_review`, configured `gpt-6.1-sol/high` under the explicit user override; `review_independence: same-family`, `acceptance_status: provisional`, pending external review. Confidence is high for the bounded DEV description and its limits, medium for transfer to unseen data. This is not a formal paper-claim audit or an acceptance-probability estimate.

## Evidence authority and computational verification

I read `AGENTS.md`, `configs/method.json`, `configs/baselines.json`, the D1/B2 and external-adapter rules in `refine-logs/EXPERIMENT_PLAN.md`, the completed raw summaries below, B1c cell index and per-query arrays, and the completed computational QA. Stale RUNNING prose in root documents is superseded by the completed receipts, not by this interpretation. Historical failures and selection exposure remain part of the record.

`results/b1c_r3_review_20261031/evidence/run/scoring/summary.json` (S below) records `status=DEV_SCORED`, `ranking_cells=736`, `imported_cells=378`, `new_cells=358`, `historical_displaced_cells_preserved=38`, `new_fit_groups=118`, `reused_fit_groups=2`, and completion `2026-10-31T05:45:14.913610+00:00` (12:45 +07). Ranking seal is `a60b352dd1bb19b4f35783ce5c5172aea6ab3bbc9d4691c740320883dd2bae88`; lock is `f567a4b6267baef3c59de1aca750d19ba3479d228109f7d098fd45d26586830d`; scorer commit is `61f73171b1869a186648aadd88f1b6f81a61376b`. `provenance/qa/b1c_r3_status_20261031T055703Z.json` records schedule status `B1C_R3_SCORED_STOP_FOR_D1`, all 358 rankings complete, no owned processes, and no TREC access.

`evidence_precheck.json` verifies 7/7 cited values; that check proves existence only. I read `results/b1c_r3_review_20261031/qa_completed_20261031T060049161714Z.json`: `status=PASS`, 736 independently rescored rankings, 239,200 per-query metric values compared, maximum metric discrepancy `3.3306690738754696e-16`; 160 means, 120 condition contrasts, 5 aggregates, 570 nominal intervals and 5 family intervals verified, maximum summary discrepancy `4.440892098500626e-16`. This QA independently parses qrels and recomputes metrics; summary reconstruction uses the locked source summarizer. My inspection of all four float64 per-query arrays found the stated shapes, finite values in [0,1], and nDCG mean residuals at most `2.22e-16`.

That is strong computational evidence for reported ranking metrics, not independent checkpoint or exact-search regeneration. QA distinguishes 1,633 omitted sealed artifacts and 238 source inputs unavailable in the compact bundle; remote full-source verification remains an attestation for those objects. It explicitly excludes regeneration from embeddings/checkpoints, fit correctness and tie/search implementation revalidation. No `EXPERIMENT_AUDIT.json` was found: `integrity_status=unavailable`, provisional with no full integrity audit. A computational PASS does not change the same-family semantic status.

## 1. Bounded fixed-anchor quality: yes

Supported wording:

> On four inspected development datasets, two declared encoder pairs, five mapping seeds and 25/50/75% unique-destination encoding budgets, the frozen centered-Procrustes mapper with exactly two lambda=10 tangent updates improved equal-24-stratum macro nDCG@10 over each of five declared external configurations in the fixed-1,024-pair fitting regime. It produces a compact forward affine document map; encoder, Recall and mixed-gallery limitations remain.

The method identity is `arc2_global_tangent2_r1`: centered rectangular Procrustes raw affine initialization, exactly two lambda=10 tangent updates, no local residual and no neural training (`configs/method.json`). Every method uses the same 1,024 allowed fitting pairs and paid gallery overwrites; anchors count in `|A union S|`. A document encoding budget is not the number of fitting pairs. Five seeds are averaged before query bootstrap; they do not multiply the independent query count.

From S.`aggregate_contrasts`, ARC2-minus-baseline nDCG effects and `ndcg10.ci_bonferroni_family95` are:

| Declared baseline configuration | Absolute nDCG delta | 99% interval, nominal family 95% |
|---|---:|---:|
| centered Procrustes | +0.0243251090 | [0.0181321752, 0.0307916403] |
| LA2M20 integration-script adaptation | +0.1040549538 | [0.0860703321, 0.1229148044] |
| official-code SimpleLinear final50 MLP5 | +0.1720998649 | [0.1498621518, 0.1947030038] |
| affine ridge lambda10, regularized bias | +0.0956530493 | [0.0754047208, 0.1164266866] |
| Embedding-Converter paper-spec adaptation | +0.1611623342 | [0.1426864118, 0.1799155828] |

The comparison with the strongest aggregate baseline matters most scientifically: macro nDCG is 0.5274775273 versus Procrustes 0.5031524183, a gain of about **2.43 nDCG points** (4.83% relative to that macro). It is a meaningful observed top-rank improvement in this fixed setting, not merely a nonzero p-value and not a predeclared practical quality threshold. Larger gains against neural/clustered adaptations should not carry the whole contribution.

S.`condition_contrasts` shows 23/24 positive mean nDCG effects versus Procrustes, 24/24 versus each other configuration. Nominal descriptive positive/unresolved counts are respectively 20/4, 24/0, 24/0, 17/7 and 23/1. These are not 120 multiplicity-controlled wins. The only nDCG negative mean against Procrustes is FiQA/E5/75%: `delta=-0.00358268756650346`, descriptive CI `[-0.009365669062142961,0.0022535550787560824]`, unresolved. Crossing zero is not equivalence or failure proof.

Recall limits are substantive. The aggregate Procrustes Recall delta is `-0.0002385903910903914`, descriptive CI `[-0.004943626172438673,0.0043358499949124945]`; condition mean signs are 11 positive, 12 negative and one tie. FiQA/E5/50% Recall delta is `-0.016504505494505495`, CI `[-0.029314690476190473,-0.0049844252136752205]`; at 75% it is `-0.0169761038961039`, CI `[-0.028262431096681098,-0.00640759740259741]`. Therefore nDCG evidence does not support Recall preservation.

All 24 ARC2 partial mean nDCGs in S.`means` are below **both** native Full-X and Full-Y. Full-X gaps range from -0.2805732372 to -0.0062492653; Full-Y gaps from -0.2347683637 to -0.0512088889. This statement is specific to nDCG; Recall exceeds Full-X in 8/24 and Full-Y in 1/24. Full-X uses its native query encoder and is operational context, not a mapper under the target-query condition. Full-Y is a reference, not a mathematical upper bound; on HotpotQA/FEVER it can itself trail Full-X. No immediate quality-improving cutover follows.

## 2. Mechanism: partial

Let M denote `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`. M.`overall_macro` supports an empirical DEV contribution of the second step: ARC2 minus `tangent1_l10` nDCG `0.006923862939737235`, `ci99_bonferroni_family95=[0.003809388309482942,0.009959126205904258]`. Two-versus-zero has delta `0.024325109040435233` and family interval `[0.01801533254696277,0.03102132243820168]`. The second step contributes about 0.69 nDCG points in the aggregate; it is smaller than the zero-to-two effect and does not remove encoder/Recall tradeoffs.

M does not establish optimality: lambda1 minus lambda10 is `+0.0031974956912717346`, family interval `[-0.0018903844098364442,0.00830403326634241]`, unresolved; lambda100 minus lambda10 is `-0.00925533869678723`, family interval `[-0.01321398029023485,-0.005510245768211927]`. Keep lambda10/two steps frozen. The normalization Jacobian supplies local angular intuition, not a finite-step monotonicity or convergence theorem. B2's existing external-method family does not independently test one-versus-two necessity. That attribution remains DEV; no new mandatory ablation is created here.

## 3. Practical/general/all-paid or cost superiority: no

Let P denote `results/b1p_r5_review_20261027/scoring/results_summary.json`. For FiQA50% and all 28,819 paid pairs, P.`contrasts[kind=arc2_allpaid_vs_baseline_allpaid]` records MiniLM ARC2-minus-Procrustes `+0.03375954732030533`, family CI `[0.018645329403840227,0.05040795355988812]`, and minus LA2M `+0.028222554511761314`, `[0.010129417979752293,0.04729686135338356]`. ARC2 also beats the declared SimpleLinear/converter configurations. Thus every benefit cannot be dismissed as merely withholding baseline supervision.

However, MiniLM all-paid ARC2 minus ridge is `-0.00011725527452398765`, family CI `[-0.00754001759934293,0.006532341944925181]`, unresolved, not equivalent. E5 all-paid ARC2 minus Procrustes is `-0.0443354790156809`, family CI `[-0.07969591141306612,-0.00927207701618083]`; minus LA2M is `-0.03747431937003851`, `[-0.07058268018538005,-0.003758372247374875]`. Their descriptive Recall losses are respectively `-0.0938989987789988` and `-0.08784069597069598`. These are real counterevidence to a general best-mapper or fair-allpaid claim.

Moreover, P.`contrasts[kind=arc2_fixed_vs_baseline_allpaid]` shows fixed1024 MiniLM ARC2 loses nDCG to **all five** all-paid comparators, including ridge delta `-0.05975841843915199`, family CI `[-0.08258263920537419,-0.03854644831580933]`. E5 fixed ARC2 loses to all-paid Procrustes (`-0.02456725354075626`) and LA2M (`-0.017706093895113878`), both with negative family intervals. Fixed-anchor success therefore cannot be sold as the best use of a budget that already provides reusable paid pairs.

A compact final map is valid structural evidence. For 384-to-768 dimensions its affine coefficients have 295,680 float32 entries (about 1.128 MiB), versus 33,927,168 weights/biases (129.422 MiB) in the specified converter. This excludes retained fitting objects and is not a runtime/RSS/dollar measurement. Ridge has the same coefficient size, and Procrustes is similarly compact. R3 receipt timings on a shared recovery host are not controlled physical efficiency comparisons. Physical migration, serving SLO, ANN-quality and real live-traffic advantages remain unsupported.

## 4. Mixed-gallery diagnostic: yes, descriptively

Let G denote `results/b1g_r1_review_20261027/scoring/results_summary.json`. G covers 450 partial cases, 210 pure fitted galleries, and exact historical per-query parity. In G.`aggregate_five_seed_conditions[FiQA,e5_small_base,arc2_global_tangent2_r1,allpaid28819,50pct]`, true replacement changes nDCG from `0.31490775036459107` to `0.29186698206096207`, delta `-0.023040768303629045`, and Recall delta is `-0.09467432234432235`. Paid top10 share falls from `0.49164` to `0.06472000000000001`. Paired score bias over the same diagnostic documents averages `+0.040654267241386696`; paid-nonanchor and unpaid biases are `+0.04174186702363513` and `+0.03968433437639738`.

This supports a compatibility limitation: a better pure-proxy endpoint does not guarantee a better mixed transition. It does not identify a unique causal error or establish a constant offset repair. Paid share need not equal population share, and the pure-proxy endpoint already consumed target fitting encodings. Diagnostic target references were excluded from fit/selection/pristine ranking. No calibration is incorporated into the frozen method.

## Baseline, exposure and deployment objections

The weakest-baseline objection is partly answered by positive macro effects against centered Procrustes and ordinary affine ridge, plus M's matched step controls, rather than relying on the largest neural deficits. It is not eliminated for general deployment: all-paid ridge remains competitive in MiniLM, and alignment wins in E5. LA2M20 is a script-guided matched-budget adaptation, not a published optimal cluster selection; SimpleLinear is the pinned official five-affine-layer MLP with final50 training, not a single linear map; the converter is a paper-spec anchor adaptation with its locked validation/refit policy, not the original multi-corpus reproduction. Do not translate these rows into universal published-method rankings.

The training-exposure objection remains: FiQA was inspected and method selection followed scores; all four datasets in this report are DEV. Converter validation/refit policy and the same 1,024-pair main regime must be disclosed. Fixed-anchor fits share a supervision count, not an assertion that their fitting procedures or validation exposures are identical. Completing breadth and deterministic numerical verification do not manufacture independence.

When-to-use is a candidate scope, not deployment advice: a target-query/target-gallery interface is required for external reasons, an existing source document space is available, only a fixed 1,024-pair mapper fit is intended, and approximate transition quality is acceptable pending confirmation. If native source retrieval remains acceptable, the observed nDCG comparisons provide no quality reason to cut over. If all paid pairs can be exploited, use the all-paid evidence when choosing a mapper. Recall-sensitive E5 use and mixed-score compatibility require particular caution; neither has a preservation guarantee. Operational requirements are assumptions until measured.

## Finite D1 and next action

**D1: narrow GO-C1**, for frozen fixed-anchor external-baseline quality confirmation only. The completed B1c removes the former unfinished-breadth gap. The Procrustes macro gain is resolved, M shows a second-step aggregate contribution, and MiniLM matched-allpaid improvements over Procrustes/LA2M show a nontrivial method effect survives beyond withheld supervision. This meets a bounded reproducible-quality route; it does not meet a general fair-allpaid or systems route. The unresolved ridge comparison is not rounded into a win, and E5 losses are not discarded.

The existing B2 is a useful finite test of that narrowed question: 180 partial cells plus four references = **184 rankings**, with **30** primary nDCG contrasts (five external configurations x two pairs x three budgets), five-seed averaging and simultaneous paired query intervals. Before any execution/labels, the user must release the current STOP and the immutable protocol must fix exact endpoint claims, rankings/ID/tie/reload checks, hashes and interpretation of all signs. A 50-query collection remains 50 queries, not 250. No universal-win threshold, post-hoc noninferiority margin, retuning, extra collection, independent all-paid study or second-step extension is mandatory for this planned route.

**STOP now after the completed DEV report and this final D1.** No B2/TREC or systems run is authorized by this review. B3/B4 remain conditional on B2 interpretation and a distinct predeclared operational question capable of distinguishing ARC2 from the strongest relevant comparator. Do not run them automatically or relabel the mapper result as a system win. Root documentation updates belong to the parent executor. Preserve all old failures, displaced cells and negative evidence.
