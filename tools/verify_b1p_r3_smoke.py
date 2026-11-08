"""Verify copied Mini smoke receipts; no training or label access."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    assert not a.output.exists();r=a.run;manifest=read(r/'full_manifest.json');smoke=r/'smoke'
    for p in smoke.rglob('*'):
        if p.is_file():
            item=manifest['files'][p.relative_to(smoke).as_posix()]
            assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],str(p)
    meta=read(smoke/'metadata.json');assert meta['status']=='B1P_SMOKE_PASS' and not meta['failures']
    blob=subprocess.check_output(['git','show',meta['code_commit']+':configs/b1p_lock.json'],cwd=ROOT)
    assert hashlib.sha256(blob).hexdigest()==meta['lock_sha256'];lock=json.loads(blob)
    assert not meta['TREC_access'] and meta['new_physical_document_encodes']==0
    assert len(meta['smoke_checks'])==6
    ranks=list((smoke/'rankings').glob('*.npy'));assert len(ranks)==6
    for p in ranks:
        x=np.load(p,allow_pickle=False);assert x.shape==(8,100) and x.dtype.kind in 'iu'
        assert x.min()>=0 and x.max()<256 and not np.any(np.diff(np.sort(x,axis=1),axis=1)==0)
    for name,expected in [('exit7',7),('sigterm',-15)]:
        assert read(smoke/'process_tests'/name/'process_exit.json')['returncode']==expected
    workers=list(smoke.glob('neural/*/worker/metadata.json'));assert len(workers)==2
    for p in workers:
        m=read(p);assert m['status']=='B1P_NEURAL_SMOKE_PASS' and not m['failures']
        assert m['new_qrel_reads']==0 and m['unpaid_target_reads']==0
        assert m['device']==lock['execution_device']['name']
        assert {k:v['version'] for k,v in m['modules'].items()}==lock['gpu_versions']
        assert read(p.parent.parent/'process_exit.json')['returncode']==0
    converter=next(p.parent for p in workers if read(p)['method']=='embedding_converter')
    neighbors=read(converter/'neighbor_parity.json')['checks'];assert len(neighbors)==38
    assert all(row['dense_exact_ids_equal'] for row in neighbors)
    resume=read(converter/'resume_parity.json')['checks'];assert len(resume)==2
    assert {row['phase'] for row in resume}=={'selection','refit'}
    assert all(all(row['equalities'].values()) for row in resume)
    m=read(converter/'metadata.json')
    assert m['config']['iterations']==500 and m['refit_iterations']==m['selected_iteration']
    receipt={'status':'PASS','code_commit':meta['code_commit'],'six_methods':6,'dense_neighbor_checks':38,
        'exact_resume_cases':2,'synthetic_exit_cases':2,'TREC_access':False,'verifier_qrel_reads':0,
        'scope':'compact receipt/hash/recovery verification; large weights/proxies remain remote; no full-quality claim'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
if __name__=='__main__':main()
