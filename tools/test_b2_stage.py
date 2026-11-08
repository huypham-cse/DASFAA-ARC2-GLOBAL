"""Finite synthetic B2 orchestration checks; no encoder, fitted model or GPU run."""
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'ops'), str(ROOT / 'src')]
import b2_stage as stage


class B2Checks(unittest.TestCase):
    def test_encoding_preserves_unsorted_acquisition_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lockpath = root / 'lock.json'
            stage.dump(lockpath, {'fixture': True})
            docs = [f'd{i}' for i in range(171332)]
            docs[0], docs[1] = docs[1], docs[0]
            ids = {'doc_ids': docs, 'query_ids': [str(i) for i in range(1, 51)],
                   'row_order': 'original parquet row order'}
            stage.dump(root / 'ids.json', ids)
            # Identity/manifest integration is real; vector validation is stubbed
            # to avoid allocating the real corpus in this finite pre-run test.
            stage.save(root / 'fixture.npy', np.ones((1, 1), dtype=np.float32))
            vector_spec = {'path': 'fixture.npy', 'sha256': stage.sha(root / 'fixture.npy')}
            stage.dump(root / 'encoding_manifest.json', {
                'status': 'ENCODING_PASS', 'code_commit': 'fixture',
                'lock': {'sha256': stage.sha(lockpath)},
                'ids': {'path': 'ids.json', 'sha256': stage.sha(root / 'ids.json')},
                'models': {label: {'outputs': {'docs': vector_spec, 'queries': vector_spec}}
                           for label in ['minilm_x', 'distilroberta_y', 'e5_small_x', 'e5_base_y']}})
            with patch.object(stage, 'validate_array', return_value=None) as validate:
                actual, _, _, _ = stage.prepare_encoding(root, lockpath, 'fixture')
            self.assertEqual(validate.call_count, 8)
            self.assertEqual(actual, ids)
            self.assertNotEqual(actual['doc_ids'], sorted(actual['doc_ids']))
            self.assertNotEqual(actual['query_ids'], sorted(actual['query_ids']))

    def test_duplicate_empty_and_nonstring_ids_rejected(self):
        for key in ['doc_ids', 'query_ids']:
            for invalid in [['z', 'z'], ['z', 1], ['z', ['nested']], ['z', ''], []]:
                with self.subTest(key=key, invalid=invalid):
                    ids = {'doc_ids': ['z', 'a'], 'query_ids': ['2', '1']}
                    ids[key] = invalid
                    with self.assertRaisesRegex(ValueError, 'nonempty unique strings'):
                        stage.validate_ids(ids)

    def test_seed_streams_and_unique_charged_nested_selections(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selections = stage.prepare_selections(root, 2048, stage.SEEDS, 128)
            for seed, (anchors, anchor_spec, paid) in selections.items():
                expected = np.random.default_rng(np.random.SeedSequence([seed, 0])).choice(2048, 128, replace=False)
                np.testing.assert_array_equal(anchors, expected)
                self.assertEqual(stage.sha(Path(anchor_spec['path'])), anchor_spec['sha256'])
                order = np.load(root / f'inputs/order_seed{seed}.npy', allow_pickle=False)
                np.testing.assert_array_equal(order, np.random.default_rng(np.random.SeedSequence([seed, 1])).permutation(2048))
                previous = set(anchors)
                for budget in stage.BUDGETS:
                    selected, spec = paid[budget]
                    self.assertEqual(len(selected), 2048 * budget // 100)
                    self.assertEqual(len(set(selected)), len(selected))
                    self.assertTrue(previous <= set(selected))
                    self.assertEqual(stage.sha(Path(spec['path'])), spec['sha256'])
                    previous = set(selected)

    def test_all_six_fits_reused_and_all_twenty_endpoints_reconstruct(self):
        # Stub only model training. Real serialization and exact retrieval run.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ids, ids_spec, vectors = stage.synthetic_inputs(root)
            target = vectors['distilroberta_y']['docs'][0]
            # Deliberately disagree with target at unpaid rows.
            proxy = np.roll(target, 1, axis=0).copy()
            calls = []

            def cpu(method, old, target_array, anchors, seed, output):
                calls.append((method, seed, len(anchors)))
                output.mkdir(parents=True)
                np.savez(output / 'parameters.npz', stub=np.zeros(1))
                stage.dump(output / 'metadata.json', {'status': 'TEST_STUB'})
                return proxy.copy(), {'status': 'TEST_STUB', 'method': method}

            def gpu(lock, lockpath, commit, out, pair, seed, method, source_spec, old, anchors, target_array, mode):
                calls.append((method, seed, len(anchors)))
                path = out / 'neural' / method / 'proxy_full.npy'
                stage.save(path, proxy)
                return proxy.copy(), stage.filespec(path), {'status': 'TEST_STUB', 'method': method}

            with patch.object(stage, 'cpu_fit', cpu), patch.object(stage, 'neural', gpu):
                cells = stage.rank_all({}, root / 'lock.json', 'test', root, ids, ids_spec, vectors, [17], 128, 'smoke')
            self.assertEqual(len(cells), 20)
            self.assertEqual(calls, [(method, 17, 128) for method in stage.METHODS])
            self.assertEqual({c['method'] for c in cells if c['seed'] is None}, {'full_x', 'full_y'})
            for method in stage.METHODS:
                group = [c for c in cells if c['method'] == method]
                self.assertEqual([c['unique_destination_encodings'] for c in group], [512, 1024, 1536])
                self.assertEqual(len({c['fit_receipt']['proxy_sha256'] for c in group}), 1)
            # Independent reconstruction: no stage/exact_topk helper is called.
            for cell in cells:
                descriptor_path = root / cell['endpoint_path']
                self.assertEqual(stage.sha(descriptor_path), cell['endpoint_sha256'])
                descriptor = json.loads(descriptor_path.read_text())
                self.assertEqual(descriptor['schema'], 'b2_exact_endpoint_v1')
                files = descriptor['files']
                for spec in files.values():
                    self.assertEqual(stage.sha(Path(spec['path'])), spec['sha256'])
                query = np.load(files['query_vectors']['path'], allow_pickle=False)
                if descriptor['kind'] == 'native':
                    gallery = np.load(files['native_vectors']['path'], allow_pickle=False)
                else:
                    gallery = np.load(files['proxy_vectors']['path'], allow_pickle=False).copy()
                    paid = np.load(files['paid_indices']['path'], allow_pickle=False)
                    anchors = np.load(files['anchor_indices']['path'], allow_pickle=False)
                    self.assertTrue(set(anchors) <= set(paid))
                    destination = np.load(files['destination_vectors']['path'], allow_pickle=False)
                    gallery[paid] = destination[paid]
                    np.testing.assert_array_equal(gallery[anchors], destination[anchors])
                scores = query @ gallery.T
                expected = np.stack([np.lexsort((np.arange(len(gallery)), -row))[:100] for row in scores])
                actual = np.load(root / cell['ranking_path'], allow_pickle=False)
                np.testing.assert_array_equal(actual, expected)
                self.assertEqual(stage.sha(root / cell['ranking_path']), cell['ranking_sha256'])

    def test_invalid_endpoint_and_overwrite_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'endpoint.json'
            dummy = {'path': '/test', 'sha256': '0' * 64}
            with self.assertRaisesRegex(ValueError, 'Invalid mixed'):
                stage.save_endpoint(path, kind='mixed', shape=[128, 768], ids=dummy, queries=dummy)
            stage.save_endpoint(path, kind='native', shape=[128, 768], ids=dummy, queries=dummy, native=dummy)
            with self.assertRaises(FileExistsError):
                stage.save_endpoint(path, kind='native', shape=[128, 768], ids=dummy, queries=dummy, native=dummy)
            array = Path(tmp) / 'vectors.npy'
            stage.save(array, np.ones((2, 3), dtype=np.float64))
            with self.assertRaisesRegex(ValueError, 'shape/dtype'):
                stage.validate_array(array, (2, 3))
            with self.assertRaises(FileExistsError):
                stage.save(array, np.ones((2, 3)))

    def test_fixed_exact_ties_and_same_id_exclusion(self):
        # Ties are row order, including around the top-k boundary.
        docs = np.zeros((105, 2), dtype=np.float32)
        docs[:, 0] = 1
        query = np.array([[1, 0]], dtype=np.float32)
        ranking = stage.exact_topk(query, docs, k=100, batch_rows=16,
                                   query_ids=['same'], document_ids=['same'] + [str(i) for i in range(1, 105)],
                                   exclude_identical_ids=True)
        np.testing.assert_array_equal(ranking[0], np.arange(1, 101))

    def test_nonzero_child_is_recorded_without_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row = stage.observed_child([sys.executable, '-c', 'raise SystemExit(7)'], os.environ.copy(), root)
            self.assertEqual(row['returncode'], 7)
            self.assertEqual(row['status'], 'EXITED')
            self.assertEqual(json.loads((root / 'process_exit.json').read_text())['returncode'], 7)
            self.assertEqual(row['stdout_sha256'], stage.sha(root / 'stdout.log'))

    def test_neural_parameters_and_actual_pairs_bound_to_worker_receipts(self):
        for method in [stage.SIMPLE, stage.CONVERTER]:
            with self.subTest(method=method), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                worker = root / 'worker'
                worker.mkdir()
                names = ['refit_checkpoint.pt', 'refit_fit.json']
                if method == stage.CONVERTER:
                    names += ['selection_checkpoint.pt', 'selection_fit.json']
                receipt = {'artifacts': {}, 'inputs': {}}
                for name in names:
                    path = worker / name
                    path.write_bytes(b'fixture-only-' + name.encode())
                    receipt['artifacts'][name] = {'sha256': stage.sha(path), 'bytes': path.stat().st_size}
                request = {'input_sha256': {}}
                for role in ['paired_source', 'paired_target']:
                    path = root / (role + '.npy')
                    stage.save(path, np.ones((2, 3), dtype=np.float32))
                    request['input_sha256'][role] = stage.sha(path)
                    receipt['inputs'][role] = {'sha256': stage.sha(path)}
                stage.dump(worker / 'metadata.json', receipt)
                stage.dump(root / 'request.json', request)
                stage.dump(root / 'process_exit.json', {'returncode': 0})
                artifacts = stage.neural_fit_artifacts(root, method, receipt, request)
                self.assertEqual(set(artifacts), set(names) | {'worker_metadata', 'request', 'process_exit', 'paired_source', 'paired_target'})
                for spec in artifacts.values():
                    self.assertEqual(stage.sha(Path(spec['path'])), spec['sha256'])
                (worker / 'refit_checkpoint.pt').write_bytes(b'changed parameters')
                with self.assertRaisesRegex(ValueError, 'parameter artifact differs'):
                    stage.neural_fit_artifacts(root, method, receipt, request)
                (worker / 'refit_checkpoint.pt').write_bytes(b'fixture-only-refit_checkpoint.pt')
                (root / 'paired_target.npy').write_bytes(b'changed paired targets')
                with self.assertRaisesRegex(ValueError, 'paired input differs'):
                    stage.neural_fit_artifacts(root, method, receipt, request)

    def test_no_label_or_encoder_import(self):
        self.assertFalse(any(name.split('.')[0] in {'torch', 'transformers', 'sentence_transformers', 'pyarrow'} for name in sys.modules))
        source = (ROOT / 'ops/b2_stage.py').read_text(encoding='utf-8')
        self.assertNotIn('load_qrels', source)
        self.assertNotIn('from b2_score', source)


if __name__ == '__main__':
    unittest.main()
