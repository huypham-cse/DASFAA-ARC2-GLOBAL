"""Package the three fixed-snapshot reviews; never changes manuscript/evidence."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


snapshot = read("INPUT_SNAPSHOT.json")
for relative, expected in snapshot["paper_relative_sha256"].items():
    assert digest(ROOT / "paper" / relative) == expected, relative
paper = read("PAPER_SCORE.json")
support = read("RESULT_TO_CLAIM_SCORE.json")
novelty = read("NOVELTY_SCORE.json")
now = datetime.now(timezone.utc).isoformat()
reports = ["PAPER_SCORE", "RESULT_TO_CLAIM_SCORE", "NOVELTY_SCORE"]
card = {
    "date": "2026-11-02", "created_utc": now,
    "model": "gpt-6.1-sol", "reasoning_effort": "high",
    "review_independence": "same-family", "acceptance_status": "provisional",
    "paper_sha256": snapshot["paper_relative_sha256"]["ARC2_Global_DASFAA2027_final.pdf"],
    "overall_score": paper["overall_score"], "recommendation": paper["recommendation"],
    "overall_confidence_out_of_5": paper["confidence"],
    "paper_dimensions": paper["scores"],
    "result_to_claim": {"verdict": support["claim_supported"], "scores": support["scores"]},
    "novelty_review": novelty,
    "interpretation": "Overall is the paper reviewer's holistic score, not an average across skills, an official DASFAA rubric, or an acceptance probability.",
    "exposure_disclosure": "Paper reviewer did not see earlier scores. Support reviewer incidentally saw prior opinions in required instructions/protocol text and disclosed this. Novelty reviewer avoided previous local scores, but search snippets exposed external commentary. None of these reviews is cross-family.",
    "followups_without_new_experiments": [
        "Add published GCPA citation and equation-level positioning against its consensus-target residual MLP and angular trust hinge.",
        "Provide accessible anonymous frozen code/evidence before submission.",
        "Obtain supervisor feedback on the current compact refinement and quality/exposure story."
    ],
    "new_experiments_required_for_current_bounded_claims": False,
    "scientific_files_changed": False,
    "report_hashes": {name + suffix: digest(HERE / (name + suffix)) for name in reports for suffix in [".md", ".json"]},
}
write_json(HERE / "SCORECARD.json", card)
md = """# ARC2-Global: current paper scorecard

**6/10 — weak accept.** This is a completed internal ARIS assessment of the current 16-page manuscript, using three separate gpt-6.1-sol/high reviewer threads. Overall confidence: **4/5**.

| ARIS review | Result | Meaning |
|---|---|---|
| Research review | **6/10 — weak accept** | A useful, coherent scoped contribution; not yet a strong accept. |
| Novelty check | **6/10 — PROCEED** | A concrete incremental computation; no inspected paper duplicates its exact update. |
| Result-to-claim | **YES**, high confidence | All 12 evaluated bounded claims supported; no material unsupported claim found. |

The overall score is one reviewer's holistic judgment. It is not an average of skill scores, an official DASFAA score, or an acceptance probability. The holistic reviewer independently rated novelty 5/10; the focused novelty reviewer rated it 6/10 under the novelty skill's stated anchors. This modest difference is retained rather than reconciled by picking a preferred score.

## Dimension scores

| Paper-review dimension | Score / 10 |
|---|---:|
| Novelty | 5 |
| Technical soundness | 8 |
| Experimental evidence | 7 |
| Practical significance | 6 |
| Clarity and figures | 8 |
| Reproducibility | 7 |
| Venue fit | 8 |

| Focused evidence-review dimension | Score / 10 |
|---|---:|
| Empirical support | 8 |
| Fairness and rigor | 8 |
| Value in the stated deployment scenario | 7 |
| Claim calibration | 9 |

## What makes the paper worth reading

The development study supports +0.0243 nDCG over Procrustes, with a positive corrected interval; the second tangent correction contributes +0.0069. These are development findings, not independent-test victories. In the prospective E5 study, gains over the declared Converter configuration persist across budgets. The five-collection E5 comparison also shows ARC2 at 25% exposure above Converter and ridge at 75% in point means; this is a descriptive quality/exposure result, not a measured physical-cost saving.

The final map has 1.13 MiB of float32 coefficients and needs no neural mapper training. Mixed-gallery and all-paid analyses explain when the approach helps and when replacing proxies can hurt. Together, these form a useful compact-migration contribution with concrete operating conditions.

## Why the overall score remains 6

The exact refinement is a defensible combination of established ingredients. On the prospective collection, Procrustes has higher nDCG point means in all six conditions, with unresolved corrected contrasts. Thus the strongest geometric-baseline advantage is not independently confirmed. One 50-query held collection and two encoder transitions also bound generality. These are contribution-strength limits; the reviews found no material contradiction in the current bounded claims.

## Finite follow-up before submission

1. Add the published [GCPA / Multi-Way Representation Alignment](https://proceedings.mlr.press/v306/achara26a.html) citation and a short technical comparison. Its consensus-target residual MLP and angular trust hinge differ from ARC2's paired-destination tangent ridge updates. This is a positioning repair, not evidence of an exact duplicate.
2. Supply an accessible anonymous frozen code/evidence package. The existing anonymous manuscript-source ZIP is not the full scientific artifact.
3. Obtain supervisor feedback on the current contribution and framing. **No new scientific experiment is required to support the claims presently written.** Broader superiority or physical deployment claims would require additional evidence.

## Review provenance and limits

All reviews are **same-family / provisional**. The paper grader did not see earlier local scores. The evidence reviewer accidentally encountered previous opinions in required AGENTS/protocol text and disclosed that exposure. The novelty reviewer avoided prior local scores but saw incidental external search commentary; primary papers alone support its technical comparisons. Consequently this is not three perfectly blinded external reviews.

Reviewers inspected all 16 PDF pages, existing per-query outputs and selected sealed records. The support reviewer checked saved means and family quantiles and hash-verified all 184 B2 rankings. No qrels were opened, no new scientific runs launched, and no manuscript or scientific inputs changed. Numerical consistency is not a complete independent re-execution of fitting/scoring or a proof of prior non-exposure.

Scored PDF SHA256: `e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc`.

## Complete reports

- [Research review](PAPER_SCORE.md)
- [Novelty check and primary-source comparisons](NOVELTY_SCORE.md)
- [Result-to-claim review](RESULT_TO_CLAIM_SCORE.md)
- [Machine-readable scorecard](SCORECARD.json)
- [Frozen input snapshot](INPUT_SNAPSHOT.json)

Original reports and differing judgments are retained. This scorecard does not modify the manuscript, submission status, protocols or historical verdicts.
"""
(HERE / "SCORECARD.md").write_text(md, encoding="utf-8")

routes = [("research-review", "PAPER_SCORE", "/root/score_paper_fresh_20261102"),
          ("result-to-claim", "RESULT_TO_CLAIM_SCORE", "/root/score_support_fresh_20261102"),
          ("novelty-check", "NOVELTY_SCORE", "/root/score_novelty_fresh_20261102")]
for skill, name, agent in routes:
    trace = ROOT / ".aris" / "traces" / skill / "2026-11-02_scoring"
    (trace / "001-score.response.md").write_bytes((HERE / (name + ".md")).read_bytes())
    write_json(trace / "001-score.meta.json", {
        "call_number": 1, "purpose": "current-paper-scoring", "timestamp": now,
        "agent_id": agent, "model": "gpt-6.1-sol", "reasoning_effort": "high",
        "reviewer_family": "openai", "review_independence": "same-family",
        "acceptance_status": "provisional", "status": "ok",
        "response_sha256": digest(HERE / (name + ".md")),
        "full_report_json": str((HERE / (name + ".json")).relative_to(ROOT)),
        "exposure_disclosure": card["exposure_disclosure"],
    })
    event = {"event": "review_trace", "skill": skill, "purpose": "current-paper-scoring",
             "agent_id": agent, "trace_path": trace.relative_to(ROOT).as_posix(), "status": "ok"}
    events = ROOT / ".aris" / "meta" / "events.jsonl"
    encoded = json.dumps(event, separators=(",", ":"))
    if encoded not in events.read_text(encoding="utf-8-sig"):
        with events.open("a", encoding="utf-8") as stream:
            stream.write(encoded + "\n")
print("Scorecard and local-only full traces saved; frozen inputs unchanged.")
