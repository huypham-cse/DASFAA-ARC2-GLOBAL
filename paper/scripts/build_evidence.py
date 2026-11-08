"""Build manuscript evidence from completed, locked scoring outputs only.

This is an analysis/rendering command, not an experiment runner.  It never
opens qrels, fits a mapper, encodes text, searches a gallery, or changes a run.
Run from anywhere: python paper/scripts/build_evidence.py
"""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / 'paper'
GEN, FIG, REVIEW = [PAPER / p for p in ('generated', 'figures', 'review')]
for p in (GEN, FIG, REVIEW):
    p.mkdir(parents=True, exist_ok=True)

PATHS = {
    'dev': 'results/b1c_r3_review_20261031/evidence/run/scoring/summary.json',
    'mechanism': 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
    'allpaid': 'results/b1p_r5_review_20261027/scoring/results_summary.json',
    'gallery': 'results/b1g_r1_review_20261027/scoring/results_summary.json',
    'trec': 'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json',
    'dev_lock': 'configs/b1c_r3_lock.json',
    'trec_lock': 'configs/b2_lock.json',
    'paid_lock': 'configs/b1p_lock.json',
    'dataset_registry': 'configs/datasets.json',
    'matched': 'results/tc1l_local_r1_20261102/full/scoring/summary.json',
    'matched_lock': 'configs/tc1l_minilm_local_20261102_lock.json',
}
if (ROOT/'artifact_layout.json').exists():
    PATHS.update(json.loads((ROOT/'artifact_layout.json').read_text())['paths'])
SOURCES, ITEMS = {}, {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(key):
    p = ROOT / PATHS[key]
    SOURCES[key] = {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)}
    return json.loads(p.read_text(encoding='utf-8'))

D = {key: read(key) for key in PATHS}
ARC = 'arc2_global_tangent2_r1'
METHODS = [ARC, 'procrustes_global', 'la2m20_integration_script_adaptation',
           'simplelinear_official_final50_mlp5', 'ridge_affine_l10_bias_regularized',
           'embedding_converter_paper_spec']
LABELS = dict(zip(METHODS, ['ARC2-Global', 'Procrustes', 'LA2M20', 'SimpleLinear', 'Affine ridge', 'Converter']))
LABELS.update(full_x='Native Full-X', full_y='Native Full-Y')
PAIRS = ['minilm_distilroberta', 'e5_small_base']
PAIR_LABELS = ['MiniLM $\u2192$ DistilRoBERTa', 'E5-small $\u2192$ E5-base']
BUDGETS = ['25pct', '50pct', '75pct']
DATASETS = ['FiQA', 'NanoNQ', 'NanoHotpotQA', 'NanoFEVER']

def provenance(name, keys, operation, records=None):
    ITEMS[name] = {'sources': keys, 'operation': operation}
    if records is not None:
        ITEMS[name]['values'] = records

def write(name, text, keys, operation, records=None):
    p = GEN / name
    p.write_text(text, encoding='utf-8')
    provenance(p.relative_to(PAPER).as_posix(), keys, operation, records)

def csvout(name, rows, keys, operation):
    p = GEN / name
    with p.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    provenance(p.relative_to(PAPER).as_posix(), keys, operation, rows)

def find(rows, **selectors):
    values = [r for r in rows if all(r.get(k) == v for k, v in selectors.items())]
    assert len(values) == 1, (selectors, len(values))
    return values[0]

def mean(key, method, pair=None, budget=None, metric='ndcg10', regime=None, dataset=None):
    selectors = {'method': method}
    for k, v in [('pair', pair), ('budget', budget), ('regime', regime), ('dataset', dataset)]:
        if v is not None:
            selectors[k] = v
    rows = [r for r in D[key]['means'] if all(r.get(k) == v for k, v in selectors.items())]
    assert rows, (key, selectors)
    return float(np.mean([r[metric]['mean'] for r in rows]))

def signed(x, precision=4):
    return f'{x:+.{precision}f}'

def interval(ci, precision=4):
    return '[' + ', '.join(signed(x, precision) for x in ci) + ']'

def ranked(value, peers, precision=4):
    """Rank unrounded adapter means; native references never enter the rank."""
    distinct = sorted(set(float(v) for v in peers), reverse=True)
    rendered = f'{value:.{precision}f}'
    if abs(value-distinct[0]) < 1e-12:
        return r'\textbf{' + rendered + '}'
    if len(distinct)>1 and abs(value-distinct[1]) < 1e-12:
        return r'\underline{' + rendered + '}'
    return rendered


def table(name, caption, label, columns, header, rows, keys, operation, records=None,
          header_rule=None, highlight_arc=True, tabcolsep=4):
    lines=[]
    for row in rows:
        if row[0] == LABELS['full_x']:
            lines.append(r'\midrule')
        prefix = r'\rowcolor{arcPale}' if highlight_arc and 'ARC2-Global' in row[0] else ''
        lines.append(prefix + ' & '.join(row) + r' \\')
    body = '\n'.join(lines)
    split_header = bool(rows and rows[0][0]=='')
    if split_header:
        first,body = body.split('\n',1)
        subheader = '\n'+(header_rule or r'\cmidrule(lr){2-4}\cmidrule(lr){5-7}')+'\n'+first
    else:
        subheader = ''
    text = ('% Generated by paper/scripts/build_evidence.py; do not hand-edit.\n'
            '\\begin{table}[t]\n\\centering\n\\small\n'
            f'\\setlength{{\\tabcolsep}}{{{tabcolsep}pt}}\n'
            f'\\caption{{{caption}}}\\label{{{label}}}\n'
            f'\\begin{{tabular}}{{{columns}}}\n\\toprule\n'
            + ' & '.join(header) + r' \\' + subheader + '\n\\midrule\n' + body
            + '\n\\bottomrule\n\\end{tabular}\n\\end{table}\n')
    write(name, text, keys, operation, records)

def verify_means(key):
    """Check every displayed condition mean against saved per-query arrays."""
    base = (ROOT / PATHS[key]).parent
    index = json.loads((base / 'cell_index.json').read_text())
    paths = list(base.glob('per_query*.npy'))
    arrays = {p.name: np.load(p, allow_pickle=False) for p in paths}
    for p in [base / 'cell_index.json'] + paths:
        SOURCES[p.relative_to(ROOT).as_posix()] = {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)}
    grouped = {}
    identity_keys = ('dataset', 'pair', 'budget', 'method') + (('regime',) if key == 'allpaid' else ())
    for i, cell in enumerate(index['cells']):
        filename = cell.get('per_query_file', 'per_query.npy')
        a = arrays[filename][cell.get('per_query_index', i)]
        identity = tuple(cell.get(k) for k in identity_keys)
        grouped.setdefault(identity, []).append(a.mean(axis=0))
    max_error = 0.
    for r in D[key]['means']:
        # Main DEV summaries do not carry a regime field; its index also omits it.
        identity = tuple(r.get(k) for k in identity_keys)
        actual = np.mean(grouped[identity], axis=0)
        for j, metric in enumerate(index['metrics']):
            err = abs(actual[j] - r[metric]['mean'])
            max_error = max(max_error, err)
            assert err < 1e-12, (key, identity, metric, err)
    return {'conditions': len(D[key]['means']), 'per_query_mean_max_error': max_error}

def build_tables():
    records, rows = [], []
    for method in METHODS:
        n, r = mean('dev', method), mean('dev', method, metric='recall100')
        rec = {'method': method, 'ndcg10': n, 'recall100': r}
        row = [r'\textbf{ARC2-Global}' if method == ARC else LABELS[method],
               ranked(n,[mean('dev', m) for m in METHODS]),
               ranked(r,[mean('dev', m,metric='recall100') for m in METHODS])]
        if method == ARC:
            row += ['---', '---']
        else:
            c = find(D['dev']['aggregate_contrasts'], right=method)['ndcg10']
            row += [r'\textcolor{gainGreen}{'+signed(c['delta'])+'}', interval(c['ci_bonferroni_family95'])]
            rec.update(delta=c['delta'], family_ci=c['ci_bonferroni_family95'])
        rows.append(row)
        records.append(rec)
    table('dev_macro.tex', 'Development means at matched 1,024-pair supervision, equally weighting 24 conditions. Differences are ARC2 minus baseline; intervals give approximate 95\\% family coverage. Bold/underline mark the best/second unrounded adapter means; blue identifies ARC2.',
          'tab:dev', 'lrrrr', ['Method', r'nDCG@10 $\uparrow$', r'R@100 $\uparrow$', '$\\Delta$ nDCG', 'Family interval'], rows,
          ['dev'], 'Means: equal arithmetic average of 24 condition means; differences/intervals: aggregate_contrasts.ndcg10.', records)
    rows = []
    for method in METHODS + ['full_x', 'full_y']:
        row = [r'\textbf{ARC2-Global}' if method == ARC else LABELS[method]]
        for pair in PAIRS:
            if method.startswith('full_'):
                value = mean('trec', method, pair)
                row.append(f'\\multicolumn{{3}}{{c}}{{{value:.4f} (native)}}')
            else:
                for b in BUDGETS:
                    val=ranked(mean('trec', method, pair, b),[mean('trec', m, pair, b) for m in METHODS])
                    if method != ARC:
                        c=find(D['trec']['contrasts'], pair=pair, budget=b, right=method)
                        if c['ndcg10']['family_interval_interpretation']=='above_zero':
                            val+=r'$^{\dagger}$'
                    row.append(val)
        rows.append(row)
    table('trec_means.tex', 'Prospective TREC-COVID nDCG@10 (higher is better), averaged over five seeds. $\\dagger$: positive ARC2-minus-baseline interval in the 30-contrast family. Unmarked baseline cells are unresolved. Bold/underline rank the six adapters before rounding; native references are separate.',
          'tab:trec', 'lrrrrrr', ['Method', '\\multicolumn{3}{c}{MiniLM $\\rightarrow$ DistilRoBERTa}', '\\multicolumn{3}{c}{E5-small $\\rightarrow$ E5-base}'],
          [['', '25\\%', '50\\%', '75\\%', '25\\%', '50\\%', '75\\%']] + rows,
          ['trec'], 'means filtered by method/pair/budget; ndcg10.mean.')
    rows, paid_records = [], []
    for method in METHODS + ['full_x', 'full_y']:
        row = [r'\textbf{ARC2-Global}' if method == ARC else LABELS[method]]
        for pair in PAIRS:
            if method.startswith('full_'):
                n = mean('allpaid', method, pair)
                r = mean('allpaid', method, pair, metric='recall100')
                row += [f'\\multicolumn{{2}}{{c}}{{{n:.4f} (native)}}', f'{r:.4f}']
            else:
                fixed = mean('allpaid', method, pair, regime='fixed1024')
                n = mean('allpaid', method, pair, regime='allpaid28819')
                r = mean('allpaid', method, pair, metric='recall100', regime='allpaid28819')
                fixed_cell=ranked(fixed,[mean('allpaid', m, pair,regime='fixed1024') for m in METHODS])
                n_cell=ranked(n,[mean('allpaid', m, pair,regime='allpaid28819') for m in METHODS])
                if method != ARC:
                    c=find(D['allpaid']['contrasts'],pair=pair,kind='arc2_allpaid_vs_baseline_allpaid',
                           right={'method':method,'regime':'allpaid28819'})['ndcg10']
                    decision=c['family_interval_interpretation']
                    if decision=='above_zero': n_cell+=r'$^{\dagger}$'
                    elif decision=='below_zero': n_cell+=r'$^{\ddagger}$'
                row += [fixed_cell, n_cell,
                        ranked(r,[mean('allpaid', m, pair,metric='recall100',regime='allpaid28819') for m in METHODS])]
                paid_records.append({'method': method, 'pair': pair, 'fixed_ndcg10': fixed, 'allpaid_ndcg10': n, 'allpaid_recall100': r})
        rows.append(row)
    table('allpaid.tex', 'FiQA at 50\\% coverage. Fixed/All fit 1,024/28,819 pairs; N/R denote nDCG@10/Recall@100. On All-N baseline cells, $\\dagger$/$\\ddagger$ mark positive/negative ARC2 differences in the 32-contrast family; unmarked comparisons are unresolved. Bold/underline rank matched adapter columns; native rows are references.',
          'tab:allpaid', 'lrrrrrr', ['Method', '\\multicolumn{3}{c}{MiniLM $\\rightarrow$ DistilRoBERTa}', '\\multicolumn{3}{c}{E5-small $\\rightarrow$ E5-base}'],
          [['', 'Fixed N', 'All N', 'All R', 'Fixed N', 'All N', 'All R']] + rows,
          ['allpaid'], 'means filtered by method/pair/regime; fixed/all-paid cells use exactly the same paid IDs.', paid_records)
    csvout('allpaid_values.csv', paid_records, ['allpaid'], 'means filtered by method/pair/regime.')
    rows, ablation = [], []
    descriptions = ['Two steps minus zero steps', 'Two steps minus one step', 'ARC2 minus affine ridge', '$\\lambda=1$ minus $\\lambda=10$', '$\\lambda=100$ minus $\\lambda=10$']
    for description, c in zip(descriptions, D['mechanism']['overall_macro']):
        m = c['ndcg10']
        ci = m['ci99_bonferroni_family95']
        rows.append([description, signed(m['delta']), interval(ci)])
        ablation.append({'contrast': description, 'left': c['left'], 'right': c['right'], 'delta': m['delta'], 'low': ci[0], 'high': ci[1]})
    table('ablation.tex', 'Development ablations with saved 99\\% individual intervals (approximate 95\\% coverage of the separately predeclared five-contrast family). All other settings are fixed; the locked method retains $\\lambda=10$ and two steps.',
          'tab:ablation', 'lrr', ['Contrast', '$\\Delta$ nDCG@10', 'Family interval'], rows,
          ['mechanism'], 'overall_macro[*].ndcg10.delta and ci99_bonferroni_family95.', ablation)
    csvout('ablation_values.csv', ablation, ['mechanism'], 'overall_macro, saved intervals; no new uncertainty calculation.')
    counts = []
    for pair in PAIRS:
        for baseline in METHODS[1:]:
            cs = [r for r in D['trec']['contrasts'] if r['pair'] == pair and r['right'] == baseline]
            decisions = [r['ndcg10']['family_interval_interpretation'] for r in cs]
            counts.append({'pair': pair, 'baseline': baseline, 'positive': decisions.count('above_zero'), 'unresolved': decisions.count('unresolved'), 'negative': decisions.count('below_zero'), 'negative_point_means': sum(c['ndcg10']['delta'] < 0 for c in cs)})
    csvout('trec_family_counts.csv', counts, ['trec'], 'Count signs of saved contrasts.ndcg10.ci_bonferroni_family95, separately from point signs.')
    family_rows = []
    for b in METHODS[1:]:
        a, e = [find(counts, pair=p, baseline=b) for p in PAIRS]
        family_rows.append([LABELS[b], f"{a['positive']}/{a['unresolved']}/{a['negative']}", f"{e['positive']}/{e['unresolved']}/{e['negative']}"])
    table('trec_family.tex', 'The entire prospective nDCG family: positive / unresolved / negative intervals across the three budgets, using the locked 30-comparison correction. Point differences and interval decisions are distinct.',
          'tab:trec-family', 'lcc', ['Baseline', 'MiniLM migration', 'E5 migration'], family_rows, ['trec'], 'Count family_interval_interpretation across all three budgets.', counts)
    return ablation


def build_budget_and_recall_tables():
    """Expose existing operating points; add no hypothesis test or interpolation."""
    records, rows = [], []
    pair='e5_small_base'
    for dataset in DATASETS+['TREC-COVID']:
        key='trec' if dataset=='TREC-COVID' else 'dev'
        values={
            'arc2_25':mean(key,ARC,pair,'25pct',dataset=dataset),
            'procrustes_25':mean(key,'procrustes_global',pair,'25pct',dataset=dataset),
            'la2m_25':mean(key,'la2m20_integration_script_adaptation',pair,'25pct',dataset=dataset),
            'simplelinear_75':mean(key,'simplelinear_official_final50_mlp5',pair,'75pct',dataset=dataset),
            'ridge_75':mean(key,'ridge_affine_l10_bias_regularized',pair,'75pct',dataset=dataset),
            'converter_75':mean(key,'embedding_converter_paper_spec',pair,'75pct',dataset=dataset),
            'full_x':mean(key,'full_x',pair,dataset=dataset),
            'full_y':mean(key,'full_y',pair,dataset=dataset)}
        assert values['arc2_25']>values['converter_75'] and values['arc2_25']>values['ridge_75']
        record={'dataset':dataset,'role':'prospective' if key=='trec' else 'development',**values,
                'arc2_minus_converter75':values['arc2_25']-values['converter_75'],
                'arc2_minus_ridge75':values['arc2_25']-values['ridge_75']}
        records.append(record)
        name=r'\textbf{TREC-COVID}' if key=='trec' else dataset
        row=[name,r'\cellcolor{arcPale}\textcolor{arcBlue}{'+f"{values['arc2_25']:.4f}"+'}']
        row += [f'{values[k]:.4f}' for k in list(values)[1:]]
        if key=='trec': row[0]=r'\midrule '+row[0]
        rows.append(row)
    table('budget_leverage.tex', 'E5 nDCG: ARC2 at 25\\% exceeds Converter and ridge at 75\\% on all five collections. Blue identifies ARC2. Proc.: Procrustes; SL: SimpleLinear; native references show full-corpus quality. TREC-COVID is prospective; other rows are development. Cross-budget point comparisons are post-hoc descriptive.',
          'tab:budget-leverage','lrrrrrrrr',
          ['Collection',r'\multicolumn{3}{c}{25\% coverage}',r'\multicolumn{3}{c}{75\% coverage}',r'\multicolumn{2}{c}{Native}'],
          [['','ARC2','Proc.','LA2M20','SL','Ridge','Conv.','Full-X','Full-Y']]+rows,
          ['dev','trec'],'Saved means only; post-hoc cross-budget description, no new interval/test, interpolation or physical cost claim.',records,
          header_rule=r'\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-9}',highlight_arc=False,tabcolsep=2.5)
    csvout('budget_leverage_values.csv',records,['dev','trec'],'Exact values behind the post-hoc cross-budget table; no new scientific run.')
    recall_rows=[]
    for method in METHODS+['full_x','full_y']:
        row=[r'\textbf{ARC2-Global}' if method==ARC else LABELS[method]]
        for pair in PAIRS:
            if method.startswith('full_'):
                row.append(r'\multicolumn{3}{c}{'+f"{mean('trec',method,pair,metric='recall100'):.4f}"+' (native)}')
            else:
                for budget in BUDGETS:
                    value=mean('trec',method,pair,budget,metric='recall100')
                    row.append(ranked(value,[mean('trec',m,pair,budget,metric='recall100') for m in METHODS]))
        recall_rows.append(row)
    table('trec_recall.tex','Companion prospective Recall@100 means (higher is better). All queries and five seeds are retained. Bold/underline rank the six adapters before rounding. Recall is auxiliary/descriptive and receives no nDCG-family significance markers.',
          'tab:trec-recall','lrrrrrr',['Method',r'\multicolumn{3}{c}{MiniLM $\rightarrow$ DistilRoBERTa}',r'\multicolumn{3}{c}{E5-small $\rightarrow$ E5-base}'],
          [['','25\\%','50\\%','75\\%','25\\%','50\\%','75\\%']]+recall_rows,
          ['trec'],'All saved Recall@100 mean rows; complete point means also plotted in prospective figure.')
    return records

COLORS = ['#0F4D92', '#767676', '#42949E', '#9A4D8E', '#B64342', '#A88420']
MARKERS = ['o', 's', '^', 'D', 'v', 'P']
STYLES = ['-', '--', '-.', ':', '--', '-.']
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Computer Modern Roman'],
                     'text.usetex': True,
                     'text.latex.preamble': r'\usepackage{amsmath}\usepackage[T1]{fontenc}\usepackage{lmodern}',
                     'mathtext.fontset': 'cm', 'axes.unicode_minus': False, 'font.size': 8,
                     'axes.titlesize': 8.5, 'axes.labelsize': 8,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8,
                     'legend.fontsize': 8, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.linewidth': .7,
                     'legend.frameon': False, 'svg.fonttype': 'none',
                     'pdf.fonttype': 42, 'savefig.facecolor': 'white'})

def savefig(fig, name, keys, operation, records):
    for suffix in ('pdf', 'svg', 'png'):
        p = FIG / (name + '.' + suffix)
        fig.savefig(p, dpi=400, metadata={'Creator': 'ARC2 manuscript evidence builder'} if suffix == 'pdf' else None)
        provenance(p.relative_to(PAPER).as_posix(), keys, operation, records)
    plt.close(fig)

def curves(key, name, macro=False):
    from plot_publication import quality_figure
    rows = []
    for pair in PAIRS:
        for method in METHODS+['full_x','full_y']:
            for budget in (['native'] if method.startswith('full_') else BUDGETS):
                selected=None if budget=='native' else budget
                row={'pair':pair,'method':method,'budget':budget,
                     'ndcg10':mean(key,method,pair,selected)}
                if not macro:row['recall100']=mean(key,method,pair,selected,metric='recall100')
                rows.append(row)
    fig=quality_figure(rows,macro=macro)
    savefig(fig, name, [key], 'Each point is the saved five-seed condition mean' + (' averaged equally over all four DEV datasets.' if macro else '; both primary nDCG and auxiliary Recall are shown.') + ' No fabricated interval bands. Full-X/Y are native reference operating points. Only measured budget points are connected.', rows)
    csvout(name + '_values.csv', rows, [key], 'Same values plotted, extracted from means.ndcg10.mean; equal dataset weight for DEV.')

def ablation_plot(records):
    from plot_publication import ablation_with_matched_controls
    fig=ablation_with_matched_controls(records,D['matched']['primary_contrasts'])
    savefig(fig, 'dev_ablation', ['mechanism','matched'], 'Panel a: saved 99% five-contrast macro intervals; panel b: saved 98.75% original K4 intervals for two MiniLM matched-target controls. No new test or pooled intervals.', {'macro':records,'matched':D['matched']['primary_contrasts']})


def matched_verification():
    base=(ROOT/PATHS['matched']).parent
    cells=json.loads((base/'cell_index.json').read_text());values=np.load(base/'per_query.npy',allow_pickle=False)
    if values.shape!=(20,500,2):raise ValueError('Require all20 matched-target cells')
    by={(c['seed'],c['method']):values[i] for i,c in enumerate(cells)}
    for row in D['matched']['means']:
        arr=np.stack([by[s,row['method']] for s in [17,29,41,53,67]])
        np.testing.assert_allclose(arr.mean(axis=(0,1)),[row['ndcg10'],row['recall100']],rtol=0,atol=1e-12)
    counts={}
    for c in D['matched']['primary_contrasts']:
        delta=np.stack([by[s,'tangent2'][:,0]-by[s,c['right']][:,0] for s in [17,29,41,53,67]])
        assert abs(delta.mean()-c['delta_ndcg10'])<1e-12
        counts[c['right']]=int((delta.mean(axis=1)>0).sum())
        assert counts[c['right']]==5
    for p in [base/'cell_index.json',base/'per_query.npy',base/'bootstrap_draws.npy']:
        rel=p.relative_to(ROOT).as_posix();SOURCES[rel]={'path':rel,'sha256':sha(p)}
    csvout('matched_target_values.csv',D['matched']['means'],['matched'],'All four matched-control means, including B0 context.')
    return {'rankings':20,'positive_seed_means':counts,'means':D['matched']['means'],'contrasts':D['matched']['primary_contrasts'],'family':D['matched']['bootstrap']}

def final_verification():
    checks = {}
    for key in ['dev', 'allpaid', 'trec']:
        checks[key] = verify_means(key)
    for key, field in [('dev', 'condition_contrasts'), ('trec', 'contrasts')]:
        for c in D[key][field]:
            for metric in ['ndcg10', 'recall100']:
                kw = dict(pair=c['pair'], budget=c['budget'], metric=metric, dataset=c['dataset'])
                actual = mean(key, c['left'], **kw) - mean(key, c['right'], **kw)
                assert abs(actual - c[metric]['delta']) < 1e-12
    decisions = [c['ndcg10']['family_interval_interpretation'] for c in D['trec']['contrasts']]
    counts = [decisions.count(s) for s in ['above_zero', 'unresolved', 'below_zero']]
    assert counts == [11, 19, 0]
    assert all(c['ndcg10']['delta'] < 0 for c in D['trec']['contrasts'] if c['right'] == 'procrustes_global')
    checks['trec_primary_counts'] = counts
    below = {}
    for native in ['full_x', 'full_y']:
        cells = [r for r in D['dev']['means'] if r['method'] == ARC]
        count = sum(r['ndcg10']['mean'] < mean('dev', native, r['pair'], dataset=r['dataset']) for r in cells)
        assert count == 24
        below[native] = count
    checks['dev_ARC2_ndcg_below_native_references'] = below
    checks['no_new_experiment'] = 'Only completed scoring JSON and saved per-query metric NPY read; qrels never read.'
    write('verification.json', json.dumps(checks, indent=2) + '\n', ['dev', 'allpaid', 'trec'], 'Checks saved means against all per-query arrays and matched point contrasts against arithmetic.')
    return checks

def main():
    ablation = build_tables()
    matched=matched_verification()
    budget_leverage=build_budget_and_recall_tables()
    curves('dev', 'dev_quality', macro=True)
    curves('trec', 'trec_quality')
    ablation_plot(ablation)
    checks = final_verification()
    for key in ['dev', 'trec']:
        rows = []
        for r in D[key]['means']:
            rows.append({k: r[k] for k in ['dataset', 'pair', 'budget', 'method']} | {'ndcg10': r['ndcg10']['mean'], 'recall100': r['recall100']['mean']})
        csvout(key + '_complete_means.csv', rows, [key], 'All condition and native-reference means copied from the completed scorer JSON.')
    # The numeric prose ledger includes exact values before manuscript rounding.
    gallery = [r for r in D['gallery']['aggregate_five_seed_conditions'] if r['dataset'] == 'FiQA' and r['method'] == ARC and r['regime'] == 'allpaid28819']
    numeric_claims = {'development': D['dev']['aggregate_contrasts'],
                      'mechanism': D['mechanism']['overall_macro'],
                      'matched_target_controls': matched,
                      'prospective': D['trec']['contrasts'],
                      'allpaid': D['allpaid']['contrasts'],
                      'mixed_gallery_example': gallery,
                      'posthoc_cross_budget_e5': budget_leverage,
                      'structural_parameters': {'coefficients': (384 + 1) * 768,
                                                 'float32_bytes': (384 + 1) * 768 * 4,
                                                 'MiB': (384 + 1) * 768 * 4 / 2**20}}
    write('numeric_claims.json', json.dumps(numeric_claims, indent=2) + '\n', ['dev', 'mechanism', 'matched', 'trec', 'allpaid', 'gallery'], 'Exact raw-scored numeric ledger for prose; structural parameter arithmetic is not measured runtime/storage.')
    for name, keys, op in [
        ('sections/experimental-setup.tex', ['dev_lock', 'trec_lock', 'paid_lock', 'dev', 'gallery'], 'Collection query counts from qrel_stats; document counts from raw gallery case counts and TREC acquisition lock; dimensions and training policies from locks; selection/search policies from committed protocols and numerics.py.'),
        ('sections/results.tex', ['dev', 'mechanism', 'matched', 'trec', 'allpaid', 'gallery'], 'Numeric prose is rounded from generated/numeric_claims.json. DEV pair macros are equal-condition means. Matched target intervals retain original K4; E5 pending. G paid_top10: paid_returned_share.after.top10.mean = 0.06472000000000001.')]:
        provenance(name, keys, op)
    for name, item in ITEMS.items():
        p = PAPER / name
        item['sha256'] = sha(p)
    mapping = {'schema': 'arc2-paper-evidence-map-v1',
               'generator': {'path': 'paper/scripts/build_evidence.py', 'sha256': sha(Path(__file__))},
               'policy': 'All scientific values from completed raw-scored JSON/NPY; no qrels, fitting, encoding or search. Saved intervals are copied, never recomputed or pooled.',
               'sources': SOURCES, 'artifacts': ITEMS, 'verification': checks}
    (REVIEW / 'EVIDENCE_MAP.json').write_text(json.dumps(mapping, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(checks, indent=2))

if __name__ == '__main__':
    main()
