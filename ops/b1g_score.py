"""Post-seal, CPU-only DEV scoring for the finite B1-G diagnostic campaign.

Both shards must be complete before cached DEV labels can be opened. This
process neither fits nor ranks galleries and never reads Mini source vectors.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import signal
import sys
import time
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'ops'))

from arc2_global.diagnostics import sha256, write_json, save_array, assert_cpu_only
from b1a_stage import Observations
from b1g_stage import (DATASETS, IDENTITY, checked_spec, read_json, inside, relative,
    check_sources, runtime, source_inventory, registry_for, artifact_hashes, require_tracked)
from b1m_score import metrics_for, load_qrels, synthetic_checks as metric_checks

METRICS = ('ndcg10', 'recall100')
SEEDS = (17, 29, 41, 53, 67)


def verify_ranking(path, ids):
    ranks = np.load(path, allow_pickle=False)
    docs, queries = ids['doc_ids'], ids['query_ids']
    if ranks.shape != (len(queries), 100) or ranks.dtype.kind not in 'iu':
        raise ValueError('Invalid sealed integer top-100 ranking')
    if np.any(ranks < 0) or np.any(ranks >= len(docs)):
        raise ValueError('Sealed ranking outside document population')
    if np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0):
        raise ValueError('Duplicate returned document')
    lookup = {doc: index for index, doc in enumerate(docs)}
    for index, query in enumerate(queries):
        if query in lookup and np.any(ranks[index] == lookup[query]):
            raise ValueError('Identical-ID document was returned')
    return ranks


def verify_shard(run, shard, registry, lock, commit, expected_seal_sha=None):
    """Validate portable sealed bytes; do not reopen registry vector paths."""
    run = Path(run).resolve(strict=True)
    seal_path = run / 'diagnostics_seal.json'
    seal_sha = sha256(seal_path)
    if expected_seal_sha is not None and seal_sha != expected_seal_sha:
        raise ValueError('Shard seal changed during scoring')
    seal, meta = read_json(seal_path), read_json(run / 'metadata.json')
    expected_lock = lock['_sha256']
    entry = lock['registries'][shard]
    if (seal.get('status'), seal.get('shard'), seal.get('code_commit'), seal.get('lock_sha256'), seal.get('registry_sha256')) != (
            'B1G_DIAGNOSTICS_SEALED', shard, commit, expected_lock, entry['sha256']):
        raise ValueError('Incomplete/incompatible shard seal')
    if (meta.get('status'), meta.get('diagnostics_seal_sha256'), meta.get('code_commit'), meta.get('lock_sha256')) != (
            'B1G_FULL_PASS', seal_sha, commit, expected_lock):
        raise ValueError('Shard must have completed successfully after sealing')
    if (seal.get('expected_groups'), seal.get('expected_cases')) != (entry['groups'], entry['cases']):
        raise ValueError('Shard sealed counts differ from lock')
    if seal.get('qrels_read') is not False or seal.get('new_fits') != 0 or seal.get('new_physical_document_encodes') != 0:
        raise ValueError('Shard purity receipt failed')
    if seal.get('source_inventory') != source_inventory(registry):
        raise ValueError('Shard source verification receipt differs from immutable registry')
    if sha256(run / 'source_registry.json') != entry['sha256'] or sha256(run / 'source_lock.json') != expected_lock:
        raise ValueError('Portable registry/lock differs from source')
    artifacts = seal['artifact_sha256']
    if not artifacts or artifact_hashes(run) != artifacts:
        raise ValueError('Portable sealed artifact population or hashes changed')
    contexts = seal['contexts']
    if len(contexts) != len(registry['contexts']):
        raise ValueError('Context receipt count differs from registry')
    for source, copied in zip(registry['contexts'], contexts):
        if copied['source'] != source or copied['sha256'] != source['sha256']:
            raise ValueError('Portable context identity differs from original')
        if sha256(inside(run, copied['copied_path'])) != source['sha256']:
            raise ValueError('Portable context changed')
    expected = {group['group_id']: group for group in registry['groups']}
    actual = seal['groups']
    if len(actual) != len(expected) or len({group['group_id'] for group in actual}) != len(actual):
        raise ValueError('Group population missing or duplicated')
    ids_by_dataset, groups, total = {}, [], 0
    for group in actual:
        original = expected.get(group['group_id'])
        if original is None or any(group.get(key) != original[key] for key in IDENTITY):
            raise ValueError('Sealed gallery identity changed')
        ids_path = inside(run, group['ids'])
        if sha256(ids_path) != original['ids']['sha256'] or group['ids_sha256'] != original['ids']['sha256']:
            raise ValueError('Portable ID hash changed')
        raw_ids = read_json(ids_path)
        ids = {name: raw_ids[name] for name in ('doc_ids', 'query_ids')}
        for name in ('doc_ids', 'query_ids'):
            values = ids[name]
            if not values or len(set(values)) != len(values) or any(not isinstance(value, str) or not value for value in values):
                raise ValueError('Invalid or duplicate portable IDs')
        if group['dataset'] in ids_by_dataset and ids_by_dataset[group['dataset']] != ids:
            raise ValueError('Dataset ID order differs across galleries')
        ids_by_dataset[group['dataset']] = ids
        for name, digest_name, source in [('anchors', 'anchors_sha256', original['anchors'])]:
            if group[digest_name] != source['sha256'] or sha256(inside(run, group[name])) != source['sha256']:
                raise ValueError('Portable selection identity changed')
        required = [group['before'], group['ids'], group['anchors'], group['sample_positions'],
                    group['proxy_sample'], group['target_sample']]
        if sha256(inside(run, group['sample_positions'])) != group['sample_sha256']:
            raise ValueError('Sample identity changed')
        folder = run / 'groups' / group['group_id']
        if read_json(folder / 'rank/metadata.json')['status'] != 'B1G_RANK_PASS' or read_json(folder / 'analyzer/metadata.json')['status'] != 'B1G_ANALYZER_PASS':
            raise ValueError('Worker incomplete')
        expected_cases = {case['case_id']: case for case in original['cases']}
        if len(group['cases']) != len(expected_cases) or len({c['case_id'] for c in group['cases']}) != len(expected_cases):
            raise ValueError('Sealed cases missing or duplicated')
        verify_ranking(inside(run, group['before']), ids)
        for case in group['cases']:
            previous = expected_cases.get(case['case_id'])
            if previous is None or case['budget'] != previous['budget']:
                raise ValueError('Sealed case identity changed')
            if case['paid_sha256'] != previous['paid']['sha256'] or sha256(inside(run, case['paid'])) != previous['paid']['sha256']:
                raise ValueError('Portable paid IDs differ from source')
            if case['published_ranking_sha256'] != previous['published_ranking']['sha256'] or sha256(inside(run, case['after'])) != case['after_sha256']:
                raise ValueError('Post-replacement ranking/source parity receipt changed')
            if read_json(inside(run, case['ranking_diagnostics'])).get('published_ranking_parity') is not True:
                raise ValueError('Missing exact published ranking array parity')
            verify_ranking(inside(run, case['after']), ids)
            required.extend(case[key] for key in ('paid', 'after', 'ranking_diagnostics', 'paired_diagnostics'))
            case['published_ranking_sha256'] = previous['published_ranking']['sha256']
        if any(path not in artifacts for path in required):
            raise ValueError('Required artifact absent from seal')
        groups.append((run, group, ids))
        total += len(group['cases'])
    if total != entry['cases']:
        raise ValueError('Sealed case total mismatch')
    return {'shard': shard, 'run': str(run), 'seal_sha256': seal_sha,
            'groups': groups, 'ids': ids_by_dataset}


def verify_population(shards):
    groups = [item for shard in shards for item in shard['groups']]
    if len(groups) != 210 or sum(len(group['cases']) for _, group, _ in groups) != 450:
        raise ValueError('Require exactly 210 fitted galleries and 450 partial cases')
    keys, cases, ids = [], [], {}
    for _, group, group_ids in groups:
        keys.append(tuple(group[key] for key in IDENTITY[1:]))
        cases.extend(case['case_id'] for case in group['cases'])
        dataset = group['dataset']
        if dataset in ids and ids[dataset] != group_ids:
            raise ValueError('Portable IDs differ between shards')
        ids[dataset] = group_ids
    if len(set(keys)) != len(keys) or len(set(cases)) != len(cases) or set(ids) != set(DATASETS):
        raise ValueError('Campaign identity collision or incomplete DEV population')
    for dataset, values in ids.items():
        if len(values['query_ids']) != (500 if dataset == 'FiQA' else 50):
            raise ValueError('Unexpected locked DEV query count')
    return groups, ids


def historical_lookup(lock):
    """Read previously inspected metrics only within the post-seal process."""
    lookup = {}
    receipts = []
    for spec in lock.get('historical_metrics', []):
        index_path, array_path = checked_spec(spec['cell_index']), checked_spec(spec['per_query'])
        index, array = read_json(index_path), np.load(array_path, allow_pickle=False)
        if index['metrics'] != list(METRICS) or array.ndim != 3 or array.shape[2] != 2:
            raise ValueError('Historical metric axes differ from unchanged scorer')
        for cell in index['cells']:
            row = cell.get('per_dataset_index', cell.get('per_query_index'))
            if not isinstance(row, int) or not 0 <= row < len(array):
                raise ValueError('Historical per-query row missing/out of range')
            key = (cell['dataset'], cell['ranking_sha256'])
            value = {'values': array[row], 'query_ids': index['query_ids'],
                     'source': str(index_path), 'row': row}
            if key in lookup:
                if lookup[key]['query_ids'] != value['query_ids'] or not np.array_equal(lookup[key]['values'], value['values']):
                    raise ValueError('Historical metrics conflict for identical ranking')
            else:
                lookup[key] = value
        receipts.append({'cell_index': spec['cell_index'], 'per_query': spec['per_query'], 'rows': len(array)})
    return lookup, receipts


def signed_summary(values):
    values = np.asarray(values, dtype=np.float64)
    return {'mean': float(values.mean()), 'std': float(values.std(ddof=0)),
            'min': float(values.min()), 'max': float(values.max()),
            'positive': int(np.count_nonzero(values > 0)), 'zero': int(np.count_nonzero(values == 0)),
            'negative': int(np.count_nonzero(values < 0)), 'observations': int(values.size)}


def descriptive_case(run, group, case, before, after, delta):
    ranking = read_json(inside(run, case['ranking_diagnostics']))
    paired = read_json(inside(run, case['paired_diagnostics']))
    if ranking['published_ranking_parity'] is not True or paired['case_id'] != case['case_id']:
        raise ValueError('Diagnostic identity/parity failed')
    row = {**{key: group[key] for key in IDENTITY}, 'case_id': case['case_id'], 'budget': case['budget'],
        'metrics': {name: {'before': float(before[:, i].mean()), 'after': float(after[:, i].mean()),
                           'delta': signed_summary(delta[:, i])} for i, name in enumerate(METRICS)},
        'counts': ranking['counts'], 'population_fractions': ranking['population_fractions'],
        'returned_shares': {endpoint: {top: {name: value['mean'] for name, value in stats.items()}
            for top, stats in ranking[endpoint].items()} for endpoint in ('before', 'after')},
        'rank_changes': {top: {name: value for name, value in stats.items() if not name.endswith('_per_query')}
                         for top, stats in ranking['changes'].items()},
        'sample_documents': paired['sample_documents'],
        'paired_strata': {stratum: {key: value for key, value in stats.items() if not key.startswith('per_query_')}
                          for stratum, stats in paired['strata'].items()},
        'proxy_direction': paired['proxy_direction'], 'true_direction': paired['true_direction'],
        'diagnostic_sources': {'run': str(run), 'ranking': case['ranking_diagnostics'], 'paired': case['paired_diagnostics']}}
    return row


def aggregate_cases(rows):
    families = {}
    for row in rows:
        key = tuple(str(row[name]) for name in ('dataset', 'pair', 'method', 'regime', 'budget'))
        families.setdefault(key, []).append(row)
    aggregates = []
    for key, values in sorted(families.items()):
        if sorted(value['seed'] for value in values) != list(SEEDS):
            raise ValueError('Every reported condition must retain all five seeds')
        aggregate = {name: values[0][name] for name in ('dataset', 'pair', 'method', 'regime', 'budget')}
        aggregate['seeds'] = list(SEEDS)
        aggregate['metrics'] = {}
        for name in METRICS:
            before = [value['metrics'][name]['before'] for value in values]
            after = [value['metrics'][name]['after'] for value in values]
            delta = [value['metrics'][name]['delta']['mean'] for value in values]
            aggregate['metrics'][name] = {'before': signed_summary(before), 'after': signed_summary(after),
                                          'delta_of_query_means': signed_summary(delta)}
        aggregate['paired_signed_bias'] = {stratum: signed_summary([v['paired_strata'][stratum]['signed_bias'] for v in values])
            if all(v['paired_strata'][stratum]['signed_bias'] is not None for v in values) else None
            for stratum in ('all', 'anchor', 'paid_nonanchor', 'unpaid')}
        aggregate['paid_returned_share'] = {endpoint: {top: signed_summary([v['returned_shares'][endpoint][top]['paid'] for v in values])
            for top in ('top10', 'top100')} for endpoint in ('before', 'after')}
        aggregates.append(aggregate)
    return aggregates


def markdown(summary):
    lines = ['# B1-G mixed-gallery development diagnostics', '',
        'All 450 partial cases and 210 pristine fitted galleries are retained. '
        'Labels are the four previously inspected DEV collections. These are descriptive diagnostics; '
        'no calibration, new fit, significance test or confidence interval was selected.', '',
        'Metric delta is after true-vector replacement minus pristine proxy retrieval. '
        'nDCG@10 uses graded gain; Recall@100 retains all positive qrels in its denominator. '
        'All 500 FiQA or 50 Nano queries count, including queries without positive judgments.', '',
        'Returned paid/proxy imbalance alone does not establish miscalibration. '
        'Paired score error is proxy minus true score on the same fixed 512 sampled documents. '
        'Reference vectors did not enter pristine ranking, paid selection, fitting or cost.', '',
        '| Dataset | Pair | Method | Regime | Budget | nDCG before | after | delta | Recall before | after | delta |',
        '|---|---|---|---|---|---:|---:|---:|---:|---:|---:|']
    for row in summary['aggregate_five_seed_conditions']:
        n, r = row['metrics']['ndcg10'], row['metrics']['recall100']
        lines.append('| ' + ' | '.join([str(row[key]) for key in ('dataset', 'pair', 'method', 'regime', 'budget')] +
            [f"{n['before']['mean']:.8f}", f"{n['after']['mean']:.8f}", f"{n['delta_of_query_means']['mean']:+.8f}",
             f"{r['before']['mean']:.8f}", f"{r['after']['mean']:.8f}", f"{r['delta_of_query_means']['mean']:+.8f}"]) + ' |')
    lines.extend(['', 'Every case, both delta signs, per-query arrays, paired error quantiles and score/direction statistics '
        'are retained in results_summary.json, per-dataset metric artifacts and the two immutable shard bundles.', '',
        'STOP: analyze B1-G with B1-M/B1-P and record D1. No automatic breadth, TREC or systems run.', ''])
    return '\n'.join(lines)


def run(args):
    out = Path(args.output).resolve()
    if out.parent != (ROOT / 'results').resolve() or not out.name.startswith('b1g_'):
        raise ValueError('Require a new direct results/b1g_* scoring output directory')
    out.mkdir(parents=True, exist_ok=False)
    began = time.perf_counter()
    lock_path = Path(args.lock).resolve()
    metadata = {'status': 'RUNNING', 'code_commit': args.code_commit, 'lock_sha256': sha256(lock_path),
        'started_unix': time.time(), 'failures': [], 'dev_qrel_access_started': False,
        'new_fits': 0, 'new_physical_document_encodes': 0, 'artificial_time_or_memory_caps': None}
    write_json(out / 'metadata.json', metadata)
    monitor = Observations(out)
    monitor.begin()
    def terminated(signum, frame):
        raise InterruptedError('Received signal ' + str(signum))
    previous = signal.signal(signal.SIGTERM, terminated)
    try:
        lock = read_json(lock_path)
        lock['_sha256'] = metadata['lock_sha256']
        require_tracked(lock_path)
        check_sources(lock, args.code_commit)
        metadata['runtime'] = runtime(lock)
        registries = {shard: registry_for(lock, shard)[0] for shard in ('main', 'mini')}
        shards = [verify_shard(path, shard, registries[shard], lock, args.code_commit)
                  for path, shard in ((args.main_run, 'main'), (args.mini_run, 'mini'))]
        groups, ids = verify_population(shards)
        # Main paths are local; Mini vectors remain on Mini and are represented
        # by its immutable pre-score inventory and verified portable context.
        for source, digest in source_inventory(registries['main']).items():
            checked_spec({'path': source, 'sha256': digest})
        if set(lock['qrels']) != set(DATASETS):
            raise ValueError('Only the four locked DEV qrel caches are permitted')
        for dataset, source in lock['qrels'].items():
            if 'url' in source or source['format'] not in ('tsv', 'parquet'):
                raise ValueError('Scoring requires local cached TSV/parquet qrels; network is forbidden')
            if dataset != 'FiQA' and (source['format'], source.get('implicit_binary_grade')) != ('parquet', 1):
                raise ValueError('Nano requires unchanged explicit published binary-pair semantics')
        history, history_receipts = historical_lookup(lock)
        write_json(out / 'synthetic_metric_checks.json', metric_checks())
        receipt = {'first_dev_qrel_open_unix': time.time(), 'code_commit': args.code_commit,
            'lock_sha256': metadata['lock_sha256'], 'shards': [{key: item[key] for key in ('shard', 'run', 'seal_sha256')} for item in shards],
            'complete_gallery_groups': len(groups), 'complete_partial_cases': 450, 'expected_sources': lock['qrels'],
            'exposure': 'Previously inspected DEV only; no independent confirmation',
            'historical_metrics': history_receipts}
        # Durable receipt precedes every qrel open/hash, including local caches.
        write_json(out / 'first_dev_qrel_open.json', receipt)
        metadata['dev_qrel_access_started'] = True
        write_json(out / 'metadata.json', metadata)
        qrels, qrel_stats = {}, []
        for dataset in DATASETS:
            qrels[dataset], stats = load_qrels(dataset, lock['qrels'][dataset], out,
                (ids[dataset]['doc_ids'], ids[dataset]['query_ids']), 'first_dev_qrel_open.json')
            qrel_stats.append(stats)
        arrays, indices, rows, parity = {}, {}, [], []
        for dataset in DATASETS:
            arrays[dataset] = {'before': [], 'after': [], 'delta': []}
            indices[dataset] = {'pure': [], 'cases': []}
        for run_path, group, group_ids in groups:
            dataset = group['dataset']
            pure = metrics_for(np.load(inside(run_path, group['before']), allow_pickle=False),
                               group_ids['doc_ids'], group_ids['query_ids'], qrels[dataset])
            pure_index = len(arrays[dataset]['before'])
            arrays[dataset]['before'].append(pure)
            indices[dataset]['pure'].append({**{key: group[key] for key in IDENTITY}, 'before_index': pure_index,
                                            'ranking_sha256': sha256(inside(run_path, group['before']))})
            for case in group['cases']:
                after = metrics_for(np.load(inside(run_path, case['after']), allow_pickle=False),
                                    group_ids['doc_ids'], group_ids['query_ids'], qrels[dataset])
                delta = after - pure
                case_index = len(arrays[dataset]['after'])
                arrays[dataset]['after'].append(after)
                arrays[dataset]['delta'].append(delta)
                indices[dataset]['cases'].append({**{key: group[key] for key in IDENTITY},
                    'case_id': case['case_id'], 'budget': case['budget'], 'before_index': pure_index,
                    'after_delta_index': case_index, 'published_ranking_sha256': case['published_ranking_sha256']})
                row = descriptive_case(run_path, group, case, pure, after, delta)
                rows.append(row)
                if lock.get('historical_metrics'):
                    key = (dataset, case['published_ranking_sha256'])
                    if key not in history:
                        raise ValueError('Mixed ranking lacks historical metric link: ' + case['case_id'])
                    saved = history[key]
                    if saved['query_ids'] != group_ids['query_ids']:
                        raise ValueError('Historical query order changed')
                    np.testing.assert_allclose(after, saved['values'], rtol=0, atol=1e-12)
                    parity.append({'case_id': case['case_id'], 'source': saved['source'], 'row': saved['row'],
                        'max_absolute_error': float(np.max(np.abs(after - saved['values'])))})
            write_json(out / 'progress.json', {'status': 'DEV_SCORING', 'pure_galleries_scored': sum(len(v['before']) for v in arrays.values()),
                'partial_cases_scored': len(rows), 'updated_unix': time.time()})
        if sum(len(v['before']) for v in arrays.values()) != 210 or len(rows) != 450:
            raise ValueError('Incomplete scoring population')
        for dataset in DATASETS:
            folder = out / dataset
            folder.mkdir()
            for name, values in arrays[dataset].items():
                save_array(folder / (name + '_per_query.npy'), np.stack(values))
            write_json(folder / 'cell_index.json', {'axes': ['cell', 'query', 'metric'], 'metrics': list(METRICS),
                'query_ids': ids[dataset]['query_ids'], 'pure_cells': indices[dataset]['pure'],
                'partial_cases': indices[dataset]['cases'], 'delta_definition': 'after minus before',
                'before_reuse': 'each unique fitted gallery scored once; cases index its pure before row'})
        summary = {'status': 'B1G_DEV_SCORED', 'code_commit': args.code_commit, 'lock_sha256': metadata['lock_sha256'],
            'partial_cases': 450, 'pure_fitted_galleries': 210, 'metrics': list(METRICS), 'qrel_stats': qrel_stats,
            'historical_metric_parity': parity, 'case_diagnostics_and_metrics': rows,
            'aggregate_five_seed_conditions': aggregate_cases(rows),
            'limits': ['inspected development evidence', 'descriptive; no calibration or new CIs/significance',
                'returned-share imbalance alone is not proof of miscalibration',
                'reference target sample excluded from fit, selection and pristine rank worker'],
            'next_action': 'STOP after B1-G analysis and ARIS/D1 record; no automatic breadth/TREC/systems'}
        # Reverify all source, contexts and both complete sealed bundles before
        # publishing a completed result. Mini vector paths are never reopened.
        check_sources(lock, args.code_commit)
        if sha256(lock_path) != metadata['lock_sha256']:
            raise ValueError('Lock changed during scoring')
        for shard in shards:
            registry, _ = registry_for(lock, shard['shard'])
            verify_shard(shard['run'], shard['shard'], registry, lock, args.code_commit, shard['seal_sha256'])
        for source, digest in source_inventory(registries['main']).items():
            checked_spec({'path': source, 'sha256': digest})
        for source in lock['qrels'].values():
            checked_spec(source)
        for spec in lock.get('historical_metrics', []):
            checked_spec(spec['cell_index'])
            checked_spec(spec['per_query'])
        assert_cpu_only()
        write_json(out / 'results_summary.json', summary)
        (out / 'results_summary.md').write_text(markdown(summary), encoding='utf-8', newline='\n')
        write_json(out / 'completed.json', {'status': 'B1G_DEV_SCORED', 'completed_unix': time.time(),
            'code_commit': args.code_commit, 'lock_sha256': metadata['lock_sha256'],
            'source_shards': receipt['shards'], 'first_dev_qrel_open_sha256': sha256(out / 'first_dev_qrel_open.json'),
            'artifact_sha256': artifact_hashes(out)})
        metadata.update(status='B1G_DEV_SCORED', completed_sha256=sha256(out / 'completed.json'))
        write_json(out / 'progress.json', {'status': 'B1G_DEV_SCORED', 'pure_galleries_scored': 210,
            'partial_cases_scored': 450, 'updated_unix': time.time()})
    except BaseException as exc:
        metadata.update(status='FAILED_PRESERVED', traceback=traceback.format_exc())
        metadata['failures'].append({'type': type(exc).__name__, 'message': str(exc)})
        write_json(out / 'failure.json', {'status': 'FAILED_PRESERVED', 'error': repr(exc),
            'traceback': metadata['traceback'], 'dev_qrel_access_started': metadata['dev_qrel_access_started']})
    finally:
        signal.signal(signal.SIGTERM, previous)
        monitor.end()
        metadata.update(ended_unix=time.time(), wall_seconds=time.perf_counter() - began,
                        peak_process_tree_rss_bytes=monitor.peak)
        write_json(out / 'metadata.json', metadata)
    print(json.dumps({'status': metadata['status'], 'output': str(out), 'failures': metadata['failures']}))
    return 0 if metadata['status'] == 'B1G_DEV_SCORED' else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--main-run', type=Path, required=True)
    parser.add_argument('--mini-run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    return run(parser.parse_args())


if __name__ == '__main__':
    raise SystemExit(main())
