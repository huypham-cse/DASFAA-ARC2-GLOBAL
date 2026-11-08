# B1-P scoring recovery readiness

Verdict: **READYTOCOMMIT**. No concrete implementation or scientific-order blocker found in the reviewed recovery. This is a same-family provisional readiness review, not an independent claim audit or an execution PASS.

Reviewer route: secondary Codex agent, GPT-6.1 high as explicitly requested; `review_independence: same-family`; `acceptance_status: provisional`.

The bounded recovery correctly handles the observed failure. The original scorer exclusively writes `started.json` twice when `dev_label_transport` exists, before source/seal checks or TSV parsing. The recovery selects the final status before one exclusive write and retains the exact original FAILED_PRESERVED metadata and failed artifacts. It never calls the incompatible original same-commit/sealed-metadata context gate; its replacement checks the separately pinned generation and recovery contexts instead.

Static verification passed: the descriptor bytes match the recovery lock and its embedded descriptor; the original source lock matches its pinned SHA256; all 25 original canonical source hashes match; `ops/b1p_score.py`, `ops/b1m_score.py` and `configs/b1p_lock.json` match generation commit `7530c8eb46b68c9d5937c4bb9ccfd929d1613e74`; both recovery orchestrator/protocol hashes match; CPU environment/version pins match the original. Python AST parsing passed for all three scorer modules.

The implemented order is sound: verify clean committed checkouts, exact failure context, source identities, runtime, all 124 sealed rankings and original ID populations, and prior opaque DEV transport; perform synthetic receipt/metric checks; require the matching qrel-free smoke before a durable scorer parse receipt; then call the unchanged hash-locked FiQA loader, metrics, ordered 32 contrasts, 20,000 shared int32 query resamples and Markdown renderer. All 500 queries, five seeds, two pairs, two regimes, six methods and full references remain included. Final revalidation precedes publication. Exclusive output creation preserves failed attempts. FiQA remains inspected DEV; TREC remains closed; STOP remains after B1-P reporting.

Remaining authorized sequence: commit the protocol, lock, descriptor and recovery tool; use a separate clean checkout for the qrel-free smoke; proceed to the unique scoring recovery directory only if that smoke passes; preserve and synchronize receipts, metrics and failures; finish the B1-P report and STOP. No new fit, encoding, selection, threshold, budget, label source or statistical family is required by this review.

Limits: this review read local code/provenance and checked hashes/syntax only. It did not contact the remote, open labels, execute smoke/scoring, inspect unavailable original raw files directly, or certify empirical outcomes. The actual gates must verify those raw files before scoring. The live tracker B1-P table row still reports the older running snapshot despite its updated completion header; align that row in the already pending tracker update.

Trace: `.aris/traces/research-review/2026-10-27_b1p_scoring_recovery/` (local trace, preserved with readiness/results).

## Bounded B1-P result interpretation (2026-10-27)

Same-family provisional interpretation only; no formal claim audit, D1 verdict or independent evaluation. The saved recovery smoke reports PASS and scoring reports DEV_SCORED at 03:20:39 UTC. Their recorded artifact hashes match locally. The (124, 500, 2) per-query array reproduces all 28 reported means and all 32 contrast deltas; interval sign labels match the saved endpoints. No qrels or remote system were accessed in this review. Original generation metadata/failure remain FAILED_PRESERVED with original scorer parse access false.

Allowed conclusions:

- On inspected FiQA DEV, all-paid ARC2 is competitive on MiniLM but has no uniform advantage across encoder pairs. MiniLM nDCG is 0.367146 versus Procrustes 0.333386, LA2M adaptation 0.338923, SimpleLinear 0.332316 and converter adaptation 0.325761; all four predeclared nDCG family intervals favor ARC2. Ridge is 0.367263; ARC2 minus ridge is -0.000117 with family interval [-0.007540, +0.006532], hence unresolved. This does not establish equivalence.
- E5 all-paid ARC2 nDCG is 0.291867 versus Procrustes 0.336202 and LA2M adaptation 0.329341; family intervals favor both baselines over ARC2. ARC2 exceeds SimpleLinear and ridge with positive family intervals. Its higher mean than converter (0.262519) is unresolved under the family interval: delta +0.029348, interval [-0.015573, +0.074762].
- Using all paid pairs rather than fixed 1,024 pairs improves MiniLM ARC2 nDCG by +0.059641, family interval [+0.039341, +0.080604]. E5 ARC2 instead has a -0.019768 nDCG mean change with unresolved family interval [-0.056330, +0.016637]; its Recall change is -0.061435 with descriptive nominal95 interval [-0.083203, -0.040108]. More fitting pairs therefore do not uniformly help the frozen method. Across the 12 method/pair combinations, all-paid increases mean nDCG in 10; E5 ARC2 and SimpleLinear are the two exceptions. Do not turn those two unresolved nDCG decreases into family-supported degradation claims.
- The fixed-1,024 narrative also needs the negative comparisons: MiniLM fixed ARC2 has lower nDCG than every all-paid baseline, with all five family intervals negative. E5 fixed ARC2 is below all-paid Procrustes/LA2M and above all-paid SimpleLinear/ridge/converter under the corresponding family intervals. The results do not establish that the smaller fitting set retains the quality of all-paid baselines.
- In both pairs and both regimes, ARC2's mean nDCG and Recall remain below the full-X and full-Y references. These reference comparisons are descriptive, without a new inferential test. The observed partial-encoding operating points do not show a quality gain over keeping the incumbent.

Limits and reporting boundary:

- These are two encoder pairs, 500 previously inspected FiQA DEV queries and five mapping seeds at the same 50% paid destination budget (28,819 documents). Fixed/all-paid changes the fitting-pair count; it does not establish equal fitting runtime or deployment cost. Baseline adaptation qualifications remain necessary.
- nDCG family intervals use the locked 32-contrast Bonferroni percentile procedure; coverage is approximate. Recall intervals are nominal95 and descriptive, without family protection. Seeds are averaged before paired query resampling; five seeds are not five independent datasets. Unresolved intervals establish neither equivalence nor noninferiority.
- Preserve the frozen lambda10/two-tangent identity and every negative result. These observations support neither an independent win, cross-encoder dominance, universal benefit from more fitting data, nor a deployment/encoding-cost advantage. They authorize no method, threshold or case switch.
- Report all six methods, both regimes, full references and all 32 contrasts; retain the failed original scorer alongside the successful recovery; finish B1-P and STOP. No additional study or formal audit is requested here.
