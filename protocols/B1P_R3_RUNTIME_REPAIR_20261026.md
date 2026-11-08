# B1-P R3 runtime repair before fresh smoke

Commit this operational note before repeating the Mini smoke. The scientific
source remains clean3b56a1c7fcdd0cf54ba7da22cfe448c6747433e2 and its unchanged
B1-P lock; no new algorithm, baseline, hyperparameter, data or scoring rule.
This note's pre-run commit is recorded separately in the new launch receipt.

The first Mini R3 smoke failed with returncode1, not a signal, at the official
package's import of pydantic_settings, before SimpleLinear training. Preserve
its original FAILED_PRESERVED metadata and raw files. A subsequent import-only
probe identified POT required by upstream's eager Gromov-Wasserstein imports.
Neither probe ran retrieval, training or parsed labels.

Install only the missing initialization dependencies in the isolated GPU env:
pydantic-settings2.16.1, python-dotenv1.2.4, POT0.9.7.post1. The eight original
locked GPU library versions and official source remain unchanged. Actual
official_components import plus exact SimpleLinear configuration comparison
now PASS. Save full CPU/GPU package inventory and the failed/successful probes.
These dependencies do not add Gromov-Wasserstein to the six-method matrix.

Run a fresh unique smoke/full schedule named mini_r3b_20261026, retaining the
first Mini attempt untouched. Require the same complete six-method, dense
neighbor, exact CUDA recovery and process-exit smoke before full. Keep51 ranks
for verified reuse and all73 remaining rows. The explicit R3 DEV transport and
first-scorer-parse accounting, full124-cell seal,32 contrasts, absence of caps,
and STOP after B1-P remain unchanged.
