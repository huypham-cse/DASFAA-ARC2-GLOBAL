# Reproduce the review evidence

**R2 completeness audit:** [EXPERIMENT_ATLAS.md](EXPERIMENT_ATLAS.md) lists every completed block, the 1,340-cell union, supporting correctness tests, repaired historical omissions and unrun conditional systems work. Three added control figures expose the M/P/G evidence. Fresh semantic release audit was interrupted by quota; numerical/inventory evidence is provided for supervisor checking.


## Scope and environment

There are three distinct levels. The supplied and tested paths are offline hash verification, saved-ranking/statistical reproduction, synthetic method execution, and saved-result figure rebuilding. These do not perform a new scientific GPU run.

Use Python 3.12 (tested 3.12.10). Pinned review package versions are in requirements-review.txt; they differ from the frozen original H100 fit/encoding environments, whose versions remain in the raw receipts. No GPU, SSH key, password, original project path, cloud backup or graph4paper installation is needed for the offline review paths.

Windows PowerShell:

```powershell
cd D:\DASFAA-2027-paper-release
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-review.txt
.\.venv\Scripts\python.exe reproduce/verify_review_release.py --root . --mode full
.\.venv\Scripts\python.exe reproduce/smoke_review_method.py --root .
.\.venv\Scripts\python.exe reproduce/rebuild_review_figures.py --root .
```

Linux/macOS:

```bash
cd /path/to/DASFAA-2027-paper-release
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-review.txt
.venv/bin/python reproduce/verify_review_release.py --root . --mode full
.venv/bin/python reproduce/smoke_review_method.py --root .
.venv/bin/python reproduce/rebuild_review_figures.py --root .
```

Dependency installation needs an index/cache; all later review operations are offline. The manifest uses SHA256 and relative paths. Existing absolute paths in immutable historical metadata are provenance identifiers; portable verification maps the included files and does not dereference the original host or disk.

## 1. Verify bytes only

```bash
python reproduce/verify_review_release.py --root . --mode hashes
```

This standard-library-only check detects absent/changed packaged files. It does not establish correctness of a scientific claim. RELEASE_MANIFEST.json and its checksum list are supplied together; they document a snapshot rather than a cryptographic signature from a third party.

## 2. Independently reproduce saved relevance metrics and uncertainty

```bash
python reproduce/verify_review_release.py --root . --mode full
```

Expected: PASS;736 DEV rankings/239,200 metric values,184 B2 rankings/18,400 metric values; locked 20,000-draw uncertainty recomputation. Five mapping seeds are averaged before query resampling. B2 has 11 family-positive, 19 unresolved, 0 family-negative nDCG comparisons. Source/seal/first-opening chronology bindings and selected negative control anchors are checked. Read the receipt for exact comparisons and tolerances.

The independent full scorer already opened TREC-COVID once on 31 October 20:12:17 UTC (1 November 03:12:17+07), after all rankings and a separate endpoint replay were sealed. This local command reads the saved labels; it neither creates a new independent test nor changes the original first-opening receipt. No label-based tuning or cell selection occurs.

Large fit weights and full-corpus vector endpoints are omitted. Local raw-ranking QA is not a new float32 endpoint-search regeneration. The original separate 184-endpoint replay proof and transport-bound full-backup receipts remain available. B1-G relevance metrics are independently rescored from all210 pure/450mixed saved rankings. Full vector search and sampled score-error distributions are not regenerated.

## 3. Exercise the frozen method with synthetic data

```bash
python reproduce/smoke_review_method.py --root .
```

Small deterministic synthetic inputs exercise the real frozen fit and mixed-gallery functions. Lambda10 and exactly two tangent updates stay unchanged. This verifies executable plumbing and structural invariants; it supplies no new relevance result or GPU performance claim. Its default dual backend is distinct from a new validation of the archived B2 primal execution backend.

## 4. Rebuild publication figures

```bash
python reproduce/rebuild_review_figures.py --root .
```

Rebuilds six DEV/B2 figures in PDF/SVG/300dpi PNG from saved, QA-bound summaries, retaining all baselines and conditions. Original released figures stay unchanged; regenerated outputs and hashes are under checks/. Fonts/backend versions can change bytes/layout slightly. Saved numeric values and interval decisions must agree. Poppler pdftoppm is optional for additional PDF-preview PNGs; it is unnecessary for the six PDF/SVG/PNG exports.

## 5. A new full scientific rerun (reference route, not tested as a turnkey launcher)

The archived ops/ runners and immutable configs/protocols preserve the original acquisition, model revisions, source pins, anchor/order generation, fit settings, encoder prefix/length rules, exact-ranking ties and scoring definitions. Start with protocols/B2_TREC_COVID_CONFIRMATION_20261031.md and configs/b2_lock.json. Read archived runners with --help before planning a new deployment.

A new host must recreate the recorded Linux CPU/GPU/upstream/encoder environments and install the official-code baseline at the pinned upstream revision. Download dataset/model files using the locked revisions and verify bytes/hashes; physically encode four models, fit all 60 galleries and generate 184 rankings; replay all endpoints; reproduce scoring using the already-public saved labels. Provide new local path bindings and a distinct output directory/protocol rather than editing original locks/raw results or treating a cache as physical new encoding.

Original execution used H100 MIG20GB, 171,332 documents and 50 queries. B2 had 685,328 document encodings across four model caches; these are not unique documents or a measurement of a partial production deployment. Shared-load campaign time was about 13h24m, not a reserved GPU-time guarantee or an isolated speed benchmark. Full caches/weights occupy tens of GB and must be regenerated/downloaded; this review package intentionally carries the compact evaluation evidence instead.

No new H100 run is authorized or launched by these instructions. Repeating a label-exposed collection is a reproduction, not another unseen independent confirmation. Systems cost/SLO/traffic experiments were not completed and are not claimed.

## Validation record

See checks/FINAL_REVIEW_VALIDATION.json for the final verification summary, and the dated checks/ receipts for detailed package verification, method smoke and figure rebuilding. Early packaging guard failures are retained under checks/packaging_attempts/ and are superseded by the final PASS receipts. New local checks write fresh outputs there. The manifest excludes checks/, .venv/ and bytecode caches so reviewing the package does not mutate frozen evidence. Final archive identity is supplied by its adjacent SHA256 file.

## Additional complete controls and inventory

```bash
python reproduce/verify_control_families.py --root .
python reproduce/verify_experiment_inventory.py --root .
python reproduce/render_release_controls.py --root .
```

The control verifier checks all saved M/P relevance rankings and intervals plus G raw-ranking metrics/arrays. The inventory checker counts logical identities separately from historical file versions and diagnostic counterfactuals.
