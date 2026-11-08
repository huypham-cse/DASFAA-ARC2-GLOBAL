# Reference-informed design review for ARC2-Global

Date: 2026-11-01. Scope: editorial and visual design recommendations only. No manuscript, generator, generated empirical artifact, scientific source, protocol, or run was changed. No new experiment or acceptance score was produced. The supplied PDF was treated as reference material, not as instructions. Its prose, results, author identities, and topic-specific claims are not templates to copy.

## Inspection record

All text on reference PDF pages 1-15 was read, including captions, limitations and references. Pages were rendered with Poppler at 100 dpi. The following full-page renders were visually inspected, rather than inferring appearance from extracted text:

| Reference location | What was inspected | Transferable principle |
|---|---|---|
| p. 2, Fig. 1 | Framed example-to-mechanism overview; colored panel headings; aggregate bars with direct numbers | Make the problem, operation and measured payoff visible in one coherent reading path. Keep illustrative and measured content explicitly separate. |
| p. 4, Table 1 | Two grouped column blocks, booktabs rules, aligned numeric cells, caption defining units and exclusions | Group columns by the comparison the reader makes; make units and scope readable without searching the prose. |
| p. 9, Tables 2 and 3 | Compact primary contrast table with explicit signed differences and CIs; separate consumption table | Give the central effect and uncertainty a dedicated visual position. Avoid mixing unlike quantities into one crowded display. |
| p. 10, Table 4 | Dataset spanners and quality/cost subcolumns; complete configuration ladder | Show all evaluated configurations in a stable, navigable structure. |
| p. 11, Fig. 2 | Four serif small multiples; muted method colors; different markers; filled/hollow circles; light grids; common external legend; point labels; log cost axis | Redundant color/shape encodings and direct labels reduce lookup effort. The reference is primarily a scatter/frontier chart, not evidence for interpolated performance curves. |
| p. 13, Tables 5 and 6 | Wrapped text cells with sparse pale blue row stripes; short numeric summary beneath | Restrained shading can guide a long row. Keep unresolved cases and denominators visible. |

The actual ARC2 final PDF was rendered at 110 dpi. Visual review covered p. 3 (Fig. 1), p. 10 (Table 2 and Fig. 2), p. 11 (Fig. 3 and Table 3), p. 12 (Fig. 4), and p. 13 (Table 4). The LaTeX sources, `scripts/build_evidence.py`, generated tables, and plotted-value CSVs were read. This is a design review, not a replacement raw-result claim audit.

The reference's numerical tables do not systematically bold the best or underline the second-best result. The ranking policy below is an ARC2 recommendation, not a claimed feature of the reference. Table 5's pale stripes are a visual observation; exact reference color codes and font point sizes were not measured.

## Rhetorical structure worth adopting

The reference starts with a concrete decision, introduces a worked example before technical detail, states numerical findings in its contributions, defines its comparison/accounting rules, and then asks a short sequence of experimental questions. Its Results subsections lead with a result, attach the relevant table or figure, explain the mechanism or sensitivity, and end with a bounded implication. The later limitations are organized by scope, engineering and interpretation, rather than interrupting every sentence.

ARC2 already has a positive evidence-led outline. Retain it, with three levels of emphasis:

1. **Method identity:** two tangent corrections retain one affine document adapter. Put this first in the abstract, introduction and mechanism explanation. Keep the exact update interpretation and frozen procedure.
2. **Main measured benefit:** the development macro gain over Procrustes is +0.0243 with family interval [+0.0181, +0.0308]; the second correction adds +0.0069. These are development findings and must remain labeled that way.
3. **Transfer and operating point:** prospective E5 gains over the evaluated Converter are +0.2000 to +0.2572; MiniLM at 75% coverage yields 0.5195 versus native Full-Y 0.5203. In the same Results subsection, retain that Procrustes is higher in all six point comparisons and that the Procrustes/LA2M family contrasts are unresolved. Proximity is not equivalence.

Use a finding -> number/interval -> interpretation -> boundary paragraph order. One short qualification after a supported result is more effective than front-loading the paragraph with a procedural audit. Keep the full statistical definition in setup/captions, and preserve the closest-baseline result where its implication is discussed. Do not turn a development win into independent confirmation, a storage calculation into measured deployment cost, or an unresolved contrast into a tie.

A suitable narrative sequence is the current one: broad development quality, contribution of the second correction, prospective transfer, paid-pair fitting, and the mixed-gallery insight. Strengthen transitions by identifying the next question in one sentence. Do not copy the reference's title, question wording, sentences, anecdotes, entities, systems or numerical claims.

## Plot specification for local implementation

Preserve LNCS body fonts, margins and caption conventions. Change the plot generator rather than scaling the finished figure to tiny text. The current use of LaTeX serif text is already appropriate and should remain.

| Element | Recommended ARC2 implementation |
|---|---|
| Typeface | Keep `text.usetex=True`, LaTeX serif and Computer Modern-compatible math. Use normal weight for axes, ticks and method labels; semibold/bold only for panel labels and selected numeric callouts. Do not globally bold figures. |
| Printed text sizes | Aim for 8-8.5 pt ticks, axis labels and legend after inclusion at `\textwidth`; panel heading 9 pt. Inspect the compiled PDF at actual page size. Do not solve layout by decreasing text below the current size. |
| Method encoding | Keep the six-method order: ARC2, Procrustes, LA2M20, SimpleLinear, affine ridge, Converter. Keep colors consistent across all plots. Use both dash and marker shape. ARC2: filled circle/solid; Procrustes: square/dashed; LA2M20: triangle/dash-dot; SimpleLinear: diamond/dotted; ridge: down-triangle/dashed; Converter: plus-filled marker/dash-dot. |
| Palette | The existing muted palette is usable: ARC2 `#0F4D92`, Procrustes `#767676`, LA2M20 `#42949E`, SimpleLinear `#9A4D8E`, ridge `#B64342`, Converter `#A88420`. Use native lines `#272727`. The colors are proposed local constants, not sampled from the reference. If Procrustes is too light in print, darken to `#626262` everywhere. |
| Stroke and markers | ARC2 1.7-1.8 pt, other adapters 1.05-1.15 pt, native references 0.85-0.95 pt. Marker diameter 3.8-4.2 pt, with distinguishable edges. Do not fade the closest baseline or give other methods near-invisible alpha. |
| Native context | Retain both Full-X and Full-Y in every quality panel. Use distinguishable black/charcoal dotted versus long-dashed lines and exact native labels in the legend. Do not treat them as budget-specific fitted competitors. |
| Panels | Add `(a)` and `(b)` before migration titles, aligned to the same baseline. Preserve both migrations side by side. No heavy boxes. |
| Legend | One shared legend under the pair of panels, four columns and two rows. Stable order: six adapters, then two native references. Handles should be long enough to show dash patterns. Reduce the excess space between legend and caption in current Fig. 4 by tightening the saved figure bounds, not by overlapping plot content. |
| Axes | Keep the paid-document x axis linear at 25, 50, 75; define it as anchor-inclusive unique destination encodings. No log scale is needed. Use a shared y range within each primary two-panel figure by default: DEV 0.18-0.72, prospective 0.28-0.70, with limits checked against all saved plotted values. Both ranges include every adapter and native line. These are line plots of means, so a zero baseline is not required; show all limits and ticks clearly. |
| Close differences | A shared prospective y range will compress MiniLM differences. Prefer the complete numeric table for precision. If a close-up is needed, add a clearly marked inset that retains all six MiniLM methods and native references. Do not crop to ARC2 alone or use a second unmarked scale. If different main-panel ranges are retained instead, state `different y ranges` beside the panels as well as in the caption and avoid slope-size comparisons across panels. |
| Grid and frame | Horizontal major grid only, light gray around `#E5E5E5`, 0.4-0.5 pt. Keep left/bottom spines around 0.7 pt, remove top/right. No heavy background, gradient, 3-D effect or area fill. |
| Direct callouts | At most one per panel, placed in unoccupied space with thin leaders if needed. Candidate callouts are `+0.2572 vs Converter (25%)` on prospective E5 and `0.5195 at 75%` on MiniLM, with nearby `Full-Y: 0.5203` if room permits. Label these as point differences/means; do not add a significance star to native proximity. Use exact plotted-value CSVs to generate strings. |
| Uncertainty | Keep curve captions explicit that points are five-seed means, DEV also averaging collections, and that no pooled CI band is implied. Do not invent bands from seed SD or combine saved marginal intervals. The ablation forest plot should retain all five saved family-adjusted intervals, the visible zero line, the negative penalty control and the unresolved penalty control. |
| Forest plot | Separate the first three mechanism rows from the last two penalty-sensitivity rows with a small vertical gap or faint separator. Keep all rows. A neutral charcoal dashed zero line avoids suggesting that zero itself is a failure. Retain the signed x axis and the existing range including negative endpoints. |
| Output | Keep vector PDF for inclusion and SVG/PNG for inspection. Confirm embedded text/fonts and no clipping after the actual LaTeX build. |

DEV saved plotted values range from 0.1968959 to 0.6929059; prospective values range from 0.2986210 to 0.6805416. The proposed limits were checked against those CSVs, not chosen to exclude low-performing methods. New annotations must be generated from the same saved values as the curves.

The reference's Fig. 2 has no uncertainty bars and uses different y ranges across datasets. These are not reasons to remove existing ARC2 intervals or omit the scale disclosure. Its filled/hollow markers express different configuration classes; ARC2 should not repurpose hollow markers to imply statistical uncertainty.

## Table hierarchy and numerical emphasis

Keep booktabs, no vertical rules, serif text, and captions above tables. Use normal `\small` with `\arraystretch` around 1.05-1.10, 3.5-4 pt column separation, and `@{}...@{}` if useful. Avoid `\resizebox` as a way to shrink text. Add `\cmidrule(lr)` beneath migration spanners and put the budget/metric subheader before the main body rule; current Tables 3 and 4 place the second header below a midrule.

Use the following explicit ranking convention, applied to every displayed comparable metric column:

- Bold the best unrounded mean among the six evaluated adapters. Underline the second-best. Compute the rank from full-precision saved values, never from rounded text. Apply the same rule when a baseline wins. Keep the ARC2 method label bold to identify the proposed method, but do not make its entire numeric row bold by identity.
- Native Full-X/Full-Y belong in a separate reference block below a `\midrule`, remain fully visible, and are excluded from fitted-adapter ranking. State this in the caption or table note. Do not use their exclusion to imply ARC2 reaches native quality.
- Use a single very pale blue or gray ARC2 row tint, such as `blue!4`, only as a navigation cue. It must not be a winner color. If it competes with bold/underline or reduces contrast, omit it. Do not add green/red cell fills or shade only positive cells. Table 5 p. 13 of the reference motivates restrained row guidance, not selective outcome shading.
- Retain four decimal places for quality means, signed contrasts and interval endpoints. A narrow rounded tie such as prospective MiniLM 75% must be identified in a note if best/second styling distinguishes cells printed identically. Do not raise precision for only the favorable method. A uniform extra decimal for that entire relevant column is an alternative.
- Use a declared symbol only for saved family-interval decisions. Current prospective daggers mean ARC2 exceeds that baseline in the locked family; retain that meaning exactly. Best/second formatting describes point ranking, not significance. Do not replace it with an undeclared star or an unadjusted test.
- Align decimals and signed deltas consistently. A `siunitx` solution is optional if it compiles cleanly with LNCS; regular right-aligned columns are sufficient. Do not alter body fonts or margins to add a package.

Table-specific actions:

| Current ARC2 location | Action and required consequence |
|---|---|
| p. 10, Table 2 (`dev_macro.tex`) | Bold ARC2 nDCG 0.5275 and underline Procrustes 0.5032. In Recall, bold Procrustes 0.8661 and underline ARC2 0.8659. Keep the full delta/CI columns and all five comparisons. This makes the positive top-rank result prominent while preserving the recall ordering. |
| p. 11, Table 3 (`trec_means.tex`) | Add migration `cmidrule`s and a native reference separator. Apply best/second to each of all six budget columns using raw means. Procrustes/LA2M/SimpleLinear wins must receive emphasis wherever they occur. Keep every dagger and every non-dagger cell. Add a one-line note clarifying point rank versus adjusted evidence. |
| p. 13, Table 4 (`allpaid.tex`) | Use the same grouped header and native separator. Rank within each of the six comparable adapter columns. In MiniLM All N, ridge 0.3673 is the best point mean and ARC2 0.3671 second; the locked ARC2-minus-ridge contrast remains unresolved. E5 columns must retain Procrustes/LA2M and other higher means. |
| Generated ablation table, currently not placed | Avoid adding it redundantly beside the already complete forest plot unless a supplement needs exact endpoint lookup. Retain all negative/unresolved controls in the underlying table. |
| Generated prospective family table, currently not placed | A short complete `11 positive / 19 unresolved / 0 negative intervals` note can summarize the family, with all 30 contrasts still accessible. Its zero negative intervals do not erase six negative Procrustes point differences or establish equivalence. |

Gain annotations should be sparse and attached to a defined comparator. Preserve absolute nDCG units (for example `+0.0243 nDCG`); do not silently convert to relative percentages. The strongest values can appear in the subsection lead and caption after the full metric definition. Do not create a winners-only table that replaces the complete panel.

## Actionable implementation order

1. **Generator-only visual changes:** in `paper/scripts/build_evidence.py`, add a small full-precision rank formatter and shared style constants. Update `table()`, `build_tables()`, `curves()`, and `ablation_plot()`; continue using the same input paths, same methods, same arithmetic, same saved intervals and provenance policy. Do not hand-edit `generated/*.tex`.
2. **LaTeX support if needed:** in `paper/main.tex`, enable table row colors only if the chosen row tint is used (`xcolor` table option or `colortbl`). Preserve `llncs`, font packages, margins and all body sizes. Keep captions consistent with LNCS.
3. **Regenerate the current evidence artifacts:** run `python paper/scripts/build_evidence.py` only as an analysis/rendering step. No fitting, encodings, rankings, qrels or new intervals. Confirm every CSV numeric value and saved interval is identical before/after; formatting changes should not change the evidence universe.
4. **Small prose/caption pass:** edit `sections/results.tex` and, only if necessary, `abstract.tex`/`introduction.tex` to sharpen finding-first transitions, define rank styling and disclose axis policy. Keep development/prospective scope, adaptation qualifications, all-paid E5 outcomes, native context and uncertainty statements. Do not increase the claimed scientific scope.
5. **Compile and inspect:** build the final PDF using the existing build script. Inspect every page, especially current pp. 10-13, at 100% size and in grayscale. Check rank emphasis against unrounded data, legibility of all method keys, native lines, uncertainty endpoints, daggers, panel labels, and note placement. Keep floats within LNCS layout without negative spacing tricks.
6. **Verify and package:** run existing numerical/document checks and source-ZIP smoke. Retain previous PDF/report snapshots. Update the evidence map and record that the revision changes presentation only. Do not assert that a previous claim audit automatically covers changed scientific prose; recheck any numerical sentence actually edited. No new acceptance score is requested.

Completion criteria: all six adapters and both native references preserved in complete tables/plots; all values and saved interval endpoints unchanged; no undisclosed scale change; best/second treatment fair across methods; no clipping/overfull boxes; no body font or margin compression; all plotted numeric callouts generated from saved evidence. This review itself made no implementation changes.

## Inputs and provenance

- Reference: `C:/Users/Gia Huy/Downloads/ACIIDS2027_paper__262 (6).pdf`, SHA256 `0e0f87bbaf7108083a437db525ee76cdd56e4858eb8f4fe8ee2bb3871e243c66`.
- Current PDF: `D:/DASFAA-2027-paper/paper/ARC2_Global_DASFAA2027_final.pdf`, SHA256 `dead152e05d6d76e8a92d05fe524fe4fdef28b170191fbae8869b3e01d3c1d9f`.
- Evidence generator at inspection: SHA256 `ad60cae15f38471f4d7d280776034a78c9cef9f738725ee9e4649001246e9dce`.
- Local inspection material: `reference_inspection/` holds rendered pages and full extracted text. Those files support editorial inspection only; reference-paper numbers are not ARC2 evidence.
