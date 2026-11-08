# B1-G completed: mixed-gallery development diagnostics

**450 partial cases, 210 pristine fitted galleries, 90 five-seed conditions; all six methods retained.**

The four collections are already inspected DEV: FiQA (500 queries) and NanoNQ, NanoHotpotQA, NanoFEVER (50 queries each). Every case retains all queries and five seeds. No new fit, encoding, calibration, confidence interval or significance test was performed.

“Before” uses the saved mapper prediction for every document, including anchors. “After” replaces exactly the original anchor-inclusive paid set with true destination vectors and reproduces its published mixed ranking. The mapper and its original fitting exposure stay fixed between endpoints; an all-paid fit already used the paid target pairs before this counterfactual. Metric delta is after minus before. No independent or physical-cost result follows from these diagnostics.

The original local verification failure is preserved: its historical-metric path comparison treated relative and resolved absolute paths differently. The separate R2 verification corrects that local path comparison; raw results, rankings, scoring and protocol remain unchanged.

Paired errors compare proxy and true scores for the same query and each of 512 label-independent sampled documents. “Unpaid bias” is mean proxy minus true score within the sampled unpaid stratum, averaged equally over seeds. Strata and their sample sizes remain separate. Returned-share imbalance or anisotropy does not establish miscalibration or causally explain relevance changes. Negative effects remain reported.

[Publication figure](figures/b1g_mixed_gallery_diagnostics.pdf) · [PNG preview](figures/b1g_mixed_gallery_diagnostics.png) · [Editable SVG](figures/b1g_mixed_gallery_diagnostics.svg) · [Figure data](figures/b1g_mixed_gallery_diagnostics.csv)

The figure shows a FiQA50 overview subset, chosen before B1-G result inspection (ARC2, Procrustes, ridge; both fitting regimes and encoder pairs); full tables retain all conditions. The tables below cover the full finite diagnostic scope. Numbers are five-seed means; no intervals are implied.

| Dataset | Pair | Method | Fit | Budget | nDCG before | after | Δ | Recall before | after | Δ | Unpaid bias | Paid top10 before | after |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FiQA | E5 | ARC2-Global | All-paid | 50pct | 0.314908 | 0.291867 | -0.023041 | 0.654164 | 0.559490 | -0.094674 | +0.039684 | 0.491640 | 0.064720 |
| FiQA | E5 | ARC2-Global | Fixed1024 | 25pct | 0.241220 | 0.273107 | +0.031887 | 0.574082 | 0.599738 | +0.025656 | +0.024702 | 0.259160 | 0.166840 |
| FiQA | E5 | ARC2-Global | Fixed1024 | 50pct | 0.241220 | 0.311635 | +0.070416 | 0.574082 | 0.620925 | +0.046842 | +0.024375 | 0.498560 | 0.333560 |
| FiQA | E5 | ARC2-Global | Fixed1024 | 75pct | 0.241220 | 0.337185 | +0.095966 | 0.574082 | 0.660609 | +0.086527 | +0.024210 | 0.750600 | 0.548520 |
| FiQA | E5 | Embedding-Converter adaptation | All-paid | 50pct | 0.158651 | 0.262519 | +0.103869 | 0.485634 | 0.578907 | +0.093274 | +0.001549 | 0.455080 | 0.462200 |
| FiQA | E5 | Embedding-Converter adaptation | Fixed1024 | 50pct | 0.041810 | 0.139665 | +0.097856 | 0.231428 | 0.335813 | +0.104385 | +0.047724 | 0.489240 | 0.084960 |
| FiQA | E5 | LA2M20 adaptation | All-paid | 50pct | 0.298918 | 0.329341 | +0.030423 | 0.633749 | 0.647331 | +0.013581 | +0.016048 | 0.563040 | 0.319600 |
| FiQA | E5 | LA2M20 adaptation | Fixed1024 | 50pct | 0.047009 | 0.229990 | +0.182981 | 0.230978 | 0.450604 | +0.219626 | +0.013111 | 0.639120 | 0.883320 |
| FiQA | E5 | A2M / Procrustes adaptation | All-paid | 50pct | 0.286096 | 0.336202 | +0.050106 | 0.605397 | 0.653389 | +0.047992 | +0.017429 | 0.497480 | 0.370720 |
| FiQA | E5 | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.235777 | 0.271778 | +0.036001 | 0.563384 | 0.602775 | +0.039391 | +0.017672 | 0.258800 | 0.272880 |
| FiQA | E5 | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.235777 | 0.310036 | +0.074259 | 0.563384 | 0.637429 | +0.074045 | +0.017444 | 0.497600 | 0.499160 |
| FiQA | E5 | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.235777 | 0.340768 | +0.104991 | 0.563384 | 0.677585 | +0.114201 | +0.017274 | 0.748680 | 0.727520 |
| FiQA | E5 | Affine ridge, lambda10 | All-paid | 50pct | 0.270585 | 0.227015 | -0.043570 | 0.602436 | 0.424511 | -0.177925 | +0.070850 | 0.478520 | 0.018120 |
| FiQA | E5 | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.101584 | 0.128054 | +0.026470 | 0.361264 | 0.333045 | -0.028219 | +0.113952 | 0.259320 | 0.020480 |
| FiQA | E5 | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.101584 | 0.147922 | +0.046337 | 0.361264 | 0.305270 | -0.055994 | +0.113395 | 0.493040 | 0.035400 |
| FiQA | E5 | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.101584 | 0.160971 | +0.059387 | 0.361264 | 0.249477 | -0.111787 | +0.111804 | 0.742560 | 0.055920 |
| FiQA | E5 | Official SimpleLinear (5-layer MLP) | All-paid | 50pct | 0.115978 | 0.167949 | +0.051971 | 0.387543 | 0.361785 | -0.025758 | +0.075464 | 0.496840 | 0.051040 |
| FiQA | E5 | Official SimpleLinear (5-layer MLP) | Fixed1024 | 50pct | 0.001270 | 0.194167 | +0.192897 | 0.011676 | 0.260156 | +0.248479 | +0.074534 | 0.520440 | 0.482000 |
| FiQA | MiniLM | ARC2-Global | All-paid | 50pct | 0.350951 | 0.367146 | +0.016195 | 0.680474 | 0.692200 | +0.011726 | +0.015366 | 0.497480 | 0.584400 |
| FiQA | MiniLM | ARC2-Global | Fixed1024 | 25pct | 0.310445 | 0.287119 | -0.023326 | 0.653350 | 0.665014 | +0.011665 | +0.012315 | 0.256560 | 0.599880 |
| FiQA | MiniLM | ARC2-Global | Fixed1024 | 50pct | 0.310445 | 0.307505 | -0.002941 | 0.653350 | 0.676569 | +0.023219 | +0.012262 | 0.499280 | 0.827600 |
| FiQA | MiniLM | ARC2-Global | Fixed1024 | 75pct | 0.310445 | 0.350072 | +0.039627 | 0.653350 | 0.688481 | +0.035131 | +0.013285 | 0.753960 | 0.940040 |
| FiQA | MiniLM | Embedding-Converter adaptation | All-paid | 50pct | 0.282716 | 0.325761 | +0.043045 | 0.645513 | 0.663269 | +0.017757 | +0.003592 | 0.491360 | 0.521360 |
| FiQA | MiniLM | Embedding-Converter adaptation | Fixed1024 | 50pct | 0.095762 | 0.249636 | +0.153875 | 0.408402 | 0.542954 | +0.134553 | +0.019405 | 0.502480 | 0.629160 |
| FiQA | MiniLM | LA2M20 adaptation | All-paid | 50pct | 0.350643 | 0.338923 | -0.011720 | 0.700134 | 0.695005 | -0.005128 | +0.000587 | 0.549880 | 0.733200 |
| FiQA | MiniLM | LA2M20 adaptation | Fixed1024 | 50pct | 0.080851 | 0.237674 | +0.156823 | 0.386279 | 0.465518 | +0.079239 | -0.000547 | 0.629760 | 0.993880 |
| FiQA | MiniLM | A2M / Procrustes adaptation | All-paid | 50pct | 0.349559 | 0.333386 | -0.016172 | 0.684799 | 0.690495 | +0.005696 | +0.001320 | 0.497440 | 0.808840 |
| FiQA | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.303883 | 0.256997 | -0.046886 | 0.652675 | 0.657992 | +0.005317 | +0.001396 | 0.255920 | 0.737200 |
| FiQA | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.303883 | 0.285828 | -0.018055 | 0.652675 | 0.668792 | +0.016117 | +0.001512 | 0.498120 | 0.907680 |
| FiQA | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.303883 | 0.341744 | +0.037861 | 0.652675 | 0.683156 | +0.030481 | +0.002026 | 0.755600 | 0.971880 |
| FiQA | MiniLM | Affine ridge, lambda10 | All-paid | 50pct | 0.342223 | 0.367263 | +0.025041 | 0.670961 | 0.680043 | +0.009082 | +0.020682 | 0.493280 | 0.540400 |
| FiQA | MiniLM | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.260493 | 0.247637 | -0.012856 | 0.600006 | 0.620122 | +0.020115 | +0.063626 | 0.255120 | 0.486560 |
| FiQA | MiniLM | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.260493 | 0.289045 | +0.028553 | 0.600006 | 0.637377 | +0.037370 | +0.062925 | 0.500360 | 0.689640 |
| FiQA | MiniLM | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.260493 | 0.343745 | +0.083252 | 0.600006 | 0.663087 | +0.063081 | +0.063051 | 0.749040 | 0.824520 |
| FiQA | MiniLM | Official SimpleLinear (5-layer MLP) | All-paid | 50pct | 0.307120 | 0.332316 | +0.025197 | 0.649500 | 0.677789 | +0.028289 | +0.019817 | 0.503680 | 0.627960 |
| FiQA | MiniLM | Official SimpleLinear (5-layer MLP) | Fixed1024 | 50pct | 0.097015 | 0.235953 | +0.138938 | 0.403497 | 0.432511 | +0.029015 | +0.042561 | 0.507280 | 0.997960 |
| NanoFEVER | E5 | ARC2-Global | Fixed1024 | 25pct | 0.743151 | 0.755451 | +0.012300 | 0.984000 | 0.982000 | -0.002000 | +0.031033 | 0.348400 | 0.177200 |
| NanoFEVER | E5 | ARC2-Global | Fixed1024 | 50pct | 0.743151 | 0.778950 | +0.035799 | 0.984000 | 0.988667 | +0.004667 | +0.030907 | 0.570800 | 0.381200 |
| NanoFEVER | E5 | ARC2-Global | Fixed1024 | 75pct | 0.743151 | 0.845120 | +0.101969 | 0.984000 | 0.994000 | +0.010000 | +0.030673 | 0.795600 | 0.620800 |
| NanoFEVER | E5 | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.746199 | 0.714662 | -0.031538 | 0.986000 | 0.987333 | +0.001333 | +0.013210 | 0.331600 | 0.322400 |
| NanoFEVER | E5 | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.746199 | 0.740210 | -0.005990 | 0.986000 | 0.995333 | +0.009333 | +0.013072 | 0.561200 | 0.606800 |
| NanoFEVER | E5 | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.746199 | 0.822735 | +0.076536 | 0.986000 | 0.995333 | +0.009333 | +0.012814 | 0.790400 | 0.825200 |
| NanoFEVER | E5 | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.610963 | 0.644785 | +0.033822 | 0.953333 | 0.926667 | -0.026667 | +0.135126 | 0.330000 | 0.034800 |
| NanoFEVER | E5 | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.610963 | 0.671094 | +0.060131 | 0.953333 | 0.894667 | -0.058667 | +0.135295 | 0.558400 | 0.076000 |
| NanoFEVER | E5 | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.610963 | 0.728986 | +0.118023 | 0.953333 | 0.866667 | -0.086667 | +0.134926 | 0.782400 | 0.123200 |
| NanoFEVER | MiniLM | ARC2-Global | Fixed1024 | 25pct | 0.541605 | 0.545253 | +0.003648 | 0.908667 | 0.932000 | +0.023333 | +0.006720 | 0.322000 | 0.325200 |
| NanoFEVER | MiniLM | ARC2-Global | Fixed1024 | 50pct | 0.541605 | 0.601114 | +0.059509 | 0.908667 | 0.942000 | +0.033333 | +0.006926 | 0.548400 | 0.605200 |
| NanoFEVER | MiniLM | ARC2-Global | Fixed1024 | 75pct | 0.541605 | 0.687064 | +0.145459 | 0.908667 | 0.966667 | +0.058000 | +0.007078 | 0.767200 | 0.820000 |
| NanoFEVER | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.530538 | 0.507365 | -0.023173 | 0.928667 | 0.926000 | -0.002667 | -0.000430 | 0.312800 | 0.464800 |
| NanoFEVER | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.530538 | 0.581358 | +0.050820 | 0.928667 | 0.936000 | +0.007333 | -0.000244 | 0.544000 | 0.734400 |
| NanoFEVER | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.530538 | 0.672905 | +0.142367 | 0.928667 | 0.958667 | +0.030000 | -0.000132 | 0.770800 | 0.904000 |
| NanoFEVER | MiniLM | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.438984 | 0.494309 | +0.055326 | 0.838667 | 0.870000 | +0.031333 | +0.035063 | 0.270400 | 0.133200 |
| NanoFEVER | MiniLM | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.438984 | 0.548820 | +0.109836 | 0.838667 | 0.912000 | +0.073333 | +0.035500 | 0.521200 | 0.290800 |
| NanoFEVER | MiniLM | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.438984 | 0.653985 | +0.215001 | 0.838667 | 0.954667 | +0.116000 | +0.035802 | 0.754000 | 0.492800 |
| NanoHotpotQA | E5 | ARC2-Global | Fixed1024 | 25pct | 0.531405 | 0.584486 | +0.053081 | 0.902000 | 0.914000 | +0.012000 | +0.031773 | 0.414400 | 0.168000 |
| NanoHotpotQA | E5 | ARC2-Global | Fixed1024 | 50pct | 0.531405 | 0.672240 | +0.140835 | 0.902000 | 0.930000 | +0.028000 | +0.031830 | 0.598400 | 0.340400 |
| NanoHotpotQA | E5 | ARC2-Global | Fixed1024 | 75pct | 0.531405 | 0.746388 | +0.214983 | 0.902000 | 0.948000 | +0.046000 | +0.031733 | 0.800000 | 0.584000 |
| NanoHotpotQA | E5 | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.537268 | 0.551235 | +0.013966 | 0.904000 | 0.916000 | +0.012000 | +0.013520 | 0.390400 | 0.380800 |
| NanoHotpotQA | E5 | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.537268 | 0.629928 | +0.092660 | 0.904000 | 0.936000 | +0.032000 | +0.013596 | 0.584400 | 0.645600 |
| NanoHotpotQA | E5 | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.537268 | 0.720207 | +0.182939 | 0.904000 | 0.950000 | +0.046000 | +0.013619 | 0.791600 | 0.849600 |
| NanoHotpotQA | E5 | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.361738 | 0.380443 | +0.018706 | 0.848000 | 0.760000 | -0.088000 | +0.136045 | 0.368800 | 0.030800 |
| NanoHotpotQA | E5 | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.361738 | 0.442446 | +0.080708 | 0.848000 | 0.720000 | -0.128000 | +0.136044 | 0.560000 | 0.061600 |
| NanoHotpotQA | E5 | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.361738 | 0.505347 | +0.143609 | 0.848000 | 0.674000 | -0.174000 | +0.135616 | 0.780800 | 0.099600 |
| NanoHotpotQA | MiniLM | ARC2-Global | Fixed1024 | 25pct | 0.344542 | 0.375981 | +0.031439 | 0.792000 | 0.806000 | +0.014000 | +0.018181 | 0.350000 | 0.312400 |
| NanoHotpotQA | MiniLM | ARC2-Global | Fixed1024 | 50pct | 0.344542 | 0.443522 | +0.098980 | 0.792000 | 0.830000 | +0.038000 | +0.018449 | 0.565200 | 0.563200 |
| NanoHotpotQA | MiniLM | ARC2-Global | Fixed1024 | 75pct | 0.344542 | 0.493434 | +0.148892 | 0.792000 | 0.844000 | +0.052000 | +0.017697 | 0.786800 | 0.793600 |
| NanoHotpotQA | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.339025 | 0.336179 | -0.002846 | 0.788000 | 0.808000 | +0.020000 | -0.001314 | 0.337200 | 0.548400 |
| NanoHotpotQA | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.339025 | 0.410956 | +0.071931 | 0.788000 | 0.824000 | +0.036000 | -0.001107 | 0.557200 | 0.805600 |
| NanoHotpotQA | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.339025 | 0.478114 | +0.139090 | 0.788000 | 0.842000 | +0.054000 | -0.001538 | 0.784000 | 0.937600 |
| NanoHotpotQA | MiniLM | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.307964 | 0.350533 | +0.042569 | 0.764000 | 0.750000 | -0.014000 | +0.082128 | 0.286400 | 0.095600 |
| NanoHotpotQA | MiniLM | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.307964 | 0.416879 | +0.108915 | 0.764000 | 0.766000 | +0.002000 | +0.082614 | 0.526000 | 0.205200 |
| NanoHotpotQA | MiniLM | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.307964 | 0.472982 | +0.165018 | 0.764000 | 0.782000 | +0.018000 | +0.081695 | 0.771200 | 0.357600 |
| NanoNQ | E5 | ARC2-Global | Fixed1024 | 25pct | 0.493646 | 0.507124 | +0.013478 | 0.980000 | 0.956000 | -0.024000 | +0.028792 | 0.366400 | 0.180400 |
| NanoNQ | E5 | ARC2-Global | Fixed1024 | 50pct | 0.493646 | 0.544348 | +0.050702 | 0.980000 | 0.956000 | -0.024000 | +0.029011 | 0.586800 | 0.387200 |
| NanoNQ | E5 | ARC2-Global | Fixed1024 | 75pct | 0.493646 | 0.610099 | +0.116453 | 0.980000 | 0.964000 | -0.016000 | +0.029138 | 0.790400 | 0.624400 |
| NanoNQ | E5 | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.492929 | 0.485237 | -0.007692 | 0.976000 | 0.976000 | +0.000000 | +0.014943 | 0.350800 | 0.308400 |
| NanoNQ | E5 | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.492929 | 0.513091 | +0.020162 | 0.976000 | 0.968000 | -0.008000 | +0.015219 | 0.573200 | 0.589200 |
| NanoNQ | E5 | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.492929 | 0.591239 | +0.098310 | 0.976000 | 0.964000 | -0.012000 | +0.015469 | 0.780800 | 0.804000 |
| NanoNQ | E5 | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.282034 | 0.321913 | +0.039880 | 0.876000 | 0.840000 | -0.036000 | +0.135674 | 0.334400 | 0.056000 |
| NanoNQ | E5 | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.282034 | 0.387064 | +0.105031 | 0.876000 | 0.780000 | -0.096000 | +0.135697 | 0.548400 | 0.109200 |
| NanoNQ | E5 | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.282034 | 0.442841 | +0.160807 | 0.876000 | 0.754000 | -0.122000 | +0.135416 | 0.778800 | 0.178800 |
| NanoNQ | MiniLM | ARC2-Global | Fixed1024 | 25pct | 0.520253 | 0.488807 | -0.031446 | 0.966000 | 0.970000 | +0.004000 | +0.003189 | 0.332000 | 0.369200 |
| NanoNQ | MiniLM | ARC2-Global | Fixed1024 | 50pct | 0.520253 | 0.526624 | +0.006372 | 0.966000 | 0.970000 | +0.004000 | +0.003296 | 0.561600 | 0.661200 |
| NanoNQ | MiniLM | ARC2-Global | Fixed1024 | 75pct | 0.520253 | 0.586833 | +0.066580 | 0.966000 | 0.976000 | +0.010000 | +0.003357 | 0.788800 | 0.867600 |
| NanoNQ | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 25pct | 0.502422 | 0.442147 | -0.060274 | 0.964000 | 0.960000 | -0.004000 | -0.000143 | 0.332000 | 0.505200 |
| NanoNQ | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 50pct | 0.502422 | 0.499511 | -0.002911 | 0.964000 | 0.954000 | -0.010000 | -0.000024 | 0.562400 | 0.772800 |
| NanoNQ | MiniLM | A2M / Procrustes adaptation | Fixed1024 | 75pct | 0.502422 | 0.571429 | +0.069007 | 0.964000 | 0.962000 | -0.002000 | +0.000058 | 0.787600 | 0.920800 |
| NanoNQ | MiniLM | Affine ridge, lambda10 | Fixed1024 | 25pct | 0.502106 | 0.480723 | -0.021383 | 0.944000 | 0.922000 | -0.022000 | +0.019422 | 0.292800 | 0.206400 |
| NanoNQ | MiniLM | Affine ridge, lambda10 | Fixed1024 | 50pct | 0.502106 | 0.517769 | +0.015664 | 0.944000 | 0.930000 | -0.014000 | +0.019557 | 0.532800 | 0.404000 |
| NanoNQ | MiniLM | Affine ridge, lambda10 | Fixed1024 | 75pct | 0.502106 | 0.585492 | +0.083386 | 0.944000 | 0.948000 | +0.004000 | +0.019456 | 0.771600 | 0.628800 |

[All diagnostic columns, 90 conditions](diagnostic_tables.csv) · [All 450 seed cases](diagnostic_cases.csv) · [Saved scoring summary](scoring/results_summary.json) · [Rendering provenance](figures/b1g_mixed_gallery_diagnostics_provenance.json)

The CSVs retain paid/proxy populations and top10/top100 shares, overlap and changed-query counts, all four paired strata, errors/quantiles, score dispersion and direction summaries. Condition CSV fields are equal means of saved per-seed summaries, including counts; consult the case CSV for integer counts and the sealed source artifacts for per-query arrays. Empty or undefined quantities are blank/NA. No equal-stratum population estimate is constructed.

Paid populations count unique destination documents |A ∪ S|, anchors included. Cached true vectors and proxy diagnostics are not fresh physical encoding work, a dollar estimate, or an SLO measurement. Nano results are for the published Nano collections. TREC remains outside this campaign.

Generation/scoring commit: `515b3d10b8c09f1900c5215b5b709b47830f3236`; lock SHA256: `ea12eb90173d9b1f9f93883f1efa157946c67a91169d3c6a57f35eef7c316c53`.

STOP after B1-G analysis and the separate ARIS/D1 record. No automatic breadth, TREC or systems campaign.
