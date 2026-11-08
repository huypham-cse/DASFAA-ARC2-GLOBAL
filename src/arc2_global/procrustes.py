"""Procrustes kernels extracted unchanged from embedding-translation.

Apache-2.0; revision 5e62baf1544264847ce3d8feeabd1ded6499b064.
Original: reproduce-scripts/la2m/exp_la2m.py. See THIRD_PARTY_NOTICES.md.
"""
import numpy as np

def procrustes_fit(src, tgt, center=True):
    """Orthogonal isometry src->tgt (cross-dim OK). Returns sm,tm,W.

    center=True (ours): mean-centred Procrustes -- subtract the source/target
    means before the SVD and add the target mean back at apply time, so the map
    captures the cloud translation as well as the rotation.
    center=False: a pure rotation about the origin (W from svd(tgt^T src), no
    mean terms), i.e. the un-centred isometry without mean-offset alignment.
    """
    if center:
        sm = src.mean(0, keepdims=True)
        tm = tgt.mean(0, keepdims=True)
    else:
        sm = np.zeros((1, src.shape[1]), dtype=np.float32)
        tm = np.zeros((1, tgt.shape[1]), dtype=np.float32)
    M = (tgt - tm).T @ (src - sm)                    # (d_tgt, d_src)
    U, _, Vt = np.linalg.svd(M, full_matrices=False)
    W = (U @ Vt).astype(np.float32)                  # (d_tgt, d_src), semi-orthogonal
    return sm.astype(np.float32), tm.astype(np.float32), W


def procrustes_apply(x, sm, tm, W):
    return ((x - sm) @ W.T + tm).astype(np.float32)
