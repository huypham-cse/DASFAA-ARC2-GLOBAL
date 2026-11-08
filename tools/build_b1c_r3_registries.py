"""Build the prospective R3 registry; never inspect labels or execute a fit.

Allocation: {"sources": [{"path": original_absolute_path, "sha256": digest,
"restored_path": restored_absolute_or_checkout_relative_path}]}. Unspecified
paths use --restored-root plus the original absolute path. No output overwrite.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHODS = ('procrustes_global', 'arc2_global_tangent2_r1',
           'la2m20_integration_script_adaptation', 'simplelinear_official_final50_mlp5',
           'ridge_affine_l10_bias_regularized', 'embedding_converter_paper_spec')
NEW = (METHODS[2], METHODS[3], METHODS[5])
BUDGETS = ('25pct', '50pct', '75pct')
B1G_RUN = '/root/arc2_global_paper_20261025/code_515b3d1_b1g/results/b1g_full_main_r1_20261027'
RESTORED_ROOT = '/network-volume/arc2_recovery_20261030/restored'


def canonical_restored_root(value):
    """Serialize the remote Linux path without host filesystem interpretation."""
    canonical = str(value).replace('\\', '/')
    if canonical != RESTORED_ROOT:
        raise ValueError('Require the exact prospective POSIX restored root')
    return canonical


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def identity(row):
    return tuple(row[k] for k in ('dataset', 'pair', 'seed', 'budget', 'method'))


def kept(group):
    return (group['dataset'] == 'FiQA' and group['pair'] == 'minilm_distilroberta'
            and group['seed'] == 17 and group['method'] in NEW[:2])


def documentary(spec):
    return {'original_path': spec['path'], 'source_sha256': spec['sha256']}


def allocation_map(allocation):
    mapping = {}
    for row in allocation.get('sources', []):
        key = row['path']
        if key in mapping and mapping[key] != row:
            raise ValueError('Conflicting acquisition allocation: ' + key)
        if not key.startswith('/') or len(row['sha256']) != 64:
            raise ValueError('Malformed acquisition allocation')
        mapping[key] = row
    return mapping


def mapped(spec, allocation):
    row = allocation.get(spec['path'])
    if row is None:
        return copy.deepcopy(spec)
    if row['sha256'] != spec['sha256']:
        raise ValueError('Allocation cannot substitute different bytes: ' + spec['path'])
    return {'path': row['restored_path'], 'sha256': spec['sha256']}


def build(allocation, restored_root):
    """Pure metadata construction, also used by finite local validation."""
    restored_root = canonical_restored_root(restored_root)
    oldlock = read(ROOT / 'configs/b1c_lock.json')
    for field in ('registry', 'existing_cells'):
        spec = oldlock[field]
        if digest(ROOT / spec['path']) != spec['sha256']:
            raise ValueError('Original B1c registry hash drift')
    original = read(ROOT / oldlock['registry']['path'])
    prior = read(ROOT / oldlock['existing_cells']['path'])
    alloc = allocation_map(allocation)
    index_path = ROOT / 'results/b1g_r1_review_20261027/main/execution_intermediates.json'
    index = {}
    for row in read(index_path)['files']:
        key = tuple(row['cache_key'][:4])
        if len(row['cache_key']) != 6 or row['cache_key'][4:] != [row['source_full_target']['sha256'], row['source_paid']['sha256']]:
            raise ValueError('B1G cache key is not bound to ordered inputs')
        if row['dtype'] != 'float32' or row['shape'][1] != 768:
            raise ValueError('B1G target slice dimensions differ')
        if key in index and index[key] != row:
            raise ValueError('Conflicting B1G target slice identity')
        index[key] = row
    if len(index) != 120:
        raise ValueError('Need all120 original B1G paid target identities')
    # Obtain all three frozen paid-ID specs without opening target vectors.
    paid = {}
    for g in original['groups']:
        for c in g['cases'] + ([g['parity_case']] if 'parity_case' in g else []):
            key = (g['dataset'], g['seed'], c['budget'])
            if key in paid and paid[key]['sha256'] != c['paid']['sha256']:
                raise ValueError('Conflicting ordered paid-ID inputs')
            paid[key] = c['paid']
    groups = []
    for source in original['groups']:
        g = copy.deepcopy(source)
        reuse = kept(g)
        g['full_target_reference'] = documentary(source['full_target_reference'])
        if not reuse:
            g['proxy'] = {'kind': 'new_fit'}
            g.pop('parity_case', None)
            g.pop('historical_fit_receipt', None)
            if g['dataset'] == 'FiQA':
                g['historical_comparison'] = {'budget': '50pct',
                    'published_ranking': mapped(source['parity_case']['published_ranking'], alloc),
                    'semantics': 'Informational only; never a fit/ranking acceptance gate or selection rule'}
        g['cases'] = []
        budgets = ('25pct', '75pct') if reuse else BUDGETS
        allbudgets = BUDGETS if reuse else budgets
        for budget in allbudgets:
            key = (g['dataset'], g['pair'], g['seed'], budget)
            row = index[key]
            original_paid = paid[(g['dataset'], g['seed'], budget)]
            if (row['source_paid']['sha256'] != original_paid['sha256']
                    or row['source_full_target']['sha256'] != source['full_target_reference']['sha256']):
                raise ValueError('B1G target slice input provenance mismatch')
            expected = {'path': B1G_RUN + '/' + row['path'], 'sha256': row['sha256']}
            target_slice = {**documentary(expected), 'shape': row['shape'], 'dtype': row['dtype'],
                            'cache_key': row['cache_key'], 'source_paid_sha256': original_paid['sha256'],
                            'source_full_target_sha256': source['full_target_reference']['sha256']}
            if expected['path'] in alloc:
                recipe = {'kind': 'saved_slice', 'file': mapped(expected, alloc)}
            elif g['dataset'] == 'FiQA':
                base = index[(g['dataset'], g['pair'], g['seed'], '75pct')]
                base_spec = {'path': B1G_RUN + '/' + base['path'], 'sha256': base['sha256']}
                recipe = {'kind': 'b1g_75_subset', 'paid': mapped(base['source_paid'], alloc),
                          'targets': mapped(base_spec, alloc)}
            else:
                recipe = {'kind': 'full_target', 'file': mapped(source['full_target_reference'], alloc)}
            case = {'case_id': g['group_id'] + '_' + budget, 'budget': budget,
                    'paid': mapped(original_paid, alloc), 'target_slice': target_slice,
                    'target_source': recipe}
            if reuse and budget == '50pct':
                case['published_ranking'] = mapped(source['parity_case']['published_ranking'], alloc)
                g['parity_case'] = case
            else:
                g['cases'].append(case)
        for name in ('old_docs', 'new_queries', 'ids', 'anchors', 'historical_fit_receipt'):
            if name in g:
                g[name] = mapped(g[name], alloc)
        if reuse:
            g['proxy']['file'] = mapped(g['proxy']['file'], alloc)
        groups.append(g)
    existing, displaced = [], []
    for row in prior['cells']:
        lost = row['dataset'] == 'FiQA' and row['method'] in NEW and not kept(row)
        if lost:
            displaced.append(copy.deepcopy(row))
        else:
            item = copy.deepcopy(row)
            item['ranking'] = mapped(item['ranking'], alloc)
            existing.append(item)
    new = [{**{k: g[k] for k in ('dataset', 'pair', 'seed', 'method')}, 'budget': c['budget']}
           for g in groups for c in g['cases']]
    expected = set(itertools.product(('FiQA', 'NanoNQ', 'NanoHotpotQA', 'NanoFEVER'),
                                    ('minilm_distilroberta', 'e5_small_base'), (17, 29, 41, 53, 67), BUDGETS, METHODS))
    expected.update((d, p, None, 'full', m) for d in ('FiQA', 'NanoNQ', 'NanoHotpotQA', 'NanoFEVER')
                    for p in ('minilm_distilroberta', 'e5_small_base') for m in ('full_x', 'full_y'))
    if (len(groups), len(new), len(existing), len(displaced)) != (120, 358, 378, 38):
        raise ValueError('R3 finite matrix count differs')
    if set(map(identity, existing)) & set(map(identity, new)) or set(map(identity, existing)) | set(map(identity, new)) != expected:
        raise ValueError('R3 does not partition the unchanged736-cell matrix')
    contexts = [{'path': p, 'sha256': digest(ROOT / p)} for p in
                ('configs/b1c_sources.json', 'configs/b1c_existing.json',
                 'results/b1g_r1_review_20261027/main/execution_intermediates.json')]
    return ({'stage': 'B1C_R3', 'expected_groups': 120, 'expected_cases': 358, 'groups': groups,
             'contexts': contexts, 'restored_root': restored_root, 'expected_new_nano_fits': 90,
             'expected_new_fiqa_fits': 28, 'expected_reused_fiqa_fits': 2,
             'scope': 'Prospective recovery of same736-cell inspected DEV matrix; original B1c interrupted'},
            {'stage': 'B1C_R3', 'cells': existing,
             'displaced_historical_cells': [{**{k: v for k, v in r.items() if k != 'ranking'},
                                             'ranking': documentary(r['ranking'])} for r in displaced],
             'scope': '378 preserved cells;38 displaced historical cells remain provenance, not active R3 results'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allocation', type=Path, required=True)
    parser.add_argument('--restored-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'configs')
    args = parser.parse_args()
    sources, existing = build(read(args.allocation), args.restored_root)
    for name in ('b1c_r3_sources.json', 'b1c_r3_existing.json'):
        if (args.output_dir / name).exists():
            raise FileExistsError('Immutable registry already exists: ' + str(args.output_dir / name))
    for name, value in [('b1c_r3_sources.json', sources), ('b1c_r3_existing.json', existing)]:
        with (args.output_dir / name).open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(value, stream, indent=2, allow_nan=False)
            stream.write('\n')
    print(json.dumps({'groups': 120, 'new': 358, 'existing': 378, 'displaced': 38}))


if __name__ == '__main__':
    main()
