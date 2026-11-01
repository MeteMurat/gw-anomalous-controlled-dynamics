#!/usr/bin/env python3
"""Recount retained scores under explicit comparison units. No new GW analysis.

A post-hoc CAL rank diagnostic never changes registered cuts. Strict score
thresholds and observed ties are retained; no randomization forces equal counts.
"""
from pathlib import Path
from collections import defaultdict
import argparse, csv, hashlib, json, math, time
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,default=ROOT,help='Output directory; archived inputs always remain beside this script.')
ARGS=parser.parse_args()
OUT=ARGS.out.resolve()
OUT.mkdir(parents=True,exist_ok=True)
START=time.perf_counter()
def load(p):return json.loads((ROOT/p).read_text())
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def table(name,rows):
 assert rows
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def jsonrows(folder):return [json.loads(p.read_text()) for p in sorted((ROOT/folder).glob('*.json'))]
manifest=load('INPUT_MANIFEST.json')
for item in manifest['files']:
 p=ROOT/item['path'];assert p.is_file() and p.stat().st_size==item['bytes']
 assert hashlib.file_digest(p.open('rb'),'sha256').hexdigest().upper()==item['sha256'],item['path']
# Registered historical cuts and exactly paired receipt recounters.
cr=load('inputs/summaries/coherence_dev_result.json');cuts=cr['assessment']['thresholds']
cal=jsonrows('inputs/legacy/coherence_dev/CALIBRATION')
assert len(cal)==24
legacy_cal=[]
for run in ['O4a','O4b']:
 rc=[r for r in cal if r['header']['topology']==run]
 for method in ['COHERENCE','ENERGY','FROZEN_F4']:
  n=sum(r['scores'][method]>cuts[method][run] for r in rc)
  assert n==1 and len(rc)==12
  legacy_cal.append({'run':run,'method':method,'cut':cuts[method][run],'unit':'CAL context','above':n,'denominator':len(rc),'physical_FAR':False})
table('LEGACY_CALIBRATION_CONTEXT_COUNTS.csv',legacy_cal)
legacy=[]
for stage in ['coherence_dev','fresh6','p2','p3']:
 baselines=jsonrows('inputs/legacy/'+stage+'/BASELINES')
 units=jsonrows('inputs/legacy/'+stage+'/UNITS')
 originals=[u for u in units if u['variant']['control']=='original']
 base={b['header']['noise_id']:b for b in baselines}
 methods=sorted(set.intersection(*(set(u['scores']) for u in units)))
 assert len(base)==len(baselines)
 for method in methods:
  for run in ['O4a','O4b','ALL']:
   panel=[u for u in originals if run=='ALL' or u['header']['topology']==run]
   if not panel:continue
   keys=sorted(set(u['header']['noise_id'] for u in panel)); bpanel=[base[k] for k in keys]
   allbase=[b for b in baselines if run=='ALL' or b['header']['topology']==run]
   above=up=down=baseabove=0
   for u in panel:
    cut=cuts[method][u['header']['topology']]
    a=u['scores'][method]>cut; b=base[u['header']['noise_id']]['scores'][method]>cut
    above+=a;baseabove+=b;up+=a and not b;down+=b and not a
   noise_above=sum(b['scores'][method]>cuts[method][b['header']['topology']] for b in bpanel)
   all_noise=sum(b['scores'][method]>cuts[method][b['header']['topology']] for b in allbase)
   legacy.append({'stage':stage,'run':run,'method':method,'original_variants':len(panel),'noise_contexts_with_injections':len(bpanel),'all_noise_contexts':len(allbase),'source_blocks_with_injections':len(set(x['header']['block_id'] for x in panel)),'ordinary_above':above,'repeated_positive_baselines':baseabove,'upward':up,'downward':down,'net_threshold_lift':(up-down)/len(panel),'noise_above_injected_contexts':noise_above,'noise_above_all_contexts':all_noise,'equal_CAL_context_count':True,'equal_heldout_FAR_established':False})
# Validate exact retained headline counts, without replacing source-block weighted pilot.
for stage,expected in [('coherence_dev',(32,24)),('fresh6',(96,43)),('p2',(48,21)),('p3',(9,0))]:
 r=[x for x in legacy if x['stage']==stage and x['run']=='ALL']
 assert {x['method']:x['ordinary_above'] for x in r}['COHERENCE']==expected[0]
 assert {x['method']:x['ordinary_above'] for x in r}['ENERGY']==expected[1]
table('LEGACY_PAIRED_FIXED_CUT_RECOUNT.csv',legacy)
# New H1 survey: same source-group max unit for CAL and TEST diagnostic.
def readcsv(p):
 with (ROOT/p).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
scores=readcsv('inputs/survey/results/ANALYSIS/SCORES.csv')
features=readcsv('inputs/survey/results/ANALYSIS/FEATURE_TABLE.csv')
fm={x['record_id']:x for x in features}
assert len(fm)==4020 and len(scores)==4020
methods=['CHEAP','ENERGY']; groups={}
for row in scores:
 f=fm[row['record_id']]
 for k in ['run','source_time_group','analysis_role']:assert row[k]==f[k]
 key=(row['run'],row['analysis_role'],row['source_time_group'])
 if key not in groups:groups[key]={'CHEAP':-math.inf,'ENERGY':-math.inf,'n':0}
 g=groups[key];g['n']+=1
 g['CHEAP']=max(g['CHEAP'],float(row['anomaly_score']))
 g['ENERGY']=max(g['ENERGY'],float(f['log10_local_power_ratio']))
variants=jsonrows('inputs/survey/results/SECONDARY_INJECTIONS/VARIANTS')
assert len(variants)==144 and len(set(v['record_id'] for v in variants))==12
score_by_id={r['record_id']:r for r in scores}
assert all(score_by_id[v['record_id']]['analysis_role']=='TEST' for v in variants)
inj_result=load('inputs/survey/results/SECONDARY_INJECTIONS/INJECTION_RESULT.json')
for v in variants:
 key=(v['run'],'TEST',v['source_time_group']); g=groups[key]
 for m in methods:
  assert g[m]==v['outcome'][m]['baseline_group_max']
  assert inj_result['calibration'][v['run']][m]['cut']==v['outcome'][m]['cut']
registered=[];rankrows=[];attainrows=[]
for run in ['O4a','O4b']:
 cal=[g for (r,role,_),g in groups.items() if r==run and role=='CALIBRATION']
 test=[g for (r,role,_),g in groups.items() if r==run and role=='TEST']
 vs=[v for v in variants if v['run']==run]
 assert len(cal)==25 and len(test)==27 and len(vs)==72
 options={}
 for m in methods:
  # Every unique score produces a deterministic strict upper-set rule.
  options[m]={}
  for cut in sorted(set(g[m] for g in cal),reverse=True):
   n=sum(g[m]>cut for g in cal)
   options[m][n]=cut
   attainrows.append({'run':run,'method':m,'CAL_groups_above':n,'CAL_groups':len(cal),'cut':cut})
 common=sorted(set(options['CHEAP'])&set(options['ENERGY']))
 for count in [n for n in common if n<=5]:
  cc={m:options[m][count] for m in methods}
  eligibility=[v for v in vs if all(v['outcome'][m]['baseline_group_max']<=cc[m] for m in methods)]
  for m in methods:
   c=cc[m]
   assert sum(g[m]>c for g in cal)==count
   vals=[v['outcome'][m] for v in vs]
   commonvals=[v['outcome'][m] for v in eligibility]
   rr={'run':run,'CAL_groups_above_each_method':count,'CAL_groups':25,'method':m,'cut':c,'TEST_noise_groups_above':sum(g[m]>c for g in test),'TEST_noise_groups':27,'injection_contexts':6,'injected_variants':72,'ordinary_context_above':sum(x['injected_score']>c for x in vals),'new_context_crossings':sum(x['noise_score']<=c<x['injected_score'] for x in vals),'ordinary_group_above':sum(x['injected_group_max']>c for x in vals),'new_group_crossings':sum(x['baseline_group_max']<=c<x['injected_group_max'] for x in vals),'common_negative_group_contexts':len(set(v['record_id'] for v in eligibility)),'common_negative_group_variants':len(eligibility),'common_negative_group_crossings':sum(x['injected_group_max']>c for x in commonvals),'registered_cut_row':count==0,'selection':'posthoc deterministic CAL rank; TEST scores never set thresholds','physical_FAR':False}
   if count==0:assert c==inj_result['calibration'][run][m]['cut'];registered.append(rr)
   rankrows.append(rr)
table('SURVEY_CAL_RANK_OPERATING_POINTS.csv',rankrows)
table('SURVEY_ATTAINABLE_CAL_RANKS.csv',attainrows)
# Preserve registered endpoint and separately report a common-negative subset.
paired=[]
for endpoint in ['context','source_group']:
 def baseline(v,m):return v['outcome'][m]['noise_score' if endpoint=='context' else 'baseline_group_max']
 def injected(v,m):return v['outcome'][m]['injected_score' if endpoint=='context' else 'injected_group_max']
 eligible=[v for v in variants if all(baseline(v,m)<=v['outcome'][m]['cut'] for m in methods)]
 for family in ['ALL']+sorted(set(v['family'] for v in eligible)):
  vp=[v for v in eligible if family=='ALL' or v['family']==family]
  for m in methods:
   above=sum(injected(v,m)>v['outcome'][m]['cut'] for v in vp)
   paired.append({'endpoint':endpoint,'family':family,'method':m,'common_negative_contexts':len(set(v['record_id'] for v in vp)),'variants':len(vp),'new_crossings':above,'fraction':above/len(vp),'is_posthoc_subset':True,'fixed_thresholds_unchanged':True,'physical_FAR':False})
table('SURVEY_COMMON_NEGATIVE_BASELINES.csv',paired)
contextrows=[]
for rid in sorted(set(v['record_id'] for v in variants)):
 rv=[v for v in variants if v['record_id']==rid]
 assert len(rv)==12
 row={'record_id':rid,'run':rv[0]['run'],'source_time_group':rv[0]['source_time_group'],'variants':12}
 for m in methods:
  row[m+'_context_baseline_positive']=rv[0]['outcome'][m]['noise_exceeds_cut']
  row[m+'_group_baseline_positive']=rv[0]['outcome'][m]['group_noise_exceeds_cut']
  row[m+'_context_new']=sum(v['outcome'][m]['new_crossing'] for v in rv)
  row[m+'_group_new']=sum(v['outcome'][m]['group_new_crossing'] for v in rv)
 row['common_group_eligible']=not(row['CHEAP_group_baseline_positive'] or row['ENERGY_group_baseline_positive'])
 contextrows.append(row)
table('SURVEY_PAIRED_CONTEXT_CONTRASTS.csv',contextrows)
assert next(x for x in paired if x['endpoint']=='source_group' and x['family']=='ALL' and x['method']=='CHEAP')['new_crossings']==87
assert next(x for x in paired if x['endpoint']=='source_group' and x['family']=='ALL' and x['method']=='ENERGY')['new_crossings']==63
summary={
 'schema':'GW_PAIRED_COMPARISON_EQUIVALENCE_AUDIT_V1','status':'PASS_SAVED_SCORE_RECOUNT_AND_EXPLICIT_SCOPE',
 'read_only_scientific_inputs':True,'new_strain_or_neural_computation':False,
 'input_files_verified':len(manifest['files']),'archive_sha256':manifest['archive_sha256'],
 'legacy_CAL_each_method_each_run':'1/12 strict exceedances at original method-specific cuts',
 'new_survey_CAL_each_method_each_run':'0/25 strict source-group exceedances at original method-specific cuts',
 'new_survey_TEST_noise_groups':{'O4a':{'CHEAP':'2/27','ENERGY':'1/27'},'O4b':{'CHEAP':'0/27','ENERGY':'2/27'}},
 'registered_context_new_crossings':{'CHEAP':'96/144','ENERGY':'69/144','common_negative_contexts':12},
 'all_144_variants_use_fixed_TEST_source_groups':True,
 'registered_group_new_crossings':{'CHEAP':'87/144','ENERGY':'69/144','CHEAP_already_positive_groups':1,'ENERGY_already_positive_groups':0},
 'posthoc_common_negative_group_subset':{'contexts':11,'excluded_context':'R4096_0949','run_contexts':{'O4a':5,'O4b':6},'variants':132,'CHEAP':'87/132','ENERGY':'63/132','equal_context_paired_difference':'24/132 = 2/11','equal_run_paired_difference':'(15/60 + 9/72)/2 = 3/16','interpretation':'Same eligibility opportunity at unchanged CAL cuts; dependent repeated variants; posthoc subset changes epoch weighting and is descriptive only'},
 'CAL_rank_rows':len(rankrows),'threshold_selection_uses_TEST':False,'registered_cuts_changed':False,
 'matched_population_FAR_established':False,'independent_variant_or_significance_claim':False,
 'runtime_seconds':time.perf_counter()-START
}
dump('COMPARISON_AUDIT.json',summary)
print(json.dumps(summary,indent=2))
