# ARC2-Global — supervisor review, 2 November 2026

**Two tangent ridge corrections improve mixed-gallery retrieval while
retaining one compact affine document adapter.** The intended application
uses destination-model queries during gradual document migration.

Read [the revised PDF](../ARC2_Global_DASFAA2027_supervisor_20261102.pdf).
The [sendable packet](D:/ARC2-Global_Supervisor_Review_20261102.zip) contains
the paper, Overleaf sources, anonymous numerical artifact, verification
summary and draft covering note. The user will send it.

| Evidence | Main message |
|---|---|
| Four-collection development | Best macro nDCG among six adapters: +0.0243 over Procrustes [0.0181,0.0308]. |
| Matched-initialization MiniLM controls — now integrated | ARC2 0.3075 vs chordal 0.2935 and Euclidean 0.2959; gains +0.0140 [0.0097,0.0186] and +0.0116 [0.0078,0.0157]. Both positive in all five seed means. |
| Second update | +0.0069 over one step [0.0038,0.0100], without another inference stage. |
| Prospective TREC-COVID | E5 beats evaluated Converter and ridge at all three budgets. MiniLM/75% reaches 0.5195 nDCG vs native Full-Y 0.5203; Recall point means lead six adapters at each budget. |
| Lower E5 destination exposure | ARC2/25% exceeds Converter and ridge/75% on all five collections; descriptive observed operating points. |
| Already-paid pairs | MiniLM improves +0.0596 [0.0393,0.0806] at unchanged 50% coverage. |
| Compact mapper | 1.13 MiB coefficients, 114.7 times fewer parameter bytes than evaluated Converter; no neural mapper training. |

GCPA is now cited from its official ICML/PMLR publication. Related work
distinguishes its consensus-direction neural corrector from ARC2's paired
destination targets, current-coefficient prior and finite affine updates.

The new ablation is FiQA/MiniLM development evidence. The completed TREC
study supplies prospective evidence, with geometric competitors retained.
Resource advantages concern destination-vector exposure and coefficient bytes;
physical encoding cost and serving SLOs require separate measurement.

## Verification and finite next step

- Current fresh ARIS [claim audit](../PAPER_CLAIM_AUDIT.md): gpt-6.1-sol/high, same-family/provisional.
- Standard LNCS: 16 pages, 175-word abstract, 19 references; no overfull boxes or undefined references; anonymous metadata.
- All 16 pages rendered/inspected; detailed figure/table checks.
- Overleaf ZIP compiled in isolation with identical paper text.
- Anonymous artifact checks 2,460 ranking records / 1,623 distinct arrays, means, gallery arithmetic and matched-control bootstrap; separately regenerates all 16 table/CSV outputs identically.

**Next: supervisor feedback on contribution framing and submission readiness.**
The local artifact is ready to share; choose anonymous hosting when arranging
the actual submission. No additional study, H100 run, retuning, label opening
or new acceptance score is implied by this revision.
