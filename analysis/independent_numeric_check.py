"""Independent numeric checks of the executed fixed-packet calculation.

Does not import or call RUN_PACKET_BOUND.py. This checks raw LS projections,
all reported recovery counts, and constants; it creates no new observation.
"""
from pathlib import Path
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import csv
import hashlib
import io
import json
import math
import time
import numpy as np

START = time.monotonic()
ROOT = Path(__file__).resolve().parents[1] / 'gw_packet_bound_20261101'
OUT = Path(__file__).resolve().parent
P = json.loads((ROOT / 'PROTOCOL.json').read_text())
R = json.loads((ROOT / 'results/RESULTS.json').read_text())
digest = lambda b: hashlib.sha256(b).hexdigest().upper()
assert digest((ROOT / 'PROTOCOL.json').read_bytes()) == R['protocol_sha256']
assert digest((ROOT / 'RUN_PACKET_BOUND.py').read_bytes()) == R['implementation_sha256']
assert P['linear_conditioning'].startswith('None;')
assert P['confidence']['alpha'] == .1
assert P['confidence']['continuous_arrival_response_lower_bound_kappa'] == .99
assert P['projection_seconds'] == [-2, 4]
assert P['confidence']['amplitude_definition'] == 'Fixed coefficient A_det, not per-phase hrss renormalization'

stored = np.load(ROOT / 'results/PROJECTION_AND_RESPONSE.npz', allow_pickle=False)
shifts = stored['arrival_shifts']
coef = stored['primary_coefficients']
response = stored['injection_response']
inj_shift = stored['injection_arrivals']
assert shifts.shape == (2049,) and coef.shape == (2049, 12, 2)
assert response.shape == (2049, 5, 2, 2)
assert np.array_equal(shifts, np.arange(-1024, 1025) / 4096)
assert np.array_equal(inj_shift, [-.25, -.125, 0., .125, .25])
norm = np.sqrt(np.sum(coef * coef, axis=-1))
idx = np.unravel_index(np.argmax(norm), norm.shape)
M = float(norm[idx])
assert math.isclose(M, R['observed_global_maximum']['coefficient_norm'], rel_tol=2e-15)
assert P['inputs'][idx[1]]['record_id'] == 'R4096_0949'
assert shifts[idx[0]] == -271 / 4096

ld = np.longdouble
t = np.arange(-8192, 16384, dtype=np.int64).astype(ld) / ld(4096)
pi = np.arccos(ld(-1))
raw_inputs = []
projected = []
raw_vs_stored_max_relative = 0.
for i, item in enumerate(P['inputs']):
    path = ROOT / 'inputs' / (item['record_id'] + '.npz')
    assert digest(path.read_bytes()) == item['npz_sha256']
    with np.load(path, allow_pickle=False) as data:
        raw = data['strain']
    assert raw.shape == (68 * 4096,)
    assert digest(np.asarray(raw, dtype='<f8').tobytes()) == item['raw_array_sha256']
    raw_inputs.append(raw)
    k = int(np.argmax(norm[:, i]))
    shift = ld(str(float(shifts[k])))
    env = np.zeros(t.size, dtype=ld)
    for centre, sign in zip(('.5', '1.5', '2.5', '3.5'), (1, -1, -1, 1)):
        env += sign * np.exp(-ld('.5') * ((t - shift - ld(centre)) / ld('.04')) ** 2)
    bs = env * np.sin(2 * pi * 256 * t)
    bc = env * np.cos(2 * pi * 256 * t)
    g11, g12, g22 = np.sum(bs * bs), np.sum(bs * bc), np.sum(bc * bc)
    x = raw[-6 * 4096:].astype(ld)
    b1, b2 = np.sum(bs * x), np.sum(bc * x)
    det = g11 * g22 - g12 * g12
    direct = np.array([(g22 * b1 - g12 * b2) / det,
                       (g11 * b2 - g12 * b1) / det], dtype=ld)
    error = float(np.max(np.abs(direct - coef[k, i].astype(ld))))
    relative = error / max(float(np.max(np.abs(direct))), 1e-40)
    raw_vs_stored_max_relative = max(raw_vs_stored_max_relative, relative)
    assert relative < 1e-8
    projected.append({'record_id': item['record_id'], 'shift_seconds': float(shift),
                      'long_double_sin_coefficient': float(direct[0]),
                      'long_double_cos_coefficient': float(direct[1]),
                      'long_double_norm': float(np.sqrt(np.sum(direct ** 2))),
                      'relative_difference_vs_stored_coefficients': relative})

independent_M = max(x['long_double_norm'] for x in projected)
assert math.isclose(independent_M, M, rel_tol=1e-8)
alpha = P['confidence']['alpha']
kappa = P['confidence']['continuous_arrival_response_lower_bound_kappa']
inflation = P['confidence']['numeric_maximum_inflation']
A90 = M * (1 + inflation) / (kappa * math.sin(math.pi * alpha))
h90 = A90 * math.sqrt(P['confidence']['full_packet_hrss_gram_upper_bound_seconds'])
assert A90 == R['primary_90_percent_phase_ensemble_bound']['coefficient_A_det_upper']
assert h90 == R['primary_90_percent_phase_ensemble_bound']['received_H1_hrss_upper_Hz_minus_half']
raw_full_packet_gram_isotropic = 2 * math.sqrt(math.pi) * .04
assert .14 < raw_full_packet_gram_isotropic < .142
# Same-centre quadrature imbalance is suppressed by exp[-(2*pi*f*sigma)^2];
# neighbour overlap by exp[-1/(4*sigma^2)]. Both are far below the .142 cap.
log_phase_imbalance = -(2 * math.pi * 256 * .04) ** 2
log_neighbour_overlap = -1 / (4 * .04 ** 2)
assert log_phase_imbalance < -4000 and log_neighbour_overlap < -150
derivative_D = 4 * math.sqrt(math.sqrt(math.pi) / (2 * .04) + (1 / 4096) * 4 / (math.e * .04 ** 2))
kappa_floor = 1 - (.5 / 4096) * derivative_D / math.sqrt(.14)
assert kappa_floor > kappa
assert math.isclose(kappa_floor, R['continuous_arrival_certificate']['derived_kappa_lower_bound'], rel_tol=1e-15)

# Recount every predeclared phase/time/noise cell at every amplitude without
# calling the original program's injection or phase-probability functions.
phis = 2 * math.pi * np.arange(32) / 32
unit = np.stack([np.cos(phis), np.sin(phis)], axis=-1)
cell_signal = np.einsum('lajk,pk->aplj', response, unit, optimize=False)
cut = M * (1 + inflation)
all_counts = []
for amp_index, row in enumerate(R['injection_comparison']['efficiency']):
    amplitude = row['coefficient_A_det']
    count = 0
    context_counts = []
    for i in range(12):
        values = coef[:, i][None, None] + amplitude * cell_signal
        maxima = np.max(np.sqrt(np.sum(values ** 2, axis=-1)), axis=-1)
        recovered = int(np.sum(maxima > cut))
        context_counts.append(recovered)
        count += recovered
    assert count == row['recovered']
    assert context_counts == R['injection_comparison']['recovered_per_context'][amp_index]
    assert count / 1920 == row['full_search_discrete_phase_efficiency']
    all_counts.append(count)
assert len(all_counts) == 57
assert 57 * 12 * 32 * 5 == 109440
assert all(a <= b for a, b in zip(all_counts, all_counts[1:]))
first90 = next(i for i, c in enumerate(all_counts) if c >= .9 * 1920)
assert R['injection_comparison']['efficiency'][first90] == R['injection_comparison']['first_grid_amplitude_reaching_90_percent']
assert R['validation']['full_raw_injection_direct_projection_checks'] == 240 == 12 * 5 * 4
assert R['validation']['maximum_direct_relative_error'] < 5e-12
assert R['validation']['full_scan_raw_vs_response_maximum_absolute_error'] < 5e-34

summary = {
    'status': 'PASS_INDEPENDENT_RAW_PROJECTIONS_INFERENCE_CONSTANTS_AND_ALL_RECOVERY_COUNTS',
    'protocol_sha256_verified': R['protocol_sha256'],
    'implementation_sha256_verified': R['implementation_sha256'],
    'independent_long_double_raw_projections': projected,
    'maximum_long_double_relative_difference': raw_vs_stored_max_relative,
    'global_maximum_stored': M,
    'global_maximum_long_double_at_reported_record_maxima': independent_M,
    'maximum_record': 'R4096_0949', 'maximum_shift_seconds': -271 / 4096,
    'coefficient_A90_independently_recomputed': A90,
    'received_H1_hrss90_independently_recomputed': h90,
    'raw_full_packet_gram_leading_exact_value_seconds': raw_full_packet_gram_isotropic,
    'phase_imbalance_log_suppression': log_phase_imbalance,
    'nearest_packet_overlap_log_suppression': log_neighbour_overlap,
    'continuous_arrival_kappa_lower_bound': kappa_floor,
    'all_57_amplitude_count_rows_recomputed': True,
    'all_109440_linear_variant_equivalent_evaluations_accounted': True,
    'all_684_context_amplitude_recovery_counts_recomputed': True,
    'full_raw_validation_checks_reported_and_reviewed': 240,
    'whole_grid_raw_linearity_check_reported_and_reviewed': True,
    'scope': 'Independent long-double recomputation at twelve reported record maxima; all recovery cells recounted from saved response matrices. Not an independently recomputed full 2049-point raw scan at every record.',
    'statistical_scope_review': 'Fixed-family uniform-independent-phase ensemble, fixed raw linear projection; no empirical FAP, fixed-phase guarantee, technological origin, event-rate or all-sky inference.',
    'secondary_alpha_025_scope': 'Illustrative four-family sensitivity adjustment only, not a completed correction for arbitrary historical adaptation.',
    'wall_seconds': time.monotonic() - START,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'NUMERIC_AUDIT.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: summary[k] for k in ('status', 'maximum_long_double_relative_difference', 'global_maximum_long_double_at_reported_record_maxima', 'received_H1_hrss90_independently_recomputed', 'wall_seconds')}))
