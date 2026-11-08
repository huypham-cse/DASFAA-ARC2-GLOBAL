"""ARC2-Global: centered Procrustes plus exactly two tangent ridge updates.

Standalone extraction of the selected evaluated computation, not a new method.
Fit accepts ordered paired anchors only. No relevance labels or queries enter fit.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from . import procrustes
from .numerics import DEFAULT_BLOCK_ROWS, _indices, _vectors, apply_affine, normalize_rows
RIDGE_LAMBDA=10.0
MIN_ANCHORS=8
TANGENT_STEPS=2
PARITY_ATOL=1e-6
REVISION="arc2_global_tangent2_r1"

@dataclass(frozen=True)
class GlobalModel:
    anchor_indices: np.ndarray
    old_anchors: np.ndarray
    new_anchors: np.ndarray
    source_mean: np.ndarray
    target_mean: np.ndarray
    matrix: np.ndarray
    base_coef: np.ndarray  # float64 raw centered-map expansion, never normalized
    one_step_coef: np.ndarray
    arc2_coef: np.ndarray

    @property
    def old_dim(self) -> int:
        return self.old_anchors.shape[1]

    @property
    def new_dim(self) -> int:
        return self.new_anchors.shape[1]


def centered_affine_coefficient(source_mean: np.ndarray, target_mean: np.ndarray,
                                matrix: np.ndarray) -> np.ndarray:
    """Expand (x-sm) @ W.T + tm to [x,1] @ [W.T; tm-sm@W.T].

    Authors' W is target_dim by source_dim. Expansion arithmetic is float64;
    the authors' means and W remain their original float32 values. In
    particular, neither row normalization nor a fitted scale enters B0.
    """
    sm, tm, w = map(np.asarray, (source_mean, target_mean, matrix))
    if (w.ndim != 2 or not all(w.shape) or sm.shape != (1, w.shape[1]) or
            tm.shape != (1, w.shape[0]) or
            any(a.dtype != np.float32 or not np.isfinite(a).all() for a in (sm, tm, w))):
        raise ValueError("invalid centered Procrustes parameters")
    linear = w.T.astype(np.float64)
    intercept = tm.astype(np.float64) - sm.astype(np.float64) @ linear
    return np.concatenate((linear, intercept), axis=0)


def _raw_affine(old: np.ndarray, coefficient: np.ndarray) -> np.ndarray:
    x = np.concatenate((old.astype(np.float64),
                        np.ones((len(old), 1), dtype=np.float64)), axis=1)
    return x @ coefficient


def _tangent2(old_anchors: np.ndarray, new_anchors: np.ndarray,
              initial: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Exact core.py target and reusable Cholesky convention, starting at B0.
    x = np.concatenate((old_anchors.astype(np.float64),
                        np.ones((len(old_anchors), 1), dtype=np.float64)), axis=1)
    y = new_anchors.astype(np.float64)
    gram = x @ x.T + RIDGE_LAMBDA * np.eye(len(x), dtype=np.float64)
    factor = cho_factor(gram, lower=True, overwrite_a=False, check_finite=True)
    coef = initial.astype(np.float64)
    first = None
    for step in (1, 2):
        z = x @ coef
        norms = np.linalg.norm(z, axis=1, keepdims=True)
        if np.any(norms <= 1e-12) or not np.isfinite(z).all():
            raise ValueError("invalid affine direction during ARC2-Global fit")
        unit = z / norms
        target = norms * (y - np.sum(unit * y, axis=1, keepdims=True) * unit)
        delta = x.T @ cho_solve(factor, target, check_finite=True)
        coef = coef + delta
        if not np.isfinite(coef).all():
            raise ValueError("non-finite ARC2-Global coefficient")
        if step == 1:
            first = coef.astype(np.float32)
    return first, coef.astype(np.float32)


def fit_arc2_global(old_docs: np.ndarray, anchor_indices: np.ndarray,
                        new_anchor_vectors: np.ndarray, *, kernel=None) -> GlobalModel:
    """Fit the one frozen candidate on ordered anchor pairs only.

    By default load the revision/hash-checked authors' source via E5. A runner
    can inject the same already verified kernel to avoid repeated loading.
    """
    old = _vectors("old_docs", old_docs)
    anchors = _indices("anchor_indices", anchor_indices, len(old))
    if len(anchors) < MIN_ANCHORS:
        raise ValueError("at least eight anchors are required")
    new_a = _vectors("new_anchor_vectors", new_anchor_vectors)
    if len(new_a) != len(anchors):
        raise ValueError("new_anchor_vectors must align with anchor_indices")
    old_a = np.asarray(old[anchors], dtype=np.float32)
    if kernel is None:
        kernel = procrustes
    sm, tm, matrix = kernel.procrustes_fit(old_a, new_a, center=True)
    base = centered_affine_coefficient(sm, tm, matrix)
    # Check orientation, intercept and normalization convention before updates.
    pinned_raw = kernel.procrustes_apply(old_a, sm, tm, matrix)
    affine_raw = _raw_affine(old_a, base)
    for label, actual, expected in (
        ("raw", affine_raw, pinned_raw),
        ("normalized", normalize_rows(affine_raw), normalize_rows(pinned_raw)),
    ):
        if not np.allclose(actual, expected, atol=PARITY_ATOL, rtol=0):
            raise AssertionError(f"STOP: ARC2-Global centered affine {label} parity failed")
    first, final = _tangent2(old_a, new_a, base)
    return GlobalModel(anchors.copy(), old_a.copy(), new_a.copy(),
                              sm.copy(), tm.copy(), matrix.copy(), base, first, final)


def _block_rows(block_rows: int) -> None:
    if not isinstance(block_rows, int) or isinstance(block_rows, bool) or block_rows < 1:
        raise ValueError("block_rows must be positive")


def build_mixed_gallery(old_docs: np.ndarray, model: GlobalModel,
                        selected_indices: np.ndarray, new_selected_vectors: np.ndarray,
                        *, block_rows: int = DEFAULT_BLOCK_ROWS) -> np.ndarray:
    """Overwrite anchor-inclusive selected rows with exact destination vectors."""
    selected = _indices("selected_indices", selected_indices, len(old_docs))
    if not set(map(int, model.anchor_indices)) <= set(map(int, selected)):
        raise ValueError("selected_indices must include every fitted anchor")
    new_selected = _vectors("new_selected_vectors", new_selected_vectors, dim=model.new_dim)
    if len(selected) != len(new_selected):
        raise ValueError("new_selected_vectors must align with selected_indices")
    anchor_to_new = {int(i): model.new_anchors[j] for j, i in enumerate(model.anchor_indices)}
    for row, index in enumerate(selected):
        if int(index) in anchor_to_new and not np.array_equal(new_selected[row], anchor_to_new[int(index)]):
            raise ValueError("selected anchor vector differs from the fit input")
    result = transform_old_docs(old_docs, model, block_rows=block_rows)
    result[selected] = new_selected
    return result


def transform_old_docs(old_docs: np.ndarray, model: GlobalModel,
                       *, block_rows: int = DEFAULT_BLOCK_ROWS) -> np.ndarray:
    old = _vectors("old_docs", old_docs, dim=model.old_dim)
    anchors = _indices("model.anchor_indices", model.anchor_indices, len(old))
    _block_rows(block_rows)
    if not np.array_equal(old[anchors], model.old_anchors):
        raise ValueError("old document anchor rows differ from fitted model")
    mapped = np.empty((len(old), model.new_dim), dtype=np.float32)
    for start in range(0, len(old), block_rows):
        end = min(len(old), start + block_rows)
        mapped[start:end] = apply_affine(old[start:end], model.arc2_coef)
    return mapped
