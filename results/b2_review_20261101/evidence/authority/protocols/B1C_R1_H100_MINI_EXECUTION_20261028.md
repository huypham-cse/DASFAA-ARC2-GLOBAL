# B1c R1: full execution on the available H10020GB MIG

This amendment is committed before the MINI smoke and before any B1c full
scientific run. It supersedes only the deployment/source-transport paragraphs
of B1C_MAIN_MATRIX_COMPLETION_20261028.md; the320missing/416existing matrix,
algorithms, adapters, anchors, paid sets, revisions, seeds, budget arithmetic,
normalization, exact search, all scoring/bootstrap rules and final STOP remain.

The original MAIN committed scientific-source snapshot1df7c3e completed its
synthetic smoke successfully (211.188seconds); no MAIN full run began and no
new DEV labels were opened. Its complete smoke and the aborted operator
transport/queue attempts remain preserved. The source project commit is585b8b8;
the clean deployment snapshot has distinct provenance, identical scientific
source hashes and byte-identical locked registries, not a full-history clone.

MAIN's current shared-GPU smoke selection used25.692seconds/500converter updates.
Linear projection for30workers is about21.4hours selection-only, up to42.8hours
with maximum-length refits, before other work. This is a rough load-dependent
projection, not a validated Nano ETA or a stopping cap. Rather than assume an
idle80GB GPU, use the available MINI endpoint and measure its matching smoke.
The user's supplied availability schedule also extends MINI beyond28October;
it is planning context, not a guarantee that the host will remain available.

New endpoint103.73.232.201:62161, Torch device
`NVIDIA H100 80GB HBM3 MIG 2g.20gb`,
MIG UUID `MIG-845e7614-1be1-5b0b-b712-bcd163b641f9`,
total21072183296bytes. Numerical library versions and CPU/GPU interpreter paths
are unchanged and match the previously used B1-P MINI runtime. The actual
baseline dependencies are pinned NumPy/SciPy/Torch/sklearn/pydantic/faiss/loguru/
tqdm; no encoder/Transformers installation or new encoding is needed. CPU
LA2M reconstruction keeps sklearn1.5.1 and Haswell/four threads. Record the
actual GPU/MIG identity, own allocations and shared-host observations. Physical
parent-GPU memory/utilization can be unavailable under MIG; preserve N/A rather
than inventing isolation or utilization. No other process/guard is modified.

Of565 historical source files,453paths are absent from MINI's inventory and
present on MAIN:1947593157bytes. Copy only those explicitly listed qrel-free
files using b1c_main_to_mini_manifest_20261028.json; retain exact original paths,
file hashes and all existing matching data. This is source relocation, not
deletion, a new fit, free encoding or a reproduction of MAIN neural trajectories.
The former47-file MINI-to-MAIN preparation is superseded and its partial target
files/logs are retained; no source data or historical result is deleted.

Deploy another clean scientific-source Git snapshot of the amended committed
project, record origin/deployment commits and verify every scientific source,
lock and registry. Run a distinct committed MINI smoke with the unchanged
500-update readiness policy. MAIN smoke is retained but cannot admit MINI full.
After matching MINI smoke PASS and complete453-file destination hash-verified
transport, rehash all565historical inputs plus the2committed source registries.
Only then launch the same finite50FiQA/180Nano/90converter schedule and separate
DEV scorer. If either smoke or any source check fails, preserve it and do not
launch full. No time/RAM/VRAM caps are added.

Use distinct MINI run names/directories. Do not relabel an old MAIN result or
claim bitwise identity of neural fitting across GPU partitions. All scientific
labels stay closed until every new320ranking/fit artifact and old416ranking
source has been verified and sealed by the unchanged scorer. TREC remains
closed. STOP after the full DEV report/final D1 for user review before B2.
