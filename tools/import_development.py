"""Copy selected existing results, without opening labels or rescoring rankings."""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ANALYSIS_SHA = 'a7b42a4b6a07bfe1389b785d57d7e5ef568653d501cc96b5d584592e9782fc2f'
METHODS = {
    'procrustes_tangent2_global': 'ARC2-Global',
    'procrustes_global': 'A2M / Procrustes adaptation',
    'embedding_converter_paper_spec_anchor1024': 'Embedding-Converter adaptation',
    'full_x': 'Full-X', 'full_y': 'Full-Y',
}

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    args=ap.parse_args(); source=args.source.resolve(strict=True)
    if digest(source/'analysis.json') != SOURCE_ANALYSIS_SHA:
        raise ValueError('Source analysis hash mismatch')
    out=ROOT/'results/fiqa_development'; out.mkdir(parents=True, exist_ok=False)
    provenance=ROOT/'provenance/source_run'; provenance.mkdir(parents=True, exist_ok=False)
    copied=[]
    def copy_file(src, dst):
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src,dst)
        if digest(src)!=digest(dst): raise AssertionError(f'Copy mismatch: {dst}')
        copied.append({'source_path':str(src),'package_path':dst.relative_to(ROOT).as_posix(),
                       'sha256':digest(dst),'bytes':dst.stat().st_size})
    a=json.loads((source/'analysis.json').read_text(encoding='utf-8'))
    m=json.loads((source/'metadata.json').read_text(encoding='utf-8'))
    index=json.loads((source/'metric_index.json').read_text(encoding='utf-8'))
    cells=index['cells']; indices=[i for i,c in enumerate(cells) if c['method'] in METHODS]
    assert len(indices)==64
    selected=[cells[i] for i in indices]
    for c in selected:
        src=source/c['ranking_path']
        if digest(src)!=c['ranking_sha256']: raise AssertionError('Original ranking changed')
        copy_file(src,out/c['ranking_path'])
    metrics=np.load(source/'per_query.npy', allow_pickle=False)
    assert metrics.shape==(144,500,2)
    np.save(out/'per_query.npy', metrics[indices], allow_pickle=False)
    dump(out/'metric_index.json', {'cells':selected,'source_cell_indices':indices,
         'columns':index['columns'],'query_ids':index['query_ids'],
         'graded_relevance':index['graded_relevance'],
         'scope':'selected existing per-query values; no qrels opened'})
    for rel in ['ids.json','backfill_order.npy']:
        copy_file(source/rel,out/rel)
    for src in sorted((source/'selections').glob('*.npy')):
        copy_file(src,out/'selections'/src.name)
    # Original metadata/seal contain full source-run context; they are provenance,
    # not additional active result rows. Never rewrite their bytes.
    for rel in ['metadata.json','metadata_pre_qrels.json','ranking_seal.json','input_manifest.json']:
        copy_file(source/rel,provenance/rel)
    summary=[r for r in a['summary'] if r['method'] in METHODS]
    assert len(summary)==12
    dump(out/'summary.json', {'scope':'FiQA inspected development; post-score selection',
         'dataset':'FiQA', 'documents':57638,'queries':500,'seeds':[17,29,41,53,67],
         'pairs':m['pairs'],'anchors':1024,'logical_budgets':{'25pct':14409,'50pct':28819},
         'new_physical_document_encodes':0,'source_analysis_sha256':SOURCE_ANALYSIS_SHA,
         'display_names':METHODS,'summary':summary,
         'references':a['full_x_full_y_references'],
         'global_specific_confidence_intervals_available':False,
         'embedding_converter_scope':'independent paper-spec 1024-anchor adaptation; not official-code reproduction',
         'excluded_method_rows_retained_at_original_source':True})
    dump(ROOT/'provenance/result_import.json', {
        'source_directory':str(source),'source_analysis_sha256':SOURCE_ANALYSIS_SHA,
        'source_per_query_sha256':digest(source/'per_query.npy'),
        'selected_source_method_ids':list(METHODS),'ranking_count':64,
        'source_cell_indices':indices,'copied_files':copied,
        'derived_files':['results/fiqa_development/per_query.npy',
                         'results/fiqa_development/metric_index.json',
                         'results/fiqa_development/summary.json'],
        'new_qrel_reads':0,'new_rankings':0,'new_scientific_runs':0,
        'source_run_context':'source metadata/seal retained verbatim; other method results remain in original repo',
        'selection_after_development_scores':True})
    print('Imported 64 existing rankings and 64x500x2 metrics; no qrels/scientific run.')

if __name__=='__main__': main()
