"""Prospective B1c R3 recovery:358 rankings,118 fresh fits,2 saved fits.

Frozen numerical helpers are imported unchanged. Destination rows are supplied
only through the exact paid budget slices; a historical full-Y hash is not a
claim that missing unpaid destination vectors were recovered. No label reader,
encoder, scoring launch, artificial resource cap, or continuation past STOP.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'ops')]
import numpy as np
import b1c_stage as frozen
from arc2_global.diagnostics import positions, safe_id, sha256, write_json
from arc2_global.numerics import _vectors, normalize_rows
from arc2_global.baseline_adapters import verify_upstream
from b1a_stage import Observations
from b1g_rank_worker import reconstruct_proxy
from b1g_stage import require_tracked, runtime
from b1p_stage import cpu_fit, LA2M, SIMPLE, CONVERTER

DATASETS, PAIRS, SEEDS, METHODS = frozen.DATASETS, frozen.PAIRS, frozen.SEEDS, frozen.METHODS
IDENTITY = frozen.IDENTITY
read_json, relative, save, ranked, PairedTargets = frozen.read_json, frozen.relative, frozen.save, frozen.ranked, frozen.PairedTargets
LOCKPATH = ROOT / 'configs/b1c_r3_lock.json'


def resolve_source_path(value, restored_root):
    """Original absolute roots have one explicit, deterministic mirror alias."""
    if str(value).startswith('/root/'):
        root = Path(restored_root).resolve()
        path = (root / str(value).lstrip('/')).resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError('Restored source path escapes immutable root')
    else:
        path = Path(value)
        if not path.is_absolute():
            path = ROOT / path
    return path.resolve(strict=True)


class Inputs(frozen.Inputs):
    def __init__(self, restored_root):
        super().__init__()
        self.restored_root = Path(restored_root).resolve()

    def path(self, spec):
        if not isinstance(spec, dict) or set(spec) != {'path', 'sha256'}:
            raise ValueError('Executable input requires exactly path and sha256')
        path = resolve_source_path(spec['path'], self.restored_root)
        return super().path({'path': str(path), 'sha256': spec['sha256']})


def reused(group):
    return (group['dataset'] == 'FiQA' and group['pair'] == 'minilm_distilroberta'
            and group['seed'] == 17 and group['method'] in (LA2M, SIMPLE))


def walk_specs(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'sha256'}:
            yield value
        else:
            for child in value.values():
                yield from walk_specs(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_specs(child)


def check_sources(lock, commit):
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != commit:
        raise ValueError('Deployment commit mismatch')
    if subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip():
        raise ValueError('Dirty tracked deployment')
    require_tracked(LOCKPATH)
    if lock.get('seeds') != list(SEEDS) or lock.get('smoke_converter_iterations') != 500:
        raise ValueError('Frozen seeds/smoke policy drift')
    if lock['converter_config']['iterations'] != 50_000 or lock['simplelinear_defaults']['num_epochs'] != 50:
        raise ValueError('Frozen baseline training budget drift')
    if (lock['expected_new_rankings'], lock['expected_existing_rankings'], lock['expected_complete_main_rankings']) != (358, 378, 736):
        raise ValueError('R3 finite matrix count drift')
    required = {'ops/b1c_r3_stage.py', 'ops/b1c_stage.py', 'ops/b1p_stage.py',
                'ops/b1p_neural_worker.py', 'ops/b1g_rank_worker.py', 'ops/b1g_stage.py'}
    sources = lock['source_sha256_canonical_lf']
    if not required <= set(sources):
        raise ValueError('R3 source lock is incomplete')
    for name, expected in sources.items():
        path = (ROOT / name).resolve(strict=True)
        if not path.is_relative_to(ROOT):
            raise ValueError('Source escaped checkout')
        require_tracked(path)
        if hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise ValueError('Canonical source drift: ' + name)


def registry_for(lock, inputs):
    path, prior = (inputs.path(lock[k]) for k in ('registry', 'existing_cells'))
    require_tracked(path)
    require_tracked(prior)
    registry, existing = read_json(path), read_json(prior)
    if registry.get('stage') != 'B1C_R3' or existing.get('stage') != 'B1C_R3':
        raise ValueError('Require distinct R3 registries')
    if Path(registry['restored_root']).resolve() != inputs.restored_root:
        raise ValueError('Restored root differs from immutable registry')
    expected = {(d, p, m, s, 'fixed1024') for d in DATASETS for p in PAIRS for m in METHODS for s in SEEDS}
    identities, gids, cases, shared = set(), set(), set(), {}
    for group in registry['groups']:
        key = tuple(group[k] for k in IDENTITY)
        gid = safe_id(group['group_id'])
        if key not in expected or key in identities or gid in gids:
            raise ValueError('Duplicate/unauthorized fitted-gallery identity')
        identities.add(key)
        gids.add(gid)
        keep = reused(group)
        budgets = {'25pct', '75pct'} if keep else {'25pct', '50pct', '75pct'}
        if len(group['cases']) != len(budgets) or {c['budget'] for c in group['cases']} != budgets:
            raise ValueError('R3 replacement requires every fresh fit at all3 budgets')
        if keep:
            if group['proxy']['kind'] != ('b1p_parameters' if group['method'] == LA2M else 'saved_npy'):
                raise ValueError('Wrong saved fit for retained FiQA identity')
            if group['parity_case']['budget'] != '50pct':
                raise ValueError('Saved fit requires50% parity')
        elif group['proxy'] != {'kind': 'new_fit'} or 'parity_case' in group:
            raise ValueError('Lost fit must be freshly fitted without old-rank parity gate')
        if group['dataset'] == 'FiQA' and not keep and group.get('historical_comparison', {}).get('budget') != '50pct':
            raise ValueError('Fresh FiQA fit requires an informational historical50% comparison')
        full = group['full_target_reference']
        if set(full) != {'original_path', 'source_sha256'}:
            raise ValueError('Historical full-Y reference must be documentary')
        records = group['cases'] + ([group['parity_case']] if keep else [])
        for case in records:
            cid = safe_id(case['case_id'])
            if cid in cases:
                raise ValueError('Duplicate case ID')
            cases.add(cid)
            desc = case['target_slice']
            targetkey = [group['dataset'], group['pair'], group['seed'], case['budget'], full['source_sha256'], case['paid']['sha256']]
            if (desc['cache_key'] != targetkey or desc['source_paid_sha256'] != case['paid']['sha256']
                    or desc['source_full_target_sha256'] != full['source_sha256'] or desc['dtype'] != 'float32'
                    or len(desc['shape']) != 2 or desc['shape'][1] != 768):
                raise ValueError('Paid target slice is not bound to exact ordered source IDs')
            recipe = case['target_source']
            keys = {'saved_slice': {'kind', 'file'}, 'full_target': {'kind', 'file'},
                    'b1g_75_subset': {'kind', 'paid', 'targets'}}
            if recipe.get('kind') not in keys or set(recipe) != keys[recipe['kind']]:
                raise ValueError('Unsupported paid target source recipe')
            if recipe['kind'] == 'full_target' and (group['dataset'] == 'FiQA' or recipe['file']['sha256'] != full['source_sha256']):
                raise ValueError('Full-Y access allowed only for restored exact Nano cache')
            if recipe['kind'] == 'b1g_75_subset':
                source75 = next(c for c in records if c['budget'] == '75pct')
                if recipe['paid']['sha256'] != source75['paid']['sha256'] or recipe['targets']['sha256'] != source75['target_slice']['source_sha256']:
                    raise ValueError('75% slice recipe belongs to another ordered source')
            for name, spec in [('paid_' + str(group['seed']) + '_' + case['budget'], case['paid'])]:
                shared_key = (group['dataset'], name)
                if shared_key in shared and shared[shared_key] != spec['sha256']:
                    raise ValueError('Ordered paid IDs drift between methods/pairs')
                shared[shared_key] = spec['sha256']
        for name in ('ids', 'anchors', 'old_docs', 'new_queries'):
            shared_key = (group['dataset'], group['pair'] if name in ('old_docs', 'new_queries') else None,
                          group['seed'] if name == 'anchors' else None, name)
            if shared_key in shared and shared[shared_key] != group[name]['sha256']:
                raise ValueError('Shared ordered input drift: ' + name)
            shared[shared_key] = group[name]['sha256']
    if identities != expected or len(gids) != 120 or len(cases) != 360:
        raise ValueError('R3 must contain120 groups,358 new cases and2 parity cases')
    if registry.get('expected_groups') != 120 or registry.get('expected_cases') != 358 or len(existing['cells']) != 378:
        raise ValueError('R3 registry count declarations differ')
    # Complete source preflight includes historical378 and recipes, before any fit.
    for spec in walk_specs(registry):
        inputs.path(spec)
    for row in existing['cells']:
        inputs.path(row['ranking'])
    return registry


def subset_targets(source_paid, source_targets, requested, n_docs):
    """Extract ordered rows by document ID; never infer missing target vectors."""
    source_paid = positions(source_paid, 'source paid', n_docs, nonempty=True)
    requested = positions(requested, 'requested paid', n_docs, nonempty=True)
    targets = _vectors('source paid targets', source_targets, dim=768)
    if len(targets) != len(source_paid):
        raise ValueError('Paid target rows do not match source ordered IDs')
    order = np.argsort(source_paid, kind='stable')
    sorted_ids = source_paid[order]
    at = np.searchsorted(sorted_ids, requested)
    if np.any(at == len(sorted_ids)) or not np.array_equal(sorted_ids[np.minimum(at, len(sorted_ids) - 1)], requested):
        raise ValueError('Source slice omits requested document/anchor')
    return np.asarray(targets[order[at]])


def prepare_targets(group, inputs, copied, n_docs, anchors):
    records = group['cases'] + ([group['parity_case']] if reused(group) else [])
    prepared = {}
    for case in records:
        budget = case['budget']
        paidpath = inputs.copy(case['paid'], copied / ('paid_seed' + str(group['seed']) + '_' + budget + '.npy'))
        paid = positions(np.load(paidpath, allow_pickle=False), 'paid', n_docs, nonempty=True)
        if len(paid) != int(np.floor(int(budget.removesuffix('pct')) / 100 * n_docs)) or not np.isin(anchors, paid).all():
            raise ValueError('Paid set must charge exact floor fraction and include all anchors')
        recipe, desc = case['target_source'], case['target_slice']
        if recipe['kind'] == 'saved_slice':
            target = inputs.array(recipe['file'])
        elif recipe['kind'] == 'b1g_75_subset':
            target = subset_targets(inputs.array(recipe['paid']), inputs.array(recipe['targets']), paid, n_docs)
        else:
            full = inputs.array(recipe['file'])
            if full.shape != (n_docs, 768) or full.dtype != np.float32:
                raise ValueError('Restored Nano full-Y shape/dtype mismatch')
            target = np.asarray(full[paid])
        target = _vectors('exact budget target slices', target, dim=768)
        if list(target.shape) != desc['shape'] or len(target) != len(paid):
            raise ValueError('Budget target exact shape/dtype mismatch')
        targetpath = copied / (group['pair'] + '_targets_seed' + str(group['seed']) + '_' + budget + '.npy')
        if not targetpath.exists():
            save(targetpath, target)
        if sha256(targetpath) != desc['source_sha256']:
            raise ValueError('Re-materialized budget target bytes differ from frozen B1G slice')
        prepared[budget] = (paid, np.load(targetpath, mmap_mode='r', allow_pickle=False), paidpath, targetpath)
    # Cross-budget overlaps must be exactly equal, including ordered anchors.
    base_paid, base_targets, _, _ = prepared['75pct']
    for budget, (paid, target, _, _) in prepared.items():
        if not np.array_equal(subset_targets(base_paid, base_targets, paid, n_docs), target):
            raise ValueError('Conflicting target values on overlapping budget slices: ' + budget)
    paired = subset_targets(base_paid, base_targets, anchors, n_docs)
    return prepared, paired


def saved_parity(computed, expected):
    if (computed.dtype != np.int64 or expected.dtype != np.int64 or computed.ndim != 2
            or computed.shape != expected.shape or not np.array_equal(computed, expected)):
        raise AssertionError('Retained saved-fit50% ranking parity failed')


def materialization_preflight(registry, inputs, out):
    """Check every exact budget slice, including20 FiQA subsets, before any fit."""
    seen, receipts = set(), []
    for group in registry['groups']:
        key = (group['dataset'], group['pair'], group['seed'])
        if key in seen:
            continue
        seen.add(key)
        copied = out / 'inputs' / group['dataset']
        old = inputs.array(group['old_docs'])
        if old.ndim != 2 or old.shape[1] != 384 or old.dtype != np.float32:
            raise ValueError('Preflight source gallery shape/dtype mismatch')
        anchorpath = inputs.copy(group['anchors'], copied / ('anchors_seed' + str(group['seed']) + '.npy'))
        anchors = positions(np.load(anchorpath, allow_pickle=False), 'anchors', len(old), nonempty=True)
        if len(anchors) != 1024:
            raise ValueError('Preflight requires exactly1024 ordered anchors')
        prepared, paired = prepare_targets(group, inputs, copied, len(old), anchors)
        for budget, (_, targets, _, path) in prepared.items():
            receipts.append({'dataset': key[0], 'pair': key[1], 'seed': key[2], 'budget': budget,
                             'path': relative(out, path), 'sha256': sha256(path),
                             'shape': list(targets.shape), 'dtype': str(targets.dtype),
                             'expected_original_B1G_sha256': next(c['target_slice']['source_sha256'] for c in
                                 group['cases'] + ([group['parity_case']] if reused(group) else []) if c['budget'] == budget)})
        del old, prepared, paired
    if len(seen) != 40 or len(receipts) != 120:
        raise ValueError('Need all40 dataset/pair/seed and120 budget slice identities before fitting')
    write_json(out / 'target_materialization_preflight.json',
               {'status': 'PASS', 'before_any_fit': True, 'budget_slices': receipts,
                'fiqa_budget_slices': 30, 'fiqa_25_50_subset_identities': 20, 'qrels_opened': False})
    return receipts


def fixture_checks(out):
    """Synthetic only: slice order/coverage/overlap, dtype, ties and serialization."""
    fixture = out / 'fixtures'
    fixture.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(17)
    target = normalize_rows(rng.normal(size=(128, 768)).astype(np.float32))
    ids = np.array([90, 4, 17, 29, 63], dtype=np.int64)
    selected = np.array([63, 4, 29], dtype=np.int64)
    np.testing.assert_array_equal(subset_targets(ids, target[ids], selected, 128), target[selected])
    failures = 0
    for sourceids, values, wanted in [(ids, target[ids], np.array([1])), (ids, target[ids].astype(np.float64), selected),
                                      (ids, target[ids, :767], selected), (np.array([4, 4]), target[:2], selected)]:
        try:
            subset_targets(sourceids, values, wanted, 128)
        except ValueError:
            failures += 1
        else:
            raise AssertionError('Invalid synthetic slice accepted')
    save(fixture / 'ordered.npy', target[selected])
    np.testing.assert_array_equal(np.load(fixture / 'ordered.npy', allow_pickle=False), target[selected])
    guarded = PairedTargets(selected, target[selected])
    np.testing.assert_array_equal(guarded[selected], target[selected])
    try:
        guarded[np.array([0])]
    except ValueError:
        pass
    else:
        raise AssertionError('Paired-only fit guard failed')
    docs = np.tile(np.array([[1., 0.]], dtype=np.float32), (128, 1))
    ranks = ranked(docs[:2], docs, np.array([1]), docs[[1]],
                   {'doc_ids': ['d' + str(i) for i in range(128)], 'query_ids': ['d0', 'q1']})
    np.testing.assert_array_equal(ranks[0], np.arange(1, 101))
    np.testing.assert_array_equal(ranks[1], np.arange(100))
    saved_parity(ranks, ranks.copy())
    corrupt = ranks.copy()
    corrupt[0, 0] = 127
    try:
        saved_parity(ranks, corrupt)
    except AssertionError:
        pass
    else:
        raise AssertionError('Saved parity accepted changed ranking')
    result = {'ordered_slice_indexing': 'PASS', 'rejected_invalid_slices': failures,
              'serialization': 'PASS', 'saved_fit_parity': 'PASS', 'paired_only_guard': 'PASS',
              'stable_ties_identical_ID_exclusion': 'PASS', 'qrels_opened': False}
    write_json(fixture / 'checks.json', result)
    return result


def smoke(lock, commit, out):
    checks = fixture_checks(out)
    rng = np.random.default_rng(17)
    old = normalize_rows(rng.normal(size=(256, 384)).astype(np.float32))
    paired = normalize_rows((old[:128] @ rng.normal(size=(384, 768)).astype(np.float32) + .1).astype(np.float32))
    anchors = np.arange(128, dtype=np.int64)
    oldpath = out / 'synthetic_old.npy'
    save(oldpath, old)
    query = normalize_rows(rng.normal(size=(8, 768)).astype(np.float32))
    ids = {'doc_ids': ['d' + str(i) for i in range(256)], 'query_ids': ['q' + str(i) for i in range(8)]}
    records = []
    for method in METHODS:
        if method == LA2M:
            proxy, receipt = cpu_fit(LA2M, old, PairedTargets(anchors, paired), anchors, 17, out / 'cpu' / ('synthetic_' + method))
            recovered = reconstruct_proxy(old, {'kind': 'b1p_parameters', 'file': {'path': str(out / 'cpu' / ('synthetic_' + method) / 'parameters.npz'), 'sha256': receipt['parameters_sha256']}}, method, {})
            np.testing.assert_array_equal(proxy, recovered)
        else:
            proxy, receipt = frozen.neural(lock, commit, out, 'synthetic', method, method, 17, oldpath, old, anchors, paired, 'smoke')
        ranking = ranked(query, _vectors('synthetic proxy', proxy, dim=768), anchors, paired, ids)
        path = out / 'rankings' / ('synthetic_' + method + '.npy')
        save(path, ranking)
        np.testing.assert_array_equal(np.load(path, allow_pickle=False), ranking)
        records.append({'method': method, 'fit_receipt': receipt, 'ranking_sha256': sha256(path)})
    return {'fixtures': checks, 'methods': records, 'scientific_rankings_generated': 0, 'qrels_opened': False}


def full(lock, commit, out, metadata, registry, inputs):
    cells, fits, parity, historical_comparisons = [], [], [], []
    (out / 'groups').mkdir()
    materialization_preflight(registry, inputs, out)
    write_json(out / 'cells_pre_qrels.json', cells)
    write_json(out / 'parity_receipts.json', parity)
    for index, group in enumerate(frozen.ordered_groups(registry['groups'])):
        dataset, pair, method, seed, regime = (group[k] for k in IDENTITY)
        gid, keep = group['group_id'], reused(group)
        folder = out / 'groups' / gid
        folder.mkdir()
        write_json(out / 'progress.json', {'stage': 'R3_GROUP_START', 'group': gid, 'group_index': index,
                   'groups_total': 120, 'rankings_complete': len(cells), 'rankings_total': 358})
        oldpath = inputs.path(group['old_docs'])
        old = _vectors('old source documents', inputs.array(group['old_docs']), dim=384)
        queries = _vectors('destination queries', inputs.array(group['new_queries']), dim=768)
        copied = out / 'inputs' / dataset
        idpath = inputs.copy(group['ids'], copied / 'ids.json')
        ids = read_json(idpath)
        if len(ids['doc_ids']) != len(old) or len(ids['query_ids']) != len(queries) or len(set(ids['doc_ids'])) != len(old) or len(set(ids['query_ids'])) != len(queries):
            raise ValueError('ID/vector population or uniqueness mismatch')
        anchorpath = inputs.copy(group['anchors'], copied / ('anchors_seed' + str(seed) + '.npy'))
        anchors = positions(np.load(anchorpath, allow_pickle=False), 'anchors', len(old), nonempty=True)
        if len(anchors) != 1024:
            raise ValueError('R3 fit requires exactly1024 ordered anchors')
        prepared, paired = prepare_targets(group, inputs, copied, len(old), anchors)
        paired_path = folder / (dataset + '_anchor_targets.npy')
        save(paired_path, paired)
        began = time.perf_counter()
        if keep:
            spec = {'kind': group['proxy']['kind'], 'file': {'path': str(inputs.path(group['proxy']['file'])), 'sha256': group['proxy']['file']['sha256']}}
            hashes = {}
            proxy = reconstruct_proxy(old, spec, method, hashes)
            receipt = {'status': 'HISTORICAL_FIT_REUSED', 'new_fit': False, 'fit_pairs': 1024,
                       'historical_fit_seconds': None, 'fit_seconds_semantics': 'Historical fit reused; null is not zero cost',
                       'reconstruction_seconds': time.perf_counter() - began, 'source_proxy': group['proxy'],
                       'reconstruction_input_hashes': hashes, 'new_physical_document_encodes': 0}
            if 'historical_fit_receipt' in group:
                inputs.copy(group['historical_fit_receipt'], folder / 'historical_fit_receipt.json')
                receipt['historical_fit_receipt'] = read_json(inputs.path(group['historical_fit_receipt']))
        elif method == LA2M:
            proxy, receipt = cpu_fit(LA2M, old, PairedTargets(anchors, paired), anchors, seed, out / 'cpu' / (dataset + '_' + gid))
            receipt['new_fit'] = True
        else:
            proxy, receipt = frozen.neural(lock, commit, out, dataset, gid, method, seed, oldpath, old, anchors, paired, 'full', group['old_docs']['sha256'])
        proxy = _vectors('pristine proxy', proxy, dim=768)
        if len(proxy) != len(old):
            raise ValueError('Proxy population mismatch')
        receipt.update(group_id=gid, dataset=dataset, pair=pair, seed=seed, regime=regime, method=method,
                       paired_target_path=relative(out, paired_path), paired_target_sha256=sha256(paired_path),
                       anchor_target_source_budget='75pct', shared_across_budgets=[c['budget'] for c in group['cases']])
        write_json(folder / 'fit_receipt.json', receipt)
        fits.append({'group_id': gid, 'path': relative(out, folder / 'fit_receipt.json'), 'sha256': sha256(folder / 'fit_receipt.json'), 'new_fit': not keep})
        for case in ([group['parity_case']] if keep else []) + sorted(group['cases'], key=lambda c: c['budget']):
            budget = case['budget']
            paid, paid_targets, paidpath, targetpath = prepared[budget]
            started = time.perf_counter()
            ranking = ranked(queries, proxy, paid, paid_targets, ids)
            search_seconds = time.perf_counter() - started
            is_parity = keep and case is group['parity_case']
            path = folder / (dataset + '_parity_50pct.npy') if is_parity else out / 'rankings' / (dataset + '_' + safe_id(case['case_id']) + '.npy')
            digest = save(path, ranking)
            np.testing.assert_array_equal(np.load(path, allow_pickle=False), ranking)
            if is_parity:
                expected = inputs.array(case['published_ranking'])
                passed = ranking.shape == expected.shape and ranking.dtype == expected.dtype == np.int64 and np.array_equal(ranking, expected)
                parity.append({'group_id': gid, 'case_id': case['case_id'], 'status': 'PASS' if passed else 'FAIL',
                               'ranking_path': relative(out, path), 'ranking_sha256': digest, 'published_ranking': case['published_ranking']})
                write_json(out / 'parity_receipts.json', parity)
                saved_parity(ranking, expected)
                continue
            if not keep and dataset == 'FiQA' and budget == '50pct':
                historical = inputs.array(group['historical_comparison']['published_ranking'])
                same_shape = ranking.shape == historical.shape
                historical_comparisons.append({'group_id': gid, 'case_id': case['case_id'],
                    'informational_only': True, 'affects_acceptance_or_selection': False,
                    'equal': bool(same_shape and ranking.dtype == historical.dtype and np.array_equal(ranking, historical)),
                    'computed_shape': list(ranking.shape), 'historical_shape': list(historical.shape),
                    'changed_rank_positions': int(np.count_nonzero(ranking != historical)) if same_shape else None,
                    'historical_ranking': group['historical_comparison']['published_ranking'],
                    'prospective_ranking_sha256': digest})
                write_json(out / 'fresh_fiqa_historical_comparisons.json', historical_comparisons)
            cells.append({**{k: group[k] for k in IDENTITY}, 'group_id': gid, 'case_id': case['case_id'],
                          'budget': budget, 'ranking_path': relative(out, path), 'ranking_sha256': digest,
                          'fit_pairs': 1024, 'unique_destination_encodings': len(np.union1d(anchors, paid)),
                          'paid_count': len(paid), 'anchor_count': len(anchors), 'new_physical_document_encodes': 0,
                          'reused': False, 'fit_reused': keep, 'fit_receipt': fits[-1], 'search_seconds': search_seconds,
                          'ids_path': relative(out, idpath), 'ids_sha256': sha256(idpath),
                          'anchors_path': relative(out, anchorpath), 'anchors_sha256': sha256(anchorpath),
                          'paid_path': relative(out, paidpath), 'paid_sha256': sha256(paidpath),
                          'paid_targets_path': relative(out, targetpath), 'paid_targets_sha256': sha256(targetpath)})
            write_json(out / 'cells_pre_qrels.json', cells)
            write_json(out / 'progress.json', {'stage': 'R3_RANKING', 'group': gid, 'rankings_complete': len(cells), 'rankings_total': 358})
        del old, queries, proxy, paired, prepared
    if len(cells) != 358 or len(fits) != 120 or sum(f['new_fit'] for f in fits) != 118 or len(parity) != 2 or len(historical_comparisons) != 28 or not all(p['status'] == 'PASS' for p in parity):
        raise AssertionError('Incomplete R3 endpoint/fit/parity accounting')
    sources = inputs.finish()
    write_json(out / 'input_hashes.json', sources)
    write_json(out / 'fit_receipts.json', fits)
    artifacts = {p.relative_to(out).as_posix(): sha256(p) for p in out.rglob('*')
                 if p.is_file() and p.relative_to(out).as_posix() not in ('metadata.json', 'progress.json', 'resource_trace.jsonl')}
    seal = {'status': 'RANKINGS_SEALED', 'stage': 'B1C_R3', 'scope': 'Same736-cell inspected DEV matrix;358 prospective recovery endpoints',
            'code_commit': commit, 'lock_sha256': metadata['lock_sha256'], 'registry_sha256': lock['registry']['sha256'],
            'existing_registry_sha256': lock['existing_cells']['sha256'], 'sealed_utc': datetime.now(timezone.utc).isoformat(),
            'cells': cells, 'fit_groups': fits, 'fiqa_50pct_parity': parity, 'source_inputs': sources,
            'fresh_fiqa_historical_comparisons': historical_comparisons,
            'inputs': {p.relative_to(out).as_posix(): sha256(p) for p in (out / 'inputs').rglob('*') if p.is_file()},
            'artifacts': artifacts, 'qrels_opened': False, 'ranking_process_qrel_reads': 0,
            'new_physical_document_encodes': 0, 'new_nano_fits': 90, 'new_fiqa_fits': 28,
            'historical_fiqa_fits_reused': 2, 'total_fit_groups': 120,
            'score_arithmetic': 'float32 query batch16 @ gallery.T; stable original row-order ties; identical ID exclusion'}
    write_json(out / 'ranking_seal.json', seal)
    metadata.update(status='B1C_R3_RANKINGS_SEALED_STOP', ranking_count=358, ranking_seal_sha256=sha256(out / 'ranking_seal.json'),
                    new_nano_fits=90, new_fiqa_fits=28, historical_fiqa_fits_reused=2,
                    next_action='Separate DEV scoring after358 seal; report/final D1 then STOP before B2')
    write_json(out / 'progress.json', {'stage': 'R3_RANKINGS_SEALED_STOP', 'rankings_complete': 358, 'rankings_total': 358})


def main():
    global LOCKPATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=('smoke', 'full'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--smoke', type=Path)
    parser.add_argument('--lock', type=Path, default=LOCKPATH)
    parser.add_argument('--restored-root', type=Path, required=True)
    args = parser.parse_args()
    LOCKPATH = args.lock.resolve(strict=True)
    frozen.LOCKPATH = LOCKPATH
    out = args.output.resolve()
    if out.parent != (ROOT / 'results').resolve() or not out.name.startswith('b1c_r3_'):
        raise ValueError('Output must be a unique results/b1c_r3_* directory')
    out.mkdir(parents=False, exist_ok=False)
    started = time.perf_counter()
    metadata = {'status': 'B1C_R3_RUNNING', 'stage': args.stage, 'code_commit': args.code_commit,
                'restored_root': str(args.restored_root.resolve()), 'started_utc': datetime.now(timezone.utc).isoformat(),
                'failures': [], 'qrels_opened': False, 'ranking_process_qrel_reads': 0,
                'TREC_access': False, 'new_physical_document_encodes': 0, 'artificial_time_memory_caps': None}
    write_json(out / 'metadata.json', metadata)
    monitor = Observations(out)
    monitor.begin()
    def interrupted(sig, frame):
        raise RuntimeError('Received signal ' + str(sig))
    signal.signal(signal.SIGTERM, interrupted)
    try:
        lock = read_json(LOCKPATH)
        metadata['lock_sha256'] = sha256(LOCKPATH)
        check_sources(lock, args.code_commit)
        metadata['runtime'] = runtime(lock)
        inputs = Inputs(args.restored_root)
        upstream = verify_upstream(lock['upstream'], lock['upstream_raw_sha256'])
        for name, digest in lock['upstream_raw_sha256'].items():
            inputs.path({'path': str(upstream / name), 'sha256': digest})
        if lock.get('acquisition_manifest'):
            require_tracked(inputs.path(lock['acquisition_manifest']))
        registry = registry_for(lock, inputs)
        metadata.update(registry_sha256=lock['registry']['sha256'], existing_registry_sha256=lock['existing_cells']['sha256'])
        if args.stage == 'smoke':
            metadata.update(smoke_checks=smoke(lock, args.code_commit, out), status='B1C_R3_SMOKE_PASS')
            metadata['source_inputs'] = inputs.finish()
        else:
            if not args.smoke:
                raise ValueError('Full requires successful matching committed R3 smoke')
            smeta = read_json(args.smoke / 'metadata.json')
            if smeta['status'] != 'B1C_R3_SMOKE_PASS' or any(smeta[k] != metadata[k] for k in ('code_commit', 'lock_sha256', 'registry_sha256', 'existing_registry_sha256', 'restored_root')):
                raise ValueError('R3 smoke identity does not match full')
            metadata['smoke'] = {'path': str(args.smoke.resolve()), 'metadata_sha256': sha256(args.smoke / 'metadata.json')}
            full(lock, args.code_commit, out, metadata, registry, inputs)
    except BaseException as exc:
        metadata.update(status='B1C_R3_FAILED_PRESERVED', failures=[repr(exc)], traceback=traceback.format_exc())
    finally:
        monitor.end()
        metadata.update(wall_seconds=time.perf_counter() - started, peak_process_tree_rss_bytes=monitor.peak,
                        ended_utc=datetime.now(timezone.utc).isoformat())
        write_json(out / 'metadata.json', metadata)
    print(json.dumps({'status': metadata['status'], 'failures': metadata['failures']}))
    return 0 if metadata['status'] in ('B1C_R3_SMOKE_PASS', 'B1C_R3_RANKINGS_SEALED_STOP') else 1


if __name__ == '__main__':
    raise SystemExit(main())
