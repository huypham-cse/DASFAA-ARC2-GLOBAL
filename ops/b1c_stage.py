"""B1c's 320 missing DEV rankings, with paired-only fits and a separate scorer.

Run only from the committed B1c lock/protocol. Existing FiQA fits must reproduce
their frozen 50% ranking before producing missing endpoints. Nano fits share
one fixed1024 model across all three budgets. This module has no qrel reader,
encoder, automatic scoring, B2 launcher, or artificial resource/time limit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'ops')]

import numpy as np
from arc2_global.diagnostics import positions, safe_id, save_array, sha256, write_json
from arc2_global.numerics import _vectors, normalize_rows
from arc2_global.retrieval import exact_topk
from b1a_stage import Observations
from b1g_rank_worker import reconstruct_proxy
from b1g_stage import require_tracked, runtime
from b1p_stage import cpu_fit, run_observed_child, LA2M, SIMPLE, CONVERTER
from b1c_recovery import verify_manifest, import_groups, synthetic_checks as recovery_checks

DATASETS = ('FiQA', 'NanoNQ', 'NanoHotpotQA', 'NanoFEVER')
PAIRS = ('minilm_distilroberta', 'e5_small_base')
SEEDS = (17, 29, 41, 53, 67)
METHODS = (LA2M, SIMPLE, CONVERTER)
IDENTITY = ('dataset', 'pair', 'method', 'seed', 'regime')
LOCKPATH = ROOT / 'configs/b1c_lock.json'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def relative(out, path):
    return Path(path).resolve().relative_to(out.resolve()).as_posix()


def save(path, values):
    path.parent.mkdir(parents=True, exist_ok=True)
    save_array(path, values)
    return sha256(path)


class Inputs:
    """Hash each immutable source once, rejecting conflicting source specs.

    Stat identity is rechecked on every access; finalization rechecks every
    cached source. Source files are never written, renamed or relabeled.
    """
    def __init__(self):
        self.files = {}

    @staticmethod
    def stamp(path):
        stat = path.stat()
        return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)

    def path(self, spec):
        if not isinstance(spec, dict) or not {'path', 'sha256'} <= set(spec):
            raise ValueError('Missing immutable input path/hash')
        if not isinstance(spec['sha256'], str) or len(spec['sha256']) != 64 or any(c not in '0123456789abcdef' for c in spec['sha256']):
            raise ValueError('Malformed source SHA256')
        path = Path(spec['path'])
        path = (path if path.is_absolute() else ROOT / path).resolve(strict=True)
        key = str(path)
        stamp = self.stamp(path)
        if key in self.files:
            previous = self.files[key]
            if previous['sha256'] != spec['sha256'] or previous['stat'] != stamp:
                raise ValueError('Conflicting or changed source: ' + key)
        else:
            if sha256(path) != spec['sha256']:
                raise ValueError('Input hash drift: ' + key)
            self.files[key] = {'sha256': spec['sha256'], 'bytes': stamp[2], 'stat': stamp}
        return path

    def array(self, spec):
        return np.load(self.path(spec), mmap_mode='r', allow_pickle=False)

    def copy(self, spec, destination):
        source = self.path(spec)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if sha256(destination) != spec['sha256']:
                raise ValueError('Conflicting copied input: ' + str(destination))
        else:
            with source.open('rb') as stream, destination.open('xb') as target:
                shutil.copyfileobj(stream, target, length=8 * 1024 * 1024)
            if sha256(destination) != spec['sha256']:
                raise ValueError('Copied input hash mismatch')
        return destination

    def finish(self):
        for key, row in self.files.items():
            if self.stamp(Path(key)) != row['stat']:
                raise ValueError('Source changed during run: ' + key)
        return {key: {'sha256': row['sha256'], 'bytes': row['bytes']} for key, row in self.files.items()}


def check_sources(lock, commit):
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != commit:
        raise ValueError('Deployment commit mismatch')
    if subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip():
        raise ValueError('Dirty tracked deployment')
    require_tracked(LOCKPATH)
    if lock.get('seeds') != list(SEEDS) or lock.get('smoke_converter_iterations') != 500:
        raise ValueError('B1c seeds/smoke configuration drift')
    if lock['converter_config']['iterations'] != 50_000 or lock['simplelinear_defaults']['num_epochs'] != 50:
        raise ValueError('Frozen baseline training budget drift')
    sources = lock['source_sha256_canonical_lf']
    required = {'ops/b1c_stage.py', 'ops/b1p_stage.py', 'ops/b1p_neural_worker.py', 'ops/b1g_rank_worker.py', 'ops/b1g_stage.py'}
    if not required <= set(sources):
        raise ValueError('B1c source lock is incomplete')
    for name, expected in sources.items():
        path = (ROOT / name).resolve(strict=True)
        if not path.is_relative_to(ROOT):
            raise ValueError('Source path escapes deployment')
        require_tracked(path)
        if hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise ValueError('Canonical source drift: ' + name)


def registry_for(lock, inputs):
    path = inputs.path(lock['registry'])
    existing = inputs.path(lock['existing_cells'])
    require_tracked(path)
    require_tracked(existing)
    registry = read_json(path)
    groups = registry['groups']
    expected = {(d, p, m, s, 'fixed1024') for d in DATASETS for p in PAIRS for m in METHODS for s in SEEDS}
    keys, gids, cases = set(), set(), set()
    endpoint_count = 0
    # Shared ordered inputs must have identical bytes across methods/pairs.
    shared = {}
    for group in groups:
        key = tuple(group[k] for k in IDENTITY)
        gid = safe_id(group['group_id'])
        if key not in expected or key in keys or gid in gids:
            raise ValueError('Duplicate or unauthorized fitted-gallery identity')
        keys.add(key)
        gids.add(gid)
        dataset, pair, method, seed, _ = key
        budgets = {'75pct'} if dataset == 'FiQA' and method == CONVERTER else ({'25pct', '75pct'} if dataset == 'FiQA' else {'25pct', '50pct', '75pct'})
        if len(group['cases']) != len(budgets) or {c['budget'] for c in group['cases']} != budgets:
            raise ValueError('Registry does not contain exactly the missing budgets')
        kind = group['proxy']['kind']
        if dataset == 'FiQA':
            if kind not in ('saved_npy', 'b1p_parameters') or (kind == 'b1p_parameters' and method != LA2M):
                raise ValueError('Unsupported FiQA saved fit')
            if group['parity_case']['budget'] != '50pct':
                raise ValueError('FiQA reuse needs the original 50% parity endpoint')
            safe_id(group['parity_case']['case_id'])
        elif kind != 'new_fit':
            raise ValueError('Nano B1c groups must use their locked new fixed1024 fit')
        records = list(group['cases']) + ([group['parity_case']] if dataset == 'FiQA' else [])
        for case in group['cases']:
            cid = safe_id(case['case_id'])
            if cid in cases:
                raise ValueError('Duplicate endpoint ID')
            cases.add(cid)
            endpoint_count += 1
        for name, spec in [('ids', group['ids']), ('anchors_' + str(seed), group['anchors'])] + [('paid_' + str(seed) + '_' + c['budget'], c['paid']) for c in records]:
            shared_key = (dataset, name)
            if shared_key in shared and shared[shared_key] != spec['sha256']:
                raise ValueError('Ordered input drift across groups: ' + str(shared_key))
            shared[shared_key] = spec['sha256']
        for name in ('old_docs', 'new_queries', 'full_target_reference'):
            shared_key = (dataset, pair, name)
            digest = group[name]['sha256']
            if shared_key in shared and shared[shared_key] != digest:
                raise ValueError('Vector cache drift across fitted groups: ' + str(shared_key))
            shared[shared_key] = digest
    if keys != expected or len(groups) != 120 or endpoint_count != 320:
        raise ValueError('B1c must contain exactly120 galleries and320 missing rankings')
    if registry.get('expected_groups', 120) != 120 or registry.get('expected_cases', 320) != 320:
        raise ValueError('Registry count declarations differ')
    return registry


class PairedTargets:
    """Supply the unchanged CPU helper only the selected destination rows."""
    def __init__(self, fit_ids, paired):
        self.fit_ids, self.paired = fit_ids, paired

    def __getitem__(self, ids):
        if not np.array_equal(ids, self.fit_ids):
            raise ValueError('CPU fit requested rows outside supplied anchors')
        return self.paired


def neural(lock, commit, out, dataset, group_id, method, seed, oldpath, old, anchors, paired, mode, source_sha256=None):
    directory = out / 'neural' / safe_id(dataset + '_' + group_id)
    directory.mkdir(parents=True, exist_ok=False)
    source = directory / (dataset + '_paired_source.npy')
    target = directory / (dataset + '_paired_target.npy')
    save(source, np.asarray(old[anchors]))
    save(target, paired)
    request = {'mode': mode, 'method': 'embedding_converter' if method == CONVERTER else 'simplelinear',
               'regime': 'anchors', 'seed': seed, 'lockpath': str(LOCKPATH),
               'output': str(directory / 'worker'), 'paired_source': str(source), 'paired_target': str(target),
               'full_source': str(oldpath), 'code_commit': commit,
               'input_sha256': {'paired_source': sha256(source), 'paired_target': sha256(target), 'full_source': source_sha256 or sha256(oldpath)}}
    write_json(directory / 'request.json', request)
    env = {**os.environ, **lock['environment'], 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1'}
    exit_record = run_observed_child([lock['gpu_python'], '-u', str(ROOT / 'ops/b1p_neural_worker.py'), '--request', str(directory / 'request.json')], env, directory, sha256(directory / 'request.json'))
    if exit_record['returncode']:
        raise RuntimeError('Neural worker failed; preserve all artifacts: ' + str(directory))
    worker = directory / 'worker'
    receipt = read_json(worker / 'metadata.json')
    if receipt['status'] != 'B1P_NEURAL_' + mode.upper() + '_PASS' or receipt.get('fit_pairs') != len(anchors):
        raise ValueError('Unexpected neural worker completion receipt')
    proxy = np.load(worker / 'proxy_full.npy', mmap_mode='r', allow_pickle=False)
    receipt = {**receipt, 'metadata_path': relative(out, worker / 'metadata.json'),
               'metadata_sha256': sha256(worker / 'metadata.json'), 'request_path': relative(out, directory / 'request.json'),
               'request_sha256': sha256(directory / 'request.json'), 'new_fit': True}
    return proxy, receipt


def ranked(queries, proxy, paid, paid_targets, ids):
    gallery = np.asarray(proxy).copy()
    gallery[paid] = paid_targets
    return exact_topk(queries, gallery, k=100, batch_rows=16, query_ids=ids['query_ids'],
                      document_ids=ids['doc_ids'], exclude_identical_ids=True)


def fixture_checks(out):
    """Small synthetic CPU checks; callable without a scientific deployment."""
    from b1m_score import synthetic_checks
    from b1c_score import synthetic_checks as b1c_checks
    fixture = out / 'fixtures'
    fixture.mkdir(parents=True, exist_ok=False)
    docs = np.tile(np.array([[1., 0.]], dtype=np.float32), (128, 1))
    queries = docs[:2].copy()
    ids = {'doc_ids': ['d' + str(i) for i in range(128)], 'query_ids': ['d0', 'q1']}
    rank = ranked(queries, docs, np.array([1]), docs[[1]], ids)
    np.testing.assert_array_equal(rank[0], np.arange(1, 101))
    np.testing.assert_array_equal(rank[1], np.arange(100))
    save(fixture / 'tied_ranking.npy', rank)
    np.testing.assert_array_equal(np.load(fixture / 'tied_ranking.npy', allow_pickle=False), rank)
    # The paired-only adapter must reject a request for other destination rows.
    guarded = PairedTargets(np.array([1]), docs[[1]])
    np.testing.assert_array_equal(guarded[np.array([1])], docs[[1]])
    try:
        guarded[np.array([0])]
    except ValueError:
        pass
    else:
        raise AssertionError('Paired target guard failed')
    checks = {'exact_ties_stable_original_order': True, 'identical_id_exclusion': True,
              'serialization': 'PASS', 'paired_target_guard': 'PASS', 'scorer_synthetic': synthetic_checks(),
              'b1c_scorer_synthetic': b1c_checks()}
    # Expected failures are receipts, never swallowed successful workers.
    exits = []
    tests = [('exit7', 'raise SystemExit(7)', 7)]
    if os.name != 'nt':
        tests.append(('sigterm', 'import os,signal;os.kill(os.getpid(),signal.SIGTERM)', -signal.SIGTERM))
    for name, script, code in tests:
        result = run_observed_child([sys.executable, '-c', script], os.environ.copy(), fixture / name)
        if result['returncode'] != code or result['status'] != 'EXITED':
            raise AssertionError('Observed failure receipt differs: ' + name)
        exits.append(result)
    checks['expected_failed_children'] = exits
    checks['whole_group_recovery'] = recovery_checks(fixture / 'recovery')
    write_json(fixture / 'checks.json', checks)
    return checks


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
            proxy, receipt = neural(lock, commit, out, 'synthetic', method, method, 17, oldpath, old, anchors, paired, 'smoke')
        _vectors('smoke proxy', proxy, dim=768)
        ranking = ranked(query, proxy, anchors, paired, ids)
        path = out / 'rankings' / ('synthetic_' + method + '.npy')
        save(path, ranking)
        np.testing.assert_array_equal(np.load(path, allow_pickle=False), ranking)
        records.append({'method': method, 'fit_receipt': receipt, 'ranking_sha256': sha256(path)})
    return {'fixtures': checks, 'methods': records, 'converter_selection_iterations': 500,
            'scientific_rankings_generated': 0, 'qrels_opened': False}


def ordered_groups(groups):
    def key(group):
        phase = 0 if group['dataset'] == 'FiQA' else (2 if group['method'] == CONVERTER else 1)
        return (phase, DATASETS.index(group['dataset']), PAIRS.index(group['pair']), group['seed'], METHODS.index(group['method']))
    return sorted(groups, key=key)


def full(lock, commit, out, metadata, registry, inputs, recovery=None):
    cells, fits, parity = import_groups(recovery, out) if recovery else ([], [], [])
    imported = set(recovery['group_ids']) if recovery else set()
    imported_counts = recovery['counts'] if recovery else {'groups': 0, 'rankings': 0, 'nano_fits': 0, 'fiqa_parity': 0}
    metadata['recovery_counts'] = {'imported': imported_counts, 'new_rankings': 320 - len(cells), 'new_nano_fits': 90 - imported_counts['nano_fits']}
    (out / 'groups').mkdir(exist_ok=True)
    write_json(out / 'cells_pre_qrels.json', cells)
    write_json(out / 'parity_receipts.json', parity)
    for index, group in enumerate(ordered_groups(registry['groups'])):
        dataset, pair, method, seed, regime = (group[k] for k in IDENTITY)
        gid = group['group_id']
        if gid in imported:
            continue
        folder = out / 'groups' / gid
        folder.mkdir()
        write_json(out / 'progress.json', {'stage': 'GROUP_START', 'group': gid, 'group_index': index,
                   'groups_total': 120, 'rankings_complete': len(cells), 'rankings_total': 320})
        oldpath = inputs.path(group['old_docs'])
        old = _vectors('old source documents', inputs.array(group['old_docs']), dim=384)
        queries = _vectors('destination queries', inputs.array(group['new_queries']), dim=768)
        copied = out / 'inputs' / dataset
        idpath = inputs.copy(group['ids'], copied / 'ids.json')
        ids = read_json(idpath)
        if len(ids['doc_ids']) != len(old) or len(ids['query_ids']) != len(queries) or len(set(ids['doc_ids'])) != len(old) or len(set(ids['query_ids'])) != len(queries):
            raise ValueError('ID/vector order population mismatch or duplicate IDs')
        anchorpath = inputs.copy(group['anchors'], copied / ('anchors_seed' + str(seed) + '.npy'))
        anchors = positions(np.load(anchorpath, allow_pickle=False), 'anchors', len(old), nonempty=True)
        if len(anchors) != 1024:
            raise ValueError('B1c fits must use exactly1024 ordered anchors')
        # This materializer is the sole full destination-cache consumer.
        target = inputs.array(group['full_target_reference'])
        if target.shape != (len(old), 768) or target.dtype != np.float32:
            raise ValueError('Destination reference row/dimension/dtype mismatch')
        began = time.perf_counter()
        paired = _vectors('paired target slices', np.asarray(target[anchors]), dim=768)
        paired_path = folder / (dataset + '_anchor_targets.npy')
        save(paired_path, paired)
        if dataset == 'FiQA':
            proxy_spec = {'kind': group['proxy']['kind'], 'file': {'path': str(inputs.path(group['proxy']['file'])), 'sha256': group['proxy']['file']['sha256']}}
            reconstruction_hashes = {}
            proxy = reconstruct_proxy(old, proxy_spec, method, reconstruction_hashes)
            receipt = {'status': 'HISTORICAL_FIT_REUSED', 'new_fit': False, 'fit_pairs': 1024,
                       'historical_fit_seconds': None, 'fit_seconds_semantics': 'historical fit is reused; null is not zero cost',
                       'reconstruction_seconds': time.perf_counter() - began, 'source_proxy': group['proxy'],
                       'reconstruction_input_hashes': reconstruction_hashes, 'new_physical_document_encodes': 0}
            if 'historical_fit_receipt' in group:
                original = inputs.path(group['historical_fit_receipt'])
                inputs.copy(group['historical_fit_receipt'], folder / 'historical_fit_receipt.json')
                receipt['historical_fit_receipt'] = read_json(original)
        elif method == LA2M:
            proxy, receipt = cpu_fit(LA2M, old, PairedTargets(anchors, paired), anchors, seed, out / 'cpu' / (dataset + '_' + gid))
            receipt.update(new_fit=True)
        else:
            proxy, receipt = neural(lock, commit, out, dataset, gid, method, seed, oldpath, old, anchors, paired, 'full', group['old_docs']['sha256'])
        proxy = _vectors('pristine proxy', proxy, dim=768)
        if len(proxy) != len(old):
            raise ValueError('Proxy population mismatch')
        receipt.update(group_id=gid, dataset=dataset, pair=pair, seed=seed, regime=regime, method=method,
                       paired_target_path=relative(out, paired_path), paired_target_sha256=sha256(paired_path),
                       shared_across_budgets=[c['budget'] for c in group['cases']])
        write_json(folder / 'fit_receipt.json', receipt)
        fits.append({'group_id': gid, 'path': relative(out, folder / 'fit_receipt.json'), 'sha256': sha256(folder / 'fit_receipt.json'), 'new_fit': dataset != 'FiQA'})
        # Existing50% output is a gate, never a newly counted scientific cell.
        cases = ([group['parity_case']] if dataset == 'FiQA' else []) + sorted(group['cases'], key=lambda c: c['budget'])
        for case in cases:
            budget = case['budget']
            paidpath = inputs.copy(case['paid'], copied / ('paid_seed' + str(seed) + '_' + budget + '.npy'))
            paid = positions(np.load(paidpath, allow_pickle=False), 'paid', len(old), nonempty=True)
            if not np.isin(anchors, paid).all():
                raise ValueError('Paid set omits anchors')
            if len(paid) != int(np.floor(int(budget.removesuffix('pct')) / 100 * len(old))):
                raise ValueError('Paid set does not charge exactly floor(budget * documents), anchors included')
            paid_targets = _vectors('gallery replacement slices', np.asarray(target[paid]), dim=768)
            started = time.perf_counter()
            ranking = ranked(queries, proxy, paid, paid_targets, ids)
            search_seconds = time.perf_counter() - started
            is_parity = dataset == 'FiQA' and case is group['parity_case']
            if is_parity:
                paritypath = folder / (dataset + '_parity_50pct.npy')
                save(paritypath, ranking)
                expected = inputs.array(case['published_ranking'])
                passed = np.array_equal(ranking, expected)
                parityrow = {'group_id': gid, 'case_id': case['case_id'], 'status': 'PASS' if passed else 'FAIL',
                             'ranking_path': relative(out, paritypath), 'ranking_sha256': sha256(paritypath),
                             'published_ranking': case['published_ranking'], 'search_seconds': search_seconds}
                parity.append(parityrow)
                write_json(out / 'parity_receipts.json', parity)
                if not passed:
                    same = ranking.shape == expected.shape
                    write_json(folder / 'parity_failure.json', {**parityrow, 'computed_shape': list(ranking.shape),
                               'expected_shape': list(expected.shape), 'changed_rank_positions': int(np.count_nonzero(ranking != expected)) if same else None,
                               'changed_query_rows': np.flatnonzero(np.any(ranking != expected, axis=1)).tolist() if same else None})
                    raise AssertionError('Historical FiQA50% parity failed: ' + gid)
                continue
            path = out / 'rankings' / (dataset + '_' + safe_id(case['case_id']) + '.npy')
            digest = save(path, ranking)
            np.testing.assert_array_equal(np.load(path, allow_pickle=False), ranking)
            cells.append({**{k: group[k] for k in IDENTITY}, 'group_id': gid, 'case_id': case['case_id'],
                          'budget': budget, 'ranking_path': relative(out, path), 'ranking_sha256': digest,
                          'fit_pairs': 1024, 'unique_destination_encodings': len(np.union1d(anchors, paid)),
                          'paid_count': len(paid), 'anchor_count': len(anchors), 'new_physical_document_encodes': 0,
                          'reused': False, 'fit_reused': dataset == 'FiQA', 'fit_receipt': fits[-1], 'search_seconds': search_seconds,
                          'ids_path': relative(out, idpath), 'ids_sha256': sha256(idpath),
                          'anchors_path': relative(out, anchorpath), 'anchors_sha256': sha256(anchorpath),
                          'paid_path': relative(out, paidpath), 'paid_sha256': sha256(paidpath)})
            write_json(out / 'cells_pre_qrels.json', cells)
            write_json(out / 'progress.json', {'stage': 'RANKING', 'group': gid, 'rankings_complete': len(cells), 'rankings_total': 320})
        del target, old, queries, proxy, paired
    if len(cells) != 320 or len(fits) != 120 or len(parity) != 30 or not all(p['status'] == 'PASS' for p in parity):
        raise AssertionError('Incomplete B1c endpoint/fit/parity accounting')
    sources = inputs.finish()
    write_json(out / 'input_hashes.json', sources)
    write_json(out / 'fit_receipts.json', fits)
    artifacts = {p.relative_to(out).as_posix(): sha256(p) for p in out.rglob('*')
                 if p.is_file() and p.relative_to(out).as_posix() not in ('metadata.json', 'progress.json', 'resource_trace.jsonl')}
    seal = {'status': 'RANKINGS_SEALED', 'scope': 'B1c missing320 inspected DEV endpoints only; STOP before D1 refresh/B2',
            'code_commit': commit, 'lock_sha256': metadata['lock_sha256'], 'registry_sha256': lock['registry']['sha256'],
            'existing_registry_sha256': lock['existing_cells']['sha256'], 'sealed_utc': datetime.now(timezone.utc).isoformat(),
            'cells': cells, 'fit_groups': fits, 'fiqa_50pct_parity': parity, 'source_inputs': sources,
            'inputs': {p.relative_to(out).as_posix(): sha256(p) for p in (out / 'inputs').rglob('*') if p.is_file()},
            'artifacts': artifacts, 'qrels_opened': False, 'ranking_process_qrel_reads': 0,
            'new_physical_document_encodes': 0, 'new_nano_fits': 90 - imported_counts['nano_fits'],
            'total_nano_fits': 90, 'historical_fiqa_fits_reused': 30,
            'recovery': metadata.get('recovery'), 'recovery_counts': metadata['recovery_counts'],
            'score_arithmetic': 'float32 query batch16 @ gallery.T; stable original row-order ties; identical ID exclusion'}
    write_json(out / 'ranking_seal.json', seal)
    metadata.update(status='B1C_RANKINGS_SEALED_STOP', ranking_count=320, ranking_seal_sha256=sha256(out / 'ranking_seal.json'),
                    new_nano_fits=90 - imported_counts['nano_fits'], total_nano_fits=90, historical_fiqa_fits_reused=30,
                    next_action='Separate DEV scoring after320 seal; refresh D1 then STOP. B2 is not authorized.')
    write_json(out / 'progress.json', {'stage': 'RANKINGS_SEALED_STOP', 'rankings_complete': 320, 'rankings_total': 320})


def main():
    global LOCKPATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=('smoke', 'full'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--smoke', type=Path)
    parser.add_argument('--lock', type=Path, default=LOCKPATH)
    parser.add_argument('--recovery', type=Path)
    args = parser.parse_args()
    LOCKPATH = args.lock.resolve(strict=True)
    out = args.output.resolve()
    if out.parent != (ROOT / 'results').resolve() or not out.name.startswith('b1c_'):
        raise ValueError('Output must be a unique results/b1c_* directory')
    out.mkdir(parents=False, exist_ok=False)
    started = time.perf_counter()
    metadata = {'status': 'RUNNING', 'stage': args.stage, 'code_commit': args.code_commit,
                'started_utc': datetime.now(timezone.utc).isoformat(), 'failures': [], 'qrels_opened': False,
                'ranking_process_qrel_reads': 0, 'TREC_access': False, 'new_physical_document_encodes': 0,
                'artificial_time_memory_caps': None}
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
        inputs = Inputs()
        registry = registry_for(lock, inputs)
        recovery = None
        if bool(args.recovery) != bool(lock.get('recovery_manifest')):
            raise ValueError('Recovery lock and --recovery must be supplied together')
        if args.recovery:
            require_tracked(args.recovery)
            recovery = verify_manifest(args.recovery, lock, inputs)
            metadata['recovery'] = {'manifest_sha256': sha256(args.recovery), 'manifest_path': str(args.recovery.resolve()),
                                    'source_run': recovery['source_run'], 'source_commit': recovery['source_commit'],
                                    'failure_evidence_retained_at_source': recovery['failure_evidence_retained_at_source'],
                                    'imported_cells_preserve_historical_fit_provenance': True}
            write_json(out / 'recovery_provenance.json', metadata['recovery'])
        metadata.update(registry_sha256=lock['registry']['sha256'], existing_registry_sha256=lock['existing_cells']['sha256'])
        if args.stage == 'smoke':
            metadata.update(smoke_checks=smoke(lock, args.code_commit, out), status='B1C_SMOKE_PASS')
            metadata['source_inputs'] = inputs.finish()
        else:
            if not args.smoke:
                raise ValueError('Full execution requires a successful matching committed smoke')
            smoke_meta = read_json(args.smoke / 'metadata.json')
            if smoke_meta['status'] != 'B1C_SMOKE_PASS' or any(smoke_meta[k] != metadata[k] for k in ('code_commit', 'lock_sha256', 'registry_sha256', 'existing_registry_sha256')):
                raise ValueError('Smoke identity does not match this full execution')
            if smoke_meta.get('recovery') != metadata.get('recovery'):
                raise ValueError('Smoke recovery identity does not match this full execution')
            metadata['smoke'] = {'path': str(args.smoke.resolve()), 'metadata_sha256': sha256(args.smoke / 'metadata.json')}
            full(lock, args.code_commit, out, metadata, registry, inputs, recovery)
    except BaseException as exc:
        metadata.update(status='FAILED_PRESERVED', failures=[repr(exc)], traceback=traceback.format_exc())
    finally:
        monitor.end()
        metadata.update(wall_seconds=time.perf_counter() - started, peak_process_tree_rss_bytes=monitor.peak,
                        ended_utc=datetime.now(timezone.utc).isoformat())
        write_json(out / 'metadata.json', metadata)
    print(json.dumps({'status': metadata['status'], 'failures': metadata['failures']}))
    return 0 if metadata['status'] in ('B1C_SMOKE_PASS', 'B1C_RANKINGS_SEALED_STOP') else 1


if __name__ == '__main__':
    raise SystemExit(main())
