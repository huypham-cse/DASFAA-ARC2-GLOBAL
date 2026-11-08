"""Read-only source/environment inventory and public dataset metadata resolution.

Does not download dataset content, load labels, fit a method or encode texts.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import urllib.request

BASE=Path('/root/arc2_global_paper_20261025')
OLD=Path('/root/arc2_p3h_20261020')
INPUT=OLD/'p8i_work_20261022_4cb7ba7/artifact/results/p8i_full_r1_20261022'

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    output=BASE/'preflight_inventory.json'
    if output.exists():raise FileExistsError('Preserve previous inventory')
    source=json.loads((INPUT/'metadata.json').read_text())
    result={'scope':'read-only inventory and public metadata; no scientific run',
            'host':platform.node(),'platform':platform.platform(),'new_qrel_reads':0,
            'models':{},'dataset_metadata':{},'environments':{},'commands':{}}
    for label,record in source['models'].items():
        directory=OLD/'p3h_b_models'/label
        actual={rel:sha(directory/rel) for rel in record['file_sha256']}
        result['models'][label]={'path':str(directory),**record,'actual_file_sha256':actual,
                                'matches_original':actual==record['file_sha256']}
    for name,docs in [('NanoNQ',5035),('NanoHotpotQA',5090),('NanoFEVER',4996)]:
        repo='zeta-alpha-ai/'+name
        url=f'https://huggingface.co/api/datasets/{repo}?blobs=true'
        with urllib.request.urlopen(url,timeout=60) as response:metadata=json.load(response)
        siblings=[r for r in metadata['siblings'] if r['rfilename'].startswith(('corpus/','queries/')) and r['rfilename'].endswith('.parquet')]
        if {r['rfilename'].split('/')[0] for r in siblings}!={'corpus','queries'}:
            raise ValueError('Missing corpus/query files in metadata')
        result['dataset_metadata'][name]={'repo':repo,'revision':metadata['sha'],
             'expected_docs':docs,'expected_queries':50,'files':siblings,
             'qrels_requested_or_read':False}
    probe='''import importlib.metadata as md,importlib,sys,json
names=['numpy','scipy','torch','sentence_transformers','transformers','pyarrow','psutil','threadpoolctl']
r={'python':sys.version,'modules':{}}
for name in names:
 try:
  mod=importlib.import_module(name)
  r['modules'][name]={'version':getattr(mod,'__version__',None),'file':getattr(mod,'__file__',None)}
 except Exception as exc:r['modules'][name]={'error':repr(exc)}
print(json.dumps(r))
'''
    env={**os.environ,'OPENBLAS_CORETYPE':'Haswell','OMP_NUM_THREADS':'4',
         'OPENBLAS_NUM_THREADS':'4','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
    for label,python in [('cpu',str(OLD/'venv/bin/python')),('gpu','/root/paper-P2/.venv/bin/python')]:
        p=subprocess.run([python,'-c',probe],capture_output=True,text=True,env=env)
        result['environments'][label]={'python_executable':python,'rc':p.returncode,
                                     'stdout':p.stdout,'stderr':p.stderr}
    for label,argv in [('gpu',['nvidia-smi','--query-gpu=name,uuid,memory.total,memory.used,utilization.gpu','--format=csv,noheader']),
                       ('processes',['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader']),
                       ('disk',['df','-h',str(BASE)])]:
        p=subprocess.run(argv,capture_output=True,text=True)
        result['commands'][label]={'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    result['fiqa_manifest']={'path':str(INPUT/'manifest.json'),'sha256':sha(INPUT/'manifest.json')}
    result['reference_root']=str(OLD/'p8_r10_work_20261025')
    guard=Path('/root/gpu-allowlist-guard-20261025-vericache/owner_stop_20261025.json')
    if guard.exists():result['guard_owner_stop_record']=json.loads(guard.read_text())
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'INVENTORY_WRITTEN','path':str(output),
                      'models_match':all(v['matches_original'] for v in result['models'].values()),
                      'dataset_revisions':{k:v['revision'] for k,v in result['dataset_metadata'].items()}}))

if __name__=='__main__':main()
