"""Zero-update CUDA load check for an explicitly relocated owned checkpoint."""
import argparse,hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src'),str(ROOT/'ops')]
from b1p_neural_worker import identity,dump,sha,state_hash

def main():
    p=argparse.ArgumentParser();p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert not a.output.exists()
    lock=json.loads((ROOT/'configs/b1p_lock.json').read_text());record={'status':'VALIDATING','optimizer_updates':0,'qrel_reads':0,'started_utc':datetime.now(timezone.utc).isoformat()}
    identity(lock,{'code_commit':a.code_commit},record)
    import torch,numpy as np
    from arc2_global.embedding_converter import ConverterConfig,build_model,_state_hash
    item=lock['checkpoint_handoff'];checkpoint=Path(item['derivative_path']);assert sha(checkpoint)==item['derivative_sha256']
    proof=json.loads(Path(item['receipt_path']).read_text());assert sha(Path(item['receipt_path']))==item['receipt_sha256']
    assert proof['all_original_fields_verified'] and proof['tensor_equality_and_bytes_verified']
    saved=torch.load(checkpoint,map_location='cpu',weights_only=False);sid=saved['identity']
    assert saved['schema']=='embedding_converter_exact_resume_v1' and json.loads(json.dumps(sid))==proof['derivative_identity']
    assert sid['cuda_device']==torch.cuda.get_device_name() and sid['torch_version']==str(torch.__version__)
    assert sid['numpy_version']==np.__version__ and sid['cuda_runtime']==torch.version.cuda
    assert hashlib.sha256((ROOT/'src/arc2_global/embedding_converter.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==sid['converter_source_sha256_canonical_lf']
    cfg=dict(sid['config']);cfg['adam_betas']=tuple(cfg['adam_betas']);config=ConverterConfig(**cfg)
    assert config==ConverterConfig(device='cuda') and sid['seed']==17
    with torch.random.fork_rng(devices=[torch.cuda.current_device()]):
        torch.random.default_generator.manual_seed(sid['seed']);torch.cuda.default_generators[torch.cuda.current_device()].manual_seed(sid['seed'])
        model=build_model(sid['source']['shape'][1],sid['target']['shape'][1],config).to('cuda')
        assert _state_hash(model)==saved['initial_state_sha256']
        optimizer=torch.optim.Adam(model.parameters(),lr=config.learning_rate,betas=config.adam_betas,eps=config.adam_epsilon,weight_decay=0,amsgrad=False,foreach=False)
        model.load_state_dict(saved['model_state'],strict=True);optimizer.load_state_dict(saved['optimizer_state'])
        for key,value in model.state_dict().items():assert torch.equal(value.detach().cpu(),saved['model_state'][key]),key
        for parameter,old_id in zip(model.parameters(),saved['optimizer_state']['param_groups'][0]['params']):
            for key,value in optimizer.state[parameter].items():
                original=saved['optimizer_state']['state'][old_id][key]
                assert torch.equal(value.detach().cpu(),original),key
        torch.set_rng_state(saved['torch_cpu_rng_state']);torch.cuda.set_rng_state(saved['torch_cuda_rng_state'])
        assert torch.equal(torch.get_rng_state(),saved['torch_cpu_rng_state'])
        assert torch.equal(torch.cuda.get_rng_state(),saved['torch_cuda_rng_state'])
        rng=np.random.default_rng();rng.bit_generator.state=saved['numpy_rng_state'];assert rng.bit_generator.state==saved['numpy_rng_state']
        record.update(status='HANDOFF_TARGET_LOAD_PASS',current_step=saved['current_step'],selected_step=saved['selected_step'],model_state_hash=state_hash(model),model_and_Adam_exact_after_CUDA_load=True,CPU_CUDA_and_NumPy_RNG_restored=True,checkpoint_sha256=sha(checkpoint),qualification=proof['qualification'])
    assert sha(checkpoint)==item['derivative_sha256']
    dump(a.output,record);print(json.dumps({'status':record['status'],'current_step':record['current_step'],'optimizer_updates':0}))
if __name__=='__main__':main()
