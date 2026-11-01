#!/usr/bin/env python3
"""Describe the frozen packet endpoint's assumptions and conservatism.

This is arithmetic on retained coefficients, not another raw/noise search.
It does not change the frozen protocol, choose a new confidence endpoint,
calibrate false alarms, or compare methods at matched false-alarm rate.
Requires NumPy, with no network access or installation.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import time
from pathlib import Path
import numpy as np

EXPECTED_RESULTS = "6b645865ea649701e25ebf6d6fdc35aae1ca57533327084622bb9fe9dd11d938"
EXPECTED_PROJECTIONS = "f3b1d2a718f023946edbfe17f740cff08eee2a4a11077d747ceaf51f76ffb1e2"


def checked(path: Path, digest: str) -> bytes:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(f"INPUT_SHA256_MISMATCH: {path.name}")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--projections", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    results = json.loads(checked(args.results, EXPECTED_RESULTS))
    checked(args.projections, EXPECTED_PROJECTIONS)
    with np.load(args.projections, allow_pickle=False) as arrays:
        coefficients = arrays["primary_coefficients"]
        arrivals = arrays["arrival_shifts"]
        maximum_by_context = np.linalg.norm(coefficients, axis=2).max(axis=0)
        maximizing_arrival = np.linalg.norm(coefficients, axis=2).argmax(axis=0)
    alpha, kappa, guard, gram_upper = 0.1, 0.99, 1e-8, 0.142
    multiplier = (1 + guard) / (kappa * math.sin(math.pi * alpha))
    observed_max = float(maximum_by_context.max())
    upper = observed_max * multiplier * math.sqrt(gram_upper)
    original_upper = results["primary_90_percent_phase_ensemble_bound"]["received_H1_hrss_upper_Hz_minus_half"]
    assert abs(upper / original_upper - 1) < 1e-12
    args.out.mkdir(parents=True, exist_ok=True)
    context_rows = []
    for index, receipt in enumerate(results["inputs_verified"]):
        context_rows.append({
            "record_id": receipt["record_id"],
            "maximum_coefficient_norm": float(maximum_by_context[index]),
            "maximizing_arrival_seconds": float(arrivals[maximizing_arrival[index]]),
            "same_formula_pointwise_hrss90": float(maximum_by_context[index] * multiplier * math.sqrt(gram_upper)),
            "common_endpoint_over_pointwise_endpoint": float(observed_max / maximum_by_context[index]),
            "interpretation": "Descriptive pointwise endpoint; common unknown-context endpoint remains the maximum, not the median or minimum.",
        })
    with (args.out / "PHASE_CONTEXT_CONSERVATISM.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=context_rows[0].keys())
        writer.writeheader()
        writer.writerows(context_rows)
    # An analytic stress case, independent of any GW data, attains the
    # circle-intersection upper bound for an isotropic response kappa*I.
    # The midpoint grid checks sharpness numerically; it is not the proof.
    points = 262144
    phase = 2 * np.pi * (np.arange(points, dtype=float) + 0.5) / points
    stress_rows = []
    for failure_probability in (0.1, 0.025):
        q = math.sin(math.pi * failure_probability)
        noise_norm = kappa * math.cos(math.pi * failure_probability)
        observed = np.hypot(noise_norm + kappa * np.cos(phase), kappa * np.sin(phase))
        missed = float(np.mean(observed < kappa * q))
        assert abs(missed - failure_probability) <= 2 / points
        stress_rows.append({
            "nominal_phase_coverage": 1 - failure_probability,
            "least_response": kappa,
            "fixed_noise_norm_over_signal_coefficient": noise_norm,
            "analytic_worst_case_miss_probability": failure_probability,
            "midpoint_phase_grid_miss_fraction": missed,
            "phase_grid_points": points,
            "coefficient_multiplier_ignoring_numeric_guard": 1 / (kappa * q),
        })
    report = {
        "schema": "GW_FROZEN_PHASE_ENDPOINT_PRACTICAL_TRADEOFF_AUDIT_V1",
        "status": "PASS_RETAINED_COEFFICIENT_ARITHMETIC_AND_ANALYTIC_STRESS_CHECK",
        "inputs": {"results_sha256": EXPECTED_RESULTS.upper(), "projections_sha256": EXPECTED_PROJECTIONS.upper()},
        "observed_maximum": observed_max,
        "unchanged_frozen_hrss90": upper,
        "coefficient_multiplier_over_observed_maximum": multiplier,
        "quadrature_norm_to_hrss_multiplier_seconds_half": multiplier * math.sqrt(gram_upper),
        "per_context_hrss90_min": min(row["same_formula_pointwise_hrss90"] for row in context_rows),
        "per_context_hrss90_median": float(np.median([row["same_formula_pointwise_hrss90"] for row in context_rows])),
        "common_over_smallest_context_endpoint": max(row["common_endpoint_over_pointwise_endpoint"] for row in context_rows),
        "sharpness_stress_cases": stress_rows,
        "fixed_phase_cancellation_counterexample": {
            "signal_coefficient": 1.0, "fixed_phase": 0.0,
            "additive_noise_projection": [-kappa, 0.0],
            "response_matrix": [[kappa, 0.0], [0.0, kappa]],
            "observed_projection_norm": 0.0,
            "conclusion": "No finite endpoint can have uniform coverage over all fixed phases and unrestricted additive nuisance; uniform independent phase is substantive.",
        },
        "counterfactual_shortcut_twice_observed_maximum": {
            "coefficient_multiplier": 2 / kappa,
            "maximum_phase_miss_probability": math.asin(0.5) / math.pi,
            "phase_coverage": 1 - math.asin(0.5) / math.pi,
            "conclusion": "A coefficient endpoint 2*M/kappa has only 5/6 worst-case phase coverage, not 90%; this is not a standard GW sensitivity benchmark.",
        },
        "interpretation": [
            "Practical value is a narrow computable phase-ensemble amplitude endpoint without fitting a noise distribution or requiring independent records.",
            "Robust noise-distribution upper limits already exist in the literature; no priority or universal superiority is claimed.",
            "The interval trades noise-model requirements for a strong phase-independence/one-packet assumption and a conservative amplitude multiplier.",
            "Taking a maximum over fixed search points enlarges the upper endpoint. This does not remove look-elsewhere corrections for detection significance.",
            "Pointwise endpoints are descriptive; replacing the maximum by their median does not retain an unknown-context claim.",
            "The 90% endpoint and 97.1875% finite true-arrival crossing response are different quantities.",
            "The stress calculation is two-dimensional geometric validation, not an additional GW observation, full-search background or matched-FAR performance test.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
        "new_raw_projections": 0, "new_neural_calls": 0, "network_requests": 0,
    }
    (args.out / "PHASE_PRACTICAL_TRADEOFF.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "unchanged_frozen_hrss90", "coefficient_multiplier_over_observed_maximum", "common_over_smallest_context_endpoint", "elapsed_seconds")}))


if __name__ == "__main__":
    main()
