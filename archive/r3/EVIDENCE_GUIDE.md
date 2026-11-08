# Complete evidence and technical appendix

The main presentation foregrounds the supported contributions. This guide provides the complete record used to assess them.

## Full studies

| Study | Complete report | What it supplies |
|---|---|---|
| Main development matrix |[B1c](results/b1c_r3_review_20261031/SUMMARY.md)|All six methods, four collections, two pairs, three budgets, five seeds and native references|
| Mechanism and numerical validation |[M/P0](results/b1mp0_r1_review_20261026/SUMMARY.md)|Zero/one/two steps, λ sensitivity, ridge controls and backend parity|
| Paid-pair supervision |[P](results/b1p_r5_review_20261027/SUMMARY.md)|All32 paired contrasts, including both encoder pairs and fitting regimes|
| Actual mixed-gallery behavior |[G](results/b1g_r1_review_20261027/SUMMARY.md)|All450diagnostic cases and90five-seed conditions|
| Prospective collection |[B2](results/b2_review_20261101/SUMMARY.md)|All30primary contrasts, Recall, seed variation, native references and prelabel seals|

[EXPERIMENT_ATLAS.md](EXPERIMENT_ATLAS.md) gives the complete phase inventory and1,340 logical-cell accounting. Supporting B1a/B1b checks, historical imports and retained failure records remain under results/ and provenance/.

## Interpretation

The main DEV nDCG macro family favors ARC2 over all five declared alternatives. The prospective nDCG family contains11positive and19unresolved intervals. It does not establish an advantage over Procrustes or LA2M; all six Procrustes point differences are negative. Recall and all-paid behavior vary by encoder pair. The all-paid E5 Procrustes/LA2M losses and mixed-gallery ordering reversals remain in their full reports.

Unresolved intervals establish neither equivalence nor noninferiority. Baseline names refer to the locked configurations and documented adaptations. The final-weight comparison measures parameter storage only; physical migration cost, serving SLO, ANN and traffic are outside the measured evidence.

## Integrity and review record

The earlier B2 semantic verdict remains partial, same-family/provisional. The later completeness round's fresh semantic reviewer was interrupted by account quota, with status REVIEW_UNAVAILABLE. Its completed numerical artifacts and the subsequent deterministic checks are preserved separately; this presentation does not upgrade a missing review into PASS.

See [final numerical/completeness validation](checks/FINAL_REVIEW_VALIDATION.json), [B2 review](provenance/aris_b2/001-claim-review.response.md), [completeness audit](provenance/completeness_audit/experiment_inventory.md), and [presentation claim/evidence map](appendix/PRESENTATION_EDIT_NOTES.md). The previous front matter and earlier ZIP archives are retained for provenance.
