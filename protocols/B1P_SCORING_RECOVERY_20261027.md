# B1-P: score the unchanged sealed R5 matrix after receipt-write failure

Commit this protocol, recovery lock and recovery orchestrator before smoke or
scoring. This is completion of the authorized B1-P report, not a new fit or
method decision. STOP after B1-P; no B1-G, breadth, TREC, systems or claim audit.

## Observed failure and immutable inputs

R5 generation at commit7530c8e completed all124 rankings and sealed them before
scoring. Original full metadata then recorded FAILED_PRESERVED because the
scorer failed. The failure is an orchestration defect: ops/b1p_score.py creates
started.json with exclusive creation and creates that same file again when
dev_label_transport exists. FileExistsError occurs before source/seal checks
or label parsing. Original scoring/ contains only started.json/failure.json;
failure.dev_qrel_access_started=false. It must remain unchanged, together with
original scorer logs, metadata, seal, source lock and all rankings.

The source descriptor provenance/qa/b1p_scoring_recovery_source_20261027.json
records exact original root/run, generation commit, metadata/lock/seal SHA256s
and failed-scoring artifact hashes. The recovery lock binds that descriptor,
the unchanged original numerical-source identities, CPU environment/versions
and the new recovery orchestrator/protocol. Do not relabel the old FAILED status
or manufacture a RANKINGS_SEALED metadata derivative. Require the exact failed
metadata, its scorer-only error and intact actual RANKINGS_SEALED seal.

## Recovery implementation and smoke

Use a separate clean committed checkout and a new orchestrator that calls the
unchanged original source/seal checks, graded metric functions, qrel loader,
summary/bootstrap and Markdown renderer. Original ops/b1p_score.py and
ops/b1m_score.py remain byte-identical. The recovery process explicitly records
the original generation commit and its own committed orchestration revision.
Validate original clean checkout/source hashes, unchanged metadata/lock/seal,
all124 ranking hashes/population and500-query/57,638-document ID population.
The new context admits only this pinned scorer failure, not arbitrary failures.

Run a new qrel-free smoke before scoring: actual sealed matrix/source/context
validation, existing graded synthetic metric checks, reproduction of the
exclusive-write failure on synthetic files and successful single-start receipt
handling. Preserve smoke failures and drift-rejection checks. Smoke PASS must
bind the recovery commit, lock, descriptor and original ranking seal. No fitting,
encoder loading, new physical destination encoding or held-out label access.

## Scoring and unchanged interpretation

Create only a unique new scoring_recovery_r1_20261027 subdirectory inside the
original raw run. Write started.json once, with the prior DEV transport status
already selected. Preserve existing attempts; no overwrite or retry loop.
Before TSV parsing, require all source/context/ranking checks and smoke PASS,
verify prior opaque inspected-DEV transport receipts, then durably record the
first scorer DEV parse receipt. That is not the first historical/transport byte
opening. Read only the original hash-locked FiQA DEV TSV. TREC stays closed.

Reuse exactly the original nDCG@10 and Recall@100 definitions, all500 queries,
five fixed seeds, six methods, two encoder pairs, two regimes and124 rankings.
Use the original ordered32 contrasts,20,000 paired query bootstrap samples,
default_rng20261026/int32 indices, linear percentiles and32-contrast nDCG
Bonferroni family. No threshold, margin, tie rule, fit, checkpoint, case selection
or statistical interpretation changes. Report every sign, failure and unresolved
interval. FiQA remains inspected development evidence, not independent evidence.

Save all124x500x2 per-query metrics, cell index, every mean/contrast, full-X/Y
references, summary Markdown/JSON and completed artifact manifest. Reverify
all original contexts/sources/rankings and recovery lock/tool bytes before
publication; verify the TSV hash after scoring. Any failure retains its output
and traceback; original raw status remains FAILED_PRESERVED even if recovery
succeeds. The live tracker/report may separately declare scoring recovery PASS.

Synchronize compact paper-relevant rankings/metrics/IDs/logs and verification
receipts; large weights/proxies remain remote with a full generation inventory.
Cached vectors imply0 new physical document encodings, not measured deployment
cost. Timing segments, original/discarded work and shared-load variation remain
qualified. Complete the B1-P report and STOP for user review.
