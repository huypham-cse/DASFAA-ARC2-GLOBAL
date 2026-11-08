# B1-P FiQA development results

Previously inspected FiQA DEV; not independent confirmation.

All 500 queries count; no-positive queries score zero. Graded nDCG@10 uses 2^rel-1 gain; Recall@100 divides by all positive qrels, including documents outside the corpus.

Means average queries then five mapping seeds. Seed SD uses ddof=1; ranges and full-Y retention are in JSON. Full references have one deterministic ranking.

| Pair | Regime | Method | nDCG@10 mean (seed SD) | Recall@100 mean (seed SD) |
|---|---|---|---:|---:|
| minilm_distilroberta | fixed1024 | procrustes_global | 0.285828 (0.004024) | 0.668792 (0.005208) |
| minilm_distilroberta | fixed1024 | arc2_global_tangent2_r1 | 0.307505 (0.006017) | 0.676569 (0.001741) |
| minilm_distilroberta | fixed1024 | la2m20_integration_script_adaptation | 0.237674 (0.003024) | 0.465518 (0.006950) |
| minilm_distilroberta | fixed1024 | simplelinear_official_final50_mlp5 | 0.235953 (0.002560) | 0.432511 (0.002190) |
| minilm_distilroberta | fixed1024 | ridge_affine_l10_bias_regularized | 0.289045 (0.005862) | 0.637377 (0.001793) |
| minilm_distilroberta | fixed1024 | embedding_converter_paper_spec | 0.249636 (0.003655) | 0.542954 (0.010934) |
| minilm_distilroberta | allpaid28819 | procrustes_global | 0.333386 (0.001104) | 0.690495 (0.002025) |
| minilm_distilroberta | allpaid28819 | arc2_global_tangent2_r1 | 0.367146 (0.000853) | 0.692200 (0.000488) |
| minilm_distilroberta | allpaid28819 | la2m20_integration_script_adaptation | 0.338923 (0.002658) | 0.695005 (0.003007) |
| minilm_distilroberta | allpaid28819 | simplelinear_official_final50_mlp5 | 0.332316 (0.002088) | 0.677789 (0.001712) |
| minilm_distilroberta | allpaid28819 | ridge_affine_l10_bias_regularized | 0.367263 (0.001195) | 0.680043 (0.000423) |
| minilm_distilroberta | allpaid28819 | embedding_converter_paper_spec | 0.325761 (0.003958) | 0.663269 (0.003971) |
| minilm_distilroberta | reference | full_x | 0.389961 (reference) | 0.700184 (reference) |
| minilm_distilroberta | reference | full_y | 0.404736 (reference) | 0.703892 (reference) |
| e5_small_base | fixed1024 | procrustes_global | 0.310036 (0.002542) | 0.637429 (0.006658) |
| e5_small_base | fixed1024 | arc2_global_tangent2_r1 | 0.311635 (0.003373) | 0.620925 (0.008032) |
| e5_small_base | fixed1024 | la2m20_integration_script_adaptation | 0.229990 (0.003297) | 0.450604 (0.014097) |
| e5_small_base | fixed1024 | simplelinear_official_final50_mlp5 | 0.194167 (0.003687) | 0.260156 (0.005130) |
| e5_small_base | fixed1024 | ridge_affine_l10_bias_regularized | 0.147922 (0.004371) | 0.305270 (0.006730) |
| e5_small_base | fixed1024 | embedding_converter_paper_spec | 0.139665 (0.005300) | 0.335813 (0.015431) |
| e5_small_base | allpaid28819 | procrustes_global | 0.336202 (0.001002) | 0.653389 (0.001889) |
| e5_small_base | allpaid28819 | arc2_global_tangent2_r1 | 0.291867 (0.001189) | 0.559490 (0.001407) |
| e5_small_base | allpaid28819 | la2m20_integration_script_adaptation | 0.329341 (0.004652) | 0.647331 (0.002887) |
| e5_small_base | allpaid28819 | simplelinear_official_final50_mlp5 | 0.167949 (0.004714) | 0.361785 (0.008745) |
| e5_small_base | allpaid28819 | ridge_affine_l10_bias_regularized | 0.227015 (0.002070) | 0.424511 (0.001965) |
| e5_small_base | allpaid28819 | embedding_converter_paper_spec | 0.262519 (0.005972) | 0.578907 (0.003774) |
| e5_small_base | reference | full_x | 0.346478 (reference) | 0.645332 (reference) |
| e5_small_base | reference | full_y | 0.389133 (reference) | 0.696797 (reference) |

All 32 predeclared nDCG contrasts form one Bonferroni family with nominal 95% family coverage: each percentile interval has 99.84375% confidence. Bootstrap coverage is approximate. Nominal 95% nDCG and Recall intervals are descriptive. The 20,000 shared paired query resamples follow five-seed averaging; seeds do not create independent queries.

| Pair | Contrast (left minus right) | Delta nDCG [family interval] | Delta Recall [descriptive 95%] |
|---|---|---:|---:|
| minilm_distilroberta | procrustes_global (allpaid28819) - procrustes_global (fixed1024) | +0.047558 [+0.031519, +0.065013] | +0.021703 [+0.009742, +0.034410] |
| minilm_distilroberta | arc2_global_tangent2_r1 (allpaid28819) - arc2_global_tangent2_r1 (fixed1024) | +0.059641 [+0.039341, +0.080604] | +0.015631 [+0.002193, +0.029359] |
| minilm_distilroberta | la2m20_integration_script_adaptation (allpaid28819) - la2m20_integration_script_adaptation (fixed1024) | +0.101249 [+0.071645, +0.135397] | +0.229487 [+0.198486, +0.261050] |
| minilm_distilroberta | simplelinear_official_final50_mlp5 (allpaid28819) - simplelinear_official_final50_mlp5 (fixed1024) | +0.096363 [+0.065745, +0.130316] | +0.245277 [+0.210141, +0.280342] |
| minilm_distilroberta | ridge_affine_l10_bias_regularized (allpaid28819) - ridge_affine_l10_bias_regularized (fixed1024) | +0.078218 [+0.054777, +0.102883] | +0.042666 [+0.025388, +0.061057] |
| minilm_distilroberta | embedding_converter_paper_spec (allpaid28819) - embedding_converter_paper_spec (fixed1024) | +0.076125 [+0.053432, +0.102150] | +0.120315 [+0.102829, +0.138404] |
| minilm_distilroberta | arc2_global_tangent2_r1 (allpaid28819) - procrustes_global (allpaid28819) | +0.033760 [+0.018645, +0.050408] | +0.001705 [-0.012078, +0.015720] |
| minilm_distilroberta | arc2_global_tangent2_r1 (allpaid28819) - la2m20_integration_script_adaptation (allpaid28819) | +0.028223 [+0.010129, +0.047297] | -0.002805 [-0.018305, +0.012420] |
| minilm_distilroberta | arc2_global_tangent2_r1 (allpaid28819) - simplelinear_official_final50_mlp5 (allpaid28819) | +0.034830 [+0.023544, +0.047191] | +0.014411 [+0.005683, +0.023532] |
| minilm_distilroberta | arc2_global_tangent2_r1 (allpaid28819) - ridge_affine_l10_bias_regularized (allpaid28819) | -0.000117 [-0.007540, +0.006532] | +0.012157 [+0.002832, +0.022805] |
| minilm_distilroberta | arc2_global_tangent2_r1 (allpaid28819) - embedding_converter_paper_spec (allpaid28819) | +0.041385 [+0.023614, +0.060969] | +0.028931 [+0.015501, +0.043066] |
| minilm_distilroberta | arc2_global_tangent2_r1 (fixed1024) - procrustes_global (allpaid28819) | -0.025882 [-0.039807, -0.013428] | -0.013925 [-0.024717, -0.003872] |
| minilm_distilroberta | arc2_global_tangent2_r1 (fixed1024) - la2m20_integration_script_adaptation (allpaid28819) | -0.031419 [-0.048612, -0.015634] | -0.018436 [-0.031152, -0.006472] |
| minilm_distilroberta | arc2_global_tangent2_r1 (fixed1024) - simplelinear_official_final50_mlp5 (allpaid28819) | -0.024811 [-0.039054, -0.011252] | -0.001220 [-0.013927, +0.011343] |
| minilm_distilroberta | arc2_global_tangent2_r1 (fixed1024) - ridge_affine_l10_bias_regularized (allpaid28819) | -0.059758 [-0.082583, -0.038546] | -0.003474 [-0.019306, +0.012448] |
| minilm_distilroberta | arc2_global_tangent2_r1 (fixed1024) - embedding_converter_paper_spec (allpaid28819) | -0.018257 [-0.036885, -0.001023] | +0.013300 [-0.001344, +0.028125] |
| e5_small_base | procrustes_global (allpaid28819) - procrustes_global (fixed1024) | +0.026167 [+0.009889, +0.044332] | +0.015960 [+0.004077, +0.028075] |
| e5_small_base | arc2_global_tangent2_r1 (allpaid28819) - arc2_global_tangent2_r1 (fixed1024) | -0.019768 [-0.056330, +0.016637] | -0.061435 [-0.083203, -0.040108] |
| e5_small_base | la2m20_integration_script_adaptation (allpaid28819) - la2m20_integration_script_adaptation (fixed1024) | +0.099351 [+0.059183, +0.140816] | +0.196726 [+0.166081, +0.228098] |
| e5_small_base | simplelinear_official_final50_mlp5 (allpaid28819) - simplelinear_official_final50_mlp5 (fixed1024) | -0.026218 [-0.067498, +0.013474] | +0.101629 [+0.063027, +0.140789] |
| e5_small_base | ridge_affine_l10_bias_regularized (allpaid28819) - ridge_affine_l10_bias_regularized (fixed1024) | +0.079093 [+0.043500, +0.117026] | +0.119241 [+0.096436, +0.142886] |
| e5_small_base | embedding_converter_paper_spec (allpaid28819) - embedding_converter_paper_spec (fixed1024) | +0.122854 [+0.097068, +0.153161] | +0.243095 [+0.217053, +0.269657] |
| e5_small_base | arc2_global_tangent2_r1 (allpaid28819) - procrustes_global (allpaid28819) | -0.044335 [-0.079696, -0.009272] | -0.093899 [-0.116955, -0.071323] |
| e5_small_base | arc2_global_tangent2_r1 (allpaid28819) - la2m20_integration_script_adaptation (allpaid28819) | -0.037474 [-0.070583, -0.003758] | -0.087841 [-0.111271, -0.065305] |
| e5_small_base | arc2_global_tangent2_r1 (allpaid28819) - simplelinear_official_final50_mlp5 (allpaid28819) | +0.123918 [+0.093821, +0.156724] | +0.197705 [+0.172536, +0.223852] |
| e5_small_base | arc2_global_tangent2_r1 (allpaid28819) - ridge_affine_l10_bias_regularized (allpaid28819) | +0.064852 [+0.043521, +0.089349] | +0.134979 [+0.110163, +0.160894] |
| e5_small_base | arc2_global_tangent2_r1 (allpaid28819) - embedding_converter_paper_spec (allpaid28819) | +0.029348 [-0.015573, +0.074762] | -0.019417 [-0.049316, +0.010749] |
| e5_small_base | arc2_global_tangent2_r1 (fixed1024) - procrustes_global (allpaid28819) | -0.024567 [-0.038609, -0.012263] | -0.032464 [-0.044156, -0.021482] |
| e5_small_base | arc2_global_tangent2_r1 (fixed1024) - la2m20_integration_script_adaptation (allpaid28819) | -0.017706 [-0.034378, -0.002178] | -0.026406 [-0.038320, -0.015057] |
| e5_small_base | arc2_global_tangent2_r1 (fixed1024) - simplelinear_official_final50_mlp5 (allpaid28819) | +0.143686 [+0.112571, +0.178479] | +0.259140 [+0.231246, +0.287408] |
| e5_small_base | arc2_global_tangent2_r1 (fixed1024) - ridge_affine_l10_bias_regularized (allpaid28819) | +0.084621 [+0.042156, +0.130647] | +0.196413 [+0.165539, +0.228683] |
| e5_small_base | arc2_global_tangent2_r1 (fixed1024) - embedding_converter_paper_spec (allpaid28819) | +0.049116 [+0.026523, +0.074037] | +0.042017 [+0.021450, +0.063107] |

An interval crossing or touching zero is unresolved. No equivalence/noninferiority margin, method selection, D1 decision or independent claim is made. Full-reference retention is descriptive. STOP after this authorized development report; no automatic B1-G, breadth, TREC or systems run.

Generation commit: `7530c8eb46b68c9d5937c4bb9ccfd929d1613e74`. Recovery scorer commit: `4062d96c353ac567fb90a6093cd8059d4647e252`. Original failed scoring attempt and FAILED_PRESERVED raw metadata remain intact.
