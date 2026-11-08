# ARC2-Global: supervisor review release

**R2 completeness audit:** [EXPERIMENT_ATLAS.md](EXPERIMENT_ATLAS.md) lists every completed block, the 1,340-cell union, supporting correctness tests, repaired historical omissions and unrun conditional systems work. Three added control figures expose the M/P/G evidence. Fresh semantic release audit was interrupted by quota; numerical/inventory evidence is provided for supervisor checking.


**Start with [START_HERE.html](START_HERE.html)** (open locally in a browser), then [CLAIM_LOCK.md](CLAIM_LOCK.md). This is the completed research evidence for review before manuscript writing, dated 1 November 2026.

The scientific method/results and manuscript remain unchanged; this packet adds documentation and offline checking tools. Both Procrustes and LA2M, every declared comparison, negative outcomes and retained failure records are included in the result reports. Large model/vector caches and duplicate transfer archives are outside this lightweight release.

## Review in this order

1. **Claim and research decision:** CLAIM_LOCK.md (~5minutes); machine-readable version CLAIM_LOCK.json.
2. **Results:** results/b1c_r3_review_20261031/SUMMARY.md (DEV) and results/b2_review_20261101/SUMMARY.md (independent), with figures and CSVs.
3. **Controls and limits:** B1-M/P0 mechanism, B1-P all-paid pairs and B1-G mixed-gallery diagnostics in the other three results folders.
4. **Independent verification:** run the commands below; inspect the newest checks/portable_verification_full_*.json receipt and checks/FINAL_REVIEW_VALIDATION.json.
5. **Original evidence:** immutable protocols/configs, source, QA receipts and ARIS response are provided for inspection.

## Quick commands (from this folder)

```bash
python reproduce/verify_review_release.py --root . --mode hashes
python -m pip install -r requirements-review.txt
python reproduce/verify_review_release.py --root . --mode full
python reproduce/smoke_review_method.py --root .
python reproduce/rebuild_review_figures.py --root .
```

The first command uses the Python standard library and needs no network or GPU. The remaining commands use the pinned review dependencies after installation and remain offline. A full verification checks saved raw rankings and statistics; it does not train models, encode the corpus or open new labels over the network. Output is written under checks/, never over the frozen evidence.

See [REPRODUCE.md](REPRODUCE.md) for Windows/Linux commands, tested scope, runtimes and the distinction between offline evidence reproduction and a new full H100 run. Paths are relative to this folder: the original D:project/backup and SSH access are not required for the tested review commands.

## Contents

| Directory/file | Purpose |
|---|---|
| src/arc2_global | Frozen ARC2-Global, kernels and declared baseline adapters |
| results/ | Saved rankings, IDs, qrels, per-query outputs, bootstrap, tables/figures and reports |
| reproduce/ | Portable offline verification, synthetic method smoke and figure rebuild |
| tools/ | Unchanged historical independent QA/render helpers used by portable wrappers |
| configs/, protocols/, ops/ | Original locked execution authority and archived runners |
| provenance/ | Source snapshot identity, package inclusions/omissions, prior QA and ARIS review |
| licenses/, THIRD_PARTY_NOTICES.md | Preserved third-party attribution |
| RELEASE_MANIFEST.json, CHECKSUMS.sha256 | Byte/hash inventory; checks/ is deliberately regenerable |

R2 also includes all660 saved G top100 ranking records, independently rescored by verify_control_families.py. Full vector/search and sampled-score reconstruction remain outside the portable scope. B1c/B2 raw-ranking metrics and locked bootstrap are independently recomputed by the full review command.

Please review: Is the bounded contribution worth developing into a paper? Is its distinction from the initializer clear? Are the controls and independent limitations stated fairly? A positive review is not an acceptance guarantee. The next step after supervisor feedback is manuscript integration and a fresh manuscript claim audit; no additional experiment is started by this package.
