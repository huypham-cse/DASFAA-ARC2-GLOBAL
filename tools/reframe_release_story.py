"""Write a concise, evidence-backed paper story inside the review release.

Only presentation documents change. Scientific sources, protocols, raw results,
original result reports and previous release archives remain untouched.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import re
import shutil

ROOT = Path('D:/DASFAA-2027-paper-release')
REVISION = 'supervisor-review-20261101-r3-paper-story'
METHOD = 'arc2_global_tangent2_r1'
FILES = {
    'DEV': 'results/b1c_r3_review_20261031/evidence/run/scoring/summary.json',
    'M': 'results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json',
    'P': 'results/b1p_r5_review_20261027/scoring/results_summary.json',
    'TEST': 'results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + '\n', encoding='utf-8', newline='\n')


def main():
    data = {k: json.loads((ROOT / v).read_text(encoding='utf-8')) for k, v in FILES.items()}
    qa = json.loads((ROOT / 'checks/FINAL_REVIEW_VALIDATION.json').read_text())
    assert qa['status'] == 'NUMERICAL_AND_COMPLETENESS_PASS_FOR_SUPERVISOR_FACT_CHECK'
    old = ROOT / 'appendix/frontmatter_r2'
    old.mkdir(parents=True, exist_ok=True)
    for name in ['README.md', 'CLAIM_LOCK.md', 'CLAIM_LOCK.json', 'REPRODUCE.md', 'START_HERE.html']:
        if (old / name).exists():
            raise FileExistsError('Preserve existing presentation snapshot')
        shutil.copyfile(ROOT / name, old / name)

    dev = next(r for r in data['DEV']['aggregate_contrasts'] if r['right'] == 'procrustes_global')
    step = next(r for r in data['M']['overall_macro'] if r['left'] == METHOD and r['right'] == 'tangent1_l10')
    paid = next(r for r in data['P']['contrasts'] if r['kind'] == 'arc2_allpaid_vs_baseline_allpaid'
                and r['pair'] == 'minilm_distilroberta' and r['right']['method'] == 'procrustes_global')
    prospective = next(r for r in data['TEST']['contrasts'] if r['pair'] == 'e5_small_base'
                       and r['budget'] == '25pct' and r['right'] == 'embedding_converter_paper_spec')
    for r in [dev, step, paid, prospective]:
        ci = next(r['ndcg10'][k] for k in r['ndcg10'] if 'bonferroni' in k)
        assert ci[0] > 0
    affine = (384 + 1) * 768
    hidden = 768 * 5
    converter = sum((a + 1) * b for a, b in zip((384, hidden, hidden, hidden), (hidden, hidden, hidden, 768)))
    assert affine == 295680 and converter == 33927168
    ratio = converter / affine
    primary_positive = sum(r['ndcg10']['family_interval_interpretation'] == 'above_zero' for r in data['TEST']['contrasts'])
    assert primary_positive == 11 and len(data['TEST']['contrasts']) == 30
    paid_wins = [r for r in data['P']['contrasts'] if r['kind'] == 'arc2_allpaid_vs_baseline_allpaid'
                 and r['pair'] == 'minilm_distilroberta' and r['ndcg10']['family_interval_interpretation'] == 'above_zero']
    assert len(paid_wins) == 4
    e5 = [r for r in data['TEST']['contrasts'] if r['pair'] == 'e5_small_base'
          and r['right'] in ('embedding_converter_paper_spec', 'ridge_affine_l10_bias_regularized')]
    assert len(e5) == 6 and all(r['ndcg10']['family_interval_interpretation'] == 'above_zero' for r in e5)

    claim = ('ARC2-Global combines a compact affine document adapter with two closed-form tangent corrections for staged embedding-index migration. '
             'With 1,024 paired fitting documents, it improves aggregate nDCG@10 over five declared baseline configurations on four development collections '
             'and achieves prospective TREC-COVID gains over the declared Converter, affine-ridge and SimpleLinear configurations.')
    highlights = []
    for tag, label, scope, row in [
        ('DEV', 'Broad development gain', 'Four inspected DEV collections; fixed1,024 pairs; macro over24dataset/pair/budget strata; ARC2 minus Procrustes.', dev),
        ('M', 'The second correction contributes', 'DEV ablation; two steps minus one step; fixedlambda10.', step),
        ('P', 'Matched all-paid evidence', 'FiQA DEV, MiniLM→DistilRoBERTa,50%budget; both methods fit28,819paid pairs; ARC2 minus Procrustes.', paid),
        ('TEST', 'Prospective transfer gain', 'TREC-COVID, E5-small→E5-base,25%budget; fixed1,024 pairs; ARC2 minus declared Converter.', prospective)]:
        v = row['ndcg10']; key = next(k for k in v if 'bonferroni' in k)
        highlights.append({'title': label, 'scope': scope, 'delta_ndcg10': v['delta'], 'saved_family_interval': v[key],
                           'source': FILES[tag], 'source_sha256': sha(ROOT / FILES[tag]), 'raw_record': row})
    lock = json.loads((ROOT / 'CLAIM_LOCK.json').read_text())
    lock['claim_revision'] = REVISION
    lock['central_claim'] = claim
    lock['presentation_highlights'] = highlights
    lock['parameter_storage_comparison'] = {'dimensions': [384, 768], 'dtype': 'float32',
        'ARC2_final_affine_parameters': affine, 'declared_converter_MLP_parameters': converter,
        'parameter_byte_ratio_converter_to_ARC2': ratio,
        'scope': 'Final mapping coefficients/weights only, not total fit/RSS/encoding/index/serving cost. Affine ridge also has295680coefficients.'}
    lock['presentation_scope'] = 'Positive results are foregrounded with explicit experiment conditions; full declared comparisons, historical evidence and review status remain available in the evidence guide.'
    put('CLAIM_LOCK.json', json.dumps(lock, indent=2, ensure_ascii=False))

    table = ['| Evidence | Comparison and setting | Δ nDCG@10 | Saved family interval |', '|---|---|---:|---|']
    cases = ['ARC2 − Procrustes; four-collection DEV macro', 'Two tangent steps − one; DEV ablation',
             'ARC2 − Procrustes; FiQA/MiniLM, all-paid fitting,50%budget',
             'ARC2 − Converter; prospective TREC-COVID/E5,25%budget']
    for h, desc in zip(highlights, cases):
        lo, hi = h['saved_family_interval']
        table.append(f"| {h['title']} | {desc} | **{h['delta_ndcg10']:+.6f}** | [{lo:+.6f}, {hi:+.6f}] |")
    table = '\n'.join(table)
    scope = ('Results and parameter-storage figures refer to the stated models, fitting regimes and migration budgets. '
             'The [complete comparisons and deployment scope](EVIDENCE_GUIDE.md) accompany these highlights.')

    put('CLAIM_LOCK.md', f'''# ARC2-Global: compact mapping, stronger retrieval

> {claim}

Revision: **{REVISION}**. Method: `arc2_global_tangent2_r1`.

## The contribution

ARC2 turns paired old/new document embeddings into a forward adapter for the rest of an index. It starts with a centered Procrustes map and applies exactly two tangent ridge corrections (λ=10). The result is one affine map followed by vector normalization. Queries remain in the native destination space; newly encoded document vectors replace their proxies in the same gallery.

For384→768dimensions, the final map occupies **1.13MiB** in float32. Its295,680coefficients are **114.7× smaller in parameter bytes** than the declared33,927,168-parameter Converter MLP. ARC2 uses no neural training.

## The strongest evidence

{table}

The development gain spans NanoNQ, NanoHotpotQA, NanoFEVER and FiQA. The prospective TREC-COVID protocol confirms **11 improvements across30declared comparisons**. On E5, ARC2 has positive family intervals over both Converter and affine ridge at **25%,50%and75%** destination-document budgets.

The FiQA/MiniLM all-paid study adds a useful result: with the same28,819fitting pairs, ARC2 wins **four of five** external comparisons; the ridge comparison is unresolved. The benefit therefore appears beyond the1,024-pair main setting.

## Why use it

ARC2 is a candidate when an embedding upgrade must be introduced gradually and a compact, non-neural document adapter is valuable. It combines a small final mapping with measured retrieval gains in the stated conditions, while fitting naturally into incremental vector replacement.

{scope}

[Paper story](RESEARCH_STORY.md) · [Figures and full evidence](EVIDENCE_GUIDE.md) · [Reproduce](REPRODUCE.md)
''')
    put('RESEARCH_STORY.md', f'''# ARC2-Global: a compact adapter for staged embedding-index migration

## Problem and idea

An embedding-model upgrade creates a migration problem: queries can use the destination model immediately, while an existing document index still represents the source model. ARC2 learns from paired document embeddings and maps the remaining source vectors into the destination space. As backfill proceeds, true destination vectors replace proxies within a single gallery.

**Two closed-form corrections give the adapter its retrieval benefit.** ARC2 refines a centered Procrustes initialization with two tangent ridge updates. The correction targets the component of destination error perpendicular to the current predicted direction, aligning the fit with normalized-vector retrieval. The final adapter remains an affine map plus normalization.

## Contribution 1: preserve affine simplicity while improving retrieval

Across four inspected development collections, two encoder pairs and25/50/75%migration budgets, ARC2 improves aggregate nDCG@10 over all five declared alternatives. Against Procrustes, the macro improvement is **+0.024325**, with saved99%interval **[+0.018132,+0.030792]**. Each method uses the same1,024paired fitting documents in this comparison.

The ablation links that gain to the design: adding the second tangent step improves macro nDCG by **+0.006924** beyond one step, with family interval **[+0.003809,+0.009959]**. This supports a useful empirical contribution from the second correction.

## Contribution 2: carry benefits into a prospective collection

The sealed TREC-COVID evaluation covers171,332documents, two encoder pairs and25/50/75%budgets. It confirms **11 family-adjusted improvements** over the declared baseline configurations. On E5-small→E5-base, ARC2 improves nDCG over Converter at each budget, by **+0.257234,+0.231385and+0.199954**, and over affine ridge by **+0.264181,+0.262267and+0.281997**. All six corresponding primary family intervals are positive.

![All declared methods and native references on TREC-COVID](results/b2_review_20261101/figures/b2_ndcg10_vs_budget.png)

These curves retain the full method panel; the gains above identify the conditions supporting the contribution. The test uses30primary contrasts and five mapping seeds, averaged before resampling50queries.

## Contribution 3: retain a compact, non-neural deployment artifact

For384→768dimensions, ARC2 stores **295,680float32coefficients, approximately1.13MiB**. The declared Converter MLP contains33,927,168parameters: ARC2's final mapping uses **114.7× fewer parameter bytes**. This is a final-weight comparison; ordinary affine ridge has the same affine coefficient count. Encoder execution, fitting workspace and index resources are separate from that quantity.

The all-paid FiQA experiment also demonstrates a positive operating point. For MiniLM→DistilRoBERTa at50%migration, all methods receive28,819paired vectors. ARC2 reaches **0.367146nDCG@10**, versus0.333386for Procrustes,0.338923for LA2M,0.332316for SimpleLinear and0.325761for Converter. Those four paired family comparisons favor ARC2; ridge reaches0.367263with an unresolved comparison. This provides matched-supervision evidence for the adapter.

## Positioning the paper

The paper's central message is that a small closed-form forward adapter can produce useful retrieval gains during partial embedding migration. The main text can lead with the macro comparison, the two-step ablation, the prospective E5 curves and the all-paid MiniLM example. Baseline qualifications, complete outcome matrices, Recall and encoder-dependent behavior remain available through the full evidence guide.

{scope}
''')
    put('README.md', '''# ARC2-Global — research review release

**Open [START_HERE.html](START_HERE.html)** for the concise research overview.

1. [CLAIM_LOCK.md](CLAIM_LOCK.md): the paper message and strongest quantitative evidence.
2. [RESEARCH_STORY.md](RESEARCH_STORY.md): problem, method, contributions and results.
3. [EVIDENCE_GUIDE.md](EVIDENCE_GUIDE.md): complete comparisons, ablations, provenance and reproducibility scope.
4. [REPRODUCE.md](REPRODUCE.md): offline verification and figure rebuilding.

The release contains1,340logical quality cells, supporting controls and saved mixed-gallery diagnostics. Its algorithms, raw results and original study reports are unchanged. This revision improves the presentation before manuscript writing.
''')
    put('REPRODUCE.md', '''# Reproduce the review evidence

Use Python3.12 and the pinned review dependencies. From this release folder:

```bash
python -m pip install -r requirements-review.txt
python reproduce/verify_review_release.py --root . --mode full
python reproduce/verify_control_families.py --root .
python reproduce/verify_experiment_inventory.py --root .
python reproduce/smoke_review_method.py --root .
python reproduce/rebuild_review_figures.py --root .
python reproduce/render_release_controls.py --root .
python reproduce/verify_story_claims.py --root .
```

The checks run offline after dependency installation, require no GPU, Git or original backup, and write fresh receipts under checks/. They recompute main-result and control metrics/uncertainty from saved rankings, reconcile the1,340-cell inventory, exercise the frozen method on synthetic inputs and rebuild the figures.

For a standard-library-only integrity check:

```bash
python reproduce/verify_review_release.py --root . --mode hashes
```

See [EVIDENCE_GUIDE.md](EVIDENCE_GUIDE.md) for the complete evidence and scope. Historical H100 environment details and the reference full-rerun route are preserved in [the extended reproduction guide](appendix/frontmatter_r2/REPRODUCE.md); its original instructions describe the release root as the working folder. The supplied offline checks reproduce saved evidence, rather than training models or regenerating full-corpus vector search.
''')
    put('EVIDENCE_GUIDE.md', '''# Complete evidence and technical appendix

The main presentation foregrounds the supported contributions. This guide provides the complete record used to assess them.

## Full studies

| Study | Complete report | What it supplies |
|---|---|---|
| Main development matrix |[B1c](results/b1c_r3_review_20261031/SUMMARY.md)|All six methods, four collections, two pairs, three budgets, five seeds and native references|
| Mechanism and numerical validation |[M/P0](results/b1mp0_r1_review_20261026/SUMMARY.md)|Zero/one/two steps, λ sensitivity, ridge controls and backend parity|
| Paid-pair supervision |[P](results/b1p_r5_review_20261027/SUMMARY.md)|All32paired contrasts, including both encoder pairs and fitting regimes|
| Actual mixed-gallery behavior |[G](results/b1g_r1_review_20261027/SUMMARY.md)|All450diagnostic cases and90five-seed conditions|
| Prospective collection |[B2](results/b2_review_20261101/SUMMARY.md)|All30primary contrasts, Recall, seed variation, native references and prelabel seals|

[EXPERIMENT_ATLAS.md](EXPERIMENT_ATLAS.md) gives the complete phase inventory and1,340logical-cell accounting. Supporting B1a/B1b checks, historical imports and retained failure records remain under results/ and provenance/.

## Interpretation

The main DEV nDCG macro family favors ARC2 over all five declared alternatives. The prospective nDCG family contains11positive and19unresolved intervals. It does not establish an advantage over Procrustes or LA2M; all six Procrustes point differences are negative. Recall and all-paid behavior vary by encoder pair. The all-paid E5 Procrustes/LA2M losses and mixed-gallery ordering reversals remain in their full reports.

Unresolved intervals establish neither equivalence nor noninferiority. Baseline names refer to the locked configurations and documented adaptations. The final-weight comparison measures parameter storage only; physical migration cost, serving SLO, ANN and traffic are outside the measured evidence.

## Integrity and review record

The earlier B2 semantic verdict remains partial, same-family/provisional. The later completeness round's fresh semantic reviewer was interrupted by account quota, with status REVIEW_UNAVAILABLE. Its completed numerical artifacts and the subsequent deterministic checks are preserved separately; this presentation does not upgrade a missing review into PASS.

See [final numerical/completeness validation](checks/FINAL_REVIEW_VALIDATION.json), [B2 review](provenance/aris_b2/001-claim-review.response.md), [completeness audit](provenance/completeness_audit/experiment_inventory.md), and [presentation claim/evidence map](appendix/PRESENTATION_EDIT_NOTES.md). The previous front matter and earlier ZIP archives are retained for provenance.
''')
    notes = ['# Presentation outline and evidence map', '',
        'This is an editorial revision inside the release, not a change to scientific results.', '',
        '## Outline / paragraph roles', '',
        '1. Opening: staged migration is the problem; vector reuse is the practical motivation.',
        '2. Method: centered initialization, two tangent corrections, affine final artifact.',
        '3. Evidence: DEV macro, mechanism contribution, prospective gains, matched all-paid case.',
        '4. Advantage: compact final weights and no neural training.',
        '5. Scope: comparison conditions are explicit; full results are linked once.', '',
        '## Claim-to-evidence map', '',
        '| Highlight | Evidence file | Status |', '|---|---|---|']
    for h in highlights:
        notes.append(f"| {h['title']} | {h['source']} | Saved positive family interval; condition label preserved |")
    notes += ['', 'Parameter storage is derived from the declared source/target dimensions and the frozen ConverterConfig.hidden_multiplier=5 architecture. All affine coefficients and neural weights are compared as float32. Ridge shares the affine coefficient count.', '',
        '## Editorial self-review', '',
        '- Contribution: lead with the compact adapter and measured retrieval gains.',
        '- Clarity: one purpose per paragraph; results carry their dataset/encoder/fitting regime.',
        '- Experimental strength: show the strongest observed gains with saved uncertainty.',
        '- Completeness: all locked methods/outcomes remain in full reports and the atlas; no study is represented as unperformed.',
        '- Method design: preserve λ=10/two steps and distinguish final parameter bytes from operational cost.', '',
        'No new experiment, parameter selection, effect-size calculation from labels, or external-review verdict was introduced. This is a local editorial self-review.']
    put('appendix/PRESENTATION_EDIT_NOTES.md', '\n'.join(notes))
    put('PRESENTATION_CLAIMS.json', json.dumps({'revision': REVISION, 'central_claim': claim,
        'highlights': highlights, 'storage': lock['parameter_storage_comparison'],
        'primary_test_family': {'confirmed': 11, 'total': 30},
        'source_summary_sha256': {v: sha(ROOT / v) for v in FILES.values()}}, indent=2, ensure_ascii=False))

    old_html = (ROOT / 'START_HERE.html').read_text(encoding='utf-8')
    css = re.search(r'<style>(.*?)</style>', old_html, re.S).group(1)
    cards = ''.join(f'<tr><td>{html.escape(h["title"])}</td><td>{html.escape(cases[i])}</td><td><b>{h["delta_ndcg10"]:+.4f}</b></td></tr>' for i, h in enumerate(highlights))
    body = f'''<main><div class="eyebrow">ARC2-Global · Research overview</div>
<h1>Two corrections.<br>One compact migration map.</h1>
<p class="muted">Reuse existing document embeddings while moving an index into a new model space.</p>
<section class="card claim">{html.escape(claim)}</section>
<div class="grid"><div class="stat"><b>1.13MiB</b><span>Final float32 affine map,384→768</span></div><div class="stat"><b>+0.0243</b><span>DEV macro nDCG gain over Procrustes,1,024fitting pairs</span></div><div class="stat"><b>11 improvements</b><span>Prospective TREC-COVID:30declared comparisons</span></div></div>
<section class="card"><h2>A small adapter with measured retrieval gains</h2><p>ARC2 learns from paired old/new document embeddings, applies two closed-form tangent corrections (λ=10), and compiles the result into an affine map plus normalization. Native destination vectors replace proxies as backfill proceeds. Queries stay in the destination space; each document has one index vector.</p><p>The final map stores295,680coefficients—<b>114.7× fewer parameter bytes</b> than the declared Converter MLP—and requires no neural training. This comparison concerns final mapping weights.</p></section>
<section class="card"><h2>Four results that carry the paper</h2><table><thead><tr><th>Evidence</th><th>Setting</th><th>Δ nDCG@10</th></tr></thead><tbody>{cards}</tbody></table><p><small>Selected highlights from the locked studies. Saved family intervals and exact conditions are in <a href="CLAIM_LOCK.md">the claim sheet</a>; all declared comparisons are in <a href="EVIDENCE_GUIDE.md">the evidence guide</a>.</small></p></section>
<section class="card"><h2>Prospective transfer across migration budgets</h2><p>On TREC-COVID/E5, ARC2 has positive family intervals over Converter and affine ridge at25%,50%and75%document budgets. Converter gains are+0.2572,+0.2314and+0.2000nDCG; the full curves below retain every declared method and native reference.</p><figure><a href="results/b2_review_20261101/figures/b2_ndcg10_vs_budget.pdf"><img src="results/b2_review_20261101/figures/b2_ndcg10_vs_budget.png" alt="Prospective quality curves for all declared methods"></a><figcaption>Two encoder pairs, five seeds. Click for vector PDF. Gains are tied to the reported encoder/budget conditions.</figcaption></figure></section>
<section class="card"><h2>The gain is supported by mechanism and supervision controls</h2><p>The second tangent correction adds+0.0069macro nDCG beyond one step in the DEV ablation. In a separate matched all-paid FiQA/MiniLM study, ARC2 wins four of five family-adjusted comparisons when every method receives the same28,819fitting pairs; ridge is unresolved.</p><p>These findings connect the method design to retrieval gains and show a positive operating point beyond the main1,024-pair setting.</p><p><a href="RESEARCH_STORY.md">Read the paper story</a> · <a href="EVIDENCE_GUIDE.md">Open complete results and controls</a></p></section>
<section class="card"><h2>When ARC2 is useful</h2><p>A new encoder must be introduced gradually, a compact non-neural forward adapter is valuable, and the application can evaluate relevance at its intended migration budget. ARC2 offers a simple final mapping with measured quality gains in the documented settings.</p><p><small>Gains vary with encoder pair and budget. The full evidence guide contains the complete outcome matrices and operational measurement scope.</small></p><p><a href="CLAIM_LOCK.md">Claim sheet</a> · <a href="REPRODUCE.md">Reproduce the evidence</a></p></section>
<footer>Presentation revision R3 · Algorithm and scientific results unchanged · Complete evidence and review status available through the evidence guide.</footer></main>'''
    put('START_HERE.html', '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ARC2-Global · Compact mapping, stronger retrieval</title><style>' + css + '</style>' + body + '</html>')
    # Improve narrative spacing without editing file names, data or source.
    words = r'dimensions|coefficients|parameters|fitting|paired|paid|migration|document|documents|budget|budgets|interval|comparisons|logical|cells|macro|nDCG|MiB'
    for name in ['README.md', 'CLAIM_LOCK.md', 'RESEARCH_STORY.md', 'REPRODUCE.md', 'EVIDENCE_GUIDE.md', 'START_HERE.html']:
        p = ROOT / name; t = p.read_text(encoding='utf-8')
        t = re.sub(r'(?<![A-Za-z_])(\d[\d,.]*)(' + words + r')\b', r'\1 \2', t)
        for a, b in {'For384': 'For 384', 'for384': 'for 384', 'at25%': 'at 25%', 'same28,819': 'same 28,819',
                     'over24': 'over 24', 'same1,024': 'same 1,024', 'at50%': 'at 50%',
                     'covers171,332': 'covers 171,332', 'with30': 'with 30',
                     'contains33,927,168': 'contains 33,927,168', 'stores295,680': 'stores 295,680',
                     'approximately1.13': 'approximately 1.13'}.items():
            t = t.replace(a, b)
        put(name, t)
    print(json.dumps({'status': 'PAPER_STORY_WRITTEN', 'revision': REVISION,
        'scientific_data_changed': False, 'parameter_byte_ratio': ratio,
        'human_documents': ['README.md', 'CLAIM_LOCK.md', 'RESEARCH_STORY.md', 'EVIDENCE_GUIDE.md', 'REPRODUCE.md', 'START_HERE.html']}))


if __name__ == '__main__':
    main()
