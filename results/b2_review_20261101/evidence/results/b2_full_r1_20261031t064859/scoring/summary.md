# B2 independent TREC-COVID results

All 184 rankings were sealed and separately recomputed before the one-shot final label opening. No postlabel tuning or method selection.

Thirty ARC2-minus-external nDCG@10 contrasts use nominal 99.833333% percentile intervals (Bonferroni 0.05/30, approximate family 95%). Recall@100 intervals are nominal 95% descriptive. Five mapping seeds are averaged before the shared paired query bootstrap. An interval touching or crossing zero is unresolved; no equivalence claim.

| Pair | Budget | ARC2 minus baseline | nDCG delta [family interval] | Recall delta [descriptive 95%] |
|---|---|---|---:|---:|
| minilm_distilroberta | 25pct | procrustes_global | -0.000051 [-0.014695, +0.013214] | +0.003062 [+0.001732, +0.004549] |
| minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | -0.001504 [-0.034306, +0.029079] | +0.016063 [+0.010314, +0.022957] |
| minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | +0.000873 [-0.032945, +0.032548] | +0.027056 [+0.019498, +0.035856] |
| minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | +0.029743 [-0.004478, +0.068326] | +0.020730 [+0.015280, +0.026654] |
| minilm_distilroberta | 25pct | embedding_converter_paper_spec | +0.039540 [+0.000630, +0.075613] | +0.024510 [+0.018926, +0.030734] |
| minilm_distilroberta | 50pct | procrustes_global | -0.004667 [-0.018618, +0.006099] | +0.001806 [+0.000673, +0.002993] |
| minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | -0.007321 [-0.026683, +0.007138] | +0.006869 [+0.003837, +0.010151] |
| minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | -0.007635 [-0.027398, +0.006922] | +0.010814 [+0.007279, +0.014730] |
| minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | +0.014517 [-0.010799, +0.042098] | +0.017297 [+0.012462, +0.023118] |
| minilm_distilroberta | 50pct | embedding_converter_paper_spec | +0.021908 [+0.000518, +0.042639] | +0.018118 [+0.014306, +0.022365] |
| minilm_distilroberta | 75pct | procrustes_global | -0.000024 [-0.004505, +0.004384] | +0.000407 [-0.000463, +0.001300] |
| minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | +0.000951 [-0.006116, +0.008781] | +0.001567 [+0.000290, +0.002926] |
| minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | +0.000211 [-0.006828, +0.008019] | +0.002820 [+0.001529, +0.004220] |
| minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | +0.018294 [+0.000440, +0.044923] | +0.014198 [+0.010259, +0.018863] |
| minilm_distilroberta | 75pct | embedding_converter_paper_spec | +0.016258 [-0.000045, +0.032084] | +0.010635 [+0.008556, +0.012882] |
| e5_small_base | 25pct | procrustes_global | -0.003240 [-0.021621, +0.014325] | -0.001991 [-0.003292, -0.000680] |
| e5_small_base | 25pct | la2m20_integration_script_adaptation | +0.042211 [-0.006417, +0.093325] | +0.027254 [+0.019888, +0.035465] |
| e5_small_base | 25pct | simplelinear_official_final50_mlp5 | +0.132873 [+0.063300, +0.205137] | +0.056936 [+0.046316, +0.068395] |
| e5_small_base | 25pct | ridge_affine_l10_bias_regularized | +0.264181 [+0.157265, +0.376758] | +0.049316 [+0.037455, +0.062524] |
| e5_small_base | 25pct | embedding_converter_paper_spec | +0.257234 [+0.175731, +0.337569] | +0.044332 [+0.034486, +0.055240] |
| e5_small_base | 50pct | procrustes_global | -0.016322 [-0.039820, +0.002298] | -0.004733 [-0.006442, -0.003115] |
| e5_small_base | 50pct | la2m20_integration_script_adaptation | +0.000594 [-0.035513, +0.035996] | +0.010501 [+0.006675, +0.014758] |
| e5_small_base | 50pct | simplelinear_official_final50_mlp5 | +0.061730 [+0.013560, +0.114461] | +0.041869 [+0.033103, +0.051642] |
| e5_small_base | 50pct | ridge_affine_l10_bias_regularized | +0.262267 [+0.157959, +0.372850] | +0.054625 [+0.042104, +0.068216] |
| e5_small_base | 50pct | embedding_converter_paper_spec | +0.231385 [+0.156717, +0.308507] | +0.043330 [+0.034415, +0.052916] |
| e5_small_base | 75pct | procrustes_global | -0.010012 [-0.026005, +0.003631] | -0.006389 [-0.008764, -0.004324] |
| e5_small_base | 75pct | la2m20_integration_script_adaptation | -0.008995 [-0.035779, +0.015646] | -0.001925 [-0.004529, +0.000478] |
| e5_small_base | 75pct | simplelinear_official_final50_mlp5 | +0.031288 [-0.003830, +0.071705] | +0.030384 [+0.022192, +0.039863] |
| e5_small_base | 75pct | ridge_affine_l10_bias_regularized | +0.281997 [+0.174800, +0.397330] | +0.063097 [+0.050156, +0.076625] |
| e5_small_base | 75pct | embedding_converter_paper_spec | +0.199954 [+0.139250, +0.264222] | +0.041427 [+0.033010, +0.050598] |

Full-X is the incumbent reference; Full-Y is the native destination reference, not an upper bound. All evaluation queries count, including queries with zero positive judgments. Graded gains are 2^rel-1. Recall divides by all positive judgments, including documents outside the corpus. All seed means, standard deviations and ranges are retained in JSON.

STOP for independent result-to-claim review. Manuscript remains untouched; no systems or ANN claim.
