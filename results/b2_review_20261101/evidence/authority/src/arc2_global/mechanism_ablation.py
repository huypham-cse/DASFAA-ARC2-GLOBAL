"""Named development ablations; the frozen ARC2-Global API is unchanged."""
import time
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from .model import centered_affine_coefficient
from .procrustes import procrustes_fit

ABLATION_ID='arc2_global_mechanism_dual_float64_r1'

def fit_tangent_path(source_pairs,target_pairs,*,ridge_lambda=10.0):
    """Keep float64 between updates; export float32 snapshots only at the end."""
    start=time.perf_counter()
    sm,tm,w=procrustes_fit(source_pairs,target_pairs,center=True)
    base=centered_affine_coefficient(sm,tm,w)
    phases={'procrustes_seconds':time.perf_counter()-start}
    x=np.concatenate((source_pairs.astype(np.float64),np.ones((len(source_pairs),1))),axis=1)
    y=target_pairs.astype(np.float64)
    start=time.perf_counter();gram=x@x.T+ridge_lambda*np.eye(len(x))
    phases['gram_seconds']=time.perf_counter()-start
    start=time.perf_counter();factor=cho_factor(gram,lower=True,check_finite=True)
    phases['factor_seconds']=time.perf_counter()-start
    coef=base.copy();snapshots=[]
    for step in (1,2):
        start=time.perf_counter();z=x@coef;norms=np.linalg.norm(z,axis=1,keepdims=True)
        if np.any(norms<=1e-12) or not np.isfinite(z).all():raise ValueError('Invalid tangent direction')
        unit=z/norms;target=norms*(y-np.sum(unit*y,axis=1,keepdims=True)*unit)
        phases[f'tangent_target{step}_seconds']=time.perf_counter()-start
        start=time.perf_counter();delta=x.T@cho_solve(factor,target,check_finite=True)
        coef=coef+delta
        if not np.isfinite(coef).all():raise ValueError('Nonfinite tangent coefficient')
        phases[f'solve_update{step}_seconds']=time.perf_counter()-start
        snapshots.append(coef.copy())
    return {'sm':sm,'tm':tm,'matrix':w,'base':base,
            'float64_steps':snapshots,'one':snapshots[0].astype(np.float32),
            'two':snapshots[1].astype(np.float32),'phases':phases,'lambda':ridge_lambda}
