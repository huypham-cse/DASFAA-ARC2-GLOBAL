"""One-shot B1-P FiQA DEV scoring, only after all 124 rankings are sealed.

This process never fits/selects a method and cannot access Nano or TREC labels.
Failed attempts retain their exclusive output directory and all partial artifacts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import traceback

import numpy as np

# Importing this module defines functions only. In particular, neither its
# multi-dataset qrel loader nor its CLI is invoked by the B1-P scorer.
try:
    from b1m_score import (inside, mean_std, metrics_for, now, parse_qrel_rows,
                           read_json, sha, synthetic_checks, write_json)
except ModuleNotFoundError as error:
    if error.name != "b1m_score":
        raise
    from ops.b1m_score import (inside, mean_std, metrics_for, now, parse_qrel_rows,
                               read_json, sha, synthetic_checks, write_json)

DATASET = "FiQA"
PAIRS = ("minilm_distilroberta", "e5_small_base")
SEEDS = (17, 29, 41, 53, 67)
REGIMES = ("fixed1024", "allpaid28819")
PRIMARY = "arc2_global_tangent2_r1"
METHODS = ("procrustes_global", PRIMARY, "la2m20_integration_script_adaptation",
           "simplelinear_official_final50_mlp5", "ridge_affine_l10_bias_regularized",
           "embedding_converter_paper_spec")
METRICS = ("ndcg10", "recall100")
BOOTSTRAP_DRAWS = 20000
BOOTSTRAP_SEED = 20261026
QREL_SHA256 = "03b27e547cd29dc721c3b93ce8ddd70df6b2d0ce954d8ef3659d386e8cd72c11"
FAMILY = {"metric": "ndcg10", "contrasts": 32, "family_confidence": 0.95,
          "per_interval_confidence": 0.9984375, "method": "bonferroni_percentile"}
KEY_FIELDS = ("dataset", "pair", "method", "regime", "seed", "budget")
ROOT = Path(__file__).resolve().parents[1]
EXPOSURE = "Previously inspected FiQA DEV; not independent confirmation"


def key(cell):
    return tuple(cell[name] for name in KEY_FIELDS)


def expected_contrasts():
    """The order and directions are fixed before current label access."""
    result = []
    for pair in PAIRS:
        for kind in ("within_method", "arc2_allpaid_vs_baseline_allpaid",
                     "arc2_fixed_vs_baseline_allpaid"):
            for method in METHODS:
                if kind != "within_method" and method == PRIMARY:
                    continue
                left = {"method": method if kind == "within_method" else PRIMARY,
                        "regime": "fixed1024" if kind == "arc2_fixed_vs_baseline_allpaid" else "allpaid28819"}
                right = {"method": method,
                         "regime": "fixed1024" if kind == "within_method" else "allpaid28819"}
                result.append({"id": f"{pair}__{kind}__{method}", "kind": kind, "pair": pair,
                               "left": left, "right": right, "familywise": True})
    return result


def source_specifications(lock):
    spec = lock["scoring"]
    if set(spec["datasets"]) != {DATASET}:
        raise ValueError("B1-P accepts only previously inspected FiQA DEV")
    source = spec["datasets"][DATASET]
    if (source.get("format") != "tsv" or not source.get("path")
            or "url" in source or "implicit_binary_grade" in source
            or source.get("sha256") != QREL_SHA256):
        raise ValueError("Require the historical hash-locked explicit-grade FiQA DEV TSV")
    if (type(spec["bootstrap_draws"]) is not int or spec["bootstrap_draws"] != BOOTSTRAP_DRAWS
            or type(spec["bootstrap_seed"]) is not int or spec["bootstrap_seed"] != BOOTSTRAP_SEED
            or spec["contrasts"] != expected_contrasts() or spec["familywise"] != FAMILY):
        raise ValueError("Require the complete ordered 32-contrast B1-P Bonferroni family")
    forbidden = ("margin", "noninferiority", "equivalence", "method_selection")
    if any(any(token in name.lower() for token in forbidden) for name in spec):
        raise ValueError("No margin, equivalence test or method selection is authorized")
    return spec


def verify_sources(lock):
    sources = lock.get("source_sha256_canonical_lf", {})
    if not {"ops/b1p_score.py", "ops/b1m_score.py"}.issubset(sources):
        raise ValueError("The lock must hash both the B1-P scorer and imported metric implementation")
    for relative, digest in sources.items():
        path = inside(ROOT, relative)
        observed = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        if observed != digest:
            raise ValueError(f"Locked source changed: {relative}")


def verify_seal(run, expected_sha):
    if sha(run / "ranking_seal.json") != expected_sha:
        raise ValueError("Ranking seal changed")
    seal = read_json(run / "ranking_seal.json")
    if seal.get("status") != "RANKINGS_SEALED":
        raise ValueError("Ranking seal does not declare RANKINGS_SEALED")
    expected = {(DATASET, pair, method, regime, seed, "50pct")
                for pair, method, regime, seed in itertools.product(PAIRS, METHODS, REGIMES, SEEDS)}
    expected.update((DATASET, pair, method, "reference", None, "full")
                    for pair in PAIRS for method in ("full_x", "full_y"))
    cells = seal["cells"]
    actual = [key(cell) for cell in cells]
    if len(actual) != 124 or len(set(actual)) != 124 or set(actual) != expected:
        raise ValueError("Require exactly 120 matched FiQA partial rankings and four full references")
    for cell in cells:
        if cell["seed"] is not None and type(cell["seed"]) is not int:
            raise ValueError("Mapping seeds must be integers")
    inputs = seal["inputs"]
    if not isinstance(inputs, dict) or "inputs/ids.json" not in inputs:
        raise ValueError("FiQA input IDs must be sealed")
    for relative, digest in inputs.items():
        if "qrel" in relative.lower():
            raise ValueError("Label files cannot enter the pre-access input seal")
        if sha(inside(run, relative)) != digest:
            raise ValueError(f"Sealed input changed: {relative}")
    ids = read_json(run / "inputs" / "ids.json")
    docs, queries = ids["doc_ids"], ids["query_ids"]
    if (len(docs) != 57638 or len(queries) != 500
            or any(not isinstance(value, str) or not value for value in docs + queries)
            or len(set(docs)) != len(docs) or len(set(queries)) != len(queries)):
        raise ValueError("Require unique original string IDs for 57,638 documents and 500 DEV queries")
    seen = set()
    for cell in cells:
        path = inside(run, cell["ranking_path"])
        if path in seen:
            raise ValueError("Each ranking cell requires a unique artifact")
        seen.add(path)
        if sha(path) != cell["ranking_sha256"]:
            raise ValueError(f"Ranking changed: {cell['ranking_path']}")
        ranks = np.load(path, allow_pickle=False)
        if ranks.shape != (500, 100) or ranks.dtype.kind not in "iu":
            raise ValueError(f"Require integer ordered top-100 ranks: {path}")
        if np.any(ranks < 0) or np.any(ranks >= len(docs)):
            raise ValueError(f"Ranking index outside original corpus: {path}")
        if np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0):
            raise ValueError(f"Duplicate document within ranking row: {path}")
    return seal, (docs, queries)


def verify_context(run, lock_sha, expected_meta=None):
    meta = read_json(run / "metadata.json")
    fields = ("status", "code_commit", "lock_sha256", "ranking_seal_sha256")
    bound = {field: meta[field] for field in fields}
    if bound["status"] != "RANKINGS_SEALED" or bound["lock_sha256"] != lock_sha:
        raise ValueError("Run is not sealed under this immutable lock")
    if expected_meta is not None and bound != expected_meta:
        raise ValueError("Run context changed during scoring")
    return bound


def save_npy(path, values):
    with path.open("xb") as stream:
        np.save(stream, values, allow_pickle=False)
        stream.flush()
        os.fsync(stream.fileno())


def verify_dev_transport(lock):
    spec=lock.get('dev_label_transport')
    if not spec:return None
    intent=read_json(Path(spec['intent_path']));verified=read_json(Path(spec['receipt_path']))
    if (intent['expected_sha256']!=QREL_SHA256 or intent['protocol']!=spec['protocol']
            or verified['status']!='DEV_LABEL_TRANSPORT_VERIFIED'
            or verified['sha256']!=QREL_SHA256
            or verified['destination']!=lock['scoring']['datasets'][DATASET]['path']
            or verified['intent_sha256']!=sha(Path(spec['intent_path']))
            or verified['judgments_parsed'] or verified['metrics_computed']):
        raise ValueError('Previously inspected DEV label transport receipt mismatch')
    return {'intent':intent,'verified':verified,'scope':'opaque prior DEV transport; first scorer parse follows verified124-cell seal'}


def load_fiqa_qrels(source, out, ids, transport=None):
    # This durable receipt precedes hashing, statting or opening the label path.
    write_json(out / "qrel_access_FiQA.json", {
        "dataset": DATASET, ("first_scorer_qrel_parse" if transport else "first_current_attempt_qrel_open"): now(),
        "access_scope": "first scorer parse/metric access; prior opaque DEV transport recorded" if transport else "first current-attempt qrel access",
        "prior_dev_label_transport": transport,
        "first_access_receipt": "first_dev_qrel_open.json", "expected_source": source,
        "exposure": EXPOSURE})
    path = Path(source["path"])
    digest = sha(path)
    size = path.stat().st_size
    if digest != source["sha256"] or ("bytes" in source and size != source["bytes"]):
        raise ValueError("FiQA DEV qrel source hash/byte mismatch")
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        qrels, columns = parse_qrel_rows(list(reader), reader.fieldnames, "tsv")
    docs, queries = ids
    doc_set = set(docs)
    stats = {"dataset": DATASET, "sha256": digest, "bytes": size, "columns": columns,
             "evaluation_queries": len(queries),
             "queries_without_positive_judgments": sum(not any(v > 0 for v in qrels.get(q, {}).values()) for q in queries),
             "positive_judgments_outside_corpus_retained_in_denominator":
                 sum(v > 0 and doc not in doc_set for q in queries for doc, v in qrels.get(q, {}).items()),
             "qrel_queries_outside_evaluation_set": len(set(qrels) - set(queries))}
    write_json(out / "qrel_verified_FiQA.json", stats)
    return qrels, stats


def interpretation(low, high):
    return "above_zero" if low > 0 else "below_zero" if high < 0 else "unresolved"


def summaries(cells, arrays, spec):
    lookup = {key(cell): arrays[index] for index, cell in enumerate(cells)}

    def partial(pair, method, regime):
        return np.stack([lookup[(DATASET, pair, method, regime, seed, "50pct")] for seed in SEEDS])

    means = []
    for pair in PAIRS:
        full_y = lookup[(DATASET, pair, "full_y", "reference", None, "full")].mean(axis=0)
        for regime, method in itertools.product(REGIMES, METHODS):
            seed_means = partial(pair, method, regime).mean(axis=1)
            row = {"dataset": DATASET, "pair": pair, "method": method, "regime": regime, "budget": "50pct"}
            for j, metric in enumerate(METRICS):
                row[metric] = {**mean_std(seed_means[:, j]), "descriptive": True,
                               "full_y_retention": float(seed_means[:, j].mean() / full_y[j]) if full_y[j] != 0 else None,
                               "delta_from_full_y": float(seed_means[:, j].mean() - full_y[j])}
            means.append(row)
        for method in ("full_x", "full_y"):
            values = lookup[(DATASET, pair, method, "reference", None, "full")].mean(axis=0)
            means.append({"dataset": DATASET, "pair": pair, "method": method, "regime": "reference", "budget": "full",
                          **{metric: {**mean_std([values[j]]), "descriptive": True}
                             for j, metric in enumerate(METRICS)}})
    # The exact same 20,000 x 500 query indices are reused across both pairs,
    # all methods/regimes and metrics. Mapping seeds are averaged first.
    indices = np.random.default_rng(BOOTSTRAP_SEED).integers(0, 500,
              size=(BOOTSTRAP_DRAWS, 500), dtype=np.int32)
    contrasts = []
    tail = (1.0 - FAMILY["family_confidence"]) / (2 * FAMILY["contrasts"])
    for definition in spec["contrasts"]:
        left, right = definition["left"], definition["right"]
        seed_delta = (partial(definition["pair"], **left) - partial(definition["pair"], **right))
        delta = seed_delta.mean(axis=0)
        row = {**definition, "dataset": DATASET, "budget": "50pct"}
        for j, metric in enumerate(METRICS):
            draws = delta[:, j][indices].mean(axis=1)
            low, high = np.quantile(draws, [0.025, 0.975], method="linear")
            value = {"delta": float(delta[:, j].mean()), "ci95": [float(low), float(high)],
                     "descriptive": True, "interval_interpretation": interpretation(low, high),
                     "mapping_seed_variability": mean_std(seed_delta.mean(axis=1)[:, j])}
            if metric == "ndcg10":
                family_low, family_high = np.quantile(draws, [tail, 1 - tail], method="linear")
                value.update(ci_bonferroni_family95=[float(family_low), float(family_high)],
                             per_interval_confidence=FAMILY["per_interval_confidence"],
                             family_interval_interpretation=interpretation(family_low, family_high))
            row[metric] = value
        contrasts.append(row)
    return means, contrasts, hashlib.sha256(indices.tobytes(order="C")).hexdigest()


def markdown(summary):
    lines = ["# B1-P FiQA development results", "", EXPOSURE + ".", "",
             "All 500 queries count; no-positive queries score zero. Graded nDCG@10 uses 2^rel-1 gain; Recall@100 divides by all positive qrels, including documents outside the corpus.", "",
             "Means average queries then five mapping seeds. Seed SD uses ddof=1; ranges and full-Y retention are in JSON. Full references have one deterministic ranking.", "",
             "| Pair | Regime | Method | nDCG@10 mean (seed SD) | Recall@100 mean (seed SD) |",
             "|---|---|---|---:|---:|"]
    for row in summary["means"]:
        values = [f"{row[m]['mean']:.6f}" + (f" ({row[m]['seed_std']:.6f})" if row[m]["seed_std"] is not None else " (reference)") for m in METRICS]
        lines.append(f"| {row['pair']} | {row['regime']} | {row['method']} | {' | '.join(values)} |")
    lines += ["", "All 32 predeclared nDCG contrasts form one Bonferroni family with nominal 95% family coverage: each percentile interval has 99.84375% confidence. Bootstrap coverage is approximate. Nominal 95% nDCG and Recall intervals are descriptive. The 20,000 shared paired query resamples follow five-seed averaging; seeds do not create independent queries.", "",
              "| Pair | Contrast (left minus right) | Delta nDCG [family interval] | Delta Recall [descriptive 95%] |", "|---|---|---:|---:|"]
    for row in summary["contrasts"]:
        label = f"{row['left']['method']} ({row['left']['regime']}) - {row['right']['method']} ({row['right']['regime']})"
        n, r = row["ndcg10"], row["recall100"]
        nlo, nhi = n["ci_bonferroni_family95"]
        rlo, rhi = r["ci95"]
        lines.append(f"| {row['pair']} | {label} | {n['delta']:+.6f} [{nlo:+.6f}, {nhi:+.6f}] | {r['delta']:+.6f} [{rlo:+.6f}, {rhi:+.6f}] |")
    lines += ["", "An interval crossing or touching zero is unresolved. No equivalence/noninferiority margin, method selection, D1 decision or independent claim is made. Full-reference retention is descriptive. STOP after this authorized development report; no automatic B1-G, breadth, TREC or systems run.", ""]
    return "\n".join(lines)


def run_score(lock_path, run, output_dir=None):
    lock_path, run = Path(lock_path).resolve(), Path(run).resolve()
    selected = Path("scoring") if output_dir is None else Path(output_dir)
    out = (selected if selected.is_absolute() else run / selected).resolve()
    if out == run or not out.is_relative_to(run):
        raise ValueError("Require a new scoring directory strictly inside the run")
    out.mkdir(exist_ok=False)
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        receipt = {"stage": "B1-P", "started_utc": now(), "status": "VALIDATING_BEFORE_SCORER_LABEL_ACCESS",
                   "lock_path": str(lock_path), "lock_sha256": sha(lock_path),
                   "scorer_sha256": sha(Path(__file__)), "scorer_code_commit": commit,
                   "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
                   "exposure": EXPOSURE, "failures": []}
        write_json(out / "started.json", receipt)
        lock = read_json(lock_path)
        if lock.get('dev_label_transport'):
            receipt['status']='VALIDATING_BEFORE_SCORER_PARSE_WITH_PRIOR_DEV_TRANSPORT'
            write_json(out / 'started.json',receipt)
        spec = source_specifications(lock)
        verify_sources(lock)
        context = verify_context(run, receipt["lock_sha256"])
        if context["code_commit"] != commit:
            raise ValueError("Rankings and scorer must use the same committed code revision")
        seal_sha = context["ranking_seal_sha256"]
        seal, ids = verify_seal(run, seal_sha)
        checks = synthetic_checks()
        write_json(out / "synthetic_scorer_checks.json", checks)
        transport=verify_dev_transport(lock)
        write_json(out / "first_dev_qrel_open.json", {
            ("first_scorer_dev_qrel_parse" if transport else "first_current_attempt_dev_qrel_open"): now(), "ranking_seal_sha256": seal_sha,
            "prior_dev_label_transport":transport,
            "lock_sha256": receipt["lock_sha256"], "scorer_sha256": receipt["scorer_sha256"],
            "scorer_code_commit": commit, "all_124_rankings_and_ids_verified": True,
            "synthetic_checks": checks, "expected_qrel_sources": spec["datasets"], "exposure": EXPOSURE})
        qrels, qrel_stats = load_fiqa_qrels(spec["datasets"][DATASET], out, ids,transport)
        arrays = []
        cells = []
        for index, cell in enumerate(seal["cells"]):
            path = inside(run, cell["ranking_path"])
            if sha(path) != cell["ranking_sha256"]:
                raise ValueError(f"Ranking changed before scoring: {path}")
            ranks = np.load(path, allow_pickle=False)
            values = metrics_for(ranks, *ids, qrels)
            if values.shape != (500, 2) or not np.isfinite(values).all():
                raise ValueError("Invalid per-query metric array")
            arrays.append(values)
            cells.append({**cell, "per_query_index": index})
        arrays = np.stack(arrays)
        save_npy(out / "per_query.npy", arrays)
        write_json(out / "cell_index.json", {"axes": ["cell", "query", "metric"],
                   "metrics": METRICS, "shape": list(arrays.shape), "query_ids": ids[1], "cells": cells})
        means, contrasts, bootstrap_sha = summaries(cells, arrays, spec)
        # Final validation precedes publication. Arrays/receipts remain durable
        # if any source, ranking, context or qrels changed during this attempt.
        verify_seal(run, seal_sha)
        verify_context(run, receipt["lock_sha256"], context)
        verify_sources(lock)
        if sha(lock_path) != receipt["lock_sha256"] or sha(Path(__file__)) != receipt["scorer_sha256"]:
            raise ValueError("Lock/scorer changed during scoring")
        if sha(Path(spec["datasets"][DATASET]["path"])) != QREL_SHA256:
            raise ValueError("FiQA DEV qrels changed during scoring")
        summary = {"status": "DEV_SCORED", "stage": "B1-P", "completed_utc": now(),
                   "ranking_cells": 124, "ranking_seal_sha256": seal_sha,
                   "lock_sha256": receipt["lock_sha256"], "scorer_sha256": receipt["scorer_sha256"],
                   "scorer_code_commit": commit, "scoring": spec, "exposure": EXPOSURE,
                   "interpretation": "DEV only; 32-contrast nDCG Bonferroni family; nominal95 and Recall descriptive; no method selection or independent/D1 claim",
                   "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": BOOTSTRAP_SEED,
                       "rng": "numpy default_rng(20261026), PCG64", "indices_shape": [20000, 500],
                       "indices_dtype": "int32", "indices_sha256_c_order": bootstrap_sha,
                       "resampling": "500 queries with replacement; average five seeds before resampling; identical indices across all conditions and metrics",
                       "familywise": FAMILY, "coverage": "approximate percentile bootstrap"},
                   "qrel_stats": qrel_stats, "means": means, "contrasts": contrasts,
                   "failures": [], "next_action": "STOP; report authorized B1-P development results"}
        write_json(out / "results_summary.json", summary)
        with (out / "results_summary.md").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(markdown(summary))
            stream.flush()
            os.fsync(stream.fileno())
        artifacts = {str(path.relative_to(out)).replace("\\", "/"): sha(path)
                     for path in sorted(out.rglob("*")) if path.is_file()}
        write_json(out / "completed.json", {"status": "DEV_SCORED", "completed_utc": now(),
                   "scorer_code_commit": commit, "summary_sha256": sha(out / "results_summary.json"),
                   "artifact_sha256": artifacts})
        return summary
    except BaseException as error:
        write_json(out / "failure.json", {"status": "FAILED_PRESERVED", "failed_utc": now(),
                   "error": repr(error), "traceback": traceback.format_exc(),
                   "dev_qrel_access_started": (out / "first_dev_qrel_open.json").exists()})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="New directory inside the run; existing attempts are preserved")
    args = parser.parse_args()
    run_score(args.lock, args.run, args.output_dir)
