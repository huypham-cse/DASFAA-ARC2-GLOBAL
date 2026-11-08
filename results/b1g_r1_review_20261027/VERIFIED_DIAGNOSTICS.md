# B1-G local verification and descriptive extraction

Verified 210 pristine galleries, 450 mixed cases and 90 five-seed conditions.

All mixed per-query metrics match the five frozen historical metric files by dataset, ranking hash and query order. Means, signed after-minus-before deltas, seed SD/ranges and all saved ranking/paired diagnostics were recomputed. No qrels, remote inputs, new fits or new inferential statistics were used.

This is computational consistency QA of inspected DEV evidence. It is not independent label validation or a formal paper-claim audit. Paid-share imbalance alone is not proof of miscalibration; paired score error remains descriptive.

| Dataset | Pair | Method | Regime | Budget | nDCG before | after | delta | Recall delta |
|---|---|---|---|---|---:|---:|---:|---:|
| FiQA | e5_small_base | arc2_global_tangent2_r1 | allpaid28819 | 50pct | 0.31490775 | 0.29186698 | -0.02304077 | -0.09467432 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24121966 | 0.27310684 | +0.03188718 | +0.02565597 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.24121966 | 0.31163521 | +0.07041554 | +0.04684244 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.24121966 | 0.33718532 | +0.09596565 | +0.08652702 |
| FiQA | e5_small_base | embedding_converter_paper_spec | allpaid28819 | 50pct | 0.15865061 | 0.26251946 | +0.10386885 | +0.09327375 |
| FiQA | e5_small_base | embedding_converter_paper_spec | fixed1024 | 50pct | 0.04180985 | 0.13966537 | +0.09785552 | +0.10438456 |
| FiQA | e5_small_base | la2m20_integration_script_adaptation | allpaid28819 | 50pct | 0.29891812 | 0.32934130 | +0.03042318 | +0.01358119 |
| FiQA | e5_small_base | la2m20_integration_script_adaptation | fixed1024 | 50pct | 0.04700906 | 0.22999032 | +0.18298126 | +0.21962619 |
| FiQA | e5_small_base | procrustes_global | allpaid28819 | 50pct | 0.28609600 | 0.33620246 | +0.05010646 | +0.04799219 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.23577734 | 0.27177804 | +0.03600070 | +0.03939082 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.23577734 | 0.31003589 | +0.07425856 | +0.07404463 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.23577734 | 0.34076801 | +0.10499067 | +0.11420081 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | allpaid28819 | 50pct | 0.27058501 | 0.22701458 | -0.04357043 | -0.17792535 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.10158416 | 0.12805447 | +0.02647031 | -0.02821889 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.10158416 | 0.14792157 | +0.04633741 | -0.05599408 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.10158416 | 0.16097149 | +0.05938733 | -0.11178721 |
| FiQA | e5_small_base | simplelinear_official_final50_mlp5 | allpaid28819 | 50pct | 0.11597835 | 0.16794941 | +0.05197106 | -0.02575802 |
| FiQA | e5_small_base | simplelinear_official_final50_mlp5 | fixed1024 | 50pct | 0.00127043 | 0.19416743 | +0.19289700 | +0.24847948 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | allpaid28819 | 50pct | 0.35095074 | 0.36714602 | +0.01619529 | +0.01172649 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.31044544 | 0.28711945 | -0.02332599 | +0.01166456 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.31044544 | 0.30750486 | -0.00294058 | +0.02321940 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.31044544 | 0.35007223 | +0.03962679 | +0.03513099 |
| FiQA | minilm_distilroberta | embedding_converter_paper_spec | allpaid28819 | 50pct | 0.28271603 | 0.32576144 | +0.04304541 | +0.01775662 |
| FiQA | minilm_distilroberta | embedding_converter_paper_spec | fixed1024 | 50pct | 0.09576155 | 0.24963648 | +0.15387493 | +0.13455271 |
| FiQA | minilm_distilroberta | la2m20_integration_script_adaptation | allpaid28819 | 50pct | 0.35064303 | 0.33892347 | -0.01171957 | -0.00512849 |
| FiQA | minilm_distilroberta | la2m20_integration_script_adaptation | fixed1024 | 50pct | 0.08085071 | 0.23767401 | +0.15682331 | +0.07923920 |
| FiQA | minilm_distilroberta | procrustes_global | allpaid28819 | 50pct | 0.34955887 | 0.33338647 | -0.01617239 | +0.00569628 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.30388301 | 0.25699670 | -0.04688631 | +0.00531721 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.30388301 | 0.28582824 | -0.01805477 | +0.01611691 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.30388301 | 0.34174406 | +0.03786105 | +0.03048105 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | allpaid28819 | 50pct | 0.34222250 | 0.36726328 | +0.02504077 | +0.00908172 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.26049267 | 0.24763689 | -0.01285578 | +0.02011540 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.26049267 | 0.28904546 | +0.02855278 | +0.03737025 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.26049267 | 0.34374457 | +0.08325190 | +0.06308065 |
| FiQA | minilm_distilroberta | simplelinear_official_final50_mlp5 | allpaid28819 | 50pct | 0.30711973 | 0.33231625 | +0.02519651 | +0.02828932 |
| FiQA | minilm_distilroberta | simplelinear_official_final50_mlp5 | fixed1024 | 50pct | 0.09701478 | 0.23595312 | +0.13893834 | +0.02901470 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.74315082 | 0.75545127 | +0.01230046 | -0.00200000 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.74315082 | 0.77894994 | +0.03579912 | +0.00466667 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74315082 | 0.84512017 | +0.10196935 | +0.01000000 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.74619924 | 0.71466167 | -0.03153757 | +0.00133333 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.74619924 | 0.74020974 | -0.00598950 | +0.00933333 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.74619924 | 0.82273549 | +0.07653625 | +0.00933333 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.61096297 | 0.64478468 | +0.03382171 | -0.02666667 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.61096297 | 0.67109381 | +0.06013083 | -0.05866667 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.61096297 | 0.72898601 | +0.11802304 | -0.08666667 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.54160497 | 0.54525280 | +0.00364783 | +0.02333333 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.54160497 | 0.60111412 | +0.05950915 | +0.03333333 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.54160497 | 0.68706384 | +0.14545887 | +0.05800000 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.53053811 | 0.50736477 | -0.02317334 | -0.00266667 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.53053811 | 0.58135767 | +0.05081956 | +0.00733333 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.53053811 | 0.67290499 | +0.14236688 | +0.03000000 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.43898389 | 0.49430945 | +0.05532556 | +0.03133333 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.43898389 | 0.54881962 | +0.10983573 | +0.07333333 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.43898389 | 0.65398488 | +0.21500099 | +0.11600000 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.53140457 | 0.58448566 | +0.05308109 | +0.01200000 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.53140457 | 0.67223953 | +0.14083496 | +0.02800000 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.53140457 | 0.74638760 | +0.21498303 | +0.04600000 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.53726826 | 0.55123462 | +0.01396635 | +0.01200000 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.53726826 | 0.62992807 | +0.09265981 | +0.03200000 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.53726826 | 0.72020712 | +0.18293886 | +0.04600000 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.36173761 | 0.38044345 | +0.01870584 | -0.08800000 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.36173761 | 0.44244608 | +0.08070847 | -0.12800000 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.36173761 | 0.50534701 | +0.14360940 | -0.17400000 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.34454211 | 0.37598069 | +0.03143858 | +0.01400000 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.34454211 | 0.44352167 | +0.09897955 | +0.03800000 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.34454211 | 0.49343446 | +0.14889234 | +0.05200000 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.33902489 | 0.33617899 | -0.00284590 | +0.02000000 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.33902489 | 0.41095595 | +0.07193106 | +0.03600000 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.33902489 | 0.47811448 | +0.13908959 | +0.05400000 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.30796422 | 0.35053302 | +0.04256880 | -0.01400000 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.30796422 | 0.41687929 | +0.10891507 | +0.00200000 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.30796422 | 0.47298218 | +0.16501797 | +0.01800000 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.49364597 | 0.50712368 | +0.01347772 | -0.02400000 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.49364597 | 0.54434822 | +0.05070226 | -0.02400000 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.49364597 | 0.61009940 | +0.11645343 | -0.01600000 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.49292882 | 0.48523705 | -0.00769177 | +0.00000000 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.49292882 | 0.51309058 | +0.02016177 | -0.00800000 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.49292882 | 0.59123919 | +0.09831037 | -0.01200000 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.28203354 | 0.32191350 | +0.03987996 | -0.03600000 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.28203354 | 0.38706437 | +0.10503083 | -0.09600000 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.28203354 | 0.44284100 | +0.16080746 | -0.12200000 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.52025266 | 0.48880674 | -0.03144591 | +0.00400000 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.52025266 | 0.52662434 | +0.00637168 | +0.00400000 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.52025266 | 0.58683260 | +0.06657994 | +0.01000000 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.50242163 | 0.44214747 | -0.06027416 | -0.00400000 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.50242163 | 0.49951053 | -0.00291109 | -0.01000000 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.50242163 | 0.57142874 | +0.06900711 | -0.00200000 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.50210572 | 0.48072307 | -0.02138265 | -0.02200000 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50210572 | 0.51776948 | +0.01566376 | -0.01400000 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.50210572 | 0.58549214 | +0.08338642 | +0.00400000 |

| Dataset | Pair | Method | Regime | Budget | Paid population | Paid top10 before | after | Paired bias all | unpaid |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| FiQA | e5_small_base | arc2_global_tangent2_r1 | allpaid28819 | 50pct | 0.50000000 | 0.49164000 | 0.06472000 | +0.04065427 | +0.03968433 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24999133 | 0.25916000 | 0.16684000 | +0.02533477 | +0.02470172 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.50000000 | 0.49856000 | 0.33356000 | +0.02533477 | +0.02437462 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74999133 | 0.75060000 | 0.54852000 | +0.02533477 | +0.02421023 |
| FiQA | e5_small_base | embedding_converter_paper_spec | allpaid28819 | 50pct | 0.50000000 | 0.45508000 | 0.46220000 | +0.00143121 | +0.00154876 |
| FiQA | e5_small_base | embedding_converter_paper_spec | fixed1024 | 50pct | 0.50000000 | 0.48924000 | 0.08496000 | +0.04816986 | +0.04772362 |
| FiQA | e5_small_base | la2m20_integration_script_adaptation | allpaid28819 | 50pct | 0.50000000 | 0.56304000 | 0.31960000 | +0.01687780 | +0.01604844 |
| FiQA | e5_small_base | la2m20_integration_script_adaptation | fixed1024 | 50pct | 0.50000000 | 0.63912000 | 0.88332000 | +0.01425492 | +0.01311142 |
| FiQA | e5_small_base | procrustes_global | allpaid28819 | 50pct | 0.50000000 | 0.49748000 | 0.37072000 | +0.01822939 | +0.01742939 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.24999133 | 0.25880000 | 0.27288000 | +0.01826877 | +0.01767187 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.50000000 | 0.49760000 | 0.49916000 | +0.01826877 | +0.01744362 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.74999133 | 0.74868000 | 0.72752000 | +0.01826877 | +0.01727372 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | allpaid28819 | 50pct | 0.50000000 | 0.47852000 | 0.01812000 | +0.07198266 | +0.07085020 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.24999133 | 0.25932000 | 0.02048000 | +0.11494613 | +0.11395228 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50000000 | 0.49304000 | 0.03540000 | +0.11494613 | +0.11339499 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.74999133 | 0.74256000 | 0.05592000 | +0.11494613 | +0.11180370 |
| FiQA | e5_small_base | simplelinear_official_final50_mlp5 | allpaid28819 | 50pct | 0.50000000 | 0.49684000 | 0.05104000 | +0.07672478 | +0.07546450 |
| FiQA | e5_small_base | simplelinear_official_final50_mlp5 | fixed1024 | 50pct | 0.50000000 | 0.52044000 | 0.48200000 | +0.07573667 | +0.07453436 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | allpaid28819 | 50pct | 0.50000000 | 0.49748000 | 0.58440000 | +0.01552500 | +0.01536553 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24999133 | 0.25656000 | 0.59988000 | +0.01258398 | +0.01231543 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.50000000 | 0.49928000 | 0.82760000 | +0.01258398 | +0.01226167 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74999133 | 0.75396000 | 0.94004000 | +0.01258398 | +0.01328507 |
| FiQA | minilm_distilroberta | embedding_converter_paper_spec | allpaid28819 | 50pct | 0.50000000 | 0.49136000 | 0.52136000 | +0.00283373 | +0.00359173 |
| FiQA | minilm_distilroberta | embedding_converter_paper_spec | fixed1024 | 50pct | 0.50000000 | 0.50248000 | 0.62916000 | +0.01997409 | +0.01940486 |
| FiQA | minilm_distilroberta | la2m20_integration_script_adaptation | allpaid28819 | 50pct | 0.50000000 | 0.54988000 | 0.73320000 | +0.00054824 | +0.00058684 |
| FiQA | minilm_distilroberta | la2m20_integration_script_adaptation | fixed1024 | 50pct | 0.50000000 | 0.62976000 | 0.99388000 | +0.00006097 | -0.00054734 |
| FiQA | minilm_distilroberta | procrustes_global | allpaid28819 | 50pct | 0.50000000 | 0.49744000 | 0.80884000 | +0.00142845 | +0.00132018 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.24999133 | 0.25592000 | 0.73720000 | +0.00174542 | +0.00139573 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.50000000 | 0.49812000 | 0.90768000 | +0.00174542 | +0.00151208 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.74999133 | 0.75560000 | 0.97188000 | +0.00174542 | +0.00202622 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | allpaid28819 | 50pct | 0.50000000 | 0.49328000 | 0.54040000 | +0.02077125 | +0.02068191 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.24999133 | 0.25512000 | 0.48656000 | +0.06409958 | +0.06362625 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50000000 | 0.50036000 | 0.68964000 | +0.06409958 | +0.06292530 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.74999133 | 0.74904000 | 0.82452000 | +0.06409958 | +0.06305057 |
| FiQA | minilm_distilroberta | simplelinear_official_final50_mlp5 | allpaid28819 | 50pct | 0.50000000 | 0.50368000 | 0.62796000 | +0.01991832 | +0.01981713 |
| FiQA | minilm_distilroberta | simplelinear_official_final50_mlp5 | fixed1024 | 50pct | 0.50000000 | 0.50728000 | 0.99796000 | +0.04337540 | +0.04256133 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.25000000 | 0.34840000 | 0.17720000 | +0.03124394 | +0.03103260 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.50000000 | 0.57080000 | 0.38120000 | +0.03124394 | +0.03090695 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.75000000 | 0.79560000 | 0.62080000 | +0.03124394 | +0.03067348 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.25000000 | 0.33160000 | 0.32240000 | +0.01325493 | +0.01321022 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.50000000 | 0.56120000 | 0.60680000 | +0.01325493 | +0.01307246 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.75000000 | 0.79040000 | 0.82520000 | +0.01325493 | +0.01281352 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.25000000 | 0.33000000 | 0.03480000 | +0.13496868 | +0.13512617 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50000000 | 0.55840000 | 0.07600000 | +0.13496868 | +0.13529451 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.75000000 | 0.78240000 | 0.12320000 | +0.13496868 | +0.13492622 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.25000000 | 0.32200000 | 0.32520000 | +0.00689082 | +0.00672016 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.50000000 | 0.54840000 | 0.60520000 | +0.00689082 | +0.00692633 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.75000000 | 0.76720000 | 0.82000000 | +0.00689082 | +0.00707775 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.25000000 | 0.31280000 | 0.46480000 | -0.00030303 | -0.00043049 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.50000000 | 0.54400000 | 0.73440000 | -0.00030303 | -0.00024375 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.75000000 | 0.77080000 | 0.90400000 | -0.00030303 | -0.00013204 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.25000000 | 0.27040000 | 0.13320000 | +0.03481643 | +0.03506269 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50000000 | 0.52120000 | 0.29080000 | +0.03481643 | +0.03549973 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.75000000 | 0.75400000 | 0.49280000 | +0.03481643 | +0.03580223 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24990177 | 0.41440000 | 0.16800000 | +0.03209717 | +0.03177253 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.50000000 | 0.59840000 | 0.34040000 | +0.03209717 | +0.03183036 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74990177 | 0.80000000 | 0.58400000 | +0.03209717 | +0.03173301 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.24990177 | 0.39040000 | 0.38080000 | +0.01361781 | +0.01351969 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.50000000 | 0.58440000 | 0.64560000 | +0.01361781 | +0.01359633 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.74990177 | 0.79160000 | 0.84960000 | +0.01361781 | +0.01361897 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.24990177 | 0.36880000 | 0.03080000 | +0.13602489 | +0.13604508 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50000000 | 0.56000000 | 0.06160000 | +0.13602489 | +0.13604407 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.74990177 | 0.78080000 | 0.09960000 | +0.13602489 | +0.13561644 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24990177 | 0.35000000 | 0.31240000 | +0.01836201 | +0.01818101 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.50000000 | 0.56520000 | 0.56320000 | +0.01836201 | +0.01844915 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74990177 | 0.78680000 | 0.79360000 | +0.01836201 | +0.01769658 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.24990177 | 0.33720000 | 0.54840000 | -0.00114311 | -0.00131407 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.50000000 | 0.55720000 | 0.80560000 | -0.00114311 | -0.00110689 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.74990177 | 0.78400000 | 0.93760000 | -0.00114311 | -0.00153801 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.24990177 | 0.28640000 | 0.09560000 | +0.08156200 | +0.08212850 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50000000 | 0.52600000 | 0.20520000 | +0.08156200 | +0.08261441 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.74990177 | 0.77120000 | 0.35760000 | +0.08156200 | +0.08169534 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24985104 | 0.36640000 | 0.18040000 | +0.02886746 | +0.02879175 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.49990070 | 0.58680000 | 0.38720000 | +0.02886746 | +0.02901097 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74995035 | 0.79040000 | 0.62440000 | +0.02886746 | +0.02913818 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.24985104 | 0.35080000 | 0.30840000 | +0.01485389 | +0.01494342 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.49990070 | 0.57320000 | 0.58920000 | +0.01485389 | +0.01521889 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.74995035 | 0.78080000 | 0.80400000 | +0.01485389 | +0.01546886 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.24985104 | 0.33440000 | 0.05600000 | +0.13549283 | +0.13567409 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.49990070 | 0.54840000 | 0.10920000 | +0.13549283 | +0.13569653 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.74995035 | 0.77880000 | 0.17880000 | +0.13549283 | +0.13541607 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24985104 | 0.33200000 | 0.36920000 | +0.00320780 | +0.00318921 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.49990070 | 0.56160000 | 0.66120000 | +0.00320780 | +0.00329632 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74995035 | 0.78880000 | 0.86760000 | +0.00320780 | +0.00335747 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.24985104 | 0.33200000 | 0.50520000 | -0.00016635 | -0.00014334 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.49990070 | 0.56240000 | 0.77280000 | -0.00016635 | -0.00002431 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.74995035 | 0.78760000 | 0.92080000 | -0.00016635 | +0.00005836 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.24985104 | 0.29280000 | 0.20640000 | +0.01928597 | +0.01942202 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.49990070 | 0.53280000 | 0.40400000 | +0.01928597 | +0.01955728 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.74995035 | 0.77160000 | 0.62880000 | +0.01928597 | +0.01945563 |

The JSON receipt also retains every existing per-seed MAE/RMSE, score-STD ratio, sampled vector cosine, direction norm and rank-overlap value. No favorable cases are filtered.

STOP after B1-G/ARIS interpretation and the D1 recommendation. No automatic TREC, breadth or systems run.
