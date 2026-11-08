# B1-M R2: repair the published binary Nano qrel parser

This amendment concerns scoring only. Commit before the repair scoring process.
The R1 computational run at4056612dcccac74fdf84ccf67783ab87afd85c26 completed
all736 sealed rankings,31 synthetic P0 full fixtures and120 real P0 budget
checks. It then stopped in NanoNQ parsing: published qrels have exactly the
columns query-id/corpus-id, with each listed pair relevant. No graded score
column exists. The initial parser wrongly required a third field. No metric
output was produced before the exception. The first NanoNQ label access remains
recorded; these are DEV labels, not a new independent exposure assertion.

The installed Sentence Transformers4.1.0 NanoBEIREvaluator's _load_dataset
builds a set of relevant corpus IDs from these two columns. Its actual source
excerpt is retained in provenance/qa/nano_qrel_parser_reference_20261026.json.
Official documentation: https://www.sbert.net/docs/package_reference/sentence_transformer/evaluation.html#nanobeirevaluator

Interpret only explicitly locked Nano two-column files as binary relevance1
for listed pairs and0 otherwise. FiQA's explicit graded TSV reader and every
nDCG/Recall formula, query denominator, bootstrap/contrast/aggregation rule
remain unchanged. Add synthetic binary-parser checks before new scoring.
No fit, encoding, selection, ranking, hyperparameter or quality-dependent case
choice is changed or repeated. TREC remains closed.

Use configs/b1m_score_r2_lock.json, binding the original code/lock/seal and
prior scoring failure/first-access receipt hashes. Verify every original ranking
and input before reading labels. Score into a new scoring_r2_binary directory
within the original run, preserving scoring/ and the original FAILED_PRESERVED
metadata. New completion receipts identify the repair; never relabel the original
attempt PASS. The separate scorer is executed from its new clean committed
checkout. Preserve all negative metric results and any further failure.

After successful scoring, verify transferred per-query arithmetic and report
B1-M complete plus B1-P0 numerical readiness. STOP before B1-P/B1-G/main breadth,
TREC, systems or paper claim audit. No new resource/time cutoff is introduced.
