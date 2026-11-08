"""Verify an extracted development handoff or its ZIP using standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def digest(stream):
    h=hashlib.sha256()
    for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('package',type=Path,nargs='?',default=Path('.'))
    args=ap.parse_args();count=0
    if args.package.is_file():
        with zipfile.ZipFile(args.package) as archive:
            matches=[n for n in archive.namelist() if n.endswith('/PACKAGE_MANIFEST.json')]
            if len(matches)!=1:raise ValueError('Require one package manifest')
            prefix=matches[0][:-len('PACKAGE_MANIFEST.json')]
            manifest=json.loads(archive.read(matches[0]))
            for name,spec in manifest['files'].items():
                if Path(name).is_absolute() or '..' in Path(name).parts or ':' in name:raise ValueError('Escaping path')
                with archive.open(prefix+name) as stream:actual=digest(stream)
                if actual!=spec['sha256']:raise ValueError('Changed ZIP member: '+name)
                if archive.getinfo(prefix+name).file_size!=spec['bytes']:raise ValueError('Wrong member size')
                count+=1
    else:
        root=args.package.resolve();manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
        for name,spec in manifest['files'].items():
            path=(root/name).resolve()
            if not path.is_relative_to(root):raise ValueError('Escaping path')
            with path.open('rb') as stream:actual=digest(stream)
            if actual!=spec['sha256'] or path.stat().st_size!=spec['bytes']:raise ValueError('Changed file: '+name)
            count+=1
    print(json.dumps({'status':'PASS','files_verified':count,'scope':'Delivered byte hashes; not a new scientific run'}))


if __name__=='__main__':main()
