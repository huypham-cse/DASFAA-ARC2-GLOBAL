"""Pinned Nano development encoding only. Never opens relevance files."""
import argparse,gc,json,os,sys,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'ops'))
from b1a_stage import dump,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--run',type=Path,required=True);a=ap.parse_args()
    lock=json.loads(a.lock.read_text());out=a.run/'encoding';out.mkdir(exist_ok=False)
    m={'status':'RUNNING','models':{},'new_qrel_reads':0,'failures':[]};start=time.perf_counter()
    try:
        import torch,sentence_transformers,transformers
        from sentence_transformers import SentenceTransformer
        versions={'numpy':np.__version__,'torch':torch.__version__,'sentence_transformers':sentence_transformers.__version__,'transformers':transformers.__version__}
        assert versions==lock['gpu_versions'],versions
        torch.set_num_threads(4);torch.manual_seed(17);torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
        m.update(versions=versions,device=torch.cuda.get_device_name(0),physical_document_encodes=0,physical_query_encodes=0)
        for label,spec in lock['models'].items():
            began=time.perf_counter();torch.cuda.reset_peak_memory_stats()
            model=SentenceTransformer(spec['path'],device='cuda',local_files_only=True,trust_remote_code=False)
            model.float();model.eval();model.max_seq_length=128
            values={}
            for dataset in lock['nano_datasets']:
                inputs=a.run/'inputs'/dataset
                texts=json.loads((inputs/'texts.json').read_text())
                folder=a.run/'vectors'/dataset;folder.mkdir(parents=True,exist_ok=True)
                for role,prefix in [('docs',spec['document_prefix']),('queries',spec['query_prefix'])]:
                    rows=[prefix+t for t in texts[role]]
                    with torch.inference_mode():
                        v=model.encode(rows,batch_size=32,show_progress_bar=False,convert_to_numpy=True,normalize_embeddings=True,precision='float32')
                    assert v.dtype==np.float32 and v.shape==(len(rows),spec['dimension'])
                    assert np.isfinite(v).all() and np.allclose(np.linalg.norm(v,axis=1),1,atol=1e-5,rtol=0)
                    path=folder/(label+'_'+role+'.npy');np.save(path,v,allow_pickle=False)
                    values[dataset+'_'+role]={'path':str(path.relative_to(a.run)),'sha256':sha(path),'shape':list(v.shape)}
                    m['physical_document_encodes' if role=='docs' else 'physical_query_encodes']+=len(rows)
                    del v
                    dump(out/'metadata.json',m)
            m['models'][label]={'outputs':values,'wall_seconds':time.perf_counter()-began,'own_peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated()}
            dump(out/'metadata.json',m);del model;gc.collect();torch.cuda.empty_cache()
        m['status']='ENCODING_PASS'
    except BaseException as exc:m.update(status='FAILED_PRESERVED',failures=[repr(exc)],traceback=traceback.format_exc())
    finally:m['wall_seconds']=time.perf_counter()-start;dump(out/'metadata.json',m)
    return 0 if m['status']=='ENCODING_PASS' else 1
if __name__=='__main__':raise SystemExit(main())
