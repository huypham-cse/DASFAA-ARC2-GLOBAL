"""Hash-pinned whole-group B1c recovery; never resumes a partial fit.

The builder is read-only and can inventory the frozen failed run before the
recovery protocol is committed. Execution requires its exact committed hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

IDENTITY = ('dataset', 'pair', 'method', 'seed', 'regime')
MUTABLE_CODE = {'ops/b1c_stage.py', 'ops/b1c_campaign.py'}
LOCK_EXCEPTIONS = {'source_sha256_canonical_lf', 'execution_device', 'amendment', 'recovery_manifest'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inside(root, name):
    root, name = Path(root).resolve(), Path(name)
    if name.is_absolute() or '..' in name.parts:
        raise ValueError('Recovery path must be relative')
    path = (root / name).resolve(strict=True)
    if not path.is_relative_to(root) or path.is_symlink():
        raise ValueError('Recovery path escaped source')
    return path


def spec(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': digest(path), 'bytes': path.stat().st_size}


def ordered(groups):
    datasets = ('FiQA', 'NanoNQ', 'NanoHotpotQA', 'NanoFEVER')
    methods = ('la2m20_integration_script_adaptation', 'simplelinear_official_final50_mlp5', 'embedding_converter_paper_spec')
    pairs = ('minilm_distilroberta', 'e5_small_base')
    return sorted(groups, key=lambda g: (0 if g['dataset'] == 'FiQA' else (2 if g['method'] == methods[2] else 1),
                  datasets.index(g['dataset']), pairs.index(g['pair']), g['seed'], methods.index(g['method'])))


def source_specs(value):
    """Walk registry only: never walk the lock's label specifications."""
    if isinstance(value, dict):
        if {'path', 'sha256'} <= value.keys():
            yield value
        else:
            for child in value.values():
                yield from source_specs(child)
    elif isinstance(value, list):
        for child in value:
            yield from source_specs(child)


def compare_locks(old, new):
    if {k: v for k, v in old.items() if k not in LOCK_EXCEPTIONS} != {k: v for k, v in new.items() if k not in LOCK_EXCEPTIONS}:
        raise ValueError('Recovery changed the scientific configuration')
    for name, sha in old['source_sha256_canonical_lf'].items():
        if name not in MUTABLE_CODE and new['source_sha256_canonical_lf'].get(name) != sha:
            raise ValueError('Recovery changed a frozen numerical/scoring source: ' + name)


def checked(root, name, expected):
    path = inside(root, name)
    if digest(path) != expected:
        raise ValueError('Recovery artifact hash mismatch: ' + name)
    return path


def build_manifest(source_run, source_code=None):
    """Inventory only an exact complete prefix from a FAILED_PRESERVED run."""
    run = Path(source_run).resolve(strict=True)
    code = Path(source_code or run.parents[1]).resolve(strict=True)
    meta = read(run / 'metadata.json')
    lockpath = code / 'configs/b1c_lock.json'
    lock = read(lockpath)
    if meta.get('status') != 'FAILED_PRESERVED' or meta.get('stage') != 'full' or not meta.get('failures'):
        raise ValueError('Recovery requires preserved failed full metadata')
    if meta.get('qrels_opened') is not False or meta.get('ranking_process_qrel_reads') != 0 or meta.get('TREC_access') is not False:
        raise ValueError('Recovery source crossed the label boundary')
    if digest(lockpath) != meta['lock_sha256']:
        raise ValueError('Failed-run lock changed')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=code, text=True).strip()
    if head != meta['code_commit']:
        raise ValueError('Failed deployment commit changed')
    code_files = {}
    for name, sha in lock['source_sha256_canonical_lf'].items():
        path = inside(code, name)
        if hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != sha:
            raise ValueError('Failed deployment source changed: ' + name)
        code_files[name] = spec(path)
    for key, expected in {**lock['cpu_versions'], 'sklearn': lock['cpu_sklearn_version'], 'executable': lock['cpu_python'], 'environment': lock['cpu_environment']}.items():
        if meta['runtime'].get(key) != expected:
            raise ValueError('Failed CPU runtime mismatch: ' + key)
    if lock['seeds'] != [17, 29, 41, 53, 67]:
        raise ValueError('Failed seed lock drift')
    registries = {}
    for name in ('registry', 'existing_cells'):
        path = Path(lock[name]['path'])
        path = path if path.is_absolute() else code / path
        if digest(path) != lock[name]['sha256']:
            raise ValueError('Failed source registry changed')
        registries[name] = spec(path)
    registry_path = Path(registries['registry']['path'])
    if meta['registry_sha256'] != lock['registry']['sha256'] or meta['existing_registry_sha256'] != lock['existing_cells']['sha256']:
        raise ValueError('Failed registry identity mismatch')
    registry = read(registry_path)
    groups = ordered(registry['groups'])
    cells = read(run / 'cells_pre_qrels.json')
    parity = read(run / 'parity_receipts.json')
    by_group, seen = {}, set()
    for row in cells:
        if row['case_id'] in seen:
            raise ValueError('Duplicate recovery cell')
        seen.add(row['case_id'])
        by_group.setdefault(row['group_id'], []).append(row)
    selected, fit_rows, used_parity = [], [], []
    artifacts = {}

    def add(name, sha=None):
        if 'qrel' in name.lower():
            raise ValueError('Label path in recovery artifacts')
        path = inside(run, name)
        actual = digest(path)
        if sha is not None and sha != actual:
            raise ValueError('Recorded recovery hash mismatch: ' + name)
        if name in artifacts and artifacts[name]['sha256'] != actual:
            raise ValueError('Conflicting recovery artifact')
        artifacts[name] = {'sha256': actual, 'bytes': path.stat().st_size}

    for group in groups:
        gid = group['group_id']
        rows = by_group.pop(gid, [])
        if not rows:
            break
        cases = {c['case_id']: c for c in group['cases']}
        if [r['case_id'] for r in rows] != [c['case_id'] for c in sorted(group['cases'], key=lambda c: c['budget'])]:
            raise ValueError('Partial group cannot be recovered: ' + gid)
        fits = [r['fit_receipt'] for r in rows]
        if any(f != fits[0] for f in fits) or fits[0]['group_id'] != gid:
            raise ValueError('Conflicting recovery fit receipts')
        fit = fits[0]
        if fit['path'] != 'groups/' + gid + '/fit_receipt.json':
            raise ValueError('Unexpected recovery fit location')
        receipt = read(checked(run, fit['path'], fit['sha256']))
        if any(receipt[k] != group[k] for k in IDENTITY) or receipt['group_id'] != gid or receipt['fit_pairs'] != 1024:
            raise ValueError('Recovery fit identity mismatch')
        if fit['new_fit'] != (group['dataset'] != 'FiQA') or receipt['new_fit'] != fit['new_fit']:
            raise ValueError('Recovery fit provenance mismatch')
        for row in rows:
            if any(row[k] != group[k] for k in IDENTITY) or row['budget'] != cases[row['case_id']]['budget']:
                raise ValueError('Recovery cell identity mismatch')
            for prefix, source in [('ids', group['ids']), ('anchors', group['anchors']), ('paid', cases[row['case_id']]['paid'])]:
                if row[prefix + '_sha256'] != source['sha256']:
                    raise ValueError('Recovery ordered input differs from registry')
                add(row[prefix + '_path'], source['sha256'])
            add(row['ranking_path'], row['ranking_sha256'])
        add(receipt['paired_target_path'], receipt['paired_target_sha256'])
        for path in inside(run, 'groups/' + gid).rglob('*'):
            if path.is_file():
                add(path.relative_to(run).as_posix())
        if group['dataset'] == 'FiQA':
            ps = [p for p in parity if p['group_id'] == gid]
            if len(ps) != 1 or ps[0]['status'] != 'PASS' or ps[0]['case_id'] != group['parity_case']['case_id'] or ps[0]['published_ranking'] != group['parity_case']['published_ranking']:
                raise ValueError('Missing or conflicting FiQA parity')
            add(ps[0]['ranking_path'], ps[0]['ranking_sha256'])
            paid = 'inputs/FiQA/paid_seed' + str(group['seed']) + '_50pct.npy'
            add(paid, group['parity_case']['paid']['sha256'])
            used_parity.extend(ps)
        else:
            kind = 'cpu' if group['method'].startswith('la2m') else 'neural'
            directory = kind + '/' + group['dataset'] + '_' + gid
            for path in inside(run, directory).rglob('*'):
                if path.is_file():
                    add(path.relative_to(run).as_posix())
            worker = read(inside(run, directory + ('/metadata.json' if kind == 'cpu' else '/worker/metadata.json')))
            if worker['status'] != ('CPU_FIT_PASS' if kind == 'cpu' else 'B1P_NEURAL_FULL_PASS'):
                raise ValueError('Incomplete recovery fit worker')
            if kind == 'cpu':
                add(directory + '/parameters.npz', worker['parameters_sha256'])
                if receipt.get('parameters_sha256') != worker['parameters_sha256']:
                    raise ValueError('CPU fit receipt parameter hash mismatch')
            else:
                request = read(checked(run, receipt['request_path'], receipt['request_sha256']))
                checked(run, receipt['metadata_path'], receipt['metadata_sha256'])
                if request['seed'] != group['seed'] or request['mode'] != 'full' or request['code_commit'] != meta['code_commit'] or request['lockpath'] != str(lockpath):
                    raise ValueError('Recovery worker request mismatch')
                if worker['request_sha256'] != receipt['request_sha256'] or worker.get('fit_pairs') != 1024 or worker.get('mode') != 'full' or worker.get('new_qrel_reads') != 0 or worker.get('unpaid_target_reads') != 0:
                    raise ValueError('Recovery worker completion/input boundary mismatch')
                if request['input_sha256']['full_source'] != group['old_docs']['sha256'] or request['full_source'] != group['old_docs']['path']:
                    raise ValueError('Recovery worker source-vector identity mismatch')
                if worker['code_commit'] != meta['code_commit'] or worker['lock_sha256'] != meta['lock_sha256'] or worker['seed'] != group['seed'] or worker['source_sha256_canonical_lf'] != lock['source_sha256_canonical_lf'] or worker['environment'] != lock['environment']:
                    raise ValueError('Recovery worker provenance mismatch')
                if {k: v['version'] for k, v in worker['modules'].items()} != lock['gpu_versions']:
                    raise ValueError('Recovery GPU runtime mismatch')
                if not worker.get('artifacts') or 'proxy_full.npy' not in worker['artifacts']:
                    raise ValueError('Recovery worker proxy is not sealed')
                for name, item in worker['artifacts'].items():
                    add(directory + '/worker/' + name, item['sha256'])
                    if inside(run, directory + '/worker/' + name).stat().st_size != item['bytes']:
                        raise ValueError('Recovery worker artifact byte count mismatch')
        selected.append(gid)
        fit_rows.append(fit)
    if by_group or not 0 < len(selected) < len(groups) or len(cells) != sum(len(g['cases']) for g in groups[:len(selected)]):
        raise ValueError('Recovery cells are not a complete ordered prefix')
    if parity != used_parity:
        raise ValueError('Recovery parity includes partial/duplicate/out-of-order groups')
    if [r['group_id'] for r in cells] != [g['group_id'] for g in groups[:len(selected)] for _ in g['cases']]:
        raise ValueError('Recovery cells are not in frozen execution order')
    progress = read(run / 'progress.json')
    if progress.get('group_index') != len(selected) or progress.get('group') != groups[len(selected)]['group_id'] or progress.get('rankings_complete') != len(cells):
        raise ValueError('Failed progress does not match completed prefix')
    failed = 'neural/' + groups[len(selected)]['dataset'] + '_' + groups[len(selected)]['group_id']
    failed_worker = read(inside(run, failed + '/worker/metadata.json'))
    failed_exit = read(inside(run, failed + '/process_exit.json'))
    if failed_worker.get('status') != 'FAILED_PRESERVED' or failed_exit.get('returncode') != 1 or 'out of memory' not in str(failed_worker.get('failures')).lower():
        raise ValueError('Expected preserved CUDA OOM evidence')
    if failed_worker.get('code_commit') != meta['code_commit'] or failed_worker.get('lock_sha256') != meta['lock_sha256'] or failed_worker.get('seed') != groups[len(selected)]['seed']:
        raise ValueError('Failed worker provenance mismatch')
    failure = {name: spec(run / name) for name in ('metadata.json', 'progress.json', 'cells_pre_qrels.json', 'parity_receipts.json')}
    for path in inside(run, failed).rglob('*'):
        if path.is_file():
            failure[path.relative_to(run).as_posix()] = spec(path)
    failed_group = run / 'groups' / groups[len(selected)]['group_id']
    if failed_group.exists():
        for path in failed_group.rglob('*'):
            if path.is_file():
                failure[path.relative_to(run).as_posix()] = spec(path)
    if (run / 'resource_trace.jsonl').exists():
        failure['resource_trace.jsonl'] = spec(run / 'resource_trace.jsonl')
    return {'format': 'B1C_WHOLE_GROUP_RECOVERY_V1', 'source_run': str(run), 'source_code': str(code),
            'source_commit': meta['code_commit'], 'source_lock': spec(lockpath), 'source_code_files': code_files, 'source_registries': registries,
            'failure_evidence_retained_at_source': failure, 'group_ids': selected, 'cells': cells,
            'fit_groups': fit_rows, 'fiqa_50pct_parity': used_parity, 'artifacts': dict(sorted(artifacts.items())),
            'counts': {'groups': len(selected), 'rankings': len(cells), 'nano_fits': sum(f['new_fit'] for f in fit_rows), 'fiqa_parity': len(used_parity)}}


def verify_manifest(path, lock, inputs=None):
    path = Path(path).resolve(strict=True)
    binding = lock.get('recovery_manifest')
    bound_path = Path(binding['path']) if binding else path
    bound_path = bound_path if bound_path.is_absolute() else Path(__file__).resolve().parents[1] / bound_path
    if not binding or path != bound_path.resolve() or digest(path) != binding['sha256']:
        raise ValueError('Recovery manifest is not pinned by this lock')
    manifest = read(path)
    fresh = build_manifest(manifest['source_run'], manifest['source_code'])
    if fresh != manifest:
        raise ValueError('Frozen recovery inventory changed')
    compare_locks(read(manifest['source_lock']['path']), lock)
    if inputs is not None:
        for source in source_specs(read(Path(manifest['source_code']) / read(manifest['source_lock']['path'])['registry']['path'])):
            inputs.path(source)
    return manifest


def import_groups(manifest, out):
    """Called only after whole-manifest verification; preserve every copied byte."""
    out, source = Path(out).resolve(), Path(manifest['source_run'])
    if out == source or out.is_relative_to(source):
        raise ValueError('Recovery output must be distinct from failed attempt')
    for name, item in manifest['artifacts'].items():
        original = checked(source, name, item['sha256'])
        destination = out / name
        if destination.exists():
            raise ValueError('Recovery destination artifact already exists')
        destination.parent.mkdir(parents=True, exist_ok=True)
        with original.open('rb') as src, destination.open('xb') as dst:
            shutil.copyfileobj(src, dst, 8 * 1024 * 1024)
        if digest(destination) != item['sha256']:
            raise ValueError('Recovery copy verification failed')
    return manifest['cells'].copy(), manifest['fit_groups'].copy(), manifest['fiqa_50pct_parity'].copy()


def synthetic_checks(root):
    """CPU/std-library fixture: no real inputs, fitting, ranking or labels."""
    root = Path(root).resolve()
    code, run = root / 'old_code', root / 'old_code/results/failed'
    run.mkdir(parents=True)

    def put(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
        return digest(path)

    def file(name, value):
        path = run / name
        put(path, value)
        return {'path': str(path), 'sha256': digest(path)}

    source = file('fixture_input.bin', [1, 2, 3])
    groups, cells, parities = [], [], []
    for dataset, method in [('FiQA', 'la2m20_integration_script_adaptation'), ('NanoNQ', 'la2m20_integration_script_adaptation'), ('NanoNQ', 'simplelinear_official_final50_mlp5')]:
        gid = dataset + '_' + method
        group = dict(dataset=dataset, pair='minilm_distilroberta', method=method, seed=17, regime='fixed1024', group_id=gid,
                     ids=source, anchors=source, cases=[{'case_id': gid + '_25pct', 'budget': '25pct', 'paid': source}])
        if dataset == 'FiQA':
            group['parity_case'] = {'case_id': gid + '_50pct', 'budget': '50pct', 'paid': source, 'published_ranking': source}
        groups.append(group)
        if method.startswith('simplelinear'):
            continue
        folder = 'groups/' + gid
        paired = file(folder + '/anchor.npy', [1])
        receipt = {k: group[k] for k in IDENTITY}
        receipt.update(group_id=gid, fit_pairs=1024, new_fit=dataset != 'FiQA', paired_target_path=folder + '/anchor.npy', paired_target_sha256=paired['sha256'])
        fitpath = folder + '/fit_receipt.json'
        put(run / fitpath, receipt)
        fit = {'group_id': gid, 'path': fitpath, 'sha256': digest(run / fitpath), 'new_fit': dataset != 'FiQA'}
        row = {k: group[k] for k in IDENTITY}
        row.update(group_id=gid, case_id=group['cases'][0]['case_id'], budget='25pct', fit_receipt=fit)
        for prefix in ('ids', 'anchors', 'paid'):
            name = 'inputs/' + dataset + '/' + prefix + '.bin'
            (run / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source['path'], run / name)
            row[prefix + '_path'], row[prefix + '_sha256'] = name, source['sha256']
        rank = file('rankings/' + gid + '.npy', [0, 1])
        row.update(ranking_path='rankings/' + gid + '.npy', ranking_sha256=rank['sha256'])
        cells.append(row)
        if dataset == 'FiQA':
            rank = file(folder + '/parity.npy', [0, 1])
            parities.append(dict(group_id=gid, case_id=group['parity_case']['case_id'], status='PASS', ranking_path=folder + '/parity.npy', ranking_sha256=rank['sha256'], published_ranking=source))
            shutil.copyfile(source['path'], run / 'inputs/FiQA/paid_seed17_50pct.npy')
        else:
            directory = 'cpu/' + dataset + '_' + gid
            param = file(directory + '/parameters.npz', [1])
            file(directory + '/metadata.json', {'status': 'CPU_FIT_PASS', 'parameters_sha256': param['sha256']})
            receipt['parameters_sha256'] = param['sha256']
            put(run / fitpath, receipt)
            fit['sha256'] = digest(run / fitpath)
    registry = code / 'configs/registry.json'
    put(registry, {'groups': groups})
    existing = code / 'configs/existing.json'
    put(existing, {'cells': []})
    lock = dict(seeds=[17, 29, 41, 53, 67], cpu_versions={'numpy': 'fixture', 'scipy': 'fixture'}, cpu_sklearn_version='fixture', cpu_python='fixture', cpu_environment={},
                registry={'path': 'configs/registry.json', 'sha256': digest(registry)}, existing_cells={'path': 'configs/existing.json', 'sha256': digest(existing)}, source_sha256_canonical_lf={})
    put(code / 'configs/b1c_lock.json', lock)
    subprocess.run(['git', 'init', '-q', str(code)], check=True, capture_output=True)
    subprocess.run(['git', 'add', 'configs'], cwd=code, check=True, capture_output=True)
    subprocess.run(['git', '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'synthetic'], cwd=code, check=True, capture_output=True)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=code, text=True).strip()
    put(run / 'metadata.json', dict(status='FAILED_PRESERVED', stage='full', failures=['synthetic OOM'], qrels_opened=False, ranking_process_qrel_reads=0, TREC_access=False,
        code_commit=commit, lock_sha256=digest(code / 'configs/b1c_lock.json'), registry_sha256=lock['registry']['sha256'], existing_registry_sha256=lock['existing_cells']['sha256'],
        runtime={'numpy': 'fixture', 'scipy': 'fixture', 'sklearn': 'fixture', 'executable': 'fixture', 'environment': {}}))
    put(run / 'cells_pre_qrels.json', cells)
    put(run / 'parity_receipts.json', parities)
    put(run / 'progress.json', {'group_index': 2, 'group': groups[2]['group_id'], 'rankings_complete': 2})
    failed = 'neural/NanoNQ_' + groups[2]['group_id']
    file(failed + '/worker/metadata.json', {'status': 'FAILED_PRESERVED', 'failures': ['CUDA out of memory'], 'code_commit': commit, 'lock_sha256': digest(code / 'configs/b1c_lock.json'), 'seed': 17})
    file(failed + '/process_exit.json', {'returncode': 1})
    manifest = build_manifest(run, code)
    target = root / 'imported'
    target.mkdir()
    recovered = import_groups(manifest, target)
    if recovered != (cells, manifest['fit_groups'], parities):
        raise AssertionError('Recovery changed historical records')
    for name, item in manifest['artifacts'].items():
        if digest(target / name) != item['sha256']:
            raise AssertionError('Recovery did not preserve bytes')
    rejected = []
    identity_drift = json.loads(json.dumps(cells))
    identity_drift[0]['seed'] = 29
    for name, change in [('duplicate', cells + cells[:1]), ('partial', cells[1:]), ('identity_drift', identity_drift), ('order_drift', cells[::-1])]:
        put(run / 'cells_pre_qrels.json', change)
        try:
            build_manifest(run, code)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError('Recovery accepted ' + name)
        put(run / 'cells_pre_qrels.json', cells)
    ranking = run / cells[0]['ranking_path']
    original = ranking.read_bytes()
    ranking.write_bytes(original + b'changed')
    try:
        build_manifest(run, code)
    except ValueError:
        rejected.append('mutation')
    else:
        raise AssertionError('Recovery accepted mutation')
    ranking.write_bytes(original)
    return {'status': 'PASS', 'imported_groups': 2, 'imported_rankings': 2, 'byte_identity': True, 'rejected': rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True, help='Frozen failed run')
    parser.add_argument('--source-code', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = build_manifest(args.build, args.source_code)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(manifest, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'manifest': spec(args.output), 'counts': manifest['counts']}))


if __name__ == '__main__':
    main()
