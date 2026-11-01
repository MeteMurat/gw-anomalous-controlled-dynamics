"""Regenerate the original source-only figure series from retained equations.

Usage: python EXPORT_PHYSICAL_SERIES.py --model PATH/PHYSICAL_MODELS.py --out DIR
This explicitly vetted original module is SHA256-pinned; no detector data,
network calls, inference or parameter fitting is performed.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import numpy as np

EXPECTED_MODEL_SHA256='6AD6772D588D50CC973894CD2433E6F7CC595A947F24BA4C7F6CAC870B815069'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def generate(model_path, out):
 model_path=Path(model_path).resolve();out=Path(out).resolve()
 if sha(model_path)!=EXPECTED_MODEL_SHA256:
  raise ValueError('RETAINED_PHYSICAL_MODEL_SHA256_MISMATCH')
 spec=importlib.util.spec_from_file_location('_gw_retained_physical_equations_display',model_path)
 module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
 spec.loader.exec_module(module)
 configs=module.source_configurations()
 if len(configs)!=6:raise ValueError('EXPECTED_SIX_FIXED_SOURCE_CONFIGURATIONS')
 rt=np.linspace(58,75,6801);pt=np.linspace(64,64.06,2401)
 rh=np.asarray([module.polarizations_at_times(rt,c['family'],c['parameters'])[0] for c in configs[:3]])
 ph=np.asarray([module.polarizations_at_times(pt,c['family'],c['parameters'])[0] for c in configs[3:]])
 arrays={'rocket_times_s':rt,'rocket_hplus':rh,'pair_times_s':pt,'pair_hplus':ph}
 if rh.shape!=(3,6801) or ph.shape!=(3,2401) or not all(np.isfinite(x).all() for x in arrays.values()):
  raise ValueError('FINITE_EXPECTED_SOURCE_SERIES_REQUIRED')
 labels=['Burn '+str(c['parameters']['burn_duration_s'])+' s' for c in configs[:3]]
 labels += [str(int(c['parameters']['gw_frequency_hz']))+' Hz' for c in configs[3:]]
 out.mkdir(parents=True,exist_ok=True)
 target=out/'physical_source_series.npz'
 np.savez_compressed(target,**arrays,config_labels=np.asarray(labels,dtype='U30'))
 metadata={
  'schema':'GW_RETAINED_PHYSICAL_EQUATION_FIGURE_SERIES_V1',
  'labels':labels,'source_model_sha256':EXPECTED_MODEL_SHA256,
  'source_module_path':str(model_path),'source_module_sha256':EXPECTED_MODEL_SHA256,
  'source_function':'polarizations_at_times, source_configurations',
  'source_parameters':configs,'source_configs':configs,'distance_pc':0.01,
  'scope':'Source-only equations; not detectorstrain replay',
  'generation':'Re-evaluation of exact retained source equations on original figure time grids; no detector noise or new source fitting',
  'array_sha256':{k:hashlib.sha256(v.tobytes()).hexdigest().upper() for k,v in arrays.items()},
  'series_file_sha256':sha(target),'real_GW_records':0,'new_F2_evaluations':0,
  'original_recipe_path':'GW_20261024/evidence/model_analysis/source_only_diagnostics.py:source-only plotting block',
  'assumptions':'Leading Newtonian source approximations at declared parameters; no engine feasibility, calibrated detection efficiency, or artificial-origin claim',
 }
 (out/'physical_source_series.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
 return metadata

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--model',required=True,type=Path)
 parser.add_argument('--out',required=True,type=Path)
 args=parser.parse_args();result=generate(args.model,args.out)
 print(json.dumps({'status':'SOURCE_EQUATIONS_REGENERATED','array_sha256':result['array_sha256'],
                   'new_real_GW_records':0,'new_F2_evaluations':0},indent=2))
