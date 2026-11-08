"""Fit the unchanged two-update ARC2-Global map to user-supplied vectors."""
from pathlib import Path
import argparse,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from arc2_global import fit_arc2_global,transform_old_docs
p=argparse.ArgumentParser();p.add_argument('--old-docs',required=True);p.add_argument('--anchor-indices',required=True);p.add_argument('--target-anchors',required=True);p.add_argument('--output',required=True)
args=p.parse_args();out=Path(args.output)
if out.exists():raise SystemExit('Refuse to overwrite output')
old=np.load(args.old_docs,allow_pickle=False);anchors=np.load(args.anchor_indices,allow_pickle=False);target=np.load(args.target_anchors,allow_pickle=False)
model=fit_arc2_global(old,anchors,target)
np.save(out,transform_old_docs(old,model),allow_pickle=False)
print('Saved ARC2-Global document proxies:',out)
