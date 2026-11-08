# ARC2-Global — current DASFAA 2027 draft

Open **[ARC2_Global_DASFAA2027_final.pdf](ARC2_Global_DASFAA2027_final.pdf)**. This is the current manuscript. Earlier PDF filenames are preserved snapshots; the build receipt identifies the latest output if Windows keeps a viewer lock open.

The paper uses the standard LNCS class, anonymous author fields, a <=200-word abstract and no margin/font compression. Figures and tables come from the frozen current ARC2-Global evidence. `manuscript/` and the earlier release ZIPs remain unchanged.

## Edit and build

Edit `main.tex`, `sections/*.tex`, `references.bib`, and the editable `figures/mechanism.tex`. Build with an installed MiKTeX/TeX Live plus Python and pypdf:

```powershell
python scripts/build_paper.py --output ARC2_Global_DASFAA2027_final.pdf
```

Rebuild the native LaTeX mechanism:

```powershell
python scripts/build_mechanism.py
```

Regenerate empirical tables/figures from completed scoring files in the parent research project (NumPy, Matplotlib and LaTeX required):

```powershell
python scripts/build_evidence.py
python scripts/build_paper.py --output ARC2_Global_DASFAA2027_final.pdf
python scripts/verify_paper.py
python scripts/package_source.py
python scripts/verify_source_zip.py
```

These commands perform analysis/rendering; they do not run H100 experiments, fit models, encode documents, retrieve new rankings or open test labels.

## Overleaf

Upload `ARC2_Global_DASFAA2027_source.zip` and select `main.tex` as the main document. The source ZIP contains anonymous manuscript sources, bibliography, prebuilt vector figures and the editable TikZ mechanism. It excludes internal review logs, local paths, server records and raw experiment bundles. Empirical evidence remains in the research project and the existing supervisor release; manuscript-source compilation does not require those large files.

## Review material

`review/SUPERVISOR_HANDOFF.md` summarizes the paper story and actual completed review status. `review/FINAL_QA.json` records deterministic numerical/layout checks. `review/EVIDENCE_MAP.json` maps tables, plot values and quantitative prose to frozen evidence. Full studies/negative conditions remain in the existing release and underlying data.

The current 2 November revision has **16 pages and a 159-word abstract**. It adds the five-collection E5 exposure comparison, a complete four-panel prospective nDCG/Recall figure, clearer all-paid uncertainty, and LaTeX table hierarchy. `scripts/plot_publication.py` controls the chart design; `scripts/build_evidence.py` supplies every plotted value from saved results. The source ZIP includes the companion `generated/trec_recall.tex` table.

All revision agents used `gpt-6.1-sol`, high. The latest fresh claim audit is **PASS** (218 claim records, 101 input hashes) and presentation review is **READY**. See `review/aciids_style_revision_20261101/` and the current supervisor handoff. `CITATION_AUDIT.md` retains the 18 source assessments with verified citation-context continuity.

The subsequent **2 November current-snapshot ARIS scoring** is complete: **6/10, weak accept** overall; focused novelty **6/10, PROCEED**; bounded result-to-claim **YES**, with empirical support **8/10**. Read [the scorecard](review/scoring_20261102/SCORECARD.md) or its [HTML view](review/scoring_20261102/SCORECARD.html). The reports preserve reviewer differences and exposure disclosures. GCPA citation/positioning and an accessible anonymous scientific artifact are the non-experimental follow-ups; the manuscript and evidence were not changed by scoring. Earlier scoring rounds remain historical assessments of earlier snapshots.

The draft is for author/supervisor review. Internal scores are neither an actual venue decision nor an acceptance probability. No GitHub publication or conference submission has been performed.
