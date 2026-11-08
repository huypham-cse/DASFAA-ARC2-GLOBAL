"""Reconstruct the exact old R3 manifest files into a NEW empty directory."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('output',type=Path)
    args=ap.parse_args();root=Path(__file__).resolve().parents[1]
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    mapping=json.loads((root/'handoff/R3_MAPPING.json').read_text())
    manifest=json.loads((root/'archive/r3/RELEASE_MANIFEST.json').read_text())
    for name,spec in manifest['files'].items():
        source=(root/mapping[name]).resolve();target=(output/name).resolve()
        if not source.is_relative_to(root) or not target.is_relative_to(output):raise ValueError('Escaping source/target')
        if hashlib.sha256(source.read_bytes()).hexdigest()!=spec['sha256']:raise ValueError('R3 source mismatch')
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    shutil.copyfile(root/'archive/r3/RELEASE_MANIFEST.json',output/'RELEASE_MANIFEST.json')
    checksum=root/'archive/r3/CHECKSUMS.sha256'
    if checksum.exists():shutil.copyfile(checksum,output/'CHECKSUMS.sha256')
    print(json.dumps({'status':'R3_RECONSTRUCTED','files':len(manifest['files']),'output':str(output)}))


if __name__=='__main__':main()
