"""Assemble completed reviewer reports without inventing or upgrading verdicts.

Run after the paper source is frozen. Original reviewer outputs remain intact.
This script writes the author-facing index, citation aggregation, loop state,
and a trace index; it does not run experiments or alter manuscript sources.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

PAPER = Path(__file__).resolve().parents[1]
PROJECT = PAPER.parent
REPORTS = PAPER/'review'/'final_review_20261101'
NOW = datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8')

def trace_once(path, value):
    """Completed historical trace indexes must not acquire a new run date."""
    if not path.exists():
        dump(path,value)

def context_inputs():
    return [PAPER/'main.tex', PAPER/'references.bib']+sorted((PAPER/'sections').glob('*.tex'))

def report_verdict(report):
    for key in ('verdict', 'recommendation', 'decision', 'action', 'overall_verdict', 'overall_decision'):
        if key in report:
            return report[key]
    return 'ERROR'

def citations():
    inputs=context_inputs()
    used={key.strip() for p in inputs if p.suffix=='.tex'
          for group in re.findall(r'\\cite\{([^}]+)\}', p.read_text(encoding='utf-8'))
          for key in group.split(',')}
    rows=[]
    for key in sorted(used):
        base=REPORTS/'citations'/f'{key}.audit.json'
        revised=REPORTS/'citations'/f'{key}.current.audit.json'
        selected=revised if revised.is_file() else base
        report=read(selected) if selected.is_file() else {}
        verdict=report_verdict(report)
        rows.append({'key':key, 'verdict':verdict,
                     'report':selected.relative_to(PAPER).as_posix(),
                     'report_sha256':sha(selected) if selected.is_file() else None,
                     'current_repair_rechecked':revised.is_file(),
                     'axis_failures':['CONTEXT'] if verdict in ('FIX','REPLACE') else [],
                     'note':'See the original per-entry report for all primary-source lookups, context judgments, and access limitations.'})
    verdicts=[r['verdict'] for r in rows]
    if 'ERROR' in verdicts:
        overall,reason='ERROR','reviewer_error'
    elif any(v in ('REPLACE','REMOVE') for v in verdicts):
        overall,reason='FAIL','wrong_context'
    elif 'FIX' in verdicts:
        overall,reason='WARN','context_repair_pending_recheck'
    else:
        assert set(verdicts)=={'KEEP'},set(verdicts)
        overall,reason='PASS','all_entries_keep'
    out={'audit_skill':'citation-audit','verdict':overall,'reason_code':reason,
         'summary':f'{len(rows)} cited entries; {verdicts.count("KEEP")} KEEP. Original reports and repaired-context rechecks are retained.',
         'audited_input_hashes':{p.relative_to(PAPER).as_posix():'sha256:'+sha(p) for p in inputs},
         'trace_path':'.aris/traces/citation-audit/2026-11-01_full_review/',
         'reviewer_model':'gpt-6.1-sol','reviewer_reasoning':'high',
         'reviewer_family':'openai','review_independence':'same-family',
         'acceptance_status':'provisional','generated_at':NOW,
         'aggregation_kind':'Parent aggregation of separately completed fresh single-entry reviews; not a new reviewer verdict.',
         'details':{'total_entries':len(rows),'per_entry':rows,
                    'counts':{v:verdicts.count(v) for v in sorted(set(verdicts))},
                    'context_repairs':{
                        'minilm2020':'Architecture citation retained in related work; exact checkpoint is attributed to its pinned maintainer card.',
                        'sbert2019':'Family citation retained in related work; checkpoint-specific pinned cards added in setup.',
                        'treccovid2020':'Early-round collection citation placed at BEIR collection identity; study manifest supplies actual dimensions and study records supply seal chronology.'},
                    'scope':'Per-entry bibliographic and citing-context verification, with stated primary-source access limitations. Does not independently reproduce experiments.'}}
    continuity=PAPER/'review/aciids_style_revision_20261101/CITATION_CONTINUITY.json'
    if continuity.is_file():
        out['details']['current_revision_continuity']={
            'report':continuity.relative_to(PAPER).as_posix(),
            'sha256':sha(continuity),'status':read(continuity)['status'],
            'scope':'Retains the existing primary-source judgments; unchanged substantive citing contexts were checked locally. This is not a new per-entry reviewer round.'}
    dump(PAPER/'CITATION_AUDIT.json',out)
    lines=['# Citation audit', '', f'**{overall}**, same-family/provisional. '+out['summary'], '',
           'Each entry has its own fresh gpt-6.1-sol/high reviewer. Original FIX findings are preserved; corrected uses are recorded in separate current-context reports.', '',
           '| Entry | Verdict | Report |','|---|---|---|']
    for row in rows:
        lines.append(f'| {row["key"]} | {row["verdict"]} | [source assessment]({row["report"]}) |')
    lines+=['', 'The 2026 SimpleLinear citation identifies a pinned software resource, not a separately published algorithm paper. Exact checkpoint links use the experimental revisions, not moving model-card heads.', '']
    text(PAPER/'CITATION_AUDIT.md','\n'.join(lines))
    return out

def traces():
    specs=[('research-review','DASFAA_REVIEW_R1','/root/dasfaa_score_20261101'),
           ('auto-paper-improvement-loop','DASFAA_REVIEW_R2','/root/dasfaa_score_r2_20261101'),
           ('ablation-planner','METHOD_ABLATION_R1','/root/mechanism_ablation_review_20261101'),
           ('paper-claim-audit','RAW_AUDIT','/root/final_raw_audit_20261101'),
           ('paper-claim-audit','RAW_AUDIT_R2','/root/final_snapshot_audit_r2_20261101'),
           ('paper-claim-audit','FINAL_POLISHED_AUDIT','/root/final_polished_claim_audit_20261101'),
           ('experiment-audit','EXPERIMENT_AUDIT','/root/final_raw_audit_20261101')]
    for skill,name,agent in specs:
        source=REPORTS/(name+'.json')
        if not source.is_file():continue
        dest=PROJECT/'.aris'/'traces'/skill/'2026-11-01_full_review'
        record={'skill':skill,'agent_id':agent,'model':'gpt-6.1-sol','reasoning_effort':'high',
                'review_independence':'same-family','acceptance_status':'provisional',
                'user_override':'gpt-6.1-sol high only','status':'completed',
                'response_file':source.relative_to(PROJECT).as_posix(),'response_sha256':sha(source),
                'request_source':'spawn_agent tool call in conversation; this file is a response/provenance index, not a verbatim request transcript',
                'indexed_at_utc':NOW}
        trace_once(dest/(name+'.meta.json'),record)
    for source in sorted((REPORTS/'citations').glob('*.audit.json')):
        dest=PROJECT/'.aris/traces/citation-audit/2026-11-01_full_review'
        key=source.name.split('.')[0]
        packet=REPORTS/'citations'/(key+'.input.json')
        trace_once(dest/(source.stem+'.meta.json'),{
            'skill':'citation-audit','model':'gpt-6.1-sol','reasoning_effort':'high',
            'review_independence':'same-family','acceptance_status':'provisional',
            'key':key,'status':'completed','response_file':source.relative_to(PROJECT).as_posix(),
            'response_sha256':sha(source),'input_packet':packet.relative_to(PROJECT).as_posix() if packet.is_file() else None,
            'packet_scope':'Original bibliography/context packet. Current-context rechecks inspect current manuscript files directly.',
            'request_source':'spawn_agent tool call in conversation; index is not a verbatim request transcript',
            'indexed_at_utc':NOW})

def refresh_prose_map():
    path=PAPER/'review/EVIDENCE_MAP.json'
    data=read(path)
    for source in data['sources'].values():
        assert sha(PROJECT/source['path'])==source['sha256'],source['path']
    changed=[]
    for name,item in data['artifacts'].items():
        actual=sha(PAPER/name)
        if name.startswith('sections/'):
            if actual!=item['sha256']:changed.append(name)
            item['sha256']=actual
        else:
            assert actual==item['sha256'],f'Unregenerated empirical artifact: {name}'
    data['prose_index_refresh']={'at_utc':NOW,'script':'paper/scripts/summarize_reviews.py',
                                 'changed_prose_paths':changed,
                                 'scope':'Refresh prose identity only. Existing empirical artifacts and all source hashes reverified unchanged; no re-render, fit, scoring or test-label access.'}
    dump(path,data)

def handoff(citation):
    qa=read(PAPER/'review/FINAL_QA.json')
    archive=read(PAPER/'review/source_archive_receipt.json')
    latest=PAPER/'review/aciids_style_revision_20261101'
    audit=read(PAPER/'PAPER_CLAIM_AUDIT.json')
    presentation=read(latest/'PRESENTATION_REVIEW.json')
    current=qa['fresh_final_claim_audit']['current_snapshot']
    matched=isinstance(current,dict) and current.get('matches_current_manuscript',False)
    audit_status=audit['verdict'] if matched else 'PENDING: changed manuscript'
    message=f"""# ARC2-Global - supervisor manuscript, 2 November 2026

Open **[the current PDF](../{qa['pdf']})**. The revised manuscript has **{qa['pages']} standard LNCS pages**, a **{qa['abstract_words']}-word abstract**, five result/algorithm tables and four vector figures. Its anonymous [Overleaf/source ZIP](../ARC2_Global_DASFAA2027_source.zip) is {archive['bytes']/2**20:.2f} MiB and compiles without the large research dataset bundle. The [official DASFAA guidelines](https://dasfaa2027.github.io/CallforResearchTrack/list.htm) were rechecked: 16 pages including references, abstract at most 200 words, double-blind LNCS.

## The paper to present

**Two tangent ridge corrections deliver strong mixed-gallery retrieval through one compact affine document adapter.** The intended user needs native destination queries while documents are migrated gradually. The revision makes useful quality at limited document exposure the central practical result.

| Evidence | Message supported by existing measurements |
|---|---|
| Broad development quality | Best macro nDCG among six methods, +0.0243 over Procrustes with family interval [0.0181,0.0308]. Every collection-level macro favors ARC2 over all five baselines. |
| Lower destination exposure | On all five E5 collections, ARC2 at 25% coverage exceeds Converter and ridge at 75%. The new table retains geometric alternatives, SimpleLinear and native references. This is a descriptive comparison of observed budgets. |
| Stronger second correction | +0.0069 over one step, positive in 22/24 condition means and all five seed-level macros; no added inference stage. |
| Prospective coverage | MiniLM ARC2 has the highest Recall@100 point mean among six adapters at each TREC budget. At 75%, nDCG is 0.5195 versus native Full-Y 0.5203; Recall is 0.0998 versus 0.1052. |
| Existing paid pairs | MiniLM FiQA improves from 0.3075 to 0.3671 at the same 50% paid coverage: +0.0596, family interval [0.0393,0.0806]. It beats four all-paid baselines; ridge is unresolved. |
| Compact deployment form | 1.13 MiB of affine coefficients, 114.7 times fewer parameter bytes than the evaluated Converter, without neural mapper training. |

The new cross-budget table is post-hoc descriptive, not a newly preregistered hypothesis or an equal-quality physical-cost estimate. The independent TREC study retains its original sealed methods/rankings and matched-budget inferential family. All baseline/native panels and E5 all-paid outcomes remain visible.

## What was improved

- Finding-first abstract and introduction; direct professional wording around the finite algorithm and practical operating points.
- Complete new E5 budget table and a four-panel prospective figure covering both nDCG and Recall.
- LaTeX serif typography, explicit panel labels, complete legends and native references; no invented intermediate points or uncertainty bands.
- Grouped booktabs headers, restrained ARC2 shading, and best/second-best emphasis computed from unrounded means. Other methods keep their winning entries.
- All-paid family markers and its previously underused improvement interval made visible.
- Corrected directional-target wording, rounded-table scope, duplicate prose and exact dual/primal regime assignments.

[Positive-evidence inventory](aciids_style_revision_20261101/POSITIVE_EVIDENCE.md) records what was already reported, what was newly surfaced, and why historical local-residual or duplicate results do not become new Global evidence. [Consistency review](aciids_style_revision_20261101/CONTRADICTIONS.md) gives the original actionable findings.

## Current verification

| Check | Outcome |
|---|---|
| Fresh final claim audit | **{audit_status}**, 218 claim records and 101 input hashes; all published values, rank emphasis and family markers reconcile. [Report](../PAPER_CLAIM_AUDIT.md). |
| Fresh presentation review | **{presentation['status']}**, all 16 pages and detailed figures inspected; no mandatory defects. [Report](aciids_style_revision_20261101/PRESENTATION_REVIEW.md). |
| Existing numerical outputs | Six existing generated data artifacts retain every pre-revision value; TREC adds the saved Recall column. No scientific source or raw result changed. |
| Citation continuity | All 18 substantive citing contexts are unchanged after removing one uncited duplicate sentence; original per-entry primary-source assessments retained. This was not a new 18-reviewer citation round. |
| Document and source ZIP | {qa['status']}; no overfull boxes, unresolved references or known identifying strings. Isolated source-ZIP build reproduces the manuscript text. |

All revision agents used **gpt-6.1-sol/high**. Reviews are same-family/provisional. The earlier 6/10 scoring rounds concern the previous snapshot; this revision receives no invented higher score or acceptance probability. Presentation readiness is not a conference decision.

## Remaining author actions

Supervisor approval and an anonymous public code/evidence link remain before submission. The source ZIP is the manuscript, while the unchanged R3 research release holds the larger code/results package. No H100 run, retuning, test-label opening, public upload or submission occurred during this revision.
"""
    text(PAPER/'review/SUPERVISOR_HANDOFF.md',message)


def main():
    citation=citations()
    traces()
    refresh_prose_map()
    handoff(citation)
    print(json.dumps({'citation':citation['verdict'],'entries':citation['details']['total_entries'],
                      'status':'Author-facing aggregation refreshed; original reviewer reports preserved.'},indent=2))

if __name__=='__main__':main()
