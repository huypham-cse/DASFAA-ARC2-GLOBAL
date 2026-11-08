# B1c-R3 complete six-method DEV results

Inspected development evidence; no independent confirmation or TREC access.

736 cells: 378 frozen imports and 358 new sealed rankings. All queries count; no-positive queries score zero. nDCG@10 uses graded 2^rel-1 gains. Recall@100 divides by all positive qrels, including documents outside the corpus.

Means average all queries then five mapping seeds. Seed SD uses ddof=1. Full-X and Full-Y are deterministic context/reference rankings; Full-Y is not an upper bound. All 160 means and 120 condition contrasts are descriptive, with nominal 95% query-bootstrap intervals in JSON.

The only inferential family is five ARC2-minus-external macro contrasts, equally weighting all 24 dataset/pair/budget strata. Each nDCG interval has 99% confidence (Bonferroni nominal family 95%). Recall intervals are nominal 95% descriptive. All 20,000 draws resample queries independently within each dataset, sharing query indices across every pair, budget, method and seed; the five seeds are averaged first. Percentile-bootstrap coverage is approximate.

| Macro contrast (ARC2 minus baseline) | nDCG delta [99% family interval] | Recall delta [descriptive 95%] |
|---|---:|---:|
| procrustes_global | +0.024325 [+0.018132, +0.030792] | -0.000239 [-0.004944, +0.004336] |
| la2m20_integration_script_adaptation | +0.104055 [+0.086070, +0.122915] | +0.090028 [+0.075394, +0.105760] |
| simplelinear_official_final50_mlp5 | +0.172100 [+0.149862, +0.194703] | +0.252882 [+0.236538, +0.269462] |
| ridge_affine_l10_bias_regularized | +0.095653 [+0.075405, +0.116427] | +0.121734 [+0.103216, +0.141376] |
| embedding_converter_paper_spec | +0.161162 [+0.142686, +0.179916] | +0.101758 [+0.087364, +0.116912] |

| Dataset | Pair | Budget | Method | nDCG mean (seed SD) | Recall mean (seed SD) |
|---|---|---|---|---:|---:|
| NanoNQ | minilm_distilroberta | 25pct | procrustes_global | 0.442147 (0.038952) | 0.960000 (0.023452) |
| NanoNQ | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.488807 (0.038594) | 0.970000 (0.007071) |
| NanoNQ | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | 0.347855 (0.013114) | 0.922000 (0.013038) |
| NanoNQ | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | 0.222132 (0.038619) | 0.922000 (0.014832) |
| NanoNQ | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.480723 (0.042100) | 0.922000 (0.022804) |
| NanoNQ | minilm_distilroberta | 25pct | embedding_converter_paper_spec | 0.355417 (0.021503) | 0.910000 (0.041231) |
| NanoNQ | minilm_distilroberta | 50pct | procrustes_global | 0.499511 (0.033637) | 0.954000 (0.020736) |
| NanoNQ | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.526624 (0.031210) | 0.970000 (0.012247) |
| NanoNQ | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | 0.425799 (0.022882) | 0.946000 (0.018166) |
| NanoNQ | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | 0.363870 (0.033279) | 0.920000 (0.020000) |
| NanoNQ | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.517769 (0.042852) | 0.930000 (0.023452) |
| NanoNQ | minilm_distilroberta | 50pct | embedding_converter_paper_spec | 0.437778 (0.023638) | 0.924000 (0.041593) |
| NanoNQ | minilm_distilroberta | 75pct | procrustes_global | 0.571429 (0.029136) | 0.962000 (0.013038) |
| NanoNQ | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.586833 (0.022697) | 0.976000 (0.008944) |
| NanoNQ | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | 0.545218 (0.027770) | 0.956000 (0.011402) |
| NanoNQ | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | 0.513224 (0.032193) | 0.952000 (0.021679) |
| NanoNQ | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.585492 (0.039399) | 0.948000 (0.022804) |
| NanoNQ | minilm_distilroberta | 75pct | embedding_converter_paper_spec | 0.558676 (0.030906) | 0.962000 (0.014832) |
| NanoNQ | minilm_distilroberta | full | full_x | 0.593082 (reference) | 0.940000 (reference) |
| NanoNQ | minilm_distilroberta | full | full_y | 0.678452 (reference) | 0.980000 (reference) |
| NanoNQ | e5_small_base | 25pct | procrustes_global | 0.485237 (0.028886) | 0.976000 (0.008944) |
| NanoNQ | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.507124 (0.027826) | 0.956000 (0.021909) |
| NanoNQ | e5_small_base | 25pct | la2m20_integration_script_adaptation | 0.364036 (0.031790) | 0.876000 (0.019494) |
| NanoNQ | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | 0.176670 (0.036812) | 0.338000 (0.020494) |
| NanoNQ | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.321913 (0.025969) | 0.840000 (0.010000) |
| NanoNQ | e5_small_base | 25pct | embedding_converter_paper_spec | 0.211340 (0.016946) | 0.862000 (0.037683) |
| NanoNQ | e5_small_base | 50pct | procrustes_global | 0.513091 (0.033191) | 0.968000 (0.010954) |
| NanoNQ | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.544348 (0.037044) | 0.956000 (0.008944) |
| NanoNQ | e5_small_base | 50pct | la2m20_integration_script_adaptation | 0.427521 (0.025104) | 0.888000 (0.039623) |
| NanoNQ | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | 0.319402 (0.015831) | 0.502000 (0.054037) |
| NanoNQ | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.387064 (0.035056) | 0.780000 (0.029155) |
| NanoNQ | e5_small_base | 50pct | embedding_converter_paper_spec | 0.275890 (0.025324) | 0.862000 (0.030332) |
| NanoNQ | e5_small_base | 75pct | procrustes_global | 0.591239 (0.025169) | 0.964000 (0.008944) |
| NanoNQ | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.610099 (0.029130) | 0.964000 (0.008944) |
| NanoNQ | e5_small_base | 75pct | la2m20_integration_script_adaptation | 0.540642 (0.044215) | 0.938000 (0.013038) |
| NanoNQ | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | 0.483878 (0.027387) | 0.700000 (0.010000) |
| NanoNQ | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.442841 (0.028881) | 0.754000 (0.041593) |
| NanoNQ | e5_small_base | 75pct | embedding_converter_paper_spec | 0.402087 (0.033090) | 0.892000 (0.034205) |
| NanoNQ | e5_small_base | full | full_x | 0.659510 (reference) | 0.930000 (reference) |
| NanoNQ | e5_small_base | full | full_y | 0.666908 (reference) | 0.960000 (reference) |
| NanoHotpotQA | minilm_distilroberta | 25pct | procrustes_global | 0.336179 (0.044108) | 0.808000 (0.032711) |
| NanoHotpotQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.375981 (0.048065) | 0.806000 (0.026077) |
| NanoHotpotQA | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | 0.262819 (0.063994) | 0.752000 (0.041473) |
| NanoHotpotQA | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | 0.217727 (0.039202) | 0.656000 (0.055946) |
| NanoHotpotQA | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.350533 (0.031933) | 0.750000 (0.020000) |
| NanoHotpotQA | minilm_distilroberta | 25pct | embedding_converter_paper_spec | 0.230659 (0.013630) | 0.708000 (0.013038) |
| NanoHotpotQA | minilm_distilroberta | 50pct | procrustes_global | 0.410956 (0.040583) | 0.824000 (0.019494) |
| NanoHotpotQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.443522 (0.046847) | 0.830000 (0.015811) |
| NanoHotpotQA | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | 0.368083 (0.053068) | 0.784000 (0.025100) |
| NanoHotpotQA | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | 0.339999 (0.032181) | 0.722000 (0.031145) |
| NanoHotpotQA | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.416879 (0.037214) | 0.766000 (0.025100) |
| NanoHotpotQA | minilm_distilroberta | 50pct | embedding_converter_paper_spec | 0.343507 (0.026759) | 0.780000 (0.018708) |
| NanoHotpotQA | minilm_distilroberta | 75pct | procrustes_global | 0.478114 (0.035229) | 0.842000 (0.010954) |
| NanoHotpotQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.493434 (0.028084) | 0.844000 (0.011402) |
| NanoHotpotQA | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | 0.464569 (0.033971) | 0.806000 (0.019494) |
| NanoHotpotQA | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | 0.448290 (0.025809) | 0.788000 (0.013038) |
| NanoHotpotQA | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.472982 (0.026034) | 0.782000 (0.021679) |
| NanoHotpotQA | minilm_distilroberta | 75pct | embedding_converter_paper_spec | 0.432884 (0.029363) | 0.814000 (0.019494) |
| NanoHotpotQA | minilm_distilroberta | full | full_x | 0.600563 (reference) | 0.890000 (reference) |
| NanoHotpotQA | minilm_distilroberta | full | full_y | 0.585935 (reference) | 0.880000 (reference) |
| NanoHotpotQA | e5_small_base | 25pct | procrustes_global | 0.551235 (0.031004) | 0.916000 (0.023022) |
| NanoHotpotQA | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.584486 (0.030010) | 0.914000 (0.020736) |
| NanoHotpotQA | e5_small_base | 25pct | la2m20_integration_script_adaptation | 0.386898 (0.054676) | 0.818000 (0.027749) |
| NanoHotpotQA | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | 0.252865 (0.058339) | 0.330000 (0.023452) |
| NanoHotpotQA | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.380443 (0.053647) | 0.760000 (0.050498) |
| NanoHotpotQA | e5_small_base | 25pct | embedding_converter_paper_spec | 0.240400 (0.018906) | 0.786000 (0.025100) |
| NanoHotpotQA | e5_small_base | 50pct | procrustes_global | 0.629928 (0.014138) | 0.936000 (0.011402) |
| NanoHotpotQA | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.672240 (0.019349) | 0.930000 (0.007071) |
| NanoHotpotQA | e5_small_base | 50pct | la2m20_integration_script_adaptation | 0.524958 (0.030544) | 0.858000 (0.014832) |
| NanoHotpotQA | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | 0.447797 (0.033410) | 0.536000 (0.018166) |
| NanoHotpotQA | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.442446 (0.026962) | 0.720000 (0.043012) |
| NanoHotpotQA | e5_small_base | 50pct | embedding_converter_paper_spec | 0.358757 (0.045691) | 0.852000 (0.029496) |
| NanoHotpotQA | e5_small_base | 75pct | procrustes_global | 0.720207 (0.017318) | 0.950000 (0.007071) |
| NanoHotpotQA | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.746388 (0.014814) | 0.948000 (0.008367) |
| NanoHotpotQA | e5_small_base | 75pct | la2m20_integration_script_adaptation | 0.669534 (0.021555) | 0.916000 (0.016733) |
| NanoHotpotQA | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | 0.617388 (0.023922) | 0.728000 (0.017889) |
| NanoHotpotQA | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.505347 (0.030573) | 0.674000 (0.048785) |
| NanoHotpotQA | e5_small_base | 75pct | embedding_converter_paper_spec | 0.501633 (0.018559) | 0.918000 (0.013038) |
| NanoHotpotQA | e5_small_base | full | full_x | 0.827753 (reference) | 0.950000 (reference) |
| NanoHotpotQA | e5_small_base | full | full_y | 0.819254 (reference) | 0.970000 (reference) |
| NanoFEVER | minilm_distilroberta | 25pct | procrustes_global | 0.507365 (0.032030) | 0.926000 (0.017385) |
| NanoFEVER | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.545253 (0.038295) | 0.932000 (0.010435) |
| NanoFEVER | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | 0.407049 (0.044351) | 0.798667 (0.049699) |
| NanoFEVER | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | 0.317965 (0.056041) | 0.818000 (0.051887) |
| NanoFEVER | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.494309 (0.041365) | 0.870000 (0.032489) |
| NanoFEVER | minilm_distilroberta | 25pct | embedding_converter_paper_spec | 0.414527 (0.067628) | 0.828667 (0.042986) |
| NanoFEVER | minilm_distilroberta | 50pct | procrustes_global | 0.581358 (0.021887) | 0.936000 (0.021654) |
| NanoFEVER | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.601114 (0.026115) | 0.942000 (0.016600) |
| NanoFEVER | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | 0.504084 (0.022061) | 0.832667 (0.039186) |
| NanoFEVER | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | 0.458844 (0.032567) | 0.868000 (0.051887) |
| NanoFEVER | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.548820 (0.022519) | 0.912000 (0.014453) |
| NanoFEVER | minilm_distilroberta | 50pct | embedding_converter_paper_spec | 0.527598 (0.041411) | 0.880000 (0.029814) |
| NanoFEVER | minilm_distilroberta | 75pct | procrustes_global | 0.672905 (0.020502) | 0.958667 (0.020494) |
| NanoFEVER | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.687064 (0.021792) | 0.966667 (0.016330) |
| NanoFEVER | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | 0.644983 (0.023469) | 0.915333 (0.034689) |
| NanoFEVER | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | 0.635301 (0.035145) | 0.928667 (0.037903) |
| NanoFEVER | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.653985 (0.008547) | 0.954667 (0.010954) |
| NanoFEVER | minilm_distilroberta | 75pct | embedding_converter_paper_spec | 0.637989 (0.020419) | 0.930667 (0.034351) |
| NanoFEVER | minilm_distilroberta | full | full_x | 0.825826 (reference) | 0.993333 (reference) |
| NanoFEVER | minilm_distilroberta | full | full_y | 0.749166 (reference) | 0.983333 (reference) |
| NanoFEVER | e5_small_base | 25pct | procrustes_global | 0.714662 (0.042561) | 0.987333 (0.015706) |
| NanoFEVER | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.755451 (0.045413) | 0.982000 (0.015384) |
| NanoFEVER | e5_small_base | 25pct | la2m20_integration_script_adaptation | 0.499051 (0.043478) | 0.906667 (0.033500) |
| NanoFEVER | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | 0.251613 (0.059729) | 0.392667 (0.058708) |
| NanoFEVER | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.644785 (0.051288) | 0.926667 (0.014530) |
| NanoFEVER | e5_small_base | 25pct | embedding_converter_paper_spec | 0.385169 (0.046753) | 0.857333 (0.043295) |
| NanoFEVER | e5_small_base | 50pct | procrustes_global | 0.740210 (0.023840) | 0.995333 (0.007303) |
| NanoFEVER | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.778950 (0.022241) | 0.988667 (0.012824) |
| NanoFEVER | e5_small_base | 50pct | la2m20_integration_script_adaptation | 0.607810 (0.044977) | 0.937333 (0.036240) |
| NanoFEVER | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | 0.472237 (0.051760) | 0.612667 (0.064739) |
| NanoFEVER | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.671094 (0.015162) | 0.894667 (0.017256) |
| NanoFEVER | e5_small_base | 50pct | embedding_converter_paper_spec | 0.562183 (0.041092) | 0.921333 (0.032880) |
| NanoFEVER | e5_small_base | 75pct | procrustes_global | 0.822735 (0.029239) | 0.995333 (0.007303) |
| NanoFEVER | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.845120 (0.025114) | 0.994000 (0.005477) |
| NanoFEVER | e5_small_base | 75pct | la2m20_integration_script_adaptation | 0.776405 (0.026888) | 0.964667 (0.023991) |
| NanoFEVER | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | 0.708746 (0.028298) | 0.820000 (0.032318) |
| NanoFEVER | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.728986 (0.008075) | 0.866667 (0.012247) |
| NanoFEVER | e5_small_base | 75pct | embedding_converter_paper_spec | 0.732576 (0.032257) | 0.954667 (0.019379) |
| NanoFEVER | e5_small_base | full | full_x | 0.898353 (reference) | 0.990000 (reference) |
| NanoFEVER | e5_small_base | full | full_y | 0.896329 (reference) | 1.000000 (reference) |
| FiQA | minilm_distilroberta | 25pct | procrustes_global | 0.256997 (0.006146) | 0.657992 (0.003162) |
| FiQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.287119 (0.005761) | 0.665014 (0.003963) |
| FiQA | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | 0.149025 (0.001873) | 0.391240 (0.010347) |
| FiQA | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | 0.142934 (0.000956) | 0.367393 (0.009583) |
| FiQA | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.247637 (0.005974) | 0.620122 (0.006011) |
| FiQA | minilm_distilroberta | 25pct | embedding_converter_paper_spec | 0.170509 (0.007797) | 0.476874 (0.014291) |
| FiQA | minilm_distilroberta | 50pct | procrustes_global | 0.285828 (0.004024) | 0.668792 (0.005208) |
| FiQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.307505 (0.006017) | 0.676569 (0.001741) |
| FiQA | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | 0.237674 (0.003024) | 0.465518 (0.006950) |
| FiQA | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | 0.235953 (0.002560) | 0.432511 (0.002190) |
| FiQA | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.289045 (0.005862) | 0.637377 (0.001793) |
| FiQA | minilm_distilroberta | 50pct | embedding_converter_paper_spec | 0.250101 (0.004706) | 0.544821 (0.011164) |
| FiQA | minilm_distilroberta | 75pct | procrustes_global | 0.341744 (0.001793) | 0.683156 (0.004849) |
| FiQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.350072 (0.002395) | 0.688481 (0.003513) |
| FiQA | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | 0.323983 (0.001112) | 0.580790 (0.006606) |
| FiQA | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | 0.323485 (0.001019) | 0.570792 (0.004154) |
| FiQA | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.343745 (0.002736) | 0.663087 (0.001598) |
| FiQA | minilm_distilroberta | 75pct | embedding_converter_paper_spec | 0.324330 (0.003491) | 0.625701 (0.006146) |
| FiQA | minilm_distilroberta | full | full_x | 0.389961 (reference) | 0.700184 (reference) |
| FiQA | minilm_distilroberta | full | full_y | 0.404736 (reference) | 0.703892 (reference) |
| FiQA | e5_small_base | 25pct | procrustes_global | 0.271778 (0.001281) | 0.602775 (0.007259) |
| FiQA | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.273107 (0.004827) | 0.599738 (0.009300) |
| FiQA | e5_small_base | 25pct | la2m20_integration_script_adaptation | 0.141574 (0.005398) | 0.336564 (0.022131) |
| FiQA | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | 0.106437 (0.002866) | 0.136716 (0.005819) |
| FiQA | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.128054 (0.003612) | 0.333045 (0.007519) |
| FiQA | e5_small_base | 25pct | embedding_converter_paper_spec | 0.087012 (0.007320) | 0.280107 (0.022550) |
| FiQA | e5_small_base | 50pct | procrustes_global | 0.310036 (0.002542) | 0.637429 (0.006658) |
| FiQA | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.311635 (0.003373) | 0.620925 (0.008032) |
| FiQA | e5_small_base | 50pct | la2m20_integration_script_adaptation | 0.229990 (0.003297) | 0.450604 (0.014097) |
| FiQA | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | 0.194167 (0.003687) | 0.260156 (0.005130) |
| FiQA | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.147922 (0.004371) | 0.305270 (0.006730) |
| FiQA | e5_small_base | 50pct | embedding_converter_paper_spec | 0.141009 (0.009980) | 0.337812 (0.018610) |
| FiQA | e5_small_base | 75pct | procrustes_global | 0.340768 (0.001368) | 0.677585 (0.001652) |
| FiQA | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.337185 (0.002324) | 0.660609 (0.004347) |
| FiQA | e5_small_base | 75pct | la2m20_integration_script_adaptation | 0.312583 (0.001734) | 0.579956 (0.006230) |
| FiQA | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | 0.278140 (0.003894) | 0.409930 (0.011177) |
| FiQA | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.160971 (0.003197) | 0.249477 (0.003220) |
| FiQA | e5_small_base | 75pct | embedding_converter_paper_spec | 0.209534 (0.007012) | 0.430505 (0.012797) |
| FiQA | e5_small_base | full | full_x | 0.346478 (reference) | 0.645332 (reference) |
| FiQA | e5_small_base | full | full_y | 0.389133 (reference) | 0.696797 (reference) |

| Dataset | Pair | Budget | ARC2 minus baseline | nDCG delta [descriptive 95%] | Recall delta [descriptive 95%] |
|---|---|---|---|---:|---:|
| NanoNQ | minilm_distilroberta | 25pct | procrustes_global | +0.046659 [+0.029898, +0.064994] | +0.010000 [+0.000000, +0.024000] |
| NanoNQ | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | +0.140952 [+0.091326, +0.194291] | +0.048000 [+0.010000, +0.096000] |
| NanoNQ | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | +0.266675 [+0.196309, +0.338375] | +0.048000 [+0.012000, +0.096000] |
| NanoNQ | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | +0.008084 [-0.018102, +0.035199] | +0.048000 [+0.010000, +0.100000] |
| NanoNQ | minilm_distilroberta | 25pct | embedding_converter_paper_spec | +0.133390 [+0.080558, +0.189730] | +0.060000 [+0.020000, +0.106000] |
| NanoNQ | minilm_distilroberta | 50pct | procrustes_global | +0.027114 [+0.015148, +0.039906] | +0.016000 [+0.000000, +0.044000] |
| NanoNQ | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | +0.100825 [+0.062730, +0.143346] | +0.024000 [-0.002000, +0.058000] |
| NanoNQ | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | +0.162754 [+0.115153, +0.212340] | +0.050000 [+0.020000, +0.086000] |
| NanoNQ | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | +0.008855 [-0.014068, +0.032913] | +0.040000 [+0.000000, +0.096000] |
| NanoNQ | minilm_distilroberta | 50pct | embedding_converter_paper_spec | +0.088847 [+0.044654, +0.135372] | +0.046000 [+0.018000, +0.080000] |
| NanoNQ | minilm_distilroberta | 75pct | procrustes_global | +0.015404 [+0.005097, +0.028704] | +0.014000 [+0.000000, +0.036000] |
| NanoNQ | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | +0.041615 [+0.018905, +0.072589] | +0.020000 [+0.006000, +0.038000] |
| NanoNQ | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | +0.073608 [+0.043874, +0.107009] | +0.024000 [+0.004000, +0.048000] |
| NanoNQ | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | +0.001340 [-0.019184, +0.021696] | +0.028000 [-0.004000, +0.072000] |
| NanoNQ | minilm_distilroberta | 75pct | embedding_converter_paper_spec | +0.028157 [-0.003755, +0.062333] | +0.014000 [+0.002000, +0.028000] |
| NanoNQ | e5_small_base | 25pct | procrustes_global | +0.021887 [+0.004588, +0.039224] | -0.020000 [-0.048000, +0.000000] |
| NanoNQ | e5_small_base | 25pct | la2m20_integration_script_adaptation | +0.143087 [+0.080860, +0.210953] | +0.080000 [+0.018000, +0.152000] |
| NanoNQ | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | +0.330454 [+0.247753, +0.415194] | +0.618000 [+0.542000, +0.692000] |
| NanoNQ | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | +0.185210 [+0.120907, +0.253543] | +0.116000 [+0.060000, +0.184000] |
| NanoNQ | e5_small_base | 25pct | embedding_converter_paper_spec | +0.295784 [+0.221047, +0.371512] | +0.094000 [+0.042000, +0.152000] |
| NanoNQ | e5_small_base | 50pct | procrustes_global | +0.031258 [+0.014752, +0.049324] | -0.012000 [-0.036000, +0.000000] |
| NanoNQ | e5_small_base | 50pct | la2m20_integration_script_adaptation | +0.116828 [+0.071832, +0.165802] | +0.068000 [+0.020000, +0.126000] |
| NanoNQ | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | +0.224947 [+0.168091, +0.283299] | +0.454000 [+0.390000, +0.518000] |
| NanoNQ | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | +0.157284 [+0.096414, +0.222747] | +0.176000 [+0.102000, +0.256000] |
| NanoNQ | e5_small_base | 50pct | embedding_converter_paper_spec | +0.268459 [+0.209996, +0.328217] | +0.094000 [+0.044000, +0.154000] |
| NanoNQ | e5_small_base | 75pct | procrustes_global | +0.018860 [+0.006173, +0.032449] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | e5_small_base | 75pct | la2m20_integration_script_adaptation | +0.069458 [+0.042337, +0.098304] | +0.026000 [+0.010000, +0.046000] |
| NanoNQ | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | +0.126222 [+0.085996, +0.168849] | +0.264000 [+0.195950, +0.340000] |
| NanoNQ | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | +0.167258 [+0.089144, +0.253864] | +0.210000 [+0.114000, +0.312000] |
| NanoNQ | e5_small_base | 75pct | embedding_converter_paper_spec | +0.208012 [+0.149533, +0.269729] | +0.072000 [+0.020000, +0.140000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | procrustes_global | +0.039802 [+0.023406, +0.056468] | -0.002000 [-0.022000, +0.016000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | +0.113162 [+0.073993, +0.153315] | +0.054000 [+0.014000, +0.096000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | +0.158254 [+0.112369, +0.205816] | +0.150000 [+0.096000, +0.208000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | +0.025448 [-0.006781, +0.056863] | +0.056000 [+0.020000, +0.096000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | embedding_converter_paper_spec | +0.145322 [+0.099969, +0.192511] | +0.098000 [+0.048000, +0.152000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | procrustes_global | +0.032566 [+0.016729, +0.048597] | +0.006000 [-0.016000, +0.028000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | +0.075439 [+0.044008, +0.107538] | +0.046000 [+0.010000, +0.082000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | +0.103523 [+0.072283, +0.136143] | +0.108000 [+0.062000, +0.158000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | +0.026642 [-0.006030, +0.059253] | +0.064000 [+0.020000, +0.116000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | embedding_converter_paper_spec | +0.100015 [+0.066148, +0.134612] | +0.050000 [+0.012000, +0.092000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | procrustes_global | +0.015320 [+0.003362, +0.027506] | +0.002000 [-0.020000, +0.018000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | +0.028866 [+0.009854, +0.048431] | +0.038000 [+0.016000, +0.062000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | +0.045145 [+0.023619, +0.068886] | +0.056000 [+0.026000, +0.090000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | +0.020452 [-0.005571, +0.048929] | +0.062000 [+0.014000, +0.116000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | embedding_converter_paper_spec | +0.060550 [+0.031902, +0.091652] | +0.030000 [+0.006000, +0.056000] |
| NanoHotpotQA | e5_small_base | 25pct | procrustes_global | +0.033251 [+0.010252, +0.053575] | -0.002000 [-0.016000, +0.012000] |
| NanoHotpotQA | e5_small_base | 25pct | la2m20_integration_script_adaptation | +0.197587 [+0.146143, +0.248330] | +0.096000 [+0.052000, +0.144000] |
| NanoHotpotQA | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | +0.331621 [+0.273474, +0.391232] | +0.584000 [+0.534000, +0.632000] |
| NanoHotpotQA | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | +0.204042 [+0.146886, +0.263884] | +0.154000 [+0.104000, +0.206000] |
| NanoHotpotQA | e5_small_base | 25pct | embedding_converter_paper_spec | +0.344086 [+0.296238, +0.393172] | +0.128000 [+0.078000, +0.182000] |
| NanoHotpotQA | e5_small_base | 50pct | procrustes_global | +0.042311 [+0.021366, +0.063227] | -0.006000 [-0.026000, +0.008000] |
| NanoHotpotQA | e5_small_base | 50pct | la2m20_integration_script_adaptation | +0.147282 [+0.106353, +0.188936] | +0.072000 [+0.030000, +0.116000] |
| NanoHotpotQA | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | +0.224442 [+0.178952, +0.271793] | +0.394000 [+0.343950, +0.446000] |
| NanoHotpotQA | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | +0.229793 [+0.167328, +0.293932] | +0.210000 [+0.152000, +0.272000] |
| NanoHotpotQA | e5_small_base | 50pct | embedding_converter_paper_spec | +0.313482 [+0.265043, +0.364007] | +0.078000 [+0.042000, +0.118000] |
| NanoHotpotQA | e5_small_base | 75pct | procrustes_global | +0.026180 [+0.008469, +0.044408] | -0.002000 [-0.018000, +0.010000] |
| NanoHotpotQA | e5_small_base | 75pct | la2m20_integration_script_adaptation | +0.076854 [+0.049633, +0.107124] | +0.032000 [-0.000000, +0.066000] |
| NanoHotpotQA | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | +0.129000 [+0.097318, +0.163879] | +0.220000 [+0.176000, +0.266000] |
| NanoHotpotQA | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | +0.241041 [+0.169538, +0.316316] | +0.274000 [+0.198000, +0.354000] |
| NanoHotpotQA | e5_small_base | 75pct | embedding_converter_paper_spec | +0.244754 [+0.195361, +0.295165] | +0.030000 [+0.004000, +0.062000] |
| NanoFEVER | minilm_distilroberta | 25pct | procrustes_global | +0.037888 [+0.017533, +0.060328] | +0.006000 [-0.012000, +0.024000] |
| NanoFEVER | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | +0.138204 [+0.083041, +0.196919] | +0.133333 [+0.065333, +0.209333] |
| NanoFEVER | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | +0.227288 [+0.168509, +0.287061] | +0.114000 [+0.056000, +0.180000] |
| NanoFEVER | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | +0.050943 [+0.026041, +0.077454] | +0.062000 [+0.022000, +0.112000] |
| NanoFEVER | minilm_distilroberta | 25pct | embedding_converter_paper_spec | +0.130726 [+0.079810, +0.181050] | +0.103333 [+0.055333, +0.158000] |
| NanoFEVER | minilm_distilroberta | 50pct | procrustes_global | +0.019756 [+0.006897, +0.033846] | +0.006000 [-0.012000, +0.024000] |
| NanoFEVER | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | +0.097030 [+0.055769, +0.143728] | +0.109333 [+0.055333, +0.170000] |
| NanoFEVER | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | +0.142270 [+0.092947, +0.196271] | +0.074000 [+0.036000, +0.118000] |
| NanoFEVER | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | +0.052295 [+0.027960, +0.078489] | +0.030000 [+0.000000, +0.068000] |
| NanoFEVER | minilm_distilroberta | 50pct | embedding_converter_paper_spec | +0.073517 [+0.036233, +0.111307] | +0.062000 [+0.018000, +0.110000] |
| NanoFEVER | minilm_distilroberta | 75pct | procrustes_global | +0.014159 [-0.000724, +0.031073] | +0.008000 [+0.000000, +0.020000] |
| NanoFEVER | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | +0.042081 [+0.016825, +0.069941] | +0.051333 [+0.016667, +0.094000] |
| NanoFEVER | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | +0.051763 [+0.022384, +0.083999] | +0.038000 [+0.014000, +0.066000] |
| NanoFEVER | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | +0.033079 [+0.012252, +0.055043] | +0.012000 [-0.004000, +0.036000] |
| NanoFEVER | minilm_distilroberta | 75pct | embedding_converter_paper_spec | +0.049075 [+0.020699, +0.075974] | +0.036000 [+0.008000, +0.070000] |
| NanoFEVER | e5_small_base | 25pct | procrustes_global | +0.040790 [+0.024462, +0.059260] | -0.005333 [-0.012000, +0.000000] |
| NanoFEVER | e5_small_base | 25pct | la2m20_integration_script_adaptation | +0.256401 [+0.196015, +0.317570] | +0.075333 [+0.032667, +0.126000] |
| NanoFEVER | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | +0.503839 [+0.434494, +0.570531] | +0.589333 [+0.514650, +0.662000] |
| NanoFEVER | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | +0.110667 [+0.061345, +0.162427] | +0.055333 [+0.013317, +0.111333] |
| NanoFEVER | e5_small_base | 25pct | embedding_converter_paper_spec | +0.370282 [+0.325571, +0.415445] | +0.124667 [+0.068000, +0.188000] |
| NanoFEVER | e5_small_base | 50pct | procrustes_global | +0.038740 [+0.023294, +0.055350] | -0.006667 [-0.017333, +0.000000] |
| NanoFEVER | e5_small_base | 50pct | la2m20_integration_script_adaptation | +0.171140 [+0.128610, +0.215100] | +0.051333 [+0.017333, +0.091333] |
| NanoFEVER | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | +0.306713 [+0.254067, +0.360874] | +0.376000 [+0.304000, +0.448000] |
| NanoFEVER | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | +0.107856 [+0.053210, +0.169800] | +0.094000 [+0.032000, +0.168000] |
| NanoFEVER | e5_small_base | 50pct | embedding_converter_paper_spec | +0.216767 [+0.180159, +0.254080] | +0.067333 [+0.028000, +0.112667] |
| NanoFEVER | e5_small_base | 75pct | procrustes_global | +0.022385 [+0.008202, +0.038244] | -0.001333 [-0.016000, +0.010000] |
| NanoFEVER | e5_small_base | 75pct | la2m20_integration_script_adaptation | +0.068715 [+0.038532, +0.101722] | +0.029333 [+0.003333, +0.060000] |
| NanoFEVER | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | +0.136374 [+0.098578, +0.177618] | +0.174000 [+0.120000, +0.232000] |
| NanoFEVER | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | +0.116134 [+0.044334, +0.196846] | +0.127333 [+0.052000, +0.215333] |
| NanoFEVER | e5_small_base | 75pct | embedding_converter_paper_spec | +0.112544 [+0.076072, +0.152826] | +0.039333 [+0.008000, +0.078000] |
| FiQA | minilm_distilroberta | 25pct | procrustes_global | +0.030123 [+0.024283, +0.036154] | +0.007022 [-0.000292, +0.014256] |
| FiQA | minilm_distilroberta | 25pct | la2m20_integration_script_adaptation | +0.138095 [+0.118084, +0.159184] | +0.273775 [+0.244768, +0.302141] |
| FiQA | minilm_distilroberta | 25pct | simplelinear_official_final50_mlp5 | +0.144186 [+0.123851, +0.165580] | +0.297622 [+0.265992, +0.328668] |
| FiQA | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | +0.039483 [+0.028035, +0.051243] | +0.044893 [+0.030316, +0.060075] |
| FiQA | minilm_distilroberta | 25pct | embedding_converter_paper_spec | +0.116610 [+0.100018, +0.134202] | +0.188141 [+0.166316, +0.210333] |
| FiQA | minilm_distilroberta | 50pct | procrustes_global | +0.021677 [+0.016900, +0.026940] | +0.007778 [-0.000648, +0.015859] |
| FiQA | minilm_distilroberta | 50pct | la2m20_integration_script_adaptation | +0.069831 [+0.055271, +0.085544] | +0.211051 [+0.181381, +0.240180] |
| FiQA | minilm_distilroberta | 50pct | simplelinear_official_final50_mlp5 | +0.071552 [+0.056814, +0.087550] | +0.244058 [+0.211935, +0.276182] |
| FiQA | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | +0.018459 [+0.010229, +0.026911] | +0.039193 [+0.023609, +0.055755] |
| FiQA | minilm_distilroberta | 50pct | embedding_converter_paper_spec | +0.057404 [+0.045439, +0.070222] | +0.131748 [+0.112206, +0.151952] |
| FiQA | minilm_distilroberta | 75pct | procrustes_global | +0.008328 [+0.004861, +0.012214] | +0.005325 [-0.002227, +0.012208] |
| FiQA | minilm_distilroberta | 75pct | la2m20_integration_script_adaptation | +0.026089 [+0.017044, +0.036380] | +0.107691 [+0.085918, +0.129615] |
| FiQA | minilm_distilroberta | 75pct | simplelinear_official_final50_mlp5 | +0.026587 [+0.017477, +0.036935] | +0.117689 [+0.095257, +0.140660] |
| FiQA | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | +0.006328 [-0.000063, +0.012667] | +0.025394 [+0.012244, +0.039269] |
| FiQA | minilm_distilroberta | 75pct | embedding_converter_paper_spec | +0.025742 [+0.017905, +0.034413] | +0.062780 [+0.048062, +0.078404] |
| FiQA | e5_small_base | 25pct | procrustes_global | +0.001329 [-0.004045, +0.006739] | -0.003037 [-0.012551, +0.005497] |
| FiQA | e5_small_base | 25pct | la2m20_integration_script_adaptation | +0.131533 [+0.107335, +0.156879] | +0.263175 [+0.231888, +0.294066] |
| FiQA | e5_small_base | 25pct | simplelinear_official_final50_mlp5 | +0.166670 [+0.142300, +0.192181] | +0.463023 [+0.429595, +0.496315] |
| FiQA | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | +0.145052 [+0.122101, +0.168694] | +0.266693 [+0.235177, +0.298572] |
| FiQA | e5_small_base | 25pct | embedding_converter_paper_spec | +0.186095 [+0.164382, +0.208448] | +0.319631 [+0.292067, +0.347496] |
| FiQA | e5_small_base | 50pct | procrustes_global | +0.001599 [-0.004109, +0.007288] | -0.016505 [-0.029315, -0.004984] |
| FiQA | e5_small_base | 50pct | la2m20_integration_script_adaptation | +0.081645 [+0.059304, +0.104505] | +0.170320 [+0.138879, +0.201335] |
| FiQA | e5_small_base | 50pct | simplelinear_official_final50_mlp5 | +0.117468 [+0.095032, +0.140533] | +0.360769 [+0.328771, +0.392712] |
| FiQA | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | +0.163714 [+0.139582, +0.188333] | +0.315655 [+0.282666, +0.348524] |
| FiQA | e5_small_base | 50pct | embedding_converter_paper_spec | +0.170626 [+0.149992, +0.191530] | +0.283112 [+0.255725, +0.310933] |
| FiQA | e5_small_base | 75pct | procrustes_global | -0.003583 [-0.009366, +0.002254] | -0.016976 [-0.028262, -0.006408] |
| FiQA | e5_small_base | 75pct | la2m20_integration_script_adaptation | +0.024602 [+0.009283, +0.040749] | +0.080653 [+0.054921, +0.105701] |
| FiQA | e5_small_base | 75pct | simplelinear_official_final50_mlp5 | +0.059046 [+0.043505, +0.075356] | +0.250679 [+0.222125, +0.279890] |
| FiQA | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | +0.176214 [+0.151480, +0.201713] | +0.411132 [+0.375872, +0.446237] |
| FiQA | e5_small_base | 75pct | embedding_converter_paper_spec | +0.127652 [+0.111784, +0.144211] | +0.230105 [+0.203039, +0.257855] |

The original38 displaced FiQA cells remain historical provenance; their prospective replacements are the active R3 cells. The 120 condition comparisons are not 120 family-tested wins. An interval touching or crossing zero is unresolved; no equivalence/noninferiority margin is specified. Preserve all negative results and baseline adaptation qualifications. No retuning, method selection, independent, cost, SLO or causal claim follows from this scorer. STOP for the authorized final D1 report; no TREC or systems run.
