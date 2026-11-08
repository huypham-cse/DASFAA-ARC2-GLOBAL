# Fresh paper-to-raw claim audit

Verdict: **PASS within scope**. Same-family / provisional; gpt-6.1-sol, high.

Audited 218 claim records and 101 fresh input hashes. PDF: 16 pages, SHA256 `e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc`.

No numerical, comparison, marker, rank or vector-figure mismatch found. All saved means reconcile to scored per-query arrays: DEV 736 cells/160 means; TREC 184/40; all-paid 124/28; ablation 736/160, each maximum absolute error 0. All eleven TREC daggers and eight all-paid family markers, best/second styling before rounding, 80 TREC metric/native points and all five complete ablation intervals reconcile.

## Found omission and resolution

The initial setup omitted the explicit TREC-COVID primal-backend assignment. The parent corrected the source to distinguish development fixed-anchor dual fits, all-paid/TREC-COVID primal fits, and reused dual fixed-anchor comparisons in the all-paid study. The corrected source and compiled PDF text were reread; the new setup page was rendered and inspected. No numerical or scientific-file change was required.
Initial PDF SHA256: `44473eaa32e0dce707554eff3f76042abf043eb88aa7a3cf6cc7aa4f63bf0128`. Final SHA256: `e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc`. Status: **resolved**.

## Scope and negative evidence

The E5 25%-versus-75% comparison holds on all five collections as a post-hoc descriptive point comparison. The complete raw baseline/native context is retained; no minimum budget, equal-quality or physical-cost assertion is supported or made. Each collection macro leads all five baselines; the second step is positive in 22/24 conditions and all five seed macros. TREC Procrustes is higher in all six unrounded nDCG cells, all Procrustes/LA2M family intervals are unresolved, MiniLM all-paid ridge remains unresolved, and E5 all-paid geometric losses and replacement losses remain visible.

## Limitations

- No qrels opened, ranking rescore, retrieval, encoding, training or new scientific run.
- Saved bootstrap intervals checked against displayed values and implemented construction; the full 20,000-draw bootstrap was not rerun.
- Fresh same-family audit; not independent external review, acceptance scoring or a submission-readiness decision.
- External literature attribution/reproduction accuracy and original human nonexposure were not independently audited.
- Raw claims in the five authorized campaigns only; illustrative mechanism numbers are not empirical evidence.

## Claim-level evidence

### C001 - exact_match
- Location: raw saved per-query reconciliation
- Claim: All dev displayed condition means use all queries and five mapping seeds (one native reference)
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"campaign":"dev","cells":736,"means":160,"max_absolute_error":0.0}`
- Notes: Independent arithmetic on saved scored arrays; no metric recomputation from qrels or rankings.

### C002 - exact_match
- Location: raw saved per-query reconciliation
- Claim: All trec displayed condition means use all queries and five mapping seeds (one native reference)
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"campaign":"trec","cells":184,"means":40,"max_absolute_error":0.0}`
- Notes: Independent arithmetic on saved scored arrays; no metric recomputation from qrels or rankings.

### C003 - exact_match
- Location: raw saved per-query reconciliation
- Claim: All paid displayed condition means use all queries and five mapping seeds (one native reference)
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"campaign":"paid","cells":124,"means":28,"max_absolute_error":0.0}`
- Notes: Independent arithmetic on saved scored arrays; no metric recomputation from qrels or rankings.

### C004 - exact_match
- Location: raw saved per-query reconciliation
- Claim: All ablation displayed condition means use all queries and five mapping seeds (one native reference)
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"campaign":"ablation","cells":736,"means":160,"max_absolute_error":0.0}`
- Notes: Independent arithmetic on saved scored arrays; no metric recomputation from qrels or rankings.

### C005 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: arc2_global_tangent2_r1, numeric column 1: \textbf{0.5275}
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.527477527300496,"rank_among_six":1,"family_decision":null}`

### C006 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: arc2_global_tangent2_r1, numeric column 2: \underline{0.8659}
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.8658612474562474,"rank_among_six":2,"family_decision":null}`

### C007 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: procrustes_global, numeric column 1: \underline{0.5032}
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.5031524182600609,"rank_among_six":2,"family_decision":null}`

### C008 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: procrustes_global, numeric column 2: \textbf{0.8661}
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.8660998378473379,"rank_among_six":1,"family_decision":null}`

### C009 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ARC2 minus procrustes_global, difference and family interval
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ci95":[0.01955835392729735,0.029207604573451666],"descriptive":false,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.018132175212397208,0.030791640313948616],"per_interval_confidence":0.99,"family_interval_interpretation":"above_zero","delta":0.024325109040435233,"ci95_descriptive":true}`

### C010 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: la2m20_integration_script_adaptation, numeric column 1: 0.4234
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.42342257351929274,"rank_among_six":4,"family_decision":null}`

### C011 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: la2m20_integration_script_adaptation, numeric column 2: 0.7758
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.7758335509398009,"rank_among_six":3,"family_decision":null}`

### C012 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ARC2 minus la2m20_integration_script_adaptation, difference and family interval
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ci95":[0.09042663100397504,0.11823577560634102],"descriptive":false,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.08607033208524335,0.1229148044499058],"per_interval_confidence":0.99,"family_interval_interpretation":"above_zero","delta":0.10405495378120326,"ci95_descriptive":true}`

### C013 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 1: 0.3554
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.3553776623832738,"rank_among_six":6,"family_decision":null}`

### C014 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 2: 0.6130
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.6129790412827912,"rank_among_six":6,"family_decision":null}`

### C015 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ARC2 minus simplelinear_official_final50_mlp5, difference and family interval
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ci95":[0.15510792403194884,0.18944839086844825],"descriptive":false,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.1498621517850371,0.19470300383538613],"per_interval_confidence":0.99,"family_interval_interpretation":"above_zero","delta":0.1720998649172223,"ci95_descriptive":true}`

### C016 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 1: 0.4318
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.4318244780276741,"rank_among_six":3,"family_decision":null}`

### C017 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 2: 0.7441
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.7441268305305805,"rank_among_six":5,"family_decision":null}`

### C018 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ARC2 minus ridge_affine_l10_bias_regularized, difference and family interval
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ci95":[0.08028494961525619,0.11133148283369526],"descriptive":false,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.07540472081021199,0.11642668663044543],"per_interval_confidence":0.99,"family_interval_interpretation":"above_zero","delta":0.09565304927282199,"ci95_descriptive":true}`

### C019 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: embedding_converter_paper_spec, numeric column 1: 0.3663
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.36631519310915567,"rank_among_six":5,"family_decision":null}`

### C020 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: embedding_converter_paper_spec, numeric column 2: 0.7641
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"mean":0.7641036175861177,"rank_among_six":4,"family_decision":null}`

### C021 - rounding_ok
- Location: generated/dev_macro.tex
- Claim: ARC2 minus embedding_converter_paper_spec, difference and family interval
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ci95":[0.1469872004230708,0.17540768321767883],"descriptive":false,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.14268641175964025,0.17991558284155384],"per_interval_confidence":0.99,"family_interval_interpretation":"above_zero","delta":0.16116233419134046,"ci95_descriptive":true}`

### C022 - rounding_ok
- Location: generated/trec_means.tex
- Claim: arc2_global_tangent2_r1, numeric column 1: 0.4619
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4619132237639601,"rank_among_six":3,"family_decision":null}`

### C023 - rounding_ok
- Location: generated/trec_means.tex
- Claim: arc2_global_tangent2_r1, numeric column 2: 0.5000
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4999550226735597,"rank_among_six":4,"family_decision":null}`

### C024 - rounding_ok
- Location: generated/trec_means.tex
- Claim: arc2_global_tangent2_r1, numeric column 3: \underline{0.5195}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.519513052034007,"rank_among_six":2,"family_decision":null}`

### C025 - rounding_ok
- Location: generated/trec_means.tex
- Claim: arc2_global_tangent2_r1, numeric column 4: \underline{0.5628}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.562801573213321,"rank_among_six":2,"family_decision":null}`

### C026 - rounding_ok
- Location: generated/trec_means.tex
- Claim: arc2_global_tangent2_r1, numeric column 5: \underline{0.5904}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5904061066004364,"rank_among_six":2,"family_decision":null}`

### C027 - rounding_ok
- Location: generated/trec_means.tex
- Claim: arc2_global_tangent2_r1, numeric column 6: 0.6098 \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.6097818790197872,"rank_among_six":3,"family_decision":null}`

### C028 - rounding_ok
- Location: generated/trec_means.tex
- Claim: procrustes_global, numeric column 1: \underline{0.4620}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.46196458443251165,"rank_among_six":2,"family_decision":"unresolved"}`

### C029 - rounding_ok
- Location: generated/trec_means.tex
- Claim: procrustes_global, numeric column 2: 0.5046
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5046218931387791,"rank_among_six":3,"family_decision":"unresolved"}`

### C030 - rounding_ok
- Location: generated/trec_means.tex
- Claim: procrustes_global, numeric column 3: \textbf{0.5195}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5195366169586203,"rank_among_six":1,"family_decision":"unresolved"}`

### C031 - rounding_ok
- Location: generated/trec_means.tex
- Claim: procrustes_global, numeric column 4: \textbf{0.5660}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5660420017846071,"rank_among_six":1,"family_decision":"unresolved"}`

### C032 - rounding_ok
- Location: generated/trec_means.tex
- Claim: procrustes_global, numeric column 5: \textbf{0.6067}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.606727648648923,"rank_among_six":1,"family_decision":"unresolved"}`

### C033 - rounding_ok
- Location: generated/trec_means.tex
- Claim: procrustes_global, numeric column 6: \textbf{0.6198} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.6197938386784891,"rank_among_six":1,"family_decision":"unresolved"}`

### C034 - rounding_ok
- Location: generated/trec_means.tex
- Claim: la2m20_integration_script_adaptation, numeric column 1: \textbf{0.4634}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4634176232530495,"rank_among_six":1,"family_decision":"unresolved"}`

### C035 - rounding_ok
- Location: generated/trec_means.tex
- Claim: la2m20_integration_script_adaptation, numeric column 2: \underline{0.5073}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5072760250312146,"rank_among_six":2,"family_decision":"unresolved"}`

### C036 - rounding_ok
- Location: generated/trec_means.tex
- Claim: la2m20_integration_script_adaptation, numeric column 3: 0.5186
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5185617727755863,"rank_among_six":4,"family_decision":"unresolved"}`

### C037 - rounding_ok
- Location: generated/trec_means.tex
- Claim: la2m20_integration_script_adaptation, numeric column 4: 0.5206
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5205904360903386,"rank_among_six":3,"family_decision":"unresolved"}`

### C038 - rounding_ok
- Location: generated/trec_means.tex
- Claim: la2m20_integration_script_adaptation, numeric column 5: 0.5898
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5898118524012599,"rank_among_six":3,"family_decision":"unresolved"}`

### C039 - rounding_ok
- Location: generated/trec_means.tex
- Claim: la2m20_integration_script_adaptation, numeric column 6: \underline{0.6188} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.6187771807287994,"rank_among_six":2,"family_decision":"unresolved"}`

### C040 - rounding_ok
- Location: generated/trec_means.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 1: 0.4610
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.46104030699300225,"rank_among_six":4,"family_decision":"unresolved"}`

### C041 - rounding_ok
- Location: generated/trec_means.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 2: \textbf{0.5076}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5075901623712186,"rank_among_six":1,"family_decision":"unresolved"}`

### C042 - rounding_ok
- Location: generated/trec_means.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 3: 0.5193
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5193021992613991,"rank_among_six":3,"family_decision":"unresolved"}`

### C043 - rounding_ok
- Location: generated/trec_means.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 4: 0.4299$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.42992858085823116,"rank_among_six":4,"family_decision":"above_zero"}`

### C044 - rounding_ok
- Location: generated/trec_means.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 5: 0.5287$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5286762204098695,"rank_among_six":4,"family_decision":"above_zero"}`

### C045 - rounding_ok
- Location: generated/trec_means.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 6: 0.5785 \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5784937222630202,"rank_among_six":4,"family_decision":"unresolved"}`

### C046 - rounding_ok
- Location: generated/trec_means.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 1: 0.4322
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4321704122423191,"rank_among_six":5,"family_decision":"unresolved"}`

### C047 - rounding_ok
- Location: generated/trec_means.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 2: 0.4854
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.48543765007369555,"rank_among_six":5,"family_decision":"unresolved"}`

### C048 - rounding_ok
- Location: generated/trec_means.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 3: 0.5012$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5012195177689744,"rank_among_six":6,"family_decision":"above_zero"}`

### C049 - rounding_ok
- Location: generated/trec_means.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 4: 0.2986$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.29862101762519416,"rank_among_six":6,"family_decision":"above_zero"}`

### C050 - rounding_ok
- Location: generated/trec_means.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 5: 0.3281$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.3281386648638847,"rank_among_six":6,"family_decision":"above_zero"}`

### C051 - rounding_ok
- Location: generated/trec_means.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 6: 0.3278$^{\dagger}$ \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.3277848331657977,"rank_among_six":6,"family_decision":"above_zero"}`

### C052 - rounding_ok
- Location: generated/trec_means.tex
- Claim: embedding_converter_paper_spec, numeric column 1: 0.4224$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4223735991713406,"rank_among_six":6,"family_decision":"above_zero"}`

### C053 - rounding_ok
- Location: generated/trec_means.tex
- Claim: embedding_converter_paper_spec, numeric column 2: 0.4780$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4780470274050105,"rank_among_six":6,"family_decision":"above_zero"}`

### C054 - rounding_ok
- Location: generated/trec_means.tex
- Claim: embedding_converter_paper_spec, numeric column 3: 0.5033
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5032547704761722,"rank_among_six":5,"family_decision":"unresolved"}`

### C055 - rounding_ok
- Location: generated/trec_means.tex
- Claim: embedding_converter_paper_spec, numeric column 4: 0.3056$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.3055679824401268,"rank_among_six":5,"family_decision":"above_zero"}`

### C056 - rounding_ok
- Location: generated/trec_means.tex
- Claim: embedding_converter_paper_spec, numeric column 5: 0.3590$^{\dagger}$
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.3590215314302837,"rank_among_six":5,"family_decision":"above_zero"}`

### C057 - rounding_ok
- Location: generated/trec_means.tex
- Claim: embedding_converter_paper_spec, numeric column 6: 0.4098$^{\dagger}$ \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.40982778236858286,"rank_among_six":5,"family_decision":"above_zero"}`

### C058 - rounding_ok
- Location: generated/trec_means.tex
- Claim: full_x, numeric column 1: \multicolumn{3}{c}{0.4935 (native)}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.4934781848463412,"rank_among_six":null,"family_decision":null}`

### C059 - rounding_ok
- Location: generated/trec_means.tex
- Claim: full_x, numeric column 2: \multicolumn{3}{c}{0.6805 (native)} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.6805416492225224,"rank_among_six":null,"family_decision":null}`

### C060 - rounding_ok
- Location: generated/trec_means.tex
- Claim: full_y, numeric column 1: \multicolumn{3}{c}{0.5203 (native)}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.5202728348242263,"rank_among_six":null,"family_decision":null}`

### C061 - rounding_ok
- Location: generated/trec_means.tex
- Claim: full_y, numeric column 2: \multicolumn{3}{c}{0.6421 (native)} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.6421134496001705,"rank_among_six":null,"family_decision":null}`

### C062 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: arc2_global_tangent2_r1, numeric column 1: \textbf{0.0896}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08963088480259038,"rank_among_six":1,"family_decision":null}`

### C063 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: arc2_global_tangent2_r1, numeric column 2: \textbf{0.0953}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09529158965710632,"rank_among_six":1,"family_decision":null}`

### C064 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: arc2_global_tangent2_r1, numeric column 3: \textbf{0.0998}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09983604059514704,"rank_among_six":1,"family_decision":null}`

### C065 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: arc2_global_tangent2_r1, numeric column 4: \underline{0.0866}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.0865798155941492,"rank_among_six":2,"family_decision":null}`

### C066 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: arc2_global_tangent2_r1, numeric column 5: \underline{0.0928}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09284227251463124,"rank_among_six":2,"family_decision":null}`

### C067 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: arc2_global_tangent2_r1, numeric column 6: 0.0997 \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09966692928143464,"rank_among_six":3,"family_decision":null}`

### C068 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: procrustes_global, numeric column 1: \underline{0.0866}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08656849639226609,"rank_among_six":2,"family_decision":null}`

### C069 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: procrustes_global, numeric column 2: \underline{0.0935}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09348540930621103,"rank_among_six":2,"family_decision":null}`

### C070 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: procrustes_global, numeric column 3: \underline{0.0994}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09942876429633421,"rank_among_six":2,"family_decision":null}`

### C071 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: procrustes_global, numeric column 4: \textbf{0.0886}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08857103007611913,"rank_among_six":1,"family_decision":null}`

### C072 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: procrustes_global, numeric column 5: \textbf{0.0976}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09757526289269891,"rank_among_six":1,"family_decision":null}`

### C073 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: procrustes_global, numeric column 6: \textbf{0.1061} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.10605638073803039,"rank_among_six":1,"family_decision":null}`

### C074 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: la2m20_integration_script_adaptation, numeric column 1: 0.0736
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.07356777060172419,"rank_among_six":3,"family_decision":null}`

### C075 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: la2m20_integration_script_adaptation, numeric column 2: 0.0884
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08842284023887333,"rank_among_six":3,"family_decision":null}`

### C076 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: la2m20_integration_script_adaptation, numeric column 3: 0.0983
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09826954011884906,"rank_among_six":3,"family_decision":null}`

### C077 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: la2m20_integration_script_adaptation, numeric column 4: 0.0593
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.059325559835467855,"rank_among_six":3,"family_decision":null}`

### C078 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: la2m20_integration_script_adaptation, numeric column 5: 0.0823
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08234134077914587,"rank_among_six":3,"family_decision":null}`

### C079 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: la2m20_integration_script_adaptation, numeric column 6: \underline{0.1016} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.10159163083373099,"rank_among_six":2,"family_decision":null}`

### C080 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 1: 0.0626
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.06257470519773327,"rank_among_six":6,"family_decision":null}`

### C081 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 2: 0.0845
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.0844776701539496,"rank_among_six":4,"family_decision":null}`

### C082 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 3: 0.0970
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09701627700333974,"rank_among_six":4,"family_decision":null}`

### C083 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 4: 0.0296
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.029643592077240412,"rank_among_six":6,"family_decision":null}`

### C084 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 5: 0.0510
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.05097373668709944,"rank_among_six":4,"family_decision":null}`

### C085 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 6: 0.0693 \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.06928258053412745,"rank_among_six":4,"family_decision":null}`

### C086 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 1: 0.0689
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.06890134085023747,"rank_among_six":4,"family_decision":null}`

### C087 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 2: 0.0780
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.0779944968405071,"rank_among_six":5,"family_decision":null}`

### C088 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 3: 0.0856
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08563775429812863,"rank_among_six":6,"family_decision":null}`

### C089 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 4: 0.0373
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.03726425994631427,"rank_among_six":5,"family_decision":null}`

### C090 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 5: 0.0382
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.038217266219315385,"rank_among_six":6,"family_decision":null}`

### C091 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 6: 0.0366 \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.03657015555736688,"rank_among_six":6,"family_decision":null}`

### C092 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: embedding_converter_paper_spec, numeric column 1: 0.0651
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.06512050655177726,"rank_among_six":5,"family_decision":null}`

### C093 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: embedding_converter_paper_spec, numeric column 2: 0.0772
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.07717310564196894,"rank_among_six":6,"family_decision":null}`

### C094 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: embedding_converter_paper_spec, numeric column 3: 0.0892
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.08920092316113651,"rank_among_six":5,"family_decision":null}`

### C095 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: embedding_converter_paper_spec, numeric column 4: 0.0422
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.042248049007770475,"rank_among_six":4,"family_decision":null}`

### C096 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: embedding_converter_paper_spec, numeric column 5: 0.0495
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.04951179253245391,"rank_among_six":5,"family_decision":null}`

### C097 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: embedding_converter_paper_spec, numeric column 6: 0.0582 \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.05824037110988424,"rank_among_six":5,"family_decision":null}`

### C098 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: full_x, numeric column 1: \multicolumn{3}{c}{0.0936 (native)}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.09355341420637212,"rank_among_six":null,"family_decision":null}`

### C099 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: full_x, numeric column 2: \multicolumn{3}{c}{0.1235 (native)} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.12353038057812048,"rank_among_six":null,"family_decision":null}`

### C100 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: full_y, numeric column 1: \multicolumn{3}{c}{0.1052 (native)}
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.10521378018323918,"rank_among_six":null,"family_decision":null}`

### C101 - rounding_ok
- Location: generated/trec_recall.tex
- Claim: full_y, numeric column 2: \multicolumn{3}{c}{0.1162 (native)} \\
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"mean":0.11624395516879528,"rank_among_six":null,"family_decision":null}`

### C102 - rounding_ok
- Location: generated/allpaid.tex
- Claim: arc2_global_tangent2_r1, numeric column 1: \textbf{0.3075}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3075048582716371,"rank_among_six":1,"family_decision":null}`

### C103 - rounding_ok
- Location: generated/allpaid.tex
- Claim: arc2_global_tangent2_r1, numeric column 2: \underline{0.3671}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.36714602143626496,"rank_among_six":2,"family_decision":null}`

### C104 - rounding_ok
- Location: generated/allpaid.tex
- Claim: arc2_global_tangent2_r1, numeric column 3: \underline{0.6922}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6922001554001553,"rank_among_six":2,"family_decision":null}`

### C105 - rounding_ok
- Location: generated/allpaid.tex
- Claim: arc2_global_tangent2_r1, numeric column 4: \textbf{0.3116}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3116352075358866,"rank_among_six":1,"family_decision":null}`

### C106 - rounding_ok
- Location: generated/allpaid.tex
- Claim: arc2_global_tangent2_r1, numeric column 5: 0.2919
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.29186698206096195,"rank_among_six":3,"family_decision":null}`

### C107 - rounding_ok
- Location: generated/allpaid.tex
- Claim: arc2_global_tangent2_r1, numeric column 6: 0.5595 \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.5594899234099235,"rank_among_six":4,"family_decision":null}`

### C108 - rounding_ok
- Location: generated/allpaid.tex
- Claim: procrustes_global, numeric column 1: 0.2858
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.28582824088854003,"rank_among_six":3,"family_decision":null}`

### C109 - rounding_ok
- Location: generated/allpaid.tex
- Claim: procrustes_global, numeric column 2: 0.3334$^{\dagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3333864741159597,"rank_among_six":4,"family_decision":"above_zero"}`

### C110 - rounding_ok
- Location: generated/allpaid.tex
- Claim: procrustes_global, numeric column 3: 0.6905
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6904948307248308,"rank_among_six":3,"family_decision":null}`

### C111 - rounding_ok
- Location: generated/allpaid.tex
- Claim: procrustes_global, numeric column 4: \underline{0.3100}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.31003589203103826,"rank_among_six":2,"family_decision":null}`

### C112 - rounding_ok
- Location: generated/allpaid.tex
- Claim: procrustes_global, numeric column 5: \textbf{0.3362}$^{\ddagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.33620246107664287,"rank_among_six":1,"family_decision":"below_zero"}`

### C113 - rounding_ok
- Location: generated/allpaid.tex
- Claim: procrustes_global, numeric column 6: \textbf{0.6534} \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.653388922188922,"rank_among_six":1,"family_decision":null}`

### C114 - rounding_ok
- Location: generated/allpaid.tex
- Claim: la2m20_integration_script_adaptation, numeric column 1: 0.2377
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.2376740142398725,"rank_among_six":5,"family_decision":null}`

### C115 - rounding_ok
- Location: generated/allpaid.tex
- Claim: la2m20_integration_script_adaptation, numeric column 2: 0.3389$^{\dagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3389234669245038,"rank_among_six":3,"family_decision":"above_zero"}`

### C116 - rounding_ok
- Location: generated/allpaid.tex
- Claim: la2m20_integration_script_adaptation, numeric column 3: \textbf{0.6950}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.695005148185148,"rank_among_six":1,"family_decision":null}`

### C117 - rounding_ok
- Location: generated/allpaid.tex
- Claim: la2m20_integration_script_adaptation, numeric column 4: 0.2300
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.22999031724981683,"rank_among_six":3,"family_decision":null}`

### C118 - rounding_ok
- Location: generated/allpaid.tex
- Claim: la2m20_integration_script_adaptation, numeric column 5: \underline{0.3293}$^{\ddagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3293413014310004,"rank_among_six":2,"family_decision":"below_zero"}`

### C119 - rounding_ok
- Location: generated/allpaid.tex
- Claim: la2m20_integration_script_adaptation, numeric column 6: \underline{0.6473} \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6473306193806192,"rank_among_six":2,"family_decision":null}`

### C120 - rounding_ok
- Location: generated/allpaid.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 1: 0.2360
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.2359531204225403,"rank_among_six":6,"family_decision":null}`

### C121 - rounding_ok
- Location: generated/allpaid.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 2: 0.3323$^{\dagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3323162470088491,"rank_among_six":5,"family_decision":"above_zero"}`

### C122 - rounding_ok
- Location: generated/allpaid.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 3: 0.6778
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6777889244089242,"rank_among_six":5,"family_decision":null}`

### C123 - rounding_ok
- Location: generated/allpaid.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 4: 0.1942
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.1941674316269752,"rank_among_six":4,"family_decision":null}`

### C124 - rounding_ok
- Location: generated/allpaid.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 5: 0.1679$^{\dagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.16794940738858383,"rank_among_six":6,"family_decision":"above_zero"}`

### C125 - rounding_ok
- Location: generated/allpaid.tex
- Claim: simplelinear_official_final50_mlp5, numeric column 6: 0.3618 \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3617845476745477,"rank_among_six":6,"family_decision":null}`

### C126 - rounding_ok
- Location: generated/allpaid.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 1: \underline{0.2890}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.28904545781234714,"rank_among_six":2,"family_decision":null}`

### C127 - rounding_ok
- Location: generated/allpaid.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 2: \textbf{0.3673}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.36726327671078884,"rank_among_six":1,"family_decision":"unresolved"}`

### C128 - rounding_ok
- Location: generated/allpaid.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 3: 0.6800
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6800430125430126,"rank_among_six":4,"family_decision":null}`

### C129 - rounding_ok
- Location: generated/allpaid.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 4: 0.1479
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.14792156930525965,"rank_among_six":5,"family_decision":null}`

### C130 - rounding_ok
- Location: generated/allpaid.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 5: 0.2270$^{\dagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.2270145751549427,"rank_among_six":5,"family_decision":"above_zero"}`

### C131 - rounding_ok
- Location: generated/allpaid.tex
- Claim: ridge_affine_l10_bias_regularized, numeric column 6: 0.4245 \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.42451112110112116,"rank_among_six":5,"family_decision":null}`

### C132 - rounding_ok
- Location: generated/allpaid.tex
- Claim: embedding_converter_paper_spec, numeric column 1: 0.2496
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.24963647764120794,"rank_among_six":4,"family_decision":null}`

### C133 - rounding_ok
- Location: generated/allpaid.tex
- Claim: embedding_converter_paper_spec, numeric column 2: 0.3258$^{\dagger}$
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.32576143937636975,"rank_among_six":6,"family_decision":"above_zero"}`

### C134 - rounding_ok
- Location: generated/allpaid.tex
- Claim: embedding_converter_paper_spec, numeric column 3: 0.6633
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6632694838494837,"rank_among_six":6,"family_decision":null}`

### C135 - rounding_ok
- Location: generated/allpaid.tex
- Claim: embedding_converter_paper_spec, numeric column 4: 0.1397
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.1396653650449041,"rank_among_six":6,"family_decision":null}`

### C136 - rounding_ok
- Location: generated/allpaid.tex
- Claim: embedding_converter_paper_spec, numeric column 5: 0.2625
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.2625194643556271,"rank_among_six":4,"family_decision":"unresolved"}`

### C137 - rounding_ok
- Location: generated/allpaid.tex
- Claim: embedding_converter_paper_spec, numeric column 6: 0.5789 \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.5789074192474193,"rank_among_six":3,"family_decision":null}`

### C138 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_x, numeric column 1: \multicolumn{2}{c}{0.3900 (native)}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.38996146433493817,"rank_among_six":null,"family_decision":null}`

### C139 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_x, numeric column 2: 0.7002
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.7001835830835832,"rank_among_six":null,"family_decision":null}`

### C140 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_x, numeric column 3: \multicolumn{2}{c}{0.3465 (native)}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3464782895762744,"rank_among_six":null,"family_decision":null}`

### C141 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_x, numeric column 4: 0.6453 \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6453320235320233,"rank_among_six":null,"family_decision":null}`

### C142 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_y, numeric column 1: \multicolumn{2}{c}{0.4047 (native)}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.4047359707946925,"rank_among_six":null,"family_decision":null}`

### C143 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_y, numeric column 2: 0.7039
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.703892218892219,"rank_among_six":null,"family_decision":null}`

### C144 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_y, numeric column 3: \multicolumn{2}{c}{0.3891 (native)}
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.3891325249294525,"rank_among_six":null,"family_decision":null}`

### C145 - rounding_ok
- Location: generated/allpaid.tex
- Claim: full_y, numeric column 4: 0.6968 \\
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"mean":0.6967968586968585,"rank_among_six":null,"family_decision":null}`

### C146 - rounding_ok
- Location: generated/ablation.tex
- Claim: Two steps minus zero steps & +0.0243 & [+0.0180, +0.0310] \\
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.024325109040435233,"ci95":[0.0195818675697136,0.029318485952316592],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.024325109040435233,"seed_std":0.004726550116148564,"seed_range":[0.017365688970446512,0.030638076764707856],"seeds":5},"ci99_bonferroni_family95":[0.01801533254696277,0.03102132243820168],"family_interval_interpretation":"above_zero"}`

### C147 - rounding_ok
- Location: generated/ablation.tex
- Claim: Two steps minus one step & +0.0069 & [+0.0038, +0.0100] \\
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.006923862939737235,"ci95":[0.004584432900988409,0.009226028099450147],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.006923862939737235,"seed_std":0.0020084533271641346,"seed_range":[0.003827292446927387,0.009036945683211683],"seeds":5},"ci99_bonferroni_family95":[0.003809388309482942,0.009959126205904258],"family_interval_interpretation":"above_zero"}`

### C148 - rounding_ok
- Location: generated/ablation.tex
- Claim: ARC2 minus affine ridge & +0.0957 & [+0.0754, +0.1166] \\
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.09565304927282199,"ci95":[0.08032542616520105,0.11153533924165686],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.09565304927282199,"seed_std":0.004068923683907757,"seed_range":[0.090691014279143,0.10139112119859749],"seeds":5},"ci99_bonferroni_family95":[0.07535298921225946,0.11663127039230592],"family_interval_interpretation":"above_zero"}`

### C149 - rounding_ok
- Location: generated/ablation.tex
- Claim: $\lambda=1$ minus $\lambda=10$ & +0.0032 & [-0.0019, +0.0083] \\
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.0031974956912717346,"ci95":[-0.0007402431692805767,0.007157619090496026],"descriptive":true,"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":0.0031974956912717337,"seed_std":0.0014261530566855027,"seed_range":[0.0014511899112586958,0.005359535138351684],"seeds":5},"ci99_bonferroni_family95":[-0.0018903844098364442,0.00830403326634241],"family_interval_interpretation":"unresolved"}`

### C150 - rounding_ok
- Location: generated/ablation.tex
- Claim: $\lambda=100$ minus $\lambda=10$ & -0.0093 & [-0.0132, -0.0055] \\
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":-0.00925533869678723,"ci95":[-0.012286411062820052,-0.006335315068491882],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.00925533869678723,"seed_std":0.0032250020729826744,"seed_range":[-0.014885255917325473,-0.006946294267227517],"seeds":5},"ci99_bonferroni_family95":[-0.01321398029023485,-0.005510245768211927],"family_interval_interpretation":"below_zero"}`

### C151 - rounding_ok
- Location: abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion
- Claim: E5 ARC2 25% > ridge75% and Converter75%, FiQA
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ARC2_25":0.27310684220470094,"Procrustes_25":0.2717780394485493,"LA2M_25":0.14157395302032982,"SimpleLinear_75":0.2781397818845367,"ridge_75":0.1609714907578672,"Converter_75":0.2095336751807801,"native_X":0.3464782895762744,"native_Y":0.3891325249294525}`
- Notes: Post-hoc descriptive cross-budget point comparison, no additional test, minimum-cost, equivalence or physical-savings claim. Full raw baseline panel retained elsewhere.

### C152 - rounding_ok
- Location: abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion
- Claim: E5 ARC2 25% > ridge75% and Converter75%, NanoNQ
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ARC2_25":0.5071236847804641,"Procrustes_25":0.48523704628244235,"LA2M_25":0.36403641053270247,"SimpleLinear_75":0.48387757204577336,"ridge_75":0.44284099940693855,"Converter_75":0.40208721230157407,"native_X":0.6595104530695758,"native_Y":0.6669078991393519}`
- Notes: Post-hoc descriptive cross-budget point comparison, no additional test, minimum-cost, equivalence or physical-savings claim. Full raw baseline panel retained elsewhere.

### C153 - rounding_ok
- Location: abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion
- Claim: E5 ARC2 25% > ridge75% and Converter75%, NanoHotpotQA
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ARC2_25":0.5844856557302884,"Procrustes_25":0.5512346178902974,"LA2M_25":0.38689849635905205,"SimpleLinear_75":0.6173880843274537,"ridge_75":0.5053470075849882,"Converter_75":0.5016332374347163,"native_X":0.8277532428383954,"native_Y":0.8192540193891485}`
- Notes: Post-hoc descriptive cross-budget point comparison, no additional test, minimum-cost, equivalence or physical-savings claim. Full raw baseline panel retained elsewhere.

### C154 - rounding_ok
- Location: abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion
- Claim: E5 ARC2 25% > ridge75% and Converter75%, NanoFEVER
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"ARC2_25":0.7554512732607813,"Procrustes_25":0.714661665844085,"LA2M_25":0.4990506224837599,"SimpleLinear_75":0.7087460112987809,"ridge_75":0.7289860142730652,"Converter_75":0.7325762381767909,"native_X":0.898352760618845,"native_Y":0.8963290572938694}`
- Notes: Post-hoc descriptive cross-budget point comparison, no additional test, minimum-cost, equivalence or physical-savings claim. Full raw baseline panel retained elsewhere.

### C155 - rounding_ok
- Location: abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion
- Claim: E5 ARC2 25% > ridge75% and Converter75%, TREC-COVID
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"ARC2_25":0.562801573213321,"Procrustes_25":0.5660420017846071,"LA2M_25":0.5205904360903386,"SimpleLinear_75":0.5784937222630202,"ridge_75":0.3277848331657977,"Converter_75":0.40982778236858286,"native_X":0.6805416492225224,"native_Y":0.6421134496001705}`
- Notes: Post-hoc descriptive cross-budget point comparison, no additional test, minimum-cost, equivalence or physical-savings claim. Full raw baseline panel retained elsewhere.

### C156 - exact_match
- Location: generated/trec_family.tex
- Claim: minilm_distilroberta/procrustes_global: 0/3/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":-5.136066855163088e-05,"ci":[-0.014694745593972814,0.013213525679703809]},{"budget":"50pct","delta":-0.004666870465219521,"ci":[-0.018617590940593846,0.00609852657610738]},{"budget":"75pct","delta":-2.3564924613148544e-05,"ci":[-0.0045045389961348515,0.004383734800061371]}]`

### C157 - exact_match
- Location: generated/trec_family.tex
- Claim: minilm_distilroberta/la2m20_integration_script_adaptation: 0/3/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":-0.001504399489089405,"ci":[-0.03430576267376661,0.02907870839908143]},{"budget":"50pct","delta":-0.007321002357654939,"ci":[-0.026682539889838944,0.007137508111023871]},{"budget":"75pct","delta":0.0009512792584207396,"ci":[-0.006116292591115391,0.008780612423464904]}]`

### C158 - exact_match
- Location: generated/trec_family.tex
- Claim: minilm_distilroberta/simplelinear_official_final50_mlp5: 0/3/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.0008729167709579025,"ci":[-0.03294484894780953,0.032548466682588796]},{"budget":"50pct","delta":-0.007635139697658929,"ci":[-0.027397841906307695,0.0069215980242743015]},{"budget":"75pct","delta":0.00021085277260803745,"ci":[-0.006827535661738342,0.008018776860536694]}]`

### C159 - exact_match
- Location: generated/trec_family.tex
- Claim: minilm_distilroberta/ridge_affine_l10_bias_regularized: 1/2/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.02974281152164104,"ci":[-0.004477666541051713,0.06832583936849443]},{"budget":"50pct","delta":0.014517372599864117,"ci":[-0.01079865042649303,0.04209814796750806]},{"budget":"75pct","delta":0.01829353426503278,"ci":[0.00043951281706854317,0.04492339866433025]}]`

### C160 - exact_match
- Location: generated/trec_family.tex
- Claim: minilm_distilroberta/embedding_converter_paper_spec: 2/1/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.03953962459261952,"ci":[0.0006302196978609639,0.07561331897623641]},{"budget":"50pct","delta":0.02190799526854917,"ci":[0.0005178011321619429,0.04263918301944054]},{"budget":"75pct","delta":0.016258281557834944,"ci":[-4.496385125866207e-05,0.03208424943554028]}]`

### C161 - exact_match
- Location: generated/trec_family.tex
- Claim: e5_small_base/procrustes_global: 0/3/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":-0.0032404285712858832,"ci":[-0.021620914986484444,0.01432474395822758]},{"budget":"50pct","delta":-0.01632154204848677,"ci":[-0.03982012404542802,0.0022978122002522048]},{"budget":"75pct","delta":-0.010011959658702082,"ci":[-0.0260053875353406,0.0036310901422503547]}]`

### C162 - exact_match
- Location: generated/trec_family.tex
- Claim: e5_small_base/la2m20_integration_script_adaptation: 0/3/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.04221113712298237,"ci":[-0.006416733787802239,0.09332456219941979]},{"budget":"50pct","delta":0.0005942541991765067,"ci":[-0.03551296863593118,0.03599603191311822]},{"budget":"75pct","delta":-0.008995301709012363,"ci":[-0.03577940334852425,0.01564579912460651]}]`

### C163 - exact_match
- Location: generated/trec_family.tex
- Claim: e5_small_base/simplelinear_official_final50_mlp5: 2/1/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.13287299235509,"ci":[0.0633001667256504,0.2051373777778217]},{"budget":"50pct","delta":0.06172988619056692,"ci":[0.01356012047442979,0.11446072714102258]},{"budget":"75pct","delta":0.0312881567567668,"ci":[-0.0038296168793180924,0.07170478814697445]}]`

### C164 - exact_match
- Location: generated/trec_family.tex
- Claim: e5_small_base/ridge_affine_l10_bias_regularized: 3/0/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.2641805555881269,"ci":[0.15726462442241934,0.37675795247986166]},{"budget":"50pct","delta":0.2622674417365517,"ci":[0.1579593697473118,0.37285038597163384]},{"budget":"75pct","delta":0.2819970458539894,"ci":[0.17480022770218387,0.3973296904795432]}]`

### C165 - exact_match
- Location: generated/trec_family.tex
- Claim: e5_small_base/embedding_converter_paper_spec: 3/0/0
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"budget":"25pct","delta":0.25723359077319435,"ci":[0.17573076152800798,0.33756850203860655]},{"budget":"50pct","delta":0.23138457517015265,"ci":[0.15671745879653792,0.3085072832020045]},{"budget":"75pct","delta":0.1999540966512042,"ci":[0.13925018639424472,0.2642221645268023]}]`

### C166 - exact_match
- Location: abstract; introduction; results 5.1; conclusion
- Claim: Each of four collection-level macros and the 24-condition overall macro leads all five baselines
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"by_collection":{"FiQA":{"arc2_global_tangent2_r1":0.3111039850390147,"procrustes_global":0.30119182263656136,"la2m20_integration_script_adaptation":0.23247146785399742,"simplelinear_official_final50_mlp5":0.21351933197073455,"ridge_affine_l10_bias_regularized":0.21956240829761495,"embedding_converter_paper_spec":0.19708258908857876},"NanoNQ":{"arc2_global_tangent2_r1":0.5439724983443252,"procrustes_global":0.5171089253286802,"la2m20_integration_script_adaptation":0.4418450629614456,"simplelinear_official_final50_mlp5":0.3465293299705576,"ridge_affine_l10_bias_regularized":0.4559672592164244,"embedding_converter_paper_spec":0.3735312220251952},"NanoHotpotQA":{"arc2_global_tangent2_r1":0.552674934505062,"procrustes_global":0.521103205055709,"la2m20_integration_script_adaptation":0.44614344522530164,"simplelinear_official_final50_mlp5":0.38734425335759665,"ridge_affine_l10_bias_regularized":0.42810517133591813,"embedding_converter_paper_spec":0.3513066259751241},"NanoFEVER":{"arc2_global_tangent2_r1":0.7021586913135823,"procrustes_global":0.6732057200192928,"la2m20_integration_script_adaptation":0.5732303180364265,"simplelinear_official_final50_mlp5":0.4741177342342063,"ridge_affine_l10_bias_regularized":0.6236630732607388,"embedding_converter_paper_spec":0.5433403353477244}},"overall":{"arc2_global_tangent2_r1":0.527477527300496,"procrustes_global":0.5031524182600609,"la2m20_integration_script_adaptation":0.42342257351929274,"simplelinear_official_final50_mlp5":0.3553776623832738,"ridge_affine_l10_bias_regularized":0.4318244780276741,"embedding_converter_paper_spec":0.36631519310915567}}`

### C167 - rounding_ok
- Location: results 5.1
- Claim: Pair-wise Procrustes gains 0.0257 MiniLM and 0.0229 E5
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"minilm_distilroberta":0.02573293623675471,"e5_small_base":0.022917281844115567}`

### C168 - exact_match
- Location: results 5.1
- Claim: Positive condition point differences versus procrustes_global
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"positive":23,"total":24,"nonpositive":[{"dataset":"FiQA","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"procrustes_global","ndcg10":{"ci95":[-0.009365669062142961,0.0022535550787560824],"descriptive":true,"interval_interpretation":"unresolved","delta":-0.00358268756650346,"mapping_seed_variability":{"mean":-0.0035826875665034607,"seed_std":0.001962039753675562,"seed_range":[-0.005220355283317977,-0.00018994209096128033],"seeds":5}},"recall100":{"ci95":[-0.028262431096681098,-0.00640759740259741],"descriptive":true,"interval_interpretation":"below_zero","delta":-0.0169761038961039,"mapping_seed_variability":{"mean":-0.0169761038961039,"seed_std":0.003127024131562652,"seed_range":[-0.02116515151515152,-0.012976262626262627],"seeds":5}},"familywise":false}]}`

### C169 - exact_match
- Location: results 5.1
- Claim: Positive condition point differences versus la2m20_integration_script_adaptation
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"positive":24,"total":24,"nonpositive":[]}`

### C170 - exact_match
- Location: results 5.1
- Claim: Positive condition point differences versus simplelinear_official_final50_mlp5
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"positive":24,"total":24,"nonpositive":[]}`

### C171 - exact_match
- Location: results 5.1
- Claim: Positive condition point differences versus ridge_affine_l10_bias_regularized
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"positive":24,"total":24,"nonpositive":[]}`

### C172 - exact_match
- Location: results 5.1
- Claim: Positive condition point differences versus embedding_converter_paper_spec
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"positive":24,"total":24,"nonpositive":[]}`

### C173 - rounding_ok
- Location: results 5.1
- Claim: Recall .8659 vs .8661, interval [-.0049,.0043]
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"arc":0.8658612474562474,"proc":0.8660998378473379,"contrast":{"ci95":[-0.004943626172438673,0.0043358499949124945],"descriptive":true,"interval_interpretation":"unresolved","delta":-0.0002385903910903914,"ci95_descriptive":true}}`

### C174 - rounding_ok
- Location: abstract; introduction; results 5.2
- Claim: Second step +.0069 [.0038,.0100], positive in22/24 conditions and each5seedmacros
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"macro":{"delta":0.006923862939737235,"ci95":[0.004584432900988409,0.009226028099450147],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.006923862939737235,"seed_std":0.0020084533271641346,"seed_range":[0.003827292446927387,0.009036945683211683],"seeds":5},"ci99_bonferroni_family95":[0.003809388309482942,0.009959126205904258],"family_interval_interpretation":"above_zero"},"positive_conditions":22,"seed_macros":{"17":0.003827292446927401,"29":0.0061808507543619105,"41":0.007927119071210941,"53":0.007647106742974308,"67":0.009036945683211721},"nonpositive":[{"dataset":"FiQA","pair":"e5_small_base","budget":"50pct","left":"arc2_global_tangent2_r1","right":"tangent1_l10","ndcg10":{"delta":-3.71972846126023e-06,"ci95":[-0.0030839288859717054,0.002977489985612013],"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":-3.7197284612603114e-06,"seed_std":0.002106062340912503,"seed_range":[-0.00248002157637028,0.0027583476439311115],"seeds":5}},"recall100":{"delta":-0.006171196581196581,"ci95":[-0.013775779914529912,0.00041544230769230243],"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":-0.006171196581196581,"seed_std":0.004028604503787422,"seed_range":[-0.013076068376068376,-0.0024871794871794872],"seeds":5}}},{"dataset":"FiQA","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"tangent1_l10","ndcg10":{"delta":-0.002057747105703452,"ci95":[-0.005128173636352115,0.0008939251850228282],"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":-0.0020577471057034525,"seed_std":0.0010340674313879601,"seed_range":[-0.0027882586065423576,-0.0002479738521519752],"seeds":5}},"recall100":{"delta":-0.00783063492063492,"ci95":[-0.014553503968253969,-0.001301718253968257],"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.007830634920634922,"seed_std":0.002014151058078034,"seed_range":[-0.009772222222222224,-0.005616666666666669],"seeds":5}}}]}`

### C175 - rounding_ok
- Location: results 5.2; figure3
- Claim: Ablation arc2_global_tangent2_r1 minus procrustes_global
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.024325109040435233,"ci95":[0.0195818675697136,0.029318485952316592],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.024325109040435233,"seed_std":0.004726550116148564,"seed_range":[0.017365688970446512,0.030638076764707856],"seeds":5},"ci99_bonferroni_family95":[0.01801533254696277,0.03102132243820168],"family_interval_interpretation":"above_zero"}`

### C176 - rounding_ok
- Location: results 5.2; figure3
- Claim: Ablation arc2_global_tangent2_r1 minus tangent1_l10
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.006923862939737235,"ci95":[0.004584432900988409,0.009226028099450147],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.006923862939737235,"seed_std":0.0020084533271641346,"seed_range":[0.003827292446927387,0.009036945683211683],"seeds":5},"ci99_bonferroni_family95":[0.003809388309482942,0.009959126205904258],"family_interval_interpretation":"above_zero"}`

### C177 - rounding_ok
- Location: results 5.2; figure3
- Claim: Ablation arc2_global_tangent2_r1 minus ridge_affine_l10_bias_regularized
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.09565304927282199,"ci95":[0.08032542616520105,0.11153533924165686],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.09565304927282199,"seed_std":0.004068923683907757,"seed_range":[0.090691014279143,0.10139112119859749],"seeds":5},"ci99_bonferroni_family95":[0.07535298921225946,0.11663127039230592],"family_interval_interpretation":"above_zero"}`

### C178 - rounding_ok
- Location: results 5.2; figure3
- Claim: Ablation tangent2_l1 minus arc2_global_tangent2_r1
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":0.0031974956912717346,"ci95":[-0.0007402431692805767,0.007157619090496026],"descriptive":true,"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":0.0031974956912717337,"seed_std":0.0014261530566855027,"seed_range":[0.0014511899112586958,0.005359535138351684],"seeds":5},"ci99_bonferroni_family95":[-0.0018903844098364442,0.00830403326634241],"family_interval_interpretation":"unresolved"}`

### C179 - rounding_ok
- Location: results 5.2; figure3
- Claim: Ablation tangent2_l100 minus arc2_global_tangent2_r1
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"delta":-0.00925533869678723,"ci95":[-0.012286411062820052,-0.006335315068491882],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.00925533869678723,"seed_std":0.0032250020729826744,"seed_range":[-0.014885255917325473,-0.006946294267227517],"seeds":5},"ci99_bonferroni_family95":[-0.01321398029023485,-0.005510245768211927],"family_interval_interpretation":"below_zero"}`

### C180 - exact_match
- Location: results 5.3
- Claim: Family supports Converter5,ridge4,SimpleLinear2, all11 comparisons marked
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"overall":{"unresolved":19,"above_zero":11},"supported":[{"pair":"minilm_distilroberta","budget":"25pct","baseline":"embedding_converter_paper_spec","delta":0.03953962459261952,"ci":[0.0006302196978609639,0.07561331897623641]},{"pair":"minilm_distilroberta","budget":"50pct","baseline":"embedding_converter_paper_spec","delta":0.02190799526854917,"ci":[0.0005178011321619429,0.04263918301944054]},{"pair":"minilm_distilroberta","budget":"75pct","baseline":"ridge_affine_l10_bias_regularized","delta":0.01829353426503278,"ci":[0.00043951281706854317,0.04492339866433025]},{"pair":"e5_small_base","budget":"25pct","baseline":"simplelinear_official_final50_mlp5","delta":0.13287299235509,"ci":[0.0633001667256504,0.2051373777778217]},{"pair":"e5_small_base","budget":"25pct","baseline":"ridge_affine_l10_bias_regularized","delta":0.2641805555881269,"ci":[0.15726462442241934,0.37675795247986166]},{"pair":"e5_small_base","budget":"25pct","baseline":"embedding_converter_paper_spec","delta":0.25723359077319435,"ci":[0.17573076152800798,0.33756850203860655]},{"pair":"e5_small_base","budget":"50pct","baseline":"simplelinear_official_final50_mlp5","delta":0.06172988619056692,"ci":[0.01356012047442979,0.11446072714102258]},{"pair":"e5_small_base","budget":"50pct","baseline":"ridge_affine_l10_bias_regularized","delta":0.2622674417365517,"ci":[0.1579593697473118,0.37285038597163384]},{"pair":"e5_small_base","budget":"50pct","baseline":"embedding_converter_paper_spec","delta":0.23138457517015265,"ci":[0.15671745879653792,0.3085072832020045]},{"pair":"e5_small_base","budget":"75pct","baseline":"ridge_affine_l10_bias_regularized","delta":0.2819970458539894,"ci":[0.17480022770218387,0.3973296904795432]},{"pair":"e5_small_base","budget":"75pct","baseline":"embedding_converter_paper_spec","delta":0.1999540966512042,"ci":[0.13925018639424472,0.2642221645268023]}]}`

### C181 - exact_match
- Location: results 5.3
- Claim: Procrustes higher in all6unrounded cells, MiniLM75 difference<.0001; all Proc/LA2M family intervals crosszero
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"pair":"minilm_distilroberta","budget":"25pct","baseline":"procrustes_global","delta":-5.136066855163088e-05,"ci":[-0.014694745593972814,0.013213525679703809]},{"pair":"minilm_distilroberta","budget":"25pct","baseline":"la2m20_integration_script_adaptation","delta":-0.001504399489089405,"ci":[-0.03430576267376661,0.02907870839908143]},{"pair":"minilm_distilroberta","budget":"50pct","baseline":"procrustes_global","delta":-0.004666870465219521,"ci":[-0.018617590940593846,0.00609852657610738]},{"pair":"minilm_distilroberta","budget":"50pct","baseline":"la2m20_integration_script_adaptation","delta":-0.007321002357654939,"ci":[-0.026682539889838944,0.007137508111023871]},{"pair":"minilm_distilroberta","budget":"75pct","baseline":"procrustes_global","delta":-2.3564924613148544e-05,"ci":[-0.0045045389961348515,0.004383734800061371]},{"pair":"minilm_distilroberta","budget":"75pct","baseline":"la2m20_integration_script_adaptation","delta":0.0009512792584207396,"ci":[-0.006116292591115391,0.008780612423464904]},{"pair":"e5_small_base","budget":"25pct","baseline":"procrustes_global","delta":-0.0032404285712858832,"ci":[-0.021620914986484444,0.01432474395822758]},{"pair":"e5_small_base","budget":"25pct","baseline":"la2m20_integration_script_adaptation","delta":0.04221113712298237,"ci":[-0.006416733787802239,0.09332456219941979]},{"pair":"e5_small_base","budget":"50pct","baseline":"procrustes_global","delta":-0.01632154204848677,"ci":[-0.03982012404542802,0.0022978122002522048]},{"pair":"e5_small_base","budget":"50pct","baseline":"la2m20_integration_script_adaptation","delta":0.0005942541991765067,"ci":[-0.03551296863593118,0.03599603191311822]},{"pair":"e5_small_base","budget":"75pct","baseline":"procrustes_global","delta":-0.010011959658702082,"ci":[-0.0260053875353406,0.0036310901422503547]},{"pair":"e5_small_base","budget":"75pct","baseline":"la2m20_integration_script_adaptation","delta":-0.008995301709012363,"ci":[-0.03577940334852425,0.01564579912460651]}]`

### C182 - rounding_ok
- Location: abstract; results 5.3
- Claim: E5 Converter gain .2000 to .2572;25% familyCI[.1757,.3376]
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `[{"ci95":[0.20634954315490223,0.3084705371596377],"ci95_descriptive":true,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.17573076152800798,0.33756850203860655],"per_interval_confidence":0.9983333333333333,"family_interval_interpretation":"above_zero","coverage":"approximate percentile bootstrap","delta":0.25723359077319435,"mapping_seed_variability":{"mean":0.25723359077319435,"seed_std":0.024304549666813863,"seed_range":[0.2170697592382117,0.2767858989374312],"seeds":5}},{"ci95":[0.18317239664563703,0.279734807298328],"ci95_descriptive":true,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.15671745879653792,0.3085072832020045],"per_interval_confidence":0.9983333333333333,"family_interval_interpretation":"above_zero","coverage":"approximate percentile bootstrap","delta":0.23138457517015265,"mapping_seed_variability":{"mean":0.2313845751701527,"seed_std":0.029319497636933305,"seed_range":[0.20310654653105573,0.26297645212259063],"seeds":5}},{"ci95":[0.1605438337886913,0.23994650419380487],"ci95_descriptive":true,"interval_interpretation":"above_zero","ci_bonferroni_family95":[0.13925018639424472,0.2642221645268023],"per_interval_confidence":0.9983333333333333,"family_interval_interpretation":"above_zero","coverage":"approximate percentile bootstrap","delta":0.1999540966512042,"mapping_seed_variability":{"mean":0.1999540966512042,"seed_std":0.011405957200445908,"seed_range":[0.18577720274153758,0.21729173903071675],"seeds":5}}]`

### C183 - rounding_ok
- Location: abstract; results5.3
- Claim: MiniLM Recall highest6adapter pointmeans all3budgets;75%=.0998 versus nativeY .1052; E5=.0997 versus .1162
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"minilm":{"25pct":{"arc2_global_tangent2_r1":0.08963088480259038,"procrustes_global":0.08656849639226609,"la2m20_integration_script_adaptation":0.07356777060172419,"simplelinear_official_final50_mlp5":0.06257470519773327,"ridge_affine_l10_bias_regularized":0.06890134085023747,"embedding_converter_paper_spec":0.06512050655177726},"50pct":{"arc2_global_tangent2_r1":0.09529158965710632,"procrustes_global":0.09348540930621103,"la2m20_integration_script_adaptation":0.08842284023887333,"simplelinear_official_final50_mlp5":0.0844776701539496,"ridge_affine_l10_bias_regularized":0.0779944968405071,"embedding_converter_paper_spec":0.07717310564196894},"75pct":{"arc2_global_tangent2_r1":0.09983604059514704,"procrustes_global":0.09942876429633421,"la2m20_integration_script_adaptation":0.09826954011884906,"simplelinear_official_final50_mlp5":0.09701627700333974,"ridge_affine_l10_bias_regularized":0.08563775429812863,"embedding_converter_paper_spec":0.08920092316113651}},"native":{"minilm_distilroberta":{"full_x":{"ndcg":0.4934781848463412,"recall":0.09355341420637212},"full_y":{"ndcg":0.5202728348242263,"recall":0.10521378018323918}},"e5_small_base":{"full_x":{"ndcg":0.6805416492225224,"recall":0.12353038057812048},"full_y":{"ndcg":0.6421134496001705,"recall":0.11624395516879528}}},"e5_arc75":0.09966692928143464}`
- Notes: Auxiliary descriptive only; nDCG proximity .5195 vs .5203 is explicitly not equivalence.

### C184 - exact_match
- Location: discussion
- Claim: All24partialDEVfive-seedARC2conditionmeansbelowFull-X
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `[{"dataset":"FiQA","pair":"minilm_distilroberta","budget":"25pct","delta":-0.10284201135940102},{"dataset":"FiQA","pair":"minilm_distilroberta","budget":"50pct","delta":-0.08245660606330107},{"dataset":"FiQA","pair":"minilm_distilroberta","budget":"75pct","delta":-0.039889234235705506},{"dataset":"FiQA","pair":"e5_small_base","budget":"25pct","delta":-0.07337144737157347},{"dataset":"FiQA","pair":"e5_small_base","budget":"50pct","delta":-0.03484308204038783},{"dataset":"FiQA","pair":"e5_small_base","budget":"75pct","delta":-0.009292970429180647},{"dataset":"NanoNQ","pair":"minilm_distilroberta","budget":"25pct","delta":-0.10427512003201356},{"dataset":"NanoNQ","pair":"minilm_distilroberta","budget":"50pct","delta":-0.06645752832153762},{"dataset":"NanoNQ","pair":"minilm_distilroberta","budget":"75pct","delta":-0.006249265267949888},{"dataset":"NanoNQ","pair":"e5_small_base","budget":"25pct","delta":-0.15238676828911168},{"dataset":"NanoNQ","pair":"e5_small_base","budget":"50pct","delta":-0.1151622280729957},{"dataset":"NanoNQ","pair":"e5_small_base","budget":"75pct","delta":-0.049411051671895634},{"dataset":"NanoHotpotQA","pair":"minilm_distilroberta","budget":"25pct","delta":-0.22458229651317352},{"dataset":"NanoHotpotQA","pair":"minilm_distilroberta","budget":"50pct","delta":-0.15704132118465658},{"dataset":"NanoHotpotQA","pair":"minilm_distilroberta","budget":"75pct","delta":-0.10712853302643671},{"dataset":"NanoHotpotQA","pair":"e5_small_base","budget":"25pct","delta":-0.24326758710810692},{"dataset":"NanoHotpotQA","pair":"e5_small_base","budget":"50pct","delta":-0.15551371655782487},{"dataset":"NanoHotpotQA","pair":"e5_small_base","budget":"75pct","delta":-0.08136563915378403},{"dataset":"NanoFEVER","pair":"minilm_distilroberta","budget":"25pct","delta":-0.28057323720528327},{"dataset":"NanoFEVER","pair":"minilm_distilroberta","budget":"50pct","delta":-0.2247119175382064},{"dataset":"NanoFEVER","pair":"minilm_distilroberta","budget":"75pct","delta":-0.13876219546138313},{"dataset":"NanoFEVER","pair":"e5_small_base","budget":"25pct","delta":-0.14290148735806363},{"dataset":"NanoFEVER","pair":"e5_small_base","budget":"50pct","delta":-0.11940282501806576},{"dataset":"NanoFEVER","pair":"e5_small_base","budget":"75pct","delta":-0.053232592177733795}]`
- Notes: Condition means only; does not assert all individual seeds below Full-X.

### C185 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__within_method__arc2_global_tangent2_r1
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.05964116316462802,"ci95":[0.04745037841766362,0.07261138137489603],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.05964116316462802,"seed_std":0.005426155358215546,"seed_range":[0.051269388104087925,0.06609533941830437],"seeds":5},"ci_bonferroni_family95":[0.03934110686868015,0.08060437708604837],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C186 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_allpaid_vs_baseline_allpaid__procrustes_global
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.03375954732030533,"ci95":[0.0241099466663953,0.04404567583409277],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.033759547320305325,"seed_std":0.0003138837740250079,"seed_range":[0.03351601138314186,0.03420657058388042],"seeds":5},"ci_bonferroni_family95":[0.018645329403840227,0.05040795355988812],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C187 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_allpaid_vs_baseline_allpaid__la2m20_integration_script_adaptation
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.028222554511761314,"ci95":[0.016899637136538557,0.039790813518619524],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.028222554511761318,"seed_std":0.001999628639381227,"seed_range":[0.02656841005855596,0.03159829765218961],"seeds":5},"ci_bonferroni_family95":[0.010129417979752293,0.04729686135338356],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C188 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_allpaid_vs_baseline_allpaid__simplelinear_official_final50_mlp5
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.034829774427415756,"ci95":[0.027452523846899942,0.042640186257219305],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.03482977442741575,"seed_std":0.0018402935714970671,"seed_range":[0.03274086161728058,0.03677170936320519],"seeds":5},"ci_bonferroni_family95":[0.023544184937148122,0.04719119478704116],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C189 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_allpaid_vs_baseline_allpaid__ridge_affine_l10_bias_regularized
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.00011725527452398765,"ci95":[-0.004625659202632946,0.00413554117820924],"descriptive":true,"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":-0.0001172552745239876,"seed_std":0.0006113664305195812,"seed_range":[-0.0008554368041709251,0.0007362642612591348],"seeds":5},"ci_bonferroni_family95":[-0.00754001759934293,0.006532341944925181],"per_interval_confidence":0.9984375,"family_interval_interpretation":"unresolved"}`

### C190 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_allpaid_vs_baseline_allpaid__embedding_converter_paper_spec
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.041384582059895376,"ci95":[0.02991963829911289,0.053459940575635176],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.04138458205989536,"seed_std":0.004103460911488156,"seed_range":[0.03687992278028356,0.045830467941444415],"seeds":5},"ci_bonferroni_family95":[0.02361352378412802,0.06096949393433256],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C191 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_fixed_vs_baseline_allpaid__procrustes_global
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.02588161584432268,"ci95":[-0.03417003916559222,-0.01801580386428984],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.025881615844322685,"seed_std":0.005376441007349862,"seed_range":[-0.03255264963104094,-0.01775337672094605],"seeds":5},"ci_bonferroni_family95":[-0.03980693975125909,-0.013428284825739776],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C192 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_fixed_vs_baseline_allpaid__la2m20_integration_script_adaptation
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.0314186086528667,"ci95":[-0.042012576023148736,-0.021343247247171016],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.031418608652866685,"seed_std":0.005557038034077977,"seed_range":[-0.03768872467442178,-0.023920362887972738],"seeds":5},"ci_bonferroni_family95":[-0.048611616293263764,-0.015633681782311927],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C193 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_fixed_vs_baseline_allpaid__simplelinear_official_final50_mlp5
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.024811388737212257,"ci95":[-0.03372933890101637,-0.0162610225585409],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.024811388737212267,"seed_std":0.005772186425378572,"seed_range":[-0.03335447780102385,-0.01749657659554149],"seeds":5},"ci_bonferroni_family95":[-0.03905427748357963,-0.01125245236317356],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C194 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_fixed_vs_baseline_allpaid__ridge_affine_l10_bias_regularized
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.05975841843915199,"ci95":[-0.0732611341251776,-0.04688267477535806],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.05975841843915203,"seed_std":0.005522419921201973,"seed_range":[-0.06695077622247533,-0.05180524963989667],"seeds":5},"ci_bonferroni_family95":[-0.08258263920537419,-0.03854644831580933],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C195 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: minilm_distilroberta__arc2_fixed_vs_baseline_allpaid__embedding_converter_paper_spec
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.01825658110473264,"ci95":[-0.029725319923615153,-0.007355581073365403],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.01825658110473264,"seed_std":0.008720804143743958,"seed_range":[-0.029215416638020856,-0.005438920162643485],"seeds":5},"ci_bonferroni_family95":[-0.036885129550449265,-0.0010228000757110728],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C196 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: e5_small_base__within_method__arc2_global_tangent2_r1
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.019768225474924635,"ci95":[-0.04220860561973594,0.002119824562517512],"descriptive":true,"interval_interpretation":"unresolved","mapping_seed_variability":{"mean":-0.019768225474924635,"seed_std":0.0033232662040852097,"seed_range":[-0.023552154355393862,-0.015668827243269116],"seeds":5},"ci_bonferroni_family95":[-0.056329874306672884,0.016636927373489714],"per_interval_confidence":0.9984375,"family_interval_interpretation":"unresolved"}`

### C197 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: e5_small_base__arc2_allpaid_vs_baseline_allpaid__procrustes_global
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.0443354790156809,"ci95":[-0.06640692702701478,-0.022976456944481204],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.0443354790156809,"seed_std":0.001794250006322547,"seed_range":[-0.04617982164286784,-0.041987726968042004],"seeds":5},"ci_bonferroni_family95":[-0.07969591141306612,-0.00927207701618083],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C198 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: e5_small_base__arc2_allpaid_vs_baseline_allpaid__la2m20_integration_script_adaptation
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":-0.03747431937003851,"ci95":[-0.05857298400789254,-0.016824419351755816],"descriptive":true,"interval_interpretation":"below_zero","mapping_seed_variability":{"mean":-0.037474319370038506,"seed_std":0.003989077040232158,"seed_range":[-0.04348784040023846,-0.033081591948529526],"seeds":5},"ci_bonferroni_family95":[-0.07058268018538005,-0.003758372247374875],"per_interval_confidence":0.9984375,"family_interval_interpretation":"below_zero"}`

### C199 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: e5_small_base__arc2_allpaid_vs_baseline_allpaid__simplelinear_official_final50_mlp5
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.12391757467237823,"ci95":[0.10435375246023457,0.14408195310550403],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.12391757467237816,"seed_std":0.0053952941696258075,"seed_range":[0.11610146564520915,0.13129062200695518],"seeds":5},"ci_bonferroni_family95":[0.09382137946545674,0.15672368372932174],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C200 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: e5_small_base__arc2_allpaid_vs_baseline_allpaid__ridge_affine_l10_bias_regularized
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.0648524069060192,"ci95":[0.05060874356271226,0.07977392875429595],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.06485240690601925,"seed_std":0.0022855490388646944,"seed_range":[0.061131910179480976,0.06651026489237026],"seeds":5},"ci_bonferroni_family95":[0.043521312095724345,0.0893493930084069],"per_interval_confidence":0.9984375,"family_interval_interpretation":"above_zero"}`

### C201 - rounding_ok
- Location: introduction;results5.5;allpaid markers
- Claim: e5_small_base__arc2_allpaid_vs_baseline_allpaid__embedding_converter_paper_spec
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"delta":0.029347517705334787,"ci95":[0.0017862511963257896,0.05698722425278101],"descriptive":true,"interval_interpretation":"above_zero","mapping_seed_variability":{"mean":0.029347517705334787,"seed_std":0.005449732474162901,"seed_range":[0.021326500545310264,0.035977619218107645],"seeds":5},"ci_bonferroni_family95":[-0.015572921137816255,0.07476185576148772],"per_interval_confidence":0.9984375,"family_interval_interpretation":"unresolved"}`

### C202 - rounding_ok
- Location: results5.5 mixed-gallery paragraph
- Claim: minilm_distilroberta allpaid before/after replacement nDCG,Recall and paidtop10
- Raw/code paths: `results/b1g_r1_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"metrics":{"ndcg10":{"before":{"mean":0.3509507352060274,"std":0.0006769150766086756,"min":0.3502338820687454,"max":0.3521592080595147,"positive":5,"zero":0,"negative":0,"observations":5},"after":{"mean":0.36714602143626507,"std":0.0007631388479719805,"min":0.3660662051912534,"max":0.36845783238036095,"positive":5,"zero":0,"negative":0,"observations":5},"delta_of_query_means":{"mean":0.016195286230237804,"std":0.0011029323178451855,"min":0.014911695060479567,"max":0.018223950311615517,"positive":5,"zero":0,"negative":0,"observations":5}},"recall100":{"before":{"mean":0.6804736696636696,"std":0.0008890444308356923,"min":0.6797136696636696,"max":0.6822136696636696,"positive":5,"zero":0,"negative":0,"observations":5},"after":{"mean":0.6922001554001553,"std":0.00043685123585445905,"min":0.6918763458763458,"max":0.693050949050949,"positive":5,"zero":0,"negative":0,"observations":5},"delta_of_query_means":{"mean":0.011726485736485737,"std":0.0010804618144230295,"min":0.009662676212676212,"max":0.012837279387279387,"positive":5,"zero":0,"negative":0,"observations":5}}},"paid_top10":{"before":{"mean":0.49748000000000003,"std":0.001394847661933025,"min":0.496,"max":0.5,"positive":5,"zero":0,"negative":0,"observations":5},"after":{"mean":0.5844,"std":0.0010039920318408774,"min":0.5832,"max":0.586,"positive":5,"zero":0,"negative":0,"observations":5}}}`

### C203 - rounding_ok
- Location: results5.5 mixed-gallery paragraph
- Claim: e5_small_base allpaid before/after replacement nDCG,Recall and paidtop10
- Raw/code paths: `results/b1g_r1_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"metrics":{"ndcg10":{"before":{"mean":0.31490775036459107,"std":0.0009087763040778174,"min":0.3132027992239177,"max":0.31566385604631897,"positive":5,"zero":0,"negative":0,"observations":5},"after":{"mean":0.29186698206096207,"std":0.0010636937868429494,"min":0.29060998983803676,"max":0.2935400851458403,"positive":5,"zero":0,"negative":0,"observations":5},"delta_of_query_means":{"mean":-0.023040768303629045,"std":0.0017566186233215187,"min":-0.02492678658987266,"max":-0.020649585352009475,"positive":0,"zero":0,"negative":5,"observations":5}},"recall100":{"before":{"mean":0.6541642457542457,"std":0.0007706851208863003,"min":0.6528375790875791,"max":0.6552375790875791,"positive":5,"zero":0,"negative":0,"observations":5},"after":{"mean":0.5594899234099234,"std":0.0012584901790893236,"min":0.5571710345210344,"max":0.5608377011877013,"positive":5,"zero":0,"negative":0,"observations":5},"delta_of_query_means":{"mean":-0.09467432234432235,"std":0.0014615635125558401,"min":-0.09723321123321123,"max":-0.09316654456654457,"positive":0,"zero":0,"negative":5,"observations":5}}},"paid_top10":{"before":{"mean":0.49164,"std":0.0018172506706560965,"min":0.489,"max":0.49360000000000004,"positive":5,"zero":0,"negative":0,"observations":5},"after":{"mean":0.06472000000000001,"std":0.0004995998398718702,"min":0.06380000000000001,"max":0.06520000000000001,"positive":5,"zero":0,"negative":0,"observations":5}}}`

### C204 - exact_match
- Location: point contrast arithmetic
- Claim: Every dev saved point contrast agrees with reconstructed means
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"contrasts":120,"max_error":4.996003610813204e-16}`

### C205 - exact_match
- Location: point contrast arithmetic
- Claim: Every trec saved point contrast agrees with reconstructed means
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"contrasts":30,"max_error":2.2898349882893854e-16}`

### C206 - exact_match
- Location: point contrast arithmetic
- Claim: Every ablation saved point contrast agrees with reconstructed means
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"contrasts":120,"max_error":2.7755575615628914e-16}`

### C207 - exact_match
- Location: point contrast arithmetic
- Claim: Every paid saved point contrast agrees with reconstructed means
- Raw/code paths: `results/b1p_r5_review_20261027/scoring/results_summary.json`
- Exact evidence: `{"contrasts":32,"max_error":3.885780586188048e-16}`

### C208 - rounding_ok
- Location: results5.5 scalar prose
- Claim: Fixed/all-paid values and replacement nDCG, E5 Recall and paid top10 shares
- Raw/code paths: `['results/b1p_r5_review_20261027/scoring/results_summary.json', 'results/b1g_r1_review_20261027/scoring/results_summary.json']`
- Exact evidence: `{"minilm_distilroberta/fixed1024 ARC2 nDCG":0.3075048582716371,"minilm_distilroberta/allpaid28819 ARC2 nDCG":0.36714602143626496,"minilm_distilroberta/replacement/before/nDCG":0.3509507352060274,"minilm_distilroberta/replacement/after/nDCG":0.36714602143626507,"e5_small_base/fixed1024 ARC2 nDCG":0.3116352075358866,"e5_small_base/allpaid28819 ARC2 nDCG":0.29186698206096195,"e5_small_base/replacement/before/nDCG":0.31490775036459107,"e5_small_base/replacement/after/nDCG":0.29186698206096207,"E5/replacement/before/Recall":0.6541642457542457,"E5/replacement/before/paid top10":0.49164,"E5/replacement/after/Recall":0.5594899234099234,"E5/replacement/after/paid top10":0.06472000000000001}`

### C209 - exact_match
- Location: actual figures/dev_quality.svg and.pdf
- Claim: 40 metric/native data points in actual vector figure
- Raw/code paths: `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`
- Exact evidence: `{"data_points":40,"max_svg_inverse_error":2.5721529350875016e-09,"pdf_paths_match_svg":true}`
- Notes: All6adapter curves at3budgets plus2native horizontal references per panel; no interval or intermediate point inferred.

### C210 - exact_match
- Location: actual figures/trec_quality.svg and.pdf
- Claim: 80 metric/native data points in actual vector figure
- Raw/code paths: `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`
- Exact evidence: `{"data_points":80,"max_svg_inverse_error":2.786030461887634e-09,"pdf_paths_match_svg":true}`
- Notes: All6adapter curves at3budgets plus2native horizontal references per panel; no interval or intermediate point inferred.

### C211 - exact_match
- Location: actual figures/dev_ablation.svg and.pdf
- Claim: All5fullsaved99%ablationintervals ononecontinuousaxis
- Raw/code paths: `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`
- Exact evidence: `{"actual_interval_coordinates":[[0.01801533279718136,0.031021322167755983],[0.003809388339971402,0.009959126306338495],[0.0753529891748366,0.11663127053121593],[-0.0018903842847903043,0.008304033564814812],[-0.013213980502791402,-0.005510245906522342]],"saved_intervals":[[0.01801533254696277,0.03102132243820168],[0.003809388309482942,0.009959126205904258],[0.07535298921225946,0.11663127039230592],[-0.0018903844098364442,0.00830403326634241],[-0.01321398029023485,-0.005510245768211927]],"pdf_paths_match_svg":true}`
- Notes: Exact independent coordinate inversion; includes large ridge contrast and negative lambda100 control.

### C212 - rounding_ok
- Location: abstract;method3.5;discussion
- Claim: 295680float32 coefficients=1182720bytes=1.13MiB;114.7times fewer parameterbytes thanConverter
- Raw/code paths: `['src/arc2_global/embedding_converter.py', 'src/arc2_global/model.py']`
- Exact evidence: `{"coefficients":295680,"bytes":1182720,"MiB":1.1279296875,"converter_parameters":33927168,"converter_bytes":135708672,"parameter_byte_ratio":114.74285714285715}`
- Notes: Structural coefficient/weight count only; same ridge coefficient count; not checkpoint size or end-to-endcost.

### C213 - exact_match
- Location: setup;method3.5
- Claim: Solverregimeassignment
- Raw/code paths: `['ops/b1p_stage.py', 'ops/b2_stage.py', 'protocols/B2_TREC_COVID_CONFIRMATION_20261031.md']`
- Exact evidence: `{"dev_arc_cells":{"B1-M sealed main-compatible cell":120},"receipts":[{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/e5_small_base_seed17_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/e5_small_base_seed29_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/e5_small_base_seed41_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/e5_small_base_seed53_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/e5_small_base_seed67_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/minilm_distilroberta_seed17_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/minilm_distilroberta_seed29_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/minilm_distilroberta_seed41_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/minilm_distilroberta_seed53_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/cpu/minilm_distilroberta_seed67_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":1024},{"path":"results/b1p_r5_review_20261027/generation/cpu/e5_small_base_seed17_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/e5_small_base_seed29_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/e5_small_base_seed41_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/e5_small_base_seed53_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/e5_small_base_seed67_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/minilm_distilroberta_seed29_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/minilm_distilroberta_seed41_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/minilm_distilroberta_seed53_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819},{"path":"results/b1p_r5_review_20261027/generation/cpu/minilm_distilroberta_seed67_allpaid28819_arc2_global_tangent2_r1/metadata.json","backend":"arc2_global_tangent2_primal_float64_r1","fit_pairs":28819}],"assignment":{"DEV_fixed1024":"dual float64","B1M_ablation":"dual float64","B1P_fixed1024_imports":"dual float64","B1P_allpaid28819":"primal float64","B2_fixed1024":"primal float64"}}`
- Notes: Found omission: original current manuscript assigned allpaid primal, but did not explicitly assign prospective fixed1024 B2 primal; parent notified for narrow disclosure correction. No incorrect numeric comparison found.

### C214 - exact_match
- Location: method equations1-10,algorithm;setup
- Claim: Frozen lambda10/exactly2targets;rawaffine float64 expansion of float32Procrustes;biasregularization;oneaffine normalizedmixedgallery;exactfloat32top100 stableties
- Raw/code paths: `['configs/baselines.json', 'configs/datasets.json', 'configs/b1c_r3_lock.json', 'configs/b1m_lock.json', 'configs/b1m_score_r2_lock.json', 'configs/b1p_lock.json', 'configs/b2_lock.json', 'src/arc2_global/model.py', 'src/arc2_global/solver_backend.py', 'src/arc2_global/mechanism_ablation.py', 'src/arc2_global/procrustes.py', 'src/arc2_global/numerics.py', 'src/arc2_global/retrieval.py', 'src/arc2_global/baseline_adapters.py', 'src/arc2_global/embedding_converter.py', 'ops/b1m_score.py', 'ops/b1p_score.py', 'ops/b1c_r3_score.py', 'ops/b2_score.py', 'ops/b1p_stage.py', 'ops/b2_stage.py', 'protocols/B2_TREC_COVID_CONFIRMATION_20261031.md', 'protocols/B1P_ALL_PAID_FIQA_20261026.md', 'protocols/B1M_B1P0_DEVELOPMENT_20261026.md']`
- Exact evidence: `{"lambda_value":10,"tangent_steps":2,"d_s":384,"d_t":768,"p":385}`
- Notes: Source inspected statically; equations, cosinegradient and exact-arithmetic scaleequivariance checked algebraically. No claim of guaranteed finite-step improvement.

### C215 - exact_match
- Location: setup scope and inferential construction
- Claim: 4DEVcollections,2migrations,3budgets,5seeds,1024anchors;TREC171332/50;paidFiQA28819/57638;20kquerybootstrap and5/5/32/30families
- Raw/code paths: `['configs/baselines.json', 'configs/datasets.json', 'configs/b1c_r3_lock.json', 'configs/b1m_lock.json', 'configs/b1m_score_r2_lock.json', 'configs/b1p_lock.json', 'configs/b2_lock.json', 'src/arc2_global/model.py', 'src/arc2_global/solver_backend.py', 'src/arc2_global/mechanism_ablation.py', 'src/arc2_global/procrustes.py', 'src/arc2_global/numerics.py', 'src/arc2_global/retrieval.py', 'src/arc2_global/baseline_adapters.py', 'src/arc2_global/embedding_converter.py', 'ops/b1m_score.py', 'ops/b1p_score.py', 'ops/b1c_r3_score.py', 'ops/b2_score.py', 'ops/b1p_stage.py', 'ops/b2_stage.py', 'protocols/B2_TREC_COVID_CONFIRMATION_20261031.md', 'protocols/B1P_ALL_PAID_FIQA_20261026.md', 'protocols/B1M_B1P0_DEVELOPMENT_20261026.md']`
- Exact evidence: `{"collections":{"FiQA":{"documents":57638,"queries":500},"NanoNQ":{"documents":5035,"queries":50},"NanoHotpotQA":{"documents":5090,"queries":50},"NanoFEVER":{"documents":4996,"queries":50},"TREC-COVID":{"documents":171332,"queries":50}},"seeds":[17,29,41,53,67],"families":{"dev":{"draws":20000,"seed":20261028,"rng":"numpy default_rng/PCG64; datasets in DATASETS order","datasets":{"NanoNQ":{"indices_shape":[20000,50],"indices_dtype":"int32","indices_sha256_c_order":"df0c87af8cde8ddd160cbe91a8f8ef8bcf1257195a6a12911b659656ca7d7d03"},"NanoHotpotQA":{"indices_shape":[20000,50],"indices_dtype":"int32","indices_sha256_c_order":"9fa43e9e11e93169f9474bb9a4b7ec619c6e81ec4f0006b9a9c6f021bcdbf475"},"NanoFEVER":{"indices_shape":[20000,50],"indices_dtype":"int32","indices_sha256_c_order":"639078103208562d9a1e016fe104b5af16619575fe9a5bfefa01b237b1d315a0"},"FiQA":{"indices_shape":[20000,500],"indices_dtype":"int32","indices_sha256_c_order":"af4fedfe906d8f77983b814f1770b53d49b840a363b62d4b409c32a6685b88cd"}},"resampling":"independent query resampling within each dataset; identical indices across pairs/budgets/methods/metrics; average five mapping seeds before resampling","macro_weighting":"equal 24 dataset/pair/budget strata","familywise":{"metric":"ndcg10","scope":"overall_equal_24_strata","contrasts":5,"family_confidence":0.95,"per_interval_confidence":0.99,"method":"bonferroni_percentile"},"condition_intervals":"nominal95 descriptive; not a 120-contrast tested family","recall_intervals":"nominal95 descriptive","coverage":"approximate percentile bootstrap"},"trec":{"draws":20000,"seed":20261031,"rng":"numpy default_rng/PCG64","query_indices_sha256":"18cc3ac6ca3c1682d83323766ad47e13572e1dd78dd618d0df797b9b7627a16a","definitions":[{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","method":"procrustes_global"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","method":"arc2_global_tangent2_r1"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","method":"la2m20_integration_script_adaptation"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","method":"simplelinear_official_final50_mlp5"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","method":"ridge_affine_l10_bias_regularized"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","method":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","method":"procrustes_global"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","method":"arc2_global_tangent2_r1"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","method":"la2m20_integration_script_adaptation"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","method":"simplelinear_official_final50_mlp5"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","method":"ridge_affine_l10_bias_regularized"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","method":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","method":"procrustes_global"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","method":"arc2_global_tangent2_r1"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","method":"la2m20_integration_script_adaptation"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","method":"simplelinear_official_final50_mlp5"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","method":"ridge_affine_l10_bias_regularized"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","method":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"full","method":"full_x"},{"kind":"mean","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"full","method":"full_y"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","left":"arc2_global_tangent2_r1","right":"procrustes_global"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","left":"arc2_global_tangent2_r1","right":"la2m20_integration_script_adaptation"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","left":"arc2_global_tangent2_r1","right":"simplelinear_official_final50_mlp5"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","left":"arc2_global_tangent2_r1","right":"ridge_affine_l10_bias_regularized"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"25pct","left":"arc2_global_tangent2_r1","right":"embedding_converter_paper_spec"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","left":"arc2_global_tangent2_r1","right":"procrustes_global"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","left":"arc2_global_tangent2_r1","right":"la2m20_integration_script_adaptation"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","left":"arc2_global_tangent2_r1","right":"simplelinear_official_final50_mlp5"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","left":"arc2_global_tangent2_r1","right":"ridge_affine_l10_bias_regularized"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"50pct","left":"arc2_global_tangent2_r1","right":"embedding_converter_paper_spec"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","left":"arc2_global_tangent2_r1","right":"procrustes_global"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","left":"arc2_global_tangent2_r1","right":"la2m20_integration_script_adaptation"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","left":"arc2_global_tangent2_r1","right":"simplelinear_official_final50_mlp5"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","left":"arc2_global_tangent2_r1","right":"ridge_affine_l10_bias_regularized"},{"kind":"contrast","dataset":"TREC-COVID","pair":"minilm_distilroberta","budget":"75pct","left":"arc2_global_tangent2_r1","right":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","method":"procrustes_global"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","method":"arc2_global_tangent2_r1"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","method":"la2m20_integration_script_adaptation"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","method":"simplelinear_official_final50_mlp5"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","method":"ridge_affine_l10_bias_regularized"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","method":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","method":"procrustes_global"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","method":"arc2_global_tangent2_r1"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","method":"la2m20_integration_script_adaptation"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","method":"simplelinear_official_final50_mlp5"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","method":"ridge_affine_l10_bias_regularized"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","method":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","method":"procrustes_global"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","method":"arc2_global_tangent2_r1"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","method":"la2m20_integration_script_adaptation"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","method":"simplelinear_official_final50_mlp5"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","method":"ridge_affine_l10_bias_regularized"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","method":"embedding_converter_paper_spec"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"full","method":"full_x"},{"kind":"mean","dataset":"TREC-COVID","pair":"e5_small_base","budget":"full","method":"full_y"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","left":"arc2_global_tangent2_r1","right":"procrustes_global"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","left":"arc2_global_tangent2_r1","right":"la2m20_integration_script_adaptation"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","left":"arc2_global_tangent2_r1","right":"simplelinear_official_final50_mlp5"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","left":"arc2_global_tangent2_r1","right":"ridge_affine_l10_bias_regularized"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"25pct","left":"arc2_global_tangent2_r1","right":"embedding_converter_paper_spec"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","left":"arc2_global_tangent2_r1","right":"procrustes_global"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","left":"arc2_global_tangent2_r1","right":"la2m20_integration_script_adaptation"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","left":"arc2_global_tangent2_r1","right":"simplelinear_official_final50_mlp5"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","left":"arc2_global_tangent2_r1","right":"ridge_affine_l10_bias_regularized"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"50pct","left":"arc2_global_tangent2_r1","right":"embedding_converter_paper_spec"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"procrustes_global"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"la2m20_integration_script_adaptation"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"simplelinear_official_final50_mlp5"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"ridge_affine_l10_bias_regularized"},{"kind":"contrast","dataset":"TREC-COVID","pair":"e5_small_base","budget":"75pct","left":"arc2_global_tangent2_r1","right":"embedding_converter_paper_spec"}],"axes":["bootstrap_draw","definition_then_metric"],"metrics":["ndcg10","recall100"],"resampling":"one identical query resample across all pairs/budgets/methods/metrics; average five mapping seeds first","family_contrasts":30,"family_alpha":0.05,"per_interval_confidence":0.9983333333333333,"recall_intervals":"nominal95 descriptive","coverage":"approximate percentile bootstrap"},"paid":{"draws":20000,"seed":20261026,"rng":"numpy default_rng(20261026), PCG64","indices_shape":[20000,500],"indices_dtype":"int32","indices_sha256_c_order":"06f1b7712fe8eb020eb247239ec6bca26b0a124ef9e9b6ede1e957a065fb25c8","resampling":"500 queries with replacement; five seeds averaged first; shared indices","familywise":{"metric":"ndcg10","contrasts":32,"family_confidence":0.95,"per_interval_confidence":0.9984375,"method":"bonferroni_percentile"},"coverage":"approximate percentile bootstrap"},"ablation":{"draws":20000,"seed":20261026,"rng":"numpy SeedSequence.spawn(4), datasets in DATASETS order; PCG64","resampling":"queries within datasets, all five seeds averaged first; same indices for every condition","familywise":false}}}`
- Notes: Protocol/config and savedscorer metadata match; sharedindices/five-seedaveraging and percentiles inspected in implementation. Full20kbootstrap notrerun. Prospective designation verified protocol/seals/timestamps only; not independent reconstruction of historical human nonexposure.

### C216 - exact_match
- Location: setup prospective scope
- Claim: 184 rankings/endpoints sealed and separately verified before first final label opening
- Raw/code paths: `['D:\\DASFAA-2027-paper\\results\\b2_review_20261101\\evidence\\results\\b2_full_r1_20261031t064859\\verification\\verification_seal.json', 'D:\\DASFAA-2027-paper\\results\\b2_review_20261101\\evidence\\results\\b2_full_r1_20261031t064859\\first_final_qrel_open.json', 'D:\\DASFAA-2027-paper\\results\\b2_review_20261101\\evidence\\results\\b2_full_r1_20261031t064859\\ranking_seal.json']`
- Exact evidence: `{"verified_cells":184,"verification_completed_utc":"2026-10-31T20:11:42.810083+00:00","first_open_utc":"2026-10-31T20:12:17.410541+00:00","verification_hash_matches":true,"ranking_seal_hash_matches":true}`
- Notes: Saved provenance checked only; qrels were not opened by this audit.

### C217 - exact_match
- Location: compiled final PDF figures
- Claim: All4 included vector figures equal audited actual figure PDF drawing streams
- Raw/code paths: `D:\DASFAA-2027-paper\paper\ARC2_Global_DASFAA2027_final.pdf`
- Exact evidence: `[{"page":3,"figure":"mechanism","decoded_content_byte_identical":true},{"page":10,"figure":"dev_quality","decoded_content_byte_identical":true},{"page":11,"figure":"dev_ablation","decoded_content_byte_identical":true},{"page":13,"figure":"trec_quality","decoded_content_byte_identical":true}]`

### C218 - exact_match
- Location: compiled finalPDF
- Claim: Current16-pagePDF contains measuredcrossbudgettable,allpaidmarkers and4panelTRECfigure
- Raw/code paths: `D:\DASFAA-2027-paper\paper\ARC2_Global_DASFAA2027_final.pdf`
- Exact evidence: `{"pages":16,"sha256":"e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc","visual_review":"16-page contact sheet and full pages11-14 inspected; labels/tablecontext/negativeevidence visible"}`
- Notes: Raster inspection supplements vector-coordinate checks. Mechanism24docs/8anchors/4extraencodes is explicitly illustrative.

## Fresh hashes

Full paper-relative manuscript/figure/PDF hashes and absolute out-of-paper raw/code/protocol hashes are in the JSON sibling. Prior review opinions/reports were not consulted.
