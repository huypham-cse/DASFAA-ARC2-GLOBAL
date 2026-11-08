"""Verify a relocated ARC2 review release offline, without Git or original paths.

Hashes mode requires Python's standard library only. Full mode additionally
requires NumPy/PyArrow. It independently rescores all B1c/B2 raw rankings from
the bundled ordered IDs and saved qrels, recomputes both locked bootstraps,
and checks frozen outcomes, including retained negative evidence. It never
invokes a scientific scorer, fits a model, searches vectors, or writes results.
Only an exclusive new JSON receipt below checks/ is written.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
import traceback

sys.dont_write_bytecode = True
TOLERANCE = 1e-12
B1C_REVIEW = 'results/b1c_r3_review_20261031'
B2_REVIEW = 'results/b2_review_20261101'
B2_RUN = 'results/b2_full_r1_20261031t064859'


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def inside(root, relative):
    root = Path(root).resolve()
    relative = str(relative)
    require(relative and not Path(relative).is_absolute() and ':' not in relative
            and '\\' not in relative and '..' not in Path(relative).parts,
            'Require portable relative path: ' + relative)
    path = (root / relative).resolve()
    require(path != root and path.is_relative_to(root), 'Path escapes release: ' + relative)
    return path


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def manifest_check(root):
    path = root / 'RELEASE_MANIFEST.json'
    manifest = read(path)
    files = manifest['files']
    require(isinstance(files, dict) and files, 'Empty release manifest')
    byte_count = 0
    for relative, spec in files.items():
        item = inside(root, relative)
        require(item.is_file() and item.stat().st_size == spec['bytes']
                and sha(item) == spec['sha256'], 'Release hash/size mismatch: ' + relative)
        byte_count += spec['bytes']
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
              and not any(part in {'checks', '.venv', '__pycache__'} for part in p.relative_to(root).parts)
              and p.name != 'RELEASE_MANIFEST.json'}
    checksum_path = root / 'CHECKSUMS.sha256'
    checksum_declared = 'CHECKSUMS.sha256 (derived)' in manifest.get('excluded_from_manifest', [])
    checksum_info = None
    if checksum_declared:
        require(checksum_path.is_file() and 'CHECKSUMS.sha256' not in files,
                'Declared checksum sidecar must exist outside the manifest hash cycle')
        observed = {}
        for line in checksum_path.read_text(encoding='utf-8').splitlines():
            require(len(line) > 66 and line[64:66] == '  ', 'Invalid SHA256 index line')
            digest, relative = line[:64], line[66:]
            require(all(c in '0123456789abcdef' for c in digest) and relative not in observed,
                    'Invalid/duplicate checksum index entry')
            inside(root, relative)
            observed[relative] = digest
        expected = {relative: spec['sha256'] for relative, spec in files.items()}
        expected['RELEASE_MANIFEST.json'] = sha(path)
        require(observed == expected, 'Derived SHA256 index differs from exact release file/manifest hashes')
        checksum_info = {'sha256': sha(checksum_path), 'entries_verified': len(observed),
                         'scope': 'Exactly manifested files plus RELEASE_MANIFEST.json; sidecar excludes itself'}
        actual.discard('CHECKSUMS.sha256')
    require(actual == set(files), 'Release file population differs: ' +
            str({'missing': sorted(set(files) - actual), 'unlisted': sorted(actual - set(files))}))
    require(manifest.get('file_count', len(files)) == len(files)
            and manifest.get('bytes', byte_count) == byte_count, 'Release manifest totals')
    return {'manifest_sha256': sha(path), 'files_verified': len(files), 'bytes_verified': byte_count,
            'derived_checksum_index': checksum_info,
            'scope': 'All manifested files and declared derived SHA256 index; checks/, .venv/ and bytecode caches excluded'}


def compact_check(bundle):
    manifest = read(bundle / 'bundle_manifest.json')
    for relative, spec in manifest['files'].items():
        path = inside(bundle, relative)
        require(path.is_file() and path.stat().st_size == spec['bytes'] and sha(path) == spec['sha256'],
                'Compact manifest differs: ' + str(path))
    actual = {p.relative_to(bundle).as_posix() for p in bundle.rglob('*') if p.is_file()}
    require(actual == set(manifest['files']) | {'bundle_manifest.json'}, 'Compact file population differs')
    return manifest


def check_sources(root, lock):
    sources = lock['source_sha256_canonical_lf']
    for relative, digest in sources.items():
        require(canonical_sha(inside(root, relative)) == digest, 'Canonical-LF source pin differs: ' + relative)
    return len(sources)


def load_helper(root, name):
    path = inside(root, 'tools/' + name + '.py')
    spec = importlib.util.spec_from_file_location('release_' + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Comparison:
    def __init__(self):
        self.numbers = 0
        self.maximum_error = 0.0

    def compare(self, actual, expected, where):
        if isinstance(expected, dict):
            require(isinstance(actual, dict) and actual.keys() == expected.keys(), 'Keys differ: ' + where)
            for name, value in expected.items():
                self.compare(actual[name], value, where + '/' + name)
        elif isinstance(expected, (list, tuple)):
            require(isinstance(actual, (list, tuple)) and len(actual) == len(expected), 'Length differs: ' + where)
            for i, value in enumerate(expected):
                self.compare(actual[i], value, f'{where}/{i}')
        elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
            require(isinstance(actual, (float, int)) and not isinstance(actual, bool), 'Numeric type differs: ' + where)
            error = abs(actual - expected)
            require(math.isfinite(error) and error <= TOLERANCE, 'Number differs: ' + where)
            self.numbers += 1
            self.maximum_error = max(self.maximum_error, error)
        else:
            require(actual == expected, 'Value differs: ' + where)


def interpret(lo, hi):
    return 'above_zero' if lo > 0 else 'below_zero' if hi < 0 else 'unresolved'


def family_outcomes(rows, interval='ci_bonferroni_family95'):
    outcomes = Counter()
    for row in rows:
        stat = row['ndcg10']
        outcome = interpret(*stat[interval])
        require(stat['family_interval_interpretation'] == outcome, 'Family interpretation contradicts interval')
        outcomes[outcome] += 1
    return dict(outcomes)


def validate_ranks(np, ranks, documents, queries):
    require(ranks.shape == (len(queries), 100) and ranks.dtype.kind in 'iu'
            and ranks.min() >= 0 and ranks.max() < len(documents)
            and not np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0), 'Invalid raw top100 ranks')
    positions = {d: i for i, d in enumerate(documents)}
    require(all(positions.get(q, -1) not in ranks[i] for i, q in enumerate(queries)), 'Identical-ID exclusion differs')


def verify_b1c(root, np):
    helper = load_helper(root, 'verify_b1c_r3_completed')
    locked = helper.locked
    locked.ROOT = root
    bundle = inside(root, B1C_REVIEW + '/evidence')
    manifest = compact_check(bundle)
    scoring = bundle / 'run/scoring'
    summary, completed = read(scoring / 'summary.json'), read(scoring / 'completed.json')
    seal, lock = read(bundle / 'run/ranking_seal.json'), read(bundle / 'authority/b1c_r3_lock.json')
    require(summary['status'] == completed['status'] == 'DEV_SCORED' and summary['failures'] == [], 'B1c scoring status')
    require(completed['summary_sha256'] == sha(scoring / 'summary.json'), 'B1c summary binding')
    for relative, digest in completed['artifact_sha256'].items():
        require(sha(inside(scoring, relative)) == digest, 'B1c scorer artifact binding')
    require(sha(bundle / 'run/ranking_seal.json') == summary['ranking_seal_sha256']
            and sha(bundle / 'authority/b1c_r3_lock.json') == summary['lock_sha256'] == seal['lock_sha256']
            and canonical_sha(root / 'configs/b1c_r3_lock.json') == canonical_sha(bundle / 'authority/b1c_r3_lock.json'),
            'B1c lock/ranking seal binding')
    pins = check_sources(root, lock)
    source_spec = locked.source_specifications(lock)
    require(summary['scoring'] == source_spec and summary['bootstrap']['draws'] == 20000
            and summary['bootstrap']['seed'] == 20261028, 'B1c bootstrap policy')
    require(seal['status'] == 'RANKINGS_SEALED' and seal['stage'] == 'B1C_R3'
            and seal['qrels_opened'] is False and seal['ranking_process_qrel_reads'] == 0,
            'B1c prelabel ranking status')
    first = read(scoring / 'first_dev_qrel_open.json')
    require(first['all_736_rankings_sources_and_ids_verified'] is True
            and first['ranking_seal_sha256'] == summary['ranking_seal_sha256']
            and first['lock_sha256'] == summary['lock_sha256']
            and datetime.fromisoformat(seal['sealed_utc']) <
            datetime.fromisoformat(first['first_current_attempt_dev_qrel_access']), 'B1c first-opening recorded order')
    index = read(scoring / 'cell_index.json')
    cells = index['cells']
    locked.check_matrix(cells, locked.expected_keys(), 736, 'portable all736 matrix')
    new = [c for c in cells if c['origin'] == 'new_sealed']
    prior = [c for c in cells if c['origin'] == 'imported_prior']
    locked.check_matrix(new, locked.missing_keys(), 358, 'portable358 new')
    locked.check_matrix(prior, locked.expected_keys() - locked.missing_keys(), 378, 'portable378 prior')
    require(index['metrics'] == ['ndcg10', 'recall100'] and index['axes'] == ['dataset_cell', 'query', 'metric'],
            'B1c metric indexing')
    records = manifest['rankings']
    require(len(records) == 736 and {r['cell_index'] for r in records} == set(range(736))
            and len({r['archive_path'] for r in records}) == 736, 'B1c archived ranking population')
    by_position = {r['cell_index']: r for r in records}
    arrays, ids, metric_count, metric_error, details = {}, {}, 0, 0.0, {}
    for dataset in locked.DATASETS:
        ordered = read(bundle / f'ids/{dataset}.json')
        docs, queries = ordered['doc_ids'], ordered['query_ids']
        require((len(docs), len(queries)) == locked.COUNTS[dataset] and len(set(docs)) == len(docs)
                and len(set(queries)) == len(queries) and index['query_ids'][dataset] == queries
                and sha(bundle / f'ids/{dataset}.json') == seal['inputs'][f'inputs/{dataset}/ids.json'],
                'B1c ordered IDs differ')
        ids[dataset] = docs, queries
        qpath = bundle / 'qrels/FiQA.tsv' if dataset == 'FiQA' else scoring / f'qrels_{dataset}.parquet'
        source = source_spec['datasets'][dataset]
        require(sha(qpath) == source['sha256'] and ('bytes' not in source or qpath.stat().st_size == source['bytes']),
                'B1c qrel hash')
        qrels, columns = helper.independent_qrels(qpath, dataset, source)
        doc_set = set(docs)
        stats = {'dataset': dataset, 'sha256': sha(qpath), 'bytes': qpath.stat().st_size,
                 'columns': columns, 'implicit_binary_grade': source.get('implicit_binary_grade'),
                 'evaluation_queries': len(queries),
                 'queries_without_positive_judgments': sum(not any(r > 0 for r in qrels.get(q, {}).values()) for q in queries),
                 'positive_judgments_outside_corpus_retained_in_denominator': sum(
                     r > 0 and d not in doc_set for q in queries for d, r in qrels.get(q, {}).items()),
                 'qrel_queries_outside_evaluation_set': len(set(qrels) - set(queries))}
        require(stats == summary['qrel_stats'][dataset], 'B1c independently parsed qrel stats')
        saved = np.load(scoring / f'per_query_{dataset}.npy', allow_pickle=False)
        require(saved.shape == (184, len(queries), 2) and np.isfinite(saved).all(), 'B1c per-query shape')
        computed = np.empty_like(saved)
        positions = []
        for i, cell in enumerate(cells):
            if cell['dataset'] != dataset:
                continue
            record = by_position[i]
            path = inside(bundle, record['archive_path'])
            require(record['sha256'] == cell['ranking_sha256'] == sha(path), 'B1c ranking source binding')
            ranks = np.load(path, allow_pickle=False)
            validate_ranks(np, ranks, docs, queries)
            row = cell['per_query_index']
            positions.append(row)
            computed[row] = helper.independent_metrics(ranks, docs, queries, qrels)
        require(sorted(positions) == list(range(184)), 'B1c per-query index population')
        error = float(np.max(np.abs(computed - saved)))
        require(error <= TOLERANCE, 'B1c independent metric discrepancy')
        arrays[dataset] = computed
        metric_count += computed.size
        metric_error = max(metric_error, error)
        details[dataset] = {'ranking_cells': 184, 'queries': len(queries), 'metric_values': computed.size,
                            'max_absolute_error': error}
        print(f'B1c {dataset}:184 raw rankings independently rescored', flush=True)
    require(metric_count == 239200, 'B1c metric population')
    # This locked mathematical summarizer is reused deliberately; no scorer entry
    # point, label loader, network function or original absolute path is called.
    means, contrasts, aggregate, bootstrap = locked.summaries(cells, arrays, ids)
    comparison = Comparison()
    for name, computed in (('means', means), ('condition_contrasts', contrasts), ('aggregate_contrasts', aggregate)):
        comparison.compare(summary[name], computed, 'b1c/' + name)
    comparison.compare(summary['bootstrap']['datasets'], bootstrap, 'b1c/bootstrap/datasets')
    outcomes = family_outcomes(aggregate)
    require(outcomes == {'above_zero': 5}, 'B1c frozen macro claim')
    return {'status': 'PASS', 'summary_sha256': sha(scoring / 'summary.json'),
            'source_pins_verified': pins, 'rankings_independently_rescored': 736,
            'new_rankings': 358, 'retained_rankings': 378, 'metric_values_compared': metric_count,
            'largest_metric_absolute_discrepancy': metric_error, 'metric_details': details,
            'bootstrap_draws': 20000, 'bootstrap_seed': 20261028,
            'bootstrap_recomputation': 'Locked summarizer applied to independently recomputed raw-ranking metrics',
            'query_index_hashes': bootstrap, 'means_verified': len(means), 'condition_contrasts_verified': len(contrasts),
            'macro_contrasts_verified': len(aggregate), 'macro_family_outcomes': outcomes,
            'summary_numeric_values_compared': comparison.numbers,
            'largest_summary_absolute_discrepancy': comparison.maximum_error,
            'exposure': 'Inspected development; no independent confirmation claim'}


def verify_b2(root, np):
    helper = load_helper(root, 'verify_b2_completed')
    bundle = inside(root, B2_REVIEW + '/evidence')
    manifest = compact_check(bundle)
    run = inside(bundle, B2_RUN)
    seal = read(run / 'ranking_seal.json')
    verification = read(run / 'verification/verification_seal.json')
    summary, completed = read(run / 'scoring/summary.json'), read(run / 'scoring/completed.json')
    seal_sha, verification_sha = sha(run / 'ranking_seal.json'), sha(run / 'verification/verification_seal.json')
    lock = read(root / 'configs/b2_lock.json')
    lock_sha = canonical_sha(root / 'configs/b2_lock.json')
    require(summary['status'] == completed['status'] == 'FINAL_SCORED' and summary['failures'] == [], 'B2 scored status')
    require(seal['lock_sha256'] == summary['lock_sha256'] == lock_sha
            and summary['ranking_seal_sha256'] == verification['ranking_seal_sha256'] == seal_sha
            and summary['verification_seal_sha256'] == verification_sha, 'B2 source/seal binding')
    pins = check_sources(root, lock)
    for relative, digest in completed['artifact_sha256'].items():
        require(sha(inside(run / 'scoring', relative)) == digest, 'B2 completed scorer artifact binding')
    require(summary['scoring'] == lock['scoring'] and lock['scoring']['bootstrap_seed'] == 20261031
            and lock['scoring']['bootstrap_draws'] == 20000 and lock['scoring']['contrasts'] == 30
            and lock['scoring']['alpha'] == 0.05, 'B2 frozen scoring policy')
    require(seal['status'] == 'RANKINGS_SEALED' and seal['qrels_opened'] is False
            and seal['ranking_process_qrel_reads'] == 0 and verification['qrels_opened'] is False
            and verification['status'] == 'ENDPOINTS_INDEPENDENTLY_VERIFIED' and verification['failures'] == [],
            'B2 prelabel verification status')
    opening = read(run / 'first_final_qrel_open.json')
    request = read(run / 'scoring/qrel_request_started.json')
    observed = read(run / 'scoring/qrel_observed_hash.json')
    require(opening['ranking_seal_sha256'] == seal_sha and opening['verification_seal_sha256'] == verification_sha
            and opening['lock_sha256'] == lock_sha and opening['all_184_rankings_verified'] is True
            and opening['expected_source'] == request['source'] == observed['source'] == lock['scoring']['qrels']
            and sha(run / 'first_final_qrel_open.json') == completed['first_final_qrel_open_sha256'] ==
            request['first_final_qrel_open_sha256'], 'B2 opening/request source binding')
    times = [seal['sealed_utc'], verification['completed_utc'],
             read(run / 'scoring/started.json')['started_utc'], opening['first_final_qrel_open_utc'],
             request['request_started_utc'], observed['observed_utc'], summary['completed_utc'], completed['completed_utc']]
    require(all(datetime.fromisoformat(a) < datetime.fromisoformat(b) for a, b in zip(times, times[1:])),
            'B2 recorded first-label-opening chronology')
    require(all(x['code_commit'] == seal['code_commit'] for x in (verification, summary, completed, opening)),
            'B2 source commit attestations')
    cells = seal['cells']
    helper.matrix(cells)
    helper.matrix(verification['verified_cells'])
    index = read(run / 'scoring/cell_index.json')
    ids = read(run / 'inputs/ids.json')
    docs, queries = ids['doc_ids'], ids['query_ids']
    require(len(docs) == len(set(docs)) == 171332 and len(queries) == len(set(queries)) == 50
            and index['query_ids'] == queries and index['cells'] == cells, 'B2 ordered ID/cell index')
    for relative, digest in seal['inputs'].items():
        require(sha(inside(run, relative)) == digest, 'B2 sealed ordered IDs/selections')
    qrels, qstats, qrel_rows = helper.independent_qrels(run / 'scoring/qrels_TREC-COVID.tsv')
    doc_set = set(docs)
    qstats.update(evaluation_queries=50,
                  queries_without_positive_judgments=sum(not any(r > 0 for r in qrels.get(q, {}).values()) for q in queries),
                  positive_judgments_outside_corpus_retained_in_denominator=sum(
                      r > 0 and d not in doc_set for q in queries for d, r in qrels.get(q, {}).items()),
                  qrel_queries_outside_evaluation_set=len(set(qrels) - set(queries)))
    require(qstats == summary['qrel_stats'] == read(run / 'scoring/qrel_verified.json'), 'B2 qrel stats')
    records = {helper.key(c): c for c in verification['verified_cells']}
    saved = np.load(run / 'scoring/per_query.npy', allow_pickle=False)
    require(saved.shape == (184, 50, 2) and np.isfinite(saved).all(), 'B2 per-query shape')
    computed = np.empty_like(saved)
    dependencies = seal['endpoint_dependency_sha256']
    omitted = manifest['omitted_large_inputs_and_fit_artifacts']
    remote_project = '/home/jovyan/arc2_b2_20261031/code_26feef1/'
    portable_dependencies, transport_dependencies = 0, 0
    for remote, digest in {**dependencies, **seal['fit_artifact_sha256']}.items():
        require(remote.startswith(remote_project), 'B2 original remote identity prefix')
        relative = remote[len(remote_project):]
        if relative in manifest['files']:
            require(manifest['files'][relative]['sha256'] == digest, 'B2 portable dependency identity')
            portable_dependencies += 1
        else:
            require(relative in omitted and omitted[relative]['sha256'] == digest,
                    'B2 omitted-large dependency transport identity')
            transport_dependencies += 1
    for i, cell in enumerate(cells):
        require(records[helper.key(cell)] == read(run / f'verification/cell_{i:03d}.json'), 'B2 per-cell verifier binding')
        record = records[helper.key(cell)]
        require(record['all_top100_ids_and_order_equal'] is True
                and record['ranking_sha256'] == cell['ranking_sha256']
                and record['endpoint_sha256'] == cell['endpoint_sha256'], 'B2 endpoint/ranking verification binding')
        endpoint_path = inside(run, cell['endpoint_path'])
        require(sha(endpoint_path) == cell['endpoint_sha256'], 'B2 endpoint descriptor hash')
        endpoint = read(endpoint_path)
        require(endpoint['schema'] == 'b2_exact_endpoint_v1' and endpoint['semantics'] == helper.SEMANTICS,
                'B2 exact endpoint semantics')
        require(all(dependencies.get(spec['path']) == spec['sha256'] for spec in endpoint['files'].values()),
                'B2 exact endpoint dependency binding')
        ranks_path = inside(run, cell['ranking_path'])
        require(sha(ranks_path) == cell['ranking_sha256'], 'B2 raw ranking hash')
        ranks = np.load(ranks_path, allow_pickle=False)
        validate_ranks(np, ranks, docs, queries)
        computed[i] = helper.metrics(ranks, docs, queries, qrels)
    metric_error = float(np.max(np.abs(saved - computed)))
    require(metric_error <= TOLERANCE, 'B2 independent metric discrepancy')
    means, contrasts, definitions, boot, indices_sha = helper.independent_summary(cells, computed)
    require(summary['bootstrap']['definitions'] == definitions
            and summary['bootstrap']['query_indices_sha256'] == indices_sha, 'B2 PCG64 query draws identity')
    stored_boot = np.load(run / 'scoring/bootstrap_draws.npy', allow_pickle=False)
    require(stored_boot.shape == boot.shape == (20000, 140), 'B2 shared bootstrap shape')
    bootstrap_error = float(np.max(np.abs(stored_boot - boot)))
    require(bootstrap_error <= TOLERANCE, 'B2 independent bootstrap discrepancy')
    comparison = Comparison()
    comparison.compare(summary['means'], means, 'b2/means')
    comparison.compare(summary['contrasts'], contrasts, 'b2/contrasts')
    outcomes = family_outcomes(contrasts)
    by_pair = {pair: family_outcomes([row for row in contrasts if row['pair'] == pair]) for pair in helper.PAIRS}
    require(outcomes == {'above_zero': 11, 'unresolved': 19}
            and by_pair['minilm_distilroberta'] == {'above_zero': 3, 'unresolved': 12}
            and by_pair['e5_small_base'] == {'above_zero': 8, 'unresolved': 7}, 'B2 frozen condition-specific claims')
    return {'status': 'PASS', 'summary_sha256': sha(run / 'scoring/summary.json'),
            'source_pins_verified': pins, 'rankings_independently_rescored': 184,
            'metric_values_compared': computed.size, 'largest_metric_absolute_discrepancy': metric_error,
            'qrel_rows': qrel_rows, 'bootstrap_draws': 20000, 'bootstrap_seed': 20261031,
            'bootstrap_values_compared': boot.size, 'largest_bootstrap_absolute_discrepancy': bootstrap_error,
            'bootstrap_recomputation': 'Independent direct indexed query-row averaging with shared PCG64 draws',
            'query_indices_sha256': indices_sha, 'means_verified': len(means), 'family_contrasts_verified': len(contrasts),
            'summary_numeric_values_compared': comparison.numbers,
            'largest_summary_absolute_discrepancy': comparison.maximum_error,
            'family_outcomes': outcomes, 'family_outcomes_by_pair': by_pair,
            'portable_endpoint_and_fit_dependencies': portable_dependencies,
            'omitted_large_dependencies_with_transport_hashes_only': transport_dependencies,
            'recorded_timeline_utc': times}


def retained_claim_anchors(root):
    """Check explicit negative/scope anchors, without claiming a fresh B1P/G audit."""
    paths = {
        'B1P': 'results/b1p_r5_review_20261027/scoring/results_summary.json',
        'B1G': 'results/b1g_r1_review_20261027/scoring/results_summary.json',
        'B1M': 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json'}
    p, g, m = (read(inside(root, paths[k])) for k in ('B1P', 'B1G', 'B1M'))
    def unique(rows, predicate):
        selected = [r for r in rows if predicate(r)]
        require(len(selected) == 1, 'Retained evidence anchor identity')
        return selected[0]
    facts = []
    for baseline, expected in (('procrustes_global', -0.0443354790156809),
                               ('la2m20_integration_script_adaptation', -0.03747431937003851)):
        row = unique(p['contrasts'], lambda r: r['pair'] == 'e5_small_base'
                     and r['kind'] == 'arc2_allpaid_vs_baseline_allpaid' and r['right']['method'] == baseline)
        require(abs(row['ndcg10']['delta'] - expected) <= TOLERANCE
                and interpret(*row['ndcg10']['ci_bonferroni_family95']) == 'below_zero', 'B1P retained E5 loss')
        facts.append({'stage': 'B1P', 'claim': 'E5 allpaid ARC2 minus ' + baseline, 'ndcg_delta': expected,
                      'family_ci': row['ndcg10']['ci_bonferroni_family95'], 'outcome': 'below_zero'})
    ridge = unique(p['contrasts'], lambda r: r['pair'] == 'minilm_distilroberta'
                   and r['kind'] == 'arc2_allpaid_vs_baseline_allpaid'
                   and r['right']['method'] == 'ridge_affine_l10_bias_regularized')
    require(interpret(*ridge['ndcg10']['ci_bonferroni_family95']) == 'unresolved', 'B1P unresolved ridge anchor')
    facts.append({'stage': 'B1P', 'claim': 'MiniLM allpaid ARC2 minus ridge remains unresolved',
                  'ndcg_delta': ridge['ndcg10']['delta'], 'family_ci': ridge['ndcg10']['ci_bonferroni_family95']})
    require(g['partial_cases'] == 450 and g['pure_fitted_galleries'] == 210
            and len(g['aggregate_five_seed_conditions']) == 90, 'B1G complete diagnostic scope')
    gallery = unique(g['aggregate_five_seed_conditions'], lambda r: r['dataset'] == 'FiQA'
                     and r['pair'] == 'e5_small_base' and r['method'] == 'arc2_global_tangent2_r1'
                     and r['regime'] == 'allpaid28819' and r['budget'] == '50pct')
    for metric, expected in (('ndcg10', -0.023040768303629045), ('recall100', -0.09467432234432235)):
        delta = gallery['metrics'][metric]['delta_of_query_means']['mean']
        require(abs(delta - expected) <= TOLERANCE, 'B1G retained negative replacement diagnostic')
        facts.append({'stage': 'B1G', 'claim': 'FiQA E5 allpaid ARC2 after-minus-before ' + metric,
                      'delta': delta, 'scope': 'descriptive diagnostic, no confidence interval/causal claim'})
    high_lambda = unique(m['overall_macro'], lambda r: r['left'] == 'tangent2_l100')
    require(abs(high_lambda['ndcg10']['delta'] - -0.00925533869678723) <= TOLERANCE
            and high_lambda['ndcg10']['family_interval_interpretation'] == 'below_zero', 'Retained lambda100 negative')
    one_step = unique(m['overall_macro'], lambda r: r['right'] == 'tangent1_l10')
    require(abs(one_step['ndcg10']['delta'] - 0.006923862939737235) <= TOLERANCE, 'Frozen DEV second-step effect')
    facts.extend([{'stage': 'B1M', 'claim': 'lambda100 minus frozen lambda10', 'ndcg_delta': high_lambda['ndcg10']['delta'],
                   'scope': 'negative DEV sensitivity; no posthoc lambda switch'},
                  {'stage': 'B1M', 'claim': 'two steps minus one step', 'ndcg_delta': one_step['ndcg10']['delta'],
                   'scope': 'DEV mechanism only; B2 does not independently test second-step necessity'}])
    return {'status': 'PASS', 'source_summary_sha256': {k: sha(inside(root, v)) for k, v in paths.items()},
            'scope': 'Manifest-bound historical summaries and explicit claim anchors; no new full B1P/B1G/ablation raw audit',
            'facts': facts}


def run(root, output, mode):
    start = time.perf_counter()
    root = Path(root).resolve()
    output = Path(output)
    output = output.resolve() if output.is_absolute() else inside(root, output.as_posix())
    require(output.is_relative_to(root / 'checks') and output.suffix == '.json' and not output.exists(),
            'Output must be a NEW JSON below release checks/; frozen results are read-only')
    result = {'status': 'RUNNING', 'verified_utc': datetime.now(timezone.utc).isoformat(),
              'mode': mode, 'release_root': str(root), 'verifier_sha256': sha(Path(__file__)),
              'offline': True, 'Git_used': False, 'original_backup_used': False,
              'new_fit': False, 'new_search': False, 'scientific_scorer_invoked': False}
    try:
        result['manifest'] = manifest_check(root)
        print(f"Release hashes PASS:{result['manifest']['files_verified']} files", flush=True)
        if mode == 'full':
            sys.path.insert(0, str(root))
            import numpy as np
            import pyarrow
            # Fail closed if a future helper accidentally requests remote data.
            import socket
            import urllib.request
            def forbidden(*args, **kwargs):
                raise RuntimeError('Network access is forbidden in portable offline verification')
            socket.create_connection = forbidden
            urllib.request.urlopen = forbidden
            result['B1c'] = verify_b1c(root, np)
            result['B2'] = verify_b2(root, np)
            result['retained_claim_anchors'] = retained_claim_anchors(root)
            result['versions'] = {'python': sys.version, 'numpy': np.__version__, 'pyarrow': pyarrow.__version__}
        result['status'] = 'PASS'
        result['limitations'] = [
            'Hashes establish package integrity relative to its manifest, not scientific correctness by themselves.',
            'Full mode recomputes metrics/bootstraps from raw saved rankings; it does not regenerate model fits, encodings or float32 retrieval scores.',
            'Large vectors/checkpoints are intentionally omitted; stored remote/transport hashes are provenance, not locally verified large payloads.',
            'B1c and historical B1M/B1P/B1G remain inspected development evidence. B2 supports its specified fixed-anchor conditions only.',
            'Recorded timestamps/seals are checked, without claiming an independent audit of every possible data access.',
            'No manuscript, universal-win, native-reference superiority, ANN, physical-cost or systems claim is authorized.']
    except Exception as error:
        result.update(status='FAIL', error=repr(error), traceback=traceback.format_exc())
    result['wall_seconds'] = time.perf_counter() - start
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'output': str(output), 'seconds': result['wall_seconds'],
                      **({'error': result['error']} if 'error' in result else {})}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path,
                        help='New JSON below checks/; default uses mode and a unique UTC timestamp')
    parser.add_argument('--mode', choices=('hashes', 'full'), default='full')
    args = parser.parse_args()
    output = args.output or Path('checks') / ('portable_verification_' + args.mode + '_' +
              datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    receipt = run(args.root, output, args.mode)
    raise SystemExit(0 if receipt['status'] == 'PASS' else 1)
