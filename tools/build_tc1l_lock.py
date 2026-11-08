"""Pin verified recovered inputs and the distinct Windows MiniLM-only run."""
import hashlib
import json
from pathlib import Path
import sys
import numpy
import scipy

ROOT=Path(__file__).resolve().parents[1]


def spec(path):
    path=Path(path)
    actual=path if path.is_absolute() else ROOT/path
    h=hashlib.sha256()
    with actual.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return {'path':str(path),'sha256':h.hexdigest()}


def main():
    original=json.loads((ROOT/'configs/tangent_control_20261102_lock.json').read_text())
    data={
        'old_docs':spec('.cache/tc1l_minilm/old_docs_1110a243fdf4.npy'),
        'new_docs':spec('.cache/tc1l_minilm/new_docs_842eaed40bee.npy'),
        'new_queries':spec('D:/DASFAA-2027-MixIndex/artifact/results/q16c_arc2_dev/q16c_encode_20261018T003211/dev_queries.npy')}
    expected={'old_docs':'59b14828cfe583d279c6cd2f79365c169b573e8331dbf4c1f4ee241214c35782',
              'new_docs':'a0d10483e5c02ddadee94aeb44da717d6fb068473702caac63249ee33a89ff56',
              'new_queries':'826911a012bb37e0b117f0929517ee3c21345dc9f402cda71c47cf677a550375'}
    assert all(data[k]['sha256']==v for k,v in expected.items())
    sources=['protocols/TC1L_MINILM_LOCAL_20261102.md','tools/build_tc1l_lock.py',
             'ops/tangent_control_local_run.py','ops/tangent_control_local_score.py',
             'ops/tangent_control_local_campaign.py','ops/tangent_control_run.py','ops/b1m_score.py']
    sources += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'src/arc2_global').glob('*.py'))]
    lock={'id':'tc1l_minilm_local_20261102_r1','scope':'MiniLM-only local FiQA development; E5 pending',
          'protocol':sources[0],'parent_lock_sha256':spec('configs/tangent_control_20261102_lock.json')['sha256'],
          'pairs':['minilm_distilroberta'],'seeds':[17,29,41,53,67],
          'methods':['procrustes','tangent2','chordal2','euclidean2'],'budget':.5,'anchor_count':1024,'lambda':10,'steps':2,
          'data':data,'ids':spec('results/fiqa_development/ids.json'),
          'anchors':{str(s):spec(f'results/fiqa_development/selections/anchors_seed_{s}.npy') for s in original['seeds']},
          'paid50':{str(s):spec(f'results/fiqa_development/selections/seed{s}_50pct.npy') for s in original['seeds']},
          'runtime':{'python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,'platform':'Windows'},'blas_threads':4,
          'expected_full_rankings':20,'expected_smoke_rankings':4,
          'qrels':{'archive':'provenance/qa/cloud_backup_20261030/local_transport_20261030.tar',
                   'member':'root/arc2_p3h_20261020/p8_r10_work_20261025/artifact/data/p4_fiqa_minilm_distilroberta/source/fiqa-extracted/fiqa/qrels/dev.tsv',
                   'sha256':original['qrels']['sha256'],'already_inspected_development':True},
          'model_provenance':{k:v for k,v in original['model_provenance'].items() if k in ['minilm_x','distilroberta_y']},
          'bootstrap':{'draws':20000,'seed':20261102,'family_size':4,'observed_contrasts':2,'E5_pending':2,'quantiles':[.00625,.99375]},
          'source_sha256':{p:spec(p)['sha256'] for p in sources},
          'STOP':'After local verification/report/ARIS; before manuscript, method, regrade, E5 or new study'}
    with (ROOT/'configs/tc1l_minilm_local_20261102_lock.json').open('x',encoding='utf-8') as stream:
        json.dump(lock,stream,indent=2);stream.write('\n')
    print('TC1L local draft lock created; all three vector hashes match original.')


if __name__=='__main__':main()
