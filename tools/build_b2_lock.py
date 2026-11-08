"""Build the B2 pre-run lock without data/label access or scientific execution."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    prior = json.loads((ROOT / 'configs/b1c_r3_lock.json').read_text(encoding='utf-8'))
    keys = ('seeds', 'cpu_versions', 'cpu_python', 'gpu_python', 'cpu_environment',
            'cpu_sklearn_version', 'gpu_versions', 'upstream', 'upstream_raw_sha256',
            'simplelinear_defaults', 'dependency_fallbacks', 'environment',
            'converter_config', 'smoke_converter_iterations', 'neighbor_block_rows',
            'execution_device')
    lock = {k: prior[k] for k in keys}
    acquisition = json.loads((ROOT / 'configs/b2_acquisition.json').read_text(encoding='utf-8'))
    q = acquisition['qrels_opaque_metadata_only']
    lock.update(stage='B2', method_revision='arc2_global_tangent2_r1', anchor_count=1024,
                budgets=[25, 50, 75], expected_rankings=184,
                encoder_python='/home/jovyan/arc2_b2_20261031/envs/encode/bin/python',
                acquisition=acquisition, encode_versions=acquisition['encode_versions'],
                dataset='TREC-COVID', TREC_access='qrel-free until all184 sealed and separately verified',
                ANN_claim=False, manuscript_updates_authorized=False,
                scoring={'bootstrap_draws': 20000, 'bootstrap_seed': 20261031,
                         'contrasts': 30, 'alpha': 0.05,
                         'qrels': {'format': 'tsv', 'url': f"https://huggingface.co/datasets/{q['repo']}/resolve/{q['revision']}/{q['path']}",
                                   'revision': q['revision'], 'bytes': q['bytes'],
                                   'git_blob_sha1': q['git_blob_sha1']}},
                STOP='After verified B2 results/figures/ARIS; no manuscript update or systems')
    extra = ['ops/b2_inputs.py', 'ops/b2_stage.py', 'ops/b2_verify.py', 'ops/b2_score.py',
             'ops/b2_campaign.py', 'configs/b2_acquisition.json',
             'protocols/B2_TREC_COVID_CONFIRMATION_20261031.md']
    sources = set(prior['source_sha256_canonical_lf']) | set(extra)
    lock['source_sha256_canonical_lf'] = {
        name: hashlib.sha256((ROOT / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        for name in sorted(sources)}
    (ROOT / 'configs/b2_lock.json').write_text(json.dumps(lock, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('B2 lock written;', len(sources), 'canonical source pins; no data or qrel access')


if __name__ == '__main__':
    main()
