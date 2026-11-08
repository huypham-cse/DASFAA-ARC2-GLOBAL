"""Verify synchronized B1a artifacts without labels or rerunning a benchmark."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from arc2_global import select_for_budget

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    if a.output.exists():raise FileExistsError('Preserve verification receipts')
    r=a.run.resolve();lock=json.loads((ROOT/'configs/b1a_r1_lock.json').read_text())
    meta=json.loads((r/'metadata.json').read_text())
    assert meta['status']=='B1A_INPUTS_AND_GPU_SMOKE_PASS' and meta['failures']==[]
    assert meta['code_commit']=='f9774835df2b3442b6e61cfd61320864533abdae'
    # The actual Linux deployment uses committed Git bytes; a Windows working
    # copy can have CRLF. Verify exact deployed bytes, plus parsed local identity.
    committed_lock=subprocess.check_output(['git','show',meta['code_commit']+':configs/b1a_r1_lock.json'],cwd=ROOT)
    assert meta['lock_sha256']==hashlib.sha256(committed_lock).hexdigest()
    assert json.loads(committed_lock)==lock
    assert meta['new_qrel_reads']==0 and not meta['benchmark_rankings_generated']
    assert not meta['independent_scoring']
    runtime=meta['cpu_runtime']
    assert runtime['numpy']=='2.4.6' and runtime['scipy']=='1.17.1'
    assert runtime['environment']=={'OPENBLAS_CORETYPE':'Haswell','OMP_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4'}
    assert runtime['upstream_raw_sha256']==lock['upstream_sha256']
    synth=json.loads((r/'synthetic_checks.json').read_text())
    assert synth['status']=='PASS' and len(synth['reference_parity'])==4
    assert all(c['exact_reference_parity'] and c['blocks']==[1,13,512] for c in synth['reference_parity'])
    paid_count=0;anchor_order_count=0
    for name,spec in lock['datasets'].items():
        receipt=meta['nano'][name];folder=r/'inputs'/name
        assert (receipt['docs'],receipt['queries'])==(spec['expected_docs'],50)
        ids=json.loads((folder/'ids.json').read_text())
        assert len(ids['doc_ids'])==spec['expected_docs'] and len(set(ids['doc_ids']))==spec['expected_docs']
        assert len(ids['query_ids'])==50 and len(set(ids['query_ids']))==50
        assert sha(folder/'ids.json')==receipt['ids_sha256']
        assert not receipt['qrels_requested_or_read']
        for f in spec['files']:
            assert sha(folder/f['rfilename'])==f['lfs']['sha256']
        for filename,record in receipt['anchor_order_files'].items():
            assert sha(folder/filename)==record['sha256'];anchor_order_count+=1
        assert len(receipt['anchor_order_files'])==10
        for seed in lock['seeds']:
            anchors=np.load(folder/f'anchors_seed{seed}.npy',allow_pickle=False)
            order=np.load(folder/f'order_seed{seed}.npy',allow_pickle=False)
            assert len(anchors)==1024 and len(set(anchors))==1024
            np.testing.assert_array_equal(np.sort(order),np.arange(spec['expected_docs']))
            previous=set()
            for fraction in [.25,.5,.75]:
                filename=f'paid_seed{seed}_{int(fraction*100)}pct.npy'
                assert sha(folder/filename)==receipt['paid_sets'][filename]['sha256']
                selected=np.load(folder/filename,allow_pickle=False)
                np.testing.assert_array_equal(selected,select_for_budget(anchors,order,n_docs=spec['expected_docs'],fraction=fraction))
                assert previous<=set(selected);previous=set(selected);paid_count+=1
    fiqa=meta['fiqa'];assert len(fiqa['vectors'])==8
    assert fiqa['ordered_ids_equal'] and fiqa['anchors_and_backfill_equal']
    order=np.load(ROOT/'results/fiqa_development/backfill_order.npy',allow_pickle=False)
    for seed in lock['seeds']:
        anchors=np.load(ROOT/f'results/fiqa_development/selections/anchors_seed_{seed}.npy',allow_pickle=False)
        for fraction in [.25,.5,.75]:
            filename=f'paid_seed{seed}_{int(fraction*100)}pct.npy';path=r/'inputs/FiQA'/filename
            assert sha(path)==fiqa['paid_sets'][filename]['sha256']
            np.testing.assert_array_equal(np.load(path,allow_pickle=False),select_for_budget(anchors,order,n_docs=57638,fraction=fraction));paid_count+=1
    gpu=meta['gpu_smoke'];assert gpu['status']=='GPU_SMOKE_PASS' and len(gpu['models'])==4
    for label,record in gpu['models'].items():
        path=r/'gpu_smoke'/(label+'.npy');assert sha(path)==record['output_sha256']
        values=np.load(path,allow_pickle=False)
        assert values.shape==(16,lock['models'][label]['dimension']) and values.dtype==np.float32
        assert np.isfinite(values).all() and np.allclose(np.linalg.norm(values,axis=1),1,atol=1e-5,rtol=0)
        assert record['device']=='cuda' and record['repeat_max_abs_difference']<=1e-6
    for name,record in meta['toy_mixed_gallery_checks'].items():
        path=r/f'toy_{name}_rankings.npy';assert sha(path)==record['ranking_sha256']
        values=np.load(path,allow_pickle=False);assert values.shape==(4,3)
        assert values.min()>=0 and values.max()<12
    assert len(meta['toy_mixed_gallery_checks'])==2
    assert list((r).rglob('*qrels*'))==[]
    report={'status':'PASS','scope':'artifact/hash/selection verification, not scientific claim audit',
            'nano_collections':3,'nano_documents':15121,'fiqa_documents':57638,
            'development_documents_ready':72759,'paid_sets_verified':paid_count,
            'new_anchor_order_arrays_verified':anchor_order_count,'fiqa_vector_files_verified_remotely':8,
            'reference_dimension_cases':4,'cuda_models':4,'toy_mixed_galleries':2,
            'new_qrel_reads':0,'benchmark_quality_scores_generated':False,
            'next_action':'STOP - user confirmation required before B1b'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
