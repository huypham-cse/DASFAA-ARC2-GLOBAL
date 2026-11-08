"""Read-only sizes for ARC2 project folders; never deletes/moves anything."""
import json
import os
from pathlib import Path
import shutil
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]


def size_tree(path):
    stack=[str(path)];total=count=0;errors=[];reparse=[]
    while stack:
        current=stack.pop()
        try:
            with os.scandir(current) as entries:
                for e in entries:
                    try:
                        st=e.stat(follow_symlinks=False)
                        if getattr(st,'st_file_attributes',0)&0x400:
                            reparse.append(e.path);continue
                        if e.is_dir(follow_symlinks=False):stack.append(e.path)
                        elif e.is_file(follow_symlinks=False):total+=st.st_size;count+=1
                    except OSError as exc:errors.append({'path':e.path,'error':str(exc)})
        except OSError as exc:errors.append({'path':current,'error':str(exc)})
    return {'path':str(path),'logical_bytes':total,'files':count,'errors':errors,'reparse_skipped':reparse}


def main():
    drive=Path('D:/');usage=shutil.disk_usage(drive)
    rows=[]
    for p in sorted(drive.iterdir()):
        if p.is_dir() and (p.name.startswith(('DASFAA-','ARC2-','mixindex-')) or p.name in ['graph4paper','tmp']):
            row=size_tree(p);rows.append(row)
            print(json.dumps({'path':row['path'],'GiB':row['logical_bytes']/2**30,'files':row['files'],'errors':len(row['errors'])}),flush=True)
    files=[{'path':str(p),'bytes':p.stat().st_size} for p in drive.iterdir() if p.is_file() and p.name.startswith('DASFAA-')]
    out={'utc':datetime.now(timezone.utc).isoformat(),'drive':'D:',
         'disk':{'total_bytes':usage.total,'used_bytes':usage.used,'free_bytes':usage.free},
         'scope':'Read-only logical file sizes; no cloud completeness or deletion inferred from filenames.',
         'directories':rows,'root_project_files':files}
    (ROOT/'provenance/qa/handoff_disk_inventory_20261102.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'free_GiB':usage.free/2**30,'total_GiB':usage.total/2**30,'audited':len(rows)}))


if __name__=='__main__':main()
