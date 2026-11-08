"""Descriptive B1-G diagnostics; no fitting, scoring labels or calibration."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import signal
import sys
import time
import traceback

import numpy as np

QUANTILES = [.01, .05, .25, .5, .75, .95, .99]
STRATA = ('all', 'anchor', 'paid_nonanchor', 'unpaid')


def whitelist(value, required, optional=()):
    if not isinstance(value, dict):
        raise ValueError('Expected JSON object')
    missing = set(required) - set(value)
    extra = set(value) - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f'Request keys: missing={sorted(missing)}, extra={sorted(extra)}')


def safe_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', value):
        raise ValueError('Invalid group/case identifier')
    return value


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def verified_path(spec, hashes):
    whitelist(spec, ('path', 'sha256'))
    if not isinstance(spec['path'], str) or not isinstance(spec['sha256'], str):
        raise ValueError('Invalid file specification')
    if not re.fullmatch('[0-9a-f]{64}', spec['sha256']):
        raise ValueError('Invalid SHA256')
    path = Path(spec['path']).resolve(strict=True)
    actual = sha256(path)
    if actual != spec['sha256']:
        raise ValueError(f'Input hash mismatch: {path}')
    hashes[str(path)] = actual
    return path


def load_array(spec, hashes):
    return np.load(verified_path(spec, hashes), allow_pickle=False)


def positions(value, name, n_docs=None, nonempty=False):
    a = np.asarray(value)
    if a.ndim != 1 or not np.issubdtype(a.dtype, np.integer):
        raise ValueError(f'{name}: expected integer positions')
    if (nonempty and not len(a)) or len(a) != len(np.unique(a)) or np.any(a < 0):
        raise ValueError(f'{name}: empty, duplicate or negative positions')
    if n_docs is not None and np.any(a >= n_docs):
        raise ValueError(f'{name}: out-of-range positions')
    return a.astype(np.int64, copy=False)


def write_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def save_array(path, value):
    with Path(path).open('xb') as stream:
        np.save(stream, value, allow_pickle=False)
        stream.flush()
        os.fsync(stream.fileno())


def assert_cpu_only():
    if any(name.split('.')[0] in ('torch', 'transformers', 'sentence_transformers') for name in sys.modules):
        raise RuntimeError('B1-G workers forbid Torch/Transformers imports')


def peak_rss_bytes():
    try:
        import resource
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(value if sys.platform == 'darwin' else value * 1024)
    except ImportError:
        try:
            import psutil
            info = psutil.Process().memory_info()
            return int(getattr(info, 'peak_wset', info.rss))
        except ImportError:
            return None


def run_worker(request_path, pass_status, operation):
    """Exclusive output, durable partial failure receipt, SIGTERM preservation."""
    request_path = Path(request_path)
    request = json.loads(request_path.read_text(encoding='utf-8-sig'))
    if not isinstance(request, dict) or not isinstance(request.get('output'), str):
        raise ValueError('Request must identify an output directory')
    out = Path(request['output'])
    out.mkdir(parents=True, exist_ok=False)
    began = time.perf_counter()
    metadata = {'status': 'B1G_STARTED', 'request_sha256': sha256(request_path),
                'group_id': request.get('group_id'), 'input_hashes': {}, 'failures': [],
                'new_physical_document_encodes': 0, 'new_fits': 0,
                'qrels_read': False, 'artificial_time_or_memory_caps': None,
                'pid': os.getpid(), 'python': sys.version, 'numpy': np.__version__,
                'started_unix': time.time()}
    write_json(out / 'metadata.json', metadata)
    def terminated(signum, frame):
        raise InterruptedError(f'Received signal {signal.Signals(signum).name}')
    previous = signal.signal(signal.SIGTERM, terminated)
    try:
        assert_cpu_only()
        operation(request, out, metadata)
        assert_cpu_only()
        metadata['status'] = pass_status
    except BaseException as exc:
        metadata['status'] = pass_status.replace('_PASS', '_FAIL')
        metadata['failures'].append({'type': type(exc).__name__, 'message': str(exc)})
        trace = traceback.format_exc()
        with (out / 'failure_traceback.txt').open('x', encoding='utf-8') as stream:
            stream.write(trace)
            stream.flush()
            os.fsync(stream.fileno())
        raise
    finally:
        signal.signal(signal.SIGTERM, previous)
        metadata.update(wall_seconds=time.perf_counter() - began,
                        peak_process_rss_bytes=peak_rss_bytes(), ended_unix=time.time())
        write_json(out / 'metadata.json', metadata)


def summary(values):
    a = np.asarray(values, dtype=np.float64).ravel()
    if not len(a):
        return {'count': 0, 'mean': None, 'std': None, 'min': None, 'max': None,
                'quantiles': {str(q): None for q in QUANTILES}}
    if not np.isfinite(a).all():
        raise ValueError('Nonfinite diagnostic values')
    return {'count': int(len(a)), 'mean': float(a.mean()), 'std': float(a.std(ddof=0)),
            'min': float(a.min()), 'max': float(a.max()),
            'quantiles': dict(zip(map(str, QUANTILES), map(float, np.quantile(a, QUANTILES))))}


def membership_masks(rows, anchors, paid):
    anchor = np.isin(rows, anchors)
    is_paid = np.isin(rows, paid)
    if np.any(anchor & ~is_paid):
        raise ValueError('Paid positions must include all anchors')
    return {'all': np.ones(np.asarray(rows).shape, dtype=bool), 'anchor': anchor,
            'paid_nonanchor': is_paid & ~anchor, 'unpaid': ~is_paid}


def ranking_diagnostics(before, after, *, n_docs, anchors, paid):
    before = np.asarray(before)
    after = np.asarray(after)
    if before.shape != after.shape or before.ndim != 2 or before.shape[1] < 100:
        raise ValueError('Expected paired top-100 rankings')
    counts = {'total_documents': int(n_docs), 'anchors': int(len(anchors)),
              'paid': int(len(paid)), 'paid_nonanchors': int(len(paid) - len(anchors)),
              'unpaid': int(n_docs - len(paid))}
    result = {'counts': counts, 'population_fractions': {
        'anchor': len(anchors) / n_docs, 'paid': len(paid) / n_docs,
        'paid_nonanchor': (len(paid) - len(anchors)) / n_docs,
        'unpaid': (n_docs - len(paid)) / n_docs}, 'before': {}, 'after': {}, 'changes': {}}
    for k in (10, 100):
        key = f'top{k}'
        for endpoint, ranking in [('before', before), ('after', after)]:
            masks = membership_masks(ranking[:, :k], anchors, paid)
            shares = {s: masks[s].mean(axis=1) for s in STRATA if s != 'all'}
            shares['paid'] = shares['anchor'] + shares['paid_nonanchor']
            result[endpoint][key] = {s: {'per_query': a.tolist(), 'mean': float(a.mean())}
                                      for s, a in shares.items()}
        overlap = np.asarray([len(set(a) & set(b)) / k for a, b in zip(before[:, :k], after[:, :k])])
        result['changes'][key] = {'intersection_over_k_per_query': overlap.tolist(),
                                  'mean_intersection_over_k': float(overlap.mean()),
                                  'changed_order_query_count': int(np.any(before[:, :k] != after[:, :k], axis=1).sum()),
                                  'changed_membership_query_count': int(np.count_nonzero(overlap < 1))}
    return result


def direction_diagnostics(vectors):
    a = np.asarray(vectors, dtype=np.float64)
    a = a / np.linalg.norm(a, axis=1, keepdims=True)
    norm = float(np.linalg.norm(a.mean(axis=0)))
    n = len(a)
    return {'documents': n, 'mean_direction_norm': norm,
            'mean_offdiagonal_cosine': float((n * norm * norm - 1) / (n - 1)) if n > 1 else None,
            'arithmetic': 'float64 row-unit directions; descriptive only'}


def paired_diagnostics(proxy_scores, true_scores, proxy_vectors, true_vectors,
                       sample_positions, anchors, paid):
    p = np.asarray(proxy_scores)
    t = np.asarray(true_scores)
    if p.shape != t.shape or p.ndim != 2 or p.shape[1] != len(sample_positions):
        raise ValueError('Paired score/sample shapes differ')
    error = p.astype(np.float64) - t.astype(np.float64)
    pv = np.asarray(proxy_vectors, dtype=np.float64)
    tv = np.asarray(true_vectors, dtype=np.float64)
    cosine = np.sum(pv * tv, axis=1) / (np.linalg.norm(pv, axis=1) * np.linalg.norm(tv, axis=1))
    result = {'sample_documents': len(sample_positions), 'queries': len(p),
              'error_definition': 'proxy_score minus true_score for the same query and document',
              'quantile_probabilities': QUANTILES, 'strata': {},
              'per_document_proxy_true_cosine': cosine.tolist(),
              'proxy_direction': direction_diagnostics(pv), 'true_direction': direction_diagnostics(tv),
              'per_query_error_mean': error.mean(axis=1).tolist(),
              'per_query_error_std': error.std(axis=1, ddof=0).tolist()}
    for name, mask in membership_masks(sample_positions, anchors, paid).items():
        e, ps, ts = error[:, mask], p[:, mask], t[:, mask]
        es = summary(e)
        pstats, tstats = summary(ps), summary(ts)
        result['strata'][name] = {'documents': int(mask.sum()), 'query_document_observations': int(e.size),
            'proxy_score': pstats, 'true_score': tstats, 'error': es,
            'signed_bias': es['mean'], 'mae': float(np.abs(e).mean()) if e.size else None,
            'rmse': float(np.sqrt(np.mean(e * e))) if e.size else None,
            'score_std_ratio': pstats['std'] / tstats['std'] if tstats['std'] else None,
            'per_query_error_mean': e.mean(axis=1).tolist() if e.size else [None] * len(p),
            'per_query_error_std': e.std(axis=1, ddof=0).tolist() if e.size else [None] * len(p),
            'proxy_true_cosine': summary(cosine[mask])}
    return result
