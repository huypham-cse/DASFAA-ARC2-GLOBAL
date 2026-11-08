"""Generate report and paper tables from imported per-query measurements."""
from pathlib import Path
import csv
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'results/fiqa_development'
METHODS=['procrustes_tangent2_global','procrustes_global','embedding_converter_paper_spec_anchor1024']
NAMES=['ARC2-Global','A2M / Procrustes adaptation','Embedding-Converter adaptation']

def downstream_report_text(path):
    """Preserve the later B1-P/B1-G report when refreshing imported evidence."""
    if not path.exists():
        return ''
    original=path.read_text(encoding='utf-8-sig')
    starts=[]
    for phase in ('B1P','B1G'):
        begin=f'<!-- BEGIN {phase}_GENERATED -->'
        end=f'<!-- END {phase}_GENERATED -->'
        if begin not in original and end not in original:
            continue
        if original.count(begin)!=1 or original.count(end)!=1 or original.index(end)<original.index(begin):
            raise ValueError(f'Cannot refresh report with malformed {phase} section markers')
        starts.append(original.index(begin))
    return original[min(starts):] if starts else ''

def mechanism_lines():
    base=ROOT/'results/b1mp0_r1_review_20261026'
    path=base/'b1m_full_r1_20261026/scoring_r2_binary/results_summary.json'
    if not path.exists():return []
    verified=json.loads((ROOT/'provenance/qa/b1mp0_result_verification.json').read_text())
    assert verified['status']=='PASS'
    result=json.loads(path.read_text());primary='arc2_global_tangent2_r1'
    labels={primary:'ARC2-Global','procrustes_global':'Procrustes','tangent1_l10':'one tangent step','ridge_affine_l10_bias_regularized':'affine ridge','tangent2_l1':'two steps/lambda 1','tangent2_l100':'two steps/lambda 100'}
    lines=['','## B1-M mechanism development results (2026-10-26)','',
           'Four DEV collections, two encoder pairs, five seeds,25/50/75% budgets:720 partial rankings+16 full references. Equal weight over 24 collection/pair/budget strata.',
           'Both numerical primary files and all 736 rankings remain frozen; the binary Nano parser repair used a separate committed scorer and preserved the failed original attempt.','',
           '| Contrast | Macro absolute delta nDCG@10 | 99% interval (five-contrast family) | Higher-mean conditions |',
           '|---|---:|---|---:|']
    for row in result['overall_macro']:
        metric=row['ndcg10'];ci=metric['ci99_bonferroni_family95']
        cells=[c for c in result['contrasts'] if c['left']==row['left'] and c['right']==row['right']]
        wins=sum(c['ndcg10']['delta']>0 for c in cells)
        lines.append(f"| {labels[row['left']]} minus {labels[row['right']]} | {metric['delta']:+.6f} | [{ci[0]:+.6f}, {ci[1]:+.6f}] | {wins}/24 |")
    e5=next(r for r in result['per_encoder_macro'] if r['scope']=='e5_small_base' and r['left']==primary and r['right']=='procrustes_global')
    lines+=['',f"Two-step refinement has positive aggregate development nDCG effects versus zero steps, one step and ridge. E5 Recall@100 has a tradeoff: macro delta {e5['recall100']['delta']:+.6f} vs Procrustes; not every condition or metric improves.",
           'Lambda1 has an unresolved aggregate nDCG difference from fixed lambda 10; lambda 100 has lower aggregate nDCG. The primary method stays two steps/lambda 10.',
           'Intervals describe these selected DEV collections conditional on five fixed mapping seeds; they are not independent confirmation. Full references, all per-condition values and negatives remain in the detailed report.',
           'B1-P0 passed 31 synthetic cases and 120 real fixed-anchor budget comparisons, with exact ordered top100 identity throughout. It establishes numerical readiness for the separately reported all-paid check; consult the live tracker for completion. Physical cost/SLO remains unmeasured.',
           '[Summary and preserved attempts](results/b1mp0_r1_review_20261026/SUMMARY.md). [All measured rows and intervals](results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.md).','']
    return lines

def main():
    later=downstream_report_text(ROOT/'REPORT.md')
    (ROOT/'manuscript/generated').mkdir(parents=True,exist_ok=True)
    data=json.loads((P/'summary.json').read_text(encoding='utf-8'))
    cells=json.loads((P/'metric_index.json').read_text(encoding='utf-8'))['cells']
    metrics=np.load(P/'per_query.npy',allow_pickle=False)
    lookup={(r['pair'],r['budget'],r['method']):r for r in data['summary']}
    rows=[]
    for pair in data['pairs']:
        for budget in ['25pct','50pct']:
            for method,name in zip(METHODS,NAMES):
                positions=[i for i,c in enumerate(cells) if (c['pair'],c['budget'],c['method'])==(pair,budget,method)]
                assert len(positions)==5
                means=metrics[positions].mean(axis=(0,1)); original=lookup[(pair,budget,method)]
                assert abs(means[0]-original['ndcg10'])<1e-12
                assert abs(means[1]-original['recall100'])<1e-12
                rows.append({'pair':pair,'budget':budget,'method':name,'ndcg10':float(means[0]),'recall100':float(means[1])})
    with (P/'comparison.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    lines=['# ARC2-Global: measured development results','',
           'FiQA: 57,638 documents, 500 DEV queries, five fixed seeds; exact top-100 search.',
           'Two encoder pairs, 1,024 fitting anchors. At 25%/50%, 14,409/28,819 unique destination documents (anchors included).',
           'Method selected after viewing development scores; this is not independent confirmation.','',
           '| Encoder pair | Budget | Method | nDCG@10 | Recall@100 |',
           '|---|---|---|---:|---:|']
    for r in rows:
        lines.append(f"| {r['pair']} | {r['budget']} | {r['method']} | {r['ndcg10']:.6f} | {r['recall100']:.6f} |")
    lines+=['','## Full-index references','', '| Pair | Reference | nDCG@10 | Recall@100 |','|---|---|---:|---:|']
    for r in data['references']:
        lines.append(f"| {r['pair']} | {r['method']} | {r['ndcg10']:.6f} | {r['recall100']:.6f} |")
    lines+=['','## Interpretation','',
        'ARC2-Global has higher mean nDCG@10 than both external adaptations in all four encoder/budget conditions.',
        'The E5 gain over plain Procrustes is small (+0.001329/+0.001599 absolute). These imported means did not include candidate-specific intervals; the later B1-M section reports its locked contrast intervals.',
        'E5 Recall@100 is lower than plain Procrustes at both budgets. Both full-index references have higher nDCG@10 than the partial ARC2-Global index.',
        'The neural baseline is a 1,024-anchor paper-spec adaptation, not the published multi-corpus training setup or an official-code reproduction.',
        'Its 896/128 anchor split selects a checkpoint, then it refits all 1,024 anchors. Target backfill vectors are not extra training examples in this comparison.',
        'Document encodings were cached: no fresh physical deployment encoding cost, dollar saving, real traffic or SLO benefit is measured here.',
        'Matched anchors/selection IDs/query populations are shared across methods. Source hashes, rankings and per-query metrics are included.',
        'Only ARC2-Global and external baseline adaptations are presented. Original research history remains intact at the provenance source.','']
    report='\n'.join(lines+mechanism_lines())
    if later:
        report=report.rstrip()+'\n\n'+later
    (ROOT/'REPORT.md').write_text(report,encoding='utf-8',newline='\n')
    tex=[r'% Generated by tools/render_results.py; measured DEV, not independent test.',
         r'\begin{table}[t]\centering\small',
         r'\caption{FiQA development nDCG@10, mean over five seeds and 500 queries. Matched anchor-budget adaptations; not original-paper reproductions.}',
         r'\label{tab:fiqa}',r'\begin{tabular}{lrrrr}\toprule',
         r'Method & MiniLM 25\% & MiniLM 50\% & E5 25\% & E5 50\% \\ \midrule']
    for method,name in zip(METHODS,['ARC2-Global','A2M / Procrustes','Embedding-Converter']):
        values=[lookup[(pair,b,method)]['ndcg10'] for pair in data['pairs'] for b in ['25pct','50pct']]
        tex.append(name+' & '+' & '.join(f'{v:.6f}' for v in values)+r' \\')
    tex += [r'\bottomrule\end{tabular}\end{table}','']
    (ROOT/'manuscript/generated/tab_fiqa.tex').write_text('\n'.join(tex),encoding='utf-8')
    recall_tex=[r'% Generated from per-query metrics; DEV evidence.',
        r'\begin{table}[t]\centering\small',
        r'\caption{FiQA development Recall@100. Same rows and budgets as Table~\ref{tab:fiqa}.}',
        r'\label{tab:recall}\begin{tabular}{lrrrr}\toprule',
        r'Method & MiniLM 25\% & MiniLM 50\% & E5 25\% & E5 50\% \\ \midrule']
    for method,name in zip(METHODS,['ARC2-Global','A2M / Procrustes','Embedding-Converter']):
        values=[lookup[(pair,b,method)]['recall100'] for pair in data['pairs'] for b in ['25pct','50pct']]
        recall_tex.append(name+' & '+' & '.join(f'{v:.6f}' for v in values)+r' \\')
    recall_tex += [r'\bottomrule\end{tabular}\end{table}','']
    (ROOT/'manuscript/generated/tab_recall.tex').write_text('\n'.join(recall_tex),encoding='utf-8')
    refs=[r'% Generated measured full-index references, not hypothetical upper bounds.',
          r'\begin{table}[t]\centering\small',
          r'\caption{Full-index references on the same FiQA development queries.}',
          r'\label{tab:references}\begin{tabular}{llrr}\toprule',
          r'Pair & Reference & nDCG@10 & Recall@100 \\ \midrule']
    for r in data['references']:
        pair='MiniLM' if r['pair'].startswith('minilm') else 'E5'
        label='Full-X' if r['method']=='full_x' else 'Full-Y'
        refs.append(f"{pair} & {label} & {r['ndcg10']:.6f} & {r['recall100']:.6f}"+r' \\')
    refs += [r'\bottomrule\end{tabular}\end{table}','']
    (ROOT/'manuscript/generated/tab_references.tex').write_text('\n'.join(refs),encoding='utf-8')
    deltas=[lookup[('e5_small_base',b,METHODS[0])]['ndcg10']-
            lookup[('e5_small_base',b,METHODS[1])]['ndcg10'] for b in ['25pct','50pct']]
    prose=(r'% Generated descriptive development interpretation.'+'\n'+
        r'\sys{} has higher mean nDCG@10 than both external adaptations in all four evaluated conditions. '+
        f'The E5 gains over plain Procrustes are {deltas[0]:.6f} and {deltas[1]:.6f} absolute at '+
        r'25\% and 50\%, respectively. '+
        r'Table~\ref{tab:recall} shows the corresponding tradeoff: E5 Recall@100 is lower than '+
        r'plain Procrustes at both budgets. Both full-index references have higher nDCG@10 '+
        r'than the partial \sys{} galleries (Table~\ref{tab:references}).'+'\n')
    (ROOT/'manuscript/generated/dev_interpretation.tex').write_text(prose,encoding='utf-8')
    print('Generated report/CSV and measured LaTeX nDCG, Recall, full references and interpretation.')

if __name__=='__main__':main()
