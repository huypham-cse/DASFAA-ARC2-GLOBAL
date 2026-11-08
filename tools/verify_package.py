"""Verify selected copied evidence and internal metrics without loading qrels."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError('Preserve existing verification receipt')
    report={'scope':'copy/hash/arithmetic verification; not independent claim audit','new_qrel_reads':0}
    imported=json.loads((ROOT/'provenance/result_import.json').read_text())
    for c in imported['copied_files']:
        path=ROOT/c['package_path']
        assert sha(path)==c['sha256'],str(path)
        assert path.stat().st_size==c['bytes']
    extraction=json.loads((ROOT/'provenance/implementation_extraction.json').read_text())
    for rel,digest in extraction['canonical_lf_hashes'].items():
        assert hashlib.sha256((ROOT/rel).read_text(encoding='utf-8').encode()).hexdigest()==digest,rel
    p=ROOT/'results/fiqa_development'
    idx=json.loads((p/'metric_index.json').read_text());cells=idx['cells']
    metrics=np.load(p/'per_query.npy',allow_pickle=False)
    assert metrics.shape==(64,500,2) and np.isfinite(metrics).all()
    ids=json.loads((p/'ids.json').read_text()); assert len(ids['doc_ids'])==57638
    assert len(ids['query_ids'])==500
    seal=json.loads((ROOT/'provenance/source_run/ranking_seal.json').read_text())
    sealed={c['ranking_path']:c for c in seal['cells']}
    for c in cells:
        assert c==sealed[c['ranking_path']]
        ranking=np.load(p/c['ranking_path'],allow_pickle=False)
        assert ranking.shape==(500,100)
        assert ranking.min()>=0 and ranking.max()<57638
        assert all(len(set(row))==100 for row in ranking)
    metadata=json.loads((ROOT/'provenance/source_run/metadata.json').read_text())
    assert metadata['ranking_seal_unix']<metadata['first_dev_qrel_open_unix']
    assert sha(ROOT/'provenance/source_run/ranking_seal.json')==metadata['ranking_seal_sha256']
    summary=json.loads((p/'summary.json').read_text())
    for row in summary['summary']:
        positions=[i for i,c in enumerate(cells) if all(c[k]==row[k] for k in ['method','pair','budget'])]
        assert len(positions)==5
        mean=metrics[positions].mean(axis=(0,1))
        assert np.allclose(mean,[row['ndcg10'],row['recall100']],atol=1e-12,rtol=0)
    for c in cells:
        if c['seed'] is None:continue
        assert c['anchor_count']==1024
        anchors=np.load(p/'selections'/f"anchors_seed_{c['seed']}.npy",allow_pickle=False)
        selected=np.load(p/'selections'/f"seed{c['seed']}_{c['budget']}.npy",allow_pickle=False)
        assert len(anchors)==1024 and set(anchors)<=set(selected)
        assert len(selected)==summary['logical_budgets'][c['budget']]==c['unique_destination_encodings']
    original=Path(imported['source_directory'])
    if (original/'per_query.npy').exists():
        assert sha(original/'per_query.npy')==imported['source_per_query_sha256']
        np.testing.assert_array_equal(metrics,np.load(original/'per_query.npy',allow_pickle=False)[imported['source_cell_indices']])
        assert sha(original/'analysis.json')==imported['source_analysis_sha256']
        report['original_per_query_subset_exact']=True
    report.update(status='PASS',copied_files=len(imported['copied_files']),rankings=64,
                  metric_shape=list(metrics.shape),summary_rows=12,
                  original_prelabel_seal_verified=True,anchor_budget_checks_passed=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
