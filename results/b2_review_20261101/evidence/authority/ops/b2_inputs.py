"""B2 explicit pinned acquisition and qrel-free encoding; no implicit hub access.

Each invocation requires a fresh output directory. Failed artifacts are retained;
chunk journals are evidence, not authorization to resume a failed scientific run.
The lock contains ``acquisition`` copied verbatim from b2_acquisition.json.
"""
import argparse
import gc
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import traceback
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def dump(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def peak_rss_bytes():
    # Linux server ru_maxrss is KiB. Windows is only used for metadata QA.
    if sys.platform == 'win32':
        return None
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)


def load_lock(lock):
    if isinstance(lock, dict):
        # Roundtrip prevents mutations leaking into callers.
        value = json.loads(json.dumps(lock))
        digest = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        source = 'in-memory canonical JSON'
    else:
        path = Path(lock)
        value, digest, source = json.loads(path.read_text(encoding='utf-8')), sha(path), str(path.resolve())
    a = value.get('acquisition', value)
    if a.get('schema_version') != 1:
        raise ValueError('Unknown acquisition schema')
    d = a['dataset']
    if d['repo'] != 'BeIR/trec-covid' or (d['expected_docs'], d['expected_queries']) != (171332, 50):
        raise ValueError('B2 requires full TREC-COVID')
    if {r['role'] for r in d['files']} != {'docs', 'queries'} or len(d['files']) != 2:
        raise ValueError('Only corpus and queries may be acquired')
    expected_paths = {'docs': 'corpus/corpus-00000-of-00001.parquet',
                      'queries': 'queries/queries-00000-of-00001.parquet'}
    for r in d['files']:
        if r['path'] != expected_paths[r['role']]:
            raise ValueError('Dataset path is not allowlisted')
    e = a['encoding']
    if (e['batch_size'], e['max_seq_length'], e['chunk_rows'], e['seed']) != (32, 128, 4096, 17):
        raise ValueError('Encoding numerical policy drift')
    for label, spec in a['models'].items():
        if not re.fullmatch(r'[a-z0-9_]+', label) or spec['max_seq_length'] != 128:
            raise ValueError('Invalid model label or length')
    return value, a, {'path': source, 'sha256': digest}


def check_code(lock, code_commit=None):
    """Real deployment Git identity and all canonical-LF source pins."""
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if code_commit is None:
        code_commit = head
    if not re.fullmatch(r'[0-9a-f]{40}', code_commit) or head != code_commit:
        raise ValueError('Deployment HEAD differs from code_commit')
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True)
    if dirty.strip():
        raise ValueError('Tracked deployment files are dirty')
    pins = lock['source_sha256_canonical_lf']
    if 'ops/b2_inputs.py' not in pins or 'configs/b2_acquisition.json' not in pins:
        raise ValueError('B2 acquisition implementation/config not source-pinned')
    for rel, digest in pins.items():
        data = (ROOT / rel).read_bytes().replace(b'\r\n', b'\n')
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError('Canonical source drift: ' + rel)
    return code_commit


def pinned_url(repo, revision, path, dataset=False):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repo')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Unpinned revision')
    p = PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or '\\' in path or any('qrel' in part.lower() for part in p.parts):
        raise ValueError('Disallowed acquisition path')
    prefix = 'datasets/' if dataset else ''
    return 'https://huggingface.co/' + prefix + repo + '/resolve/' + revision + '/' + urllib.parse.quote(path, safe='/')


def download(url, path, digest, size=None):
    if not re.fullmatch(r'[0-9a-f]{64}', digest):
        raise ValueError('Missing full file SHA256')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + '.download')
    began = time.perf_counter()
    with urllib.request.urlopen(url, timeout=60) as response, partial.open('xb') as f:
        for block in iter(lambda: response.read(8 * 1024 * 1024), b''):
            f.write(block)
        f.flush()
        os.fsync(f.fileno())
    if sha(partial) != digest or (size is not None and partial.stat().st_size != size):
        raise ValueError('Pinned download identity mismatch: ' + str(path))
    partial.rename(path)
    return {'sha256': digest, 'bytes': path.stat().st_size, 'url': url,
            'wall_seconds': time.perf_counter() - began}


def acquire(lock, out, code_commit=None):
    """Acquire only explicit corpus/query/model files into a fresh assets dir."""
    value, a, identity = load_lock(lock)
    code_commit = check_code(value, code_commit)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    m = {'status': 'RUNNING', 'started_utc': now(), 'lock': identity, 'code_commit': code_commit,
         'files': {}, 'qrels_requested_or_read': False, 'failures': []}
    dump(out / 'acquisition_manifest.json', m)
    try:
        d = a['dataset']
        for r in d['files']:
            rel = 'input/' + r['role'] + '.parquet'
            m['files'][rel] = download(pinned_url(d['repo'], d['revision'], r['path'], True),
                                       out / rel, r['sha256'], r['bytes'])
            dump(out / 'acquisition_manifest.json', m)
        for label, spec in a['models'].items():
            for name, digest in spec['file_sha256'].items():
                rel = 'models/' + label + '/' + name
                m['files'][rel] = download(pinned_url(spec['id'], spec['revision'], name), out / rel, digest)
                dump(out / 'acquisition_manifest.json', m)
        check_code(value, code_commit)
        m.update(status='ACQUISITION_PASS', source_check_before_and_after=True)
    except BaseException as exc:
        m.update(status='FAILED_PRESERVED', failures=[repr(exc)], traceback=traceback.format_exc())
        try:
            check_code(value, code_commit)
            m['source_check_after_failure'] = 'PASS'
        except BaseException as source_exc:
            m['source_check_after_failure'] = repr(source_exc)
        raise
    finally:
        m.update(ended_utc=now(), wall_seconds=time.perf_counter()-start, peak_rss_bytes=peak_rss_bytes())
        dump(out / 'acquisition_manifest.json', m)
    return m


def verify_assets(a, assets):
    assets = Path(assets)
    manifest = json.loads((assets / 'acquisition_manifest.json').read_text())
    if manifest['status'] != 'ACQUISITION_PASS' or manifest['qrels_requested_or_read'] is not False:
        raise ValueError('Assets were not successfully acquired without labels')
    files = {}
    for r in a['dataset']['files']:
        files['input/' + r['role'] + '.parquet'] = (r['sha256'], r['bytes'])
    for label, spec in a['models'].items():
        for rel, digest in spec['file_sha256'].items():
            files['models/' + label + '/' + rel] = (digest, None)
    if set(manifest['files']) != set(files):
        raise ValueError('Acquisition file inventory mismatch')
    checked = {}
    for rel, (digest, size) in files.items():
        path = assets / rel
        if sha(path) != digest or (size is not None and path.stat().st_size != size):
            raise ValueError('Asset drift: ' + rel)
        checked[rel] = {'sha256': digest, 'bytes': path.stat().st_size}
    return checked


def read_inputs(a, assets):
    import pyarrow.parquet as pq
    rows = {}
    for role in ['docs', 'queries']:
        cols = ['_id', 'title', 'text'] if role == 'docs' else ['_id', 'text']
        values = pq.read_table(Path(assets) / 'input' / (role + '.parquet'), columns=cols).to_pylist()
        if len(values) != a['dataset']['expected_' + role]:
            raise ValueError('Dataset count mismatch: ' + role)
        if any(not isinstance(r['_id'], str) or not isinstance(r['text'], str) for r in values):
            raise ValueError('Unexpected ID/text schema')
        ids = [r['_id'] for r in values]
        if len(set(ids)) != len(ids):
            raise ValueError('Duplicate ' + role + ' IDs')
        if role == 'docs':
            if any(not isinstance(r['title'], str) for r in values):
                raise ValueError('Unexpected title schema')
            texts = [(r['title'] + ' ' + r['text']).strip() for r in values]
        else:
            texts = [r['text'] for r in values]
        rows[role] = (ids, texts)
    return rows


def encode(lock, assets, out, smoke=False, code_commit=None):
    """Encode fixed original-order inputs with hash-verified local models only."""
    value, a, identity = load_lock(lock)
    code_commit = check_code(value, code_commit)
    out, assets = Path(out), Path(assets)
    out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    m = {'status': 'RUNNING', 'mode': 'smoke' if smoke else 'full', 'started_utc': now(),
         'lock': identity, 'code_commit': code_commit, 'qrels_requested_or_read': False, 'models': {}, 'failures': [],
         'physical_document_encodes_completed': 0, 'physical_query_encodes_completed': 0}
    dump(out / 'encoding_manifest.json', m)
    try:
        # Set before importing torch. No hub fallback or remote code.
        os.environ.update(CUBLAS_WORKSPACE_CONFIG=':4096:8', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
        import numpy as np
        import torch
        import sentence_transformers
        import transformers
        import pyarrow
        from sentence_transformers import SentenceTransformer
        versions = {'numpy': np.__version__, 'torch': torch.__version__,
                    'sentence_transformers': sentence_transformers.__version__, 'transformers': transformers.__version__}
        if versions != a['encode_versions']:
            raise ValueError('Encoding runtime version drift: ' + repr(versions))
        m.update(versions=versions, python=sys.version, pyarrow_version=pyarrow.__version__,
                 inputs=verify_assets(a, assets), acquisition_manifest_sha256=sha(assets/'acquisition_manifest.json'))
        torch.set_num_threads(4)
        torch.manual_seed(17)
        torch.cuda.manual_seed_all(17)
        torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        torch.backends.cudnn.benchmark = False
        m.update(cuda_device=torch.cuda.get_device_name(0), cuda_version=torch.version.cuda)
        rows = read_inputs(a, assets)
        if smoke:
            rows = {role: (ids[:a['encoding']['smoke_'+role]], texts[:a['encoding']['smoke_'+role]])
                    for role, (ids, texts) in rows.items()}
        ids = {'doc_ids': rows['docs'][0], 'query_ids': rows['queries'][0],
               'row_order': a['dataset']['row_order']}
        dump(out / 'ids.json', ids)
        m['ids'] = {'path': 'ids.json', 'sha256': sha(out/'ids.json')}
        (out/'vectors').mkdir()
        (out/'journals').mkdir()
        dump(out / 'encoding_manifest.json', m)
        for label, spec in a['models'].items():
            began = time.perf_counter()
            torch.cuda.reset_peak_memory_stats()
            model = SentenceTransformer(str(assets/'models'/label), device='cuda',
                                        local_files_only=True, trust_remote_code=False)
            model.float()
            model.eval()
            model.max_seq_length = 128
            rec = {'started_utc': now(), 'model_id': spec['id'], 'revision': spec['revision'],
                   'max_seq_length': 128, 'outputs': {}}
            m['models'][label] = rec
            for role in ['docs', 'queries']:
                texts = rows[role][1]
                prefix = spec['document_prefix' if role == 'docs' else 'query_prefix']
                path = out/'vectors'/(label+'_'+role+'.npy')
                shape = (len(texts), spec['dimension'])
                arr = np.lib.format.open_memmap(path, mode='w+', dtype=np.float32, shape=shape)
                journal_path = out/'journals'/(label+'_'+role+'.jsonl')
                rec['active'] = {'role': role, 'attempted_start': None, 'completed_rows': 0}
                with journal_path.open('x', encoding='utf-8', newline='\n') as journal:
                    for s in range(0, len(texts), a['encoding']['chunk_rows']):
                        stop = min(s+a['encoding']['chunk_rows'], len(texts))
                        rec['active'].update(attempted_start=s, attempted_stop=stop)
                        dump(out/'encoding_manifest.json', m)
                        tick = time.perf_counter()
                        with torch.inference_mode():
                            v = model.encode([prefix+t for t in texts[s:stop]], batch_size=32,
                                             show_progress_bar=False, convert_to_numpy=True,
                                             normalize_embeddings=True, precision='float32')
                        if v.dtype != np.float32 or v.shape != (stop-s, spec['dimension']) or not np.isfinite(v).all():
                            raise ValueError('Invalid encoded tensor: '+label+' '+role)
                        if not np.allclose(np.linalg.norm(v, axis=1), 1, atol=1e-5, rtol=0):
                            raise ValueError('Non-unit encoded tensor: '+label+' '+role)
                        arr[s:stop] = v
                        arr.flush()
                        with path.open('rb') as synced:
                            os.fsync(synced.fileno())
                        item = {'start': s, 'stop': stop, 'completed_utc': now(),
                                'float32_chunk_sha256': hashlib.sha256(v.tobytes(order='C')).hexdigest(),
                                'wall_seconds': time.perf_counter()-tick}
                        journal.write(json.dumps(item, sort_keys=True)+'\n')
                        journal.flush()
                        os.fsync(journal.fileno())
                        m['physical_document_encodes_completed' if role == 'docs' else 'physical_query_encodes_completed'] += stop-s
                        rec['active']['completed_rows'] = stop
                        m['peak_rss_bytes'] = peak_rss_bytes()
                        dump(out/'encoding_manifest.json', m)
                        del v
                del arr
                rec['outputs'][role] = {'path': str(path.relative_to(out)), 'sha256': sha(path),
                                         'shape': list(shape), 'dtype': 'float32',
                                         'journal_path': str(journal_path.relative_to(out)), 'journal_sha256': sha(journal_path)}
                rec.pop('active')
                dump(out/'encoding_manifest.json', m)
            rec.update(ended_utc=now(), wall_seconds=time.perf_counter()-began,
                       own_peak_cuda_allocated_bytes=torch.cuda.max_memory_allocated())
            del model
            gc.collect()
            torch.cuda.empty_cache()
            dump(out/'encoding_manifest.json', m)
        if verify_assets(a, assets) != m['inputs']:
            raise ValueError('Corpus/query/model input bytes changed during encoding')
        if sha(assets/'acquisition_manifest.json') != m['acquisition_manifest_sha256']:
            raise ValueError('Acquisition manifest changed during encoding')
        check_code(value, code_commit)
        m.update(status='SMOKE_ENCODING_PASS' if smoke else 'ENCODING_PASS', source_check_before_and_after=True,
                 asset_check_before_and_after=True)
    except BaseException as exc:
        m.update(status='FAILED_PRESERVED', failures=[repr(exc)], traceback=traceback.format_exc())
        try:
            check_code(value, code_commit)
            m['source_check_after_failure'] = 'PASS'
        except BaseException as source_exc:
            m['source_check_after_failure'] = repr(source_exc)
        raise
    finally:
        m.update(ended_utc=now(), wall_seconds=time.perf_counter()-start, peak_rss_bytes=peak_rss_bytes())
        dump(out/'encoding_manifest.json', m)
    return m


def main():
    # Equivalent stage spelling is convenient for finite campaign launchers.
    argv = sys.argv[1:]
    if '--stage' in argv:
        pos = argv.index('--stage')
        stage = argv[pos+1]
        argv = [{'smoke': 'smoke-encode'}.get(stage, stage)] + argv[:pos] + argv[pos+2:]
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for command in ['acquire', 'smoke-encode', 'encode']:
        q = sub.add_parser(command)
        q.add_argument('--lock', type=Path, required=True)
        q.add_argument('--out', type=Path, required=True)
        q.add_argument('--code-commit', required=True)
        if command != 'acquire':
            q.add_argument('--assets', type=Path, required=True)
    args = p.parse_args(argv)
    if args.command == 'acquire':
        acquire(args.lock, args.out, code_commit=args.code_commit)
    else:
        encode(args.lock, args.assets, args.out, smoke=args.command == 'smoke-encode', code_commit=args.code_commit)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
