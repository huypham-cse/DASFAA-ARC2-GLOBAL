# ARC2-Global — development handoff, 2 November 2026

Start with **`paper/ARC2_Global_DASFAA2027_final.pdf`** (16 pages). Edit
`paper/main.tex` and `paper/sections/`, not the legacy `manuscript/` tree.
The current paper, method code, all compact comparison evidence and the new
positive MiniLM mechanism experiment are included. Nothing is submitted or
published by this handoff.

## What is finished

- The frozen method is centered rectangular Procrustes followed by two tangent
  ridge updates, lambda10, no local residual or neural mapper training.
- Main development comparisons, mechanism/sensitivity/all-paid/mixed-gallery
  studies and the prospective TREC-COVID study are complete. Full comparisons,
  native references and failed/negative evidence are retained.
- New TC1L control: FiQA development, MiniLM -> DistilRoBERTa,50% paid exposure,
  five seeds,20rankings. ARC2 nDCG@10=0.307505, versus norm-scaled Chordal2
  0.293506 and EuclideanResidual2 0.295915. Corrected differences:
  +0.013999[0.009704,0.018621] and +0.011589[0.007821,0.015656]. Both gains are
  positive in allfive fixed seed means. See the complete report at
  `results/tc1l_local_r1_20261102/report/SUMMARY.md` and its vector figure.
- TC1L numerical QA PASS and ARIS result-to-claim YES/high, same-family/
  provisional. The manuscript has **not yet incorporated TC1L**.

## Finite paper completion checklist

1. Add the new matched-initialization MiniLM ablation to Experiments/Results.
   Ready-to-use LaTeX and PDF figure are in `paper/additional_material/`.
2. Add/position against published GCPA (*Multi-Way Representation Alignment*,
   ICML2026): https://proceedings.mlr.press/v306/achara26a.html.
   Read `paper/review/scoring_20261102/NOVELTY_SCORE.md` for the equation-level
   difference. Do not describe angular Procrustes correction itself as first.
3. Prepare a separate anonymous public code/evidence artifact. **This private
   development ZIP contains operational provenance and is not the public
   anonymous artifact.** The Overleaf ZIP is the manuscript-only route.
4. Obtain supervisor feedback, check the eventual submission instructions,
   page limit and anonymity, then freeze the submission version.

No additional experiment is required to retain the exact bounded current
claims. Optional research includes the pending E5 control, more independent
conditions or deployment measurements. None was started by this packaging.
The last holistic internal score was6/10 before TC1L; no regrade was performed.

## Scientific boundaries to preserve

FiQA and Nano datasets are inspected development evidence. TC1L is a distinct
Windows measurement, not new independent confirmation or byte-identical Linux
reproduction. Original TC1 remote status is unconfirmed; E5 controls remain
pending. TREC geometric comparisons, native-model quality and negative all-paid
E5 findings remain in the paper/evidence. Match a claim to its actual study;
do not turn coefficient-storage or cache exposure into measured end-to-end cost.
Paid destination documents are the unique union of anchors and replacements.

Before a new scientific run, create and commit a new immutable protocol, run
smoke first and use a new directory. Keep the original locks, raw files and
negative evidence. New variants need separate names. Do not tune on final-test
labels. Writing/packaging does not authorize another H100 job.

## Working map

| Path | Purpose |
|---|---|
| `paper/` | Current editable LaTeX, bibliography, figures, source PDF and reviews |
| `src/arc2_global/` | Frozen ARC2-Global and explicitly named controls/adapters |
| `ops/`, `configs/`, `protocols/` | Original scientific execution/protocol records |
| `results/` | Current raw rankings, per-query outputs, summaries and TC1L |
| `findings.md`, `EXPERIMENT_LOG.md` | Latest completed results and scope |
| `inputs/minilm_fiqa/` | Byte-identical vectors sufficient for the local MiniLM control |
| `archive/r3/`, `handoff/R3_MAPPING.json` | Prior complete supervisor release, deduplicated by exact bytes |
| `provenance/source_history.bundle` | Original Git commits, including pre-run locks |
| `research_skills/ARIS/` | Local skill snapshots; optional for scientific execution |

## Read and verify without an experiment

Python3.10+ is sufficient for package hashes:

```text
python handoff/verify_package.py .
```

The full old R3 review snapshot can be reconstructed into a new empty directory:

```text
python handoff/reconstruct_r3.py ../ARC2-R3-review
```

It contains the old portable verification instructions. Large physical H100
weights/vector caches are **not** all inside this ZIP; the two server backup
folders remain separate archival material. The package is enough to continue
paper/code development and inspect/recompute bundled metrics, not a promise of
one-command full H100 re-encoding/checkpoint reproduction.

## Build the paper

Install a working MiKTeX/TeX Live with LNCS dependencies. From `paper/`:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Upload the separate Overleaf ZIP and select `main.tex` to use the same sources.
The supplementary TC1L fragment is intentionally not included by `main.tex` yet.

## Resume experimental development safely

Read the lock/protocol first. Original Windows and server absolute paths are
historical provenance. To propose a relocated MiniLM run without changing them:

```text
python handoff/prepare_local_draft.py
```

That command writes a new protocol/lock draft only; it does not fit, retrieve,
score, contact H100 or change old records. Review and commit the draft before
running its printed campaign command. Use an environment with NumPy, SciPy,
psutil and threadpoolctl; exact observed versions are recorded in the draft.
The original Windows runtime was NumPy2.5.3/SciPy1.18.1/Python3.12.10.

For original history, clone `provenance/source_history.bundle` into a separate
directory. The handoff working tree includes additional portable files that
are not part of the frozen scientific source commits. Its package manifest
identifies every delivered file and original source.
