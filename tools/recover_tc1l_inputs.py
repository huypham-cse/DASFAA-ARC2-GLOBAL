"""Recover only the two byte-identical MiniLM document caches from old TAR."""
import hashlib
import json
from pathlib import Path
import tarfile

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={'old_docs_1110a243fdf4.npy':'59b14828cfe583d279c6cd2f79365c169b573e8331dbf4c1f4ee241214c35782',
          'new_docs_842eaed40bee.npy':'a0d10483e5c02ddadee94aeb44da717d6fb068473702caac63249ee33a89ff56'}


def main():
    source=ROOT/'provenance/qa/cloud_backup_20261030/local_transport_20261030.tar'
    destination=ROOT/'.cache/tc1l_minilm';destination.mkdir(parents=True,exist_ok=True)
    rows=[]
    with tarfile.open(source) as archive:
        for member in archive.getmembers():
            name=Path(member.name).name
            if name not in EXPECTED:continue
            path=destination/name
            if not member.isfile() or path.exists():raise ValueError('Preserve input / require regular archive member')
            digest=hashlib.sha256()
            with archive.extractfile(member) as inp,path.open('xb') as out:
                for block in iter(lambda:inp.read(8*1024*1024),b''):
                    digest.update(block);out.write(block)
            if digest.hexdigest()!=EXPECTED[name]:raise ValueError('Recovered cache SHA mismatch; preserve for diagnosis')
            rows.append({'path':str(path),'sha256':digest.hexdigest(),'bytes':member.size,'archive_member':member.name})
    if len(rows)!=2:raise ValueError('Missing or duplicate cache members')
    receipt=ROOT/'provenance/qa/tc1l_input_recovery_20261102.json'
    with receipt.open('x',encoding='utf-8') as stream:
        json.dump({'source_archive':str(source),'scope':'Byte transport only; no numerical use, qrels, re-encoding or new rankings','files':rows},stream,indent=2);stream.write('\n')
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
