"""Named development controls; the frozen ARC2 implementation is unchanged."""
import time
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from .procrustes import procrustes_fit
from .model import centered_affine_coefficient
from .numerics import _vectors

METHODS = ('tangent2', 'chordal2', 'euclidean2')


def residual_target(z, y, method):
    r = np.linalg.norm(z, axis=1, keepdims=True)
    if not np.isfinite(z).all() or np.any(r <= 1e-12):
        raise ValueError('Invalid raw direction; preserve failure')
    u = z / r
    c = np.sum(u * y, axis=1, keepdims=True)
    if method == 'tangent2':
        target = r * (y - c * u)
    elif method == 'chordal2':
        target = r * (y - u)
    elif method == 'euclidean2':
        target = y - z
    else:
        raise ValueError('Unknown residual control')
    return target, r, u, c


def fit_controls(old_pairs, new_pairs):
    old = _vectors('old_pairs', old_pairs)
    y = _vectors('new_pairs', new_pairs).astype(np.float64)
    if len(old) != len(y) or len(old) < 8:
        raise ValueError('Require aligned anchor pairs')
    began = time.perf_counter()
    sm, tm, w = procrustes_fit(old, new_pairs, center=True)
    base = centered_affine_coefficient(sm, tm, w)
    base_seconds = time.perf_counter() - began
    x = np.concatenate((old.astype(np.float64), np.ones((len(old), 1))), axis=1)
    began = time.perf_counter()
    gram = x @ x.T + 10.0 * np.eye(len(x))
    factor = cho_factor(gram, lower=True, check_finite=True)
    factor_seconds = time.perf_counter() - began
    outputs = {'procrustes': base.astype(np.float32)}
    states, records = {}, {}
    for method in METHODS:
        coef = base.copy()
        snapshots, steps = [], []
        began_method = time.perf_counter()
        for step in (1, 2):
            began = time.perf_counter()
            target, r, u, c = residual_target(x @ coef, y, method)
            alpha = cho_solve(factor, target, check_finite=True)
            delta = x.T @ alpha
            error = (x.T @ x + 10.0 * np.eye(x.shape[1])) @ delta - x.T @ target
            radial = np.sum(u * target, axis=1, keepdims=True) * u
            coef = coef + delta
            if not np.isfinite(coef).all():
                raise ValueError('Nonfinite control coefficient')
            snapshots.append(coef.copy())
            steps.append({'step': step, 'seconds': time.perf_counter() - began,
                          'radius_quantiles': np.quantile(r, [0, .25, .5, .75, 1]).tolist(),
                          'cosine_quantiles': np.quantile(c, [0, .25, .5, .75, 1]).tolist(),
                          'target_norm': float(np.linalg.norm(target)),
                          'radial_energy': float(np.sum(radial**2)),
                          'tangent_energy': float(np.sum((target-radial)**2)),
                          'xt_target_norm': float(np.linalg.norm(x.T @ target)),
                          'update_norm': float(np.linalg.norm(delta)),
                          'coefficient_norm': float(np.linalg.norm(coef)),
                          'normal_equation_relative_residual': float(np.linalg.norm(error) / max(np.linalg.norm(x.T @ target), 1e-300))})
        outputs[method] = coef.astype(np.float32)
        states[method] = snapshots
        records[method] = {'update_trajectory_seconds': time.perf_counter()-began_method,
                           'steps': steps}
    return {'coefficients': outputs, 'base_float64': base, 'float64_steps': states,
            'source_mean': sm, 'target_mean': tm, 'matrix': w,
            'shared_procrustes_seconds': base_seconds,
            'shared_dual_factor_seconds': factor_seconds, 'trajectories': records}
