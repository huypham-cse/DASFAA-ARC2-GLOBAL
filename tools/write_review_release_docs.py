"""Write the supervisor-facing claim lock and portable review instructions."""
from pathlib import Path
import json
import importlib.metadata

OUT = Path('D:/DASFAA-2027-paper-release')


def put(name, text):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + '\n', encoding='utf-8', newline='\n')


def main():
    claim = {
        'claim_revision': 'supervisor-review-20261101-r1',
        'purpose': 'Freeze the interpretation of completed evidence before manuscript writing; not a new experiment protocol or method revision.',
        'method': 'arc2_global_tangent2_r1',
        'algorithm': {'initialization': 'centered rectangular Procrustes affine map',
                      'ridge_lambda': 10, 'tangent_steps': 2, 'local_residual': False,
                      'neural_training_required': False, 'main_fit_pairs': 1024},
        'central_claim': 'ARC2-Global is a compact forward document-space adapter that applies two closed-form tangent corrections to a centered Procrustes map. With 1,024 fitting pairs, it improves aggregate nDCG@10 across four inspected development collections. A prospective TREC-COVID test confirms gains in 11 of 30 declared comparisons against the specified ridge, SimpleLinear and Converter configurations, while its incremental nDCG advantage over Procrustes and LA2M remains unresolved.',
        'independent_family': {'positive': 11, 'unresolved': 19, 'negative': 0,
                               'positive_by_baseline': {'Procrustes': 0, 'LA2M20': 0, 'SimpleLinear': 2, 'affine_ridge': 4, 'Converter': 5},
                               'comparisons_per_baseline': 6,
                               'nDCG_Procrustes_point_differences_all_negative': True,
                               'no_equivalence_or_noninferiority_claim': True},
        'statistical_scope': 'B2: all50queries, seeds17/29/41/53/67 averaged before20kshared query bootstrap, seed20261031,30Bonferroni contrasts. Approximate percentile family coverage95%; Recall95% nominal descriptive.',
        'evidence_sources': {
            'DEV': 'results/b1c_r3_review_20261031/evidence/run/scoring/summary.json',
            'independent': 'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json',
            'all_paid': 'results/b1p_r5_review_20261027/scoring/results_summary.json',
            'mechanism': 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
            'mixed_diagnostics': 'results/b1g_r1_review_20261027/scoring/results_summary.json'},
        'preserved_limits': ['No independently confirmed nDCG advantage over Procrustes/LA2M.',
                             'All-paid E5 loses to Procrustes/LA2M; MiniLM versus ridge is unresolved.',
                             'Two-step necessity is DEV evidence; not an independent B2 ablation.',
                             'Mixed-vector replacement can reverse proxy-only ordering.',
                             'No measured physical migration cost, dollar saving, ANN/SLO or real-traffic benefit.',
                             'No novelty priority or venue acceptance probability established.'],
        'review_assurance': {'claim_supported': 'partial', 'review_independence': 'same-family',
                             'acceptance_status': 'provisional', 'formal_paper_integrity_audit': 'not performed'},
        'no_results_removed': True,
        'manuscript_modified': False,
        'further_experiments_authorized_by_package': False}
    put('CLAIM_LOCK.json', json.dumps(claim, indent=2))
    put('CLAIM_LOCK.md', '''# ARC2-Global: claim frozen for supervisor review

Revision: **supervisor-review-20261101-r1**. This freezes the interpretation of completed results before writing the paper. It changes neither the algorithm nor any scientific protocol, label exposure, ranking or scoring threshold.

> ARC2-Global is a compact forward document-space adapter that applies two closed-form tangent corrections to a centered Procrustes map. With 1,024 fitting pairs, it improves aggregate nDCG@10 across four inspected development collections. A prospective TREC-COVID test confirms gains in 11 of 30 declared comparisons against the specified ridge, SimpleLinear and Converter configurations, while its incremental nDCG advantage over Procrustes and LA2M remains unresolved.

## What is established

- **DEV quality:** all five declared macro nDCG comparisons favor ARC2 on NanoNQ, NanoHotpotQA, NanoFEVER and FiQA, under matched 1,024-anchor fitting. These collections were inspected during development.
- **Independent evidence:** the frozen TREC-COVID test contains 171,332 documents, 50 queries, two encoder pairs, five seeds and 25/50/75% paid-document budgets. All184 rankings were sealed and separately replayed before the first final-label opening. The30 primary nDCG family intervals yield11 positive,19 unresolved and0 negative decisions.
- **Mechanism:** the DEV second-step effect is +0.006924 nDCG, family interval [+0.003809,+0.009959]. It is an empirical ablation result, not a convergence or optimality theorem.
- **Representation structure:** the final384-to768 affine map has295,680 float32 coefficients,1,182,720 bytes (~1.128MiB), excluding retained fit objects. ARC2 requires no neural training. Ridge is equally compact and Procrustes similarly compact.

## All independent comparisons remain visible

| Declared baseline configuration | Confirmed improvement | Unresolved | Confirmed worse |
|---|---:|---:|---:|
| A2M / centered Procrustes adaptation | 0/6 | 6/6 | 0/6 |
| LA2M20 integration-script adaptation | 0/6 | 6/6 | 0/6 |
| SimpleLinear official code, locked final50/5-layer policy | 2/6 | 4/6 | 0/6 |
| Affine ridge, lambda10 with regularized bias | 4/6 | 2/6 | 0/6 |
| Embedding-Converter paper-spec adaptation | 5/6 | 1/6 | 0/6 |

All six Procrustes point differences are negative. An interval crossing zero does not demonstrate equality, noninferiority or equivalence. Baseline names refer to the documented configurations; the Converter training regime is not a reproduction of its published multi-corpus setting.

## When this method is a reasonable candidate

A destination-space migration is required, only a declared small paired fitting set is available, and a compact non-neural forward adapter is useful. Evaluate the actual mixed index at the intended budget and inspect both nDCG and Recall before choosing a cutover. Query vectors stay in the native destination space; each document ID has one true or proxy vector.

All-paid fitting can change the choice: FiQA/E5 ARC2 loses to Procrustes and LA2M when all28,819 paid pairs are available; MiniLM versus all-paid ridge is unresolved. TREC-COVID/E5 native Full-X also exceeds Full-Y, and ARC2 is below both. These are substantive limits, not deleted exceptions.

## Claims excluded from this release

Universal or strongest-baseline superiority; equivalence/noninferiority from unresolved intervals; optimal use of every paid pair; an independent one-versus-two-step win; measured dollar/physical migration savings; isolated H100 throughput; ANN, serving SLO or real-traffic benefits. Partial destination exposure is |A union S| with anchors included. B2 full-corpus model caches are not physical partial-deployment cost measurements.

The ARIS semantic verdict is **partial**, same-family/provisional. Computational QA is PASS; a formal manuscript claim audit has not been run. No manuscript is included or modified. No new experiment, retuning or method switch is authorized by this package.

Evidence: [DEV](results/b1c_r3_review_20261031/SUMMARY.md), [independent B2](results/b2_review_20261101/SUMMARY.md), [all-paid control](results/b1p_r5_review_20261027/SUMMARY.md), [mechanism](results/b1mp0_r1_review_20261026/SUMMARY.md), [mixed diagnostics](results/b1g_r1_review_20261027/SUMMARY.md), and [fresh ARIS review](provenance/aris_b2/001-claim-review.response.md).
''')
    put('README.md', '''# ARC2-Global: supervisor review release

**Start with [START_HERE.html](START_HERE.html)** (open locally in a browser), then [CLAIM_LOCK.md](CLAIM_LOCK.md). This is the completed research evidence for review before manuscript writing, dated1November2026.

The original project and manuscript remain unchanged. Both Procrustes and LA2M, every declared comparison, negative outcomes and retained failure records are included in the result reports. Large model/vector caches and duplicate transfer archives are outside this lightweight release.

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

B1-G has all reported scored diagnostics and tables here, but its sampled-vector replay inputs remain in the original project. Its historical QA is preserved; the portable verifier does not claim to regenerate those omitted vectors. B1c/B2 raw-ranking metrics and locked bootstrap are independently recomputed by the full review command.

Please review: Is the bounded contribution worth developing into a paper? Is its distinction from the initializer clear? Are the controls and independent limitations stated fairly? A positive review is not an acceptance guarantee. The next step after supervisor feedback is manuscript integration and a fresh manuscript claim audit; no additional experiment is started by this package.
''')
    deps = ('numpy', 'scipy', 'pyarrow', 'matplotlib', 'threadpoolctl')
    put('requirements-review.txt', '# Observed portable-review environment, Python3.12.10. Not the historical H100 fit runtime.\n' + '\n'.join(n + '==' + importlib.metadata.version(n) for n in deps))
    put('REPRODUCE.md', r'''# Reproduce the review evidence

## Scope and environment

There are three distinct levels. The supplied and tested paths are offline hash verification, saved-ranking/statistical reproduction, synthetic method execution, and saved-result figure rebuilding. These do not perform a new scientific GPU run.

Use Python3.12 (tested3.12.10). Pinned review package versions are in requirements-review.txt; they differ from the frozen original H100 fit/encoding environments, whose versions remain in the raw receipts. No GPU, SSH key, password, original project path, cloud backup or graph4paper installation is needed for the offline review paths.

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

Expected: PASS;736DEV rankings/239,200metric values,184B2 rankings/18,400metric values; locked20,000-draw uncertainty recomputation. Five mapping seeds are averaged before query resampling. B2 has11family-positive,19unresolved,0family-negative nDCG comparisons. Source/seal/first-opening chronology bindings and selected negative control anchors are checked. Read the receipt for exact comparisons and tolerances.

The independent full scorer already opened TREC-COVID once on31October20:12:17UTC (1November03:12:17+07), after all rankings and a separate endpoint replay were sealed. This local command reads the saved labels; it neither creates a new independent test nor changes the original first-opening receipt. No label-based tuning or cell selection occurs.

Large fit weights and full-corpus vector endpoints are omitted. Local raw-ranking QA is not a new float32 endpoint-search regeneration. The original separate184-endpoint replay proof and transport-bound full-backup receipts remain available. B1-G scored diagnostics are hash/anchor checked, not fully regenerated from omitted sampled-vector inputs.

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

A new host must recreate the recorded Linux CPU/GPU/upstream/encoder environments and install the official-code baseline at the pinned upstream revision. Download dataset/model files using the locked revisions and verify bytes/hashes; physically encode four models, fit all60galleries and generate184rankings; replay all endpoints; reproduce scoring using the already-public saved labels. Provide new local path bindings and a distinct output directory/protocol rather than editing original locks/raw results or treating a cache as physical new encoding.

Original execution used H100MIG20GB,171,332documents and50queries. B2 had685,328document encodings across four model caches; these are not unique documents or a measurement of a partial production deployment. Shared-load campaign time was about13h24m, not a reserved GPU-time guarantee or an isolated speed benchmark. Full caches/weights occupy tens of GB and must be regenerated/downloaded; this review package intentionally carries the compact evaluation evidence instead.

No new H100 run is authorized or launched by these instructions. Repeating a label-exposed collection is a reproduction, not another unseen independent confirmation. Systems cost/SLO/traffic experiments were not completed and are not claimed.

## Validation record

See checks/FINAL_REVIEW_VALIDATION.json for the final verification summary, and the dated checks/ receipts for detailed package verification, method smoke and figure rebuilding. Early packaging guard failures are retained under checks/packaging_attempts/ and are superseded by the final PASS receipts. New local checks write fresh outputs there. The manifest excludes checks/, .venv/ and bytecode caches so reviewing the package does not mutate frozen evidence. Final archive identity is supplied by its adjacent SHA256 file.
''')
    put('START_HERE.html', '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ARC2-Global · Supervisor review</title>
<style>body{margin:0;background:#f4f6f8;color:#202d3a;font:16px/1.65 system-ui,Arial,sans-serif}main{max-width:1080px;margin:auto;padding:48px 30px}h1{font-size:38px;letter-spacing:-1px;line-height:1.15;margin:10px 0 16px}h2{font-size:23px;margin:0 0 14px}p{margin:8px 0 15px}a{color:#0f4d92}small,.muted{color:#596c7c}.eyebrow{color:#0f4d92;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;font-size:12px}.card{background:white;padding:28px 32px;border-radius:12px;border:1px solid #e0e6ec;margin:22px 0}.claim{border-left:5px solid #0f4d92;font-size:19px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.stat{background:#eaf1f8;border-radius:8px;padding:20px}.stat b{display:block;font-size:29px;color:#0f4d92}.stat span{font-size:14px}table{border-collapse:collapse;width:100%;font-size:15px}td,th{text-align:left;padding:10px;border-bottom:1px solid #e4e8ec}th{color:#45596c;font-size:13px}figure{margin:22px 0 4px}img{display:block;width:100%;height:auto}figcaption{font-size:13px;color:#596c7c;margin-top:12px}code{background:#edf2f6;padding:3px 6px;border-radius:4px;font-size:13px}.steps{display:flex;gap:12px;align-items:stretch}.step{flex:1;background:#f1f5f8;padding:15px;border-radius:7px}.arrow{align-self:center;color:#0f4d92;font-size:24px}footer{font-size:13px;color:#596c7c;margin-top:30px}@media(max-width:700px){main{padding:25px 16px}.card{padding:22px}.grid{grid-template-columns:1fr}.steps{display:block}.arrow{display:block;text-align:center}h1{font-size:30px}}@media print{body{background:white}.card{break-inside:avoid}main{padding:0}.grid{grid-template-columns:repeat(3,1fr)}}</style>
<main><div class="eyebrow">Research checkpoint · 1 November 2026</div><h1>ARC2-Global<br>Compact embedding-index migration</h1><p class="muted">Supervisor review before manuscript writing. Completed evidence, frozen method, explicit scope.</p>
<section class="card claim">Two closed-form tangent corrections refine a centered Procrustes map. Under1,024fitting pairs, ARC2 improves aggregate development nDCG and has independent gains against specified baseline configurations. Independent advantage over Procrustes and LA2M remains unresolved.</section>
<div class="grid"><div class="stat"><b>1,024</b><span>Paired anchors in the main comparison</span></div><div class="stat"><b>11 / 30</b><span>Independent comparisons with positive family intervals</span></div><div class="stat"><b>No neural fit</b><span>Final affine map ≈1.128MiB for384→768; coefficient storage only</span></div></div>
<section class="card"><h2>What the algorithm does</h2><div class="steps"><div class="step"><b>1 · Fit paired anchors</b><br>Old and new embeddings of a small document set initialize a centered Procrustes map.</div><span class="arrow">→</span><div class="step"><b>2 · Correct directions</b><br>Exactly two tangent ridge updates, lambda10. No relevance labels or query mapping.</div><span class="arrow">→</span><div class="step"><b>3 · Serve a mixed gallery</b><br>Map remaining old vectors; overwrite paid rows with true new vectors. One vector per document.</div></div><p><small>Count all unique destination encodings as |A∪S|, including anchors. This structure alone does not establish measured production cost savings.</small></p></section>
<section class="card"><h2>Development evidence</h2><p>Four inspected collections: NanoNQ, NanoHotpotQA, NanoFEVER and FiQA. Two encoder pairs, five seeds,25/50/75%backfill;736rankings. All five declared macro nDCG comparison intervals favor ARC2. Ablation, all-paid fitting and mixed-gallery controls are retained.</p><figure><a href="results/b1c_r3_review_20261031/figures/b1c_r3_quality_budget.pdf"><img src="results/b1c_r3_review_20261031/figures/b1c_r3_quality_budget.png" alt="Full DEV quality versus budget with all six methods and native references"></a><figcaption>Inspected development evidence. Click for vector PDF. <a href="results/b1c_r3_review_20261031/SUMMARY.md">Complete report</a>.</figcaption></figure></section>
<section class="card"><h2>Prospective TREC-COVID test</h2><p>171,332documents,50queries,184sealed rankings. Separate exact endpoint replay preceded first final-label access. The frozen30-comparison nDCG family has11positive intervals,19unresolved and0negative.</p><table><thead><tr><th>Declared configuration</th><th>Positive</th><th>Unresolved</th><th>Negative</th></tr></thead><tbody><tr><td>Procrustes adaptation</td><td>0/6</td><td>6/6</td><td>0/6</td></tr><tr><td>LA2M20 adaptation</td><td>0/6</td><td>6/6</td><td>0/6</td></tr><tr><td>SimpleLinear official-code configuration</td><td>2/6</td><td>4/6</td><td>0/6</td></tr><tr><td>Affine ridge</td><td>4/6</td><td>2/6</td><td>0/6</td></tr><tr><td>Converter paper-spec adaptation</td><td>5/6</td><td>1/6</td><td>0/6</td></tr></tbody></table><figure><a href="results/b2_review_20261101/figures/b2_all30_primary_contrasts.pdf"><img src="results/b2_review_20261101/figures/b2_all30_primary_contrasts.png" alt="All30 independent ARC2-minus-baseline contrasts with family intervals"></a><figcaption>All30primary contrasts, approximate95%Bonferroni family coverage. Unresolved does not mean equal or noninferior. <a href="results/b2_review_20261101/SUMMARY.md">All results and references</a>.</figcaption></figure></section>
<section class="card"><h2>Where the evidence draws the boundary</h2><p>All six independent Procrustes point differences are negative, with intervals crossing zero. All-paid FiQA/E5 loses to Procrustes and LA2M; MiniLM versus ridge is unresolved. Actual mixed replacement can reverse proxy-only ordering. E5 native Full-X can exceed Full-Y, so retaining an incumbent may be the better quality choice.</p><p>ARC2 is a candidate for a required destination-space migration with a small declared fit set and a preference for a compact non-neural map. The actual endpoint and relevance/Recall targets should determine adoption. Physical migration cost, SLO, ANN and real traffic are unmeasured.</p></section>
<section class="card"><h2>How to inspect this release</h2><p><a href="CLAIM_LOCK.md">Frozen claim</a> · <a href="README.md">Folder guide</a> · <a href="REPRODUCE.md">Reproduction commands</a> · <a href="provenance/aris_b2/001-claim-review.response.md">ARIS review</a></p><p><code>python reproduce/verify_review_release.py --root . --mode full</code></p><p>Independently recompute saved relevance metrics and uncertainty, exercise the frozen method on synthetic inputs, and rebuild figures offline. The original project, backup disks, server credentials and manuscript are unnecessary for these commands.</p><p class="muted">ARIS verdict: partial, same-family/provisional. Computational and visual QA: PASS. Formal manuscript audit and manuscript writing remain separate.</p></section><footer>No manuscript was changed or packaged. No scientific run, retuning or omitted baseline is hidden by this release. Large-vector regeneration and a fresh H100 deployment are outside the tested portable-review scope.</footer></main></html>''')
    # Readability of generated English prose: retain literal paths/commands, add
    # spacing in narrative text where templates use compact numeric notation.
    replacements = {'dated1November2026': 'dated 1 November 2026', 'Python3.12': 'Python 3.12',
                    'tested3.12.10': 'tested 3.12.10', 'all184': 'all 184', 'The30': 'The 30',
                    'yield11': 'yield 11', ',19unresolved': ', 19 unresolved', 'and0negative': 'and 0 negative',
                    'final384': 'final 384', 'has295,680': 'has 295,680', 'coefficients,1,182': 'coefficients, 1,182',
                    'all28,819': 'all 28,819', '736DEV': '736 DEV', '239,200metric': '239,200 metric',
                    '184B2': '184 B2', '18,400metric': '18,400 metric', 'locked20,000': 'locked 20,000',
                    'has11family': 'has 11 family', ',19unresolved': ', 19 unresolved', ',0family': ', 0 family',
                    'on31October20:12:17UTC': 'on 31 October 20:12:17 UTC', '1November03:12:17': '1 November 03:12:17',
                    'separate184': 'separate 184', 'all60galleries': 'all 60 galleries', 'generate184rankings': 'generate 184 rankings',
                    'H100MIG20GB,171,332documents and50queries': 'H100 MIG20GB, 171,332 documents and 50 queries',
                    'had685,328document': 'had 685,328 document', 'about13h24m': 'about 13h24m',
                    'Under1,024fitting': 'Under 1,024 fitting', 'for384→768': 'for 384→768',
                    'seeds,25/50/75%backfill;736rankings': 'seeds, 25/50/75% backfill; 736 rankings',
                    '171,332documents,50queries,184sealed': '171,332 documents, 50 queries, 184 sealed',
                    'frozen30-comparison': 'frozen 30-comparison', 'has11positive': 'has 11 positive',
                    'All30primary': 'All 30 primary', 'approximate95%Bonferroni': 'approximate 95% Bonferroni'}
    for name in ('README.md', 'CLAIM_LOCK.md', 'REPRODUCE.md', 'START_HERE.html'):
        p = OUT / name; text = p.read_text(encoding='utf-8')
        for a, b in replacements.items():
            text = text.replace(a, b)
        put(name, text)
    print('Release claim, supervisor summary and reproduction guide written.')


if __name__ == '__main__':
    main()
