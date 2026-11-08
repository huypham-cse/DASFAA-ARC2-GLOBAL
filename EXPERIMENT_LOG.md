# Current additional development experiments

<!-- TC1L_CURRENT_BEGIN -->
2 November 2026: **TC1L MINILM LOCAL COMPLETE / STOP FOR REVIEW**.
Pre-run commit66be60f. All20full rankings sealed/scored; local independent
metric QA PASS (20,000values, maxerror2.22e-16), bootstrap exact.
ARC2 nDCG0.307505 vsChordal0.293506 /Euclidean0.295915 /B0.285828.
T-C +0.013999 [0.009704,0.018621]; T-E +0.011589 [0.007821,0.015656],
both positive with originalK4 correction (98.75% individual intervals).
Both gains positive in all5fixed seeds. Full71.28s, sampledpeakRSS514.58MiB.
ARIS claim_supported=yes/high, same-family/provisional. Mechanism DEV evidence
under matched initialization/supervision/arithmetic; not independent confirmation.
E5 remains pending; remote TC1 status unknown and preserved. Manuscript and
frozen ARC2 unchanged. [Result table/figure](results/tc1l_local_r1_20261102/report/SUMMARY.md).
STOP before manuscript edits, regrade, method changes, E5 or new studies.
<!-- TC1L_CURRENT_END -->

<!-- TC1_CURRENT_BEGIN -->
2 November 2026: **TC1 REMOTE STATUS UNCONFIRMED / SSH TIMEOUT**.
Pre-run07d0456; lock c48679786a8216e18fcdd61fe7cae366b7c9b0383c7a3da35293c1a10e78c30b.
Launched .201 tmux arc2_tc1_20261102, campaignPID554726. Last observed:
synthetic PASS7.97s; real smoke RUNNING(PID554743). No full/scoring result
observed. Original SSH disconnected10054; repeated .201/.225 timeout.
.240 read-only accessible but separate host without cache/project. No duplicate
run started. Local MiniLM X/query/full-Y hashes match; E5 complete cache not
established; laptop freeRAM~1.49GiB. No local science started. Exact continuation:

efine-logs/TC1_STATUS_20261102.md; canonical JSON
provenance/qa/tangent_control_status_20261102.json. Reconnect and read existing
campaign before recovery. Manuscript/frozen ARC2/history unchanged.
<!-- TC1_CURRENT_END -->

Canonical prior evidence remains in REPORT.md, findings.md and the single tracker; no historical results are replaced.
