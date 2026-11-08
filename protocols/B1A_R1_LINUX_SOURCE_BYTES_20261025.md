# B1a-R1: correct Linux upstream byte identity

Before any retry: preserve the failed first B1a attempt at commit
7e5bd0f36a9875eec800006811215903ef21f2a9 and
`code_7e5bd0f/results/b1a_20261025T162000Z`. Its metadata records
`FAILED_PRESERVED: Upstream kernel changed`. It stopped in the source check
before numerical fitting, dataset content downloads or GPU encoding; no qrels,
TREC access, benchmark rankings or scientific quality scores were generated.

The initial lock incorrectly supplied the Windows CRLF hash of
`reproduce-scripts/la2m/exp_la2m.py` to a Linux LF checkout. The original source
repo had already documented this distinction in its P8-R2 protocol; failing
to carry that distinction into B1a was a packaging mistake.

The observed clean upstream Git revision is unchanged:
`5e62baf1544264847ce3d8feeabd1ded6499b064`.
Require this exact Linux **raw-byte** SHA256:
`37015108e855101f3855755b755836280d8bb073389b23455825980302b49c67`.
The previously supplied Windows raw hash is
`8040db888379dca990bf0ac74c87d5b27b5269c0fe7c359f4fd76f8950b249b1`;
converting the observed Linux bytes to CRLF reproduces it exactly. Do not
accept arbitrary alternate hashes or normalize upstream code during admission.
Also check the upstream Git revision and clean worktree before extracting the
two original numerical functions.

`configs/b1a_r1_lock.json` is a new lock retaining all original model/data IDs,
seeds, source-reference expectations, numerical settings, CPU/GPU roles, paid
sets and scientific scope; only this documented source-byte fix, added upstream
revision/cleanliness check, and explicit lock-path CLI are introduced. The old
lock and original protocol stay unchanged. Commit the amendment, revised runner
and new lock before a new code checkout and unique `results/b1a_*` retry.

All B1a PASS/FAIL requirements and the STOP for user confirmation remain.
No automatic B1b, full benchmark, TREC scoring or claim audit is authorized.
