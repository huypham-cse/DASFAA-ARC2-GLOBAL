# B1-P R1: restore original dense float32 neighbor scores

Pre-run amendment, commit before a fresh R1 smoke/full schedule. First B1-P
commit1eaac90965c78ddb595f6ad5b5bd2bc3ffb2eef2 passed CPU and official SimpleLinear
smoke, then converter neighbor parity failed on synthetic near ties: six of959
ordered entries differed at k7. Row-block GEMM changed tiny float32 score values
relative to the historical whole-matrix calculation. No converter training,
full scientific run or qrel read occurred in that attempt. Preserve its metadata,
arrays, SimpleLinear checkpoint and logs at code_1eaac90/results; receipt subset
is synchronized locally. Do not relabel the failed attempt PASS.

Use backend dense_float32_scores_stable_topk_r1: normalize as before, compute
the original entire float32 target@target.T once, set its diagonal to -inf,
then select each row's exact top100 through partition and explicit boundary
ties/ascending row IDs followed by final-k sorting. Score arithmetic now matches
the original implementation; avoid only the whole N-by-N integer argsort output.
The retained block_rows256 argument groups row processing, not score GEMM.
Replace previous blocked-score/no-square-workspace descriptions accordingly.

The refit float32 similarity matrix at28,819 pairs is about3.094GiB. H100 host
observation showed roughly1,875GiB available RAM; this is feasibility information,
not a new memory gate or authorization to run it on the laptop. Training, data,
normalization, k100, sampling, losses, model, seeds, checkpoint/refit rule,
rankings/scoring matrix and32-contrast family are unchanged.

Keep exact ordered parity assertions for all duplicate/near-tie cases and two
1024x768 synthetic fixtures; repeated whole-score calculations must have zero
score drift. Repeat the complete six-method smoke from a new clean checkout and
unique directory. Only after PASS may its already-authorized full B1-P schedule
run. No new time/resource cap, label-driven tuning or subsequent item is added.
