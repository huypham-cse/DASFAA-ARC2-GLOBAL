"""Expand the supervisor packet from audited saved evidence; no scientific run."""
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import hashlib

SRC = Path(__file__).resolve().parents[1]
ROOT = SRC.with_name('DASFAA-2027-paper-release')
REV = 'supervisor-review-20261101-r2-completeness'


def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))


def put(p, text):
    (ROOT / p).write_text(text.strip() + '\n', encoding='utf-8', newline='\n')


def interval(v):
    keys = [k for k in v if 'bonferroni' in k]
    assert len(keys) == 1, keys
    lo, hi = v[keys[0]]
    return f"{v['delta']:+.6f} [{lo:+.6f}, {hi:+.6f}]"


def main():
    M = read('results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json')
    P = read('results/b1p_r5_review_20261027/scoring/results_summary.json')
    G = read('results/b1g_r1_review_20261027/scoring/results_summary.json')
    C = read('results/b1c_r3_review_20261031/evidence/run/scoring/summary.json')
    assert M['ranking_cells'] == C['ranking_cells'] == 736 and P['ranking_cells'] == 124
    lines = ['# Complete experiment atlas — ARC2-Global', '',
        'Revision **r2-completeness**, 1 November2026. This is a saved-evidence review packet before paper writing. The original r1 ZIP remains unchanged; no numerical method, ranking, label exposure, threshold or scientific protocol changed.', '',
        '## 1. Exact experiment coverage', '',
        '**1,340 unique planned logical quality cells =736 main DEV +360 additional ablation cells +60 additional all-paid cells +184 independent cells.** There are1,320partial cells and20native references. Five seeds, budgets, shared queries and reused historical rankings do not create1,340independent statistical observations.', '',
        '| Block | Completed measurement | Increment to disjoint quality union | Status / location |',
        '|---|---|---:|---|',
        '| B0 historical import |64 inspected FiQA rankings, all original byte versions retained |0, subset of main identities |[Imported evidence](results/fiqa_development/summary.json); source import/extraction manifests in provenance/ |',
        '| B1a input / encoder readiness |60 nested paid sets,4encoder repeat tests,2toy galleries,4dimension parity cases |0 |[Readiness report](results/b1a_r1_20261025/SUMMARY.md) |',
        '| B1b external-adapter correctness |25LA2M oracle fixtures,15ridge cases,5official-code SimpleLinear comparisons |0 |[Baseline validation](results/b1b_20261026/SUMMARY.md) |',
        '| B1c main DEV |736rankings:720partial +16native; six methods, four collections, two pairs, three budgets, five seeds |736 |[All six-method results](results/b1c_r3_review_20261031/SUMMARY.md) |',
        '| B1-M mechanism/sensitivity |736rankings, including360extra one-step/lambda1/lambda100 identities |360 |[Mechanism report](results/b1mp0_r1_review_20261026/SUMMARY.md) |',
        '| B1-P0 backend parity |31synthetic fixtures/62updates;40real fit identities/120budget checks; zero top100 drift |0 |[P0 included with M](results/b1mp0_r1_review_20261026/SUMMARY.md) |',
        '| B1-P paid-pair supervision |124rankings:60fixed +60allpaid +4native; same FiQA50% destination budget |60 |[All-paid report](results/b1p_r5_review_20261027/SUMMARY.md) |',
        '| B1-G mixed-gallery diagnostics |450paired replacement cases,210pure galleries,90five-seed conditions; no new fits |0; diagnostic counterfactuals counted separately |[All diagnostics](results/b1g_r1_review_20261027/SUMMARY.md) |',
        '| B2 prospective TREC-COVID |184rankings,60fits, separate prelabel endpoint replay and one-shot scoring |184 |[Independent report](results/b2_review_20261101/SUMMARY.md) |',
        '| B3 / B4 physical100K and traffic replay |Not run; conditional systems route |0 |No cost/SLO/real-traffic claim |', '',
        'The five source indices I/M/P/C/B have1,844rows, with504repeated logical identities. An equivalent chronological union is64+692+80+320+184=1,340. Main-first disjoint counting above is easier to read. Native references are deduplicated across seeds/methods. B1c and M both contain736rows but compare different method panels; adding the two totals directly would double-count376identities. P overlaps main in64identities.', '',
        'Collections: NanoNQ5,035documents/50queries; NanoHotpotQA5,090/50; NanoFEVER4,996/50; FiQA57,638/500 inspected DEV; TREC-COVID171,332/50 prospective. Sum of corpus entries across collections:244,091, not a claim of globally distinct text documents. MS MARCO100K, ORCAS and AOL replay are unrun conditional work. Both real encoder pairs are384→768 (MiniLM→DistilRoBERTa and E5-small→E5-base).', '',
        '## 2. Mechanism and sensitivity — all five saved macro comparisons', '',
        '| Left minus right | nDCG delta [saved99% interval; five-comparison family] |', '|---|---:|']
    for row in M['overall_macro']:
        lines.append(f"| {row['left']} minus {row['right']} | {interval(row['ndcg10'])} |")
    lines += ['', 'The second update contributes about0.006924aggregate nDCG beyond one step. Lambda1 is unresolved versus the locked lambda10; lambda100 is worse. The method remains lambda10/two steps, with no post-score parameter selection or independent one-step necessity claim.', '',
        '![All mechanism controls](results/control_figures/b1m_mechanism_controls.png)', '',
        'P0 is correctness evidence: stored coefficient difference up to7.27595761418e-12 and normalized proxy difference3.72529029846e-09 were recorded; zero ordered top100 changes across120real budget checks. This is tolerance-validated numerical parity, not byte-identical coefficients, new quality evidence or physical cost.', '',
        '## 3. All-paid fitting — complete matched external comparisons', '',
        'FiQA50% gives28,819paid destination pairs to every compared all-paid mapper; fitting only1,024of them is a different supervision regime, not the same experiment. The top panels below compare all-paid ARC2 against all-paid baselines. The bottom panels retain fixed ARC2 versus all-paid competitors. All32original contrasts remain in the detailed report;20are drawn in the figure.', '',
        '| Pair | All-paid ARC2 minus all-paid baseline | nDCG delta [saved32-comparison family interval] |', '|---|---|---:|']
    for row in P['contrasts']:
        if row['kind'] == 'arc2_allpaid_vs_baseline_allpaid':
            lines.append(f"| {row['pair']} | {row['right']['method']} | {interval(row['ndcg10'])} |")
    lines += ['', '**MiniLM all-paid ARC2 has four positive family comparisons; ridge is unresolved.** E5 loses to Procrustes/LA2M, beats the declared SimpleLinear/ridge configurations, and is unresolved versus Converter. Fixed1024MiniLM ARC2 is below all five all-paid comparators. Thus the positive result and the supervision limit are both visible.', '',
        '![All-paid and fixed-fit comparisons](results/control_figures/b1p_allpaid_controls.png)', '',
        '## 4. Mixed-gallery diagnostics — actual replacement can reverse ordering', '',
        'The original450cases reuse210fitted galleries. R2 includes unchanged raw top100 outputs for210proxy-only galleries and450mixed endpoints in a short content-addressed layout, along with all saved metric arrays and90seed-averaged conditions. The verification independently rescores those rankings; it does not rerun full vector search, fit models or regenerate sampled score-error distributions.', '',
        '![All six methods, both pairs, FiQA50 all-paid diagnostic](results/control_figures/b1g_proxy_mixed_controls.png)', '',
        'For all-paid FiQA/E5 at50%, ARC2 proxy-only nDCG0.314908 becomes0.291867; Procrustes0.286096 becomes0.336202; ridge0.270585 becomes0.227015. A better proxy-only ranking can therefore become a worse mixed endpoint. This is descriptive evidence, not proof of a unique calibration cause or a repair. The figure displays all six methods for both pairs in that fixed view; the CSV retains all90conditions.', '',
        '## 5. Full quality includes Recall and native references', '',
        '| DEV macro ARC2 minus baseline | nDCG mean delta | Recall mean delta [nominal descriptive95%] |', '|---|---:|---:|']
    for row in C['aggregate_contrasts']:
        recall = row['recall100']; lo, hi = recall['ci95']
        lines.append(f"| {row['right']} | {row['ndcg10']['delta']:+.6f} | {recall['delta']:+.6f} [{lo:+.6f}, {hi:+.6f}] |")
    lines += ['', 'All five DEV nDCG macro family comparisons favor ARC2. Overall DEV Recall versus Procrustes is unresolved; E5 Recall losses and the FiQA/E5/75%nDCG negative mean remain reported. In B2, nDCG family decisions are11positive/19unresolved/0negative. Recall versus Procrustes has2positive,3negative and1unresolved nominal intervals; all three E5 Recall intervals are negative. These nominal Recall decisions are not interchangeable with the30-comparison nDCG family.', '',
        'Native Full-X exceeds Full-Y on both NanoHotpotQA pairs, both NanoFEVER pairs and TREC/E5. A required migration may still be the operational scenario, but the destination model is not assumed to improve relevance. All native references remain visible; cutover is not automatically warranted.', '',
        '## 6. What the first release missed, and what is repaired', '',
        '- **Presentation:** it foregrounded736main DEV +184independent rows and hid the360extra ablation and60all-paid identities in subsidiary reports. Quantitative M/P/G results now have dedicated sections and three new figures.',
        '- **Historical bytes:** ten original Converter25%FiQA rankings were absent, although their logical conditions had current R3 versions. All64original imported ranking hashes and all38displaced historical byte versions are now preserved. Historical versions are not counted as new logical conditions.',
        '- **Validation/history:** raw B1a/B1b validation, all available compact failed/smoke bundles, import/source seals and supporting QA are added. Old STOP strings inside immutable reports describe their original dates; this atlas is the current coverage guide.',
        '- **G reproducibility:** r1 only provided scored arrays/tables. R2 adds all660saved raw G ranking records with their hashes and group binding contexts, enabling independent relevance rescoring. Large vectors, model checkpoints, sampled score arrays and new vector-search regeneration remain outside the lightweight scope.', '',
        'No data was newly tuned or selected, no negative result removed, no final collection reopened over the network, and no manuscript changed. Earlier interrupted runs remain interrupted. Original r1 ZIP is preserved for comparison.', '',
        '## 7. Verification and review status', '',
        'Run `python reproduce/verify_review_release.py --root . --mode full` for hashes plus main736DEV/184B2rankings and their locked bootstrap. Run `python reproduce/verify_control_families.py --root .` for all736M/124Prankings, their declared means/intervals, and all210pure/450mixed G raw rankings and saved metric arrays. Run `python reproduce/verify_experiment_inventory.py --root .` for the1,340logical union and historical coverage.', '',
        'Saved-control render: `python reproduce/render_release_controls.py --root .` writes fresh figures under checks/. Original source/results remain frozen. See checks/ for final receipts and provenance/completeness_audit/ for the audited source inventory.', '',
        'The earlier completed B2 semantic verdict remains partial/same-family/provisional. A new zero-context release-claim reviewer completed numerical checks but hit the account usage limit before a final semantic verdict. That fresh review is recorded as REVIEW_UNAVAILABLE, not PASS. This packet is for supervisor fact-checking, not a submission-ready claim-audit certificate. No further scientific experiment is launched.']
    text = '\n'.join(lines)
    # Keep generated narrative readable without changing paths or scientific values.
    for a, b in [('1 November2026','1 November 2026'), ('There are1,320partial','There are 1,320 partial'),
                 ('and20native','and 20 native'), ('create1,340independent','create 1,340 independent'),
                 ('about0.006924aggregate','about 0.006924 aggregate'), ('across120real','across 120 real'),
                 ('normalized proxy difference3.','normalized proxy difference 3.'), ('up to7.','up to 7.'),
                 ('FiQA50%','FiQA 50%'), ('gives28,819paid','gives 28,819 paid'), ('only1,024of','only 1,024 of'),
                 ('fixed1024MiniLM','fixed-1,024 MiniLM'), ('original450cases reuse210fitted','original 450 cases reuse 210 fitted'),
                 ('for210proxy-only','for 210 proxy-only'), ('and450mixed','and 450 mixed'), ('all90conditions','all 90 conditions')]:
        text = text.replace(a, b)
    put('EXPERIMENT_ATLAS.md', text)
    c = read('CLAIM_LOCK.json'); c['claim_revision'] = REV
    c.pop('no_results_removed', None)
    c['complete_experiment_coverage'] = {'main_DEV': 736, 'extra_mechanism': 360, 'extra_allpaid': 60,
        'independent_B2': 184, 'unique_quality_cells': 1340, 'G_diagnostic_cases_separate': 450,
        'original_FiQA_versions_retained': 64, 'B3_B4': 'not run / conditional'}
    c['fresh_release_semantic_audit'] = 'REVIEW_UNAVAILABLE: account quota interrupted final reviewer verdict; deterministic numerical/inventory checks retained.'
    put('CLAIM_LOCK.json', json.dumps(c, indent=2))
    for name in ['CLAIM_LOCK.md', 'README.md', 'REPRODUCE.md']:
        t = (ROOT / name).read_text(encoding='utf-8').replace('supervisor-review-20261101-r1', REV)
        t = t.replace('B1-G has all reported scored diagnostics and tables here, but its sampled-vector replay inputs remain in the original project. Its historical QA is preserved; the portable verifier does not claim to regenerate those omitted vectors.', 'R2 also includes all660saved G top100 ranking records, independently rescored by verify_control_families.py. Full vector/search and sampled-score reconstruction remain outside the portable scope.')
        t = t.replace('B1-G scored diagnostics are hash/anchor checked, not fully regenerated from omitted sampled-vector inputs.', 'B1-G relevance metrics are independently rescored from all210pure/450mixed saved rankings. Full vector search and sampled score-error distributions are not regenerated.')
        lead = '\n\n**R2 completeness audit:** [EXPERIMENT_ATLAS.md](EXPERIMENT_ATLAS.md) lists every completed block, the1,340-cell union, supporting correctness tests, repaired historical omissions and unrun conditional systems work. Three added control figures expose the M/P/G evidence. Fresh semantic release audit was interrupted by quota; numerical/inventory evidence is provided for supervisor checking.\n'
        t = t.replace(lead, '\n')
        i = t.index('\n'); t = t[:i] + lead + t[i:]
        if name == 'REPRODUCE.md':
            t += '\n## Additional complete controls and inventory\n\n```bash\npython reproduce/verify_control_families.py --root .\npython reproduce/verify_experiment_inventory.py --root .\npython reproduce/render_release_controls.py --root .\n```\n\nThe control verifier checks all saved M/P relevance rankings and intervals plus G raw-ranking metrics/arrays. The inventory checker counts logical identities separately from historical file versions and diagnostic counterfactuals.\n'
        put(name, t)
    t = (ROOT / 'START_HERE.html').read_text(encoding='utf-8')
    banner = '<section class="card"><h2>Complete evidence: 1,340 logical quality cells</h2><p><b>736 main DEV +360 additional ablation +60 additional all-paid +184 prospective test cells.</b> Reused rows are deduplicated. Separately: 450 mixed-gallery diagnostic cases and correctness/readiness tests. These are not independent statistical observations.</p><p><a href="EXPERIMENT_ATLAS.md">Open the complete experiment atlas</a> · <a href="provenance/completeness_audit/experiment_inventory.md">Source-to-package inventory</a></p></section>'
    if '<h2>Complete evidence: 1,340' not in t:
            t = t.replace('<section class="card"><h2>Development evidence</h2>', banner + '<section class="card"><h2>Development evidence</h2>', 1)
    controls = '<section class="card"><h2>Mechanism, all-paid supervision and actual mixed galleries</h2><p>The previous cover underreported these completed studies. All five mechanism macro comparisons, all32paid-supervision contrasts and all90mixed conditions are available in the atlas and linked raw reports.</p>'
    for file, title in [('b1m_mechanism_controls','Zero/one/two steps and lambda sensitivity'), ('b1p_allpaid_controls','MiniLM all-paid ARC2 wins four comparisons; E5 defines the limit'), ('b1g_proxy_mixed_controls','Proxy-only ordering can reverse after actual vector replacement')]:
        controls += f'<h3>{title}</h3><figure><a href="results/control_figures/{file}.pdf"><img src="results/control_figures/{file}.png" alt="{title}"></a></figure>'
    controls += '<p>All-paid results use the same28,819paid pairs for every all-paid baseline. DEV evidence remains inspected. Recall and nDCG have different outcomes; no cost/SLO benefit is inferred.</p></section>'
    if '<h2>Mechanism, all-paid supervision' not in t:
            t = t.replace('<section class="card"><h2>Where the evidence draws the boundary</h2>', controls + '<section class="card"><h2>Where the evidence draws the boundary</h2>', 1)
    t = t.replace('ARIS verdict: partial, same-family/provisional. Computational and visual QA: PASS. Formal manuscript audit and manuscript writing remain separate.', 'Earlier completed B2 ARIS verdict: partial, same-family/provisional. R2 numerical/inventory checks are recorded separately. A fresh semantic release audit was interrupted by account quota and has no final PASS verdict. Formal manuscript audit and writing remain separate.')
    put('START_HERE.html', t)
    for folder in ['.aris/traces/research-review/2026-11-01_release_completeness', '.aris/traces/paper-claim-audit/2026-11-01_supervisor_release']:
        out = ROOT / 'provenance/completeness_audit'; out.mkdir(exist_ok=True)
        for p in (SRC / folder).iterdir():
            if p.is_file() and p.suffix in ('.json', '.md', '.py'):
                shutil.copyfile(p, out / p.name)
    shutil.copyfile(SRC / 'tools/render_release_controls.py', ROOT / 'reproduce/render_release_controls.py')
    print('R2 experiment atlas and expanded supervisor overview written; original numerical claims unchanged.')


if __name__ == '__main__':
    main()
