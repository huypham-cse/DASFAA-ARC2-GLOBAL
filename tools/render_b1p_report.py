"""Render the completed B1-P report from verified frozen scoring outputs."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "results/b1p_r5_review_20261027"
PRIMARY = "arc2_global_tangent2_r1"
PAIRS = ("minilm_distilroberta", "e5_small_base")
METHODS = {
    "procrustes_global": "A2M / global Procrustes adaptation",
    PRIMARY: "ARC2-Global",
    "la2m20_integration_script_adaptation": "LA2M, 20 clusters (adaptation)",
    "simplelinear_official_final50_mlp5": "SimpleLinear official code (5-layer MLP)",
    "ridge_affine_l10_bias_regularized": "Affine ridge, lambda10 (bias regularized)",
    "embedding_converter_paper_spec": "Embedding-Converter paper-spec adaptation",
}


def render():
    qa = json.loads((ROOT / "provenance/qa/b1p_r5_completed_verification_20261027.json").read_text())
    assert qa["status"] == "PASS"
    summary = json.loads((BUNDLE / "scoring/results_summary.json").read_text())
    assert summary["status"] == "DEV_SCORED" and summary["ranking_cells"] == 124
    rows = {(x["pair"], x["regime"], x["method"]): x for x in summary["means"]}
    contrasts = summary["contrasts"]
    assert len(contrasts) == 32 and len(rows) == 28
    lines = [
        "# B1-P completed: all-paid fitting at the same 50% encoding budget", "",
        "**COMPLETE and locally verified, 27 October 2026.**",
        "",
        "FiQA inspected DEV: 57,638 documents, 500 queries, two encoder pairs and five seeds. "
        "Both regimes replace the same 28,819 paid IDs (anchors included); fitting uses either "
        "1,024 anchor pairs or all 28,819 already-paid pairs. No method, lambda10/tangent2, "
        "quality threshold or case selection was changed after scoring.",
        "",
        "All 124 rankings are sealed: 120 partial cells and four full references. "
        "51 rankings were reused and 73 generated in R5. All ten all-paid converter fits passed. "
        "The original scorer failed before TSV parsing on duplicate exclusive receipt creation; "
        "its FAILED_PRESERVED metadata and logs remain unchanged. A separately committed, "
        "qrel-free-smoked CPU recovery scored the unchanged seal successfully.",
        "", "## All-paid comparison", "",
        "Five-seed means. Every partial row below uses the same 50% destination encoding budget "
        "and all 28,819 fitting pairs. References are separate operating points: Full-X uses "
        "the incumbent query/document encoder; Full-Y uses the target encoder throughout.", "",
        "| Method | MiniLM to DistilRoBERTa nDCG@10 | Recall@100 | E5-small to E5-base nDCG@10 | Recall@100 |",
        "|---|---:|---:|---:|---:|",
    ]
    for method, label in list(METHODS.items()) + [("full_x", "Full-X reference"), ("full_y", "Full-Y reference")]:
        regime = "reference" if method.startswith("full_") else "allpaid28819"
        values = [rows[(pair, regime, method)][metric]["mean"]
                  for pair in PAIRS for metric in ("ndcg10", "recall100")]
        lines.append(f"| {label} | " + " | ".join(f"{v:.6f}" for v in values) + " |")
    lines += ["", "## Matched all-paid nDCG contrasts", "",
        "ARC2-Global minus each baseline. Intervals use the predeclared 32-contrast "
        "Bonferroni family (approximate 95% family coverage; 99.84375% per interval). "
        "An interval crossing zero is unresolved, not equivalence.", "",
        "| Pair | Baseline | Delta nDCG | Family interval | Interpretation |",
        "|---|---|---:|---|---|",
    ]
    for c in contrasts:
        if c["kind"] != "arc2_allpaid_vs_baseline_allpaid":
            continue
        v = c["ndcg10"]
        lo, hi = v["ci_bonferroni_family95"]
        pair = "MiniLM" if c["pair"] == PAIRS[0] else "E5"
        lines.append(f"| {pair} | {METHODS[c['right']['method']]} | {v['delta']:+.6f} | "
                     f"[{lo:+.6f}, {hi:+.6f}] | {v['family_interval_interpretation']} |")
    lines += ["", "## Effect of additional fitting pairs on ARC2-Global", "",
        "Encoding budget stays 50%; only the fitting-pair count changes. Recall intervals "
        "below are nominal 95% descriptive intervals, outside the nDCG family correction.", "",
        "| Pair | Fixed1,024 nDCG | All-paid nDCG | Delta nDCG [family interval] | Delta Recall [descriptive95] |",
        "|---|---:|---:|---|---|",
    ]
    for pair in PAIRS:
        c = next(c for c in contrasts if c["pair"] == pair and c["kind"] == "within_method"
                 and c["right"]["method"] == PRIMARY)
        n, rec = c["ndcg10"], c["recall100"]
        nlo, nhi = n["ci_bonferroni_family95"]
        rlo, rhi = rec["ci95"]
        fixed = rows[(pair, "fixed1024", PRIMARY)]["ndcg10"]["mean"]
        paid = rows[(pair, "allpaid28819", PRIMARY)]["ndcg10"]["mean"]
        lines.append(f"| {pair} | {fixed:.6f} | {paid:.6f} | {n['delta']:+.6f} "
                     f"[{nlo:+.6f}, {nhi:+.6f}] | {rec['delta']:+.6f} [{rlo:+.6f}, {rhi:+.6f}] |")
    lines += ["", "## Supported conclusions and limits", "",
        "- MiniLM: all-paid ARC2 has higher nDCG than Procrustes, LA2M, official-code SimpleLinear "
        "and the converter, with all four family intervals above zero. Its nDCG difference "
        "from affine ridge is unresolved. Recall is higher than ridge descriptively; this "
        "does not establish nDCG equivalence or overall dominance.",
        "- E5: all-paid ARC2 trails Procrustes and LA2M in the nDCG family comparisons, exceeds "
        "SimpleLinear/ridge, and is unresolved against the converter. Its all-paid nDCG mean "
        "is below fixed-anchor ARC2, with that family interval unresolved; Recall decreases "
        "with a negative descriptive interval. More fitting pairs are not uniformly beneficial.",
        "- MiniLM fixed-anchor ARC2 trails every all-paid baseline in the locked cross-regime "
        "nDCG comparisons. Thus fixed-anchor comparisons alone do not establish superiority "
        "over baselines trained on all already-paid pairs.",
        "- ARC2 means remain below both Full-X and Full-Y on both metrics in both encoder "
        "pairs/regimes. All methods, both regimes, references and all 32 contrast signs remain reported.",
        "- This is development evidence with encoder-dependent strengths. It establishes neither "
        "an independent paper win nor a dollar saving, physical migration cost, SLO benefit, "
        "universal best method or D1 admission. No method switch is selected here.",
        "", "## Evidence and next action", "",
        "Generation: `7530c8e`; recovery orchestrator: `4062d96`. Unchanged original metric/bootstrap "
        "sources; 20,000 shared query resamples after five-seed averaging. Local QA recomputed "
        "all 28 means, 32 contrast deltas and 96 intervals; largest difference was 2.22e-16.",
        "",
        "[Complete fixed/all-paid means, seed variation and all 32 nDCG/Recall contrasts](scoring/results_summary.md), "
        "[machine-readable results](scoring/results_summary.json), "
        "[per-query output](scoring/per_query.npy), "
        "[generation inventory](full_manifest.json). Large weights/proxies stay remote; "
        "this local bundle contains all rankings, IDs, selections, metrics and logs. "
        "Cached-vector encodes are not a physical deployment cost measurement.",
        "",
        "B1-P is complete. Current execution and subsequent phase status are maintained in "
        "the single live experiment tracker and the consolidated REPORT.md.", "",
    ]
    text = "\n".join(lines)
    (BUNDLE / "SUMMARY.md").write_text(text, encoding="utf-8", newline="\n")
    report = ROOT / "REPORT.md"
    original = report.read_text(encoding="utf-8")
    original = original.replace(
        "It enables the later all-paid experiment; that experiment and physical cost/SLO remain unrun.",
        "It established numerical readiness for B1-P, now reported below. Physical cost/SLO remains unmeasured.")
    begin, end = "<!-- BEGIN B1P_GENERATED -->", "<!-- END B1P_GENERATED -->"
    section = text.replace("# B1-P completed:", "## B1-P completed:", 1)
    for heading in ("All-paid comparison", "Matched all-paid nDCG contrasts",
                    "Effect of additional fitting pairs on ARC2-Global", "Supported conclusions and limits",
                    "Evidence and next action"):
        section = section.replace("## " + heading, "### " + heading)
    for target in ("scoring/results_summary.md", "scoring/results_summary.json", "scoring/per_query.npy", "full_manifest.json"):
        section = section.replace(f"]({target})", f"](results/b1p_r5_review_20261027/{target})")
    block = begin + "\n" + section + end
    if begin in original:
        a, b = original.index(begin), original.index(end) + len(end)
        original = original[:a] + block + original[b:]
    else:
        original = original.rstrip() + "\n\n" + block + "\n"
    report.write_text(original, encoding="utf-8", newline="\n")
    print("Rendered verified B1-P SUMMARY.md and REPORT.md; no scientific inputs changed")


if __name__ == "__main__":
    render()
