"""Deterministic CPU feature definitions for a NEW exploratory GW survey.

This does not implement or modify frozen F2, a detector network statistic,
data quality checks, selection, data acquisition, or false-alarm calibration.
Input is one contiguous 68-second strain array: 64-second past + 4-second target.
Only installed NumPy/SciPy are required. No network, GPU or neural model is used.
"""
import numpy as np
from scipy import fft, signal

SCHEMA = "GW_CPU_FEATURE_DEFINITION_V1"
FS = 4096
NREF, NTARGET = 64 * FS, 4 * FS
BANDS = ((64, 128), (128, 256), (256, 512), (512, 768))
# The final upper edge is excluded too: [64,768) Hz, without shared bins.
SOS = signal.butter(4, (64., 768.), btype="bandpass", fs=FS, output="sos")
FEATURE_NAMES = (
    "log10_local_power_ratio", "log10_target_band_power", "log10_reference_band_power",
    "peak_over_rms", "excess_kurtosis", "energy_centroid_s", "energy_spread_s",
    "spectral_entropy", "spectral_centroid_hz", "spectral_spread_hz", "maximum_bin_fraction",
    "band_64_128_fraction", "band_128_256_fraction", "band_256_512_fraction",
    "band_512_768_fraction", "envelope_acf_peak", "envelope_acf_lag_s",
    "carrier_acf_peak", "carrier_acf_lag_s")


def _acf_peak(x, lower_s, upper_s):
    """Biased linear ACF / zero-lag power; first index wins an exact tie."""
    y = x - np.mean(x)
    n = len(y)
    a = fft.rfft(y, fft.next_fast_len(2*n - 1), workers=1)
    acf = fft.irfft(a * a.conj(), workers=1)[:n]
    if acf[0] <= np.finfo(np.float64).tiny:
        return 0., 0., True
    lo, hi = int(np.ceil(lower_s*FS)), int(np.floor(upper_s*FS))
    k = lo + int(np.argmax(acf[lo:hi+1]))
    return float(acf[k]/acf[0]), float(k/FS), False


def extract_record(record):
    """Return 19 scoring features plus absolute/raw/reference diagnostics.

    Signal conventions are fixed, not chosen after seeing records:
    * Float64; require exactly 278528 finite samples at 4096 Hz.
    * Fourth-order Butterworth bandpass applied once to all 68 s with
      scipy.signal.sosfiltfilt, padtype='odd', padlen=27 samples. This is a
      noncausal finite-record feature definition, not a physical waveform model.
      No data beyond the support are invented; endpoint effects must be assessed
      in subsequent injection validation.
    * Target: periodic Hann periodogram, constant detrend, density scaling.
      Reference: 16 nonoverlapping 4-s periodic Hann Welch segments, median
      average with SciPy's median bias correction, same bins and detrend.
    * The target/reference PSD shape uses a fixed relative numerical floor
      max(reference in-band PSD)*1e-12. It is a feature regularizer, not a
      measured detector noise floor or a detection threshold.
    * Envelope ACF lags [0.08,1] s; carrier ACF [1/768,1/64] s. ACF is signed,
      linearly zero-padded and divided by its zero-lag value (no lag correction).
    """
    x = np.asarray(record, dtype=np.float64)
    if x.shape != (NREF + NTARGET,) or not np.isfinite(x).all():
        raise ValueError("REQUIRES_FINITE_CONTIGUOUS_68S_AT_4096HZ")
    raw_ref, raw_target = x[:NREF], x[NREF:]
    raw_var = [float(np.mean((z-np.mean(z))**2)) for z in (raw_ref, raw_target)]
    if min(raw_var) <= np.finfo(np.float64).tiny:
        raise ValueError("NONCONSTANT_REFERENCE_AND_TARGET_REQUIRED")
    y = signal.sosfiltfilt(SOS, x, padtype="odd", padlen=27)
    reference, target = y[:NREF], y[NREF:]
    vr, vt = float(np.mean(reference**2)), float(np.mean(target**2))
    if min(vr, vt) <= np.finfo(np.float64).tiny or not np.isfinite(vr+vt):
        raise ValueError("NONZERO_FINITE_BAND_POWER_REQUIRED")
    rms = np.sqrt(vt)
    weights = target**2 / (NTARGET*vt)
    t = np.arange(NTARGET, dtype=np.float64)/FS
    centre = float(np.sum(weights*t))
    f, p_ref = signal.welch(reference, fs=FS, window="hann", nperseg=NTARGET,
                             noverlap=0, detrend="constant", scaling="density",
                             average="median")
    ft, p_target = signal.periodogram(target, fs=FS, window="hann",
                                        detrend="constant", scaling="density")
    if not np.array_equal(f, ft):
        raise RuntimeError("PSD_GRID_MISMATCH")
    keep = (f >= 64.) & (f < 768.)
    frequencies = f[keep]
    ref, original = p_ref[keep], p_target[keep]
    floor = float(np.max(ref))*1.e-12
    if floor <= 0. or not np.isfinite(floor):
        raise ValueError("REFERENCE_PSD_SCALE_REQUIRED")
    normalized = original / np.maximum(ref, floor)
    total = float(normalized.sum())
    if total <= 0. or not np.isfinite(total):
        raise ValueError("NORMALIZED_TARGET_POWER_REQUIRED")
    p = normalized/total
    positive = p > 0.
    centroid = float(np.sum(frequencies*p))
    values = {
        "log10_local_power_ratio": float(np.log10(vt)-np.log10(vr)),
        "log10_target_band_power": float(np.log10(vt)),
        "log10_reference_band_power": float(np.log10(vr)),
        "peak_over_rms": float(np.max(np.abs(target))/rms),
        "excess_kurtosis": float(np.mean((target/rms)**4)-3.),
        "energy_centroid_s": centre,
        "energy_spread_s": float(np.sqrt(np.sum(weights*(t-centre)**2))),
        "spectral_entropy": float(-np.sum(p[positive]*np.log(p[positive]))/np.log(len(p))),
        "spectral_centroid_hz": centroid,
        "spectral_spread_hz": float(np.sqrt(np.sum(p*(frequencies-centroid)**2))),
        "maximum_bin_fraction": float(p.max())}
    for lower, upper in BANDS:
        values["band_%d_%d_fraction" % (lower, upper)] = float(
            p[(frequencies >= lower) & (frequencies < upper)].sum())
    envelope = np.abs(signal.hilbert(target))
    ep, el, ec = _acf_peak(envelope, .08, 1.)
    cp, cl, cc = _acf_peak(target, 1/768, 1/64)
    values.update(envelope_acf_peak=ep, envelope_acf_lag_s=el,
                  carrier_acf_peak=cp, carrier_acf_lag_s=cl)
    # These retain absolute and reference behavior that target/reference ratios
    # can erase for a source present throughout both target and reference.
    diagnostics = {
        "raw_reference_power": raw_var[0], "raw_target_power": raw_var[1],
        "reference_psd_peak_hz": float(frequencies[int(np.argmax(ref))]),
        "reference_psd_peak_fraction": float(np.max(ref)/np.sum(ref)),
        "target_unwhitened_psd_peak_hz": float(frequencies[int(np.argmax(original))]),
        "target_unwhitened_psd_peak_fraction": float(np.max(original)/np.sum(original)),
        "reference_in_band_psd_integral": float(np.sum(ref)*(FS/NTARGET)),
        "target_in_band_psd_integral": float(np.sum(original)*(FS/NTARGET)),
        "psd_regularized_bin_fraction": float(np.mean(ref < floor)),
        "envelope_acf_degenerate": bool(ec), "carrier_acf_degenerate": bool(cc)}
    if set(values) != set(FEATURE_NAMES) or not all(np.isfinite(v) for v in values.values()):
        raise ValueError("NONFINITE_FEATURE")
    if not all(np.isfinite(v) for v in diagnostics.values()):
        raise ValueError("NONFINITE_DIAGNOSTIC")
    return {"schema": SCHEMA, "features": values, "diagnostics": diagnostics,
            "sample_rate_hz": FS, "reference_seconds": 64, "target_seconds": 4,
            "band_edges_hz": [64, 768], "upper_band_edge_included": False,
            "statistical_status": "FEATURES_ONLY_NO_FALSE_ALARM_INFERENCE"}


def features(record):
    """Convenience interface returning the 19 scalar primary features only."""
    return extract_record(record)["features"]
