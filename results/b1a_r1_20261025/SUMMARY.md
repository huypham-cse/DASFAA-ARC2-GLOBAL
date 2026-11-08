# B1a completed: inputs and small H100 smoke

**PASS. STOP: waiting for user confirmation before B1b.**

Successful pre-run commit: `f9774835df2b3442b6e61cfd61320864533abdae`.
Run: 2026-10-25T16:14:23.090346+00:00 to 2026-10-25T16:14:46.054130+00:00.
Recorded attempt wall time: **22.96 seconds**; peak observed process-tree RSS **1.59 GiB**.
This excludes operator/protocol preparation, source inventory and artifact-transfer time. Shared-server smoke timings are not isolated GPU cost/throughput evidence.

## Prepared inputs

| Collection | Documents | Queries | Ready state |
|---|---:|---:|---|
| NanoNQ | 5,035 | 50 | pinned corpus/query files, IDs and paid selections; full corpus not encoded here |
| NanoHotpotQA | 5,090 | 50 | pinned corpus/query files, IDs and paid selections; full corpus not encoded here |
| NanoFEVER | 4,996 | 50 | pinned corpus/query files, IDs and paid selections; full corpus not encoded here |
| FiQA | 57,638 | 500 DEV | eight existing vector files and source/ID/anchor/order hashes verified |
| **Total development corpus entries** | **72,759** | **650** | input readiness, not new quality results |

## Smoke outcomes

- Exact historical-reference parity: four dimension cases, proxies and mixed galleries at block sizes 1/13/512.
- Exact-search toy tie and identical-ID exclusion checks passed.
- 60 nested, anchor-inclusive paid sets verified; 30 new Nano anchor/order arrays hashed.
- Four cached models encoded fixed synthetic texts on CUDA, float32, 128-token maximum, explicit E5 prefixes; all shape/finite/unit checks passed.
- Every model repeated the encode with maximum absolute difference 0.0.
- Both synthetic mixed galleries passed: 12 docs, 8 fitting pairs, 9 paid IDs, 3 proxies, 4 queries, exact top3.
- Largest worker-owned CUDA allocated peak: **453.24 MiB**.
- Synthetic preparation performed 96 document and 32 query encoder evaluations including repeats across all four models. No full-corpus re-encoding/deployment cost is billed.
- Raw archive checksum and local hash/selection/metric-format verification passed.

## Preserved failure and scope

The first attempt stopped in the upstream source-byte check because the lock used the Windows CRLF hash on a clean Linux LF checkout. No fit, dataset content download or CUDA encode occurred in that attempt. Original metadata/resource trace remain in `../b1a_first_failure_20261025/`; the separate R1 amendment corrects the exact Linux bytes without altering method/data/seeds.
Local synchronization verification initially compared the Linux lock hash with the Windows working-copy bytes. The corrected verifier checks the exact committed Git blob at the recorded pre-run commit plus semantic equality; the failed local assumption is retained in provenance/qa/b1a_local_verifier_attempt1.json. No scientific output was changed or rerun for this verifier repair.
No qrels or TREC-COVID files were requested/read. No benchmark nDCG/Recall, independent test, baseline fit campaign, cost/SLO trial or claim audit was performed.
ARIS pre-run readiness reviews are same-family/provisional, not a paper acceptance or independent scientific result.
The CPU numerical environment has an incompatible encoder stack; we preserved it and used a separate existing GPU encoder environment. The full baseline adapters/scientific protocol are not certified by this small smoke.

## Next item requiring user confirmation

**B1b:** pin and implement genuine clustered LA2M, official-code SimpleLinear and standard affine ridge, qualify their adaptations, and validate the adapters on synthetic/qrel-free fixtures. Do not start the full benchmark matrix in that item.
