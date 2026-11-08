"""Build B1c's finite completion registry from existing sealed metadata only."""
import copy
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE = '/root/arc2_global_paper_20261025'
MROOT = REMOTE + '/code_4056612/results/b1m_full_r1_20261026'
METHODS = ['procrustes_global', 'arc2_global_tangent2_r1',
           'la2m20_integration_script_adaptation', 'simplelinear_official_final50_mlp5',
           'ridge_affine_l10_bias_regularized', 'embedding_converter_paper_spec']
NEW = [METHODS[2], METHODS[3], METHODS[5]]
DATASETS = ['NanoNQ', 'NanoHotpotQA', 'NanoFEVER', 'FiQA']
PAIRS = ['minilm_distilroberta', 'e5_small_base']
SEEDS = [17, 29, 41, 53, 67]
BUDGETS = ['25pct', '50pct', '75pct']


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def spec(path):
    return {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}


def dump(path, value):
    with (ROOT / path).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def identity(row):
    return tuple(row[k] for k in ['dataset', 'pair', 'seed', 'budget', 'method'])


def main():
    mainreg = read('configs/b1g_sources_main.json')
    minireg = read('configs/b1g_sources_mini.json')
    historical = mainreg['groups'] + minireg['groups']
    mlocal = 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/'
    mseal = read(mlocal + 'ranking_seal.json')
    m_inputs = mseal['inputs']
    groups = []
    existing = {}
    # The first three completed main methods plus all full native references.
    for row in mseal['cells']:
        if row['method'] not in METHODS and row['method'] not in ['full_x', 'full_y']:
            continue
        item = {k: row[k] for k in ['dataset', 'pair', 'seed', 'budget', 'method']}
        item.update(ranking={'path': MROOT + '/' + row['ranking_path'], 'sha256': row['ranking_sha256']},
                    original_source='B1-M sealed main-compatible cell', original_method=row['method'])
        existing[identity(item)] = item
    # Original converter 25/50 cells: retain the original method alias.
    imported = read('results/fiqa_development/metrics/index.json') if (ROOT / 'results/fiqa_development/metrics/index.json').exists() else None
    if imported is None:
        # Imported64's source seal is the primary rank identity, not a generated table.
        imported = read('provenance/source_run/ranking_seal.json')
    cells = imported['cells'] if isinstance(imported, dict) else imported
    for row in cells:
        if 'embedding_converter' not in row['method']:
            continue
        item = {k: row[k] for k in ['pair', 'seed', 'budget']}
        item.update(dataset='FiQA', method=METHODS[5], original_method=row['method'],
                    original_source='imported FiQA development source',
                    ranking={'path': REMOTE + '/code_42731eb_full_r4/results/fiqa_development/' + row['ranking_path'], 'sha256': row['ranking_sha256']})
        existing[identity(item)] = item
    for group in historical:
        if group['dataset'] != 'FiQA' or group['regime'] != 'fixed1024' or group['method'] not in NEW:
            continue
        g = copy.deepcopy(group)
        assert len(g['cases']) == 1 and g['cases'][0]['budget'] == '50pct'
        g['parity_case'] = g['cases'][0]
        if g['method'] != METHODS[5]:
            old = g['parity_case']
            item = {k: g[k] for k in ['dataset', 'pair', 'seed', 'method']}
            item.update(budget='50pct', ranking=old['published_ranking'],
                        original_method=g['method'], original_source='B1-P fixed1024 sealed cell')
            existing[identity(item)] = item
        missing_budgets = ['75pct'] if g['method'] == METHODS[5] else ['25pct', '75pct']
        g['cases'] = []
        for budget in missing_budgets:
            rel = f"inputs/FiQA/paid_seed{g['seed']}_{budget}.npy"
            g['cases'].append({'case_id': g['group_id'] + '_' + budget, 'budget': budget,
                               'paid': {'path': MROOT + '/' + rel, 'sha256': m_inputs[rel]}})
        groups.append(g)
    assert len(groups) == 30
    # All Nano vectors/ordered selections already exist; never encode again here.
    bases = [g for g in mainreg['groups'] if g['dataset'] != 'FiQA' and g['method'] == METHODS[0]]
    assert len(bases) == 30
    for base in bases:
        for method in NEW:
            g = copy.deepcopy(base)
            g.update(method=method, group_id=f"{g['dataset']}_{g['pair']}_seed{g['seed']}_fixed1024_{method}", proxy={'kind': 'new_fit'})
            for case in g['cases']:
                case['case_id'] = g['group_id'] + '_' + case['budget']
                del case['published_ranking']
            groups.append(g)
    missing = [{**{k: g[k] for k in ['dataset', 'pair', 'seed', 'method']}, 'budget': c['budget']}
               for g in groups for c in g['cases']]
    expected = set(itertools.product(DATASETS, PAIRS, SEEDS, BUDGETS, METHODS))
    expected.update((d, p, None, 'full', m) for d in DATASETS for p in PAIRS for m in ['full_x', 'full_y'])
    before = read('.aris/traces/research-review/2026-10-27_next_steps/dev_matrix_inventory.json')
    assert set(map(identity, missing)) == set(map(identity, before['missing_identities']))
    assert len(existing) == 416 and len(missing) == 320 and len(groups) == 120
    assert set(existing).isdisjoint(map(identity, missing))
    assert set(existing) | set(map(identity, missing)) == expected
    contexts = [spec(p) for p in ['configs/b1g_sources_main.json', 'configs/b1g_sources_mini.json']]
    groups.sort(key=lambda g: (g['dataset'] != 'FiQA', g['method'] == METHODS[5] if g['dataset'] != 'FiQA' else False,
                               DATASETS.index(g['dataset']), PAIRS.index(g['pair']), g['seed'], NEW.index(g['method'])))
    dump('configs/b1c_sources.json', {'groups': groups, 'contexts': contexts,
         'scope': 'B1c exactly320 missing DEV rankings;30 reused FiQA groups,90 potential new Nano fits; no TREC'})
    dump('configs/b1c_existing.json', {'cells': sorted(existing.values(), key=lambda x: str(identity(x))),
         'scope': '416 immutable existing main DEV cells; original method aliases and source identity retained'})
    print(json.dumps({'groups': len(groups), 'missing': len(missing), 'existing': len(existing), 'expected_main': len(expected)}))


if __name__ == '__main__':
    main()
