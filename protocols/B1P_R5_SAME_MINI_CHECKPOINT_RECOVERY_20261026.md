# B1-P R5: restore the original Mini checkpoint after R4 guard kill

Commit this amendment, lock and frozen checkpoint receipt before new smoke/full.
This is operational recovery of B1-P, not a new method or scientific selection.

## Reason and preserved evidence

R4 commit42731eb passed six-method full-H100 smoke and the actual zero-update
20,000-step model/Adam/RNG handoff verifier. A new shared GPU guard started
11:05:22UTC after the previously observed guard expired. Its log explicitly
killed R4 worker3337858 at11:13:45UTC, matching cwd and PID. R4 full recorded
SIGKILL/-9 after16.3643s, no reported resumed update, and no scoring. Preserve
R4 metadata, the original/derivative checkpoints and all negative evidence.
Do not disable/edit the guard, disguise the worker, alter other jobs or retry
the same full-H100 deployment while this blocking condition is unchanged.

The original R3b Mini worker was intentionally stopped for relocation after
target checks passed. Its final logged step was28,000 and durable checkpoint
step25,000. Its original FAILED_PRESERVED metadata and the explicit operator
intent/stop receipts remain intact. Use that newer original Mini checkpoint,
not the R4 20,000-step full-device derivative. An explicit raw byte copy is
frozen under handoff_mini_r5_20261026; the lock pins its path, size and SHA256
and the receipt SHA. No reserialization, device-identity edit or field change.

## Unchanged scientific scope and identity

Use the original .201:62161 MIG2g.20gb device and the exact CPU/GPU libraries
and environments in the lock. The numerical converter source remains byte
identical to3b56a1c/42731eb. Its unchanged strict resume verifier must accept
the actual paired inputs, normalized inputs, dense neighbors, configuration,
runtime, seeded initial model and saved optimizer/RNG/history before updates.
Only MiniLM seed17 allpaid28819 Embedding-Converter selection resumes at25,000;
other neural fits start normally. Finish its original50,000-step selection,
then a fresh same-seed all-paid refit at the original earliest-best MAE step.

FiQA inspected DEV57,638 documents/500 queries; two encoder pairs; five seeds;
50% paid28,819 including anchors; fixed1,024 versus all-paid; six methods;
124 rankings and32 fixed contrasts remain unchanged. ARC2-Global stays
lambda10/tangent2, no local/neural mapper. No label-based decision or tuning.
TREC stays closed. Preserve reused51 ranks and complete the remaining73.

## Smoke, execution, access accounting and STOP

Create a new clean immutable checkout and unique R5 schedule/smoke/full paths.
Repeat the full prescribed six-method synthetic smoke,38 dense-neighbor checks,
two exact same-device CUDA resume tests and signed exit7/SIGTERM tests. Full
starts only after smoke PASS for this commit/lock. Reverify the266 transported
qrel-free files, prior successful rankings and original DEV transport receipts.
No new DEV label transport: use the already-present inspected TSV and retain
its opaque transport/first-scorer-parse distinction. All124 rankings are sealed
before separate scorer parsing. Scores remain development evidence.

Use the existing explicit per-cell hash-checked resume interface. R4 CPU-only
handoff verifier is historical and is not invoked for this unedited same-device
checkpoint. Production fit rechecks the actual data and snapshot identity.
Record load/resources and actual failures. No elapsed-time/RAM/VRAM/free-memory
admission threshold, retry loop or signal suppression. A detached finite
smoke-to-full schedule survives closing the laptop terminal.

Keep source/resumed timing segments and snapshot/setup overhead separate;
3,000 post25k logged Mini updates are discarded for this continuation, with
unreported work unquantified. R4 failed setup and its other discarded branch
are retained separately, not added twice as productive training time. Resumed
elapsed_seconds is not total end-to-end fit/deployment cost. Cached physical
destination encodings remain0. STOP after B1-P report; no B1-G, breadth, TREC,
systems or claim audit auto-launch. Do not edit active checkout after launch.
