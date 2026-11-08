"""Isolated paired score diagnostics on sampled true vectors only."""
import argparse
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from arc2_global.diagnostics import (whitelist, safe_id, load_array, positions,
    write_json, save_array, run_worker, paired_diagnostics, sha256)
from arc2_global.numerics import _vectors


def execute(request, out, metadata):
    whitelist(request, ('output', 'group_id', 'proxy_sample', 'target_sample', 'new_queries',
                       'sample_positions', 'anchors', 'cases'), ('dataset', 'pair', 'seed', 'regime'))
    safe_id(request['group_id'])
    hashes = metadata['input_hashes']
    proxy = _vectors('sample proxy', load_array(request['proxy_sample'], hashes))
    target = _vectors('sample target', load_array(request['target_sample'], hashes), dim=proxy.shape[1])
    queries = _vectors('new queries', load_array(request['new_queries'], hashes), dim=proxy.shape[1])
    sample = positions(load_array(request['sample_positions'], hashes), 'sample', nonempty=True)
    anchors = positions(load_array(request['anchors'], hashes), 'anchors', nonempty=True)
    if len(proxy) != len(target) or len(proxy) != len(sample):
        raise ValueError('Paired sample rows do not align')
    if not isinstance(request['cases'], list) or not request['cases']:
        raise ValueError('Cases must be nonempty')
    for case in request['cases']:
        whitelist(case, ('case_id', 'paid'))
    case_ids = [safe_id(c['case_id']) for c in request['cases']]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError('Duplicate case identifiers')
    proxy_scores = queries @ proxy.T
    true_scores = queries @ target.T
    save_array(out / 'proxy_scores.npy', proxy_scores)
    save_array(out / 'true_scores.npy', true_scores)
    metadata.update({key: request[key] for key in ('dataset', 'pair', 'seed', 'regime') if key in request})
    metadata.update(sample_documents=len(sample), queries=len(queries),
                    score_arithmetic='float32 queries @ same-document sample.T',
                    target_access='only hash-verified sample target vectors; no full target corpus', cases=[])
    (out / 'cases').mkdir()
    for case in request['cases']:
        whitelist(case, ('case_id', 'paid'))
        paid = positions(load_array(case['paid'], hashes), 'paid')
        if not np.isin(anchors, paid).all():
            raise ValueError('Paid positions omit anchors')
        folder = out / 'cases' / case['case_id']
        folder.mkdir()
        diagnostics = paired_diagnostics(proxy_scores, true_scores, proxy, target, sample, anchors, paid)
        diagnostics['case_id'] = case['case_id']
        write_json(folder / 'paired_diagnostics.json', diagnostics)
        metadata['cases'].append({'case_id': case['case_id'], 'status': 'PASS'})
    metadata['artifacts'] = {name: {'sha256': sha256(out / name)} for name in ('proxy_scores.npy', 'true_scores.npy')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True)
    args = parser.parse_args()
    run_worker(args.request, 'B1G_ANALYZER_PASS', execute)
