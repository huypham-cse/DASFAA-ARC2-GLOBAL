"""Official SimpleLinear CUDA validation on synthetic anchor pairs only."""
from __future__ import annotations
import argparse
import gc
import hashlib
import importlib
import json
from pathlib import Path
import platform
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

def dump(path,obj):
    temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(obj,indent=2)+'\n');temporary.replace(path)

def state_hash(model):
    h=hashlib.sha256()
    for name,value in model.state_dict().items():
        h.update(name.encode());h.update(value.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lock',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    args.output.mkdir(exist_ok=False);lock=json.loads(args.lock.read_text())
    began=time.perf_counter()
    record={'status':'RUNNING','scope':'official-code synthetic adapter validation only',
            'new_qrel_reads':0,'real_dataset_or_encoder_loaded':False,'checks':[],
            'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'failures':[]}
    try:
        import numpy as np
        import torch
        from arc2_global.baseline_adapters import official_components,fit_simplelinear,mixed_gallery
        from arc2_global.numerics import normalize_rows,select_for_budget
        if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable')
        torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
        torch,MappingConfig,SimpleConfig,Mapper,Model=official_components(
            lock['upstream'],lock['upstream_raw_sha256'],lock['dependency_fallbacks'])
        modules={}
        for name in lock['gpu_versions']:
            mod=importlib.import_module(name)
            modules[name]={'version':mod.__version__,'file':mod.__file__}
        if {k:v['version'] for k,v in modules.items()}!=lock['gpu_versions']:
            raise ValueError('GPU dependency version drift')
        record.update(modules=modules,cuda_runtime=torch.version.cuda,device=torch.cuda.get_device_name(0),
                      official_mapper_file=sys.modules[Mapper.__module__].__file__)
        defaults=SimpleConfig().model_dump()
        if defaults!=lock['simplelinear_defaults']:raise ValueError('Official defaults changed')
        rng=np.random.default_rng(17)
        old=normalize_rows(rng.normal(size=(96,384)).astype(np.float32))
        target=normalize_rows(old@rng.normal(size=(384,768)).astype(np.float32))
        anchors=np.sort(rng.choice(96,32,replace=False)).astype(np.int64)
        paid=select_for_budget(anchors,np.arange(96),n_docs=96,fraction=.5)
        x,y=old[anchors].copy(),target[anchors].copy()
        np.save(args.output/'source.npy',old,allow_pickle=False)
        np.save(args.output/'target.npy',target,allow_pickle=False)
        np.save(args.output/'anchors.npy',anchors,allow_pickle=False)
        np.save(args.output/'paid.npy',paid,allow_pickle=False)
        for seed in lock['seeds']:
            started=time.perf_counter();torch.cuda.reset_peak_memory_stats();torch.manual_seed(seed)
            initial=Model(384,768,hidden_dim=defaults['hidden_dim'],layer_num=defaults['layer_num'],activation=defaults['activation']).to('cuda')
            initial_hash=state_hash(initial)
            tx=torch.from_numpy(x).to('cuda');ty=torch.from_numpy(y).to('cuda')
            with torch.no_grad():
                pred=initial(tx)
                initial_loss=float((torch.nn.functional.mse_loss(pred,ty)+.5*(1-torch.nn.functional.cosine_similarity(pred,ty,dim=1).mean())).item())
            del initial,pred
            adapter=fit_simplelinear(x,y,seed=seed,device='cuda',upstream=lock['upstream'],
                source_hashes=lock['upstream_raw_sha256'],expected_defaults=defaults,
                dependency_fallbacks=lock['dependency_fallbacks'])
            raw=adapter.transform_raw(old);mapper=adapter.mapper
            if next(mapper.model.parameters()).device.type!='cuda':raise AssertionError('Not CUDA')
            linears=sum(isinstance(layer,torch.nn.Linear) for layer in mapper.model.layers)
            if linears!=5 or not isinstance(mapper.model.activation,torch.nn.SELU):raise AssertionError('Official architecture differs')
            if not isinstance(mapper.optimizer,torch.optim.AdamW):raise AssertionError('Optimizer differs')
            if mapper._cosine_weight!=.5:raise AssertionError('Official loss differs')
            if len(mapper.scheduler.state_dict())==0:raise AssertionError('Scheduler absent')
            final_hash=state_hash(mapper.model)
            mapper.model.zero_grad()
            loss=mapper._combined_loss(mapper.model(tx),ty);final_loss=float(loss.item());loss.backward()
            gradients=[p.grad for p in mapper.model.parameters()]
            if any(g is None or not torch.isfinite(g).all() for g in gradients):raise AssertionError('Invalid gradients')
            gradient_norm=float(torch.sqrt(sum((g*g).sum() for g in gradients)).item())
            if gradient_norm<=0 or final_hash==initial_hash or final_loss>=initial_loss:
                raise AssertionError('Synthetic training failed to update/reduce loss')
            # Independent direct use of the exact authors' class with the same
            # seed/config/data. No additional optimizer step is taken above.
            torch.manual_seed(seed)
            direct=Mapper(MappingConfig(device='cuda',simple_linear_config=SimpleConfig()))
            direct.fit(x.copy(),y.copy(),np.arange(len(x),dtype=np.int64))
            expected=np.asarray(direct.transform(old),dtype=np.float32)
            delta=float(np.max(np.abs(raw-expected)))
            if delta>1e-6:raise AssertionError('Adapter vs official-direct prediction drift')
            if state_hash(direct.model)!=final_hash:raise AssertionError('Same-seed final states differ')
            proxy=normalize_rows(raw)
            if not np.isfinite(proxy).all():raise AssertionError('Nonfinite normalized proxy')
            gallery=mixed_gallery(proxy,anchors,y,paid,target[paid])
            np.testing.assert_array_equal(gallery[paid],target[paid])
            unpaid=np.setdiff1d(np.arange(96),paid)
            np.testing.assert_array_equal(gallery[unpaid],proxy[unpaid])
            np.save(args.output/f'adapter_seed{seed}.npy',raw,allow_pickle=False)
            np.save(args.output/f'official_seed{seed}.npy',expected,allow_pickle=False)
            np.save(args.output/f'proxy_seed{seed}.npy',proxy,allow_pickle=False)
            np.save(args.output/f'gallery_seed{seed}.npy',gallery,allow_pickle=False)
            record['checks'].append({'seed':seed,'status':'PASS','fit_pairs':32,'dims':[384,768],
                'actual_affine_layers':linears,'activation':'SELU','epochs':50,'batch_size':4028,
                'initial_loss':initial_loss,'final_eval_loss':final_loss,'gradient_norm':gradient_norm,
                'initial_state_sha256':initial_hash,'final_state_sha256':final_hash,
                'direct_state_sha256':state_hash(direct.model),'max_raw_prediction_delta':delta,
                'paid_documents':48,'paid_only_overwrite_and_unpaid_identity':True,
                'official_reported_last_epoch_loss':mapper.metadata['final_loss'],
                'wall_seconds':time.perf_counter()-started,
                'own_peak_cuda_allocated_bytes':torch.cuda.max_memory_allocated()})
            dump(args.output/'metadata.json',record)
            del adapter,mapper,direct,tx,ty,raw,expected,proxy,loss,gradients;gc.collect();torch.cuda.empty_cache()
        record.update(status='SIMPLELINEAR_OFFICIAL_CUDA_CHECKS_PASS',configuration=defaults,
                      policy='fixed final epoch on supplied pairs; no early stopping/checkpoint selection')
    except BaseException as exc:
        record.update(status='FAILED_PRESERVED',failures=[repr(exc)],traceback=traceback.format_exc())
    finally:
        record['wall_seconds']=time.perf_counter()-began;dump(args.output/'metadata.json',record)
    print(json.dumps({'status':record['status'],'checks':len(record['checks']),'failures':record['failures']}))
    return 0 if record['status']=='SIMPLELINEAR_OFFICIAL_CUDA_CHECKS_PASS' else 1

if __name__=='__main__':raise SystemExit(main())
