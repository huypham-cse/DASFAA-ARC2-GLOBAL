from pathlib import Path
import subprocess,os,json,sys,time
r=Path('/root/arc2_global_paper_20261025/mini_bootstrap_20261026')
def run(argv,env=None):
 print('COMMAND',argv,flush=True)
 p=subprocess.run(argv,env=env)
 if p.returncode:raise RuntimeError('setup command failed '+str(p.returncode))
run([sys.executable,'-m','pip','install','--target',str(r/'uv'),'uv'])
uv=str(r/'uv/bin/uv');env={**os.environ,'UV_PYTHON_INSTALL_DIR':str(r/'python')}
run([uv,'python','install','3.11.17'],env)
py=subprocess.check_output([uv,'python','find','3.11.17'],env=env,text=True).strip()
run([uv,'venv','--python',py,'/root/arc2_p3h_20261020/venv'],env)
run([uv,'venv','--python',py,'/root/paper-P2/.venv'],env)
run([uv,'pip','install','--python','/root/arc2_p3h_20261020/venv/bin/python','numpy==2.4.6','scipy==1.17.1','scikit-learn==1.5.1','psutil'],env)
run([uv,'pip','install','--python','/root/paper-P2/.venv/bin/python','torch==2.6.0+cu124','--index-url','https://download.pytorch.org/whl/cu124'],env)
run([uv,'pip','install','--python','/root/paper-P2/.venv/bin/python','numpy==2.2.6','scipy==1.15.3','scikit-learn==1.6.1','pydantic==2.14.1','faiss-cpu==1.15.1','loguru==0.7.3','tqdm==4.70.1','psutil','pyyaml','pandas'],env)
(r/'completed.json').write_text(json.dumps({'status':'ENVIRONMENT_INSTALL_COMPLETE','python':py,'finished_unix':time.time()}))
