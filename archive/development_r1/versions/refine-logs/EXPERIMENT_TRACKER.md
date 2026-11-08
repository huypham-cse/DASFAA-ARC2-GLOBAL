# ARC2-Global tracker

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

R2 release COMPLETE1Nov2026: D:/DASFAA-2027-paper-release-20261101-r2-complete.zip (371,845,465bytes,SHA0de0dbac7f886f0da1524abad445e6883a4259c252c8ef61b788248433550344),6247manifestedfilesverifiedinsideZIP. SeeEXPERIMENT_ATLAS.md inrelease:1340logicalqualitycells+G660rawdiagnosticrankings, 64historicalimports/38displacedrecords/4777nonGsourcefilesretained,9paperfigures. Allnumeric/coverage/visualchecksPASS; freshsemanticARISreviewREVIEW_UNAVAILABLE duequota. No manuscript/algorithm/rawchanges. STOPforuser/supervisorreview; no furtherautomaticexperiments. Receiptprovenance/qa/supervisor_release_completeness_R2_20261101.json.

R2 completeness audit1Nov2026: current logical quality union1340=736mainDEV+360ablation+60allpaid+184B2; G210pure/450mixed separate. Corrected R1 omission of10historical converter25% rawrankings, supportingB1a/B1b/compactfailures; now64imports/38displacedrecords and4777nonGsourcefiles preserved. AllM/P/I/G rawranking metrics/locked control intervals independentlyverified;9paperfigures(6main+3controls). Freshsemanticreleaseaudit interruptedbyaccountquota: REVIEW_UNAVAILABLE, notPASS; priorcompletedB2partialreview unchanged. D:/DASFAA-2027-paper-release isR2, completeAtlasfrontpage. No newH100experiment, retuning, ormanuscriptchange. STOPafterfinalR2ZIP andnumericchecks.

Release handoff COMPLETE1Nov2026: D:/DASFAA-2027-paper-release and adjacent DASFAA-2027-paper-release-20261101.zip (236,649,934bytes). Archive all4400manifested files rehashed inside ZIP; portable full QA and6figure rebuild PASS; claim frozen for supervisor review. Receipt provenance/qa/supervisor_release_handoff_20261101.json. No manuscript/new experiment or external sending.

Supervisor review release authorized 1 Nov2026: user requested claim freeze and a new clean D:folder before manuscript writing. Release at D:/DASFAA-2027-paper-release, claim revision supervisor-review-20261101-r1. Original scientific sources/results unchanged. Portable raw-ranking/statistical QA PASS on736DEV+184B2, frozen-method synthetic smoke8checks PASS,6figures rebuilt identically. No SSH/Git/originalbackup required for portable review. Full H100 rerun is an archived reference route, not a tested one-command deployment. Manuscript remains unchanged. STOP after supervisor package; await supervisor/user feedback before paper writing or new experiments.

<!-- B2_CURRENT_BEGIN -->
1 November 2026: **B2 COMPLETE**, all 184rankings/60fits, endpoint replay before labels, FINAL_SCORED03:12:54+07. Local QA PASS (results\b2_review_20261101\qa_completed_20261101T020214554697Z.json); all 1,138 compact files/181,895,786bytes verified. Primary family: 11 positive / 19 unresolved / 0 negative; all 6 Procrustes point differences negative, all Procrustes/LA2M family intervals unresolved. ARIS claim_supported=partial, same-family/provisional. Complete report/figures at results/b2_review_20261101; root REPORT/CLAIMS current. Backup: 1,330 files / 58,977,150,839 bytes complete 03:16:10+07, zero pending; no owned remote B2 job remains. Manuscript: 20 files unchanged. STOP before manuscript changes, B3/B4, retuning or new datasets. Earlier execution entries below are historical.
<!-- B2_CURRENT_END -->

Revision2, updated31Oct2026. **B1-M/P0/P/G COMPLETE locally;
B1c R3 COMPLETE: scored/verified/report+figures/final D1; original320/R2 INTERRUPTED; TREC CLOSED.**

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

B2 LIVE 31 Oct 22:11:39 +07: full RUNNING,109/184 rankings (59.24%),
35/60 fit groups complete. All five MiniLM Converter fits PASS; latest two
lasted153.91 and113.85min under changing shared load. Current E5 seed17
Converter selection36,500/50,000 after1046.74s, finite/no failures; five
Converter fits remain including current. GPU snapshot1826/20096MiB with
one external process plus owned worker348974. Campaign252862 and full261763
are alive. No final qrel receipt/scoring. Output545.3GBfree.
BackupPID7844 active:587files/23,721,491,411bytes verified partial. One SSH
session disconnect was followed by successful reconnect/poll at22:10:16;
35groups,182pending/unstable files. This did not stop the scientific job.
Manuscript20files unchanged. Raw status provenance/qa/b2_status_20261031T151139Z.json;
local backup/manuscript receipt b2_local_status_20261031T151139Z.json.
No source, method, lock or runtime changes. Finish remaining fixed schedule,
separate endpoint verification, one-shot scoring, local QA/figures/ARIS;
leave manuscript unchanged and STOP before systems or any new experiment.

B2 LIVE31Oct17:23:27+07: fullRUNNING71/184rankings (38.59%),23/60fitgroups
complete. ThirdConverterMiniLMseed41PASS40.35min; nowseed53selection2250/50000
finite/nofailures.7Converterfitsremainincludingcurrent,37totalfitgroups.
Sharedloadreturned:5externalGPUprocesses+ownedworker299647,8110/20096MiB;
prioronly-ownedGPUvisibilitywasatemporarysnapshot. No finalqrelreceipt/scoring.
Output~556.8GBfree. BackupPID7844active,506files/18232181857bytes persisted
verifiedpartial; latestpoll17:21:17 had59pending/unstable/newfiles,notfailure.
Rawstatus provenance/qa/b2_status_20261031T102328Z.json. Manuscriptunchanged.

B2 LIVE31Oct16:42:21+07: fullRUNNING53/184rankings (28.80%),17/60fitgroups
complete. MiniLMseed17ConverterPASS79.22min; seed29ConverterPASS46.77min.
Currentseed41Converterselection14000/50000 after163.21s, finite/no failures.
8Converterfitsremain includingcurrent;43totalfitgroupsremain. SnapshotGPUshows
onlyownedworker288615,1041/20096MiB; sharedload hasfallen, but onesnapshotdoes
notestablishisolatedcostorconstantfuturepace. Noqrelreceipt, no scoringyet.
Output~561.8GBfree. BackupPID7844active,414files/12740803822bytes persisted
verifiedpartial; latestpoll16:39:33 has72pending/unstable/newfiles (notfailure).
Currentproof provenance/qa/b2_status_20261031T094221Z.json. Manuscriptunchanged.

B2 LIVE31Oct15:18:34+07: fullencodingPASS36m02s,all4models171332docs+50queries
each (685328physicaldocencodes,notuniquedocuments). Full fit/rankRUNNING,
17/184rankings,5/60fitgroupscomplete. CurrentMiniLMseed17Converterselection
50000done2734.33s, refit2500finite106.29s; no run/workerfailures. No completed
fullConverteryet, nofinalqrelreceipt. FullcontrollerPID261763,worker262366;
campaign252862 continues. SharedMIG9104/20096MiB with5otherGPUprocesses;
output~572.6GBfree. No isolatedperformanceorqualityclaim.
BackupPID7844active,326files/7249606586bytes persistedverifiedpartial;
latestpoll15:17:29 had6unstable/pendingfiles. Manuscript20filesunchanged.
Rawstatus provenance/qa/b2_status_20261031T081835Z.json.

B2 ETAcheck31Oct14:08:20+07: campaignRUNNINGatencode_full, nofinalqrelreceipt.
DistilRoBERTa all171332docs/50queries complete463.00s. E5base98304/171332docs;
totalphysicaldocencodes269636/685328across4models. No qualityscoresyet.
Provisionalremainingplan:~20-30minencoding,then60fits (including10converter
selection50000+selectedlengthrefit),184rankings andseparatereplay/scoring.
HistoricalloadedB1cconverterfits~40-87mineach suggest~8-16hremainingoverall,
roughly31Oct22:00-1Nov06:00+07. Thisisabroadplanningrange,notmeasuredB2fullfit
ETAorstoplimit; updateafterfirstfullconverter. Sharedloadcanchangeit.
Rawproof provenance/qa/b2_eta_20261031T070820Z.json. No method/manuscriptchanges.

B2 LIVE31Oct13:57:40+07: independentcampaign r1_20261031t064859 RUNNING on
Mini.201:62161, H100MIG20GB. Pre-runcommit26feef1026bea610ec7f53d581c3c9064949d004
andb2_lock SHAe00c970a4061ce6d50f2af9817621243959a9372e6c12a0d4e9c9c9c9d2a93f5
verifiedclean/all61pins. ExactGitcommit sparse deployment omitted only unneeded
historicalrawblobs; requiredsource+config+protocol+tools allpresent/verified.
Deploymentroot /home/jovyan/arc2_b2_20261031/code_26feef1; PID252862 detached.

AcquisitionPASS36.02s (allmodel/corpus/queryhashesverified); encoderSmokePASS
15.91s; CPU/GPUall6methodsyntheticsmoke20/20PASS13:52:40; separate20endpoint
replayPASS13:52:44. FullencodingPID253787 started13:52:44,firstdistilroberta
model106496/171332docs at13:57:40. No failure, nofinalqrelreceipt. Auto next:
full4modelencoding,60fits/184rankings,separate184endpointreplay,one-shotscore
30familycontrasts,STOPforlocalverification/figures/ARIS. No manuscriptupdate,
newmethod,datasetselection orsystems. Timingforecastsneedfullfit observations.

Localstartup proof21files hashverified: b2_r1_startup_proof_20261031.tar.gz,
receiptand b2_r1_startup_verified_20261031.json. Currentstatusreceipt:
provenance/qa/b2_r1_live_status_20261031T0657.json. Manuscript20filesunchanged.
B2incrementalbackupoperator97204/PID7844 active toD:/ARC2-B2-backup-20261031;
25files/880647462bytes persisted verified at13:56:34,partial. Itcopiescompleted
fits/encodings withwholefilehash,skipschangingtensorsuntilcomplete,preserves
failedfinaloutputs. Keep laptopawakeforcopy; remoteexperimentindependent.

B2 AUTHORIZED31Oct2026, PREPARING: user released the next independent
confirmation but excluded manuscript updates. Fixed184rankings/60fits/30nDCG
contrasts, full171332docs/50queries, same6methods/2pairs/5seeds/25,50,75%.
Protocol B2_TREC_COVID_CONFIRMATION_20261031.md andb2_lock prepared; ARIS
pre-runreview002PASS(samefamilyprovisional),27synthetictestsPASS. Initialreview
found/fixedoriginalIDorder,richmanifestbinding andfitartifactverification;
001retained. Dedicatedencodevenv ready onMini.201,H100MIG20GB; baselineenv
unchanged. NoB2scientificrunorqreldownloadyet. Commitprotocol/sourcefirst,
then acquire,pinnedencodersmoke,6methodsmoke,separatesmokereplay,fullencode,
184rankings,separate184endpointreplay,one-shotscore,localQA/figures/ARIS.
No manuscript or systems changes authorized. TREC labels stillclosed.

COMPLETE31Oct2026: full358/358rankings sealed12:39:55+07; separate736-cell
DEVscorercompleted12:45:14+07, scheduleB1C_R3_SCORED_STOP_FOR_D1. No scientific
failures, no owned campaign/worker left. Deployment61f73171 andlockf567a4b6
unchanged; TRECclosed. Statusproof b1c_r3_status_20261031T055703Z.json.

Local review bundle:1540files/120882877bytes,736rawrankings, orderedIDs,qrels,
perqueryarrays and completedscorerhashes verified. Independent metric
recalculation239200values maxerr3.33e-16; locked20kdrawmeans/intervals maxerr
4.44e-16. QA: results/b1c_r3_review_20261031/qa_completed_20261031T060049161714Z.json.
Compact scope excludes checkpoint/vector regeneration; fullrawbackupseparate.
Three figures (quality/Recall/macro+120conditiondeltas) exportedPDF/SVG/PNG300dpi,
CSVrawparity andvisualQA PASS. Complete tables160means/120contrasts/5macro.

All5fixed1024macro nDCGfamilyCIsabovezero; Procrustesdelta+.024325CI
[+.018132,+.030792],23/24highermeans; other4each24/24highermeans. Recall and
allpaid/native-reference limits retained. ARISfinalD1 narrowGO-C1 recommendation,
overallpartial/samefamilyprovisional, no systemsadmission. Trace
.aris/traces/result-to-claim/2026-10-31_b1c_r3/. Current REPORT/CLAIMS/findings
andthistracker supersedehistorical RUNNING notesbelow. Finitecurrentrelease
complete; STOPbeforeB2/TREC/systems, awaituserreview, noautomaticnewrun.
Backup current B1c-R3 complete31Oct13:05+07:2,484files/64,478,738,712bytes (~64.48GB),120groups,0pending/0unstable; watcher exited after terminal coverage. Data at D:/ARC2-B1c-R3-backup-20261030; proof provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json. Scope is current campaign outputs, not every historical project/cache.

Latest31Oct09:16:42+07: R3 advanced346/358rankings (96.65%),116/120groups.
NanoFEVER E5seed17 completed; currentseed29selection50000done/refit12750finite,
no run/worker failures.4fitgroupsremain includingcurrent. Worker206552 active,
samecontrollers2777/2997. SharedMIG6846/20096MiB with5otherGPUprocesses again;
load fluctuates, do not infer an exclusive window. Output~584.6GBfree.
No scorer completion/failure,TRECclosed. BackupPID16356 active,2357files /
59430288363bytes persisted partial; recent live refit checkpoint hashchange
rejected/partial preserved at09:15:45, retrying. Rawstatus:
provenance/qa/b1c_r3_status_20261031T021643Z.json.
STOPafterfullDEVreport/finalD1beforeB2.

Latest31Oct08:52:38+07: R3 stillRUNNING343/358rankings,115/120groups. Current
NanoFEVER E5seed17 selection50000done,refit36250finite, no failures;5fitgroups
remain includingcurrent. Progress withinfit advanced since08:10, not stalled.
GPUsharedmemory now2870/20096MiB, oneothercomputeprocess visible plus ours
(previouslyfive); this snapshot does not prove exclusiveGPU/cost isolation.
Ownedworker197122 active. Output~585.9GBfree. No scorer completion/failure,
TRECclosed. BackupPID16356 active,2334files/58847301965bytes persisted partial;
latestsuccessfulpoll08:50:14 has4pending/unstablefiles. Rawstatus:
provenance/qa/b1c_r3_status_20261031T015239Z.json.
STOPafterfullDEVreport/finalD1beforeB2.

Latest31Oct08:09:51+07: R3 FULL RUNNING,343/358rankings (95.81%),115/120groups.
18more rankings since01:26. Five fitgroupsremain includingcurrent, all NanoFEVER
E5converter seeds17/29/41/53/67. Currentseed17selection20250/50000 finite,
no run/worker failures. Samecontrollers2777/2997; worker197122 active.
SharedMIG9066/20096MiB with5external GPUprocesses, output~585.9GBfree.
Latest3completedconverters86.8/38.4/69.0minutes. Remaining generationestimate
~3-7h at this variablepace, then seal/separateDEVscoring; not a cap/deadline.
No scorer completion/failure, TRECclosed. Rawstatus:
provenance/qa/b1c_r3_status_20261031T010952Z.json.
BackupPID16356 active;2331files/58711334575bytes persisted verifiedpartial.
Latestpoll08:07 showed4unstable/pendingfiles. No claim terminalbackupcomplete.
STOPafterfullDEVreport/finalD1beforeB2.

Latest31Oct01:25:56+07: R3 FULL RUNNING,325/358rankings,109/120groups.
Current HP E5 seed67 converter selection36000/50000, finite gradients/parameters,
no run/worker failures. Count unchanged until fit finishes;11fitsremain.
Ownedworker116226 active, samecontrollers2777/2997. SharedMIG8222/20096MiB
with5otherGPUprocesses; output~594.0GBfree. No scoring, TRECclosed.
BackupPID16356 active;2169files/51138680673bytes persisted verified coverage,
partial. Latestpoll01:25:30 has4unstable/pendingfiles, not backup failure.
Rawstatus: provenance/qa/b1c_r3_status_20261030T182556Z.json.
STOPafterfullDEVreport/finalD1beforeB2.

Latest31Oct00:47:27+07: R3 advanced to325/358rankings (90.78%),109/120groups.
HP E5 seed53 converter completed; next HP E5 seed67 has started.11fitgroups
remain includingcurrent. Earlier00:47:09snapshot showed refit49750finite,
no run/worker failures; subsequent progress confirms its successful completion.
SharedMIG8222/20096MiB and5externalGPUprocesses; output~594.2GBfree.
No scoring yet, TRECclosed. Rawproofs b1c_r3_status_20261030T174709Z.json and
b1c_r3_progress_20261030T174727Z.json in provenance/qa/.
Backup activePID16356 (watcher59203),2145files/50012044919bytes persisted,
partial. Latest successfulpoll00:45:48 had4unstable/pendingfiles. Livecheckpoint
hash mismatch preserved/retried, never accepted as verified bytes. No scientific
code/lock changes or job interference. STOPafterreport/finalD1beforeB2.

Latest31Oct00:22:59+07: Mini R3 FULL still RUNNING,322/358rankings,108/120groups.
Count unchanged while HP E5 seed53 converter completes. Selection50000done,
refit15750 finite; no run/worker failures. Same owned PIDs2777/2997/102334.
MIG8078/20096MiB shared with5externalGPUprocesses; XFS~594.7GBfree. No scorer
started/failure, TRECclosed. Rawstatus b1c_r3_status_20261030T172259Z.json.
Local backup process was absent at this check (cause not established); last
persisted2142files/49.876GB, partial. Live checkpoint hash errors and partials
retained; previous successfulpoll00:15:44 showed9unstable/pendingfiles. Same
backup root/state restarted as watcher59203; no scientific job interruption.
STOPafterfullDEVreport/finalD1beforeB2.

Latest31Oct00:09:52+07: Mini .201 SSH works. R3 FULL RUNNING,322/358rankings
(89.94%),108/120groups,12fitsremain including current. HP E5 seed53 converter
selection47000, finite gradients/parameters, no run/worker failures. Same
campaign2777/controller2997, activeworker102334. Shared MIG7858/20096MiB,
5external GPUprocesses plus owned worker; utilization unavailable in nvidia-smi
MIG view, no claim of100%GPU. XFS~595.3GBfree. No scoring yet, TRECclosed.
Rawstatus: provenance/qa/b1c_r3_status_20261030T170952Z.json (UTCdate30Oct).
Backup watcher21644 remains running; persisted2142files/49876093677bytes,
partial. One live selection_resume.pt hash-change error retained at00:09:24;
partial preserved, unverified bytes not accepted. Watcher retries; this is
not a scientific failure or proof of final backup completeness.
STOPafterfullDEVreport/finalD1beforeB2.

MAIN connectivity30Oct23:59+07: fresh authenticated SSH attempt to
103.73.232.225:52194 failed TCP connect timeout20s, before authentication;
independent TCP5s probe also timedout. SSHconfig confirms same host/port/key.
Cannot inspect GPU/CPU load or establish whether MAIN is free. No MAIN launch
or MINI experiment alteration. Receipt:
provenance/qa/h100_main_connectivity_20261030T165919Z.json.

ETA check30Oct22:33+07: R3 still316/358,106/120groups. Current HP E5 seed29
converter selection50000done/refit19000 finite, no failures.14fitsremain
including current. Latest loaded converter fits40.1/65.9/67.3minutes (one
prior56.6min); estimate9-16h remaining generation if this range persists,
roughly31Oct07:30-14:30+07, plus sealing/separate scoring. Not a deadline or
stop cap; shared load may change it. CPUquota400000/100000=4shared cores;
MIG8834/20096MiB with5external GPUprocesses. MAIN.225:52194 TCP check timedout5s;
no spare reachable worker verified. No runtime/scientific changes or other-job
interference. Rawproofs: b1c_r3_eta_20261030T153333Z.json and
b1c_r3_recent_fit_times_20261030T1533Z.json in provenance/qa/.
After seal: automatic separate736-cell DEVscore, then verified retrieval,
all-results/quality-budget figures and finalD1. STOPbeforeB2/TREC/systems.

Backup resume VERIFIED30Oct22:15:21+07: watcher72964 advanced to675files /
20485735823bytes, beyond prior659files. Both Windows path repairs effective;
no new errors in restarted watcher. Partial backup only; keep laptop awake/
connected. Receipt provenance/qa/b1c_r3_backup_restart_verified_20261030T1515Z.json.

Latest30Oct22:12:23+07: R3 FULL RUNNING,316/358rankings (88.27%),106/120groups.
Nine more rankings since19:52. Current NanoHotpotQA E5 seed29 converter
selection step38000, finite parameters/gradients, no run/worker failures.
14fitsremain including current; shared MIG8690/20096MiB with5other GPUprocesses.
Same campaign2777/controller2997; currentworker64229 active. XFS~597.8GBfree.
No scoring; all358must seal before separate736-cell DEVscore. TRECclosed.
Rawstatus: provenance/qa/b1c_r3_status_20261030T151223Z.json.

Backup correction: previous watcher3088 no longer running. Persisted coverage
659files/20424260876bytes, partial. Its retained events show FileNotFoundError
then Invalid backup relative path: old receipt local paths used Windows
separators, while inside() rejected them. Local operator repair2b6c64c accepts
validated relative Windows paths, writes new receipts with POSIX separators,
continues rejecting drive/UNC/root/traversal escapes (7fixturechecksPASS).
No raw scientific/source/lock/run changes. New watcher72964 restarting same
backup root, existing coverage/errors/partialfiles preserved. Proof:
provenance/qa/b1c_r3_backup_windows_path_repair_20261030.json.
A second operator defect reproduced: ordinary264-character Windows file writes
raise FileNotFoundError on this laptop; backup partial/snapshot names exceed
that limit. Fix1fe8aa4 uses extended-length local root, keeps receipt-relative
paths and escape guards; actual268-character read/write fixture PASS. Error
tracebacks now retained. Watcher21121 was stopped only to load this local fix;
watcher72964 is the current restart, scientific job unaffected. Rawproof:
provenance/qa/b1c_r3_backup_windows_long_path_repair_20261030.json.
STOPafterfullDEVreport/finalD1beforeB2.

Latest30Oct19:52:23+07: R3 FULL RUNNING,307/358rankings (85.75%),103/120groups
complete. Count unchanged because current NanoHotpotQA MiniLM seed53 converter
has not finished; it is advancing, not stopped. Selection50000complete; refit
step36500 with finite gradients/parameters. No run/worker failures.17fitsremain
including current. Shared Mini GPU still has five other processes; observed
8286/20096MiB aggregate. XFS output has~601.0GB free. No source/method changes.
Backup transfer continues without a new recorded error: 650files /
20419491641bytes (~20.42GB) in persisted verified current-session coverage.
Partial backup only; watcher3088 remains active. No scoring yet; all358must
seal first. Raw status: provenance/qa/b1c_r3_status_20261030T125223Z.json;
backup receipt: provenance/qa/b1c_r3_backup_status_20261030T1252Z.json.
TRECclosed; STOPafterfullDEVreport/finalD1beforeB2.

Backup restart verification: new ranged-transfer watcher has reconciled/copied
425files /8,684,339,866bytes in its current persisted verified coverage at
19:04:38+07, beyond initial inventory; no new error reported in this session.
This is partial current-session coverage, not total unique bytes across runs.
Remote training was not paused or changed. Raw local receipt:
provenance/qa/b1c_r3_backup_restart_progress_20261030.json.

Latest30Oct18:58:34+07: R3 FULL RUNNING,307/358rankings complete (85.75%),
103/120groups complete. Current NanoHotpotQA MiniLM seed53 converter selection
step8250, finite parameters/gradients, no worker failures. Scientific deployment
61f73171 unchanged. Output XFS has~601.6GB free; storage issue remains fixed.
No current quality scoring; all358must seal before separate736-cell DEVscore.

Shared load increased: Mini MIG observed7,858/20,096MiB and five other privpetal
GPU processes alongside owned worker. Shared CPU quota remains4cores; four
other workers each~78%CPU, owned worker~73%CPU in the process-average snapshot.
Latest completed converter fit took3393.946s (~56.6min), versus the preceding
four~18.8-19.1min.17converter fits remain, including the active one; prior~8h
ETA is superseded by this actual slowdown. Completion depends on shared load;
do not assume the earlier19min/fit pace. No other jobs/priorities were modified.
Raw load/timing: provenance/qa/b1c_r3_load_fit_times_20261030T115319Z.json.

Backup last old-session verified event:400files/7,978,276,548bytes at18:51:28+07,
PARTIAL. SSH rekey timeout observed; old copy stopped without touching training.
Backup operator repair committeda985f9d:128MiB byte ranges, rotate authenticated
connections before384MiB payload (installed Paramiko default rekey512MiB),
network read timeouts and persisted inventory/coverage. Whole-file hashes still
required; partial files preserved; no credential on disk; no scientific caps.
Multirange/reconnect/tampered-payload fixture and compilation PASS. New watcher
session3088 launched;19:00:27+07 first inventory PASS103groups/2010files and
operator_state.json persisted. Existing verified files remain in
D:/ARC2-B1c-R3-backup-20261030; reconciliation/transfer in progress, not complete.
Backup transport repair: provenance/qa/b1c_r3_backup_transport_repair_20261030.json.
Current raw status: provenance/qa/b1c_r3_status_20261030T115834Z.json.
TRECclosed; STOPafterfullDEVreport/finalD1beforeB2.

Latest30Oct16:04:45+07: R3 FULL RUNNING again,286/358 new rankings complete
(96/120 groups). New NanoNQ E5 seed29 converter is at selection step10250,
finite gradients/parameters, no worker failures. Same campaign/controller PIDs
2777/2997 resumed16:02:40+07. Deployment61f73171 clean; lockf567a4b6 unchanged.

Output-only relocation VERIFIED:1,741 files /32,917,276,618bytes copied with
SHA256/filemode/mtime verification to
/home/jovyan/arc2_b1c_r3_outputs_20261030/b1c_r3_full_mini_r3b_20261030t0347.
Original logical full-run path is now its symlink. Existing NFS output tree
retained under /network-volume/arc2_recovery_20261030/
preserved_before_output_relocation_20261030/. All immutable source device,
inode,size,mtime stamps unchanged; Git/config/runtime/restored/upstream stayed
in place. GPU worker14216 finished naturally before copying; copy/verification
16:01:05-16:02:40+07. Controller pause15:54:45-16:02:40+07 is recorded in wall
elapsed; no isolated cost/traffic/SLO claim. No rerun or numerical alteration.
Output volume now has~610.4GB free (568.5GiB).

Local raw-backup watcher is active, incremental to
D:/ARC2-B1c-R3-backup-20261030; restarted after adding exact relocated-output
allowance and verified-existing-file skip. It reported325 files /4.20GB in its
current verified coverage at16:04:16+07; this is PARTIAL, not complete backup.
Keep laptop awake/connected for that copy; remote scientific campaign itself
runs detached and is independent of laptop SSH.24 converter fits remain,
roughly7.5-8h at recent~19min/fit plus sealing/scoring, subject to shared load.
No current quality scoring yet; all358 must seal first. TREC stays closed.
Proofs: provenance/qa/b1c_r3_storage_relocation_proof_20261030.tar.gz and
provenance/qa/b1c_r3_status_20261030T090445Z.json. STOP after report/final D1.

Latest30Oct15:55+07: campaign retained283/358 rankings (95/120 completed groups).
Current NanoNQ E5 seed17 converter is allowed to finish normally. Operator18614
has paused only controllers2777/2997 (SIGSTOP), awaiting that worker's natural
exit before the output-only storage transfer. Actual NFS free~8GB cannot fit
remaining~25GB+ checkpoints; /home/jovyan XFS has~599GB free. Preoperation
procedure/source committed6d6cbe9; same-family ARIS operator review and Linux
opaque copy/symlink fixture PASS. No numerical/code/lock/input changes or new
scientific run. Full raw output will be copied/hash/mode/mtime verified, old
NFS raw tree preserved, only its output-directory alias switched, same PIDs
resumed. Whole-owned-root relocation was rejected because cached source
inode checks must stay intact. Source/Git/env/restored/upstream remain on NFS.
Receipt: provenance/qa/b1c_r3_output_storage_procedure_20261030.json.
Local incremental raw backup operator running to
D:/ARC2-B1c-R3-backup-20261030 while laptop awake/connected; prior first pass
already copied~2.24GB/290files, two interrupted .part files preserved.
No claim that all raw data is locally backed up until coverage verification.
Current quality scoring still waits for all358-ranking seal; TREC closed.

Latest30Oct10:48:26+07: R3 FULL RUNNING on Mini .201, deployment61f73171,
pre-run authorityd8233eed, lockf567a4b6. Matching smoke PASS56.043762s;
SimpleLinear synthetic PASS13.584341s, converter synthetic PASS31.713179s.
All630restored sources/2,086,042,311bytes verified; all120 real paid-target slice
hashes PASS before any full fit. Both saved FiQA seed17 galleries passed strict
historical50% parity; their4 prospective25/75rankings complete. First fresh
FiQA MiniLM seed17 converter running,4/358 endpoints observed; no current
quality scoring or TREC access. Current scientificroot:
/network-volume/arc2_recovery_20261030/code_61f7317_b1c_r3
results/b1c_r3_full_mini_r3b_20261030t0347
results/b1c_r3_schedule_mini_r3b_20261030t0347
CampaignPID2777; serial smoke/full/separateDEVscore, then STOPforreport/finalD1.
No artificial elapsed/RAM/VRAM caps; no other jobs/priority modified.

First R3 smoke03:40UTC failed before SimpleLinear fitting: missing yaml.
OriginalFAILED_PRESERVED retained. Operator-only repair restored exact historical
PyYAML6.0.3,pydantic-settings2.16.1,python-dotenv1.2.4,POT0.9.7.post1 with
--no-deps; all8 core GPUversions/defaults/APIimport reverified. Repair receipt
committed78dc7f5 before distinct fresh03:46:33UTC smoke. Same scientific
source/deployment/lock and numerical settings; no discarded quality result.
Complete failed raw smoke and repair bundle downloaded and remote/local SHA
matched; receipt/sourceaudit in provenance/qa/b1c_r3*. Current snapshot:
provenance/qa/b1c_r3_status_20261030T034826Z.json.

Recovery preparation30Oct10:34+07: user reports no other originals/uploads.
Exact original565-source recovery is therefore unavailable; do not claim the
original320/R2 campaign complete. Prospective R3 recovers the same736-cell DEV
matrix via378 retained +358 new rankings,118 fresh baseline fits and2 verified
saved-fit groups. The38 displaced historical cells remain untouched evidence.
Protocol: protocols/B1C_R3_FILESYSTEM_RECOVERY_20261030.md; distinct R3 lock and
registries must commit before matching smoke/fits. Algorithm/data/stats unchanged.

Operator-only recovery now restored/hash-verified115 cloud files from11 Main
archives; both pinned numerical runtimes installed/metadata-verified; complete
official upstream Git revision cloned. 515 local exact-byte files (including
opaque historical DEV-label transport) are uploading; no labels parsed, no new
scientific smoke/fit/ranking/scoring yet. Target is persistent
/network-volume/arc2_recovery_20261030, not the missing original /root tree.
All120 paid-target slice hashes must pass before any full fit. An ARIS review
caught Windows path separators in a prospective registry; corrected before
commit or execution, eight finite tests PASS. TREC remains closed.

Earlier cloud inventory assessment: completion file and BOTH inventories match
their original hashes; public Main78/105 payloads, Mini0/72 payloads. Available
source bytes and local matches enable the narrower R3 acquisition, not complete
historical server restoration. See provenance/qa/cloud_backup_20261030/.

Incident30Oct09:47-09:49+07: .201 SSH reachable, same hostname, but /root
contains only image/config defaults. Both project/runtime roots absent, no
B1c process or tmux session, GPU25MiB/20096MiB/no compute processes. PID1
elapsed13651s at09:49 (~3h47m) is consistent with container recreation;
physical host reset/cause not established. /home/jovyan empty; bounded search
of normal roots and /network-volume found no actual ARC2/B1c project (only
unrelated Git-object filename substrings). .225 TCP port52194 still times out.
No scientific recovery, scoring or write to the missing original roots.

Local previous backup path no longer exists; user confirmed it was uploaded
to cloud and supplied Drive folder1lkDcW4UsNumOy78ntyaPMsJTrhj-ghXt. Local
28Oct backup completion receipt proves the original backup completed then,
not current cloud integrity or inclusion of later B1c runs. Inspect cloud
inventory/archive hashes before recovery. Earlier local M/P/G/scored main
results remain available; new B1c raw artifacts are not yet recovered. Last
observed242/320 is historical generation, not a currently verified reuse set.
Earlier RUNNING notes below remain timestamped evidence, superseded here.

Explicit .225 retry29Oct20:13+07: three TCP attempts to103.73.232.225:52194
each timed out after~12s, before SSH authentication. Parallel control to
.201:62161 connected in0.375s and returned its OpenSSH banner. This points
to unreachability of the configured .225 endpoint, rather than a general
loss of SSH connectivity from the laptop. CPU/GPU load on .225 remains unknown;
no login or scientific job there. Receipt:
provenance/qa/b1c_225_retry_20261029T131312Z.json.

User-requested .225 recheck29Oct: SSH to103.73.232.225:52194 again timed
out at TCP connect before authentication. Local ~/.ssh/config still points
to that same host/port. CPU/GPU load cannot be inspected; no new job launched
there. Do not infer server reset/deletion from timeout. User-provided rental
schedule last listed MAIN through28Oct; current allocation/connection details
would need external confirmation. Receipt:provenance/qa/b1c_main_recheck_20261029.json.

CPU use measured29Oct19:34+07 over5.102s: shared container quota4 CPU cores;
aggregate~4.012 core-equivalents during sample. Owned baseline worker216388
used0.0686 core-equivalents (~6.9% of one core); other llama220913 used3.8105.
Quota is shared across jobs, not an exclusive4-core assignment to ARC2.
No scheduling or scientific changes. Receipt:
provenance/qa/b1c_cpu_usage_20261029T123437Z.json.

CPU increase requested29Oct19:24-19:26+07. User authorized increasing owned
worker CPU allocation/priority. Inspection: owned worker nice0 (normal),
affinity already all128 allowed logical CPUs,18 threads; CAP_SYS_NICE,
CAP_SYS_ADMIN and CAP_SYS_RESOURCE absent, RLIMIT_NICE=(0,0). Container
cpu.max4 cores and cgroup filesystem read-only. A disposable child attempting
nice-5 received PermissionError errno13; live worker was not modified.
No successful CPU increase is claimed. Additional CPU reservation/own cgroup
or container must be configured by the host administrator. Current experiment
continues unchanged; no other job, source, algorithm or baseline budget changed.
Admin request: reserve2-4 CPU cores exclusively for ARC2 in its own CPU cgroup/
container rather than sharing the existing4-core quota with other projects.
Receipts:provenance/qa/b1c_cpu_authority_20261029.json and
provenance/qa/b1c_cpu_priority_probe_20261029.json.

Acceleration feasibility29Oct19:18+07: Mini still RUNNING242/320, fifth refit
42500/49750. Main80GB .225:52194 SSH timed out; separate5s TCP probes to
both .225 and40GB .240:58319 timed out. This establishes current endpoint
unreachability, not deletion or a known server reset. Mini cpu.max remains
400000/100000 and cgroup2 mount is read-only, so the agent cannot raise this
quota from inside the container. Practical remedy: administrator-provided
CPU capacity/isolation, or a reachable less-contended endpoint. Preserve all
completed work; validate any relocation under a committed runtime amendment
and matching smoke. No source/method/step count/priority/other job changed;
current worker remains running. Receipt:
provenance/qa/b1c_acceleration_feasibility_20261029.json.

Live check29Oct18:45+07:242/320 rankings,4/30 converter fits complete.
Fifth NanoNQ MiniLM/seed67 fresh refit33750/49750 (~68%), up from2500 at
16:24. Full/schedule/worker216388 active, failures empty, finite losses/
gradients/parameters. No scoring/current label access; no run changes.
Shared MIG11166/20096MiB; other llama still active (~356% CPU in ps).
Receipt:provenance/qa/b1c_recovery_r2_status_20261029T114551Z.json.

Live check29Oct16:24+07:242/320 rankings complete,78 remaining;4/30 converter
fits PASS. Fifth NanoNQ MiniLM/seed67 selection complete1988.60s, selected
49750; fresh refit2500/49750 (~5%), elapsed785.68s. Fourth fit completed
13370.12s wall (selection11309.66s/refit1970.06s). Speeds vary sharply with
shared load; current other llama220913 active again (~361% CPU in ps).
Full/schedule/worker216388 RUNNING, failures empty, finite losses/gradients/
parameters; no scoring/current label access. Shared MIG18099/20096MiB.
No run changes. Receipt:
provenance/qa/b1c_recovery_r2_status_20261029T092452Z.json.

Live check29Oct13:49+07:239/320 rankings complete,81 remaining;3/30 converter
fits PASS. Fourth NanoNQ MiniLM/seed53 selection15000/50000 (30%), elapsed
6656.7s, refit pending. Third completed31754.13s wall with selected48250.
Full/schedule/worker193974 RUNNING, failures empty, finite losses/gradients/
parameters; no scoring/current label access. Fresh5.097s CPU sample: other
llama3.565 cores, owned worker0.0647, container quota4 cores. Severe shared
CPU contention persists. Shared MIG18005/20096MiB. No run changes. Receipt:
provenance/qa/b1c_recovery_r2_status_20261029T064944Z.json.

Measured slowdown29Oct11:12+07,10.0936s sample: container cpu.max400000/100000
(4 core-equivalents), aggregate~4.016 cores, throttle102/102 periods. Other
llama114773 consumed3.637 cores; owned converter148640 only0.0575 cores.
Owned main thread ran0.453s and waited8.156s in CPU runqueue (~80.8% elapsed).
This directly confirms severe CPU scheduling contention in the sample; it is
not a full-run bottleneck decomposition or isolated GPU utilization claim.
Heavy baseline policy also executes50k selection plus selected-length fresh
refit for each of30 fits. Runtime remedy is uncontended/more CPU allocation,
not a hidden change to epochs/batch/method. No process/priority/guard modified.
Receipt:provenance/qa/b1c_recovery_r2_contention_20261029T041246Z.json.

Live check29Oct11:10+07:236/320 rankings complete,84 remaining;2/30 converter
fits PASS. Third NanoNQ MiniLM/seed41 selection complete, selected48250;
fresh refit42000/48250 (~87%), elapsed16645.8s at last checkpoint. Full/
schedule/worker148640 active, failures empty; losses/gradients/parameters
finite. No scoring/current label access. Other llama job still active (~362%
CPU in ps), shared MIG17861/20096MiB. No run changes. Receipt:
provenance/qa/b1c_recovery_r2_status_20261029T041057Z.json.

Live check29Oct02:39+07:233/320 rankings complete,87 remaining. First NanoNQ
MiniLM/seed17 converter fit PASS (selection14094.42s,refit1960.15s), its three
budget rankings generated. Second converter NanoNQ MiniLM/seed29 selection
complete; fresh refit41750/49750 (~84%), worker112782 active. One of30
converter fits complete. Full/schedule RUNNING, failures empty; finite
losses/gradients/parameters and no scoring/label access. Other llama job
active again (~351% CPU in ps); shared MIG11286/20096MiB. No run changes.
Receipt:provenance/qa/b1c_recovery_r2_status_20261029T0239plus07.json
(raw remote observation UTC28Oct19:39, local29Oct02:39).

Live check28Oct20:01+07: first converter selection50000/50000 complete,
14094.4155s, locked paired-vector selection chose49500 refit updates. Fresh
refit5250/49500 at207.35s, latest250 updates~10.35s; currently much faster
than previous shared-load selection checkpoints, not an isolated speed claim
or guaranteed ETA. Other llama process no longer appears in process/GPU list;
shared MIG7896/20096MiB. Worker90351/full/schedule active, failures empty,
finite losses/gradients/parameters. Rankings still230/320 until fit finishes;
no scoring/label access and no run changes. Receipt:
provenance/qa/b1c_recovery_r2_status_20261028T130110Z.json.

Live check28Oct19:36+07: first converter selection43500/50000 (87%), up
from23750 at17:36; elapsed12797.9s. First fit still active, refit not started;
rankings remain230/320 until fitting and all three budget rankings finish.
Full/schedule RUNNING, failures empty, losses/gradients/parameters finite,
no current scoring or label access. Shared MIG19043/20096MiB and other llama
job remain active. No run changes. Receipt:
provenance/qa/b1c_recovery_r2_status_20261028T123618Z.json.

Live check28Oct17:36+07: still230/320 rankings because first converter fit
has not finished. It is progressing: selection23750/50000 (47.5%), up from
4500 at16:27; elapsed5646s at its latest checkpoint. Refit follows the locked
selected-iteration policy after selection. Full/schedule RUNNING, worker90351
alive, finite losses/gradients/parameters, no new failures/OOM and no scoring.
Shared MIG18943/20096MiB; other llama job remains active. No run changes.
Receipt:provenance/qa/b1c_recovery_r2_status_20261028T103654Z.json.

Live check28Oct16:27+07:230/320 rankings generated (95 imported+135 new),
90 remaining, all belonging to30 Nano converter fits. All50 FiQA reuse and
180 Nano LA2M/SimpleLinear endpoints complete. First converter active:
NanoNQ MiniLM/seed17 selection4500/50000, elapsed1447.30s at that checkpoint,
finite gradients/parameters/loss. Full/schedule RUNNING, failures empty;
no scoring or current label opening. Other llama job still active (~360% CPU
in ps), shared MIG18697/20096MiB; worker own reserved~772MiB. No run changes.
72% ranking completion is not72% elapsed work: the long30-converter phase
has only just begun. Earlier smoke-only6-12h projections are not reliable
under this observed load; no full-worker ETA established yet.
Receipt:provenance/qa/b1c_recovery_r2_status_20261028T0927Z.json.

Live check28Oct14:30+07:146/320 generated (95 imported+51 newly generated
since recovery),174 remaining. NanoNQ LA2M/SimpleLinear complete; current
NanoHotpotQA E5/seed29 LA2M group active. Full/schedule RUNNING, failures
empty; previous SimpleLinear worker exited0/PASS, no new OOM. GPU shared
17296/20096MiB occupied by other jobs at observation; own current stage CPU.
Scoring not started and labels/TREC unopened. No run changes.
Receipt:provenance/qa/b1c_recovery_r2_status_20261028T073103Z.json.

Latest28Oct13:51+07: matching committed smoke B1C_SMOKE_PASS,436.567892s,
all three methods and recovery fixtures passed. Full metadata RUNNING/no
failures, verifying/importing complete prefix before remaining225 endpoints.
This supersedes the historical smoke-running checkpoints below. Full launch
receipt:provenance/qa/b1c_recovery_r2_full_started_20261028.json.

R2 actual launch13:43:29+07 from committed protocol989e679 and distinct
scientific-source deployment67d7b16c28f7205d3873f6fe09df62eab722fdd4.
All38 locked sources verified. Manifeste9e06db2... pins385 artifacts/731400870
bytes across45 complete groups,95 ranks,15 Nano fits and30 FiQA parity checks.
Matching smoke13:49+07 RUNNING/no failures; LA2M and SimpleLinear PASS,
converter selection500/refit500 steps complete, finite losses/gradients,
final artifact serialization still underway. Full has not started at this
observation; campaign automatically proceeds after smoke PASS, then separate
scoring only after320 seal. No local laptop dependency.

Current R2 root:/root/arc2_global_paper_20261025/code_67d7b16_b1c_r2.
Tmux:arc2_b1c_recovery_r2_retry1_20261028. Results schedule/smoke/full use
mini_r2_20261028. Operator prep:b1c_prepare_mini_r2_retry1_20261028.
Initial R2 operator launch failed before scientific-directory creation because
clean source snapshot lacked the empty results parent; original logs retained.
Created that parent and relaunched identical commit/arguments in distinct
operator retry directory; no scientific source or output overwritten.
Local receipts:b1c_recovery_r2_source_snapshot_20261028.json and
b1c_recovery_r2_live_20261028.json in provenance/qa. ARIS trace remains local
.aris/traces/research-review/2026-10-28_b1c_recovery/ (same-family/provisional).

User authorized continuation28Oct. R2 protocol preserves original failure;
same Mini now has available GPU memory after another job ended independently.
Qrel-free source inventory verifies45 complete groups/95 rankings/30 parity
checks; recovery imports their bytes and executes225 endpoints/75 Nano fits.
Original lock and numerical/scoring sources unchanged. Added complete-group
recovery fixtures PASS: byte identity, duplicate/partial/identity/order/mutation
rejection. ARIS review round3 found no remaining STOP-level implementation
bug (same-family/provisional); its original-artifact verification finding was
fixed before commit. R2 full remains gated on finalized committed manifest/lock
and matching committed smoke. No restart or scoring has occurred at this note.
Protocol:protocols/B1C_R2_OOM_RECOVERY_20261028.md.

Latest check28Oct13:15+07: campaign stopped12:55:41+07 at95/320 generated
rankings. NanoNQ E5/seed41 SimpleLinear worker exited1 with CUDA out-of-memory
while moving its model to CUDA, before training; not SIGKILL or CPU OOM
(cgroup oom/oom_kill remain0). Gate/full metadata FAILED_PRESERVED; no owned
B1c campaign/training process remains. Other jobs still occupy19998/20096MiB
on the Mini. All completed artifacts and failure logs retained; scorer has
not run and labels/TREC remain closed.225 new rankings remain, plus separate
scoring/report/final D1. Recovery requires preserving this attempt and verifying
completed artifacts under a committed recovery protocol; no automatic restart
or change to other jobs. Receipt:provenance/qa/b1c_status_20261028T061507Z.json.

Latest live check28Oct12:53+07:89/320 new rankings, up39 since12:37;
50 FiQA reuse plus39 Nano rankings. Current NanoNQ E5/seed29 SimpleLinear
GPU worker alive. Metadata RUNNING/failures empty; no scoring yet. Mini MIG
total19834/20096MiB includes other jobs; completed SimpleLinear workers reserve
about144MiB themselves and are succeeding despite shared load. No OOM observed.
Receipt:provenance/qa/b1c_status_20261028T055311Z.json. No run changes.

Live check28Oct12:37+07:50/320 new rankings generated; all30 FiQA
saved-fit parity receipts present. FiQA reuse is complete and the first
NanoNQ MiniLM/seed17 LA2M group has started. Metadata RUNNING, failures empty;
scoring has not started and qrels/TREC remain unopened by this campaign.
Other jobs occupy19498/20096MiB of the Mini MIG memory, so later GPU workers
face resource contention; no isolated-throughput or reliable finish-time claim.
No process, method or resource policy changed. Snapshot:
provenance/qa/b1c_status_20261028T0538Z.json. The416 existing cells remain the
scored main-matrix count; the50 new cells are generated but not yet scored.

Current authorized scope: protocol/commit/cache verification/smoke, complete320
missing DEV rankings, separate scorer/full six-method report, final D1 then
STOP for user before B2. Source registry120groups/320missing and existing
registry416cells reconcile736 main cells. Original protocol/source committed
585b8b8; clean scientific-source deployment1df7c3e retained its MAIN smoke PASS
(211.188s). MAIN's own full queue was stopped BEFORE any full run/label opening.
Its47-file MINI-to-MAIN operator transfer was superseded; partial copies/logs
remain and no source data was deleted. MAIN has other GPU jobs and high load.

R1 amendment74c6a75 moves full execution to MINI .201,20GB MIG. Clean source
snapshot19f3f0e has35 verified scientific sources and unchanged numerical
policies/registries/statistics; only endpoint/amendment fields changed in lock.
MINI matching smoke PASS at41.057s; all three methods and B1c matrix/tamper,
parser/ties/exclusion/failure fixtures passed. Source snapshot and smoke receipts
are in provenance/qa/b1c_mini_* and results/b1c_smoke_mini_r1_review_20261028.
MINI lacked the auxiliary Parquet reader: installed only pyarrow25.0.1 (the
exact MAIN version) using--no-deps. Synthetic reader PASS confirms unchanged
CPU NumPy2.4.6/SciPy1.17.1/sklearn1.5.1 and implicit positive-pair parsing.
No real qrel was opened or hashed by these readiness checks; FiQA label path
was checked for existence/size only. TREC remains closed.

Source transfer COMPLETE:453 required qrel-free files,1947593157bytes, MAIN→MINI,
both exit codes0 and exact manifest SHA256 verified. Receipt
provenance/qa/b1c_main_to_mini_transfer_20261028.json; elapsed3637.76s.
Local exec session43308 exited successfully; no laptop/network dependency remains.
The server gate queue is already running in tmux
`arc2_b1c_full_gate_mini_20261028`; source
`/root/arc2_global_paper_20261025/b1c_prepare_mini_20261028/queue_after_inputs_r1.py`.
Verified453-file transport and all565 historical inputs+2committed registries
PASS. The queue launched the already committed full campaign28Oct11:27+07,
PID62886/worker62887. At11:28 observation:2/320rankings generated, second FiQA
saved-fit group active, metadata RUNNING with no failures or qrel access.
Its only route is50FiQA→180Nano→90converter→separate736-cell DEV scoring→STOP
for report/final D1; no B2 or systems launch. Full is now running independently
inside server tmux. Launch observation:provenance/qa/b1c_full_launch_observation_20261028.json.

Current deployment: `/root/arc2_global_paper_20261025/code_19f3f0e_b1c` on MINI.
Expected full `results/b1c_full_mini_r1_20261028`; schedule
`results/b1c_schedule_mini_r1_20261028`; scorer `full/scoring/summary.json`.
Gate status: `b1c_prepare_mini_20261028/after_gate_status.json`; transport marker:
`b1c_prepare_mini_20261028/transfer_r1_received.json`. If transfer fails, retain
partials/attempt and resume through a new operator transport manifest; never
bypass the final input hashes. Scientific recovery requires preserving its run.
Smoke projection for30converter workers is6.19h selection-only to11.61h with
maximum refit, before other work; this is unvalidated1024-anchor extrapolation,
not an ETA or cap. Update forecast from the first real worker. No artificial caps.

Protocols: B1C_MAIN_MATRIX_COMPLETION_20261028.md and
B1C_R1_H100_MINI_EXECUTION_20261028.md. ARIS implementation review is same-family/
provisional and found/fixed artifact-seal verification and smoke coverage;
trace .aris/traces/research-review/2026-10-28_b1c/ remains local, not committed.

**File-review clarification: B1c is still 416/736. Next is completion of320
planned DEV rankings, then final D1 refresh, then conditional B2.** The existing
ARIS/D1 is a scoped provisional recommendation, not full-breadth admission.
No scientific job, calibration or TREC scoring was started in the file review.

All124 rankings are sealed and scored:120 partial cells plus4 full references.
R5 reused51 artifacts and generated73;10/10 all-paid converter fits passed.
Original scorer failed before parse on duplicate exclusive started.json writing;
its FAILED_PRESERVED metadata and original scoring/ remain intact. Recovery
commit4062d96 passed committed qrel-free smoke, then scored unchanged generation
7530c8e at10:20:39+07. The numerical metric/bootstrap source and statistical
family are unchanged. All124 ranks,28means,32contrasts and96intervals passed
local computational verification (largest difference2.22e-16); no local qrel
files opened and TREC remains closed. No method/threshold/label-based selection.

MiniLM all-paid ARC2 nDCG0.367146 exceeds four baselines with positive family
intervals; ridge0.367263 comparison unresolved. E5 all-paid ARC2 nDCG0.291867
trails Procrustes0.336202/LA2M0.329341 with negative family intervals. Both regimes,
all baselines/references, every contrast and negative remain in the full report.
This is inspected DEV, not an independent/cost/SLO result. Current D1 is below.

Latest results: results/b1g_r1_review_20261027/SUMMARY.md and REPORT.md. B1-G
used existing450cases/210galleries, two CPU shards(main137/377;mini73/73), source
515b3d10 committed before matching smokes/full. Separate DEV scoring completed;
all450historical per-query arrays match exactly. Local R2 QA recomputed all
450ranking/paired diagnostics and90five-seed conditions,3795503numeric values,
largest discrepancy0. Figure PDF/PNG/SVG and full CSVs passed QA. Original local
verifier path-comparison failure is preserved; only new verifier path handling
changed. QA: provenance/qa/b1g_completed_verification_r2_20261027.json.

ARIS CLAIMS_FROM_RESULTS.md: partial overall, same-family provisional; fixed
supervision mechanism effect yes, general fair-allpaid/cost/SLO superiority no,
descriptive mixed-transition limitation yes. D1 narrow GO-C1 for frozen quality
confirmation only; no systems admission, no independent run launched. E5allpaid
ARC2pure.314908 falls to mixed.291867; paid top10 share6.472% despite50%population.
Score bias is a hypothesis, not causal proof. Ridge unresolved is not equivalence.
STOP before any next scientific phase. TREC/breadth/systems/formal audit unstarted.

| ID | Block | Deliverable | State | Evidence / next action |
|---|---|---|---|---|
| B0a | package | global-only standalone API | PASS - exact parity | src/arc2_global |
| B0b | package | 64 selected FiQA rankings, metrics, seals | PASS - hashes/metrics | results/fiqa_development |
| B0c | package | exact parity and hash/arithmetic checks | PASS | provenance/qa |
| B0d | paper | reused template; measured report/scaffold | PASS - 5 pages | manuscript; REPORT.md |
| B1a | DEV | protocol/data/model/environment lock + smoke; random paid-set rule | PASS - H100 + local verification | results/b1a_r1_20261025/SUMMARY.md; first failure retained |
| B1b | DEV | genuine LA2M, official SimpleLinear, standard affine ridge | PASS - synthetic H100 + local verification | results/b1b_20261026/SUMMARY.md; adapters ready, no benchmark result |
| B1-M | DEV MUST | 0/1/2 tangent; lambda=1/10/100; ridge control | COMPLETE - scored/local verification | results/b1mp0_r1_review_20261026/SUMMARY.md; fixed two/lambda10 preserved |
| B1-P0 | DEV MUST | identified all-paid solver backend + parity/drift checks | PASS - numerical readiness | 31 synthetic +120 real budget checks; exact ordered top100 identity; no all-paid fit |
| B1-P | DEV MUST | FiQA50%, all paid pairs, six methods, two pairs/five seeds | COMPLETE - SCORED / LOCAL QA PASS |124/124 sealed/scored;10/10 converter fits PASS; all means/32 contrasts/96 CIs verified; original scorer failure preserved; STOP |
| B1-G | DEV MUST | proxy/true score and ranking diagnostics | COMPLETE - SCORED / LOCAL + FIGURE QA PASS |210galleries/450cases/90conditions; zero historical metric and local arithmetic discrepancy; source515b3d10; no newfit |
| B1c | DEV | four development collections, fixed six-system matrix | RUNNING ON MINI; transfer/prefight PASS | R1 protocol74c6a75/deployment19f3f0e; launched11:27+07;2/320 new ranks observed11:28, no scoring yet; auto50/180/90 then separate scorer |
| D1 | decision | GO-C1 / CONFIRMATION-ONLY / NO-GO-FOR-SYSTEMS | SCOPED PROVISIONAL GO-C1 / FINAL REFRESH AFTER B1c | existing ARIS supports fixed-supervision quality question only; systems not admitted; retain old review; full breadth informs final decision |
| B2a | independent | separate protocol, 30 contrasts, sealed TREC rankings/endpoints | CONDITIONAL / NOT STARTED | complete B1c and refresh D1 first; fixed-anchor quality confirmation, not independent one-vs-two-step attribution |
| B2b | independent | one TREC score; CI interpretation fixed before labels | CONDITIONAL / NOT STARTED | crossing zero is unresolved, not equivalence |
| D2 | decision | C2 hypothesis and quality/cost target justify case study | NOT EVALUATED | after B2 interpretation; no automatic campaign |
| B3a | systems | physical runner, event ledger, failures, actual-method smoke | CONDITIONAL / NOT STARTED | D2 first; no cache billed as fresh encoding |
| B3b | systems | 100K, four strategies, two pairs/three paired trials | CONDITIONAL / NOT STARTED | 24 deployments /36h nominal observation if admitted |
| B4a | traffic | held-out ORCAS random/frequency/coverage replay | CONDITIONAL / NOT STARTED | agreement is proxy; judged relevance if applicable |
| P1 | writing | evidence-selected route, figures and complete paper | NOT STARTED | optional systems route does not block mapper paper |
| P2 | audit | ARIS result-to-claim and fresh paper/raw audit | PARTIAL - B1-G ARIS COMPLETE / PAPER AUDIT NOT STARTED | current semantic review is same-family provisional; no formal paper-claim audit |
| P3 | release | build/render/provenance/reproduction freeze | NOT STARTED | finite completion; no automatic extra dataset |

Maximum if every stage is admitted: 920 main rankings (900 partial +20 refs),
360 extra DEV ablations and 60 all-paid DEV rankings = 1,340. The 64 imported
rankings may be reused on verified identity; at most 1,276 additional cells.
Before TREC: 1,156 DEV cells, of which 64 imported; TREC adds 184 only if admitted.
Ranking counts are not numbers of learned fits or newly physically encoded docs.

Completed unique planned quality cells:836 =64 original imports +772 newly scored.
B1-M contributed692 new unique cells. B1-P adds80:60 all-paid plus20 fixed
LA2M/SimpleLinear rows; its other44 were already scored. Artifact reuse51 =44
previously scored +7 prior successful R1 rankings newly scored here. R5's73 new
rankings plus7 prior R1 rankings produce these80 new unique quality cells.
Maximum remaining 504 =320 DEV main +184 conditional TREC. No remaining B1-P rows.
B1-G is diagnostics, not an extra dataset; D1 is now recorded above. No compute-hour
percentage follows from these cell counts. All original failed attempts remain
preserved; successful B1-M binary scoring and B1-P recovery have separate receipts.

## Next work after careful file review

### Storage check 28 October 2026, 08:32 +07

Both SSH hosts remain reachable. This was a file/stat inventory only, not a
scientific run, label read or complete backup verification. Current project
directory `/root/arc2_global_paper_20261025` occupies approximately12.74GB on
MAIN .225 and34.23GB on MINI .201 (decimal disk-usage bytes; duplicates included).
Local compact results retain rankings/IDs/per-query metrics/summaries/logs and
verified B1-G portable diagnostics, but large proxy arrays, fitted coefficients
and neural checkpoints are not all backed up locally. B1-P's recorded25.54GB
large raw inventory remains a priority to preserve before a destructive reset.
The saved FiQA fitted galleries required for proposed B1c reuse also need backup.
Older roots additionally occupy30.70GB MAIN/0.78GB MINI under
`/root/arc2_p3h_20261020`; MAIN also has a217.61GB
`/root/p8-a-recompute-20261022` tree whose backup completeness was not audited.
Do not interpret these aggregate sizes as unique data or a required download total.
Downloaded inventories: `provenance/qa/server_storage_main_20261028.json` and
`provenance/qa/server_storage_mini_20261028.json`. They contain paths/sizes,
not file-hash verification or a backup completion receipt. No bulk backup or
remote deletion was performed. Scientific STOP and TREC closure are unchanged.

User then authorized backup to D. A resumable two-host opaque archive backup is
COMPLETE in `D:/ARC2-server-backup-20261028` (launch receipt:
`provenance/qa/server_backup_launch_20261028.json`; helper
`tools/backup_server_archives.py`). Scope: both current-project and old
`arc2_p3h_20261020` roots on both hosts,85.18GB apparent regular-file bytes
before compression, including duplicate/hardlinked content. Inventories contain
53707 MAIN and23679 MINI entries. All371 large current-project files in the
earlier inventory still exist with unchanged size; this does not establish
absence of deletion before that earlier inventory. First archive on each host
has passed source/stream/member SHA256 verification. Completion checked28Oct:
both hosts100%, MAIN105/105 and MINI72/72 archives,77386 source entries,
85184835251 source bytes and75990282054 compressed archive bytes. All177
archives passed source/stream/member SHA256 checks during copying. Closure
receipt `provenance/qa/server_backup_completion_20261028.json` confirms every
receipt/archive exists with its expected size, total entries/bytes match both
inventories, no partial or failure files, and final `completion.json` exists.
The backup process has exited. Consult each host's `status.json` and individual
`archives/*.verified.json` plus final `completion.json`. Partial downloads would
be preserved for diagnosis if a later attempt failed;
restarting the helper skips completed verified archives. The217.61GB older
`p8-a-recompute` root is outside this job and remains unverified/unbacked by it;
no reference to it was found in current configs/ops or B1-G source registries.
No server data is removed. No new scientific run/scoring or label analysis.

- Confirmed from actual local indices:416 main DEV identities present,320missing,
  zero conflicting ranking hashes for duplicate identities. Evidence:
  .aris/traces/research-review/2026-10-27_next_steps/dev_matrix_inventory.json.
- B1c missing work:270 Nano rankings (three remaining methods, two pairs, five
  seeds, three budgets),40 FiQA LA2M/SimpleLinear25/75%,10 FiQA converter75%.
  FiQA has30 already-fitted galleries with original50% parity; verify current
  artifact identity before reuse. Nano needs up to 90 method fits if no other
  compatible historical artifacts are found; a fit supplies all three budgets.
- Use a finite execution order: FiQA reuse50, Nano LA2M/SimpleLinear180, Nano
  converter90. Separate protocol/smoke/seals/scorer remain required; no run yet.
  No new collection, hyperparameter sweep or extra required ablation was added.
- Update manuscript evidence from B1-M/P/G while breadth runs; independent
  quality vs external methods remains the planned184-cell/30-contrast B2.
  One-step necessity remains DEV evidence unless a separate prospective choice
  changes that scope before labels; no automatic extension.
- Renderer overwrite defect fixed on temporary copies; preservation/idempotence
  and malformed-marker regression PASS. Live REPORT and raw evidence unchanged.
  Receipt provenance/qa/next_steps_render_regression_20261027.json. README's stale
  B1b checkpoint is corrected; frozen definition-time configs remain untouched.
- Default closure is mapper paper -> claim/citation audit -> build/render/release.
  B3/B4 need a separate later D2. A proxy/native compatibility candidate is
  optional new-method research, not a hidden repair or paper-closure requirement.
  Full explanation is in the single live plan's current-critical-path section;
  ARIS same-family/provisional review trace is .aris/traces/research-review/2026-10-27_next_steps/.

## Current B1-G execution pointers

- Scientific pre-run commit:515b3d10b8c09f1900c5215b5b709b47830f3236. Protocol protocols/B1G_MIXED_GALLERY_DIAGNOSTICS_20261027.md; configs/b1g_lock.json and both source registries. ARIS readiness review ARIS_B1G_READINESS.md is provisional, not a scientific verdict.
- Both hosts use /root/arc2_global_paper_20261025/code_515b3d1_b1g. Successful smokes: results/b1g_smoke_main_r2_20261027 and results/b1g_smoke_mini_r2_20261027. Initial launcher invocations used an output outside the required checkout/results directory and were rejected before scientific execution; logs/receipts retained. Corrected only invocation paths, with identical committed source/lock.
- Full runs launched13:29+07: results/b1g_full_main_r1_20261027 (PID4048961, .225) and results/b1g_full_mini_r1_20261027 (PID47910, .201). Detached jobs; no artificial time/RAM caps. CPU-only, existing saved fits; all historical ranks must match before completion. Scoring waits for BOTH complete qrel-free seals.
- Both full runs completed B1G_FULL_PASS with B1G_DIAGNOSTICS_SEALED: MAIN137galleries/377cases,628.782s; MINI73/73,529.969s. Every reconstructed mixed ordered top100 matches its historical ranking. These are CPU diagnostics on shared hosts, not deployment fitting/physical encoding cost. Portable exports preserve everything except the declared paid-target execution-cache prefix, retained at source; archives are hash-bound. Mini extraction on Windows required extended paths; partial files were byte-checked and the missing files extracted without changing raw data. At13:43 the remaining step was export/import for the common scorer; subsequent scoring/QA completed as recorded below.
- Separate source515b3d10 scorer completed B1G_DEV_SCORED at20:31+07 in results/b1g_score_r1_20261027 on MAIN; wall25.605s, all450historical per-query deltas0. Current DEV label receipt records both preexisting seals. The portable scorer bundle is local results/b1g_r1_review_20261027/scoring. No TREC label access.
- Local R1 verifier failure (relative versus resolved Linux historical-source path) preserved at provenance/qa/b1g_completed_verification_20261027.json. R2 source-only verifier repair kept every hash/rank/numeric tolerance unchanged; successful receipt provenance/qa/b1g_completed_verification_r2_20261027.json. Figures/SUMMARY/CSVs use the verified artifacts; provenance/qa/b1g_figure_visual_verification_20261027.json records PNG/PDF visual checks and SVG parse.
- ARIS trace .aris/traces/result-to-claim/2026-10-27_b1g/; deterministic compact evidence check59verified; no formal integrity audit. Root CLAIMS_FROM_RESULTS.md and findings.md record the verdict. Remote completion receipt provenance/qa/b1g_remote_completion_stop_20261027.json confirms no active owned B1-G process on MAIN. Local raw bundles retain all portable rankings/samples/scores/IDs/contexts/logs; redundant transport archives stay untracked with versioned hash receipts.
- Final checkpoint receipt provenance/qa/b1g_completion_d1_stop_20261027.json binds current report/review/QA hashes and unchanged frozen sources. MINI also has no active owned B1-G process: provenance/qa/b1g_mini_completion_stop_20261027.json; declared paid-target caches remain retained. This completes B1-G and D1; no B2 or systems launch.
- B1-G diagnostics do not increase the836 completed planned benchmark-cell count. Current phase ends after local verification, ARIS interpretation and a bounded D1 recommendation. TREC remains closed.

## Current B1-P execution pointers

- Generation protocol: B1P_ALL_PAID_FIQA_20261026.md and R1-R5 amendments; immutable source7530c8e. Original remote run /root/arc2_global_paper_20261025/code_7530c8e_mini_r5/results/b1p_full_mini_r5_20261026. Its top-level FAILED_PRESERVED status records the first scorer failure, not a missing fit.
- Recovery protocol: protocols/B1P_SCORING_RECOVERY_20261027.md; lock configs/b1p_score_recovery_lock.json; immutable recovery source4062d96. Remote checkout /root/arc2_global_paper_20261025/code_4062d96_score_recovery.
- Successful scoring: original remote run/scoring_recovery_r1_20261027/completed.json = DEV_SCORED. Original scoring/started.json and failure.json remain unchanged; first original parse never began. Prior opaque DEV transport remains recorded.
- Local complete bundle: results/b1p_r5_review_20261027/; SUMMARY.md and scoring/results_summary.md/json; per_query.npy; all124 rankings/IDs/selections/logs; full_manifest.json covers25,539,871,372 original raw bytes remaining on Mini. Local export omits large weights/proxies, not negative outcomes.
- Generation/scoring hash checks and recomputed means/CIs: provenance/qa/b1p_r5_generation_verification_20261027.json and b1p_r5_completed_verification_20261027.json. Verifier tools/verify_b1p_completed.py; report generator tools/render_b1p_report.py.
- STOP confirmed27Oct10:29+07: no owned B1-P training/scoring process; raw metadata/seal unchanged. Receipt provenance/qa/b1p_completion_stop_receipt_20261027.json. No automatic next item.
- Keep older R1/R2/R4 guard failures, R3b intentional relocation stop,20k derivative/25k original checkpoints and discarded timing segments. Never modify other jobs/guard or claim isolated physical deployment costs from these shared/cache runs.

## Historical CPU-load observation26Oct22:42+07 (before completion)

Fresh10.0855s sample: cgroup CPU quota400000/100000 =4 core-equivalents;
usage delta40.3303 CPU-seconds, with throttling in101/101 periods. llama-server
PID2700 used3.839 cores; owned worker32678 used0.135 cores. Worker main thread
ran1.1816s and waited7.9845s in CPU runqueue (~79.2% of sample). This is direct
sample evidence of severe CPU contention, not a full-run performance breakdown.
Memory limit60GiB; memory.events max/oom/oom_kill all0. No artificial run-time,
RAM or VRAM cap. Configured CPU threads4 and deterministic float32/no-TF32,
batch64 remain locked; those are reproducibility/numerical settings. The source
also samples on CPU and checks GPU loss/gradient finiteness each update, causing
CPU/GPU synchronization; its separate overhead has not been profiled.

First converter selection50k complete; current refit14,250/48,750, recent0.1423s
per update. One of ten all-paid converter fits started; nine remain. At roughly
0.15s/update, nine50k selections alone are18.75h; similarly long fresh refits
can bring that near37.5h, before neighbors, checkpoints, mapping, other methods
and scoring. Thus20-40h for remaining converter work is an extrapolation under
similar load, not a reserved/guaranteed finish window or cap. Whole B1-P can
extend1-2days or more; earlier few-hour expectations do not describe this Mini
schedule. Do not interpret51/124 rankings as wall-clock completion fraction.
No workload, priority, guard, method, iteration count or batch change made.
Primary operational remedy is additional/uncontended CPU allocation, or a
full-H100 allocation where the shared guard permits this worker. Keep other
jobs and guard untouched. Evidence: provenance/qa/b1p_r5_performance_20261026T154239Z.json.

## Performance observation17:42+07 (no run change)

Measured cgroup quota4 CPU cores. First10s sample used3.985 core-equivalents,
with throttling in101/101 periods; worker total CPU about0.104 cores. Separate
10.01s scheduler sample: worker main thread ran0.864s and waited8.269s in the
CPU runqueue (~82.6% of elapsed); llama-server PID2700 used3.473 cores. This
confirms substantial CPU scheduling contention in that sample. GPU utilization
is unavailable through this MIG container's nvidia-smi permissions;0.867GiB
is worker CUDA reserved memory, not utilization. Worker RSS about1.98GiB.
Recent training speed~0.200s/update; selection18750/50000 at17:39. No quality
score or isolated-speed claim follows. No workload, priority, code or cap was
changed; other jobs remain untouched. Sources: provenance/qa/
b1p_mini_perf_observation_20261026T103945Z.json and
b1p_mini_scheduler_observation_20261026T104156Z.json.

Code also uses CPU-side sampling and CUDA-dependent Python health checks each
update; these impose synchronization overhead, not yet separately profiled.
PyTorch documentation: https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html#avoid-unnecessary-cpu-gpu-synchronization .

## Historical R4 preparation (superseded by observed guard kill above)

User requested transfer for throughput. Main guard expired17:00+07; quota16
CPU cores, CUDA full132 multiprocessors. A frozen20,000-step selection snapshot
has been copied and verified; explicit full-device derivative preserves all
state/tensor bytes except CUDA device identity. At that historical preparation
point Mini was to remain running until target smoke and zero-update checks passed. Scientific source
converter unchanged; sole resume cell is MiniLM/seed17/allpaid converter.
See B1P_R4_RETURN_TO_FULL_H100_20261026.md and ARIS_B1P_R4_READINESS.md.
This is mixed-device continuation; prior/discarded/resumed timings stay separate.
No R4 scientific smoke/full had started before that protocol commit. This historical preparation is not current execution status.
