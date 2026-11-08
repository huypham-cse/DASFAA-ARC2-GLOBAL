"""Verify portable B1-G bundles and extract descriptive evidence, without qrels.

This is computational consistency QA, not an independent label validation or
formal paper-claim audit. It never opens remote source paths or qrel files.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import time
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'ops'))
from arc2_global.diagnostics import (sha256, positions, ranking_diagnostics,
    paired_diagnostics, assert_cpu_only)
from b1g_stage import read_json, inside, artifact_hashes, document_sample
from b1g_score import verify_shard, verify_population

CODE_COMMIT = '515b3d10b8c09f1900c5215b5b709b47830f3236'
DATASETS = ('NanoNQ', 'NanoHotpotQA', 'NanoFEVER', 'FiQA')
METRICS = ('ndcg10', 'recall100')
IDENTITY = ('group_id', 'dataset', 'pair', 'method', 'seed', 'regime')
FAMILY = ('dataset', 'pair', 'method', 'regime', 'budget')
SEEDS = (17, 29, 41, 53, 67)
TOLERANCE = 1e-12


def windows_long_path(path):
    """Use extended absolute input roots before opening deeply nested exports."""
    absolute = os.path.abspath(os.path.expanduser(os.fspath(path)))
    if os.name != 'nt' or absolute.startswith('\\\\?\\'):
        return Path(absolute)
    if absolute.startswith('\\\\'):
        return Path('\\\\?\\UNC\\' + absolute[2:])
    return Path('\\\\?\\' + absolute)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exclusive_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


class Comparison:
    def __init__(self):
        self.numeric_values = 0
        self.largest_absolute_error = 0.0

    def compare(self, actual, expected, where):
        if isinstance(expected, dict):
            require(isinstance(actual, dict) and actual.keys() == expected.keys(), 'Keys differ: ' + where)
            for key in expected:
                self.compare(actual[key], expected[key], where + '/' + str(key))
        elif isinstance(expected, (list, tuple)):
            require(isinstance(actual, (list, tuple)) and len(actual) == len(expected), 'Length differs: ' + where)
            for index, value in enumerate(expected):
                self.compare(actual[index], value, where + '/' + str(index))
        elif isinstance(expected, (float, int, np.number)) and not isinstance(expected, (bool, np.bool_)):
            require(isinstance(actual, (float, int, np.number)) and not isinstance(actual, (bool, np.bool_)), 'Numeric type differs: ' + where)
            error = abs(float(actual) - float(expected))
            require(np.isfinite(error) and error <= TOLERANCE, f'Numeric discrepancy {where}: {error}')
            self.numeric_values += 1
            self.largest_absolute_error = max(self.largest_absolute_error, error)
        else:
            require(actual == expected, 'Value differs: ' + where)

    def array(self, actual, expected, where):
        a, b = np.asarray(actual), np.asarray(expected)
        require(a.shape == b.shape, 'Array shape differs: ' + where)
        require(np.isfinite(a).all() and np.isfinite(b).all(), 'Nonfinite array: ' + where)
        error = float(np.max(np.abs(a.astype(np.float64) - b.astype(np.float64)))) if a.size else 0.0
        require(error <= TOLERANCE, f'Array discrepancy {where}: {error}')
        self.numeric_values += int(a.size)
        self.largest_absolute_error = max(self.largest_absolute_error, error)


def signed_summary(values):
    """Independent arithmetic for the predeclared descriptive fields."""
    a = np.asarray(values, dtype=np.float64)
    require(a.size > 0 and np.isfinite(a).all(), 'Empty/nonfinite summary input')
    mean = float(np.sum(a) / a.size)
    return {'mean': mean, 'std': float(np.sqrt(np.sum((a - mean) ** 2) / a.size)),
            'min': float(np.min(a)), 'max': float(np.max(a)),
            'positive': int(np.sum(a > 0)), 'zero': int(np.sum(a == 0)),
            'negative': int(np.sum(a < 0)), 'observations': int(a.size)}


def verify_sources(lock):
    observed = {}
    for relative, expected in lock['source_sha256_canonical_lf'].items():
        path = inside(ROOT, relative)
        digest = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        require(digest == expected, 'Frozen scientific source changed: ' + relative)
        observed[relative] = digest
    return observed


def normalized_scorer_source(locked_path, remote_checkout):
    """Resolve frozen relative specs in the recorded Linux checkout, never locally."""
    source = PurePosixPath(locked_path)
    require('..' not in source.parts, 'Historical source cannot escape its checkout')
    if source.is_absolute():
        return str(source)
    require(remote_checkout is not None, 'Relative historical source requires the sealed remote checkout')
    checkout = PurePosixPath(remote_checkout)
    require(checkout.is_absolute(), 'Recorded remote checkout must be absolute POSIX')
    return str(checkout / source)


def local_history(lock, b1m, b1p, remote_checkout=None):
    """Map the five locked metric hash pairs to explicit local copies."""
    candidates = [(Path(b1m) / dataset / 'cell_index.json', Path(b1m) / dataset / 'per_query.npy')
                  for dataset in DATASETS]
    candidates.append((Path(b1p) / 'cell_index.json', Path(b1p) / 'per_query.npy'))
    expected = {(spec['cell_index']['sha256'], spec['per_query']['sha256']): spec
                for spec in lock['historical_metrics']}
    require(len(expected) == 5, 'Require all five locked historical metric sources')
    seen, lookup, receipts = set(), {}, []
    for index_path, array_path in candidates:
        digests = (sha256(index_path), sha256(array_path))
        require(digests in expected and digests not in seen, 'Historical copy differs from locked source: ' + str(index_path))
        seen.add(digests)
        index, array = read_json(index_path), np.load(array_path, allow_pickle=False)
        require(index['metrics'] == list(METRICS) and array.shape == (len(index['cells']), len(index['query_ids']), 2), 'Historical metric axes differ')
        if 'shape' in index:
            require(list(array.shape) == index['shape'], 'Historical declared shape differs')
        require(array.ndim == 3 and array.shape[2] == 2 and np.isfinite(array).all(), 'Historical metric array invalid')
        for cell in index['cells']:
            row = cell.get('per_dataset_index', cell.get('per_query_index'))
            require(isinstance(row, int) and 0 <= row < len(array), 'Historical metric row invalid')
            key = (cell['dataset'], cell['ranking_sha256'])
            value = {'values': array[row], 'query_ids': index['query_ids'], 'row': row,
                     'locked_source': normalized_scorer_source(expected[digests]['cell_index']['path'], remote_checkout),
                     'locked_source_specification': expected[digests]['cell_index'], 'local_source': str(index_path.resolve())}
            if key in lookup:
                require(lookup[key]['query_ids'] == value['query_ids'] and np.array_equal(lookup[key]['values'], value['values']),
                        'Historical sources disagree for identical ranking')
            else:
                lookup[key] = value
        receipts.append({'cell_index': str(index_path.resolve()), 'cell_index_sha256': digests[0],
                         'per_query': str(array_path.resolve()), 'per_query_sha256': digests[1], 'rows': len(array),
                         'locked_cell_index_specification': expected[digests]['cell_index'],
                         'normalized_scorer_source': normalized_scorer_source(expected[digests]['cell_index']['path'], remote_checkout)})
    require(seen == set(expected), 'Historical source population incomplete')
    return lookup, receipts


def verify_runtime_receipt(metadata, lock):
    recorded = metadata['runtime']
    require(recorded['numpy'] == lock['cpu_versions']['numpy'] and recorded['scipy'] == lock['cpu_versions']['scipy']
            and recorded['sklearn'] == lock['cpu_sklearn_version'] and recorded['environment'] == lock['cpu_environment']
            and recorded['executable'] == lock['cpu_python'], 'Execution numerical runtime receipt differs')
    require(metadata['new_fits'] == metadata['new_physical_document_encodes'] == 0
            and metadata['artificial_time_or_memory_caps'] is None, 'Execution scope/resource receipt differs')


def verify_scoring_envelope(scoring, shards, lock, commit):
    completed, metadata = read_json(scoring / 'completed.json'), read_json(scoring / 'metadata.json')
    require(completed['status'] == metadata['status'] == 'B1G_DEV_SCORED', 'Scoring is incomplete')
    verify_runtime_receipt(metadata, lock)
    require(metadata['dev_qrel_access_started'] is True, 'Scoring parse state receipt differs')
    require(metadata['completed_sha256'] == sha256(scoring / 'completed.json'), 'Scoring completion changed')
    for value in (completed, metadata):
        require(value['code_commit'] == commit and value['lock_sha256'] == lock['_sha256'], 'Scoring binding differs')
    observed = artifact_hashes(scoring)
    observed.pop('completed.json', None)
    require(observed == completed['artifact_sha256'], 'Completed scorer artifact hashes/population changed')
    first = read_json(scoring / 'first_dev_qrel_open.json')
    require(sha256(scoring / 'first_dev_qrel_open.json') == completed['first_dev_qrel_open_sha256'], 'Pre-parse receipt changed')
    require(first['code_commit'] == commit and first['lock_sha256'] == lock['_sha256'], 'Pre-parse binding differs')
    require(first['complete_gallery_groups'] == 210 and first['complete_partial_cases'] == 450, 'Incomplete pre-parse population')
    require(first['expected_sources'] == lock['qrels'], 'Recorded label sources differ from lock')
    require(first['shards'] == completed['source_shards'], 'Scoring shard receipts disagree')
    expected = {shard['shard']: shard['seal_sha256'] for shard in shards}
    recorded = {item['shard']: item['seal_sha256'] for item in first['shards']}
    require(len(first['shards']) == 2 and expected == recorded, 'Scoring did not bind both downloaded seals')
    first_time = first['first_dev_qrel_open_unix']
    for shard in shards:
        require(read_json(Path(shard['run']) / 'diagnostics_seal.json')['sealed_unix'] <= first_time, 'Label access preceded shard seal')
    for dataset, source in lock['qrels'].items():
        # These are metadata receipts only. The recorded qrel paths are never opened.
        access = read_json(scoring / ('qrel_access_' + dataset + '.json'))
        verified = read_json(scoring / ('qrel_verified_' + dataset + '.json'))
        require(access['expected_source'] == source and access['dataset'] == verified['dataset'] == dataset, 'Label receipt identity differs')
        require(access['first_access_receipt'] == 'first_dev_qrel_open.json', 'Label receipt is not linked to current parse')
        require(datetime.fromisoformat(access['first_dev_qrel_open']).timestamp() >= first_time, 'Loader receipt preceded pre-parse receipt')
        require(verified['sha256'] == source['sha256'] and verified['implicit_binary_grade'] == source.get('implicit_binary_grade'), 'Label verification receipt differs')
        if 'bytes' in source:
            require(verified['bytes'] == source['bytes'], 'Label byte receipt differs')
    require(completed['completed_unix'] >= first_time, 'Completion predates parse receipt')
    return completed, first


def inspect_worker_requests(run, group, original, lock):
    folder = run / 'groups' / group['group_id']
    rank = read_json(folder / 'rank_request.json')
    analyzer = read_json(folder / 'analyzer_request.json')
    require(set(rank) == {'output', *IDENTITY, 'old_docs', 'new_queries', 'ids', 'sample_positions', 'anchors', 'proxy', 'cases'}, 'Rank request scope changed')
    require(set(analyzer) == {'output', 'group_id', 'dataset', 'pair', 'seed', 'regime', 'proxy_sample', 'target_sample', 'new_queries', 'sample_positions', 'anchors', 'cases'}, 'Analyzer request scope changed')
    require(all(rank[key] == group[key] for key in IDENTITY)
            and all(analyzer[key] == group[key] for key in ('group_id', 'dataset', 'pair', 'seed', 'regime')), 'Worker gallery identity differs')
    intermediate_receipt = read_json(run / 'execution_intermediates.json')
    require(intermediate_receipt['excluded_prefix'] == 'execution_paid_targets/', 'Execution tensor exclusion scope differs')
    intermediates = {value['sha256']: value for value in intermediate_receipt['files']}
    require(all(value['path'].startswith('execution_paid_targets/') and value['portable'] is False
                and value['retained_in_remote_raw_run'] is True for value in intermediates.values()), 'Intermediate preservation receipt differs')
    require(rank['old_docs'] == original['old_docs'] and rank['new_queries'] == analyzer['new_queries'] == original['new_queries']
            and rank['proxy'] == original['proxy'], 'Worker frozen source identity changed')
    require(rank['ids']['sha256'] == original['ids']['sha256'] and rank['anchors']['sha256'] == original['anchors']['sha256'], 'Worker copied IDs/anchors changed')
    require(rank['sample_positions']['sha256'] == analyzer['sample_positions']['sha256'] == group['sample_sha256'], 'Worker sample identity changed')
    require(analyzer['proxy_sample']['sha256'] == sha256(inside(run, group['proxy_sample']))
            and analyzer['target_sample']['sha256'] == sha256(inside(run, group['target_sample'])), 'Analyzer paired sample changed')
    rank_meta = read_json(folder / 'rank/metadata.json')
    analyzer_meta = read_json(folder / 'analyzer/metadata.json')
    forbidden = {original['full_target_reference']['path'], *(spec['path'] for spec in lock['qrels'].values())}
    require(not forbidden.intersection(rank_meta['input_hashes']) and not forbidden.intersection(analyzer_meta['input_hashes']), 'Forbidden reference/labels entered a worker')
    for value in (rank_meta, analyzer_meta):
        require(value['qrels_read'] is False and value['new_fits'] == value['new_physical_document_encodes'] == 0, 'Worker purity receipt differs')
    expected = {case['case_id']: case for case in original['cases']}
    require(len(rank['cases']) == len(analyzer['cases']) == len(expected), 'Worker case population differs')
    for case in rank['cases']:
        source = expected[case['case_id']]
        require(set(case) == {'case_id', 'budget', 'paid', 'paid_targets', 'published_ranking'}, 'Rank case request scope changed')
        require(case['budget'] == source['budget'] and case['paid']['sha256'] == source['paid']['sha256']
                and case['published_ranking'] == source['published_ranking'], 'Rank case source differs')
        intermediate = intermediates[case['paid_targets']['sha256']]
        require(intermediate['source_full_target']['sha256'] == original['full_target_reference']['sha256']
                and intermediate['source_paid']['sha256'] == source['paid']['sha256'] and intermediate['dtype'] == 'float32', 'Paid target materialization source differs')
    for case in analyzer['cases']:
        require(set(case) == {'case_id', 'paid'} and case['paid']['sha256'] == expected[case['case_id']]['paid']['sha256'], 'Analyzer paid selection differs')


def condensed_case(run, group, case, before, after, delta, ranking, paired):
    return {**{name: group[name] for name in IDENTITY}, 'case_id': case['case_id'], 'budget': case['budget'],
        'metrics': {name: {'before': float(before[:, i].mean()), 'after': float(after[:, i].mean()),
                           'delta': signed_summary(delta[:, i])} for i, name in enumerate(METRICS)},
        'counts': ranking['counts'], 'population_fractions': ranking['population_fractions'],
        'returned_shares': {endpoint: {top: {name: value['mean'] for name, value in values.items()}
            for top, values in ranking[endpoint].items()} for endpoint in ('before', 'after')},
        'rank_changes': {top: {name: value for name, value in values.items() if not name.endswith('_per_query')}
            for top, values in ranking['changes'].items()},
        'sample_documents': paired['sample_documents'],
        'paired_strata': {stratum: {name: value for name, value in values.items() if not name.startswith('per_query_')}
            for stratum, values in paired['strata'].items()},
        'proxy_direction': paired['proxy_direction'], 'true_direction': paired['true_direction'],
        'diagnostic_sources': {'run': str(run), 'ranking': case['ranking_diagnostics'], 'paired': case['paired_diagnostics']}}


def aggregate_cases(rows):
    families = {}
    for row in rows:
        families.setdefault(tuple(str(row[key]) for key in FAMILY), []).append(row)
    result = []
    for key in sorted(families):
        rows_for_family = families[key]
        require(sorted(row['seed'] for row in rows_for_family) == list(SEEDS), 'Five-seed condition incomplete')
        result.append({**{name: rows_for_family[0][name] for name in FAMILY}, 'seeds': list(SEEDS),
            'metrics': {name: {**{endpoint: signed_summary([row['metrics'][name][endpoint] for row in rows_for_family]) for endpoint in ('before', 'after')},
                              'delta_of_query_means': signed_summary([row['metrics'][name]['delta']['mean'] for row in rows_for_family])} for name in METRICS},
            'paired_signed_bias': {stratum: signed_summary([row['paired_strata'][stratum]['signed_bias'] for row in rows_for_family])
                if all(row['paired_strata'][stratum]['signed_bias'] is not None for row in rows_for_family) else None
                for stratum in ('all', 'anchor', 'paid_nonanchor', 'unpaid')},
            'paid_returned_share': {endpoint: {top: signed_summary([row['returned_shares'][endpoint][top]['paid'] for row in rows_for_family])
                for top in ('top10', 'top100')} for endpoint in ('before', 'after')}})
    return result


def extraction(rows, aggregates):
    families = {}
    for row in rows:
        families.setdefault(tuple(str(row[key]) for key in FAMILY), []).append(row)
    result = []
    for aggregate in aggregates:
        family = sorted(families[tuple(str(aggregate[key]) for key in FAMILY)], key=lambda row: row['seed'])
        require(len({row['population_fractions']['paid'] for row in family}) == 1, 'Population fraction differs across seeds')
        result.append({**aggregate, 'population_paid_fraction': family[0]['population_fractions']['paid'],
            'per_seed_existing_diagnostics': [{
                'seed': row['seed'], 'case_id': row['case_id'],
                'all_mae': row['paired_strata']['all']['mae'], 'all_rmse': row['paired_strata']['all']['rmse'],
                'unpaid_mae': row['paired_strata']['unpaid']['mae'], 'unpaid_rmse': row['paired_strata']['unpaid']['rmse'],
                'all_score_std_ratio': row['paired_strata']['all']['score_std_ratio'],
                'unpaid_score_std_ratio': row['paired_strata']['unpaid']['score_std_ratio'],
                'sample_proxy_true_cosine_mean': row['paired_strata']['all']['proxy_true_cosine']['mean'],
                'proxy_mean_direction_norm': row['proxy_direction']['mean_direction_norm'],
                'true_mean_direction_norm': row['true_direction']['mean_direction_norm'],
                'top10_intersection_over_k': row['rank_changes']['top10']['mean_intersection_over_k'],
                'top100_intersection_over_k': row['rank_changes']['top100']['mean_intersection_over_k']}
                for row in family]})
    return result


def report_markdown(result):
    lines = ['# B1-G local verification and descriptive extraction', '',
        f"Verified {result['pure_fitted_galleries']} pristine galleries, {result['partial_cases']} mixed cases and {result['five_seed_conditions']} five-seed conditions.", '',
        'All mixed per-query metrics match the five frozen historical metric files by dataset, ranking hash and query order. '
        'Means, signed after-minus-before deltas, seed SD/ranges and all saved ranking/paired diagnostics were recomputed. '
        'No qrels, remote inputs, new fits or new inferential statistics were used.', '',
        'This is computational consistency QA of inspected DEV evidence. It is not independent label validation or a formal paper-claim audit. '
        'Paid-share imbalance alone is not proof of miscalibration; paired score error remains descriptive.', '',
        '| Dataset | Pair | Method | Regime | Budget | nDCG before | after | delta | Recall delta |',
        '|---|---|---|---|---|---:|---:|---:|---:|']
    for row in result['descriptive_extraction']:
        metrics = row['metrics']; ndcg = metrics['ndcg10']
        lines.append('| ' + ' | '.join([str(row[key]) for key in FAMILY] +
            [f"{ndcg['before']['mean']:.8f}", f"{ndcg['after']['mean']:.8f}", f"{ndcg['delta_of_query_means']['mean']:+.8f}",
             f"{metrics['recall100']['delta_of_query_means']['mean']:+.8f}"]) + ' |')
    lines.extend(['', '| Dataset | Pair | Method | Regime | Budget | Paid population | Paid top10 before | after | Paired bias all | unpaid |',
        '|---|---|---|---|---|---:|---:|---:|---:|---:|'])
    for row in result['descriptive_extraction']:
        def fmt(value):
            return 'null' if value is None else f"{value['mean']:+.8f}"
        lines.append('| ' + ' | '.join([str(row[key]) for key in FAMILY] +
            [f"{row['population_paid_fraction']:.8f}", f"{row['paid_returned_share']['before']['top10']['mean']:.8f}",
             f"{row['paid_returned_share']['after']['top10']['mean']:.8f}", fmt(row['paired_signed_bias']['all']),
             fmt(row['paired_signed_bias']['unpaid'])]) + ' |')
    lines.extend(['', 'The JSON receipt also retains every existing per-seed MAE/RMSE, score-STD ratio, sampled vector cosine, '
        'direction norm and rank-overlap value. No favorable cases are filtered.', '',
        'STOP after B1-G/ARIS interpretation and the D1 recommendation. No automatic TREC, breadth or systems run.', ''])
    return '\n'.join(lines)


def verify(args):
    began = time.perf_counter()
    # Prefix only input bundle roots. Receipt/report paths remain ordinary paths.
    for name in ('main_run', 'mini_run', 'scoring', 'b1m_scoring', 'b1p_scoring'):
        setattr(args, name, windows_long_path(getattr(args, name)))
    lock_path, scoring = Path(args.lock).resolve(), Path(args.scoring).resolve()
    lock = read_json(lock_path)
    lock['_sha256'] = sha256(lock_path)
    source_hashes = verify_sources(lock)
    # A malformed export must be rejected by name before any raw label file
    # could be hashed as an unexpected artifact. JSON access receipts are metadata.
    for root in (Path(args.main_run), Path(args.mini_run), scoring):
        for path in root.rglob('*'):
            require(not ('qrel' in path.name.lower() and path.suffix.lower() in ('.parquet', '.tsv', '.csv', '.jsonl')),
                    'Raw qrel file is forbidden in a portable QA input: ' + str(path))
    shards, registries = [], {}
    for name, path in (('main', args.main_run), ('mini', args.mini_run)):
        run = Path(path).resolve()
        registry_path = run / 'source_registry.json'
        require(sha256(registry_path) == lock['registries'][name]['sha256'], 'Portable registry differs from lock')
        registry = read_json(registry_path)
        registries[name] = registry
        shards.append(verify_shard(run, name, registry, lock, args.code_commit))
        generation_metadata = read_json(run / 'metadata.json')
        verify_runtime_receipt(generation_metadata, lock)
        require(generation_metadata['stage'] == 'full' and generation_metadata['shard'] == name
                and generation_metadata['qrels_read'] is False, 'Generation stage/purity receipt differs')
        seal = read_json(run / 'diagnostics_seal.json')
        require(seal['portable_excluded_prefix'] == 'execution_paid_targets/'
                and seal['execution_intermediates'] == read_json(run / 'execution_intermediates.json')['files'], 'Intermediate inventories disagree')
    groups, ids = verify_population(shards)
    completed, first = verify_scoring_envelope(scoring, shards, lock, args.code_commit)
    remote_main_run = PurePosixPath(next(item['run'] for item in first['shards'] if item['shard'] == 'main'))
    require(remote_main_run.is_absolute() and remote_main_run.parent.name == 'results', 'Recorded Main run must be inside its Linux checkout/results')
    remote_checkout = remote_main_run.parent.parent
    history, history_receipts = local_history(lock, args.b1m_scoring, args.b1p_scoring, remote_checkout)
    summary = read_json(scoring / 'results_summary.json')
    require((summary['status'], summary['code_commit'], summary['lock_sha256'], summary['partial_cases'], summary['pure_fitted_galleries'], summary['metrics']) ==
        ('B1G_DEV_SCORED', args.code_commit, lock['_sha256'], 450, 210, list(METRICS)), 'Summary binding/population differs')
    comparison = Comparison()
    saved_cases = {row['case_id']: row for row in summary['case_diagnostics_and_metrics']}
    require(len(saved_cases) == len(summary['case_diagnostics_and_metrics']) == 450, 'Summary case population differs')
    expected_groups = {group['group_id']: (run, group, group_ids) for run, group, group_ids in groups}
    expected_cases = {case['case_id']: (run, group, case, group_ids) for run, group, group_ids in groups for case in group['cases']}
    indexed_groups, indexed_cases, recomputed_rows, parity = set(), set(), [], []
    arrays_by_dataset, shapes = {}, {}
    for dataset in DATASETS:
        folder = scoring / dataset
        index = read_json(folder / 'cell_index.json')
        require(index['axes'] == ['cell', 'query', 'metric'] and index['metrics'] == list(METRICS)
                and index['query_ids'] == ids[dataset]['query_ids'] and index['delta_definition'] == 'after minus before', 'Scoring metric axes differ')
        arrays = {name: np.load(folder / (name + '_per_query.npy'), allow_pickle=False) for name in ('before', 'after', 'delta')}
        q = len(index['query_ids'])
        require(arrays['before'].shape == (len(index['pure_cells']), q, 2)
                and arrays['after'].shape == arrays['delta'].shape == (len(index['partial_cases']), q, 2), 'Scoring metric shape differs')
        require(all(value.dtype == np.float64 and np.isfinite(value).all() for value in arrays.values()), 'Metrics must be finite float64')
        require(all(np.all((arrays[name] >= 0) & (arrays[name] <= 1 + TOLERANCE)) for name in ('before', 'after')), 'Quality metrics outside range')
        arrays_by_dataset[dataset] = arrays
        shapes[dataset] = {name: list(value.shape) for name, value in arrays.items()}
        pure_rows = {}
        for row_position, cell in enumerate(index['pure_cells']):
            gid = cell['group_id']
            require(gid in expected_groups and gid not in indexed_groups and cell['before_index'] == row_position, 'Pure gallery indexing differs')
            run, group, group_ids = expected_groups[gid]
            require(all(cell[key] == group[key] for key in IDENTITY) and group['dataset'] == dataset
                    and cell['ranking_sha256'] == sha256(inside(run, group['before'])), 'Pure gallery source differs')
            indexed_groups.add(gid)
            pure_rows[gid] = arrays['before'][row_position]
            original = next(item for registry in registries.values() for item in registry['groups'] if item['group_id'] == gid)
            inspect_worker_requests(run, group, original, lock)
            sample = positions(np.load(inside(run, group['sample_positions']), allow_pickle=False), 'sample', group['documents'], nonempty=True)
            require(np.array_equal(sample, document_sample(group_ids, dataset, lock['sample'])), 'Fixed sample differs from ID-hash rule')
            anchors = positions(np.load(inside(run, group['anchors']), allow_pickle=False), 'anchors', group['documents'], nonempty=True)
            require(len(anchors) == group['anchor_count'] == 1024, 'Anchor population differs')
            proxy = np.load(inside(run, group['proxy_sample']), allow_pickle=False)
            target = np.load(inside(run, group['target_sample']), allow_pickle=False)
            proxy_scores = np.load(run / 'groups' / gid / 'analyzer/proxy_scores.npy', allow_pickle=False)
            true_scores = np.load(run / 'groups' / gid / 'analyzer/true_scores.npy', allow_pickle=False)
            require(proxy.shape == target.shape and len(proxy) == 512 and proxy.dtype == target.dtype == np.float32, 'Paired sample vector shape/dtype differs')
            require(proxy_scores.shape == true_scores.shape == (q, 512) and proxy_scores.dtype == true_scores.dtype == np.float32
                    and np.isfinite(proxy_scores).all() and np.isfinite(true_scores).all(), 'Paired score array invalid')
            for vectors in (proxy, target):
                require(np.isfinite(vectors).all() and np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-4, rtol=0), 'Sample vector units invalid')
            group['_verification'] = (sample, anchors, proxy, target, proxy_scores, true_scores)
        for row_position, cell in enumerate(index['partial_cases']):
            cid = cell['case_id']
            require(cid in expected_cases and cid not in indexed_cases and cell['after_delta_index'] == row_position, 'Mixed case indexing differs')
            run, group, case, group_ids = expected_cases[cid]
            require(group['dataset'] == dataset and all(cell[key] == group[key] for key in IDENTITY) and cell['budget'] == case['budget']
                    and cell['published_ranking_sha256'] == case['published_ranking_sha256'], 'Mixed case source differs')
            require(index['pure_cells'][cell['before_index']]['group_id'] == group['group_id'], 'Mixed case points to another pure gallery')
            indexed_cases.add(cid)
            before, after, delta = pure_rows[group['group_id']], arrays['after'][row_position], arrays['delta'][row_position]
            comparison.array(delta, after - before, cid + '/delta')
            saved = history[(dataset, case['published_ranking_sha256'])]
            require(saved['query_ids'] == group_ids['query_ids'], 'Historical query order differs')
            comparison.array(after, saved['values'], cid + '/historical_metrics')
            parity.append({'case_id': cid, 'source': saved['locked_source'], 'row': saved['row'],
                'max_absolute_error': float(np.max(np.abs(after - saved['values'])))})
            sample, anchors, proxy, target, ps, ts = group['_verification']
            paid = positions(np.load(inside(run, case['paid']), allow_pickle=False), 'paid', group['documents'])
            require(np.isin(anchors, paid).all() and len(paid) == case['paid_count'], 'Unique paid encoding accounting differs')
            budget = int(str(case['budget']).removesuffix('pct')) / 100
            require(len(paid) == int(np.floor(budget * group['documents'])), 'Paid encoding count differs from budget')
            ranking = ranking_diagnostics(np.load(inside(run, group['before']), allow_pickle=False), np.load(inside(run, case['after']), allow_pickle=False),
                n_docs=group['documents'], anchors=anchors, paid=paid)
            ranking.update(case_id=cid, budget=case['budget'], published_ranking_parity=True)
            comparison.compare(read_json(inside(run, case['ranking_diagnostics'])), ranking, cid + '/ranking_diagnostics')
            paired = paired_diagnostics(ps, ts, proxy, target, sample, anchors, paid)
            paired['case_id'] = cid
            comparison.compare(read_json(inside(run, case['paired_diagnostics'])), paired, cid + '/paired_diagnostics')
            row = condensed_case(run, group, case, before, after, delta, ranking, paired)
            # Recorded run paths refer to remote locations; every actual relative
            # diagnostic path is independently verified against the local seal.
            row['diagnostic_sources']['run'] = saved_cases[cid]['diagnostic_sources']['run']
            comparison.compare(saved_cases[cid], row, cid + '/summary')
            recomputed_rows.append(row)
    require(len(indexed_groups) == 210 and len(indexed_cases) == 450, 'Scoring does not cover the entire sealed campaign')
    aggregates = aggregate_cases(recomputed_rows)
    require(len(aggregates) == 90, 'Expected exactly 90 five-seed conditions')
    comparison.compare(summary['aggregate_five_seed_conditions'], aggregates, 'five_seed_conditions')
    parity_by_case = {row['case_id']: row for row in summary['historical_metric_parity']}
    require(len(parity_by_case) == len(summary['historical_metric_parity']) == 450, 'Historical parity receipt incomplete')
    for row in parity:
        comparison.compare(parity_by_case[row['case_id']], row, row['case_id'] + '/parity_receipt')
    comparison.compare(summary['qrel_stats'], [read_json(scoring / ('qrel_verified_' + dataset + '.json')) for dataset in DATASETS], 'qrel_receipt_stats')
    assert_cpu_only()
    return {'status': 'PASS', 'verified_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Computational consistency QA of inspected DEV artifacts; no independent label validation or formal paper-claim audit',
        'code_commit': args.code_commit, 'lock_sha256': lock['_sha256'],
        'main_run': str(Path(args.main_run).resolve()), 'mini_run': str(Path(args.mini_run).resolve()), 'scoring': str(scoring),
        'seal_sha256': {shard['shard']: shard['seal_sha256'] for shard in shards}, 'completed_sha256': sha256(scoring / 'completed.json'),
        'portable_shard_files_verified': sum(len(read_json(Path(shard['run']) / 'diagnostics_seal.json')['artifact_sha256']) for shard in shards),
        'scoring_files_verified': len(completed['artifact_sha256']), 'frozen_source_sha256_canonical_lf': source_hashes,
        'pure_fitted_galleries': 210, 'partial_cases': 450, 'five_seed_conditions': 90,
        'historical_metric_cells_verified': 450, 'before_after_delta_arrays': shapes,
        'ranking_diagnostics_recomputed': 450, 'paired_score_diagnostics_recomputed': 450,
        'local_historical_sources': history_receipts, 'numeric_values_compared': comparison.numeric_values,
        'largest_absolute_discrepancy': comparison.largest_absolute_error, 'tolerance': TOLERANCE,
        'local_qrel_reads': 0, 'remote_source_reads': 0, 'new_fits': 0, 'new_significance_tests_or_intervals': 0,
        'numpy_version': np.__version__, 'verifier_sha256': sha256(Path(__file__)),
        'descriptive_extraction': extraction(recomputed_rows, aggregates), 'wall_seconds': time.perf_counter() - began}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    bundle = ROOT / 'results/b1g_r1_review_20261027'
    parser.add_argument('--main-run', type=Path, default=bundle / 'main')
    parser.add_argument('--mini-run', type=Path, default=bundle / 'mini')
    parser.add_argument('--scoring', type=Path, default=bundle / 'scoring')
    parser.add_argument('--lock', type=Path, default=ROOT / 'configs/b1g_lock.json')
    parser.add_argument('--code-commit', default=CODE_COMMIT)
    parser.add_argument('--b1m-scoring', type=Path, default=ROOT / 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary')
    parser.add_argument('--b1p-scoring', type=Path, default=ROOT / 'results/b1p_r5_review_20261027/scoring')
    parser.add_argument('--receipt', type=Path, default=ROOT / 'provenance/qa/b1g_completed_verification_r2_20261027.json',
                        help='New exclusive JSON QA/extraction receipt')
    parser.add_argument('--report', type=Path, help='Optional new exclusive Markdown extraction')
    args = parser.parse_args()
    require(not args.receipt.exists() and (args.report is None or not args.report.exists()), 'Outputs must be new; earlier QA is preserved')
    try:
        result = verify(args)
        if args.report is not None:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            with args.report.open('x', encoding='utf-8', newline='\n') as stream:
                stream.write(report_markdown(result))
            result['report'] = {'path': str(args.report.resolve()), 'sha256': sha256(args.report)}
        exclusive_json(args.receipt, result)
        print(json.dumps({key: result[key] for key in ('status', 'partial_cases', 'pure_fitted_galleries', 'five_seed_conditions', 'largest_absolute_discrepancy')}))
        return 0
    except BaseException as error:
        exclusive_json(args.receipt, {'status': 'FAILED_PRESERVED', 'error': repr(error), 'traceback': traceback.format_exc(),
            'local_qrel_reads': 0, 'remote_source_reads': 0, 'verifier_sha256': sha256(Path(__file__))})
        raise


if __name__ == '__main__':
    raise SystemExit(main())
