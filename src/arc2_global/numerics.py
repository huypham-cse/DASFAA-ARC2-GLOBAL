"""Unchanged selected validation, affine application and budget helpers."""
from __future__ import annotations
import numpy as np
DEFAULT_BLOCK_ROWS=512

def _vectors(name: str, value: np.ndarray, *, dim: int | None = None) -> np.ndarray:
    array = np.asarray(value)
    if array.dtype != np.float32 or array.ndim != 2 or not len(array):
        raise ValueError(f"{name} must be a nonempty float32 matrix")
    if dim is not None and array.shape[1] != dim:
        raise ValueError(f"{name} has incorrect dimension")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} contains NaN or Inf")
    if not np.allclose(np.linalg.norm(array, axis=1), 1.0, atol=1e-4, rtol=0):
        raise ValueError(f"{name} must contain L2-unit rows")
    return array


def _indices(name: str, value: np.ndarray, n_docs: int) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 1 or not np.issubdtype(array.dtype, np.integer):
        raise ValueError(f"{name} must be a 1D integer array")
    if len(array) != len(np.unique(array)) or np.any(array < 0) or np.any(array >= n_docs):
        raise ValueError(f"{name} has duplicates or out-of-range values")
    return array.astype(np.int64, copy=False)


def normalize_rows(value: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(value, axis=1, keepdims=True)
    if np.any(norms <= 1e-12) or not np.isfinite(value).all():
        raise ValueError("non-finite or zero row")
    return (value / norms).astype(np.float32)


def apply_affine(old_docs: np.ndarray, coef: np.ndarray) -> np.ndarray:
    """Normalized forward document map; no query mapping is performed."""
    old = np.asarray(old_docs)
    if old.ndim != 2 or old.dtype != np.float32 or coef.shape[0] != old.shape[1] + 1:
        raise ValueError("old documents/affine coefficient shape or dtype mismatch")
    x = np.concatenate((old, np.ones((len(old), 1), dtype=np.float32)), axis=1)
    return normalize_rows(x @ coef)


def select_for_budget(anchor_indices: np.ndarray, backfill_order: np.ndarray,
                      *, n_docs: int, fraction: float) -> np.ndarray:
    """Select exactly floor(fraction*N) unique IDs, charging anchors."""
    if not 0.0 <= fraction <= 1.0:
        raise ValueError("fraction must be in [0, 1]")
    anchors = _indices("anchor_indices", anchor_indices, n_docs)
    order = _indices("backfill_order", backfill_order, n_docs)
    if len(order) != n_docs:
        raise ValueError("backfill_order must be a full corpus permutation")
    target = int(np.floor(fraction * n_docs))
    if target < len(anchors):
        raise ValueError("budget is smaller than the anchor count")
    selected = set(map(int, anchors))
    for doc in map(int, order):
        if len(selected) == target:
            break
        selected.add(doc)
    result = np.asarray(sorted(selected), dtype=np.int64)
    if len(result) != target:
        raise AssertionError("could not fill destination-encoding budget")
    return result
