"""Read-only inventory of pinned baseline sources and existing environments."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

BASE=Path('/root/arc2_global_paper_20261025')
UP=Path('/root/arc2_p3h_20261020/upstream_clean')

def main():
    result={'scope':'read-only baseline inventory; no fitting/data/qrels',
            'upstream':str(UP),'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=UP,text=True).strip(),
            'dirty':subprocess.check_output(['git','status','--porcelain'],cwd=UP,text=True).strip(),
            'source_sha256':{},'environments':{}}
    paths=sorted((UP/'src/embedding_translation').rglob('*.py'))+[UP/'reproduce-scripts/la2m/exp_la2m.py']
    for p in paths:result['source_sha256'][p.relative_to(UP).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    common="""import sys,json,importlib
r={'python':sys.version,'modules':{}}
"""
    cpu=common+"""for name in ['numpy','scipy','sklearn','psutil','threadpoolctl']:
 m=importlib.import_module(name);r['modules'][name]={'version':getattr(m,'__version__',None),'file':m.__file__}
print(json.dumps(r))
"""
    gpu=common+"""sys.path.insert(0,'/root/arc2_p3h_20261020/upstream_clean/src')
sys.path.extend(['/root/arc2_p3h_20261020/venv/lib/python3.11/site-packages','/root/miniforge3/envs/sandboxdp/lib/python3.11/site-packages'])
for name in ['numpy','scipy','torch','sklearn','pydantic','faiss','loguru','tqdm']:
 m=importlib.import_module(name);r['modules'][name]={'version':getattr(m,'__version__',None),'file':m.__file__}
from embedding_translation.config import MappingConfig,SimpleLinearMapperConfig
from embedding_translation.mapper.simple_linear.strategy import SimpleLinearMapper
r['simplelinear_defaults']=SimpleLinearMapperConfig().model_dump()
r['official_class_module']=SimpleLinearMapper.__module__
print(json.dumps(r))
"""
    env={**os.environ,'OPENBLAS_CORETYPE':'Haswell','OMP_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4',
         'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
    for name,py,code in [('cpu','/root/arc2_p3h_20261020/venv/bin/python',cpu),
                         ('gpu','/root/paper-P2/.venv/bin/python',gpu)]:
        p=subprocess.run([py,'-c',code],capture_output=True,text=True,env=env)
        result['environments'][name]={'python_executable':py,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    p=subprocess.run(['nvidia-smi','--query-gpu=name,uuid,memory.used,utilization.gpu','--format=csv,noheader'],capture_output=True,text=True)
    result['gpu_observation']=p.stdout.strip()
    out=BASE/'b1b_inventory_20261026.json'
    with out.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({'path':str(out),'source_files':len(paths),'environment_exit_codes':{k:v['rc'] for k,v in result['environments'].items()}}))

if __name__=='__main__':main()
