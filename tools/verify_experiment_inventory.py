"""Reconcile every planned logical condition and historical ranking byte version."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product
import argparse
import hashlib
import json
import sys
sys.dont_write_bytecode = True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--output', type=Path)
    args = ap.parse_args(); root = args.root.resolve()
    read = lambda rel: json.loads((root / rel).read_text(encoding='utf-8'))
    studies = {'I': read('results/fiqa_development/metric_index.json')['cells'],
               'M': sum([read(f'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/{d}/cell_index.json')['cells']
                         for d in ('NanoNQ', 'NanoHotpotQA', 'NanoFEVER', 'FiQA')], []),
               'P': read('results/b1p_r5_review_20261027/scoring/cell_index.json')['cells'],
               'C': read('results/b1c_r3_review_20261031/evidence/run/scoring/cell_index.json')['cells'],
               'B': read('results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/cell_index.json')['cells']}
    aliases = {'procrustes_tangent2_global': 'arc2_global_tangent2_r1',
               'embedding_converter_paper_spec_anchor1024': 'embedding_converter_paper_spec'}
    def key(c):
        method = aliases.get(c['method'], c['method'])
        reference = method in ('full_x', 'full_y')
        return (c.get('dataset', 'FiQA'), c['pair'], method, None if reference else c['seed'],
                'full' if reference else c['budget'], 'reference' if reference else c.get('regime', 'fixed1024'))
    keys = {name: {key(c) for c in cells} for name, cells in studies.items()}
    assert {n: len(k) for n, k in keys.items()} == {'I': 64, 'M': 736, 'P': 124, 'C': 736, 'B': 184}
    ds = ('NanoNQ', 'NanoHotpotQA', 'NanoFEVER', 'FiQA'); pairs = ('minilm_distilroberta', 'e5_small_base')
    seeds = (17, 29, 41, 53, 67); budgets = ('25pct', '50pct', '75pct')
    methods = ('arc2_global_tangent2_r1', 'procrustes_global', 'la2m20_integration_script_adaptation',
               'simplelinear_official_final50_mlp5', 'ridge_affine_l10_bias_regularized', 'embedding_converter_paper_spec')
    expected = {(d, p, m, s, b, 'fixed1024') for d, p, m, s, b in product(ds + ('TREC-COVID',), pairs, methods, seeds, budgets)}
    expected |= {(d, p, m, s, b, 'fixed1024') for d, p, m, s, b in product(ds, pairs, ('tangent1_l10', 'tangent2_l1', 'tangent2_l100'), seeds, budgets)}
    expected |= {('FiQA', p, m, s, '50pct', 'allpaid28819') for p, m, s in product(pairs, methods, seeds)}
    expected |= {(d, p, m, None, 'full', 'reference') for d, p, m in product(ds + ('TREC-COVID',), pairs, ('full_x', 'full_y'))}
    union = set().union(*keys.values()); assert union == expected and len(union) == 1340
    assert len(keys['M'] - keys['C']) == 360 and len(keys['P'] - (keys['C'] | keys['M'])) == 60
    rank_hashes = set()
    for path in (root / 'results').rglob('*.npy'):
        if 'rank' in path.as_posix().lower():
            rank_hashes.add(hashlib.sha256(path.read_bytes()).hexdigest())
    def digest(c):
        return c.get('ranking_sha256') or c['ranking'].get('sha256', c['ranking'].get('source_sha256'))
    coverage = {}
    for name, cells in studies.items():
        missing = [key(c) for c in cells if digest(c) not in rank_hashes]
        assert not missing, (name, missing)
        coverage[name] = {'index_rows': len(cells), 'unique_logical_keys': len(keys[name]), 'all_ranking_hashes_present': True}
    displaced = read('configs/b1c_r3_existing.json')['displaced_historical_cells']
    assert len(displaced) == 38 and all(digest(c) in rank_hashes for c in displaced)
    for name in ('b1a_r1_20261025', 'b1b_20261026'):
        assert (root / 'results' / name / 'metadata.json').is_file()
    g = read('results/b1g_r1_review_20261027/portable_rankings/ranking_index.json')
    assert g['pure_galleries'] == 210 and g['mixed_cases'] == 450
    result = {'status': 'PASS', 'checked_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Logical matrix and saved raw-ranking coverage; no new fit, retrieval or qrel access',
              'unique_quality_cells': len(union), 'DEV': 1156, 'independent': 184,
              'main_DEV': 736, 'additional_ablation': 360, 'additional_allpaid': 60,
              'source_index_rows': sum(len(x) for x in studies.values()),
              'repeated_logical_source_rows': sum(len(x) for x in studies.values()) - len(union),
              'missing_keys': 0, 'unexpected_keys': 0, 'ranking_hash_coverage': coverage,
              'displaced_historical_versions_retained': len(displaced),
              'G_diagnostic_cases_separate': 450, 'G_pure_rankings_separate': 210,
              'B3_B4': 'not run / conditional',
              'limitations': ['Logical conditions are not independent statistical observations or physical fit invocations.',
                             'Imported history is exactly64rows; historical byte variants do not increase logical cell counts.',
                             'Large model/vector payloads and sampled score-error replay are outside this compact inventory.']}
    out = args.output or Path('checks') / ('experiment_inventory_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    out = out.resolve() if out.is_absolute() else (root / out).resolve()
    if not out.is_relative_to(root / 'checks') or out.exists():
        raise ValueError('Choose a new JSON receipt under checks/')
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({'status': 'PASS', 'unique_quality_cells': 1340, 'output': str(out)}))


if __name__ == '__main__':
    main()
