"""Verify saved B1b correctness artifacts; never load qrels or benchmark data."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    if a.output.exists():raise FileExistsError('Preserve verification receipts')
    run=a.run.resolve();m=json.loads((run/'metadata.json').read_text())
    assert m['status']=='B1B_BASELINE_ADAPTERS_PASS' and not m['failures']
    lock_bytes=subprocess.check_output(['git','show',m['code_commit']+':configs/b1b_lock.json'],cwd=ROOT)
    assert hashlib.sha256(lock_bytes).hexdigest()==m['lock_sha256']
    lock=json.loads(lock_bytes)
    assert m['new_qrel_reads']==0 and not m['benchmark_quality_scoring']
    assert not m['real_dataset_or_encoder_loaded']
    cpu=json.loads((run/'cpu_checks.json').read_text())
    assert cpu==m['cpu_checks'] and cpu['status']=='CPU_BASELINES_PASS'
    assert len(cpu['la2m'])==25 and len(cpu['ridge'])==15
    assert cpu['singleton_global_fallback'] and cpu['invalid_gallery_rejections']==3
    assert m['cpu_runtime']['versions']==lock['cpu_versions']
    for c in cpu['la2m']:
        assert c['max_raw_delta']<=1e-6 and c['nonanchor_target_invariance']
        assert c['paired_only_fit'] and c['paid_overwrite_and_unpaid_identity']
        if c['clusters']>1:assert c['local_maps']>=2
    for c in cpu['ridge']:
        assert c['coefficient_max_delta']<=1e-6 and c['lambda']==10
        assert c['bias_regularized'] and c['nonorthogonal']
    raw_parity=[]
    for seed in lock['seeds']:
        source=np.load(run/f'source_seed{seed}.npy',allow_pickle=False)
        target=np.load(run/f'target_seed{seed}.npy',allow_pickle=False)
        actual=np.load(run/f'la2m_adapter_seed{seed}.npy',allow_pickle=False)
        expected=np.load(run/f'la2m_official_seed{seed}.npy',allow_pickle=False)
        assert source.shape==(1152,384) and target.shape==actual.shape==expected.shape==(1152,768)
        assert np.isfinite(actual).all() and np.isfinite(expected).all()
        delta=float(np.max(np.abs(actual-expected)));assert delta<=1e-6
        raw_parity.append(delta)
    gpu=json.loads((run/'simplelinear_gpu/metadata.json').read_text())
    assert gpu==m['simplelinear'] and gpu['status']=='SIMPLELINEAR_OFFICIAL_CUDA_CHECKS_PASS'
    assert len(gpu['checks'])==5 and gpu['configuration']==lock['simplelinear_defaults']
    assert {k:v['version'] for k,v in gpu['modules'].items()}==lock['gpu_versions']
    folder=run/'simplelinear_gpu'
    anchors=np.load(folder/'anchors.npy',allow_pickle=False)
    paid=np.load(folder/'paid.npy',allow_pickle=False)
    target=np.load(folder/'target.npy',allow_pickle=False)
    assert len(anchors)==32 and len(paid)==48 and set(anchors)<=set(paid)
    unpaid=np.setdiff1d(np.arange(96),paid)
    for c in gpu['checks']:
        assert c['seed'] in lock['seeds'] and c['actual_affine_layers']==5
        assert c['activation']=='SELU' and c['epochs']==50 and c['batch_size']==4028
        assert c['initial_state_sha256']!=c['final_state_sha256']==c['direct_state_sha256']
        assert math.isfinite(c['gradient_norm']) and c['gradient_norm']>0
        assert math.isfinite(c['final_eval_loss']) and c['final_eval_loss']<c['initial_loss']
        seed=c['seed']
        actual=np.load(folder/f'adapter_seed{seed}.npy',allow_pickle=False)
        expected=np.load(folder/f'official_seed{seed}.npy',allow_pickle=False)
        proxy=np.load(folder/f'proxy_seed{seed}.npy',allow_pickle=False)
        gallery=np.load(folder/f'gallery_seed{seed}.npy',allow_pickle=False)
        assert actual.shape==expected.shape==proxy.shape==gallery.shape==(96,768)
        assert np.isfinite(actual).all() and np.isfinite(proxy).all()
        assert float(np.max(np.abs(actual-expected)))<=1e-6
        assert np.allclose(np.linalg.norm(proxy,axis=1),1,atol=1e-5,rtol=0)
        np.testing.assert_array_equal(gallery[paid],target[paid])
        np.testing.assert_array_equal(gallery[unpaid],proxy[unpaid])
    assert not list(run.rglob('*qrels*'))
    report={'status':'PASS','scope':'local artifact/array verification; not paper claim audit',
            'la2m_oracle_cases':25,'ridge_independent_cases':15,'official_simplelinear_cuda_cases':5,
            'main_shape':[1024,384,768],'main_la2m_clusters':20,
            'saved_main_la2m_max_delta':max(raw_parity),'new_qrel_reads':0,
            'benchmark_quality_results':False,'frozen_ARC2_changed':False,
            'next_action':'STOP - wait for user confirmation before B1-M'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
