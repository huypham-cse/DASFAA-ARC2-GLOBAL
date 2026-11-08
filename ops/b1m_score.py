"""One-shot, sealed-ranking DEV scorer for B1-M; never an independent test.

Run only after the ranking runner has sealed the entire 720+16 cell matrix.
All label access is confined to this separate process. No method selection is
performed here. A failed attempt retains its directory and cannot be resumed.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import traceback
import urllib.request

import numpy as np

DATASETS = ("NanoNQ", "NanoHotpotQA", "NanoFEVER", "FiQA")
PAIRS = ("minilm_distilroberta", "e5_small_base")
SEEDS = (17, 29, 41, 53, 67)
BUDGETS = ("25pct", "50pct", "75pct")
PRIMARY = "arc2_global_tangent2_r1"
METHODS = ("procrustes_global", PRIMARY, "tangent1_l10", "tangent2_l1",
           "tangent2_l100", "ridge_affine_l10_bias_regularized")
METRICS = ("ndcg10", "recall100")
BOOTSTRAP_DRAWS = 20000
CONTRASTS = ((PRIMARY, "procrustes_global"), (PRIMARY, "tangent1_l10"),
             (PRIMARY, "ridge_affine_l10_bias_regularized"),
             ("tangent2_l1", PRIMARY), ("tangent2_l100", PRIMARY))


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    """Exclusive creation: receipts and results are never overwritten."""
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        import os
        os.fsync(stream.fileno())


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def inside(run, relative):
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"Expected relative sealed path: {relative}")
    path = (run / rel).resolve()
    if not path.is_relative_to(run):
        raise ValueError(f"Path escaped run: {relative}")
    return path


def key(cell):
    return tuple(cell[name] for name in ("dataset", "pair", "seed", "budget", "method"))


def verify_seal(run, expected_seal_sha):
    if sha(run / "ranking_seal.json") != expected_seal_sha:
        raise ValueError("Ranking seal changed")
    seal = read_json(run / "ranking_seal.json")
    expected = set(itertools.product(DATASETS, PAIRS, SEEDS, BUDGETS, METHODS))
    expected.update((d, p, None, "full", m) for d in DATASETS for p in PAIRS
                    for m in ("full_x", "full_y"))
    cells = seal["cells"]
    actual = [key(cell) for cell in cells]
    if len(actual) != 736 or len(set(actual)) != 736 or set(actual) != expected:
        raise ValueError("Require exactly the complete 720 mechanism cells + 16 refs; DEV only")
    inputs = seal["inputs"]
    if not isinstance(inputs, dict) or not inputs:
        raise ValueError("Seal must hash all input files")
    for dataset in DATASETS:
        if f"inputs/{dataset}/ids.json" not in inputs:
            raise ValueError(f"IDs are not sealed: {dataset}")
    for relative, digest in inputs.items():
        if "qrel" in relative.lower():
            raise ValueError("Qrel files cannot enter the pre-access input seal")
        if sha(inside(run, relative)) != digest:
            raise ValueError(f"Input changed: {relative}")
    seen_paths = set()
    ids = {}
    for dataset in DATASETS:
        data = read_json(run / "inputs" / dataset / "ids.json")
        docs, queries = data["doc_ids"], data["query_ids"]
        if not docs or not queries or any(not isinstance(x, str) or not x for x in docs + queries):
            raise ValueError(f"Invalid string IDs: {dataset}")
        if len(docs) != len(set(docs)) or len(queries) != len(set(queries)):
            raise ValueError(f"Duplicate IDs: {dataset}")
        ids[dataset] = (docs, queries)
    for cell in cells:
        relative = cell["ranking_path"]
        if relative in seen_paths:
            raise ValueError("One unique ranking artifact required per cell")
        seen_paths.add(relative)
        path = inside(run, relative)
        if sha(path) != cell["ranking_sha256"]:
            raise ValueError(f"Ranking changed: {relative}")
        ranks = np.load(path, allow_pickle=False)
        docs, queries = ids[cell["dataset"]]
        if ranks.shape != (len(queries), min(100, len(docs))) or ranks.dtype.kind not in "iu":
            raise ValueError(f"Invalid integer top-100 matrix: {relative}")
        if np.any(ranks < 0) or np.any(ranks >= len(docs)):
            raise ValueError(f"Ranking row outside corpus: {relative}")
        if ranks.shape[1] > 1 and np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0):
            raise ValueError(f"Duplicate returned documents: {relative}")
    return seal, ids


def metrics_for(ranks, docs, queries, qrels):
    """Graded gain 2**rel-1; full positive-qrel Recall denominator.

    Unjudged documents have grade zero. All evaluation queries remain in the
    array; an unjudged query has both metrics zero. Negative labels are treated
    as nonrelevant. The qrel loader rejects nonfinite grades.
    """
    result = np.zeros((len(queries), 2), dtype=np.float64)
    discount = 1.0 / np.log2(np.arange(2, 12, dtype=np.float64))
    for i, query in enumerate(queries):
        positive = {doc: rel for doc, rel in qrels.get(query, {}).items() if rel > 0}
        if not positive:
            continue
        returned = [docs[int(row)] for row in ranks[i, :100]]
        grades = np.array([positive.get(doc, 0.0) for doc in returned[:10]], dtype=np.float64)
        ideal = np.array(sorted(positive.values(), reverse=True)[:10], dtype=np.float64)
        dcg = np.sum(np.expm1(grades * math.log(2.0)) * discount[:len(grades)])
        idcg = np.sum(np.expm1(ideal * math.log(2.0)) * discount[:len(ideal)])
        if not np.isfinite(idcg) or not np.isfinite(dcg):
            raise ValueError("Nonfinite graded DCG")
        result[i, 0] = dcg / idcg
        result[i, 1] = sum(doc in positive for doc in returned) / len(positive)
    return result


def synthetic_checks():
    docs = ["a", "b", "c"]
    queries = ["graded", "zero", "unjudged"]
    ranks = np.array([[1, 0, 2], [0, 1, 2], [0, 1, 2]], dtype=np.int64)
    qrels = {"graded": {"a": 2.0, "b": 1.0, "outside": 1.0}, "zero": {"a": 0.0}}
    actual = metrics_for(ranks, docs, queries, qrels)
    expected_ndcg = (1 + 3 / math.log2(3)) / (3 + 1 / math.log2(3) + 1 / 2)
    np.testing.assert_allclose(actual[0], [expected_ndcg, 2 / 3], rtol=0, atol=1e-14)
    np.testing.assert_array_equal(actual[1:], np.zeros((2, 2)))
    # Serialization preserves the selected tie order; no score-based resorting.
    import io
    stream = io.BytesIO()
    np.save(stream, ranks, allow_pickle=False)
    stream.seek(0)
    np.testing.assert_array_equal(np.load(stream, allow_pickle=False), ranks)
    ideal = metrics_for(np.array([[0, 1, 2]]), docs, ["q"], {"q": {"a": 2, "b": 1}})
    np.testing.assert_allclose(ideal, [[1, 1]], rtol=0, atol=1e-14)
    binary_rows = [{"query-id": "binary", "corpus-id": "a"},
                   {"query-id": "binary", "corpus-id": "outside"}]
    binary_qrels, binary_columns = parse_qrel_rows(
        binary_rows, ["query-id", "corpus-id"], "parquet", implicit_binary_grade=1)
    assert binary_qrels == {"binary": {"a": 1.0, "outside": 1.0}}
    binary_metrics = metrics_for(np.array([[1, 0, 2], [0, 1, 2]]), docs,
                                 ["binary", "unjudged"], binary_qrels)
    expected_binary_ndcg = (1 / math.log2(3)) / (1 + 1 / math.log2(3))
    np.testing.assert_allclose(binary_metrics[0], [expected_binary_ndcg, 0.5], rtol=0, atol=1e-14)
    np.testing.assert_array_equal(binary_metrics[1], [0, 0])
    # Identical two-column data must fail without the explicit locked opt-in,
    # and the parquet-only repair must never reinterpret a two-column TSV.
    for format_name, implicit in (("parquet", None), ("tsv", 1)):
        try:
            parse_qrel_rows(binary_rows, binary_columns, format_name, implicit)
        except ValueError:
            pass
        else:
            raise AssertionError("Implicit binary labels accepted outside the locked parquet format")
    return {"status": "PASS", "graded_ndcg": float(actual[0, 0]),
            "full_qrel_denominator_recall": float(actual[0, 1]),
            "zero_and_unjudged_queries": "zero", "serialized_order": "unchanged",
            "implicit_binary_parser": {"status": "PASS", "ndcg10": float(binary_metrics[0, 0]),
                                       "recall100": float(binary_metrics[0, 1]),
                                       "unlisted_pairs": 0, "requires_explicit_parquet_opt_in": True}}


def source_specifications(lock):
    spec = lock["scoring"]
    if set(spec["datasets"]) != set(DATASETS):
        raise ValueError("Only four named DEV collections are allowed; no TREC/test collection")
    if (spec["bootstrap_draws"] != BOOTSTRAP_DRAWS or spec["bootstrap_seed"] != 20261026
            or spec["familywise"] is not False or "quality_margin" in spec):
        raise ValueError("Uncertainty lock differs from B1-M; no quality margin is justified")
    if spec["contrasts"] != [list(pair) for pair in CONTRASTS]:
        raise ValueError("The five contrast directions/order must be locked before labels")
    if spec["aggregate_familywise"] != {
            "scope": "overall_equal_24_strata", "contrasts": 5,
            "family_confidence": 0.95, "per_interval_confidence": 0.99,
            "method": "bonferroni_percentile"}:
        raise ValueError("Require the locked five-contrast overall aggregate family")
    for dataset, source in spec["datasets"].items():
        expected_format = "tsv" if dataset == "FiQA" else "parquet"
        if source["format"] != expected_format:
            raise ValueError(f"Unexpected qrel format: {dataset}")
        if "implicit_binary_grade" in source and (
                dataset == "FiQA" or source["format"] != "parquet"
                or type(source["implicit_binary_grade"]) is not int
                or source["implicit_binary_grade"] != 1):
            raise ValueError("Implicit grade=1 is supported only for locked Nano parquet positive pairs")
        if len(source["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in source["sha256"]):
            raise ValueError(f"Qrels must have a predeclared SHA256: {dataset}")
        if dataset == "FiQA":
            if not source.get("path") or "url" in source:
                raise ValueError("FiQA must use the locked existing DEV TSV")
        elif not source.get("url", "").startswith("https://") or not isinstance(source.get("bytes"), int):
            raise ValueError("Nano qrels require pinned HTTPS source, bytes and SHA256")
    return spec


def qrel_rows(path, format_name, implicit_binary_grade=None):
    if format_name == "parquet":
        import pyarrow.parquet as pq
        table = pq.read_table(path)
        columns = table.column_names
        rows = table.to_pylist()
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            columns = reader.fieldnames
            rows = list(reader)
    return parse_qrel_rows(rows, columns, format_name, implicit_binary_grade)


def parse_qrel_rows(rows, columns, format_name, implicit_binary_grade=None):
    """Parse explicit grades, or the opt-in published Nano positive-pair format.

    With the locked parquet opt-in, each listed pair has grade 1. Unlisted
    pairs stay absent and therefore receive grade zero in metrics_for.
    """
    binary = (format_name == "parquet" and type(implicit_binary_grade) is int
              and implicit_binary_grade == 1
              and set(columns or ()) == {"query-id", "corpus-id"})
    choices = (("query-id", "corpus-id", "score"), ("query_id", "corpus_id", "score"),
               ("query-id", "corpus-id", "relevance"), ("query_id", "corpus_id", "relevance"),
               ("query_id", "doc_id", "relevance"))
    matching = [choice for choice in choices if set(columns or ()) == set(choice)]
    if not binary and len(matching) != 1:
        raise ValueError(f"Unknown/ambiguous explicit qrel columns: {columns}")
    qcol, dcol, rcol = ("query-id", "corpus-id", None) if binary else matching[0]
    qrels = {}
    for row in rows:
        query, doc = str(row[qcol]), str(row[dcol])
        rel = 1.0 if binary else float(row[rcol])
        if not query or not doc or query == "None" or doc == "None" or not math.isfinite(rel):
            raise ValueError("Invalid qrel ID or grade")
        if doc in qrels.setdefault(query, {}):
            raise ValueError(f"Duplicate qrel pair: {query}/{doc}")
        qrels[query][doc] = rel
    return qrels, (qcol, dcol) if binary else matching[0]


def load_qrels(dataset, source, out, ids, first_access):
    # This receipt is durable and exclusively created before any label source
    # is opened, hashed, or requested over the network. Expected hashes come
    # from the pre-run lock; observed hashes are written separately afterward.
    write_json(out / f"qrel_access_{dataset}.json", {
        "dataset": dataset, "first_dev_qrel_open": now(), "first_access_receipt": first_access,
        "expected_source": source, "exposure": "DEV, not independent confirmation"})
    if "url" in source:
        path = out / f"qrels_{dataset}.parquet"
        with urllib.request.urlopen(source["url"]) as response, path.open("xb") as stream:
            import shutil
            shutil.copyfileobj(response, stream)
    else:
        path = Path(source["path"])
    digest, size = sha(path), path.stat().st_size
    if digest != source["sha256"] or ("bytes" in source and size != source["bytes"]):
        raise ValueError(f"Qrel source hash/byte mismatch: {dataset}")
    qrels, columns = qrel_rows(path, source["format"], source.get("implicit_binary_grade"))
    docs, queries = ids
    doc_set = set(docs)
    stats = {"dataset": dataset, "sha256": digest, "bytes": size, "columns": columns,
             "implicit_binary_grade": source.get("implicit_binary_grade"),
             "evaluation_queries": len(queries),
             "queries_without_positive_judgments": sum(not any(v > 0 for v in qrels.get(q, {}).values()) for q in queries),
             "positive_judgments_outside_corpus_retained_in_denominator":
                 sum(v > 0 and d not in doc_set for q in queries for d, v in qrels.get(q, {}).items()),
             "qrel_queries_outside_evaluation_set": len(set(qrels) - set(queries))}
    write_json(out / f"qrel_verified_{dataset}.json", stats)
    return qrels, stats


def mean_std(values):
    return {"mean": float(np.mean(values)),
            "seed_std": float(np.std(values, ddof=1)) if len(values) > 1 else None,
            "seed_range": [float(np.min(values)), float(np.max(values))] if len(values) > 1 else None,
            "seeds": len(values)}


def interval(delta, indices):
    samples = delta[indices].mean(axis=1)
    low, high = np.quantile(samples, [0.025, 0.975], method="linear")
    return {"delta": float(delta.mean()), "ci95": [float(low), float(high)],
            "interval_interpretation": "above_zero" if low > 0 else "below_zero" if high < 0 else "unresolved"}


def summaries(cells, arrays, ids):
    lookup = {key(cell): arrays[cell["dataset"]][index]
              for cell in cells for index in [cell["per_dataset_index"]]}
    rows = []
    for dataset in DATASETS:
        for pair in PAIRS:
            for budget, method in itertools.product(BUDGETS, METHODS):
                means = np.array([lookup[(dataset, pair, seed, budget, method)].mean(axis=0) for seed in SEEDS])
                rows.append({"dataset": dataset, "pair": pair, "budget": budget, "method": method,
                             **{metric: mean_std(means[:, j]) for j, metric in enumerate(METRICS)}})
            for method in ("full_x", "full_y"):
                mean = lookup[(dataset, pair, None, "full", method)].mean(axis=0)
                rows.append({"dataset": dataset, "pair": pair, "budget": "full", "method": method,
                             **{metric: mean_std([mean[j]]) for j, metric in enumerate(METRICS)}})
    # Each dataset gets one RNG stream; the same sampled query indices are
    # reused for every method, seed-averaged contrast, budget and encoder.
    children = np.random.SeedSequence(20261026).spawn(len(DATASETS))
    indices = {dataset: np.random.default_rng(child).integers(0, len(ids[dataset][1]),
               size=(BOOTSTRAP_DRAWS, len(ids[dataset][1])), dtype=np.int32)
               for dataset, child in zip(DATASETS, children)}
    contrasts = []
    differences, draws_by_stratum, seed_means = {}, {}, {}
    for dataset, pair, budget, (left, right) in itertools.product(DATASETS, PAIRS, BUDGETS, CONTRASTS):
        seed_deltas = np.stack([lookup[(dataset, pair, seed, budget, left)] -
                               lookup[(dataset, pair, seed, budget, right)] for seed in SEEDS])
        delta = seed_deltas.mean(axis=0)
        stratum = (dataset, pair, budget, left, right)
        differences[stratum] = delta
        draws_by_stratum[stratum] = np.stack([delta[:, j][indices[dataset]].mean(axis=1) for j in range(2)], axis=1)
        seed_means[stratum] = seed_deltas.mean(axis=1)
        contrasts.append({"dataset": dataset, "pair": pair, "budget": budget,
                          "left": left, "right": right,
                          **{metric: {**interval(delta[:, j], indices[dataset]),
                             "mapping_seed_variability": mean_std(seed_means[stratum][:, j])}
                             for j, metric in enumerate(METRICS)}})
    encoder_macro, overall_macro = [], []
    for scope_pairs, scope in [(PAIRS, "overall"), *[((pair,), pair) for pair in PAIRS]]:
        for left, right in CONTRASTS:
            strata = [(d, p, b, left, right) for d in DATASETS for p in scope_pairs for b in BUDGETS]
            draws = np.mean([draws_by_stratum[s] for s in strata], axis=0)
            seeds = np.mean([seed_means[s] for s in strata], axis=0)
            entry = {"scope": scope, "left": left, "right": right, "strata": len(strata),
                     "aggregation": f"equal weight over {len(strata)} dataset/pair/budget strata; within dataset equal queries; five-seed average"}
            for j, metric in enumerate(METRICS):
                low, high = np.quantile(draws[:, j], [0.025, 0.975], method="linear")
                entry[metric] = {"delta": float(np.mean([differences[s][:, j].mean() for s in strata])),
                                 "ci95": [float(low), float(high)], "descriptive": True,
                                 "interval_interpretation": "above_zero" if low > 0 else "below_zero" if high < 0 else "unresolved",
                                 "mapping_seed_variability": mean_std(seeds[:, j])}
                if scope == "overall" and metric == "ndcg10":
                    # Only these five locked overall-primary-metric contrasts
                    # belong to the Bonferroni family; Recall stays descriptive.
                    low99, high99 = np.quantile(draws[:, j], [0.005, 0.995], method="linear")
                    entry[metric]["ci99_bonferroni_family95"] = [float(low99), float(high99)]
                    entry[metric]["family_interval_interpretation"] = "above_zero" if low99 > 0 else "below_zero" if high99 < 0 else "unresolved"
            (overall_macro if scope == "overall" else encoder_macro).append(entry)
    return rows, contrasts, encoder_macro, overall_macro


def markdown(summary):
    lines = ["# B1-M development mechanism results", "",
             "Development evidence only, including previously inspected FiQA. The fixed proposed method remains two tangent steps, lambda=10.", "",
             "All evaluation queries count; no-positive-judgment queries receive zero. nDCG@10 uses graded 2^rel−1 gain; Recall@100 divides by all positive qrels.", "",
             "Means average queries then five seeds; seed SD is sample SD (ddof=1). Full references have one deterministic ranking.", "",
             "| Dataset | Pair | Budget | Method | nDCG@10 mean ± seed SD | Recall@100 mean ± seed SD |",
             "|---|---|---|---|---:|---:|"]
    for row in summary["means"]:
        values = []
        for metric in METRICS:
            value = row[metric]
            values.append(f"{value['mean']:.6f}" + (f" ± {value['seed_std']:.6f}" if value['seed_std'] is not None else " (reference)"))
        lines.append(f"| {row['dataset']} | {row['pair']} | {row['budget']} | {row['method']} | {' | '.join(values)} |")
    lines += ["", "Paired nominal 95% intervals use 20,000 query bootstrap draws after five-seed averaging. The same indices are reused within a dataset for every method, encoder and budget. These intervals are descriptive and marginal; an interval touching/crossing zero is unresolved, never equivalence. Mapping-seed SD/range are separate in JSON and do not create independent queries.", "",
              "| Dataset / aggregate | Pair | Budget | Contrast (left − right) | Δ nDCG@10 [95% CI] | Δ Recall@100 [95% CI] |", "|---|---|---|---|---:|---:|"]
    for row in summary["contrasts"] + summary["per_encoder_macro"] + summary["overall_macro"]:
        values = [f"{row[m]['delta']:+.6f} [{row[m]['ci95'][0]:+.6f}, {row[m]['ci95'][1]:+.6f}]" for m in METRICS]
        lines.append(f"| {row.get('dataset', row.get('scope'))} | {row.get('pair', row.get('scope'))} | {row.get('budget', 'equal-stratum macro')} | {row['left']} − {row['right']} | {' | '.join(values)} |")
    lines += ["", "Only the five predeclared overall 24-stratum nDCG contrasts form a family. Their 99% percentile intervals use Bonferroni allocation for nominal 95% family coverage. They remain DEV estimates; percentile-bootstrap coverage is approximate. Per-encoder and Recall intervals are outside this family.", "",
              "| Overall contrast | Δ nDCG@10 [99% interval, five-contrast family] |", "|---|---:|"]
    for row in summary["overall_macro"]:
        value = row["ndcg10"]
        low, high = value["ci99_bonferroni_family95"]
        lines.append(f"| {row['left']} − {row['right']} | {value['delta']:+.6f} [{low:+.6f}, {high:+.6f}] |")
    lines += ["", "No scientifically justified quality/noninferiority margin is declared. This report performs no equivalence test, method selection or automatic next-stage admission. B1-P/B1-G remain necessary for the later development decision.", ""]
    return "\n".join(lines)


def verify_run_context(run, meta, lock_sha, context):
    if context is None:
        if meta["status"] != "RANKINGS_SEALED" or meta["lock_sha256"] != lock_sha:
            raise ValueError("Run is not sealed under this immutable lock")
        return meta["ranking_seal_sha256"]
    required = {"original_lock_sha256", "ranking_seal_sha256", "original_code_commit",
                "prior_failure_sha256", "prior_failure_path", "prior_first_access_sha256"}
    if not isinstance(context, dict) or set(context) != required:
        raise ValueError("Repair context must contain exactly the declared provenance fields")
    if (meta["status"] != "FAILED_PRESERVED"
            or meta["lock_sha256"] != context["original_lock_sha256"]
            or meta["code_commit"] != context["original_code_commit"]
            or meta["ranking_seal_sha256"] != context["ranking_seal_sha256"]):
        raise ValueError("Repair context does not bind the failed original run/lock/code/seal")
    if lock_sha == context["original_lock_sha256"]:
        raise ValueError("Format repair requires a separately committed new scoring lock")
    if context["prior_failure_path"] != "scoring/failure.json":
        raise ValueError("Repair must preserve the original scoring/failure.json")
    failure_path = inside(run, context["prior_failure_path"])
    first_path = run / "scoring" / "first_dev_qrel_open.json"
    if (sha(failure_path) != context["prior_failure_sha256"]
            or sha(first_path) != context["prior_first_access_sha256"]):
        raise ValueError("Original failure/first-access evidence changed")
    failure, first = read_json(failure_path), read_json(first_path)
    if (failure["status"] != "FAILED_PRESERVED"
            or failure["dev_qrel_access_started"] is not True
            or first["lock_sha256"] != context["original_lock_sha256"]
            or first["ranking_seal_sha256"] != context["ranking_seal_sha256"]):
        raise ValueError("Prior failure/access receipts do not bind the original exposed DEV scoring")
    return context["ranking_seal_sha256"]


def run_score(lock_path, run, output_dir=None):
    lock_path, run = lock_path.resolve(), run.resolve()
    selected = Path("scoring") if output_dir is None else Path(output_dir)
    out = (selected if selected.is_absolute() else run / selected).resolve()
    if out == run or not out.is_relative_to(run):
        raise ValueError("Scoring output must be a new directory strictly within the run")
    out.mkdir(exist_ok=False)
    lock = read_json(lock_path)
    context = lock.get("rescore_context")
    scorer_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=Path(__file__).resolve().parents[1], text=True).strip()
    receipt = {"started_utc": now(), "status": "VALIDATING_WITH_LABELS_CLOSED",
               "lock_path": str(lock_path), "lock_sha256": sha(lock_path),
               "scorer_sha256": sha(Path(__file__)), "python": sys.version,
               "scorer_code_commit": scorer_commit, "rescore_context": context,
               "numpy": np.__version__, "platform": platform.platform(),
               "exposure": "DEV only; FiQA previously inspected", "failures": []}
    if context is not None:
        receipt["status"] = "VALIDATING_FORMAT_REPAIR_AFTER_PRIOR_DEV_ACCESS"
    write_json(out / "started.json", receipt)
    try:
        spec = source_specifications(lock)
        for relative, digest in lock.get("source_sha256_canonical_lf", {}).items():
            path = Path(__file__).resolve().parents[1] / relative
            actual = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            if actual != digest:
                raise ValueError(f"Locked source changed: {relative}")
        meta = read_json(run / "metadata.json")
        seal_sha = verify_run_context(run, meta, receipt["lock_sha256"], context)
        seal, ids = verify_seal(run, seal_sha)
        checks = synthetic_checks()
        write_json(out / "synthetic_scorer_checks.json", checks)
        first_access = {"first_dev_qrel_open": now(), "ranking_seal_sha256": seal_sha,
                        "lock_sha256": receipt["lock_sha256"], "scorer_sha256": receipt["scorer_sha256"],
                        "scorer_code_commit": scorer_commit, "rescore_context": context,
                        "all_736_rankings_and_ids_verified": True, "synthetic_checks": checks,
                        "expected_qrel_sources": spec["datasets"], "exposure": "DEV only"}
        if context is not None:
            first_access["access_scope"] = "First label access in this repair attempt; original DEV access is preserved in rescore_context"
        write_json(out / "first_dev_qrel_open.json", first_access)
        arrays, cells, qrel_stats = {}, [], []
        for dataset in DATASETS:
            qrels, stats = load_qrels(dataset, spec["datasets"][dataset], out, ids[dataset], "first_dev_qrel_open.json")
            qrel_stats.append(stats)
            dataset_cells = [cell for cell in seal["cells"] if cell["dataset"] == dataset]
            values = []
            for index, cell in enumerate(dataset_cells):
                ranking = np.load(inside(run, cell["ranking_path"]), allow_pickle=False)
                values.append(metrics_for(ranking, *ids[dataset], qrels))
                cells.append({**cell, "per_dataset_index": index})
            arrays[dataset] = np.stack(values)
            directory = out / dataset
            directory.mkdir(exist_ok=False)
            np.save(directory / "per_query.npy", arrays[dataset], allow_pickle=False)
            write_json(directory / "cell_index.json", {"axes": ["cell", "query", "metric"],
                       "metrics": METRICS, "query_ids": ids[dataset][1], "cells": cells[-len(dataset_cells):]})
        rows, contrasts, encoder_macro, overall_macro = summaries(cells, arrays, ids)
        # Re-hash every ranking and input, plus the protocol and source qrels,
        # before publishing any final results. Partial arrays survive failures.
        verify_seal(run, seal_sha)
        verify_run_context(run, read_json(run / "metadata.json"), receipt["lock_sha256"], context)
        if sha(lock_path) != receipt["lock_sha256"] or sha(Path(__file__)) != receipt["scorer_sha256"]:
            raise ValueError("Lock/scorer changed during scoring")
        for dataset in DATASETS:
            source = spec["datasets"][dataset]
            path = out / f"qrels_{dataset}.parquet" if "url" in source else Path(source["path"])
            if sha(path) != source["sha256"]:
                raise ValueError(f"Qrels changed during scoring: {dataset}")
        summary = {"status": "DEV_SCORED", "completed_utc": now(), "ranking_cells": len(cells),
                   "ranking_seal_sha256": seal_sha, "lock_sha256": receipt["lock_sha256"],
                   "scorer_code_commit": scorer_commit, "rescore_context": context,
                   "scorer_sha256": receipt["scorer_sha256"], "scoring": spec,
                   "interpretation": "DEV only; nominal marginal descriptive CIs; five overall nDCG contrasts have locked Bonferroni family intervals; no independent confirmation or method selection",
                   "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": 20261026, "rng": "numpy SeedSequence.spawn(4), datasets in DATASETS order; PCG64",
                                 "resampling": "queries within datasets, all five seeds averaged first; same indices for every condition", "familywise": False},
                   "qrel_stats": qrel_stats, "means": rows, "contrasts": contrasts,
                   "per_encoder_macro": encoder_macro, "overall_macro": overall_macro, "failures": []}
        write_json(out / "results_summary.json", summary)
        with (out / "results_summary.md").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(markdown(summary))
        artifacts = {str(path.relative_to(out)).replace("\\", "/"): sha(path)
                     for path in sorted(out.rglob("*")) if path.is_file()}
        write_json(out / "completed.json", {"status": "DEV_SCORED", "completed_utc": now(),
                   "scorer_code_commit": scorer_commit, "rescore_context": context,
                   "summary_sha256": sha(out / "results_summary.json"),
                   "markdown_sha256": sha(out / "results_summary.md"),
                   "artifact_sha256": artifacts})
    except BaseException as error:
        write_json(out / "failure.json", {"status": "FAILED_PRESERVED", "failed_utc": now(),
                   "error": repr(error), "traceback": traceback.format_exc(),
                   "dev_qrel_access_started": (out / "first_dev_qrel_open.json").exists()})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", required=True, type=Path)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="New output directory within run (default: scoring); existing attempts are preserved")
    args = parser.parse_args()
    run_score(args.lock, args.run, args.output_dir)
