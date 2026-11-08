"""Separately identified primal implementation of the frozen tangent updates.

This module does not replace ``model._tangent2`` or its historical backend.
Only the ridge solve changes: (X.T X + lambda I) delta = X.T target.
Initialization, tangent targets, bias regularization and storage are unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.linalg import cho_factor, cho_solve

from . import procrustes
from .model import (GlobalModel, MIN_ANCHORS, PARITY_ATOL, RIDGE_LAMBDA,
                    centered_affine_coefficient, _raw_affine)
from .numerics import _indices, _vectors, normalize_rows

BACKEND_ID = "arc2_global_tangent2_primal_float64_r1"


@dataclass(frozen=True)
class PrimalGlobalModel(GlobalModel):
    """Same model arrays, with explicit backend and regularization provenance."""

    backend_id: str = BACKEND_ID
    ridge_lambda: float = RIDGE_LAMBDA
    tangent_steps: int = 2


def tangent2_primal(old_anchors: np.ndarray, new_anchors: np.ndarray,
                    initial: np.ndarray, *, ridge_lambda: float = RIDGE_LAMBDA,
                    return_float64: bool = False
                    ) -> tuple[np.ndarray, np.ndarray]:
    """Return stored-float32 first/final coefficients; update in float64.

    ``initial`` must be the float64 raw affine expansion B0. Lambda10 is the
    frozen method; other positive lambdas are for separately named ablations.
    The intercept coordinate is regularized identically to every other column.
    No explicit inverse or n-by-n Gram matrix is constructed. For diagnostics,
    ``return_float64=True`` exposes copies before the float32 storage cast.
    """
    old = _vectors("old_anchors", old_anchors)
    new = _vectors("new_anchors", new_anchors)
    if len(old) != len(new) or len(old) < MIN_ANCHORS:
        raise ValueError("at least eight aligned anchor pairs are required")
    base = np.asarray(initial)
    if (base.dtype != np.float64 or base.shape != (old.shape[1] + 1, new.shape[1])
            or not np.isfinite(base).all()):
        raise ValueError("initial must be a finite float64 raw affine coefficient")
    if (isinstance(ridge_lambda, (bool, np.bool_))
            or not np.isscalar(ridge_lambda) or not np.isfinite(ridge_lambda)
            or ridge_lambda <= 0):
        raise ValueError("ridge_lambda must be a finite positive scalar")
    if not isinstance(return_float64, bool):
        raise ValueError("return_float64 must be boolean")
    x = np.concatenate((old.astype(np.float64),
                        np.ones((len(old), 1), dtype=np.float64)), axis=1)
    y = new.astype(np.float64)
    gram = x.T @ x + float(ridge_lambda) * np.eye(x.shape[1], dtype=np.float64)
    factor = cho_factor(gram, lower=True, overwrite_a=False, check_finite=True)
    coef = base.copy()
    first = None
    for step in (1, 2):
        z = x @ coef
        norms = np.linalg.norm(z, axis=1, keepdims=True)
        if np.any(norms <= 1e-12) or not np.isfinite(z).all():
            raise ValueError("invalid affine direction during ARC2-Global fit")
        unit = z / norms
        target = norms * (y - np.sum(unit * y, axis=1, keepdims=True) * unit)
        delta = cho_solve(factor, x.T @ target, check_finite=True)
        coef = coef + delta
        if not np.isfinite(coef).all():
            raise ValueError("non-finite ARC2-Global coefficient")
        if step == 1:
            first = coef.copy() if return_float64 else coef.astype(np.float32)
    return first, coef.copy() if return_float64 else coef.astype(np.float32)


def fit_arc2_global_primal(old_docs: np.ndarray, anchor_indices: np.ndarray,
                           new_anchor_vectors: np.ndarray, *, kernel=None,
                           ridge_lambda: float = RIDGE_LAMBDA) -> PrimalGlobalModel:
    """Fit ordered paid pairs with the identified primal backend.

    This is an opt-in API. The original fit function and dual backend remain
    unchanged. It accepts no queries, full-target corpus or relevance labels.
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
    pinned_raw = kernel.procrustes_apply(old_a, sm, tm, matrix)
    affine_raw = _raw_affine(old_a, base)
    for label, actual, expected in (
        ("raw", affine_raw, pinned_raw),
        ("normalized", normalize_rows(affine_raw), normalize_rows(pinned_raw)),
    ):
        if not np.allclose(actual, expected, atol=PARITY_ATOL, rtol=0):
            raise AssertionError(f"STOP: ARC2-Global centered affine {label} parity failed")
    first, final = tangent2_primal(old_a, new_a, base, ridge_lambda=ridge_lambda)
    return PrimalGlobalModel(
        anchors.copy(), old_a.copy(), new_a.copy(), sm.copy(), tm.copy(),
        matrix.copy(), base, first, final, ridge_lambda=float(ridge_lambda))


def compare_scored_rankings(reference_scores, actual_scores, reference_rank, actual_rank, k):
    """Describe top-k inversions, using each query's actual score drift bound.

    Caller supplies all-document ranks and finite scores from the same locked
    arithmetic/batching. Reference gaps > 2 epsilon are unexplained. All ties
    are ordered by ascending integer document row ID. No labels are accepted.
    """
    mismatches = []
    inversion_count = unexplained_count = membership_changed = 0
    epsilons = []
    for qi in range(len(reference_rank)):
        reference, candidate = reference_rank[qi, :k], actual_rank[qi, :k]
        finite = np.isfinite(reference_scores[qi]) & np.isfinite(actual_scores[qi])
        drift = float(np.max(np.abs(reference_scores[qi, finite].astype(np.float64)
                                    - actual_scores[qi, finite].astype(np.float64))))
        epsilons.append(drift)
        if np.array_equal(reference, candidate):
            continue
        union = np.union1d(reference, candidate)
        dp = np.empty(reference_rank.shape[1], dtype=np.int64)
        pp = np.empty(actual_rank.shape[1], dtype=np.int64)
        dp[reference_rank[qi]] = np.arange(len(dp))
        pp[actual_rank[qi]] = np.arange(len(pp))
        ordered = union[np.argsort(dp[union], kind="stable")]
        inversions = []
        for i, better in enumerate(ordered):
            for worse in ordered[i + 1:]:
                if pp[better] < pp[worse]:
                    continue
                gap = float(reference_scores[qi, better]) - float(reference_scores[qi, worse])
                unexplained = gap > 2 * drift
                inversions.append({"reference_better_id": int(better), "reference_worse_id": int(worse),
                                   "reference_score_gap": gap, "score_drift_bound": 2 * drift,
                                   "unexplained": bool(unexplained)})
                unexplained_count += int(unexplained)
        inversion_count += len(inversions)
        overlap = int(len(np.intersect1d(reference, candidate)))
        membership_changed += int(overlap != k)
        mismatches.append({"query_row": qi, "score_maxabs": drift,
                           "reference_top_ids": reference.tolist(), "actual_top_ids": candidate.tolist(),
                           "positions_changed": int(np.count_nonzero(reference != candidate)),
                           "membership_overlap": overlap, "inversions": inversions})
    return {"k": k, "queries": len(reference_rank), "queries_with_difference": len(mismatches),
            "queries_with_membership_difference": membership_changed,
            "ordered_agreement_fraction": 1. - len(mismatches) / len(reference_rank),
            "set_agreement_fraction": 1. - membership_changed / len(reference_rank),
            "score_maxabs": max(epsilons), "score_maxabs_per_query": epsilons,
            "inversion_count": inversion_count, "unexplained_inversion_count": unexplained_count,
            "mismatches": mismatches}


def compare_ranking_drift(queries, reference_proxy, actual_proxy, *, k=100, batch_rows=16,
                          query_ids=None, document_ids=None, exclude_identical_ids=False):
    """Qrel-free drift diagnostics using frozen retrieval float32 batches.

    Proxy inputs must already follow the frozen float32 normalization path.
    Exact ranks use stable score-descending sort, hence ascending row-ID ties.
    This reports differences without treating near-tie order changes as parity
    failures; callers apply their preregistered numeric and unexplained bounds.
    """
    reference = _vectors("reference_proxy", reference_proxy)
    actual = _vectors("actual_proxy", actual_proxy, dim=reference.shape[1])
    q = _vectors("queries", queries, dim=reference.shape[1])
    if actual.shape != reference.shape:
        raise ValueError("Proxy shapes must match")
    if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k <= len(reference):
        raise ValueError("Invalid k")
    if isinstance(batch_rows, bool) or not isinstance(batch_rows, int) or batch_rows < 1:
        raise ValueError("Invalid query batch")
    positions = None
    if exclude_identical_ids:
        if query_ids is None or document_ids is None:
            raise ValueError("Explicit IDs needed for identical-ID exclusion")
        if len(query_ids) != len(q) or len(document_ids) != len(reference):
            raise ValueError("IDs do not match vector rows")
        if len(set(document_ids)) != len(document_ids):
            raise ValueError("Duplicate document IDs")
        positions = {value: i for i, value in enumerate(document_ids)}
    summaries = []
    for start in range(0, len(q), batch_rows):
        ds = q[start:start + batch_rows] @ reference.T
        ps = q[start:start + batch_rows] @ actual.T
        if positions is not None:
            for j, qid in enumerate(query_ids[start:start + len(ds)]):
                if qid in positions:
                    ds[j, positions[qid]] = ps[j, positions[qid]] = -np.inf
            if np.any(np.isfinite(ds).sum(axis=1) < k):
                raise ValueError("Too few eligible documents")
        dr = np.argsort(-ds, axis=1, kind="stable")
        pr = np.argsort(-ps, axis=1, kind="stable")
        result = compare_scored_rankings(ds, ps, dr, pr, k)
        for mismatch in result["mismatches"]:
            mismatch["query_row"] += start
        summaries.append(result)
    changed = sum(row["queries_with_difference"] for row in summaries)
    membership = sum(row["queries_with_membership_difference"] for row in summaries)
    return {"k": k, "batch_rows": batch_rows, "queries": len(q),
            "queries_with_difference": changed, "queries_with_membership_difference": membership,
            "ordered_agreement_fraction": 1. - changed / len(q),
            "set_agreement_fraction": 1. - membership / len(q),
            "score_maxabs": max(row["score_maxabs"] for row in summaries),
            "score_maxabs_per_query": [e for row in summaries for e in row["score_maxabs_per_query"]],
            "inversion_count": sum(row["inversion_count"] for row in summaries),
            "unexplained_inversion_count": sum(row["unexplained_inversion_count"] for row in summaries),
            "mismatches": [m for row in summaries for m in row["mismatches"]],
            "score_arithmetic": "float32 query batch @ proxy.T",
            "tie_rule": "score descending, integer document row ID ascending",
            "exclude_identical_ids": exclude_identical_ids}
