"""Verify the positive presentation against saved raw summaries; no scoring."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args(); root = args.root.resolve()
    read = lambda rel: json.loads((root / rel).read_text(encoding='utf-8'))
    claims = read('PRESENTATION_CLAIMS.json')
    summaries = {}
    for rel, h in claims['source_summary_sha256'].items():
        assert hashlib.sha256((root / rel).read_bytes()).hexdigest() == h
        summaries[rel] = read(rel)
    for highlight in claims['highlights']:
        s = summaries[highlight['source']]
        rows = s.get('overall_macro', []) + s.get('aggregate_contrasts', []) + s.get('contrasts', [])
        assert highlight['raw_record'] in rows
        row = highlight['raw_record']['ndcg10']
        ci = next(v for k, v in row.items() if 'bonferroni' in k)
        assert ci == highlight['saved_family_interval'] and ci[0] > 0
        assert row['delta'] == highlight['delta_ndcg10']
        text = (root / 'CLAIM_LOCK.md').read_text(encoding='utf-8')
        assert f"{row['delta']:+.6f}" in text
    test = next(s for s in summaries.values() if s.get('stage') == 'B2')
    assert len(test['contrasts']) == 30
    assert sum(c['ndcg10']['family_interval_interpretation'] == 'above_zero' for c in test['contrasts']) == 11
    e5 = [c for c in test['contrasts'] if c['pair'] == 'e5_small_base' and
          c['right'] in ['embedding_converter_paper_spec', 'ridge_affine_l10_bias_regularized']]
    assert len(e5) == 6 and all(c['ndcg10']['family_interval_interpretation'] == 'above_zero' for c in e5)
    paid = next(s for s in summaries.values() if s.get('ranking_cells') == 124)
    rows = [c for c in paid['contrasts'] if c['kind'] == 'arc2_allpaid_vs_baseline_allpaid' and c['pair'] == 'minilm_distilroberta']
    assert len(rows) == 5 and sum(c['ndcg10']['family_interval_interpretation'] == 'above_zero' for c in rows) == 4
    assert next(c for c in rows if c['right']['method'] == 'ridge_affine_l10_bias_regularized')['ndcg10']['family_interval_interpretation'] == 'unresolved'
    parsed = ast.parse((root / 'src/arc2_global/embedding_converter.py').read_text())
    config = next(n for n in parsed.body if isinstance(n, ast.ClassDef) and n.name == 'ConverterConfig')
    multiplier = next(n.value.value for n in config.body if isinstance(n, ast.AnnAssign) and n.target.id == 'hidden_multiplier')
    storage = claims['storage']; source, target = storage['dimensions']; hidden = target * multiplier
    linear = (source + 1) * target
    mlp = sum((a + 1) * b for a, b in zip((source, hidden, hidden, hidden), (hidden, hidden, hidden, target)))
    assert linear == storage['ARC2_final_affine_parameters'] == 295680
    assert mlp == storage['declared_converter_MLP_parameters'] == 33927168
    assert math.isclose(mlp / linear, storage['parameter_byte_ratio_converter_to_ARC2'], rel_tol=0, abs_tol=1e-12)
    lock = read('CLAIM_LOCK.json')
    assert lock['independent_family']['positive'] == 11 and lock['independent_family']['unresolved'] == 19
    assert lock['independent_family']['nDCG_Procrustes_point_differences_all_negative'] is True
    out = root / 'checks' / ('presentation_claims_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    out.parent.mkdir(exist_ok=True)
    receipt = {'status': 'PASS', 'revision': claims['revision'], 'saved_highlights_verified': len(claims['highlights']),
               'all_primary_test_outcomes_retained': True, 'parameter_storage_ratio': mlp / linear,
               'source_summary_sha256': claims['source_summary_sha256'],
               'scope': 'Deterministic check of positive presentation numbers and conditions; not an external semantic review.',
               'new_scientific_experiment': False, 'verified_utc': datetime.now(timezone.utc).isoformat()}
    with out.open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, indent=2); stream.write('\n')
    print(json.dumps({'status': 'PASS', 'output': str(out), 'parameter_storage_ratio': mlp / linear}))


if __name__ == '__main__':
    main()
