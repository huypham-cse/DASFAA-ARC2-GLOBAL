# ARC2-Global paper improvement loop

Scope: improve the existing manuscript, citations, mathematical explanation and presentation. No new scientific run, method selection, tuning, qrel opening or public upload. Reviewer model is **gpt-6.1-sol, high**, following the explicit user override. The maximum is two fresh scoring rounds; scores are internal same-family simulations, not DASFAA decisions or acceptance probabilities.

## Preserved input

`review/final_review_20261101/before_review.pdf` preserves the manuscript at the start of this loop. Original reviews and their read-input hashes remain under the same directory; later edits do not retrospectively change their verdicts.

## Round 1 — review, revise, compile

Fresh reviewer `/root/dasfaa_score_20261101`: **6/10, weak accept, confidence 4/5**. Novelty 6, technical soundness 8, experimental support 7, practical significance 6, clarity 7, reproducibility 8, venue fit 8. The overall is holistic.

Changes implemented:

- Explained the tangent target as a raw-norm-scaled negative cosine gradient and the ridge correction as a quadratic fit centered on the current map.
- Stated the exact common-positive-scale identity, with its analytical assumptions; no convergence or finite-step retrieval guarantee was introduced.
- Distinguished target-principal-direction regularization in related work from per-anchor tangent targets.
- Added the measured prospective MiniLM 75% operating point: 0.5195 versus native Full-Y 0.5203, explicitly a point comparison.
- Clarified that the all-paid experiment keeps lambda 10 in the summed objective.
- Corrected architecture-versus-checkpoint attribution with four experimental-revision model-card links; moved the early-round TREC citation to collection background.
- Fixed Windows viewer locks by compiling in a unique build directory.

Fresh bottom-up audit: 353 claim ledger entries, 97 checks, no mismatch. Separate A–F experiment-integrity audit PASS within its recorded no-qrel-open scope. Those reports are bound to their original snapshots, not automatically to later prose.

Compiled revised manuscript: 15 standard LNCS pages, 155-word abstract. Its source ZIP independently compiles without research data and produces identical extracted text.

## Round 2 — fresh review

Fresh reviewer `/root/dasfaa_score_r2_20261101`: **6/10, weak accept, confidence 4/5**. Novelty 5, technical 7, experimental 7, practical 6, clarity 8, reproducibility 6, venue fit 8. This reviewer saw the manuscript and actual PDF without the prior score or change list. The difference in dimension scores is reviewer variation; no artificial score increase is asserted.

The reviewer confirmed the core equations and inspected all 15 pages and four figures. No critical mathematical correction or mandatory new experiment was requested. Its six ranked concerns were addressed by specifying the current-map-centered cosine-target fit, identifying HMoE as contextual rather than evaluated, accurately stating the separate reproducibility package and pending anonymous link, replacing “two-pair” with “two-migration”, stating shared bootstrap query indices, defining normalization at first use, and darkening the mechanism's small secondary labels.

A second fresh raw audit verified 58 claim groups and reconstructed 388 mean rows and all four saved interval families, with 520 recorded input hashes. Its PASS belongs to the pre-polish snapshot. Final post-polish review is recorded separately; it never inherits that PASS merely because the previous version passed.

Final polish is assessed by compilation, visual QA and a separate claim audit. It does not create a third scoring round or a new reviewer score. The current state and final artifact hashes are recorded in `PAPER_IMPROVEMENT_STATE.json` and `review/FINAL_QA.json`.

The final auditor identified one aggregation-scope issue: all 24 partial-development five-seed condition means are below native Full-X, but two individual NanoNQ/MiniLM/75% seeds are above it. The Discussion now explicitly says “five-seed ARC2 condition mean”; no result value or comparison was changed. The finding and its resolution remain in the final audit ledger. Float placement was also adjusted using standard top/text float fractions so that the all-paid table stays in Results; the final manuscript remains 15 pages with unchanged LNCS fonts and margins.

## Skill coverage

| Skill | Application |
|---|---|
| auto-paper-improvement-loop | Two fresh review → edit → compile rounds; preserved original and explicit state. |
| research-review | Substantive DASFAA review, strongest rejection argument, ranked actionable writing fixes. |
| result-to-claim | Existing completed bounded claim verdict retained; no new empirical scope inferred from prose. |
| paper-claim-audit | Fresh source-to-raw checks, exact values/rounding, comparison scope and chronology. |
| experiment-audit | Read-only A–F code/provenance checks; no test labels reopened. |
| citation-audit | Fresh single-entry primary-source assessments for all 18 references; targeted rechecks of repaired contexts. |
| research-lit / novelty-check | Primary literature positioning and recent closest-method comparison in the method review. |
| ablation-planner | Review of existing 0/1/2-step, lambda, all-paid and mixed-gallery controls; no automatic new runs. |
| formula-derivation | Explicit assumptions and checked gradient, retained-prior and scale identities. |
| research-paper-writing / ml-paper-writing | Result-led structure, precise technical contribution and consistent terminology. |
| paper-compile / PDF | Standard LNCS build, page/abstract/reference checks, full-page visual inspection and isolated ZIP build. |
| Scientific Figure Making | Existing native LaTeX/TikZ mechanism and complete empirical vector figures retained; legibility polish only. |
| render-html | Generated supervisor dashboard from canonical Markdown, with source hash; dashboard is an index, not an additional semantic verdict. |

`kill-argument` routes empirical work to `research-review`; its adversarial purpose is covered by the fresh reviewer’s rejection memo, without invoking a theory-only workflow. Idea generation, experimental roadmap creation and method redesign are outside this completed-paper editing task.

## Completion

The first completed version passed its scoped 18-group/94-hash audit and was 15 pages. That verdict belongs to its original snapshot, preserved under `review/final_review_20261101/` and in Git.

## User-requested evidence and design revision - 2 November 2026

The user supplied an ACIIDS paper as a visual/rhetorical reference and requested a thorough search for underused results. The revision preserves all scientific inputs and introduces no new experiment or final-label access.

- Surfaced E5 ARC2 at 25% coverage exceeding Converter and affine ridge at 75% on all five collections; explicitly post-hoc descriptive, with geometric/neural/native context in the new table.
- Surfaced MiniLM TREC Recall point means leading all six adapters at all three budgets; now shown with all other methods/native references in the four-panel prospective figure.
- Added the second-step breadth (22/24 conditions, all five seed macros) and the all-paid MiniLM gain of +0.0596 [0.0393,0.0806].
- Resolved directional-alignment wording, missing auxiliary-metric coverage, hidden all-paid interval decisions, rounded-value ambiguity, repeated scope prose, and complete dual/primal regime assignments.
- Applied booktabs groups, restrained identity shading, full-precision best/second emphasis and true LaTeX chart typography. No values, saved intervals, axis endpoints or comparison methods were invented or removed.

The final revision is 16 LNCS pages with a 159-word abstract. A fresh claim audit reports **PASS**, 218 claim records and 101 current input hashes; presentation review reports **READY** with no mandatory fixes. Source-ZIP compilation and both HTML render-fidelity reviews pass. Six existing generated numerical artifacts retain all previous values. Citation contexts retain all substantive source attributions.

The previous two 6/10 scores remain historical; this user-requested revision has no new acceptance score. Read `review/SUPERVISOR_HANDOFF.md` for the current manuscript and `review/aciids_style_revision_20261101/` for the complete evidence inventory and resolved findings. No further automatic review/experiment loop is running.
