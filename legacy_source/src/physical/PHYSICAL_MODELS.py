"""P3 fixed physical-parameter source probes, leading Newtonian approximation.

This module supplies two declared source models, not an artificial-origin
classifier: (1) a mass/momentum-conserving Newtonian rocket plus ballistic
exhaust with permanent memory and (2) a natural-degenerate circular compact
pair in the leading quadrupole approximation. No data loading, score fitting,
network request, model training or h_rss amplitude renormalization occurs.

The whole analytic source history is sampled on the requested 68-second
observation. A memory signal is never switched off; a persistent compact pair
is never switched on only in the target. The first 64 seconds may change.
"""
from __future__ import annotations

import hashlib
import json
import math
import numpy as np

SCHEMA = 'F7_P3_FIXED_NEWTONIAN_PHYSICAL_SOURCES_V1'
G = 6.67430e-11
C = 299792458.0
PARSEC_M = 3.085677581491367e16
M_JUPITER_KG = 1.89813e27
RATES = (4096, 16384)
CONTEXT_SECONDS = 68
TARGET_START_SECONDS = 64
CENTER_SECONDS = 66.0
FAMILIES = ('newtonian_rocket_memory', 'kepler_compact_pair')
CONTROLS = ('original', 'incoherent')
DISTANCE_GRID_PC = (0.001, 0.01, 0.1)
PRODUCTION_DISTANCE_PC = 0.01
INCLINATION_RAD = math.pi / 3.0
POLARIZATION_ANGLE_RAD = 0.2
ORBIT_PHASE_RAD = 0.37
ROCKET_DURATIONS_S = (0.01, 0.1, 10.0)
PAIR_FREQUENCIES_HZ = (64.0, 256.0, 512.0)


def need(ok, why):
    if not ok:
        raise RuntimeError('P3_PHYSICAL_SOURCE_HOLD: ' + str(why))


def stable_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def _number(value, name):
    need(type(value) in (int, float) and math.isfinite(value), 'FINITE_NUMBER_' + name)
    return float(value)


def source_configurations():
    """Six fixed source models. These parameters precede new noisy evaluation."""
    common = dict(distance_pc=PRODUCTION_DISTANCE_PC, inclination_rad=INCLINATION_RAD,
                  polarization_angle_rad=POLARIZATION_ANGLE_RAD)
    configurations = []
    for index, duration in enumerate(ROCKET_DURATIONS_S, 1):
        configurations.append(dict(
            source_id='ROCKET_T' + str(index), family='newtonian_rocket_memory',
            parameters=dict(common, initial_mass_kg=M_JUPITER_KG,
                initial_velocity_m_s=0.001*C, delta_velocity_m_s=0.001*C,
                relative_exhaust_speed_m_s=0.01*C, burn_duration_s=duration,
                burn_center_s=CENTER_SECONDS, velocity_transition='quintic_smoothstep',
                fiducial_body_radius_m=10000.0,
                source_model='Newtonian_rocket_plus_ballistic_exhaust_memory')))
    for index, frequency in enumerate(PAIR_FREQUENCIES_HZ, 1):
        configurations.append(dict(
            source_id='PAIR_F' + str(index), family='kepler_compact_pair',
            parameters=dict(common, component_mass_kg=1e24, gw_frequency_hz=frequency,
                gw_phase_rad=ORBIT_PHASE_RAD, phase_reference_s=CENTER_SECONDS,
                source_model='Newtonian_equal_mass_circular_compact_pair_quadrupole')))
    return configurations


def variants():
    """Twelve dictionaries: six fixed models times original/delayed-copy control."""
    return [dict(source, control=control, variant_id=source['source_id']+'_'+control)
            for source in source_configurations() for control in CONTROLS]


def _validated_variant(variant):
    need(isinstance(variant, dict) and any(variant == candidate for candidate in variants()),
         'EXACT_DECLARED_VARIANT')
    return variant


def quintic_transition(x):
    """C2 velocity transition; its first two derivatives vanish at both ends."""
    x = np.asarray(x, dtype=np.float64)
    s = np.clip(x, 0.0, 1.0)
    return s*s*s*(10.0+s*(-15.0+6.0*s))


def rocket_history(times_s, parameters):
    """Closed Newtonian rocket quantities in SI units, for arbitrary times.

    Exhaust is expelled backward at constant speed u relative to the rocket.
    Each emitted parcel then follows an inertial trajectory. Initial uniform
    translation supplies only a constant strain, subtracted in polarizations.
    Newtonian mass and momentum are conserved; internal energy powers kinetic
    energy. Relativistic rest-mass conversion is an omitted O(u^2/c^2) term.
    """
    t = np.asarray(times_s, dtype=np.float64)
    need(np.isfinite(t).all(), 'FINITE_SOURCE_TIMES')
    p = parameters
    mass0 = _number(p['initial_mass_kg'], 'initial_mass_kg')
    v0 = _number(p['initial_velocity_m_s'], 'initial_velocity_m_s')
    dv = _number(p['delta_velocity_m_s'], 'delta_velocity_m_s')
    exhaust = _number(p['relative_exhaust_speed_m_s'], 'relative_exhaust_speed_m_s')
    duration = _number(p['burn_duration_s'], 'burn_duration_s')
    center = _number(p['burn_center_s'], 'burn_center_s')
    need(mass0 > 0 and dv > 0 and exhaust > 0 and duration > 0, 'POSITIVE_ROCKET_PARAMETERS')
    need(max(abs(v0), abs(v0+dv), abs(v0-exhaust), abs(v0+dv-exhaust))/C <= 0.011,
         'DECLARED_NONRELATIVISTIC_SPEED_BOUND')
    start = center-duration/2.0
    x = (t-start)/duration
    s = np.clip(x, 0.0, 1.0)
    transition = quintic_transition(x)
    velocity_increment = dv*transition
    velocity = v0+velocity_increment
    acceleration = 30.0*dv/duration*s*s*(1.0-s)*(1.0-s)
    mass = mass0*np.exp(-velocity_increment/exhaust)
    # expm1 retains the small mass-loss/strain limit without cancellation.
    expelled = -mass0*np.expm1(-velocity_increment/exhaust)
    mass_flow = mass*acceleration/exhaust
    integral_transition = np.where(x < 0, 0.0,
        np.where(x > 1.0, x-0.5, 2.5*s**4-3.0*s**5+s**6))
    position = v0*t+dv*duration*integral_transition
    kinetic_second_moment_increment = exhaust*exhaust*expelled
    return dict(mass_kg=mass, expelled_mass_kg=expelled, velocity_m_s=velocity,
                acceleration_m_s2=acceleration, mass_flow_kg_s=mass_flow,
                position_m=position,
                second_moment_increment_kg_m2_s2=kinetic_second_moment_increment,
                kinetic_energy_increment_j=0.5*kinetic_second_moment_increment)


def compact_pair_parameters(parameters):
    """Kepler orbit and radiation-reaction validity diagnostics in SI units."""
    p = parameters
    mass = _number(p['component_mass_kg'], 'component_mass_kg')
    frequency = _number(p['gw_frequency_hz'], 'gw_frequency_hz')
    distance = _number(p['distance_pc'], 'distance_pc')*PARSEC_M
    need(mass > 0 and frequency > 0 and distance > 0, 'POSITIVE_PAIR_PARAMETERS')
    omega = math.pi*frequency
    radius = (G*mass/(4.0*omega*omega))**(1.0/3.0)
    separation = 2.0*radius
    velocity = omega*radius
    luminosity = (64.0/5.0)*G**4*mass**5/(C**5*separation**5)
    binding_energy = G*mass*mass/(2.0*separation)
    coalescence = binding_energy/(4.0*luminosity)
    frequency_derivative = 3.0*frequency/(8.0*coalescence)
    drift = frequency_derivative*CONTEXT_SECONDS
    phase_error = math.pi*frequency_derivative*CONTEXT_SECONDS**2
    radius_schwarzschild_component = 2.0*G*mass/C**2
    amplitude = 8.0*G*mass*radius*radius*omega*omega/(C**4*distance)
    need(velocity/C < 0.0011 and radius_schwarzschild_component/separation < 1e-5,
         'WEAK_FIELD_SLOW_ORBIT_BOUND')
    need(phase_error < 0.002 and coalescence > 1e7*CONTEXT_SECONDS,
         'CONSTANT_ORBIT_68S_APPROXIMATION_BOUND')
    return dict(orbital_angular_frequency_rad_s=omega, component_orbital_radius_m=radius,
                separation_m=separation, orbital_speed_m_s=velocity,
                orbital_speed_over_c=velocity/C,
                component_schwarzschild_radius_m=radius_schwarzschild_component,
                schwarzschild_to_separation_ratio=radius_schwarzschild_component/separation,
                face_on_strain_amplitude=amplitude, leading_gw_luminosity_w=luminosity,
                binding_energy_magnitude_j=binding_energy,
                leading_coalescence_time_s=coalescence,
                frequency_drift_68s_hz=drift,
                omitted_radiation_reaction_phase_68s_rad=phase_error,
                exact_relativistic_orbit=False, constant_orbit_approximation=True,
                ordinary_material_megastructure_claim=False,
                artificial_origin_identifiable=False)


def source_validity(family, parameters):
    if family == 'kepler_compact_pair':
        return compact_pair_parameters(parameters)
    need(family == 'newtonian_rocket_memory', 'DECLARED_FAMILY')
    p = parameters
    duration = float(p['burn_duration_s']);u = float(p['relative_exhaust_speed_m_s'])
    mass0 = float(p['initial_mass_kg']);dv = float(p['delta_velocity_m_s'])
    v0 = float(p['initial_velocity_m_s']);body = float(p['fiducial_body_radius_m'])
    lost = -mass0*math.expm1(-dv/u)
    max_speed = max(abs(v0), abs(v0+dv), abs(v0-u), abs(v0+dv-u))
    return dict(maximum_rocket_or_exhaust_speed_over_c=max_speed/C,
                expelled_mass_fraction=lost/mass0,
                final_mass_kg=mass0-lost,
                kinetic_energy_added_j=0.5*u*u*lost,
                omitted_rest_mass_energy_fraction=0.5*u*u*lost/(mass0*C*C),
                body_schwarzschild_to_radius=2.0*G*mass0/(C*C*body),
                fiducial_body_size_to_burn_light_distance=body/(C*duration),
                fiducial_body_kR_at_768hz=2.0*math.pi*768.0*body/C,
                fiducial_body_kR_at_inverse_burn_time=2.0*math.pi*body/(C*duration),
                body_radius_is_fiducial_not_an_extended_source_simulation=True,
                finite_body_stress_and_form_factor_not_computed=True,
                newtonian_mass_momentum_conservation=True,
                exact_relativistic_energy_conservation=False,
                source_stress_and_engine_feasibility_demonstrated=False,
                retarded_motion_corrections_order=max_speed/C,
                permanent_memory_retained=True,
                memory_strain_artificially_windowed=False)


def polarizations_at_times(times_s, family, parameters):
    """Physical source polarizations; distance fixes amplitude without rescaling."""
    t = np.asarray(times_s, dtype=np.float64)
    p = parameters
    distance = _number(p['distance_pc'], 'distance_pc')*PARSEC_M
    inclination = _number(p['inclination_rad'], 'inclination_rad')
    psi = _number(p['polarization_angle_rad'], 'polarization_angle_rad')
    need(distance > 0 and np.isfinite(t).all(), 'DISTANCE_AND_TIMES')
    cos_i = math.cos(inclination)
    if family == 'newtonian_rocket_memory':
        history = rocket_history(t, p)
        # hbar_zz = 4G*S/(c4D); TT hplus = hbar_zz*sin(i)^2/2.
        plus0 = (2.0*G/(C**4*distance))*history['second_moment_increment_kg_m2_s2']*(1.0-cos_i*cos_i)
        cross0 = np.zeros_like(plus0)
    elif family == 'kepler_compact_pair':
        orbit = compact_pair_parameters(p)
        phase = 2.0*orbit['orbital_angular_frequency_rad_s']*(t-float(p['phase_reference_s']))+float(p['gw_phase_rad'])
        amplitude = orbit['face_on_strain_amplitude']
        # The minus signs follow d2/dt2 of positions a(cosΩt,sinΩt,0).
        plus0 = -0.5*amplitude*(1.0+cos_i*cos_i)*np.cos(phase)
        cross0 = -amplitude*cos_i*np.sin(phase)
    else:
        need(False, 'DECLARED_FAMILY')
    cp, sp = math.cos(2.0*psi), math.sin(2.0*psi)
    hp = cp*plus0-sp*cross0
    hx = sp*plus0+cp*cross0
    need(np.isfinite(hp).all() and np.isfinite(hx).all(), 'FINITE_POLARIZATIONS')
    return hp, hx


def source_polarizations(rate_hz, variant, delay_s=0.0):
    """Sample the analytic full source history on 68s; no source truncation."""
    _validated_variant(variant)
    need(type(rate_hz) is int and rate_hz in RATES, 'RATE_4096_OR_16384')
    delay = _number(delay_s, 'delay_s')
    times = np.arange(CONTEXT_SECONDS*rate_hz, dtype=np.float64)/rate_hz-delay
    return polarizations_at_times(times,variant['family'],variant['parameters'])


def project_detectors(response_by_detector, variant, rates=(4096,)):
    _validated_variant(variant)
    need(type(rates) is tuple and rates and len(set(rates)) == len(rates) and
         all(type(fs) is int and fs in RATES for fs in rates), 'SUPPORTED_RATE_TUPLE')
    need(isinstance(response_by_detector, dict) and
         set(response_by_detector) in ({'H1','L1'},{'H1','L1','V1'}), 'HL_OR_HLV_RESPONSES')
    signal, responses = {}, {}
    for index, detector in enumerate(d for d in ('H1','L1','V1') if d in response_by_detector):
        response = response_by_detector[detector]
        need(isinstance(response,dict) and set(response) == {'Fplus','Fcross','delay_s'},
             'EXACT_RESPONSE_FIELDS')
        fp,fc,delay = (_number(response[key],detector+':'+key)
                       for key in ('Fplus','Fcross','delay_s'))
        need(fp*fp+fc*fc <= 1.0+1e-14 and abs(delay) <= 0.043,
             'BOUNDED_DECLARED_RESPONSE')
        extra = 0.15*index if variant['control'] == 'incoherent' else 0.0
        actual = delay+extra
        signal[detector] = {}
        for fs in rates:
            hp,hx = source_polarizations(fs,variant,actual)
            signal[detector][fs] = fp*hp+fc*hx
        responses[detector] = dict(Fplus=fp,Fcross=fc,delay_s=delay,
            negative_control_extra_delay_s=extra,applied_delay_s=actual)
    lineage = dict(schema=SCHEMA,variant=variant,rates_hz=list(rates),responses=responses,
        source_parameters_physical_units=variant['parameters'],
        source_model_id=variant['source_id'],
        physical_source_kind='leading_order_Newtonian_model',
        source_validity=source_validity(variant['family'],variant['parameters']),
        no_hrss_renormalization=True, amplitude_set_by_mass_motion_distance=True,
        full68s_source=True, source_model_continues_outside_observed_window=True,
        source_strain_switched_on_only_in_target=False,
        source_reference_nonzero_samples={det:{str(fs):int(np.count_nonzero(arr[:64*fs]))
            for fs,arr in bank.items()} for det,bank in signal.items()},
        normalization='PHYSICAL_MASS_MOTION_DISTANCE_SI_NOT_HRSS_OR_SNR',
        response_status='FROZEN_CALLER_RESPONSE_NOT_NEW_SKY_FIT',
        source_formula_role='Specified Newtonian source extension, not new general-relativistic simulation.',
        message_decoding=False,artificial_origin_inference=False,physical_FAP=False,
        thresholds_fit=False,new_F2_calls=0,network_access=False)
    lineage['signal_array_sha256'] = {d:{str(fs):hashlib.sha256(a.tobytes(order='C')).hexdigest().upper()
        for fs,a in bank.items()} for d,bank in signal.items()}
    lineage['lineage_sha256'] = hashlib.sha256(stable_bytes(lineage)).hexdigest().upper()
    return signal,lineage


def inject(raw_by_detector,response_by_detector,variant):
    """Add full analytic detector strains to copies; input arrays remain intact."""
    need(isinstance(raw_by_detector,dict) and isinstance(response_by_detector,dict) and
         set(raw_by_detector) in ({'H1','L1'},{'H1','L1','V1'}) and
         set(raw_by_detector) == set(response_by_detector), 'RAW_RESPONSE_DETECTORS')
    first = next(iter(raw_by_detector.values()))
    need(isinstance(first,dict), 'RAW_RATE_DICTIONARY')
    rates = tuple(sorted(first))
    need(rates and 4096 in rates and all(type(fs) is int and fs in RATES for fs in rates),
         'RAW_SUPPORTED_RATES')
    for detector,bank in raw_by_detector.items():
        need(isinstance(bank,dict) and tuple(sorted(bank)) == rates, 'SAME_RAW_RATES')
        for fs,array in bank.items():
            need(isinstance(array,np.ndarray) and array.dtype == np.float64 and
                 array.shape == (CONTEXT_SECONDS*fs,) and np.isfinite(array).all(),
                 'FINITE_RAW_FLOAT64_SHAPE')
    signal,lineage = project_detectors(response_by_detector,variant,rates)
    output = {};unchanged = True
    for detector,bank in raw_by_detector.items():
        output[detector] = {}
        for fs,raw in bank.items():
            projected = signal[detector][fs];result = raw.copy();active = projected != 0.0
            result[active] += projected[active]
            need(np.isfinite(result).all(), 'FINITE_INJECTED_STRAIN')
            output[detector][fs] = result
            unchanged = unchanged and result[:64*fs].tobytes() == raw[:64*fs].tobytes()
    lineage['injected_array_sha256'] = {d:{str(fs):hashlib.sha256(a.tobytes(order='C')).hexdigest().upper()
        for fs,a in bank.items()} for d,bank in output.items()}
    lineage['first64s_bitwise_unchanged'] = bool(unchanged)
    lineage.pop('lineage_sha256')
    lineage['lineage_sha256'] = hashlib.sha256(stable_bytes(lineage)).hexdigest().upper()
    return output,lineage
