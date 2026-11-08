# B1-M completed; B1-P0 numerical readiness PASS

Both user-authorized items are complete. Frozen ARC2-Global remains two steps/lambda 10. STOP before B1-P/B1-G/main learned-baseline breadth/TREC/systems.

Ranking computation pre-run commit: 4056612dcccac74fdf84ccf67783ab87afd85c26 (R1 Linux input-byte amendment). Scoring repair pre-run commit: 55a600f104ded05562d4212d7c07a1330701a4b0. Original first protocol 5070bda and all failed attempts remain preserved.

## Mechanism findings

NanoNQ, NanoHotpotQA, NanoFEVER and FiQA DEV; two encoder pairs; five seeds; 25/50/75% budgets. Each mean condition averages all queries and five seeds. Macro estimates weight 24 dataset/pair/budget cells equally. Counts below are higher means, not numbers of individually significant comparisons.

| Primary minus comparator | Macro delta nDCG@10 | 99% interval, five-contrast family | Higher/lower mean conditions |
|---|---:|---|---|
| Procrustes (zero steps) | +0.024325 | [+0.018015, +0.031021] | 23 / 1 |
| one tangent step | +0.006924 | [+0.003809, +0.009959] | 22 / 2 |
| affine ridge | +0.095653 | [+0.075353, +0.116631] | 24 / 0 |

The second tangent update has a positive aggregate nDCG contribution beyond one step. The improvement over ordinary ridge supports testing the Procrustes initialization/angular refinement mechanism in this fixed 1,024-anchor regime. These are DEV mechanism findings, not a comparison against every external method or an independent paper victory.

## Sensitivity and retained negatives

- tangent2_l1 minus fixed lambda 10: +0.003197, 99% CI [-0.001890, +0.008304].
- tangent2_l100 minus fixed lambda 10: -0.009255, 99% CI [-0.013214, -0.005510].
- E5 macro Recall@100 vs Procrustes: -0.007654, descriptive 95% CI [-0.014072, -0.002479].
- FiQA E5 at 75% has lower mean nDCG than Procrustes (delta -0.003583; interval crosses zero) and lower Recall. FiQA E5 one-step comparisons at 50/75% are also retained.

Lambda 10 is retained as locked; lambda 1 is not selected after seeing scores. Full-X/Y references and every positive/negative condition are in [the detailed generated report](b1m_full_r1_20261026/scoring_r2_binary/results_summary.md).

## B1-P0

- Synthetic full validation: 31 fixtures, 62 update comparisons, including 1,024/2048 synthetic anchors; all gates passed.
- Real validation: 40 ordered 1,024-anchor fits and 120 paid-gallery budget comparisons. Changed ordered top100 query comparisons: 0.
- Largest real stored-coefficient difference: 7.27595761418e-12; normalized proxy difference: 3.72529029846e-09. All score-gap/numeric gates passed.
- The identified primal backend stays opt-in; primary quality rankings used frozen dual. No real 28,819-pair fit or all-paid benchmark was run. This is backend readiness, not byte-identical coefficients or a physical cost claim.

## Execution, failures and storage

The R1 mechanism computational attempt recorded 14.03 minutes and peak process-tree RSS 1.84 GiB on the shared host, excluding preparation/transfer and the later scoring repair. P0 synthetic full took 4.28s with RSS 0.18 GiB. These timings are not isolated deployment cost.
Nano preparation physically encoded 60,484 document representations and 600 query representations across four models. FiQA vectors were hash-verified caches.44 existing FiQA rankings matched after qrel-free identity checking and retained original bytes. The other 692 cells are new, including 360 new ablation rows. No cached vector is billed as a fresh deployment encoding.
The first smoke stopped on two Windows-working-copy/Git-LF derived JSON hashes before encoding/scoring. R1 corrected exact deployed input bytes, preserving the first attempt. The R1 computational run completed 736 rankings and 120 real P0 checks, then failed parsing published binary Nano qrels. Original metadata remains FAILED_PRESERVED. The R2 amendment interprets listed Nano pairs as relevance 1 according to the official evaluator; it changed no ranking, fitting or metric formula. R2 separately records successful DEV scoring and preserves the original NanoNQ first-label access and failure.

Local verification passed: all 736 ranking hashes, sealed input hashes, per-query means and the 20,000-draw paired-bootstrap arithmetic were checked without opening qrels. TREC labels remain closed.

This local bundle contains the raw rankings, per-query outputs, IDs/selections, metadata/logs and a complete 2,201-file H100 manifest. Full vector/coefficient/synthetic-array payloads (about 1.38 GB total raw campaign files) remain at `/root/arc2_global_paper_20261025/code_4056612/results/`; they were hash-inventoried/checked on H100 and omitted from the 38 MB review transfer. This is an explicitly selected local bundle, not a claim of full raw backup.

## Next authorized decision

Wait for user instruction before B1-P (the matched FiQA 50% all-paid-pairs experiment on all six systems), B1-G, remaining external-baseline breadth, D1 and prospective TREC confirmation. The unchanged live plan remains refine-logs/EXPERIMENT_PLAN.md. No automatic next-stage job is running.
