"""Render B2 from completed, independently verified saved scores only.

No label access, fitting, selection, scoring or bootstrap is performed. A PASS
QA receipt binding the exact completed summary is mandatory before rendering.
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
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / 'results/b2_review_20261101'
PRIMARY = 'arc2_global_tangent2_r1'
METHODS = {
    PRIMARY: 'ARC2-Global',
    'procrustes_global': 'A2M / centered Procrustes adaptation',
    'la2m20_integration_script_adaptation': 'LA2M20 integration-script adaptation',
    'simplelinear_official_final50_mlp5': 'SimpleLinear official code, final50, 5-layer MLP',
    'ridge_affine_l10_bias_regularized': 'Affine ridge, lambda10, regularized bias',
    'embedding_converter_paper_spec': 'Embedding-Converter paper-spec adaptation',
}
SHORT = dict(zip(METHODS, ('ARC2-Global', 'Procrustes adaptation', 'LA2M20 adaptation',
    'SimpleLinear (official code)', 'Affine ridge', 'Converter adaptation')))
BASELINES = tuple(m for m in METHODS if m != PRIMARY)
PAIRS = ('minilm_distilroberta', 'e5_small_base')
PAIR_LABELS = dict(zip(PAIRS, ('MiniLM → DistilRoBERTa', 'E5-small → E5-base')))
BUDGETS = ('25pct', '50pct', '75pct')
PAID = dict(zip(BUDGETS, (42833, 85666, 128499)))
METRICS = ('ndcg10', 'recall100')
COLORS = dict(zip(METHODS, ('#0F4D92', '#B64342', '#5B9B59', '#9A4D8E', '#42949E', '#A17C25')))
SKILL = 'D:/graph4paper/figures4papers/scientific-figure-making/SKILL.md'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8', newline='\n')


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(k for r in rows for k in r)), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def interval_status(interval):
    lo, hi = interval
    assert math.isfinite(lo) and math.isfinite(hi) and lo <= hi
    return 'above_zero' if lo > 0 else 'below_zero' if hi < 0 else 'unresolved'


def verified_summary(bundle, qa_path):
    qa = read_json(qa_path)
    if qa.get('status') != 'PASS':
        raise ValueError('Independent completed QA must PASS before rendering')
    candidates = [p for p in (bundle / 'evidence').rglob('summary.json') if read_json(p).get('stage') == 'B2']
    if len(candidates) != 1:
        raise ValueError('Require exactly one completed B2 summary in compact evidence')
    path = candidates[0]
    summary = read_json(path)
    completed = read_json(path.with_name('completed.json'))
    if (summary.get('stage'), summary.get('status'), summary.get('ranking_cells')) != ('B2', 'FINAL_SCORED', 184):
        raise ValueError('Require the complete 184-ranking FINAL_SCORED matrix')
    if completed.get('status') != 'FINAL_SCORED' or completed['artifact_sha256']['summary.json'] != digest(path):
        raise ValueError('Completed scoring receipt does not bind summary')
    if digest(path) not in json.dumps(qa):
        raise ValueError('QA receipt does not bind this exact summary SHA256')
    if len(summary['means']) != 40 or len(summary['contrasts']) != 30 or summary['failures']:
        raise ValueError('Require all 40 means / 30 contrasts and no scorer failure')
    lookup = {(r['pair'], r['budget'], r['method']): r for r in summary['means']}
    expected = {(p, b, m) for p in PAIRS for b in BUDGETS for m in METHODS}
    expected |= {(p, 'full', m) for p in PAIRS for m in ('full_x', 'full_y')}
    if set(lookup) != expected or len(lookup) != 40:
        raise ValueError('Means identity mismatch')
    contrasts = {(r['pair'], r['budget'], r['right']): r for r in summary['contrasts']}
    if set(contrasts) != {(p, b, m) for p in PAIRS for b in BUDGETS for m in BASELINES}:
        raise ValueError('Contrasts identity mismatch')
    for row in summary['contrasts']:
        assert row['left'] == PRIMARY
        for metric in METRICS:
            v = row[metric]
            assert math.isfinite(v['delta'])
            assert interval_status(v['ci95']) == v['interval_interpretation']
        v = row['ndcg10']
        assert abs(v['per_interval_confidence'] - (1 - .05/30)) < 1e-14
        assert interval_status(v['ci_bonferroni_family95']) == v['family_interval_interpretation']
    for name in ('cell_index.json', 'per_query.npy'):
        assert completed['artifact_sha256'][name] == digest(path.with_name(name))
    return summary, path, lookup, contrasts


def flatten_means(summary):
    rows = []
    lookup = {(r['pair'], r['budget'], r['method']): r for r in summary['means']}
    for r in summary['means']:
        row = {k: r[k] for k in ('dataset', 'pair', 'budget', 'method')}
        row['method_label'] = METHODS.get(r['method'], r['method'].replace('_', '-').title() + ' native reference')
        row['unique_destination_encodings'] = PAID.get(r['budget'], 171332 if r['method'] == 'full_y' else 0)
        row['fitting_pairs'] = 1024 if r['budget'] != 'full' else 0
        for metric in METRICS:
            v = r[metric]
            for k in ('mean', 'seed_std', 'seeds'):
                row[f'{metric}_{k}'] = v[k]
            row[f'{metric}_seed_min'], row[f'{metric}_seed_max'] = v['seed_range'] or (None, None)
            row[f'{metric}_ci95_low'], row[f'{metric}_ci95_high'] = v['ci95']
            for reference in ('full_x', 'full_y'):
                ref = lookup[r['pair'], 'full', reference][metric]['mean']
                row[f'{metric}_delta_from_{reference}'] = v['mean'] - ref
            full_y = lookup[r['pair'], 'full', 'full_y'][metric]['mean']
            row[f'{metric}_full_y_retention'] = v['mean'] / full_y if full_y else None
        rows.append(row)
    return rows


def flatten_contrasts(summary):
    rows = []
    for r in summary['contrasts']:
        row = {k: r[k] for k in ('dataset', 'pair', 'budget', 'left', 'right')}
        row['baseline_label'] = METHODS[r['right']]
        for metric in METRICS:
            v = r[metric]
            row[f'{metric}_delta'] = v['delta']
            row[f'{metric}_ci95_low'], row[f'{metric}_ci95_high'] = v['ci95']
            row[f'{metric}_ci95_status'] = v['interval_interpretation']
            seed = v['mapping_seed_variability']
            row[f'{metric}_seed_delta_std'] = seed['seed_std']
            row[f'{metric}_seed_delta_min'], row[f'{metric}_seed_delta_max'] = seed['seed_range']
        v = r['ndcg10']
        row['ndcg10_family_low'], row['ndcg10_family_high'] = v['ci_bonferroni_family95']
        row['ndcg10_family_status'] = v['family_interval_interpretation']
        row['ndcg10_individual_coverage'] = v['per_interval_confidence']
        rows.append(row)
    return rows


def seed_means(summary_path):
    import numpy as np
    index = read_json(summary_path.with_name('cell_index.json'))
    array = np.load(summary_path.with_name('per_query.npy'), allow_pickle=False)
    assert array.shape == (184, 50, 2) and np.isfinite(array).all()
    rows = []
    for i, cell in enumerate(index['cells']):
        row = {k: cell[k] for k in ('dataset', 'pair', 'budget', 'method', 'seed', 'fit_pairs', 'unique_destination_encodings')}
        for j, metric in enumerate(index['metrics']):
            row[metric] = float(array[i, :, j].mean())
        rows.append(row)
    return rows


def derive(summary):
    rows = []
    for pair in (*PAIRS, 'all_pairs'):
        for baseline in (*BASELINES, 'all_baselines'):
            selected = [r for r in summary['contrasts'] if (pair == 'all_pairs' or r['pair'] == pair)
                and (baseline == 'all_baselines' or r['right'] == baseline)]
            counts = Counter(r['ndcg10']['family_interval_interpretation'] for r in selected)
            signs = Counter('positive' if r['ndcg10']['delta'] > 0 else 'negative' if r['ndcg10']['delta'] < 0 else 'zero' for r in selected)
            rows.append({'pair': pair, 'baseline': baseline, 'conditions': len(selected),
                'family_above_zero': counts['above_zero'], 'family_unresolved': counts['unresolved'],
                'family_below_zero': counts['below_zero'], 'positive_means': signs['positive'],
                'negative_means': signs['negative'], 'zero_means': signs['zero']})
    return {'status': 'DESCRIPTIVE_DERIVED_FROM_VERIFIED_SAVED_SCORES', 'primary_counts': rows,
        'negative_contrasts_either_metric': [r for r in summary['contrasts'] if any(r[m]['delta'] < 0 for m in METRICS)],
        'uncertainty': 'All intervals copied from saved scorer; no new CI, bootstrap, p-value, macro test or equivalence margin.'}


def style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': [f for f in ('Arial', 'Helvetica', 'DejaVu Sans') if f in available],
        'font.size': 11, 'axes.linewidth': 1.2, 'axes.spines.top': False, 'axes.spines.right': False,
        'legend.frameon': False, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'axes.labelsize': 11, 'xtick.labelsize': 10, 'ytick.labelsize': 10})
    return plt, {'matplotlib': matplotlib.__version__, 'font_path': font_manager.findfont(font_manager.FontProperties(family=plt.rcParams['font.family'])),
        'colors': COLORS, 'dpi': 300, 'figure_skill': SKILL,
        'skill_references': ['references/design-theory.md', 'references/api.md']}


def save_figure(fig, folder, name):
    paths = []
    for extension in ('pdf', 'svg', 'png'):
        path = folder / f'{name}.{extension}'
        fig.savefig(path, dpi=300, facecolor='white', bbox_inches='tight', pad_inches=.08)
        paths.append(path)
    return paths


def quality_figure(plt, lookup, folder, metric):
    from matplotlib.lines import Line2D
    from matplotlib.ticker import MaxNLocator
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7))
    markers = ('o', 's', '^', 'D', 'v', 'P')
    styles = ('-', '--', '-.', ':', '--', '-.')
    figure_rows = []
    for i, pair in enumerate(PAIRS):
        ax = axes[i]
        values = []
        for method, marker, line in zip(METHODS, markers, styles):
            rows = [lookup[pair, b, method] for b in BUDGETS]
            ys = [r[metric]['mean'] for r in rows]
            values.extend(ys)
            ax.plot((25, 50, 75), ys, color=COLORS[method], marker=marker, ls=line,
                lw=2.8 if method == PRIMARY else 1.6, markersize=6 if method == PRIMARY else 5,
                zorder=6 if method == PRIMARY else 3)
            figure_rows.extend({'pair': pair, 'budget': b, 'method': method, 'metric': metric,
                'mean': r[metric]['mean']} for b, r in zip(BUDGETS, rows))
        for reference, color, line in (('full_x', '#272727', '--'), ('full_y', '#767676', ':')):
            v = lookup[pair, 'full', reference][metric]['mean']
            values.append(v)
            ax.axhline(v, color=color, ls=line, lw=1.4, zorder=1)
            figure_rows.append({'pair': pair, 'budget': 'full', 'method': reference, 'metric': metric, 'mean': v})
        low, high = min(values), max(values)
        span = max(high-low, .03 if metric == 'ndcg10' else .01)
        ax.set_ylim(max(0, low-span*.10), min(1, high+span*.14))
        ax.set_xlim(21, 79)
        ax.set_xticks((25, 50, 75), ('25%', '50%', '75%'))
        ax.yaxis.set_major_locator(MaxNLocator(5))
        ax.grid(axis='y', color='#E9E9E9', linewidth=.7, zorder=0)
        ax.set_title(f'({chr(97+i)}) {PAIR_LABELS[pair]}', loc='left', fontsize=12, pad=9)
        ax.set_xlabel('Paid destination documents |A ∪ S| / N')
        ax.set_ylabel('nDCG@10' if metric == 'ndcg10' else 'Recall@100')
    handles = [Line2D([0], [0], color=COLORS[m], marker=k, ls=l, lw=2 if m == PRIMARY else 1.5,
        label=SHORT[m]) for m, k, l in zip(METHODS, markers, styles)]
    handles.extend([Line2D([0], [0], color=c, ls=l, label=label) for c, l, label in
        (('#272727', '--', 'Full-X native reference'), ('#767676', ':', 'Full-Y native reference'))])
    fig.legend(handles=handles, ncol=4, loc='lower center', bbox_to_anchor=(.5, .04), fontsize=9)
    fig.text(.5, .005, 'TREC-COVID · exact retrieval · 1,024 fitting pairs · five-seed means; intervals in tables',
        ha='center', fontsize=9, color='#4D4D4D')
    fig.tight_layout(pad=1.3, rect=(0, .22, 1, 1))
    paths = save_figure(fig, folder, f'b2_{metric}_vs_budget')
    plt.close(fig)
    return paths, figure_rows


def forest_figure(plt, contrasts, folder):
    from matplotlib.lines import Line2D
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 7.3), sharex=True)
    data = []
    for i, pair in enumerate(PAIRS):
        ax = axes[i]
        ticks, labels = [], []
        for j, baseline in enumerate(BASELINES):
            for k, budget in enumerate(BUDGETS):
                y = 18 - (j*4+k)
                v = contrasts[pair, budget, baseline]['ndcg10']
                lo, hi = v['ci_bonferroni_family95']
                color = '#0F4D92' if lo > 0 else '#B64342' if hi < 0 else '#767676'
                ax.plot((lo, hi), (y, y), color=color, lw=1.7)
                ax.plot((lo, lo), (y-.13, y+.13), color=color, lw=1.2)
                ax.plot((hi, hi), (y-.13, y+.13), color=color, lw=1.2)
                ax.scatter([v['delta']], [y], color=color, s=31, zorder=4,
                    marker='o' if lo > 0 else 's' if hi < 0 else 'D')
                ticks.append(y)
                name = SHORT[baseline].replace(' adaptation', '').replace(' (official code)', '')
                labels.append(f'{name} · {budget[:2]}%')
                data.append({'pair': pair, 'budget': budget, 'baseline': baseline,
                    'delta': v['delta'], 'low': lo, 'high': hi, 'status': v['family_interval_interpretation']})
            if j < len(BASELINES)-1:
                ax.axhline(18-(j*4+3), color='#EBEBEB', lw=.8)
        ax.axvline(0, color='#272727', lw=1.1, ls='--', zorder=1)
        ax.set_yticks(ticks, labels, fontsize=9)
        ax.set_ylim(-1, 19)
        ax.set_title(f'({chr(97+i)}) {PAIR_LABELS[pair]}', loc='left', fontsize=12, pad=10)
        ax.set_xlabel('ARC2 − baseline nDCG@10')
        ax.grid(axis='x', color='#EAEAEA', lw=.7)
    all_lows = [r['low'] for r in data]
    all_highs = [r['high'] for r in data]
    span = max(all_highs)-min(all_lows)
    axes[0].set_xlim(min(all_lows)-.06*span, max(all_highs)+.06*span)
    fig.legend(handles=[Line2D([0], [0], color='#0F4D92', marker='o', label='Improvement supported'),
        Line2D([0], [0], color='#767676', marker='D', label='Unresolved')],
        ncol=2, loc='lower center', bbox_to_anchor=(.5, .06), fontsize=10)
    fig.text(.5, .026, 'All 30 primary contrasts · ~99.833% individual percentile intervals · approximate 95% Bonferroni family coverage',
        ha='center', fontsize=9)
    fig.text(.5, .002, 'Five mapping seeds averaged before 50-query paired bootstrap; zero-crossing intervals do not establish equivalence.',
        ha='center', fontsize=9, color='#4D4D4D')
    fig.tight_layout(pad=1.5, rect=(0, .13, 1, 1))
    paths = save_figure(fig, folder, 'b2_all30_primary_contrasts')
    plt.close(fig)
    return paths, data


def interval_text(v, key='ci95'):
    return f"[{v[key][0]:+.5f}, {v[key][1]:+.5f}]"


def report(summary, source, qa_path, lookup, derived):
    overall = next(r for r in derived['primary_counts'] if r['pair'] == 'all_pairs' and r['baseline'] == 'all_baselines')
    baseline_counts = {r['baseline']: r for r in derived['primary_counts'] if r['pair'] == 'all_pairs'}
    pro = [r for r in summary['contrasts'] if r['right'] == 'procrustes_global']
    lines = ['# B2: independent TREC-COVID fixed-anchor confirmation', '',
        f"Completed one-shot final scoring: `{summary['status']}`; **{overall['family_above_zero']}/30 primary contrasts support improvement, "
        f"{overall['family_unresolved']}/30 remain unresolved, {overall['family_below_zero']}/30 support worse performance** under the locked family intervals.", '',
        f"Confirmed improvements occur against Converter ({baseline_counts['embedding_converter_paper_spec']['family_above_zero']}/6), "
        f"affine ridge ({baseline_counts['ridge_affine_l10_bias_regularized']['family_above_zero']}/6), "
        f"and SimpleLinear ({baseline_counts['simplelinear_official_final50_mlp5']['family_above_zero']}/6) under the locked configurations. "
        'All six ARC2-minus-Procrustes nDCG means are negative and all six family intervals cross zero. '
        'These unresolved comparisons do not demonstrate equality, noninferiority or equivalence. The result remains conditional on the declared configurations; no method switch follows automatically.', '',
        '## Evidence and scope', '',
        '- Full TREC-COVID: 171,332 documents, all 50 queries, two encoder migrations, seeds 17/29/41/53/67, six methods, three paid budgets.',
        '- Complete 184 exact-search rankings: 180 partial endpoints from 60 fits plus four native Full-X/Full-Y references. Exactly 1,024 paired anchors per fit.',
        '- Charge unique destination documents as |A ∪ S|, including anchors: 42,833 / 85,666 / 128,499 (25/50/75%). Nonanchor paid rows add no fitting pairs.',
        '- nDCG@10 uses graded gain 2^rel−1; Recall@100 includes all positive judgments in its denominator; unjudged documents are nonrelevant. No query filtering.',
        '- The locked 30 primary nDCG contrasts use 20,000 paired query bootstrap draws, PCG64 seed 20261031, with five mapping seeds averaged first. '
        'Each percentile interval has ~99.8333% individual coverage for approximate 95% Bonferroni family coverage. There are 50 query units, not 250 independent observations.',
        '- Recall intervals and condition-mean intervals are nominal 95% descriptive. No new interval, post-hoc macro test, p-value or equivalence margin is introduced by this report.',
        '- Full native references use their own native queries and documents; mixed-gallery methods use destination queries. They are contextual references, not extra primary contrasts.', '',
        '## Primary results by declared baseline', '',
        '| Migration | Baseline configuration | Above zero | Unresolved | Below zero | Negative nDCG means |',
        '|---|---|---:|---:|---:|---:|']
    for r in derived['primary_counts']:
        if r['pair'] in PAIRS and r['baseline'] in BASELINES:
            lines.append(f"| {PAIR_LABELS[r['pair']]} | {METHODS[r['baseline']]} | {r['family_above_zero']} | {r['family_unresolved']} | {r['family_below_zero']} | {r['negative_means']} |")
    lines += ['', 'All negative and unresolved outcomes are retained below and in the CSV files. Above/below zero refer only to the primary family interval, not a mean sign.', '',
        '## All 40 condition means and native references', '',
        'Values are mean ± mapping-seed sample SD; native references have one deterministic ranking and no mapping-seed SD. Nominal 95% query-bootstrap intervals, seed min/max, '
        'native-reference differences and Full-Y retention are in [all_means.csv](tables/all_means.csv). ARC2 is numerically below native Full-Y in all six conditions on both metrics; '
        'these reference differences are descriptive and have no new inferential test.', '']
    for pair in PAIRS:
        lines += [f'### {PAIR_LABELS[pair]}', '', '| Budget | Method | nDCG@10 ± seed SD | Recall@100 ± seed SD |', '|---|---|---:|---:|']
        for budget in (*BUDGETS, 'full'):
            for method in (METHODS if budget != 'full' else ('full_x', 'full_y')):
                r = lookup[pair, budget, method]
                values = [f"{r[m]['mean']:.5f}" + (f" ± {r[m]['seed_std']:.5f}" if r[m]['seed_std'] is not None else ' (native)') for m in METRICS]
                label = METHODS.get(method, method.replace('_', '-').title())
                lines.append(f"| {budget[:2]+'%' if budget != 'full' else 'full'} | {label} | {values[0]} | {values[1]} |")
        lines += ['']
    lines += ['## All 30 ARC2-minus-baseline contrasts', '',
        'nDCG intervals below are the primary ~99.8333% individual intervals (approximate 95% 30-comparison family). Recall intervals are nominal 95% descriptive. '
        'Seed delta SD/range and nominal nDCG intervals are retained in [all_contrasts.csv](tables/all_contrasts.csv).', '']
    for pair in PAIRS:
        lines += [f'### {PAIR_LABELS[pair]}', '', '| Budget | Baseline | Δ nDCG@10 | Primary interval | Decision | Δ Recall@100 | Descriptive 95% interval |',
            '|---|---|---:|---|---|---:|---|']
        for budget in BUDGETS:
            for baseline in BASELINES:
                r = next(r for r in summary['contrasts'] if (r['pair'], r['budget'], r['right']) == (pair, budget, baseline))
                n, rec = r['ndcg10'], r['recall100']
                lines.append(f"| {budget[:2]}% | {SHORT[baseline]} | {n['delta']:+.5f} | {interval_text(n, 'ci_bonferroni_family95')} | {n['family_interval_interpretation']} | {rec['delta']:+.5f} | {interval_text(rec)} |")
        lines += ['']
    lines += ['## Figures and reproducibility', '',
        '- [nDCG@10 versus paid destination coverage](figures/b2_ndcg10_vs_budget.pdf) ([PNG](figures/b2_ndcg10_vs_budget.png), [SVG](figures/b2_ndcg10_vs_budget.svg)).',
        '- [Recall@100 versus paid destination coverage](figures/b2_recall100_vs_budget.pdf) ([PNG](figures/b2_recall100_vs_budget.png), [SVG](figures/b2_recall100_vs_budget.svg)).',
        '- [All 30 primary contrasts](figures/b2_all30_primary_contrasts.pdf) ([PNG](figures/b2_all30_primary_contrasts.png), [SVG](figures/b2_all30_primary_contrasts.svg)).',
        '- [All 184 ranking-level seed means](tables/seed_means.csv), [primary sign/interval counts](tables/primary_counts.csv), [all negative contrasts](tables/negative_contrasts.csv).',
        f'- Exact saved summary SHA256: `{digest(source)}`.',
        f'- Independent computational QA: [{qa_path.name}]({qa_path.name}), SHA256 `{digest(qa_path)}`. '
        'This compact verification does not claim regeneration of the remote encoder outputs, fit checkpoints or exact endpoints.',
        '- Rendering provenance and artifact hashes: [render_provenance.json](render_provenance.json). Visual inspection is recorded separately in [visual_qa.json](visual_qa.json).', '',
        '## Baseline qualifications and limits', '',
        'ARC2 is the frozen centered rectangular Procrustes initialization, lambda10 and exactly two tangent updates; there is no local residual or neural mapper. '
        'A2M/Procrustes is the centered affine adaptation. LA2M20 uses 20 source-anchor clusters and the integration-script singleton fallback. '
        'SimpleLinear uses pinned official code, a five-layer MLP and final50 epochs. Ridge regularizes the affine bias at lambda10. '
        'Embedding-Converter is the locked paper-spec adaptation with 50,000 selection iterations and a fresh selected-length refit on all 1,024 anchors; '
        'anchor validation MAE, never final qrels, selected training length. These labels do not claim full original-paper reproduction.', '',
        'The independent test is conditional on this dataset, the two pinned encoder migrations, the fixed 1,024-anchor fitting regime and 128-token encoder setting. '
        'It does not test one-versus-two tangent necessity, all-paid supervision, an optimal anchor budget, ANN behavior, measured deployment cost, isolated hardware speed, SLOs or real traffic. '
        'Full destination caches were physically prepared for evaluation; the charged partial exposure does not demonstrate physical encoding savings. Shared execution timing is not an isolated performance benchmark.', '',
        '**STOP after the authorized B2 result review and ARIS analysis. Manuscript unchanged; no automatic systems run, new dataset, retuning or submission-facing method switch.**', '']
    assert len(pro) == 6 and all(r['ndcg10']['delta'] < 0 and r['ndcg10']['family_interval_interpretation'] == 'unresolved' for r in pro)
    assert all(lookup[p, b, PRIMARY][m]['mean'] < lookup[p, 'full', 'full_y'][m]['mean']
        for p in PAIRS for b in BUDGETS for m in METRICS)
    return '\n'.join(lines)


def previews(folder):
    poppler = shutil.which('pdftoppm')
    if not poppler:
        raise RuntimeError('pdftoppm is required to render vector-PDF previews for visual QA')
    paths = []
    for path in sorted(folder.glob('b2_*.pdf')):
        prefix = folder / 'previews' / (path.stem + '_pdf')
        prefix.parent.mkdir(exist_ok=True)
        subprocess.run([poppler, '-f', '1', '-singlefile', '-scale-to', '1800', '-png', str(path), str(prefix)],
            check=True, capture_output=True)
        paths.append(prefix.with_suffix('.png'))
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument('--qa', type=Path, required=True)
    args = parser.parse_args()
    bundle, qa_path = args.bundle.resolve(), args.qa.resolve()
    summary, source, lookup, contrasts = verified_summary(bundle, qa_path)
    tables, figures = bundle / 'tables', bundle / 'figures'
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    derived = derive(summary)
    mean_rows, contrast_rows = flatten_means(summary), flatten_contrasts(summary)
    for name, rows in [('all_means', mean_rows), ('all_contrasts', contrast_rows),
        ('seed_means', seed_means(source)), ('primary_counts', derived['primary_counts']),
        ('negative_contrasts', [r for r in contrast_rows if any(r[m+'_delta'] < 0 for m in METRICS)])]:
        write_csv(tables / f'{name}.csv', rows)
    write_json(tables / 'derived_summary.json', derived)
    plt, figure_style = style()
    outputs = []
    for metric in METRICS:
        paths, data = quality_figure(plt, lookup, figures, metric)
        outputs.extend(paths)
        write_csv(tables / f'figure_{metric}_values.csv', data)
    paths, data = forest_figure(plt, contrasts, figures)
    outputs.extend(paths)
    write_csv(tables / 'figure_primary_contrasts.csv', data)
    outputs.extend(previews(figures))
    (bundle / 'SUMMARY.md').write_text(report(summary, source, qa_path, lookup, derived), encoding='utf-8', newline='\n')
    outputs += [bundle / 'SUMMARY.md', *sorted(tables.glob('*'))]
    write_json(bundle / 'render_provenance.json', {'status': 'RENDERED_FROM_INDEPENDENTLY_VERIFIED_SAVED_SCORES',
        'generated_utc': datetime.now(timezone.utc).isoformat(), 'summary': str(source),
        'summary_sha256': digest(source), 'qa': str(qa_path), 'qa_sha256': digest(qa_path),
        'renderer': str(Path(__file__).resolve()), 'renderer_sha256': digest(__file__),
        'python': platform.python_version(), 'style': figure_style,
        'pdf_preview_renderer': shutil.which('pdftoppm'),
        'row_counts': {'means': len(mean_rows), 'primary_contrasts': len(contrast_rows), 'ranking_seed_means': 184},
        'statistical_policy': derived['uncertainty'],
        'outputs': {str(p.relative_to(bundle)): {'sha256': digest(p), 'bytes': p.stat().st_size} for p in outputs}})
    print(json.dumps({'status': 'RENDERED', 'summary_sha256': digest(source), 'output': str(bundle),
        'counts': derived['primary_counts'][-1], 'figures': len(paths)}, indent=2))


if __name__ == '__main__':
    main()
