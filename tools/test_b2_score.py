"""Qrel-free synthetic checks for B2's final scoring/verification gates."""
from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'ops'), str(ROOT / 'src')]
import b2_verify as verify
import b2_score as score


class B2ScoreChecks(unittest.TestCase):
    def smoke_fixture(self, run):
        """Twenty real serialized endpoints with deliberate equal-score ties."""
        import b2_stage as stage
        (run / 'inputs').mkdir()
        (run / 'synthetic').mkdir()
        ids = {'doc_ids': [f'd{i:05}' for i in range(2048)], 'query_ids': [f'q{i:05}' for i in range(8)]}
        verify.write_json(run / 'inputs/ids.json', ids)
        ids_spec = stage.filespec(run / 'inputs/ids.json')
        gallery = np.tile(np.array([[1., 0.]], dtype=np.float32), (2048, 1))
        queries = gallery[:8].copy()
        specs = {}
        for label in ('minilm_x', 'distilroberta_y'):
            for role, values in [('docs', gallery), ('queries', queries)]:
                path = run / 'synthetic' / f'{label}_{role}.npy'
                np.save(path, values)
                specs[label, role] = stage.filespec(path)
        selections = stage.prepare_selections(run, 2048, [17], 128)
        anchors, anchor_spec, paid_sets = selections[17]
        ranks = stage.exact_topk(queries, gallery, k=100, query_ids=ids['query_ids'], document_ids=ids['doc_ids'], exclude_identical_ids=True)
        cells, deps, fit_sealed = [], {}, {}
        fit_records = {}
        for method in verify.METHODS:
            names = ['parameters.npz', 'metadata.json']
            if method in ('simplelinear_official_final50_mlp5', 'embedding_converter_paper_spec'):
                names = ['worker_metadata', 'request', 'process_exit', 'refit_checkpoint.pt', 'refit_fit.json', 'paired_source', 'paired_target']
                if method == 'embedding_converter_paper_spec':
                    names += ['selection_checkpoint.pt', 'selection_fit.json']
            artifacts = {}
            directory = run / 'fit' / method
            directory.mkdir(parents=True)
            for name in names:
                path = directory / name
                path.write_bytes(b'synthetic frozen fit artifact')
                spec = stage.filespec(path)
                artifacts[name] = spec
                fit_sealed[spec['path']] = spec['sha256']
            fit_records[method] = {'fit_artifacts': artifacts,
                                   'proxy_sha256': specs['distilroberta_y', 'docs']['sha256'],
                                   'fit_anchor_indices_sha256': anchor_spec['sha256']}
        for i, identity in enumerate(sorted(verify.smoke_keys(), key=str)):
            cell = dict(zip(verify.KEY_FIELDS, identity))
            files = {'ids': ids_spec}
            if cell['budget'] == 'full':
                label = 'minilm_x' if cell['method'] == 'full_x' else 'distilroberta_y'
                files.update(query_vectors=specs[label, 'queries'], native_vectors=specs[label, 'docs'])
                kind, npaid = 'native', 0 if cell['method'] == 'full_x' else 2048
            else:
                paid, paid_spec = paid_sets[int(cell['budget'][:-3])]
                files.update(query_vectors=specs['distilroberta_y', 'queries'], proxy_vectors=specs['distilroberta_y', 'docs'],
                             destination_vectors=specs['distilroberta_y', 'docs'], paid_indices=paid_spec, anchor_indices=anchor_spec)
                kind, npaid = 'mixed', len(paid)
            endpoint_path = run / f'endpoint_{i}.json'
            verify.write_json(endpoint_path, {'schema': 'b2_exact_endpoint_v1', 'kind': kind, 'files': files,
                                             'semantics': verify.SEMANTICS, 'shape': [2048, 2]})
            rank_path = run / f'rank_{i}.npy'
            np.save(rank_path, ranks)
            cell.update(endpoint_path=endpoint_path.name, endpoint_sha256=verify.sha(endpoint_path),
                        ranking_path=rank_path.name, ranking_sha256=verify.sha(rank_path),
                        regime='reference' if kind == 'native' else 'fixed1024',
                        fit_pairs=0 if kind == 'native' else 128, unique_destination_encodings=npaid,
                        fit_receipt=None if kind == 'native' else fit_records[cell['method']])
            cells.append(cell)
            deps.update({s['path']: s['sha256'] for s in files.values()})
        seal = {'status': 'RANKINGS_SEALED', 'mode': 'smoke', 'code_commit': 'fixture', 'lock_sha256': verify.sha(run / 'lock.json'),
                'qrels_opened': False, 'ranking_process_qrel_reads': 0, 'cells': cells, 'encoding_manifest': None,
                'inputs': {p.relative_to(run).as_posix(): verify.sha(p) for p in (run / 'inputs').iterdir()},
                'endpoint_dependency_sha256': deps, 'fit_artifact_sha256': fit_sealed}
        verify.write_json(run / 'ranking_seal.json', seal)
        return seal

    def test_twenty_endpoint_smoke_replay_distinct_seal(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            verify.write_json(run / 'lock.json', {'synthetic': True})
            seal = self.smoke_fixture(run)
            with mock.patch.object(verify, 'committed_context', return_value=({}, 'fixture')):
                verify.run_verify(run / 'lock.json', run, smoke=True)
            self.assertEqual(verify.read_json(run / 'verification/verification_seal.json')['status'], 'B2_ENDPOINT_SMOKE_PASS')
            with self.assertRaises(ValueError):
                verify.verify_seal(run)
            with self.assertRaises(ValueError):
                score.verify_verification(run, seal, verify.sha(run / 'lock.json'), 'fixture')
            self.assertFalse((run / 'first_final_qrel_open.json').exists())

    def test_sealed_wrong_ranking_replay_failure_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            verify.write_json(run / 'lock.json', {'synthetic': True})
            seal = self.smoke_fixture(run)
            cell = seal['cells'][0]
            path = run / cell['ranking_path']
            ranks = np.load(path)
            ranks[:, [0, 1]] = ranks[:, [1, 0]]
            np.save(path, ranks)
            cell['ranking_sha256'] = verify.sha(path)
            (run / 'ranking_seal.json').unlink()
            verify.write_json(run / 'ranking_seal.json', seal)
            with mock.patch.object(verify, 'committed_context', return_value=({}, 'fixture')):
                with self.assertRaises(ValueError):
                    verify.run_verify(run / 'lock.json', run, smoke=True)
            self.assertTrue((run / 'verification/failure.json').exists())
            self.assertTrue(list((run / 'verification').glob('mismatch_*_recomputed.npy')))
            self.assertFalse((run / 'verification/verification_seal.json').exists())
            self.assertFalse((run / 'first_final_qrel_open.json').exists())

    def test_frozen_fit_parameter_tamper_and_missing_coverage_rejected(self):
        for method, artifact in [('procrustes_global', 'parameters.npz'),
                                 ('simplelinear_official_final50_mlp5', 'refit_checkpoint.pt'),
                                 ('embedding_converter_paper_spec', 'selection_checkpoint.pt')]:
            with self.subTest(method=method), tempfile.TemporaryDirectory() as directory:
                run = Path(directory)
                verify.write_json(run / 'lock.json', {'synthetic': True})
                seal = self.smoke_fixture(run)
                cell = next(c for c in seal['cells'] if c['method'] == method)
                spec = cell['fit_receipt']['fit_artifacts'][artifact]
                verify.verify_seal(run, smoke=True)
                Path(spec['path']).write_bytes(b'tampered parameters')
                with self.assertRaises(ValueError):
                    verify.verify_seal(run, smoke=True)
                self.assertFalse((run / 'first_final_qrel_open.json').exists())
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            verify.write_json(run / 'lock.json', {'synthetic': True})
            seal = self.smoke_fixture(run)
            seal['fit_artifact_sha256'].pop(next(iter(seal['fit_artifact_sha256'])))
            with self.assertRaises(ValueError):
                verify.verify_fit_artifacts(seal)

    def test_complete_unique_matrix(self):
        rows = [dict(zip(verify.KEY_FIELDS, k)) for k in sorted(verify.expected_keys(), key=str)]
        verify.check_matrix(rows)
        for bad in (rows[:-1], rows[:-1] + [rows[0]]):
            with self.assertRaises(ValueError):
                verify.check_matrix(bad)

    def test_metrics_all_queries_graded_outside_corpus(self):
        checks = score.metric_checks()
        self.assertEqual(checks['status'], 'PASS')

    def test_duplicate_nonfinite_qrels_rejected(self):
        good = {'query-id': 'q', 'corpus-id': 'd', 'score': '1'}
        for rows in ([good, good], [{**good, 'score': 'nan'}], [{**good, 'score': 'inf'}]):
            with self.assertRaises(ValueError):
                score.parse_qrel_rows(rows, list(good), 'tsv')

    def test_independent_equal_score_ties_and_identical_id_exclusion(self):
        gallery = np.ones((6, 2), dtype=np.float32)
        query = np.ones((2, 2), dtype=np.float32)
        actual = verify.independent_exact(query, gallery, ['q', 'b', 'c', 'd', 'e', 'f'], ['q', 'z'], k=4)
        np.testing.assert_array_equal(actual, [[1, 2, 3, 4], [0, 1, 2, 3]])
        with self.assertRaises(ValueError):
            verify.independent_exact(query * np.nan, gallery, list('abcdef'), ['q', 'z'], k=4)

    def test_immutable_rank_hash_wrong_ids_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'r.npy'
            docs = [f'd{i}' for i in range(101)]
            for values in (np.zeros((1, 100), dtype=np.int64), np.arange(1, 101).reshape(1, 100) + 1):
                np.save(path, values)
                with self.assertRaises(ValueError):
                    verify.verify_rank_array(path, verify.sha(path), docs, ['q'])
            np.save(path, np.arange(100).reshape(1, 100))
            digest = verify.sha(path)
            with path.open('ab') as stream:
                stream.write(b'tamper')
            with self.assertRaises(ValueError):
                verify.verify_rank_array(path, digest, docs, ['q'])

    def test_wrong_duplicate_input_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ids.json'
            path.write_text(json.dumps({'doc_ids': ['a', 'a'], 'query_ids': ['q']}))
            with self.assertRaises(ValueError):
                verify.read_ids(path, None)

    def test_original_unsorted_id_row_order_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ids.json'
            ids = {'doc_ids': ['doc9', 'doc2', 'doc10'], 'query_ids': ['1', '2', '10']}
            path.write_text(json.dumps(ids))
            actual = verify.read_ids(path, (3, 3))
            self.assertEqual(actual, (ids['doc_ids'], ids['query_ids']))
            self.assertNotEqual(actual[0], sorted(actual[0]))
            self.assertNotEqual(actual[1], sorted(actual[1]))
            for field in ('doc_ids', 'query_ids'):
                for invalid in (['a', 'a', 'b'], ['a', 2, 'b'], ['a', '', 'b']):
                    bad = copy.deepcopy(ids)
                    bad[field] = invalid
                    path.write_text(json.dumps(bad))
                    with self.assertRaises(ValueError):
                        verify.read_ids(path, (3, 3))

    def test_rich_encoding_output_schema_named_file_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            encoding = {'models': {'minilm_x': {'outputs': {}}}}
            for role, count in [('docs', 3), ('queries', 2)]:
                path = run / f'{role}.npy'
                np.save(path, np.zeros((count, 384), dtype=np.float32))
                journal = run / f'{role}.jsonl'
                journal.write_text('{"synthetic":true}\n')
                encoding['models']['minilm_x']['outputs'][role] = {
                    'path': path.name, 'sha256': verify.sha(path),
                    'shape': [count, 384], 'dtype': 'float32',
                    'journal_path': journal.name, 'journal_sha256': verify.sha(journal)}
            manifest = run / 'encoding_manifest.json'
            verify.write_json(manifest, encoding)
            query_file = {'path': str((run / 'queries.npy').resolve()), 'sha256': verify.sha(run / 'queries.npy')}
            canonical = verify.encoding_output_spec(manifest, encoding, 'minilm_x', 'queries', (3, 2))
            self.assertEqual(set(canonical), {'path', 'sha256'})
            verify.require_encoder_file(query_file, canonical, 'named query binding')
            wrong_role = verify.encoding_output_spec(manifest, encoding, 'minilm_x', 'docs', (3, 2))
            for wrong in (wrong_role, {**query_file, 'sha256': '0' * 64}):
                with self.assertRaises(ValueError):
                    verify.require_encoder_file(wrong, canonical, 'wrong role/hash')
            for field, wrong in [('shape', [3, 384]), ('dtype', 'float64'),
                                 ('sha256', '0' * 64), ('journal_sha256', '0' * 64)]:
                bad = copy.deepcopy(encoding)
                bad['models']['minilm_x']['outputs']['queries'][field] = wrong
                with self.assertRaises(ValueError):
                    verify.encoding_output_spec(manifest, bad, 'minilm_x', 'queries', (3, 2))

    def test_receipt_exactly_once_before_acquire(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            out = run / 'scoring'
            out.mkdir()
            opener = mock.Mock()
            with self.assertRaises(ValueError):
                score.acquire_qrels(out, score.QREL_SOURCE, opener=opener)
            opener.assert_not_called()
            score.write_first_open(run, {'synthetic': True})
            before = (run / 'first_final_qrel_open.json').read_bytes()
            with self.assertRaises(FileExistsError):
                score.write_first_open(run, {'synthetic': 'overwrite'})
            self.assertEqual(before, (run / 'first_final_qrel_open.json').read_bytes())
            fake = b'query-id\tcorpus-id\tscore\nq\td\t2\n'
            source = {'url': 'fixture://fake', 'bytes': len(fake), 'format': 'tsv',
                      'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(fake)).encode() + b'\0' + fake).hexdigest()}
            def fake_opener(url):
                self.assertTrue((run / 'first_final_qrel_open.json').exists())
                return io.BytesIO(fake)
            qrels, stats, path = score.acquire_qrels(out, source, fake_opener)
            self.assertEqual(qrels, {'q': {'d': 2.0}})
            self.assertEqual(stats['sha256'], hashlib.sha256(fake).hexdigest())
            with self.assertRaises(FileExistsError):
                score.acquire_qrels(out, source, fake_opener)

    def test_mismatch_qrel_blob_preserved_no_parse(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            out = run / 'scoring'
            out.mkdir()
            score.write_first_open(run, {'synthetic': True})
            source = {**score.QREL_SOURCE, 'bytes': 3, 'git_blob_sha1': '0' * 40}
            with mock.patch.object(score, 'parse_qrel_rows') as parse:
                with self.assertRaises(ValueError):
                    score.acquire_qrels(out, source, lambda url: io.BytesIO(b'bad'))
                parse.assert_not_called()
            self.assertEqual((out / 'qrels_TREC-COVID.tsv').read_bytes(), b'bad')
            self.assertTrue((out / 'qrel_observed_hash.json').exists())

    def test_missing_verification_seal(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                score.verify_verification(Path(directory), {}, '0' * 64, 'commit')

    def test_missing_ranking_seal_does_not_open_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                verify.verify_seal(Path(directory))
            self.assertFalse((Path(directory) / 'first_final_qrel_open.json').exists())

    def test_scoring_failure_preserved_duplicate_open_no_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            score.write_first_open(run, {'synthetic': True})
            with mock.patch.object(score, 'acquire_qrels') as acquire:
                with self.assertRaises(ValueError):
                    score.run_score(run / 'unused_lock.json', run)
                acquire.assert_not_called()
            self.assertTrue((run / 'scoring/failure.json').exists())
            with self.assertRaises(FileExistsError):
                score.run_score(run / 'unused_lock.json', run)

    def test_shared_bootstrap_and_thirty_family_intervals(self):
        cells = [dict(zip(verify.KEY_FIELDS, k)) for k in sorted(verify.expected_keys(), key=str)]
        arrays = np.zeros((184, 3, 2), dtype=np.float64)
        for index, cell in enumerate(cells):
            if cell['method'] == verify.PRIMARY:
                arrays[index] = [[1, 0.5], [-1, -0.5], [0, 0]]
        means, contrasts, bootstrap, draws = score.summaries(cells, arrays)
        self.assertEqual((len(means), len(contrasts), draws.shape), (40, 30, (20000, 140)))
        for row in contrasts:
            self.assertEqual(row['ndcg10']['family_interval_interpretation'], 'unresolved')
            self.assertEqual(row['ndcg10']['per_interval_confidence'], 1 - .05 / 30)
            self.assertNotIn('ci_bonferroni_family95', row['recall100'])
        first = [i for i, d in enumerate(bootstrap['definitions']) if d['kind'] == 'contrast'][0]
        indices = np.random.default_rng(score.BOOTSTRAP_SEED).integers(0, 3, size=(20000, 3), dtype=np.int32)
        expected = np.array([1., -1., 0.])[indices].mean(axis=1)
        np.testing.assert_allclose(draws[:, 2 * first], expected, rtol=0, atol=1e-15)
        self.assertEqual(bootstrap['query_indices_sha256'], hashlib.sha256(indices.tobytes()).hexdigest())
        self.assertEqual(score.interpretation(0, 1), 'unresolved')
        self.assertEqual(score.interpretation(-1, 0), 'unresolved')

    def test_source_and_policy_lock(self):
        lock = {'scoring': {'bootstrap_draws': 20000, 'bootstrap_seed': 20261031,
                           'contrasts': 30, 'alpha': .05, 'qrels': score.QREL_SOURCE}}
        score.source_specifications(lock)
        for name, changed in [('bootstrap_seed', 7), ('contrasts', 5), ('alpha', .1)]:
            bad = copy.deepcopy(lock)
            bad['scoring'][name] = changed
            with self.assertRaises(ValueError):
                score.source_specifications(bad)


if __name__ == '__main__':
    unittest.main()
