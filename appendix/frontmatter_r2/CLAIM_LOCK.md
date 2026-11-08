# ARC2-Global: claim frozen for supervisor review

**R2 completeness audit:** [EXPERIMENT_ATLAS.md](EXPERIMENT_ATLAS.md) lists every completed block, the 1,340-cell union, supporting correctness tests, repaired historical omissions and unrun conditional systems work. Three added control figures expose the M/P/G evidence. Fresh semantic release audit was interrupted by quota; numerical/inventory evidence is provided for supervisor checking.


Revision: **supervisor-review-20261101-r2-completeness**. This freezes the interpretation of completed results before writing the paper. It changes neither the algorithm nor any scientific protocol, label exposure, ranking or scoring threshold.

> ARC2-Global is a compact forward document-space adapter that applies two closed-form tangent corrections to a centered Procrustes map. With 1,024 fitting pairs, it improves aggregate nDCG@10 across four inspected development collections. A prospective TREC-COVID test confirms gains in 11 of 30 declared comparisons against the specified ridge, SimpleLinear and Converter configurations, while its incremental nDCG advantage over Procrustes and LA2M remains unresolved.

## What is established

- **DEV quality:** all five declared macro nDCG comparisons favor ARC2 on NanoNQ, NanoHotpotQA, NanoFEVER and FiQA, under matched 1,024-anchor fitting. These collections were inspected during development.
- **Independent evidence:** the frozen TREC-COVID test contains 171,332 documents, 50 queries, two encoder pairs, five seeds and 25/50/75% paid-document budgets. All184 rankings were sealed and separately replayed before the first final-label opening. The 30 primary nDCG family intervals yield 11 positive,19 unresolved and0 negative decisions.
- **Mechanism:** the DEV second-step effect is +0.006924 nDCG, family interval [+0.003809,+0.009959]. It is an empirical ablation result, not a convergence or optimality theorem.
- **Representation structure:** the final 384-to768 affine map has 295,680 float32 coefficients, 1,182,720 bytes (~1.128MiB), excluding retained fit objects. ARC2 requires no neural training. Ridge is equally compact and Procrustes similarly compact.

## All independent comparisons remain visible

| Declared baseline configuration | Confirmed improvement | Unresolved | Confirmed worse |
|---|---:|---:|---:|
| A2M / centered Procrustes adaptation | 0/6 | 6/6 | 0/6 |
| LA2M20 integration-script adaptation | 0/6 | 6/6 | 0/6 |
| SimpleLinear official code, locked final50/5-layer policy | 2/6 | 4/6 | 0/6 |
| Affine ridge, lambda10 with regularized bias | 4/6 | 2/6 | 0/6 |
| Embedding-Converter paper-spec adaptation | 5/6 | 1/6 | 0/6 |

All six Procrustes point differences are negative. An interval crossing zero does not demonstrate equality, noninferiority or equivalence. Baseline names refer to the documented configurations; the Converter training regime is not a reproduction of its published multi-corpus setting.

## When this method is a reasonable candidate

A destination-space migration is required, only a declared small paired fitting set is available, and a compact non-neural forward adapter is useful. Evaluate the actual mixed index at the intended budget and inspect both nDCG and Recall before choosing a cutover. Query vectors stay in the native destination space; each document ID has one true or proxy vector.

All-paid fitting can change the choice: FiQA/E5 ARC2 loses to Procrustes and LA2M when all 28,819 paid pairs are available; MiniLM versus all-paid ridge is unresolved. TREC-COVID/E5 native Full-X also exceeds Full-Y, and ARC2 is below both. These are substantive limits, not deleted exceptions.

## Claims excluded from this release

Universal or strongest-baseline superiority; equivalence/noninferiority from unresolved intervals; optimal use of every paid pair; an independent one-versus-two-step win; measured dollar/physical migration savings; isolated H100 throughput; ANN, serving SLO or real-traffic benefits. Partial destination exposure is |A union S| with anchors included. B2 full-corpus model caches are not physical partial-deployment cost measurements.

The ARIS semantic verdict is **partial**, same-family/provisional. Computational QA is PASS; a formal manuscript claim audit has not been run. No manuscript is included or modified. No new experiment, retuning or method switch is authorized by this package.

Evidence: [DEV](results/b1c_r3_review_20261031/SUMMARY.md), [independent B2](results/b2_review_20261101/SUMMARY.md), [all-paid control](results/b1p_r5_review_20261027/SUMMARY.md), [mechanism](results/b1mp0_r1_review_20261026/SUMMARY.md), [mixed diagnostics](results/b1g_r1_review_20261027/SUMMARY.md), and [fresh ARIS review](provenance/aris_b2/001-claim-review.response.md).
