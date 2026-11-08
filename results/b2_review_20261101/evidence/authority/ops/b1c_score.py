"""One-shot B1c DEV scorer: 320 sealed new rankings plus 416 frozen imports.

No labels are accessed until the complete six-method matrix, IDs, sources and
code have been verified. Failed attempts are preserved and cannot be resumed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

import numpy as np

try:
    from b1m_score import (inside, load_qrels, mean_std, metrics_for, now,
                           read_json, sha, synthetic_checks as metric_checks,
                           write_json)
except ModuleNotFoundError as error:
    if error.name != "b1m_score":
        raise
    from ops.b1m_score import (inside, load_qrels, mean_std, metrics_for, now,
                               read_json, sha, synthetic_checks as metric_checks,
                               write_json)

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ("NanoNQ", "NanoHotpotQA", "NanoFEVER", "FiQA")
PAIRS = ("minilm_distilroberta", "e5_small_base")
SEEDS = (17, 29, 41, 53, 67)
BUDGETS = ("25pct", "50pct", "75pct")
PRIMARY = "arc2_global_tangent2_r1"
METHODS = ("procrustes_global", PRIMARY, "la2m20_integration_script_adaptation",
           "simplelinear_official_final50_mlp5", "ridge_affine_l10_bias_regularized",
           "embedding_converter_paper_spec")
METRICS = ("ndcg10", "recall100")
KEY_FIELDS = ("dataset", "pair", "seed", "budget", "method")
BOOTSTRAP_DRAWS = 20000
BOOTSTRAP_SEED = 20261028
CONTRASTS = tuple((PRIMARY, method) for method in METHODS if method != PRIMARY)
FAMILY = {"metric": "ndcg10", "scope": "overall_equal_24_strata", "contrasts": 5,
          "family_confidence": 0.95, "per_interval_confidence": 0.99,
          "method": "bonferroni_percentile"}
COUNTS = {"NanoNQ": (5035, 50), "NanoHotpotQA": (5090, 50),
          "NanoFEVER": (4996, 50), "FiQA": (57638, 500)}
EXPOSURE = "Inspected development evidence; no independent confirmation or TREC access"


def key(cell):
    return tuple(cell[field] for field in KEY_FIELDS)


def expected_keys():
    result = set(itertools.product(DATASETS, PAIRS, SEEDS, BUDGETS, METHODS))
    result.update((dataset, pair, None, "full", method)
                  for dataset in DATASETS for pair in PAIRS for method in ("full_x", "full_y"))
    return result


def missing_keys():
    learned = (METHODS[2], METHODS[3], METHODS[5])
    result = {(dataset, pair, seed, budget, method)
              for dataset in DATASETS[:3] for pair in PAIRS for seed in SEEDS
              for budget in BUDGETS for method in learned}
    result.update(("FiQA", pair, seed, budget, method) for pair in PAIRS for seed in SEEDS
                  for budget in ("25pct", "75pct") for method in learned[:2])
    result.update(("FiQA", pair, seed, "75pct", METHODS[5]) for pair in PAIRS for seed in SEEDS)
    return result


def source_specifications(lock):
    spec = lock["scoring"]
    # This file contains source declarations only; reading it does not open labels.
    historical = read_json(ROOT / "configs/b1m_score_r2_lock.json")["scoring"]["datasets"]
    if spec.get("datasets") != historical or set(spec["datasets"]) != set(DATASETS):
        raise ValueError("Require exactly the historical four hash-pinned DEV label sources; no TREC")
    if (type(spec.get("bootstrap_draws")) is not int or spec["bootstrap_draws"] != BOOTSTRAP_DRAWS
            or type(spec.get("bootstrap_seed")) is not int or spec["bootstrap_seed"] != BOOTSTRAP_SEED
            or spec.get("contrasts") != [list(pair) for pair in CONTRASTS]
            or spec.get("familywise") != FAMILY):
        raise ValueError("Require the predeclared five macro contrasts and shared-query bootstrap")
    if any(any(word in name.lower() for word in ("margin", "equivalence", "noninferiority", "selection"))
           for name in spec):
        raise ValueError("No new margin or method selection is authorized")
    return spec


def verify_sources(lock):
    sources = lock.get("source_sha256_canonical_lf", {})
    required = {"ops/b1c_score.py", "ops/b1m_score.py", "configs/b1m_score_r2_lock.json"}
    if not required.issubset(sources):
        raise ValueError("Lock must hash scorer, imported metric/label loader and historical source declarations")
    for relative, digest in sources.items():
        observed = hashlib.sha256(inside(ROOT, relative).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        if observed != digest:
            raise ValueError(f"Locked source changed: {relative}")


def external_path(value):
    path = Path(value)
    return (path if path.is_absolute() else inside(ROOT, value)).resolve()


def verify_artifact_specs(value, verified=None):
    """Verify every source path/hash pair once, without interpreting its contents."""
    verified = {} if verified is None else verified
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            path = external_path(value["path"])
            if "qrel" in str(path).lower():
                raise ValueError("Label sources are forbidden in the pre-access registry")
            digest = value["sha256"]
            if path in verified and verified[path] != digest:
                raise ValueError(f"Conflicting source hash: {path}")
            if path not in verified and sha(path) != digest:
                raise ValueError(f"Source changed: {path}")
            verified[path] = digest
        for child in value.values():
            verify_artifact_specs(child, verified)
    elif isinstance(value, list):
        for child in value:
            verify_artifact_specs(child, verified)
    return verified


def load_registry(lock, name):
    spec = lock[name]
    path = external_path(spec["path"])
    if sha(path) != spec["sha256"]:
        raise ValueError(f"Frozen {name} registry changed")
    return read_json(path)


def check_matrix(cells, expected, count, description):
    actual = [key(cell) for cell in cells]
    if len(actual) != count or len(set(actual)) != count or set(actual) != expected:
        raise ValueError(f"Require exactly {description}, without duplicate identities")
    for cell in cells:
        if cell["seed"] is not None and type(cell["seed"]) is not int:
            raise ValueError("Mapping seeds must be integers")


def verify_ranking(path, digest, ids):
    if sha(path) != digest:
        raise ValueError(f"Ranking changed: {path}")
    ranks = np.load(path, allow_pickle=False)
    docs, queries = ids
    if ranks.shape != (len(queries), min(100, len(docs))) or ranks.dtype.kind not in "iu":
        raise ValueError(f"Invalid ordered integer top-100 ranking: {path}")
    if np.any(ranks < 0) or np.any(ranks >= len(docs)):
        raise ValueError(f"Ranking outside corpus: {path}")
    if np.any(np.diff(np.sort(ranks, axis=1), axis=1) == 0):
        raise ValueError(f"Duplicate document within ranking row: {path}")


def verify_sealed_artifacts(run, artifacts):
    """Verify the stage's immutable artifact manifest, including fit outputs."""
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("Seal must declare its immutable generated artifacts")
    for relative, digest in artifacts.items():
        # The stage's cell-index metadata names the pre-label boundary; it
        # contains ranking identities, not judgments. Only this exact root
        # artifact is exempt from the label-path guard, and it is still hashed.
        if "qrel" in relative.lower() and relative != "cells_pre_qrels.json":
            raise ValueError("Labels cannot enter the pre-access artifact seal")
        if sha(inside(run, relative)) != digest:
            raise ValueError(f"Sealed artifact changed: {relative}")


def verify_seal(run, seal_sha, lock):
    if sha(run / "ranking_seal.json") != seal_sha:
        raise ValueError("Ranking seal changed")
    seal = read_json(run / "ranking_seal.json")
    if seal.get("status") != "RANKINGS_SEALED":
        raise ValueError("Require RANKINGS_SEALED status")
    if seal.get("existing_registry_sha256") != lock["existing_cells"]["sha256"]:
        raise ValueError("Seal does not bind the frozen 416-cell registry")
    registry = load_registry(lock, "registry")
    existing = load_registry(lock, "existing_cells")["cells"]
    new = seal["cells"]
    check_matrix(new, missing_keys(), 320, "the 320 missing DEV cells")
    check_matrix(existing, expected_keys() - missing_keys(), 416, "the 416 prior DEV cells")
    check_matrix(existing + new, expected_keys(), 736, "the complete 736-cell DEV matrix")
    inputs = seal["inputs"]
    if not isinstance(inputs, dict) or not inputs:
        raise ValueError("Seal must hash all inputs")
    for relative, digest in inputs.items():
        if "qrel" in relative.lower():
            raise ValueError("Labels cannot enter the pre-access input seal")
        if sha(inside(run, relative)) != digest:
            raise ValueError(f"Sealed input changed: {relative}")
    verify_sealed_artifacts(run, seal.get("artifacts"))
    ids = {}
    for dataset in DATASETS:
        relative = f"inputs/{dataset}/ids.json"
        if relative not in inputs:
            raise ValueError(f"IDs are not sealed: {dataset}")
        data = read_json(inside(run, relative))
        docs, queries = data["doc_ids"], data["query_ids"]
        if ((len(docs), len(queries)) != COUNTS[dataset]
                or any(not isinstance(x, str) or not x for x in docs + queries)
                or len(set(docs)) != len(docs) or len(set(queries)) != len(queries)):
            raise ValueError(f"Invalid original ordered IDs: {dataset}")
        ids[dataset] = (docs, queries)
    groups = registry["groups"]
    if {group["dataset"] for group in groups} != set(DATASETS):
        raise ValueError("Source registry must cover exactly the four DEV datasets")
    registry_keys = []
    for group in groups:
        if group["ids"]["sha256"] != inputs[f"inputs/{group['dataset']}/ids.json"]:
            raise ValueError("Staged IDs differ from the source registry")
        for case in group["cases"]:
            registry_keys.append((group["dataset"], group["pair"], group["seed"], case["budget"], group["method"]))
    if len(registry_keys) != 320 or set(registry_keys) != missing_keys():
        raise ValueError("Source registry does not describe precisely the 320 missing cells")
    verified = verify_artifact_specs(registry)
    verify_artifact_specs(existing, verified)
    cells = []
    seen = set()
    for origin, rows in (("imported_prior", existing), ("new_sealed", new)):
        for cell in rows:
            if origin == "imported_prior":
                path, digest = external_path(cell["ranking"]["path"]), cell["ranking"]["sha256"]
            else:
                path, digest = inside(run, cell["ranking_path"]), cell["ranking_sha256"]
            if path in seen:
                raise ValueError(f"A ranking artifact serves multiple identities: {path}")
            seen.add(path)
            verify_ranking(path, digest, ids[cell["dataset"]])
            cells.append({**cell, "origin": origin, "resolved_ranking_path": str(path), "ranking_sha256": digest})
    return cells, ids


def verify_context(run, lock_sha, expected=None):
    metadata = read_json(run / "metadata.json")
    fields = ("status", "code_commit", "lock_sha256", "ranking_seal_sha256")
    context = {field: metadata[field] for field in fields}
    if context["status"] != "B1C_RANKINGS_SEALED_STOP" or context["lock_sha256"] != lock_sha:
        raise ValueError("Run is not at the complete B1c ranking-seal STOP under this lock")
    if expected is not None and context != expected:
        raise ValueError("Run context changed during scoring")
    return context


def save_npy(path, values):
    with path.open("xb") as stream:
        np.save(stream, values, allow_pickle=False)
        stream.flush()
        os.fsync(stream.fileno())


def resources():
    """Observe process memory; no resource threshold or stop policy is added."""
    try:
        import resource
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return {"peak_rss_bytes": int(value if sys.platform == "darwin" else value * 1024),
                "source": "resource.getrusage(RUSAGE_SELF).ru_maxrss"}
    except ImportError:
        try:
            import psutil
            info = psutil.Process().memory_info()
            return {"peak_rss_bytes": int(info.peak_wset) if hasattr(info, "peak_wset") else None,
                    "current_rss_bytes": int(info.rss), "source": "psutil.Process.memory_info"}
        except ImportError:
            return {"peak_rss_bytes": None, "source": "unavailable; no threshold applied"}


def interpretation(low, high):
    return "above_zero" if low > 0 else "below_zero" if high < 0 else "unresolved"


def interval(values, draws, descriptive=True, family=False):
    low, high = np.quantile(draws, [0.025, 0.975], method="linear")
    result = {"mean": float(np.mean(values)), "ci95": [float(low), float(high)],
              "descriptive": descriptive, "interval_interpretation": interpretation(low, high)}
    if family:
        low, high = np.quantile(draws, [0.005, 0.995], method="linear")
        result.update(ci_bonferroni_family95=[float(low), float(high)],
                      per_interval_confidence=0.99,
                      family_interval_interpretation=interpretation(low, high))
    return result


def bootstrap_columns(values, rng, draws=BOOTSTRAP_DRAWS, batch=256):
    """Shared query draws for every column; bounded-memory count multiplication."""
    queries = len(values)
    output = np.empty((draws, values.shape[1]), dtype=np.float64)
    digest = hashlib.sha256()
    for start in range(0, draws, batch):
        size = min(batch, draws - start)
        indices = rng.integers(0, queries, size=(size, queries), dtype=np.int32)
        digest.update(indices.tobytes(order="C"))
        weights = np.zeros((size, queries), dtype=np.float64)
        np.add.at(weights, (np.arange(size)[:, None], indices), 1.0 / queries)
        output[start:start + size] = weights @ values
    return output, digest.hexdigest()


def summaries(cells, arrays, ids):
    lookup = {key(cell): arrays[cell["dataset"]][cell["per_query_index"]] for cell in cells}
    means, contrasts, bootstrap = [], [], {}
    aggregate_draws = np.zeros((BOOTSTRAP_DRAWS, len(CONTRASTS), len(METRICS)), dtype=np.float64)
    aggregate_values = np.zeros((len(CONTRASTS), len(METRICS)), dtype=np.float64)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    for dataset in DATASETS:
        columns, definitions = [], []
        def partial(pair, budget, method):
            return np.stack([lookup[(dataset, pair, seed, budget, method)] for seed in SEEDS])
        for pair in PAIRS:
            full_y = lookup[(dataset, pair, None, "full", "full_y")].mean(axis=0)
            for budget, method in itertools.product(BUDGETS, METHODS):
                seed_values = partial(pair, budget, method)
                columns.append(seed_values.mean(axis=0))
                definitions.append(("mean", {"dataset": dataset, "pair": pair, "budget": budget,
                                             "method": method}, seed_values.mean(axis=1), full_y))
            for method in ("full_x", "full_y"):
                values = lookup[(dataset, pair, None, "full", method)]
                columns.append(values)
                definitions.append(("mean", {"dataset": dataset, "pair": pair, "budget": "full",
                                             "method": method}, values.mean(axis=0)[None, :], full_y))
            for budget, (left, right) in itertools.product(BUDGETS, CONTRASTS):
                seed_delta = partial(pair, budget, left) - partial(pair, budget, right)
                columns.append(seed_delta.mean(axis=0))
                definitions.append(("contrast", {"dataset": dataset, "pair": pair, "budget": budget,
                                                 "left": left, "right": right}, seed_delta.mean(axis=1), None))
        values = np.stack(columns, axis=1)  # query, condition, metric
        draws, digest = bootstrap_columns(values.reshape(len(values), -1), rng)
        draws = draws.reshape(BOOTSTRAP_DRAWS, len(columns), len(METRICS))
        bootstrap[dataset] = {"indices_shape": [BOOTSTRAP_DRAWS, len(ids[dataset][1])],
                              "indices_dtype": "int32", "indices_sha256_c_order": digest}
        for index, (kind, row, seed_means, full_y) in enumerate(definitions):
            for metric_index, metric in enumerate(METRICS):
                result = interval(values[:, index, metric_index], draws[:, index, metric_index])
                if kind == "mean":
                    result.update(mean_std(seed_means[:, metric_index]))
                    if row["budget"] != "full":
                        result.update(full_y_retention=(result["mean"] / full_y[metric_index]
                                                       if full_y[metric_index] != 0 else None),
                                      delta_from_full_y=float(result["mean"] - full_y[metric_index]))
                else:
                    result["delta"] = result.pop("mean")
                    result["mapping_seed_variability"] = mean_std(seed_means[:, metric_index])
                row[metric] = result
            if kind == "mean":
                means.append(row)
            else:
                row["familywise"] = False
                contrasts.append(row)
                ci = CONTRASTS.index((row["left"], row["right"]))
                aggregate_draws[:, ci] += draws[:, index] / 24
                aggregate_values[ci] += values[:, index].mean(axis=0) / 24
    aggregate = []
    for index, (left, right) in enumerate(CONTRASTS):
        row = {"left": left, "right": right, "strata": 24, "aggregation": "equal_dataset_pair_budget"}
        for j, metric in enumerate(METRICS):
            result = interval([aggregate_values[index, j]], aggregate_draws[:, index, j],
                              descriptive=metric != "ndcg10", family=metric == "ndcg10")
            result["delta"] = result.pop("mean")
            # Nominal 95% intervals are descriptive even for the family-tested metric.
            result["ci95_descriptive"] = True
            row[metric] = result
        aggregate.append(row)
    return means, contrasts, aggregate, bootstrap


def markdown(summary):
    lines = ["# B1c complete six-method DEV results", "", EXPOSURE + ".", "",
             "736 cells: 416 frozen imports and 320 new sealed rankings. All queries count; no-positive queries score zero. nDCG@10 uses graded 2^rel-1 gains. Recall@100 divides by all positive qrels, including documents outside the corpus.", "",
             "Means average all queries then five mapping seeds. Seed SD uses ddof=1. Full-X and Full-Y are deterministic context/reference rankings; Full-Y is not an upper bound. All 160 means and 120 condition contrasts are descriptive, with nominal 95% query-bootstrap intervals in JSON.", "",
             "The only inferential family is five ARC2-minus-external macro contrasts, equally weighting all 24 dataset/pair/budget strata. Each nDCG interval has 99% confidence (Bonferroni nominal family 95%). Recall intervals are nominal 95% descriptive. All 20,000 draws resample queries independently within each dataset, sharing query indices across every pair, budget, method and seed; the five seeds are averaged first. Percentile-bootstrap coverage is approximate.", "",
             "| Macro contrast (ARC2 minus baseline) | nDCG delta [99% family interval] | Recall delta [descriptive 95%] |", "|---|---:|---:|"]
    for row in summary["aggregate_contrasts"]:
        n, r = row["ndcg10"], row["recall100"]
        nl, nh = n["ci_bonferroni_family95"]
        rl, rh = r["ci95"]
        lines.append(f"| {row['right']} | {n['delta']:+.6f} [{nl:+.6f}, {nh:+.6f}] | {r['delta']:+.6f} [{rl:+.6f}, {rh:+.6f}] |")
    lines += ["", "| Dataset | Pair | Budget | Method | nDCG mean (seed SD) | Recall mean (seed SD) |", "|---|---|---|---|---:|---:|"]
    for row in summary["means"]:
        numbers = [f"{row[m]['mean']:.6f}" + (f" ({row[m]['seed_std']:.6f})" if row[m]["seed_std"] is not None else " (reference)") for m in METRICS]
        lines.append(f"| {row['dataset']} | {row['pair']} | {row['budget']} | {row['method']} | {' | '.join(numbers)} |")
    lines += ["", "| Dataset | Pair | Budget | ARC2 minus baseline | nDCG delta [descriptive 95%] | Recall delta [descriptive 95%] |", "|---|---|---|---|---:|---:|"]
    for row in summary["condition_contrasts"]:
        numbers = []
        for metric in METRICS:
            result = row[metric]
            low, high = result["ci95"]
            numbers.append(f"{result['delta']:+.6f} [{low:+.6f}, {high:+.6f}]")
        lines.append(f"| {row['dataset']} | {row['pair']} | {row['budget']} | {row['right']} | {' | '.join(numbers)} |")
    lines += ["", "The 120 condition comparisons are not 120 family-tested wins. An interval touching or crossing zero is unresolved; no equivalence/noninferiority margin is specified. Preserve all negative results and baseline adaptation qualifications. No retuning, method selection, independent, cost, SLO or causal claim follows from this scorer. STOP for the authorized final D1 report; no TREC or systems run.", ""]
    return "\n".join(lines)


def write_means_csv(path, rows):
    fields = ["dataset", "pair", "budget", "method"]
    fields += [f"{metric}_{name}" for metric in METRICS for name in
               ("mean", "seed_std", "seed_min", "seed_max", "ci95_low", "ci95_high", "full_y_retention", "delta_from_full_y")]
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            flat = {name: row[name] for name in fields[:4]}
            for metric in METRICS:
                value = row[metric]
                for name in ("mean", "seed_std", "full_y_retention", "delta_from_full_y"):
                    flat[f"{metric}_{name}"] = value.get(name)
                flat[f"{metric}_seed_min"], flat[f"{metric}_seed_max"] = value["seed_range"] or (None, None)
                flat[f"{metric}_ci95_low"], flat[f"{metric}_ci95_high"] = value["ci95"]
            writer.writerow(flat)
        stream.flush()
        os.fsync(stream.fileno())


def synthetic_checks():
    checks = metric_checks()
    assert len(expected_keys()) == 736 and len(missing_keys()) == 320
    dummy = [dict(zip(KEY_FIELDS, identity)) for identity in expected_keys()]
    check_matrix(dummy, expected_keys(), 736, "synthetic matrix")
    for bad in (dummy[:-1], dummy[:-1] + [dummy[0]]):
        try:
            check_matrix(bad, expected_keys(), 736, "synthetic matrix")
        except ValueError:
            pass
        else:
            raise AssertionError("Incomplete/duplicate matrix accepted")
    values = np.array([[0.0, 1.0], [1.0, -1.0], [3.0, 2.0]])
    actual, digest = bootstrap_columns(values, np.random.default_rng(23), draws=37, batch=7)
    indices = np.random.default_rng(23).integers(0, 3, size=(37, 3), dtype=np.int32)
    np.testing.assert_allclose(actual, values[indices].mean(axis=1), rtol=0, atol=1e-15)
    assert digest == hashlib.sha256(indices.tobytes(order="C")).hexdigest()
    # This tamper check uses only a temporary synthetic ranking, never real data.
    import tempfile
    with tempfile.TemporaryDirectory(prefix="b1c_scorer_synthetic_") as directory:
        fixture_run = Path(directory).resolve()
        fit_path = fixture_run / "fit_request.json"
        fit_path.write_text('{"synthetic":true}\n', encoding="utf-8")
        cells_path = fixture_run / "cells_pre_qrels.json"
        cells_path.write_text('[]\n', encoding="utf-8")
        artifacts = {"fit_request.json": sha(fit_path), "cells_pre_qrels.json": sha(cells_path)}
        verify_sealed_artifacts(fixture_run, artifacts)
        fit_path.write_text('{"synthetic":"changed"}\n', encoding="utf-8")
        try:
            verify_sealed_artifacts(fixture_run, artifacts)
        except ValueError:
            pass
        else:
            raise AssertionError("Tampered generated artifact accepted")
        path = Path(directory) / "ranking.npy"
        np.save(path, np.array([[0, 1]], dtype=np.int32), allow_pickle=False)
        digest = sha(path)
        verify_ranking(path, digest, (["a", "b"], ["q"]))
        with path.open("ab") as stream:
            stream.write(b"changed")
        try:
            verify_ranking(path, digest, (["a", "b"], ["q"]))
        except ValueError:
            pass
        else:
            raise AssertionError("Tampered ranking accepted")
    return {"status": "PASS", "metric_checks": checks, "matrix_missing_duplicate_checks": "PASS",
            "shared_query_bootstrap_vs_direct_indices": "PASS", "ranking_tamper_rejection": "PASS",
            "generated_artifact_tamper_rejection": "PASS",
            "real_labels_accessed": False}


def run_score(lock_path, run, output=None):
    lock_path, run = Path(lock_path).resolve(), Path(run).resolve()
    selected = Path("scoring") if output is None else Path(output)
    out = (selected if selected.is_absolute() else run / selected).resolve()
    if out == run or not out.is_relative_to(run):
        raise ValueError("Require a new scoring directory strictly inside the run")
    out.mkdir(exist_ok=False)
    start = time.perf_counter()
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        receipt = {"stage": "B1c", "status": "VALIDATING_BEFORE_DEV_LABEL_ACCESS", "started_utc": now(),
                   "lock_path": str(lock_path), "lock_sha256": sha(lock_path),
                   "scorer_sha256": sha(Path(__file__)), "scorer_code_commit": commit,
                   "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
                   "exposure": EXPOSURE, "failures": []}
        write_json(out / "started.json", receipt)
        lock = read_json(lock_path)
        spec = source_specifications(lock)
        verify_sources(lock)
        context = verify_context(run, receipt["lock_sha256"])
        if context["code_commit"] != commit:
            raise ValueError("Ranker and scorer must use the same committed code revision")
        cells, ids = verify_seal(run, context["ranking_seal_sha256"], lock)
        checks = synthetic_checks()
        write_json(out / "synthetic_scorer_checks.json", checks)
        write_json(out / "first_dev_qrel_open.json", {
            "first_current_attempt_dev_qrel_access": now(), "ranking_seal_sha256": context["ranking_seal_sha256"],
            "lock_sha256": receipt["lock_sha256"], "scorer_code_commit": commit,
            "all_736_rankings_sources_and_ids_verified": True, "synthetic_checks": checks,
            "expected_qrel_sources": spec["datasets"], "exposure": EXPOSURE})
        arrays, qrel_stats, qrel_paths = {}, {}, {}
        for dataset in DATASETS:
            source = spec["datasets"][dataset]
            qrels, qrel_stats[dataset] = load_qrels(dataset, source, out, ids[dataset], "first_dev_qrel_open.json")
            qrel_paths[dataset] = out / f"qrels_{dataset}.parquet" if "url" in source else Path(source["path"])
            values = []
            for cell in cells:
                if cell["dataset"] != dataset:
                    continue
                path = Path(cell["resolved_ranking_path"])
                if sha(path) != cell["ranking_sha256"]:
                    raise ValueError(f"Ranking changed before scoring: {path}")
                ranks = np.load(path, allow_pickle=False)
                metrics = metrics_for(ranks, *ids[dataset], qrels)
                if metrics.shape != (len(ids[dataset][1]), 2) or not np.isfinite(metrics).all():
                    raise ValueError("Invalid per-query metrics")
                cell["per_query_index"] = len(values)
                cell["per_query_file"] = f"per_query_{dataset}.npy"
                values.append(metrics)
            arrays[dataset] = np.stack(values)
            save_npy(out / f"per_query_{dataset}.npy", arrays[dataset])
            del qrels
        write_json(out / "cell_index.json", {"axes": ["dataset_cell", "query", "metric"],
                   "metrics": METRICS, "query_ids": {d: ids[d][1] for d in DATASETS},
                   "shapes": {d: list(a.shape) for d, a in arrays.items()}, "cells": cells})
        means, contrasts, aggregate, bootstrap = summaries(cells, arrays, ids)
        verify_sources(lock)
        verify_context(run, receipt["lock_sha256"], context)
        verify_seal(run, context["ranking_seal_sha256"], lock)
        if sha(lock_path) != receipt["lock_sha256"] or sha(Path(__file__)) != receipt["scorer_sha256"]:
            raise ValueError("Lock or scorer changed during scoring")
        for dataset, path in qrel_paths.items():
            if sha(path) != spec["datasets"][dataset]["sha256"]:
                raise ValueError(f"DEV qrels changed during scoring: {dataset}")
        summary = {"status": "DEV_SCORED", "stage": "B1c", "completed_utc": now(),
                   "ranking_cells": 736, "imported_cells": 416, "new_cells": 320,
                   "ranking_seal_sha256": context["ranking_seal_sha256"],
                   "lock_sha256": receipt["lock_sha256"], "scorer_sha256": receipt["scorer_sha256"],
                   "scorer_code_commit": commit, "scoring": spec, "exposure": EXPOSURE,
                   "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": BOOTSTRAP_SEED,
                       "rng": "numpy default_rng/PCG64; datasets in DATASETS order", "datasets": bootstrap,
                       "resampling": "independent query resampling within each dataset; identical indices across pairs/budgets/methods/metrics; average five mapping seeds before resampling",
                       "macro_weighting": "equal 24 dataset/pair/budget strata", "familywise": FAMILY,
                       "condition_intervals": "nominal95 descriptive; not a 120-contrast tested family",
                       "recall_intervals": "nominal95 descriptive", "coverage": "approximate percentile bootstrap"},
                   "qrel_stats": qrel_stats, "means": means, "condition_contrasts": contrasts,
                   "aggregate_contrasts": aggregate, "elapsed_seconds": time.perf_counter() - start,
                   "resources": resources(),
                   "failures": [], "next_action": "STOP for final D1 reporting; no TREC or systems run"}
        write_json(out / "summary.json", summary)
        with (out / "summary.md").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(markdown(summary))
            stream.flush()
            os.fsync(stream.fileno())
        write_means_csv(out / "means.csv", means)
        write_json(out / "metadata.json", {**receipt, "status": "DEV_SCORED", "completed_utc": now(),
                   "elapsed_seconds": summary["elapsed_seconds"], "ranking_cells": 736,
                   "resources": summary["resources"],
                   "next_action": summary["next_action"]})
        artifacts = {str(p.relative_to(out)).replace("\\", "/"): sha(p)
                     for p in sorted(out.rglob("*")) if p.is_file()}
        write_json(out / "completed.json", {"status": "DEV_SCORED", "completed_utc": now(),
                   "scorer_code_commit": commit, "summary_sha256": sha(out / "summary.json"),
                   "artifact_sha256": artifacts, "next_action": summary["next_action"]})
        return summary
    except BaseException as error:
        write_json(out / "failure.json", {"status": "FAILED_PRESERVED", "failed_utc": now(),
                   "error": repr(error), "traceback": traceback.format_exc(),
                   "elapsed_seconds": time.perf_counter() - start, "resources": resources(),
                   "dev_qrel_access_started": (out / "first_dev_qrel_open.json").exists()})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=Path("configs/b1c_lock.json"))
    parser.add_argument("--run", type=Path)
    parser.add_argument("--output", "--output-dir", dest="output", type=Path)
    parser.add_argument("--synthetic", action="store_true", help="Qrel-free checks only; no scientific run")
    args = parser.parse_args()
    if args.synthetic:
        import json
        print(json.dumps(synthetic_checks(), indent=2))
    elif args.run is None:
        parser.error("--run is required unless --synthetic is selected")
    else:
        run_score(args.lock, args.run, args.output)
