# Reproduce the review evidence

Use Python3.12 and the pinned review dependencies. From this release folder:

```bash
python -m pip install -r requirements-review.txt
python reproduce/verify_review_release.py --root . --mode full
python reproduce/verify_control_families.py --root .
python reproduce/verify_experiment_inventory.py --root .
python reproduce/smoke_review_method.py --root .
python reproduce/rebuild_review_figures.py --root .
python reproduce/render_release_controls.py --root .
python reproduce/verify_story_claims.py --root .
```

The checks run offline after dependency installation, require no GPU, Git or original backup, and write fresh receipts under checks/. They recompute main-result and control metrics/uncertainty from saved rankings, reconcile the1,340-cell inventory, exercise the frozen method on synthetic inputs and rebuild the figures.

For a standard-library-only integrity check:

```bash
python reproduce/verify_review_release.py --root . --mode hashes
```

See [EVIDENCE_GUIDE.md](EVIDENCE_GUIDE.md) for the complete evidence and scope. Historical H100 environment details and the reference full-rerun route are preserved in [the extended reproduction guide](appendix/REPRODUCE_EXTENDED.md); its original instructions describe the release root as the working folder. The supplied offline checks reproduce saved evidence, rather than training models or regenerating full-corpus vector search.
