"""Anchor-budget adaptation of Yoon & Arik's ACL 2025 Embedding-Converter.

This is an independently written *paper-spec reimplementation*, not official
code or a reproduction of the paper's large multi-corpus training experiment.
Ported from the historical standalone external paper-spec baseline.
B1-P preserves its numerical model, optimizer, sampling and selection/refit
policy. Exact neighbor scores retain the original full float32 matrix multiply;
only top-k selection replaces complete-row sorting with partitioning and stable
boundary handling. Blocking SGEMM changed observed near-tie neighbor ordering.
No data/model downloading, qrels, search, or implicit tuning occurs here.
PyTorch is imported lazily so the core package retains its existing dependencies.
Scientific use requires a separately committed protocol. Resources are observed
without artificial time/RSS/CUDA admission or stopping thresholds.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import math
import os
from pathlib import Path
import time
from typing import Callable

import numpy as np


PAPER_URL = "https://aclanthology.org/2025.acl-long.1237.pdf"
METHOD = "embedding_converter_paper_spec_paired_budget"
NEIGHBOR_IMPLEMENTATION = "dense_float32_scores_stable_topk_r1"
SPLIT_SEED_OFFSET = 20261025
RESUME_SCHEMA = "embedding_converter_exact_resume_v1"


@dataclass(frozen=True)
class ConverterConfig:
    """Defaults retain published width, losses, k, optimizer rate and iterations.

    Sampling/reductions, Adam secondary defaults, hidden-only activations and
    final-checkpoint selection are explicit reimplementation choices. Changing
    the iterations or width must be recorded as a further adaptation.
    """

    hidden_multiplier: int = 5
    iterations: int = 50_000
    batch_size: int = 64
    local_k: int = 100
    local_samples_per_center: int = 1
    alpha: float = 0.1
    beta: float = 0.1
    learning_rate: float = 0.001
    adam_betas: tuple[float, float] = (0.9, 0.999)
    adam_epsilon: float = 1e-8
    report_every: int = 250
    transform_batch_size: int = 256
    threads: int = 4
    device: str = "cpu"

    def __post_init__(self):
        integers = (self.hidden_multiplier, self.iterations, self.batch_size,
                    self.local_k, self.local_samples_per_center, self.report_every,
                    self.transform_batch_size, self.threads)
        if any(isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in integers):
            raise ValueError("integer configuration values must be positive integers")
        if any(not math.isfinite(v) or v < 0 for v in (self.alpha, self.beta)):
            raise ValueError("loss weights must be finite and nonnegative")
        if not math.isfinite(self.learning_rate) or self.learning_rate <= 0:
            raise ValueError("learning_rate must be finite and positive")
        if (len(self.adam_betas) != 2 or any(not 0 <= v < 1 for v in self.adam_betas)
                or not math.isfinite(self.adam_epsilon) or self.adam_epsilon <= 0):
            raise ValueError("invalid Adam parameters")
        if self.device not in ("cpu", "cuda"):
            raise ValueError("device must be cpu or cuda (one current CUDA device)")


def parameter_count(source_dim: int, target_dim: int, hidden_multiplier: int = 5) -> int:
    if min(source_dim, target_dim, hidden_multiplier) < 1:
        raise ValueError("dimensions and multiplier must be positive")
    hidden = target_dim * hidden_multiplier
    widths = (source_dim, hidden, hidden, hidden, target_dim)
    return sum((a + 1) * b for a, b in zip(widths[:-1], widths[1:]))


def build_model(source_dim: int, target_dim: int, config: ConverterConfig):
    """Four affine layers, three SELUs, unit-normalized final output."""
    import torch
    from torch import nn

    if min(source_dim, target_dim) < 1:
        raise ValueError("embedding dimensions must be positive")
    hidden = config.hidden_multiplier * target_dim

    class ConverterMLP(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(source_dim, hidden), nn.SELU(),
                nn.Linear(hidden, hidden), nn.SELU(),
                nn.Linear(hidden, hidden), nn.SELU(),
                nn.Linear(hidden, target_dim),
            )

        def forward(self, values):
            return torch.nn.functional.normalize(self.layers(values), p=2, dim=-1, eps=1e-12)

    return ConverterMLP()


def _vectors(values: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(values)
    if (result.ndim != 2 or min(result.shape) < 1 or result.dtype != np.float32
            or not np.isfinite(result).all()):
        raise ValueError(f"{name} must be a nonempty finite float32 matrix")
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    if np.any(norms < 1e-12):
        raise ValueError(f"{name} contains a zero vector")
    # Input embeddings in this repository are already unit rows; normalize
    # defensively, without centering or using any non-anchor target vectors.
    return np.ascontiguousarray(result / norms, dtype=np.float32)


def target_neighbors(target_anchors: np.ndarray, k: int, *, block_rows: int = 256) -> np.ndarray:
    """Original dense float32 cosine scores, exact stable top-k selection.

    The full target @ target.T operation is retained byte-for-byte in shape and
    arithmetic: row-blocked SGEMM changed near-tie ordering in the first smoke.
    Self is excluded. Partitioning finds the kth score; strictly higher scores
    plus the smallest row IDs among boundary ties form the k candidates, which
    are ordered by descending score then ascending row ID. Complete rows are
    never sorted. ``block_rows`` groups row processing only, not score GEMM.
    The score matrix costs O(n*n) float32 memory; output costs O(n*k) int64.
    """
    target = _vectors(target_anchors, "target_anchors")
    if not isinstance(k, int) or isinstance(k, bool) or not 0 < k < len(target):
        raise ValueError("local_k must be positive and smaller than anchor count")
    if isinstance(block_rows, bool) or not isinstance(block_rows, int) or block_rows < 1:
        raise ValueError("block_rows must be a positive integer")
    similarities = target @ target.T
    np.fill_diagonal(similarities, -np.inf)
    output = np.empty((len(target), k), dtype=np.int64)
    for start in range(0, len(target), block_rows):
        stop = min(start + block_rows, len(target))
        for offset, row in enumerate(similarities[start:stop]):
            threshold = np.partition(row, len(row)-k)[len(row)-k]
            higher = np.flatnonzero(row > threshold)
            boundary = np.flatnonzero(row == threshold)[:k-len(higher)]
            candidates = np.concatenate((higher, boundary))
            output[start+offset] = candidates[np.lexsort((candidates, -row[candidates]))]
    return output


def anchor_split(count: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Historical seeded split: floor(n/8) validation, remaining training.

    For the fixed 1,024-anchor regime this is exactly 896/128. The same rule
    gives 25,217/3,602 for 28,819 all-paid pairs. Validation uses no qrels.
    """
    if isinstance(count, bool) or not isinstance(count, int) or count < 8:
        raise ValueError("at least eight paired rows are required")
    order = np.random.default_rng(seed + SPLIT_SEED_OFFSET).permutation(count).astype(np.int64)
    validation_count = count // 8
    return order[validation_count:], order[:validation_count]


def synthetic_neighbor_parity(seed: int = 17) -> dict:
    """Qrel-free smoke evidence against the original complete stable argsort.

    This function is intentionally invoked only after the protocol is committed.
    Its dense reference is limited to small synthetic matrices, never real pairs.
    Tests k=100, exact duplicate/boundary ties, excluded self and partial blocks.
    """
    rng = np.random.default_rng(seed)
    random = rng.normal(size=(137, 19)).astype(np.float32)
    tied = np.tile(np.eye(7, dtype=np.float32), (21, 1))[:137].copy()
    near = random.copy()
    near[1] = near[0]
    near[2] = near[0] + np.float32(2**-20) * rng.normal(size=19).astype(np.float32)
    checks = []
    for name, values in (("random", random), ("duplicate_boundary_ties", tied), ("near_ties", near)):
        # Original routine defensively normalizes exactly once on its input.
        normalized = _vectors(values, "synthetic_target")
        dense = normalized @ normalized.T
        np.fill_diagonal(dense, -np.inf)
        for k in (1, 7, 100, 136):
            expected = np.argsort(-dense, axis=1, kind="stable")[:, :k].astype(np.int64)
            for block in (16, 64, 256):
                actual = target_neighbors(values, k, block_rows=block)
                np.testing.assert_array_equal(actual, expected)
                if np.any(actual == np.arange(len(values))[:, None]):
                    raise AssertionError("self neighbor retained")
                checks.append({"fixture": name, "k": k, "block_rows": block,
                               "dense_exact_ids_equal": True, "sha256": _array_hash(actual)})
    # Real-width synthetic parity exercises the original 1,024-anchor shape
    # using this process's actual NumPy/BLAS package before any full job.
    normal = rng.normal(size=(1024, 768)).astype(np.float32)
    offset = (normal + np.float32(.05) * rng.normal(size=(1, 768)).astype(np.float32)).astype(np.float32)
    for name, values in (("fullwidth_normal", normal), ("fullwidth_normal_offset", offset)):
        normalized = _vectors(values, "synthetic_fullwidth_target")
        dense = normalized @ normalized.T
        np.fill_diagonal(dense, -np.inf)
        expected = np.argsort(-dense, axis=1, kind="stable")[:, :100].astype(np.int64)
        actual = target_neighbors(values, 100, block_rows=256)
        np.testing.assert_array_equal(actual, expected)
        # The candidate implementation now uses the same whole-matrix SGEMM;
        # record its independently recomputed float32 score drift explicitly.
        scores = normalized @ normalized.T
        np.fill_diagonal(scores, -np.inf)
        valid = np.isfinite(scores)
        max_score_drift = float(np.max(np.abs(
            scores[valid].astype(np.float64)-dense[valid].astype(np.float64))))
        if max_score_drift != 0:
            raise AssertionError("Whole-matrix score arithmetic drift")
        checks.append({"fixture": name, "rows": 1024, "target_dim": 768,
                       "k": 100, "block_rows": 256, "dense_exact_ids_equal": True,
                       "max_float32_score_drift": max_score_drift, "sha256": _array_hash(actual)})
    return {"implementation": NEIGHBOR_IMPLEMENTATION, "seed": seed, "checks": checks,
            "reference": "original float32 dense @ and stable argsort; synthetic only"}


def three_losses(predicted_center, true_center, predicted_global, true_global,
                 predicted_local, true_local):
    """MAE regression and global/local cosine-distance discrepancies.

    center/global shapes: [batch, dim]. local: [batch, samples, dim].
    Each term uses a mean reduction, including the regression's coordinates.
    Predicted/true tensors must already contain unit rows.
    """
    import torch
    regression = torch.mean(torch.abs(predicted_center - true_center))
    # |(1-cos(pred)) - (1-cos(true))| equals the absolute cosine gap.
    global_loss = torch.mean(torch.abs(
        (predicted_center * predicted_global).sum(-1)
        - (true_center * true_global).sum(-1)))
    local_loss = torch.mean(torch.abs(
        (predicted_center[:, None, :] * predicted_local).sum(-1)
        - (true_center[:, None, :] * true_local).sum(-1)))
    return regression, global_loss, local_loss


def _array_hash(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def _state_hash(model) -> str:
    result = hashlib.sha256()
    for name, tensor in model.state_dict().items():
        result.update(name.encode())
        result.update(tensor.detach().cpu().numpy().tobytes())
    return result.hexdigest()


def _file_hash(path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_torch_save(path, value) -> None:
    """Replace one durable local snapshot; a failed write leaves its predecessor."""
    import torch
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    try:
        with temporary.open("wb") as stream:
            torch.save(value, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        if os.name != "nt":
            descriptor = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


@dataclass
class FittedConverter:
    model: object
    source_dim: int
    target_dim: int
    config: ConverterConfig
    metadata: dict

    def transform(self, source: np.ndarray, *, batch_size: int | None = None,
                  raw: bool = False) -> np.ndarray:
        import torch
        source = _vectors(source, "source")
        if source.shape[1] != self.source_dim:
            raise ValueError("source dimension differs from fitted converter")
        batch_size = self.config.transform_batch_size if batch_size is None else batch_size
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        output = np.empty((len(source), self.target_dim), dtype=np.float32)
        self.model.eval()
        with torch.no_grad():
            for start in range(0, len(source), batch_size):
                stop = min(start + batch_size, len(source))
                values = torch.from_numpy(source[start:stop]).to(self.config.device)
                output[start:stop] = (self.model.layers(values) if raw else self.model(values)).cpu().numpy()
        if not np.isfinite(output).all() or (not raw and not np.allclose(
                np.linalg.norm(output, axis=1), 1, atol=1e-4, rtol=0)):
            raise RuntimeError("converter produced invalid or non-unit vectors")
        return output


def fit_converter(source_anchors: np.ndarray, target_anchors: np.ndarray, *,
                  seed: int, config: ConverterConfig | None = None,
                  validation_source: np.ndarray | None = None,
                  validation_target: np.ndarray | None = None,
                  report: Callable[[dict], None] | None = None,
                  neighbor_block_rows: int = 256,
                  checkpoint_path: str | os.PathLike | None = None,
                  resume_path: str | os.PathLike | None = None,
                  checkpoint_every: int = 5_000,
                  checkpoint_hook: Callable[[int], None] | None = None) -> FittedConverter:
    """Fit only paired anchors; final iteration is the prespecified checkpoint.

    Per update, sample 64 centers uniformly with replacement, 64 independent
    global endpoints, and one uniformly sampled neighbor per center from its
    exact target-space top100. This is an unbiased estimator of the three
    corresponding *mean-reduced* empirical objectives. It is not asserted to
    match undocumented original minibatch construction. Endpoint deduplication
    preserves gradients and bounds forward rows by batch*(2+local_samples).

    Optional disjoint anchor validation selects the earliest lowest coordinate
    MAE checkpoint at report_every intervals (and final step), while completing
    the full iteration budget. This differs from paper retrieval validation.
    Caller owns a prespecified split and any separately recorded all-anchor refit.

    Resource observations never shorten the fit. Actual numerical/OS failures
    raise; the caller preserves progress, failure metadata and process RSS trace.
    Optional atomic snapshots preserve the last completed update (before loading
    selected validation weights), Adam, sampling/Torch RNGs and full history.
    Resume accepts only this schema with identical data/configuration/runtime.
    The hook runs after each durable snapshot, for interruption smoke checks.
    """
    import torch

    config = ConverterConfig() if config is None else config
    if (isinstance(checkpoint_every, bool) or not isinstance(checkpoint_every, int)
            or checkpoint_every < 1):
        raise ValueError("checkpoint_every must be a positive integer")
    if checkpoint_hook is not None and checkpoint_path is None:
        raise ValueError("checkpoint_hook requires checkpoint_path")
    source = _vectors(source_anchors, "source_anchors")
    target = _vectors(target_anchors, "target_anchors")
    if len(source) != len(target):
        raise ValueError("paired anchor counts differ")
    if (validation_source is None) != (validation_target is None):
        raise ValueError("both validation matrices must be provided together")
    validation_old = validation_new = None
    if validation_source is not None:
        validation_old = _vectors(validation_source, "validation_source")
        validation_new = _vectors(validation_target, "validation_target")
        if (len(validation_old) != len(validation_new) or validation_old.shape[1] != source.shape[1]
                or validation_new.shape[1] != target.shape[1]):
            raise ValueError("validation pairing/dimensions differ")
    if config.device == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("requested CUDA device unavailable")
        if os.getenv("CUBLAS_WORKSPACE_CONFIG") not in (":4096:8", ":16:8"):
            raise RuntimeError("set deterministic CUBLAS_WORKSPACE_CONFIG before torch/CUDA initialization")
    import psutil
    rss_process = psutil.Process()
    start = time.perf_counter()
    peak_rss = 0
    peak_cuda_reserved = 0

    def check_resources(step):
        nonlocal peak_rss, peak_cuda_reserved
        elapsed = time.perf_counter() - start
        if rss_process is not None:
            peak_rss = max(peak_rss, rss_process.memory_info().rss)
        if config.device == "cuda":
            peak_cuda_reserved = max(peak_cuda_reserved, torch.cuda.max_memory_reserved())


    check_resources(0)
    neighbor_started = time.perf_counter()
    neighbors = target_neighbors(target, config.local_k, block_rows=neighbor_block_rows)
    neighbor_construction_seconds = time.perf_counter() - neighbor_started
    def array_identity(values):
        return None if values is None else {
            "shape": list(values.shape), "dtype": str(values.dtype), "sha256": _array_hash(values)}

    # Both supplied and defensively normalized bytes are bound to the snapshot.
    # Equal normalized directions alone are insufficient identity for recovery.
    resume_identity = {
        "method": METHOD, "config": asdict(config), "seed": seed,
        "converter_source_sha256_canonical_lf": hashlib.sha256(
            Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
        "source": array_identity(np.asarray(source_anchors)),
        "target": array_identity(np.asarray(target_anchors)),
        "normalized_source": array_identity(source), "normalized_target": array_identity(target),
        "validation_source": array_identity(None if validation_source is None else np.asarray(validation_source)),
        "validation_target": array_identity(None if validation_target is None else np.asarray(validation_target)),
        "normalized_validation_source": array_identity(validation_old),
        "normalized_validation_target": array_identity(validation_new),
        "neighbor_implementation": NEIGHBOR_IMPLEMENTATION,
        "neighbor_block_rows": neighbor_block_rows, "neighbor_sha256": _array_hash(neighbors),
        "torch_version": str(torch.__version__), "numpy_version": np.__version__,
        "cuda_runtime": torch.version.cuda if config.device == "cuda" else None,
        "cuda_device": torch.cuda.get_device_name() if config.device == "cuda" else None,
        "cublas_workspace_config": os.getenv("CUBLAS_WORKSPACE_CONFIG") if config.device == "cuda" else None,
    }
    resumed_from = None
    resume_read_seconds = checkpoint_write_seconds = 0.0
    checkpoint_writes = 0
    prior_checkpoint_observations = None
    old_threads = torch.get_num_threads()
    old_determinism = torch.are_deterministic_algorithms_enabled()
    old_warn_only = torch.is_deterministic_algorithms_warn_only_enabled()
    old_matmul_tf32 = torch.backends.cuda.matmul.allow_tf32
    old_cudnn_tf32 = torch.backends.cudnn.allow_tf32
    history = []
    rng = np.random.default_rng(seed)
    try:
        torch.set_num_threads(config.threads)
        torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        cuda_devices = [torch.cuda.current_device()] if config.device == "cuda" else []
        # fork_rng protects the caller's CPU and selected-device random states.
        with torch.random.fork_rng(devices=cuda_devices):
            torch.random.default_generator.manual_seed(seed)
            if cuda_devices:
                torch.cuda.default_generators[cuda_devices[0]].manual_seed(seed)
            model = build_model(source.shape[1], target.shape[1], config).to(config.device)
            initial_state_sha256 = _state_hash(model)
            optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate,
                                         betas=config.adam_betas, eps=config.adam_epsilon,
                                         weight_decay=0, amsgrad=False, foreach=False)
            source_tensor = torch.from_numpy(source).to(config.device)
            target_tensor = torch.from_numpy(target).to(config.device)
            validation_old_tensor = (torch.from_numpy(validation_old).to(config.device)
                                     if validation_old is not None else None)
            validation_new_tensor = (torch.from_numpy(validation_new).to(config.device)
                                     if validation_new is not None else None)
            best_validation = math.inf
            selected_step = config.iterations
            selected_state = None
            completed_step = 0
            if resume_path is not None:
                read_started = time.perf_counter()
                resolved_resume = Path(resume_path).resolve(strict=True)
                resume_sha256 = _file_hash(resolved_resume)
                # This is a caller-owned local training snapshot, never legacy
                # model weights or an untrusted downloaded pickle.
                saved = torch.load(resolved_resume, map_location="cpu", weights_only=False)
                required = {"schema", "identity", "initial_state_sha256", "model_state",
                            "optimizer_state", "numpy_rng_state", "torch_cpu_rng_state",
                            "torch_cuda_rng_state", "current_step", "history", "best_validation",
                            "selected_step", "selected_state", "observations", "resumed_from"}
                if not isinstance(saved, dict) or set(saved) != required or saved["schema"] != RESUME_SCHEMA:
                    raise ValueError("Unsupported exact-resume snapshot; legacy weights are not optimizer state")
                if saved["identity"] != resume_identity:
                    raise ValueError("Resume input/configuration/runtime identity mismatch")
                if saved["initial_state_sha256"] != initial_state_sha256:
                    raise ValueError("Resume seeded initial model identity mismatch")
                completed_step = saved["current_step"]
                if (isinstance(completed_step, bool) or not isinstance(completed_step, int)
                        or not 1 <= completed_step <= config.iterations):
                    raise ValueError("Invalid resume update index")
                expected_reports = [s for s in range(1, completed_step + 1)
                                    if s == 1 or s % config.report_every == 0 or s == config.iterations]
                history = saved["history"]
                if not isinstance(history, list) or [row["step"] for row in history] != expected_reports:
                    raise ValueError("Resume report history does not match completed updates")
                validation_rows = [row for row in history if "validation_mae" in row]
                expected_selected = (min(validation_rows, key=lambda row: row["validation_mae"])["step"]
                                     if validation_rows else config.iterations)
                expected_best = min((row["validation_mae"] for row in validation_rows), default=math.inf)
                if (saved["selected_step"] != expected_selected or saved["best_validation"] != expected_best
                        or (saved["selected_state"] is None) != (not validation_rows)):
                    raise ValueError("Resume validation selection state is inconsistent")
                model.load_state_dict(saved["model_state"], strict=True)
                optimizer.load_state_dict(saved["optimizer_state"])
                if len(optimizer.state) != len(list(model.parameters())):
                    raise ValueError("Resume Adam state is incomplete")
                for parameter in model.parameters():
                    state = optimizer.state[parameter]
                    if (set(state) != {"step", "exp_avg", "exp_avg_sq"}
                            or float(state["step"]) != completed_step
                            or state["exp_avg"].shape != parameter.shape
                            or state["exp_avg_sq"].shape != parameter.shape
                            or not bool(torch.isfinite(parameter).all())
                            or not bool(torch.isfinite(state["exp_avg"]).all())
                            or not bool(torch.isfinite(state["exp_avg_sq"]).all())):
                        raise ValueError("Resume Adam/model state is invalid")
                group = optimizer.param_groups[0]
                if (len(optimizer.param_groups) != 1 or group["lr"] != config.learning_rate
                        or group["betas"] != config.adam_betas or group["eps"] != config.adam_epsilon
                        or group["weight_decay"] != 0 or group["amsgrad"] or group["foreach"] is not False
                        or group.get("maximize", False) or group.get("capturable", False)
                        or group.get("differentiable", False) or group.get("fused", False)):
                    raise ValueError("Resume Adam configuration differs")
                best_validation = saved["best_validation"]
                selected_step = saved["selected_step"]
                selected_state = saved["selected_state"]
                rng.bit_generator.state = saved["numpy_rng_state"]
                torch.set_rng_state(saved["torch_cpu_rng_state"])
                if cuda_devices:
                    if saved["torch_cuda_rng_state"] is None:
                        raise ValueError("Resume CUDA RNG state missing")
                    torch.cuda.set_rng_state(saved["torch_cuda_rng_state"], cuda_devices[0])
                elif saved["torch_cuda_rng_state"] is not None:
                    raise ValueError("Unexpected CUDA RNG in CPU snapshot")
                prior_checkpoint_observations = saved["observations"]
                resumed_from = {"path": str(resolved_resume), "sha256": resume_sha256,
                                "current_step": completed_step, "previous_resume": saved["resumed_from"]}
                resume_read_seconds = time.perf_counter() - read_started
                del saved

            def save_resume(step):
                nonlocal checkpoint_write_seconds, checkpoint_writes
                snapshot_started = time.perf_counter()
                snapshot = {
                    "schema": RESUME_SCHEMA, "identity": resume_identity,
                    "initial_state_sha256": initial_state_sha256,
                    "model_state": model.state_dict(), "optimizer_state": optimizer.state_dict(),
                    "numpy_rng_state": rng.bit_generator.state,
                    "torch_cpu_rng_state": torch.get_rng_state(),
                    "torch_cuda_rng_state": torch.cuda.get_rng_state(cuda_devices[0]) if cuda_devices else None,
                    "current_step": step, "history": history,
                    "best_validation": best_validation, "selected_step": selected_step,
                    "selected_state": selected_state, "resumed_from": resumed_from,
                    "observations": {
                        "segment_elapsed_before_snapshot_seconds": time.perf_counter() - start,
                        "segment_write_seconds_before_snapshot": checkpoint_write_seconds,
                        "segment_writes_before_snapshot": checkpoint_writes,
                        "resume_read_seconds": resume_read_seconds,
                        "prior_checkpoint_observations": prior_checkpoint_observations,
                        "timing_semantics": "observations only; interrupted snapshot's own write duration cannot be stored inside itself",
                    },
                }
                _atomic_torch_save(checkpoint_path, snapshot)
                checkpoint_write_seconds += time.perf_counter() - snapshot_started
                checkpoint_writes += 1
                if checkpoint_hook is not None:
                    checkpoint_hook(step)

            model.train()
            for step in range(completed_step + 1, config.iterations + 1):
                check_resources(step - 1)
                center = rng.integers(len(source), size=config.batch_size)
                global_endpoint = rng.integers(len(source), size=config.batch_size)
                positions = rng.integers(config.local_k, size=(config.batch_size,
                                                              config.local_samples_per_center))
                local_endpoint = neighbors[center[:, None], positions]
                combined = np.concatenate((center, global_endpoint, local_endpoint.ravel()))
                unique, inverse = np.unique(combined, return_inverse=True)
                unique_index = torch.from_numpy(unique).to(config.device)
                inverse_index = torch.from_numpy(inverse).to(config.device)
                combined_index = torch.from_numpy(combined).to(config.device)
                predicted = model(source_tensor[unique_index])[inverse_index]
                truth = target_tensor[combined_index]
                batch = config.batch_size
                regression, global_loss, local_loss = three_losses(
                    predicted[:batch], truth[:batch], predicted[batch:2*batch], truth[batch:2*batch],
                    predicted[2*batch:].reshape(batch, config.local_samples_per_center, -1),
                    truth[2*batch:].reshape(batch, config.local_samples_per_center, -1))
                loss = regression + config.alpha * global_loss + config.beta * local_loss
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"nonfinite converter loss at step {step}")
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in model.parameters()):
                    raise FloatingPointError(f"nonfinite converter gradient at step {step}")
                optimizer.step()
                if step == 1 or step % config.report_every == 0 or step == config.iterations:
                    gradient_norm = float(torch.sqrt(sum(
                        torch.sum(p.grad.detach() ** 2) for p in model.parameters() if p.grad is not None)))
                    parameters_finite = all(bool(torch.isfinite(p).all()) for p in model.parameters())
                    if not parameters_finite:
                        raise FloatingPointError(f"nonfinite converter parameters at step {step}")
                    row = {"gradients_finite": True, "gradient_norm": gradient_norm, "gradient_nonzero": gradient_norm > 0,
                           "parameters_finite": parameters_finite,
                           "own_cuda_allocated_bytes": torch.cuda.memory_allocated() if config.device == "cuda" else 0,
                           "step": step, "loss": float(loss.detach()),
                           "regression": float(regression.detach()),
                           "global": float(global_loss.detach()), "local": float(local_loss.detach()),
                           "elapsed_seconds": time.perf_counter() - start,
                           "observed_rss_bytes": peak_rss,
                           "cuda_reserved_bytes": peak_cuda_reserved}
                    if validation_old_tensor is not None and (
                            step % config.report_every == 0 or step == config.iterations):
                        model.eval()
                        with torch.no_grad():
                            validation_mae = float(torch.mean(torch.abs(
                                model(validation_old_tensor) - validation_new_tensor)))
                        model.train()
                        if not math.isfinite(validation_mae):
                            raise FloatingPointError(f"nonfinite validation MAE at step {step}")
                        row["validation_mae"] = validation_mae
                        if validation_mae < best_validation:
                            best_validation = validation_mae
                            selected_step = step
                            selected_state = {key: value.detach().cpu().clone()
                                              for key, value in model.state_dict().items()}
                    history.append(row)
                    if report is not None:
                        report(dict(row))
                if checkpoint_path is not None and (step % checkpoint_every == 0 or step == config.iterations):
                    save_resume(step)
            # A completed imported snapshot still gets its own durable local
            # copy without any repeated update or validation computation.
            if checkpoint_path is not None and completed_step == config.iterations:
                save_resume(completed_step)
            check_resources(config.iterations)
            if selected_state is not None:
                model.load_state_dict(selected_state)
            model.eval()
    finally:
        torch.set_num_threads(old_threads)
        torch.use_deterministic_algorithms(old_determinism, warn_only=old_warn_only)
        torch.backends.cuda.matmul.allow_tf32 = old_matmul_tf32
        torch.backends.cudnn.allow_tf32 = old_cudnn_tf32
    final_state_sha256 = _state_hash(model)
    metadata = {"initial_state_sha256": initial_state_sha256,
                "final_state_sha256": final_state_sha256,
                "parameters_updated": initial_state_sha256 != final_state_sha256,
                "all_step_losses_and_gradients_finite": True,
                "method": METHOD, "implementation": "independent_paper_spec_reimplementation",
                "official_source_revision": None, "official_code_license": None,
                "paper_url": PAPER_URL, "seed": seed, "config": asdict(config),
                "anchor_count": len(source), "source_anchor_sha256": _array_hash(source),
                "target_anchor_sha256": _array_hash(target),
                "neighbor_sha256": _array_hash(neighbors),
                "neighbor_construction_seconds": neighbor_construction_seconds,
                "neighbor_implementation": NEIGHBOR_IMPLEMENTATION,
                "neighbor_block_rows": neighbor_block_rows,
                "neighbor_block_rows_semantics": "row selection grouping only; score GEMM is whole-matrix",
                "parameter_count": sum(p.numel() for p in model.parameters()),
                "completed_iterations": config.iterations, "selected_iteration": selected_step,
                "checkpoint_selection": ("earliest_best_anchor_validation_mae"
                    if validation_old is not None else "final_fixed_iteration"),
                "validation_count": 0 if validation_old is None else len(validation_old),
                "validation_source_sha256": None if validation_old is None else _array_hash(validation_old),
                "validation_target_sha256": None if validation_new is None else _array_hash(validation_new),
                "loss_reduction": "mean_coordinates_regression_mean_pairs_global_mean_neighbors_local",
                "local_neighbor_population": "paired_training_anchors_only_exclude_self_stable_ties",
                "elapsed_seconds": time.perf_counter() - start,
                "observed_peak_rss_bytes": peak_rss if rss_process is not None else None,
                "process_peak_cuda_reserved_bytes": peak_cuda_reserved if config.device == "cuda" else None,
                "resumed_from": resumed_from,
                "resume_schema": RESUME_SCHEMA,
                "resume_checkpoint_path": None if checkpoint_path is None else str(Path(checkpoint_path).resolve()),
                "checkpoint_every": checkpoint_every,
                "checkpoint_overhead_seconds": {"segment_write": checkpoint_write_seconds,
                    "segment_resume_read_verify_restore": resume_read_seconds,
                    "segment_writes": checkpoint_writes,
                    "prior_checkpoint_observations": prior_checkpoint_observations},
                "timing_semantics": "history/resources are observations in their originating process segment; resume and checkpoint overhead recorded separately",
                "torch_version": str(torch.__version__), "numpy_version": np.__version__,
                "history": history}
    return FittedConverter(model, source.shape[1], target.shape[1], config, metadata)


def synthetic_resume_parity(seed: int = 17, *, device: str = "cpu",
                            output_directory: str | os.PathLike | None = None) -> dict:
    """Qrel-free 500-update smoke, interrupted durably at update 250.

    Tiny widths keep this a recovery check rather than another full-width fit.
    Both validation selection and fresh all-pairs refit exercise the production
    snapshot/load code, with exact model/Adam/RNG/loss equality. Invoke only after
    the applicable scientific smoke protocol has been committed.
    """
    from dataclasses import replace
    import tempfile
    import torch

    def equal_state(left, right):
        if isinstance(left, torch.Tensor):
            return isinstance(right, torch.Tensor) and torch.equal(left, right)
        if isinstance(left, np.ndarray):
            return isinstance(right, np.ndarray) and np.array_equal(left, right)
        if isinstance(left, dict):
            return (isinstance(right, dict) and left.keys() == right.keys()
                    and all(equal_state(left[key], right[key]) for key in left))
        if isinstance(left, (list, tuple)):
            return (type(left) is type(right) and len(left) == len(right)
                    and all(equal_state(a, b) for a, b in zip(left, right)))
        return left == right

    class SyntheticInterruption(RuntimeError):
        pass

    rng = np.random.default_rng(seed + 173)
    source = rng.normal(size=(137, 7)).astype(np.float32)
    target = rng.normal(size=(137, 9)).astype(np.float32)
    config = ConverterConfig(hidden_multiplier=2, iterations=500, batch_size=8,
                             local_k=100, report_every=250, threads=1, device=device)
    # A temporary directory is only for callers that do not need retained smoke
    # artifacts; the worker supplies a unique preserved directory instead.
    temporary = tempfile.TemporaryDirectory() if output_directory is None else None
    directory = Path(temporary.name if temporary is not None else output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    checks = []
    try:
        for phase in ("selection", "refit"):
            train, validation = anchor_split(len(source), seed)
            arguments = ({"source_anchors": source[train], "target_anchors": target[train],
                          "validation_source": source[validation], "validation_target": target[validation]}
                         if phase == "selection" else
                         {"source_anchors": source, "target_anchors": target})
            full_path = directory / (phase + "_uninterrupted_resume.pt")
            interrupted_path = directory / (phase + "_interrupted_resume.pt")
            resumed_path = directory / (phase + "_resumed_resume.pt")
            if full_path.exists() or interrupted_path.exists() or resumed_path.exists():
                raise FileExistsError("Synthetic parity must use fresh snapshot paths")
            reference = fit_converter(**arguments, seed=seed, config=config)
            full = fit_converter(**arguments, seed=seed, config=config,
                                 checkpoint_path=full_path, checkpoint_every=250)
            def interrupt(step):
                if step == 250:
                    raise SyntheticInterruption("intentional post-checkpoint interruption at update250")
            try:
                fit_converter(**arguments, seed=seed, config=config,
                              checkpoint_path=interrupted_path, checkpoint_every=250,
                              checkpoint_hook=interrupt)
            except SyntheticInterruption:
                pass
            else:
                raise AssertionError("Synthetic fit did not interrupt")
            saved_250 = torch.load(interrupted_path, map_location="cpu", weights_only=False)
            if saved_250["current_step"] != 250:
                raise AssertionError("Interrupted snapshot is not update250")
            interrupted_sha256 = _file_hash(interrupted_path)
            changed_arguments = dict(arguments)
            changed_arguments["source_anchors"] = arguments["source_anchors"].copy()
            changed_arguments["source_anchors"][0, 0] += np.float32(.25)
            rejection_checks = {}
            for name, trial_arguments, trial_config in (
                    ("changed_config_rejected", arguments, replace(config, alpha=config.alpha + .01)),
                    ("changed_source_rejected", changed_arguments, config)):
                try:
                    fit_converter(**trial_arguments, seed=seed, config=trial_config,
                                  resume_path=interrupted_path)
                except ValueError as exc:
                    if str(exc) != "Resume input/configuration/runtime identity mismatch":
                        raise
                    rejection_checks[name] = True
                else:
                    raise AssertionError("Resume accepted drift: " + name)
            resumed = fit_converter(**arguments, seed=seed, config=config,
                                    checkpoint_path=resumed_path, resume_path=interrupted_path,
                                    checkpoint_every=250)
            final_full = torch.load(full_path, map_location="cpu", weights_only=False)
            final_resumed = torch.load(resumed_path, map_location="cpu", weights_only=False)
            numerical_keys = ("step", "loss", "regression", "global", "local", "validation_mae",
                              "gradient_norm", "gradient_nonzero", "gradients_finite", "parameters_finite")
            numerical_history = lambda fit: [{key: row[key] for key in numerical_keys if key in row}
                                             for row in fit.metadata["history"]]
            equalities = {
                **rejection_checks,
                "returned_model_bitwise_equal": equal_state(full.model.state_dict(), resumed.model.state_dict()),
                "selected_step_equal": full.metadata["selected_iteration"] == resumed.metadata["selected_iteration"],
                "initial_state_hash_equal": full.metadata["initial_state_sha256"] == resumed.metadata["initial_state_sha256"],
                "final_state_hash_equal": full.metadata["final_state_sha256"] == resumed.metadata["final_state_sha256"],
                "numerical_history_exact_equal": numerical_history(full) == numerical_history(resumed),
                "snapshot_enabled_vs_disabled_model_bitwise_equal": equal_state(
                    reference.model.state_dict(), full.model.state_dict()),
                "snapshot_enabled_vs_disabled_history_exact_equal": numerical_history(reference) == numerical_history(full),
                "snapshot_enabled_vs_disabled_selection_equal": reference.metadata["selected_iteration"] == full.metadata["selected_iteration"],
            }
            for key in ("model_state", "optimizer_state", "numpy_rng_state", "torch_cpu_rng_state",
                        "torch_cuda_rng_state", "selected_state", "selected_step", "best_validation"):
                equalities[key + "_exact_equal"] = equal_state(final_full[key], final_resumed[key])
            if not all(equalities.values()):
                raise AssertionError("Exact resume parity failed: " + repr(equalities))
            # Completed selection snapshots must also reconstruct selected
            # weights with a zero-update resume (including any earlier optimum).
            completed = fit_converter(**arguments, seed=seed, config=config, resume_path=full_path)
            if (not equal_state(full.model.state_dict(), completed.model.state_dict())
                    or numerical_history(full) != numerical_history(completed)
                    or full.metadata["selected_iteration"] != completed.metadata["selected_iteration"]):
                raise AssertionError("Completed snapshot reconstruction differs")
            equalities["completed_snapshot_zero_update_reconstruction_equal"] = True
            checks.append({"phase": phase, "iterations": 500, "interruption_step": 250,
                           "source_dim": 7, "target_dim": 9, "local_k": 100,
                           "train_rows": len(arguments["source_anchors"]),
                           "selected_iteration": full.metadata["selected_iteration"],
                           "uninterrupted_final_state_sha256": full.metadata["final_state_sha256"],
                           "resumed_final_state_sha256": resumed.metadata["final_state_sha256"],
                           "interrupted_checkpoint_sha256": interrupted_sha256,
                           "uninterrupted_snapshot_sha256": _file_hash(full_path),
                           "resumed_snapshot_sha256": _file_hash(resumed_path),
                           "equalities": equalities})
    finally:
        if temporary is not None:
            temporary.cleanup()
    return {"schema": RESUME_SCHEMA, "seed": seed, "device": device, "checks": checks,
            "comparison": "bitwise states and exact loss/selection history; timing/resources excluded",
            "scope": "tiny-width paired synthetic recovery proof; full-width model remains in worker smoke"}
