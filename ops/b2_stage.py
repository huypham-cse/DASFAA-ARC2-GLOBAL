"""B2 TREC-COVID paired-anchor fits and reconstructable, qrel-free exact endpoints.

This driver deliberately has no scoring or label acquisition entry point.  The
independent verifier must replay the sealed endpoints before a scorer runs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'ops')]
from b1a_stage import Observations, dump, sha
from b1p_stage import (cpu_fit, check_identity, PROC, PRIMARY,
                       RIDGE, LA2M, SIMPLE, CONVERTER)
from arc2_global import normalize_rows, select_for_budget
from arc2_global.retrieval import exact_topk

METHODS = [PROC, RIDGE, PRIMARY, LA2M, SIMPLE, CONVERTER]
PAIRS = {'minilm_distilroberta': ('minilm_x', 'distilroberta_y'),
         'e5_small_base': ('e5_small_x', 'e5_base_y')}
SEEDS = [17, 29, 41, 53, 67]
BUDGETS = [25, 50, 75]
ENDPOINT_SCHEMA = 'b2_exact_endpoint_v1'
SEMANTICS = {'dtype': 'float32', 'score': 'dot', 'k': 100, 'batch_rows': 16,
             'tie_policy': 'descending score then ascending document row index',
             'exclude_identical_ids': True}


def save(path, array):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    np.save(path, array, allow_pickle=False)
    return sha(path)


def filespec(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': sha(path)}


def observed_child(argv, env, directory):
    """No caps/retries; terminate only our child when the owner is interrupted."""
    row = {'status': 'STARTING', 'argv': argv, 'started_utc': datetime.now(timezone.utc).isoformat()}
    path = directory / 'process_exit.json'
    process = None
    with (directory / 'stdout.log').open('x') as stdout, (directory / 'stderr.log').open('x') as stderr:
        try:
            process = subprocess.Popen(argv, env=env, stdout=stdout, stderr=stderr)
            row.update(status='RUNNING', pid=process.pid)
            dump(path, row)
            row['returncode'] = process.wait()
        except BaseException as exc:
            row.update(owner_interruption=repr(exc))
            if process is not None and process.poll() is None:
                process.terminate()
                row['returncode'] = process.wait()
            raise
        finally:
            code = row.get('returncode')
            row.update(status='EXITED' if code is not None else 'START_FAILED',
                       signal_number=-code if code is not None and code < 0 else None,
                       ended_utc=datetime.now(timezone.utc).isoformat())
            stdout.flush()
            stderr.flush()
            row.update(stdout_sha256=sha(directory / 'stdout.log'), stderr_sha256=sha(directory / 'stderr.log'))
            dump(path, row)
    return row


def prepare_selections(out, n_docs, seeds, anchor_count):
    """Preserve the DEV SeedSequence anchor/order streams and charged budgets."""
    result = {}
    for seed in seeds:
        anchors = np.random.default_rng(np.random.SeedSequence([seed, 0])).choice(
            n_docs, anchor_count, replace=False).astype(np.int64)
        order = np.random.default_rng(np.random.SeedSequence([seed, 1])).permutation(n_docs).astype(np.int64)
        anchor_path = out / 'inputs' / f'anchors_seed{seed}.npy'
        save(anchor_path, anchors)
        save(out / 'inputs' / f'order_seed{seed}.npy', order)
        paid = {}
        previous = set()
        for budget in BUDGETS:
            selected = select_for_budget(anchors, order, n_docs=n_docs, fraction=budget / 100)
            if not previous <= set(selected) or not set(anchors) <= set(selected):
                raise ValueError('Non-nested paid selections')
            previous = set(selected)
            path = out / 'inputs' / f'paid_seed{seed}_{budget}pct.npy'
            save(path, selected)
            paid[budget] = (selected, filespec(path))
        result[seed] = (anchors, filespec(anchor_path), paid)
    return result


def save_endpoint(path, *, kind, shape, ids, queries, native=None, proxy=None,
                  destination=None, paid=None, anchors=None):
    """Serialize file identities and the complete endpoint reconstruction rule."""
    if kind == 'native':
        if native is None or any(v is not None for v in [proxy, destination, paid, anchors]):
            raise ValueError('Invalid native descriptor')
        files = {'ids': ids, 'query_vectors': queries, 'native_vectors': native}
    elif kind == 'mixed':
        if native is not None or any(v is None for v in [proxy, destination, paid, anchors]):
            raise ValueError('Invalid mixed descriptor')
        files = {'ids': ids, 'query_vectors': queries, 'proxy_vectors': proxy,
                 'destination_vectors': destination, 'paid_indices': paid,
                 'anchor_indices': anchors}
    else:
        raise ValueError('Unknown endpoint kind')
    if path.exists():
        raise FileExistsError(path)
    dump(path, {'schema': ENDPOINT_SCHEMA, 'kind': kind, 'files': files,
                'shape': list(shape), 'semantics': SEMANTICS})
    return sha(path)


def validate_array(path, shape):
    array = np.load(path, mmap_mode='r', allow_pickle=False)
    if array.shape != shape or array.dtype != np.float32:
        raise ValueError(f'Vector shape/dtype mismatch: {path}')
    for start in range(0, len(array), 4096):
        block = array[start:start + 4096]
        if not np.isfinite(block).all() or not np.allclose(np.linalg.norm(block, axis=1), 1, atol=1e-4, rtol=0):
            raise ValueError(f'Invalid normalized vectors: {path}')
    return array


def validate_ids(ids):
    """Validate acquisition row identities without changing their pinned order."""
    for key in ['doc_ids', 'query_ids']:
        values = ids[key]
        if (not isinstance(values, list) or not values
                or any(not isinstance(value, str) or not value for value in values)
                or len(set(values)) != len(values)):
            raise ValueError('IDs must be nonempty unique strings in acquisition row order')
    return ids


def prepare_encoding(encoding, lockpath, commit):
    manifest_path = encoding / 'encoding_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest['status'] != 'ENCODING_PASS' or manifest['lock']['sha256'] != sha(lockpath):
        raise ValueError('Encoding manifest status/lock mismatch')
    if manifest['code_commit'] != commit:
        raise ValueError('Encoding commit mismatch')

    def checked(spec):
        path = Path(spec['path'])
        if not path.is_absolute():
            path = encoding / path
        if sha(path) != spec['sha256']:
            raise ValueError('Encoding input hash drift: ' + str(path))
        return filespec(path)

    ids_spec = checked(manifest['ids'])
    ids = validate_ids(json.loads(Path(ids_spec['path']).read_text(encoding='utf-8')))
    if len(ids['doc_ids']) != 171332 or len(ids['query_ids']) != 50:
        raise ValueError('TREC-COVID population differs from locked corpus')
    vectors = {}
    for label, dimension in [('minilm_x', 384), ('distilroberta_y', 768), ('e5_small_x', 384), ('e5_base_y', 768)]:
        vectors[label] = {}
        for role, rows in [('docs', 171332), ('queries', 50)]:
            spec = checked(manifest['models'][label]['outputs'][role])
            vectors[label][role] = (validate_array(spec['path'], (rows, dimension)), spec)
    return ids, ids_spec, vectors, filespec(manifest_path)


def neural_fit_artifacts(request_dir, method, receipt, request):
    """Bind actual trained parameter files and paired inputs to worker receipts."""
    worker = request_dir / 'worker'
    result = {'worker_metadata': filespec(worker / 'metadata.json'),
              'request': filespec(request_dir / 'request.json'),
              'process_exit': filespec(request_dir / 'process_exit.json')}
    names = ['refit_checkpoint.pt', 'refit_fit.json']
    if method == CONVERTER:
        names += ['selection_checkpoint.pt', 'selection_fit.json']
    for name in names:
        spec = filespec(worker / name)
        recorded = receipt['artifacts'].get(name)
        if (recorded is None or spec['sha256'] != recorded['sha256']
                or Path(spec['path']).stat().st_size != recorded['bytes']):
            raise ValueError('Neural parameter artifact differs from worker receipt: ' + name)
        result[name] = spec
    for role in ['paired_source', 'paired_target']:
        spec = filespec(request_dir / (role + '.npy'))
        if (spec['sha256'] != request['input_sha256'][role]
                or spec['sha256'] != receipt['inputs'][role]['sha256']):
            raise ValueError('Neural paired input differs from request/worker receipt: ' + role)
        result[role] = spec
    return result


def neural(lock, lockpath, commit, out, pair, seed, method, source_spec, old, anchors, target, mode):
    request_dir = out / 'neural' / f'{pair}_seed{seed}_{method}'
    request_dir.mkdir(parents=True, exist_ok=False)
    x = request_dir / 'paired_source.npy'
    y = request_dir / 'paired_target.npy'
    save(x, np.asarray(old[anchors]))
    save(y, np.asarray(target[anchors]))
    request = {'mode': mode, 'method': 'embedding_converter' if method == CONVERTER else 'simplelinear',
               'regime': 'anchors', 'seed': seed, 'lockpath': str(lockpath),
               'output': str(request_dir / 'worker'), 'paired_source': str(x), 'paired_target': str(y),
               'full_source': source_spec['path'], 'code_commit': commit,
               'input_sha256': {'paired_source': sha(x), 'paired_target': sha(y), 'full_source': source_spec['sha256']}}
    dump(request_dir / 'request.json', request)
    env = {**os.environ, **lock['environment'], 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1'}
    exit_record = observed_child([lock['gpu_python'], '-u', str(ROOT / 'ops/b1p_neural_worker.py'),
                                  '--request', str(request_dir / 'request.json')], env, request_dir)
    if exit_record['returncode']:
        raise RuntimeError(f'Neural worker failed; preserve {request_dir}: {exit_record}')
    receipt = json.loads((request_dir / 'worker/metadata.json').read_text())
    if receipt['status'] != 'B1P_NEURAL_' + mode.upper() + '_PASS':
        raise ValueError('Neural worker did not pass')
    receipt['fit_artifacts'] = neural_fit_artifacts(request_dir, method, receipt, request)
    path = request_dir / 'worker/proxy_full.npy'
    return validate_array(path, (len(old), 768)), filespec(path), receipt


def rank_all(lock, lockpath, commit, out, ids, ids_spec, vectors, seeds, anchor_count, mode):
    selections = prepare_selections(out, len(ids['doc_ids']), seeds, anchor_count)
    cells = []
    pairs = PAIRS if mode == 'full' else {'synthetic': ('minilm_x', 'distilroberta_y')}

    def rank(pair, seed, method, budget, query, gallery, endpoint_args, receipt=None, paid_count=0):
        key = f'{pair}_seed{seed}_{method}_{budget}'
        endpoint = out / 'endpoints' / (key + '.json')
        endpoint_hash = save_endpoint(endpoint, shape=gallery.shape, ids=ids_spec, **endpoint_args)
        began = time.perf_counter()
        ranking = exact_topk(query, gallery, **{k: SEMANTICS[k] for k in ['k', 'batch_rows', 'exclude_identical_ids']},
                             query_ids=ids['query_ids'], document_ids=ids['doc_ids'])
        seconds = time.perf_counter() - began
        path = out / 'rankings' / (key + '.npy')
        digest = save(path, ranking)
        cell = {'dataset': 'TREC-COVID' if mode == 'full' else 'synthetic', 'pair': pair, 'seed': seed,
                'method': method, 'budget': budget, 'regime': 'reference' if seed is None else 'fixed1024',
                'fit_pairs': 0 if seed is None else anchor_count, 'unique_destination_encodings': paid_count,
                'physical_destination_document_encodes_in_fit_or_rank': 0,
                'endpoint_path': endpoint.relative_to(out).as_posix(), 'endpoint_sha256': endpoint_hash,
                'ranking_path': path.relative_to(out).as_posix(), 'ranking_sha256': digest,
                'search_seconds': seconds, 'fit_receipt': receipt}
        cells.append(cell)
        dump(out / 'cells_pre_qrels.json', cells)
        dump(out / 'progress.json', {'stage': 'EXACT_RANKING', 'cells': len(cells), 'total': 184 if mode == 'full' else 20})

    for pair, (source, destination) in pairs.items():
        old, source_spec = vectors[source]['docs']
        target, target_spec = vectors[destination]['docs']
        query, query_spec = vectors[destination]['queries']
        oldquery, oldquery_spec = vectors[source]['queries']
        rank(pair, None, 'full_x', 'full', oldquery, old,
             {'kind': 'native', 'queries': oldquery_spec, 'native': source_spec}, paid_count=0)
        rank(pair, None, 'full_y', 'full', query, target,
             {'kind': 'native', 'queries': query_spec, 'native': target_spec}, paid_count=len(target))
        for seed in seeds:
            anchors, anchor_spec, paid_sets = selections[seed]
            for method in METHODS:
                dump(out / 'progress.json', {'stage': 'FIT', 'pair': pair, 'seed': seed, 'method': method, 'cells': len(cells)})
                if method in [SIMPLE, CONVERTER]:
                    proxy, proxy_spec, receipt = neural(lock, lockpath, commit, out, pair, seed, method,
                                                       source_spec, old, anchors, target, mode)
                else:
                    directory = out / 'cpu' / f'{pair}_seed{seed}_{method}'
                    proxy, receipt = cpu_fit(method, old, target, anchors, seed, directory)
                    save(directory / 'proxy_full.npy', proxy)
                    proxy_spec = filespec(directory / 'proxy_full.npy')
                    receipt['fit_artifacts'] = {name: filespec(directory / name)
                                                for name in ['parameters.npz', 'metadata.json']}
                receipt = {**receipt, 'fit_anchor_indices_sha256': anchor_spec['sha256'],
                           'proxy_sha256': proxy_spec['sha256'], 'reused_for_budgets': BUDGETS}
                for budget in BUDGETS:
                    paid, paid_spec = paid_sets[budget]
                    gallery = np.array(proxy, dtype=np.float32, copy=True)
                    gallery[paid] = target[paid]
                    rank(pair, seed, method, f'{budget}pct', query, gallery,
                         {'kind': 'mixed', 'queries': query_spec, 'proxy': proxy_spec,
                          'destination': target_spec, 'paid': paid_spec, 'anchors': anchor_spec}, receipt, len(paid))
                    del gallery
                del proxy
    expected = 184 if mode == 'full' else 20
    if len(cells) != expected:
        raise ValueError('Incomplete exact endpoint campaign')
    return cells


def synthetic_inputs(out):
    rng = np.random.default_rng(17)
    old = normalize_rows(rng.normal(size=(2048, 384)).astype(np.float32))
    target = normalize_rows((old @ rng.normal(size=(384, 768)).astype(np.float32) + .1).astype(np.float32))
    oldquery = normalize_rows(rng.normal(size=(8, 384)).astype(np.float32))
    query = normalize_rows(rng.normal(size=(8, 768)).astype(np.float32))
    ids = {'doc_ids': [f'd{i:05}' for i in range(2048)], 'query_ids': [f'q{i:05}' for i in range(8)]}
    path = out / 'inputs/ids.json'
    dump(path, ids)
    vectors = {}
    for label, docs, queries in [('minilm_x', old, oldquery), ('distilroberta_y', target, query)]:
        vectors[label] = {}
        for role, array in [('docs', docs), ('queries', queries)]:
            path = out / 'synthetic' / f'{label}_{role}.npy'
            save(path, array)
            vectors[label][role] = (array, filespec(path))
    return ids, filespec(out / 'inputs/ids.json'), vectors


def validate_lock(lock):
    if lock['stage'] != 'B2' or lock['seeds'] != SEEDS or lock['anchor_count'] != 1024:
        raise ValueError('B2 protocol identity mismatch')
    if lock['budgets'] != BUDGETS or lock['expected_rankings'] != 184:
        raise ValueError('B2 campaign dimensions differ')
    if lock['converter_config']['iterations'] != 50000 or lock['smoke_converter_iterations'] != 500:
        raise ValueError('Frozen converter iterations differ')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['smoke', 'full'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--lock', type=Path, required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--encoding', type=Path)
    parser.add_argument('--smoke', type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.parent != (ROOT / 'results').resolve() or not out.name.startswith('b2_'):
        raise ValueError('New B2 output must be directly under results/b2_*')
    out.mkdir(exist_ok=False)
    began = time.perf_counter()
    lockpath = args.lock.resolve(strict=True)
    monitor = Observations(out)
    monitor.begin()
    meta = {'status': 'RUNNING', 'stage': args.stage, 'code_commit': args.code_commit,
            'lock_sha256': sha(lockpath), 'started_utc': datetime.now(timezone.utc).isoformat(),
            'failures': [], 'qrels_opened': False, 'ranking_process_qrel_reads': 0,
            'artificial_time_memory_caps': None, 'new_physical_document_encodes': 0,
            'physical_cost_claim': False, 'search': 'exact only; no ANN measurement'}
    dump(out / 'metadata.json', meta)

    def interrupted(sig, frame):
        raise RuntimeError(f'Received signal {sig}')
    signal.signal(signal.SIGTERM, interrupted)
    try:
        lock = json.loads(lockpath.read_text(encoding='utf-8'))
        validate_lock(lock)
        check_identity(lock, args.code_commit)
        from threadpoolctl import threadpool_info
        blas = threadpool_info()
        numerical = [row for row in blas if row.get('internal_api') == 'openblas']
        if not numerical or not all(row.get('architecture') == 'Haswell' and row['num_threads'] == 4 for row in numerical):
            raise ValueError('Locked four-thread Haswell runtime differs')
        meta['runtime'] = {'python': sys.executable, 'blas': blas, 'cpu_environment': lock['cpu_environment']}
        if args.stage == 'smoke':
            ids, ids_spec, vectors = synthetic_inputs(out)
            cells = rank_all(lock, lockpath, args.code_commit, out, ids, ids_spec, vectors, [17], 128, 'smoke')
            meta.update(status='B2_SMOKE_PASS', ranking_count=len(cells))
        else:
            if args.smoke is None or args.encoding is None:
                raise ValueError('Full requires matching --smoke and --encoding')
            smoke = json.loads((args.smoke / 'metadata.json').read_text())
            if smoke['status'] != 'B2_SMOKE_PASS' or smoke['code_commit'] != args.code_commit or smoke['lock_sha256'] != meta['lock_sha256']:
                raise ValueError('Matching smoke required before full')
            if sha(args.smoke / 'ranking_seal.json') != smoke['ranking_seal_sha256']:
                raise ValueError('Matching smoke seal changed')
            ids, ids_spec, vectors, encoding_spec = prepare_encoding(args.encoding.resolve(), lockpath, args.code_commit)
            dump(out / 'inputs/ids.json', ids)
            # The descriptors point to this run's sealed ordered IDs.
            ids_spec = filespec(out / 'inputs/ids.json')
            cells = rank_all(lock, lockpath, args.code_commit, out, ids, ids_spec, vectors, SEEDS, 1024, 'full')
            meta['encoding_manifest'] = encoding_spec
        # Recheck every encoded input/proxy/selection and code before sealing.
        checked = {}
        fit_artifacts = {}
        for cell in cells:
            endpoint_path = out / cell['endpoint_path']
            if sha(endpoint_path) != cell['endpoint_sha256'] or sha(out / cell['ranking_path']) != cell['ranking_sha256']:
                raise ValueError('Endpoint/ranking changed before seal')
            descriptor = json.loads(endpoint_path.read_text())
            for spec in descriptor['files'].values():
                if spec['path'] not in checked:
                    checked[spec['path']] = sha(Path(spec['path']))
                if checked[spec['path']] != spec['sha256']:
                    raise ValueError('Endpoint dependency changed before seal')
            for spec in (cell.get('fit_receipt') or {}).get('fit_artifacts', {}).values():
                if spec['path'] not in fit_artifacts:
                    fit_artifacts[spec['path']] = sha(Path(spec['path']))
                if fit_artifacts[spec['path']] != spec['sha256']:
                    raise ValueError('Fit artifact changed before seal')
        check_identity(lock, args.code_commit)
        if sha(lockpath) != meta['lock_sha256']:
            raise ValueError('Lock changed during attempt')
        if meta.get('encoding_manifest') and sha(Path(meta['encoding_manifest']['path'])) != meta['encoding_manifest']['sha256']:
            raise ValueError('Encoding manifest changed before seal')
        seal = {'status': 'RANKINGS_SEALED', 'sealed_utc': datetime.now(timezone.utc).isoformat(),
                'code_commit': args.code_commit, 'lock_sha256': meta['lock_sha256'], 'mode': args.stage,
                'endpoint_schema': ENDPOINT_SCHEMA, 'cells': cells,
                'inputs': {p.relative_to(out).as_posix(): sha(p) for p in (out / 'inputs').rglob('*') if p.is_file()},
                'endpoint_dependency_sha256': checked, 'qrels_opened': False, 'ranking_process_qrel_reads': 0,
                'fit_artifact_sha256': fit_artifacts,
                'encoding_manifest': meta.get('encoding_manifest'), 'physical_cost_claim': False}
        dump(out / 'ranking_seal.json', seal)
        meta['ranking_seal_sha256'] = sha(out / 'ranking_seal.json')
        if args.stage == 'full':
            meta.update(status='B2_RANKINGS_SEALED_STOP', ranking_count=184,
                        next_action='Independent exact replay of all 184 endpoints before qrel scoring')
    except BaseException as exc:
        meta.update(status='FAILED_PRESERVED', failures=[repr(exc)], traceback=traceback.format_exc())
    finally:
        monitor.end()
        meta.update(wall_seconds=time.perf_counter() - began, peak_process_tree_rss_bytes=monitor.peak,
                    ended_utc=datetime.now(timezone.utc).isoformat())
        dump(out / 'metadata.json', meta)
    print(json.dumps({'status': meta['status'], 'failures': meta['failures']}))
    return 0 if meta['status'] in ['B2_SMOKE_PASS', 'B2_RANKINGS_SEALED_STOP'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
