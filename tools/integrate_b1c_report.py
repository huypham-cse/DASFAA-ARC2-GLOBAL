"""Build the current consolidated report from completed, verified DEV evidence.

No ranking, qrel, fitting or scientific selection is performed here. Historical
result bundles remain read-only; the active report is a generated navigation view.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'results/b1c_r3_review_20261031'
PRIMARY = 'arc2_global_tangent2_r1'
LABELS = {
    PRIMARY: 'ARC2-Global', 'procrustes_global': 'A2M / Procrustes adaptation',
    'la2m20_integration_script_adaptation': 'LA2M20 adaptation',
    'simplelinear_official_final50_mlp5': 'SimpleLinear official code, 5-layer MLP',
    'ridge_affine_l10_bias_regularized': 'Affine ridge, lambda10',
    'embedding_converter_paper_spec': 'Embedding-Converter paper-spec adaptation',
}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    source = BUNDLE / 'evidence/run/scoring/summary.json'
    summary = read(source)
    receipts = [read(p) for p in BUNDLE.glob('qa_completed_*.json')]
    matching = [q for q in receipts if q.get('status') == 'PASS'
                and q.get('summary_sha256') == hashlib.sha256(source.read_bytes()).hexdigest()]
    if not matching:
        raise ValueError('No matching completed local verification receipt')
    lines = ['# ARC2-Global: current consolidated results', '',
        'Updated 31 October 2026. **The complete B1c-R3 DEV matrix is scored and locally verified.**', '',
        'With 1,024 shared fitting anchors, ARC2-Global has higher aggregate nDCG@10 than all five '
        'declared external baseline configurations across four inspected development collections. '
        'All five predeclared macro comparison intervals exclude zero in its favor. '
        'This supports a bounded quality claim; the all-paid and Recall results below define its limits.', '',
        '[Complete six-method report and figures](results/b1c_r3_review_20261031/SUMMARY.md) | '
        '[Raw scored summary](results/b1c_r3_review_20261031/evidence/run/scoring/summary.json) | '
        '[Current claim review](CLAIMS_FROM_RESULTS.md) | '
        '[Execution tracker](refine-logs/EXPERIMENT_TRACKER.md).', '',
        '## Complete fixed-anchor comparison', '',
        'NanoNQ (5,035 documents, 50 queries), NanoHotpotQA (5,090/50), NanoFEVER (4,996/50), '
        'FiQA (57,638/500); two encoder pairs, five seeds and 25/50/75% paid-document budgets. '
        'Both pairs map 384 to 768 dimensions: MiniLM to DistilRoBERTa and E5-small to E5-base. '
        'The method is frozen at two tangent updates and lambda10; no local residual or neural training.', '',
        f"All {summary['ranking_cells']} cells are present: {summary['imported_cells']} retained and "
        f"{summary['new_cells']} new rankings, with 118 fresh fit groups and two saved-fit reuse groups. "
        'The 38 displaced historical FiQA cells and earlier interrupted attempts remain provenance. '
        'R3 completion does not relabel those old attempts as successful.', '',
        'Each contrast below equally weights the 24 dataset/pair/budget strata after averaging five seeds. '
        'The locked 20,000-draw query bootstrap uses 99% intervals per nDCG comparison, giving approximate '
        '95% coverage for the five-comparison family. Per-condition and Recall intervals are descriptive. '
        'Higher mean counts are not counts of statistically significant wins.', '',
        '| ARC2 minus baseline | Absolute nDCG@10 delta | 99% interval | Higher/lower/tied means, out of24 |',
        '|---|---:|---|---:|']
    for row in summary['aggregate_contrasts']:
        metric = row['ndcg10']; lo, hi = metric['ci_bonferroni_family95']
        conditions = [c for c in summary['condition_contrasts'] if c['right'] == row['right']]
        counts = [sum(c['ndcg10']['delta'] > 0 for c in conditions),
                  sum(c['ndcg10']['delta'] < 0 for c in conditions),
                  sum(c['ndcg10']['delta'] == 0 for c in conditions)]
        lines.append(f"| {LABELS[row['right']]} | {metric['delta']:+.6f} | [{lo:+.6f}, {hi:+.6f}] | {'/'.join(map(str,counts))} |")
    proc = next(c for c in summary['aggregate_contrasts'] if c['right'] == 'procrustes_global')
    r = proc['recall100']; lo, hi = r['ci95']
    lines += ['', f"The overall Recall@100 difference against Procrustes is {r['delta']:+.6f} "
        f"(descriptive95% interval [{lo:+.6f}, {hi:+.6f}]), which is unresolved. "
        'The sole lower nDCG condition mean against Procrustes is FiQA/E5 at75%; E5 Recall also has losses. '
        'All24 partial ARC2 nDCG means are below both native Full-X and Full-Y references. '
        'This statement concerns nDCG: Recall is above Full-X in8/24 conditions and above Full-Y in1/24.', '',
        'Procrustes/A2M and LA2M20 are the declared adaptations; SimpleLinear uses official upstream code '
        'with the locked five-layer/final50-epoch training policy. Embedding-Converter is a paper-spec '
        'adaptation with 50,000 selection steps and a selected-length fresh refit, trained on the same1,024 '
        'paired anchors. These results do not reproduce its published multi-corpus training setting. '
        'Full-X uses its native query/document encoder and is an incumbent reference; Full-Y is the '
        'destination-native reference, not a mathematical upper bound.', '',
        '## Mechanism and supervision controls', '',
        'B1-M ablations are a separate completed DEV study. Its five-comparison interval family differs '
        'from the B1c external-baseline family, so their intervals must not be interchanged.', '',
        '| B1-M contrast | Absolute nDCG@10 delta | 99% family interval |', '|---|---:|---|']
    mechanism = read(ROOT / 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json')
    aliases = {PRIMARY: 'ARC2-Global', 'tangent1_l10': 'one tangent step',
               'tangent2_l1': 'two steps, lambda1', 'tangent2_l100': 'two steps, lambda100',
               'procrustes_global': 'Procrustes', 'ridge_affine_l10_bias_regularized': 'affine ridge'}
    for row in mechanism['overall_macro']:
        m = row['ndcg10']; lo, hi = m['ci99_bonferroni_family95']
        lines.append(f"| {aliases[row['left']]} minus {aliases[row['right']]} | {m['delta']:+.6f} | [{lo:+.6f}, {hi:+.6f}] |")
    lines += ['', 'B1-P0 verified the all-paid numerical backend against the frozen reference. '
        'B1-P then gave every method all28,819 already-paid pairs on FiQA50%, removing the withheld-supervision '
        'objection at that operating point. The outcome is encoder-dependent:', '',
        '| All-paid FiQA50% method | MiniLM nDCG@10 | E5 nDCG@10 |', '|---|---:|---:|']
    paid = read(ROOT / 'results/b1p_r5_review_20261027/scoring/results_summary.json')
    lookup = {(r['pair'], r['method']): r for r in paid['means'] if r['regime'] == 'allpaid28819'}
    for method, label in LABELS.items():
        values = [lookup[(pair, method)]['ndcg10']['mean'] for pair in ('minilm_distilroberta', 'e5_small_base')]
        lines.append(f"| {label} | {values[0]:.6f} | {values[1]:.6f} |")
    lines += ['', 'MiniLM ARC2 has positive family-adjusted nDCG comparisons against four configurations; '
        'the ridge comparison is unresolved. E5 ARC2 is below Procrustes and LA2M with all paid pairs. '
        'The fixed-anchor result does not establish best use of every available paid pair.', '',
        '[All-paid report, all32 contrasts and retained failures](results/b1p_r5_review_20261027/SUMMARY.md).', '',
        '## Mixed-gallery behavior', '',
        'B1-G reused frozen galleries to compare pure proxies with actual mixed endpoints. '
        'For all-paid FiQA/E5 at50%, five-seed nDCG means are:', '',
        '| Method | Pure-proxy diagnostic | Mixed endpoint | Mixed minus proxy |', '|---|---:|---:|---:|']
    gallery = read(ROOT / 'results/b1g_r1_review_20261027/scoring/results_summary.json')
    for method in (PRIMARY, 'procrustes_global', 'ridge_affine_l10_bias_regularized'):
        row = next(r for r in gallery['aggregate_five_seed_conditions']
                   if r['pair'] == 'e5_small_base' and r['method'] == method and r['regime'] == 'allpaid28819')
        m = row['metrics']['ndcg10']
        lines.append(f"| {LABELS[method]} | {m['before']['mean']:.6f} | {m['after']['mean']:.6f} | {m['delta_of_query_means']['mean']:+.6f} |")
    lines += ['', 'Thus better pure-proxy quality can reverse after true-vector replacement. The score/share '
        'diagnostics suggest a compatibility hypothesis; they do not prove a unique cause or a calibration fix. '
        'The pure-proxy endpoint is a diagnostic counterfactual, not a zero-encoding deployment.', '',
        '[Complete mixed-gallery evidence](results/b1g_r1_review_20261027/SUMMARY.md).', '',
        '## Use case, efficiency and limits', '',
        'The supported use case is a required destination-space migration with a small declared fitting set '
        'and partial native backfill. ARC2 offers a simple affine forward map with empirical aggregate '
        'nDCG gains over the declared fixed-anchor alternatives. Evaluate the actual mixed endpoint before '
        'cutover, especially when more paired data or E5 encoders are available. A relevance/Recall target '
        'can favor a different method or retaining the incumbent.', '',
        'For384-to768 dimensions, the final affine map has295,680 float32 coefficients including bias '
        '(1,182,720 bytes, approximately1.128MiB). This is algebraic coefficient storage only, excluding '
        'fitting objects; ridge is equally compact and Procrustes similarly compact. No neural training '
        'is required for ARC2. Cached destination exposure counts unique documents as|A union S|, anchors '
        'included. These measurements performed zero new physical document encodings. No dollar saving, '
        'isolated H100 cost, serving SLO or real-traffic gain is established.', '',
        '## Verification and finite next step', '',
        'All736 compact rankings were rescored locally using a separate metric implementation and the '
        'locked DEV qrels;239,200 metric values agree within3.33e-16. The locked20,000-draw means/intervals '
        'agree within4.44e-16. The compact bundle verifies scoring evidence, not regeneration from all '
        'model checkpoints/vectors; full backup has a separate completion receipt.', '',
        'The full six-method DEV comparison is finished. Final D1 and its scope are recorded in '
        '[CLAIMS_FROM_RESULTS.md](CLAIMS_FROM_RESULTS.md). **STOP before B2/TREC-COVID or systems execution** '
        'until the user reviews the completed result. TREC labels remain closed. If released, the existing '
        'plan calls for one prospective184-cell/30-contrast confirmation, then the mapper paper and claim '
        'audit. B3/B4 remain conditional rather than automatic requirements.', '',
        'Raw results, negative outcomes and failed/interrupted runs remain authoritative; the manuscript '
        'still needs the completed DEV evidence integrated before it can be treated as a current paper.', '']
    backup_path = ROOT / 'provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json'
    if backup_path.exists():
        backup = read(backup_path)
        if backup['status'] != 'COMPLETE_CAMPAIGN_BACKED_UP' or backup['pending']:
            raise ValueError('Terminal backup receipt does not establish completion')
        lines += [f"The current B1c-R3 full/smoke/schedule output backup is complete on D: "
                  f"{backup['files']:,} files, {backup['bytes']:,} verified bytes "
                  '(approximately64.48GB), zero pending files. This backup scope does not include '
                  'every historical project or source/runtime cache. '
                  '[Terminal backup receipt](provenance/qa/b1c_r3_terminal_backup_receipt_20261031.json).', '']
    (ROOT / 'REPORT.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
