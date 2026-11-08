"""CPU-only, qrel-free B1-G staging over already fitted galleries.

Only the materializer opens the full target reference: workers receive paid
slices or the fixed 512-document sample. No fit, encoder or label API is used.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'ops'))

from arc2_global.diagnostics import (sha256, write_json, save_array, safe_id,
    positions, paired_diagnostics, assert_cpu_only)
from b1a_stage import Observations

DATASETS = ('NanoNQ', 'NanoHotpotQA', 'NanoFEVER', 'FiQA')
IDENTITY = ('group_id', 'dataset', 'pair', 'method', 'seed', 'regime')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def file_spec(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': sha256(path)}


def checked_spec(spec):
    if not isinstance(spec, dict) or not {'path', 'sha256'} <= set(spec):
        raise ValueError('Invalid source file specification')
    path = Path(spec['path'])
    path = (path if path.is_absolute() else ROOT / path).resolve(strict=True)
    if sha256(path) != spec['sha256']:
        raise ValueError('Source hash drift: ' + str(path))
    return path


def inside(root, relative):
    root = Path(root).resolve()
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Sealed artifact path must be relative')
    path = (root / rel).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Sealed artifact escaped run')
    return path


def relative(root, path):
    return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()


def check_sources(lock, commit):
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip()
    if head != commit or dirty:
        raise ValueError('Require the committed deployment revision and clean tracked sources')
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0'))
    source_hashes = lock['source_sha256_canonical_lf']
    if not source_hashes:
        raise ValueError('Empty source lock')
    for name, expected in source_hashes.items():
        if name.replace('\\', '/') not in tracked:
            raise ValueError('Source is not committed: ' + name)
        path = ROOT / name
        actual = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        if actual != expected:
            raise ValueError('Canonical source drift: ' + name)
    assert_cpu_only()


def require_tracked(path):
    path = Path(path).resolve()
    name = path.relative_to(ROOT).as_posix()
    subprocess.run(['git', 'ls-files', '--error-unmatch', name], cwd=ROOT,
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def runtime(lock):
    import numpy as np
    import scipy
    from threadpoolctl import threadpool_info
    expected_env = lock['cpu_environment']
    if expected_env != {'OPENBLAS_CORETYPE': 'Haswell', 'OMP_NUM_THREADS': '4', 'OPENBLAS_NUM_THREADS': '4'}:
        raise ValueError('Unsupported numerical environment lock')
    if any(os.environ.get(key) != value for key, value in expected_env.items()):
        raise ValueError('BLAS/thread environment differs from lock')
    if Path(sys.executable).resolve() != Path(lock['cpu_python']).resolve():
        raise ValueError('CPU Python differs from lock')
    if {'numpy': np.__version__, 'scipy': scipy.__version__} != lock['cpu_versions']:
        raise ValueError('CPU numerical versions differ from lock')
    sklearn_version = importlib.metadata.version('scikit-learn')
    if sklearn_version != lock['cpu_sklearn_version']:
        raise ValueError('Saved LA2M routing requires the pinned sklearn version')
    # Force BLAS initialization, then observe actual configuration as well as env.
    np.ones((2, 2), dtype=np.float32) @ np.ones((2, 2), dtype=np.float32)
    pools = threadpool_info()
    blas = [pool for pool in pools if pool.get('user_api') == 'blas']
    if not blas or any(pool.get('num_threads') != 4 for pool in blas):
        raise ValueError('Require four actual BLAS threads')
    for pool in blas:
        if pool.get('internal_api') == 'openblas' and str(pool.get('architecture', '')).lower() != 'haswell':
            raise ValueError('Actual OpenBLAS core differs from Haswell')
    return {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
            'hostname': platform.node(), 'numpy': np.__version__, 'scipy': scipy.__version__,
            'sklearn': sklearn_version, 'environment': expected_env, 'threadpools': pools}


def source_inventory(registry):
    """Enumerate only the explicit qrel-free source fields, never lock qrels."""
    records = {}
    def add(spec):
        if not isinstance(spec, dict) or not {'path', 'sha256'} <= set(spec):
            raise ValueError('Missing locked source spec')
        key = str(spec['path'])
        digest = spec['sha256']
        if key in records and records[key] != digest:
            raise ValueError('Conflicting source hashes')
        records[key] = digest
    for group in registry['groups']:
        for key in ('old_docs', 'new_queries', 'full_target_reference', 'ids', 'anchors'):
            add(group[key])
        add(group['proxy']['file'])
        for case in group['cases']:
            add(case['paid'])
            add(case['published_ranking'])
    for spec in registry['contexts']:
        add(spec)
    return records


def registry_for(lock, shard):
    entry = lock['registries'][shard]
    path = checked_spec(entry)
    require_tracked(path)
    registry = read_json(path)
    groups = registry['groups']
    if registry['shard'] != shard or len(groups) != entry['groups'] or len(groups) != registry['expected_groups']:
        raise ValueError('Registry group count/shard differs from lock')
    gids, cases, keys, pure_keys = [], [], [], []
    for group in groups:
        gids.append(safe_id(group['group_id']))
        pure_keys.append(tuple(group[key] for key in IDENTITY[1:]))
        if group['dataset'] not in DATASETS or group['seed'] not in (17, 29, 41, 53, 67):
            raise ValueError('Registry scope is not locked DEV/seeds')
        if group['pair'] not in ('minilm_distilroberta', 'e5_small_base'):
            raise ValueError('Registry pair not in locked scope')
        if not group['cases']:
            raise ValueError('Empty gallery group')
        for case in group['cases']:
            cases.append(safe_id(case['case_id']))
            keys.append(tuple(group[k] for k in IDENTITY[1:]) + (str(case['budget']),))
    if len(set(gids)) != len(gids) or len(set(pure_keys)) != len(pure_keys) or len(set(cases)) != len(cases) or len(set(keys)) != len(keys):
        raise ValueError('Duplicate group, case or scientific identity')
    if len(cases) != entry['cases'] or len(cases) != registry['expected_cases']:
        raise ValueError('Registry case count differs from lock')
    source_inventory(registry)
    return registry, path


def verify_inventory(registry):
    inventory = source_inventory(registry)
    for path, digest in inventory.items():
        checked_spec({'path': path, 'sha256': digest})
    return inventory


def document_sample(ids, dataset, spec):
    import numpy as np
    docs = ids['doc_ids']
    if spec['algorithm'] != 'hash_id' or spec['size'] != 512:
        raise ValueError('Only the committed 512-document ID-hash sample is supported')
    if len(docs) < 512 or len(set(docs)) != len(docs):
        raise ValueError('Sample requires at least 512 unique documents')
    if any(not isinstance(doc, str) or not doc for doc in docs):
        raise ValueError('Invalid string document IDs')
    salted = [(hashlib.sha256((spec['salt'] + '\0' + dataset + '\0' + doc).encode('utf-8')).digest(), doc, i)
              for i, doc in enumerate(docs)]
    return np.asarray(sorted(row[2] for row in sorted(salted)[:spec['size']]), dtype=np.int64)


def copy_source(spec, folder, suffix=None):
    """Content addressed portable copy; the original identity stays in receipt."""
    source = Path(spec['path'])
    destination = folder / (spec['sha256'] + (suffix or source.suffix))
    if not destination.exists():
        shutil.copyfile(source, destination)
    if sha256(destination) != spec['sha256']:
        raise ValueError('Portable input copy differs from locked source')
    return file_spec(destination)


def worker(script, request, request_path, expected_status, expected_failure=False):
    write_json(request_path, request)
    with request_path.with_suffix('.stdout.log').open('x', encoding='utf-8') as stdout, request_path.with_suffix('.stderr.log').open('x', encoding='utf-8') as stderr:
        process = subprocess.Popen([sys.executable, '-u', str(ROOT / 'ops' / script), '--request', str(request_path)],
                                   stdout=stdout, stderr=stderr, env=os.environ.copy())
        try:
            returncode = process.wait()
        except BaseException:
            if process.poll() is None:
                process.terminate()
            process.wait()
            raise
    meta = read_json(Path(request['output']) / 'metadata.json')
    if expected_failure:
        if returncode == 0 or meta['status'] != expected_status:
            raise AssertionError('Intentional worker failure was not preserved')
    elif returncode != 0 or meta['status'] != expected_status:
        raise RuntimeError('Worker failed; preserve outputs: ' + str(request_path))
    return meta


def run_group(group, out, lock, cache):
    import numpy as np
    from arc2_global.numerics import _vectors
    gid = group['group_id']
    folder = out / 'groups' / gid
    folder.mkdir(parents=True)
    copied = out / 'inputs'
    ids_spec = copy_source(group['ids'], copied, '.json')
    ids = read_json(ids_spec['path'])
    if not {'doc_ids', 'query_ids'} <= set(ids) or len(set(ids['query_ids'])) != len(ids['query_ids']):
        raise ValueError('Missing or duplicate portable IDs')
    if any(not isinstance(q, str) or not q for q in ids['query_ids']):
        raise ValueError('Invalid query IDs')
    anchor_spec = copy_source(group['anchors'], copied, '.npy')
    n_docs = len(ids['doc_ids'])
    anchors = positions(np.load(anchor_spec['path'], allow_pickle=False), 'anchors', n_docs, nonempty=True)
    sample = document_sample(ids, group['dataset'], lock['sample'])
    sample_key = (group['dataset'], group['ids']['sha256'])
    # Equal dataset IDs/order are required across all pairs, seeds and regimes.
    doc_identity = hashlib.sha256(json.dumps(ids['doc_ids'], ensure_ascii=False).encode('utf-8')).hexdigest()
    if group['dataset'] in cache['dataset_ids'] and cache['dataset_ids'][group['dataset']] != doc_identity:
        raise ValueError('Dataset document row identity changed across groups')
    cache['dataset_ids'][group['dataset']] = doc_identity
    if sample_key not in cache['samples']:
        path = copied / ('sample_' + group['dataset'] + '_' + doc_identity[:16] + '.npy')
        if not path.exists():
            save_array(path, sample)
        cache['samples'][sample_key] = file_spec(path)
    sample_spec = cache['samples'][sample_key]
    # Read reference solely to materialize fixed sample and genuine paid rows.
    target = np.load(group['full_target_reference']['path'], mmap_mode='r', allow_pickle=False)
    if target.ndim != 2 or len(target) != n_docs:
        raise ValueError('Full reference/ID shape mismatch')
    sample_target_key = (group['dataset'], group['pair'], group['full_target_reference']['sha256'], sample_spec['sha256'])
    if sample_target_key not in cache['targets']:
        path = copied / ('target_sample_' + hashlib.sha256(repr(sample_target_key).encode()).hexdigest() + '.npy')
        save_array(path, _vectors('target sample', target[sample]))
        cache['targets'][sample_target_key] = file_spec(path)
    target_sample = cache['targets'][sample_target_key]
    cases = []
    portable_cases = []
    for case in group['cases']:
        paid_spec = copy_source(case['paid'], copied, '.npy')
        paid = positions(np.load(paid_spec['path'], allow_pickle=False), 'paid', n_docs)
        if not np.isin(anchors, paid).all():
            raise ValueError('Paid source omits anchors')
        paid_key = (group['dataset'], group['pair'], group['seed'], str(case['budget']),
                    group['full_target_reference']['sha256'], paid_spec['sha256'])
        if paid_key not in cache['paid']:
            tensor_cache = out / 'execution_paid_targets'
            tensor_cache.mkdir(exist_ok=True)
            path = tensor_cache / (hashlib.sha256(repr(paid_key).encode()).hexdigest() + '.npy')
            paid_target = _vectors('paid targets', target[paid])
            save_array(path, paid_target)
            cache['paid'][paid_key] = file_spec(path)
            cache.setdefault('paid_receipts', []).append({'path': relative(out, path), 'sha256': sha256(path),
                'shape': list(paid_target.shape), 'dtype': str(paid_target.dtype),
                'source_full_target': group['full_target_reference'], 'source_paid': case['paid'],
                'cache_key': list(paid_key), 'retained_in_remote_raw_run': True,
                'portable': False, 'scope': 'execution-only genuine paid target slices'})
            del paid_target
        cases.append({'case_id': case['case_id'], 'budget': case['budget'], 'paid': paid_spec,
                      'paid_targets': cache['paid'][paid_key], 'published_ranking': case['published_ranking']})
        portable_cases.append({'case_id': case['case_id'], 'budget': case['budget'],
            'paid': relative(out, paid_spec['path']), 'paid_sha256': paid_spec['sha256'],
            'paid_count': len(paid), 'after': relative(out, folder / 'rank' / 'cases' / case['case_id'] / 'after.npy'),
            'ranking_diagnostics': relative(out, folder / 'rank' / 'cases' / case['case_id'] / 'ranking_diagnostics.json'),
            'paired_diagnostics': relative(out, folder / 'analyzer' / 'cases' / case['case_id'] / 'paired_diagnostics.json')})
    del target
    rank_request = {key: group[key] for key in IDENTITY}
    rank_request.update(output=str(folder / 'rank'), old_docs=group['old_docs'], new_queries=group['new_queries'],
                        ids=ids_spec, sample_positions=sample_spec, anchors=anchor_spec, proxy=group['proxy'], cases=cases)
    worker('b1g_rank_worker.py', rank_request, folder / 'rank_request.json', 'B1G_RANK_PASS')
    analyzer_request = {key: group[key] for key in ('group_id', 'dataset', 'pair', 'seed', 'regime')}
    analyzer_request.update(output=str(folder / 'analyzer'), proxy_sample=file_spec(folder / 'rank' / 'sample_proxy.npy'),
        target_sample=target_sample, new_queries=group['new_queries'], sample_positions=sample_spec, anchors=anchor_spec,
        cases=[{'case_id': case['case_id'], 'paid': case['paid']} for case in cases])
    worker('b1g_analyze_worker.py', analyzer_request, folder / 'analyzer_request.json', 'B1G_ANALYZER_PASS')
    for portable, original in zip(portable_cases, group['cases']):
        portable['published_ranking_sha256'] = original['published_ranking']['sha256']
        portable['after_sha256'] = sha256(inside(out, portable['after']))
    return {**{key: group[key] for key in IDENTITY}, 'ids': relative(out, ids_spec['path']),
        'ids_sha256': ids_spec['sha256'], 'anchors': relative(out, anchor_spec['path']), 'anchors_sha256': anchor_spec['sha256'],
        'sample_positions': relative(out, sample_spec['path']), 'sample_sha256': sample_spec['sha256'],
        'before': relative(out, folder / 'rank' / 'before.npy'),
        'proxy_sample': relative(out, folder / 'rank' / 'sample_proxy.npy'),
        'target_sample': relative(out, target_sample['path']), 'anchor_count': len(anchors),
        'documents': n_docs, 'queries': len(ids['query_ids']), 'cases': portable_cases}


def synthetic_checks(out):
    """Qrel-free fixtures exercise subprocess isolation and retained failures."""
    import copy
    import numpy as np
    from arc2_global.numerics import normalize_rows
    from arc2_global.retrieval import exact_topk
    from b1m_score import synthetic_checks as metric_checks
    folder = out / 'fixtures'
    folder.mkdir()
    rng = np.random.default_rng(17)
    old = normalize_rows(rng.normal(size=(128, 4)).astype(np.float32))
    old[:4] = old[4]  # Exact ties must retain original row order.
    queries = old[[4, 7, 8]].copy()
    target = normalize_rows(old + np.array([.05, -.02, .03, 0], dtype=np.float32))
    anchors = np.array([1, 3], dtype=np.int64)
    paid = np.arange(64, dtype=np.int64)
    sample = np.arange(128, dtype=np.int64)
    ids = {'doc_ids': ['d' + str(i) for i in range(128)], 'query_ids': ['d0', 'q1', 'q2']}
    paths = {}
    for name, value in [('old', old), ('queries', queries), ('target_sample', target), ('anchors', anchors),
                        ('paid', paid), ('sample', sample), ('paid_targets', target[paid])]:
        path = folder / (name + '.npy')
        save_array(path, value)
        paths[name] = file_spec(path)
    write_json(folder / 'ids.json', ids)
    paths['ids'] = file_spec(folder / 'ids.json')
    coefficient = np.concatenate([np.eye(4, dtype=np.float32), np.zeros((1, 4), dtype=np.float32)])
    zero = np.zeros((1, 4), dtype=np.float32)
    eye = np.eye(4, dtype=np.float32)
    with (folder / 'b1m.npz').open('xb') as stream:
        np.savez(stream, procrustes_source_mean=zero, procrustes_target_mean=zero, procrustes_matrix=eye,
                 frozen_two=coefficient, ridge_affine_l10_bias_regularized=coefficient)
    with (folder / 'b1p.npz').open('xb') as stream:
        np.savez(stream, source_mean=zero, target_mean=zero, matrix=eye, two=coefficient, coefficient=coefficient,
                 centroids=old[[4, 11]], global_source_mean=zero, global_target_mean=zero, global_matrix=eye,
                 cluster0_source_mean=zero, cluster0_target_mean=zero, cluster0_matrix=eye)
    from b1g_rank_worker import reconstruct_proxy, PROC, PRIMARY, RIDGE, LA2M
    results = []
    modes = [('saved_npy', PROC, paths['old'])]
    modes += [('b1m_parameters', method, file_spec(folder / 'b1m.npz')) for method in (PROC, PRIMARY, RIDGE)]
    modes += [('b1p_parameters', method, file_spec(folder / 'b1p.npz')) for method in (PROC, PRIMARY, RIDGE, LA2M)]
    base_request = None
    for index, (kind, method, proxy_file) in enumerate(modes):
        proxy_spec = {'kind': kind, 'file': proxy_file}
        proxy = reconstruct_proxy(old, proxy_spec, method, {})
        gallery = proxy.copy()
        gallery[paid] = target[paid]
        expected = exact_topk(queries, gallery, query_ids=ids['query_ids'], document_ids=ids['doc_ids'], exclude_identical_ids=True)
        published = folder / ('published_' + str(index) + '.npy')
        save_array(published, expected)
        request = {'output': str(folder / ('rank_' + str(index))), 'group_id': 'fixture_' + str(index),
            'method': method, 'dataset': 'synthetic', 'pair': 'synthetic', 'seed': 17, 'regime': 'fixture',
            'old_docs': paths['old'], 'new_queries': paths['queries'], 'ids': paths['ids'],
            'sample_positions': paths['sample'], 'anchors': paths['anchors'], 'proxy': proxy_spec,
            'cases': [{'case_id': 'fixture_case', 'budget': '50pct', 'paid': paths['paid'],
                       'paid_targets': paths['paid_targets'], 'published_ranking': file_spec(published)}]}
        worker('b1g_rank_worker.py', request, folder / ('request_' + str(index) + '.json'), 'B1G_RANK_PASS')
        results.append({'kind': kind, 'method': method, 'status': 'PASS'})
        if base_request is None:
            base_request = request
    # Separate exact tie/exclusion fixture with analytically known order.
    docs = np.array([[1, 0], [1, 0], [0, 1], [-1, 0]], dtype=np.float32)
    tie = exact_topk(docs[:1], docs, k=3, query_ids=['a'], document_ids=['a', 'b', 'c', 'd'], exclude_identical_ids=True)
    np.testing.assert_array_equal(tie, [[1, 2, 3]])
    analyzer = {'output': str(folder / 'analyzer'), 'group_id': 'fixture',
        'proxy_sample': file_spec(Path(base_request['output']) / 'sample_proxy.npy'),
        'target_sample': paths['target_sample'], 'new_queries': paths['queries'],
        'sample_positions': paths['sample'], 'anchors': paths['anchors'],
        'cases': [{'case_id': 'fixture_case', 'paid': paths['paid']}]}
    worker('b1g_analyze_worker.py', analyzer, folder / 'analyzer_request.json', 'B1G_ANALYZER_PASS')
    p, t = np.eye(2, dtype=np.float32), np.flip(np.eye(2, dtype=np.float32), axis=0).copy()
    known = paired_diagnostics(np.array([[1, 0]], dtype=np.float32), np.array([[0, 1]], dtype=np.float32),
                               p, t, np.array([0, 1]), np.array([0]), np.array([0]))
    stats = known['strata']['all']
    np.testing.assert_allclose([stats['signed_bias'], stats['mae'], stats['rmse']], [0, 1, 1], rtol=0, atol=0)
    bad_ranks = np.load(base_request['cases'][0]['published_ranking']['path'], allow_pickle=False).copy()
    bad_ranks[0, [0, 1]] = bad_ranks[0, [1, 0]]
    save_array(folder / 'wrong_published.npy', bad_ranks)
    wrong = copy.deepcopy(base_request)
    wrong['output'] = str(folder / 'intentional_wrong_ranking')
    wrong['cases'][0]['published_ranking'] = file_spec(folder / 'wrong_published.npy')
    worker('b1g_rank_worker.py', wrong, folder / 'wrong_ranking_request.json', 'B1G_RANK_FAIL', expected_failure=True)
    if not (folder / 'intentional_wrong_ranking/cases/fixture_case/parity_failure.json').exists():
        raise AssertionError('Missing retained ranking parity evidence')
    forbidden = copy.deepcopy(base_request)
    forbidden.update(output=str(folder / 'intentional_forbidden_reference'), full_target_reference=paths['target_sample'])
    worker('b1g_rank_worker.py', forbidden, folder / 'forbidden_request.json', 'B1G_RANK_FAIL', expected_failure=True)
    report = {'status': 'PASS', 'proxy_modes': results, 'exact_ties_and_identical_id_exclusion': True,
        'paired_known_bias_mae_rmse': [0, 1, 1], 'intentional_wrong_ranking_rejected': True,
        'full_target_worker_request_rejected': True, 'synthetic_metric_checks': metric_checks(),
        'real_qrels_read': False, 'scientific_galleries_read': False, 'new_fits': 0}
    write_json(out / 'synthetic_checks.json', report)
    return report


def artifact_hashes(out):
    excluded = {'metadata.json', 'progress.json', 'resource_trace.jsonl', 'diagnostics_seal.json'}
    return {relative(out, path): sha256(path) for path in sorted(out.rglob('*'))
            if path.is_file() and relative(out, path) not in excluded
            and not relative(out, path).startswith('execution_paid_targets/')}


def require_smoke(path, commit, lock_sha, shard, registry_sha):
    meta = read_json(Path(path) / 'metadata.json')
    if (meta.get('status'), meta.get('stage'), meta.get('code_commit'), meta.get('lock_sha256'),
        meta.get('shard'), meta.get('registry_sha256')) != ('B1G_SMOKE_PASS', 'smoke', commit, lock_sha, shard, registry_sha):
        raise ValueError('Full requires a completed smoke for this exact commit/lock/shard/registry')
    if sha256(Path(path) / 'synthetic_checks.json') != meta['synthetic_checks_sha256']:
        raise ValueError('Smoke fixture receipt changed')
    for rel, digest in meta['smoke_artifact_sha256'].items():
        if sha256(inside(path, rel)) != digest:
            raise ValueError('Smoke artifact changed: ' + rel)


def run(args):
    out = Path(args.output).resolve()
    if out.parent != (ROOT / 'results').resolve() or not out.name.startswith('b1g_'):
        raise ValueError('Require a new direct results/b1g_* output directory')
    out.mkdir(parents=True, exist_ok=False)
    lock_path = Path(args.lock).resolve()
    began = time.perf_counter()
    metadata = {'status': 'RUNNING', 'stage': args.stage, 'shard': args.shard, 'code_commit': args.code_commit,
        'lock_sha256': sha256(lock_path), 'started_unix': time.time(), 'qrels_read': False,
        'new_fits': 0, 'new_physical_document_encodes': 0, 'artificial_time_or_memory_caps': None, 'failures': []}
    write_json(out / 'metadata.json', metadata)
    monitor = Observations(out)
    monitor.begin()
    def terminated(signum, frame):
        raise InterruptedError('Received signal ' + str(signum))
    previous = signal.signal(signal.SIGTERM, terminated)
    try:
        lock = read_json(lock_path)
        require_tracked(lock_path)
        check_sources(lock, args.code_commit)
        metadata['runtime'] = runtime(lock)
        registry, registry_path = registry_for(lock, args.shard)
        metadata['registry_sha256'] = sha256(registry_path)
        if args.stage == 'smoke':
            synthetic_checks(out)
            check_sources(lock, args.code_commit)
            checked_spec(lock['registries'][args.shard])
            metadata.update(status='B1G_SMOKE_PASS', synthetic_checks_sha256=sha256(out / 'synthetic_checks.json'),
                            smoke_artifact_sha256=artifact_hashes(out))
        else:
            if not args.smoke:
                raise ValueError('Full requires --smoke from this shard')
            require_smoke(args.smoke, args.code_commit, metadata['lock_sha256'], args.shard, metadata['registry_sha256'])
            inventory = verify_inventory(registry)
            (out / 'inputs').mkdir()
            (out / 'groups').mkdir()
            (out / 'contexts').mkdir()
            shutil.copyfile(registry_path, out / 'source_registry.json')
            shutil.copyfile(lock_path, out / 'source_lock.json')
            contexts = []
            for spec in registry['contexts']:
                copied = copy_source(spec, out / 'contexts')
                contexts.append({'source': spec, 'copied_path': relative(out, copied['path']), 'sha256': copied['sha256']})
            completed, count = [], 0
            cache = {'samples': {}, 'targets': {}, 'paid': {}, 'dataset_ids': {}}
            for group in registry['groups']:
                completed.append(run_group(group, out, lock, cache))
                count += len(group['cases'])
                write_json(out / 'progress.json', {'status': 'RUNNING', 'groups_passed': len(completed),
                    'cases_passed': count, 'expected_groups': registry['expected_groups'],
                    'expected_cases': registry['expected_cases'], 'updated_unix': time.time()})
            if len(completed) != registry['expected_groups'] or count != registry['expected_cases']:
                raise ValueError('Incomplete B1-G matrix; no seal permitted')
            check_sources(lock, args.code_commit)
            checked_spec(lock['registries'][args.shard])
            verify_inventory(registry)
            if sha256(lock_path) != metadata['lock_sha256']:
                raise ValueError('Lock changed while running')
            assert_cpu_only()
            for intermediate in cache['paid'].values():
                checked_spec(intermediate)
            write_json(out / 'execution_intermediates.json', {'excluded_prefix': 'execution_paid_targets/',
                'retention': 'preserved in raw shard run; optional omission from compact scorer export',
                'files': cache.get('paid_receipts', [])})
            seal = {'status': 'B1G_DIAGNOSTICS_SEALED', 'shard': args.shard, 'code_commit': args.code_commit,
                'lock_sha256': metadata['lock_sha256'], 'registry_sha256': metadata['registry_sha256'],
                'sealed_unix': time.time(), 'groups': completed, 'expected_groups': registry['expected_groups'],
                'expected_cases': registry['expected_cases'], 'source_inventory': inventory, 'contexts': contexts,
                'qrels_read': False, 'new_fits': 0, 'new_physical_document_encodes': 0,
                'reference_access': 'materializer only: paid slices plus fixed document sample; never full target rank API',
                'portable_excluded_prefix': 'execution_paid_targets/',
                'execution_intermediates': cache.get('paid_receipts', []),
                'artifact_sha256': artifact_hashes(out)}
            write_json(out / 'diagnostics_seal.json', seal)
            metadata.update(status='B1G_FULL_PASS', groups_passed=len(completed), cases_passed=count,
                            diagnostics_seal_sha256=sha256(out / 'diagnostics_seal.json'))
            write_json(out / 'progress.json', {'status': 'B1G_FULL_PASS', 'groups_passed': len(completed),
                'cases_passed': count, 'updated_unix': time.time()})
    except BaseException as exc:
        metadata.update(status='FAILED_PRESERVED', traceback=traceback.format_exc())
        metadata['failures'].append({'type': type(exc).__name__, 'message': str(exc)})
        (out / 'failure_traceback.txt').write_text(metadata['traceback'], encoding='utf-8')
    finally:
        signal.signal(signal.SIGTERM, previous)
        monitor.end()
        metadata.update(ended_unix=time.time(), wall_seconds=time.perf_counter() - began,
                        peak_process_tree_rss_bytes=monitor.peak)
        write_json(out / 'metadata.json', metadata)
    print(json.dumps({'status': metadata['status'], 'output': str(out), 'failures': metadata['failures']}))
    return 0 if metadata['status'] in ('B1G_SMOKE_PASS', 'B1G_FULL_PASS') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=('smoke', 'full'), required=True)
    parser.add_argument('--shard', choices=('main', 'mini'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--smoke', type=Path)
    parser.add_argument('--lock', type=Path, default=ROOT / 'configs/b1g_lock.json')
    return run(parser.parse_args())


if __name__ == '__main__':
    raise SystemExit(main())
