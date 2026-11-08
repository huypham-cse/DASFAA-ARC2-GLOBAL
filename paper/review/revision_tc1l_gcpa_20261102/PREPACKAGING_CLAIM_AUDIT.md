# Paper Claim Audit Report

**Date:** 2026-11-02T09:22:15.825774+00:00
**Auditor:** GPT-6.1-sol, high, fresh zero-context thread (user override).
**Paper:** ARC2-Global: Tangent-Corrected Alignment for Embedding-Index Migration
**Overall verdict: PASS**
**Review independence:** same-family. **Acceptance status:** provisional.

PASS: 103 grouped numerical, comparison, scope and caption claims reconcile to the declared evidence; no material mismatch found.

Fresh paper-to-evidence review of declared manuscript TeX/Bib, generated tables, figure PDFs, frozen result summaries, per-query arrays, saved bootstrap draws, locks and mapper source. No prior audits/reviews/trackers or executor interpretation reports were read. No qrels were opened and no fitting, retrieval, rescoring or scientific experiment was run.

## Verification coverage

- Claim records: 103 grouped claims; exact_match: 46; rounding_ok: 57; material mismatches: 0.
- Checked every displayed numeric cell in all seven declared generated TeX tables, including source-package companion tables. Repeated prose statements share evidence with their corresponding tables.
- Recomputed all 392 saved method means from frozen per-query arrays. Largest absolute discrepancy: 1.11e-15. Every adapter group contains exactly seeds 17, 29, 41, 53 and 67.
- Recovered all 30 prospective nDCG family intervals and both new matched-target intervals from saved bootstrap draws; endpoint discrepancy: 0.
- Checked table bold/underline ranks before rounding and all prospective/all-paid significance markers. Inspected all four figure PDF renders and matched their captions, scales, point order and interval signs to evidence.
- Verified the GCPA distinction against the [official PMLR paper page](https://proceedings.mlr.press/v306/achara26a.html) and its official PDF, Section 3.4/Eq.8.

## Issues found

None. No manuscript changes are required by this claim audit.

## Interpretation limits

The matched-target result is MiniLM-only FiQA development evidence, with the two E5 contrasts still pending. The paper states that scope and retains the original four-contrast correction. Prospective advantages are limited to the stated baseline configurations; Procrustes/LA2M remain unresolved. Cross-budget results are descriptive, Recall is auxiliary, and proximity to Full-Y is not presented as equivalence.

This audit verifies reporting fidelity. It does not re-open qrels, redo historical access/seal verification, run new experiments, or replace the separate citation/novelty review. Same-family assurance remains provisional. HTML rendering was disabled as requested.

## All claims (detailed)

### Claim 1: exact_match
**Location:** `sections/results.tex: matched residual controls`

**Paper text:**

```tex
\paragraph{Tangent targeting improves matched residual controls.}
Holding initialization and supervision fixed isolates an additional benefit
on FiQA/MiniLM (Fig.~\ref{fig:ablation}b). ARC2 reaches $0.3075$ nDCG,
versus $0.2935$ for the norm-scaled chordal control, $0.2959$ for Euclidean
residual refinement and $0.2858$ for unrefined Procrustes. The tangent gains
are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$),
respectively, with both differences positive in all five fixed seed means.
The chordal comparison supports removing the radial target component in this
development configuration. It shares the norm-scaling rule, without imposing
identical later states or equal target norms.
```

**Checked statement:** both differences positive in all five fixed seed means

**Paper value:** `5`

**Evidence:** `D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/summary.json`

**Evidence value:**

```json
5
```

[np.float64(0.014091522297069115), np.float64(0.014442350945513882), np.float64(0.01413530584186301), np.float64(0.012806648311579516), np.float64(0.014519448306938965)]

### Claim 2: exact_match
**Location:** `sections/results.tex: matched residual controls`

**Paper text:**

```tex
\paragraph{Tangent targeting improves matched residual controls.}
Holding initialization and supervision fixed isolates an additional benefit
on FiQA/MiniLM (Fig.~\ref{fig:ablation}b). ARC2 reaches $0.3075$ nDCG,
versus $0.2935$ for the norm-scaled chordal control, $0.2959$ for Euclidean
residual refinement and $0.2858$ for unrefined Procrustes. The tangent gains
are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$),
respectively, with both differences positive in all five fixed seed means.
The chordal comparison supports removing the radial target component in this
development configuration. It shares the norm-scaling rule, without imposing
identical later states or equal target norms.
```

**Checked statement:** both differences positive in all five fixed seed means

**Paper value:** `5`

**Evidence:** `D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/summary.json`

**Evidence value:**

```json
5
```

[np.float64(0.01165823840255209), np.float64(0.013169960003684367), np.float64(0.011445941889303257), np.float64(0.009613888122461944), np.float64(0.01205879735034543)]

### Claim 3: rounding_ok
**Location:** `generated/dev_macro.tex: ARC2-Global`

**Paper text:**

```tex
\rowcolor{arcPale}\textbf{ARC2-Global} & \textbf{0.5275} & \underline{0.8659} & --- & --- \\
```

**Paper value:** `[0.5275, 0.8659]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.527477527300496,
  0.8658612474562474
]
```

Equal weight over 24 conditions; each condition uses all five seeds.

### Claim 4: rounding_ok
**Location:** `generated/dev_macro.tex: Procrustes`

**Paper text:**

```tex
Procrustes & \underline{0.5032} & \textbf{0.8661} & \textcolor{gainGreen}{+0.0243} & [+0.0181, +0.0308] \\
```

**Paper value:** `[0.5032, 0.8661, 0.0243, 0.0181, 0.0308]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.5031524182600609,
  0.8660998378473379,
  0.024325109040435233,
  0.018132175212397208,
  0.030791640313948616
]
```

Equal weight over 24 conditions; each condition uses all five seeds.

### Claim 5: rounding_ok
**Location:** `generated/dev_macro.tex: LA2M20`

**Paper text:**

```tex
LA2M20 & 0.4234 & 0.7758 & \textcolor{gainGreen}{+0.1041} & [+0.0861, +0.1229] \\
```

**Paper value:** `[0.4234, 0.7758, 0.1041, 0.0861, 0.1229]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.42342257351929274,
  0.7758335509398009,
  0.10405495378120326,
  0.08607033208524335,
  0.1229148044499058
]
```

Equal weight over 24 conditions; each condition uses all five seeds.

### Claim 6: rounding_ok
**Location:** `generated/dev_macro.tex: SimpleLinear`

**Paper text:**

```tex
SimpleLinear & 0.3554 & 0.6130 & \textcolor{gainGreen}{+0.1721} & [+0.1499, +0.1947] \\
```

**Paper value:** `[0.3554, 0.613, 0.1721, 0.1499, 0.1947]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.3553776623832738,
  0.6129790412827912,
  0.1720998649172223,
  0.1498621517850371,
  0.19470300383538613
]
```

Equal weight over 24 conditions; each condition uses all five seeds.

### Claim 7: rounding_ok
**Location:** `generated/dev_macro.tex: Affine ridge`

**Paper text:**

```tex
Affine ridge & 0.4318 & 0.7441 & \textcolor{gainGreen}{+0.0957} & [+0.0754, +0.1164] \\
```

**Paper value:** `[0.4318, 0.7441, 0.0957, 0.0754, 0.1164]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.4318244780276741,
  0.7441268305305805,
  0.09565304927282199,
  0.07540472081021199,
  0.11642668663044543
]
```

Equal weight over 24 conditions; each condition uses all five seeds.

### Claim 8: rounding_ok
**Location:** `generated/dev_macro.tex: Converter`

**Paper text:**

```tex
Converter & 0.3663 & 0.7641 & \textcolor{gainGreen}{+0.1612} & [+0.1427, +0.1799] \\
```

**Paper value:** `[0.3663, 0.7641, 0.1612, 0.1427, 0.1799]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.36631519310915567,
  0.7641036175861177,
  0.16116233419134046,
  0.14268641175964025,
  0.17991558284155384
]
```

Equal weight over 24 conditions; each condition uses all five seeds.

### Claim 9: rounding_ok
**Location:** `generated/trec_means.tex: ARC2-Global`

**Paper text:**

```tex
\rowcolor{arcPale}\textbf{ARC2-Global} & 0.4619 & 0.5000 & \underline{0.5195} & \underline{0.5628} & \underline{0.5904} & 0.6098 \\
```

**Paper value:** `[0.4619, 0.5, 0.5195, 0.5628, 0.5904, 0.6098]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.4619132237639601,
  0.4999550226735597,
  0.519513052034007,
  0.562801573213321,
  0.5904061066004364,
  0.6097818790197872
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 10: rounding_ok
**Location:** `generated/trec_means.tex: Procrustes`

**Paper text:**

```tex
Procrustes & \underline{0.4620} & 0.5046 & \textbf{0.5195} & \textbf{0.5660} & \textbf{0.6067} & \textbf{0.6198} \\
```

**Paper value:** `[0.462, 0.5046, 0.5195, 0.566, 0.6067, 0.6198]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.46196458443251165,
  0.5046218931387791,
  0.5195366169586203,
  0.5660420017846071,
  0.606727648648923,
  0.6197938386784891
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 11: rounding_ok
**Location:** `generated/trec_means.tex: LA2M20`

**Paper text:**

```tex
LA2M20 & \textbf{0.4634} & \underline{0.5073} & 0.5186 & 0.5206 & 0.5898 & \underline{0.6188} \\
```

**Paper value:** `[0.4634, 0.5073, 0.5186, 0.5206, 0.5898, 0.6188]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.4634176232530495,
  0.5072760250312146,
  0.5185617727755863,
  0.5205904360903386,
  0.5898118524012599,
  0.6187771807287994
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 12: rounding_ok
**Location:** `generated/trec_means.tex: SimpleLinear`

**Paper text:**

```tex
SimpleLinear & 0.4610 & \textbf{0.5076} & 0.5193 & 0.4299$^{\dagger}$ & 0.5287$^{\dagger}$ & 0.5785 \\
```

**Paper value:** `[0.461, 0.5076, 0.5193, 0.4299, 0.5287, 0.5785]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.46104030699300225,
  0.5075901623712186,
  0.5193021992613991,
  0.42992858085823116,
  0.5286762204098695,
  0.5784937222630202
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 13: rounding_ok
**Location:** `generated/trec_means.tex: Affine ridge`

**Paper text:**

```tex
Affine ridge & 0.4322 & 0.4854 & 0.5012$^{\dagger}$ & 0.2986$^{\dagger}$ & 0.3281$^{\dagger}$ & 0.3278$^{\dagger}$ \\
```

**Paper value:** `[0.4322, 0.4854, 0.5012, 0.2986, 0.3281, 0.3278]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.4321704122423191,
  0.48543765007369555,
  0.5012195177689744,
  0.29862101762519416,
  0.3281386648638847,
  0.3277848331657977
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 14: rounding_ok
**Location:** `generated/trec_means.tex: Converter`

**Paper text:**

```tex
Converter & 0.4224$^{\dagger}$ & 0.4780$^{\dagger}$ & 0.5033 & 0.3056$^{\dagger}$ & 0.3590$^{\dagger}$ & 0.4098$^{\dagger}$ \\
```

**Paper value:** `[0.4224, 0.478, 0.5033, 0.3056, 0.359, 0.4098]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.4223735991713406,
  0.4780470274050105,
  0.5032547704761722,
  0.3055679824401268,
  0.3590215314302837,
  0.40982778236858286
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 15: rounding_ok
**Location:** `generated/trec_means.tex: Native Full-X`

**Paper text:**

```tex
Native Full-X & \multicolumn{3}{c}{0.4935 (native)} & \multicolumn{3}{c}{0.6805 (native)} \\
```

**Paper value:** `[0.4935, 0.6805]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.4934781848463412,
  0.6805416492225224
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 16: rounding_ok
**Location:** `generated/trec_means.tex: Native Full-Y`

**Paper text:**

```tex
Native Full-Y & \multicolumn{3}{c}{0.5203 (native)} & \multicolumn{3}{c}{0.6421 (native)} \\
```

**Paper value:** `[0.5203, 0.6421]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.5202728348242263,
  0.6421134496001705
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 17: rounding_ok
**Location:** `generated/trec_recall.tex: ARC2-Global`

**Paper text:**

```tex
\rowcolor{arcPale}\textbf{ARC2-Global} & \textbf{0.0896} & \textbf{0.0953} & \textbf{0.0998} & \underline{0.0866} & \underline{0.0928} & 0.0997 \\
```

**Paper value:** `[0.0896, 0.0953, 0.0998, 0.0866, 0.0928, 0.0997]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.08963088480259038,
  0.09529158965710632,
  0.09983604059514704,
  0.0865798155941492,
  0.09284227251463124,
  0.09966692928143464
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 18: rounding_ok
**Location:** `generated/trec_recall.tex: Procrustes`

**Paper text:**

```tex
Procrustes & \underline{0.0866} & \underline{0.0935} & \underline{0.0994} & \textbf{0.0886} & \textbf{0.0976} & \textbf{0.1061} \\
```

**Paper value:** `[0.0866, 0.0935, 0.0994, 0.0886, 0.0976, 0.1061]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.08656849639226609,
  0.09348540930621103,
  0.09942876429633421,
  0.08857103007611913,
  0.09757526289269891,
  0.10605638073803039
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 19: rounding_ok
**Location:** `generated/trec_recall.tex: LA2M20`

**Paper text:**

```tex
LA2M20 & 0.0736 & 0.0884 & 0.0983 & 0.0593 & 0.0823 & \underline{0.1016} \\
```

**Paper value:** `[0.0736, 0.0884, 0.0983, 0.0593, 0.0823, 0.1016]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.07356777060172419,
  0.08842284023887333,
  0.09826954011884906,
  0.059325559835467855,
  0.08234134077914587,
  0.10159163083373099
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 20: rounding_ok
**Location:** `generated/trec_recall.tex: SimpleLinear`

**Paper text:**

```tex
SimpleLinear & 0.0626 & 0.0845 & 0.0970 & 0.0296 & 0.0510 & 0.0693 \\
```

**Paper value:** `[0.0626, 0.0845, 0.097, 0.0296, 0.051, 0.0693]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.06257470519773327,
  0.0844776701539496,
  0.09701627700333974,
  0.029643592077240412,
  0.05097373668709944,
  0.06928258053412745
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 21: rounding_ok
**Location:** `generated/trec_recall.tex: Affine ridge`

**Paper text:**

```tex
Affine ridge & 0.0689 & 0.0780 & 0.0856 & 0.0373 & 0.0382 & 0.0366 \\
```

**Paper value:** `[0.0689, 0.078, 0.0856, 0.0373, 0.0382, 0.0366]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.06890134085023747,
  0.0779944968405071,
  0.08563775429812863,
  0.03726425994631427,
  0.038217266219315385,
  0.03657015555736688
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 22: rounding_ok
**Location:** `generated/trec_recall.tex: Converter`

**Paper text:**

```tex
Converter & 0.0651 & 0.0772 & 0.0892 & 0.0422 & 0.0495 & 0.0582 \\
```

**Paper value:** `[0.0651, 0.0772, 0.0892, 0.0422, 0.0495, 0.0582]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.06512050655177726,
  0.07717310564196894,
  0.08920092316113651,
  0.042248049007770475,
  0.04951179253245391,
  0.05824037110988424
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 23: rounding_ok
**Location:** `generated/trec_recall.tex: Native Full-X`

**Paper text:**

```tex
Native Full-X & \multicolumn{3}{c}{0.0936 (native)} & \multicolumn{3}{c}{0.1235 (native)} \\
```

**Paper value:** `[0.0936, 0.1235]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.09355341420637212,
  0.12353038057812048
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 24: rounding_ok
**Location:** `generated/trec_recall.tex: Native Full-Y`

**Paper text:**

```tex
Native Full-Y & \multicolumn{3}{c}{0.1052 (native)} & \multicolumn{3}{c}{0.1162 (native)} \\
```

**Paper value:** `[0.1052, 0.1162]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.10521378018323918,
  0.11624395516879528
]
```

Native references are separate from adapters; pre-rounding order checked below.

### Claim 25: rounding_ok
**Location:** `generated/allpaid.tex: ARC2-Global`

**Paper text:**

```tex
\rowcolor{arcPale}\textbf{ARC2-Global} & \textbf{0.3075} & \underline{0.3671} & \underline{0.6922} & \textbf{0.3116} & 0.2919 & 0.5595 \\
```

**Paper value:** `[0.3075, 0.3671, 0.6922, 0.3116, 0.2919, 0.5595]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.3075048582716371,
  0.36714602143626496,
  0.6922001554001553,
  0.3116352075358866,
  0.29186698206096195,
  0.5594899234099235
]
```



### Claim 26: rounding_ok
**Location:** `generated/allpaid.tex: Procrustes`

**Paper text:**

```tex
Procrustes & 0.2858 & 0.3334$^{\dagger}$ & 0.6905 & \underline{0.3100} & \textbf{0.3362}$^{\ddagger}$ & \textbf{0.6534} \\
```

**Paper value:** `[0.2858, 0.3334, 0.6905, 0.31, 0.3362, 0.6534]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.28582824088854003,
  0.3333864741159597,
  0.6904948307248308,
  0.31003589203103826,
  0.33620246107664287,
  0.653388922188922
]
```



### Claim 27: rounding_ok
**Location:** `generated/allpaid.tex: LA2M20`

**Paper text:**

```tex
LA2M20 & 0.2377 & 0.3389$^{\dagger}$ & \textbf{0.6950} & 0.2300 & \underline{0.3293}$^{\ddagger}$ & \underline{0.6473} \\
```

**Paper value:** `[0.2377, 0.3389, 0.695, 0.23, 0.3293, 0.6473]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.2376740142398725,
  0.3389234669245038,
  0.695005148185148,
  0.22999031724981683,
  0.3293413014310004,
  0.6473306193806192
]
```



### Claim 28: rounding_ok
**Location:** `generated/allpaid.tex: SimpleLinear`

**Paper text:**

```tex
SimpleLinear & 0.2360 & 0.3323$^{\dagger}$ & 0.6778 & 0.1942 & 0.1679$^{\dagger}$ & 0.3618 \\
```

**Paper value:** `[0.236, 0.3323, 0.6778, 0.1942, 0.1679, 0.3618]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.2359531204225403,
  0.3323162470088491,
  0.6777889244089242,
  0.1941674316269752,
  0.16794940738858383,
  0.3617845476745477
]
```



### Claim 29: rounding_ok
**Location:** `generated/allpaid.tex: Affine ridge`

**Paper text:**

```tex
Affine ridge & \underline{0.2890} & \textbf{0.3673} & 0.6800 & 0.1479 & 0.2270$^{\dagger}$ & 0.4245 \\
```

**Paper value:** `[0.289, 0.3673, 0.68, 0.1479, 0.227, 0.4245]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.28904545781234714,
  0.36726327671078884,
  0.6800430125430126,
  0.14792156930525965,
  0.2270145751549427,
  0.42451112110112116
]
```



### Claim 30: rounding_ok
**Location:** `generated/allpaid.tex: Converter`

**Paper text:**

```tex
Converter & 0.2496 & 0.3258$^{\dagger}$ & 0.6633 & 0.1397 & 0.2625 & 0.5789 \\
```

**Paper value:** `[0.2496, 0.3258, 0.6633, 0.1397, 0.2625, 0.5789]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.24963647764120794,
  0.32576143937636975,
  0.6632694838494837,
  0.1396653650449041,
  0.2625194643556271,
  0.5789074192474193
]
```



### Claim 31: rounding_ok
**Location:** `generated/allpaid.tex: Native Full-X`

**Paper text:**

```tex
Native Full-X & \multicolumn{2}{c}{0.3900 (native)} & 0.7002 & \multicolumn{2}{c}{0.3465 (native)} & 0.6453 \\
```

**Paper value:** `[0.39, 0.7002, 0.3465, 0.6453]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.38996146433493817,
  0.7001835830835832,
  0.3464782895762744,
  0.6453320235320233
]
```



### Claim 32: rounding_ok
**Location:** `generated/allpaid.tex: Native Full-Y`

**Paper text:**

```tex
Native Full-Y & \multicolumn{2}{c}{0.4047 (native)} & 0.7039 & \multicolumn{2}{c}{0.3891 (native)} & 0.6968 \\
```

**Paper value:** `[0.4047, 0.7039, 0.3891, 0.6968]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.4047359707946925,
  0.703892218892219,
  0.3891325249294525,
  0.6967968586968585
]
```



### Claim 33: rounding_ok
**Location:** `generated/budget_leverage.tex: FiQA`

**Paper text:**

```tex
FiQA & \cellcolor{arcPale}\textcolor{arcBlue}{0.2731} & 0.2718 & 0.1416 & 0.2781 & 0.1610 & 0.2095 & 0.3465 & 0.3891 \\
```

**Paper value:** `[0.2731, 0.2718, 0.1416, 0.2781, 0.161, 0.2095, 0.3465, 0.3891]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.27310684220470094,
  0.2717780394485493,
  0.14157395302032982,
  0.2781397818845367,
  0.1609714907578672,
  0.2095336751807801,
  0.3464782895762744,
  0.3891325249294525
]
```

Cross-budget comparison is explicitly descriptive.

### Claim 34: rounding_ok
**Location:** `generated/budget_leverage.tex: NanoNQ`

**Paper text:**

```tex
NanoNQ & \cellcolor{arcPale}\textcolor{arcBlue}{0.5071} & 0.4852 & 0.3640 & 0.4839 & 0.4428 & 0.4021 & 0.6595 & 0.6669 \\
```

**Paper value:** `[0.5071, 0.4852, 0.364, 0.4839, 0.4428, 0.4021, 0.6595, 0.6669]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.5071236847804641,
  0.48523704628244235,
  0.36403641053270247,
  0.48387757204577336,
  0.44284099940693855,
  0.40208721230157407,
  0.6595104530695758,
  0.6669078991393519
]
```

Cross-budget comparison is explicitly descriptive.

### Claim 35: rounding_ok
**Location:** `generated/budget_leverage.tex: NanoHotpotQA`

**Paper text:**

```tex
NanoHotpotQA & \cellcolor{arcPale}\textcolor{arcBlue}{0.5845} & 0.5512 & 0.3869 & 0.6174 & 0.5053 & 0.5016 & 0.8278 & 0.8193 \\
```

**Paper value:** `[0.5845, 0.5512, 0.3869, 0.6174, 0.5053, 0.5016, 0.8278, 0.8193]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.5844856557302884,
  0.5512346178902974,
  0.38689849635905205,
  0.6173880843274537,
  0.5053470075849882,
  0.5016332374347163,
  0.8277532428383954,
  0.8192540193891485
]
```

Cross-budget comparison is explicitly descriptive.

### Claim 36: rounding_ok
**Location:** `generated/budget_leverage.tex: NanoFEVER`

**Paper text:**

```tex
NanoFEVER & \cellcolor{arcPale}\textcolor{arcBlue}{0.7555} & 0.7147 & 0.4991 & 0.7087 & 0.7290 & 0.7326 & 0.8984 & 0.8963 \\
```

**Paper value:** `[0.7555, 0.7147, 0.4991, 0.7087, 0.729, 0.7326, 0.8984, 0.8963]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.7554512732607813,
  0.714661665844085,
  0.4990506224837599,
  0.7087460112987809,
  0.7289860142730652,
  0.7325762381767909,
  0.898352760618845,
  0.8963290572938694
]
```

Cross-budget comparison is explicitly descriptive.

### Claim 37: rounding_ok
**Location:** `generated/budget_leverage.tex: TREC-COVID`

**Paper text:**

```tex
\midrule \textbf{TREC-COVID} & \cellcolor{arcPale}\textcolor{arcBlue}{0.5628} & 0.5660 & 0.5206 & 0.5785 & 0.3278 & 0.4098 & 0.6805 & 0.6421 \\
```

**Paper value:** `[0.5628, 0.566, 0.5206, 0.5785, 0.3278, 0.4098, 0.6805, 0.6421]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.562801573213321,
  0.5660420017846071,
  0.5205904360903386,
  0.5784937222630202,
  0.3277848331657977,
  0.40982778236858286,
  0.6805416492225224,
  0.6421134496001705
]
```

Cross-budget comparison is explicitly descriptive.

### Claim 38: rounding_ok
**Location:** `generated/ablation.tex`

**Paper text:**

```tex
Two steps minus zero steps & +0.0243 & [+0.0180, +0.0310] \\
```

**Paper value:** `[0.0243, 0.018, 0.031]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  0.024325109040435233,
  0.01801533254696277,
  0.03102132243820168
]
```

Separate five-contrast family; differs from main-matrix bootstrap draw seed.

### Claim 39: rounding_ok
**Location:** `generated/ablation.tex`

**Paper text:**

```tex
Two steps minus one step & +0.0069 & [+0.0038, +0.0100] \\
```

**Paper value:** `[0.0069, 0.0038, 0.01]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  0.006923862939737235,
  0.003809388309482942,
  0.009959126205904258
]
```

Separate five-contrast family; differs from main-matrix bootstrap draw seed.

### Claim 40: rounding_ok
**Location:** `generated/ablation.tex`

**Paper text:**

```tex
ARC2 minus affine ridge & +0.0957 & [+0.0754, +0.1166] \\
```

**Paper value:** `[0.0957, 0.0754, 0.1166]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  0.09565304927282199,
  0.07535298921225946,
  0.11663127039230592
]
```

Separate five-contrast family; differs from main-matrix bootstrap draw seed.

### Claim 41: rounding_ok
**Location:** `generated/ablation.tex`

**Paper text:**

```tex
$\lambda=1$ minus $\lambda=10$ & +0.0032 & [-0.0019, +0.0083] \\
```

**Paper value:** `[0.0032, -0.0019, 0.0083]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  0.0031974956912717346,
  -0.0018903844098364442,
  0.00830403326634241
]
```

Separate five-contrast family; differs from main-matrix bootstrap draw seed.

### Claim 42: rounding_ok
**Location:** `generated/ablation.tex`

**Paper text:**

```tex
$\lambda=100$ minus $\lambda=10$ & -0.0093 & [-0.0132, -0.0055] \\
```

**Paper value:** `[-0.0093, -0.0132, -0.0055]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  -0.00925533869678723,
  -0.01321398029023485,
  -0.005510245768211927
]
```

Separate five-contrast family; differs from main-matrix bootstrap draw seed.

### Claim 43: exact_match
**Location:** `generated/trec_family.tex: Procrustes`

**Paper text:**

```tex
Procrustes & 0/3/0 & 0/3/0 \\
```

**Paper value:** `[0, 3, 0, 0, 3, 0]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0,
  3,
  0,
  0,
  3,
  0
]
```



### Claim 44: exact_match
**Location:** `generated/trec_family.tex: LA2M20`

**Paper text:**

```tex
LA2M20 & 0/3/0 & 0/3/0 \\
```

**Paper value:** `[0, 3, 0, 0, 3, 0]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0,
  3,
  0,
  0,
  3,
  0
]
```



### Claim 45: exact_match
**Location:** `generated/trec_family.tex: SimpleLinear`

**Paper text:**

```tex
SimpleLinear & 0/3/0 & 2/1/0 \\
```

**Paper value:** `[0, 3, 0, 2, 1, 0]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0,
  3,
  0,
  2,
  1,
  0
]
```



### Claim 46: exact_match
**Location:** `generated/trec_family.tex: Affine ridge`

**Paper text:**

```tex
Affine ridge & 1/2/0 & 3/0/0 \\
```

**Paper value:** `[1, 2, 0, 3, 0, 0]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  1,
  2,
  0,
  3,
  0,
  0
]
```



### Claim 47: exact_match
**Location:** `generated/trec_family.tex: Converter`

**Paper text:**

```tex
Converter & 2/1/0 & 3/0/0 \\
```

**Paper value:** `[2, 1, 0, 3, 0, 0]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  2,
  1,
  0,
  3,
  0,
  0
]
```



### Claim 48: rounding_ok
**Location:** `abstract/results/introduction`

**Paper text:**

```tex
\method{} achieves the highest macro \ndcg{} among the six evaluated
methods (Table~\ref{tab:dev}). Its gain over Procrustes is $0.0243$, with
family-adjusted interval $[0.0181,0.0308]$. The effect extends across both
migrations: descriptive pair-wise gains are $0.0257$ for MiniLM and $0.0229$
for E5. Each of the four collection-level macros also favors ARC2 over every
baseline. At the finer condition level, ARC2 leads Procrustes in 23 of 24
point means and every other baseline in all 24. Figure~\ref{fig:dev-quality}
shows the complete budget curves.
```

**Checked statement:** gain over Procrustes is 0.0243, with family-adjusted interval [0.0181, 0.0308]

**Paper value:** `[0.0243, 0.0181, 0.0308]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.024325109040435233,
  0.018132175212397208,
  0.030791640313948616
]
```



### Claim 49: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
\method{} achieves the highest macro \ndcg{} among the six evaluated
methods (Table~\ref{tab:dev}). Its gain over Procrustes is $0.0243$, with
family-adjusted interval $[0.0181,0.0308]$. The effect extends across both
migrations: descriptive pair-wise gains are $0.0257$ for MiniLM and $0.0229$
for E5. Each of the four collection-level macros also favors ARC2 over every
baseline. At the finer condition level, ARC2 leads Procrustes in 23 of 24
point means and every other baseline in all 24. Figure~\ref{fig:dev-quality}
shows the complete budget curves.
```

**Checked statement:** descriptive pair-wise gains are $0.0257$ for MiniLM and $0.0229$ for E5

**Paper value:** `[0.0257, 0.0229]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.025732936236754725,
  0.022917281844115747
]
```



### Claim 50: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
\method{} achieves the highest macro \ndcg{} among the six evaluated
methods (Table~\ref{tab:dev}). Its gain over Procrustes is $0.0243$, with
family-adjusted interval $[0.0181,0.0308]$. The effect extends across both
migrations: descriptive pair-wise gains are $0.0257$ for MiniLM and $0.0229$
for E5. Each of the four collection-level macros also favors ARC2 over every
baseline. At the finer condition level, ARC2 leads Procrustes in 23 of 24
point means and every other baseline in all 24. Figure~\ref{fig:dev-quality}
shows the complete budget curves.
```

**Checked statement:** ARC2 leads Procrustes in 23 of 24 point means and every other baseline in all 24

**Paper value:** `[23, 24, 24, 24, 24]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  23,
  24,
  24,
  24,
  24
]
```

{'procrustes_global': 23, 'la2m20_integration_script_adaptation': 24, 'simplelinear_official_final50_mlp5': 24, 'ridge_affine_l10_bias_regularized': 24, 'embedding_converter_paper_spec': 24}

### Claim 51: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
\method{} achieves the highest macro \ndcg{} among the six evaluated
methods (Table~\ref{tab:dev}). Its gain over Procrustes is $0.0243$, with
family-adjusted interval $[0.0181,0.0308]$. The effect extends across both
migrations: descriptive pair-wise gains are $0.0257$ for MiniLM and $0.0229$
for E5. Each of the four collection-level macros also favors ARC2 over every
baseline. At the finer condition level, ARC2 leads Procrustes in 23 of 24
point means and every other baseline in all 24. Figure~\ref{fig:dev-quality}
shows the complete budget curves.
```

**Checked statement:** Each of the four collection-level macros also favors ARC2 over every baseline

**Paper value:** `4`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
4
```

{'FiQA': True, 'NanoNQ': True, 'NanoHotpotQA': True, 'NanoFEVER': True}

### Claim 52: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
The improvement concerns top-ranked relevance: macro Recall is $0.8659$
versus Procrustes' $0.8661$, with descriptive difference interval
$[-0.0049,0.0043]$. The single negative Procrustes nDCG point difference is
FiQA/E5 at 75\% ($-0.0036$). Native Full-X and Full-Y provide the
full-corpus operating context.
```

**Checked statement:** macro Recall is $0.8659$ versus Procrustes' $0.8661$, with descriptive difference interval $[-0.0049,0.0043]$

**Paper value:** `[0.8659, 0.8661, -0.0049, 0.0043]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  0.8658612474562474,
  0.8660998378473379,
  -0.004943626172438673,
  0.0043358499949124945
]
```



### Claim 53: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
The improvement concerns top-ranked relevance: macro Recall is $0.8659$
versus Procrustes' $0.8661$, with descriptive difference interval
$[-0.0049,0.0043]$. The single negative Procrustes nDCG point difference is
FiQA/E5 at 75\% ($-0.0036$). Native Full-X and Full-Y provide the
full-corpus operating context.
```

**Checked statement:** FiQA/E5 at 75\% ($-0.0036$)

**Paper value:** `-0.0036`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
-0.00358268756650346
```



### Claim 54: rounding_ok
**Location:** `abstract/introduction/results`

**Paper text:**

```tex
A second correction adds $0.0069$ macro nDCG beyond one step, with family
interval $[0.0038,0.0100]$. The point gain appears in 22 of 24 conditions
and in each of the five seed-level macros. Both updates retain one affine
inference stage. The complete initialized refinement gains $0.0957$ over
affine ridge (Fig.~\ref{fig:ablation}a), jointly evaluating the target and
alignment prior.
```

**Checked statement:** A second correction adds $0.0069$ macro nDCG beyond one step, with family interval $[0.0038,0.0100]$

**Paper value:** `[0.0069, 0.0038, 0.01]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  0.006923862939737235,
  0.003809388309482942,
  0.009959126205904258
]
```



### Claim 55: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
A second correction adds $0.0069$ macro nDCG beyond one step, with family
interval $[0.0038,0.0100]$. The point gain appears in 22 of 24 conditions
and in each of the five seed-level macros. Both updates retain one affine
inference stage. The complete initialized refinement gains $0.0957$ over
affine ridge (Fig.~\ref{fig:ablation}a), jointly evaluating the target and
alignment prior.
```

**Checked statement:** point gain appears in 22 of 24 conditions and in each of the five seed-level macros

**Paper value:** `[22, 5]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json`

**Evidence value:**

```json
[
  22,
  5
]
```



### Claim 56: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
\paragraph{Tangent targeting improves matched residual controls.}
Holding initialization and supervision fixed isolates an additional benefit
on FiQA/MiniLM (Fig.~\ref{fig:ablation}b). ARC2 reaches $0.3075$ nDCG,
versus $0.2935$ for the norm-scaled chordal control, $0.2959$ for Euclidean
residual refinement and $0.2858$ for unrefined Procrustes. The tangent gains
are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$),
respectively, with both differences positive in all five fixed seed means.
The chordal comparison supports removing the radial target component in this
development configuration. It shares the norm-scaling rule, without imposing
identical later states or equal target norms.
```

**Checked statement:** ARC2 reaches $0.3075$ nDCG, versus $0.2935$ for the norm-scaled chordal control, $0.2959$ for Euclidean residual refinement and $0.2858$ for unrefined Procrustes

**Paper value:** `[0.3075, 0.2935, 0.2959, 0.2858]`

**Evidence:** `D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/summary.json`

**Evidence value:**

```json
[
  0.3075048582716371,
  0.2935058031310443,
  0.2959154931179677,
  0.28582824088854003
]
```



### Claim 57: rounding_ok
**Location:** `sections/results.tex/Fig. dev_ablation(b)`

**Paper text:**

```tex
\paragraph{Tangent targeting improves matched residual controls.}
Holding initialization and supervision fixed isolates an additional benefit
on FiQA/MiniLM (Fig.~\ref{fig:ablation}b). ARC2 reaches $0.3075$ nDCG,
versus $0.2935$ for the norm-scaled chordal control, $0.2959$ for Euclidean
residual refinement and $0.2858$ for unrefined Procrustes. The tangent gains
are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$),
respectively, with both differences positive in all five fixed seed means.
The chordal comparison supports removing the radial target component in this
development configuration. It shares the norm-scaling rule, without imposing
identical later states or equal target norms.
```

**Checked statement:** The tangent gains are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$), respectively

**Paper value:** `[0.014, 0.0097, 0.0186]`

**Evidence:** `D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/summary.json`

**Evidence value:**

```json
[
  0.013999055140592891,
  0.009703861642472786,
  0.018620502805854717
]
```



### Claim 58: rounding_ok
**Location:** `sections/results.tex/Fig. dev_ablation(b)`

**Paper text:**

```tex
\paragraph{Tangent targeting improves matched residual controls.}
Holding initialization and supervision fixed isolates an additional benefit
on FiQA/MiniLM (Fig.~\ref{fig:ablation}b). ARC2 reaches $0.3075$ nDCG,
versus $0.2935$ for the norm-scaled chordal control, $0.2959$ for Euclidean
residual refinement and $0.2858$ for unrefined Procrustes. The tangent gains
are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$),
respectively, with both differences positive in all five fixed seed means.
The chordal comparison supports removing the radial target component in this
development configuration. It shares the norm-scaling rule, without imposing
identical later states or equal target norms.
```

**Checked statement:** The tangent gains are $0.0140$ ($[0.0097,0.0186]$) and $0.0116$ ($[0.0078,0.0157]$), respectively

**Paper value:** `[0.0116, 0.0078, 0.0157]`

**Evidence:** `D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/summary.json`

**Evidence value:**

```json
[
  0.011589365153669408,
  0.007820844428750586,
  0.015656396532695304
]
```



### Claim 59: rounding_ok
**Location:** `abstract`

**Paper text:**

```tex
begin{abstract}
Embedding-model upgrades must preserve retrieval quality while document re-encoding proceeds under a limited budget. We propose \method, a compact document adapter that refines centered Procrustes alignment with two ridge-fitted tangent corrections. The updates target cosine-relevant directions and collapse into one affine map, preserving native destination queries without neural mapper training. Across four development collections, two encoder migrations and three anchor-inclusive budgets, \method\ achieves the highest macro \ndcg\ among six evaluated methods. Its gain over Procrustes is 0.0243, with family-adjusted interval [0.0181, 0.0308]; the second correction adds 0.0069. Matched-initialization FiQA/MiniLM controls also favor tangent targeting over chordal and Euclidean residuals, with positive corrected intervals. On prospective TREC-COVID/E5, gains over the evaluated Converter range from 0.2000 to 0.2572. A descriptive comparison across all five collections further shows E5 ARC2 at 25\% coverage exceeding Converter and affine ridge at 75\%. On TREC-COVID/MiniLM, 75\% coverage yields 0.5195 nDCG versus native Full-Y's 0.5203, with the highest Recall@100 point mean among the six adapters. The final 384-to-768-dimensional coefficient matrix occupies 1.13\,MiB, using 114.7 times fewer parameter bytes than the evaluated Converter.
\keywords{Embedding migration \and Vector retrieval \and Representation alignment \and Mixed galleries}
\end{abstract}
```

**Checked statement:** gains over the evaluated Converter range from 0.2000 to 0.2572

**Paper value:** `[0.2, 0.2572]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.1999540966512042,
  0.25723359077319435
]
```



### Claim 60: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
On the held collection, E5 ARC2 exceeds the evaluated Converter and affine
ridge at \textbf{all three migration budgets}. At 25\% coverage, the
Converter gain is $0.2572$, with family interval $[0.1757,0.3376]$. At 50\%,
ARC2 reaches $0.5904$ nDCG versus Converter's $0.3590$ and ridge's $0.3281$
(Table~\ref{tab:trec}). Across both migrations, the 30-contrast family supports
five improvements over Converter, four over ridge and two over SimpleLinear.
The table marks all eleven supported comparisons.
```

**Checked statement:** Converter gain is $0.2572$, with family interval $[0.1757,0.3376]$

**Paper value:** `[0.2572, 0.1757, 0.3376]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.25723359077319435,
  0.17573076152800798,
  0.33756850203860655
]
```



### Claim 61: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
On the held collection, E5 ARC2 exceeds the evaluated Converter and affine
ridge at \textbf{all three migration budgets}. At 25\% coverage, the
Converter gain is $0.2572$, with family interval $[0.1757,0.3376]$. At 50\%,
ARC2 reaches $0.5904$ nDCG versus Converter's $0.3590$ and ridge's $0.3281$
(Table~\ref{tab:trec}). Across both migrations, the 30-contrast family supports
five improvements over Converter, four over ridge and two over SimpleLinear.
The table marks all eleven supported comparisons.
```

**Checked statement:** At 50\%, ARC2 reaches $0.5904$ nDCG versus Converter's $0.3590$ and ridge's $0.3281$

**Paper value:** `[0.5904, 0.359, 0.3281]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.5904061066004364,
  0.3590215314302837,
  0.3281386648638847
]
```



### Claim 62: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
On the held collection, E5 ARC2 exceeds the evaluated Converter and affine
ridge at \textbf{all three migration budgets}. At 25\% coverage, the
Converter gain is $0.2572$, with family interval $[0.1757,0.3376]$. At 50\%,
ARC2 reaches $0.5904$ nDCG versus Converter's $0.3590$ and ridge's $0.3281$
(Table~\ref{tab:trec}). Across both migrations, the 30-contrast family supports
five improvements over Converter, four over ridge and two over SimpleLinear.
The table marks all eleven supported comparisons.
```

**Checked statement:** five improvements over Converter, four over ridge and two over SimpleLinear; all eleven supported comparisons

**Paper value:** `[5, 4, 2, 11]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  5,
  4,
  2,
  11
]
```

{'procrustes_global': 0, 'la2m20_integration_script_adaptation': 0, 'simplelinear_official_final50_mlp5': 2, 'ridge_affine_l10_bias_regularized': 4, 'embedding_converter_paper_spec': 5}

### Claim 63: rounding_ok
**Location:** `sections/results.tex/abstract`

**Paper text:**

```tex
MiniLM provides a useful partial-migration operating point: at 75\% coverage,
ARC2 reaches $0.5195$ nDCG versus native Full-Y's $0.5203$, while one quarter
of the gallery still uses proxies. Its Recall@100 point mean is the highest
among the six adapters at each budget, reaching $0.0998$ at 75\% versus
native Full-Y's $0.1052$. E5 reaches $0.0997$ Recall at 75\%, versus Full-Y's
$0.1162$ (Fig.~\ref{fig:trec-quality}). These auxiliary results distinguish
coverage at 100 from relevance near the top; proximity in nDCG is not an
equivalence test.
```

**Checked statement:** at 75\% coverage, ARC2 reaches $0.5195$ nDCG versus native Full-Y's $0.5203$

**Paper value:** `[0.5195, 0.5203]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.519513052034007,
  0.5202728348242263
]
```



### Claim 64: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
MiniLM provides a useful partial-migration operating point: at 75\% coverage,
ARC2 reaches $0.5195$ nDCG versus native Full-Y's $0.5203$, while one quarter
of the gallery still uses proxies. Its Recall@100 point mean is the highest
among the six adapters at each budget, reaching $0.0998$ at 75\% versus
native Full-Y's $0.1052$. E5 reaches $0.0997$ Recall at 75\%, versus Full-Y's
$0.1162$ (Fig.~\ref{fig:trec-quality}). These auxiliary results distinguish
coverage at 100 from relevance near the top; proximity in nDCG is not an
equivalence test.
```

**Checked statement:** Recall@100 point mean is the highest among the six adapters at each budget

**Paper value:** `3`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
3
```



### Claim 65: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
MiniLM provides a useful partial-migration operating point: at 75\% coverage,
ARC2 reaches $0.5195$ nDCG versus native Full-Y's $0.5203$, while one quarter
of the gallery still uses proxies. Its Recall@100 point mean is the highest
among the six adapters at each budget, reaching $0.0998$ at 75\% versus
native Full-Y's $0.1052$. E5 reaches $0.0997$ Recall at 75\%, versus Full-Y's
$0.1162$ (Fig.~\ref{fig:trec-quality}). These auxiliary results distinguish
coverage at 100 from relevance near the top; proximity in nDCG is not an
equivalence test.
```

**Checked statement:** reaching $0.0998$ at 75\% versus native Full-Y's $0.1052$. E5 reaches $0.0997$ Recall at 75\%, versus Full-Y's $0.1162$

**Paper value:** `[0.0998, 0.1052, 0.0997, 0.1162]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  0.09983604059514704,
  0.10521378018323918,
  0.09966692928143464,
  0.11624395516879528
]
```



### Claim 66: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
Geometric alignment remains competitive: before rounding, Procrustes has
higher nDCG point means in all six cells, although its MiniLM/75\% difference
is below $0.0001$. All Procrustes and LA2M nDCG family intervals cross zero.
The confirmed advantages therefore concern the evaluated Converter, ridge
and SimpleLinear configurations.
```

**Checked statement:** Procrustes has higher nDCG point means in all six cells

**Paper value:** `6`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
6
```

[-5.136066855163088e-05, -0.004666870465219521, -2.3564924613148544e-05, -0.0032404285712858832, -0.01632154204848677, -0.010011959658702082]

### Claim 67: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
Geometric alignment remains competitive: before rounding, Procrustes has
higher nDCG point means in all six cells, although its MiniLM/75\% difference
is below $0.0001$. All Procrustes and LA2M nDCG family intervals cross zero.
The confirmed advantages therefore concern the evaluated Converter, ridge
and SimpleLinear configurations.
```

**Checked statement:** MiniLM/75\% difference is below $0.0001$

**Paper value:** `true`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
true
```



### Claim 68: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
\subsection{Higher E5 Quality at Lower Document Exposure}
\input{generated/budget_leverage}
A useful budget pattern extends across all five collections
(Table~\ref{tab:budget-leverage}): E5 ARC2 at 25\% coverage exceeds both
Converter and affine ridge at 75\%. On TREC-COVID, the respective nDCG means
are $0.5628$, $0.4098$ and $0.3278$. The advantage is visible even after the
two comparators receive a much larger set of true destination vectors.
```

**Checked statement:** All Procrustes and LA2M nDCG family intervals cross zero

**Paper value:** `12`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
12
```



### Claim 69: exact_match
**Location:** `abstract/introduction/results/generated/budget_leverage caption`

**Paper text:**

```tex
\subsection{Paid Pairs Strengthen MiniLM Adaptation}
\input{generated/allpaid}
Using already-paid pairs improves MiniLM adaptation without increasing the
50\% document budget. ARC2 rises from $0.3075$ to $0.3671$ nDCG, a gain of
$0.0596$ with family interval $[0.0393,0.0806]$. In matched all-paid
comparisons it exceeds Procrustes, LA2M, SimpleLinear and Converter; ridge is
unresolved. Table~\ref{tab:allpaid} makes these family decisions visible.
```

**Checked statement:** E5 ARC2 at 25\% coverage exceeds both Converter and affine ridge at 75\% on all five collections

**Paper value:** `5`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
5
```

Also checked TREC raw summary; no matched-budget significance inferred.

### Claim 70: rounding_ok
**Location:** `introduction/results`

**Paper text:**

```tex
\subsection{Paid Pairs Strengthen MiniLM Adaptation}
\input{generated/allpaid}
Using already-paid pairs improves MiniLM adaptation without increasing the
50\% document budget. ARC2 rises from $0.3075$ to $0.3671$ nDCG, a gain of
$0.0596$ with family interval $[0.0393,0.0806]$. In matched all-paid
comparisons it exceeds Procrustes, LA2M, SimpleLinear and Converter; ridge is
unresolved. Table~\ref{tab:allpaid} makes these family decisions visible.
```

**Checked statement:** gain of $0.0596$ with family interval $[0.0393,0.0806]$

**Paper value:** `[0.0596, 0.0393, 0.0806]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.05964116316462802,
  0.03934110686868015,
  0.08060437708604837
]
```



### Claim 71: exact_match
**Location:** `sections/results.tex: all-paid ordering minilm_distilroberta`

**Paper text:**

```tex
E5 changes the method ordering: ARC2 trails all-paid Procrustes and LA2M,
exceeds SimpleLinear and ridge, and is unresolved against Converter. Its
fixed-to-all-paid change, $0.3116$ to $0.2919$, is unresolved. Fixed-anchor
MiniLM ARC2 also trails every all-paid baseline in the cross-regime family
comparisons. All-paid fitting retains $\lambda=10$ in the summed objective;
it tests the fixed procedure at larger supervision, rather than isolating
data quantity at a fixed effective penalty.
```

**Checked statement:** In matched all-paid comparisons / E5 changes the method ordering

**Paper value:** `{"procrustes_global": "above_zero", "la2m20_integration_script_adaptation": "above_zero", "simplelinear_official_final50_mlp5": "above_zero", "ridge_affine_l10_bias_regularized": "unresolved", "embedding_converter_paper_spec": "above_zero"}`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
{
  "procrustes_global": "above_zero",
  "la2m20_integration_script_adaptation": "above_zero",
  "simplelinear_official_final50_mlp5": "above_zero",
  "ridge_affine_l10_bias_regularized": "unresolved",
  "embedding_converter_paper_spec": "above_zero"
}
```



### Claim 72: exact_match
**Location:** `sections/results.tex: all-paid ordering e5_small_base`

**Paper text:**

```tex
E5 changes the method ordering: ARC2 trails all-paid Procrustes and LA2M,
exceeds SimpleLinear and ridge, and is unresolved against Converter. Its
fixed-to-all-paid change, $0.3116$ to $0.2919$, is unresolved. Fixed-anchor
MiniLM ARC2 also trails every all-paid baseline in the cross-regime family
comparisons. All-paid fitting retains $\lambda=10$ in the summed objective;
it tests the fixed procedure at larger supervision, rather than isolating
data quantity at a fixed effective penalty.
```

**Checked statement:** In matched all-paid comparisons / E5 changes the method ordering

**Paper value:** `{"procrustes_global": "below_zero", "la2m20_integration_script_adaptation": "below_zero", "simplelinear_official_final50_mlp5": "above_zero", "ridge_affine_l10_bias_regularized": "above_zero", "embedding_converter_paper_spec": "unresolved"}`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
{
  "procrustes_global": "below_zero",
  "la2m20_integration_script_adaptation": "below_zero",
  "simplelinear_official_final50_mlp5": "above_zero",
  "ridge_affine_l10_bias_regularized": "above_zero",
  "embedding_converter_paper_spec": "unresolved"
}
```



### Claim 73: exact_match
**Location:** `sections/results.tex`

**Paper text:**

```tex
E5 changes the method ordering: ARC2 trails all-paid Procrustes and LA2M,
exceeds SimpleLinear and ridge, and is unresolved against Converter. Its
fixed-to-all-paid change, $0.3116$ to $0.2919$, is unresolved. Fixed-anchor
MiniLM ARC2 also trails every all-paid baseline in the cross-regime family
comparisons. All-paid fitting retains $\lambda=10$ in the summed objective;
it tests the fixed procedure at larger supervision, rather than isolating
data quantity at a fixed effective penalty.
```

**Checked statement:** Fixed-anchor MiniLM ARC2 also trails every all-paid baseline in the cross-regime family comparisons

**Paper value:** `5`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
5
```



### Claim 74: rounding_ok
**Location:** `sections/results.tex: replacement minilm_distilroberta`

**Paper text:**

```tex
\paragraph{Evaluate the gallery that will be searched.}
With each fitted map fixed, true-vector replacement raises MiniLM all-paid
nDCG from $0.3510$ to $0.3671$, but lowers E5 from $0.3149$ to $0.2919$.
For E5, Recall falls from $0.6542$ to $0.5595$ and the paid-document share of
top-10 results falls from $0.4916$ to $0.0647$, despite 50\% paid coverage.
These measured replacement effects make mixed-gallery relevance the
appropriate selection criterion: proxy-only quality can favor a different
operating point from the gallery containing native and mapped vectors.
```

**Checked statement:** true-vector replacement raises MiniLM all-paid nDCG from $0.3510$ to $0.3671$, but lowers E5 from $0.3149$ to $0.2919$

**Paper value:** `[0.351, 0.3671]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1g_r1_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.3509507352060274,
  0.36714602143626507
]
```



### Claim 75: rounding_ok
**Location:** `sections/results.tex: replacement e5_small_base`

**Paper text:**

```tex
\paragraph{Evaluate the gallery that will be searched.}
With each fitted map fixed, true-vector replacement raises MiniLM all-paid
nDCG from $0.3510$ to $0.3671$, but lowers E5 from $0.3149$ to $0.2919$.
For E5, Recall falls from $0.6542$ to $0.5595$ and the paid-document share of
top-10 results falls from $0.4916$ to $0.0647$, despite 50\% paid coverage.
These measured replacement effects make mixed-gallery relevance the
appropriate selection criterion: proxy-only quality can favor a different
operating point from the gallery containing native and mapped vectors.
```

**Checked statement:** true-vector replacement raises MiniLM all-paid nDCG from $0.3510$ to $0.3671$, but lowers E5 from $0.3149$ to $0.2919$

**Paper value:** `[0.3149, 0.2919]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1g_r1_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.31490775036459107,
  0.29186698206096207
]
```



### Claim 76: rounding_ok
**Location:** `sections/results.tex`

**Paper text:**

```tex
\paragraph{Evaluate the gallery that will be searched.}
With each fitted map fixed, true-vector replacement raises MiniLM all-paid
nDCG from $0.3510$ to $0.3671$, but lowers E5 from $0.3149$ to $0.2919$.
For E5, Recall falls from $0.6542$ to $0.5595$ and the paid-document share of
top-10 results falls from $0.4916$ to $0.0647$, despite 50\% paid coverage.
These measured replacement effects make mixed-gallery relevance the
appropriate selection criterion: proxy-only quality can favor a different
operating point from the gallery containing native and mapped vectors.
```

**Checked statement:** For E5, Recall falls from $0.6542$ to $0.5595$ and the paid-document share of top-10 results falls from $0.4916$ to $0.0647$

**Paper value:** `[0.6542, 0.5595, 0.4916, 0.0647]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1g_r1_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  0.6541642457542457,
  0.5594899234099234,
  0.49164,
  0.06472000000000001
]
```



### Claim 77: exact_match
**Location:** `sections/discussion.tex`

**Paper text:**

```tex
\paragraph{When the adapter is useful.}
ARC2 targets required destination-model queries during staged document
replacement. E5 demonstrates useful quality at limited exposure; MiniLM
benefits from fitting all paid pairs without increasing document coverage.
Procrustes and LA2M remain competitive on the held collection, so deployment
choice should follow encoder-specific mixed-gallery validation. When source
queries remain acceptable, Full-X is also viable: all 24 partial-development
five-seed ARC2 condition means are below it.
```

**Checked statement:** all 24 partial-development five-seed ARC2 condition means are below [Full-X]

**Paper value:** `24`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
24
```



### Claim 78: exact_match
**Location:** `abstract/method/discussion`

**Paper text:**

```tex
The final mapper has $pd_t$ coefficients regardless of anchor count. For
$384\!\rightarrow\!768$, this is $295{,}680$ float32 values, or $1{,}182{,}720$
bytes ($1.13$\,MiB), including the intercept. This is coefficient storage;
fitting objects, document galleries, and encoder weights are additional.
Application requires one affine multiplication and normalization per document,
with $O(Npd_t)$ arithmetic for a complete proxy gallery.
```

**Checked statement:** 295,680 float32 values, or 1,182,720 bytes (1.13 MiB)

**Paper value:** `[295680, 1182720, 1.13]`

**Evidence:** `D:\DASFAA-2027-paper\src\arc2_global\model.py`

**Evidence value:**

```json
[
  295680,
  1182720,
  1.13
]
```



### Claim 79: exact_match
**Location:** `abstract/discussion`

**Paper text:**

```tex
section{Practical Value of Directional Adaptation}
\label{sec:discussion}
\paragraph{Compact inference with stronger development ranking.}
The 295,680 float32 coefficients occupy 1.13\,MiB, or 114.7 times fewer
parameter bytes than the evaluated Converter. Both corrections are absorbed
into this matrix. Affine ridge has the same coefficient count; refinement
provides the measured quality benefit, while affine mapping provides compactness.
```

**Checked statement:** 114.7 times fewer parameter bytes than the evaluated Converter

**Paper value:** `114.7`

**Evidence:** `D:\DASFAA-2027-paper\src\arc2_global\embedding_converter.py`

**Evidence value:**

```json
114.7
```

Converter=33927168 float32 parameters; ARC2=295680; ratio=114.74285714285715.

### Claim 80: exact_match
**Location:** `generated/dev_macro.tex: bold/underline`

**Paper text:**

```tex
\caption{Development means at matched 1,024-pair supervision, equally weighting 24 conditions. Differences are ARC2 minus baseline; intervals give approximate 95\% family coverage. Bold/underline mark the best/second unrounded adapter means; blue identifies ARC2.}
```

**Checked statement:** Bold/underline rank adapter means before rounding

**Paper value:** `["best", "second", "second", "best", "other", "other", "other", "other", "other", "other", "other", "other"]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
[
  "best",
  "second",
  "second",
  "best",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other"
]
```



### Claim 81: exact_match
**Location:** `generated/trec_means.tex: bold/underline`

**Paper text:**

```tex
\caption{Prospective TREC-COVID nDCG@10 (higher is better), averaged over five seeds. $\dagger$: positive ARC2-minus-baseline interval in the 30-contrast family. Unmarked baseline cells are unresolved. Bold/underline rank the six adapters before rounding; native references are separate.}
```

**Checked statement:** Bold/underline rank adapter means before rounding

**Paper value:** `["other", "other", "second", "second", "second", "other", "second", "other", "best", "best", "best", "best", "best", "second", "other", "other", "other", "second", "other", "best", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other"]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  "other",
  "other",
  "second",
  "second",
  "second",
  "other",
  "second",
  "other",
  "best",
  "best",
  "best",
  "best",
  "best",
  "second",
  "other",
  "other",
  "other",
  "second",
  "other",
  "best",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other"
]
```



### Claim 82: exact_match
**Location:** `generated/trec_recall.tex: bold/underline`

**Paper text:**

```tex
\caption{Companion prospective Recall@100 means (higher is better). All queries and five seeds are retained. Bold/underline rank the six adapters before rounding. Recall is auxiliary/descriptive and receives no nDCG-family significance markers.}
```

**Checked statement:** Bold/underline rank adapter means before rounding

**Paper value:** `["best", "best", "best", "second", "second", "other", "second", "second", "second", "best", "best", "best", "other", "other", "other", "other", "other", "second", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other"]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  "best",
  "best",
  "best",
  "second",
  "second",
  "other",
  "second",
  "second",
  "second",
  "best",
  "best",
  "best",
  "other",
  "other",
  "other",
  "other",
  "other",
  "second",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other"
]
```



### Claim 83: exact_match
**Location:** `generated/allpaid.tex: bold/underline`

**Paper text:**

```tex
\caption{FiQA at 50\% coverage. Fixed/All fit 1,024/28,819 pairs; N/R denote nDCG@10/Recall@100. On All-N baseline cells, $\dagger$/$\ddagger$ mark positive/negative ARC2 differences in the 32-contrast family; unmarked comparisons are unresolved. Bold/underline rank matched adapter columns; native rows are references.}
```

**Checked statement:** Bold/underline rank adapter means before rounding

**Paper value:** `["best", "second", "second", "best", "other", "other", "other", "other", "other", "second", "best", "best", "other", "other", "best", "other", "second", "second", "other", "other", "other", "other", "other", "other", "second", "best", "other", "other", "other", "other", "other", "other", "other", "other", "other", "other"]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  "best",
  "second",
  "second",
  "best",
  "other",
  "other",
  "other",
  "other",
  "other",
  "second",
  "best",
  "best",
  "other",
  "other",
  "best",
  "other",
  "second",
  "second",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "second",
  "best",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other",
  "other"
]
```



### Claim 84: exact_match
**Location:** `generated/trec_means.tex: significance markers`

**Paper text:**

```tex
\caption{Prospective TREC-COVID nDCG@10 (higher is better), averaged over five seeds. $\dagger$: positive ARC2-minus-baseline interval in the 30-contrast family. Unmarked baseline cells are unresolved. Bold/underline rank the six adapters before rounding; native references are separate.}
```

**Checked statement:** All baseline interval markers use the declared comparison family

**Paper value:** `["unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "unresolved", "positive", "positive", "unresolved", "unresolved", "unresolved", "positive", "positive", "positive", "positive", "positive", "positive", "unresolved", "positive", "positive", "positive"]`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
[
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "unresolved",
  "positive",
  "positive",
  "unresolved",
  "unresolved",
  "unresolved",
  "positive",
  "positive",
  "positive",
  "positive",
  "positive",
  "positive",
  "unresolved",
  "positive",
  "positive",
  "positive"
]
```



### Claim 85: exact_match
**Location:** `generated/allpaid.tex: significance markers`

**Paper text:**

```tex
\caption{FiQA at 50\% coverage. Fixed/All fit 1,024/28,819 pairs; N/R denote nDCG@10/Recall@100. On All-N baseline cells, $\dagger$/$\ddagger$ mark positive/negative ARC2 differences in the 32-contrast family; unmarked comparisons are unresolved. Bold/underline rank matched adapter columns; native rows are references.}
```

**Checked statement:** All baseline interval markers use the declared comparison family

**Paper value:** `["above_zero", "below_zero", "above_zero", "below_zero", "above_zero", "above_zero", "unresolved", "above_zero", "above_zero", "unresolved"]`

**Evidence:** `D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json`

**Evidence value:**

```json
[
  "above_zero",
  "below_zero",
  "above_zero",
  "below_zero",
  "above_zero",
  "above_zero",
  "unresolved",
  "above_zero",
  "above_zero",
  "unresolved"
]
```



### Claim 86: exact_match
**Location:** `sections/experimental-setup.tex`

**Paper text:**

```tex
\paragraph{Collections and migrations.}
Development uses FiQA (57,638 documents, 500 development queries), NanoNQ
(5,035/50), NanoHotpotQA (5,090/50), and NanoFEVER (4,996/50), drawn from
BEIR and NanoBEIR~\cite{beir2021,nanobeir}. FiQA informed method selection
after its scores were inspected; all four collections are development evidence.
We subsequently fixed a separate confirmation on the BEIR release of
TREC-COVID~\cite{treccovid2020,beir2021}. Its input manifest contains all
171,332 documents and 50 queries. For this study, labels remained
closed until every ranking and endpoint had been sealed and separately
verified. This distinguishes development evidence from the prospective test.
We evaluate two 384-to-768-dimensional migrations:
\texttt{all-MiniLM-L6-v2} to \texttt{all-distilroberta-v1}, and
\texttt{e5-small-v2} to \texttt{e5-base-v2}.\footnote{Pinned maintainer cards:
\href{https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md}{MiniLM},
\href{https://huggingface.co/sentence-transformers/all-distilroberta-v1/blob/842eaed40bee4d61673a81c92d5689a8fed7a09f/README.md}{DistilRoBERTa},
\href{https://huggingface.co/intfloat/e5-small-v2/blob/ffb93f3bd4047442299a41ebb6fa998a38507c52/README.md}{E5-small}, and
\href{https://huggingface.co/intfloat/e5-base-v2/blob/f52bf8ec8c7124536f0efb74aca902b2995e5bcd/README.md}{E5-base}.}
Model revisions and input hashes are pinned. Text encoding uses normalized
float32 vectors, a maximum of 128 tokens, and the E5 query/passage prefixes.
```

**Checked statement:** Development uses FiQA (57,638 documents, 500 development queries), NanoNQ (5,035/50), NanoHotpotQA (5,090/50), and NanoFEVER (4,996/50)

**Paper value:** `[{"name": "NanoNQ", "docs": 5035, "queries": 50}, {"name": "NanoHotpotQA", "docs": 5090, "queries": 50}, {"name": "NanoFEVER", "docs": 4996, "queries": 50}, {"name": "FiQA", "docs": 57638, "queries": 500}]`

**Evidence:** `D:/DASFAA-2027-paper/configs/datasets.json`

**Evidence value:**

```json
[
  {
    "name": "NanoNQ",
    "docs": 5035,
    "queries": 50
  },
  {
    "name": "NanoHotpotQA",
    "docs": 5090,
    "queries": 50
  },
  {
    "name": "NanoFEVER",
    "docs": 4996,
    "queries": 50
  },
  {
    "name": "FiQA",
    "docs": 57638,
    "queries": 500
  }
]
```

Registry counts agree with locked Nano manifests and per-query array axes. FiQA is explicitly development.

### Claim 87: exact_match
**Location:** `sections/experimental-setup.tex`

**Paper text:**

```tex
\paragraph{Collections and migrations.}
Development uses FiQA (57,638 documents, 500 development queries), NanoNQ
(5,035/50), NanoHotpotQA (5,090/50), and NanoFEVER (4,996/50), drawn from
BEIR and NanoBEIR~\cite{beir2021,nanobeir}. FiQA informed method selection
after its scores were inspected; all four collections are development evidence.
We subsequently fixed a separate confirmation on the BEIR release of
TREC-COVID~\cite{treccovid2020,beir2021}. Its input manifest contains all
171,332 documents and 50 queries. For this study, labels remained
closed until every ranking and endpoint had been sealed and separately
verified. This distinguishes development evidence from the prospective test.
We evaluate two 384-to-768-dimensional migrations:
\texttt{all-MiniLM-L6-v2} to \texttt{all-distilroberta-v1}, and
\texttt{e5-small-v2} to \texttt{e5-base-v2}.\footnote{Pinned maintainer cards:
\href{https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md}{MiniLM},
\href{https://huggingface.co/sentence-transformers/all-distilroberta-v1/blob/842eaed40bee4d61673a81c92d5689a8fed7a09f/README.md}{DistilRoBERTa},
\href{https://huggingface.co/intfloat/e5-small-v2/blob/ffb93f3bd4047442299a41ebb6fa998a38507c52/README.md}{E5-small}, and
\href{https://huggingface.co/intfloat/e5-base-v2/blob/f52bf8ec8c7124536f0efb74aca902b2995e5bcd/README.md}{E5-base}.}
Model revisions and input hashes are pinned. Text encoding uses normalized
float32 vectors, a maximum of 128 tokens, and the E5 query/passage prefixes.
```

**Checked statement:** Its input manifest contains all 171,332 documents and 50 queries

**Paper value:** `{"docs": 171332, "queries": 50}`

**Evidence:** `D:/DASFAA-2027-paper/configs/b2_lock.json`

**Evidence value:**

```json
{
  "docs": 171332,
  "queries": 50
}
```



### Claim 88: exact_match
**Location:** `sections/experimental-setup.tex`

**Paper text:**

```tex
\paragraph{Collections and migrations.}
Development uses FiQA (57,638 documents, 500 development queries), NanoNQ
(5,035/50), NanoHotpotQA (5,090/50), and NanoFEVER (4,996/50), drawn from
BEIR and NanoBEIR~\cite{beir2021,nanobeir}. FiQA informed method selection
after its scores were inspected; all four collections are development evidence.
We subsequently fixed a separate confirmation on the BEIR release of
TREC-COVID~\cite{treccovid2020,beir2021}. Its input manifest contains all
171,332 documents and 50 queries. For this study, labels remained
closed until every ranking and endpoint had been sealed and separately
verified. This distinguishes development evidence from the prospective test.
We evaluate two 384-to-768-dimensional migrations:
\texttt{all-MiniLM-L6-v2} to \texttt{all-distilroberta-v1}, and
\texttt{e5-small-v2} to \texttt{e5-base-v2}.\footnote{Pinned maintainer cards:
\href{https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md}{MiniLM},
\href{https://huggingface.co/sentence-transformers/all-distilroberta-v1/blob/842eaed40bee4d61673a81c92d5689a8fed7a09f/README.md}{DistilRoBERTa},
\href{https://huggingface.co/intfloat/e5-small-v2/blob/ffb93f3bd4047442299a41ebb6fa998a38507c52/README.md}{E5-small}, and
\href{https://huggingface.co/intfloat/e5-base-v2/blob/f52bf8ec8c7124536f0efb74aca902b2995e5bcd/README.md}{E5-base}.}
Model revisions and input hashes are pinned. Text encoding uses normalized
float32 vectors, a maximum of 128 tokens, and the E5 query/passage prefixes.
```

**Checked statement:** For this study, labels remained closed until every ranking and endpoint had been sealed and separately verified

**Paper value:** `{"lock_access_policy": "qrel-free until all184 sealed and separately verified", "ranking_cells": 184, "ranking_seal": "08e82c19a2d1974edb094e520d0b1b6ac4e6138e3a717c5014d183669c7c25de", "verification_seal": "78e67ab2aac47d0590db54ffd20170c30f8e7a5c96153bf17a1fee1e5322c968"}`

**Evidence:** `D:/DASFAA-2027-paper/configs/b2_lock.json`

**Evidence value:**

```json
{
  "lock_access_policy": "qrel-free until all184 sealed and separately verified",
  "ranking_cells": 184,
  "ranking_seal": "08e82c19a2d1974edb094e520d0b1b6ac4e6138e3a717c5014d183669c7c25de",
  "verification_seal": "78e67ab2aac47d0590db54ffd20170c30f8e7a5c96153bf17a1fee1e5322c968"
}
```

Supported by pre-run access policy and distinct seals in raw scoring metadata; this claim audit does not re-run historical seal verification.

### Claim 89: exact_match
**Location:** `sections/experimental-setup.tex`

**Paper text:**

```tex
\paragraph{Matched supervision and exposure.}
The main matrix crosses four development collections, two migrations,
three paid-document budgets (25/50/75\%), six methods, and seeds
17, 29, 41, 53, and 67. All methods fit the same ordered 1,024 paired anchors
and replace the same paid document rows. Paid sets contain all anchors and
are nested, with exactly $\lfloor \rho N\rfloor$ unique target document vectors;
the accounting is $|A\cup S|$, including anchors. On the Nano collections and
TREC-COVID, independent seeded streams sample anchors without replacement
and a document permutation; unseen permutation rows fill the budget. FiQA
retains its historical anchor/order arrays. Neither fitting nor selection uses
relevance labels. Paid nonanchor vectors provide replacement only in this
fixed-anchor regime. A separate FiQA experiment holds the 50\% paid set
fixed and compares fitting on 1,024 versus all 28,819 paid pairs.
Development fixed-anchor ARC2 rankings use the float64 dual backend;
all-paid and TREC-COVID fits use the float64 primal backend in
Sect.~\ref{sec:method-cost}. The all-paid study reuses the dual fixed-anchor
comparisons. Both backends implement the same two-update rule.
```

**Checked statement:** The main matrix crosses four development collections, two migrations, three paid-document budgets (25/50/75%), six methods, and seeds 17, 29, 41, 53, and 67

**Paper value:** `{"collections": 4, "pairs": ["minilm_distilroberta", "e5_small_base"], "budgets": ["25pct", "50pct", "75pct"], "methods": ["arc2_global_tangent2_r1", "procrustes_global", "la2m20_integration_script_adaptation", "simplelinear_official_final50_mlp5", "ridge_affine_l10_bias_regularized", "embedding_converter_paper_spec"], "seeds": [17, 29, 41, 53, 67], "raw_conditions": 24}`

**Evidence:** `D:/DASFAA-2027-paper/configs/b1c_r3_lock.json`

**Evidence value:**

```json
{
  "collections": 4,
  "pairs": [
    "minilm_distilroberta",
    "e5_small_base"
  ],
  "budgets": [
    "25pct",
    "50pct",
    "75pct"
  ],
  "methods": [
    "arc2_global_tangent2_r1",
    "procrustes_global",
    "la2m20_integration_script_adaptation",
    "simplelinear_official_final50_mlp5",
    "ridge_affine_l10_bias_regularized",
    "embedding_converter_paper_spec"
  ],
  "seeds": [
    17,
    29,
    41,
    53,
    67
  ],
  "raw_conditions": 24
}
```

Raw per-query indexes contain all 24 conditions and each of five seeds; no best-seed selection.

### Claim 90: exact_match
**Location:** `sections/method.tex / experimental-setup.tex`

**Paper text:**

```tex
Let $A$ be the paired anchor set used for fitting and $S$ the set selected for
document replacement. The unique destination-document budget is
\begin{equation}
 b=|A\cup S|,\qquad b=\lfloor\rho N\rfloor .
 \label{eq:budget}
\end{equation}
Anchors consume this budget. Our selection starts with $A$ and fills the
remaining slots from a fixed random document order, skipping duplicates, so
$A\subseteq S$ and $|S|=b$. Larger budgets extend the same order and retain the
same fitted anchors. The principal setting uses $m=|A|=1{,}024$ pairs; an
all-paid-pairs comparison separately fits on every paid pair. Fit uses paired
document vectors without queries or relevance labels. This separates the
amount of fitting supervision from the number of true vectors in the gallery.
The same map serves several replacement budgets; after full replacement,
scores depend entirely on the destination encoder.
```

**Checked statement:** Paid sets contain all anchors and are nested, with exactly floor(rho N) unique target document vectors; the accounting is |A union S|, including anchors

**Paper value:** `{"implementation": "select_for_budget seeds selected with anchor set, skips duplicates, uses floor(fraction*n_docs); build_mixed_gallery verifies anchor inclusion", "primary_anchor_count": 1024, "allpaid_count": 28819}`

**Evidence:** `D:/DASFAA-2027-paper/src/arc2_global/numerics.py`

**Evidence value:**

```json
{
  "implementation": "select_for_budget seeds selected with anchor set, skips duplicates, uses floor(fraction*n_docs); build_mixed_gallery verifies anchor inclusion",
  "primary_anchor_count": 1024,
  "allpaid_count": 28819
}
```

1024 and 28819 fit-pair counts also appear in all-paid cell_index metadata; 28819=floor(.5*57638).

### Claim 91: exact_match
**Location:** `sections/method.tex`

**Paper text:**

```tex
One global ridge regression shares these correction targets across anchors.
Stacking their rows into $T^{(t)}$, we solve
\begin{align}
 \Delta_t&=\mathop{\arg\min}_{\Delta\in\mathbb{R}^{p\times d_t}}
 \|\widetilde{X}\Delta-T^{(t)}\|_F^2+\lambda\|\Delta\|_F^2,
 \label{eq:ridge-objective}\\
 &=\widetilde{X}^{\top}
 (\widetilde{X}\widetilde{X}^{\top}+\lambda I_m)^{-1}T^{(t)},
 \qquad B_{t+1}=B_t+\Delta_t .
 \label{eq:tangent-update}
\end{align}
The penalty regularizes the correction, including its intercept. Equivalently,
changing variables to the updated coefficient matrix yields
\begin{equation}
 B_{t+1}=\mathop{\arg\min}_C
 \|\widetilde X C-(\widetilde X B_t+T^{(t)})\|_F^2
 +\lambda\|C-B_t\|_F^2.
 \label{eq:current-prior}
\end{equation}
Unlike zero-centered ridge onto $Y_A$, this penalty retains the current map
while fitting norm-scaled cosine descent targets. We fix $\lambda=10$ and perform
exactly two updates, recomputing targets after the first; the development
ablation in Sect.~\ref{sec:results} measures the second update's contribution.
A Cholesky
factorization is reused across updates. The refined map is unconstrained;
fitting requires paired document vectors and linear solves, with no neural
mapper training.
```

**Checked statement:** We fix lambda=10 and perform exactly two updates, recomputing targets after the first

**Paper value:** `{"lambda": 10, "steps": 2, "source_target": "norms * (y - sum(unit*y) * unit)", "ridge_intercept": "penalized with identical diagonal"}`

**Evidence:** `D:/DASFAA-2027-paper/src/arc2_global/model.py`

**Evidence value:**

```json
{
  "lambda": 10,
  "steps": 2,
  "source_target": "norms * (y - sum(unit*y) * unit)",
  "ridge_intercept": "penalized with identical diagonal"
}
```



### Claim 92: exact_match
**Location:** `sections/method.tex / setup`

**Paper text:**

```tex
\paragraph{Matched supervision and exposure.}
The main matrix crosses four development collections, two migrations,
three paid-document budgets (25/50/75\%), six methods, and seeds
17, 29, 41, 53, and 67. All methods fit the same ordered 1,024 paired anchors
and replace the same paid document rows. Paid sets contain all anchors and
are nested, with exactly $\lfloor \rho N\rfloor$ unique target document vectors;
the accounting is $|A\cup S|$, including anchors. On the Nano collections and
TREC-COVID, independent seeded streams sample anchors without replacement
and a document permutation; unseen permutation rows fill the budget. FiQA
retains its historical anchor/order arrays. Neither fitting nor selection uses
relevance labels. Paid nonanchor vectors provide replacement only in this
fixed-anchor regime. A separate FiQA experiment holds the 50\% paid set
fixed and compares fitting on 1,024 versus all 28,819 paid pairs.
Development fixed-anchor ARC2 rankings use the float64 dual backend;
all-paid and TREC-COVID fits use the float64 primal backend in
Sect.~\ref{sec:method-cost}. The all-paid study reuses the dual fixed-anchor
comparisons. Both backends implement the same two-update rule.
```

**Checked statement:** Development fixed-anchor ARC2 rankings use the float64 dual backend; all-paid and TREC-COVID fits use the float64 primal backend

**Paper value:** `{"dual": "X.T @ cho_solve(XX.T+10I, target)", "primal": "cho_solve(X.T X+10I, X.T @ target)", "coefficient_storage": "float32", "updates": "float64"}`

**Evidence:** `D:/DASFAA-2027-paper/src/arc2_global/solver_backend.py`

**Evidence value:**

```json
{
  "dual": "X.T @ cho_solve(XX.T+10I, target)",
  "primal": "cho_solve(X.T X+10I, X.T @ target)",
  "coefficient_storage": "float32",
  "updates": "float64"
}
```

Both source kernels use the same B0 expansion, target and two updates. Backend usage is also declared by the raw study configs; this is not a fresh ranking parity test.

### Claim 93: exact_match
**Location:** `sections/experimental-setup.tex: matched-target controls`

**Paper text:**

```tex
\paragraph{Matched-target controls.}
An additional FiQA/MiniLM study at 50\% coverage holds $B_0$, the ordered
1,024 anchors, $\lambda=10$, the current-map penalty and two updates fixed.
It replaces the tangent target by either norm-scaled chordal error
$r(y-u)$ or Euclidean error $y-z$, recomputed at each control's own state.
All four arms, including unrefined $B_0$, run in the same Windows environment
(NumPy 2.5.3, SciPy 1.18.1), using float64 dual fitting and the same float32
exact search. This is a separate development measurement.
```

**Checked statement:** holds B0, the ordered 1,024 anchors, lambda=10, the current-map penalty and two updates fixed; norm-scaled chordal error r(y-u) or Euclidean error y-z, recomputed at each control's own state

**Paper value:** `{"anchor_count": 1024, "lambda": 10, "steps": 2, "runtime": {"python": "3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]", "numpy": "2.5.3", "scipy": "1.18.1", "platform": "Windows"}, "target_formulas": ["r*(y-c*u)", "r*(y-u)", "y-z"], "state": "coef reset to same base per method and recomputed each step"}`

**Evidence:** `D:/DASFAA-2027-paper/src/arc2_global/residual_ablation.py`

**Evidence value:**

```json
{
  "anchor_count": 1024,
  "lambda": 10,
  "steps": 2,
  "runtime": {
    "python": "3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]",
    "numpy": "2.5.3",
    "scipy": "1.18.1",
    "platform": "Windows"
  },
  "target_formulas": [
    "r*(y-c*u)",
    "r*(y-u)",
    "y-z"
  ],
  "state": "coef reset to same base per method and recomputed each step"
}
```



### Claim 94: exact_match
**Location:** `sections/experimental-setup.tex: matched-target scope`

**Paper text:**

```tex
Each locked analysis uses 20,000 paired query-bootstrap draws after
averaging the five mapping seeds. Development macro effects weight the
24 collection/migration/budget conditions equally and resample queries
within each collection. Within each analysis, the same sampled query indices
are shared across methods, budgets and migrations for that collection.
Saved 99\% percentile intervals give approximate
95\% coverage for the five-comparison family; the ablations have a separate
five-contrast family. The all-paid experiment uses its predeclared
32-contrast family. TREC-COVID has 30 primary contrasts
(five baselines, two migrations, three budgets), with approximately
99.8333\% individual percentile intervals for approximate 95\% family
coverage. Its independent units are the 50 queries. Recall intervals are
nominal 95\% descriptive intervals. An interval touching zero is unresolved.
The matched-target study retains its original four-contrast family, with
98.75\% individual intervals; two MiniLM contrasts are observed and the two
planned E5 contrasts remain pending.
These intervals condition on the five observed mapping seeds and fixed
collections and encoder pairs; development intervals do not adjust for
method selection.\footnote{The accompanying anonymous artifact provides
mapper code, baseline settings, frozen per-query results, raw ranking evidence
and scripts to verify the reported numerical results.}
```

**Checked statement:** two MiniLM contrasts are observed and the two planned E5 contrasts remain pending

**Paper value:** `{"draws": 20000, "seed": 20261102, "unit": "query after five-seed averaging", "family_size": 4, "observed_contrasts": 2, "pending_E5_contrasts": 2, "individual_coverage": 0.9875, "approx_original_family_coverage": 0.95, "quantile_method": "linear", "query_indices_sha256_le_int64": "d18a5bb239f4672c36b37c15105218b8c4694b75e21f3e5f349849bcfef9a132"}`

**Evidence:** `D:/DASFAA-2027-paper/configs/tc1l_minilm_local_20261102_lock.json`

**Evidence value:**

```json
{
  "draws": 20000,
  "seed": 20261102,
  "unit": "query after five-seed averaging",
  "family_size": 4,
  "observed_contrasts": 2,
  "pending_E5_contrasts": 2,
  "individual_coverage": 0.9875,
  "approx_original_family_coverage": 0.95,
  "quantile_method": "linear",
  "query_indices_sha256_le_int64": "d18a5bb239f4672c36b37c15105218b8c4694b75e21f3e5f349849bcfef9a132"
}
```

MiniLM-only FiQA development; original two-pair campaign is explicitly incomplete. 98.75% individual coverage gives approximate 95% family coverage over four planned contrasts.

### Claim 95: exact_match
**Location:** `sections/experimental-setup.tex: neural baselines`

**Paper text:**

```tex
\paragraph{Comparison methods.}
We retain the full five-baseline panel: centered rectangular Procrustes
(an A2M adaptation); LA2M with 20 source-anchor clusters, local alignment
for clusters with at least two anchors and global fallback for singletons;
SimpleLinear; affine ridge with $\lambda=10$
and a regularized bias; and Embedding-Converter~\cite{la2m,simplelinear,embeddingconverter}.
SimpleLinear uses pinned official code: despite its name, the locked
configuration is a five-layer SELU MLP, trained for the final 50 epochs with
batch size 4,028 and the MSE plus cosine loss, without qrel-based stopping.
Converter is a paper-specification adaptation with a 50,000-update
selection run, batch size 64, and local neighborhood size 100. Paired-vector
validation MAE selects the earliest minimum at 250-update checkpoints;
a fresh fit uses all fitting pairs for that selected length. Unlike the
original retrieval-based validation, this adaptation uses paired-vector MAE
to respect paired-document-only supervision. These are the
declared implementations and training policies, rather than claims to
reproduce every original-paper setting. \method{} remains fixed at two
tangent updates and $\lambda=10$ throughout.
```

**Checked statement:** Converter is a paper-specification adaptation with a 50,000-update selection run, batch size 64, and local neighborhood size 100; earliest minimum at 250-update checkpoints

**Paper value:** `{"hidden_multiplier": 5, "iterations": 50000, "batch_size": 64, "local_k": 100, "local_samples_per_center": 1, "alpha": 0.1, "beta": 0.1, "learning_rate": 0.001, "adam_betas": [0.9, 0.999], "adam_epsilon": 1e-08, "report_every": 250, "transform_batch_size": 256, "threads": 4, "device": "cuda"}`

**Evidence:** `D:/DASFAA-2027-paper/src/arc2_global/embedding_converter.py`

**Evidence value:**

```json
{
  "hidden_multiplier": 5,
  "iterations": 50000,
  "batch_size": 64,
  "local_k": 100,
  "local_samples_per_center": 1,
  "alpha": 0.1,
  "beta": 0.1,
  "learning_rate": 0.001,
  "adam_betas": [
    0.9,
    0.999
  ],
  "adam_epsilon": 1e-08,
  "report_every": 250,
  "transform_batch_size": 256,
  "threads": 4,
  "device": "cuda"
}
```

Source selects strictly smaller validation MAE and retains first equal minimum; paired-vector validation policy is described as an adaptation.

### Claim 96: exact_match
**Location:** `sections/experimental-setup.tex: SimpleLinear`

**Paper text:**

```tex
\paragraph{Comparison methods.}
We retain the full five-baseline panel: centered rectangular Procrustes
(an A2M adaptation); LA2M with 20 source-anchor clusters, local alignment
for clusters with at least two anchors and global fallback for singletons;
SimpleLinear; affine ridge with $\lambda=10$
and a regularized bias; and Embedding-Converter~\cite{la2m,simplelinear,embeddingconverter}.
SimpleLinear uses pinned official code: despite its name, the locked
configuration is a five-layer SELU MLP, trained for the final 50 epochs with
batch size 4,028 and the MSE plus cosine loss, without qrel-based stopping.
Converter is a paper-specification adaptation with a 50,000-update
selection run, batch size 64, and local neighborhood size 100. Paired-vector
validation MAE selects the earliest minimum at 250-update checkpoints;
a fresh fit uses all fitting pairs for that selected length. Unlike the
original retrieval-based validation, this adaptation uses paired-vector MAE
to respect paired-document-only supervision. These are the
declared implementations and training policies, rather than claims to
reproduce every original-paper setting. \method{} remains fixed at two
tangent updates and $\lambda=10$ throughout.
```

**Checked statement:** a five-layer SELU MLP, trained for the final 50 epochs with batch size 4,028 and the MSE plus cosine loss

**Paper value:** `{"learning_rate": 0.0001, "num_epochs": 50, "batch_size": 4028, "gradient_clip": 1.0, "weight_decay": 1e-05, "scheduler_patience": 5, "scheduler_factor": 0.5, "early_stopping_patience": 10, "min_delta": 1e-06, "device": null, "layer_num": 4, "activation": "selu", "dropout": 0.0, "hidden_dim": 512, "use_local_distill": false, "local_k": 50, "local_tau": 0.1, "local_weight": 0.5, "faiss_use_float32": true, "knn_recompute_epochs": 0, "global_weight": 0.5, "cosine_weight": 0.5, "mse_weight": 1.0, "normalize_output": false, "loss_kind": "mse_cos"}`

**Evidence:** `D:/DASFAA-2027-paper/configs/b1c_r3_lock.json`

**Evidence value:**

```json
{
  "learning_rate": 0.0001,
  "num_epochs": 50,
  "batch_size": 4028,
  "gradient_clip": 1.0,
  "weight_decay": 1e-05,
  "scheduler_patience": 5,
  "scheduler_factor": 0.5,
  "early_stopping_patience": 10,
  "min_delta": 1e-06,
  "device": null,
  "layer_num": 4,
  "activation": "selu",
  "dropout": 0.0,
  "hidden_dim": 512,
  "use_local_distill": false,
  "local_k": 50,
  "local_tau": 0.1,
  "local_weight": 0.5,
  "faiss_use_float32": true,
  "knn_recompute_epochs": 0,
  "global_weight": 0.5,
  "cosine_weight": 0.5,
  "mse_weight": 1.0,
  "normalize_output": false,
  "loss_kind": "mse_cos"
}
```

Locked layer_num=4 means four hidden transformations plus output; wrapper executes pinned official model, final50 policy identified in raw method name. No original-method reproduction claim is made.

### Claim 97: exact_match
**Location:** `sections/experimental-setup.tex: retrieval`

**Paper text:**

```tex
\paragraph{Retrieval and inference.}
Destination queries search a single gallery containing unit-normalized
proxies and paid true vectors, using exact float32 inner products and
top-100 retrieval. Score ties use original document row order; identical
query/document IDs are excluded. Native Full-X and Full-Y use their own
query/document encoders throughout and provide reference operating points.
Our primary metric is graded \ndcg{} with gain $2^{\mathrm{rel}}-1$; auxiliary
\recall{} measures coverage over all
positive judgments, including positives outside a Nano corpus. All queries
count; unjudged documents are nonrelevant. The prospective figure reports both
metrics; a companion Recall table is included in the manuscript-source package.
```

**Checked statement:** exact float32 inner products and top-100 retrieval. Score ties use original document row order; identical query/document IDs are excluded

**Paper value:** `{"dtype": "float32", "k": 100, "tie_rule": "stable argsort(-scores)", "id_exclusion": "explicit flag with ID map"}`

**Evidence:** `D:/DASFAA-2027-paper/src/arc2_global/retrieval.py`

**Evidence value:**

```json
{
  "dtype": "float32",
  "k": 100,
  "tie_rule": "stable argsort(-scores)",
  "id_exclusion": "explicit flag with ID map"
}
```

Raw per-query axes and result metric names agree. No ANN-quality claim is present.

### Claim 98: exact_match
**Location:** `sections/experimental-setup.tex: inference`

**Paper text:**

```tex
Each locked analysis uses 20,000 paired query-bootstrap draws after
averaging the five mapping seeds. Development macro effects weight the
24 collection/migration/budget conditions equally and resample queries
within each collection. Within each analysis, the same sampled query indices
are shared across methods, budgets and migrations for that collection.
Saved 99\% percentile intervals give approximate
95\% coverage for the five-comparison family; the ablations have a separate
five-contrast family. The all-paid experiment uses its predeclared
32-contrast family. TREC-COVID has 30 primary contrasts
(five baselines, two migrations, three budgets), with approximately
99.8333\% individual percentile intervals for approximate 95\% family
coverage. Its independent units are the 50 queries. Recall intervals are
nominal 95\% descriptive intervals. An interval touching zero is unresolved.
The matched-target study retains its original four-contrast family, with
98.75\% individual intervals; two MiniLM contrasts are observed and the two
planned E5 contrasts remain pending.
These intervals condition on the five observed mapping seeds and fixed
collections and encoder pairs; development intervals do not adjust for
method selection.\footnote{The accompanying anonymous artifact provides
mapper code, baseline settings, frozen per-query results, raw ranking evidence
and scripts to verify the reported numerical results.}
```

**Checked statement:** 20,000 paired query-bootstrap draws after averaging the five mapping seeds; approximate 95% family coverage

**Paper value:** `{"main": {"draws": 20000, "seed": 20261028, "rng": "numpy default_rng/PCG64; datasets in DATASETS order", "datasets": {"NanoNQ": {"indices_shape": [20000, 50], "indices_dtype": "int32", "indices_sha256_c_order": "df0c87af8cde8ddd160cbe91a8f8ef8bcf1257195a6a12911b659656ca7d7d03"}, "NanoHotpotQA": {"indices_shape": [20000, 50], "indices_dtype": "int32", "indices_sha256_c_order": "9fa43e9e11e93169f9474bb9a4b7ec619c6e81ec4f0006b9a9c6f021bcdbf475"}, "NanoFEVER": {"indices_shape": [20000, 50], "indices_dtype": "int32", "indices_sha256_c_order": "639078103208562d9a1e016fe104b5af16619575fe9a5bfefa01b237b1d315a0"}, "FiQA": {"indices_shape": [20000, 500], "indices_dtype": "int32", "indices_sha256_c_order": "af4fedfe906d8f77983b814f1770b53d49b840a363b62d4b409c32a6685b88cd"}}, "resampling": "independent query resampling within each dataset; identical indices across pairs/budgets/methods/metrics; average five mapping seeds before resampling", "macro_weighting": "equal 24 dataset/pair/budget strata", "familywise": {"metric": "ndcg10", "scope": "overall_equal_24_strata", "contrasts": 5, "family_confidence": 0.95, "per_interval_confidence": 0.99, "method": "bonferroni_percentile"}, "condition_intervals": "nominal95 descriptive; not a 120-contrast tested family", "recall_intervals": "nominal95 descriptive", "coverage": "approximate percentile bootstrap"}, "ablation_family": {"scope": "overall_equal_24_strata", "contrasts": 5, "family_confidence": 0.95, "per_interval_confidence": 0.99, "method": "bonferroni_percentile"}, "paid": {"draws": 20000, "seed": 20261026, "rng": "numpy default_rng(20261026), PCG64", "indices_shape": [20000, 500], "indices_dtype": "int32", "indices_sha256_c_order": "06f1b7712fe8eb020eb247239ec6bca26b0a124ef9e9b6ede1e957a065fb25c8", "resampling": "500 queries with replacement; five seeds averaged first; shared indices", "familywise": {"metric": "ndcg10", "contrasts": 32, "family_confidence": 0.95, "per_interval_confidence": 0.9984375, "method": "bonferroni_percentile"}, "coverage": "approximate percentile bootstrap"}, "trec": {"draws": 20000, "seed": 20261031, "rng": "numpy default_rng/PCG64", "query_indices_sha256": "18cc3ac6ca3c1682d83323766ad47e13572e1dd78dd618d0df797b9b7627a16a", "axes": ["bootstrap_draw", "definition_then_metric"], "metrics": ["ndcg10", "recall100"], "resampling": "one identical query resample across all pairs/budgets/methods/metrics; average five mapping seeds first", "family_contrasts": 30, "family_alpha": 0.05, "per_interval_confidence": 0.9983333333333333, "recall_intervals": "nominal95 descriptive", "coverage": "approximate percentile bootstrap"}, "target_controls": {"draws": 20000, "seed": 20261102, "unit": "query after five-seed averaging", "family_size": 4, "observed_contrasts": 2, "pending_E5_contrasts": 2, "individual_coverage": 0.9875, "approx_original_family_coverage": 0.95, "quantile_method": "linear", "query_indices_sha256_le_int64": "d18a5bb239f4672c36b37c15105218b8c4694b75e21f3e5f349849bcfef9a132"}}`

**Evidence:** `D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json`

**Evidence value:**

```json
{
  "main": {
    "draws": 20000,
    "seed": 20261028,
    "rng": "numpy default_rng/PCG64; datasets in DATASETS order",
    "datasets": {
      "NanoNQ": {
        "indices_shape": [
          20000,
          50
        ],
        "indices_dtype": "int32",
        "indices_sha256_c_order": "df0c87af8cde8ddd160cbe91a8f8ef8bcf1257195a6a12911b659656ca7d7d03"
      },
      "NanoHotpotQA": {
        "indices_shape": [
          20000,
          50
        ],
        "indices_dtype": "int32",
        "indices_sha256_c_order": "9fa43e9e11e93169f9474bb9a4b7ec619c6e81ec4f0006b9a9c6f021bcdbf475"
      },
      "NanoFEVER": {
        "indices_shape": [
          20000,
          50
        ],
        "indices_dtype": "int32",
        "indices_sha256_c_order": "639078103208562d9a1e016fe104b5af16619575fe9a5bfefa01b237b1d315a0"
      },
      "FiQA": {
        "indices_shape": [
          20000,
          500
        ],
        "indices_dtype": "int32",
        "indices_sha256_c_order": "af4fedfe906d8f77983b814f1770b53d49b840a363b62d4b409c32a6685b88cd"
      }
    },
    "resampling": "independent query resampling within each dataset; identical indices across pairs/budgets/methods/metrics; average five mapping seeds before resampling",
    "macro_weighting": "equal 24 dataset/pair/budget strata",
    "familywise": {
      "metric": "ndcg10",
      "scope": "overall_equal_24_strata",
      "contrasts": 5,
      "family_confidence": 0.95,
      "per_interval_confidence": 0.99,
      "method": "bonferroni_percentile"
    },
    "condition_intervals": "nominal95 descriptive; not a 120-contrast tested family",
    "recall_intervals": "nominal95 descriptive",
    "coverage": "approximate percentile bootstrap"
  },
  "ablation_family": {
    "scope": "overall_equal_24_strata",
    "contrasts": 5,
    "family_confidence": 0.95,
    "per_interval_confidence": 0.99,
    "method": "bonferroni_percentile"
  },
  "paid": {
    "draws": 20000,
    "seed": 20261026,
    "rng": "numpy default_rng(20261026), PCG64",
    "indices_shape": [
      20000,
      500
    ],
    "indices_dtype": "int32",
    "indices_sha256_c_order": "06f1b7712fe8eb020eb247239ec6bca26b0a124ef9e9b6ede1e957a065fb25c8",
    "resampling": "500 queries with replacement; five seeds averaged first; shared indices",
    "familywise": {
      "metric": "ndcg10",
      "contrasts": 32,
      "family_confidence": 0.95,
      "per_interval_confidence": 0.9984375,
      "method": "bonferroni_percentile"
    },
    "coverage": "approximate percentile bootstrap"
  },
  "trec": {
    "draws": 20000,
    "seed": 20261031,
    "rng": "numpy default_rng/PCG64",
    "query_indices_sha256": "18cc3ac6ca3c1682d83323766ad47e13572e1dd78dd618d0df797b9b7627a16a",
    "axes": [
      "bootstrap_draw",
      "definition_then_metric"
    ],
    "metrics": [
      "ndcg10",
      "recall100"
    ],
    "resampling": "one identical query resample across all pairs/budgets/methods/metrics; average five mapping seeds first",
    "family_contrasts": 30,
    "family_alpha": 0.05,
    "per_interval_confidence": 0.9983333333333333,
    "recall_intervals": "nominal95 descriptive",
    "coverage": "approximate percentile bootstrap"
  },
  "target_controls": {
    "draws": 20000,
    "seed": 20261102,
    "unit": "query after five-seed averaging",
    "family_size": 4,
    "observed_contrasts": 2,
    "pending_E5_contrasts": 2,
    "individual_coverage": 0.9875,
    "approx_original_family_coverage": 0.95,
    "quantile_method": "linear",
    "query_indices_sha256_le_int64": "d18a5bb239f4672c36b37c15105218b8c4694b75e21f3e5f349849bcfef9a132"
  }
}
```

Family sizes 5/5/32/30/4 remain separate; saved TREC and TC bootstrap quantiles reproduce every checked family endpoint exactly. No seed population or selection-adjusted inference is claimed.

### Claim 99: exact_match
**Location:** `sections/results.tex / captions: scope`

**Paper text:**

```tex
Geometric alignment remains competitive: before rounding, Procrustes has
higher nDCG point means in all six cells, although its MiniLM/75\% difference
is below $0.0001$. All Procrustes and LA2M nDCG family intervals cross zero.
The confirmed advantages therefore concern the evaluated Converter, ridge
and SimpleLinear configurations.
```

**Checked statement:** The confirmed advantages therefore concern the evaluated Converter, ridge and SimpleLinear configurations

**Paper value:** `{"procrustes_unresolved": 6, "la2m_unresolved": 6, "supported_converter": 5, "supported_ridge": 4, "supported_simplelinear": 2}`

**Evidence:** `D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json`

**Evidence value:**

```json
{
  "procrustes_unresolved": 6,
  "la2m_unresolved": 6,
  "supported_converter": 5,
  "supported_ridge": 4,
  "supported_simplelinear": 2
}
```

Development collection status, prospective TREC scope, descriptive cross-budget comparison, nominal Recall, and non-equivalence to Full-Y are explicitly stated.

### Claim 100: exact_match
**Location:** `sections/related-work.tex / references.bib`

**Paper text:**

```tex
\paragraph{Geometric alignment and refinement.}
Orthogonal Procrustes provides the classical least-squares alignment underlying our initialization~\cite{schonemann1966procrustes}.
Recent work connects approximate preservation of pairwise inner products to bounds on Procrustes alignment error and demonstrates interoperability across retrieval models~\cite{maystre2025procrustes}.
Unpaired translation pursues a different supervision regime: vec2vec learns translation through a shared latent representation without known correspondences~\cite{jha2025geometry}, while mini-vec2vec combines pseudo-pair construction, Procrustes estimation, and iterative matching and clustering refinements~\cite{dar2025mini}.
GCPA also corrects directional mismatch after Procrustes alignment~\cite{gcpa2026}.
It constructs a shared multi-model universe and trains a residual MLP toward consensus directions with an angular trust penalty.
ARC2 instead targets paired destination documents and regularizes two affine ridge corrections around the current coefficient matrix (Eq.~\ref{eq:current-prior}).
The distinction lies in the destination target, coefficient-space prior and finite affine computation; directional post-alignment correction itself is established.
```

**Checked statement:** GCPA also corrects directional mismatch after Procrustes alignment. It constructs a shared multi-model universe and trains a residual MLP toward consensus directions with an angular trust penalty.

**Paper value:** `{"source_url": "https://proceedings.mlr.press/v306/achara26a.html", "official_pdf": "https://raw.githubusercontent.com/mlresearch/v306/main/assets/achara26a/achara26a.pdf", "source_sections": ["3.4 Eq.5 consensus", "3.4 Eq.8 residual MLP/angular trust", "Appendix C.1 trust threshold"], "bibliography": "PMLR 306:310-331, ICML 2026, Achara et al."}`

**Evidence:** `D:/DASFAA-2027-paper/.aris/traces/paper-claim-audit/2026-11-02_tc1l_gcpa/achara26a.pdf`

**Evidence value:**

```json
{
  "source_url": "https://proceedings.mlr.press/v306/achara26a.html",
  "official_pdf": "https://raw.githubusercontent.com/mlresearch/v306/main/assets/achara26a/achara26a.pdf",
  "source_sections": [
    "3.4 Eq.5 consensus",
    "3.4 Eq.8 residual MLP/angular trust",
    "Appendix C.1 trust threshold"
  ],
  "bibliography": "PMLR 306:310-331, ICML 2026, Achara et al."
}
```

Official PMLR page and official PDF support the wording. ARC2 distinction is destination-document target plus coefficient-space current-map prior and finite affine solve; directional post-alignment correction is explicitly acknowledged as established.

### Claim 101: exact_match
**Location:** `sections/results.tex / figure captions`

**Paper text:**

```tex
\subsection{Directional Targets Add Value without an Inference Stage}
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{dev_ablation.pdf}
  \caption{Development mechanism controls. (a) Equal-condition macro effects,
  with saved 99\% intervals for five contrasts. (b) FiQA/MiniLM at 50\%
  coverage: matched-initialization target controls, with 98.75\% intervals
  retaining the original four-contrast family. Panels use separate scales;
  all intervals are shown in full.}
  \label{fig:ablation}
\end{figure}
```

**Checked statement:** All six adapters and native references are shown; explicitly panel-specific vertical ranges; all intervals are shown in full

**Paper value:** `{"figures": ["dev_quality.pdf", "dev_ablation.pdf", "trec_quality.pdf"], "visual_review": "All four PDF figure renders inspected; development points and held-collection point order match raw means; separate scales labeled; new target-control intervals fully visible."}`

**Evidence:** `D:/DASFAA-2027-paper/paper/figures/dev_ablation.pdf`

**Evidence value:**

```json
{
  "figures": [
    "dev_quality.pdf",
    "dev_ablation.pdf",
    "trec_quality.pdf"
  ],
  "visual_review": "All four PDF figure renders inspected; development points and held-collection point order match raw means; separate scales labeled; new target-control intervals fully visible."
}
```



### Claim 102: exact_match
**Location:** `sections/introduction.tex: mechanism caption`

**Paper text:**

```tex
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{mechanism.pdf}
\caption{A worked \method\ migration. Paired document vectors train centered Procrustes and two tangent corrections, yielding one affine adapter. Unencoded documents remain searchable through proxies; backfill replaces them with native vectors in the same gallery. The 24-document corpus, eight anchors, four additional encodings and displayed hits are illustrative, not measured retrieval results.}
\label{fig:mechanism}
\end{figure}
```

**Checked statement:** The 24-document corpus, eight anchors, four additional encodings and displayed hits are illustrative, not measured retrieval results.

**Paper value:** `{"corpus": 24, "anchors": 8, "additional": 4, "paid": 12, "hits": "illustrative", "equations": "consistent with method and code"}`

**Evidence:** `D:/DASFAA-2027-paper/paper/figures/mechanism.pdf`

**Evidence value:**

```json
{
  "corpus": 24,
  "anchors": 8,
  "additional": 4,
  "paid": 12,
  "hits": "illustrative",
  "equations": "consistent with method and code"
}
```

Diagram visual arithmetic is 8+4=12 and paid coverage 12/24. No empirical claim inferred from the diagram.

### Claim 103: exact_match
**Location:** `sections/experimental-setup.tex: artifact footnote`

**Paper text:**

```tex
The accompanying anonymous artifact provides
mapper code, baseline settings, frozen per-query results, raw ranking evidence
and scripts to verify the reported numerical results.
```

**Paper value:** `{"mapper_code": true, "baseline_settings": true, "frozen_per_query": true, "ranking_evidence": true, "verification_script": true}`

**Evidence:** `D:/ARC2-Global_Anonymous_Artifact_20261102/MANIFEST.json`

**Evidence value:**

```json
{
  "mapper_code": true,
  "baseline_settings": true,
  "frozen_per_query": true,
  "ranking_evidence": true,
  "verification_script": true
}
```

Inspected the actual artifact manifest, file availability and offline verifier source. Did not rely on an executor QA report or re-run scoring. Parent supplied the artifact path as operational context.

## Declared input hashes

Hash scope is exactly the declared manuscript/evidence/config/code inputs read in this invocation, plus the inspected compiled PDF and cached official GCPA PDF. In-paper keys are relative to `paper/`; external keys are absolute. No prior audit artifact is an input.

```json
{
  "D:/ARC2-Global_Anonymous_Artifact_20261102/MANIFEST.json": "sha256:61c3fbe28014c8b02988d35eddd14ef5184e80431fb8301527cb06e77d25aa77",
  "D:/ARC2-Global_Anonymous_Artifact_20261102/verify.py": "sha256:ade631367396c920c4f8400cbc0f7fd85544fed8cd958d1d4410f22f39939538",
  "D:/DASFAA-2027-paper/.aris/traces/paper-claim-audit/2026-11-02_tc1l_gcpa/achara26a.pdf": "sha256:75a0e06fec9bb08754dd75cb33148a60cc91d5176f918383a8609e369f826012",
  "D:/DASFAA-2027-paper/configs/b1c_r3_lock.json": "sha256:f567a4b6267baef3c59de1aca750d19ba3479d228109f7d098fd45d26586830d",
  "D:/DASFAA-2027-paper/configs/b1p_lock.json": "sha256:0224200454b0deb8f2176e509d8bd99da0f59c7ae7b12a2488ec6eadad7308ad",
  "D:/DASFAA-2027-paper/configs/b2_lock.json": "sha256:e00c970a4061ce6d50f2af9817621243959a9372e6c12a0d4e9c9c9c9d2a93f5",
  "D:/DASFAA-2027-paper/configs/datasets.json": "sha256:c26318609b4959f2c07110c3e610de8f77befcad2c35d8de836d7821eb8a9b82",
  "D:/DASFAA-2027-paper/configs/tc1l_minilm_local_20261102_lock.json": "sha256:82c54141f70c451ab7d90833a8c78f9e14d765aa7e19ca4cbccded50b6a2dbd6",
  "ARC2_Global_DASFAA2027_supervisor_20261102.pdf": "sha256:a6bff1fdc33169679dc45abce0c6d516ecbd96dbc63cd50770304089ecde4451",
  "figures/dev_ablation.pdf": "sha256:aed7707354ac9369006cf82e8a5f647629a0b6dc024a7f10a13ad7a7f2dbf947",
  "figures/dev_quality.pdf": "sha256:41dfa46bcb687071d9ee18ed0f1b604af2ee9e610511474882b2e152df7f7cb0",
  "figures/mechanism.pdf": "sha256:7a311bc8dd166bce96db914c5f94ad55a53fef32fc83953b2ba33ae6c2a49360",
  "figures/trec_quality.pdf": "sha256:d9af72af39fd4ae598cd6b85faf913ef61bf868002129fe370d37c9638d966c2",
  "generated/ablation.tex": "sha256:024435422d3cd2e5c977fa680365e1a7983e763ad813c91a4d65eb4db847571e",
  "generated/allpaid.tex": "sha256:bd28688f51a306c9990c0174f1c3b88786eb266a5e76bafffc0217c851de4c13",
  "generated/budget_leverage.tex": "sha256:dc8d45d6b72643735ae2135c8f970687b0eca5a9d8849de46988976a77e6719b",
  "generated/dev_macro.tex": "sha256:58e7543a91a5bbfcce75969e6277967cc1978ec1fc6e96d5461c60d821b3ff27",
  "generated/trec_family.tex": "sha256:b249a6c58e87792b9bed0dee93e631e66d65c7f0381fb38d3c03f0a19ed4fc9e",
  "generated/trec_means.tex": "sha256:354d8f8e46373015b3af96c5e66c3923777a5e88baef2f95be84728f99555dce",
  "generated/trec_recall.tex": "sha256:92fbea88b6557670feb56192669e114184b0b77a0b20baa083bc74fbc7b5fbdd",
  "main.tex": "sha256:704d831a3f56001486627c701512c0a03b7dcaba6ee1c5939418898f25cbd747",
  "references.bib": "sha256:03f83b8433278cfc7c42331894bbed39adebd15b639140cd44c5238c5ec7a893",
  "sections/abstract.tex": "sha256:9e067024e515895185e0c588d083bc454d372d4af10032011622795330570597",
  "sections/conclusion.tex": "sha256:e99185b6264336089099ad7201552d3d83ebb3f9d8cb75e236453a38b5970193",
  "sections/discussion.tex": "sha256:4529307286eeca7d4b30adb3d20368f320ee291262059779993bb403d4ab3c71",
  "sections/experimental-setup.tex": "sha256:02b50e48781e445d8d331c0b58c4113d421b73fb2b3a6cc7f20a73c7c33f5cf6",
  "sections/introduction.tex": "sha256:65315cd9c709b70451ce9fb4c66e69938917245d007c5782b247fcd60c469523",
  "sections/method.tex": "sha256:d0104ddb693c16483dfef65bac68bf5224a61cb5828798556e76856996951da5",
  "sections/related-work.tex": "sha256:de6a7e97f0ef75ec5cf8b3e38bd93294c1dd676d1bc26f5c0ac493e7058a4212",
  "sections/results.tex": "sha256:747336a8f1064156b1268bbb09f95a640bb0fcea67d5e322ab84eeef5d90511f",
  "D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/cell_index.json": "sha256:c4d23f1730dbd10b3975590faf77ab0210869d19306c6adfe64785e3e7e515aa",
  "D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/per_query_FiQA.npy": "sha256:3008af5125a8ab4d941aa1b8597507c9e30caa17dad2ab5c4f2c8eff3a15c9da",
  "D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/per_query_NanoFEVER.npy": "sha256:4dcb99a9ce16125b857721ec035f9a5d0ddbc78099ff1023d95bacfc11efac5d",
  "D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/per_query_NanoHotpotQA.npy": "sha256:46966df3fffc74b63b935082b77db720cbcbc5b97bd0a656d3b9d732c508c7ee",
  "D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/per_query_NanoNQ.npy": "sha256:59ff7a5599c53252d22680101e3804cef6effd189d8b73c158eb051add09d180",
  "D:/DASFAA-2027-paper/results/b1c_r3_review_20261031/evidence/run/scoring/summary.json": "sha256:501f065498d7325d402fcf2eef616b1d4b602ecf91d042d9ac03f780f597fec5",
  "D:/DASFAA-2027-paper/results/b1g_r1_review_20261027/scoring/results_summary.json": "sha256:2b5dbab47bb470bb546ef79a3c591144c9093d0090c7cc7b2eace416353df70f",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/FiQA/cell_index.json": "sha256:ff35ab9114296da0b9ce2349edaf915180b84413589042113133292f5cb12601",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/FiQA/per_query.npy": "sha256:4647bc64355eb1de7a5e94045993895078d350d9485a4fdba24c7205b8297a5c",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/NanoFEVER/cell_index.json": "sha256:31dea095fa0af0ea391de807d3a3ce7bc5a27b5e0d86e46bfa304b175428028a",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/NanoFEVER/per_query.npy": "sha256:9dc985097699befc5073e172d3609c73951086445138e065fa981645951b54eb",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/NanoHotpotQA/cell_index.json": "sha256:b0b710c3fc0074aabab239721db266dafbd5a51115e87fb0fd4827df186e4811",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/NanoHotpotQA/per_query.npy": "sha256:d0e714342e6b3d08564ab3d988bc73f8a529db5b610a32b8d55a8bb12cb56799",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/NanoNQ/cell_index.json": "sha256:06c4fa7251355dc4d4c955b974e21c1013e30dab7814203f1db787bae4d9ceb3",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/NanoNQ/per_query.npy": "sha256:a53be45fba376c9ed072bbf326bdb6450599d7ed9605e87b50ed0decd9ca96e2",
  "D:/DASFAA-2027-paper/results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json": "sha256:688d8b07a91b952f7ef96e859c5daa08cae4122c8ee69ae8dccf64dbe351eded",
  "D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/cell_index.json": "sha256:9163fb3cdf52fffbfa9f11e2ee4685cd56a1785b6f67da91ab4b31c2e8381375",
  "D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/per_query.npy": "sha256:551dc388059b6a530df550acbbd9a477de76cd0cc188ce54da0a1198be1434d1",
  "D:/DASFAA-2027-paper/results/b1p_r5_review_20261027/scoring/results_summary.json": "sha256:3ba283b580f6a7b2704a4c6746243987a9056c852e8e7f71ef78399984418fe7",
  "D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/bootstrap_draws.npy": "sha256:6517eb44b5c1967d7f3c54f72329f60f707892c85a395cf56210f6e58715ddba",
  "D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/cell_index.json": "sha256:d814ca87e947638e826d8f46bacab4f0f3526150ada9552c5ca59ca4b1776410",
  "D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/per_query.npy": "sha256:ffae3f16c279f3968c430537694df82ea0e8ec7aaed58576125522c9fb1d24be",
  "D:/DASFAA-2027-paper/results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json": "sha256:646b1f535db1138dc51a2d8d1296b97de89ba8354ead9f88e45080c9cb5f18c7",
  "D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/bootstrap_draws.npy": "sha256:86f445b094eb05d67bca7fe74503bd6019baf7b4c8d89d752fb0a8ebc46b0fa6",
  "D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/cell_index.json": "sha256:6888c2a279f3383b2704c4a3780d8a03d875bb8bd7ffe60b54a3ff5bcbbc6703",
  "D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/per_query.npy": "sha256:c32465773a25930e3c99328f4d2022940b889ac9bc835033b78c8f49f6dfa51a",
  "D:/DASFAA-2027-paper/results/tc1l_local_r1_20261102/full/scoring/summary.json": "sha256:79d3f10ea259a74e9543c4912b4f597266c87057e5e456216eee541d1bf0de41",
  "D:/DASFAA-2027-paper/src/arc2_global/__init__.py": "sha256:fcc953b59fcd88e686af0fb6555c78d8abdf31aae50e348905e80760b0a325cf",
  "D:/DASFAA-2027-paper/src/arc2_global/baseline_adapters.py": "sha256:c0269d631defb4ba00f09bf6def75182b988a9d4b8c719c81633c800e1189b0d",
  "D:/DASFAA-2027-paper/src/arc2_global/diagnostics.py": "sha256:0905e7c4cab1b0263b661f2d29677890080811e56218fbfcf0c81d2c14a18d9d",
  "D:/DASFAA-2027-paper/src/arc2_global/embedding_converter.py": "sha256:1df925b184f506db800945ae8e420c59aa34e8bf895ccfb33d0d972c7eae0508",
  "D:/DASFAA-2027-paper/src/arc2_global/mechanism_ablation.py": "sha256:c1e87fc33198b75976954f2388c486880b37a388ff8b3267e223b3f8b5c84d9b",
  "D:/DASFAA-2027-paper/src/arc2_global/model.py": "sha256:a678d522ce47be251af8d43fb21f94591e373aae6a8abcd290929f787b3aa6e2",
  "D:/DASFAA-2027-paper/src/arc2_global/numerics.py": "sha256:27b5d96941af54a2e5f202df447a34548d369d8bd6a1b4013af047803d85a5a5",
  "D:/DASFAA-2027-paper/src/arc2_global/procrustes.py": "sha256:2a6142a65498f0376e7fd8e4cc433b4a1a1bd072e8fa3379f5a11585cd299e64",
  "D:/DASFAA-2027-paper/src/arc2_global/residual_ablation.py": "sha256:e4fd831580c52420d661b0e9792a720a2fa134e49122dc168076d7d0135f90f2",
  "D:/DASFAA-2027-paper/src/arc2_global/retrieval.py": "sha256:d984d348cff6869ec6efa5c7eeb60402bce4b9df9c967e84c520f70d892ba3b1",
  "D:/DASFAA-2027-paper/src/arc2_global/solver_backend.py": "sha256:1b76bb8adf98ecc846505b7c89d983a0cf0740931d925e775a34f24a66da9887"
}
```

Full trace: `.aris/traces/paper-claim-audit/2026-11-02_tc1l_gcpa/`.
