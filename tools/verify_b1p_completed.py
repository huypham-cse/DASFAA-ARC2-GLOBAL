"""Local computational verification of the compact B1-P bundle; no qrel reads."""
from datetime import datetime
import argparse
import hashlib
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ops import b1p_score as scorer
from ops.b1p_score_recovery import verify_preserved_metadata


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(bundle, receipt):
    began = time.perf_counter()
    bundle = Path(bundle).resolve()
    gen, scoring = bundle / "generation", bundle / "scoring"
    read, sha = scorer.read_json, scorer.sha
    manifest = read(bundle / "full_manifest.json")["files"]
    compact = [path for path in gen.rglob("*") if path.is_file()]
    for path in compact:
        item = manifest[path.relative_to(gen).as_posix()]
        require(path.stat().st_size == item["bytes"] and sha(path) == item["sha256"], f"Generation changed: {path}")
    lock = read(bundle / "recovery_lock.json")
    descriptor = lock["source_descriptor"]
    require(read(ROOT / lock["descriptor_path"]) == descriptor, "Source descriptor mismatch")
    require(sha(ROOT / lock["descriptor_path"]) == lock["descriptor_sha256"], "Source descriptor hash mismatch")
    verify_preserved_metadata(gen, descriptor)
    for relative, digest in descriptor["original_scoring_files_sha256"].items():
        require(sha(scorer.inside(gen, relative)) == digest, "Original scoring failure changed")
    require({path.name for path in (gen / "scoring").iterdir()} == {"started.json", "failure.json"}, "Original scoring artifacts changed")
    require(read(gen / "scoring/failure.json")["dev_qrel_access_started"] is False, "Original parse had started")
    source_lock = read(ROOT / "configs/b1p_lock.json")
    require(sha(ROOT / "configs/b1p_lock.json") == descriptor["source_lock_sha256"], "Original lock changed")
    spec = scorer.source_specifications(source_lock)
    scorer.verify_sources(source_lock)
    for relative, digest in lock["recovery_source_sha256_canonical_lf"].items():
        observed = hashlib.sha256((ROOT / relative).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        require(observed == digest, "Recovery source changed")
    seal, ids = scorer.verify_seal(gen, descriptor["ranking_seal_sha256"])
    launch = read(bundle / "launch_intent.json")
    expected = {"lock_sha256": sha(bundle / "recovery_lock.json"), "descriptor_sha256": lock["descriptor_sha256"],
        "generation_code_commit": descriptor["source_code_commit"], "recovery_scorer_code_commit": launch["recovery_commit"],
        "ranking_seal_sha256": descriptor["ranking_seal_sha256"], "original_metadata_sha256": descriptor["metadata_sha256"]}
    require(launch["generation_commit"] == expected["generation_code_commit"]
            and launch["TREC_access"] is False and launch["new_fitting"] is False, "Launch scope mismatch")
    manifest_files = 0
    for name, status in (("smoke", "B1P_SCORING_RECOVERY_SMOKE_PASS"), ("scoring", "DEV_SCORED")):
        directory = bundle / name
        completed = read(directory / "completed.json")
        require(completed["status"] == status and completed["binding"] == expected
                and completed["TREC_access"] is False and completed["original_failure_preserved"] is True
                and completed["dev_qrel_access_started"] is (name == "scoring"), "Completion binding/scope mismatch")
        files = completed["artifact_sha256"]
        require({path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file()}
                == set(files) | {"completed.json"}, "Completed artifact set mismatch")
        for relative, digest in files.items():
            require(sha(scorer.inside(directory, relative)) == digest, f"Completed artifact changed: {name}/{relative}")
        context = read(directory / "context_verified.json")
        require(context["binding"] == expected and context["TREC_access"] is False
                and context["all_124_rankings_and_ids_verified"] is True, "Context verification mismatch")
        require(read(directory / "synthetic_scorer_checks.json")["status"] == "PASS", "Synthetic metric checks failed")
        manifest_files += len(files)
    first = read(scoring / "first_dev_qrel_open.json")
    require(first["binding"] == expected and first["all_124_rankings_and_ids_verified"] is True
            and first["smoke_completed_sha256"] == sha(bundle / "smoke/completed.json"), "Pre-parse receipt mismatch")
    first_time = datetime.fromisoformat(first["first_scorer_dev_qrel_parse"]).timestamp()
    loader_time = datetime.fromisoformat(read(scoring / "qrel_access_FiQA.json")["first_scorer_qrel_parse"]).timestamp()
    require(seal["sealed_unix"] < first_time <= loader_time, "Label parse receipt precedes complete seal")
    index, summary = read(scoring / "cell_index.json"), read(scoring / "results_summary.json")
    require(index["query_ids"] == ids[1] and index["metrics"] == list(scorer.METRICS)
            and index["shape"] == [124, 500, 2], "Per-query axes mismatch")
    require(len(index["cells"]) == 124 and len({scorer.key(cell) for cell in index["cells"]}) == 124, "Cell population mismatch")
    for position, (cell, sealed) in enumerate(zip(index["cells"], seal["cells"])):
        require(cell == {**sealed, "per_query_index": position}, "Indexed cell differs from seal")
    arrays = np.load(scoring / "per_query.npy", allow_pickle=False)
    require(arrays.shape == (124, 500, 2) and np.isfinite(arrays).all()
            and np.all((arrays >= 0) & (arrays <= 1)), "Invalid per-query metrics")
    require(summary["status"] == "DEV_SCORED" and summary["TREC_access"] is False
            and summary["original_failure_preserved"] is True and summary["original_raw_status"] == "FAILED_PRESERVED"
            and all(summary[field] == value for field, value in expected.items()), "Summary provenance mismatch")
    require(summary["scoring"] == spec and spec["contrasts"] == scorer.expected_contrasts()
            and spec["familywise"] == scorer.FAMILY and len(summary["contrasts"]) == 32, "Contrast family changed")
    means, contrasts, bootstrap_sha = scorer.summaries(index["cells"], arrays, spec)
    largest, numeric = 0.0, 0
    def compare(actual, expected_value, where):
        nonlocal largest, numeric
        if isinstance(expected_value, dict):
            require(isinstance(actual, dict) and actual.keys() == expected_value.keys(), f"Keys differ: {where}")
            for key, value in expected_value.items():
                compare(actual[key], value, f"{where}/{key}")
        elif isinstance(expected_value, (list, tuple)):
            require(len(actual) == len(expected_value), f"Length differs: {where}")
            for position, value in enumerate(expected_value):
                compare(actual[position], value, f"{where}/{position}")
        elif isinstance(expected_value, (int, float)) and not isinstance(expected_value, bool):
            error = abs(actual - expected_value)
            require(np.isfinite(error) and error <= 1e-12, f"Numeric discrepancy: {where}: {error}")
            largest, numeric = max(largest, error), numeric + 1
        else:
            require(actual == expected_value, f"Value differs: {where}")
    compare(summary["means"], means, "means")
    compare(summary["contrasts"], contrasts, "contrasts")
    bootstrap = summary["bootstrap"]
    require(bootstrap["draws"] == 20000 and bootstrap["seed"] == 20261026
            and bootstrap["indices_dtype"] == "int32" and bootstrap["indices_shape"] == [20000, 500]
            and bootstrap["indices_sha256_c_order"] == bootstrap_sha and bootstrap["familywise"] == scorer.FAMILY,
            "Bootstrap provenance mismatch")
    historical = ROOT / "results/fiqa_development"
    old_index = read(historical / "metric_index.json")
    require(old_index["query_ids"] == ids[1] and old_index["columns"] == list(scorer.METRICS), "Historical metric axes differ")
    old_arrays = np.load(historical / "per_query.npy", allow_pickle=False)
    by_hash = {cell["ranking_sha256"]: old_arrays[i] for i, cell in enumerate(old_index["cells"])}
    matched = 0
    for position, cell in enumerate(index["cells"]):
        if cell["ranking_sha256"] in by_hash:
            compare(arrays[position].tolist(), by_hash[cell["ranking_sha256"]].tolist(), "historical hash-matched metrics")
            matched += 1
    result = {"status": "PASS", "verified_utc": scorer.now(), "scope": "Local computational consistency verification; not independent label validation or a formal paper claim audit",
        "bundle": str(bundle), "binding": expected, "generation_compact_files_verified": len(compact),
        "generation_full_inventory_files": len(manifest), "scorer_smoke_manifest_files_verified": manifest_files,
        "ranking_cells": 124, "per_query_shape": list(arrays.shape), "means_verified": len(means),
        "ordered_contrasts_verified": len(contrasts), "nominal95_intervals_verified": 64, "bonferroni_intervals_verified": 32,
        "numeric_values_compared": numeric, "largest_absolute_discrepancy": largest, "tolerance": 1e-12,
        "bootstrap_indices_sha256": bootstrap_sha, "historical_ranking_sha_matched_metric_cells": matched,
        "original_failure_preserved": True, "original_parse_started": False, "TREC_access": False,
        "local_qrel_reads": 0, "new_fitting": False, "numpy_version": np.__version__,
        "verifier_sha256": sha(Path(__file__)), "wall_seconds": time.perf_counter() - began}
    scorer.write_json(receipt, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=ROOT / "results/b1p_r5_review_20261027")
    parser.add_argument("--receipt", type=Path, default=ROOT / "provenance/qa/b1p_r5_completed_verification_20261027.json")
    args = parser.parse_args()
    print(verify(args.bundle, args.receipt))
