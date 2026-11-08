# ARC2-Global paper workspace

**Latest manuscript delivery (2 November 2026):**
[Supervisor packet](D:/ARC2-Global_Supervisor_Review_20261102.zip),
[current PDF](paper/ARC2_Global_DASFAA2027_supervisor_20261102.pdf),
[updated Overleaf ZIP](D:/ARC2-Global_Overleaf_20261102_r2.zip), and
[anonymous artifact](D:/ARC2-Global_Anonymous_Artifact_20261102.zip).
The MiniLM matched-target ablation is integrated in Results/Figure 3; GCPA is
cited and distinguished in related work. Standard 16-page LNCS, 175-word
abstract, 19 references. Read [the current handoff](paper/review/SUPERVISOR_HANDOFF.md).
The user will send the packet. No method/raw run or previous delivery ZIP
was changed. final.pdf/source.zip aliases now point to this revision.

The following dated handoffs and experiment summaries are historical.

**Current handoff (2 November 2026):**
[Development ZIP](D:/ARC2-Global_Development_20261102.zip) and
[Overleaf ZIP](D:/ARC2-Global_Overleaf_20261102.zip) are complete and verified.
Read [the keep/archive/cleanup guide](D:/ARC2-Global_Keep_Archive_Cleanup_20261102.md).
The development ZIP has a portable START_HERE.md and the latest positive
TC1L mechanism control; the Overleaf ZIP contains the unchanged16-page draft
plus a ready-to-integrate TC1L supplement. GCPA/TC1L manuscript integration
and supervisor feedback remain the finite paper checklist. No source folders
were deleted and no public upload was performed.

**R2 completeness correction:** [complete experiment atlas](D:/DASFAA-2027-paper-release/EXPERIMENT_ATLAS.md) now exposes all1,340logicalqualitycells plus450diagnosticcases and supportingtests. Current supervisor packet isR2; the original r1 ZIP is preserved as an audit snapshot.

**Supervisor review package (1 Nov2026):** [open the clean release](D:/DASFAA-2027-paper-release/START_HERE.html). Claim frozen; portable verification/figures/synthetic smoke PASS; manuscript unchanged.

<!-- B2_CURRENT_BEGIN -->
1 November 2026: **B2 COMPLETE and locally verified**, 184/184 rankings, 60/60 fits, separate endpoint verification before one-shot scoring. Primary nDCG family:11 positive,19 unresolved, 0 negative intervals. Independent advantage is confirmed for specific Converter/ridge/SimpleLinear configurations; Procrustes and LA2M advantages remain unconfirmed. All negatives are retained. Backup complete 58.98 GB / 1,330 files.

[Current report](REPORT.md) | [Independent B2 tables and figures](results/b2_review_20261101/SUMMARY.md) | [Claim assessment](CLAIMS_FROM_RESULTS.md) | [Tracker](refine-logs/EXPERIMENT_TRACKER.md).

STOP after results/QA/figures/ARIS. Manuscript remains unchanged; no B3/B4, new datasets or retuning. Earlier execution notes below are historical and do not describe the current job status.
<!-- B2_CURRENT_END -->

[Recovery protocol](protocols/B1C_R3_FILESYSTEM_RECOVERY_20261030.md) |
[Live tracker](refine-logs/EXPERIMENT_TRACKER.md).
The38 displaced FiQA cells stay historical evidence; R3 refits missing baseline
models consistently across all three budgets. This does not complete or relabel
the original320-cell attempt. STOP after full DEV report/final D1, before B2.

[Current consolidated report](REPORT.md) | [Complete six-method results and figures](results/b1c_r3_review_20261031/SUMMARY.md) | [B1-G diagnostics](results/b1g_r1_review_20261027/SUMMARY.md)
| [ARIS claim-by-claim review](CLAIMS_FROM_RESULTS.md) | [Research findings](findings.md).
The angular-refinement DEV effect is supported; fair all-paid results remain
encoder-dependent and the MiniLM ridge comparison unresolved. B1-G identifies
an actual mixed-replacement quality reversal on E5, without proving its cause.
All negative results and failed attempts remain retained. No new fit or algorithm change.

[Latest B1-P results and all comparisons](results/b1p_r5_review_20261027/SUMMARY.md).
MiniLM all-paid ARC2 has higher nDCG than four baselines, with an unresolved
ridge comparison; E5 trails Procrustes/LA2M. Both regimes, all references,
negative results and all32 predeclared contrasts remain reported.

[Latest B1-M/B1-P0 results](results/b1mp0_r1_review_20261026/SUMMARY.md),
[B1b results](results/b1b_20261026/SUMMARY.md) and
[B1a results and preserved failure](results/b1a_r1_20261025/SUMMARY.md).
DEV mechanism results remain available; independent B2 results and their narrower scope are linked above.
Read [REPORT.md](REPORT.md)
for existing results and the [single experiment plan](refine-logs/EXPERIMENT_PLAN.md)
for what remains. Progress is in the [tracker](refine-logs/EXPERIMENT_TRACKER.md).

**Plan revision 2:** mandatory 0/1/2-step and lambda controls, affine ridge as a
main baseline, a FiQA 50% all-paid-pairs comparison, and mixed-gallery score
diagnostics now precede the decision on independent/system experiments. The
fixed method is unchanged. B3/B4 are conditional rather than automatic. The
expanded maximum is 1,340 ranking cells including development controls; the
independent contrast family becomes 30 because ridge is added. These are
planned cells, not completed results or permission to run them.

## What is here

- `src/arc2_global/`: standalone selected algorithm, without historical method
  branches. Centered Procrustes, two tangent ridge updates, lambda=10, normalized
  proxies, anchor-inclusive true-vector replacement. No neural mapper training.
- `results/fiqa_development/`: only ARC2-Global, A2M/Procrustes adaptation and
  Embedding-Converter adaptation, plus full-X/full-Y references. 64 existing
  rankings, selected per-query metrics, anchor/selection IDs and summaries.
- `REPORT.md`: regenerated means and limits, including Recall and full references.
- `manuscript/`: reused LNCS class/style, bibliography and section layout from
  the previous paper; text rewritten for the actual method and evidence.
- `configs/`: fixed method identity and proposed dataset/method registry.
- `protocols/`: packaging checks and completed, committed B1a/B1b preparation
  protocols. The next scientific campaign needs its own committed protocol.
- `provenance/`: verbatim original run metadata/seal, import hashes, algorithm
  extraction mapping, archive/reuse record and local QA receipts. Exact synthetic
  parity passed in four dimension configurations; 64 rankings and 12 mean rows
  passed hash/per-query verification. The working manuscript compiles to five pages.

The original repositories remain untouched. The earlier contents of this folder,
including Git history, manuscript, figures, literature notes and reviews, are
preserved at `D:/DASFAA-2027-paper-before-arc2-global-20261025`. We reused its
template, bibliography and section structure; its numerical placeholder tables
and reviews are not empirical support for this paper. Literature notes remain
available there as leads requiring primary-source checks.

## Scope of imported FiQA evidence

FiQA is inspected development data: 57,638 documents, 500 DEV queries, two
encoder pairs, five seeds, 25%/50% anchor-inclusive budgets. ARC2-Global was
selected after inspecting these scores. Packaging is not an independent test.
The imported report had no candidate-specific confidence intervals; the new
B1-M fixed contrasts are reported separately above and in REPORT.md. Physical
deployment cost, real traffic and SLO advantage remain unmeasured. Baselines are adaptations, not original
paper reproductions. Source method IDs are preserved in raw/provenance files.

The two external baseline families in the imported64-ranking study are A2M/Procrustes
and Embedding-Converter. The earlier Procrustes+local8 control is not the
published clustered LA2M algorithm and is not counted as independent LA2M evidence.
The clustered LA2M adaptation, official-code SimpleLinear and standard affine
ridge passed B1b synthetic validation and the B1-P FiQA50% benchmark; breadth remains pending. SimpleLinear
is the upstream five-affine-layer MLP despite its name; LA2M's fixed20 clusters
are a script-guided matched-budget setting, not a published optimum. The ridge
row also serves as a mechanism control.

## Proposed data scope

| Collection | Documents | Evaluation queries | Role |
|---|---:|---:|---|
| NanoNQ | 5,035 | 50 | development breadth |
| NanoHotpotQA | 5,090 | 50 | development breadth |
| NanoFEVER | 4,996 | 50 | development breadth |
| FiQA full corpus | 57,638 | existing 500 DEV | inspected development |
| TREC-COVID full | 171,332 | 50 | prospective independent confirmation |
| MS MARCO Documents v1 subset | 100,000 | freeze after ID/log preparation | systems/ORCAS |
| **Total corpus entries across collections** | **344,091** | | |

This follows the user's selected MS MARCO 100K scope and latest five-collection
retrieval table. No custom FEVER/HotpotQA 100K, MS MARCO 1M or AOL-IA is added to
the core plan. ORCAS references MS MARCO documents and adds no corpus to this sum.
The sum is corpus entries across datasets, not a claim of globally deduplicated
texts or number of physical destination encodings in repeated deployments.

## Local use

```powershell
python -m pip install -e .
python tools/render_results.py
python tools/render_b1p_report.py
python tools/verify_package.py --output provenance/qa/verify_repeat.json
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Re-rendering reads saved metrics, never qrels. Verification receipts use unique
paths. Historical Linux runtime versions are in source metadata; local packaging
versions do not replace the historical numerical environment. Model and data
files are not duplicated here: their immutable hashes/locations are recorded.
Future execution must locate/hash-check them and commit its environment lock.

## Current checkpoint

B1a/B1b and B1-M/P0/P/G are complete. The live tracker distinguishes these
finished controls from B1c's remaining main external-baseline comparisons.
Current order: B1c protocol/smoke/completion, final D1, conditional B2,
then evidence-based writing/audit/release. B3/B4 remain separately conditional.
The scoped D1 recommendation does not skip unfinished breadth or authorize a run.

`tools/render_results.py` now preserves the current B1-P/B1-G report sections
when refreshing the historical imported evidence; its previous overwrite defect
was reproduced and fixed on temporary copies. `tools/render_b1p_report.py`
points status to the live tracker rather than regenerating an obsolete next phase.
Regression receipt: provenance/qa/next_steps_render_regression_20261027.json.

The five-page manuscript still covers the imported FiQA subset and predates
B1-M/P/G integration. REPORT.md is the current numerical/claim report. The
manuscript needs its measured tables, scope, baseline list and conditional
systems wording updated before submission. Credentials stay outside this project.

Current report regeneration: `python tools/integrate_b1c_report.py`. B1c figures: `python tools/render_b1c_r3_report.py` (requires the matching local PASS QA receipt; rerender requires visual review). Legacy `tools/render_results.py` targets imported FiQA, not the current consolidated report.
