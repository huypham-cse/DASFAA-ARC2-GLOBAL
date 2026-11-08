# B1-P R2: recover completed cells and preserve interrupted training state

Pre-run amendment to B1P_ALL_PAID_FIQA_20261026 and its dense-neighbor R1.
User authorized continuation on26Oct after the R1 full failure. Commit this
protocol, updated lock and implementation before any new numerical smoke/full.

## Evidence and unchanged scientific scope

R1 checkout f1457b8 completed its synthetic smoke and51/124 ranking artifacts
(44 previously imported plus7 new). At09:31:30+07 on26Oct its first all-paid
MiniLM seed17 Embedding-Converter worker exited abnormally during refit; the
last recorded refit step is43,750. Selection completed50,000 updates and chose
49,750 by the locked paired-vector validation rule. No B1-P scorer ran and no
new FiQA or TREC label opening occurred. Parent did not persist child exit code;
worker metadata RUNNING is stale. Empty stderr and current oom_kill=0 are not
enough to assign a signal, actor or root cause. Preserve the failed directory,
its metadata, resource traces, weights and all successful cells unchanged.

All datasets, encoder revisions, cached vector identities, paid rows, regimes,
six methods, seeds, full124-cell population, losses, precision, neighbor math,
selection/refit rule, exact retrieval and32-contrast scorer remain unchanged.
ARC2-Global retains lambda10 and two tangent steps. No quality-based selection,
shortened fit, new labels, added comparison, time cap or resource gate is added.

## Recovery of completed work

Pin provenance/qa/b1p_r1_recovery_source_20261026.json by its file SHA256 in the
updated lock. Its111-file manifest binds the failed run metadata,51 ranking
files, input IDs/selections and completed fit metadata/parameters/neural outputs.
Verify all byte counts/hashes, unchanged prior source commit/lock and failure
status, and identical new/old input arrays. All44 ordinary imported cells must
agree with the normal locked import path. Copy only the7 additional completed
ranking cells, retaining original receipts and source paths/commit. No new
paired timing is attributed to reused fits. Never edit the failed source run.
Skip those7 fits in the original pair/seed schedule; produce the remaining73
rankings. Final separate scoring still requires the complete124-cell seal.

The failed converter has no optimizer checkpoint. Its weights at selection
cannot resume the interrupted refit. Restart this failed fit from its original
seed and execute the full locked selection plus fresh selected-step refit.
This restarts computation, not the scientific design or a new method search.

## Durable checkpoint and exit evidence

New converter fits write an atomic latest resume checkpoint every5,000 updates
and at the final step (every250 in the synthetic smoke). Snapshots include
current-update model and Adam states, NumPy sampling state, Torch CPU/CUDA RNG,
completed step, initial state identity, full logged history, best validation
value/selected step/best model, configuration and source/target/validation array
identities. Resume validates those identities before restoring all states and
starts at the next update. Stored current-update weights are distinct from
the selected best weights returned at selection completion. Snapshot I/O is
included in observed wall time and recorded as overhead, never subtracted from
a physical-cost claim. This study still uses cached document vectors.

The paired-only worker may accept explicitly hash-pinned selection/refit resume
checkpoint paths in a fresh request/output directory. No qrels, queries or
unpaid target arrays enter that API. This R2 launch uses no old resume snapshot;
new snapshots enable a later documented recovery without restarting a fit.
No automatic retry loop or signal suppression is added. Real failures stop
the attempt, preserve its state and require inspection.

Persist child PID/start record before waiting, then signed subprocess return
code, signal number/name when negative, stdout/stderr hashes, end time and
before/after cgroup memory events. Do not infer the earlier unrecorded signal
from a future child failure. Persist selected_iteration before beginning refit.

## Smoke before full and finite stopping point

Run a new unique R2 six-method smoke under the committed CPU/GPU environments.
Retain original dense-neighbor exact parity and scorer synthetic checks. Add
synthetic child exit7 and self-SIGTERM checks of the actual process recorder.
Add tiny paired-vector CUDA checkpoint tests for both validation-selection and
fixed-iteration refit: uninterrupted versus interrupt-after-snapshot/resume,
requiring identical final state, selected step and numerical training history
(timing/resources excluded). Checkpoint identity drift must be rejected.
No benchmark/qrel is needed for these tests. Keep actual full converter width
and original500-update selection/refit in the ordinary six-method smoke.

Only after all smoke checks pass may the already-authorized B1-P full run start
in a new clean checkout and unique directory. It reuses the verified51 ranks,
completes73, seals124, and invokes the same separate FiQA DEV scorer once.
Preserve failed/negative/shared-load observations. Report B1-P and STOP before
B1-G, remaining breadth, TREC, systems or paper claim audit.
