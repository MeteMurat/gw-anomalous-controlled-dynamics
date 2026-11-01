"""Add a clearly labelled known-injection-location response from saved projections.

The original full-search exceedance, protocol and confidence bound are not
modified. This is a descriptive derived check, not a new decision threshold.
"""
from pathlib import Path
import csv
import hashlib
import json
import time
import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'
start=time.monotonic()
source=(OUT/'RESULTS.json').read_bytes()
r=json.loads(source)
with np.load(OUT/'PROJECTION_AND_RESPONSE.npz',allow_pickle=False) as data:
    shifts=data['arrival_shifts']
    coeff=data['primary_coefficients']
    arrivals=data['injection_arrivals']
    K=data['injection_response']
indices=np.rint(arrivals*4096).astype(int)+1024
noise=coeff[indices].transpose(1,0,2)
phase=np.arange(32)*(2*np.pi/32)
directions=np.column_stack((np.cos(phase),np.sin(phase)))
at_true=np.stack([directions@K[k,j].T for j,k in enumerate(indices)])
cut=r['observed_global_maximum']['inflated_for_numeric_guard']
rows=[]
for old in r['injection_comparison']['efficiency']:
    A=old['coefficient_A_det']
    values=noise[:,:,None,:]+A*at_true[None,:,:,:]
    count=int(np.count_nonzero(np.hypot(values[:,:,:,0],values[:,:,:,1])>cut))
    rows.append({'coefficient_A_det':A,
                 'actual_hrss_phase_invariant_approx':old['actual_hrss_phase_invariant_approx'],
                 'known_location_crossings':count,'variants':1920,
                 'known_location_crossing_fraction':count/1920,
                 'full_search_statistic_exceedances':old['recovered'],
                 'full_search_statistic_exceedance_fraction':old['full_search_discrete_phase_efficiency'],
                 'analytic_continuous_phase_known_location_fraction':old['analytic_continuous_phase_efficiency_lower_mean'],
                 'analytic_continuous_phase_minimum_over_contexts_and_arrivals':old['analytic_continuous_phase_efficiency_lower_min']})
assert all(a['known_location_crossings']<=a['full_search_statistic_exceedances'] for a in rows)
first90=next((a for a in rows if a['known_location_crossing_fraction']>=.9),None)
out={'schema':'GW_PACKET_KNOWN_LOCATION_DERIVED_RESPONSE_V1',
     'status':'COMPLETE_DERIVED_FROM_FROZEN_PROJECTION_OUTPUTS',
     'parent_results_sha256':hashlib.sha256(source).hexdigest().upper(),
     'primary_protocol_changed':False,'primary_confidence_bound_changed':False,
     'derived_criterion':'Norm of the exact two-basis LS response at the known injected arrival, strictly above the unchanged observed global maximum with numeric guard.',
     'context_count':12,'arrival_count':5,'phase_count':32,'amplitude_count':57,
     'evaluations':109440,'new_independent_noise_observations':0,
     'is_localization_or_event_recovery_test':False,
     'full_search_curve_label':'Full-search statistic exceedance; its largest response may occur at another arrival.',
     'known_location_curve_label':'Known-injection-location threshold crossing; no requirement on the global argmax.',
     'first_tested_amplitude_reaching_90_percent_known_location_fraction':first90,
     'rows':rows,'derived_numeric_seconds':time.monotonic()-start}
(OUT/'TRUE_LOCATION_RESPONSE.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf8')
with (OUT/'known_location_response.csv').open('w',newline='',encoding='utf8') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(json.dumps({'status':out['status'],'first90':first90,'seconds':out['derived_numeric_seconds']}))
