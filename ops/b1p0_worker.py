"""Finite, qrel-free B1-P0 primal/dual synthetic validation only.

The committed JSON lock enumerates every fixture. No data/model loading,
quality metric, GPU operation or real all-paid fit is implemented here.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import threading
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def dump(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Observations:
    """Sample own RSS and host load; never impose resource/time thresholds."""

    def __init__(self, output):
        self.output = output
        self.stop = threading.Event()
        self.peak = 0
        self.errors = []

    def sample(self):
        import psutil
        row = {"unix": time.time(), "pid": os.getpid()}
        try:
            process = psutil.Process()
            rss = process.memory_info().rss
            self.peak = max(self.peak, rss)
            row.update(process_rss_bytes=rss,
                       host_available_memory_bytes=psutil.virtual_memory().available,
                       host_cpu_percent=psutil.cpu_percent(interval=None))
        except Exception as exc:
            row["observation_error"] = repr(exc)
            self.errors.append(repr(exc))
        with (self.output / "resource_trace.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row) + "\n")

    def run(self):
        while not self.stop.wait(1):
            self.sample()

    def begin(self):
        self.sample()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def end(self):
        self.stop.set()
        self.thread.join()
        self.sample()


def fixture(case):
    import numpy as np
    from arc2_global.numerics import normalize_rows
    rng = np.random.default_rng(case["seed"])
    n, dx, dy = case["document_count"], case["source_dim"], case["target_dim"]
    kind = case["fixture"]
    if kind == "random":
        old = normalize_rows(rng.normal(size=(n, dx)).astype(np.float32))
    elif kind == "near_collinear":
        old = np.zeros((n, dx), dtype=np.float32)
        old[:, 0] = 1
        old = normalize_rows(old + 1e-5 * rng.normal(size=(n, dx)).astype(np.float32))
    elif kind == "degenerate":
        old = np.zeros((n, dx), dtype=np.float32)
        old[:, 0] = 1
    else:
        raise ValueError("Unrecognized synthetic fixture")
    matrix = rng.normal(size=(dx, dy)).astype(np.float32)
    shift = .05 * rng.normal(size=(1, dy)).astype(np.float32)
    target = normalize_rows((old @ matrix + shift).astype(np.float32))
    queries = normalize_rows(rng.normal(size=(case["query_count"], dy)).astype(np.float32))
    return old, target, queries


def exact_ranks(scores):
    import numpy as np
    ids = np.arange(scores.shape[1], dtype=np.int64)
    return np.asarray([np.lexsort((ids, -row)) for row in scores], dtype=np.int64)


def rank_comparison(dual_scores, primal_scores, dual_rank, primal_rank, k):
    from arc2_global.solver_backend import compare_scored_rankings
    return compare_scored_rankings(dual_scores, primal_scores, dual_rank, primal_rank, k)


def tie_toy(output):
    import numpy as np
    # Duplicate unit document vectors and orthogonal query directions exercise exact
    # score ties using the same float32 matrix multiplication as retrieval.
    docs = np.array([[1, 0], [1, 0], [0, 1], [0, 1], [-1, 0], [-1, 0]], dtype=np.float32)
    queries = np.array([[1, 0], [0, 1]], dtype=np.float32)
    scores = queries @ docs.T
    expected = np.tile(np.arange(6, dtype=np.int64), (2, 1))
    expected[1] = [2, 3, 0, 1, 4, 5]
    actual = exact_ranks(scores)
    np.savez(output / "tie_toy.npz", queries=queries, documents=docs, scores=scores, expected=expected, actual=actual)
    np.testing.assert_array_equal(actual, expected)
    # A deliberate near-tie reversal must be retained and explained, while
    # an inconsistent ranking with a large score gap must be flagged.
    near_dual = np.array([[1., 1. - 2**-23, .5]], dtype=np.float32)
    near_primal = np.array([[1. - 2**-23, 1., .5]], dtype=np.float32)
    near = rank_comparison(near_dual, near_primal, exact_ranks(near_dual), exact_ranks(near_primal), 2)
    if near["queries_with_difference"] != 1 or near["unexplained_inversion_count"]:
        raise AssertionError("near-tie gap-bound diagnostic failed")
    bad = rank_comparison(scores[:1], scores[:1], actual[:1], actual[:1, ::-1], 6)
    if bad["unexplained_inversion_count"] == 0:
        raise AssertionError("unexplained discrepancy diagnostic failed")
    result = {"tie_rule": "score descending, integer document row ID ascending",
              "exact_ties_pass": True, "near_tie_diagnostic": near,
              "deliberate_inconsistent_ranking_diagnostic": bad}
    dump(output / "tie_toy.json", result)
    return result


def diagnostic_dual_float64(old_anchors, new_anchors, initial):
    """Instrument the unchanged frozen equations solely to retain float64 states.

    The caller checks both float32 casts bitwise against frozen model._tangent2.
    This diagnostic is not an alternative selectable backend or fit policy.
    """
    import numpy as np
    from scipy.linalg import cho_factor, cho_solve
    from arc2_global.model import RIDGE_LAMBDA
    x = np.concatenate((old_anchors.astype(np.float64),
                        np.ones((len(old_anchors), 1), dtype=np.float64)), axis=1)
    y = new_anchors.astype(np.float64)
    gram = x @ x.T + RIDGE_LAMBDA * np.eye(len(x), dtype=np.float64)
    factor = cho_factor(gram, lower=True, overwrite_a=False, check_finite=True)
    coef = initial.astype(np.float64)
    result = []
    for step in (1, 2):
        z = x @ coef
        norms = np.linalg.norm(z, axis=1, keepdims=True)
        if np.any(norms <= 1e-12) or not np.isfinite(z).all():
            raise ValueError("invalid affine direction during frozen diagnostic")
        unit = z / norms
        target = norms * (y - np.sum(unit * y, axis=1, keepdims=True) * unit)
        delta = x.T @ cho_solve(factor, target, check_finite=True)
        coef = coef + delta
        if not np.isfinite(coef).all():
            raise ValueError("non-finite frozen diagnostic coefficient")
        result.append(coef.copy())
    return tuple(result)


def validate_lock(lock, stage):
    required_seeds = [17, 29, 41, 53, 67]
    if lock["seeds"] != required_seeds:
        raise ValueError("Seeds differ from the fixed five-seed contract")
    tolerances = lock["tolerances"]
    if (tolerances["coefficient_maxabs"] != 1e-6
            or tolerances["normalized_proxy_maxabs"] != 1e-6
            or tolerances["float64_atol"] != 1e-9 or tolerances["float64_rtol"] != 1e-9
            or tolerances["score_maxabs"] != 1e-6
            or tolerances["unexplained_rank_discrepancies"] != 0):
        raise ValueError("B1-P0 tolerance contract mismatch")
    cases = lock["stages"][stage]
    if not cases or len(cases) > 64:
        raise ValueError("A finite nonempty stage of at most 64 synthetic fixtures is required")
    names = set()
    for case in cases:
        name = case["name"]
        if not name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in name) or name in names:
            raise ValueError("Case names must be unique safe path components")
        names.add(name)
        if case["seed"] not in required_seeds:
            raise ValueError("Unregistered synthetic seed")
        if (case["source_dim"], case["target_dim"]) not in [(24, 24), (24, 40), (40, 24), (384, 768)]:
            raise ValueError("Unregistered synthetic dimensions")
        if case["fixture"] not in ["random", "near_collinear", "degenerate"]:
            raise ValueError("Unregistered synthetic fixture type")
        if not (8 <= case["anchor_count"] <= 2048
                and case["anchor_count"] <= case["document_count"] <= 4096
                and 1 <= case["query_count"] <= 32):
            raise ValueError("Synthetic fixture size outside B1-P0 scope")
    return cases


def check_identity(lock, code_commit, record):
    import numpy as np
    import scipy
    import psutil
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != code_commit:
        raise ValueError("Deployment commit differs from --code-commit")
    if subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True).strip():
        raise ValueError("Dirty tracked deployment source")
    actual_sources = {}
    for relative, expected in lock["source_sha256_canonical_lf"].items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("Source lock path escapes repository")
        digest = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        actual_sources[relative] = digest
        if digest != expected:
            raise ValueError("Source drift: " + relative)
    versions = {"numpy": np.__version__, "scipy": scipy.__version__}
    if versions != lock["versions"]:
        raise ValueError("Numerical environment version drift")
    environment = {key: os.environ.get(key) for key in lock["environment"]}
    if environment != lock["environment"]:
        raise ValueError("Locked environment variables differ")
    record.update(source_sha256_canonical_lf=actual_sources, versions=versions,
                  environment=environment, psutil_version=psutil.__version__,
                  module_origins={"numpy": np.__file__, "scipy": scipy.__file__},
                  numpy_build=str(np.__config__.CONFIG), code_commit=head)


def run_case(case, output, tolerances):
    import numpy as np
    from arc2_global import procrustes
    from arc2_global.retrieval import exact_topk
    from arc2_global.model import (centered_affine_coefficient, _tangent2,
                                  fit_arc2_global)
    from arc2_global.numerics import normalize_rows
    from arc2_global.solver_backend import (BACKEND_ID, tangent2_primal,
                                          fit_arc2_global_primal, compare_ranking_drift)
    output.mkdir(exist_ok=False)
    began = time.perf_counter()
    row = {**case, "status": "RUNNING", "backend_id": BACKEND_ID,
           "ridge_lambda": 10., "tangent_steps": 2, "steps": []}
    dump(output / "metadata.json", row)
    try:
        old, target, queries = fixture(case)
        n = case["anchor_count"]
        x, y = old[:n].copy(), target[:n].copy()
        ids = np.arange(n, dtype=np.int64)
        sm, tm, matrix = procrustes.procrustes_fit(x, y, center=True)
        base = centered_affine_coefficient(sm, tm, matrix)
        for name, value in [("source", old), ("target", target), ("queries", queries),
                            ("anchors", ids), ("base_coef", base), ("source_mean", sm),
                            ("target_mean", tm), ("matrix", matrix)]:
            np.save(output / (name + ".npy"), value, allow_pickle=False)
        start = time.perf_counter()
        dual = _tangent2(x, y, base)
        row["dual_update_wall_seconds"] = time.perf_counter() - start
        dual64 = diagnostic_dual_float64(x, y, base)
        for frozen, diagnostic in zip(dual, dual64):
            np.testing.assert_array_equal(frozen, diagnostic.astype(np.float32))
        start = time.perf_counter()
        primal64 = tangent2_primal(x, y, base, return_float64=True)
        primal = tuple(coefficient.astype(np.float32) for coefficient in primal64)
        row["primal_update_wall_seconds"] = time.perf_counter() - start
        augmented = np.concatenate((old, np.ones((len(old), 1), dtype=np.float32)), axis=1)
        for step, dc, pc, d64, p64 in zip((1, 2), dual, primal, dual64, primal64):
            # These deliberately use the frozen stored-float32 forward path.
            dr, pr = augmented @ dc, augmented @ pc
            dn, pn = normalize_rows(dr), normalize_rows(pr)
            # Frozen retrieval batch_rows=16, float32 dot and stable row-ID ties.
            ds = np.concatenate([queries[start:start + 16] @ dn.T for start in range(0, len(queries), 16)])
            ps = np.concatenate([queries[start:start + 16] @ pn.T for start in range(0, len(queries), 16)])
            d_rank, p_rank = exact_ranks(ds), exact_ranks(ps)
            np.testing.assert_array_equal(d_rank[:, :100], exact_topk(queries, dn, k=min(100, len(old)), batch_rows=16))
            np.testing.assert_array_equal(p_rank[:, :100], exact_topk(queries, pn, k=min(100, len(old)), batch_rows=16))
            prefix = f"step{step}_"
            for name, value in [("dual_coef", dc), ("primal_coef", pc),
                                ("dual_coef_float64", d64), ("primal_coef_float64", p64),
                                ("dual_raw_proxy", dr), ("primal_raw_proxy", pr),
                                ("dual_proxy", dn), ("primal_proxy", pn),
                                ("dual_scores", ds), ("primal_scores", ps),
                                ("dual_rank", d_rank), ("primal_rank", p_rank)]:
                np.save(output / (prefix + name + ".npy"), value, allow_pickle=False)
            delta = {"step": step, "coefficient_maxabs": float(np.max(np.abs(dc.astype(np.float64) - pc))),
                     "float64_coefficient_maxabs": float(np.max(np.abs(d64 - p64))),
                     "float64_allclose": bool(np.allclose(d64, p64, atol=tolerances["float64_atol"], rtol=tolerances["float64_rtol"])),
                     "raw_proxy_maxabs": float(np.max(np.abs(dr.astype(np.float64) - pr))),
                     "normalized_proxy_maxabs": float(np.max(np.abs(dn.astype(np.float64) - pn))),
                     "score_maxabs": float(np.max(np.abs(ds.astype(np.float64) - ps))),
                     "coefficient_byte_identical": bool(np.array_equal(dc, pc)),
                     "normalized_proxy_byte_identical": bool(np.array_equal(dn, pn)),
                     "ranking": [compare_ranking_drift(queries, dn, pn, k=min(k, len(old)), batch_rows=16) for k in (10, 100)]}
            row["steps"].append(delta)
            dump(output / "metadata.json", row)
            if delta["coefficient_maxabs"] > tolerances["coefficient_maxabs"]:
                raise AssertionError("Coefficient parity tolerance failed")
            if not delta["float64_allclose"]:
                raise AssertionError("Float64 diagnostic coefficient parity tolerance failed")
            if delta["normalized_proxy_maxabs"] > tolerances["normalized_proxy_maxabs"]:
                raise AssertionError("Normalized proxy parity tolerance failed")
            if delta["score_maxabs"] > tolerances["score_maxabs"]:
                raise AssertionError("Float32 retrieval score parity tolerance failed")
            if any(r["unexplained_inversion_count"] > tolerances["unexplained_rank_discrepancies"] for r in delta["ranking"]):
                raise AssertionError("Unexplained top-k discrepancy beyond score-gap drift bound")
        # Exercise each public fit API without altering the common-B0 update
        # comparison above; independently recomputed frozen Procrustes must agree.
        start = time.perf_counter()
        public = fit_arc2_global_primal(old, ids, y, kernel=procrustes)
        row["primal_public_fit_wall_seconds"] = time.perf_counter() - start
        if public.backend_id != BACKEND_ID or public.ridge_lambda != 10 or public.tangent_steps != 2:
            raise AssertionError("Public backend identity mismatch")
        np.testing.assert_array_equal(public.base_coef, base)
        np.testing.assert_array_equal(public.one_step_coef, primal[0])
        np.testing.assert_array_equal(public.arc2_coef, primal[1])
        # Avoid a second n-by-n solve just for fit-wrapper verification. The
        # small shapes exercise unchanged frozen fit as well as its core above.
        if case["source_dim"] == 24 and case["fixture"] == "random":
            frozen = fit_arc2_global(old, ids, y, kernel=procrustes)
            np.testing.assert_array_equal(frozen.base_coef, base)
            np.testing.assert_array_equal(frozen.one_step_coef, dual[0])
            np.testing.assert_array_equal(frozen.arc2_coef, dual[1])
            row["frozen_public_fit_verified"] = True
        row["public_primal_fit_verified"] = True
        row["status"] = "PASS"
    except BaseException as exc:
        row.update(status="FAILED_PRESERVED", failure=repr(exc), traceback=traceback.format_exc())
        raise
    finally:
        row["wall_seconds"] = time.perf_counter() - began
        dump(output / "metadata.json", row)
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage", choices=("smoke", "full"), required=True)
    parser.add_argument("--code-commit", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    began = time.perf_counter()
    record = {"status": "RUNNING", "stage": args.stage, "scope": "B1-P0 finite synthetic only",
              "started_utc": datetime.now(timezone.utc).isoformat(), "checks": [], "failures": [],
              "new_qrel_reads": 0, "real_dataset_or_encoder_loaded": False,
              "benchmark_quality_scoring": False, "artificial_time_or_memory_caps": None,
              "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
              "host": platform.node(), "requested_code_commit": args.code_commit,
              "score_arithmetic": "float32 query batch @ normalized stored-float32 proxy.T; batch_rows=16",
              "tie_rule": "score descending, integer document row ID ascending"}
    monitor = Observations(output)
    monitor_started = False
    def interrupted(signum, frame):
        raise RuntimeError(f"Received signal {signum}")
    signal.signal(signal.SIGTERM, interrupted)
    try:
        record["lock_sha256"] = sha(args.lock)
        lock = json.loads(args.lock.read_text(encoding="utf-8"))
        dump(output / "lock_copy.json", lock)
        cases = validate_lock(lock, args.stage)
        check_identity(lock, args.code_commit, record)
        monitor.begin()
        monitor_started = True
        record["tie_toy"] = tie_toy(output)
        dump(output / "metadata.json", record)
        for case in cases:
            record["checks"].append(run_case(case, output / case["name"], lock["tolerances"]))
            dump(output / "metadata.json", record)
        record["status"] = "B1P0_" + args.stage.upper() + "_PASS"
        record["next_action"] = "STOP: report B1-P0; no automatic B1-P or benchmark launch"
    except BaseException as exc:
        record.update(status="FAILED_PRESERVED", failures=[repr(exc)], traceback=traceback.format_exc())
    finally:
        if monitor_started:
            monitor.end()
        record.update(wall_seconds=time.perf_counter() - began, peak_process_rss_bytes=monitor.peak,
                      resource_observation_errors=monitor.errors, ended_utc=datetime.now(timezone.utc).isoformat())
        record["artifacts"] = {str(p.relative_to(output)): {"sha256": sha(p), "bytes": p.stat().st_size}
                               for p in sorted(output.rglob("*")) if p.is_file() and p != output / "metadata.json"}
        dump(output / "metadata.json", record)
    print(json.dumps({"status": record["status"], "checks": len(record["checks"]), "failures": record["failures"]}))
    return 0 if record["status"] == "B1P0_" + args.stage.upper() + "_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
