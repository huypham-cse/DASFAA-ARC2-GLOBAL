"""Render the complete B1c R3 DEV report from independently verified saved scores.

No scorer, labels, fitting, selection or resampling is invoked. All intervals
come directly from the frozen scorer. --qa must identify a completed PASS receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / 'results/b1c_r3_review_20261031'
DEFAULT_QA = DEFAULT_BUNDLE / 'qa_completed_20261031T060049161714Z.json'
PRIMARY = 'arc2_global_tangent2_r1'
METHODS = {
    PRIMARY: 'ARC2-Global',
    'procrustes_global': 'A2M / Procrustes adaptation',
    'la2m20_integration_script_adaptation': 'LA2M20 adaptation',
    'simplelinear_official_final50_mlp5': 'SimpleLinear official code (5-layer MLP)',
    'ridge_affine_l10_bias_regularized': 'Affine ridge, lambda10',
    'embedding_converter_paper_spec': 'Embedding-Converter adaptation',
}
SHORT = dict(zip(METHODS, ('ARC2', 'Procrustes', 'LA2M20', 'SimpleLinear', 'Ridge', 'Converter')))
BASELINES = tuple(m for m in METHODS if m != PRIMARY)
PAIRS = ('minilm_distilroberta', 'e5_small_base')
PAIR_LABELS = ('MiniLM → DistilRoBERTa', 'E5-small → E5-base')
DATASETS = ('NanoNQ', 'NanoHotpotQA', 'NanoFEVER', 'FiQA')
BUDGETS = ('25pct', '50pct', '75pct')
METRICS = ('ndcg10', 'recall100')
COLORS = dict(zip(METHODS, ('#0F4D92', '#B64342', '#5B9B59', '#9A4D8E', '#42949E', '#A17C25')))


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def average(values):
    values = list(values)
    if not values or not all(math.isfinite(v) for v in values):
        raise ValueError('Empty or nonfinite descriptive aggregate')
    return math.fsum(values) / len(values)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8', newline='\n')


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(k for r in rows for k in r)), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def verified_summary(bundle, qa_path):
    qa = read_json(qa_path)
    if qa.get('status') != 'PASS':
        raise ValueError('Independent completed QA must PASS before rendering')
    evidence = bundle / 'evidence'
    candidates = list(evidence.rglob('summary.json'))
    candidates = [p for p in candidates if read_json(p).get('stage') == 'B1c-R3']
    if len(candidates) != 1:
        raise ValueError('Require exactly one completed B1c-R3 summary')
    path = candidates[0]
    summary = read_json(path)
    completed = read_json(path.with_name('completed.json'))
    if (summary.get('status'), summary.get('ranking_cells'), summary.get('imported_cells'), summary.get('new_cells')) != ('DEV_SCORED', 736, 378, 358):
        raise ValueError('Incomplete R3 matrix')
    if completed.get('status') != 'DEV_SCORED' or completed.get('summary_sha256') != digest(path):
        raise ValueError('Summary does not match completed scorer receipt')
    # The verifier must name this summary hash somewhere in its signed-by-hash inputs.
    if digest(path) not in json.dumps(qa):
        raise ValueError('QA receipt does not bind the exact saved summary SHA256')
    if len(summary['means']) != 160 or len(summary['condition_contrasts']) != 120 or len(summary['aggregate_contrasts']) != 5:
        raise ValueError('Require all means, references and comparisons')
    lookup = {(r['dataset'], r['pair'], r['budget'], r['method']): r for r in summary['means']}
    expected = {(d, p, b, m) for d in DATASETS for p in PAIRS for b in BUDGETS for m in METHODS}
    expected |= {(d, p, 'full', m) for d in DATASETS for p in PAIRS for m in ('full_x', 'full_y')}
    if set(lookup) != expected or len(lookup) != 160:
        raise ValueError('Means do not cover exactly 144 partial +16 reference conditions')
    for row in summary['means']:
        for metric in METRICS:
            if not math.isfinite(row[metric]['mean']):
                raise ValueError('Nonfinite saved mean')
    return summary, path, lookup


def means_table(summary):
    rows = []
    for row in summary['means']:
        flat = {k: row[k] for k in ('dataset', 'pair', 'budget', 'method')}
        flat['method_label'] = METHODS.get(row['method'], row['method'].replace('_', '-').title() + ' native reference')
        flat['scope'] = 'native full reference' if row['budget'] == 'full' else 'fixed 1024 anchors; five-seed mean'
        for metric in METRICS:
            v = row[metric]
            for name in ('mean', 'seed_std', 'full_y_retention', 'delta_from_full_y'):
                flat[f'{metric}_{name}'] = v.get(name)
            flat[f'{metric}_seed_min'], flat[f'{metric}_seed_max'] = v['seed_range'] or (None, None)
            flat[f'{metric}_ci95_low'], flat[f'{metric}_ci95_high'] = v['ci95']
        rows.append(flat)
    return rows


def contrasts_table(contrasts, macro=False):
    rows = []
    for row in contrasts:
        flat = {k: row[k] for k in ('dataset', 'pair', 'budget', 'left', 'right') if k in row}
        flat['baseline_label'] = METHODS[row['right']]
        flat['strata'] = row.get('strata', 1)
        for metric in METRICS:
            v = row[metric]
            flat[f'{metric}_delta'] = v['delta']
            flat[f'{metric}_ci95_low'], flat[f'{metric}_ci95_high'] = v['ci95']
            flat[f'{metric}_ci95_status'] = v['interval_interpretation']
            flat[f'{metric}_ci95_scope'] = 'nominal 95%; descriptive'
            if 'ci_bonferroni_family95' in v:
                flat[f'{metric}_family_low'], flat[f'{metric}_family_high'] = v['ci_bonferroni_family95']
                flat[f'{metric}_family_status'] = v['family_interval_interpretation']
                flat[f'{metric}_family_scope'] = '99% individual; approximate 95% five-comparison family'
            if 'mapping_seed_variability' in v:
                seed = v['mapping_seed_variability']
                flat[f'{metric}_seed_delta_std'] = seed['seed_std']
                flat[f'{metric}_seed_delta_min'], flat[f'{metric}_seed_delta_max'] = seed['seed_range']
        rows.append(flat)
    return rows


def derive(summary, lookup):
    counts = []
    grouped = []
    for method in BASELINES:
        cases = [r for r in summary['condition_contrasts'] if r['right'] == method]
        row = {'baseline': method, 'baseline_label': METHODS[method], 'conditions': len(cases)}
        for metric in METRICS:
            signs = Counter('higher' if r[metric]['delta'] > 0 else 'lower' if r[metric]['delta'] < 0 else 'tied' for r in cases)
            row[metric] = {k: signs[k] for k in ('higher', 'lower', 'tied')}
        counts.append(row)
        for axis, values in (('pair', PAIRS), ('dataset', DATASETS)):
            for value in values:
                selected = [r for r in cases if r[axis] == value]
                grouped.append({'axis': axis, 'value': value, 'baseline': method,
                    'conditions': len(selected), **{metric + '_delta': average(r[metric]['delta'] for r in selected) for metric in METRICS},
                    'interpretation': 'descriptive equal-condition mean; no new interval or significance test'})
    reference_counts = {}
    for metric in METRICS:
        reference_counts[metric] = {}
        for reference in ('full_x', 'full_y'):
            signs = Counter()
            for d in DATASETS:
                for p in PAIRS:
                    ref = lookup[d, p, 'full', reference][metric]['mean']
                    for b in BUDGETS:
                        delta = lookup[d, p, b, PRIMARY][metric]['mean'] - ref
                        signs['higher' if delta > 0 else 'lower' if delta < 0 else 'tied'] += 1
            reference_counts[metric][reference] = dict(signs)
    macro_means = []
    for method in METHODS:
        chosen = [r for r in summary['means'] if r['method'] == method]
        macro_means.append({'method': method, 'conditions': len(chosen),
            **{metric: average(r[metric]['mean'] for r in chosen) for metric in METRICS}})
    negatives = [{k: r[k] for k in ('dataset', 'pair', 'budget', 'right')} | {metric: r[metric]['delta'] for metric in METRICS}
                 for r in summary['condition_contrasts'] if any(r[m]['delta'] < 0 for m in METRICS)]
    return {'status': 'DESCRIPTIVE_DERIVED_FROM_VERIFIED_SAVED_SCORES', 'sign_counts': counts,
        'pair_and_dataset_deltas': grouped, 'arc2_vs_native_reference_sign_counts': reference_counts,
        'equal_24_condition_method_means': macro_means, 'negative_condition_comparisons_either_metric': negatives,
        'uncertainty': 'All plotted intervals are copied from scorer; no new bootstrap, CI or p-value computed.'}


def style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': [f for f in ('Arial', 'Helvetica', 'DejaVu Sans') if f in available],
        'font.size': 10, 'axes.linewidth': 1.1, 'axes.spines.top': False, 'axes.spines.right': False,
        'legend.frameon': False, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'axes.labelsize': 10, 'xtick.labelsize': 8.5, 'ytick.labelsize': 8.5})
    return plt, {'matplotlib': matplotlib.__version__, 'font_path': font_manager.findfont(font_manager.FontProperties(family=plt.rcParams['font.family'])),
        'colors': COLORS, 'dpi': 300, 'figure_skill': 'D:/graph4paper/figures4papers/scientific-figure-making/SKILL.md',
        'demo': 'D:/graph4paper/figures4papers/figure_ophthal_review/plot_trend.py'}


def save_figure(fig, folder, name):
    paths = []
    for extension in ('pdf', 'svg', 'png'):
        path = folder / f'{name}.{extension}'
        fig.savefig(path, dpi=300, facecolor='white', bbox_inches='tight', pad_inches=.05)
        paths.append(path)
    return paths


def quality_figure(plt, lookup, folder, metric='ndcg10'):
    from matplotlib.lines import Line2D
    from matplotlib.ticker import MaxNLocator
    fig, axes = plt.subplots(2, 4, figsize=(12.5, 6.3), sharex=True)
    markers = ('o', 's', '^', 'D', 'v', 'P')
    styles = ('-', '--', '-.', ':', '--', '-.')
    figure_rows = []
    for i, pair in enumerate(PAIRS):
        for j, dataset in enumerate(DATASETS):
            ax = axes[i, j]
            values = []
            for method, marker, line in zip(METHODS, markers, styles):
                rows = [lookup[dataset, pair, b, method] for b in BUDGETS]
                ys = [r[metric]['mean'] for r in rows]
                values.extend(ys)
                ax.plot((25, 50, 75), ys, color=COLORS[method], marker=marker, ls=line,
                    lw=2.1 if method == PRIMARY else 1.25, markersize=4.6 if method == PRIMARY else 3.4,
                    zorder=5 if method == PRIMARY else 3)
                figure_rows.extend({'dataset': dataset, 'pair': pair, 'budget': b, 'method': method, 'metric': metric,
                    'mean': r[metric]['mean']} for b, r in zip(BUDGETS, rows))
            for reference, color, line in (('full_x', '#272727', '--'), ('full_y', '#767676', ':')):
                v = lookup[dataset, pair, 'full', reference][metric]['mean']
                values.append(v)
                ax.axhline(v, color=color, ls=line, lw=1.25, zorder=1)
                figure_rows.append({'dataset': dataset, 'pair': pair, 'budget': 'full', 'method': reference, 'metric': metric, 'mean': v})
            low, high = min(values), max(values)
            span = max(high - low, .04)
            ax.set_ylim(max(0, low - span * .10), min(1, high + span * .12))
            ax.set_xlim(21, 79)
            ax.set_xticks((25, 50, 75), ('25%', '50%', '75%'))
            ax.yaxis.set_major_locator(MaxNLocator(4))
            ax.grid(axis='y', color='#E9E9E9', linewidth=.6, zorder=0)
            ax.set_title(f'({chr(97 + i*4+j)}) {dataset}', loc='left', fontsize=10.5, pad=6)
            if j == 0:
                ax.set_ylabel(('nDCG@10' if metric == 'ndcg10' else 'Recall@100'))
            if i == 1:
                ax.set_xlabel('Destination encoding budget', fontsize=9)
    handles = [Line2D([], [], color=COLORS[m], marker=mk, ls=ls, lw=1.8 if m == PRIMARY else 1.3,
                     markersize=4, label=SHORT[m]) for m, mk, ls in zip(METHODS, markers, styles)]
    handles += [Line2D([], [], color='#272727', ls='--', label='Native Full-X'), Line2D([], [], color='#767676', ls=':', label='Native Full-Y')]
    fig.legend(handles=handles, ncol=4, loc='upper center', bbox_to_anchor=(.52, 1.005), columnspacing=1.6, handlelength=2.2, fontsize=9)
    fig.text(.008, .70, PAIR_LABELS[0], rotation=90, ha='left', va='center', fontsize=10)
    fig.text(.008, .285, PAIR_LABELS[1], rotation=90, ha='left', va='center', fontsize=10)
    fig.tight_layout(pad=1.1, rect=(.025, .045, 1, .89))
    fig.text(.52, .012, 'Inspected DEV · fixed 1,024 anchors · five-seed means · |A ∪ S| includes anchors · panel y-ranges differ', ha='center', fontsize=8.5)
    name = 'b1c_r3_quality_budget' if metric == 'ndcg10' else 'b1c_r3_recall_budget'
    paths = save_figure(fig, folder, name)
    plt.close(fig)
    write_csv(folder / f'{name}.csv', figure_rows)
    return paths + [folder / f'{name}.csv']


def contrast_figure(plt, summary, folder):
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    fig = plt.figure(figsize=(12.2, 8.2))
    grid = fig.add_gridspec(1, 2, width_ratios=(1, 1.48), wspace=.48)
    ax = fig.add_subplot(grid[0, 0])
    macro = {r['right']: r for r in summary['aggregate_contrasts']}
    for y, method in enumerate(BASELINES):
        v = macro[method]['ndcg10']
        lo, hi = v['ci_bonferroni_family95']
        ax.plot([lo, hi], [y, y], color='#0F4D92', lw=2)
        ax.scatter(v['delta'], y, color='#0F4D92', s=36, zorder=3)
        ax.text(0.98, y+.19, f"{v['delta']:+.4f} [{lo:+.4f}, {hi:+.4f}]", transform=ax.get_yaxis_transform(),
                ha='right', va='top', fontsize=8.5, color='#4D4D4D')
    ax.axvline(0, color='#767676', ls='--', lw=1)
    ax.set_yticks(range(5), [SHORT[m] for m in BASELINES])
    ax.set_ylim(4.7, -.7)
    maxhigh = max(macro[m]['ndcg10']['ci_bonferroni_family95'][1] for m in BASELINES)
    ax.set_xlim(-.008, maxhigh * 1.08)
    ax.set_xlabel('Macro Δ nDCG@10 (ARC2 − baseline)')
    ax.set_title('(a) Five predeclared macro contrasts', loc='left', fontsize=11, pad=13)
    fig.text(.10, .105, '99% individual percentile intervals\nBonferroni: approximate 95% five-comparison family\nEqual weight: 24 dataset × pair × budget strata',
             va='top', fontsize=8.5, linespacing=1.45)
    heat = fig.add_subplot(grid[0, 1])
    order = [(d, p, b) for p in PAIRS for d in DATASETS for b in BUDGETS]
    lookup = {(r['dataset'], r['pair'], r['budget'], r['right']): r['ndcg10']['delta'] for r in summary['condition_contrasts']}
    matrix = np.array([[lookup[d, p, b, m] for m in BASELINES] for d, p, b in order])
    cmap = LinearSegmentedColormap.from_list('negative_white_arc2blue', ['#B64342', '#FFFFFF', '#0F4D92'])
    limit = float(np.max(np.abs(matrix)))
    im = heat.imshow(matrix, aspect='auto', cmap=cmap, norm=TwoSlopeNorm(0, vmin=-limit, vmax=limit))
    heat.set_xticks(range(5), [SHORT[m] for m in BASELINES], rotation=28, ha='right', fontsize=9)
    heat.set_yticks(range(24), [f"{'MiniLM' if p == PAIRS[0] else 'E5'} · {d} · {b[:2]}%" for d,p,b in order], fontsize=8)
    for y in (2.5, 5.5, 8.5, 11.5, 14.5, 17.5, 20.5):
        heat.axhline(y, color='white', lw=1.2 if y != 11.5 else 2.5)
    for (y,x), value in np.ndenumerate(matrix):
        heat.text(x,y,f'{value:+.3f}',ha='center',va='center',fontsize=7.2,
                  color='#B64342' if value < 0 else 'white' if abs(value) > limit * .56 else '#272727',
                  fontweight='bold' if value < 0 else 'normal')
    heat.set_title('(b) All 120 condition mean differences', loc='left', fontsize=11, pad=13)
    for spine in heat.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=heat, shrink=.52, pad=.025, fraction=.035)
    cbar.set_label('Δ nDCG@10', fontsize=9)
    cbar.ax.tick_params(labelsize=8)
    fig.subplots_adjust(left=.10, right=.96, bottom=.22, top=.94)
    fig.text(.52,.012,'Inspected DEV · negative differences retained in red · condition means are descriptive, without family-tested claims',ha='center',fontsize=8.5)
    paths = save_figure(fig, folder, 'b1c_r3_macro_and_condition_deltas')
    plt.close(fig)
    return paths


def markdown(summary, derived, summary_path, bundle):
    def signed(value):
        return f'{value:+.6f}'
    proc = 'procrustes_global'
    negative_ndcg = [r for r in summary['condition_contrasts'] if r['ndcg10']['delta'] < 0]
    if len(negative_ndcg) != 1:
        raise ValueError('Revisit interpretation if the frozen negative-condition count changes')
    negative = negative_ndcg[0]
    e5_recall = next(r['recall100_delta'] for r in derived['pair_and_dataset_deltas']
        if r['axis'] == 'pair' and r['value'] == PAIRS[1] and r['baseline'] == proc)
    overall_recall = next(r['recall100']['delta'] for r in summary['aggregate_contrasts'] if r['right'] == proc)
    refs = derived['arc2_vs_native_reference_sign_counts']
    lines = ['# B1c R3 complete six-method development report', '',
        '**COMPLETE; 736 scored rankings, 144 partial condition means, 16 native references, 120 matched condition contrasts.**', '',
        'Four inspected DEV collections (FiQA: 57,638 documents / 500 queries; NanoNQ: 5,035 / 50; '
        'NanoHotpotQA: 5,090 / 50; NanoFEVER: 4,996 / 50), two encoder pairs, five seeds '
        '(17, 29, 41, 53, 67), and 25% / 50% / 75% budgets. All six methods use the same '
        'fixed 1,024 anchor pairs. Unique logical destination document exposure is |A ∪ S|; anchors count. '
        'No new physical document encoding was performed in this recovery.', '',
        'R3 retains 378 frozen rankings and adds 358 sealed rankings from 118 fresh fits plus two saved fits. '
        'The 38 displaced historical FiQA cells and failed/interrupted attempts remain preserved; '
        'the prospective R3 cells consistently replace each affected gallery at all three budgets. '
        'The separate scorer opened only the four locked DEV sources after the complete seal. TREC remains closed.', '',
        '[Quality–budget figure](figures/b1c_r3_quality_budget.pdf) · [PNG](figures/b1c_r3_quality_budget.png) · '
        '[SVG](figures/b1c_r3_quality_budget.svg) · [Recall counterpart](figures/b1c_r3_recall_budget.pdf) · '
        '[Macro intervals and every condition delta](figures/b1c_r3_macro_and_condition_deltas.pdf)', '',
        'The quality figure shows all six methods and native Full-X / Full-Y references across all eight '
        'dataset/pair panels. Each curve is a five-seed mean; panel y-ranges differ. Native Full-X uses '
        'the incumbent query/document encoder; native Full-Y uses the target encoder throughout. These are '
        'separate full-corpus reference operating points, and Full-Y is not a mathematical upper bound.', '',
        '## Predeclared macro comparison', '',
        'ARC2 minus each baseline, equally weighting all 24 dataset × pair × budget conditions after '
        'averaging the five mapping seeds. Every nDCG interval below is the saved 99% percentile interval '
        'for the predeclared five-comparison Bonferroni family (approximate 95% family coverage). '
        'Recall intervals are nominal 95% descriptive. The 20,000 draws independently resample queries '
        'within datasets and share each dataset’s query indices across pairs, budgets, methods and metrics. '
        'No p-values or new uncertainty calculations are introduced.', '',
        '| ARC2 minus baseline | Δ nDCG@10 [99% family interval] | Δ Recall@100 [descriptive 95%] |',
        '|---|---:|---:|']
    for row in summary['aggregate_contrasts']:
        n, r = row['ndcg10'], row['recall100']
        nl, nh = n['ci_bonferroni_family95']
        rl, rh = r['ci95']
        lines.append(f"| {METHODS[row['right']]} | {signed(n['delta'])} [{signed(nl)}, {signed(nh)}] | {signed(r['delta'])} [{signed(rl)}, {signed(rh)}] |")
    lines += ['', 'All five macro nDCG family intervals are above zero. This supports a fixed-supervision '
        'development advantage averaged over the locked matrix. It does not imply dominance in each '
        'condition, an independent confirmation, or superiority under all-paid supervision.', '',
        '## All condition signs retained', '',
        'Counts compare point means across the 24 matched conditions per baseline; they are descriptive '
        'higher/lower/tied counts, not 120 family-tested wins. Exact zero defines a tie.', '',
        '| Baseline | nDCG higher / lower / tied | Recall higher / lower / tied |', '|---|---:|---:|']
    for row in derived['sign_counts']:
        counts = [' / '.join(str(row[m][s]) for s in ('higher','lower','tied')) for m in METRICS]
        lines.append(f"| {row['baseline_label']} | {' | '.join(counts)} |")
    for axis, title in (('pair','Encoder-pair macro deltas'), ('dataset','Dataset macro deltas')):
        lines += ['', '### ' + title, '', 'Equal-weight descriptive averages of the saved condition deltas; no new intervals or tests.', '',
                  '| Scope | Baseline | Δ nDCG@10 | Δ Recall@100 |', '|---|---|---:|---:|']
        for row in derived['pair_and_dataset_deltas']:
            if row['axis'] == axis:
                label = PAIR_LABELS[PAIRS.index(row['value'])] if axis == 'pair' else row['value']
                lines.append(f"| {label} | {SHORT[row['baseline']]} | {signed(row['ndcg10_delta'])} | {signed(row['recall100_delta'])} |")
    lines += ['', '## Interpretation and preserved limits', '',
        f"- ARC2 partial-condition nDCG means are below native Full-X in {refs['ndcg10']['full_x'].get('lower', 0)}/24 "
        f"conditions and Full-Y in {refs['ndcg10']['full_y'].get('lower', 0)}/24. "
        f"Recall exceeds Full-X in {refs['recall100']['full_x'].get('higher', 0)}/24 conditions and "
        f"Full-Y in {refs['recall100']['full_y'].get('higher', 0)}/24, so these references are not upper bounds. "
        f"{negative['dataset']} / E5 / {negative['budget'][:2]}% is the sole negative ARC2-minus-Procrustes nDCG point contrast "
        f"({signed(negative['ndcg10']['delta'])}). The E5 Recall macro difference versus Procrustes is {signed(e5_recall)}; "
        f"the overall Recall difference is {signed(overall_recall)} with a descriptive interval crossing zero. "
        'Every negative condition contrast remains in the full tables and figure data.',
        '- The existing [FiQA all-paid B1-P experiment](../b1p_r5_review_20261027/SUMMARY.md) remains material: '
        'E5 all-paid ARC2 trails Procrustes and LA2M in family nDCG comparisons; MiniLM versus all-paid ridge is '
        'unresolved. Additional fitting pairs are not uniformly beneficial. B1c fixed-anchor averages do not erase that evidence.',
        '- Procrustes is a mathematical A2M adaptation; LA2M20 is an integration-script adaptation. '
        'SimpleLinear uses pinned official code with the five-layer MLP and final 50 epochs. '
        'Embedding-Converter is a paper-spec adaptation with 1,024 paired anchors. These are qualified implementations, '
        'not original-paper reproduction claims.',
        '- ARC2 stays centered rectangular Procrustes with lambda=10 and exactly two tangent updates, '
        'without local residual or neural fitting. No post-score method, seed, budget or subset selection was performed.',
        '- Fit/map/search resource receipts reflect shared-load execution on the recorded H100 MIG instance. '
        'They do not establish isolated accelerator performance, physical dollar savings, real-traffic behavior, '
        'SLO improvement or a causal explanation of mixed-gallery effects.', '',
        '## Complete tables and provenance', '',
        '[All 144 partial means and 16 references](condition_means.csv) · '
        '[All 120 matched condition contrasts](condition_contrasts.csv) · '
        '[Five macro contrasts](macro_contrasts.csv) · [Derived descriptive analysis](derived_analysis.json) · '
        f'[Frozen scorer summary]({summary_path.relative_to(bundle).as_posix()}) · '
        '[Rendering provenance](figures/b1c_r3_render_provenance.json)', '',
        'CSV means retain mapping-seed SD/range, saved nominal query-bootstrap intervals, Full-Y retention '
        'and deltas. All queries count, including zero-positive queries; nDCG@10 uses graded 2^rel−1 gain, '
        'and Recall@100 divides by all positive qrels, including positives outside a Nano corpus. '
        'Condition intervals are nominal 95% descriptive, outside the five macro nDCG family. '
        'An interval crossing or touching zero is unresolved, not evidence of equivalence.', '',
        f"Scorer commit: `{summary['scorer_code_commit']}`. Lock SHA256: `{summary['lock_sha256']}`. "
        f"Ranking seal SHA256: `{summary['ranking_seal_sha256']}`.", '',
        '**STOP after the separately recorded final D1 review. No B2, TREC, systems campaign or method switch is authorized here.**', '']
    return '\n'.join(lines)


def render(bundle, qa_path):
    bundle, qa_path = bundle.resolve(), qa_path.resolve()
    summary, summary_path, lookup = verified_summary(bundle, qa_path)
    folder = bundle / 'figures'
    folder.mkdir(exist_ok=True)
    table = means_table(summary)
    contrasts = contrasts_table(summary['condition_contrasts'])
    macro = contrasts_table(summary['aggregate_contrasts'], macro=True)
    derived = derive(summary, lookup)
    derived['source_summary_sha256'] = digest(summary_path)
    write_csv(bundle / 'condition_means.csv', table)
    write_csv(bundle / 'condition_contrasts.csv', contrasts)
    write_csv(bundle / 'macro_contrasts.csv', macro)
    write_csv(bundle / 'pair_dataset_deltas.csv', derived['pair_and_dataset_deltas'])
    write_json(bundle / 'derived_analysis.json', derived)
    (bundle / 'SUMMARY.md').write_text(markdown(summary, derived, summary_path, bundle), encoding='utf-8', newline='\n')
    plt, style_info = style()
    outputs = quality_figure(plt, lookup, folder)
    outputs += quality_figure(plt, lookup, folder, 'recall100')
    outputs += contrast_figure(plt, summary, folder)
    outputs += [bundle / name for name in ('condition_means.csv','condition_contrasts.csv','macro_contrasts.csv',
                'pair_dataset_deltas.csv','derived_analysis.json','SUMMARY.md')]
    provenance = {'status': 'RENDERED_FROM_INDEPENDENTLY_VERIFIED_SAVED_SCORES',
        'generated_utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
        'inputs_sha256': {str(p): digest(p) for p in (Path(__file__), qa_path, summary_path, summary_path.with_name('completed.json'))},
        'outputs_sha256': {p.relative_to(bundle).as_posix(): digest(p) for p in outputs}, 'style': style_info,
        'new_scientific_computation': False, 'uncertainty': 'saved scorer intervals only; none recomputed',
        'visual_qa': 'PENDING: inspect all PNGs and vector exports',
        'scope': 'All 144 partial +16 reference means;120 condition contrasts;five macro contrasts;no omitted negative conditions'}
    write_json(folder / 'b1c_r3_render_provenance.json', provenance)
    print(json.dumps({'status': provenance['status'], 'outputs': len(outputs), 'visual_qa': provenance['visual_qa']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument('--qa', type=Path, default=DEFAULT_QA)
    args = parser.parse_args()
    render(args.bundle, args.qa)
