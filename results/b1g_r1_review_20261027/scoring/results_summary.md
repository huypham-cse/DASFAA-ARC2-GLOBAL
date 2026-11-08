# B1-G mixed-gallery development diagnostics

All 450 partial cases and 210 pristine fitted galleries are retained. Labels are the four previously inspected DEV collections. These are descriptive diagnostics; no calibration, new fit, significance test or confidence interval was selected.

Metric delta is after true-vector replacement minus pristine proxy retrieval. nDCG@10 uses graded gain; Recall@100 retains all positive qrels in its denominator. All 500 FiQA or 50 Nano queries count, including queries without positive judgments.

Returned paid/proxy imbalance alone does not establish miscalibration. Paired score error is proxy minus true score on the same fixed 512 sampled documents. Reference vectors did not enter pristine ranking, paid selection, fitting or cost.

| Dataset | Pair | Method | Regime | Budget | nDCG before | after | delta | Recall before | after | delta |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| FiQA | e5_small_base | arc2_global_tangent2_r1 | allpaid28819 | 50pct | 0.31490775 | 0.29186698 | -0.02304077 | 0.65416425 | 0.55948992 | -0.09467432 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.24121966 | 0.27310684 | +0.03188718 | 0.57408213 | 0.59973810 | +0.02565597 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.24121966 | 0.31163521 | +0.07041554 | 0.57408213 | 0.62092458 | +0.04684244 |
| FiQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.24121966 | 0.33718532 | +0.09596565 | 0.57408213 | 0.66060916 | +0.08652702 |
| FiQA | e5_small_base | embedding_converter_paper_spec | allpaid28819 | 50pct | 0.15865061 | 0.26251946 | +0.10386885 | 0.48563367 | 0.57890742 | +0.09327375 |
| FiQA | e5_small_base | embedding_converter_paper_spec | fixed1024 | 50pct | 0.04180985 | 0.13966537 | +0.09785552 | 0.23142808 | 0.33581264 | +0.10438456 |
| FiQA | e5_small_base | la2m20_integration_script_adaptation | allpaid28819 | 50pct | 0.29891812 | 0.32934130 | +0.03042318 | 0.63374943 | 0.64733062 | +0.01358119 |
| FiQA | e5_small_base | la2m20_integration_script_adaptation | fixed1024 | 50pct | 0.04700906 | 0.22999032 | +0.18298126 | 0.23097817 | 0.45060436 | +0.21962619 |
| FiQA | e5_small_base | procrustes_global | allpaid28819 | 50pct | 0.28609600 | 0.33620246 | +0.05010646 | 0.60539674 | 0.65338892 | +0.04799219 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.23577734 | 0.27177804 | +0.03600070 | 0.56338445 | 0.60277527 | +0.03939082 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.23577734 | 0.31003589 | +0.07425856 | 0.56338445 | 0.63742908 | +0.07404463 |
| FiQA | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.23577734 | 0.34076801 | +0.10499067 | 0.56338445 | 0.67758526 | +0.11420081 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | allpaid28819 | 50pct | 0.27058501 | 0.22701458 | -0.04357043 | 0.60243647 | 0.42451112 | -0.17792535 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.10158416 | 0.12805447 | +0.02647031 | 0.36126407 | 0.33304517 | -0.02821889 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.10158416 | 0.14792157 | +0.04633741 | 0.36126407 | 0.30526999 | -0.05599408 |
| FiQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.10158416 | 0.16097149 | +0.05938733 | 0.36126407 | 0.24947686 | -0.11178721 |
| FiQA | e5_small_base | simplelinear_official_final50_mlp5 | allpaid28819 | 50pct | 0.11597835 | 0.16794941 | +0.05197106 | 0.38754256 | 0.36178455 | -0.02575802 |
| FiQA | e5_small_base | simplelinear_official_final50_mlp5 | fixed1024 | 50pct | 0.00127043 | 0.19416743 | +0.19289700 | 0.01167622 | 0.26015570 | +0.24847948 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | allpaid28819 | 50pct | 0.35095074 | 0.36714602 | +0.01619529 | 0.68047367 | 0.69220016 | +0.01172649 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.31044544 | 0.28711945 | -0.02332599 | 0.65334994 | 0.66501450 | +0.01166456 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.31044544 | 0.30750486 | -0.00294058 | 0.65334994 | 0.67656934 | +0.02321940 |
| FiQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.31044544 | 0.35007223 | +0.03962679 | 0.65334994 | 0.68848093 | +0.03513099 |
| FiQA | minilm_distilroberta | embedding_converter_paper_spec | allpaid28819 | 50pct | 0.28271603 | 0.32576144 | +0.04304541 | 0.64551286 | 0.66326948 | +0.01775662 |
| FiQA | minilm_distilroberta | embedding_converter_paper_spec | fixed1024 | 50pct | 0.09576155 | 0.24963648 | +0.15387493 | 0.40840168 | 0.54295439 | +0.13455271 |
| FiQA | minilm_distilroberta | la2m20_integration_script_adaptation | allpaid28819 | 50pct | 0.35064303 | 0.33892347 | -0.01171957 | 0.70013364 | 0.69500515 | -0.00512849 |
| FiQA | minilm_distilroberta | la2m20_integration_script_adaptation | fixed1024 | 50pct | 0.08085071 | 0.23767401 | +0.15682331 | 0.38627874 | 0.46551793 | +0.07923920 |
| FiQA | minilm_distilroberta | procrustes_global | allpaid28819 | 50pct | 0.34955887 | 0.33338647 | -0.01617239 | 0.68479855 | 0.69049483 | +0.00569628 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.30388301 | 0.25699670 | -0.04688631 | 0.65267489 | 0.65799210 | +0.00531721 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.30388301 | 0.28582824 | -0.01805477 | 0.65267489 | 0.66879180 | +0.01611691 |
| FiQA | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.30388301 | 0.34174406 | +0.03786105 | 0.65267489 | 0.68315594 | +0.03048105 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | allpaid28819 | 50pct | 0.34222250 | 0.36726328 | +0.02504077 | 0.67096129 | 0.68004301 | +0.00908172 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.26049267 | 0.24763689 | -0.01285578 | 0.60000631 | 0.62012171 | +0.02011540 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.26049267 | 0.28904546 | +0.02855278 | 0.60000631 | 0.63737656 | +0.03737025 |
| FiQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.26049267 | 0.34374457 | +0.08325190 | 0.60000631 | 0.66308697 | +0.06308065 |
| FiQA | minilm_distilroberta | simplelinear_official_final50_mlp5 | allpaid28819 | 50pct | 0.30711973 | 0.33231625 | +0.02519651 | 0.64949960 | 0.67778892 | +0.02828932 |
| FiQA | minilm_distilroberta | simplelinear_official_final50_mlp5 | fixed1024 | 50pct | 0.09701478 | 0.23595312 | +0.13893834 | 0.40349673 | 0.43251143 | +0.02901470 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.74315082 | 0.75545127 | +0.01230046 | 0.98400000 | 0.98200000 | -0.00200000 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.74315082 | 0.77894994 | +0.03579912 | 0.98400000 | 0.98866667 | +0.00466667 |
| NanoFEVER | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.74315082 | 0.84512017 | +0.10196935 | 0.98400000 | 0.99400000 | +0.01000000 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.74619924 | 0.71466167 | -0.03153757 | 0.98600000 | 0.98733333 | +0.00133333 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.74619924 | 0.74020974 | -0.00598950 | 0.98600000 | 0.99533333 | +0.00933333 |
| NanoFEVER | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.74619924 | 0.82273549 | +0.07653625 | 0.98600000 | 0.99533333 | +0.00933333 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.61096297 | 0.64478468 | +0.03382171 | 0.95333333 | 0.92666667 | -0.02666667 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.61096297 | 0.67109381 | +0.06013083 | 0.95333333 | 0.89466667 | -0.05866667 |
| NanoFEVER | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.61096297 | 0.72898601 | +0.11802304 | 0.95333333 | 0.86666667 | -0.08666667 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.54160497 | 0.54525280 | +0.00364783 | 0.90866667 | 0.93200000 | +0.02333333 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.54160497 | 0.60111412 | +0.05950915 | 0.90866667 | 0.94200000 | +0.03333333 |
| NanoFEVER | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.54160497 | 0.68706384 | +0.14545887 | 0.90866667 | 0.96666667 | +0.05800000 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.53053811 | 0.50736477 | -0.02317334 | 0.92866667 | 0.92600000 | -0.00266667 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.53053811 | 0.58135767 | +0.05081956 | 0.92866667 | 0.93600000 | +0.00733333 |
| NanoFEVER | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.53053811 | 0.67290499 | +0.14236688 | 0.92866667 | 0.95866667 | +0.03000000 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.43898389 | 0.49430945 | +0.05532556 | 0.83866667 | 0.87000000 | +0.03133333 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.43898389 | 0.54881962 | +0.10983573 | 0.83866667 | 0.91200000 | +0.07333333 |
| NanoFEVER | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.43898389 | 0.65398488 | +0.21500099 | 0.83866667 | 0.95466667 | +0.11600000 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.53140457 | 0.58448566 | +0.05308109 | 0.90200000 | 0.91400000 | +0.01200000 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.53140457 | 0.67223953 | +0.14083496 | 0.90200000 | 0.93000000 | +0.02800000 |
| NanoHotpotQA | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.53140457 | 0.74638760 | +0.21498303 | 0.90200000 | 0.94800000 | +0.04600000 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.53726826 | 0.55123462 | +0.01396635 | 0.90400000 | 0.91600000 | +0.01200000 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.53726826 | 0.62992807 | +0.09265981 | 0.90400000 | 0.93600000 | +0.03200000 |
| NanoHotpotQA | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.53726826 | 0.72020712 | +0.18293886 | 0.90400000 | 0.95000000 | +0.04600000 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.36173761 | 0.38044345 | +0.01870584 | 0.84800000 | 0.76000000 | -0.08800000 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.36173761 | 0.44244608 | +0.08070847 | 0.84800000 | 0.72000000 | -0.12800000 |
| NanoHotpotQA | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.36173761 | 0.50534701 | +0.14360940 | 0.84800000 | 0.67400000 | -0.17400000 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.34454211 | 0.37598069 | +0.03143858 | 0.79200000 | 0.80600000 | +0.01400000 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.34454211 | 0.44352167 | +0.09897955 | 0.79200000 | 0.83000000 | +0.03800000 |
| NanoHotpotQA | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.34454211 | 0.49343446 | +0.14889234 | 0.79200000 | 0.84400000 | +0.05200000 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.33902489 | 0.33617899 | -0.00284590 | 0.78800000 | 0.80800000 | +0.02000000 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.33902489 | 0.41095595 | +0.07193106 | 0.78800000 | 0.82400000 | +0.03600000 |
| NanoHotpotQA | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.33902489 | 0.47811448 | +0.13908959 | 0.78800000 | 0.84200000 | +0.05400000 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.30796422 | 0.35053302 | +0.04256880 | 0.76400000 | 0.75000000 | -0.01400000 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.30796422 | 0.41687929 | +0.10891507 | 0.76400000 | 0.76600000 | +0.00200000 |
| NanoHotpotQA | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.30796422 | 0.47298218 | +0.16501797 | 0.76400000 | 0.78200000 | +0.01800000 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.49364597 | 0.50712368 | +0.01347772 | 0.98000000 | 0.95600000 | -0.02400000 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.49364597 | 0.54434822 | +0.05070226 | 0.98000000 | 0.95600000 | -0.02400000 |
| NanoNQ | e5_small_base | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.49364597 | 0.61009940 | +0.11645343 | 0.98000000 | 0.96400000 | -0.01600000 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 25pct | 0.49292882 | 0.48523705 | -0.00769177 | 0.97600000 | 0.97600000 | +0.00000000 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 50pct | 0.49292882 | 0.51309058 | +0.02016177 | 0.97600000 | 0.96800000 | -0.00800000 |
| NanoNQ | e5_small_base | procrustes_global | fixed1024 | 75pct | 0.49292882 | 0.59123919 | +0.09831037 | 0.97600000 | 0.96400000 | -0.01200000 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.28203354 | 0.32191350 | +0.03987996 | 0.87600000 | 0.84000000 | -0.03600000 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.28203354 | 0.38706437 | +0.10503083 | 0.87600000 | 0.78000000 | -0.09600000 |
| NanoNQ | e5_small_base | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.28203354 | 0.44284100 | +0.16080746 | 0.87600000 | 0.75400000 | -0.12200000 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 25pct | 0.52025266 | 0.48880674 | -0.03144591 | 0.96600000 | 0.97000000 | +0.00400000 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 50pct | 0.52025266 | 0.52662434 | +0.00637168 | 0.96600000 | 0.97000000 | +0.00400000 |
| NanoNQ | minilm_distilroberta | arc2_global_tangent2_r1 | fixed1024 | 75pct | 0.52025266 | 0.58683260 | +0.06657994 | 0.96600000 | 0.97600000 | +0.01000000 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 25pct | 0.50242163 | 0.44214747 | -0.06027416 | 0.96400000 | 0.96000000 | -0.00400000 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 50pct | 0.50242163 | 0.49951053 | -0.00291109 | 0.96400000 | 0.95400000 | -0.01000000 |
| NanoNQ | minilm_distilroberta | procrustes_global | fixed1024 | 75pct | 0.50242163 | 0.57142874 | +0.06900711 | 0.96400000 | 0.96200000 | -0.00200000 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 25pct | 0.50210572 | 0.48072307 | -0.02138265 | 0.94400000 | 0.92200000 | -0.02200000 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 50pct | 0.50210572 | 0.51776948 | +0.01566376 | 0.94400000 | 0.93000000 | -0.01400000 |
| NanoNQ | minilm_distilroberta | ridge_affine_l10_bias_regularized | fixed1024 | 75pct | 0.50210572 | 0.58549214 | +0.08338642 | 0.94400000 | 0.94800000 | +0.00400000 |

Every case, both delta signs, per-query arrays, paired error quantiles and score/direction statistics are retained in results_summary.json, per-dataset metric artifacts and the two immutable shard bundles.

STOP: analyze B1-G with B1-M/B1-P and record D1. No automatic breadth, TREC or systems run.
