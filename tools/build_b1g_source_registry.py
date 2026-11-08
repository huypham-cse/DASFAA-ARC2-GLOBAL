"""Inventory existing B1-G inputs only; never compute diagnostics or read qrels."""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path('/root/arc2_global_paper_20261025')
MROOT = BASE / 'code_4056612/results/b1m_full_r1_20261026'
PROOT = BASE / 'code_7530c8e_mini_r5/results/b1p_full_mini_r5_20261026'
R1 = BASE / 'code_f1457b8_r1/results/b1p_full_r1_20261026'
PRIMARY = 'arc2_global_tangent2_r1'
MAIN = ('procrustes_global', PRIMARY, 'ridge_affine_l10_bias_regularized')
PAIRS = {'minilm_distilroberta': ('minilm_x', 'distilroberta_y'),
         'e5_small_base': ('e5_small_x', 'e5_base_y')}


def read(p):
    return json.loads(Path(p).read_text())


def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', choices=['main', 'mini'], required=True)
    ap.add_argument('--seal', type=Path, required=True)
    ap.add_argument('--legacy', type=Path)
    ap.add_argument('--inventory', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    assert not a.output.exists()
    cache = {}

    def fs(p, expected=None):
        p = Path(p)
        if str(p) not in cache:
            cache[str(p)] = {'path': str(p), 'sha256': digest(p)}
        item = cache[str(p)]
        if expected is not None:
            assert item['sha256'] == expected, str(p)
        return dict(item)

    pseal = read(a.seal)
    groups = {}
    contexts = [fs(a.seal)]
    if a.shard == 'main':
        ms = read(MROOT / 'ranking_seal.json')
        ml = read(MROOT.parent.parent / 'configs/b1m_lock.json')
        manifest = read(ml['fiqa']['manifest_path'])
        inv = read(a.inventory)['files']
        contexts += [fs(MROOT / n) for n in ['metadata.json', 'ranking_seal.json',
                     'p0_real_checks.json', 'encoding/metadata.json', 'scoring_r2_binary/completed.json']]
        contexts += [fs(MROOT.parent.parent / 'configs/b1m_lock.json'), fs(a.inventory), fs(a.legacy)]

        def mspec(rel):
            return fs(MROOT / rel, inv[MROOT.name + '/' + rel]['sha256'])

        def common(dataset, pair, seed):
            old, new = PAIRS[pair]
            if dataset == 'FiQA':
                vectors = manifest['vectors'][pair]
                vr = {name: fs(vectors[name]['path'], vectors[name]['sha256'])
                      for name in ['old_docs', 'new_docs', 'new_queries']}
            else:
                vr = {name: mspec(f'vectors/{dataset}/{label}_{kind}.npy') for name, label, kind in
                      [('old_docs', old, 'docs'), ('new_docs', new, 'docs'), ('new_queries', new, 'queries')]}
            return {'old_docs': vr['old_docs'], 'new_queries': vr['new_queries'],
                    'full_target_reference': vr['new_docs'], 'ids': mspec(f'inputs/{dataset}/ids.json'),
                    'anchors': mspec(f'inputs/{dataset}/anchors_seed{seed}.npy')}

        for c in ms['cells']:
            if c['seed'] is None or c['method'] not in MAIN:
                continue
            dataset, pair, seed, method = (c[k] for k in ['dataset', 'pair', 'seed', 'method'])
            gid = f'{dataset}_{pair}_seed{seed}_fixed1024_{method}'
            if gid not in groups:
                params = f'coefficients/{dataset}_{pair}_seed{seed}/parameters.npz'
                groups[gid] = dict(group_id=gid, dataset=dataset, pair=pair, method=method,
                                   seed=seed, regime='fixed1024', **common(dataset, pair, seed),
                                   proxy={'kind': 'b1m_parameters', 'file': mspec(params)}, cases=[])
            groups[gid]['cases'].append({'case_id': gid + '_' + c['budget'], 'budget': c['budget'],
                'paid': mspec(f'inputs/{dataset}/paid_seed{seed}_{c["budget"]}.npy'),
                'published_ranking': fs(MROOT / c['ranking_path'], c['ranking_sha256'])})
        legacy = {(x['pair'], x['seed']): x for x in read(a.legacy)}
        ipath = MROOT / 'inputs/FiQA'
    else:
        pl = read(PROOT.parent.parent / 'configs/b1p_lock.json')
        manifest = read(pl['fiqa']['manifest_path'])
        contexts += [fs(PROOT / n) for n in ['metadata.json', 'ranking_seal.json',
                    'scoring_recovery_r1_20261027/completed.json']]
        contexts += [fs(PROOT.parent.parent / 'configs/b1p_lock.json')]
        ipath = PROOT / 'inputs'

        def common(dataset, pair, seed):
            vectors = manifest['vectors'][pair]
            return {'old_docs': fs(vectors['old_docs']['path'], vectors['old_docs']['sha256']),
                    'new_queries': fs(vectors['new_queries']['path'], vectors['new_queries']['sha256']),
                    'full_target_reference': fs(vectors['new_docs']['path'], vectors['new_docs']['sha256']),
                    'ids': fs(ipath / 'ids.json'), 'anchors': fs(ipath / f'anchors_seed{seed}.npy')}

    for c in pseal['cells']:
        if c['seed'] is None or (c['regime'] == 'fixed1024' and c['method'] in MAIN):
            continue
        historical = c['regime'] == 'fixed1024' and c['method'] == 'embedding_converter_paper_spec'
        prior = bool(c.get('recovery_source_path'))
        if (a.shard == 'main') != (historical or prior):
            continue
        dataset, pair, seed, method, regime = (c[k] for k in ['dataset', 'pair', 'seed', 'method', 'regime'])
        gid = f'{dataset}_{pair}_seed{seed}_{regime}_{method}'
        assert gid not in groups
        origin = R1 if prior else PROOT
        if historical:
            x = legacy[(pair, seed)]
            mp = Path(x['path'])
            m = read(mp)
            contexts.append(fs(mp, x['expected_metadata_sha256']))
            assert m['status'] == 'CONVERTER_WORKER_PASS' and not m['qrels_read']
            assert m['proxy']['array_sha256'] == x['expected_proxy_sha256']
            proxy = {'kind': 'saved_npy', 'file': fs(mp.parent / 'proxy_full.npy', m['proxy']['sha256'])}
            rank = fs(BASE / 'code_42731eb_full_r4/results/fiqa_development' /
                      x['source_ranking_path'], c['ranking_sha256'])
        elif method in ['simplelinear_official_final50_mlp5', 'embedding_converter_paper_spec']:
            folder = origin / 'neural' / f'{pair}_seed{seed}_{regime}_{method}' / 'worker'
            receipt = c['fit_receipt']
            proxy = {'kind': 'saved_npy', 'file': fs(folder / 'proxy_full.npy',
                     receipt['artifacts']['proxy_full.npy']['sha256'])}
            contexts.append(fs(folder / 'metadata.json'))
            rank = fs(origin / c['ranking_path'], c['ranking_sha256'])
        else:
            params = origin / 'cpu' / f'{pair}_seed{seed}_{regime}_{method}' / 'parameters.npz'
            proxy = {'kind': 'b1p_parameters', 'file': fs(params, c['fit_receipt']['parameters_sha256'])}
            rank = fs(origin / c['ranking_path'], c['ranking_sha256'])
        group = dict(group_id=gid, dataset=dataset, pair=pair, method=method, seed=seed,
                     regime=regime, **common(dataset, pair, seed), proxy=proxy, cases=[])
        group['cases'].append({'case_id': gid + '_50pct', 'budget': '50pct',
            'paid': fs(ipath / f'paid_seed{seed}_50pct.npy'), 'published_ranking': rank})
        groups[gid] = group
    values = sorted(groups.values(), key=lambda x: x['group_id'])
    count = sum(len(g['cases']) for g in values)
    expected = (137, 377) if a.shard == 'main' else (73, 73)
    assert (len(values), count) == expected, (len(values), count)
    registry = {'shard': a.shard, 'expected_groups': len(values), 'expected_cases': count,
                'groups': values, 'contexts': list({x['path']: x for x in contexts}.values()),
                'scope': 'Existing fitted artifacts only; inventory performed without fitting, diagnostics or qrel reads'}
    with a.output.open('x') as f:
        json.dump(registry, f, indent=2)
        f.write('\n')
    print(json.dumps({'shard': a.shard, 'groups': len(values), 'cases': count,
                      'unique_source_files_hashed': len(cache), 'output': str(a.output)}))


if __name__ == '__main__':
    main()
