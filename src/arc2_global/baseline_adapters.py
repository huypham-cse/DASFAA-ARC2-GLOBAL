"""External baseline adapters with paired-only fit APIs.

LA2M follows the pinned integration-script algorithm. SimpleLinear executes the
unmodified upstream package class. These are matched-budget adaptations, not
reproductions of the publications' original experimental setups.
"""
from dataclasses import dataclass
import importlib
import inspect
from pathlib import Path
import subprocess
import sys
import hashlib
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from .numerics import _vectors, _indices, normalize_rows
from .procrustes import procrustes_fit, procrustes_apply

UPSTREAM_REVISION='5e62baf1544264847ce3d8feeabd1ded6499b064'

def paired(source_pairs,target_pairs):
    x=_vectors('source_pairs',source_pairs);y=_vectors('target_pairs',target_pairs)
    if len(x)!=len(y):raise ValueError('Paired row counts differ')
    return x,y

@dataclass
class RidgeModel:
    coefficient: np.ndarray
    target_pairs: np.ndarray
    ridge_lambda: float=10.0

    def transform_raw(self,source):
        old=_vectors('source',source,dim=self.coefficient.shape[0]-1)
        augmented=np.concatenate((old,np.ones((len(old),1),dtype=np.float32)),axis=1)
        return augmented@self.coefficient

    def transform(self,source):return normalize_rows(self.transform_raw(source))

def fit_ridge(source_pairs,target_pairs):
    """Unconstrained affine ridge; lambda=10 regularizes bias as well."""
    x,y=paired(source_pairs,target_pairs)
    augmented=np.concatenate((x.astype(np.float64),np.ones((len(x),1))),axis=1)
    gram=augmented.T@augmented+10.0*np.eye(augmented.shape[1])
    coefficient=cho_solve(cho_factor(gram,lower=True),augmented.T@y.astype(np.float64))
    return RidgeModel(coefficient.astype(np.float32),y.copy())

@dataclass
class LA2MModel:
    kmeans: object
    local_maps: dict
    global_map: tuple
    anchor_labels: np.ndarray
    target_pairs: np.ndarray

    def transform_raw(self,source):
        old=_vectors('source',source,dim=self.global_map[0].shape[1])
        assigned=self.kmeans.predict(old)
        result=np.empty((len(old),self.target_pairs.shape[1]),dtype=np.float32)
        for cluster in np.unique(assigned):
            rows=np.flatnonzero(assigned==cluster)
            params=self.local_maps.get(int(cluster)) or self.global_map
            result[rows]=procrustes_apply(old[rows],*params)
        return result

    def transform(self,source):return normalize_rows(self.transform_raw(source))

def fit_la2m(source_pairs,target_pairs,*,seed,n_clusters=20):
    """Source-anchor KMeans and per-cluster centered rectangular Procrustes.

    The >=2 local-fit rule and singleton global fallback match the original
    integration script. This is not the package's PCA/same-dimension variant.
    """
    from sklearn.cluster import KMeans
    x,y=paired(source_pairs,target_pairs)
    if isinstance(n_clusters,bool) or not isinstance(n_clusters,int) or n_clusters<1:
        raise ValueError('Invalid cluster count')
    km=KMeans(n_clusters=min(n_clusters,len(x)),n_init=4,random_state=seed)
    labels=km.fit_predict(x)
    local={}
    for c in np.unique(labels):
        mask=labels==c
        local[int(c)]=procrustes_fit(x[mask],y[mask],center=True) if mask.sum()>=2 else None
    return LA2MModel(km,local,procrustes_fit(x,y,center=True),labels.copy(),y.copy())

def verify_upstream(root,source_hashes):
    root=Path(root).resolve(strict=True)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()
    if revision!=UPSTREAM_REVISION or dirty:raise ValueError('Upstream revision/cleanliness mismatch')
    for rel,digest in source_hashes.items():
        if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:
            raise ValueError('Upstream raw-byte drift: '+rel)
    return root

def official_components(upstream,source_hashes,dependency_fallbacks=()):
    root=verify_upstream(upstream,source_hashes)
    import torch
    # Existing GPU packages remain first. Append missing dependencies only;
    # do not install/upgrade another project's environment or replace torch.
    sys.path.insert(0,str(root/'src'))
    for path in dependency_fallbacks:
        if str(path) not in sys.path:sys.path.append(str(path))
    from embedding_translation.config import MappingConfig,SimpleLinearMapperConfig
    module=importlib.import_module('embedding_translation.mapper.simple_linear.strategy')
    expected=(root/'src/embedding_translation/mapper/simple_linear/strategy.py').resolve()
    if Path(inspect.getsourcefile(module.SimpleLinearMapper)).resolve()!=expected:
        raise ValueError('Imported class is not the pinned official source')
    return torch,MappingConfig,SimpleLinearMapperConfig,module.SimpleLinearMapper,module.SimpleLinearModel

@dataclass
class SimpleLinearModelAdapter:
    mapper: object
    target_pairs: np.ndarray
    configuration: dict

    def transform_raw(self,source):
        old=_vectors('source',source,dim=self.mapper.metadata['input_dim'])
        return np.asarray(self.mapper.transform(old),dtype=np.float32)

    def transform(self,source):return normalize_rows(self.transform_raw(source))

def fit_simplelinear(source_pairs,target_pairs,*,seed,device,upstream,
                     source_hashes,expected_defaults,dependency_fallbacks=()):
    """Official fit/transform; fixed 50-epoch final model on all supplied pairs."""
    x,y=paired(source_pairs,target_pairs)
    torch,MappingConfig,SimpleConfig,Mapper,_=official_components(upstream,source_hashes,dependency_fallbacks)
    scfg=SimpleConfig()
    if scfg.model_dump()!=expected_defaults:raise ValueError('Official configuration drift')
    if scfg.use_local_distill:raise ValueError('Local distillation is outside this adaptation')
    torch.manual_seed(seed)
    config=MappingConfig(device=device,simple_linear_config=scfg)
    mapper=Mapper(config)
    mapper.fit(x.copy(),y.copy(),np.arange(len(x),dtype=np.int64))
    return SimpleLinearModelAdapter(mapper,y.copy(),scfg.model_dump())

def mixed_gallery(proxies,fit_indices,fit_targets,paid_indices,paid_targets):
    """Shared unit proxies, then paid-only replacement; fitted pairs are paid."""
    proxy=_vectors('proxies',proxies)
    fit=_indices('fit_indices',fit_indices,len(proxy));paid=_indices('paid_indices',paid_indices,len(proxy))
    yf=_vectors('fit_targets',fit_targets,dim=proxy.shape[1])
    yp=_vectors('paid_targets',paid_targets,dim=proxy.shape[1])
    if len(fit)!=len(yf) or len(paid)!=len(yp):raise ValueError('Target/ID row mismatch')
    if not set(fit)<=set(paid):raise ValueError('Fit pairs not included in paid set')
    positions={int(index):row for row,index in enumerate(paid)}
    for row,index in enumerate(fit):
        if not np.array_equal(yf[row],yp[positions[int(index)]]):raise ValueError('Fitted target changed')
    gallery=proxy.copy();gallery[paid]=yp
    return gallery
