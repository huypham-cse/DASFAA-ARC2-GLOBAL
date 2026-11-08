"""Small offline CUDA encoder smoke. No benchmark texts, qrels or quality scores."""
from __future__ import annotations
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import traceback

def dump(path,obj):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(obj,indent=2)+'\n');temp.replace(path)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lock',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    args.output.mkdir(exist_ok=False)
    lock=json.loads(args.lock.read_text())
    record={'status':'RUNNING','scope':'synthetic-text GPU encoder smoke only',
            'pid':os.getpid(),'python':sys.version,'platform':platform.platform(),
            'benchmark_labels_requested_or_read':False,'models':{},'failures':[]}
    began=time.perf_counter()
    try:
        import numpy as np
        import torch
        import sentence_transformers
        import transformers
        from sentence_transformers import SentenceTransformer
        actual={'numpy':np.__version__,'torch':torch.__version__,
                'sentence_transformers':sentence_transformers.__version__,'transformers':transformers.__version__}
        if actual!=lock['gpu_versions']:raise ValueError(f'GPU runtime drift: {actual}')
        if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable')
        torch.set_num_threads(4);torch.manual_seed(17)
        torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
        torch.use_deterministic_algorithms(True)
        record.update(versions=actual,cuda_runtime=torch.version.cuda,
                      device_name=torch.cuda.get_device_name(0))
        docs=lock['toy_documents'];queries=lock['toy_queries']
        for label,spec in lock['models'].items():
            started=time.perf_counter();torch.cuda.reset_peak_memory_stats()
            model=SentenceTransformer(spec['path'],device='cuda',local_files_only=True,trust_remote_code=False)
            model.float();model.eval();model.max_seq_length=128
            if next(model.parameters()).device.type!='cuda':raise AssertionError('Model not on GPU')
            texts=[spec['document_prefix']+x for x in docs]+[spec['query_prefix']+x for x in queries]
            with torch.inference_mode():
                values=model.encode(texts,batch_size=4,show_progress_bar=False,
                                    convert_to_numpy=True,normalize_embeddings=True,precision='float32')
                repeat=model.encode(texts,batch_size=4,show_progress_bar=False,
                                    convert_to_numpy=True,normalize_embeddings=True,precision='float32')
            if values.dtype!=np.float32 or values.shape!=(len(texts),spec['dimension']):
                raise AssertionError('Encoder output shape/dtype')
            if not np.isfinite(values).all() or not np.allclose(np.linalg.norm(values,axis=1),1,atol=1e-5,rtol=0):
                raise AssertionError('Encoder output finite/unit check')
            difference=float(np.max(np.abs(values-repeat)))
            if difference>1e-6:raise AssertionError('Repeated deterministic encode drift')
            target=args.output/(label+'.npy');np.save(target,values,allow_pickle=False)
            record['models'][label]={'status':'PASS','revision':spec['revision'],
                'dimension':spec['dimension'],'max_seq_length':128,
                'document_prefix':spec['document_prefix'],'query_prefix':spec['query_prefix'],
                'documents':len(docs),'queries':len(queries),'repeat_count':2,
                'physical_toy_document_encodes':2*len(docs),'physical_toy_query_encodes':2*len(queries),
                'repeat_max_abs_difference':difference,'device':'cuda','dtype':'float32',
                'wall_seconds':time.perf_counter()-started,
                'own_peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated(),
                'own_peak_cuda_reserved_bytes':torch.cuda.max_memory_reserved(),
                'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
            dump(args.output/'metadata.json',record)
            del model,values,repeat;gc.collect();torch.cuda.empty_cache()
        record['status']='GPU_SMOKE_PASS'
    except BaseException as exc:
        record.update(status='FAILED_PRESERVED',failures=[repr(exc)],traceback=traceback.format_exc())
    finally:
        record['wall_seconds']=time.perf_counter()-began;dump(args.output/'metadata.json',record)
    print(json.dumps({'status':record['status'],'models':len(record['models'])}))
    return 0 if record['status']=='GPU_SMOKE_PASS' else 1

if __name__=='__main__':raise SystemExit(main())
