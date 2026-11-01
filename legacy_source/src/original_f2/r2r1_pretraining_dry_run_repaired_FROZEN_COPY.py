from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

try:
    import scipy
    from scipy import signal
except Exception as exc:
    raise SystemExit("SCIPY_IMPORT_FAILED: " + repr(exc))


SEED = 20260919
CONTEXT_S = 64
TARGET_S = 4
TARGET_STRIDE_S = 2

BRANCHES = {
    "low_mid": {
        "fs": 4096,
        "band": (20.0, 1600.0),
        "stft_nperseg": 1048,
        "stft_hop": 524,
        "stft_nfft": 1048,
        "tone_hz": 431.0,
    },
    "high": {
        "fs": 16384,
        "band": (1600.0, 5000.0),
        "stft_nperseg": 4192,
        "stft_hop": 2096,
        "stft_nfft": 4192,
        "tone_hz": 2300.0,
    },
}

OBJECTIVE_WEIGHTS = {
    "invariance": 25.0,
    "variance": 25.0,
    "covariance": 1.0,
    "masked_reconstruction": 1.0,
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest().upper()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            block = f.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest().upper()


def robust_mad(x: np.ndarray) -> tuple[float, float]:
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med)))
    return med, 1.4826 * mad


def bandlimit_real(x: np.ndarray, fs: int, band: tuple[float, float]) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), d=1.0 / fs)
    keep = (f >= band[0]) & (f <= band[1])
    X[~keep] = 0.0
    return np.fft.irfft(X, n=len(x))


def deterministic_whiten(
    context: np.ndarray,
    target: np.ndarray,
    fs: int,
    band: tuple[float, float],
) -> tuple[np.ndarray, dict]:
    # Reconstruct the prospectively defined R1 preprocessing semantics:
    # linear detrend context/target, 4-s Hann Welch, 50% overlap,
    # density scaling, median averaging, deterministic positive PSD floor.
    context = signal.detrend(np.asarray(context, dtype=np.float64), type="linear")
    target = signal.detrend(np.asarray(target, dtype=np.float64), type="linear")

    psd_n = 4 * fs
    f_psd, pxx = signal.welch(
        context,
        fs=float(fs),
        window="hann",
        nperseg=psd_n,
        noverlap=psd_n // 2,
        nfft=psd_n,
        detrend=False,
        return_onesided=True,
        scaling="density",
        average="median",
    )
    pos = pxx[np.isfinite(pxx) & (pxx > 0.0)]
    if pos.size == 0:
        raise RuntimeError("NO_POSITIVE_PSD")
    active = pos
    mask_band = (f_psd >= band[0]) & (f_psd <= band[1]) & np.isfinite(pxx) & (pxx > 0.0)
    if np.any(mask_band):
        active = pxx[mask_band]
    floor = max(np.finfo(np.float64).tiny, 1e-12 * float(np.median(active)))
    pxx = np.maximum(pxx, floor)

    ft = np.fft.rfft(target)
    f_t = np.fft.rfftfreq(len(target), d=1.0 / fs)
    p_interp = np.interp(f_t, f_psd, pxx, left=pxx[0], right=pxx[-1])
    white = np.fft.irfft(ft / np.sqrt(np.maximum(p_interp, floor)), n=len(target))
    white = bandlimit_real(white, fs, band)

    med, scale = robust_mad(white)
    if not np.isfinite(scale) or scale <= 0.0:
        raise RuntimeError("ZERO_OR_NONFINITE_MAD")
    morph = (white - med) / scale

    unwhitened_band = bandlimit_real(target, fs, band)
    rms = float(np.sqrt(np.mean(unwhitened_band * unwhitened_band)))
    amp = float(np.log10(max(rms, np.finfo(np.float64).tiny)))

    meta = {
        "psd_floor": floor,
        "morph_median_before_norm": med,
        "morph_robust_scale": scale,
        "amplitude_log10_rms": amp,
    }
    return morph, meta


def periodic_hann(n: int) -> np.ndarray:
    k = np.arange(n, dtype=np.float64)
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * k / float(n))


def r1t_stft(x: np.ndarray, fs: int, band: tuple[float, float], nperseg: int, hop: int, nfft: int):
    if nfft != nperseg:
        raise RuntimeError("R1T_ZERO_PADDING_FORBIDDEN")
    if nperseg % 2 != 0 or hop * 2 != nperseg:
        raise RuntimeError("R1T_EXACT_50PCT_OVERLAP_VIOLATION")
    if len(x) < nperseg:
        raise RuntimeError("TARGET_TOO_SHORT")
    count = 1 + (len(x) - nperseg) // hop
    starts = np.arange(count, dtype=np.int64) * np.int64(hop)
    w = periodic_hann(nperseg)
    norm = float(np.sum(w))
    out = np.empty((nfft // 2 + 1, count), dtype=np.float64)
    for j, s in enumerate(starts):
        frame = x[int(s):int(s)+nperseg]
        if len(frame) != nperseg:
            raise RuntimeError("TRUNCATED_STFT_FRAME")
        z = np.fft.rfft(frame * w, n=nfft) / norm
        out[:, j] = np.log10(np.maximum(np.abs(z) ** 2, np.finfo(np.float64).tiny))
    f = np.fft.rfftfreq(nfft, d=1.0/fs)
    keep = (f >= band[0]) & (f <= band[1])
    return out[keep, :], f[keep], starts


def translate_crop_pad(x: np.ndarray, shift: int) -> np.ndarray:
    y = np.zeros_like(x)
    if shift == 0:
        y[:] = x
    elif shift > 0:
        y[shift:] = x[:-shift]
    else:
        y[:shift] = x[-shift:]
    return y


def augment_view(x: np.ndarray, fs: int, rng: np.random.Generator) -> tuple[np.ndarray, dict]:
    # Deterministic subset of the already-frozen allowed augmentation family.
    max_shift = int(round(0.125 * fs))
    shift = int(rng.integers(-max_shift, max_shift + 1))
    y = translate_crop_pad(x, shift)

    sign = -1.0 if float(rng.random()) < 0.5 else 1.0
    y = y * sign

    gain = float(np.exp(rng.uniform(np.log(0.9), np.log(1.1))))
    y = y * gain

    noise_rms = min(0.01, 0.005)
    y_rms = float(np.sqrt(np.mean(y*y)))
    y = y + rng.standard_normal(len(y)) * (noise_rms * max(y_rms, np.finfo(float).tiny))

    # One deterministic small contiguous time mask, <=2.5% of segment.
    mask_len = max(1, int(math.floor(0.02 * len(y))))
    m0 = int(rng.integers(0, len(y) - mask_len + 1))
    y[m0:m0+mask_len] = 0.0

    return y, {
        "shift_samples": shift,
        "sign": sign,
        "gain": gain,
        "noise_rms_fraction": noise_rms,
        "time_mask_samples": mask_len,
    }


def vicreg_schema_dry_run(rng: np.random.Generator) -> dict:
    # Objective-plumbing test only; not model output and not training.
    z1 = rng.standard_normal((16, 128))
    z2 = z1 + 0.05 * rng.standard_normal((16, 128))

    inv = float(np.mean((z1-z2)**2))
    eps = 1e-4
    std1 = np.sqrt(np.var(z1, axis=0, ddof=1) + eps)
    std2 = np.sqrt(np.var(z2, axis=0, ddof=1) + eps)
    var = float(np.mean(np.maximum(0.0, 1.0-std1)) + np.mean(np.maximum(0.0, 1.0-std2)))

    def cov_pen(z):
        zc = z - z.mean(axis=0, keepdims=True)
        c = (zc.T @ zc) / (len(z)-1)
        off = c - np.diag(np.diag(c))
        return float(np.sum(off*off) / z.shape[1])
    cov = cov_pen(z1) + cov_pen(z2)

    a = rng.standard_normal((128,))
    b = a + 0.1 * rng.standard_normal((128,))
    delta = 1.0
    d = np.abs(a-b)
    huber = float(np.mean(np.where(d <= delta, 0.5*d*d, delta*(d-0.5*delta))))

    total = (
        OBJECTIVE_WEIGHTS["invariance"]*inv
        + OBJECTIVE_WEIGHTS["variance"]*var
        + OBJECTIVE_WEIGHTS["covariance"]*cov
        + OBJECTIVE_WEIGHTS["masked_reconstruction"]*huber
    )
    return {
        "invariance": inv,
        "variance": var,
        "covariance": cov,
        "masked_reconstruction_huber": huber,
        "weighted_total_schema_probe": total,
        "weights": OBJECTIVE_WEIGHTS,
    }


def torch_runtime_probe() -> dict:
    try:
        import torch
        return {
            "available": True,
            "version": torch.__version__,
            "cuda_available": bool(torch.cuda.is_available()),
            "cuda_device_count": int(torch.cuda.device_count()),
        }
    except Exception as exc:
        return {
            "available": False,
            "error": repr(exc),
        }


def make_synthetic(fs: int, tone_hz: float, seed: int) -> np.ndarray:
    n = (CONTEXT_S + TARGET_S) * fs
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=np.float64) / float(fs)
    # Colored-ish deterministic background plus stable tone and weak chirp.
    x = (
        0.35*rng.standard_normal(n)
        + 0.12*np.sin(2*np.pi*37.0*t)
        + 0.08*np.sin(2*np.pi*tone_hz*t)
    )
    # Add a weak smooth chirp only inside the target to exercise morphology.
    start = CONTEXT_S * fs
    tt = np.arange(TARGET_S*fs, dtype=np.float64) / float(fs)
    chirp = 0.05 * signal.chirp(tt, f0=max(25.0, tone_hz*0.8), f1=tone_hz*1.15, t1=TARGET_S)
    x[start:] += chirp
    return x.astype(np.float64, copy=False)


def run(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    cache = outdir / "synthetic_cache"
    cache.mkdir(exist_ok=True)

    gates = []
    branch_summaries = {}

    def gate(name, ok, detail):
        gates.append({"gate": name, "pass": bool(ok), "detail": str(detail)})
        print(("PASS  " if ok else "FAIL  ") + name + "  " + str(detail))

    torch_info = torch_runtime_probe()
    gate("PYTHON_NUMPY_SCIPY_RUNTIME", True, f"python={sys.version.split()[0]};numpy={np.__version__};scipy={scipy.__version__}")
    gate("PYTORCH_RUNTIME_AVAILABLE", bool(torch_info.get("available")), json.dumps(torch_info, sort_keys=True))

    for bi, (name, spec) in enumerate(BRANCHES.items()):
        fs = int(spec["fs"])
        x = make_synthetic(fs, float(spec["tone_hz"]), SEED + 100*bi)

        p = cache / f"{name}_synthetic.npy"
        np.save(p, x, allow_pickle=False)
        h1 = sha256_file(p)
        y = np.load(p, allow_pickle=False)
        h2 = sha256_file(p)

        gate(f"{name.upper()}_SYNTHETIC_CACHE_SHA_STABLE", h1 == h2, h1)
        gate(f"{name.upper()}_SYNTHETIC_CACHE_ROUNDTRIP_EXACT", np.array_equal(x, y), f"samples={len(y)}")

        context_n = CONTEXT_S * fs
        target_n = TARGET_S * fs
        context = y[:context_n]
        target = y[context_n:context_n+target_n]
        gate(f"{name.upper()}_CAUSAL_CONTEXT_EXACT", len(context) == context_n, f"context_samples={len(context)}")
        gate(f"{name.upper()}_TARGET_LENGTH_EXACT", len(target) == target_n, f"target_samples={len(target)}")

        morph, meta = deterministic_whiten(context, target, fs, tuple(spec["band"]))
        gate(f"{name.upper()}_WHITENED_TARGET_FINITE", np.isfinite(morph).all(), f"n={len(morph)}")
        gate(f"{name.upper()}_ROBUST_NORM_MEDIAN_NEAR_ZERO", abs(float(np.median(morph))) < 1e-10, f"median={np.median(morph):.3e}")
        _, scale_after = robust_mad(morph)
        gate(f"{name.upper()}_ROBUST_NORM_SCALE_NEAR_ONE", abs(scale_after-1.0) < 1e-8, f"scale={scale_after:.12f}")

        tf, f, starts = r1t_stft(
            morph, fs, tuple(spec["band"]),
            int(spec["stft_nperseg"]), int(spec["stft_hop"]), int(spec["stft_nfft"])
        )
        gate(f"{name.upper()}_R1T_FRAME_COUNT_30", tf.shape[1] == 30, f"shape={list(tf.shape)}")
        gate(f"{name.upper()}_R1T_FINITE", np.isfinite(tf).all(), f"freq_bins={tf.shape[0]}")
        gate(f"{name.upper()}_R1T_INTEGER_STARTS", np.issubdtype(starts.dtype, np.integer), f"last_start={int(starts[-1])}")

        rng1 = np.random.default_rng(SEED + 1000 + bi)
        rng2 = np.random.default_rng(SEED + 2000 + bi)
        v1, a1 = augment_view(morph, fs, rng1)
        v2, a2 = augment_view(morph, fs, rng2)
        gate(f"{name.upper()}_AUG_VIEW1_FINITE", np.isfinite(v1).all(), json.dumps(a1, sort_keys=True))
        gate(f"{name.upper()}_AUG_VIEW2_FINITE", np.isfinite(v2).all(), json.dumps(a2, sort_keys=True))
        gate(f"{name.upper()}_AUG_VIEWS_DISTINCT", not np.array_equal(v1, v2), "independent frozen-policy views")

        # Batch/schema construction: CW status is metadata sidecar only and never enters model tensors.
        model_batch = {
            "temporal_view1": np.stack([v1, v2], axis=0),
            "temporal_view2": np.stack([v2, v1], axis=0),
            "tf_view": np.stack([tf, tf], axis=0),
            "amplitude_log10_rms": np.asarray([meta["amplitude_log10_rms"]]*2, dtype=np.float64),
        }
        sidecar = {
            "cw_status": ["CW_FREE", "CW_ACTIVE_OR_MIXED"],
            "branch": [name, name],
        }
        gate(f"{name.upper()}_CW_NOT_IN_MODEL_BATCH",
             "cw_status" not in model_batch,
             "cw_status retained only in sidecar")
        gate(f"{name.upper()}_MODEL_BATCH_FINITE",
             all(np.isfinite(v).all() for v in model_batch.values()),
             ";".join(f"{k}:{list(v.shape)}" for k,v in model_batch.items()))

        branch_summaries[name] = {
            "fs": fs,
            "band": list(spec["band"]),
            "cache_sha256": h1,
            "target_samples": target_n,
            "stft_shape": list(tf.shape),
            "stft_frames": int(tf.shape[1]),
            "amplitude_log10_rms": meta["amplitude_log10_rms"],
            "view1": a1,
            "view2": a2,
            "model_batch_keys": sorted(model_batch.keys()),
            "sidecar_keys": sorted(sidecar.keys()),
        }

    obj = vicreg_schema_dry_run(np.random.default_rng(SEED + 9999))
    gate("VICREG_SCHEMA_COMPONENTS_FINITE",
         all(np.isfinite(float(obj[k])) for k in ("invariance","variance","covariance","masked_reconstruction_huber","weighted_total_schema_probe")),
         json.dumps(obj, sort_keys=True))
    gate("VICREG_FROZEN_WEIGHTS_25_25_1_1",
         obj["weights"] == OBJECTIVE_WEIGHTS,
         json.dumps(obj["weights"], sort_keys=True))

    # Explicitly prove that no training machinery is invoked by this helper.
    # AST inspection avoids the prior self-match bug caused by searching
    # forbidden token strings that were themselves present as string literals.
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            if func.attr in ("backward", "zero_grad"):
                found.append(f"call:{func.attr}@line{getattr(node, 'lineno', -1)}")
            elif func.attr == "step":
                base = func.value
                if isinstance(base, ast.Name) and "optim" in base.id.lower():
                    found.append(f"call:{base.id}.step@line{getattr(node, 'lineno', -1)}")
        elif isinstance(func, ast.Name):
            if func.id.lower() in ("backward", "zero_grad"):
                found.append(f"call:{func.id}@line{getattr(node, 'lineno', -1)}")
    gate("NO_OPTIMIZER_OR_BACKWARD_EXECUTION", len(found) == 0, "ast_calls=" + repr(found))

    failed = [g for g in gates if not g["pass"]]
    result = {
        "stage": "T0-F2-R2",
        "role": "pretraining pipeline dry run only",
        "all_pass": len(failed) == 0,
        "gates_total": len(gates),
        "gates_failed": len(failed),
        "failed_gates": failed,
        "torch_runtime": torch_info,
        "branches": branch_summaries,
        "objective_schema_probe": obj,
        "network": "NONE",
        "public_strain": "NONE",
        "scientific_training": "NONE",
        "optimizer_step": "FORBIDDEN",
        "backward_pass": "FORBIDDEN",
        "zero_lag": "NONE",
    }
    with (outdir / "D_R2_DRY_RUN_SUMMARY.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    with (outdir / "D_R2_DRY_RUN_GATES.json").open("w", encoding="utf-8") as f:
        json.dump(gates, f, indent=2, sort_keys=True)

    print("PASS_R2_PRETRAINING_PIPELINE_DRY_RUN" if result["all_pass"] else "HOLD_R2_PRETRAINING_PIPELINE_DRY_RUN")
    print(f"gates={result['gates_total']-result['gates_failed']}/{result['gates_total']}")
    print("public_strain=NONE")
    print("scientific_training=NONE")
    print("optimizer_step=FORBIDDEN")
    print("backward_pass=FORBIDDEN")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    result = run(args.outdir)
    raise SystemExit(0 if result["all_pass"] else 2)


if __name__ == "__main__":
    main()