"""Write a NEW relocated protocol/lock draft; never run science or edit old locks."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import tarfile
import numpy
import scipy


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def main():
    root=Path(__file__).resolve().parents[1]
    old=root/'configs/tc1l_minilm_local_20261102_lock.json';lock=json.loads(old.read_text())
    suffix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    name='tc1l_relocated_'+suffix
    for role,filename in [('old_docs','old_docs.npy'),('new_docs','new_docs.npy'),('new_queries','new_queries.npy')]:
        relative='inputs/minilm_fiqa/'+filename
        if digest(root/relative)!=lock['data'][role]['sha256']:raise ValueError('Changed bundled vector cache')
        lock['data'][role]['path']=relative
    label=root/'inputs/minilm_fiqa/fiqa_dev.tsv'
    if digest(label)!=lock['qrels']['sha256']:raise ValueError('Changed historical DEV label bytes')
    archive_relative='inputs/minilm_fiqa/'+name+'_dev_labels.tar'
    with tarfile.open(root/archive_relative,'x') as archive:archive.add(label,arcname='fiqa_dev.tsv')
    lock['qrels'].update(archive=archive_relative,member='fiqa_dev.tsv')
    lock['id']=name
    lock['runtime']={'python':sys.version,'platform':platform.system(),'numpy':numpy.__version__,'scipy':scipy.__version__}
    protocol='protocols/'+name+'_DRAFT.md';lockname='configs/'+name+'_DRAFT.json'
    text=('# Relocated MiniLM control protocol DRAFT\n\n'
          'Review and COMMIT before any synthetic or scientific run.\n'
          'Carry forward all mathematical, exposure, K4 inference, gating and STOP rules\n'
          'from protocols/TC1L_MINILM_LOCAL_20261102.md. This is a new environment\n'
          'measurement with relocated byte-identical inputs; not an independent test.\n\n'
          'Runtime: '+json.dumps(lock['runtime'])+'\n\n'
          'Twenty rankings, four rows, five fixed seeds; E5 pending; no method tuning.\n')
    (root/protocol).write_text(text,encoding='utf-8')
    lock['protocol']=protocol;lock['source_sha256'][protocol]=digest(root/protocol)
    for source in list(lock['source_sha256']):lock['source_sha256'][source]=digest(root/source)
    (root/lockname).write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
    print('Draft only; no fit, retrieval, scoring or network request performed.')
    print('Review and commit:',protocol,lockname)
    print('Then run: python ops/tangent_control_local_campaign.py --lock '+lockname+' --output results/'+name)


if __name__=='__main__':main()
