"""B2 one-shot independent TREC-COVID final scorer, after separate verification.

Labels are requested only after all 184 rankings and the qrel-free verification
seal pass. A durable run-root receipt prevents a second final label opening,
including after failure. No resumption, method selection, or postlabel tuning.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import os
from pathlib import Path
import sys
import time
import traceback
import urllib.request

import numpy as np

try:
    from b1m_score import (inside, mean_std, metrics_for, now, parse_qrel_rows,
                          read_json, sha, synthetic_checks as metric_checks, write_json)
    from b1c_r3_score import bootstrap_columns, resources, save_npy
    from b2_verify import (ROOT, DATASET, PAIRS, SEEDS, BUDGETS, PRIMARY, METHODS,
                           KEY_FIELDS, key, check_matrix, committed_context, verify_seal)
except ModuleNotFoundError:
    from ops.b1m_score import (inside, mean_std, metrics_for, now, parse_qrel_rows,
                              read_json, sha, synthetic_checks as metric_checks, write_json)
    from ops.b1c_r3_score import bootstrap_columns, resources, save_npy
    from ops.b2_verify import (ROOT, DATASET, PAIRS, SEEDS, BUDGETS, PRIMARY, METHODS,
                               KEY_FIELDS, key, check_matrix, committed_context, verify_seal)

METRICS = ('ndcg10', 'recall100')
DRAWS = 20000
BOOTSTRAP_SEED = 20261031
FAMILY_CONTRASTS = 30
ALPHA = 0.05
QREL_REVISION = '532ac68ee6756ac22c9346eebf65bd3c6a042e10'
QREL_SOURCE = {'format': 'tsv',
               'url': f'https://huggingface.co/datasets/BeIR/trec-covid-qrels/resolve/{QREL_REVISION}/test.tsv',
               'revision': QREL_REVISION, 'bytes': 980831,
               'git_blob_sha1': '9cb5167175d7cdbf9d85ea828c6a3da943fe7053'}


def source_specifications(lock):
    spec = lock['scoring']
    if (type(spec.get('bootstrap_draws')) is not int or spec['bootstrap_draws'] != DRAWS
            or type(spec.get('bootstrap_seed')) is not int or spec['bootstrap_seed'] != BOOTSTRAP_SEED
            or type(spec.get('contrasts')) is not int or spec['contrasts'] != FAMILY_CONTRASTS
            or spec.get('alpha') != ALPHA or spec.get('qrels') != QREL_SOURCE):
        raise ValueError('Require exact B2 preregistered scoring/source policy')
    if any(any(word in name.lower() for word in ('margin', 'equivalence', 'noninferiority', 'selection')) for name in spec):
        raise ValueError('No postlabel margins or selection policy')
    return spec


def verify_verification(run, seal, lock_sha, commit):
    path = run / 'verification' / 'verification_seal.json'
    verified = read_json(path)
    if (verified.get('status') != 'ENDPOINTS_INDEPENDENTLY_VERIFIED'
            or verified.get('qrels_opened') is not False
            or verified.get('ranking_seal_sha256') != sha(run / 'ranking_seal.json')
            or verified.get('lock_sha256') != lock_sha or verified.get('code_commit') != commit
            or verified.get('failures') != []):
        raise ValueError('Separate endpoint verification seal missing or invalid')
    records = verified['verified_cells']
    check_matrix(records)
    ranking_cells = {key(cell): cell for cell in seal['cells']}
    for record in records:
        cell = ranking_cells[key(record)]
        if (record.get('all_top100_ids_and_order_equal') is not True
                or record['ranking_sha256'] != cell['ranking_sha256']
                or record['endpoint_sha256'] != cell['endpoint_sha256']):
            raise ValueError('Verification is not bound to every sealed endpoint/ranking')
    if (run / 'verification' / 'failure.json').exists():
        raise ValueError('Preserved failed verification cannot authorize final labels')
    return sha(path)


def write_first_open(run, receipt):
    """Exclusive durable receipt before GET, file open, hashing or decoding labels."""
    write_json(run / 'first_final_qrel_open.json', receipt)
    # On POSIX, sync the containing directory as well as the receipt itself.
    if hasattr(os, 'O_DIRECTORY'):
        fd = os.open(run, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def acquire_qrels(out, source, opener=None):
    """Caller must already have durably written first_final_qrel_open.json."""
    run = out.parent
    if not (run / 'first_final_qrel_open.json').is_file():
        raise ValueError('No durable first final label opening receipt')
    path = out / 'qrels_TREC-COVID.tsv'
    write_json(out / 'qrel_request_started.json', {'request_started_utc': now(),
               'source': source, 'first_final_qrel_open_sha256': sha(run / 'first_final_qrel_open.json')})
    opener = urllib.request.urlopen if opener is None else opener
    with opener(source['url']) as response, path.open('xb') as stream:
        for block in iter(lambda: response.read(1024 * 1024), b''):
            stream.write(block)
        stream.flush()
        os.fsync(stream.fileno())
    content = path.read_bytes()
    blob_sha = hashlib.sha1(b'blob ' + str(len(content)).encode('ascii') + b'\0' + content).hexdigest()
    digest = hashlib.sha256(content).hexdigest()
    write_json(out / 'qrel_observed_hash.json', {'bytes': len(content), 'sha256': digest,
               'git_blob_sha1': blob_sha, 'source': source, 'observed_utc': now()})
    if len(content) != source['bytes'] or blob_sha != source['git_blob_sha1']:
        raise ValueError('Pinned final qrel Git blob/byte mismatch; preserve and STOP')
    # Decode/parse only after byte identity is established, retaining all grades.
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        qrels, columns = parse_qrel_rows(reader, reader.fieldnames, 'tsv')
    return qrels, {'sha256': digest, 'bytes': len(content), 'git_blob_sha1': blob_sha, 'columns': columns}, path


def interpretation(low, high):
    return 'above_zero' if low > 0 else 'below_zero' if high < 0 else 'unresolved'


def interval(values, draws, family=False):
    low, high = np.quantile(draws, [0.025, 0.975], method='linear')
    result = {'mean': float(np.mean(values)), 'ci95': [float(low), float(high)],
              'ci95_descriptive': True, 'interval_interpretation': interpretation(low, high)}
    if family:
        tail = ALPHA / (2 * FAMILY_CONTRASTS)
        low, high = np.quantile(draws, [tail, 1 - tail], method='linear')
        result.update(ci_bonferroni_family95=[float(low), float(high)],
                      per_interval_confidence=1 - ALPHA / FAMILY_CONTRASTS,
                      family_interval_interpretation=interpretation(low, high),
                      coverage='approximate percentile bootstrap')
    return result


def summaries(cells, arrays):
    lookup = {key(cell): arrays[index] for index, cell in enumerate(cells)}
    columns, definitions = [], []
    for pair in PAIRS:
        for budget, method in itertools.product(BUDGETS, METHODS):
            values = np.stack([lookup[(DATASET, pair, seed, budget, method)] for seed in SEEDS])
            columns.append(values.mean(axis=0))
            definitions.append(('mean', {'dataset': DATASET, 'pair': pair, 'budget': budget, 'method': method}, values.mean(axis=1)))
        for method in ('full_x', 'full_y'):
            values = lookup[(DATASET, pair, None, 'full', method)]
            columns.append(values)
            definitions.append(('mean', {'dataset': DATASET, 'pair': pair, 'budget': 'full', 'method': method}, values.mean(axis=0)[None, :]))
        for budget, baseline in itertools.product(BUDGETS, [m for m in METHODS if m != PRIMARY]):
            values = np.stack([lookup[(DATASET, pair, seed, budget, PRIMARY)] -
                               lookup[(DATASET, pair, seed, budget, baseline)] for seed in SEEDS])
            columns.append(values.mean(axis=0))
            definitions.append(('contrast', {'dataset': DATASET, 'pair': pair, 'budget': budget,
                                             'left': PRIMARY, 'right': baseline}, values.mean(axis=1)))
    # Every method, metric and contrast is one column in one bootstrap call:
    # identical query resamples across all pairs/budgets/methods/metrics.
    values = np.concatenate(columns, axis=1)
    boot, index_digest = bootstrap_columns(values, np.random.default_rng(BOOTSTRAP_SEED), draws=DRAWS)
    means, contrasts = [], []
    for i, (kind, identity, seed_means) in enumerate(definitions):
        row = dict(identity)
        for j, metric in enumerate(METRICS):
            result = interval(columns[i][:, j], boot[:, 2 * i + j], family=kind == 'contrast' and metric == 'ndcg10')
            if kind == 'contrast':
                result['delta'] = result.pop('mean')
                result['mapping_seed_variability'] = mean_std(seed_means[:, j])
            else:
                result.update(mean_std(seed_means[:, j]))
            row[metric] = result
        (means if kind == 'mean' else contrasts).append(row)
    if len(means) != 40 or len(contrasts) != FAMILY_CONTRASTS:
        raise ValueError('Summary matrix drift')
    bootstrap = {'draws': DRAWS, 'seed': BOOTSTRAP_SEED, 'rng': 'numpy default_rng/PCG64',
                 'query_indices_sha256': index_digest, 'definitions': [dict(kind=k, **v) for k, v, _ in definitions],
                 'axes': ['bootstrap_draw', 'definition_then_metric'], 'metrics': METRICS,
                 'resampling': 'one identical query resample across all pairs/budgets/methods/metrics; average five mapping seeds first',
                 'family_contrasts': FAMILY_CONTRASTS, 'family_alpha': ALPHA,
                 'per_interval_confidence': 1 - ALPHA / FAMILY_CONTRASTS,
                 'recall_intervals': 'nominal95 descriptive', 'coverage': 'approximate percentile bootstrap'}
    return means, contrasts, bootstrap, boot


def markdown(summary):
    lines = ['# B2 independent TREC-COVID results', '',
             'All 184 rankings were sealed and separately recomputed before the one-shot final label opening. No postlabel tuning or method selection.', '',
             'Thirty ARC2-minus-external nDCG@10 contrasts use nominal 99.833333% percentile intervals (Bonferroni 0.05/30, approximate family 95%). Recall@100 intervals are nominal 95% descriptive. Five mapping seeds are averaged before the shared paired query bootstrap. An interval touching or crossing zero is unresolved; no equivalence claim.', '',
             '| Pair | Budget | ARC2 minus baseline | nDCG delta [family interval] | Recall delta [descriptive 95%] |',
             '|---|---|---|---:|---:|']
    for row in summary['contrasts']:
        n, r = row['ndcg10'], row['recall100']
        nl, nh = n['ci_bonferroni_family95']
        rl, rh = r['ci95']
        lines.append(f"| {row['pair']} | {row['budget']} | {row['right']} | {n['delta']:+.6f} [{nl:+.6f}, {nh:+.6f}] | {r['delta']:+.6f} [{rl:+.6f}, {rh:+.6f}] |")
    lines += ['', 'Full-X is the incumbent reference; Full-Y is the native destination reference, not an upper bound. All evaluation queries count, including queries with zero positive judgments. Graded gains are 2^rel-1. Recall divides by all positive judgments, including documents outside the corpus. All seed means, standard deviations and ranges are retained in JSON.', '',
              'STOP for independent result-to-claim review. Manuscript remains untouched; no systems or ANN claim.', '']
    return '\n'.join(lines)


def run_score(lock_path, run):
    lock_path, run = Path(lock_path).resolve(), Path(run).resolve()
    out = run / 'scoring'
    out.mkdir(exist_ok=False)
    start = time.perf_counter()
    try:
        if (run / 'first_final_qrel_open.json').exists():
            raise ValueError('Final qrels already opened once; no retry or recovery authorized')
        lock, commit = committed_context(lock_path)
        spec = source_specifications(lock)
        lock_sha = sha(lock_path)
        write_json(out / 'started.json', {'status': 'VALIDATING_BEFORE_FINAL_LABEL_ACCESS', 'started_utc': now(),
                   'lock_sha256': lock_sha, 'code_commit': commit, 'python': sys.version, 'numpy': np.__version__})
        seal, ids = verify_seal(run, lock_sha, commit)
        verification_sha = verify_verification(run, seal, lock_sha, commit)
        seal_sha = sha(run / 'ranking_seal.json')
        checks = metric_checks()
        write_json(out / 'synthetic_metric_checks.json', checks)
        receipt = {'first_final_qrel_open_utc': now(), 'dataset': DATASET,
                   'ranking_seal_sha256': seal_sha, 'verification_seal_sha256': verification_sha,
                   'lock_sha256': lock_sha, 'code_commit': commit, 'all_184_rankings_verified': True,
                   'expected_source': spec['qrels'], 'policy': 'exactly once; failure preserved; no postlabel tuning'}
        write_first_open(run, receipt)
        qrels, qrel_stats, qrel_path = acquire_qrels(out, spec['qrels'])
        docs, queries = ids
        doc_set = set(docs)
        qrel_stats.update(evaluation_queries=len(queries),
            queries_without_positive_judgments=sum(not any(v > 0 for v in qrels.get(q, {}).values()) for q in queries),
            positive_judgments_outside_corpus_retained_in_denominator=sum(v > 0 and d not in doc_set for q in queries for d, v in qrels.get(q, {}).items()),
            qrel_queries_outside_evaluation_set=len(set(qrels) - set(queries)))
        write_json(out / 'qrel_verified.json', qrel_stats)
        values = []
        for cell in seal['cells']:
            path = inside(run, cell['ranking_path'])
            if sha(path) != cell['ranking_sha256']:
                raise ValueError('Ranking changed before metric computation')
            ranks = np.load(path, allow_pickle=False)
            metrics = metrics_for(ranks, docs, queries, qrels)
            if metrics.shape != (len(queries), 2) or not np.isfinite(metrics).all():
                raise ValueError('Invalid per-query metrics')
            values.append(metrics)
        arrays = np.stack(values)
        save_npy(out / 'per_query.npy', arrays)
        write_json(out / 'cell_index.json', {'cells': seal['cells'], 'query_ids': queries,
                   'axes': ['cell', 'query', 'metric'], 'metrics': METRICS})
        means, contrasts, bootstrap, boot = summaries(seal['cells'], arrays)
        save_npy(out / 'bootstrap_draws.npy', boot)
        committed_context(lock_path)
        verify_seal(run, lock_sha, commit)
        if verify_verification(run, seal, lock_sha, commit) != verification_sha or sha(run / 'ranking_seal.json') != seal_sha:
            raise ValueError('Prelabel seals changed during scoring')
        if sha(qrel_path) != qrel_stats['sha256']:
            raise ValueError('Final qrels changed during scoring')
        summary = {'status': 'FINAL_SCORED', 'stage': 'B2', 'completed_utc': now(), 'ranking_cells': 184,
                   'lock_sha256': lock_sha, 'code_commit': commit, 'ranking_seal_sha256': seal_sha,
                   'verification_seal_sha256': verification_sha, 'scoring': spec, 'qrel_stats': qrel_stats,
                   'means': means, 'contrasts': contrasts, 'bootstrap': bootstrap,
                   'elapsed_seconds': time.perf_counter() - start, 'resources': resources(), 'failures': [],
                   'next_action': 'STOP for independent result-to-claim review; manuscript untouched; no systems'}
        write_json(out / 'summary.json', summary)
        with (out / 'summary.md').open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(markdown(summary))
            stream.flush()
            os.fsync(stream.fileno())
        artifacts = {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}
        write_json(out / 'completed.json', {'status': 'FINAL_SCORED', 'completed_utc': now(),
                   'artifact_sha256': artifacts, 'first_final_qrel_open_sha256': sha(run / 'first_final_qrel_open.json'),
                   'code_commit': commit, 'next_action': summary['next_action']})
        return summary
    except BaseException as error:
        write_json(out / 'failure.json', {'status': 'FAILED_PRESERVED', 'failed_utc': now(),
                   'error': repr(error), 'traceback': traceback.format_exc(),
                   'elapsed_seconds': time.perf_counter() - start, 'resources': resources(),
                   'final_qrel_access_started': (run / 'first_final_qrel_open.json').exists()})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, default=Path('configs/b2_lock.json'))
    parser.add_argument('--run', type=Path, required=True)
    args = parser.parse_args()
    run_score(args.lock, args.run)
