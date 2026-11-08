# B1-M development mechanism results

Development evidence only, including previously inspected FiQA. The fixed proposed method remains two tangent steps, lambda=10.

All evaluation queries count; no-positive-judgment queries receive zero. nDCG@10 uses graded 2^rel−1 gain; Recall@100 divides by all positive qrels.

Means average queries then five seeds; seed SD is sample SD (ddof=1). Full references have one deterministic ranking.

| Dataset | Pair | Budget | Method | nDCG@10 mean ± seed SD | Recall@100 mean ± seed SD |
|---|---|---|---|---:|---:|
| NanoNQ | minilm_distilroberta | 25pct | procrustes_global | 0.442147 ± 0.038952 | 0.960000 ± 0.023452 |
| NanoNQ | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.488807 ± 0.038594 | 0.970000 ± 0.007071 |
| NanoNQ | minilm_distilroberta | 25pct | tangent1_l10 | 0.473481 ± 0.042969 | 0.970000 ± 0.007071 |
| NanoNQ | minilm_distilroberta | 25pct | tangent2_l1 | 0.500289 ± 0.042228 | 0.968000 ± 0.004472 |
| NanoNQ | minilm_distilroberta | 25pct | tangent2_l100 | 0.452855 ± 0.037871 | 0.970000 ± 0.007071 |
| NanoNQ | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.480723 ± 0.042100 | 0.922000 ± 0.022804 |
| NanoNQ | minilm_distilroberta | 50pct | procrustes_global | 0.499511 ± 0.033637 | 0.954000 ± 0.020736 |
| NanoNQ | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.526624 ± 0.031210 | 0.970000 ± 0.012247 |
| NanoNQ | minilm_distilroberta | 50pct | tangent1_l10 | 0.516667 ± 0.024943 | 0.966000 ± 0.020736 |
| NanoNQ | minilm_distilroberta | 50pct | tangent2_l1 | 0.542874 ± 0.039583 | 0.972000 ± 0.004472 |
| NanoNQ | minilm_distilroberta | 50pct | tangent2_l100 | 0.505990 ± 0.030056 | 0.964000 ± 0.025100 |
| NanoNQ | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.517769 ± 0.042852 | 0.930000 ± 0.023452 |
| NanoNQ | minilm_distilroberta | 75pct | procrustes_global | 0.571429 ± 0.029136 | 0.962000 ± 0.013038 |
| NanoNQ | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.586833 ± 0.022697 | 0.976000 ± 0.008944 |
| NanoNQ | minilm_distilroberta | 75pct | tangent1_l10 | 0.580201 ± 0.027121 | 0.974000 ± 0.013416 |
| NanoNQ | minilm_distilroberta | 75pct | tangent2_l1 | 0.593339 ± 0.028271 | 0.976000 ± 0.008944 |
| NanoNQ | minilm_distilroberta | 75pct | tangent2_l100 | 0.574952 ± 0.028760 | 0.964000 ± 0.015166 |
| NanoNQ | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.585492 ± 0.039399 | 0.948000 ± 0.022804 |
| NanoNQ | minilm_distilroberta | full | full_x | 0.593082 (reference) | 0.940000 (reference) |
| NanoNQ | minilm_distilroberta | full | full_y | 0.678452 (reference) | 0.980000 (reference) |
| NanoNQ | e5_small_base | 25pct | procrustes_global | 0.485237 ± 0.028886 | 0.976000 ± 0.008944 |
| NanoNQ | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.507124 ± 0.027826 | 0.956000 ± 0.021909 |
| NanoNQ | e5_small_base | 25pct | tangent1_l10 | 0.497885 ± 0.026229 | 0.972000 ± 0.010954 |
| NanoNQ | e5_small_base | 25pct | tangent2_l1 | 0.527482 ± 0.026604 | 0.936000 ± 0.021909 |
| NanoNQ | e5_small_base | 25pct | tangent2_l100 | 0.502706 ± 0.026300 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.321913 ± 0.025969 | 0.840000 ± 0.010000 |
| NanoNQ | e5_small_base | 50pct | procrustes_global | 0.513091 ± 0.033191 | 0.968000 ± 0.010954 |
| NanoNQ | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.544348 ± 0.037044 | 0.956000 ± 0.008944 |
| NanoNQ | e5_small_base | 50pct | tangent1_l10 | 0.534751 ± 0.031473 | 0.968000 ± 0.010954 |
| NanoNQ | e5_small_base | 50pct | tangent2_l1 | 0.557761 ± 0.035009 | 0.940000 ± 0.020000 |
| NanoNQ | e5_small_base | 50pct | tangent2_l100 | 0.537096 ± 0.035768 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.387064 ± 0.035056 | 0.780000 ± 0.029155 |
| NanoNQ | e5_small_base | 75pct | procrustes_global | 0.591239 ± 0.025169 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.610099 ± 0.029130 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 75pct | tangent1_l10 | 0.605045 ± 0.028117 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 75pct | tangent2_l1 | 0.617758 ± 0.026396 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 75pct | tangent2_l100 | 0.606239 ± 0.028496 | 0.964000 ± 0.008944 |
| NanoNQ | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.442841 ± 0.028881 | 0.754000 ± 0.041593 |
| NanoNQ | e5_small_base | full | full_x | 0.659510 (reference) | 0.930000 (reference) |
| NanoNQ | e5_small_base | full | full_y | 0.666908 (reference) | 0.960000 (reference) |
| NanoHotpotQA | minilm_distilroberta | 25pct | procrustes_global | 0.336179 ± 0.044108 | 0.808000 ± 0.032711 |
| NanoHotpotQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.375981 ± 0.048065 | 0.806000 ± 0.026077 |
| NanoHotpotQA | minilm_distilroberta | 25pct | tangent1_l10 | 0.371427 ± 0.045448 | 0.804000 ± 0.028810 |
| NanoHotpotQA | minilm_distilroberta | 25pct | tangent2_l1 | 0.373615 ± 0.047165 | 0.796000 ± 0.039749 |
| NanoHotpotQA | minilm_distilroberta | 25pct | tangent2_l100 | 0.361539 ± 0.047608 | 0.806000 ± 0.027019 |
| NanoHotpotQA | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.350533 ± 0.031933 | 0.750000 ± 0.020000 |
| NanoHotpotQA | minilm_distilroberta | 50pct | procrustes_global | 0.410956 ± 0.040583 | 0.824000 ± 0.019494 |
| NanoHotpotQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.443522 ± 0.046847 | 0.830000 ± 0.015811 |
| NanoHotpotQA | minilm_distilroberta | 50pct | tangent1_l10 | 0.434255 ± 0.045812 | 0.828000 ± 0.022804 |
| NanoHotpotQA | minilm_distilroberta | 50pct | tangent2_l1 | 0.444162 ± 0.045469 | 0.826000 ± 0.015166 |
| NanoHotpotQA | minilm_distilroberta | 50pct | tangent2_l100 | 0.430480 ± 0.039982 | 0.828000 ± 0.022804 |
| NanoHotpotQA | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.416879 ± 0.037214 | 0.766000 ± 0.025100 |
| NanoHotpotQA | minilm_distilroberta | 75pct | procrustes_global | 0.478114 ± 0.035229 | 0.842000 ± 0.010954 |
| NanoHotpotQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.493434 ± 0.028084 | 0.844000 ± 0.011402 |
| NanoHotpotQA | minilm_distilroberta | 75pct | tangent1_l10 | 0.491321 ± 0.025360 | 0.842000 ± 0.010954 |
| NanoHotpotQA | minilm_distilroberta | 75pct | tangent2_l1 | 0.499902 ± 0.024025 | 0.842000 ± 0.010954 |
| NanoHotpotQA | minilm_distilroberta | 75pct | tangent2_l100 | 0.489845 ± 0.027629 | 0.842000 ± 0.010954 |
| NanoHotpotQA | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.472982 ± 0.026034 | 0.782000 ± 0.021679 |
| NanoHotpotQA | minilm_distilroberta | full | full_x | 0.600563 (reference) | 0.890000 (reference) |
| NanoHotpotQA | minilm_distilroberta | full | full_y | 0.585935 (reference) | 0.880000 (reference) |
| NanoHotpotQA | e5_small_base | 25pct | procrustes_global | 0.551235 ± 0.031004 | 0.916000 ± 0.023022 |
| NanoHotpotQA | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.584486 ± 0.030010 | 0.914000 ± 0.020736 |
| NanoHotpotQA | e5_small_base | 25pct | tangent1_l10 | 0.579141 ± 0.026965 | 0.918000 ± 0.020494 |
| NanoHotpotQA | e5_small_base | 25pct | tangent2_l1 | 0.555757 ± 0.027769 | 0.908000 ± 0.029496 |
| NanoHotpotQA | e5_small_base | 25pct | tangent2_l100 | 0.588945 ± 0.029346 | 0.918000 ± 0.020494 |
| NanoHotpotQA | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.380443 ± 0.053647 | 0.760000 ± 0.050498 |
| NanoHotpotQA | e5_small_base | 50pct | procrustes_global | 0.629928 ± 0.014138 | 0.936000 ± 0.011402 |
| NanoHotpotQA | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.672240 ± 0.019349 | 0.930000 ± 0.007071 |
| NanoHotpotQA | e5_small_base | 50pct | tangent1_l10 | 0.658131 ± 0.017332 | 0.930000 ± 0.010000 |
| NanoHotpotQA | e5_small_base | 50pct | tangent2_l1 | 0.651983 ± 0.017836 | 0.934000 ± 0.011402 |
| NanoHotpotQA | e5_small_base | 50pct | tangent2_l100 | 0.664060 ± 0.017834 | 0.932000 ± 0.008367 |
| NanoHotpotQA | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.442446 ± 0.026962 | 0.720000 ± 0.043012 |
| NanoHotpotQA | e5_small_base | 75pct | procrustes_global | 0.720207 ± 0.017318 | 0.950000 ± 0.007071 |
| NanoHotpotQA | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.746388 ± 0.014814 | 0.948000 ± 0.008367 |
| NanoHotpotQA | e5_small_base | 75pct | tangent1_l10 | 0.740241 ± 0.014641 | 0.950000 ± 0.010000 |
| NanoHotpotQA | e5_small_base | 75pct | tangent2_l1 | 0.734493 ± 0.028562 | 0.950000 ± 0.007071 |
| NanoHotpotQA | e5_small_base | 75pct | tangent2_l100 | 0.742685 ± 0.014981 | 0.948000 ± 0.008367 |
| NanoHotpotQA | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.505347 ± 0.030573 | 0.674000 ± 0.048785 |
| NanoHotpotQA | e5_small_base | full | full_x | 0.827753 (reference) | 0.950000 (reference) |
| NanoHotpotQA | e5_small_base | full | full_y | 0.819254 (reference) | 0.970000 (reference) |
| NanoFEVER | minilm_distilroberta | 25pct | procrustes_global | 0.507365 ± 0.032030 | 0.926000 ± 0.017385 |
| NanoFEVER | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.545253 ± 0.038295 | 0.932000 ± 0.010435 |
| NanoFEVER | minilm_distilroberta | 25pct | tangent1_l10 | 0.538737 ± 0.032742 | 0.934000 ± 0.017385 |
| NanoFEVER | minilm_distilroberta | 25pct | tangent2_l1 | 0.550630 ± 0.042491 | 0.933333 ± 0.015811 |
| NanoFEVER | minilm_distilroberta | 25pct | tangent2_l100 | 0.523789 ± 0.036861 | 0.924000 ± 0.021654 |
| NanoFEVER | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.494309 ± 0.041365 | 0.870000 ± 0.032489 |
| NanoFEVER | minilm_distilroberta | 50pct | procrustes_global | 0.581358 ± 0.021887 | 0.936000 ± 0.021654 |
| NanoFEVER | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.601114 ± 0.026115 | 0.942000 ± 0.016600 |
| NanoFEVER | minilm_distilroberta | 50pct | tangent1_l10 | 0.594786 ± 0.027424 | 0.934000 ± 0.025210 |
| NanoFEVER | minilm_distilroberta | 50pct | tangent2_l1 | 0.605501 ± 0.034828 | 0.943333 ± 0.024152 |
| NanoFEVER | minilm_distilroberta | 50pct | tangent2_l100 | 0.585631 ± 0.025319 | 0.938000 ± 0.018499 |
| NanoFEVER | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.548820 ± 0.022519 | 0.912000 ± 0.014453 |
| NanoFEVER | minilm_distilroberta | 75pct | procrustes_global | 0.672905 ± 0.020502 | 0.958667 ± 0.020494 |
| NanoFEVER | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.687064 ± 0.021792 | 0.966667 ± 0.016330 |
| NanoFEVER | minilm_distilroberta | 75pct | tangent1_l10 | 0.684410 ± 0.021057 | 0.962667 ± 0.013416 |
| NanoFEVER | minilm_distilroberta | 75pct | tangent2_l1 | 0.685122 ± 0.015021 | 0.966667 ± 0.016330 |
| NanoFEVER | minilm_distilroberta | 75pct | tangent2_l100 | 0.681177 ± 0.027844 | 0.962667 ± 0.013416 |
| NanoFEVER | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.653985 ± 0.008547 | 0.954667 ± 0.010954 |
| NanoFEVER | minilm_distilroberta | full | full_x | 0.825826 (reference) | 0.993333 (reference) |
| NanoFEVER | minilm_distilroberta | full | full_y | 0.749166 (reference) | 0.983333 (reference) |
| NanoFEVER | e5_small_base | 25pct | procrustes_global | 0.714662 ± 0.042561 | 0.987333 ± 0.015706 |
| NanoFEVER | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.755451 ± 0.045413 | 0.982000 ± 0.015384 |
| NanoFEVER | e5_small_base | 25pct | tangent1_l10 | 0.741649 ± 0.045155 | 0.985333 ± 0.017416 |
| NanoFEVER | e5_small_base | 25pct | tangent2_l1 | 0.768404 ± 0.033852 | 0.981333 ± 0.010954 |
| NanoFEVER | e5_small_base | 25pct | tangent2_l100 | 0.746596 ± 0.045189 | 0.984000 ± 0.016228 |
| NanoFEVER | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.644785 ± 0.051288 | 0.926667 ± 0.014530 |
| NanoFEVER | e5_small_base | 50pct | procrustes_global | 0.740210 ± 0.023840 | 0.995333 ± 0.007303 |
| NanoFEVER | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.778950 ± 0.022241 | 0.988667 ± 0.012824 |
| NanoFEVER | e5_small_base | 50pct | tangent1_l10 | 0.765515 ± 0.027915 | 0.992667 ± 0.011643 |
| NanoFEVER | e5_small_base | 50pct | tangent2_l1 | 0.798699 ± 0.009368 | 0.980667 ± 0.015528 |
| NanoFEVER | e5_small_base | 50pct | tangent2_l100 | 0.770051 ± 0.027802 | 0.992667 ± 0.011643 |
| NanoFEVER | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.671094 ± 0.015162 | 0.894667 ± 0.017256 |
| NanoFEVER | e5_small_base | 75pct | procrustes_global | 0.822735 ± 0.029239 | 0.995333 ± 0.007303 |
| NanoFEVER | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.845120 ± 0.025114 | 0.994000 ± 0.005477 |
| NanoFEVER | e5_small_base | 75pct | tangent1_l10 | 0.835692 ± 0.029318 | 0.994667 ± 0.007674 |
| NanoFEVER | e5_small_base | 75pct | tangent2_l1 | 0.857485 ± 0.020600 | 0.990000 ± 0.010274 |
| NanoFEVER | e5_small_base | 75pct | tangent2_l100 | 0.838967 ± 0.026537 | 0.992667 ± 0.007226 |
| NanoFEVER | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.728986 ± 0.008075 | 0.866667 ± 0.012247 |
| NanoFEVER | e5_small_base | full | full_x | 0.898353 (reference) | 0.990000 (reference) |
| NanoFEVER | e5_small_base | full | full_y | 0.896329 (reference) | 1.000000 (reference) |
| FiQA | minilm_distilroberta | 25pct | procrustes_global | 0.256997 ± 0.006146 | 0.657992 ± 0.003162 |
| FiQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 | 0.287119 ± 0.005761 | 0.665014 ± 0.003963 |
| FiQA | minilm_distilroberta | 25pct | tangent1_l10 | 0.278498 ± 0.006179 | 0.663462 ± 0.006783 |
| FiQA | minilm_distilroberta | 25pct | tangent2_l1 | 0.296096 ± 0.005755 | 0.662389 ± 0.003341 |
| FiQA | minilm_distilroberta | 25pct | tangent2_l100 | 0.269626 ± 0.005321 | 0.661684 ± 0.003682 |
| FiQA | minilm_distilroberta | 25pct | ridge_affine_l10_bias_regularized | 0.247637 ± 0.005974 | 0.620122 ± 0.006011 |
| FiQA | minilm_distilroberta | 50pct | procrustes_global | 0.285828 ± 0.004024 | 0.668792 ± 0.005208 |
| FiQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 | 0.307505 ± 0.006017 | 0.676569 ± 0.001741 |
| FiQA | minilm_distilroberta | 50pct | tangent1_l10 | 0.300349 ± 0.006080 | 0.675085 ± 0.003914 |
| FiQA | minilm_distilroberta | 50pct | tangent2_l1 | 0.316744 ± 0.005406 | 0.675631 ± 0.003129 |
| FiQA | minilm_distilroberta | 50pct | tangent2_l100 | 0.294721 ± 0.004917 | 0.673491 ± 0.006916 |
| FiQA | minilm_distilroberta | 50pct | ridge_affine_l10_bias_regularized | 0.289045 ± 0.005862 | 0.637377 ± 0.001793 |
| FiQA | minilm_distilroberta | 75pct | procrustes_global | 0.341744 ± 0.001793 | 0.683156 ± 0.004849 |
| FiQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 | 0.350072 ± 0.002395 | 0.688481 ± 0.003513 |
| FiQA | minilm_distilroberta | 75pct | tangent1_l10 | 0.347212 ± 0.002306 | 0.688321 ± 0.002328 |
| FiQA | minilm_distilroberta | 75pct | tangent2_l1 | 0.354680 ± 0.002774 | 0.686445 ± 0.003220 |
| FiQA | minilm_distilroberta | 75pct | tangent2_l100 | 0.344491 ± 0.001069 | 0.686066 ± 0.003976 |
| FiQA | minilm_distilroberta | 75pct | ridge_affine_l10_bias_regularized | 0.343745 ± 0.002736 | 0.663087 ± 0.001598 |
| FiQA | minilm_distilroberta | full | full_x | 0.389961 (reference) | 0.700184 (reference) |
| FiQA | minilm_distilroberta | full | full_y | 0.404736 (reference) | 0.703892 (reference) |
| FiQA | e5_small_base | 25pct | procrustes_global | 0.271778 ± 0.001281 | 0.602775 ± 0.007259 |
| FiQA | e5_small_base | 25pct | arc2_global_tangent2_r1 | 0.273107 ± 0.004827 | 0.599738 ± 0.009300 |
| FiQA | e5_small_base | 25pct | tangent1_l10 | 0.273016 ± 0.003176 | 0.599144 ± 0.007227 |
| FiQA | e5_small_base | 25pct | tangent2_l1 | 0.272330 ± 0.004288 | 0.593976 ± 0.014687 |
| FiQA | e5_small_base | 25pct | tangent2_l100 | 0.273246 ± 0.002712 | 0.597026 ± 0.005516 |
| FiQA | e5_small_base | 25pct | ridge_affine_l10_bias_regularized | 0.128054 ± 0.003612 | 0.333045 ± 0.007519 |
| FiQA | e5_small_base | 50pct | procrustes_global | 0.310036 ± 0.002542 | 0.637429 ± 0.006658 |
| FiQA | e5_small_base | 50pct | arc2_global_tangent2_r1 | 0.311635 ± 0.003373 | 0.620925 ± 0.008032 |
| FiQA | e5_small_base | 50pct | tangent1_l10 | 0.311639 ± 0.002293 | 0.627096 ± 0.007136 |
| FiQA | e5_small_base | 50pct | tangent2_l1 | 0.302536 ± 0.004411 | 0.617130 ± 0.014016 |
| FiQA | e5_small_base | 50pct | tangent2_l100 | 0.312260 ± 0.002799 | 0.623952 ± 0.006537 |
| FiQA | e5_small_base | 50pct | ridge_affine_l10_bias_regularized | 0.147922 ± 0.004371 | 0.305270 ± 0.006730 |
| FiQA | e5_small_base | 75pct | procrustes_global | 0.340768 ± 0.001368 | 0.677585 ± 0.001652 |
| FiQA | e5_small_base | 75pct | arc2_global_tangent2_r1 | 0.337185 ± 0.002324 | 0.660609 ± 0.004347 |
| FiQA | e5_small_base | 75pct | tangent1_l10 | 0.339243 ± 0.002737 | 0.668440 ± 0.005238 |
| FiQA | e5_small_base | 75pct | tangent2_l1 | 0.328560 ± 0.003972 | 0.642345 ± 0.005310 |
| FiQA | e5_small_base | 75pct | tangent2_l100 | 0.339387 ± 0.002674 | 0.664083 ± 0.006569 |
| FiQA | e5_small_base | 75pct | ridge_affine_l10_bias_regularized | 0.160971 ± 0.003197 | 0.249477 ± 0.003220 |
| FiQA | e5_small_base | full | full_x | 0.346478 (reference) | 0.645332 (reference) |
| FiQA | e5_small_base | full | full_y | 0.389133 (reference) | 0.696797 (reference) |

Paired nominal 95% intervals use 20,000 query bootstrap draws after five-seed averaging. The same indices are reused within a dataset for every method, encoder and budget. These intervals are descriptive and marginal; an interval touching/crossing zero is unresolved, never equivalence. Mapping-seed SD/range are separate in JSON and do not create independent queries.

| Dataset / aggregate | Pair | Budget | Contrast (left − right) | Δ nDCG@10 [95% CI] | Δ Recall@100 [95% CI] |
|---|---|---|---|---:|---:|
| NanoNQ | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.046659 [+0.029852, +0.064881] | +0.010000 [+0.000000, +0.022000] |
| NanoNQ | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.015326 [+0.007426, +0.024493] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.008084 [-0.018180, +0.034516] | +0.048000 [+0.010000, +0.100000] |
| NanoNQ | minilm_distilroberta | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.011483 [+0.001181, +0.021818] | -0.002000 [-0.006000, +0.000000] |
| NanoNQ | minilm_distilroberta | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.035952 [-0.051362, -0.021845] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.027114 [+0.015109, +0.040071] | +0.016000 [+0.000000, +0.044000] |
| NanoNQ | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.009958 [+0.004479, +0.016527] | +0.004000 [+0.000000, +0.012000] |
| NanoNQ | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.008855 [-0.013899, +0.032898] | +0.040000 [+0.000000, +0.096000] |
| NanoNQ | minilm_distilroberta | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.016249 [+0.005294, +0.028512] | +0.002000 [-0.006000, +0.012000] |
| NanoNQ | minilm_distilroberta | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.020634 [-0.032001, -0.010459] | -0.006000 [-0.016000, +0.000000] |
| NanoNQ | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.015404 [+0.004990, +0.028970] | +0.014000 [+0.000000, +0.036000] |
| NanoNQ | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.006632 [+0.001483, +0.013773] | +0.002000 [+0.000000, +0.006000] |
| NanoNQ | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.001340 [-0.019134, +0.021471] | +0.028000 [-0.004000, +0.072000] |
| NanoNQ | minilm_distilroberta | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.006506 [-0.000494, +0.013926] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | minilm_distilroberta | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.011881 [-0.024982, -0.002069] | -0.012000 [-0.032000, +0.000000] |
| NanoNQ | e5_small_base | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.021887 [+0.004558, +0.039297] | -0.020000 [-0.048000, +0.000000] |
| NanoNQ | e5_small_base | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.009238 [+0.000596, +0.018515] | -0.016000 [-0.036000, +0.000000] |
| NanoNQ | e5_small_base | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.185210 [+0.120397, +0.255492] | +0.116000 [+0.058000, +0.184000] |
| NanoNQ | e5_small_base | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.020358 [+0.005120, +0.037319] | -0.020000 [-0.044000, +0.000000] |
| NanoNQ | e5_small_base | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.004417 [-0.013190, +0.003684] | +0.008000 [+0.000000, +0.020000] |
| NanoNQ | e5_small_base | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.031258 [+0.014208, +0.049145] | -0.012000 [-0.036000, +0.000000] |
| NanoNQ | e5_small_base | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.009598 [+0.001217, +0.018235] | -0.012000 [-0.036000, +0.000000] |
| NanoNQ | e5_small_base | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.157284 [+0.096256, +0.224007] | +0.176000 [+0.102000, +0.256000] |
| NanoNQ | e5_small_base | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.013413 [-0.002354, +0.029542] | -0.016000 [-0.036000, +0.000000] |
| NanoNQ | e5_small_base | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.007252 [-0.015782, +0.000889] | +0.008000 [+0.000000, +0.024000] |
| NanoNQ | e5_small_base | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.018860 [+0.005932, +0.032919] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | e5_small_base | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.005055 [-0.003650, +0.014042] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | e5_small_base | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.167258 [+0.088444, +0.255237] | +0.210000 [+0.116000, +0.312000] |
| NanoNQ | e5_small_base | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.007659 [-0.006496, +0.021438] | +0.000000 [+0.000000, +0.000000] |
| NanoNQ | e5_small_base | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.003860 [-0.011537, +0.003497] | +0.000000 [+0.000000, +0.000000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.039802 [+0.023172, +0.056838] | -0.002000 [-0.022000, +0.014000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.004554 [-0.002185, +0.011429] | +0.002000 [-0.004000, +0.008000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.025448 [-0.007157, +0.057082] | +0.056000 [+0.020000, +0.096000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.002366 [-0.017679, +0.012407] | -0.010000 [-0.024000, +0.002000] |
| NanoHotpotQA | minilm_distilroberta | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.014442 [-0.025314, -0.003660] | +0.000000 [-0.008000, +0.010000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.032566 [+0.016406, +0.048913] | +0.006000 [-0.016000, +0.026000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.009266 [+0.001270, +0.018101] | +0.002000 [-0.004000, +0.008000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.026642 [-0.005710, +0.060337] | +0.064000 [+0.020000, +0.116000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.000640 [-0.011244, +0.012779] | -0.004000 [-0.012000, +0.004000] |
| NanoHotpotQA | minilm_distilroberta | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.013042 [-0.024161, -0.001947] | -0.002000 [-0.012000, +0.010000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.015320 [+0.003177, +0.027498] | +0.002000 [-0.020000, +0.018000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.002113 [-0.003404, +0.007460] | +0.002000 [+0.000000, +0.006000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.020452 [-0.005892, +0.049767] | +0.062000 [+0.014000, +0.118000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.006467 [-0.000415, +0.014088] | -0.002000 [-0.006000, +0.000000] |
| NanoHotpotQA | minilm_distilroberta | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.003589 [-0.011033, +0.003715] | -0.002000 [-0.014000, +0.010000] |
| NanoHotpotQA | e5_small_base | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.033251 [+0.009799, +0.053406] | -0.002000 [-0.016000, +0.010000] |
| NanoHotpotQA | e5_small_base | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.005345 [-0.009926, +0.018435] | -0.004000 [-0.010000, +0.000000] |
| NanoHotpotQA | e5_small_base | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.204042 [+0.147093, +0.264344] | +0.154000 [+0.104000, +0.208000] |
| NanoHotpotQA | e5_small_base | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.028729 [-0.049446, -0.009277] | -0.006000 [-0.022000, +0.012000] |
| NanoHotpotQA | e5_small_base | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | +0.004459 [-0.007826, +0.018297] | +0.004000 [+0.000000, +0.010000] |
| NanoHotpotQA | e5_small_base | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.042311 [+0.021027, +0.062996] | -0.006000 [-0.026000, +0.008000] |
| NanoHotpotQA | e5_small_base | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.014109 [+0.000938, +0.025931] | +0.000000 [-0.006000, +0.006000] |
| NanoHotpotQA | e5_small_base | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.229793 [+0.168401, +0.295326] | +0.210000 [+0.150000, +0.272000] |
| NanoHotpotQA | e5_small_base | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.020257 [-0.039573, -0.002879] | +0.004000 [-0.004000, +0.012000] |
| NanoHotpotQA | e5_small_base | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.008180 [-0.019060, +0.003061] | +0.002000 [-0.004000, +0.010000] |
| NanoHotpotQA | e5_small_base | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.026180 [+0.008167, +0.044578] | -0.002000 [-0.018000, +0.010000] |
| NanoHotpotQA | e5_small_base | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.006147 [-0.002711, +0.014200] | -0.002000 [-0.006000, +0.000000] |
| NanoHotpotQA | e5_small_base | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.241041 [+0.170263, +0.317266] | +0.274000 [+0.198000, +0.354000] |
| NanoHotpotQA | e5_small_base | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.011895 [-0.029312, +0.003648] | +0.002000 [+0.000000, +0.006000] |
| NanoHotpotQA | e5_small_base | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.003702 [-0.009432, +0.002023] | +0.000000 [+0.000000, +0.000000] |
| NanoFEVER | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.037888 [+0.017574, +0.060544] | +0.006000 [-0.012000, +0.024000] |
| NanoFEVER | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.006516 [-0.004255, +0.016637] | -0.002000 [-0.014000, +0.010000] |
| NanoFEVER | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.050943 [+0.025293, +0.077037] | +0.062000 [+0.022000, +0.112000] |
| NanoFEVER | minilm_distilroberta | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.005377 [-0.006654, +0.017947] | +0.001333 [-0.018667, +0.025333] |
| NanoFEVER | minilm_distilroberta | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.021464 [-0.039116, -0.004469] | -0.008000 [-0.024000, +0.008000] |
| NanoFEVER | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.019756 [+0.006924, +0.033807] | +0.006000 [-0.012000, +0.024000] |
| NanoFEVER | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.006328 [-0.000455, +0.014403] | +0.008000 [+0.000000, +0.020000] |
| NanoFEVER | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.052295 [+0.027428, +0.078295] | +0.030000 [+0.000000, +0.068000] |
| NanoFEVER | minilm_distilroberta | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.004387 [-0.002960, +0.012209] | +0.001333 [-0.018667, +0.024667] |
| NanoFEVER | minilm_distilroberta | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.015484 [-0.027427, -0.004824] | -0.004000 [-0.012000, +0.000000] |
| NanoFEVER | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.014159 [-0.000868, +0.030990] | +0.008000 [+0.000000, +0.020000] |
| NanoFEVER | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.002654 [-0.002513, +0.008358] | +0.004000 [+0.000000, +0.012000] |
| NanoFEVER | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.033079 [+0.012201, +0.055590] | +0.012000 [-0.004000, +0.038000] |
| NanoFEVER | minilm_distilroberta | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.001942 [-0.006699, +0.002289] | +0.000000 [+0.000000, +0.000000] |
| NanoFEVER | minilm_distilroberta | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.005887 [-0.017063, +0.004917] | -0.004000 [-0.012000, +0.000000] |
| NanoFEVER | e5_small_base | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.040790 [+0.024334, +0.059433] | -0.005333 [-0.012000, +0.000000] |
| NanoFEVER | e5_small_base | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.013802 [+0.006795, +0.021753] | -0.003333 [-0.008667, +0.000000] |
| NanoFEVER | e5_small_base | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.110667 [+0.061163, +0.162680] | +0.055333 [+0.013333, +0.111333] |
| NanoFEVER | e5_small_base | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.012953 [-0.003826, +0.030210] | -0.000667 [-0.010667, +0.007333] |
| NanoFEVER | e5_small_base | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.008855 [-0.016334, -0.002485] | +0.002000 [+0.000000, +0.006000] |
| NanoFEVER | e5_small_base | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.038740 [+0.023113, +0.055308] | -0.006667 [-0.017333, +0.000000] |
| NanoFEVER | e5_small_base | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.013435 [+0.003777, +0.023990] | -0.004000 [-0.012000, +0.000000] |
| NanoFEVER | e5_small_base | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.107856 [+0.052348, +0.168989] | +0.094000 [+0.032000, +0.168000] |
| NanoFEVER | e5_small_base | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.019749 [+0.005976, +0.034907] | -0.008000 [-0.024000, +0.000000] |
| NanoFEVER | e5_small_base | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.008899 [-0.018333, -0.000971] | +0.004000 [+0.000000, +0.012000] |
| NanoFEVER | e5_small_base | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.022385 [+0.007854, +0.038203] | -0.001333 [-0.016000, +0.010000] |
| NanoFEVER | e5_small_base | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.009428 [+0.001629, +0.018497] | -0.000667 [-0.006000, +0.004000] |
| NanoFEVER | e5_small_base | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.116134 [+0.043332, +0.197382] | +0.127333 [+0.052000, +0.213333] |
| NanoFEVER | e5_small_base | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.012365 [+0.003083, +0.022867] | -0.004000 [-0.012000, +0.000000] |
| NanoFEVER | e5_small_base | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.006154 [-0.013855, -0.000544] | -0.001333 [-0.004000, +0.000000] |
| FiQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.030123 [+0.024368, +0.036101] | +0.007022 [-0.000159, +0.014235] |
| FiQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.008622 [+0.006392, +0.011119] | +0.001552 [-0.002270, +0.005320] |
| FiQA | minilm_distilroberta | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.039483 [+0.028077, +0.051386] | +0.044893 [+0.030367, +0.059963] |
| FiQA | minilm_distilroberta | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.008976 [+0.005716, +0.012375] | -0.002625 [-0.007955, +0.002514] |
| FiQA | minilm_distilroberta | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.017494 [-0.021190, -0.014003] | -0.003330 [-0.008328, +0.001773] |
| FiQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.021677 [+0.016809, +0.026952] | +0.007778 [-0.000619, +0.015941] |
| FiQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.007156 [+0.005311, +0.009194] | +0.001484 [-0.002246, +0.005042] |
| FiQA | minilm_distilroberta | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.018459 [+0.010175, +0.026919] | +0.039193 [+0.023457, +0.055710] |
| FiQA | minilm_distilroberta | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.009239 [+0.006311, +0.012307] | -0.000938 [-0.005907, +0.003989] |
| FiQA | minilm_distilroberta | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.012783 [-0.016089, -0.009721] | -0.003078 [-0.008382, +0.002481] |
| FiQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − procrustes_global | +0.008328 [+0.004817, +0.012344] | +0.005325 [-0.001974, +0.012391] |
| FiQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.002861 [+0.001552, +0.004256] | +0.000160 [-0.002377, +0.002667] |
| FiQA | minilm_distilroberta | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.006328 [-0.000015, +0.012665] | +0.025394 [+0.012275, +0.039401] |
| FiQA | minilm_distilroberta | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | +0.004608 [+0.002880, +0.006428] | -0.002036 [-0.006731, +0.002227] |
| FiQA | minilm_distilroberta | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | -0.005582 [-0.008205, -0.003139] | -0.002415 [-0.006573, +0.001659] |
| FiQA | e5_small_base | 25pct | arc2_global_tangent2_r1 − procrustes_global | +0.001329 [-0.004086, +0.006684] | -0.003037 [-0.012592, +0.005627] |
| FiQA | e5_small_base | 25pct | arc2_global_tangent2_r1 − tangent1_l10 | +0.000091 [-0.002748, +0.002763] | +0.000594 [-0.003549, +0.004847] |
| FiQA | e5_small_base | 25pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.145052 [+0.122177, +0.168496] | +0.266693 [+0.235355, +0.298002] |
| FiQA | e5_small_base | 25pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.000777 [-0.006812, +0.005138] | -0.005762 [-0.015214, +0.003091] |
| FiQA | e5_small_base | 25pct | tangent2_l100 − arc2_global_tangent2_r1 | +0.000139 [-0.002761, +0.003060] | -0.002712 [-0.007273, +0.001778] |
| FiQA | e5_small_base | 50pct | arc2_global_tangent2_r1 − procrustes_global | +0.001599 [-0.004119, +0.007264] | -0.016505 [-0.029270, -0.004880] |
| FiQA | e5_small_base | 50pct | arc2_global_tangent2_r1 − tangent1_l10 | -0.000004 [-0.003084, +0.002977] | -0.006171 [-0.013776, +0.000415] |
| FiQA | e5_small_base | 50pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.163714 [+0.139400, +0.188445] | +0.315655 [+0.283380, +0.348220] |
| FiQA | e5_small_base | 50pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.009099 [-0.015660, -0.002714] | -0.003795 [-0.011347, +0.003888] |
| FiQA | e5_small_base | 50pct | tangent2_l100 − arc2_global_tangent2_r1 | +0.000625 [-0.002110, +0.003434] | +0.003028 [-0.001684, +0.007871] |
| FiQA | e5_small_base | 75pct | arc2_global_tangent2_r1 − procrustes_global | -0.003583 [-0.009513, +0.002247] | -0.016976 [-0.028318, -0.006277] |
| FiQA | e5_small_base | 75pct | arc2_global_tangent2_r1 − tangent1_l10 | -0.002058 [-0.005128, +0.000894] | -0.007831 [-0.014554, -0.001302] |
| FiQA | e5_small_base | 75pct | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.176214 [+0.151233, +0.201775] | +0.411132 [+0.376014, +0.446305] |
| FiQA | e5_small_base | 75pct | tangent2_l1 − arc2_global_tangent2_r1 | -0.008626 [-0.013383, -0.003987] | -0.018264 [-0.028816, -0.008875] |
| FiQA | e5_small_base | 75pct | tangent2_l100 − arc2_global_tangent2_r1 | +0.002202 [-0.000299, +0.004791] | +0.003474 [-0.001622, +0.008326] |
| minilm_distilroberta | minilm_distilroberta | equal-stratum macro | arc2_global_tangent2_r1 − procrustes_global | +0.025733 [+0.020161, +0.031751] | +0.007177 [-0.000071, +0.014700] |
| minilm_distilroberta | minilm_distilroberta | equal-stratum macro | arc2_global_tangent2_r1 − tangent1_l10 | +0.006832 [+0.004414, +0.009364] | +0.002100 [-0.000140, +0.004525] |
| minilm_distilroberta | minilm_distilroberta | equal-stratum macro | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.024284 [+0.014025, +0.034508] | +0.042623 [+0.026934, +0.060208] |
| minilm_distilroberta | minilm_distilroberta | equal-stratum macro | tangent2_l1 − arc2_global_tangent2_r1 | +0.005802 [+0.001967, +0.009557] | -0.001578 [-0.005474, +0.002693] |
| minilm_distilroberta | minilm_distilroberta | equal-stratum macro | tangent2_l100 − arc2_global_tangent2_r1 | -0.014853 [-0.019389, -0.010576] | -0.003902 [-0.008073, -0.000128] |
| e5_small_base | e5_small_base | equal-stratum macro | arc2_global_tangent2_r1 − procrustes_global | +0.022917 [+0.016366, +0.029493] | -0.007654 [-0.014072, -0.002479] |
| e5_small_base | e5_small_base | equal-stratum macro | arc2_global_tangent2_r1 − tangent1_l10 | +0.007016 [+0.003288, +0.010548] | -0.004617 [-0.008774, -0.001672] |
| e5_small_base | e5_small_base | equal-stratum macro | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.167022 [+0.140561, +0.194920] | +0.200846 [+0.173120, +0.230346] |
| e5_small_base | e5_small_base | equal-stratum macro | tangent2_l1 − arc2_global_tangent2_r1 | +0.000593 [-0.005584, +0.006643] | -0.006374 [-0.011160, -0.002234] |
| e5_small_base | e5_small_base | equal-stratum macro | tangent2_l100 − arc2_global_tangent2_r1 | -0.003658 [-0.006768, -0.000457] | +0.002538 [+0.000684, +0.004709] |
| overall | overall | equal-stratum macro | arc2_global_tangent2_r1 − procrustes_global | +0.024325 [+0.019582, +0.029318] | -0.000239 [-0.004979, +0.004306] |
| overall | overall | equal-stratum macro | arc2_global_tangent2_r1 − tangent1_l10 | +0.006924 [+0.004584, +0.009226] | -0.001259 [-0.003620, +0.000648] |
| overall | overall | equal-stratum macro | arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.095653 [+0.080325, +0.111535] | +0.121734 [+0.103203, +0.141605] |
| overall | overall | equal-stratum macro | tangent2_l1 − arc2_global_tangent2_r1 | +0.003197 [-0.000740, +0.007158] | -0.003976 [-0.007255, -0.000820] |
| overall | overall | equal-stratum macro | tangent2_l100 − arc2_global_tangent2_r1 | -0.009255 [-0.012286, -0.006335] | -0.000682 [-0.002814, +0.001361] |

Only the five predeclared overall 24-stratum nDCG contrasts form a family. Their 99% percentile intervals use Bonferroni allocation for nominal 95% family coverage. They remain DEV estimates; percentile-bootstrap coverage is approximate. Per-encoder and Recall intervals are outside this family.

| Overall contrast | Δ nDCG@10 [99% interval, five-contrast family] |
|---|---:|
| arc2_global_tangent2_r1 − procrustes_global | +0.024325 [+0.018015, +0.031021] |
| arc2_global_tangent2_r1 − tangent1_l10 | +0.006924 [+0.003809, +0.009959] |
| arc2_global_tangent2_r1 − ridge_affine_l10_bias_regularized | +0.095653 [+0.075353, +0.116631] |
| tangent2_l1 − arc2_global_tangent2_r1 | +0.003197 [-0.001890, +0.008304] |
| tangent2_l100 − arc2_global_tangent2_r1 | -0.009255 [-0.013214, -0.005510] |

No scientifically justified quality/noninferiority margin is declared. This report performs no equivalence test, method selection or automatic next-stage admission. B1-P/B1-G remain necessary for the later development decision.
