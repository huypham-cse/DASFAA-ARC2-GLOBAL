"""Freeze TC1 cache/code identities before any synthetic or scientific run."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    original=json.loads((ROOT/'configs/b1c_r3_sources.json').read_text())
    inventory=json.loads((ROOT/'provenance/qa/tangent_control_inventory_20261102.json').read_text())
    assert all(f['match'] for f in inventory['files'])
    assert inventory['runtime_exit']==0
    runtime=json.loads(inventory['runtime'])
    groups=[]; seen=set()
    for g in original['groups']:
        identity=(g['pair'],g['seed'])
        if g['dataset']!='FiQA' or identity in seen:continue
        seen.add(identity)
        c=next(c for c in g['cases'] if c['budget']=='75pct')
        row={k:g[k] for k in ['pair','seed','old_docs','new_queries','ids','anchors','full_target_reference']}
        row.update(paid75=c['paid'],targets75=c['target_source']['file'])
        local=f"results/fiqa_development/selections/seed{g['seed']}_50pct.npy"
        row['paid50']={'path':local,'sha256':sha(ROOT/local)}
        groups.append(row)
    assert len(groups)==10
    groups.sort(key=lambda g:(g['pair'],g['seed']))
    models=json.loads((ROOT/'configs/b1m_lock.json').read_text())['models']
    sources=['protocols/FIQA_MATCHED_RESIDUAL_CONTROLS_20261102.md',
             'tools/build_tangent_control_lock.py','ops/tangent_control_run.py',
             'ops/tangent_control_score.py','ops/tangent_control_campaign.py','ops/b1m_score.py']
    sources += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'src/arc2_global').glob('*.py'))]
    ids='results/fiqa_development/ids.json'
    alias=json.loads((ROOT/'results/b1c_r3_review_20261031/evidence/run/scoring/qrel_path_alias_FiQA.json').read_text())
    lock={'id':'fiqa_matched_residual_controls_20261102_r1',
          'protocol':sources[0],'scope':'FiQA inspected DEV; unchanged ARC2; mechanism controls only',
          'runtime':{'python':runtime['python'],'numpy':runtime['numpy'],'scipy':runtime['scipy'],
                     'cpu_python':'/network-volume/arc2_recovery_20261030/envs/cpu/bin/python'},
          'execution_endpoint':{'host':'103.73.232.201','port':62161,'device':'cpu','cgroup_cpu_quota':inventory['cpu_quota']},
          'blas_threads':4,'pairs':['minilm_distilroberta','e5_small_base'],
          'seeds':[17,29,41,53,67],'budget':.5,'anchor_count':1024,
          'lambda':10,'steps':2,'methods':['procrustes','tangent2','chordal2','euclidean2'],
          'expected_full_rankings':40,'expected_smoke_rankings':8,
          'ids':{'path':ids,'sha256':sha(ROOT/ids)},'groups':groups,
          'model_provenance':models,
          'qrels':{'path':alias['resolved_path'],'sha256':alias['sha256_unchanged'],
                   'already_inspected_development':True},
          'source_sha256':{p:sha(ROOT/p) for p in sources},
          'bootstrap':{'draws':20000,'seed':20261102,'family_size':4,'quantiles':[.00625,.99375]},
          'STOP':'After full local verification/report/ARIS; before manuscript/method/new-study changes'}
    path=ROOT/'configs/tangent_control_20261102_lock.json'
    with path.open('x',encoding='utf-8') as stream:json.dump(lock,stream,indent=2);stream.write('\n')
    print('Frozen',len(groups),'groups,',len(sources),'code/protocol sources; lockSHA',sha(path))


if __name__=='__main__':main()
