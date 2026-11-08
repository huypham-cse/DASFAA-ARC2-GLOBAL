"""Inspect a caller-owned B1-P snapshot or make a verified CPU handoff derivative.

This is serialization infrastructure, not a training/resume implementation. It
never imports the converter or performs optimizer updates. Use only with owned
snapshots: the exact-resume format requires torch.load(weights_only=False).
Scientific continuation still requires its separately committed protocol.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import tempfile


SCHEMA = "embedding_converter_exact_resume_v1"
SOURCE_DEVICE = "NVIDIA H100 80GB HBM3 MIG 2g.20gb"
DESTINATION_DEVICE = "NVIDIA H100 80GB HBM3"
REQUIRED_KEYS = {
    "schema", "identity", "initial_state_sha256", "model_state",
    "optimizer_state", "numpy_rng_state", "torch_cpu_rng_state",
    "torch_cuda_rng_state", "current_step", "history", "best_validation",
    "selected_step", "selected_state", "observations", "resumed_from",
}
IDENTITY_KEYS = {
    "method", "config", "seed", "converter_source_sha256_canonical_lf",
    "source", "target", "normalized_source", "normalized_target",
    "validation_source", "validation_target", "normalized_validation_source",
    "normalized_validation_target", "neighbor_implementation",
    "neighbor_block_rows", "neighbor_sha256", "torch_version", "numpy_version",
    "cuda_runtime", "cuda_device", "cublas_workspace_config",
}
QUALIFICATION = (
    "Exact state handoff: every original field is preserved except identity.cuda_device; "
    "tensor values are bitwise preserved in CPU serialization. Subsequent numerical "
    "trajectory on the destination device is not claimed bitwise identical to an "
    "uninterrupted MIG run."
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest_stream(stream):
    stream.seek(0)
    result = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        result.update(chunk)
    stream.seek(0)
    return result.hexdigest()


def digest_file(path):
    with path.open("rb") as stream:
        return digest_stream(stream)


def load_cpu(stream, torch):
    placements = Counter()

    def map_storage(storage, location):
        # torch.load initially deserializes storage on CPU. Returning it avoids
        # CUDA allocation while retaining an inventory of original device tags.
        placements[location] += 1
        return storage

    return torch.load(stream, map_location=map_storage, weights_only=False), dict(placements)


def validate_snapshot(saved, torch):
    """Check the frozen format and the same step/selection/Adam invariants as fit."""
    require(isinstance(saved, dict) and set(saved) == REQUIRED_KEYS,
            "Unsupported exact-resume top-level keys")
    require(saved["schema"] == SCHEMA, "Unsupported exact-resume schema")
    identity = saved["identity"]
    require(isinstance(identity, dict) and set(identity) == IDENTITY_KEYS,
            "Unsupported exact-resume identity keys")
    require(identity["cuda_device"] == SOURCE_DEVICE, "Source is not the authorized original MIG identity")
    require(identity["method"] == "embedding_converter_paper_spec_paired_budget",
            "Unexpected converter method")
    require(identity["neighbor_implementation"] == "dense_float32_scores_stable_topk_r1",
            "Unexpected neighbor implementation")
    config = identity["config"]
    require(isinstance(config, dict) and config.get("device") == "cuda"
            and type(config.get("iterations")) is int and config["iterations"] == 50_000,
            "Expected the original CUDA 50000-update configuration")
    for field in ("converter_source_sha256_canonical_lf", "neighbor_sha256"):
        require(isinstance(identity[field], str) and re.fullmatch(r"[0-9a-f]{64}", identity[field]),
                f"Invalid original identity hash: {field}")
    require(isinstance(saved["initial_state_sha256"], str)
            and re.fullmatch(r"[0-9a-f]{64}", saved["initial_state_sha256"]),
            "Invalid initial state hash")
    step = saved["current_step"]
    # The converter itself rejects step zero as an exact-resume input.
    require(type(step) is int and 1 <= step <= config["iterations"], "Invalid completed update index")
    interval = config.get("report_every")
    require(type(interval) is int and interval > 0, "Invalid report interval")
    expected = [s for s in range(1, step + 1)
                if s == 1 or s % interval == 0 or s == config["iterations"]]
    history = saved["history"]
    require(isinstance(history, list) and all(isinstance(row, dict) for row in history)
            and [row.get("step") for row in history] == expected, "Inconsistent completed history")
    rows = [row for row in history if "validation_mae" in row]
    require(all(math.isfinite(row["validation_mae"]) for row in rows), "Nonfinite validation history")
    selected = min(rows, key=lambda row: row["validation_mae"])["step"] if rows else config["iterations"]
    best = min((row["validation_mae"] for row in rows), default=math.inf)
    require(type(saved["selected_step"]) is int and saved["selected_step"] == selected
            and saved["best_validation"] == best
            and (saved["selected_state"] is None) == (not rows), "Inconsistent validation selection")
    model = saved["model_state"]
    optimizer = saved["optimizer_state"]
    require(isinstance(model, dict) and bool(model), "Missing model state")
    require(isinstance(optimizer, dict) and set(optimizer) == {"state", "param_groups"},
            "Unexpected Adam state keys")
    groups = optimizer["param_groups"]
    require(isinstance(groups, list) and len(groups) == 1, "Expected one Adam parameter group")
    group = groups[0]
    parameters = group["params"]
    states = optimizer["state"]
    require(isinstance(parameters, list) and len(parameters) == len(set(parameters))
            and len(parameters) == len(model) and set(states) == set(parameters), "Incomplete Adam state")
    for parameter, tensor in zip(parameters, model.values()):
        state = states[parameter]
        require(isinstance(tensor, torch.Tensor) and bool(torch.isfinite(tensor).all()), "Invalid model tensor")
        require(isinstance(state, dict) and set(state) == {"step", "exp_avg", "exp_avg_sq"},
                "Unexpected Adam parameter state")
        require(isinstance(state["step"], torch.Tensor) and state["step"].numel() == 1
                and float(state["step"]) == step, "Adam update count differs from current_step")
        for field in ("exp_avg", "exp_avg_sq"):
            value = state[field]
            require(isinstance(value, torch.Tensor) and value.shape == tensor.shape
                    and bool(torch.isfinite(value).all()), f"Invalid Adam {field}")
    require(group["lr"] == config["learning_rate"] and group["betas"] == config["adam_betas"]
            and group["eps"] == config["adam_epsilon"] and group["weight_decay"] == 0
            and group["amsgrad"] is False and group["foreach"] is False
            and not any(group.get(key, False) for key in
                        ("maximize", "capturable", "differentiable", "fused")), "Adam configuration differs")
    if saved["selected_state"] is not None:
        selected_state = saved["selected_state"]
        require(isinstance(selected_state, dict) and list(selected_state) == list(model), "Incomplete selected model")
        for key, value in selected_state.items():
            require(isinstance(value, torch.Tensor) and value.shape == model[key].shape
                    and value.dtype == model[key].dtype and bool(torch.isfinite(value).all()),
                    f"Invalid selected model tensor: {key}")
    for key in ("torch_cpu_rng_state", "torch_cuda_rng_state"):
        value = saved[key]
        require(isinstance(value, torch.Tensor) and value.dtype == torch.uint8
                and value.ndim == 1 and value.numel() > 0, f"Missing or invalid {key}")
    require(isinstance(saved["numpy_rng_state"], dict), "Missing NumPy RNG state")


def compare_exact(original, derivative, torch, np, path="snapshot", tensors=None):
    """Recursively compare types, scalar/array bytes, tensors, and mapping metadata."""
    if tensors is None:
        tensors = []
    if path == "snapshot.identity.cuda_device":
        require(original == SOURCE_DEVICE and derivative == DESTINATION_DEVICE,
                "Unauthorized identity change")
        return tensors
    require(type(original) is type(derivative), f"Type changed at {path}")
    if isinstance(original, torch.Tensor):
        require(original.device.type == derivative.device.type == "cpu"
                and original.layout == derivative.layout == torch.strided
                and original.dtype == derivative.dtype and original.shape == derivative.shape
                and original.stride() == derivative.stride()
                and original.requires_grad == derivative.requires_grad, f"Tensor metadata changed at {path}")
        before = original.detach().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()
        after = derivative.detach().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()
        require(torch.equal(original, derivative) and before == after, f"Tensor values/bytes changed at {path}")
        tensors.append({"path": path, "dtype": str(original.dtype), "shape": list(original.shape),
                        "sha256": hashlib.sha256(before).hexdigest(), "bytes": len(before)})
    elif isinstance(original, dict):
        require(list(original) == list(derivative), f"Mapping keys/order changed at {path}")
        for key in original:
            compare_exact(original[key], derivative[key], torch, np, f"{path}.{key}", tensors)
        if hasattr(original, "__dict__") or hasattr(derivative, "__dict__"):
            compare_exact(vars(original) if hasattr(original, "__dict__") else {},
                          vars(derivative) if hasattr(derivative, "__dict__") else {},
                          torch, np, f"{path}.__metadata__", tensors)
    elif isinstance(original, (list, tuple)):
        require(len(original) == len(derivative), f"Sequence length changed at {path}")
        for index, (before, after) in enumerate(zip(original, derivative)):
            compare_exact(before, after, torch, np, f"{path}[{index}]", tensors)
    elif isinstance(original, (np.ndarray, np.generic)):
        require(original.dtype == derivative.dtype and original.shape == derivative.shape
                and not original.dtype.hasobject and original.tobytes() == derivative.tobytes(),
                f"NumPy value changed at {path}")
    elif isinstance(original, float):
        require(struct.pack("!d", original) == struct.pack("!d", derivative), f"Float bytes changed at {path}")
    elif original is None or isinstance(original, (bool, int, str, bytes)):
        require(original == derivative, f"Value changed at {path}")
    else:
        raise ValueError(f"Unsupported snapshot value type at {path}: {type(original).__name__}")
    return tensors


def stage_file(destination, writer):
    """Durably stage without replacing anything; retain partial files on faults."""
    descriptor, name = tempfile.mkstemp(prefix=destination.name + ".partial-", dir=destination.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            writer(stream)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        print(f"Write failed; partial artifact preserved: {temporary}", file=sys.stderr)
        raise
    return temporary


def publish_exclusive(temporary, destination):
    # Hard-link publication is atomic and refuses even a concurrently created
    # destination. Both paths are in the same directory/filesystem.
    os.link(temporary, destination)
    if os.name != "nt":
        descriptor = os.open(destination.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True, help="Trusted SHA-256 of the frozen owned input")
    parser.add_argument("--inspect-only", action="store_true", help="Print JSON header; write no artifacts")
    parser.add_argument("--output", type=Path, help="Exclusive new derivative checkpoint path")
    parser.add_argument("--receipt", type=Path, help="Exclusive new JSON verification receipt path")
    parser.add_argument("--destination-device-name", choices=[DESTINATION_DEVICE])
    args = parser.parse_args()
    if args.inspect_only:
        if any(value is not None for value in (args.output, args.receipt, args.destination_device_name)):
            parser.error("--inspect-only cannot be combined with output, receipt, or destination options")
    elif any(value is None for value in (args.output, args.receipt, args.destination_device_name)):
        parser.error("handoff requires --output, --receipt, and --destination-device-name")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", args.expected_sha256):
        parser.error("--expected-sha256 must contain exactly 64 hexadecimal characters")
    source = args.source.resolve(strict=True)
    expected_hash = args.expected_sha256.lower()
    if not args.inspect_only:
        output = args.output.absolute()
        receipt = args.receipt.absolute()
        require(len({os.path.normcase(str(path.resolve())) for path in (source, output, receipt)}) == 3,
                "Source, output, and receipt must be distinct paths")
        for path in (output, receipt):
            require(path.parent.is_dir() and not os.path.lexists(path), f"Output must be new in an existing directory: {path}")
    # Verify before importing Torch and, crucially, before unpickling the owned file.
    with source.open("rb") as stream:
        require(digest_stream(stream) == expected_hash, "Source SHA-256 mismatch; nothing loaded or written")
        import torch
        import numpy as np
        saved, placements = load_cpu(stream, torch)
        require(digest_stream(stream) == expected_hash, "Source changed during load")
    validate_snapshot(saved, torch)
    header = {"schema": SCHEMA, "source": str(source), "source_sha256": expected_hash,
              "identity": saved["identity"], "current_step": saved["current_step"],
              "selected_step": saved["selected_step"], "history_rows": len(saved["history"]),
              "serialized_storage_locations": placements, "loaded_tensor_device": "cpu"}
    if args.inspect_only:
        require(digest_file(source) == expected_hash, "Source changed during inspection")
        print(json.dumps(header, indent=2, allow_nan=False))
        return
    derivative = dict(saved)
    derivative["identity"] = dict(saved["identity"], cuda_device=args.destination_device_name)
    before_tensors = compare_exact(saved, derivative, torch, np)
    temporary = stage_file(output, lambda stream: torch.save(derivative, stream))
    try:
        derivative_hash = digest_file(temporary)
        with temporary.open("rb") as stream:
            reloaded, derivative_placements = load_cpu(stream, torch)
        after_tensors = compare_exact(saved, reloaded, torch, np)
        require(before_tensors == after_tensors, "Tensor inventory differs after serialization")
        require(digest_file(temporary) == derivative_hash, "Derivative changed during verification")
        require(digest_file(source) == expected_hash, "Original source changed; derivative not published")
        record = {"receipt_schema": "b1p_checkpoint_device_handoff_v1",
                  "created_utc": datetime.now(timezone.utc).isoformat(),
                  "source": str(source), "source_sha256": expected_hash,
                  "derivative": str(output), "derivative_sha256": derivative_hash,
                  "checkpoint_schema": SCHEMA, "original_identity": saved["identity"],
                  "derivative_identity": reloaded["identity"], "changed_fields": ["identity.cuda_device"],
                  "current_step": saved["current_step"], "selected_step": saved["selected_step"],
                  "history_rows": len(saved["history"]), "optimizer_updates_performed": 0,
                  "original_serialized_storage_locations": placements,
                  "derivative_serialized_storage_locations": derivative_placements,
                  "tensor_placement_note": "CUDA storage tags may become CPU tags; numerical tensor bytes are unchanged.",
                  "all_original_fields_verified": True, "tensor_equality_and_bytes_verified": True,
                  "verified_tensors": after_tensors, "source_unchanged_sha256_verified": True,
                  "tool_torch_version": str(torch.__version__), "tool_numpy_version": np.__version__,
                  "qualification": QUALIFICATION}
        receipt_bytes = (json.dumps(record, indent=2, allow_nan=False) + "\n").encode("utf-8")
        staged_receipt = stage_file(receipt, lambda stream: stream.write(receipt_bytes))
        try:
            publish_exclusive(temporary, output)
            publish_exclusive(staged_receipt, receipt)
        except BaseException:
            print(f"Publication failed; existing/verified artifacts preserved at {output}, "
                  f"{temporary}, {receipt}, {staged_receipt}. Inspect before retrying.", file=sys.stderr)
            raise
    except BaseException:
        if temporary.exists():
            print(f"Unpublished derivative preserved: {temporary}", file=sys.stderr)
        raise
    print(json.dumps({"derivative": str(output), "sha256": derivative_hash, "receipt": str(receipt),
                      "current_step": saved["current_step"], "selected_step": saved["selected_step"],
                      "qualification": QUALIFICATION}, indent=2, allow_nan=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Checkpoint handoff failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
