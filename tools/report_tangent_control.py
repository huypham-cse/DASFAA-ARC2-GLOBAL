"""Verify TC1 saved results independently, then build its finite table/figure."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')


def independent_metrics(ranking,ids,qrels):
    output=[]
    for q,hits in zip(ids['query_ids'],ranking):
        rels={d:v for d,v in qrels.get(q,{}).items() if v>0}
        if not rels:output.append([0.,0.]);continue
        returned=[ids['doc_ids'][int(i)] for i in hits]
        actual=sum((2.**rels.get(d,0)-1)/np.log2(i+2) for i,d in enumerate(returned[:10]))
        ideal=sum((2.**r-1)/np.log2(i+2) for i,r in enumerate(sorted(rels.values(),reverse=True)[:10]))
        output.append([actual/ideal,sum(d in rels for d in returned)/len(rels)])
    return np.array(output,dtype=np.float64)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run',type=Path,required=True);ap.add_argument('--qrels',type=Path,required=True)
    ap.add_argument('--lock',type=Path,default=ROOT/'configs/tangent_control_20261102_lock.json')
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=False)
    run=args.run;score=run/'full/scoring';full=run/'full'
    lock=json.loads(args.lock.read_text());expected_rankings=20*len(lock['pairs'])
    local=lock['id'].startswith('tc1l_')
    summary=json.loads((score/'summary.json').read_text())
    seal=json.loads((full/'ranking_seal.json').read_text())
    for relative,h in seal['artifacts'].items():assert sha(full/relative)==h,relative
    assert sha(args.qrels)==lock['qrels']['sha256']
    ids=json.loads((full/'ids.json').read_text());assert sha(full/'ids.json')==lock['ids']['sha256']
    labels={}
    with args.qrels.open(encoding='utf-8') as stream:
        for row in csv.DictReader(stream,delimiter='\t'):
            labels.setdefault(row['query-id'],{})[row['corpus-id']]=float(row['score'])
    cells=json.loads((score/'cell_index.json').read_text());values=np.load(score/'per_query.npy',allow_pickle=False)
    assert values.shape==(expected_rankings,500,2)
    max_metric=0.
    for i,c in enumerate(cells):
        assert sha(full/c['ranking_path'])==c['sha256']
        actual=independent_metrics(np.load(full/c['ranking_path'],allow_pickle=False),ids,labels)
        error=float(np.max(np.abs(actual-values[i])));max_metric=max(max_metric,error)
        assert error<1e-12
    diffs=[]
    max_mean=0.
    for pair in lock['pairs']:
        methods={}
        for method in lock['methods']:
            rows=np.stack([values[i] for i,c in enumerate(cells) if c['pair']==pair and c['method']==method])
            methods[method]=rows.mean(axis=0)
            row=next(r for r in summary['means'] if r['pair']==pair and r['method']==method)
            for j,k in enumerate(['ndcg10','recall100']):
                e=abs(float(rows[:,:,j].mean())-row[k]);max_mean=max(max_mean,e);assert e<1e-14
        for control in ['chordal2','euclidean2']:
            diffs.append(methods['tangent2'][:,0]-methods[control][:,0])
    differences=np.stack(diffs,axis=1);rng=np.random.default_rng(20261102)
    recreated=np.concatenate([differences[rng.integers(0,500,size=(200,500))].mean(axis=1) for _ in range(100)])
    stored=np.load(score/'bootstrap_draws.npy',allow_pickle=False)
    boot_error=float(np.max(np.abs(stored-recreated)));assert boot_error<1e-14
    for j,c in enumerate(summary['primary_contrasts']):
        low,high=np.quantile(recreated[:,j],[.00625,.99375])
        np.testing.assert_allclose([c['delta_ndcg10'],c['lower'],c['upper']],[differences[:,j].mean(),low,high],rtol=0,atol=1e-14)
    paper_hash=sha(ROOT/'paper/ARC2_Global_DASFAA2027_final.pdf')
    assert paper_hash=='e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc'
    qa={'status':'PASS','rankings_verified':expected_rankings,'per_query_values_verified':int(values.size),
        'independent_metric_maxabs':max_metric,'mean_maxabs':max_mean,'bootstrap_maxabs':boot_error,
        'paper_unchanged':True,'paper_sha256':paper_hash,'lock_sha256':sha(args.lock),
        'seal_sha256':sha(full/'ranking_seal.json'),'qrels_sha256':sha(args.qrels)}
    write(out/'LOCAL_QA.json',qa)
    counts={v:sum(c['verdict']==v for c in summary['primary_contrasts']) for v in ['positive','negative','unresolved']}
    text=['# FiQA matched-residual ablation — '+('TC1L MiniLM local' if local else 'TC1'),'',
          f"**Complete and locally verified.** Primary contrasts: {counts['positive']} positive, {counts['negative']} negative, {counts['unresolved']} unresolved.",'',
          'FiQA development; 57,638 documents, 500 queries, 1,024 fitted anchors, 50% paid exposure (28,819 unique documents including anchors), five seeds, exact search. No new encodings or neural training.','',
          '| Method | MiniLM nDCG@10 | E5 nDCG@10 | MiniLM Recall@100 | E5 Recall@100 |',
          '|---|---:|---:|---:|---:|']
    labels_method={'procrustes':'Procrustes initialization','tangent2':'ARC2 Tangent2','chordal2':'Chordal2 (norm-matched)','euclidean2':'EuclideanResidual2'}
    if local:
        text[-2:]=['| Method | MiniLM nDCG@10 | MiniLM Recall@100 |','|---|---:|---:|']
    for method in ['procrustes','euclidean2','chordal2','tangent2']:
        rows={r['pair']:r for r in summary['means'] if r['method']==method}
        a=rows[lock['pairs'][0]]
        if local:
            text.append(f"| {labels_method[method]} | {a['ndcg10']:.6f} | {a['recall100']:.6f} |")
        else:
            b=rows[lock['pairs'][1]]
            text.append(f"| {labels_method[method]} | {a['ndcg10']:.6f} | {b['ndcg10']:.6f} | {a['recall100']:.6f} | {b['recall100']:.6f} |")
    text+=['','## Locked primary comparisons','',
           '| Encoder transition | ARC2 minus control | Delta nDCG@10 | Corrected interval | Verdict |',
           '|---|---|---:|---|---|']
    for c in summary['primary_contrasts']:
        text.append(f"| {c['pair']} | {labels_method[c['right']]} | {c['delta_ndcg10']:+.6f} | [{c['lower']:+.6f}, {c['upper']:+.6f}] | {c['verdict']} |")
    text+=['','Four prespecified two-sided contrasts'+('; only two MiniLM contrasts observed here, both E5 contrasts pending' if local else '')+'. Five-seed averaging precedes paired query bootstrap (20,000 draws); individual98.75% percentile intervals, approximate95% original-family coverage. Recall/B0 are descriptive.','',
           'Tangent versus chordal isolates radial target inclusion conditional on this computation. Tangent versus Euclidean also changes prediction-norm weighting. These are already-inspected DEV results, not independent confirmation or universal-best evidence.','',
           '## Resources and verification','']
    for stage in ['synthetic','smoke','full']:
        m=json.loads((run/stage/'metadata.json').read_text())
        text.append(f"- {stage}: {m['status']}; {m['elapsed_seconds']:.1f} seconds; peak RSS {m['peak_rss_bytes']/2**20:.1f} MiB.")
    text+=['','Shared Procrustes/factor timings and per-arm phase times are diagnostic, not standalone deployment-cost measurements.','',
           f"Local QA PASS: all{expected_rankings} rankings and{values.size:,} per-query metric values checked against labels; maximum metric difference {max_metric:.3g}; bootstrap difference {boot_error:.3g}.",'',
           ('Protocol: `protocols/TC1L_MINILM_LOCAL_20261102.md`; distinct Windows measurement; E5 pending.' if local else 'Protocol: `protocols/FIQA_MATCHED_RESIDUAL_CONTROLS_20261102.md`; pre-run commit `07d0456`.')+' Historical runs and manuscript remain unchanged.','',
           '**STOP:** interpret this finite ablation before any manuscript edit, method change, regrade or new study.','']
    (out/'SUMMARY.md').write_text('\n'.join(text),encoding='utf-8')
    sys.path.insert(0,str(ROOT/'paper/scripts'))
    from plot_publication import _PublicationFigure, _STYLE
    import matplotlib as mpl
    mpl.use('Agg')
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    with mpl.rc_context(_STYLE):
        fig=_PublicationFigure(figsize=(4.1 if local else 6.8,2.7),layout='constrained');FigureCanvasAgg(fig)
        axes=fig.subplots(1,len(lock['pairs']),sharey=True,squeeze=False).ravel()
        for ax,pair,title in zip(axes,lock['pairs'],['MiniLM $\\rightarrow$ DistilRoBERTa','E5-small $\\rightarrow$ E5-base']):
            rows=[c for c in summary['primary_contrasts'] if c['pair']==pair]
            ax.axvline(0,color='#777777',linewidth=.8,linestyle=(0,(3,3)),zorder=0)
            for y,c in zip([1,0],rows):
                x=c['delta_ndcg10'];lo=c['lower'];hi=c['upper']
                ax.errorbar(x,y,xerr=[[max(0,x-lo)],[max(0,hi-x)]],fmt='o',color='#0F4D92',capsize=3,markersize=5,elinewidth=1.4)
                ax.annotate(f'{x:+.4f}',(x,y),xytext=(0,10),textcoords='offset points',ha='center',fontsize=8)
            ax.set_yticks([0,1],['vs. Euclidean2','vs. Chordal2']);ax.set_ylim(-.5,1.6)
            ax.set_title(title);ax.set_xlabel(r'$\Delta$ nDCG@10 (ARC2 $-$ control)')
            ax.ticklabel_format(axis='x',style='plain',useOffset=False)
            ax.margins(x=.15)
        fig.suptitle('Matched initialization, anchors, regularization and two updates',fontsize=9)
        for suffix in ['pdf','svg','png']:
            fig.savefig(out/('fig_tangent_controls.'+suffix),dpi=300,bbox_inches='tight',pad_inches=.05)
    print(json.dumps({'qa':qa,'primary_counts':counts,'output':str(out)},indent=2))


if __name__=='__main__':main()
