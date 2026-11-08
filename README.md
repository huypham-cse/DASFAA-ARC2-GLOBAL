# ARC2-Global — private development handoff, revision 2

Start with `paper/ARC2_Global_DASFAA2027_supervisor_20261102.pdf` and edit
`paper/main.tex`, `paper/sections/`, `paper/references.bib` and the figure code.
This is the complete working handoff for continuing paper/code development.
It is distinct from the compact anonymous artifact and supervisor-review ZIP.

## Current completed state

- The MiniLM matched-initialization ablation is already integrated in Results
  and Figure 3. Both corrected intervals are positive; original K4 remains.
- GCPA is cited and positioned from the official publication.
- Current paper: 16 standard LNCS pages, 175-word abstract, 19 references.
- Fresh ARIS claim audit PASS: 313 records / 85 input hashes, same-family,
  provisional. It is a numerical audit, not a conference acceptance decision.
- Anonymous artifact and updated Overleaf sources are in `deliverables/`.
- All original R1 handoff files remain either at their original path or in
  `archive/development_r1/versions/` if a current file replaced them. The old
  full R3 manifest and its reconstruction mapping remain intact.

## What to do next

1. Read `paper/review/SUPERVISOR_HANDOFF.md` and the current PDF; collect
   supervisor feedback, then revise the LaTeX and figures in `paper/`.
2. Regenerate numerical tables/figures only from completed outputs. From the
   root: `python paper/scripts/build_evidence.py`. LaTeX is required for plots.
3. Compile in `paper/`: `pdflatex main.tex`, `bibtex main`, then pdflatex twice.
   Alternatively upload the supplied Overleaf ZIP and select `main.tex`.
4. Recheck any changed claim and arrange blind artifact hosting/submission
   after review. No automatic job or public upload is started by unpacking.

Optional research, such as the pending E5 mechanism control, needs a new
explicit scope and pre-run committed protocol. No extra experiment is needed
to preserve the current bounded claims. Do not silently change the algorithm
or tune using already-opened test labels.

## Working map

| Path | Purpose |
|---|---|
| `src/arc2_global/` | Frozen mapper, controls and baseline adapters |
| `paper/` | Current editable manuscript, figures, audit and evidence map |
| `results/` | Completed rankings, per-query arrays, all comparisons and TC1L |
| `configs/`, `protocols/`, `ops/` | Locked settings and execution code |
| `inputs/minilm_fiqa/` | Included MiniLM development vectors/queries/labels |
| `handoff/` | Portable hash verifier, R3 reconstruction and relocation helper |
| `research_skills/ARIS/` | Included optional ARIS skill snapshot |
| `provenance/source_history.bundle` | Original full Git history |
| `provenance/source_history_update.bundle` | Current commits after that history |
| `deliverables/` | Current anonymous artifact and Overleaf ZIPs |

## Verify the delivered folder

```sh
python handoff/verify_package.py .
```

All 6,258 original R3 manifested files are preserved. To reconstruct that
specific old review snapshot into a new empty folder:

```sh
python handoff/reconstruct_r3.py ../ARC2-R3-review
```

The private original audit contains historical absolute machine paths. These
are provenance, not portable live commands. The separately included anonymous
artifact has normalized paths and its own offline verifier. No SSH key or
login secret is supplied. Full H100 encoder weights/checkpoints and all E5
vector caches are not included; retain the large server backups separately.

## Restore current Git history in a separate directory

From this folder (use an absolute path for the second bundle if needed):

```sh
git clone provenance/source_history.bundle ../ARC2-source-history
git -C ../ARC2-source-history fetch ../ARC2-Global_Development_20261102_r2/provenance/source_history_update.bundle master
git -C ../ARC2-source-history merge --ff-only FETCH_HEAD
```

The restored Git checkout is the original source history. This delivered
folder additionally has portable helper files, inputs and deduplicated release
evidence identified by `PACKAGE_MANIFEST.json`; keep them separately rather
than blindly adding the large bundles/archives to a new Git commit. Before a
new scientific run, author/commit its protocol in a working source checkout,
relocate inputs without editing original locks, smoke first and retain failures.

For a relocated MiniLM proposal, `python handoff/prepare_local_draft.py` writes
a draft only; it never starts a scientific run. The selected frozen ARC2 is
lambda=10, exactly two tangent ridge updates, no local residual or neural
mapper training. Paired destination exposure counts all unique anchors and
replacement rows. FiQA/Nano/TC1L are development; TREC is the completed
prospective study, not a new unseen dataset for tuning.

This private development folder contains provenance and is not anonymous.
Use `deliverables/ARC2_Global_Anonymous_Artifact.zip` for blind review.
