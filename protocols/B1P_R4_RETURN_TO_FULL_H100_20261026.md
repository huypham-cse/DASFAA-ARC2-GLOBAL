# B1-P R4: explicit checkpoint continuation on the full H100

User authorized moving back to103.73.232.225:52194 on26Oct for higher throughput.
Pre-run commit must pin this protocol, source hashes, device, original frozen
checkpoint SHA, explicit derivative SHA and handoff receipt SHA before new
scientific smoke/full. Checkpoint serialization/identity inspection is setup,
with zero optimizer updates, not an additional scientific training experiment.

## Operational evidence and unchanged scope

Mini .201 has a4-core cgroup quota. At17:42, the worker main thread waited
8.269/10.01s in the CPU runqueue while llama-server used3.473 cores. Its first
converter was still in selection with durable snapshots. Source83% wait is an
observed sample, not a decomposition of all training time or GPU utilization.
The80GB host guard expired17:00+07; at17:46 no active guard was found, quota16
cores and about3.9GiB free VRAM. A later CUDA probe reported2.82GiB free,
132 multiprocessors, NVIDIA H10080GB HBM3,84,929,478,656 total CUDA bytes.
GPU UUID: GPU-fc097b05-fa24-a5d9-6411-06cedd74e4ec. Shared load is recorded;
there is no promise of exclusive use or guaranteed speedup. Do not change the
guard, priorities, cgroup settings or other jobs. No artificial resource cap.

All scientific method/data/metric settings remain B1-P: FiQA inspected DEV,
two encoder pairs, five seeds,50% paid28819, fixed1024 versus allpaid, six
methods,124 rankings,32 locked contrasts. Lambda10/tangent2, neural batch64,
50,000 selection updates, earliest-best paired-MAE rule and fresh same-seed
selected-step refit remain unchanged. No labels or outcomes select a handoff.
TREC remains closed. Retain all failed, negative and discarded compute evidence.

## State relocation without rewriting the source

While Mini continues, freeze one opened completed atomic selection_resume.pt
by copying its bytes to a new handoff directory. Record actual current_step,
source path, original request, timestamp and raw SHA; preserve the raw snapshot
and all Mini history/metadata. Transfer only the required owned artifacts.

Use ops/b1p_checkpoint_handoff.py on CPU with the trusted raw hash. Create an
explicit new derivative changing only identity.cuda_device from
NVIDIA H10080GB HBM3 MIG2g.20gb to NVIDIA H10080GB HBM3. Preserve every model,
Adam, NumPy/CPU/CUDA RNG, current step, history, initial hash, best-validation
state and observation field. Verify all field/tensor bytes before and after
serialization; CPU storage tags may replace CUDA tags without numeric changes.
Keep converter.py byte-identical to3b56a1c. Do not weaken its strict production
resume identity checks. Only the first MiniLM seed17 all-paid converter gets
the explicitly pinned selection resume checkpoint; other fits start normally.

This preserves the exact handoff state. The subsequent full-GPU floating-point
trajectory is not claimed bitwise identical to uninterrupted MIG training.
The first converter selection is a documented mixed-device continuation; its
fresh selected-step refit runs entirely on the destination. Original and current
segment times, snapshot overhead and discarded post-snapshot Mini compute are
reported separately; resumed elapsed_seconds alone is not total selection cost.

## Validation, operator stop and full schedule

Use a new clean checkout and unique R4 smoke/full directories. Execute the
complete six-method synthetic smoke with38 dense-neighbor parity checks,
same-device CUDA exact-resume tests and synthetic exit checks. Also execute
ops/b1p_handoff_verify.py: load the actual derivative on target, require the
strict seeded initial-model hash, exact model+Adam loading and CPU/CUDA/NumPy
RNG restoration with zero optimizer updates. Production fit independently
rechecks the actual normalized paired data, neighbors and configuration before
its first resumed update. No extra real-data trajectory experiment is added.

Keep Mini running until destination smoke and zero-update handoff validation
PASS. Immediately before R4 full, stop only the verified owned Mini worker by
SIGTERM; let its parent/campaign record the observed exit. Write a separate
intentional operator-relocation receipt before signalling, including PID/request
identity, chosen checkpoint step and latest post-snapshot logged step. Preserve
the resulting original FAILED_PRESERVED metadata; do not relabel old runs.

R4 full verifies/imports the same51 successful ranks and completes73 remaining
rows. First selection resumes from pinned checkpoint N through50,000 and applies
the original best-checkpoint/fresh-refit policy. Seal all124 before the separate
DEV scorer. Destination uses its already-present historically inspected FiQA
TSV; no new label transport is needed. R3 transport remains upstream provenance.
Report B1-P and STOP before B1-G, breadth, TREC, systems or paper audit.
