#!/usr/bin/env python3
"""One fixed phase-coded packet: raw linear response and random-phase bound.

The twelve original 68-second inputs and frozen protocol are read-only. The
reported confidence is over a uniform independent source carrier phase, not
over arbitrary fixed phases or a newly established instrumental-noise law.
"""
from __future__ import annotations

import os
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_key] = '1'

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
import traceback

import numpy as np

FS = 4096
SIGMA = 0.04
CENTRES = np.array([0.5, 1.5, 2.5, 3.5], dtype=np.float64)
PRIMARY_CODE = np.array([1., -1., -1., 1.])
CODES = {'phase_code_plus_minus_minus_plus': PRIMARY_CODE,
         'uncoded_control': np.array([1., 1., 1., 1.]),
         'alternating_code_control': np.array([1., -1., 1., -1.])}
PROTOCOL_SHA = '170C5EC4085DD0CB4F45E2FCC5B1B66722F16E5D1CD120536D2CC67BEB1C3320'


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf8')


def envelope(t, shifts, code=PRIMARY_CODE):
    result = np.zeros((len(shifts), len(t)), dtype=np.float64)
    for centre, sign in zip(CENTRES, code):
        arg = (t[None, :] - shifts[:, None] - centre) / SIGMA
        result += sign * np.exp(-0.5 * arg * arg)
    return result


def basis(t, shift):
    e = envelope(t, np.array([shift]))[0]
    return np.column_stack((e*np.sin(2*np.pi*256*t), e*np.cos(2*np.pi*256*t)))


def direct_ls(t, raw, shift):
    template = basis(t, shift)
    gram = template.T @ template
    return np.linalg.solve(gram, template.T @ raw)


def scan(t, X, shifts, code, deadline, *, injection_shifts=None, batch=64, progress=True):
    """Exact floating-point raw template projection, batched to bound memory."""
    sine, cosine = np.sin(2*np.pi*256*t), np.cos(2*np.pi*256*t)
    gram_rhs = np.column_stack((sine*sine, sine*cosine, cosine*cosine))
    y_parts = [np.ascontiguousarray((X*sine).T), np.ascontiguousarray((X*cosine).T)]
    if injection_shifts is not None:
        ei = envelope(t, injection_shifts)
        for e in ei:
            y_parts.append(np.column_stack((e*sine*sine, e*sine*cosine, e*cosine*cosine)))
    rhs = np.concatenate(y_parts, axis=1)
    result = np.empty((len(shifts), len(X), 2), dtype=np.float64)
    grams = np.empty((len(shifts), 3), dtype=np.float64)
    response = (np.empty((len(shifts), len(injection_shifts), 2, 2), dtype=np.float64)
                if injection_shifts is not None else None)
    for start in range(0, len(shifts), batch):
        if time.monotonic() > deadline:
            raise RuntimeError('NUMERIC_BUDGET_EXPIRED_NO_INFERENCE_RELEASE')
        stop = min(start+batch, len(shifts))
        e = envelope(t, shifts[start:stop], code)
        g = (e*e) @ gram_rhs
        b = e @ rhs
        det = g[:, 0]*g[:, 2]-g[:, 1]*g[:, 1]
        if not np.all(det > 0):
            raise RuntimeError('SINGULAR_TEMPLATE_GRAM')
        n = len(X)
        result[start:stop, :, 0] = (g[:, 2, None]*b[:, :n] - g[:, 1, None]*b[:, n:2*n])/det[:, None]
        result[start:stop, :, 1] = (g[:, 0, None]*b[:, n:2*n] - g[:, 1, None]*b[:, :n])/det[:, None]
        grams[start:stop] = g
        if response is not None:
            for j in range(len(injection_shifts)):
                c11, c12, c22 = b[:, 2*n+3*j:2*n+3*j+3].T
                response[start:stop, j, 0, 0] = (g[:, 2]*c11-g[:, 1]*c12)/det
                response[start:stop, j, 0, 1] = (g[:, 2]*c12-g[:, 1]*c22)/det
                response[start:stop, j, 1, 0] = (g[:, 0]*c12-g[:, 1]*c11)/det
                response[start:stop, j, 1, 1] = (g[:, 0]*c22-g[:, 1]*c12)/det
        if progress and (start == 0 or stop == len(shifts) or start % 512 == 0):
            print('PACKET_SCAN', start, stop, 'of', len(shifts), flush=True)
    return result, grams, response


def exact_single_projection_phase_power(noise_norm, amplitude, cut):
    """Continuous-phase detection probability at the included true template.

    The full-search detection probability is at least this value. The local
    noise vectors here are the observed data used as fixed injection contexts.
    """
    n = np.asarray(noise_norm)
    out = np.zeros(n.shape, dtype=np.float64)
    nonzero = n > 0
    c = (cut*cut - n[nonzero]*n[nonzero] - amplitude*amplitude)/(2*n[nonzero]*amplitude)
    out[nonzero] = np.arccos(np.clip(c, -1., 1.))/np.pi
    out[~nonzero] = float(amplitude > cut)
    return out


def geometry_checks():
    checks=[]
    phase = (np.arange(262144)+0.5)*(2*np.pi/262144)
    for alpha in (0.1, 0.025):
        r = math.sin(math.pi*alpha)
        for d in (0., .1, .5, .9, math.cos(math.pi*alpha), 1., 1.5, 2., 5.):
            fraction = float(np.mean(np.hypot(d+np.cos(phase), np.sin(phase)) < r))
            if fraction > alpha+2/len(phase):
                raise RuntimeError('RANDOM_PHASE_GEOMETRY_VALIDATION_FAILED')
            checks.append({'alpha':alpha,'noise_norm_over_A':d,'phase_grid_failure_fraction':fraction})
    return {'status':'PASS','phase_grid':len(phase),'cases':checks,
            'fixed_phase_counterexample':{'noise':'n=-A*(1,0)', 'source_phase':0,
                                          'observed_projection':[0,0],
                                          'meaning':'No confidence coverage for every fixed carrier phase is claimed.'}}


def run(root, out):
    started=time.monotonic()
    protocol_bytes=(root/'PROTOCOL.json').read_bytes()
    if sha(protocol_bytes)!=PROTOCOL_SHA:
        raise RuntimeError('FROZEN_PROTOCOL_SHA_MISMATCH')
    protocol=json.loads(protocol_bytes)
    deadline=started+protocol['computing_budget']['maximum_numeric_seconds']
    out.mkdir(parents=True,exist_ok=True)
    if (out/'RESULTS.json').exists():
        raise RuntimeError('RESULT_ALREADY_EXISTS_USE_A_NEW_OUTPUT_DIRECTORY')
    input_rows=protocol['inputs']
    raw_full=[]
    verification=[]
    for item in input_rows:
        path=root/'inputs'/(item['record_id']+'.npz')
        if sha(path.read_bytes())!=item['npz_sha256']:
            raise RuntimeError('INPUT_NPZ_SHA_MISMATCH:'+item['record_id'])
        with np.load(path,allow_pickle=False) as z:
            x=np.asarray(z['strain'],dtype=np.float64)
        if x.shape!=(68*FS,) or not np.isfinite(x).all():
            raise RuntimeError('INVALID_RAW_INPUT:'+item['record_id'])
        if sha(x.astype('<f8',copy=False).tobytes())!=item['raw_array_sha256']:
            raise RuntimeError('RAW_ARRAY_SHA_MISMATCH:'+item['record_id'])
        raw_full.append(x)
        verification.append({'record_id':item['record_id'],'npz_sha256':item['npz_sha256'],
                             'raw_array_sha256':item['raw_array_sha256'],'samples':len(x),'status':'PASS'})
    X=np.ascontiguousarray(np.stack(raw_full)[:,-6*FS:])
    t=np.arange(-2*FS,4*FS,dtype=np.float64)/FS
    shifts=np.arange(-1024,1025,dtype=np.float64)/FS
    inj_shifts=np.array(protocol['injection_design']['arrival_seconds'],dtype=np.float64)
    all_curves={}
    records=[]
    scan_timing={}
    for code_name,code in CODES.items():
        scan_started=time.monotonic()
        print('PACKET_CODE_BEGIN',code_name,flush=True)
        coeff,gram,response=scan(t,X,shifts,code,deadline,
                                injection_shifts=inj_shifts if code_name==next(iter(CODES)) else None)
        scan_timing[code_name]=time.monotonic()-scan_started
        all_curves[code_name]=coeff
        if code_name==next(iter(CODES)):
            main,main_gram,K=coeff,gram,response
        norm=np.hypot(coeff[:,:,0],coeff[:,:,1])
        for i,item in enumerate(input_rows):
            k=int(np.argmax(norm[:,i]))
            records.append({'code':code_name,'record_id':item['record_id'],'run':item['run'],
                            'target_gps':item['target_gps'],'arrival_shift_seconds':float(shifts[k]),
                            'maximum_coefficient_norm':float(norm[k,i]),
                            'sin_coefficient':float(coeff[k,i,0]),'cos_coefficient':float(coeff[k,i,1]),
                            'carrier_phase_rad':float(np.arctan2(coeff[k,i,1],coeff[k,i,0])),
                            'source_time_group':item['source_time_group']})
    g11,g12,g22=main_gram.T
    delta=np.hypot(g11-g22,2*g12)
    eig_min=float(np.min((g11+g22-delta)/(2*FS)))
    eig_max=float(np.max((g11+g22+delta)/(2*FS)))
    if eig_min<.14 or eig_max>.142:
        raise RuntimeError('DECLARED_TEMPLATE_GRAM_CERTIFICATE_FAILED')
    D=4*math.sqrt(math.sqrt(math.pi)/(2*SIGMA)+(1/FS)*4/(math.e*SIGMA**2))
    kappa_derivative=1-(0.5/FS)*D/math.sqrt(.14)
    if kappa_derivative<.99:
        raise RuntimeError('CONTINUOUS_ARRIVAL_DERIVATIVE_CERTIFICATE_FAILED')
    norm=np.hypot(main[:,:,0],main[:,:,1])
    global_lag,global_record=np.unravel_index(int(np.argmax(norm)),norm.shape)
    M=float(norm[global_lag,global_record]);M_guard=M*(1+1e-8)
    bound_A=M_guard/(.99*math.sin(math.pi*.1))
    bound_h=bound_A*math.sqrt(.142)
    bound_A4=M_guard/(.99*math.sin(math.pi*.025))
    print('PACKET_OBSERVED_MAXIMUM',format(M,'.17g'),'HRSS90',format(bound_h,'.17g'),flush=True)

    # Exact true-template response and deterministic simultaneous-grid injections.
    inj_indices=np.rint(inj_shifts*FS).astype(int)+1024
    identity_error=max(float(np.max(np.abs(K[k,j]-np.eye(2)))) for j,k in enumerate(inj_indices))
    if identity_error>5e-12:
        raise RuntimeError('INCLUDED_TEMPLATE_LINEAR_RESPONSE_IDENTITY_FAILED')
    phases=np.arange(32,dtype=np.float64)*(2*np.pi/32)
    directions=np.column_stack((np.cos(phases),np.sin(phases)))
    signal_response=np.einsum('tjkl,pl->jptk',K,directions,optimize=False)
    true_norm=norm[inj_indices,:].T
    amplitudes=np.logspace(-25,-18,57,dtype=np.float64)
    efficiency=[]
    recovery_by_context=np.zeros((len(amplitudes),len(X)),dtype=np.int64)
    injection_started=time.monotonic()
    for ai,A in enumerate(amplitudes):
        if time.monotonic()>deadline:
            raise RuntimeError('NUMERIC_BUDGET_EXPIRED_DURING_INJECTION_GRID')
        recovered=0
        for i in range(len(X)):
            injected=main[None,None,:,i,:]+A*signal_response
            detected=np.max(np.hypot(injected[:,:,:,0],injected[:,:,:,1]),axis=2)>M_guard
            count=int(np.count_nonzero(detected))
            recovered+=count;recovery_by_context[ai,i]=count
        exact_lower=exact_single_projection_phase_power(true_norm,A,M_guard)
        efficiency.append({'coefficient_A_det':float(A),'conservative_hrss_upper':float(A*math.sqrt(.142)),
                           'actual_hrss_phase_invariant_approx':float(A*math.sqrt(2*math.sqrt(math.pi)*SIGMA)),
                           'recovered':recovered,'variants':1920,'full_search_discrete_phase_efficiency':recovered/1920,
                           'analytic_continuous_phase_efficiency_lower_mean':float(np.mean(exact_lower)),
                           'analytic_continuous_phase_efficiency_lower_min':float(np.min(exact_lower))})
        if ai%14==0 or ai==len(amplitudes)-1:
            print('PACKET_INJECTION',ai+1,'/',len(amplitudes),'recovered',recovered,'/1920',flush=True)
    if np.any(np.diff([row['recovered'] for row in efficiency])<0):
        raise RuntimeError('RAY_SEARCH_EFFICIENCY_NONMONOTONIC')
    injection_seconds=time.monotonic()-injection_started

    # Independent direct raw-array checks, including full 68-second construction.
    direct_checks=[]
    tfull=np.arange(-64*FS,4*FS,dtype=np.float64)/FS
    for i in range(12):
        for j,shift in enumerate(inj_shifts):
            for phase in (0.,0.7,math.pi/2,math.pi):
                A=1e-22
                full_e=envelope(tfull,np.array([shift]))[0]
                signal=A*full_e*(np.sin(2*np.pi*256*tfull)*math.cos(phase)+np.cos(2*np.pi*256*tfull)*math.sin(phase))
                if np.count_nonzero(signal[:-6*FS]):
                    raise RuntimeError('NONZERO_FLOAT_TEMPLATE_EXCLUDED_FROM_PROJECTION')
                injected=raw_full[i]+signal
                actual=direct_ls(t,injected[-6*FS:],shift)
                expected=main[inj_indices[j],i]+A*directions[0] if phase==0 else main[inj_indices[j],i]+A*np.array([math.cos(phase),math.sin(phase)])
                error=float(np.max(np.abs(actual-expected)))
                scale=max(float(np.max(np.abs(actual))),A)
                if error>5e-12*scale:
                    raise RuntimeError('FULL_RAW_INJECTION_LINEARITY_FAILED')
                direct_checks.append({'record_id':input_rows[i]['record_id'],'shift':float(shift),
                                      'phase':phase,'absolute_error':error,'relative_error':error/scale})
    # Recompute a whole grid from one freshly injected full raw record.
    shift=-.25;phase=.7;A=1e-22
    e=envelope(tfull,np.array([shift]))[0]
    signal=A*e*(np.sin(2*np.pi*256*tfull)*math.cos(phase)+np.cos(2*np.pi*256*tfull)*math.sin(phase))
    injected=raw_full[0]+signal
    direct_curve,_,_=scan(t,injected[None,-6*FS:],shifts,PRIMARY_CODE,deadline,progress=False)
    predicted=main[:,0]+A*np.einsum('tkl,l->tk',K[:,0],np.array([math.cos(phase),math.sin(phase)]))
    whole_grid_error=float(np.max(np.abs(direct_curve[:,0]-predicted)))
    if whole_grid_error>5e-12*max(float(np.max(np.abs(predicted))),A):
        raise RuntimeError('FULL_SCAN_RAW_VS_LINEAR_RESPONSE_PARITY_FAILED')
    geometry=geometry_checks()
    elapsed=time.monotonic()-started
    if elapsed>900:
        raise RuntimeError('NUMERIC_BUDGET_EXPIRED_BEFORE_FINAL_EXPORT')
    try:
        import resource
        peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    except ImportError:
        peak_mib=None
    first_90=next((row for row in efficiency if row['full_search_discrete_phase_efficiency']>=.9),None)
    results={
      'schema':'GW_PHASE_CODED_PACKET_MODEL_CONDITIONAL_BOUND_V1',
      'status':'COMPLETE_FIXED_FAMILY_RAW_PROJECTION_AND_PHASE_ENSEMBLE_BOUND',
      'completed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'protocol_sha256':PROTOCOL_SHA,'implementation_sha256':sha(Path(__file__).read_bytes()),
      'inputs_verified':verification,'input_contexts':12,'source_time_groups':12,
      'target_duration_seconds':48,'allowed_packet_anchor_union_seconds':6,
      'independent_observation_count_asserted':False,
      'source_model':protocol['waveform'],'arrival_grid':protocol['arrival_grid'],
      'observed_global_maximum':{'coefficient_norm':M,'inflated_for_numeric_guard':M_guard,
                                'record_id':input_rows[global_record]['record_id'],
                                'run':input_rows[global_record]['run'],
                                'target_gps':input_rows[global_record]['target_gps'],
                                'arrival_shift_seconds':float(shifts[global_lag]),
                                'sin_coefficient':float(main[global_lag,global_record,0]),
                                'cos_coefficient':float(main[global_lag,global_record,1])},
      'primary_90_percent_phase_ensemble_bound':{'alpha':.1,'coefficient_A_det_upper':bound_A,
                                               'received_H1_hrss_upper_Hz_minus_half':bound_h,
                                               'scope':'At most one declared packet in the twelve supports and continuous arrival range; uniform source carrier phase independent of arbitrary fixed additive nuisance.',
                                               'noise_independence_across_records_required':False,
                                               'coverage_for_each_fixed_phase_claimed':False,
                                               'posterior_probability_claimed':False,
                                               'global_false_alarm_probability':None},
      'secondary_four_family_sensitivity_adjustment':{'alpha':.025,'coefficient_A_det_upper':bound_A4,
                                                    'received_H1_hrss_upper_Hz_minus_half':bound_A4*math.sqrt(.142),
                                                    'scope':'Four-family Bonferroni sensitivity illustration only; not a correction for every prior adaptive choice.'},
      'continuous_arrival_certificate':{'dt_weighted_gram_minimum':eig_min,'dt_weighted_gram_maximum':eig_max,
                                        'fixed_gram_lower_bound':.14,'fixed_full_packet_hrss_gram_upper_bound':.142,
                                        'derivative_norm_upper_bound':D,'nearest_grid_error_seconds':.5/FS,
                                        'derived_kappa_lower_bound':kappa_derivative,'used_kappa':.99,
                                        'basis_response_at_matching_grid_max_error':identity_error},
      'injection_comparison':{'status':'COMPLETE','amplitude_levels':57,'contexts':12,'phases_per_arrival':32,
                              'arrival_shifts':inj_shifts.tolist(),'variants_per_amplitude':1920,
                              'completed_variant_equivalent_evaluations':109440,
                              'new_independent_noise_observations':0,
                              'statistic_threshold':M_guard,'comparison':'Strict > observed global maximum with numeric guard',
                              'first_grid_amplitude_reaching_90_percent':first_90,
                              'is_confidence_bound':False,'efficiency':efficiency,
                              'recovered_per_context':recovery_by_context.tolist()},
      'descriptive_controls':{'codes':{name:code.tolist() for name,code in CODES.items()},
                               'records':records,'controls_used_for_inference':False,
                               'instrumental_or_artificial_origin_classifier':False},
      'validation':{'full_raw_injection_direct_projection_checks':len(direct_checks),
                     'maximum_direct_relative_error':max(c['relative_error'] for c in direct_checks),
                     'full_scan_raw_vs_response_maximum_absolute_error':whole_grid_error,
                     'geometry':geometry,'direct_checks':direct_checks},
      'runtime':{'numeric_wall_seconds':elapsed,'scan_seconds':scan_timing,
                 'injection_grid_seconds':injection_seconds,'peak_memory_MiB_linux':peak_mib,
                 'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform(),
                 'threads':{key:os.environ[key] for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},
                 'new_network_requests':0,'new_neural_calls':0,'new_installations':0},
      'old_4096_counters_modified':False,
      'interpretation_limits':protocol['scope_limits']+[
        'The primary linear projection deliberately does not estimate an empirical instrumental-noise FAR.',
        'Wrong-code controls are descriptive; the confidence theorem is not applied to a code-contrast or nonlinear score.',
        'The bound is conditional on the specified random-phase signal model and one-family statistic; it is not absence of all technosignatures.',
        'A fixed-phase signal could be cancelled by fixed additive nuisance; that counterexample is explicitly retained.']}
    write_json(out/'RESULTS.json',results)
    with (out/'observed_code_projections.csv').open('w',newline='',encoding='utf8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    with (out/'injection_efficiency.csv').open('w',newline='',encoding='utf8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(efficiency[0]));writer.writeheader();writer.writerows(efficiency)
    np.savez_compressed(out/'PROJECTION_AND_RESPONSE.npz',arrival_shifts=shifts,
                        primary_coefficients=main,primary_gram=main_gram,
                        injection_response=K,injection_arrivals=inj_shifts,
                        uncoded_coefficients=all_curves['uncoded_control'],
                        alternating_coefficients=all_curves['alternating_code_control'])
    write_json(out/'GEOMETRY_VALIDATION.json',geometry)
    print('PACKET_FINAL',json.dumps({'status':results['status'],'hrss90':bound_h,
                                    'coefficient_A90':bound_A,'numeric_seconds':elapsed,
                                    'peak_MiB':peak_mib,'injection_evaluations':109440}),flush=True)
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    root=args.root.resolve();out=args.out.resolve() if args.out else root/'results'
    try:
        run(root,out)
    except Exception:
        out.mkdir(parents=True,exist_ok=True)
        (out/'ERROR.log').write_text(traceback.format_exc(),encoding='utf8')
        raise


if __name__=='__main__':
    main()
