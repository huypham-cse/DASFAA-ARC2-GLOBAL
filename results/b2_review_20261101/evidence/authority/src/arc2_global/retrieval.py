"""Exact float32 inner-product retrieval with explicit deterministic tie order."""
import numpy as np
from .numerics import _vectors

def exact_topk(queries, documents, *, k=100, batch_rows=16,
               query_ids=None, document_ids=None, exclude_identical_ids=False):
    docs=_vectors('documents',documents)
    q=_vectors('queries',queries,dim=docs.shape[1])
    if isinstance(k,bool) or not isinstance(k,int) or not 1<=k<=len(docs):
        raise ValueError('Invalid k')
    if isinstance(batch_rows,bool) or not isinstance(batch_rows,int) or batch_rows<1:
        raise ValueError('Invalid query batch')
    if exclude_identical_ids:
        if query_ids is None or document_ids is None:
            raise ValueError('Explicit IDs needed for identical-ID exclusion')
        if len(query_ids)!=len(q) or len(document_ids)!=len(docs):
            raise ValueError('IDs do not match vector rows')
        if len(set(document_ids))!=len(document_ids):raise ValueError('Duplicate document IDs')
        positions={v:i for i,v in enumerate(document_ids)}
    result=np.empty((len(q),k),dtype=np.int64)
    for start in range(0,len(q),batch_rows):
        scores=q[start:start+batch_rows]@docs.T
        if exclude_identical_ids:
            for j,qid in enumerate(query_ids[start:start+len(scores)]):
                if qid in positions:scores[j,positions[qid]]=-np.inf
            if np.any(np.isfinite(scores).sum(axis=1)<k):
                raise ValueError('Too few eligible documents')
        result[start:start+len(scores)]=np.argsort(-scores,axis=1,kind='stable')[:,:k]
    return result
