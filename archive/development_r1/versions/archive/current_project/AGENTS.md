# ARC2-Global paper workspace

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

CURRENT-SNAPSHOT ARIS SCORING COMPLETE - 2 November 2026. Read
`paper/review/scoring_20261102/SCORECARD.md` for the current assessment:
overall6/10 weak accept; focused novelty6/10 PROCEED; result-to-claim YES,
support8/10. All three reviewer threads used gpt-6.1-sol/high;
same-family/provisional, not an acceptance probability. The support reviewer
disclosed prior-opinion exposure in required instructions/protocol text;
the paper grader avoided earlier scores. Reports retain differing judgments.
Current PDF/source/scientific inputs unchanged. No experiments/qrel opening.
Follow-ups: cite/position against published GCPA and provide an accessible
anonymous scientific artifact. No manuscript edit was made in scoring.
Full reviewer traces remain project-local, per the ARIS tracing skill.
STOP for user/supervisor feedback; older task summaries below are historical.

PAPER STYLE REVISION COMPLETE - 2 November 2026. The user explicitly
requested a thorough evidence/consistency audit and professional design using
the supplied ACIIDS paper as a style reference. Current manuscript:
`paper/ARC2_Global_DASFAA2027_final.pdf`, 16 standard LNCS pages, 159-word
abstract; SHA256
`e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc`.
Read `paper/README.md`, `paper/review/SUPERVISOR_HANDOFF.md` and
`paper/PAPER_IMPROVEMENT_STATE.json`. Revision evidence and reports are under
`paper/review/aciids_style_revision_20261101/` (folder retains task-start date).

Fresh current claim audit PASS: 218 claim records, 101 current input hashes;
canonical `paper/PAPER_CLAIM_AUDIT.json`. Presentation review READY, all16
pages inspected, no mandatory fixes. All revision agents used gpt-6.1-sol/high,
same-family/provisional. Earlier two6/10 scores belong to prior snapshot;
no new acceptance score/probability was assigned. Original reviews retained.

Newly surfaced evidence: E5 ARC2/25% exceeds Converter and ridge/75% on all
five collections (post-hoc descriptive; no equal-quality physical-cost claim);
MiniLM TREC Recall point means lead six adapters at all3budgets; second-step
benefit22/24 conditions/all5seedmacros; MiniLM allpaid-minus-fixed +0.0596
[0.0393,0.0806]. All baseline/native and E5 allpaid outcomes remain visible.
The solver omission is resolved: DEV fixed-anchor ARC2 dual float64; allpaid
and TREC primal float64; allpaid comparisons reuse dual fixed rankings.

Native mechanism retained; empirical charts use true LaTeX serif with complete
legends and both prospective metrics. Tables use grouped booktabs, identity
tint, and full-precision best/second emphasis. Existing six generated numerical
artifacts keep all previous values; substantive citation contexts unchanged.
The anonymous manuscript ZIP compiles independently; separate R3 research
release unchanged. Anonymous public evidence/code link remains pending.
Scientific src/ops/configs/protocols/results and legacy manuscript unchanged.
No H100 job, new experiment, retuning, qrel opening, public upload or submission.
STOP for supervisor/user feedback; previous writing STOPs below are historical.

R3 PAPER-STORY RELEASE1Nov2026: latest ZIP D:/DASFAA-2027-paper-release-20261101-r3-paper-story.zip,372032202bytes, SHA46e511a935d2068e86c4c19532fe4ad7a0b5e00a36018452f78705bd889b7a3e. User explicitly requested concise positive paper-style framing INSIDE releaseZIP, not an exhaustive front-page audit. Lead with contribution/strongest supported results; place complete comparisons, history and operational scope behind EVIDENCE_GUIDE.md. README/CLAIM_LOCK/RESEARCH_STORY/START_HERE now revised; fullAtlas/rawdata/limits retained. No rootREPORT/CLAIMS or manuscript rewrite in this editorial task. All6007scientificfiles unchanged; newpresentationclaims verified;6258manifested files verified insideZIP. Parameterstorage1.13MiB/114.7x versusdeclaredConverterweights isstructural, notmeasured end-to-endcost. Receiptprovenance/qa/supervisor_release_story_R3_20261101.json. STOPforuser/supervisorreview.

R2 release COMPLETE1Nov2026: D:/DASFAA-2027-paper-release-20261101-r2-complete.zip (371,845,465bytes,SHA0de0dbac7f886f0da1524abad445e6883a4259c252c8ef61b788248433550344),6247manifestedfilesverifiedinsideZIP. SeeEXPERIMENT_ATLAS.md inrelease:1340logicalqualitycells+G660rawdiagnosticrankings, 64historicalimports/38displacedrecords/4777nonGsourcefilesretained,9paperfigures. Allnumeric/coverage/visualchecksPASS; freshsemanticARISreviewREVIEW_UNAVAILABLE duequota. No manuscript/algorithm/rawchanges. STOPforuser/supervisorreview; no furtherautomaticexperiments. Receiptprovenance/qa/supervisor_release_completeness_R2_20261101.json.

R2 completeness audit1Nov2026: current logical quality union1340=736mainDEV+360ablation+60allpaid+184B2; G210pure/450mixed separate. Corrected R1 omission of10historical converter25% rawrankings, supportingB1a/B1b/compactfailures; now64imports/38displacedrecords and4777nonGsourcefiles preserved. AllM/P/I/G rawranking metrics/locked control intervals independentlyverified;9paperfigures(6main+3controls). Freshsemanticreleaseaudit interruptedbyaccountquota: REVIEW_UNAVAILABLE, notPASS; priorcompletedB2partialreview unchanged. D:/DASFAA-2027-paper-release isR2, completeAtlasfrontpage. No newH100experiment, retuning, ormanuscriptchange. STOPafterfinalR2ZIP andnumericchecks.

Supervisor review release authorized 1 Nov2026: user requested claim freeze and a new clean D:folder before manuscript writing. Release at D:/DASFAA-2027-paper-release, claim revision supervisor-review-20261101-r1. Original scientific sources/results unchanged. Portable raw-ranking/statistical QA PASS on736DEV+184B2, frozen-method synthetic smoke8checks PASS,6figures rebuilt identically. No SSH/Git/originalbackup required for portable review. Full H100 rerun is an archived reference route, not a tested one-command deployment. Manuscript remains unchanged. STOP after supervisor package; await supervisor/user feedback before paper writing or new experiments.

<!-- B2_CURRENT_BEGIN -->
1 November 2026: **B2 COMPLETE**, all 184rankings/60fits, endpoint replay before labels, FINAL_SCORED03:12:54+07. Local QA PASS (results\b2_review_20261101\qa_completed_20261101T020214554697Z.json); all 1,138 compact files/181,895,786bytes verified. Primary family: 11 positive / 19 unresolved / 0 negative; all 6 Procrustes point differences negative, all Procrustes/LA2M family intervals unresolved. ARIS claim_supported=partial, same-family/provisional. Complete report/figures at results/b2_review_20261101; root REPORT/CLAIMS current. Backup: 1,330 files / 58,977,150,839 bytes complete 03:16:10+07, zero pending; no owned remote B2 job remains. Manuscript: 20 files unchanged. STOP before manuscript changes, B3/B4, retuning or new datasets. Earlier execution entries below are historical.
<!-- B2_CURRENT_END -->

B2 LIVE 31 Oct 23:47:30 +07: full RUNNING,127/184 rankings (69.02%),
41/60 fit groups complete. Six of ten Converter fits PASS (all five MiniLM
and E5seed17; latest58.43min). Current E5seed29 Converter finished selection
50,000 steps in3008.03s; fresh refit at7000steps/215.84s, finite/no failures.
Four Converter fits remain including current;19 total fit groups remain.
Campaign252862/full261763 alive. GPU2614/20096MiB, two external compute
processes plus owned worker361500. No final label opening/scoring yet.
Output539.3GBfree. BackupPID7844 active,848files/40,196,068,953bytes verified
partial; latest successful poll23:46:37 had41groups/3pending or unstable.
All20 manuscript file hashes unchanged. No source, lock, method or runtime
changes. Raw status provenance/qa/b2_status_20261031T164730Z.json and local
backup/manuscript receipt b2_local_status_20261031T164730Z.json.
Auto: complete184 rankings -> separate endpoint verification -> one-shot
scoring -> STOP for local QA/figures/ARIS; leave manuscript unchanged.

B2 RELEASE31Oct2026: User authorized the planned independent TREC-COVID
confirmation through verified results/figures/ARIS, explicitly excluding
manuscript updates. Earlier B1c/D1 STOP below is now released for B2 only.
Protocol protocols/B2_TREC_COVID_CONFIRMATION_20261031.md, configs/b2_lock.json
pin184rankings/60fits/30primarycontrasts. No retuning, newdataset or systems.
Keep TRECqrels closed until184sealed+separateendpointverificationPASS.
Dedicatedencoder runtime ready onMini.201; pre-runreviewPASSsamefamilyprovisional,
27syntheticchecks and61sourcepins. Scientificsmoke/full notyetstarted.
STOPafterB2 resultsreview; leave manuscript unchanged (20fileSHA baseline).

Current31Oct2026: B1c-R3 COMPLETE,358newrankings/736scoredcells. Fullsealed
12:39:55+07, separateDEVscore12:45:14; no ownedrunremains. LocalQA PASS:
736rawrankings rescored,239200values maxerr3.33e-16; locked20kbootstrapmaxerr
4.44e-16. All5fixed1024macronDCGfamilyCIspositive; limitations/allpaidnegative
rowsretained. Sixmethodreport/CSV and3figures PDF/SVG/PNGvisualQA PASS.
ARISfinalD1 narrowGO-C1 recommendation; overallpartial/samefamilyprovisional.
Current REPORT.md,CLAIMS_FROM_RESULTS.md,findings.md,plan/tracker updated.
Use tools/integrate_b1c_report.py forconsolidatedreport; legacyrender_results.py
onlydescribesimportedFiQAandmustnotreplacecurrentreport. No source/lock/raw
changes; original320/R2 interruptedattempts+38displacedhistoricalcells preserved.
TRECclosed. STOPbeforeB2/TREC/systems untiluserreview; noautomaticnewphase.
Ifreleased,nextscientificitemexistingB2184cells/30contrasts undernewprotocol.
CurrentcampaignbackupCOMPLETE13:05+07:2484files/64.479GB,0pending;
receipt provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json.
CompactQAdoesnotclaimcheckpointregeneration.

Latest30Oct09:49+07: B1c is NOT RUNNING. SSH Mini .201 works but original
/root/arc2_global_paper_20261025 and /root/arc2_p3h_20261020 are absent;
no campaign/worker/tmux session, GPU25MiB/20096MiB/no compute processes.
Same hostname, PID1 only~3h47m old; observations consistent with container
recreation/filesystem replacement, not a completed scientific run. Searches
of normal roots, empty /home/jovyan and mounted /network-volume found no
actual ARC2/B1c project. MAIN .225 still times out. Prior RUNNING notes below
are historical. Local backup D:/ARC2-server-backup-20261028 was moved to
cloud by the user; user provided Google Drive folder for recovery. Original
28Oct backup predates current B1c run. Local earlier scored results remain;
new B1c raw/checkpoint recovery is unconfirmed. Never claim242 latest-observed
rankings are currently reusable without actual artifact verification. See
tracker; no new run/scoring started during this incident check.

Latest28Oct13:51+07: R2 matching smoke PASS436.568s; full recovery RUNNING,
verifying/importing95 completed rankings before225 remaining endpoints.
No failures. This supersedes the smoke-running checkpoint immediately below.

User released OOM recovery28Oct. New protocol B1C_R2_OOM_RECOVERY_20261028.md
and recovery lock/95-cell manifest committed989e679; scientific-source
deployment67d7b16c28f7205d3873f6fe09df62eab722fdd4. R2 campaign launched on
same Mini at13:43:29+07 in server tmux; matching smoke currently running.
95 rankings/45 completed groups are pinned for import;225 endpoints/75 new
Nano fits remain. No numerical/scorer/original-lock changes. Full/scoring wait
for matching smoke/all320 seal respectively. Source deployment
/root/arc2_global_paper_20261025/code_67d7b16_b1c_r2; schedule/full/smoke names
mini_r2_20261028. See single tracker for latest live status. Original R1 failure
below remains unchanged and is not the R2 status. STOP after report/final D1.

Latest execution check28Oct13:15+07: B1c MINI full is FAILED_PRESERVED,
stopped12:55:41 at95/320 new rankings due to SimpleLinear CUDA OOM at model
allocation. No owned full/worker remains;225 rankings plus scoring/report/D1
remain. No scorer/label/TREC opening. Preserve all artifacts; recovery needs
committed protocol and verified reuse. Historical RUNNING observations below
are superseded. See tracker and b1c_status_20261028T061507Z.json.

Read README.md, refine-logs/EXPERIMENT_PLAN.md and its tracker first.
This workspace contains ARC2-Global only as the proposed method. Do not add
historical method implementations or their result rows to the active report.
The original repository and the archived earlier paper remain intact; their
locked protocols/raw results are authoritative for imported measurements.

- Existing FiQA results are inspected development evidence, with method
  selection after scores. Packaging does not make them independent.
- Preserve original source IDs, hashes, negative outcomes, failed attempts,
  and baseline adaptation qualifications in provenance. A clean report is
  not authorization to erase research history or conceal method selection.
- Numerical identity: centered rectangular Procrustes raw affine expansion,
  lambda=10, exactly two tangent updates, no local residual/neural training.
  Alterations require a separately named revision and new protocol.
- Count unique destination document encodings |A union S|, anchors included.
  Seeds: 17,29,41,53,67. Exact retrieval is primary; ANN agreement is separate.
- Before new scientific runs: commit a precise immutable protocol with source,
  model/data revisions, hashes, seeds, tie handling, ranking seal, scoring rule
  and failures; smoke first; use a new output directory. Never tune on test qrels.
- No artificial elapsed-time/RAM/VRAM/headroom stop thresholds are authorized.
  Record resources/load; retain actual OS/I/O/numerical failures and contamination.
- Current execution2026-10-27: B1-M/P0/P/G complete; B1-P124/124 scored and verified.
  Generation7530c8e old metadata remains FAILED_PRESERVED for original scorer
  duplicate-start receipt defect before parse. Actual recovery4062d96 smoke
  PASS, then scoring DEV_SCORED at10:20+07, output originalrun/
  scoring_recovery_r1_20261027. No original status/lock/source/rank change.
  All10 converters PASS; local QA recomputed28means/32contrasts/96intervals.
  B1-P results results/b1p_r5_review_20261027/SUMMARY.md; single tracker current.
  B1-P completion STOP receipt b1p_completion_stop_receipt_20261027.json retained.
  MiniLM allpaid ARC2 beats4 baselines in nDCG family comparisons; ridge unresolved.
  E5 trails Procrustes/LA2M; retain negatives and all fixed/allpaid results.
  No method switch/independent/cost/SLO claim. Current bounded D1 below; TREC closed.
  User authorized B1-G+ARIS27Oct: existing450cases/210fitted galleries, CPU-only
  main137/377 andmini73/73 shards; no newfits/embeddings/calibration.
  Protocol B1G_MIXED_GALLERY_DIAGNOSTICS_20261027.md and b1g_lock freeze
  source registries at pre-run commit515b3d10. Both shard smokes PASS; full CPU
  diagnostics launched27Oct13:29+07 in code_515b3d1_b1g/results on both hosts.
  Both full shards now PASS/sealed:210galleries/450mixed exact old-rank matches.
  Separate DEV scoring PASS; all450historical per-query arrays exact. R2 local QA
  PASS:450ranking/paired diagnostics,90five-seed conditions,3795503values, maxerror0.
  First local verifier path-normalization failure remains preserved; no raw/source change.
  Figure PNG/PDF visual QA and SVG validation PASS. Latest bundle
  results/b1g_r1_review_20261027; current REPORT.md, CLAIMS_FROM_RESULTS.md, findings.md.
  ARIS overallpartial, same-family provisional. D1 narrowGO-C1 for frozen fixed-anchor
  mechanism/quality confirmation only; systems not admitted, no next experiment authorized.
  No owned MAIN B1-G process; completion receipt b1g_remote_completion_stop_20261027.json.
  Full original25.54GB inventory retained remote; local compact bundle includes
  every ranking,ID,selection,per-query metric,mean,CI and all JSON/log evidence.
- B1-P STOP was released for B1-G by explicit user instruction27Oct. STOP after
  finite B1-G report and ARIS/D1 analytical recommendation; await user before
  remaining breadth/TREC/systems or formal claim audit. No algorithm retuning.
- Keep the original failed input-byte smoke and binary-qrel scorer attempt.
  R2 successful scoring is separate; original FAILED_PRESERVED metadata stays.
  Frozen dual remains the primary; validated primal backend is opt-in, and current
  all-paid fits belong to the separately locked B1-P campaign. Large raw vectors/coefficients/synthetic
  arrays remain on H100 with the full manifest; the local result is a documented
  compact review bundle containing all rankings/per-query metrics/IDs/logs.
- REPORT.md and the current result summary include B1-M/B1-P/B1-G and D1; the manuscript
  predates these studies. Pre-run lock/registry files retain their historical bytes;
  current completion status belongs in the live tracker/receipts.
- Old manuscript numerical tables/figures and reviews based on placeholders
  are not evidence. Generate every reported number from the selected raw results.
- Keep one live experiment plan/tracker. Versioned snapshots are provenance.
- File review27Oct: B1c remains416/736 main DEV cells; exactly 320 planned
  rankings missing. Complete it before final D1 refresh/B2. Existing scoped D1
  review remains unchanged and provisional; it does not waive unfinished breadth.
  FiQA50 missing endpoints have30 saved-fit reuse paths; Nano270 endpoints need
  up to 90 method fits if no further compatible cache exists. No run authorized
  by this roadmap review. See current critical path in the existing plan.
  Legacy render_results refresh now preserves B1P/G sections; sandbox regression
  PASS. Neither live REPORT nor raw/source scientific artifacts was regenerated.
  Frozen definition-time configs retain old status strings intentionally; use
  tracker/receipts for completion. B2 confirms fixed-anchor quality against
  external baselines; one-versus-two necessity stays DEV unless prospectively extended.

- User released B1c on28Oct: execute the existing320 missing DEV rankings,
  complete the six-method report and refresh final D1, then STOP before B2.
  Protocol B1C_MAIN_MATRIX_COMPLETION_20261028.md, configs/b1c_lock.json and
  b1c_sources/b1c_existing bind120groups/320new/416existing. Commit before
  matching H100 smoke/full. FiQA30 saved fits require exact50% parity; Nano
  has90 fixed1024 fits shared across25/50/75%. Separate scorer only after all
  new320 rankings seal, retains all736 results, no TREC or method changes.
  R1 amendment74c6a75 moves full to MINI .201 MIG20GB; deployment19f3f0e.
  MAIN smoke1df7c3e PASS remains; MAIN full queue stopped before full. MINI
  matching smoke PASS41.057s.453files/1.9476GB transfer COMPLETE and567-source
  preflight PASS. Full campaign launched28Oct11:27+07,62886/62887;2/320 new
  rankings observed11:28, RUNNING/no failures, no scoring or TREC access yet.
  Local transfer session43308 exited0; laptop no longer required. See tracker.
  Separate scoring waits for320 seal; no TREC access. Missing
  auxiliary pyarrow25.0.1 installed--no-deps and synthetic-reader checked;
  numerical versions unchanged. No artificial caps or changes to others' jobs.
  Backups of selected roots on both hosts are complete on D;217.61GB old
  p8-a-recompute root is outside that backup, not used by current registries.


- B1-P initial smoke failure (six synthetic near-tie neighbor swaps) is kept.
  R1 restores original dense float32 neighbor scores and stable rowwise top-k;
  no training policy changed. Read the live tracker for exact current status.
