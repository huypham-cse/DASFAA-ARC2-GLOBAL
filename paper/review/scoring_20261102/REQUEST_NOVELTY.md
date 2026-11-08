# Fresh ARIS novelty scoring

Use gpt-6.1-sol/high only, no delegation. Read-only evaluation: no manuscript,
algorithm, dataset, qrel or scientific-run changes. Workspace D:/DASFAA-2027-paper.
Operational scope is supplied here; do not read old reviewer scores or author
narratives. Disclose any incidental exposure rather than claiming perfect blindness.

Read CURRENT paper/main.tex, sections/*.tex, references.bib and the 16-page
paper/ARC2_Global_DASFAA2027_final.pdf (SHA256
e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc).
Current method implementation under src/arc2_global/model.py/numerics.py and
solver_backend.py may be inspected to disambiguate equations.

Read paper/review/scoring_20261102/LITERATURE_SEARCH.json: nine parent query
formulations across three claims and candidate PRIMARY links, not earlier review
opinions. Continue targeted live primary-source lookup as needed, including the
most recent six months as of 2 November 2026. Use only primary papers,
author-maintained code or official publisher records for technical conclusions.
Verify latest versions, not only search snippets. Search availability is finite;
do not label a non-exhaustive search a proof that no prior work exists.

Priority overlaps: HMoE (ICML2026 Yang/Cao), Embedding-Converter, A2M/LA2M,
Drift-Adapter, FastFill, mini-vec2vec, Procrustes Bounds, spherical interpolation,
and newly discovered Multi-Way Representation Alignment/GCPA arXiv2602.06205
(latest v2 revised July2026). Verify that paper's latest method and correction
equations; do not infer identity from both methods using directional correction.
Older RobProc / iterative Procrustes is another search lead to examine if relevant.

Extract 3-5 actual technical claims; distinguish established ingredients,
new composition, empirical findings and workflow setting. Compare targets,
prior/regularization, parameterization, supervision, mapping direction and
inference form. Score novelty 1-10 with the skill's anchor: 5 means clear
neighbors but a defensible delta; reserve1-3 for a named published result
already containing the contribution. Give a verified one-sentence technical
delta, strongest novelty rejection, and smallest response needed. Separate a
missing citation from a demonstrated duplicate. Do not silently require a
new scientific experiment to fix literature positioning.

=== NOVELTY VERDICT LIMITS (these bound how you judge, never how widely you search) ===
Search exhaustively; judge calibrated. Two failures waste months equally:
passing an idea a published paper already contains, and killing a viable idea
because the territory has neighbors.
1. Proximity is information, not a verdict. Someone working nearby goes in the
   report; it is not by itself a reason to reject.
2. ABANDON has exactly one qualification: a specific published paper already
   contains this result — name that paper. No named paper, no ABANDON.
3. Crowded-but-deltaed is PROCEED: state the delta in one sentence a reviewer
   could verify. Thin or contested delta is PROCEED WITH CAUTION — say what
   would make it carry, not why it should die. CAUTION is not a safe middle:
   if you cannot name the specific thing that makes the delta thin, the
   verdict is PROCEED.
4. Concurrent or competing work is not a veto. That is a race — report it and
   let the user decide whether to run it.
5. A direct attack on a central problem is legitimate novelty when nobody has
   executed it well. "This area is hot" does not mean "this area is taken."
6. This check is an early gate, never the last one — more triage, pilots, or
   external review still stand between any idea and a paper, whatever order
   this run uses. A wrongly passed idea dies cheaply at one of them; a wrongly
   killed idea is never seen again. When torn between two verdicts, choose the
   more permissive one.
Say plainly when an idea clears the check. Do not manufacture overlap.

Write NOVELTY_SCORE.md/.json in paper/review/scoring_20261102/, including live
primary URLs, inspected method sections, exact version, current input hashes,
access limitations, score/rationale and PROCEED/PROCEED WITH CAUTION/ABANDON.
Record same-family/provisional, not official acceptance or a global novelty proof.
