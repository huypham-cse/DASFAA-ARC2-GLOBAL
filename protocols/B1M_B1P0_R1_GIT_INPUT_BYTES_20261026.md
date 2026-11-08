# B1-M/P0 R1: exact committed Linux input bytes

Pre-run amendment to B1M_B1P0_DEVELOPMENT_20261026.md. First pre-run commit
5070bda3288e7f80b978898bb8710ba4107ca687 passed P0 smoke6/6, then mechanism smoke
stopped before synthetic fitting, encoding, dataset ranking or qrel access.
The input lock used current Windows working-copy hashes for two derived JSON
files, while their already-committed Git blobs have LF bytes. No source/data
content, array, method, model, metric, tolerance, scope or interpretation changed.

R1 pins exact committed Git blob SHA256 for all packaged inputs, as deployed
on the clean Linux checkout. The only changed packaged hashes are metric_index
and summary JSON; provenance/qa/b1mp0_windows_git_input_differences.json records
both byte counts/hashes. All raw rankings, vectors, selections and historical
results remain untouched. Original failed metadata/logs and successful P0 smoke
remain at code_5070bda/results on H100, with compact receipts synchronized locally.

Commit this amendment and updated locks before a fresh unique R1 schedule.
Repeat both smokes, then P0 full and mechanism full. Keep every original run.
No tuning, new endpoint, test-label access, time or resource cutoff is introduced.
