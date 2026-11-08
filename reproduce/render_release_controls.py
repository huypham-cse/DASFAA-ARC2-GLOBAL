"""Render completed M/P/G controls from saved scorer JSONs, without scoring.

The default input is the clean supervisor release. Output must be a new
directory: either results/control_figures (initial packaging) or a directory
under checks/. Existing directories are never overwritten. No qrels,
models, rankings, fitted objects, or resampling routines are accessed.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

HERE = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = HERE if (HERE / 'CLAIM_LOCK.json').exists() else HERE.with_name('DASFAA-2027-paper-release')
PRIMARY = 'arc2_global_tangent2_r1'
METHODS = {
    PRIMARY: 'ARC2-Global',
    'procrustes_global': 'Procrustes adaptation',
    'la2m20_integration_script_adaptation': 'LA2M20 adaptation',
    'simplelinear_official_final50_mlp5': 'SimpleLinear (official)',
    'ridge_affine_l10_bias_regularized': 'Affine ridge',
    'embedding_converter_paper_spec': 'Converter adaptation',
}
COLORS = dict(zip(METHODS, ('#0F4D92', '#B64342', '#5B9B59', '#9A4D8E', '#42949E', '#A17C25')))
PAIRS = ('minilm_distilroberta', 'e5_small_base')
PAIR_LABELS = ('MiniLM → DistilRoBERTa', 'E5-small → E5-base')
SOURCES = {
    'M': 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
    'P': 'results/b1p_r5_review_20261027/scoring/results_summary.json',
    'G': 'results/b1g_r1_review_20261027/scoring/results_summary.json',
}
POSITIVE, NEGATIVE, UNRESOLVED = '#0F4D92', '#B64342', '#767676'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def status_color(status):
    return {'above_zero': POSITIVE, 'below_zero': NEGATIVE, 'unresolved': UNRESOLVED}[status]


def check_interval(value, interval_key):
    lo, hi = value[interval_key]
    if not all(math.isfinite(v) for v in (lo, hi, value['delta'])) or lo > hi:
        raise ValueError('Invalid saved interval')
    decision = 'above_zero' if lo > 0 else 'below_zero' if hi < 0 else 'unresolved'
    if decision != value['family_interval_interpretation']:
        raise ValueError('Saved family interval and decision disagree')


def load_sources(root):
    summaries, inputs = {}, []
    for study, relative in SOURCES.items():
        path = root / relative
        summary = read_json(path)
        completed_path = path.with_name('completed.json')
        completed = read_json(completed_path)
        saved_hash = completed.get('summary_sha256') or completed.get('artifact_sha256', {}).get(path.name)
        if saved_hash != digest(path):
            raise ValueError(f'{study} completed receipt does not bind saved summary')
        if summary.get('failures'):
            raise ValueError(f'{study} scorer has unresolved failures')
        summaries[study] = summary
        inputs.extend({'study': study, 'path': p.relative_to(root).as_posix(), 'sha256': digest(p)}
                      for p in (path, completed_path))
    if summaries['M']['status'] != 'DEV_SCORED' or summaries['M']['ranking_cells'] != 736:
        raise ValueError('Require completed 736-ranking mechanism study')
    if len(summaries['M']['overall_macro']) != 5:
        raise ValueError('Require all five locked mechanism macro contrasts')
    if summaries['P']['status'] != 'DEV_SCORED' or len(summaries['P']['contrasts']) != 32:
        raise ValueError('Require completed 32-contrast all-paid study')
    if (summaries['G']['status'], summaries['G']['partial_cases'], summaries['G']['pure_fitted_galleries']) != ('B1G_DEV_SCORED', 450, 210):
        raise ValueError('Require complete G diagnostics')
    if len(summaries['G']['aggregate_five_seed_conditions']) != 90:
        raise ValueError('Require all 90 G five-seed conditions')
    return summaries, inputs


def plotting():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ('Arial', 'Helvetica', 'DejaVu Sans') if f in available]
    plt.rcParams.update({'font.family': fonts, 'font.size': 10, 'axes.linewidth': 1.0,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'legend.frameon': False, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
                         'svg.hashsalt': 'arc2-control-figures-r1', 'axes.labelsize': 10,
                         'xtick.labelsize': 9, 'ytick.labelsize': 10})
    return plt, {'matplotlib': matplotlib.__version__, 'font_family': fonts,
                 'font_path': font_manager.findfont(font_manager.FontProperties(family=fonts)),
                 'dpi': 300, 'colors': COLORS, 'style': 'existing ARC2 release / figures4papers house style'}


def save(fig, folder, stem):
    from PIL import Image
    import xml.etree.ElementTree as ET
    outputs = []
    for extension in ('pdf', 'svg', 'png'):
        path = folder / f'{stem}.{extension}'
        meta = {'CreationDate': None, 'ModDate': None, 'Creator': 'ARC2 saved-controls renderer'} if extension == 'pdf' else {'Date': None} if extension == 'svg' else {'Software': 'ARC2 saved-controls renderer'}
        fig.savefig(path, dpi=300, facecolor='white', bbox_inches='tight', pad_inches=.12, metadata=meta)
        outputs.append(path)
    with Image.open(folder / f'{stem}.png') as im:
        if min(im.size) < 1000 or min(im.info.get('dpi', (0, 0))) < 299:
            raise ValueError('PNG size/DPI export failed')
        qa = {'png_size': list(im.size), 'png_dpi': list(im.info['dpi'])}
    ET.parse(folder / f'{stem}.svg')
    if not (folder / f'{stem}.pdf').read_bytes().startswith(b'%PDF'):
        raise ValueError('Invalid PDF export')
    return outputs, qa


def mechanism(plt, summary, folder):
    labels = ('ARC2 − zero-step Procrustes', 'ARC2 − one tangent step', 'ARC2 − affine ridge',
              'λ=1 two-step − locked ARC2', 'λ=100 two-step − locked ARC2')
    rows = []
    for label, raw in zip(labels, summary['overall_macro']):
        v = raw['ndcg10']; check_interval(v, 'ci99_bonferroni_family95')
        rows.append({'contrast': label, 'left': raw['left'], 'right': raw['right'], 'metric': 'ndcg10',
                     'delta': v['delta'], 'interval_low': v['ci99_bonferroni_family95'][0],
                     'interval_high': v['ci99_bonferroni_family95'][1],
                     'decision': v['family_interval_interpretation'], 'per_interval_confidence': .99,
                     'family_size': 5, 'strata': 24, 'scope': 'inspected DEV'})
    if [(r['left'], r['right']) for r in rows] != [
        (PRIMARY, 'procrustes_global'), (PRIMARY, 'tangent1_l10'),
        (PRIMARY, 'ridge_affine_l10_bias_regularized'), ('tangent2_l1', PRIMARY), ('tangent2_l100', PRIMARY)]:
        raise ValueError('Unexpected M contrast order/identity')
    fig, ax = plt.subplots(figsize=(12.2, 4.5))
    fig.subplots_adjust(left=.29, right=.70, top=.83, bottom=.25)
    for y, row in enumerate(rows):
        c = status_color(row['decision']); x = row['delta']
        ax.errorbar(x, y, xerr=[[x-row['interval_low']], [row['interval_high']-x]],
                    fmt='o', color=c, capsize=4, markersize=6, linewidth=1.8)
        ax.text(1.035, y, f"{x:+.6f}  [{row['interval_low']:+.6f}, {row['interval_high']:+.6f}]",
                transform=ax.get_yaxis_transform(), va='center', fontsize=10, color=c)
    ax.axvline(0, color='#4D4D4D', lw=.9, ls='--')
    ax.set_yticks(range(5), labels); ax.invert_yaxis(); ax.set_ylim(4.55, -.55)
    ax.set_xlim(-.028, .13); ax.set_xlabel('Macro Δ nDCG@10 (left method − right method)')
    ax.grid(axis='x', alpha=.15); ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0, pad=9)
    fig.suptitle('B1-M · Mechanism and sensitivity controls', x=.29, y=.97, ha='left', fontsize=15, fontweight='bold')
    fig.text(.29, .88, 'All five predeclared macro comparisons · saved 99% family intervals', fontsize=11)
    fig.text(.29, .115, 'Four inspected DEV collections · two encoder pairs · 25/50/75% budgets · five seeds averaged first', fontsize=9)
    fig.text(.29, .065, 'Equal weighting of 24 conditions. Approximate 95% coverage for the five-contrast family.', fontsize=9)
    fig.text(.29, .015, 'ARC2 remains λ=10 / two steps. λ=1 is unresolved; no post-score selection or independent ablation claim.', fontsize=9)
    write_csv(folder/'b1m_mechanism_controls.csv', rows)
    outputs, qa = save(fig, folder, 'b1m_mechanism_controls'); plt.close(fig)
    return rows, outputs, qa


def allpaid(plt, summary, folder):
    baselines = list(METHODS)[1:]
    kinds = ('arc2_allpaid_vs_baseline_allpaid', 'arc2_fixed_vs_baseline_allpaid')
    lookup = {(r['pair'], r['kind'], r['right']['method']): r for r in summary['contrasts'] if r['kind'] in kinds}
    if len(lookup) != 20:
        raise ValueError('Require all 20 fixed/all-paid versus all-paid contrasts')
    rows = []
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.3))
    fig.subplots_adjust(left=.17, right=.975, bottom=.19, top=.82, wspace=.55, hspace=.55)
    for i, kind in enumerate(kinds):
        for j, pair in enumerate(PAIRS):
            ax = axes[i, j]
            for y, method in enumerate(baselines):
                raw=lookup[pair,kind,method]; v=raw['ndcg10']; check_interval(v, 'ci_bonferroni_family95')
                if abs(v['per_interval_confidence']-.9984375) > 1e-14:
                    raise ValueError('Wrong P family interval coverage')
                lo,hi=v['ci_bonferroni_family95']; x=v['delta']; c=status_color(v['family_interval_interpretation'])
                ax.errorbar(x,y,xerr=[[x-lo],[hi-x]],fmt='o',color=c,linewidth=1.8,capsize=3,markersize=5)
                ax.text(.985,y,f'{x:+.4f}',transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=9,color=c,
                        bbox={'facecolor':'white','edgecolor':'none','pad':1.2})
                rows.append({'pair':pair,'kind':kind,'left_method':raw['left']['method'],'left_regime':raw['left']['regime'],
                             'baseline':method,'right_regime':raw['right']['regime'],'delta':x,'interval_low':lo,'interval_high':hi,
                             'decision':v['family_interval_interpretation'],'per_interval_confidence':v['per_interval_confidence'],
                             'family_size':32,'metric':'ndcg10','dataset':'FiQA','paid_documents':28819,'budget':'50pct'})
            ax.axvline(0,color='#4D4D4D',ls='--',lw=.9); ax.set_xlim(-.10,.19)
            ax.set_ylim(4.65,-.65); ax.set_yticks(range(5),[METHODS[m] for m in baselines])
            ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0,pad=7);ax.grid(axis='x',alpha=.15)
            ax.set_xlabel('Δ nDCG@10 (ARC2 − baseline)')
            fit='all 28,819 paid pairs' if i==0 else 'fixed 1,024 anchors'
            ax.set_title(f'({chr(97+i*2+j)}) {PAIR_LABELS[j]}\nARC2 fit: {fit}',loc='left',fontsize=11,pad=13)
    from matplotlib.lines import Line2D
    handles=[Line2D([],[],marker='o',linestyle='none',color=c,label=label) for c,label in
             [(POSITIVE,'Family interval above zero'),(UNRESOLVED,'Unresolved'),(NEGATIVE,'Family interval below zero')]]
    fig.suptitle('B1-P · All-paid supervision changes the comparison',x=.17,y=.975,ha='left',fontsize=15,fontweight='bold')
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.16,.935),ncol=3,fontsize=9)
    fig.text(.17,.115,'FiQA inspected DEV · same 50% destination budget (28,819 unique documents, anchors included) · five-seed means',fontsize=9)
    fig.text(.17,.080,'All baselines fit all 28,819 paid pairs. Top: ARC2 uses all paid pairs. Bottom: ARC2 uses 1,024 anchors.',fontsize=9)
    fig.text(.17,.045,'Saved 99.84375% intervals from the full 32-contrast family (~95% coverage); 20 contrasts shown, no new correction.',fontsize=9)
    fig.text(.17,.010,'Procrustes/LA2M/Converter are qualified adaptations; SimpleLinear: official five-layer MLP, final50; ridge: λ10, bias regularized.',fontsize=8.5)
    write_csv(folder/'b1p_allpaid_controls.csv',rows)
    outputs,qa=save(fig,folder,'b1p_allpaid_controls');plt.close(fig)
    return rows,outputs,qa


def mixed(plt, summary, folder):
    all_rows=[]
    for r in summary['aggregate_five_seed_conditions']:
        row={k:r[k] for k in ('dataset','pair','method','regime','budget')}
        row['seed_count']=len(r['seeds'])
        for metric in ('ndcg10','recall100'):
            for endpoint in ('before','after','delta_of_query_means'):
                row[f'{metric}_{endpoint}']=r['metrics'][metric][endpoint]['mean']
        row['unpaid_signed_bias']=r['paired_signed_bias']['unpaid']['mean']
        for endpoint in ('before','after'):
            row[f'paid_top10_{endpoint}']=r['paid_returned_share'][endpoint]['top10']['mean']
        all_rows.append(row)
    rows=[r for r in all_rows if r['dataset']=='FiQA' and r['regime']=='allpaid28819' and r['budget']=='50pct']
    lookup={(r['pair'],r['method']):r for r in rows}
    if set(lookup)!={(p,m) for p in PAIRS for m in METHODS}:
        raise ValueError('Require all six methods / both pairs in FiQA50 all-paid view')
    fig,axes=plt.subplots(2,2,figsize=(12.6,8.3))
    fig.subplots_adjust(left=.17,right=.975,bottom=.19,top=.82,wspace=.55,hspace=.56)
    for i,metric in enumerate(('ndcg10','recall100')):
        for j,pair in enumerate(PAIRS):
            ax=axes[i,j]
            for y,method in enumerate(METHODS):
                row=lookup[pair,method];a=row[f'{metric}_before'];b=row[f'{metric}_after'];c=COLORS[method]
                ax.plot([a,b],[y,y],color=c,lw=2,zorder=1)
                ax.plot(a,y,marker='o',mfc='white',mec=c,mew=1.5,ms=6,linestyle='none',zorder=3)
                ax.plot(b,y,marker='s',mfc=c,mec=c,ms=5.5,linestyle='none',zorder=4)
                delta=row[f'{metric}_delta_of_query_means']
                ax.text(.99,y,f'{delta:+.4f}',transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=9,color=c,
                        bbox={'facecolor':'white','edgecolor':'none','pad':1})
            ax.set_xlim((.10,.42) if i==0 else (.30,.75));ax.set_ylim(5.7,-.7)
            ax.set_yticks(range(6),list(METHODS.values()));ax.tick_params(axis='y',length=0,pad=7)
            ax.spines['left'].set_visible(False);ax.grid(axis='x',alpha=.15)
            ax.set_xlabel('nDCG@10' if metric=='ndcg10' else 'Recall@100')
            ax.set_title(f'({chr(97+i*2+j)}) {PAIR_LABELS[j]}',loc='left',fontsize=11,pad=13)
    from matplotlib.lines import Line2D
    handles=[Line2D([],[],marker='o',mfc='white',mec='#4D4D4D',linestyle='none',label='Before: proxy-only gallery'),
             Line2D([],[],marker='s',color='#4D4D4D',linestyle='none',label='After: actual paid-vector replacement')]
    fig.suptitle('B1-G · The actual mixed gallery can reverse the proxy-only ordering',x=.17,y=.975,ha='left',fontsize=14,fontweight='bold')
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.16,.935),ncol=2,fontsize=9)
    fig.text(.17,.115,'FiQA50 all-paid view · all six methods / both encoder pairs · same frozen fit and paid set at both endpoints',fontsize=9)
    fig.text(.17,.080,'Five-seed means; numbers at right are after − before. Descriptive diagnostics: no intervals or significance tests.',fontsize=9)
    fig.text(.17,.045,'Each fit already saw all 28,819 paid pairs; proxy-only predicts every row, including anchors. Before is a counterfactual.',fontsize=9)
    fig.text(.17,.010,'Inspected DEV; qualified baseline configurations as in B1-P. Full90-condition CSV retained; no causal calibration or cost claim.',fontsize=9)
    write_csv(folder/'b1g_proxy_mixed_controls.csv',rows);write_csv(folder/'b1g_all90_conditions.csv',all_rows)
    outputs,qa=save(fig,folder,'b1g_proxy_mixed_controls');plt.close(fig)
    return rows,outputs,qa


def output_directory(root, requested):
    if requested is None:
        output=root/'checks'/('control_figures_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    else:
        output=Path(requested)
        if not output.is_absolute():output=root/output
    output=output.resolve()
    try:relative=output.relative_to(root)
    except ValueError as error:raise ValueError('Output must remain inside the selected root') from error
    if not relative.parts or not (relative.as_posix()=='results/control_figures' or relative.parts[0]=='checks'):
        raise ValueError('Output allowed only in a new checks/ directory or initial results/control_figures')
    if output.exists():raise FileExistsError('Refuse to overwrite existing output; choose a fresh checks/ directory')
    return output


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=DEFAULT_ROOT,help='Input release root; default clean sibling release or this portable release')
    parser.add_argument('--output',help='Fresh output path within root (default unique checks/control_figures_UTC)')
    args=parser.parse_args(argv);root=args.root.resolve()
    summaries,inputs=load_sources(root)
    output=output_directory(root,args.output)
    plt,style=plotting();output.mkdir(parents=True,exist_ok=False)
    qa={};figures={}
    for study,renderer in (('M',mechanism),('P',allpaid),('G',mixed)):
        rows,files,checks=renderer(plt,summaries[study],output)
        qa[study]=checks
        figures[study]={'plotted_rows':len(rows),'artifacts':[{'path':p.name,'sha256':digest(p)} for p in files]}
    provenance={'status':'RENDERED_PENDING_VISUAL_QA','scope':'Saved JSON means/deltas/intervals only; no qrels, fitting, scoring, bootstrap or new CI',
                'inputs':inputs,'script_sha256':digest(Path(__file__)),'python':platform.python_version(),
                'style':style,'figures':figures,'format_checks':qa,
                'intervals':{'M':'saved99% intervals; five-comparison family, approximate95% coverage',
                             'P':'saved99.84375% intervals; original32-comparison family, approximate95% coverage',
                             'G':'descriptive five-seed before/after means; no intervals'},
                'subset':'G: full predeclared FiQA50 allpaid scope, all six methods/both pairs; all90 conditions exported',
                'rendered_utc':datetime.now(timezone.utc).isoformat()}
    provenance['csv_artifacts']=[{'path':p.name,'sha256':digest(p)} for p in sorted(output.glob('*.csv'))]
    write_json(output/'render_provenance.json',provenance)
    print(json.dumps({'status':provenance['status'],'output':str(output),'figure_count':len(figures)}))


if __name__=='__main__':
    main()
