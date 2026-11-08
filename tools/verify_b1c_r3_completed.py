"""Verify the completed B1c-R3 compact DEV bundle without fitting or retrieval.

Metrics and qrel parsing are independent of the scientific scorer. Summary and
20,000-draw bootstrap recomputation deliberately reuse its locked summarizer.
Only a uniquely named QA JSON is written; scientific artifacts are read-only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ops import b1c_r3_score as locked


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inside(root, relative):
    require(isinstance(relative, str) and "trec" not in relative.lower(),
            "Only the locked four DEV datasets may be accessed")
    result = (root / relative).resolve()
    require(result.is_relative_to(root) and result != root, "Path escapes compact bundle")
    return result


def independent_qrels(path, dataset, source):
    """Read the exact locked DEV formats, rejecting duplicate judgments."""
    if dataset == "FiQA":
        require(source["format"] == "tsv", "FiQA format changed")
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            columns, rows = reader.fieldnames, list(reader)
        variants = (("query-id", "corpus-id", "score"),
                    ("query_id", "corpus_id", "score"),
                    ("query-id", "corpus-id", "relevance"),
                    ("query_id", "corpus_id", "relevance"),
                    ("query_id", "doc_id", "relevance"))
        matching = [names for names in variants if set(columns or ()) == set(names)]
        require(len(matching) == 1, "Unexpected explicit DEV TSV columns")
        qcol, dcol, grade_col = matching[0]
        used_columns = list(matching[0])
    else:
        require(dataset in ("NanoNQ", "NanoHotpotQA", "NanoFEVER")
                and source["format"] == "parquet"
                and source.get("implicit_binary_grade") == 1,
                "Require the locked Nano positive-pair format")
        import pyarrow.parquet as pq
        table = pq.read_table(path)
        require(set(table.column_names) == {"query-id", "corpus-id"},
                "Unexpected Nano qrel columns")
        rows = table.to_pylist()
        qcol, dcol, grade_col = "query-id", "corpus-id", None
        used_columns = [qcol, dcol]
    judgments = {}
    for row in rows:
        query, document = str(row[qcol]), str(row[dcol])
        grade = 1.0 if grade_col is None else float(row[grade_col])
        require(query and document and query != "None" and document != "None"
                and math.isfinite(grade), "Invalid DEV judgment")
        per_query = judgments.setdefault(query, {})
        require(document not in per_query, "Duplicate DEV judgment")
        per_query[document] = grade
    return judgments, used_columns


def independent_metrics(ranks, documents, queries, judgments):
    """Standard graded nDCG@10 and Recall@100, retaining all positive qrels."""
    result = np.zeros((len(queries), 2), dtype=np.float64)
    for row, query in enumerate(queries):
        relevant = {document: grade for document, grade in judgments.get(query, {}).items()
                    if grade > 0}
        if not relevant:
            continue
        returned = [documents[int(index)] for index in ranks[row, :100]]
        ideal = sorted(relevant.values(), reverse=True)[:10]
        denominator = math.fsum((2.0 ** grade - 1.0) / math.log2(position + 2)
                                for position, grade in enumerate(ideal))
        numerator = math.fsum((2.0 ** relevant.get(document, 0.0) - 1.0)
                              / math.log2(position + 2)
                              for position, document in enumerate(returned[:10]))
        require(math.isfinite(numerator) and math.isfinite(denominator), "Nonfinite DCG")
        result[row] = numerator / denominator, len(set(returned) & relevant.keys()) / len(relevant)
    return result


def verify(bundle, qa):
    started = time.perf_counter()
    bundle, qa = Path(bundle).resolve(), Path(qa).resolve()
    review = ROOT / "results/b1c_r3_review_20261031"
    require(bundle.is_relative_to(review.resolve()), "Require the authorized R3 review bundle")
    require(qa.is_relative_to(review.resolve()) and not qa.is_relative_to(bundle)
            and qa.suffix == ".json" and not qa.exists(), "Require a new QA JSON outside evidence")
    manifest_path = bundle / "bundle_manifest.json"
    manifest = read(manifest_path)
    files = manifest["files"]
    require(isinstance(files, dict) and files, "Missing compact manifest")
    remote_to_local = {}
    byte_count = 0
    for relative, spec in files.items():
        path = inside(bundle, relative)
        require(path.is_file() and path.stat().st_size == spec["bytes"]
                and sha(path) == spec["sha256"], "Compact hash/size mismatch: " + relative)
        remote_to_local.setdefault(spec["path"], []).append(path)
        byte_count += spec["bytes"]
    actual_files = {p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()}
    require(actual_files == set(files) | {"bundle_manifest.json"}, "Compact file population mismatch")
    print(f"Compact manifest verified: {len(files)} files, {byte_count} bytes", flush=True)

    scoring = bundle / "run/scoring"
    completed, summary = read(scoring / "completed.json"), read(scoring / "summary.json")
    require(completed["status"] == summary["status"] == "DEV_SCORED", "Scoring not complete")
    require(completed["summary_sha256"] == sha(scoring / "summary.json"), "Summary completion hash mismatch")
    artifacts = completed["artifact_sha256"]
    actual_scoring = {p.relative_to(scoring).as_posix() for p in scoring.rglob("*") if p.is_file()}
    require(actual_scoring == set(artifacts) | {"completed.json"}, "Scorer artifact population mismatch")
    for relative, digest in artifacts.items():
        require(sha(inside(scoring, relative)) == digest, "Scorer artifact changed: " + relative)

    lock_path = bundle / "authority/b1c_r3_lock.json"
    lock, seal = read(lock_path), read(bundle / "run/ranking_seal.json")
    require(sha(lock_path) == summary["lock_sha256"] == seal["lock_sha256"], "R3 lock binding mismatch")
    require(sha(ROOT / "configs/b1c_r3_lock.json") == sha(lock_path), "Local authoritative lock differs")
    for relative, digest in lock["source_sha256_canonical_lf"].items():
        source = inside(ROOT, relative)
        require(hashlib.sha256(source.read_bytes().replace(b"\r\n", b"\n")).hexdigest() == digest,
                "Locked scientific source changed: " + relative)
    spec = locked.source_specifications(lock)
    require(summary["scoring"] == spec and summary["bootstrap"]["draws"] == 20000
            and summary["bootstrap"]["seed"] == 20261028
            and summary["bootstrap"]["familywise"] == locked.FAMILY, "Locked scoring policy mismatch")
    require(sha(bundle / "run/ranking_seal.json") == summary["ranking_seal_sha256"], "Ranking seal hash mismatch")
    require(seal["status"] == "RANKINGS_SEALED" and seal["stage"] == "B1C_R3"
            and seal["qrels_opened"] is False and seal["ranking_process_qrel_reads"] == 0,
            "Pre-label ranking seal scope mismatch")
    require(completed["scorer_code_commit"] == summary["scorer_code_commit"] == seal["code_commit"],
            "Scientific deployment commit mismatch")
    require(seal["registry_sha256"] == lock["registry"]["sha256"]
            and seal["existing_registry_sha256"] == lock["existing_cells"]["sha256"], "Registry binding mismatch")
    for name, relative in (("registry", "authority/b1c_r3_sources.json"),
                           ("existing_cells", "authority/b1c_r3_existing.json"),
                           ("acquisition_manifest", "authority/b1c_r3_acquisition.json")):
        require(sha(bundle / relative) == lock[name]["sha256"], "Bundled authority registry changed: " + name)
    registry = read(bundle / "authority/b1c_r3_sources.json")
    locked.verify_prior_partition(read(bundle / "authority/b1c_r3_existing.json"))
    for name, value in (("new_nano_fits", 90), ("new_fiqa_fits", 28),
                        ("historical_fiqa_fits_reused", 2), ("total_fit_groups", 120),
                        ("new_physical_document_encodes", 0)):
        require(seal[name] == value, "Seal accounting differs: " + name)
    metadata = read(bundle / "run/metadata.json")
    require(metadata["status"] == "B1C_R3_RANKINGS_SEALED_STOP"
            and metadata["ranking_count"] == 358 and metadata["failures"] == []
            and metadata["TREC_access"] is False and metadata["qrels_opened"] is False
            and metadata["ranking_process_qrel_reads"] == 0
            and metadata["ranking_seal_sha256"] == summary["ranking_seal_sha256"]
            and metadata["code_commit"] == summary["scorer_code_commit"]
            and metadata["lock_sha256"] == summary["lock_sha256"], "Run completion metadata mismatch")
    first = read(scoring / "first_dev_qrel_open.json")
    require(first["all_736_rankings_sources_and_ids_verified"] is True
            and first["ranking_seal_sha256"] == summary["ranking_seal_sha256"]
            and first["lock_sha256"] == summary["lock_sha256"], "First DEV opening receipt mismatch")
    require(datetime.fromisoformat(seal["sealed_utc"])
            < datetime.fromisoformat(first["first_current_attempt_dev_qrel_access"]),
            "DEV access receipt precedes the complete ranking seal")
    require(summary["failures"] == [] and read(scoring / "synthetic_scorer_checks.json")["status"] == "PASS",
            "Scorer failures or synthetic check failure")

    index = read(scoring / "cell_index.json")
    cells = index["cells"]
    locked.check_matrix(cells, locked.expected_keys(), 736, "all736 prescribed identities")
    new = [c for c in cells if c["origin"] == "new_sealed"]
    retained = [c for c in cells if c["origin"] == "imported_prior"]
    locked.check_matrix(new, locked.missing_keys(), 358, "all358 prospective identities")
    locked.check_matrix(retained, locked.expected_keys() - locked.missing_keys(), 378, "all378 retained identities")
    require((summary["ranking_cells"], summary["new_cells"], summary["imported_cells"]) == (736, 358, 378),
            "Summary partition count mismatch")
    require(index["metrics"] == list(locked.METRICS)
            and index["axes"] == ["dataset_cell", "query", "metric"], "Metric axes mismatch")
    sealed_new = {locked.key(c): c for c in seal["cells"]}
    require(set(sealed_new) == locked.missing_keys() and len(seal["cells"]) == 358, "Sealed new matrix mismatch")
    historical = {locked.key(c): c for c in read(ROOT / "configs/b1c_existing.json")["cells"]}
    for cell in new:
        original = sealed_new[locked.key(cell)]
        require(all(cell.get(k) == v for k, v in original.items()), "New indexed cell differs from seal")
    for cell in retained:
        original = historical[locked.key(cell)]
        require(cell["ranking_sha256"] == original["ranking"]["sha256"], "Retained historical ranking hash changed")

    fits = seal["fit_groups"]
    group_by_id = {g["group_id"]: g for g in registry["groups"]}
    require(len(fits) == len(group_by_id) == 120
            and {f["group_id"] for f in fits} == set(group_by_id), "Fit receipt population mismatch")
    fit_statuses = Counter()
    for fit in fits:
        path = inside(bundle / "run", fit["path"])
        require(sha(path) == fit["sha256"] == seal["artifacts"][fit["path"]], "Fit receipt seal mismatch")
        receipt, group = read(path), group_by_id[fit["group_id"]]
        require(all(receipt[name] == group[name] for name in ("group_id", "dataset", "pair", "seed", "regime", "method")),
                "Fit receipt identity differs from frozen source group")
        reused = locked.recoverable_fiqa_group((group["dataset"], group["pair"], group["seed"], group["method"]))
        require(receipt["new_fit"] is (not reused) and fit["new_fit"] is (not reused),
                "Fit reuse accounting mismatch")
        if "new_physical_document_encodes" in receipt:
            require(receipt["new_physical_document_encodes"] == 0, "Fit encoding accounting mismatch")
        if "metadata_path" in receipt:
            require(sha(inside(bundle / "run", receipt["metadata_path"])) == receipt["metadata_sha256"],
                    "Neural worker metadata binding mismatch")
        fit_statuses[receipt["status"]] += 1
    require(sum(f["new_fit"] for f in fits) == 118, "Require118 fresh and2 reused fit groups")

    # Check every available pre-label sealed artifact; list omitted large raw files.
    available_sealed, omitted_sealed = [], []
    for relative, digest in seal["artifacts"].items():
        path = inside(bundle / "run", relative)
        if path.is_file():
            require(sha(path) == digest, "Available sealed artifact hash mismatch: " + relative)
            available_sealed.append(relative)
        else:
            omitted_sealed.append(relative)
    source_verified, source_unavailable = 0, 0
    for remote, item in seal["source_inputs"].items():
        candidates = remote_to_local.get(remote, [])
        for path in candidates:
            require(sha(path) == item["sha256"] and path.stat().st_size == item["bytes"],
                    "Available source seal mismatch")
        if candidates:
            source_verified += 1
        else:
            source_unavailable += 1

    ranking_records = manifest["rankings"]
    require(len(ranking_records) == 736 and {r["cell_index"] for r in ranking_records} == set(range(736)),
            "Ranking archive index is incomplete or duplicated")
    by_position = {r["cell_index"]: r for r in ranking_records}
    require(len({r["archive_path"] for r in ranking_records}) == 736, "Ranking archive path reused")
    ids, saved, recomputed, metric_details = {}, {}, {}, {}
    maximum_metric_error, metric_values = 0.0, 0
    for dataset in locked.DATASETS:
        id_path = bundle / f"ids/{dataset}.json"
        require(sha(id_path) == seal["inputs"][f"inputs/{dataset}/ids.json"], "Ordered ID seal mismatch")
        ordered = read(id_path)
        documents, queries = ordered["doc_ids"], ordered["query_ids"]
        require((len(documents), len(queries)) == locked.COUNTS[dataset]
                and all(isinstance(v, str) and v for v in documents + queries)
                and len(set(documents)) == len(documents) and len(set(queries)) == len(queries), "Invalid ordered IDs")
        require(index["query_ids"][dataset] == queries, "Scoring query order differs from ID seal")
        ids[dataset] = documents, queries
        qrel_path = (bundle / "qrels/FiQA.tsv" if dataset == "FiQA"
                     else scoring / f"qrels_{dataset}.parquet")
        source = spec["datasets"][dataset]
        require(sha(qrel_path) == source["sha256"]
                and ("bytes" not in source or qrel_path.stat().st_size == source["bytes"]), "DEV qrel lock mismatch")
        judgments, columns = independent_qrels(qrel_path, dataset, source)
        doc_set = set(documents)
        stats = {"dataset": dataset, "sha256": sha(qrel_path), "bytes": qrel_path.stat().st_size,
                 "columns": columns, "implicit_binary_grade": source.get("implicit_binary_grade"),
                 "evaluation_queries": len(queries),
                 "queries_without_positive_judgments": sum(not any(v > 0 for v in judgments.get(q, {}).values()) for q in queries),
                 "positive_judgments_outside_corpus_retained_in_denominator": sum(v > 0 and d not in doc_set for q in queries for d, v in judgments.get(q, {}).items()),
                 "qrel_queries_outside_evaluation_set": len(set(judgments) - set(queries))}
        require(stats == summary["qrel_stats"][dataset], "Independently parsed qrel stats differ")
        values = np.load(scoring / f"per_query_{dataset}.npy", allow_pickle=False)
        dataset_cells = [c for c in cells if c["dataset"] == dataset]
        require(values.shape == (184, len(queries), 2) and list(values.shape) == index["shapes"][dataset]
                and values.dtype == np.float64 and np.isfinite(values).all(), "Per-query shape/type mismatch")
        require(Counter(c["per_query_index"] for c in dataset_cells) == Counter(range(184)), "Per-query index reused or absent")
        saved[dataset], recomputed[dataset] = values, np.empty_like(values)
        dataset_max = 0.0
        for position, cell in enumerate(cells):
            if cell["dataset"] != dataset:
                continue
            record = by_position[position]
            ranking_path = inside(bundle, record["archive_path"])
            require(record["sha256"] == cell["ranking_sha256"] == sha(ranking_path), "Archived ranking hash/identity mismatch")
            ranks = np.load(ranking_path, allow_pickle=False)
            require(ranks.shape == (len(queries), 100) and ranks.dtype.kind in "iu"
                    and np.all(ranks >= 0) and np.all(ranks < len(documents))
                    and not np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0), "Invalid top-100 ranking")
            require(cell["per_query_file"] == f"per_query_{dataset}.npy", "Metric filename mismatch")
            independently = independent_metrics(ranks, documents, queries, judgments)
            recomputed[dataset][cell["per_query_index"]] = independently
            error = float(np.max(np.abs(independently - values[cell["per_query_index"]])))
            require(error <= 1e-12, f"Independent metrics differ: {locked.key(cell)} ({error})")
            dataset_max = max(dataset_max, error)
            metric_values += independently.size
        maximum_metric_error = max(maximum_metric_error, dataset_max)
        metric_details[dataset] = {"shape": list(values.shape), "cells": len(dataset_cells),
                                   "largest_absolute_discrepancy": dataset_max, "qrel_stats": stats}
        print(f"Independent DEV metrics verified: {dataset}, 184 cells, max error {dataset_max:.3g}", flush=True)

    print("Recomputing locked 20,000-draw shared-query bootstrap", flush=True)
    means, contrasts, aggregate, bootstrap = locked.summaries(cells, recomputed, ids)
    numeric, largest = 0, 0.0
    def compare(actual, expected, where):
        nonlocal numeric, largest
        if isinstance(expected, dict):
            require(isinstance(actual, dict) and actual.keys() == expected.keys(), "Keys differ: " + where)
            for name, value in expected.items():
                compare(actual[name], value, where + "/" + name)
        elif isinstance(expected, (list, tuple)):
            require(isinstance(actual, (list, tuple)) and len(actual) == len(expected), "Length differs: " + where)
            for position, value in enumerate(expected):
                compare(actual[position], value, f"{where}/{position}")
        elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
            require(isinstance(actual, (float, int)) and not isinstance(actual, bool), "Numeric type differs: " + where)
            error = abs(actual - expected)
            require(math.isfinite(error) and error <= 1e-12, f"Summary differs: {where}: {error}")
            numeric, largest = numeric + 1, max(largest, error)
        else:
            require(actual == expected, "Value differs: " + where)
    for name, result in (("means", means), ("condition_contrasts", contrasts), ("aggregate_contrasts", aggregate)):
        compare(summary[name], result, name)
    compare(summary["bootstrap"]["datasets"], bootstrap, "bootstrap/datasets")
    require((len(means), len(contrasts), len(aggregate)) == (160, 120, 5), "Summary population mismatch")
    result = {"status": "PASS", "verified_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Local computational verification of completed compact DEV evidence; not independent confirmation or formal paper claim audit",
              "bundle": str(bundle), "bundle_manifest_sha256": sha(manifest_path),
              "summary_sha256": sha(scoring / "summary.json"),
              "lock_sha256": sha(lock_path), "ranking_seal_sha256": sha(bundle / "run/ranking_seal.json"),
              "scorer_code_commit": summary["scorer_code_commit"],
              "compact_manifest_files_verified": len(files), "compact_bytes_verified": byte_count,
              "scoring_completed_artifact_hashes_verified": len(artifacts),
              "prescribed_unique_cells_verified": 736, "new_cells_verified": 358, "retained_cells_verified": 378,
              "fit_receipts_verified": 120, "new_fit_groups_verified": 118,
              "historical_fit_groups_reused_verified": 2, "fit_receipt_statuses": dict(fit_statuses),
              "rankings_independently_rescored": 736, "per_query_metric_values_compared": metric_values,
              "metric_recomputation": "Independent qrel parsing; graded gains 2^rel-1; zero for no-positive queries; all positive qrels in Recall denominator",
              "metric_details": metric_details, "largest_metric_absolute_discrepancy": maximum_metric_error,
              "means_verified": 160, "condition_contrasts_verified": 120, "aggregate_contrasts_verified": 5,
              "nominal95_intervals_verified": 570, "bonferroni99_intervals_verified": 5,
              "summary_numeric_values_compared": numeric, "largest_summary_absolute_discrepancy": largest,
              "bootstrap_draws": 20000, "bootstrap_seed": 20261028, "bootstrap_indices": bootstrap,
              "summary_recomputation": "Locked source summarizer applied to independently recomputed per-query metrics",
              "available_ranking_seal_artifacts_verified": len(available_sealed),
              "omitted_ranking_seal_artifacts": omitted_sealed,
              "source_inputs_locally_verified": source_verified, "source_inputs_not_in_compact_bundle": source_unavailable,
              "limitations": ["Full embedding arrays, learned checkpoints and absent source/generated artifacts are not independently rehashed or regenerated here; their remote seals remain attestations.",
                              "Rankings were not regenerated from embeddings/checkpoints; exact-search implementation, tie decisions and fit correctness are outside this compact computational verification.",
                              "This is inspected DEV evidence; no independent/test result or method selection authorization follows."],
              "local_DEV_qrel_reads": 4, "TREC_access": False, "new_fitting": False, "new_retrieval": False,
              "tolerance": 1e-12, "python_version": sys.version, "numpy_version": np.__version__,
              "verifier_sha256": sha(Path(__file__)), "wall_seconds": time.perf_counter() - started,
              "next_action": "STOP after authorized final D1 reporting; no B2/TREC/systems run"}
    qa.parent.mkdir(parents=True, exist_ok=True)
    with qa.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "qa": str(qa), "metric_max_error": maximum_metric_error,
                      "summary_max_error": largest, "seconds": result["wall_seconds"]}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=ROOT / "results/b1c_r3_review_20261031/evidence")
    parser.add_argument("--qa", type=Path)
    args = parser.parse_args()
    receipt = args.qa or ROOT / ("results/b1c_r3_review_20261031/qa_completed_"
                               + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    verify(args.bundle, receipt)
