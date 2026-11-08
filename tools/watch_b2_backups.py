"""Incremental local backup for one exact B2 campaign; credentials stay in RAM.

Reuses the tested ranged SSH transport, Windows long paths and whole-file SHA
acceptance from the B1c operator. This script never launches scientific work.
"""
import argparse
import re
import sys
import watch_b1c_r3_backups as backup

REMOTE = r'''
import hashlib,json,pathlib,sys,collections
project=pathlib.Path(sys.argv[1]).resolve(); name=sys.argv[2]
previous=json.load(sys.stdin); files=[]
def read(p,default):
    return json.loads(p.read_text()) if p.exists() else default
schedule=project/'results'/('b2_schedule_'+name)
status=read(schedule/'metadata.json',{}).get('status')
terminal=bool(status and status!='RUNNING')
failed=terminal and status!='B2_SCORED_STOP_FOR_REVIEW'
full=project/'results'/('b2_full_'+name)
cells=read(full/'cells_pre_qrels.json',[])
counts=collections.Counter((c['pair'],c['seed'],c['method']) for c in cells if c['seed'] is not None)
groups={p+'_seed'+str(s)+'_'+m for (p,s,m),n in counts.items() if n==3}
for kind in ('schedule','assets','encode_smoke','smoke','encode_full','full'):
    root=project/'results'/('b2_'+kind+'_'+name)
    if not root.exists(): continue
    ready=terminal
    if kind=='assets': ready=ready or read(root/'acquisition_manifest.json',{}).get('status')=='ACQUISITION_PASS'
    elif kind.startswith('encode_'): ready=ready or read(root/'encoding_manifest.json',{}).get('status') in ('SMOKE_ENCODING_PASS','ENCODING_PASS')
    elif kind=='smoke': ready=ready or read(root/'metadata.json',{}).get('status')=='B2_SMOKE_PASS'
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.is_symlink() or p.name.endswith(('.tmp','.writing')): continue
        if not p.resolve().is_relative_to(project): raise ValueError('Escaping remote output')
        rel=p.relative_to(project).as_posix()
        complete=ready or (kind=='full' and any('/cpu/'+g+'/' in '/'+rel or '/neural/'+g+'/' in '/'+rel for g in groups))
        small=p.suffix in ('.json','.jsonl','.log')
        early=kind=='full' and ('/rankings/' in rel or '/endpoints/' in rel or '/inputs/' in rel)
        # Active checkpoints/partially-filled tensors are preserved server-side;
        # copy after fit/encoding completion, not while their contents change.
        if not (complete or early or small): continue
        st=p.stat(); stamp=[st.st_size,st.st_mtime_ns]; old=previous.get(rel,{})
        if old.get('stat')==stamp: digest=old['sha256']
        else:
            h=hashlib.sha256()
            with p.open('rb') as stream:
                for block in iter(lambda:stream.read(1024*1024),b''): h.update(block)
            digest=h.hexdigest()
        after=p.stat()
        if [after.st_size,after.st_mtime_ns]!=stamp: continue
        mutable=p.suffix in ('.log','.jsonl') or p.name in ('metadata.json','progress.json','cells_pre_qrels.json','encoding_manifest.json','acquisition_manifest.json')
        files.append({'path':rel,'stat':stamp,'sha256':digest,'immutable':bool(complete or early) and not mutable,'priority':0 if complete or early else 1})
print(json.dumps({'files':files,'completed_groups':sorted(groups),'campaign_status':status,'terminal':terminal,'failed':failed}))
'''


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--remote-project', required=True)
    parser.add_argument('--name', required=True)
    args, remaining = parser.parse_known_args()
    if not re.fullmatch(r'/home/jovyan/arc2_b2_20261031/code_[0-9a-f]{7,40}', args.remote_project):
        raise ValueError('Only the explicitly deployed B2 checkout is allowed')
    if not re.fullmatch(r'[a-z0-9_]+', args.name):
        raise ValueError('Unsafe campaign name')
    backup.PROJECT = args.remote_project
    backup.CAMPAIGN = args.name
    backup.RELOCATED_FULL = args.remote_project
    backup.REMOTE = REMOTE
    if '--local-root' not in remaining:
        remaining += ['--local-root', 'D:/ARC2-B2-backup-20261031']
    sys.argv = [sys.argv[0]] + remaining
    return backup.main()


if __name__ == '__main__':
    raise SystemExit(main())
