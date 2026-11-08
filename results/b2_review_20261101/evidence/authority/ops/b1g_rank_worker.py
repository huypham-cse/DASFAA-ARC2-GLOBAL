"""Qrel-free B1-G rankings reconstructed solely from frozen proxies/parameters."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from arc2_global.diagnostics import (whitelist, safe_id, verified_path, load_array,
    positions, write_json, save_array, run_worker, ranking_diagnostics, sha256)
from arc2_global.numerics import _vectors, normalize_rows, apply_affine
from arc2_global.procrustes import procrustes_apply
from arc2_global.retrieval import exact_topk

PROC = 'procrustes_global'
PRIMARY = 'arc2_global_tangent2_r1'
RIDGE = 'ridge_affine_l10_bias_regularized'
LA2M = 'la2m20_integration_script_adaptation'


def reconstruct_proxy(old, spec, method, hashes):
    whitelist(spec, ('kind', 'file'))
    if spec['kind'] == 'saved_npy':
        proxy = _vectors('saved pristine proxy', load_array(spec['file'], hashes))
        if len(proxy) != len(old):
            raise ValueError('Saved proxy/document row mismatch')
        return proxy
    if spec['kind'] not in ('b1m_parameters', 'b1p_parameters'):
        raise ValueError('Unknown proxy kind')
    with np.load(verified_path(spec['file'], hashes), allow_pickle=False) as archive:
        params = {key: archive[key] for key in archive.files}
    b1m = spec['kind'] == 'b1m_parameters'
    if method == PROC:
        keys = ('procrustes_source_mean', 'procrustes_target_mean', 'procrustes_matrix') if b1m else ('source_mean', 'target_mean', 'matrix')
        fn = lambda block: normalize_rows(procrustes_apply(block, *(params[k] for k in keys)))
    elif method == PRIMARY:
        coefficient = params['frozen_two' if b1m else 'two']
        fn = lambda block: apply_affine(block, coefficient)
    elif method == RIDGE:
        coefficient = params[RIDGE if b1m else 'coefficient']
        fn = lambda block: apply_affine(block, coefficient)
    elif method == LA2M and not b1m:
        from sklearn.cluster import KMeans
        km = KMeans(n_clusters=len(params['centroids']), n_init=4)
        km.cluster_centers_ = params['centroids']
        km.n_features_in_ = old.shape[1]
        km._n_threads = 4
        global_map = tuple(params['global_' + key] for key in ('source_mean', 'target_mean', 'matrix'))
        def fn(block):
            assigned = km.predict(block)
            raw = np.empty((len(block), global_map[1].shape[1]), dtype=np.float32)
            for cluster in np.unique(assigned):
                rows = np.flatnonzero(assigned == cluster)
                keys = [f'cluster{cluster}_{key}' for key in ('source_mean', 'target_mean', 'matrix')]
                available = [key in params for key in keys]
                if any(available) and not all(available):
                    raise ValueError('Incomplete saved local Procrustes map')
                values = tuple(params[key] for key in keys) if all(available) else global_map
                raw[rows] = procrustes_apply(block[rows], *values)
            return normalize_rows(raw)
    else:
        raise ValueError('Unsupported frozen method/parameter combination')
    return _vectors('reconstructed proxy', np.concatenate([fn(old[s:s + 512]) for s in range(0, len(old), 512)]))


def execute(request, out, metadata):
    whitelist(request, ('output', 'group_id', 'method', 'dataset', 'pair', 'seed', 'regime',
                       'old_docs', 'new_queries', 'ids', 'sample_positions', 'anchors', 'proxy', 'cases'))
    safe_id(request['group_id'])
    hashes = metadata['input_hashes']
    old = _vectors('old documents', load_array(request['old_docs'], hashes))
    queries = _vectors('new queries', load_array(request['new_queries'], hashes))
    ids = json.loads(verified_path(request['ids'], hashes).read_text(encoding='utf-8-sig'))
    if not isinstance(ids, dict) or not {'doc_ids', 'query_ids'} <= set(ids):
        raise ValueError('IDs must contain doc_ids and query_ids')
    # Documentary ID metadata (e.g. row_order) is covered by the file hash.
    if len(ids['doc_ids']) != len(old) or len(ids['query_ids']) != len(queries):
        raise ValueError('ID/vector row mismatch')
    anchors = positions(load_array(request['anchors'], hashes), 'anchors', len(old), nonempty=True)
    sample = positions(load_array(request['sample_positions'], hashes), 'sample', len(old), nonempty=True)
    proxy = reconstruct_proxy(old, request['proxy'], request['method'], hashes)
    if proxy.shape[1] != queries.shape[1]:
        raise ValueError('Proxy/query dimension mismatch')
    if not isinstance(request['cases'], list) or not request['cases']:
        raise ValueError('Cases must be nonempty')
    for case in request['cases']:
        whitelist(case, ('case_id', 'budget', 'paid', 'paid_targets', 'published_ranking'))
    case_ids = [safe_id(c['case_id']) for c in request['cases']]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError('Duplicate case identifiers')
    def rank(gallery):
        return exact_topk(queries, gallery, k=100, batch_rows=16,
                         query_ids=ids['query_ids'], document_ids=ids['doc_ids'], exclude_identical_ids=True)
    before = rank(proxy)
    save_array(out / 'before.npy', before)
    save_array(out / 'sample_proxy.npy', proxy[sample])
    metadata.update(dataset=request['dataset'], pair=request['pair'], seed=request['seed'], regime=request['regime'],
                    method=request['method'], documents=len(old), queries=len(queries), sample_documents=len(sample),
                    proxy_semantics='pristine prediction for every document, including anchors',
                    score_arithmetic='float32 query batch16 @ gallery.T; stable row-order ties; identical ID exclusion',
                    cases=[])
    (out / 'cases').mkdir()
    for case in request['cases']:
        whitelist(case, ('case_id', 'budget', 'paid', 'paid_targets', 'published_ranking'))
        folder = out / 'cases' / case['case_id']
        folder.mkdir()
        paid = positions(load_array(case['paid'], hashes), 'paid', len(old))
        if not np.isin(anchors, paid).all():
            raise ValueError('Paid positions omit anchors')
        target = _vectors('paid target slices', load_array(case['paid_targets'], hashes), dim=proxy.shape[1])
        if len(target) != len(paid):
            raise ValueError('Paid target/position mismatch')
        gallery = proxy.copy()
        gallery[paid] = target
        after = rank(gallery)
        save_array(folder / 'after.npy', after)
        expected = load_array(case['published_ranking'], hashes)
        if not np.array_equal(after, expected):
            save_array(folder / 'expected.npy', expected)
            same_shape = after.shape == expected.shape
            changed = np.flatnonzero(np.any(after != expected, axis=1)).tolist() if same_shape else None
            write_json(folder / 'parity_failure.json', {'computed_shape': list(after.shape),
                'expected_shape': list(expected.shape), 'changed_query_rows': changed,
                'changed_query_count': len(changed) if changed is not None else None,
                'changed_rank_positions': int(np.count_nonzero(after != expected)) if same_shape else None,
                'query_ids': [ids['query_ids'][i] for i in changed] if changed is not None else None})
            raise AssertionError('Published mixed ranking parity failed: ' + case['case_id'])
        diagnostics = ranking_diagnostics(before, after, n_docs=len(old), anchors=anchors, paid=paid)
        diagnostics.update(case_id=case['case_id'], budget=case['budget'], published_ranking_parity=True)
        write_json(folder / 'ranking_diagnostics.json', diagnostics)
        metadata['cases'].append({'case_id': case['case_id'], 'status': 'PASS', 'after_sha256': sha256(folder / 'after.npy')})
    metadata['artifacts'] = {name: {'sha256': sha256(out / name)} for name in ('before.npy', 'sample_proxy.npy')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True)
    args = parser.parse_args()
    run_worker(args.request, 'B1G_RANK_PASS', execute)
