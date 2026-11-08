"""Bounded recovery of the preserved, pre-parse B1-P scorer failure.

The generation checkout and failed attempt are immutable. Only the separately
committed recovery checkout writes a new smoke or scoring directory. Numerical
and statistical functions are imported unchanged from the original scorer.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import tempfile
import time
import traceback

import numpy as np

try:
    import b1p_score as original
except ModuleNotFoundError as error:
    if error.name != "b1p_score":
        raise
    from ops import b1p_score as original

ROOT = Path(__file__).resolve().parents[1]
TOOL = Path(__file__).resolve()
PROTOCOL = "protocols/B1P_SCORING_RECOVERY_20261027.md"
read_json, write_json, sha, inside, now = (
    original.read_json, original.write_json, original.sha, original.inside, original.now)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_sha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def git_identity(root, commit):
    observed = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    require(observed == commit, "Checkout commit differs from pinned commit")
    # Raw run directories are intentionally untracked; every tracked file must
    # still match HEAD, and untracked source/config/protocol files are rejected.
    subprocess.run(["git", "diff", "--quiet", "HEAD", "--"], cwd=root, check=True)
    unknown = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "--", ".", ":!results/**"],
        cwd=root, text=True).strip()
    require(not unknown, "Checkout contains uncommitted files outside results")
    return observed


def verify_runtime(lock, source_lock):
    for field in ("cpu_environment", "cpu_versions", "cpu_sklearn_version"):
        require(lock[field] == source_lock[field], f"Recovery changed original {field}")
    for name, version in lock["cpu_versions"].items():
        require(importlib.metadata.version(name) == version, f"CPU version mismatch: {name}")
    require(importlib.metadata.version("scikit-learn") == lock["cpu_sklearn_version"],
            "CPU scikit-learn version mismatch")
    for name, value in lock["cpu_environment"].items():
        require(os.environ.get(name) == value, f"CPU environment mismatch: {name}")
    from threadpoolctl import threadpool_info
    blas = threadpool_info()
    numerical = [row for row in blas if row.get("internal_api") == "openblas"]
    require(numerical and all(row.get("architecture") == "Haswell" and row["num_threads"] == 4
                              for row in numerical), "Original Haswell/four-thread BLAS required")
    require("torch" not in sys.modules and "transformers" not in sys.modules,
            "Recovery must not load GPU or encoder modules")
    return {"python": sys.version, "executable": sys.executable, "numpy": np.__version__,
            "platform": platform.platform(), "environment": lock["cpu_environment"], "blas": blas}


def verify_recovery_sources(lock):
    sources = lock["recovery_source_sha256_canonical_lf"]
    require(set(sources) == {"ops/b1p_score_recovery.py", PROTOCOL},
            "Recovery lock must hash exactly the recovery orchestrator and protocol")
    for relative, digest in sources.items():
        require(canonical_sha(inside(ROOT, relative)) == digest, f"Recovery source changed: {relative}")


def verify_preserved_metadata(run, descriptor):
    require(sha(run / "metadata.json") == descriptor["metadata_sha256"], "Original metadata changed")
    meta = read_json(run / "metadata.json")
    require(meta["status"] == "FAILED_PRESERVED"
            and meta["code_commit"] == descriptor["source_code_commit"]
            and meta["lock_sha256"] == descriptor["source_lock_sha256"]
            and meta["ranking_seal_sha256"] == descriptor["ranking_seal_sha256"]
            and meta["ranking_count"] == 124
            and meta["failures"] == ["RuntimeError('Scorer failed; preserve all sealed rankings')"]
            and meta["ranking_process_qrel_reads"] == 0 and meta["TREC_access"] is False,
            "Original failure is outside this bounded scorer recovery")


def verify_original_context(descriptor):
    """Accept only the exact failed metadata, never relabel it as sealed."""
    run = Path(descriptor["run"]).resolve()
    root = Path(descriptor["source_root"]).resolve()
    require(root != ROOT and run.parent == root / "results", "Require separate original generation checkout")
    require(descriptor["original_qrel_parse_started"] is False
            and descriptor["ranking_count"] == 124
            and descriptor["raw_status_remains"] == "FAILED_PRESERVED"
            and descriptor["TREC_access"] is False, "Recovery scope differs from exact pre-parse failure")
    git_identity(root, descriptor["source_code_commit"])
    verify_preserved_metadata(run, descriptor)
    files = descriptor["original_scoring_files_sha256"]
    require(set(files) == {"scoring/started.json", "scoring/failure.json", "scorer.stdout.log", "scorer.stderr.log"},
            "Require complete original pre-parse failure artifacts")
    for relative, digest in files.items():
        require(sha(inside(run, relative)) == digest, f"Original failure artifact changed: {relative}")
    require({path.name for path in (run / "scoring").iterdir()} == {"started.json", "failure.json"},
            "Original attempt contains unexpected or label-access artifacts")
    failure = read_json(run / "scoring/failure.json")
    started = read_json(run / "scoring/started.json")
    require(failure["status"] == "FAILED_PRESERVED"
            and failure["error"] == "FileExistsError(17, 'File exists')"
            and failure["dev_qrel_access_started"] is False
            and started["status"] == "VALIDATING_BEFORE_SCORER_LABEL_ACCESS"
            and started["scorer_code_commit"] == descriptor["source_code_commit"]
            and started["lock_sha256"] == descriptor["source_lock_sha256"],
            "Original attempt is not the exclusive started-receipt pre-parse failure")
    return run, root


def validate(lock_path, code_commit, expected_lock_sha):
    require(sha(lock_path) == expected_lock_sha, "Recovery lock changed")
    lock = read_json(lock_path)
    git_identity(ROOT, code_commit)
    verify_recovery_sources(lock)
    descriptor_path = Path(lock["descriptor_path"])
    if not descriptor_path.is_absolute():
        descriptor_path = inside(ROOT, lock["descriptor_path"])
    require(sha(descriptor_path) == lock["descriptor_sha256"], "Recovery descriptor changed")
    descriptor = read_json(descriptor_path)
    require(descriptor == lock["source_descriptor"], "Descriptor differs from locked original context")
    run, old_root = verify_original_context(descriptor)
    source_path = Path(descriptor["source_lock_path"]).resolve()
    require(source_path == old_root / "configs/b1p_lock.json", "Unexpected original lock path")
    require(sha(source_path) == descriptor["source_lock_sha256"], "Original lock changed")
    source_lock = read_json(source_path)
    spec = original.source_specifications(source_lock)
    original.verify_sources(source_lock)  # unchanged guard verifies the NEW checkout
    for relative, digest in source_lock["source_sha256_canonical_lf"].items():
        require(canonical_sha(inside(old_root, relative)) == digest, f"Original source changed: {relative}")
    started = read_json(run / "scoring/started.json")
    require(started["scorer_sha256"] == sha(old_root / "ops/b1p_score.py"), "Original scorer identity changed")
    runtime = verify_runtime(lock, source_lock)
    seal, ids = original.verify_seal(run, descriptor["ranking_seal_sha256"])
    require(seal["ranking_process_qrel_reads"] == 0, "Ranking process parsed qrels")
    transport = original.verify_dev_transport(source_lock)
    require(transport is not None, "This recovery requires the original opaque DEV transport")
    return lock, descriptor, run, spec, seal, ids, transport, runtime


def started_receipt(stage, lock_path, code_commit):
    # Compute the final status before this receipt's single exclusive write.
    return {"stage": "B1-P scoring recovery", "mode": stage, "started_utc": now(),
            "status": "VALIDATING_BEFORE_SCORER_PARSE_WITH_PRIOR_DEV_TRANSPORT",
            "lock_path": str(lock_path), "lock_sha256": sha(lock_path),
            "scorer_sha256": sha(TOOL), "recovery_scorer_code_commit": code_commit,
            "exposure": original.EXPOSURE, "TREC_access": False}


def receipt_regression_check():
    """Exercise the actual exclusive writer without any label or real run."""
    with tempfile.TemporaryDirectory(prefix="b1p_receipt_fixture_") as directory:
        root = Path(directory)
        old = root / "old_started.json"
        write_json(old, {"status": "VALIDATING_BEFORE_SCORER_LABEL_ACCESS"})
        try:
            write_json(old, {"status": "VALIDATING_BEFORE_SCORER_PARSE_WITH_PRIOR_DEV_TRANSPORT"})
        except FileExistsError:
            pass
        else:
            raise ValueError("Original exclusive-write failure did not reproduce")
        new = root / "new_started.json"
        receipt = started_receipt("smoke", old, "synthetic_fixture")
        write_json(new, receipt)
        require(read_json(new) == receipt and receipt["status"] ==
                "VALIDATING_BEFORE_SCORER_PARSE_WITH_PRIOR_DEV_TRANSPORT", "Single-write recovery receipt mismatch")
        meta = {"status": "FAILED_PRESERVED", "code_commit": "fixture_generation_commit",
                "lock_sha256": "fixture_lock_sha", "ranking_seal_sha256": "fixture_seal_sha",
                "ranking_count": 124, "failures": ["RuntimeError('Scorer failed; preserve all sealed rankings')"],
                "ranking_process_qrel_reads": 0, "TREC_access": False}
        write_json(root / "metadata.json", meta)
        descriptor = {"metadata_sha256": sha(root / "metadata.json"),
                      "source_code_commit": meta["code_commit"], "source_lock_sha256": meta["lock_sha256"],
                      "ranking_seal_sha256": meta["ranking_seal_sha256"]}
        verify_preserved_metadata(root, descriptor)
        # Mutate only a temporary fixture, retaining the pinned prior digest.
        (root / "metadata.json").write_text('{"status":"RANKINGS_SEALED"}\n', encoding="utf-8")
        try:
            verify_preserved_metadata(root, descriptor)
        except ValueError as error:
            require(str(error) == "Original metadata changed", "Unexpected fixture rejection")
        else:
            raise ValueError("Changed original context fixture was accepted")
    return {"original_duplicate_exclusive_write": "FileExistsError reproduced",
            "recovery_started_receipt": "final status written once",
            "changed_original_metadata": "rejected against pinned SHA256", "qrel_access": False}


def binding(lock, descriptor, receipt):
    return {"lock_sha256": receipt["lock_sha256"], "descriptor_sha256": lock["descriptor_sha256"],
            "generation_code_commit": descriptor["source_code_commit"],
            "recovery_scorer_code_commit": receipt["recovery_scorer_code_commit"],
            "ranking_seal_sha256": descriptor["ranking_seal_sha256"],
            "original_metadata_sha256": descriptor["metadata_sha256"]}


def verify_smoke(path, expected):
    path = Path(path).resolve()
    require(path.is_relative_to(ROOT / "results") and path != ROOT / "results",
            "Smoke must be inside recovery checkout results")
    smoke = read_json(path / "completed.json")
    require(smoke["status"] == "B1P_SCORING_RECOVERY_SMOKE_PASS"
            and smoke["binding"] == expected and smoke["dev_qrel_access_started"] is False,
            "Require PASS qrel-free smoke with identical recovery context")
    for relative, digest in smoke["artifact_sha256"].items():
        require(sha(inside(path, relative)) == digest, f"Smoke artifact changed: {relative}")
    require(not (path / "failure.json").exists(), "Smoke has a failure receipt")
    return sha(path / "completed.json")


def run(stage, lock_path, code_commit, output, smoke=None):
    require(stage in ("smoke", "score"), "Unknown recovery stage")
    lock_path, out = Path(lock_path).resolve(), Path(output).resolve()
    preliminary = read_json(lock_path)
    raw = Path(preliminary["source_descriptor"]["run"]).resolve()
    if stage == "smoke":
        require(out.parent == ROOT / "results", "Smoke output must be a new directory under recovery results")
    else:
        require(out.parent == raw and out.name.startswith("scoring_recovery_"),
                "Scoring output must be a new scoring_recovery_* directory inside original run")
        require(smoke is not None, "Score requires --smoke")
    out.mkdir(exist_ok=False)
    began = time.perf_counter()
    try:
        receipt = started_receipt(stage, lock_path, code_commit)
        write_json(out / "started.json", receipt)
        lock, descriptor, raw, spec, seal, ids, transport, runtime = validate(
            lock_path, code_commit, receipt["lock_sha256"])
        bound = binding(lock, descriptor, receipt)
        checks = original.synthetic_checks()
        write_json(out / "synthetic_scorer_checks.json", checks)
        write_json(out / "receipt_regression_check.json", receipt_regression_check())
        write_json(out / "context_verified.json", {"binding": bound, "runtime": runtime,
                   "all_124_rankings_and_ids_verified": True, "prior_dev_label_transport": transport,
                   "original_failure_preserved": True, "TREC_access": False})
        if stage == "smoke":
            status = "B1P_SCORING_RECOVERY_SMOKE_PASS"
        else:
            smoke_sha = verify_smoke(smoke, bound)
            write_json(out / "first_dev_qrel_open.json", {
                "first_scorer_dev_qrel_parse": now(), "binding": bound,
                "prior_dev_label_transport": transport, "all_124_rankings_and_ids_verified": True,
                "synthetic_checks": checks, "expected_qrel_sources": spec["datasets"],
                "smoke_completed_sha256": smoke_sha, "exposure": original.EXPOSURE})
            qrels, qrel_stats = original.load_fiqa_qrels(spec["datasets"][original.DATASET], out, ids, transport)
            arrays, cells = [], []
            for index, cell in enumerate(seal["cells"]):
                path = inside(raw, cell["ranking_path"])
                require(sha(path) == cell["ranking_sha256"], "Ranking changed before scoring")
                values = original.metrics_for(np.load(path, allow_pickle=False), *ids, qrels)
                require(values.shape == (500, 2) and np.isfinite(values).all(), "Invalid per-query metrics")
                arrays.append(values)
                cells.append({**cell, "per_query_index": index})
            arrays = np.stack(arrays)
            require(arrays.shape == (124, 500, 2), "Incomplete per-query array")
            original.save_npy(out / "per_query.npy", arrays)
            write_json(out / "cell_index.json", {"axes": ["cell", "query", "metric"],
                       "metrics": original.METRICS, "shape": list(arrays.shape), "query_ids": ids[1], "cells": cells})
            means, contrasts, bootstrap_sha = original.summaries(cells, arrays, spec)
            require(sha(Path(spec["datasets"][original.DATASET]["path"])) == original.QREL_SHA256,
                    "FiQA DEV qrels changed during scoring")
            status = "DEV_SCORED"
            summary = {"status": status, "stage": "B1-P", "completed_utc": now(), **bound,
                "ranking_cells": 124, "scorer_sha256": receipt["scorer_sha256"],
                "scorer_code_commit": code_commit, "original_failure_preserved": True,
                "original_raw_status": "FAILED_PRESERVED", "scoring": spec, "exposure": original.EXPOSURE,
                "interpretation": "DEV only; no method selection or independent/D1 claim",
                "bootstrap": {"draws": original.BOOTSTRAP_DRAWS, "seed": original.BOOTSTRAP_SEED,
                    "rng": "numpy default_rng(20261026), PCG64", "indices_shape": [20000, 500],
                    "indices_dtype": "int32", "indices_sha256_c_order": bootstrap_sha,
                    "resampling": "500 queries with replacement; five seeds averaged first; shared indices",
                    "familywise": original.FAMILY, "coverage": "approximate percentile bootstrap"},
                "qrel_stats": qrel_stats, "means": means, "contrasts": contrasts,
                "TREC_access": False, "failures": [], "next_action": "STOP after authorized B1-P report"}
        # Re-run every provenance/source/input gate before publishing either PASS.
        validate(lock_path, code_commit, receipt["lock_sha256"])
        require(sha(TOOL) == receipt["scorer_sha256"], "Recovery tool changed during attempt")
        if stage == "score":
            require(verify_smoke(smoke, bound) == smoke_sha, "Smoke changed during scoring")
            require(sha(Path(spec["datasets"][original.DATASET]["path"])) == original.QREL_SHA256,
                    "FiQA DEV qrels changed before publication")
            write_json(out / "results_summary.json", summary)
            with (out / "results_summary.md").open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(original.markdown(summary))
                stream.write(f"\nGeneration commit: `{descriptor['source_code_commit']}`. "
                             f"Recovery scorer commit: `{code_commit}`. "
                             "Original failed scoring attempt and FAILED_PRESERVED raw metadata remain intact.\n")
                stream.flush()
                os.fsync(stream.fileno())
        artifacts = {path.relative_to(out).as_posix(): sha(path) for path in sorted(out.rglob("*")) if path.is_file()}
        try:
            import resource
            peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except ImportError:
            peak_rss = None
        completed = {"status": status, "completed_utc": now(), "binding": bound,
                     "wall_seconds": time.perf_counter() - began, "peak_process_rss_bytes": peak_rss,
                     "dev_qrel_access_started": stage == "score", "TREC_access": False,
                     "original_failure_preserved": True, "artifact_sha256": artifacts,
                     "next_action": "STOP after B1-P report; no automatic next study"}
        write_json(out / "completed.json", completed)
        return completed
    except BaseException as error:
        write_json(out / "failure.json", {"status": "FAILED_PRESERVED", "failed_utc": now(),
                   "error": repr(error), "traceback": traceback.format_exc(),
                   "wall_seconds": time.perf_counter() - began,
                   "dev_qrel_access_started": (out / "first_dev_qrel_open.json").exists(), "TREC_access": False})
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("smoke", "score"), required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smoke", type=Path)
    args = parser.parse_args()
    def interrupted(signum, frame):
        raise RuntimeError(f"Received signal {signum}")
    signal.signal(signal.SIGTERM, interrupted)
    run(args.stage, args.lock, args.code_commit, args.output, args.smoke)


if __name__ == "__main__":
    main()
