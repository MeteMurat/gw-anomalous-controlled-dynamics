#!/usr/bin/env python3
"""Independent, standard-library checks of the random-phase amplitude bound.

These checks contain no GW data and make no network calls. Analytic coverage
comes from PHASE_BOUND_PROOF.md; a phase grid is a numerical check, not its proof.
"""
import json
import math
from pathlib import Path
import platform

OUT = Path(__file__).resolve().parent
ALPHA = 0.1
KAPPA = 0.99
FS = 4096
DT = 1 / FS
SIGMA = 0.04
OMEGA = 2 * math.pi * 256
PHASE_POINTS = 200000

def circle_probability(noise_norm, radius, amplitude=1.0):
    if noise_norm == 0:
        return float(amplitude <= radius)
    value = (amplitude * amplitude + noise_norm * noise_norm - radius * radius) / (2 * amplitude * noise_norm)
    if value >= 1:
        return 0.0
    if value <= -1:
        return 1.0
    return math.acos(value) / math.pi

def phase_grid_fraction(noise_norm, radius, amplitude=1.0):
    return sum(
        math.hypot(noise_norm + amplitude * math.cos(2 * math.pi * k / PHASE_POINTS),
                   amplitude * math.sin(2 * math.pi * k / PHASE_POINTS)) < radius
        for k in range(PHASE_POINTS)
    ) / PHASE_POINTS

q = math.sin(math.pi * ALPHA)
noise_norms = [0, 0.1, 0.7, math.sqrt(1 - q * q), 1.0, 1.1, 1.5]
circle_checks = []
for norm in noise_norms:
    analytic = circle_probability(norm, q)
    grid = phase_grid_fraction(norm, q)
    assert analytic <= ALPHA + 1e-14
    assert abs(grid - analytic) <= 2 / PHASE_POINTS
    circle_checks.append({'noise_norm_over_A': norm, 'analytic_failure_probability': analytic,
                          'phase_grid_failure_fraction': grid})

derivative_integral = math.sqrt(math.pi) / (2 * SIGMA)
derivative_total_variation = 4 / (math.e * SIGMA * SIGMA)
D = 4 * math.sqrt(derivative_integral + DT * derivative_total_variation)
m_lower = 1 - (DT / 2) * D / math.sqrt(0.14)
assert KAPPA < m_lower < 1
edge_tail = 32 * (DT + SIGMA * SIGMA / (2 * 0.25)) * math.exp(-(0.25 / SIGMA) ** 2)
beta = math.pi * SIGMA / DT
omega_sigma = OMEGA * SIGMA
assert beta * beta > 1000
assert omega_sigma * omega_sigma > 1000
assert (beta - omega_sigma) ** 2 > 1000

# Direct checks use the four-second target. The analytic lower bound remains
# valid for a larger raw projection window containing this target, e.g. [-2,4).
def basis_gram(shift, start=0.0):
    ss = cc = sc = 0.0
    for index in range(round((4 - start) * FS)):
        t = start + index * DT
        envelope = sum(sign * math.exp(-0.5 * ((t - shift - centre) / SIGMA) ** 2)
                       for centre, sign in zip((0.5, 1.5, 2.5, 3.5), (1, -1, -1, 1)))
        a, b = envelope * math.sin(OMEGA * t), envelope * math.cos(OMEGA * t)
        ss += a * a * DT
        cc += b * b * DT
        sc += a * b * DT
    spread = math.hypot(ss - cc, 2 * sc)
    return {'ss': ss, 'cc': cc, 'sc': sc,
            'lambda_min': (ss + cc - spread) / 2,
            'lambda_max': (ss + cc + spread) / 2}

grams = []
for start in (0.0, -2.0):
    for shift in (-0.25, -0.125, 0, 0.125, 0.25):
        result = basis_gram(shift, start)
        assert result['lambda_min'] > 0.14
        assert result['lambda_max'] < 0.142
        grams.append({'window_seconds': [start, 4], 'shift_seconds': shift, **result})

report = {
    'schema': 'GW_RANDOM_PHASE_BOUND_INDEPENDENT_VALIDATION_V1',
    'status': 'PASS_ANALYTIC_CONDITIONS_AND_NUMERICAL_CHECKS',
    'python': platform.python_version(),
    'no_GW_data_or_network_or_neural_calls': True,
    'phase_grid_points_per_case': PHASE_POINTS,
    'circle_checks': circle_checks,
    'worst_case_noise_norm_over_A': math.cos(math.pi * ALPHA),
    'alpha': ALPHA, 'chosen_kappa': KAPPA,
    'derivative_uniform_discrete_L2_bound': D,
    'nearest_sample_response_lower_bound': m_lower,
    'chosen_gram_lower': 0.14, 'chosen_full_packet_gram_upper': 0.142,
    'target_omitted_envelope_energy_bound': edge_tail,
    'gaussian_alias_exponent_beta_squared': beta * beta,
    'quadrature_anisotropy_exponent_omega_sigma_squared': omega_sigma * omega_sigma,
    'nearest_alias_anisotropy_exponent': (beta - omega_sigma) ** 2,
    'sampled_gram_checks': grams,
    'A90_over_M': 1 / (KAPPA * q),
    'hrss90_over_M': math.sqrt(0.142) / (KAPPA * q),
    'scope': 'Coverage over independent uniform source carrier phase for a fixed single-packet model and fixed linear projection; not fixed-phase, FAP, all-sky, distance or population-rate inference.',
    'fixed_phase_counterexample': 'For a fixed phase phi0, choose deterministic n=-A*T*u(phi0). Then x=0, M=0 and the positive amplitude is excluded with certainty.',
}
(OUT / 'PHASE_BOUND_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
