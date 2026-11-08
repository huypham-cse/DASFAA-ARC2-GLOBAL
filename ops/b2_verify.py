"""B2 qrel-free independent endpoint verification. No label reader or scoring."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

import numpy as np

try:
    from b1m_score import inside, now, read_json, sha, write_json
    from b1c_r3_score import resources, save_npy
except ModuleNotFoundError:
    from ops.b1m_score import inside, now, read_json, sha, write_json
    from ops.b1c_r3_score import resources, save_npy

ROOT = Path(__file__).resolve().parents[1]
DATASET = 'TREC-COVID'
PAIRS = ('minilm_distilroberta', 'e5_small_base')
SEEDS = (17, 29, 41, 53, 67)
BUDGETS = ('25pct', '50pct', '75pct')
PRIMARY = 'arc2_global_tangent2_r1'
METHODS = ('procrustes_global', PRIMARY, 'la2m20_integration_script_adaptation',
           'simplelinear_official_final50_mlp5', 'ridge_affine_l10_bias_regularized',
           'embedding_converter_paper_spec')
KEY_FIELDS = ('dataset', 'pair', 'seed', 'budget', 'method')
SEMANTICS = {'dtype': 'float32', 'score': 'dot', 'k': 100, 'batch_rows': 16,
             'tie_policy': 'descending score then ascending document row index',
             'exclude_identical_ids': True}


def key(cell):
    return tuple(cell[field] for field in KEY_FIELDS)


def expected_keys():
    result = {(DATASET, p, s, b, m) for p, s, b, m in
              itertools.product(PAIRS, SEEDS, BUDGETS, METHODS)}
    result.update((DATASET, p, None, 'full', m) for p in PAIRS for m in ('full_x', 'full_y'))
    return result


def smoke_keys():
    result = {('synthetic', 'synthetic', 17, b, m) for b, m in itertools.product(BUDGETS, METHODS)}
    result.update(('synthetic', 'synthetic', None, 'full', m) for m in ('full_x', 'full_y'))
    return result


def check_matrix(cells):
    keys = [key(cell) for cell in cells]
    if len(keys) != 184 or len(set(keys)) != 184 or set(keys) != expected_keys():
        raise ValueError('Require complete unique B2 180 partial cells and 4 references')


def canonical_sha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def committed_context(lock_path):
    lock_path = Path(lock_path).resolve()
    lock = read_json(lock_path)
    sources = lock.get('source_sha256_canonical_lf', {})
    required = {'ops/b2_verify.py', 'ops/b2_score.py', 'ops/b2_stage.py',
                'ops/b1m_score.py', 'ops/b1c_r3_score.py'}
    if not required <= set(sources):
        raise ValueError('B2 lock must pin verifier, scorer, ranker and imported helpers')
    for path in [lock_path] + [inside(ROOT, relative) for relative in sources]:
        if not path.is_relative_to(ROOT):
            raise ValueError('Committed lock/source outside checkout')
        subprocess.check_output(['git', 'ls-files', '--error-unmatch', '--', path.relative_to(ROOT).as_posix()], cwd=ROOT)
    for relative, digest in sources.items():
        if canonical_sha(inside(ROOT, relative)) != digest:
            raise ValueError('Source drift: ' + relative)
    if subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip():
        raise ValueError('Dirty tracked B2 checkout')
    versions = lock['cpu_versions']
    import scipy
    if versions.get('numpy') != np.__version__ or versions.get('scipy') != scipy.__version__:
        raise ValueError('Unpinned CPU numerical versions')
    for name, value in lock.get('cpu_environment', {}).items():
        if os.environ.get(name) != str(value):
            raise ValueError('CPU environment drift: ' + name)
    return lock, subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()


def read_ids(path, expected_counts=(171332, 50)):
    ids = read_json(path)
    docs, queries = ids['doc_ids'], ids['query_ids']
    if not docs or not queries or any(not isinstance(x, str) or not x for x in docs + queries):
        raise ValueError('Require nonempty string IDs')
    if len(set(docs)) != len(docs) or len(set(queries)) != len(queries):
        raise ValueError('Duplicate document/query IDs')
    if expected_counts is not None and (len(docs), len(queries)) != expected_counts:
        raise ValueError('B2 corpus/query count drift')
    # Row order is pinned by acquisition/encoding; IDs must never be sorted.
    return docs, queries


def load_spec(spec):
    if not isinstance(spec, dict) or set(spec) != {'path', 'sha256'}:
        raise ValueError('Require exact path/SHA256 file specification')
    path = Path(spec['path'])
    if not path.is_absolute() or 'qrel' in str(path).lower():
        raise ValueError('Endpoint inputs must be absolute label-free paths')
    if sha(path) != spec['sha256']:
        raise ValueError('Endpoint source changed: ' + str(path))
    return path


def vectors(spec, shape=None):
    values = np.load(load_spec(spec), allow_pickle=False, mmap_mode='r')
    if values.ndim != 2 or values.dtype != np.dtype('float32') or not np.isfinite(values).all():
        raise ValueError('Require finite float32 matrix')
    if not np.allclose(np.linalg.norm(values, axis=1), 1.0, atol=1e-4, rtol=0):
        raise ValueError('Require normalized endpoint vectors')
    if shape is not None and values.shape != tuple(shape):
        raise ValueError('Vector shape drift')
    return values


def indices(spec, count):
    values = np.load(load_spec(spec), allow_pickle=False)
    if values.ndim != 1 or values.dtype.kind not in 'iu' or len(np.unique(values)) != len(values):
        raise ValueError('Require unique one-dimensional integer indices')
    if len(values) and (np.min(values) < 0 or np.max(values) >= count):
        raise ValueError('Document indices outside corpus')
    return values


def independent_exact(queries, gallery, docs, query_ids, k=100, batch_rows=16):
    """Independent implementation: full score rows, lexicographic total order."""
    if (queries.dtype != np.float32 or gallery.dtype != np.float32 or
            queries.ndim != 2 or gallery.ndim != 2 or queries.shape[1] != gallery.shape[1]
            or queries.shape[0] != len(query_ids) or gallery.shape[0] != len(docs)
            or not np.isfinite(queries).all() or not np.isfinite(gallery).all()):
        raise ValueError('Invalid endpoint matrices')
    rows = np.arange(len(docs), dtype=np.int64)
    doc_positions = {value: row for row, value in enumerate(docs)}
    result = np.empty((len(query_ids), k), dtype=np.int64)
    for start in range(0, len(queries), batch_rows):
        scores = queries[start:start + batch_rows] @ gallery.T
        if not np.isfinite(scores).all():
            raise ValueError('Nonfinite endpoint dot product')
        for offset, row in enumerate(scores):
            query_id = query_ids[start + offset]
            if query_id in doc_positions:
                row[doc_positions[query_id]] = -np.inf
            if np.isfinite(row).sum() < k:
                raise ValueError('Fewer than k eligible documents')
            result[start + offset] = np.lexsort((rows, -row))[:k]
    return result


def reload_endpoint(endpoint, expected_counts=(171332, 50)):
    if endpoint.get('schema') != 'b2_exact_endpoint_v1' or endpoint.get('semantics') != SEMANTICS:
        raise ValueError('Endpoint schema/search semantics drift')
    files = endpoint['files']
    docs, query_ids = read_ids(load_spec(files['ids']), expected_counts)
    shape = endpoint['shape']
    if len(shape) != 2 or shape[0] != len(docs):
        raise ValueError('Endpoint gallery shape differs from IDs')
    queries = vectors(files['query_vectors'], (len(query_ids), shape[1]))
    if endpoint['kind'] == 'native':
        if set(files) != {'ids', 'query_vectors', 'native_vectors'}:
            raise ValueError('Unexpected native endpoint inputs')
        gallery = vectors(files['native_vectors'], shape)
        paid, anchors = None, None
    elif endpoint['kind'] == 'mixed':
        if set(files) != {'ids', 'query_vectors', 'proxy_vectors', 'destination_vectors', 'paid_indices', 'anchor_indices'}:
            raise ValueError('Unexpected mixed endpoint inputs')
        gallery = np.array(vectors(files['proxy_vectors'], shape), copy=True)
        destination = vectors(files['destination_vectors'], shape)
        paid, anchors = indices(files['paid_indices'], len(docs)), indices(files['anchor_indices'], len(docs))
        if not set(anchors.tolist()) <= set(paid.tolist()):
            raise ValueError('Every anchor must count as a paid destination encoding')
        gallery[paid] = destination[paid]
    else:
        raise ValueError('Unsupported endpoint kind')
    return queries, gallery, docs, query_ids, paid, anchors


def verify_rank_array(path, digest, docs, queries):
    if sha(path) != digest:
        raise ValueError('Sealed ranking changed: ' + str(path))
    ranks = np.load(path, allow_pickle=False)
    if ranks.shape != (len(queries), 100) or ranks.dtype.kind not in 'iu':
        raise ValueError('Invalid integer top100 ranking matrix')
    if np.any(ranks < 0) or np.any(ranks >= len(docs)):
        raise ValueError('Ranking IDs outside corpus')
    if np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0):
        raise ValueError('Duplicate returned document IDs')
    for i, query in enumerate(queries):
        if query in {docs[int(row)] for row in ranks[i]}:
            raise ValueError('Identical query/document ID returned')
    return ranks


def encoding_output_spec(manifest_path, encoding, label, role, counts=(171332, 50)):
    """Validate the rich encoder record; return only its file identity."""
    spec = encoding['models'][label]['outputs'][role]
    if set(spec) != {'path', 'sha256', 'shape', 'dtype', 'journal_path', 'journal_sha256'}:
        raise ValueError('Unexpected encoding output metadata schema')
    dimension = {'minilm_x': 384, 'distilroberta_y': 768, 'e5_small_x': 384, 'e5_base_y': 768}[label]
    expected_shape = [counts[0] if role == 'docs' else counts[1], dimension]
    if role not in ('docs', 'queries') or spec['shape'] != expected_shape or spec['dtype'] != 'float32':
        raise ValueError('Encoding output shape/dtype/role drift')
    def resolved(value):
        path = Path(value)
        return path.resolve() if path.is_absolute() else (Path(manifest_path).parent / path).resolve()
    canonical = {'path': str(resolved(spec['path'])), 'sha256': spec['sha256']}
    path = load_spec(canonical)
    load_spec({'path': str(resolved(spec['journal_path'])), 'sha256': spec['journal_sha256']})
    header = np.load(path, allow_pickle=False, mmap_mode='r')
    if list(header.shape) != expected_shape or header.dtype != np.dtype('float32'):
        raise ValueError('Encoding output header differs from metadata')
    return canonical


def require_encoder_file(actual, expected, description):
    if actual != expected:
        raise ValueError(description)


def verify_fit_artifacts(seal):
    sealed = seal.get('fit_artifact_sha256', {})
    if not isinstance(sealed, dict) or not sealed:
        raise ValueError('Require nonempty sealed CPU and neural fit artifact map')
    for path, digest in sealed.items():
        load_spec({'path': path, 'sha256': digest})
    referenced = {}
    for cell in seal['cells']:
        receipt = cell.get('fit_receipt')
        if cell['budget'] == 'full':
            if receipt is not None:
                raise ValueError('Native reference cannot carry a fitted mapping')
            continue
        artifacts = (receipt or {}).get('fit_artifacts', {})
        if cell['method'] in ('simplelinear_official_final50_mlp5', 'embedding_converter_paper_spec'):
            required = {'worker_metadata', 'request', 'process_exit', 'refit_checkpoint.pt',
                        'refit_fit.json', 'paired_source', 'paired_target'}
            if cell['method'] == 'embedding_converter_paper_spec':
                required.update({'selection_checkpoint.pt', 'selection_fit.json'})
        else:
            required = {'parameters.npz', 'metadata.json'}
        if not required <= set(artifacts):
            raise ValueError('Missing required frozen fit parameters/receipts')
        for spec in artifacts.values():
            if not isinstance(spec, dict) or set(spec) != {'path', 'sha256'} or sealed.get(spec['path']) != spec['sha256']:
                raise ValueError('Fit artifact absent from sealed hash coverage')
            referenced[spec['path']] = spec['sha256']
    if referenced != sealed:
        raise ValueError('Sealed fit artifacts do not exactly cover declared cell fits')


def verify_seal(run, lock_sha=None, code_commit=None, *, smoke=False):
    run = Path(run).resolve()
    seal = read_json(run / 'ranking_seal.json')
    if seal.get('status') != 'RANKINGS_SEALED' or seal.get('mode') != ('smoke' if smoke else 'full'):
        raise ValueError('Require matching sealed B2 ranking mode')
    if seal.get('qrels_opened') is not False or seal.get('ranking_process_qrel_reads') != 0:
        raise ValueError('Ranking process label exposure is forbidden')
    if lock_sha is not None and seal.get('lock_sha256') != lock_sha:
        raise ValueError('Ranking lock differs from committed lock')
    if code_commit is not None and seal.get('code_commit') != code_commit:
        raise ValueError('Ranking code commit differs from verifier/scorer')
    if smoke:
        keys = [key(cell) for cell in seal['cells']]
        if len(keys) != 20 or len(set(keys)) != 20 or set(keys) != smoke_keys():
            raise ValueError('Require exact unique 20-cell synthetic smoke matrix')
    else:
        check_matrix(seal['cells'])
    verify_fit_artifacts(seal)
    counts = (2048, 8) if smoke else (171332, 50)
    inputs = seal.get('inputs', {})
    if not inputs:
        raise ValueError('Require hashed run inputs')
    for relative, digest in inputs.items():
        if 'qrel' in relative.lower() or sha(inside(run, relative)) != digest:
            raise ValueError('Unsealed or label-bearing input: ' + relative)
    if smoke:
        if seal.get('encoding_manifest') is not None:
            raise ValueError('Synthetic smoke cannot consume real encoding manifest')
    else:
        manifest_path = load_spec(seal['encoding_manifest'])
        encoding = read_json(manifest_path)
        if (encoding.get('status') != 'ENCODING_PASS'
                or (lock_sha is not None and encoding['lock']['sha256'] != lock_sha)
                or (code_commit is not None and encoding.get('code_commit') != code_commit)):
            raise ValueError('Encoding manifest lock/commit/status drift')
        encoding_ids_spec = dict(encoding['ids'])
        encoding_ids_path = Path(encoding_ids_spec['path'])
        if not encoding_ids_path.is_absolute():
            encoding_ids_path = (manifest_path.parent / encoding_ids_path).resolve()
        encoding_ids_spec['path'] = str(encoding_ids_path)
        encoding_ids = read_ids(load_spec(encoding_ids_spec), counts)
    dependencies = seal.get('endpoint_dependency_sha256', {})
    if not dependencies:
        raise ValueError('Require complete endpoint dependency hashes')
    for path, digest in dependencies.items():
        load_spec({'path': path, 'sha256': digest})
    encoded_cache = {}
    def encoded_spec(label, role):
        if smoke:
            path = (run / 'synthetic' / f'{label}_{role}.npy').resolve()
            return {'path': str(path), 'sha256': dependencies[str(path)]}
        if (label, role) not in encoded_cache:
            encoded_cache[label, role] = encoding_output_spec(manifest_path, encoding, label, role, counts)
        return encoded_cache[label, role]
    all_ids, seen_rankings, seen_endpoints = None, set(), set()
    for cell in seal['cells']:
        for field, seen in [('ranking_path', seen_rankings), ('endpoint_path', seen_endpoints)]:
            if cell[field] in seen:
                raise ValueError('Every cell requires unique ranking and descriptor paths')
            seen.add(cell[field])
            if sha(inside(run, cell[field])) != cell[field.replace('_path', '_sha256')]:
                raise ValueError('Cell artifact changed: ' + cell[field])
        endpoint = read_json(inside(run, cell['endpoint_path']))
        if endpoint.get('schema') != 'b2_exact_endpoint_v1' or endpoint.get('semantics') != SEMANTICS:
            raise ValueError('Endpoint schema/search semantics drift')
        files = endpoint['files']
        for spec in files.values():
            if dependencies.get(spec['path']) != spec['sha256']:
                raise ValueError('Endpoint input absent from dependency seal')
        source, target = {'synthetic': ('minilm_x', 'distilroberta_y'),
                          'minilm_distilroberta': ('minilm_x', 'distilroberta_y'),
                          'e5_small_base': ('e5_small_x', 'e5_base_y')}[cell['pair']]
        label = source if cell['method'] == 'full_x' else target
        require_encoder_file(files['query_vectors'], encoded_spec(label, 'queries'),
                             'Endpoint queries belong to another encoder/role')
        if cell['budget'] == 'full':
            if endpoint['kind'] != 'native' or files['native_vectors'] != encoded_spec(label, 'docs'):
                raise ValueError('Native reference does not use its named encoder')
            if cell['regime'] != 'reference' or cell['fit_pairs'] != 0 or cell['unique_destination_encodings'] != (0 if cell['method'] == 'full_x' else counts[0]):
                raise ValueError('Reference anchor/destination accounting drift')
        elif endpoint['kind'] != 'mixed' or files['destination_vectors'] != encoded_spec(target, 'docs'):
            raise ValueError('Mixed endpoint does not use the named destination encoder')
        elif cell['regime'] != 'fixed1024' or cell['fit_pairs'] != (128 if smoke else 1024):
            raise ValueError('Partial endpoint must use frozen fixed1024 regime')
        if cell['budget'] != 'full' and (cell['fit_receipt'].get('proxy_sha256') != files['proxy_vectors']['sha256']
                or cell['fit_receipt'].get('fit_anchor_indices_sha256') != files['anchor_indices']['sha256']):
            raise ValueError('Frozen fit receipt proxy/anchor binding drift')
        docs, queries = read_ids(load_spec(endpoint['files']['ids']), counts)
        if not smoke and (docs, queries) != encoding_ids:
            raise ValueError('Endpoint ordered IDs differ from encoded document/query rows')
        if all_ids is None:
            all_ids = (docs, queries)
        elif all_ids != (docs, queries):
            raise ValueError('All endpoints must share ordered corpus/query IDs')
        verify_rank_array(inside(run, cell['ranking_path']), cell['ranking_sha256'], docs, queries)
    return seal, all_ids


def run_verify(lock_path, run, *, smoke=False):
    run = Path(run).resolve()
    out = run / 'verification'
    out.mkdir(exist_ok=False)
    start = time.perf_counter()
    try:
        lock, commit = committed_context(lock_path)
        lock_sha = sha(lock_path)
        write_json(out / 'started.json', {'status': 'QREL_FREE_VERIFYING', 'started_utc': now(),
                   'code_commit': commit, 'lock_sha256': lock_sha, 'python': sys.version,
                   'numpy': np.__version__, 'platform': platform.platform(), 'qrels_opened': False})
        seal, ids = verify_seal(run, lock_sha, commit, smoke=smoke)
        seal_sha = sha(run / 'ranking_seal.json')
        records = []
        for number, cell in enumerate(seal['cells']):
            endpoint = read_json(inside(run, cell['endpoint_path']))
            queries, gallery, docs, query_ids, paid, anchors = reload_endpoint(endpoint, (2048, 8) if smoke else (171332, 50))
            if (cell['budget'] == 'full') != (endpoint['kind'] == 'native'):
                raise ValueError('Reference/mixed endpoint identity mismatch')
            if paid is not None and (cell['unique_destination_encodings'] != len(paid)
                                     or cell['fit_pairs'] != len(anchors) or len(anchors) != (128 if smoke else 1024)
                                     or len(paid) != int(len(docs) * int(cell['budget'][:-3]) / 100)):
                raise ValueError('Anchor/union destination accounting drift')
            if paid is not None:
                expected_anchors = np.random.default_rng(np.random.SeedSequence([cell['seed'], 0])).choice(len(docs), 128 if smoke else 1024, replace=False)
                order = np.random.default_rng(np.random.SeedSequence([cell['seed'], 1])).permutation(len(docs))
                selected = set(expected_anchors.tolist())
                for index in order:
                    if len(selected) == len(paid):
                        break
                    selected.add(int(index))
                if not np.array_equal(anchors, expected_anchors) or not np.array_equal(paid, np.array(sorted(selected), dtype=np.int64)):
                    raise ValueError('Frozen seed anchor/order paid selection drift')
            actual = independent_exact(queries, gallery, docs, query_ids)
            expected = verify_rank_array(inside(run, cell['ranking_path']), cell['ranking_sha256'], docs, query_ids)
            if not np.array_equal(actual, expected):
                save_npy(out / f'mismatch_{number:03d}_recomputed.npy', actual)
                mismatch = np.argwhere(actual != expected)
                write_json(out / f'mismatch_{number:03d}.json', {'cell': cell, 'unequal_positions': int(len(mismatch)),
                           'first_positions': mismatch[:100].tolist()})
                raise ValueError('Independent endpoint recomputation disagrees: ' + str(key(cell)))
            record = {field: cell[field] for field in KEY_FIELDS}
            record.update(endpoint_sha256=cell['endpoint_sha256'], ranking_sha256=cell['ranking_sha256'],
                          all_top100_ids_and_order_equal=True)
            write_json(out / f'cell_{number:03d}.json', record)
            records.append(record)
            del gallery, queries, actual, expected
        verify_seal(run, lock_sha, commit, smoke=smoke)
        committed_context(lock_path)
        if sha(run / 'ranking_seal.json') != seal_sha:
            raise ValueError('Ranking seal changed during verification')
        write_json(out / 'verification_seal.json', {'status': 'B2_ENDPOINT_SMOKE_PASS' if smoke else 'ENDPOINTS_INDEPENDENTLY_VERIFIED',
                   'completed_utc': now(), 'ranking_seal_sha256': seal_sha, 'lock_sha256': lock_sha,
                   'code_commit': commit, 'qrels_opened': False, 'verified_cells': records,
                   'verification': 'independent full float32 dot/lexsort; every ordered top100 ID equal',
                   'elapsed_seconds': time.perf_counter() - start, 'resources': resources(), 'failures': []})
    except BaseException as error:
        write_json(out / 'failure.json', {'status': 'FAILED_PRESERVED', 'failed_utc': now(),
                   'error': repr(error), 'traceback': traceback.format_exc(), 'qrels_opened': False,
                   'elapsed_seconds': time.perf_counter() - start, 'resources': resources()})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, default=Path('configs/b2_lock.json'))
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--smoke', action='store_true', help='Only the exact 20-cell synthetic smoke; cannot authorize final labels')
    args = parser.parse_args()
    run_verify(args.lock, args.run, smoke=args.smoke)
