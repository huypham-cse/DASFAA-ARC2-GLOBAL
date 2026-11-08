"""Build a new immutable B1c-R3 lock after source allocation/registries exist.

This reads metadata/source bytes only. It never touches label files, vectors,
models or the network and never runs smoke/fits/scoring or creates a commit.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = 'protocols/B1C_R3_FILESYSTEM_RECOVERY_20261030.md'
DEFAULT_BASE = '/network-volume/arc2_recovery_20261030'
RESTORED_ROOT = DEFAULT_BASE + '/restored'
NEW_SOURCES = (PROTOCOL, 'ops/b1c_r3_stage.py', 'ops/b1c_r3_score.py', 'ops/b1c_r3_campaign.py',
               'tools/build_b1c_r3_registries.py', 'tools/build_b1c_r3_lock.py', 'tools/test_b1c_r3_stage.py',
               'configs/b1c_lock.json', 'configs/b1c_existing.json', 'configs/b1c_sources.json',
               'configs/b1c_recovery_r2_lock.json', 'configs/b1c_recovery_r2_manifest.json',
               'configs/b1c_r3_sources.json', 'configs/b1c_r3_existing.json', 'configs/b1c_r3_acquisition.json',
               'results/b1g_r1_review_20261027/main/execution_intermediates.json',
               'protocols/B1C_R2_OOM_RECOVERY_20261028.md')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path, canonical=False):
    data = Path(path).read_bytes()
    return hashlib.sha256(data.replace(b'\r\n', b'\n') if canonical else data).hexdigest()


def spec(relative):
    return {'path': relative, 'sha256': digest(ROOT / relative)}


def validate_remote_paths(runtime_base, restored_root):
    """Compare remote path literals; never resolve them on the build host."""
    base = str(runtime_base).replace('\\', '/').rstrip('/')
    if base != DEFAULT_BASE or restored_root != RESTORED_ROOT:
        raise ValueError('Registry/runtime require the exact prospective POSIX restored root')
    return base


def build(runtime_base=DEFAULT_BASE, dependency_fallbacks=None, runtime_receipt=None):
    old = read(ROOT / 'configs/b1c_lock.json')
    r2 = read(ROOT / 'configs/b1c_recovery_r2_lock.json')
    lock = copy.deepcopy(old)
    sources = copy.deepcopy(r2['source_sha256_canonical_lf'])
    lock['source_sha256_canonical_lf'] = sources
    for relative, expected in old['source_sha256_canonical_lf'].items():
        if (relative not in ('ops/b1c_stage.py', 'ops/b1c_campaign.py')
                and sources.get(relative) != expected):
            raise ValueError('R2 must preserve every original numerical/config/protocol digest: ' + relative)
    # Preserve every historical numerical/source digest, rather than refreshing
    # old entries from potentially changed bytes.
    for relative, expected in sources.items():
        if digest(ROOT / relative, canonical=True) != expected:
            raise ValueError('Historical frozen source drift: ' + relative)
    for relative in NEW_SOURCES:
        observed = digest(ROOT / relative, canonical=True)
        if relative in sources and sources[relative] != observed:
            raise ValueError('Conflicting inherited source digest: ' + relative)
        sources[relative] = observed
    registry = read(ROOT / 'configs/b1c_r3_sources.json')
    existing = read(ROOT / 'configs/b1c_r3_existing.json')
    acquisition = read(ROOT / 'configs/b1c_r3_acquisition.json')
    base = validate_remote_paths(runtime_base, registry['restored_root'])
    if (registry.get('stage'), existing.get('stage'), len(registry['groups']),
            sum(len(g['cases']) for g in registry['groups']), len(existing['cells']),
            len(existing['displaced_historical_cells'])) != ('B1C_R3', 'B1C_R3', 120, 358, 378, 38):
        raise ValueError('R3 registries do not bind the finite unchanged matrix')
    if not isinstance(acquisition.get('sources'), list):
        raise ValueError('Missing explicit R3 acquisition source allocation')
    lock.update(stage='B1C_R3', protocol=PROTOCOL, amendment=PROTOCOL,
                historical_protocols=[old['protocol'], old.get('amendment'), 'protocols/B1C_R2_OOM_RECOVERY_20261028.md'],
                cpu_python=base + '/envs/cpu/bin/python', gpu_python=base + '/envs/gpu/bin/python',
                upstream=base + '/upstream/embedding-translation',
                upstream_revision='5e62baf1544264847ce3d8feeabd1ded6499b064',
                dependency_fallbacks=dependency_fallbacks if dependency_fallbacks is not None else [base + '/envs/cpu/lib/python3.11/site-packages'],
                registry=spec('configs/b1c_r3_sources.json'), existing_cells=spec('configs/b1c_r3_existing.json'),
                acquisition_manifest=spec('configs/b1c_r3_acquisition.json'),
                expected_new_rankings=358, expected_existing_rankings=378,
                expected_complete_main_rankings=736, expected_fit_groups=120,
                expected_new_nano_fits=90, expected_new_fiqa_fits=28,
                expected_historical_fiqa_fits_reused=2, expected_saved_fit_parity=2,
                expected_informational_fiqa_historical_comparisons=28,
                displaced_historical_cells=38, restored_root=registry['restored_root'],
                original_b1c_state='INTERRUPTED_NOT_COMPLETE; original320 and R2 outputs cannot be claimed recovered from metadata alone',
                historical_locks=[spec('configs/b1c_lock.json'), spec('configs/b1c_recovery_r2_lock.json')],
                new_physical_document_encodes=0, artificial_time_memory_caps=None, TREC_access=False,
                STOP='After complete same736-cell DEV report and final D1; STOP before B2/TREC/systems')
    lock.pop('recovery_manifest', None)
    if lock['restored_root'] != RESTORED_ROOT:
        raise ValueError('Lock must serialize the exact prospective POSIX restored root')
    lock['recovery_source_policy'] = {
        'all_active_sources_sha256_verified_before_any_fit': True,
        'all_120_budget_slices_match_original_B1G_npy_sha256_before_any_fit': True,
        'fiqa_75pct_source_slices': 10, 'fiqa_25_50_ordered_subsets': 20,
        'fit_anchor_targets': 'Extract ordered1024 anchors from same dataset/pair/seed75pct slice',
        'gallery_targets': 'Exact respective budget slice only; SHA256 equals original B1G execution_intermediates entry',
        'missing_unpaid_fiqa_target_reconstruction': False,
        'full_y_access': 'Restored exact-hash Nano cache materialization only; FiQA full-Y remains documentary',
        'saved_fit_parity_required': 'Only MiniLM->distilroberta FiQA seed17 LA2M and SimpleLinear50pct',
        'fresh_fiqa_old_rank_comparisons': 'Informational only; never gate or select a fit/output'}
    # The endpoint values remain the R1 Mini contract. Runtime
    # checks require exact device/UUID/versions; a read-only observation is
    # provenance, not permission to relax an identity mismatch.
    lock['execution_device'] = copy.deepcopy(old['execution_device'])
    lock['execution_device']['verification_requirement'] = 'Read-only30Oct03:26UTC check confirmed same Mini MIG; smoke independently enforces exact identity/versions'
    if runtime_receipt is not None:
        path = Path(runtime_receipt).resolve(strict=True)
        relative = path.relative_to(ROOT).as_posix()
        lock['runtime_readonly_verification'] = spec(relative)
        sources[relative] = digest(path, canonical=True)
    # Scientific and version declarations must remain inherited exactly.
    for field in ('seeds', 'cpu_versions', 'cpu_sklearn_version', 'gpu_versions', 'cpu_environment', 'environment',
                  'upstream_raw_sha256', 'simplelinear_defaults', 'converter_config', 'smoke_converter_iterations',
                  'neighbor_block_rows', 'models', 'datasets', 'scoring', 'model_revision'):
        if field in old and lock[field] != old[field]:
            raise ValueError('Scientific/version setting changed: ' + field)
    return lock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-base', default=DEFAULT_BASE)
    parser.add_argument('--dependency-fallback', action='append')
    parser.add_argument('--runtime-receipt', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'configs/b1c_r3_lock.json')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Immutable R3 lock already exists: ' + str(args.output))
    lock = build(args.runtime_base, args.dependency_fallback, args.runtime_receipt)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(lock, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'path': str(args.output), 'sha256': digest(args.output), 'new': 358, 'existing': 378,
                      'fresh_fits': 118, 'reused_fits': 2, 'scientific_run_started': False}))


if __name__ == '__main__':
    main()
