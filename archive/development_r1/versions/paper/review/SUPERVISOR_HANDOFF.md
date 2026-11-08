# ARC2-Global - supervisor manuscript, 2 November 2026

Open **[the current PDF](../ARC2_Global_DASFAA2027_final.pdf)**. The revised manuscript has **16 standard LNCS pages**, a **159-word abstract**, five result/algorithm tables and four vector figures. Its anonymous [Overleaf/source ZIP](../ARC2_Global_DASFAA2027_source.zip) is 1.25 MiB and compiles without the large research dataset bundle. The [official DASFAA guidelines](https://dasfaa2027.github.io/CallforResearchTrack/list.htm) were rechecked: 16 pages including references, abstract at most 200 words, double-blind LNCS.

## The paper to present

**Two tangent ridge corrections deliver strong mixed-gallery retrieval through one compact affine document adapter.** The intended user needs native destination queries while documents are migrated gradually. The revision makes useful quality at limited document exposure the central practical result.

| Evidence | Message supported by existing measurements |
|---|---|
| Broad development quality | Best macro nDCG among six methods, +0.0243 over Procrustes with family interval [0.0181,0.0308]. Every collection-level macro favors ARC2 over all five baselines. |
| Lower destination exposure | On all five E5 collections, ARC2 at 25% coverage exceeds Converter and ridge at 75%. The new table retains geometric alternatives, SimpleLinear and native references. This is a descriptive comparison of observed budgets. |
| Stronger second correction | +0.0069 over one step, positive in 22/24 condition means and all five seed-level macros; no added inference stage. |
| Prospective coverage | MiniLM ARC2 has the highest Recall@100 point mean among six adapters at each TREC budget. At 75%, nDCG is 0.5195 versus native Full-Y 0.5203; Recall is 0.0998 versus 0.1052. |
| Existing paid pairs | MiniLM FiQA improves from 0.3075 to 0.3671 at the same 50% paid coverage: +0.0596, family interval [0.0393,0.0806]. It beats four all-paid baselines; ridge is unresolved. |
| Compact deployment form | 1.13 MiB of affine coefficients, 114.7 times fewer parameter bytes than the evaluated Converter, without neural mapper training. |

The new cross-budget table is post-hoc descriptive, not a newly preregistered hypothesis or an equal-quality physical-cost estimate. The independent TREC study retains its original sealed methods/rankings and matched-budget inferential family. All baseline/native panels and E5 all-paid outcomes remain visible.

## What was improved

- Finding-first abstract and introduction; direct professional wording around the finite algorithm and practical operating points.
- Complete new E5 budget table and a four-panel prospective figure covering both nDCG and Recall.
- LaTeX serif typography, explicit panel labels, complete legends and native references; no invented intermediate points or uncertainty bands.
- Grouped booktabs headers, restrained ARC2 shading, and best/second-best emphasis computed from unrounded means. Other methods keep their winning entries.
- All-paid family markers and its previously underused improvement interval made visible.
- Corrected directional-target wording, rounded-table scope, duplicate prose and exact dual/primal regime assignments.

[Positive-evidence inventory](aciids_style_revision_20261101/POSITIVE_EVIDENCE.md) records what was already reported, what was newly surfaced, and why historical local-residual or duplicate results do not become new Global evidence. [Consistency review](aciids_style_revision_20261101/CONTRADICTIONS.md) gives the original actionable findings.

## Current verification

| Check | Outcome |
|---|---|
| Fresh final claim audit | **PASS**, 218 claim records and 101 input hashes; all published values, rank emphasis and family markers reconcile. [Report](../PAPER_CLAIM_AUDIT.md). |
| Fresh presentation review | **READY**, all 16 pages and detailed figures inspected; no mandatory defects. [Report](aciids_style_revision_20261101/PRESENTATION_REVIEW.md). |
| Existing numerical outputs | Six existing generated data artifacts retain every pre-revision value; TREC adds the saved Recall column. No scientific source or raw result changed. |
| Citation continuity | All 18 substantive citing contexts are unchanged after removing one uncited duplicate sentence; original per-entry primary-source assessments retained. This was not a new 18-reviewer citation round. |
| Document and source ZIP | PASS; no overfull boxes, unresolved references or known identifying strings. Isolated source-ZIP build reproduces the manuscript text. |

All revision agents used **gpt-6.1-sol/high**. Reviews are same-family/provisional. The earlier 6/10 scoring rounds concern the previous snapshot; this revision receives no invented higher score or acceptance probability. Presentation readiness is not a conference decision.

## Remaining author actions

Supervisor approval and an anonymous public code/evidence link remain before submission. The source ZIP is the manuscript, while the unchanged R3 research release holds the larger code/results package. No H100 run, retuning, test-label opening, public upload or submission occurred during this revision.
