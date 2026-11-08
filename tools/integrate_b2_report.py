"""Integrate completed B2 evidence and its ARIS review into current project notes.

Requires completed computational and semantic receipts; never writes manuscript.
Historical protocols, results and prior claim assessment remain unchanged.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'results/b2_review_20261101'
TRACE = ROOT / '.aris/traces/result-to-claim/2026-11-01_b2'
BEGIN, END = '<!-- B2_CURRENT_BEGIN -->', '<!-- B2_CURRENT_END -->'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, text):
    path.write_text(text, encoding='utf-8', newline='\n')


def prepend_block(path, content):
    text = path.read_text(encoding='utf-8')
    if BEGIN in text:
        start, end = text.index(BEGIN), text.index(END) + len(END)
        text = text[:start] + text[end:].lstrip('\n')
    first = text.index('\n')
    write(path, text[:first] + '\n\n' + BEGIN + '\n' + content.strip() + '\n' + END + '\n\n' + text[first:].lstrip('\n'))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qa', type=Path, required=True)
    args = ap.parse_args()
    qa = read(args.qa)
    scoring = REVIEW / 'evidence/results/b2_full_r1_20261031t064859/scoring'
    summary = read(scoring / 'summary.json')
    if qa['status'] != 'PASS' or qa['summary_sha256'] != hashlib.sha256((scoring / 'summary.json').read_bytes()).hexdigest():
        raise ValueError('QA does not bind completed summary')
    verdict = read(TRACE / 'verdict.json')
    if verdict.get('claim_supported') not in ('yes', 'partial', 'no'):
        raise ValueError('Completed semantic claim review required')
    if verdict.get('review_independence') != 'same-family' or verdict.get('acceptance_status') != 'provisional':
        raise ValueError('Review assurance route changed')
    outcomes = Counter(c['ndcg10']['family_interval_interpretation'] for c in summary['contrasts'])
    assert outcomes == {'above_zero': 11, 'unresolved': 19}
    table = ['| ARC2 minus declared baseline configuration | Positive family intervals | Unresolved | Negative family intervals |',
             '|---|---:|---:|---:|']
    labels = {'procrustes_global': 'A2M / Procrustes adaptation',
              'la2m20_integration_script_adaptation': 'LA2M20 adaptation',
              'simplelinear_official_final50_mlp5': 'SimpleLinear official code, locked policy',
              'ridge_affine_l10_bias_regularized': 'Affine ridge, lambda10',
              'embedding_converter_paper_spec': 'Embedding-Converter paper-spec adaptation'}
    for method, label in labels.items():
        counts = Counter(c['ndcg10']['family_interval_interpretation'] for c in summary['contrasts'] if c['right'] == method)
        table.append(f"| {label} | {counts['above_zero']}/6 | {counts['unresolved']}/6 | {counts['below_zero']}/6 |")
    counts_table = '\n'.join(table)
    core = f'''Updated 1 November 2026. **B2 independent TREC-COVID confirmation is complete:** 171,332 documents, 50 queries, two frozen encoder pairs, five seeds, 25/50/75% budgets; all 184 rankings and 60 fit groups. Rankings sealed at 02:56:09+07, separate exact endpoint replay finished 03:11:42, first final-label receipt 03:12:17, scoring completed 03:12:54. No scientific failures or postlabel changes.

The locked 30-comparison nDCG@10 family has **11 positive intervals, 19 unresolved, 0 negative intervals**. This is a condition-specific independent result. It does not establish equivalence or noninferiority in the unresolved comparisons.

{counts_table}

All six nDCG point differences against Procrustes are negative (-0.016322 to -0.000024), with family intervals crossing zero. All six LA2M comparisons are also unresolved. Independent broad superiority over these baselines is unconfirmed. Recall is descriptive: against Procrustes, ARC2 gains for MiniLM and loses for E5; these intervals were not corrected as the primary family.

MiniLM ARC2 nDCG at 25/50/75% is 0.461913/0.499955/0.519513, versus native Full-X 0.493478 and Full-Y 0.520273. E5 ARC2 is 0.562802/0.590406/0.609782 versus Full-X 0.680542 and Full-Y 0.642113. Retaining an incumbent can therefore be the appropriate quality choice. Full-Y is a native reference, not an upper bound.

[All B2 results, tables and figures](results/b2_review_20261101/SUMMARY.md) | [Raw independent summary](results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json) | [Current ARIS claim review](CLAIMS_FROM_RESULTS.md).

Independent local QA recomputed all 184 rankings/18,400 metric values (maximum difference {qa['largest_metric_absolute_discrepancy']:.3g}) and 2.8 million saved bootstrap values. This validates the saved evidence, not fresh local regeneration of large vector endpoints. The remote separate verifier replayed every ordered top100 endpoint before labels. Full backup: 1,330 files/58,977,150,839 verified bytes on D, zero pending. All 20 manuscript file hashes remain unchanged.

The current result is a compact, neural-training-free forward adapter with clear fixed-anchor DEV benefits and a narrower independent advantage over specified baseline configurations. It has no measured isolated cost, serving SLO, ANN or real-traffic benefit. B2 encoded all four full-corpus model caches for representation evaluation; it did not measure actual partial-migration deployment savings.

**STOP:** B2 results/QA/figures/ARIS are complete. Manuscript editing, new datasets, retuning and B3/B4 were not performed. The remaining paper work is to integrate this bounded evidence and audit the resulting manuscript when authorized; no additional benchmark is automatically required.
'''
    report = ROOT / 'REPORT.md'
    t = report.read_text(encoding='utf-8')
    old = 'The full six-method DEV comparison is finished. Final D1 and its scope are recorded in [CLAIMS_FROM_RESULTS.md](CLAIMS_FROM_RESULTS.md). **STOP before B2/TREC-COVID or systems execution** until the user reviews the completed result. TREC labels remain closed. If released, the existing plan calls for one prospective184-cell/30-contrast confirmation, then the mapper paper and claim audit. B3/B4 remain conditional rather than automatic requirements.'
    t = t.replace(old, 'The full six-method DEV comparison is finished. Its historical D1 led to the now-completed B2 above. The current STOP is after B2 review; B3/B4 remain conditional and were not run.')
    t = t.replace('These measurements performed zero new physical document encodings.', 'Those cached DEV measurements performed zero new physical document encodings.')
    write(report, t)
    prepend_block(report, core + '\nThe following sections retain the completed inspected DEV evidence and its limitations.\n')

    short = '''1 November 2026: **B2 COMPLETE and locally verified**, 184/184 rankings, 60/60 fits, separate endpoint verification before one-shot scoring. Primary nDCG family:11 positive,19 unresolved, 0 negative intervals. Independent advantage is confirmed for specific Converter/ridge/SimpleLinear configurations; Procrustes and LA2M advantages remain unconfirmed. All negatives are retained. Backup complete 58.98 GB / 1,330 files.\n\n[Current report](REPORT.md) | [Independent B2 tables and figures](results/b2_review_20261101/SUMMARY.md) | [Claim assessment](CLAIMS_FROM_RESULTS.md) | [Tracker](refine-logs/EXPERIMENT_TRACKER.md).\n\nSTOP after results/QA/figures/ARIS. Manuscript remains unchanged; no B3/B4, new datasets or retuning. Earlier execution notes below are historical and do not describe the current job status.'''
    p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8')
    if '**B2 RUNNING' in t:
        start, end = t.index('**B2 RUNNING'), t.index('[Recovery protocol]')
        t = t[:start] + t[end:]
    t = t.replace('New DEV mechanism results and CIs are available; independent confirmation is pending.', 'DEV mechanism results remain available; independent B2 results and their narrower scope are linked above.')
    write(p, t); prepend_block(p, short)

    state = f'''1 November 2026: **B2 COMPLETE**, all 184rankings/60fits, endpoint replay before labels, FINAL_SCORED03:12:54+07. Local QA PASS ({args.qa.relative_to(ROOT) if args.qa.is_absolute() else args.qa}); all 1,138 compact files/181,895,786bytes verified. Primary family: 11 positive / 19 unresolved / 0 negative; all 6 Procrustes point differences negative, all Procrustes/LA2M family intervals unresolved. ARIS claim_supported={verdict['claim_supported']}, same-family/provisional. Complete report/figures at results/b2_review_20261101; root REPORT/CLAIMS current. Backup: 1,330 files / 58,977,150,839 bytes complete 03:16:10+07, zero pending; no owned remote B2 job remains. Manuscript: 20 files unchanged. STOP before manuscript changes, B3/B4, retuning or new datasets. Earlier execution entries below are historical.'''
    for name in ['refine-logs/EXPERIMENT_PLAN.md', 'refine-logs/EXPERIMENT_TRACKER.md', 'AGENTS.md']:
        prepend_block(ROOT / name, state)
    prepend_block(ROOT / 'findings.md', '''1 November 2026. B2 prospective TREC-COVID confirmation is complete and locally verified: 184 rankings / 60 fits, all source and chronology bindings PASS; 18,400 metric values and 2.8 million bootstrap values independently reproduced. Primary family: 11 positive / 19 unresolved / 0 negative intervals. Independent confirmed improvements: Converter 5/6, ridge 4/6, SimpleLinear 2/6; Procrustes and LA2M 0/6 each. All six Procrustes nDCG point differences are negative; unresolved is not equivalence. MiniLM Recall improves relative to Procrustes; E5 Recall falls (descriptive intervals). All native references and negatives remain reported.

The DEV aggregate benefit remains supported, while transfer is baseline/encoder/budget dependent. No physical cost/SLO/traffic conclusion follows from this representation experiment. B1-P all-paid losses and B1-G mixed-gallery reversal remain material. ARIS final review is same-family/provisional; full verdict and exact effects are in [CLAIMS_FROM_RESULTS.md](CLAIMS_FROM_RESULTS.md) and [REPORT.md](REPORT.md).

Full B2 backup: 1,330 files / 58,977,150,839 bytes complete 03:16:10+07. Compact evidence: 1,138 files / 181,895,786 bytes verified. All 20 manuscript file hashes unchanged. Current finite phase ends after results/QA/figures/ARIS; STOP before manuscript edits, B3/B4, new datasets or retuning. Earlier DEV checkpoints below are historical.''')
    claim = f'''# Current ARC2-Global claim assessment

1 November 2026. B1-M/P0/P/G/B1c development studies and independent B2 are complete. Overall `claim_supported: {verdict['claim_supported']}`; `review_independence: same-family`; `acceptance_status: provisional`. Computational QA is separate from semantic assurance; no formal paper integrity audit was run.

{counts_table}

On the prospective TREC-COVID test, the family-adjusted nDCG evidence supports 11 specific improvements. The 19 unresolved comparisons establish neither equivalence nor noninferiority. All six Procrustes point differences are negative; none has a negative family interval. The original DEV macro gains over all five baselines remain valid inspected DEV evidence, but broad Procrustes/LA2M advantage did not receive independent confirmation.

ARC2-Global is a compact closed-form forward adapter requiring no neural training. Under the declared 1,024-anchor protocol it improves aggregate DEV nDCG and shows independent advantages over specified Converter, affine-ridge and SimpleLinear configurations. Which alternative to use remains encoder-, budget- and metric-dependent. The two-step mechanism attribution remains DEV; B2 tested frozen external comparisons rather than one-step ablation.

Do not claim best use of every paid pair, guaranteed superiority over native incumbents, general equivalence, isolated efficiency/dollar savings, serving SLO, ANN or real traffic. Prior all-paid E5 losses and the mixed-gallery reversal remain material; partial backfill document counts are logical exposure, not measured deployment cost.

[Full fresh reviewer response](.aris/traces/result-to-claim/2026-11-01_b2/001-claim-review.response.md) | [Structured verdict](.aris/traces/result-to-claim/2026-11-01_b2/verdict.json) | [All numerical results](REPORT.md) | [All independent comparisons](results/b2_review_20261101/SUMMARY.md) | [Prior DEV assessment, preserved](.aris/traces/result-to-claim/2026-11-01_b2/prior_claim_assessment_20261031.md).

**Finite route:** complete the current result package and STOP. The next paper work is evidence integration and manuscript claim audit when authorized. Manuscript is unchanged; no automatic new experiments or model selection.
'''
    write(ROOT / 'CLAIMS_FROM_RESULTS.md', claim)
    print('Integrated completed B2 notes; manuscript untouched.')


if __name__ == '__main__':
    main()
