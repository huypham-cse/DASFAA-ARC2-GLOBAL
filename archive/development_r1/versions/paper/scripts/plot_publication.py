"""Publication plots from saved ARC2 evidence, without reads or file writes.

Public API: ``quality_figure(rows, macro=False)`` and
``ablation_figure(records)`` return Matplotlib Figures.  Callers own export
and provenance.  No inference, averaging, interval estimation, or smoothing is
performed here.  TeX rendering requires the existing manuscript TeX runtime.
"""

from collections.abc import Iterable, Mapping
import math

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.lines import Line2D


ARC = 'arc2_global_tangent2_r1'
PAIRS = ('minilm_distilroberta', 'e5_small_base')
BUDGETS = ('25pct', '50pct', '75pct')
METHODS = (
    ARC,
    'procrustes_global',
    'la2m20_integration_script_adaptation',
    'simplelinear_official_final50_mlp5',
    'ridge_affine_l10_bias_regularized',
    'embedding_converter_paper_spec',
)
NATIVES = ('full_x', 'full_y')
LABELS = dict(zip(METHODS + NATIVES, (
    'ARC2-Global', 'Procrustes', 'LA2M20', 'SimpleLinear',
    'Affine ridge', 'Converter', 'Native Full-X', 'Native Full-Y',
)))

# Method identity is redundant in color, marker, and stroke, including in print.
_ENCODING = {
    ARC: ('#0F4D92', 'o', '-'),
    METHODS[1]: ('#626262', 's', (0, (4, 2))),
    METHODS[2]: ('#32848E', '^', (0, (5, 1.5, 1, 1.5))),
    METHODS[3]: ('#914781', 'D', (0, (1, 1.4))),
    METHODS[4]: ('#AD413F', 'v', (0, (3, 1.5))),
    METHODS[5]: ('#967512', 'P', (0, (5, 1.5, 1, 1.5))),
}
_NATIVE_STYLES = {'full_x': (0, (1, 1.8)), 'full_y': (0, (6, 2))}

_STYLE = {
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman'],
    'font.size': 8.5,
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsmath}\usepackage[T1]{fontenc}\usepackage{lmodern}',
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'axes.titlesize': 9,
    'axes.labelsize': 8.5,
    'axes.linewidth': 0.7,
    'axes.edgecolor': '#252525',
    'axes.labelcolor': '#151515',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'xtick.color': '#252525',
    'ytick.color': '#252525',
    'xtick.major.width': 0.65,
    'ytick.major.width': 0.65,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'legend.fontsize': 7.8,
    'legend.frameon': False,
    'pdf.fonttype': 42,
    'svg.fonttype': 'none',
    'savefig.facecolor': 'white',
}


class _PublicationFigure(Figure):
    """Keep TeX's draw-time font configuration local to this Figure.

    Matplotlib's TeX manager reads font/preamble rcParams during drawing, after
    construction.  Entering this context for both phases avoids changing the
    caller's global style and preserves the fonts for later PDF/SVG/PNG export.
    """

    def draw(self, renderer):
        with mpl.rc_context(_STYLE):
            return super().draw(renderer)


def _number(value, field):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f'{field} must be finite, got {value!r}')
    return result


def _quality_index(rows: Iterable[Mapping], metric='ndcg10'):
    cells = {}
    for row in rows:
        identity = (row['pair'], row['method'], row['budget'])
        pair, method, budget = identity
        if pair not in PAIRS or method not in METHODS + NATIVES:
            raise ValueError(f'Unknown quality cell: {identity!r}')
        allowed = ('native',) if method in NATIVES else BUDGETS
        if budget not in allowed:
            raise ValueError(f'Unexpected budget: {identity!r}')
        if identity in cells:
            raise ValueError(f'Duplicate quality cell: {identity!r}')
        cells[identity] = _number(row[metric], metric)
    expected = {
        (pair, method, budget)
        for pair in PAIRS for method in METHODS + NATIVES
        for budget in (('native',) if method in NATIVES else BUDGETS)
    }
    if set(cells) != expected:
        raise ValueError(f'Incomplete quality panel; missing {sorted(expected - set(cells))!r}')
    return cells


def quality_figure(rows: Iterable[Mapping], macro: bool = False) -> Figure:
    """Plot every saved cell at its actual budget, with native references.

    Development is a two-panel nDCG view.  Prospective rows that also provide
    ``recall100`` produce a four-panel view: primary nDCG above auxiliary
    Recall.  Prospective panel ranges differ explicitly to expose the small
    MiniLM differences while retaining all methods and native references.
    All supplied means are plotted verbatim; no interval is inferred.  Curve
    segments only connect the three measured budget means.  Callers should
    explain that these are descriptive means, without invented CI bands.
    """
    rows = list(rows)
    cells = _quality_index(rows)
    has_recall = not macro and any('recall100' in row for row in rows)
    if has_recall and not all('recall100' in row for row in rows):
        raise ValueError('Recall must be supplied for every adapter and native reference.')
    recall_cells = _quality_index(rows, 'recall100') if has_recall else None
    metrics = [('ndcg10', cells)] + ([('recall100', recall_cells)] if has_recall else [])
    bounds = {
        ('ndcg10', PAIRS[0]): (0.18, 0.72) if macro else (0.42, 0.53),
        ('ndcg10', PAIRS[1]): (0.18, 0.72) if macro else (0.28, 0.70),
        ('recall100', PAIRS[0]): (0.06, 0.11),
        ('recall100', PAIRS[1]): (0.02, 0.13),
    }
    for metric, values in metrics:
        for pair in PAIRS:
            low, high = bounds[metric, pair]
            if any(not low <= value <= high for (p, _, _), value in values.items() if p == pair):
                raise ValueError(f'{pair}/{metric} exceeds declared limits {(low, high)}; '
                                 'revise the publication scale before plotting.')

    with mpl.rc_context(_STYLE):
        fig = _PublicationFigure(figsize=(4.8, 4.05 if has_recall else 2.65), facecolor='white')
        axes = fig.subplots(len(metrics), 2, sharex=True, squeeze=False)
        pair_titles = (r'MiniLM $\rightarrow$ DistilRoBERTa',
                       r'E5-small $\rightarrow$ E5-base')
        for row_index, (metric, metric_cells) in enumerate(metrics):
            for col_index, (pair, title) in enumerate(zip(PAIRS, pair_titles)):
                ax = axes[row_index, col_index]
                panel = chr(ord('a') + row_index * 2 + col_index)
                for method in METHODS:
                    color, marker, style = _ENCODING[method]
                    values = [metric_cells[pair, method, budget] for budget in BUDGETS]
                    ax.plot(
                        (25, 50, 75), values, color=color, linestyle=style,
                        marker=marker, markersize=4.0 if method == ARC else 3.7,
                        markeredgewidth=0.55, markeredgecolor=color,
                        linewidth=1.8 if method == ARC else 1.1,
                        zorder=5 if method == ARC else 3, label=LABELS[method],
                    )
                for method in NATIVES:
                    ax.axhline(metric_cells[pair, method, 'native'], color='#272727',
                               linestyle=_NATIVE_STYLES[method], linewidth=0.9,
                               zorder=2, label=LABELS[method])
                ax.set_title(r'\textbf{(' + panel + ')} ' + title, pad=6)
                ax.set_xlim(21, 79)
                ax.set_ylim(*bounds[metric, pair])
                ax.set_xticks((25, 50, 75))
                if macro:
                    ticks = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7)
                elif metric == 'ndcg10':
                    ticks = (0.42, 0.45, 0.48, 0.51) if col_index == 0 else (0.3, 0.4, 0.5, 0.6, 0.7)
                else:
                    ticks = (0.06, 0.08, 0.10) if col_index == 0 else (0.02, 0.05, 0.08, 0.11)
                ax.set_yticks(ticks)
                ax.grid(axis='y', color='#E5E5E5', linewidth=0.45, zorder=0)
                ax.tick_params(axis='both', pad=2.5)
            ylabel = ('Macro nDCG@10' if macro else
                      ('nDCG@10 (primary)' if metric == 'ndcg10' and has_recall else
                       'Recall@100 (auxiliary)' if metric == 'recall100' else 'nDCG@10'))
            axes[row_index, 0].set_ylabel(ylabel, labelpad=4)
        if not macro:
            fig.text(0.985, 0.985, 'Panel-specific y ranges', ha='right', va='top',
                     fontsize=7.4, color='#454545')
        fig.supxlabel(r'Paid destination documents (\%)', x=0.54, y=0.16 if has_recall else 0.215,
                      fontsize=8.5)

        # Explicit handles keep every legend key equally readable, even when
        # method curves overlap in the data panels.
        handles = []
        for method in METHODS:
            color, marker, style = _ENCODING[method]
            handles.append(Line2D([], [], color=color, marker=marker,
                                  linestyle=style, markersize=3.8,
                                  linewidth=1.8 if method == ARC else 1.1,
                                  label=LABELS[method]))
        for method in NATIVES:
            handles.append(Line2D([], [], color='#272727',
                                  linestyle=_NATIVE_STYLES[method], linewidth=0.9,
                                  label=LABELS[method]))
        fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.51, 0.015),
                   ncol=4, handlelength=2.0, columnspacing=0.8,
                   handletextpad=0.4, labelspacing=0.55, borderaxespad=0)
        fig.subplots_adjust(left=0.12, right=0.985,
                            bottom=0.245 if has_recall else 0.34,
                            top=0.91 if has_recall else (0.885 if macro else 0.85),
                            wspace=0.35, hspace=0.48)
        return fig


_CONTROLS = (
    (ARC, 'procrustes_global', r'2 steps $-$ 0 steps'),
    (ARC, 'tangent1_l10', r'2 steps $-$ 1 step'),
    (ARC, 'ridge_affine_l10_bias_regularized', r'ARC2 $-$ affine ridge'),
    ('tangent2_l1', ARC, r'$\lambda=1$ $-$ $\lambda=10$'),
    ('tangent2_l100', ARC, r'$\lambda=100$ $-$ $\lambda=10$'),
)


def ablation_figure(records: Iterable[Mapping]) -> Figure:
    """Plot all five saved controls and full intervals without recomputation.

    A single continuous x axis retains the large ridge contrast and negative
    controls.  Exact signed point labels make the small second-step gain
    legible without a broken axis, interval magnification, or omitted control.
    """
    cells = {}
    for record in records:
        key = (record['left'], record['right'])
        if key in cells:
            raise ValueError(f'Duplicate ablation contrast: {key!r}')
        delta, low, high = (_number(record[k], k) for k in ('delta', 'low', 'high'))
        if not low <= delta <= high:
            raise ValueError(f'Point lies outside saved ablation interval: {key!r}')
        cells[key] = (delta, low, high)
    expected = {(left, right) for left, right, _ in _CONTROLS}
    if set(cells) != expected:
        raise ValueError('Ablation plot requires exactly the five declared controls; '
                         f'missing={expected - set(cells)}, extra={set(cells) - expected}')
    limits = (-0.02, 0.125)
    if any(low < limits[0] or high > limits[1] for _, low, high in cells.values()):
        raise ValueError('A saved interval exceeds the declared continuous ablation axis.')

    with mpl.rc_context(_STYLE):
        fig = _PublicationFigure(figsize=(4.8, 2.45), facecolor='white')
        ax = fig.subplots()
        positions = (0, 1, 2, 3.55, 4.55)
        for index, ((left, right, label), y) in enumerate(zip(_CONTROLS, positions)):
            delta, low, high = cells[left, right]
            color = '#0F4D92' if index < 3 else '#626262'
            ax.plot((low, high), (y, y), color=color, linewidth=1.6,
                    solid_capstyle='butt', zorder=3)
            ax.plot((low, low), (y - 0.09, y + 0.09), color=color,
                    linewidth=0.8, zorder=3)
            ax.plot((high, high), (y - 0.09, y + 0.09), color=color,
                    linewidth=0.8, zorder=3)
            ax.plot(delta, y, marker='o' if index < 3 else 's', color=color,
                    markersize=4, markeredgewidth=0.5, linestyle='none', zorder=4)
            ax.annotate(f'{delta:+.4f}', (delta, y), xytext=(0, 7),
                        textcoords='offset points', ha='center', va='bottom',
                        color=color, fontsize=8.2, zorder=5)

        ax.axvline(0, color='#454545', linestyle=(0, (3, 2)), linewidth=0.8, zorder=1)
        ax.axhline(2.85, color='#E2E2E2', linewidth=0.6, zorder=0)
        ax.set_yticks(positions, [item[2] for item in _CONTROLS])
        ax.tick_params(axis='y', length=0, pad=5)
        ax.set_ylim(5.05, -0.8)
        ax.set_xlim(*limits)
        ax.set_xticks((-0.02, 0, 0.04, 0.08, 0.12))
        ax.set_xticklabels((r'$-0.02$', '0.00', '0.04', '0.08', '0.12'))
        ax.set_xlabel(r'$\Delta$ macro nDCG@10 (family-adjusted intervals)', labelpad=4)
        ax.grid(axis='x', color='#E5E5E5', linewidth=0.45, zorder=0)
        fig.subplots_adjust(left=0.30, right=0.98, top=0.97, bottom=0.205)
        return fig
