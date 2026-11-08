"""Read-only local QA of completed B2; no scorer imports, network, fit or search.

Resolves final mutable backup files through operator_state.coverage, verifies
portable evidence hashes, independently parses saved qrels, rescoring rankings
and recomputing the shared PCG64 bootstrap by direct query-index averaging.
Large vector/checkpoint hashes are matched to terminal transport coverage; they
are not rehashed or regenerated. Writes only a new, exclusive QA receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = 'results/b2_full_r1_20261031t064859'
PAIRS = ('minilm_distilroberta', 'e5_small_base')
SEEDS = (17, 29, 41, 53, 67)
BUDGETS = ('25pct', '50pct', '75pct')
PRIMARY = 'arc2_global_tangent2_r1'
METHODS = ('procrustes_global', PRIMARY, 'la2m20_integration_script_adaptation',
           'simplelinear_official_final50_mlp5', 'ridge_affine_l10_bias_regularized',
           'embedding_converter_paper_spec')
FIELDS = ('dataset', 'pair', 'seed', 'budget', 'method')
METRICS = ('ndcg10', 'recall100')
SEMANTICS = {'dtype': 'float32', 'score': 'dot', 'k': 100, 'batch_rows': 16,
             'tie_policy': 'descending score then ascending document row index',
             'exclude_identical_ids': True}


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def key(cell):
    return tuple(cell[name] for name in FIELDS)


def matrix(cells):
    expected = {('TREC-COVID', p, s, b, m) for p, s, b, m in
                itertools.product(PAIRS, SEEDS, BUDGETS, METHODS)}
    expected.update(('TREC-COVID', p, None, 'full', m)
                    for p in PAIRS for m in ('full_x', 'full_y'))
    actual = [key(c) for c in cells]
    require(len(actual) == 184 and len(set(actual)) == 184 and set(actual) == expected,
            'Incomplete/duplicate 184-cell matrix')


class Evidence:
    def __init__(self, backup):
        self.backup = Path(backup).resolve()
        self.state_path = self.backup / 'operator_state.json'
        self.state = read(self.state_path)
        self.coverage = self.state['coverage']
        self.remote = self.state['remote_project'].rstrip('/')
        self.rehashed = {}
        self.transport_only = {}

    def relative(self, name):
        name = str(name)
        if name.startswith(self.remote + '/'):
            name = name[len(self.remote) + 1:]
        require(not name.startswith('/') and '..' not in Path(name).parts,
                'Invalid original path: ' + name)
        return name

    def path(self, name, digest=None, *, large=False):
        name = self.relative(name)
        require(name in self.coverage, 'Missing terminal coverage: ' + name)
        spec = self.coverage[name]
        path = (self.backup / spec['local']).resolve()
        require(path.is_relative_to(self.backup) and path.is_file(), 'Missing backup: ' + name)
        require(path.stat().st_size == spec['bytes'], 'Backup size drift: ' + name)
        require(digest is None or spec['sha256'] == digest, 'Coverage digest drift: ' + name)
        if large or spec['bytes'] > 16 * 1024 * 1024 and not name.endswith('bootstrap_draws.npy'):
            self.transport_only[name] = spec
        elif name not in self.rehashed:
            require(sha(path) == spec['sha256'], 'Backup hash drift: ' + name)
            self.rehashed[name] = spec
        return path

    def json(self, name, digest=None):
        return read(self.path(name, digest))

    def run(self, name, digest=None):
        return self.path(RUN + '/' + name, digest)

    def run_json(self, name, digest=None):
        return read(self.run(name, digest))


def independent_qrels(path):
    content = path.read_bytes()
    require(len(content) == 980831, 'Locked qrel byte count')
    blob = hashlib.sha1(b'blob ' + str(len(content)).encode('ascii') + b'\0' + content).hexdigest()
    require(blob == '9cb5167175d7cdbf9d85ea828c6a3da943fe7053', 'Locked qrel Git blob')
    judgments, count = {}, 0
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        require(reader.fieldnames == ['query-id', 'corpus-id', 'score'], 'Qrel columns')
        for row in reader:
            q, d, r = row['query-id'], row['corpus-id'], float(row['score'])
            require(q and d and math.isfinite(r), 'Invalid qrel')
            per_query = judgments.setdefault(q, {})
            require(d not in per_query, 'Duplicate qrel')
            per_query[d] = r
            count += 1
    return judgments, {'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest(),
                       'git_blob_sha1': blob, 'columns': reader.fieldnames}, count


def metrics(ranks, docs, queries, qrels):
    result = np.zeros((50, 2), dtype=np.float64)
    for i, q in enumerate(queries):
        positives = {d: grade for d, grade in qrels.get(q, {}).items() if grade > 0}
        if not positives:
            continue
        returned = [docs[int(row)] for row in ranks[i]]
        ideal = sorted(positives.values(), reverse=True)[:10]
        idcg = math.fsum((2.0 ** grade - 1.0) / math.log2(j + 2)
                         for j, grade in enumerate(ideal))
        dcg = math.fsum((2.0 ** positives.get(d, 0.0) - 1.0) / math.log2(j + 2)
                        for j, d in enumerate(returned[:10]))
        result[i] = dcg / idcg, sum(d in positives for d in returned) / len(positives)
    return result


def interpretation(lo, hi):
    return 'above_zero' if lo > 0 else 'below_zero' if hi < 0 else 'unresolved'


def seed_stats(values):
    return {'mean': float(np.mean(values)),
            'seed_std': float(np.std(values, ddof=1)) if len(values) > 1 else None,
            'seed_range': [float(np.min(values)), float(np.max(values))] if len(values) > 1 else None,
            'seeds': len(values)}


def independent_summary(cells, arrays):
    lookup = {key(c): arrays[i] for i, c in enumerate(cells)}
    definitions, columns, seed_means = [], [], []
    def partial(pair, budget, method):
        return np.stack([lookup[('TREC-COVID', pair, s, budget, method)] for s in SEEDS])
    def append(kind, pair, budget, values, **identity):
        definitions.append(dict(kind=kind, dataset='TREC-COVID', pair=pair, budget=budget, **identity))
        columns.append(values.mean(axis=0))
        seed_means.append(values.mean(axis=1))
    for pair in PAIRS:
        for budget, method in itertools.product(BUDGETS, METHODS):
            append('mean', pair, budget, partial(pair, budget, method), method=method)
        for method in ('full_x', 'full_y'):
            append('mean', pair, 'full', lookup[('TREC-COVID', pair, None, 'full', method)][None], method=method)
        for budget, baseline in itertools.product(BUDGETS, [m for m in METHODS if m != PRIMARY]):
            append('contrast', pair, budget, partial(pair, budget, PRIMARY) - partial(pair, budget, baseline),
                   left=PRIMARY, right=baseline)
    # Independent algorithm: gather the sampled query rows directly, then sum.
    # No scientific scorer/helper imports or weighted BLAS bootstrap call.
    values = np.concatenate(columns, axis=1)
    indices = np.random.Generator(np.random.PCG64(20261031)).integers(
        0, 50, size=(20000, 50), dtype=np.int32)
    index_sha = hashlib.sha256(indices.astype('<i4', copy=False).tobytes(order='C')).hexdigest()
    boot = np.empty((20000, 140), dtype=np.float64)
    for start in range(0, 20000, 100):
        boot[start:start + 100] = values[indices[start:start + 100]].mean(axis=1)
    means, contrasts = [], []
    for i, definition in enumerate(definitions):
        row = {k: v for k, v in definition.items() if k != 'kind'}
        contrast = definition['kind'] == 'contrast'
        for j, metric in enumerate(METRICS):
            draws = boot[:, 2 * i + j]
            lo, hi = np.quantile(draws, [0.025, 0.975], method='linear')
            stat = {'delta' if contrast else 'mean': float(columns[i][:, j].mean()),
                    'ci95': [float(lo), float(hi)], 'ci95_descriptive': True,
                    'interval_interpretation': interpretation(lo, hi)}
            if contrast:
                stat['mapping_seed_variability'] = seed_stats(seed_means[i][:, j])
                if metric == 'ndcg10':
                    lo, hi = np.quantile(draws, [0.05 / 60, 1 - 0.05 / 60], method='linear')
                    stat.update(ci_bonferroni_family95=[float(lo), float(hi)],
                                per_interval_confidence=1 - 0.05 / 30,
                                family_interval_interpretation=interpretation(lo, hi),
                                coverage='approximate percentile bootstrap')
            else:
                stat.update(seed_stats(seed_means[i][:, j]))
            row[metric] = stat
        (contrasts if contrast else means).append(row)
    return means, contrasts, definitions, boot, index_sha


def verify(backup, qa, bundle=None):
    started = time.perf_counter()
    ev = Evidence(backup)
    terminal_path = sorted(ev.backup.glob('coverage_*.json'))[-1]
    terminal = read(terminal_path)
    terminal_event = json.loads((ev.backup / 'operator_events.jsonl').read_text().splitlines()[-1])
    require(terminal['coverage'] == ev.coverage and terminal['pending'] == []
            and terminal['all_current_files_verified'] is True and len(terminal['completed_groups']) == 60
            and terminal_event['status'] == 'COMPLETE_CAMPAIGN_BACKED_UP', 'Terminal transport receipt')
    seal = ev.run_json('ranking_seal.json')
    seal_sha = sha(ev.run('ranking_seal.json'))
    verification = ev.run_json('verification/verification_seal.json')
    ver_sha = sha(ev.run('verification/verification_seal.json'))
    summary = ev.run_json('scoring/summary.json')
    complete = ev.run_json('scoring/completed.json')
    lock_path = ROOT / 'configs/b2_lock.json'
    lock, commit = read(lock_path), seal['code_commit']
    lock_sha = hashlib.sha256(lock_path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    require(lock_sha == seal['lock_sha256'], 'Canonical-LF lock differs from remote seal')
    sources = lock['source_sha256_canonical_lf']
    for relative, digest in sources.items():
        require(hashlib.sha256((ROOT / relative).read_bytes().replace(b'\r\n', b'\n')).hexdigest() == digest,
                'Local canonical-LF source drift: ' + relative)
    # Bind the actual pre-run Git object graph as well as the working source.
    for relative, digest in [('configs/b2_lock.json', lock_sha)] + list(sources.items()):
        data = subprocess.check_output(['git', 'show', f'{commit}:{relative}'], cwd=ROOT)
        require(hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() == digest,
                'Pre-run commit/source binding drift: ' + relative)
    cells = seal['cells']
    matrix(cells)
    matrix(verification['verified_cells'])
    require(seal['status'] == 'RANKINGS_SEALED' and seal['mode'] == 'full'
            and seal['qrels_opened'] is False and seal['ranking_process_qrel_reads'] == 0,
            'Invalid full prelabel ranking seal')
    require(verification['status'] == 'ENDPOINTS_INDEPENDENTLY_VERIFIED'
            and verification['qrels_opened'] is False and verification['failures'] == [],
            'Separate endpoint verification not PASS')
    for record in (verification, summary):
        require(record['ranking_seal_sha256'] == seal_sha, 'Ranking seal binding')
    for record in (verification, summary, seal):
        require(record['lock_sha256'] == lock_sha and record['code_commit'] == commit, 'Source/lock binding')
    require(summary['status'] == complete['status'] == 'FINAL_SCORED' and summary['failures'] == []
            and summary['ranking_cells'] == 184 and summary['verification_seal_sha256'] == ver_sha,
            'Final scorer status/binding')
    require(summary['scoring'] == lock['scoring'] and lock['scoring']['bootstrap_draws'] == 20000
            and lock['scoring']['bootstrap_seed'] == 20261031 and lock['scoring']['contrasts'] == 30
            and lock['scoring']['alpha'] == 0.05, 'Scoring policy drift')
    for relative, digest in complete['artifact_sha256'].items():
        ev.run('scoring/' + relative, digest)
    opening = ev.run_json('first_final_qrel_open.json', complete['first_final_qrel_open_sha256'])
    require(opening['ranking_seal_sha256'] == seal_sha and opening['verification_seal_sha256'] == ver_sha
            and opening['lock_sha256'] == lock_sha and opening['code_commit'] == commit
            and opening['all_184_rankings_verified'] is True
            and opening['expected_source'] == lock['scoring']['qrels'], 'First opening binding')
    request = ev.run_json('scoring/qrel_request_started.json')
    observed = ev.run_json('scoring/qrel_observed_hash.json')
    require(request['first_final_qrel_open_sha256'] == sha(ev.run('first_final_qrel_open.json'))
            and request['source'] == observed['source'] == lock['scoring']['qrels'], 'Qrel request binding')
    timeline = {'rankings_sealed': seal['sealed_utc'], 'endpoints_verified': verification['completed_utc'],
                'scorer_started': ev.run_json('scoring/started.json')['started_utc'],
                'first_open_receipt': opening['first_final_qrel_open_utc'],
                'network_request_started': request['request_started_utc'],
                'qrel_bytes_observed': observed['observed_utc'], 'summary_completed': summary['completed_utc'],
                'scoring_sealed': complete['completed_utc']}
    times = [datetime.fromisoformat(t) for t in timeline.values()]
    require(all(a < b for a, b in zip(times, times[1:])), 'Prelabel/scoring chronological order')
    for relative, digest in seal['inputs'].items():
        ev.run(relative, digest)
    ids = ev.run_json('inputs/ids.json')
    docs, queries = ids['doc_ids'], ids['query_ids']
    require(len(docs) == len(set(docs)) == 171332 and len(queries) == len(set(queries)) == 50
            and all(isinstance(x, str) and x for x in docs + queries), 'Ordered IDs')
    for seed in SEEDS:
        anchors = np.load(ev.run(f'inputs/anchors_seed{seed}.npy'), allow_pickle=False)
        order = np.load(ev.run(f'inputs/order_seed{seed}.npy'), allow_pickle=False)
        expected_a = np.random.default_rng(np.random.SeedSequence([seed, 0])).choice(171332, 1024, replace=False)
        expected_o = np.random.default_rng(np.random.SeedSequence([seed, 1])).permutation(171332)
        require(np.array_equal(anchors, expected_a) and np.array_equal(order, expected_o), 'Anchor/order RNG identity')
        tail = order[~np.isin(order, anchors)]
        for budget, count in zip(BUDGETS, (42833, 85666, 128499)):
            paid = np.load(ev.run(f'inputs/paid_seed{seed}_{budget}.npy'), allow_pickle=False)
            require(np.array_equal(paid, np.sort(np.concatenate((anchors, tail[:count-1024])))),
                    'Locked anchor-inclusive paid selection')
    for mapping in ('endpoint_dependency_sha256', 'fit_artifact_sha256'):
        for path, digest in seal[mapping].items():
            ev.path(path, digest)
    encoding_spec = seal['encoding_manifest']
    encoding = ev.json(encoding_spec['path'], encoding_spec['sha256'])
    require(encoding['status'] == 'ENCODING_PASS' and encoding['lock']['sha256'] == lock_sha
            and encoding['code_commit'] == commit and encoding['failures'] == []
            and encoding['qrels_requested_or_read'] is False
            and encoding['ids']['sha256'] == seal['inputs']['inputs/ids.json'], 'Encoding identities')
    require(encoding['physical_document_encodes_completed'] == 4 * 171332
            and encoding['physical_query_encodes_completed'] == 4 * 50, 'Physical encoding counts')
    encode_root = str(Path(ev.relative(encoding_spec['path'])).parent).replace('\\', '/')
    for model_name, model in lock['acquisition']['models'].items():
        output = encoding['models'][model_name]
        require(output['model_id'] == model['id'] and output['revision'] == model['revision']
                and output['max_seq_length'] == 128, 'Locked encoder revision/length')
        for role, count in (('docs', 171332), ('queries', 50)):
            artifact = output['outputs'][role]
            require(artifact['shape'] == [count, model['dimension']] and artifact['dtype'] == 'float32',
                    'Encoded vector shape/type')
            ev.path(encode_root + '/' + artifact['path'], artifact['sha256'])
            ev.path(encode_root + '/' + artifact['journal_path'], artifact['journal_sha256'])
    schedule = ev.json('results/b2_schedule_r1_20261031t064859/metadata.json')
    require(schedule['status'] == 'B2_SCORED_STOP_FOR_REVIEW' and schedule['code_commit'] == commit
            and schedule['lock_sha256'] == lock_sha and schedule['manuscript_updates'] is False
            and schedule['next_scientific_phase_auto_launch'] is False, 'Campaign completion/STOP')
    require([j['stage'] for j in schedule['jobs']] ==
            ['acquire', 'encode_smoke', 'smoke', 'verify_smoke', 'encode_full', 'full', 'verify', 'score'],
            'Required matching smoke/full/verification/scoring order')
    previous_end = None
    for job in schedule['jobs']:
        start_time, end_time = map(datetime.fromisoformat, (job['started_utc'], job['ended_utc']))
        require(job['returncode'] == 0 and start_time < end_time
                and (previous_end is None or previous_end < start_time), 'Campaign job failure/overlap')
        previous_end = end_time
        receipt = ev.json(job['receipt_path'], job['receipt_sha256'])
        require(receipt.get('failures', []) == [], 'Job failure receipt')
    verified = {key(c): c for c in verification['verified_cells']}
    index = ev.run_json('scoring/cell_index.json')
    require(index['cells'] == cells and index['query_ids'] == queries and index['metrics'] == list(METRICS)
            and index['axes'] == ['cell', 'query', 'metric'], 'Scoring index identity/order')
    qrels, qstats, qrel_rows = independent_qrels(ev.run('scoring/qrels_TREC-COVID.tsv'))
    doc_set = set(docs)
    qstats.update(evaluation_queries=50,
                  queries_without_positive_judgments=sum(not any(r > 0 for r in qrels.get(q, {}).values()) for q in queries),
                  positive_judgments_outside_corpus_retained_in_denominator=sum(
                      r > 0 and d not in doc_set for q in queries for d, r in qrels.get(q, {}).items()),
                  qrel_queries_outside_evaluation_set=len(set(qrels) - set(queries)))
    require(qstats == summary['qrel_stats'] == ev.run_json('scoring/qrel_verified.json'), 'Independent qrel stats')
    require(all(observed[k] == qstats[k] for k in ('bytes', 'sha256', 'git_blob_sha1')), 'Observed qrel hash binding')
    values = np.load(ev.run('scoring/per_query.npy'), allow_pickle=False)
    require(values.shape == (184, 50, 2) and np.isfinite(values).all(), 'Per-query shape/values')
    independently = np.empty_like(values)
    fits, statuses = {}, Counter()
    for i, cell in enumerate(cells):
        record = verified[key(cell)]
        require(record['all_top100_ids_and_order_equal'] is True
                and record['ranking_sha256'] == cell['ranking_sha256']
                and record['endpoint_sha256'] == cell['endpoint_sha256'], 'Independent verifier cell binding')
        require(ev.run_json(f'verification/cell_{i:03d}.json') == record, 'Per-cell verification receipt')
        endpoint = ev.run_json(cell['endpoint_path'], cell['endpoint_sha256'])
        require(endpoint['schema'] == 'b2_exact_endpoint_v1' and endpoint['semantics'] == SEMANTICS,
                'Endpoint search semantics')
        require(endpoint['shape'][0] == 171332, 'Endpoint gallery rows')
        for spec in endpoint['files'].values():
            require(seal['endpoint_dependency_sha256'].get(spec['path']) == spec['sha256'],
                    'Endpoint source dependency binding')
        expected_encoder = {'minilm_distilroberta': ('minilm_x', 'distilroberta_y'),
                            'e5_small_base': ('e5_small_x', 'e5_base_y')}[cell['pair']]
        model = expected_encoder[0 if cell['method'] == 'full_x' else 1]
        require(endpoint['files']['query_vectors']['path'].endswith('/vectors/' + model + '_queries.npy'),
                'Named query encoder binding')
        require(endpoint['shape'][1] == (384 if cell['method'] == 'full_x' else 768), 'Named encoder dimension')
        if cell['budget'] != 'full':
            require(endpoint['kind'] == 'mixed' and cell['fit_pairs'] == 1024
                    and cell['unique_destination_encodings'] == dict(zip(BUDGETS, (42833, 85666, 128499)))[cell['budget']],
                    'Partial cell budget/fit identity')
            receipt = cell['fit_receipt']
            fit_key = (cell['pair'], cell['seed'], cell['method'])
            if fit_key in fits:
                require(fits[fit_key] == receipt, 'Shared fit receipt changed across budgets')
            else:
                fits[fit_key] = receipt
                statuses[receipt['status']] += 1
                metadata_spec = receipt['fit_artifacts'].get('metadata.json',
                                receipt['fit_artifacts'].get('worker_metadata'))
                metadata = ev.json(metadata_spec['path'], metadata_spec['sha256'])
                decorations = {'fit_artifacts', 'fit_anchor_indices_sha256', 'proxy_sha256', 'reused_for_budgets'}
                require({k: v for k, v in receipt.items() if k not in decorations} == metadata,
                        'Sealed fit receipt differs from actual metadata')
                if 'process_exit' in receipt['fit_artifacts']:
                    spec = receipt['fit_artifacts']['process_exit']
                    exit_record = ev.json(spec['path'], spec['sha256'])
                    require(exit_record['status'] == 'EXITED' and exit_record['returncode'] == 0
                            and exit_record['signal_number'] is None, 'Neural process failure')
                if cell['method'] == 'simplelinear_official_final50_mlp5':
                    require(receipt['configuration'] == lock['simplelinear_defaults'], 'SimpleLinear frozen defaults')
                if cell['method'] == 'embedding_converter_paper_spec':
                    require(receipt['config'] == lock['converter_config'] and receipt['train_count'] == 896
                            and receipt['validation_count'] == 128
                            and receipt['selected_iteration'] == receipt['refit_iterations']
                            and 0 < receipt['selected_iteration'] <= 50000,
                            'Converter locked selection/fresh refit')
                for health in ('selection_health', 'refit_health'):
                    if health in receipt:
                        names = (('losses_finite', 'parameters_finite', 'all_step_losses_and_gradients_finite',
                                  'initial_gradient_nonzero', 'parameters_updated') if
                                 cell['method'] == 'embedding_converter_paper_spec' else
                                 ('initial_gradients_finite_nonzero', 'parameters_updated', 'parameters_finite',
                                  'gradients_finite'))
                        require(all(receipt[health][name] is True for name in names), 'Neural health failure')
            require(receipt['fit_pairs'] == 1024 and receipt.get('failures', []) == [], 'Fit status/exposure')
            require(receipt['fit_anchor_indices_sha256'] == endpoint['files']['anchor_indices']['sha256']
                    and receipt['proxy_sha256'] == endpoint['files']['proxy_vectors']['sha256'], 'Fit/endpoint binding')
            for spec in receipt['fit_artifacts'].values():
                require(seal['fit_artifact_sha256'].get(spec['path']) == spec['sha256'], 'Fit artifact binding')
            if 'new_qrel_reads' in receipt:
                require(receipt['new_qrel_reads'] == receipt['unpaid_target_reads'] == 0
                        and receipt['code_commit'] == commit and receipt['lock_sha256'] == lock_sha,
                        'Neural fit label/source identity')
                require(datetime.fromisoformat(receipt['ended_utc']) < times[0], 'Fit completed after ranking seal')
            require(endpoint['files']['destination_vectors']['path'].endswith('/vectors/' + expected_encoder[1] + '_docs.npy'),
                    'Named destination encoder')
            require(endpoint['files']['paid_indices']['sha256'] == seal['inputs'][f"inputs/paid_seed{cell['seed']}_{cell['budget']}.npy"],
                    'Paid set identity')
        else:
            require(endpoint['kind'] == 'native' and endpoint['files']['native_vectors']['path'].endswith('/vectors/' + model + '_docs.npy'),
                    'Native reference encoder')
        ranks = np.load(ev.run(cell['ranking_path'], cell['ranking_sha256']), allow_pickle=False)
        require(ranks.shape == (50, 100) and ranks.dtype.kind in 'iu' and ranks.min() >= 0
                and ranks.max() < 171332 and all(len(set(row)) == 100 for row in ranks), 'Ranking shape/row validity')
        require(all(queries[j] not in [docs[int(n)] for n in row] for j, row in enumerate(ranks)), 'Identical-ID exclusion')
        independently[i] = metrics(ranks, docs, queries, qrels)
    require(len(fits) == 60 and statuses == {'CPU_FIT_PASS': 40, 'B1P_NEURAL_FULL_PASS': 20}, 'All 60 fits complete')
    metric_error = float(np.max(np.abs(values - independently)))
    require(metric_error <= 1e-12, 'Independent metric discrepancy')
    print(f'184 rankings / 18400 metrics independently verified; max error {metric_error:.3g}', flush=True)
    means, contrasts, definitions, boot, index_sha = independent_summary(cells, independently)
    require(summary['bootstrap']['definitions'] == definitions and summary['bootstrap']['query_indices_sha256'] == index_sha,
            'Shared PCG64 draw identities')
    stored_boot = np.load(ev.run('scoring/bootstrap_draws.npy'), allow_pickle=False)
    require(stored_boot.shape == boot.shape == (20000, 140), 'Bootstrap matrix shape')
    bootstrap_error = float(np.max(np.abs(boot - stored_boot)))
    require(bootstrap_error <= 1e-12, 'Independent bootstrap draws differ')
    numeric, summary_error = 0, 0.0
    def compare(actual, expected, where):
        nonlocal numeric, summary_error
        if isinstance(expected, dict):
            require(isinstance(actual, dict) and actual.keys() == expected.keys(), 'Summary keys: ' + where)
            for name, val in expected.items():
                compare(actual[name], val, where + '/' + name)
        elif isinstance(expected, list):
            require(isinstance(actual, list) and len(actual) == len(expected), 'Summary list: ' + where)
            for i, val in enumerate(expected):
                compare(actual[i], val, f'{where}/{i}')
        elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
            error = abs(actual - expected)
            require(math.isfinite(error) and error <= 1e-12, 'Summary number differs: ' + where)
            numeric += 1
            summary_error = max(summary_error, error)
        else:
            require(actual == expected, 'Summary value differs: ' + where)
    compare(summary['means'], means, 'means')
    compare(summary['contrasts'], contrasts, 'contrasts')
    failure_paths = [k for k in ev.coverage if 'failure' in k.lower() and k.startswith('results/b2_')]
    require(not failure_paths, 'Preserved B2 failure requires review: ' + str(failure_paths))
    stderr = []
    for relative, spec in ev.coverage.items():
        if relative.startswith('results/b2_') and relative.endswith('stderr.log') and spec['bytes']:
            path = ev.path(relative)
            stderr.append({'path': relative, 'bytes': spec['bytes'], 'sha256': spec['sha256'],
                           'first_1200_characters': path.read_text(encoding='utf-8', errors='replace')[:1200]})
    effects = Counter(row['ndcg10']['family_interval_interpretation'] for row in contrasts)
    by_pair = {p: dict(Counter(row['ndcg10']['family_interval_interpretation'] for row in contrasts if row['pair'] == p)) for p in PAIRS}
    result = {'status': 'PASS', 'verified_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Independent local computation from completed B2 saved qrels/rankings; no new scientific scoring invocation',
              'backup_root': str(ev.backup), 'operator_state_sha256': sha(ev.state_path),
              'terminal_coverage_receipt_sha256': sha(terminal_path), 'terminal_backup_event': terminal_event,
              'terminal_backup_files': len(ev.coverage),
              'terminal_backup_bytes': sum(s['bytes'] for s in ev.coverage.values()),
              'remote_project': ev.remote, 'code_commit': commit, 'lock_sha256_canonical_lf': lock_sha,
              'source_canonical_lf_pins_verified': len(sources), 'pre_run_git_objects_verified': len(sources) + 1,
              'ranking_seal_sha256': seal_sha, 'verification_seal_sha256': ver_sha,
              'summary_sha256': sha(ev.run('scoring/summary.json')), 'timeline_utc': timeline,
              'prescribed_unique_cells_verified': 184, 'rankings_independently_rescored': 184,
              'fit_groups_verified': len(fits), 'fit_statuses': dict(statuses),
              'ordered_document_ids': len(docs), 'ordered_query_ids': len(queries), 'qrel_rows': qrel_rows,
              'qrel_stats': qstats, 'per_query_metric_values_compared': independently.size,
              'largest_metric_absolute_discrepancy': metric_error,
              'means_verified': len(means), 'primary_contrasts_verified': len(contrasts),
              'nominal95_intervals_verified': 140, 'bonferroni_family95_intervals_verified': 30,
              'summary_numeric_values_compared': numeric, 'largest_summary_absolute_discrepancy': summary_error,
              'bootstrap_draws': 20000, 'bootstrap_seed': 20261031, 'bootstrap_rng': 'PCG64',
              'bootstrap_query_indices_sha256': index_sha, 'bootstrap_values_compared': boot.size,
              'largest_bootstrap_absolute_discrepancy': bootstrap_error,
              'bootstrap_recomputation': 'Independent direct indexed query-row averaging, shared indices; mapping seeds averaged first',
              'primary_family_outcomes': dict(effects), 'primary_family_outcomes_by_pair': by_pair,
              'primary_effects': [{'pair': r['pair'], 'budget': r['budget'], 'baseline': r['right'],
                                   'delta': r['ndcg10']['delta'], 'family_ci': r['ndcg10']['ci_bonferroni_family95'],
                                   'outcome': r['ndcg10']['family_interval_interpretation']} for r in contrasts],
              'scorer_completed_artifact_hashes_verified': len(complete['artifact_sha256']),
              'backup_files_locally_rehashed': len(ev.rehashed),
              'backup_bytes_locally_rehashed': sum(v['bytes'] for v in ev.rehashed.values()),
              'large_files_transport_coverage_bindings': len(ev.transport_only),
              'large_bytes_transport_coverage_bindings': sum(v['bytes'] for v in ev.transport_only.values()),
              'preserved_failure_paths': failure_paths, 'nonempty_stderr_evidence': stderr,
              'local_saved_qrel_reads': 1, 'new_network_qrel_opening': False, 'new_fitting': False, 'new_search': False,
              'limitations': ['Large vectors/checkpoints are bound to terminal backup coverage hashes and sizes, not independently rehashed or regenerated in this local QA.',
                              'Exact retrieval was separately regenerated remotely before labels; local QA checks that seal and all cell bindings, without recomputing float32 scores/ties.',
                              'Timestamps and first-opening receipts establish recorded order, not an independent audit of every possible human/data access.',
                              'No universal win, native-reference superiority, independent two-step necessity, ANN, physical-cost, isolated hardware performance or systems claim follows.'],
              'tolerance': 1e-12, 'python_version': sys.version, 'numpy_version': np.__version__,
              'verifier_sha256': sha(Path(__file__)), 'wall_seconds': time.perf_counter() - started,
              'next_action': 'STOP after B2 verified results, figures and ARIS review; manuscript untouched'}
    if bundle is not None:
        result['compact_bundle'] = verify_bundle(Path(bundle), ev)
    result['wall_seconds'] = time.perf_counter() - started
    qa = Path(qa)
    qa.parent.mkdir(parents=True, exist_ok=True)
    with qa.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'qa': str(qa), 'metric_max_error': metric_error,
                      'summary_max_error': summary_error, 'bootstrap_max_error': bootstrap_error,
                      'outcomes': dict(effects), 'seconds': result['wall_seconds']}), flush=True)
    return result


def verify_bundle(bundle, ev):
    bundle = bundle.resolve()
    manifest_path = bundle / 'bundle_manifest.json'
    manifest = read(manifest_path)
    require(manifest['scientific_code_commit'] == '26feef1026bea610ec7f53d581c3c9064949d004',
            'Compact scientific source commit')
    byte_count, coverage_count, authority_count = 0, 0, 0
    for relative, spec in manifest['files'].items():
        path = (bundle / relative).resolve()
        require(path.is_relative_to(bundle) and path.is_file(), 'Compact path missing/escape')
        require(path.stat().st_size == spec['bytes'] and sha(path) == spec['sha256'],
                'Compact hash/size drift: ' + relative)
        byte_count += spec['bytes']
        if relative.startswith('authority/'):
            original = relative[len('authority/'):]
            require(hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() ==
                    hashlib.sha256((ROOT / original).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                    'Compact authority differs from local source: ' + relative)
            authority_count += 1
        else:
            original = ev.relative(spec['path'])
            require(original == relative and original in ev.coverage, 'Compact original path binding')
            stored = ev.coverage[original]
            require(stored['sha256'] == spec['sha256'] and stored['bytes'] == spec['bytes'],
                    'Compact differs from terminal coverage')
            coverage_count += 1
    require(len(manifest['files']) == manifest['file_count'] and byte_count == manifest['bytes'],
            'Compact manifest totals')
    for relative, spec in manifest['omitted_large_inputs_and_fit_artifacts'].items():
        stored = ev.coverage[relative]
        require(stored['sha256'] == spec['sha256'] and stored['bytes'] == spec['bytes'],
                'Omitted large artifact transport coverage')
    return {'path': str(bundle), 'manifest_sha256': sha(manifest_path),
            'files_verified': manifest['file_count'], 'bytes_verified': byte_count,
            'coverage_bound_files': coverage_count, 'authority_files': authority_count,
            'omitted_large_artifacts_transport_bound': len(manifest['omitted_large_inputs_and_fit_artifacts'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backup', type=Path, default=Path('D:/ARC2-B2-backup-20261031'))
    parser.add_argument('--bundle', type=Path)
    parser.add_argument('--qa', type=Path)
    args = parser.parse_args()
    qa = args.qa or ROOT / ('results/b2_review_20261101/qa_completed_' +
                          datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    verify(args.backup, qa, args.bundle)
