"""CPU-only synthetic ARC2 smoke; no dataset, qrels or scientific claim.

Example: python reproduce/smoke_review_method.py --root .
Default output: checks/synthetic_method_smoke/<unique-UTC-timestamp>.json.
An explicit --output must name a file that does not already exist.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, default=None,
        help='New receipt file; omitted: checks/synthetic_method_smoke/<UTC timestamp>.json')
    args = parser.parse_args()
    root = args.root.resolve()
    run_stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    requested_output = args.output if args.output is not None else Path('checks/synthetic_method_smoke') / f'{run_stamp}.json'
    out = requested_output.resolve() if requested_output.is_absolute() else (root / requested_output).resolve()
    if out == root or any(out.is_relative_to(root / name) for name in
        ('results', 'src', 'ops', 'configs', 'protocols', 'tools', 'reproduce', 'manuscript')):
        raise ValueError('Choose an output outside frozen source/evidence directories, such as checks/synthetic_method_smoke.json')
    if out.exists():
        raise FileExistsError(f'Output already exists; choose a new receipt path: {out}')
    sys.path.insert(0, str(root / 'src'))
    import numpy as np
    import scipy
    from arc2_global import fit_arc2_global, transform_old_docs, build_mixed_gallery, normalize_rows, select_for_budget
    from arc2_global.model import RIDGE_LAMBDA, TANGENT_STEPS, REVISION
    started = time.perf_counter()
    rng = np.random.default_rng(17)
    n, source_dim, target_dim, anchor_count = 256, 16, 24, 128
    old = normalize_rows(rng.normal(size=(n, source_dim)).astype(np.float32))
    linear = rng.normal(size=(source_dim, target_dim)).astype(np.float32)
    target = normalize_rows(old @ linear + .03 * rng.normal(size=(n, target_dim)).astype(np.float32))
    anchors = rng.choice(n, size=anchor_count, replace=False)
    order = rng.permutation(n)
    paid = select_for_budget(anchors, order, n_docs=n, fraction=.75)
    model = fit_arc2_global(old, anchors, target[anchors])
    proxy = transform_old_docs(old, model, block_rows=37)
    gallery = build_mixed_gallery(old, model, paid, target[paid], block_rows=37)
    ids = [f'synthetic_doc_{i:03d}' for i in range(n)]
    unpaid = np.setdiff1d(np.arange(n), paid)
    checks = {
        'frozen_lambda10_and_exactly_two_tangent_steps': RIDGE_LAMBDA == 10 and TANGENT_STEPS == 2,
        'finite_float32_unit_proxy_rows': bool(proxy.dtype == np.float32 and np.isfinite(proxy).all()
            and np.allclose(np.linalg.norm(proxy, axis=1), 1, atol=1e-5, rtol=0)),
        'finite_float32_unit_mixed_rows': bool(gallery.dtype == np.float32 and np.isfinite(gallery).all()
            and np.allclose(np.linalg.norm(gallery, axis=1), 1, atol=1e-5, rtol=0)),
        'all_paid_rows_exactly_overwritten': bool(np.array_equal(gallery[paid], target[paid])),
        'all_unpaid_rows_equal_saved_proxy': bool(np.array_equal(gallery[unpaid], proxy[unpaid])),
        'all_anchors_counted_in_paid_union': bool(set(map(int, anchors)) <= set(map(int, paid)) and len(paid) == 192),
        'one_vector_per_unique_document_id_in_original_order': bool(gallery.shape == (len(ids), target_dim)
            and len(set(ids)) == n and len(dict(zip(ids, gallery))) == n),
        'fit_receives_only_128_paired_anchors': bool(len(model.anchor_indices) == 128
            and np.array_equal(model.old_anchors, old[anchors]) and np.array_equal(model.new_anchors, target[anchors])),
    }
    if not all(checks.values()):
        raise AssertionError(f'Synthetic smoke failed: {checks}')
    paths = [root / 'src/arc2_global' / name for name in ('model.py', 'numerics.py', 'procrustes.py', '__init__.py')]
    receipt = {'status': 'PASS', 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Synthetic software smoke only; no real dataset, qrels, final-test fit or research result.',
        'method_revision': REVISION, 'entrypoint': 'arc2_global.model.fit_arc2_global',
        'backend_id': None,
        'backend_identity': 'Default model._tangent2 dual anchor-Gram Cholesky; float64 solve and float32 stored updates.',
        'backend_note': 'The default GlobalModel exposes no canonical backend_id. This smoke does not exercise or relabel B2\'s declared primal backend.',
        'device': 'CPU; NumPy/SciPy only', 'seed': 17, 'documents': n, 'anchors': anchor_count,
        'source_dim': source_dim, 'target_dim': target_dim, 'unique_destination_documents': len(paid),
        'lambda': RIDGE_LAMBDA, 'tangent_steps': TANGENT_STEPS,
        'elapsed_seconds': time.perf_counter() - started, 'python': platform.python_version(),
        'entrypoint_sha256': sha256(__file__),
        'output_selection': 'unique UTC timestamp default' if args.output is None else 'explicit exclusive file',
        'numpy': np.__version__, 'scipy': scipy.__version__, 'checks': checks,
        'source_sha256': {p.relative_to(root).as_posix(): sha256(p) for p in paths}}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'checks': len(checks), 'output': str(out),
        'scope': receipt['scope'], 'backend_identity': receipt['backend_identity']}, indent=2))


if __name__ == '__main__':
    main()
