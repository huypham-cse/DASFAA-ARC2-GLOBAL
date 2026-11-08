# ARC2-Global — current supervisor draft

Open **[the revised PDF](ARC2_Global_DASFAA2027_supervisor_20261102.pdf)**.
`ARC2_Global_DASFAA2027_final.pdf` is an identical convenience alias. This
revision integrates the MiniLM matched-initialization controls into Results
and Figure 3, and positions ARC2 against GCPA in related work.

The document has **16 standard LNCS pages, a 175-word abstract and 19
references**, anonymous author fields and ordinary template dimensions.
No scientific method, raw ranking or original protocol changed.

## Deliverables

- [Supervisor packet](D:/ARC2-Global_Supervisor_Review_20261102.zip): PDF, source ZIP, anonymous artifact and a short review note. User will send it.
- [Updated Overleaf ZIP](D:/ARC2-Global_Overleaf_20261102_r2.zip): select `main.tex`; no large data bundle required to compile.
- [Anonymous numerical artifact](D:/ARC2-Global_Anonymous_Artifact_20261102.zip): frozen mapper, six evidence groups, ranking arrays, verification and table/figure scripts.

The artifact is a prepared local ZIP, not a hosted link. Its README defines
frozen-output verification and mapper use on supplied vectors, separately
from full encoder training or physical deployment reproduction.

## Edit and build

Edit `main.tex`, `sections/*.tex`, `references.bib` and
`figures/mechanism.tex`. From the project root:

```sh
python paper/scripts/build_evidence.py
python paper/scripts/build_paper.py --output ARC2_Global_DASFAA2027_final.pdf
python paper/scripts/verify_paper.py
python paper/scripts/package_source.py
python paper/scripts/verify_source_zip.py
```

These commands read completed results and render the manuscript; they do not
fit, encode, open qrels or launch H100 jobs. Changed paper inputs require a
new hash-scoped audit before being treated as checked.

## Checks and provenance

See [the supervisor handoff](review/SUPERVISOR_HANDOFF.md),
[revision/evidence map](review/revision_tc1l_gcpa_20261102/REVISION_NOTES.md),
[current claim audit](PAPER_CLAIM_AUDIT.md), `review/FINAL_QA.json`,
`review/SOURCE_ZIP_SMOKE.json` and `review/EVIDENCE_MAP.json`.
The current audit is its Markdown/JSON pair; the older audit HTML and
scorecards are historical snapshots. This revision receives no new
acceptance score.

Previous documents are retained under
`review/revision_tc1l_gcpa_20261102/before/`. Original D: delivery ZIPs remain
intact. Full ARIS traces stay private. No email, public upload or conference
submission has been performed.
