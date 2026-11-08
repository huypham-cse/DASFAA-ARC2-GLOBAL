"""Finite qrel-free R3 checks; no scientific fit, encoder or GPU is invoked."""
from __future__ import annotations
import copy
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'ops'), str(ROOT / 'tools')]
import numpy as np
import b1c_r3_stage as stage
import build_b1c_r3_registries as builder
import build_b1c_r3_lock as lock_builder


class R3Checks(unittest.TestCase):
    def test_remote_root_is_canonical_across_host_path_types(self):
        expected = '/network-volume/arc2_recovery_20261030/restored'
        for value in (expected, PurePosixPath(expected), PureWindowsPath(expected), Path(expected)):
            registry, _ = builder.build({'sources': []}, value)
            self.assertEqual(registry['restored_root'], expected)
            self.assertNotIn('\\', registry['restored_root'])
        for value in ('network-volume/arc2_recovery_20261030/restored',
                      '/network-volume/arc2_recovery_20261030/restored/',
                      '/network-volume/arc2_recovery_20261030/restored/../other'):
            with self.assertRaisesRegex(ValueError, 'exact prospective POSIX'):
                builder.canonical_restored_root(value)
        self.assertEqual(lock_builder.RESTORED_ROOT, expected)
        self.assertEqual(lock_builder.validate_remote_paths(PureWindowsPath(lock_builder.DEFAULT_BASE), expected), lock_builder.DEFAULT_BASE)
        with self.assertRaisesRegex(ValueError, 'exact prospective POSIX'):
            lock_builder.validate_remote_paths(lock_builder.DEFAULT_BASE, str(PureWindowsPath(expected)))

    def test_prospective_configs_use_exact_linux_root_literal(self):
        for name in ('b1c_r3_sources.json', 'b1c_r3_lock.json'):
            value = stage.read_json(ROOT / 'configs' / name)['restored_root']
            self.assertEqual(value, '/network-volume/arc2_recovery_20261030/restored')
            self.assertNotIn('\\', value)

    def test_finite_partition(self):
        registry, existing = builder.build({'sources': []}, Path('/network-volume/arc2_recovery_20261030/restored'))
        self.assertEqual(len(registry['groups']), 120)
        self.assertEqual(sum(len(g['cases']) for g in registry['groups']), 358)
        self.assertEqual(sum(stage.reused(g) for g in registry['groups']), 2)
        self.assertEqual(len(existing['cells']), 378)
        self.assertEqual(len(existing['displaced_historical_cells']), 38)
        for g in registry['groups']:
            self.assertEqual(set(g['full_target_reference']), {'original_path', 'source_sha256'})
            if g['dataset'] == 'FiQA':
                self.assertTrue(all(c['target_source']['kind'] == 'b1g_75_subset' for c in g['cases']))

    def test_slice_fixtures(self):
        with tempfile.TemporaryDirectory() as tmp:
            checks = stage.fixture_checks(Path(tmp))
            self.assertEqual(checks['rejected_invalid_slices'], 4)
            self.assertFalse(checks['qrels_opened'])

    def test_registry_validator_accepts_only_expected_recovery(self):
        restored = Path('/network-volume/arc2_recovery_20261030/restored')
        registry, existing = builder.build({'sources': []}, restored)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rp, ep = root / 'registry.json', root / 'existing.json'
            stage.write_json(rp, registry)
            stage.write_json(ep, existing)
            lock = {'registry': {'path': str(rp), 'sha256': stage.sha256(rp)},
                    'existing_cells': {'path': str(ep), 'sha256': stage.sha256(ep)}}
            class MetadataOnlyInputs:
                restored_root = restored.resolve()
                def path(self, spec):
                    # Do not inspect scientific payloads in a schema unit test.
                    return Path(spec['path'])
            with patch.object(stage, 'require_tracked', lambda p: None):
                stage.registry_for(lock, MetadataOnlyInputs())
                registry['groups'][2]['cases'][0]['target_slice']['cache_key'][2] = 67
                stage.write_json(rp, registry)
                with self.assertRaisesRegex(ValueError, 'exact ordered source IDs'):
                    stage.registry_for(lock, MetadataOnlyInputs())

    def test_conflicting_overlaps_rejected(self):
        """Even independently hash-valid budget slices must agree on overlap."""
        rng = np.random.default_rng(17)
        vectors = stage.normalize_rows(rng.normal(size=(128, 768)).astype(np.float32))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sources = root / 'sources'
            sources.mkdir()
            cases = []
            for budget, count in [('25pct', 32), ('50pct', 64), ('75pct', 96)]:
                paid = np.arange(count, dtype=np.int64)[::-1].copy()
                values = vectors[paid].copy()
                if budget == '25pct':
                    values[0] = vectors[127]
                pp, tp = sources / (budget + '_paid.npy'), sources / (budget + '_target.npy')
                stage.save(pp, paid)
                stage.save(tp, values)
                cases.append({'budget': budget, 'paid': {'path': str(pp), 'sha256': stage.sha256(pp)},
                              'target_source': {'kind': 'saved_slice', 'file': {'path': str(tp), 'sha256': stage.sha256(tp)}},
                              'target_slice': {'shape': list(values.shape), 'source_sha256': stage.sha256(tp)}})
            group = {'dataset': 'NanoNQ', 'pair': 'e5_small_base', 'seed': 17,
                     'method': stage.LA2M, 'cases': cases}
            with self.assertRaisesRegex(ValueError, 'Conflicting target values'):
                stage.prepare_targets(group, stage.Inputs(root), root / 'copies', 128, np.arange(8))

    def test_prepared_exact_slices_and_anchor_order(self):
        rng = np.random.default_rng(17)
        values = stage.normalize_rows(rng.normal(size=(128, 768)).astype(np.float32))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sourcepaid = np.arange(96, dtype=np.int64)[::-1].copy()
            p75, t75 = root / 'p75.npy', root / 't75.npy'
            stage.save(p75, sourcepaid)
            stage.save(t75, values[sourcepaid])
            cases = []
            for budget, count in [('25pct', 32), ('50pct', 64), ('75pct', 96)]:
                paid = np.arange(count, dtype=np.int64)[::-1].copy()
                pp, expected = root / (budget + '.npy'), root / (budget + '_expected.npy')
                stage.save(pp, paid)
                stage.save(expected, values[paid])
                cases.append({'budget': budget, 'paid': {'path': str(pp), 'sha256': stage.sha256(pp)},
                              'target_source': {'kind': 'b1g_75_subset', 'paid': {'path': str(p75), 'sha256': stage.sha256(p75)},
                                                'targets': {'path': str(t75), 'sha256': stage.sha256(t75)}},
                              'target_slice': {'shape': [count, 768], 'source_sha256': stage.sha256(expected)}})
            group = {'dataset': 'NanoNQ', 'pair': 'e5_small_base', 'seed': 17, 'method': stage.LA2M, 'cases': cases}
            anchors = np.array([7, 2, 6, 0])
            prepared, paired = stage.prepare_targets(group, stage.Inputs(root), root / 'copies', 128, anchors)
            np.testing.assert_array_equal(paired, values[anchors])
            for budget, (paid, target, _, path) in prepared.items():
                np.testing.assert_array_equal(target, values[paid])
                self.assertEqual(stage.sha256(path), next(c['target_slice']['source_sha256'] for c in cases if c['budget'] == budget))
            broken = copy.deepcopy(group)
            broken['cases'][0]['target_slice']['source_sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'bytes differ'):
                stage.prepare_targets(broken, stage.Inputs(root), root / 'copies', 128, anchors)
            for _, target, _, _ in prepared.values():
                target._mmap.close()

    def test_no_label_or_model_module_import(self):
        self.assertFalse(any(name.split('.')[0] in {'torch', 'transformers', 'sentence_transformers', 'pyarrow'} for name in sys.modules))
        source = (ROOT / 'ops/b1c_r3_stage.py').read_text(encoding='utf-8')
        self.assertNotIn('load_qrels', source)
        self.assertNotIn('from b1c_score', source)


if __name__ == '__main__':
    unittest.main()
