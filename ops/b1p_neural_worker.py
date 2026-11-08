"""Paired-only B1-P external neural adapters; request JSON is the only input API.

No encoder, full-target cache, qrels, ranking or scoring code is imported here.
Launch only from the separately committed B1-P protocol. There are no artificial
wall/RSS/CUDA limits; actual failures and partial artifacts remain preserved.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import datetime, timezone
import gc
import hashlib
import importlib
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
from contextlib import redirect_stdout, redirect_stderr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def dump(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def state_hash(model):
    result = hashlib.sha256()
    for name, tensor in model.state_dict().items():
        result.update(name.encode())
        result.update(tensor.detach().cpu().numpy().tobytes())
    return result.hexdigest()


class Observations:
    """Observe this process, including its own CUDA allocator, without caps."""
    def __init__(self, output):
        self.output = output
        self.stop = threading.Event()
        self.peak_rss = self.peak_allocated = self.peak_reserved = 0
        self.errors = []

    def sample(self):
        import psutil
        import torch
        row = {"unix": time.time(), "pid": os.getpid()}
        try:
            rss = psutil.Process().memory_info().rss
            self.peak_rss = max(self.peak_rss, rss)
            row.update(process_rss_bytes=rss, host_available_memory_bytes=psutil.virtual_memory().available,
                       host_cpu_percent=psutil.cpu_percent(interval=None))
            if torch.cuda.is_initialized():
                self.peak_allocated = max(self.peak_allocated, torch.cuda.max_memory_allocated())
                self.peak_reserved = max(self.peak_reserved, torch.cuda.max_memory_reserved())
                row.update(own_cuda_allocated_bytes=torch.cuda.memory_allocated(),
                           own_cuda_reserved_bytes=torch.cuda.memory_reserved(),
                           own_peak_cuda_allocated_bytes=self.peak_allocated,
                           own_peak_cuda_reserved_bytes=self.peak_reserved)
        except Exception as exc:
            row["observation_error"] = repr(exc)
            self.errors.append(repr(exc))
        with (self.output / "resource_trace.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, allow_nan=False) + "\n")

    def begin(self):
        self.sample()
        def loop():
            while not self.stop.wait(1):
                self.sample()
        self.thread = threading.Thread(target=loop, daemon=True)
        self.thread.start()

    def end(self):
        self.stop.set()
        self.thread.join()
        self.sample()


def identity(lock, request, record):
    """Pin deployed code, the immutable protocol lock, environment and versions."""
    # Load GPU numpy/torch first; fallback paths can supply missing auxiliary
    # dependencies but cannot replace this environment's numerical packages.
    import numpy as np
    import torch
    for path in lock.get("dependency_fallbacks", []):
        if path not in sys.path:
            sys.path.append(path)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != request["code_commit"]:
        raise ValueError("Deployment commit mismatch")
    if subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True).strip():
        raise ValueError("Dirty tracked deployment source")
    actual_sources = {}
    for relative, expected in lock["source_sha256_canonical_lf"].items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("Locked source escapes repository")
        digest = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        actual_sources[relative] = digest
        if digest != expected:
            raise ValueError("Source drift: " + relative)
    environment = {key: os.environ.get(key) for key in lock["environment"]}
    if environment != lock["environment"]:
        raise ValueError("Locked environment drift")
    if environment.get("CUBLAS_WORKSPACE_CONFIG") not in (":4096:8", ":16:8"):
        raise ValueError("Deterministic CUBLAS configuration is required")
    modules = {}
    for name, expected in lock["gpu_versions"].items():
        module = importlib.import_module(name)
        version = str(module.__version__)
        modules[name] = {"version": version, "file": module.__file__}
        if version != expected:
            raise ValueError("GPU dependency version drift: " + name)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable")
    if lock.get('execution_device'):
        spec=lock['execution_device']
        if (torch.cuda.get_device_name(0)!=spec['name'] or
                torch.cuda.get_device_properties(0).total_memory!=spec['total_memory_bytes']):
            raise RuntimeError('Deployment MIG identity differs from committed device')
        listing=subprocess.check_output(['nvidia-smi','-L'],text=True)
        expected_uuid=spec.get('mig_uuid') or spec['gpu_uuid']
        if expected_uuid not in listing:
            raise RuntimeError('Assigned GPU/MIG UUID differs from committed device')
    torch.set_num_threads(4)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.cuda.reset_peak_memory_stats()
    record.update(code_commit=head, source_sha256_canonical_lf=actual_sources,
                  environment=environment, modules=modules, cuda_runtime=torch.version.cuda,
                  device=torch.cuda.get_device_name(0), numpy_build=str(np.__config__.CONFIG))


def inputs(request, lock, record):
    import numpy as np
    from arc2_global.embedding_converter import _vectors
    allowed = {"mode", "method", "regime", "seed", "lockpath", "output", "paired_source",
               "paired_target", "full_source", "code_commit", "input_sha256"}
    if set(request) not in (allowed, allowed | {"resume_checkpoints"}):
        raise ValueError("Request keys must exactly match the paired-only API: " + repr(sorted(set(request) ^ allowed)))
    if request["mode"] not in ("smoke", "full") or request["method"] not in ("embedding_converter", "simplelinear"):
        raise ValueError("Invalid mode/method")
    if request["regime"] not in ("anchors", "all_paid") or request["seed"] not in [17, 29, 41, 53, 67]:
        raise ValueError("Invalid regime/seed")
    if "resume_checkpoints" in request:
        checkpoints = request["resume_checkpoints"]
        if (request["method"] != "embedding_converter" or not isinstance(checkpoints, dict)
                or not checkpoints or not set(checkpoints) <= {"selection", "refit"}):
            raise ValueError("Only paired converter selection/refit resume checkpoints are supported")
        manifest = {}
        for phase, value in checkpoints.items():
            if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
                raise ValueError("Resume checkpoint must specify exactly path and sha256")
            path = Path(value["path"]).resolve(strict=True)
            digest = sha(path)
            if digest != value["sha256"]:
                raise ValueError("Resume checkpoint hash drift: " + phase)
            manifest[phase] = {"path": str(path), "sha256": digest}
        record["requested_resume_checkpoints"] = manifest
    arrays = {}
    manifest = {}
    for name in ("paired_source", "paired_target", "full_source"):
        path = Path(request[name]).resolve(strict=True)
        actual = sha(path)
        if actual != request["input_sha256"][name]:
            raise ValueError("Input hash drift: " + name)
        array = np.load(path, mmap_mode="r", allow_pickle=False)
        # Original converter defensive normalization is retained inside the fit;
        # this validation does not mutate or substitute the mmap's stored bytes.
        _vectors(array, name)
        arrays[name] = array
        manifest[name] = {"path": str(path), "sha256": actual, "shape": list(array.shape), "dtype": str(array.dtype)}
    x, y, full = (arrays[name] for name in ("paired_source", "paired_target", "full_source"))
    if len(x) != len(y) or x.shape[1] != 384 or y.shape[1] != 768 or full.shape[1] != 384:
        raise ValueError("Pairing or frozen 384-to-768 dimensions differ")
    expected = 128 if request["mode"] == "smoke" else (1024 if request["regime"] == "anchors" else 28819)
    if len(x) != expected:
        raise ValueError("Paired row count differs from locked regime")
    record.update(inputs=manifest, fit_pairs=len(x), new_qrel_reads=0,
                  target_population="supplied paired rows only; no unpaid target or qrels API")
    return x, y, full


def progress(output, phase):
    def append(row):
        with (output / (phase + "_progress.jsonl")).open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
    return append


def checkpoint(output, phase, fitted):
    import torch
    value = {"state_dict": fitted.model.state_dict(), "metadata": fitted.metadata}
    with (output / (phase + "_checkpoint.pt")).open("xb") as stream:
        torch.save(value, stream)
    dump(output / (phase + "_fit.json"), fitted.metadata)
    if not all(bool(torch.isfinite(p).all()) for p in fitted.model.parameters()):
        raise FloatingPointError("Nonfinite checkpoint parameters")
    history = fitted.metadata["history"]
    if (not history or not fitted.metadata["all_step_losses_and_gradients_finite"]
            or not all(row["parameters_finite"] and row["gradients_finite"]
                       and __import__("math").isfinite(row["loss"]) for row in history)):
        raise FloatingPointError("Checkpoint health requires finite parameters, losses and gradients")
    if not history[0]["gradient_nonzero"] or not fitted.metadata["parameters_updated"]:
        raise FloatingPointError("Checkpoint health requires nonzero initial gradient and changed parameters")
    return {"checkpoint_sha256": sha(output / (phase + "_checkpoint.pt")),
            "state_sha256": state_hash(fitted.model), "reported_checkpoints": len(history),
            "losses_finite": all(__import__("math").isfinite(row["loss"]) for row in history),
            "parameters_finite": True, "all_step_losses_and_gradients_finite": True,
            "initial_gradient_nonzero": True, "parameters_updated": True,
            "initial_state_sha256": fitted.metadata["initial_state_sha256"],
            "final_state_sha256": fitted.metadata["final_state_sha256"],
            "late_zero_gradient_allowed": True}


def resume_checkpoint(output, phase, request, record):
    """Prefer a worker's own durable snapshot; otherwise verify an explicit one.

    Fresh worker directories remain mandatory. Recovery from another worker is
    opt-in through path+hash, and converter.fit_converter independently verifies
    the exact-resume schema and all numerical input/configuration identities.
    """
    own = output / (phase + "_resume.pt")
    requested = request.get("resume_checkpoints", {}).get(phase)
    if own.exists():
        chosen = own
        digest = sha(chosen)
        origin = "own_worker_snapshot"
    elif requested is not None:
        chosen = Path(requested["path"]).resolve(strict=True)
        digest = sha(chosen)
        if digest != requested["sha256"]:
            raise ValueError("Resume checkpoint changed before fit: " + phase)
        origin = "explicit_hashed_snapshot"
    else:
        return own, None
    record.setdefault("resume_checkpoints_used", {})[phase] = {
        "path": str(chosen), "sha256": digest, "origin": origin}
    dump(output / "metadata.json", record)
    return own, chosen


def fit_embedding_converter(x, y, request, lock, output, record):
    import numpy as np
    import torch
    from arc2_global import embedding_converter as converter
    cfg_dict = dict(lock["converter_config"])
    cfg_dict["adam_betas"] = tuple(cfg_dict["adam_betas"])
    config = converter.ConverterConfig(**cfg_dict)
    frozen = converter.ConverterConfig(device="cuda")
    if asdict(config) != asdict(frozen):
        raise ValueError("Full converter configuration differs from preserved paper-spec baseline")
    if request["mode"] == "smoke":
        if lock["smoke_converter_iterations"] != 500:
            raise ValueError("Smoke is fixed to 500 updates with unchanged full width/loss/k")
        config = replace(config, iterations=500)
        record["neighbor_synthetic_parity"] = converter.synthetic_neighbor_parity(request["seed"])
        dump(output / "neighbor_parity.json", record["neighbor_synthetic_parity"])
        record["resume_synthetic_parity"] = converter.synthetic_resume_parity(
            request["seed"], device="cuda", output_directory=output / "resume_synthetic")
        dump(output / "resume_parity.json", record["resume_synthetic_parity"])
    train, validation = converter.anchor_split(len(x), request["seed"])
    np.save(output / "train_positions.npy", train, allow_pickle=False)
    np.save(output / "validation_positions.npy", validation, allow_pickle=False)
    record.update(train_count=len(train), validation_count=len(validation), config=asdict(config),
                  validation_policy="default_rng(seed+20261025); first floor(N/8) validation; rest training; earliest minimum MAE at 250-step checkpoints",
                  refit_policy="fresh model and Adam; same seed; selected_iteration updates; every supplied paired row",
                  durable_resume_policy="exact model+Adam+NumPy/Torch RNG; every5000 updates full/every250 smoke and final; identical paired inputs/configuration/runtime required",
                  independent_paper_spec_adaptation=True)
    dump(output / "metadata.json", record)
    checkpoint_every = 250 if request["mode"] == "smoke" else 5_000
    selection_checkpoint, selection_resume = resume_checkpoint(output, "selection", request, record)
    selected = converter.fit_converter(np.asarray(x[train]), np.asarray(y[train]), seed=request["seed"],
        config=config, validation_source=np.asarray(x[validation]), validation_target=np.asarray(y[validation]),
        report=progress(output, "selection"), neighbor_block_rows=lock["neighbor_block_rows"],
        checkpoint_path=selection_checkpoint, resume_path=selection_resume, checkpoint_every=checkpoint_every)
    record["selection_health"] = checkpoint(output, "selection", selected)
    selected_iteration = int(selected.metadata["selected_iteration"])
    # Selection always completes its entire budget. Refit duration is chosen
    # solely by the earliest minimum held-out paired-vector coordinate MAE.
    if selected.metadata["completed_iterations"] != config.iterations:
        raise AssertionError("Incomplete selection budget")
    record.update(selected_iteration=selected_iteration, selection_seconds=selected.metadata["elapsed_seconds"])
    # Persist selection before the potentially long all-pairs refit, including
    # exact-resume provenance/overhead already written to selection_fit.json.
    dump(output / "metadata.json", record)
    del selected
    gc.collect()
    torch.cuda.empty_cache()
    refit_checkpoint, refit_resume = resume_checkpoint(output, "refit", request, record)
    fitted = converter.fit_converter(np.asarray(x), np.asarray(y), seed=request["seed"],
        config=replace(config, iterations=selected_iteration), report=progress(output, "refit"),
        neighbor_block_rows=lock["neighbor_block_rows"], checkpoint_path=refit_checkpoint,
        resume_path=refit_resume, checkpoint_every=checkpoint_every)
    record["refit_health"] = checkpoint(output, "refit", fitted)
    record.update(refit_iterations=selected_iteration, refit_seconds=fitted.metadata["elapsed_seconds"])
    return fitted


def fit_simplelinear(x, y, request, lock, output, record):
    import numpy as np
    import torch
    from arc2_global.baseline_adapters import fit_simplelinear as fit, official_components
    defaults = lock["simplelinear_defaults"]
    _, _, _, _, Model = official_components(lock["upstream"], lock["upstream_raw_sha256"], lock["dependency_fallbacks"])
    # Initial state is diagnostic only, with the same official model constructor
    # and seed; fit below resets the seed exactly as the validated adapter does.
    torch.manual_seed(request["seed"])
    initial = Model(384, 768, hidden_dim=defaults["hidden_dim"], layer_num=defaults["layer_num"],
                    activation=defaults["activation"]).to("cuda")
    initial_hash = state_hash(initial)
    bx = torch.from_numpy(np.asarray(x[:64]).copy()).to("cuda")
    by = torch.from_numpy(np.asarray(y[:64]).copy()).to("cuda")
    initial_prediction = initial(bx)
    initial_loss = (torch.nn.functional.mse_loss(initial_prediction, by)
                    + .5 * (1-torch.nn.functional.cosine_similarity(initial_prediction, by, dim=1).mean()))
    initial_loss.backward()
    initial_gradients = [p.grad for p in initial.parameters()]
    if not bool(torch.isfinite(initial_loss)) or any(g is None or not bool(torch.isfinite(g).all()) for g in initial_gradients):
        raise FloatingPointError("Invalid official initial loss/gradients")
    initial_gradient_norm = float(torch.sqrt(sum(torch.sum(g.detach()**2) for g in initial_gradients)))
    if initial_gradient_norm <= 0:
        raise FloatingPointError("Zero official initial gradient")
    initial_loss_value = float(initial_loss.detach())
    del initial, initial_prediction, initial_loss, initial_gradients
    gc.collect()
    began = time.perf_counter()
    from loguru import logger
    log_sink = logger.add(str(output / "official_loguru.log"), enqueue=False, backtrace=False, diagnose=False)
    try:
        with (output / "official_training_raw.log").open("x", encoding="utf-8", buffering=1) as log:
            with redirect_stdout(log), redirect_stderr(log):
                fitted = fit(np.asarray(x), np.asarray(y), seed=request["seed"], device="cuda",
                    upstream=lock["upstream"], source_hashes=lock["upstream_raw_sha256"],
                    expected_defaults=defaults, dependency_fallbacks=lock["dependency_fallbacks"])
    finally:
        logger.remove(log_sink)
    mapper = fitted.mapper
    model = mapper.model
    if not all(bool(torch.isfinite(p).all()) for p in model.parameters()):
        raise FloatingPointError("Nonfinite official model parameters")
    final_hash = state_hash(model)
    if initial_hash == final_hash:
        raise AssertionError("Official fit did not update model parameters")
    # Independent post-fit gradient health has no optimizer update or impact on
    # saved model parameters, predictions or official training trajectory.
    bx = torch.from_numpy(np.asarray(x[:64]).copy()).to("cuda")
    by = torch.from_numpy(np.asarray(y[:64]).copy()).to("cuda")
    model.zero_grad(set_to_none=True)
    loss = mapper._combined_loss(model(bx), by)
    if not bool(torch.isfinite(loss)):
        raise FloatingPointError("Nonfinite official post-fit loss")
    loss.backward()
    gradients = [p.grad for p in model.parameters()]
    if any(g is None or not bool(torch.isfinite(g).all()) for g in gradients):
        raise FloatingPointError("Missing/nonfinite official gradients")
    gradient_norm = float(torch.sqrt(sum(torch.sum(g.detach()**2) for g in gradients)))
    health = {"initial_loss": initial_loss_value, "initial_gradient_norm": initial_gradient_norm,
              "initial_gradients_finite_nonzero": True,
              "initial_state_sha256": initial_hash, "final_state_sha256": final_hash,
              "parameters_updated": True, "parameters_finite": True, "postfit_loss": float(loss.detach()),
              "gradient_norm": gradient_norm, "gradients_finite": True,
              "late_zero_gradient_allowed": True}
    model.zero_grad(set_to_none=True)
    with (output / "refit_checkpoint.pt").open("xb") as stream:
        torch.save({"state_dict": model.state_dict(), "optimizer": mapper.optimizer.state_dict(),
                    "scheduler": mapper.scheduler.state_dict(), "metadata": mapper.metadata,
                    "configuration": fitted.configuration}, stream)
    dump(output / "refit_fit.json", {"official_metadata": mapper.metadata, "configuration": fitted.configuration,
                                      "health": health, "fit_wall_seconds": time.perf_counter()-began})
    record.update(refit_health=health, refit_seconds=time.perf_counter()-began,
                  configuration=fitted.configuration, policy="official fixed final epoch; 50 epochs; all supplied pairs; no validation selection")
    return fitted


def mapping(fitted, full, request, output, record):
    import numpy as np
    import torch
    from arc2_global.numerics import normalize_rows
    began = time.perf_counter()
    raw = np.lib.format.open_memmap(output / "raw_proxy_full.npy", mode="w+", dtype=np.float32, shape=(len(full), 768))
    proxy = np.lib.format.open_memmap(output / "proxy_full.npy", mode="w+", dtype=np.float32, shape=(len(full), 768))
    for start in range(0, len(full), 256):
        stop = min(start+256, len(full))
        source = np.asarray(full[start:stop])
        if request["method"] == "embedding_converter":
            raw[start:stop] = fitted.transform(source, raw=True)
            proxy[start:stop] = fitted.transform(source)
        else:
            raw[start:stop] = fitted.transform_raw(source)
            proxy[start:stop] = normalize_rows(raw[start:stop])
        if not np.isfinite(raw[start:stop]).all() or not np.isfinite(proxy[start:stop]).all():
            raise FloatingPointError("Nonfinite mapped rows")
        if not np.allclose(np.linalg.norm(proxy[start:stop], axis=1), 1, atol=1e-4, rtol=0):
            raise FloatingPointError("Nonunit proxy rows")
    raw.flush()
    proxy.flush()
    record.update(mapping_seconds=time.perf_counter()-began, proxy_rows=len(full), transform_batch_size=256,
                  raw_proxy_semantics="pre-final-normalization MLP output" if request["method"] == "embedding_converter" else "official mapper direct transform output",
                  own_peak_cuda_allocated_bytes=torch.cuda.max_memory_allocated(),
                  own_peak_cuda_reserved_bytes=torch.cuda.max_memory_reserved())
    del raw, proxy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    output = Path(request["output"]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    began = time.perf_counter()
    record = {"status": "RUNNING", "method": request.get("method"), "regime": request.get("regime"),
              "mode": request.get("mode"), "seed": request.get("seed"), "failures": [],
              "started_utc": datetime.now(timezone.utc).isoformat(), "request_sha256": sha(args.request),
              "new_qrel_reads": 0, "unpaid_target_reads": 0, "artificial_time_or_memory_caps": None,
              "python": sys.version, "executable": sys.executable, "platform": platform.platform(), "host": platform.node()}
    dump(output / "metadata.json", record)
    monitor = Observations(output)
    monitor_started = False
    def interrupted(signum, frame):
        raise RuntimeError(f"Received signal {signum}")
    signal.signal(signal.SIGTERM, interrupted)
    try:
        lockpath = Path(request["lockpath"])
        lock = json.loads(lockpath.read_text(encoding="utf-8"))
        record["lock_sha256"] = sha(lockpath)
        dump(output / "lock_copy.json", lock)
        dump(output / "request_copy.json", request)
        identity(lock, request, record)
        monitor.begin()
        monitor_started = True
        x, y, full = inputs(request, lock, record)
        if request["method"] == "embedding_converter":
            fitted = fit_embedding_converter(x, y, request, lock, output, record)
        else:
            fitted = fit_simplelinear(x, y, request, lock, output, record)
        mapping(fitted, full, request, output, record)
        record["status"] = "B1P_NEURAL_" + request["mode"].upper() + "_PASS"
    except BaseException as exc:
        record.update(status="FAILED_PRESERVED", failures=[repr(exc)], traceback=traceback.format_exc())
    finally:
        if monitor_started:
            monitor.end()
        record.update(wall_seconds=time.perf_counter()-began, peak_process_rss_bytes=monitor.peak_rss,
                      resource_observation_errors=monitor.errors, ended_utc=datetime.now(timezone.utc).isoformat())
        record["artifacts"] = {str(p.relative_to(output)): {"sha256": sha(p), "bytes": p.stat().st_size}
                               for p in sorted(output.rglob("*")) if p.is_file() and p != output / "metadata.json"}
        dump(output / "metadata.json", record)
    print(json.dumps({"status": record["status"], "failures": record["failures"]}))
    return 1 if record["status"] == "FAILED_PRESERVED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
