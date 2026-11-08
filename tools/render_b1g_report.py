"""Render verified B1-G descriptive tables and a publication figure.

Usage: python tools/render_b1g_report.py [--bundle results/b1g_r1_review_20261027]
Requires the completed local PASS receipt before reading results or writing outputs.
Reads saved diagnostics/metrics only; never imports a scorer or reads qrels/vectors.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / 'results/b1g_r1_review_20261027'
QA = ROOT / 'provenance/qa/b1g_completed_verification_r2_20261027.json'
PRIMARY = 'arc2_global_tangent2_r1'
PROC = 'procrustes_global'
RIDGE = 'ridge_affine_l10_bias_regularized'
METHODS = {
    PRIMARY: 'ARC2-Global', PROC: 'A2M / Procrustes adaptation',
    RIDGE: 'Affine ridge, lambda10',
    'la2m20_integration_script_adaptation': 'LA2M20 adaptation',
    'simplelinear_official_final50_mlp5': 'Official SimpleLinear (5-layer MLP)',
    'embedding_converter_paper_spec': 'Embedding-Converter adaptation',
}
PAIRS = ('minilm_distilroberta', 'e5_small_base')
CONDITION_KEYS = ('dataset', 'pair', 'method', 'regime', 'budget')
STRATA = ('all', 'anchor', 'paid_nonanchor', 'unpaid')
SEEDS = [17, 29, 41, 53, 67]
PALETTE = {PRIMARY: '#0F4D92', PROC: '#B64342', RIDGE: '#42949E'}
BASE = 'b1g_mixed_gallery_diagnostics'


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def mean(values):
    values = list(values)
    if any(value is None for value in values):
        return None
    if not values or not all(math.isfinite(value) for value in values):
        raise ValueError('Nonfinite/empty descriptive mean')
    return math.fsum(values) / len(values)


def condition(row):
    return tuple(row[key] for key in CONDITION_KEYS)


def verified_summary(bundle):
    qa = read_json(QA)
    if qa.get('status') != 'PASS':
        raise ValueError('Completed local verification must have status PASS before rendering')
    if 'bundle' in qa and Path(qa['bundle']).resolve() != bundle:
        raise ValueError('Verification receipt belongs to a different bundle')
    summary_path = bundle / 'scoring/results_summary.json'
    summary = read_json(summary_path)
    if (summary.get('status'), summary.get('partial_cases'), summary.get('pure_fitted_galleries')) != (
            'B1G_DEV_SCORED', 450, 210):
        raise ValueError('Require completed finite B1-G results')
    if summary['metrics'] != ['ndcg10', 'recall100']:
        raise ValueError('Unexpected metric axes')
    completed = read_json(bundle / 'scoring/completed.json')
    if completed['status'] != 'B1G_DEV_SCORED':
        raise ValueError('Scoring completion receipt missing')
    if completed['artifact_sha256']['results_summary.json'] != digest(summary_path):
        raise ValueError('Scoring summary differs from its completed artifact hash')
    if any(completed[key] != summary[key] for key in ('code_commit', 'lock_sha256')):
        raise ValueError('Scoring completion binding differs')
    grouped = defaultdict(list)
    rows = summary['case_diagnostics_and_metrics']
    if len(rows) != 450 or len({row['case_id'] for row in rows}) != 450:
        raise ValueError('Missing/duplicate partial cases')
    for row in rows:
        if row['method'] not in METHODS or row['pair'] not in PAIRS or row['sample_documents'] != 512:
            raise ValueError('Unexpected method/pair/sample population')
        grouped[condition(row)].append(row)
    aggregates = summary['aggregate_five_seed_conditions']
    if len(grouped) != 90 or len(aggregates) != 90 or {condition(a) for a in aggregates} != set(grouped):
        raise ValueError('Require all 90 five-seed conditions')
    for aggregate in aggregates:
        cases = grouped[condition(aggregate)]
        if sorted(row['seed'] for row in cases) != SEEDS or aggregate['seeds'] != SEEDS:
            raise ValueError('Five-seed condition is incomplete')
        for metric in ('ndcg10', 'recall100'):
            for endpoint in ('before', 'after'):
                calculated = mean(row['metrics'][metric][endpoint] for row in cases)
                if abs(calculated - aggregate['metrics'][metric][endpoint]['mean']) > 1e-12:
                    raise ValueError('Aggregate differs from saved case means')
    for shard, counts in [('main', (137, 377)), ('mini', (73, 73))]:
        seal = read_json(bundle / shard / 'diagnostics_seal.json')
        if seal['status'] != 'B1G_DIAGNOSTICS_SEALED' or (seal['expected_groups'], seal['expected_cases']) != counts:
            raise ValueError('Incomplete source shard')
        if seal['code_commit'] != summary['code_commit'] or seal['lock_sha256'] != summary['lock_sha256']:
            raise ValueError('Source/scoring identity mismatch')
    return summary, grouped


def flat_case(row):
    value = {key: row[key] for key in ('case_id', 'group_id', 'dataset', 'pair', 'method', 'regime', 'budget', 'seed')}
    value['method_label'] = METHODS[row['method']]
    value['sample_documents'] = row['sample_documents']
    for metric in ('ndcg10', 'recall100'):
        for endpoint in ('before', 'after'):
            value[f'{metric}_{endpoint}'] = row['metrics'][metric][endpoint]
        value[f'{metric}_delta'] = row['metrics'][metric]['delta']['mean']
    for key, item in row['counts'].items():
        value['population_count_' + key] = item
    for key, item in row['population_fractions'].items():
        value['population_fraction_' + key] = item
    for endpoint in ('before', 'after'):
        for top in ('top10', 'top100'):
            for group, item in row['returned_shares'][endpoint][top].items():
                value[f'{endpoint}_{top}_fraction_{group}'] = item
    for top in ('top10', 'top100'):
        for key, item in row['rank_changes'][top].items():
            value[f'{top}_{key}'] = item
    for stratum in STRATA:
        stats = row['paired_strata'][stratum]
        for key in ('documents', 'query_document_observations', 'signed_bias', 'mae', 'rmse', 'score_std_ratio'):
            value[f'paired_{stratum}_{key}'] = stats[key]
        for kind in ('proxy_score', 'true_score', 'error', 'proxy_true_cosine'):
            for key in ('mean', 'std', 'min', 'max'):
                value[f'paired_{stratum}_{kind}_{key}'] = stats[kind][key]
            for probability, item in stats[kind]['quantiles'].items():
                value[f'paired_{stratum}_{kind}_q{probability}'] = item
    for endpoint in ('proxy', 'true'):
        for key in ('mean_direction_norm', 'mean_offdiagonal_cosine'):
            value[f'{endpoint}_{key}'] = row[endpoint + '_direction'][key]
    return value


def write_csv(path, rows):
    columns = list(dict.fromkeys(key for row in rows for key in row))
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def aggregate_table(grouped):
    rows = []
    for key, cases in sorted(grouped.items()):
        flattened = [flat_case(case) for case in sorted(cases, key=lambda case: case['seed'])]
        row = dict(zip(CONDITION_KEYS, key))
        row.update(method_label=METHODS[row['method']], seeds='17;29;41;53;67', seed_count=5,
                   aggregation='equal mean of five saved per-seed summaries; not pooled uncertainty')
        for name, item in flattened[0].items():
            if isinstance(item, (int, float)) and name != 'seed':
                row[name] = mean(case[name] for case in flattened)
        rows.append(row)
    return rows


def make_figure(table, folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib import font_manager
    import numpy as np
    available_fonts = {entry.name for entry in font_manager.fontManager.ttflist}
    font_stack = [name for name in ('Arial', 'Helvetica', 'DejaVu Sans') if name in available_fonts]
    plt.rcParams.update({'font.family': font_stack or ['sans-serif'],
        'font.size': 15, 'axes.linewidth': 2, 'axes.spines.top': False, 'axes.spines.right': False,
        'legend.frameon': False, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'axes.labelsize': 14, 'xtick.labelsize': 10.5, 'ytick.labelsize': 11})
    chosen = [row for row in table if row['dataset'] == 'FiQA' and row['budget'] == '50pct'
              and row['method'] in (PRIMARY, PROC, RIDGE)]
    lookup = {(row['pair'], row['regime'], row['method']): row for row in chosen}
    if len(lookup) != 12:
        raise ValueError('Figure requires exactly 12 fixed/all-paid FiQA50 conditions')
    ordering = [(regime, method) for regime in ('fixed1024', 'allpaid28819') for method in (PRIMARY, PROC, RIDGE)]
    figure_rows = [lookup[(pair, regime, method)] for pair in PAIRS for regime, method in ordering]
    write_csv(folder / (BASE + '.csv'), figure_rows)
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
    x = np.arange(6)
    colors = [PALETTE[method] for _, method in ordering]
    labels = [f"{'1,024' if regime == 'fixed1024' else '28,819'}\n{label}"
              for regime in ('fixed1024', 'allpaid28819') for label in ('ARC2', 'Proc.', 'Ridge')]
    ndcg_max = max(row['ndcg10_' + endpoint] for row in chosen for endpoint in ('before', 'after'))
    bias_extent = max(abs(row['paired_unpaid_signed_bias']) for row in chosen)
    for index, pair in enumerate(PAIRS):
        rows = [lookup[(pair, regime, method)] for regime, method in ordering]
        for column, (before_key, after_key) in enumerate([
                ('ndcg10_before', 'ndcg10_after'), (None, None),
                ('before_top10_fraction_paid', 'after_top10_fraction_paid')]):
            ax = axes[index, column]
            ax.axvline(2.5, color='#CFCECE', lw=1.2, zorder=0)
            if column != 1:
                for position, row, color in zip(x, rows, colors):
                    a, b = row[before_key], row[after_key]
                    ax.plot([position, position], [a, b], color=color, lw=2.2, zorder=2)
                    ax.scatter(position, a, marker='o', facecolors='white', edgecolors=color, s=54, lw=1.8, zorder=3)
                    ax.scatter(position, b, marker='o', color=color, s=42, zorder=4)
            else:
                ax.axhline(0, color='#767676', lw=1.2, zorder=0)
                bars = ax.bar(x, [row['paired_unpaid_signed_bias'] for row in rows],
                              width=.62, color=colors, edgecolor='#272727', linewidth=.8)
                for position in range(3, 6):
                    bars[position].set_hatch('//')
            ax.set_xlim(-.6, 5.6)
            ax.set_xticks(x, labels)
            ax.tick_params(axis='x', length=0)
            if index == 1:
                ax.set_xlabel('Fitting pairs (50% encoding budget)', fontsize=11.5, labelpad=9)
            if column == 0:
                ax.set_ylim(0, min(1, max(.05, ndcg_max * 1.16)))
                ax.set_ylabel('nDCG@10')
            elif column == 1:
                extent = max(.001, bias_extent * 1.22)
                ax.set_ylim(-extent, extent)
                ax.set_ylabel('Proxy score − true score')
                ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
            else:
                if any(abs(row['population_fraction_paid'] - .5) > 1e-12 for row in rows):
                    raise ValueError('FiQA50 population reference is not 50%')
                ax.axhline(.5, color='#767676', ls='--', lw=1.5, zorder=1)
                ax.set_ylim(0, 1)
                ax.set_ylabel('Paid fraction in top-10')
            ax.set_title(f"({chr(97 + index * 3 + column)}) " +
                         ('Retrieval before / after' if column == 0 else 'Unpaid paired score bias' if column == 1 else 'Returned paid share'),
                         fontsize=14, loc='left', pad=10)
        axes[index, 0].text(-.21, .5, 'MiniLM → DistilRoBERTa' if index == 0 else 'E5-small → E5-base',
                            transform=axes[index, 0].transAxes, rotation=90, ha='center', va='center', fontsize=13)
    handles = [Line2D([], [], color='#272727', marker='o', markerfacecolor='white', lw=0, label='Before: pristine proxy'),
               Line2D([], [], color='#272727', marker='o', lw=0, label='After: paid true replacement'),
               Line2D([], [], color='#767676', ls='--', label='Paid population: 50%')]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.5, 1.01), ncol=3, fontsize=12)
    fig.tight_layout(pad=2, rect=(.025, .03, 1, .97))
    fig.text(.5, .012, 'FiQA DEV · five-seed means · same original fit at both endpoints · descriptive, no calibration or uncertainty intervals',
             ha='center', fontsize=10.5)
    for extension in ('pdf', 'svg', 'png'):
        fig.savefig(folder / (BASE + '.' + extension), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return {'matplotlib': matplotlib.__version__, 'numpy': np.__version__,
            'font_path': font_manager.findfont(font_manager.FontProperties(family=plt.rcParams['font.family'])),
            'figure_size_inches': [15, 8], 'raster_dpi': 300, 'figure_conditions': 12,
            'colors': PALETTE, 'intervals': 'none; descriptive five-seed means'}


def markdown(table, summary):
    def fmt(value, signed=False):
        return 'NA' if value is None else format(value, '+.6f' if signed else '.6f')
    lines = ['# B1-G completed: mixed-gallery development diagnostics', '',
        '**450 partial cases, 210 pristine fitted galleries, 90 five-seed conditions; all six methods retained.**', '',
        'The four collections are already inspected DEV: FiQA (500 queries) and NanoNQ, NanoHotpotQA, '
        'NanoFEVER (50 queries each). Every case retains all queries and five seeds. '
        'No new fit, encoding, calibration, confidence interval or significance test was performed.', '',
        '“Before” uses the saved mapper prediction for every document, including anchors. '
        '“After” replaces exactly the original anchor-inclusive paid set with true destination vectors '
        'and reproduces its published mixed ranking. The mapper and its original fitting exposure stay fixed '
        'between endpoints; an all-paid fit already used the paid target pairs before this counterfactual. '
        'Metric delta is after minus before. No independent or physical-cost result follows from these diagnostics.', '',
        'The original local verification failure is preserved: its historical-metric path comparison treated '
        'relative and resolved absolute paths differently. The separate R2 verification corrects that local '
        'path comparison; raw results, rankings, scoring and protocol remain unchanged.', '',
        'Paired errors compare proxy and true scores for the same query and each of 512 label-independent sampled '
        'documents. “Unpaid bias” is mean proxy minus true score within the sampled unpaid stratum, averaged '
        'equally over seeds. Strata and their sample sizes remain separate. Returned-share imbalance or anisotropy '
        'does not establish miscalibration or causally explain relevance changes. Negative effects remain reported.', '',
        '[Publication figure](figures/' + BASE + '.pdf) · [PNG preview](figures/' + BASE + '.png) · '
        '[Editable SVG](figures/' + BASE + '.svg) · [Figure data](figures/' + BASE + '.csv)', '',
        'The figure shows a FiQA50 overview subset, chosen before B1-G result inspection '
        '(ARC2, Procrustes, ridge; both fitting regimes and encoder pairs); full tables retain all conditions. '
        'The tables below cover the full finite diagnostic scope. Numbers are five-seed means; no intervals are implied.', '',
        '| Dataset | Pair | Method | Fit | Budget | nDCG before | after | Δ | Recall before | after | Δ | Unpaid bias | Paid top10 before | after |',
        '|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in table:
        values = [row['dataset'], 'MiniLM' if row['pair'] == PAIRS[0] else 'E5', METHODS[row['method']],
                  'Fixed1024' if row['regime'] == 'fixed1024' else 'All-paid', row['budget']]
        values += [fmt(row[key], key.endswith('_delta') or key == 'paired_unpaid_signed_bias') for key in (
            'ndcg10_before', 'ndcg10_after', 'ndcg10_delta', 'recall100_before', 'recall100_after', 'recall100_delta',
            'paired_unpaid_signed_bias', 'before_top10_fraction_paid', 'after_top10_fraction_paid')]
        lines.append('| ' + ' | '.join(values) + ' |')
    lines += ['', '[All diagnostic columns, 90 conditions](diagnostic_tables.csv) · '
              '[All 450 seed cases](diagnostic_cases.csv) · [Saved scoring summary](scoring/results_summary.json) · '
              '[Rendering provenance](figures/' + BASE + '_provenance.json)', '',
        'The CSVs retain paid/proxy populations and top10/top100 shares, overlap and changed-query counts, '
        'all four paired strata, errors/quantiles, score dispersion and direction summaries. Condition CSV fields '
        'are equal means of saved per-seed summaries, including counts; consult the case CSV for integer counts '
        'and the sealed source artifacts for per-query arrays. Empty or undefined quantities are blank/NA. '
        'No equal-stratum population estimate is constructed.', '',
        'Paid populations count unique destination documents |A ∪ S|, anchors included. Cached true vectors '
        'and proxy diagnostics are not fresh physical encoding work, a dollar estimate, or an SLO measurement. '
        'Nano results are for the published Nano collections. TREC remains outside this campaign.', '',
        f"Generation/scoring commit: `{summary['code_commit']}`; lock SHA256: `{summary['lock_sha256']}`.", '',
        'STOP after B1-G analysis and the separate ARIS/D1 record. No automatic breadth, TREC or systems campaign.', '']
    return '\n'.join(lines)


def render(bundle=DEFAULT_BUNDLE):
    bundle = Path(bundle).resolve()
    summary, grouped = verified_summary(bundle)
    table = aggregate_table(grouped)
    case_table = [flat_case(row) for row in sorted(summary['case_diagnostics_and_metrics'],
                                                  key=lambda row: (*condition(row), row['seed']))]
    folder = bundle / 'figures'
    folder.mkdir(exist_ok=True)
    write_csv(bundle / 'diagnostic_tables.csv', table)
    write_csv(bundle / 'diagnostic_cases.csv', case_table)
    style = make_figure(table, folder)
    (bundle / 'SUMMARY.md').write_text(markdown(table, summary), encoding='utf-8', newline='\n')
    inputs = [QA, Path(__file__), bundle / 'scoring/results_summary.json', bundle / 'scoring/completed.json',
              bundle / 'main/diagnostics_seal.json', bundle / 'mini/diagnostics_seal.json']
    outputs = [bundle / 'SUMMARY.md', bundle / 'diagnostic_tables.csv', bundle / 'diagnostic_cases.csv']
    outputs += [folder / (BASE + suffix) for suffix in ('.csv', '.pdf', '.svg', '.png')]
    provenance = {'status': 'RENDERED_FROM_VERIFIED_RESULTS', 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'bundle': str(bundle), 'generation_code_commit': summary['code_commit'], 'lock_sha256': summary['lock_sha256'],
        'inputs_sha256': {str(path.resolve()): digest(path) for path in inputs},
        'outputs_sha256': {path.relative_to(bundle).as_posix(): digest(path) for path in outputs},
        'python': platform.python_version(), 'style': style, 'new_scientific_computation': False,
        'data_processing': 'descriptive aggregation of saved metrics/diagnostics only',
        'visual_qa': 'PENDING: inspect PNG and vector exports for clipping, labels and correspondence to CSV',
        'figure_skill': 'D:/graph4paper/figures4papers/scientific-figure-making/SKILL.md',
        'figure_demo': 'D:/graph4paper/figures4papers/figure_ImmunoStruct/plot_bars.py'}
    (folder / (BASE + '_provenance.json')).write_text(json.dumps(provenance, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': provenance['status'], 'bundle': str(bundle), 'conditions': len(table),
                      'cases': len(case_table), 'visual_qa': provenance['visual_qa']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=DEFAULT_BUNDLE)
    render(parser.parse_args().bundle)
