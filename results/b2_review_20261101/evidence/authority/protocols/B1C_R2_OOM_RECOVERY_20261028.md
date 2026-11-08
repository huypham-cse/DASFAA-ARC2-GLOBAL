# B1c R2: recover the preserved Mini CUDA allocation failure

28 October 2026, Asia/Saigon. Commit this protocol, recovery lock, completed-work
manifest and recovery implementation before the matching smoke or full run.
The user authorized continuation after the recorded CUDA OOM. This amendment
changes recovery orchestration only; B1C_MAIN_MATRIX_COMPLETION_20261028.md
and B1C_R1_H100_MINI_EXECUTION_20261028.md retain their scientific definitions.

## Preserved attempt and fixed scope

Original deployment19f3f0e76255d76012a360477c28ecdea25eec70 on Mini .201:
`/root/arc2_global_paper_20261025/code_19f3f0e_b1c/results/b1c_full_mini_r1_20261028`.
It stopped28Oct12:55:41+07 with FAILED_PRESERVED and95 generated rankings.
The failed NanoNQ E5/seed41 SimpleLinear worker returned1 with CUDA OOM at
model allocation, before fitting. It was not SIGKILL; recorded CPU oom and
oom_kill counters remained0. No current scorer ran and no labels were opened.

Preserve this entire source attempt, its status, failed worker, inputs, logs,
resource traces and timings. Never edit it to PASS or overwrite any output.
The original configs/b1c_lock.json, both registries, original protocols and
frozen numerical sources remain byte-identical. New sources/lock/manifest
have distinct paths and a distinct pre-run commit.

Complete exactly the original320 missing DEV rankings and separate736-cell
scoring/report/final D1, then STOP before B2/TREC/systems. There is no new
dataset, method, margin, training setting, paid-set or selection policy.

## Identity and compatible reuse

The completed prefix contains45 whole groups:30 FiQA saved-fit groups yielding
50 new endpoints and30 successful historical50% parity checks, followed by15
Nano groups yielding45 endpoints. Reuse exactly these95 endpoints,15 completed
new Nano fits and30 historical FiQA reconstructions. Finish225 endpoints with
75 fresh Nano fits. Final accounting remains120 groups,90 Nano fits total and
30 historical FiQA fits; imported work is not zero-cost new fitting.

Before commitment, inventory the stopped source with a qrel-free manifest.
Bind its original deployment commit, original lock, failure metadata, original
registries and completed cell/parity indices. Require the exact ordered whole-
group prefix of the original registry: no duplicate, missing, extra, renamed
or incomplete endpoint/group. Verify every existing declared ranking, fit,
IDs, ordered anchors and paid array against its saved digest and registry.
Successful neural metadata and artifacts must verify. Failed group45 contributes
no reusable model, checkpoint or ranking and must start fresh.

Copy only complete-group generated artifacts and their dependencies, shared
inputs, rankings and parity files to a unique new recovery output directory.
Copy byte-identically, verify before/after, and preserve old absolute paths and
old commit/lock fields inside historical requests/receipts as provenance.
Those requests must never execute. Retain original failure evidence at source
and bind it in the recovery manifest. Newly executed workers use the new
deployment commit/recovery lock and distinct output paths. Recheck original
source specs for skipped groups as well as remaining groups. At final seal,
bind all imported/generated artifacts and provenance before any scoring.

## Endpoint and unchanged computation

Stay on103.73.232.201:62161, same MIG UUID
MIG-845e7614-1be1-5b0b-b712-bcd163b641f9, H1002g.20gb,
21072183296bytes; CPU/GPU Python paths and all versions remain as R1.
Read-only28Oct13:33+07 observation found1797/20096MiB occupied after the large
other GPU process ended. This observation is not a reservation or guarantee.
Do not modify other jobs, priority, guards, partitions or allocator settings.
No artificial elapsed/RAM/VRAM caps or headroom thresholds are introduced.

ARC2-Global, LA2M20, official SimpleLinear50 epochs/batch4028 and converter
50000 selection updates/batch64 plus its locked fresh selected-length refit
remain unchanged. Keep all seeds,1024 anchors, destination exposure |A union S|,
three budgets, model/cache hashes, deterministic settings, normalization,
exact float32 batch16 ranking, ID exclusions and stable document-row ties.
All fitting and rankings remain qrel-free; no physical encoding is performed.

## Matching smoke, full and separate scoring

First pass the matching committed synthetic smoke for all three learned
methods, including the unchanged500-update converter smoke. Add recovery
fixtures: complete prefix imports unchanged; input/artifact mutation, duplicate,
incomplete group or identity drift rejects reuse. Preserve actual smoke failures.
Only matching code, recovery lock, manifest and both registries admit full.

Run remaining groups in the unchanged order, importing completed groups rather
than rerunning them. Generate a new complete320-ranking seal and record95
imported/225 newly generated rankings and15 imported/75 fresh Nano fits.
The new run's metadata describes its own execution; original statuses/times
remain intact. Preserve any new CUDA/OS/I/O/verification failure and stop.
There is no unbounded silent retry or dropped cell.

After all320 rankings and dependencies seal, use the unchanged separate B1c
scorer with the recovery lock. It must reject any changed/unsealed input and
verify the same416 existing plus320 completed cells before opening DEV labels.
The original four DEV label sources,736 cells, five declared macro contrasts,
20000 shared-query bootstrap draws/seed20261028 and confidence rules remain.
Record first current DEV label opening; TREC labels remain closed.

Retrieve and verify results, report all positive/negative conditions, generate
the full comparison figures and refresh final D1 through ARIS. This campaign
does not measure isolated H100 deployment cost, SLO or traffic. STOP for user
review before any B2 or systems launch.
