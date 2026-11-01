"""Engineering tests on synthetic arrays/tables only; zero real GW observations."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import time
import unittest
import numpy as np
from CPU_FEATURES import extract_record, features, FEATURE_NAMES, FS, NREF, NTARGET
from ANALYZE_TABLE import grouped_roles, rank_rows, descriptive_periodicity


def noise(seed):
    return np.random.default_rng(seed).normal(size=NREF+NTARGET)


def table():
    rng=np.random.default_rng(876)
    rows=[]
    for block in range(10):
        start=1_400_000_000.+8192*block
        for detector in ("H1","L1"):
            for j in range(16):
                rows.append(dict(record_id=f"{block}_{detector}_{j}",run="O4b",detector=detector,
                                 source_id=f"{block}_{detector}",source_start_gps=start,
                                 source_stop_gps=start+4096,gps=start+80+80*j,
                                 features={k:float(x) for k,x in zip(FEATURE_NAMES,rng.normal(size=len(FEATURE_NAMES)))}))
    return rows


class EngineTests(unittest.TestCase):
    def test_finite_features_and_disjoint_bands(self):
        result=extract_record(noise(1))
        self.assertEqual(set(FEATURE_NAMES),set(result["features"]))
        self.assertEqual(len(FEATURE_NAMES),19)
        self.assertAlmostEqual(sum(result["features"][f"band_{a}_{b}_fraction"] for a,b in ((64,128),(128,256),(256,512),(512,768))),1.,places=12)
        self.assertTrue(all(np.isfinite(v) for v in result["features"].values()))

    def test_persistent_tone_absolute_response_when_ratio_near_one(self):
        baseline=noise(2)
        t=np.arange(len(baseline))/FS
        tone=baseline+20*np.sin(2*np.pi*256*t)
        before,after=extract_record(baseline),extract_record(tone)
        a,b=before["features"],after["features"]
        self.assertLess(abs(b["log10_local_power_ratio"]),.05)
        self.assertGreater(b["log10_reference_band_power"]-a["log10_reference_band_power"],2.)
        self.assertGreater(b["log10_target_band_power"]-a["log10_target_band_power"],2.)
        self.assertAlmostEqual(after["diagnostics"]["reference_psd_peak_hz"],256.)

    def test_known_packet_interval(self):
        x=noise(3);t=np.arange(NTARGET)/FS
        env=sum(np.exp(-.5*((t-c)/.035)**2) for c in np.arange(.4,3.5,.5))
        x[NREF:]+=20*env*np.sin(2*np.pi*128*t)
        result=features(x)
        self.assertLess(abs(result["envelope_acf_lag_s"]-.5),.015)

    def test_invalid_input_rejection(self):
        for x in (np.zeros(NREF+NTARGET),np.ones(NREF+NTARGET),np.ones(NREF+NTARGET-1),
                  np.full(NREF+NTARGET,np.nan),np.full(NREF+NTARGET,np.inf)):
            with self.assertRaises(ValueError):
                features(x)
        x=noise(4);x[NREF+3]=np.nan
        with self.assertRaises(ValueError):
            features(x)

    def test_scientific_amplitude_is_finite(self):
        result=extract_record(noise(5)*1.e-22)
        self.assertTrue(all(np.isfinite(v) for v in result["features"].values()))
        self.assertLess(result["features"]["log10_target_band_power"],-40.)

    def test_source_and_coeval_group_no_leakage(self):
        rows,groups=grouped_roles(table())
        self.assertEqual(len(groups),10)
        mapping={}
        for row in rows:
            mapping.setdefault(row["source_start_gps"],set()).add(row["analysis_role"])
        self.assertTrue(all(len(v)==1 for v in mapping.values()))
        self.assertEqual({r["analysis_role"] for r in rows},{"TRAIN","CALIBRATION","TEST"})
        reverse,_=grouped_roles(list(reversed(table())))
        self.assertEqual({r["record_id"]:r["analysis_role"] for r in rows},
                         {r["record_id"]:r["analysis_role"] for r in reverse})

    def test_transitive_overlapping_source_containers(self):
        rows=table()[:1]
        a=rows[0]
        b=copy.deepcopy(a);b.update(record_id="b",detector="V1",source_id="b",source_start_gps=a["source_stop_gps"]-1,
                                  source_stop_gps=a["source_stop_gps"]+4095,gps=a["source_stop_gps"]+80)
        c=copy.deepcopy(b);c.update(record_id="c",detector="L1",source_id="c",source_start_gps=b["source_stop_gps"]-1,
                                  source_stop_gps=b["source_stop_gps"]+4095,gps=b["source_stop_gps"]+80)
        result,groups=grouped_roles([a,b,c])
        self.assertEqual(len(groups),1)
        self.assertEqual(len({r["source_time_group"] for r in result}),1)
        self.assertEqual(result[0]["analysis_role"],"UNSPLIT_TOO_FEW_SOURCE_GROUPS")

    def test_test_values_cannot_refit_training_or_calibration(self):
        original=table();ranked,report=rank_rows(original)
        changed=copy.deepcopy(original)
        test_id=next(r["record_id"] for r in ranked if r["analysis_role"]=="TEST")
        next(r for r in changed if r["record_id"]==test_id)["features"][FEATURE_NAMES[0]]=1.e6
        ranked2,report2=rank_rows(changed)
        self.assertEqual(report["models"],report2["models"])
        self.assertIn(test_id,report2["candidate_record_ids"])
        self.assertIsNone(report2["discovery_p_value"])
        self.assertLessEqual(len(report2["candidate_record_ids"]),8)
        self.assertFalse(report2["morphological_maximum_time_permutation_performed"])

    def test_constant_features_omitted(self):
        rows=table()
        for r in rows:r["features"][FEATURE_NAMES[0]]=7.
        _,report=rank_rows(rows)
        for model in report["models"].values():
            self.assertIn(FEATURE_NAMES[0],model["omitted_degenerate_features"])

    def test_duplicates_overlap_and_missing_tables_reject(self):
        for case in ([],table()[:1]*2):
            with self.assertRaises(ValueError):rank_rows(case)
        rows=table()[:2];rows[1]["gps"]=rows[0]["gps"]+1
        with self.assertRaises(ValueError):rank_rows(rows)

    def test_insufficient_reference_is_not_ranking_complete(self):
        _,report=rank_rows(table()[:16])
        self.assertEqual(report["status"],"TABLE_ANALYZED_NO_ELIGIBLE_TEST_RANKS")
        self.assertEqual(report["scored_test_records"],0)
        self.assertFalse(report["historical_source_roles_validated_here"])

    def test_cli_outputs_valid_jsonl_and_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);input_path=folder/"synthetic.jsonl"
            input_path.write_text("".join(json.dumps(r)+"\n" for r in table()),encoding="utf-8")
            done=subprocess.run([sys.executable,str(Path(__file__).with_name("ANALYZE_TABLE.py")),
                                 str(input_path),"--out",str(folder/"analysis")],
                                text=True,capture_output=True,timeout=20)
            self.assertEqual(done.returncode,0,done.stderr)
            report=json.loads((folder/"analysis"/"ANALYSIS.json").read_text())
            self.assertEqual(report["unique_input_records"],320)
            self.assertIsNone(report["discovery_p_value"])
            self.assertTrue((folder/"analysis"/"CANDIDATES.csv").read_text().startswith("record_id,"))

    def test_descriptive_gps_scan_uses_actual_gaps(self):
        rows=table();ranked,_=rank_rows(rows)
        for r in ranked:r["features"][FEATURE_NAMES[0]]=float(np.cos(2*np.pi*(r["gps"]-1_400_000_000)/500.))
        result=descriptive_periodicity(ranked,FEATURE_NAMES[0])
        self.assertEqual(len(result),2)
        for item in result:
            self.assertEqual(item["status"],"DESCRIPTIVE_COARSE_GPS_SCAN_ONLY")
            self.assertFalse(item["gaps_concatenated"])
            self.assertIsNone(item["p_value"])
            self.assertGreater(item["span_seconds"],len([r for r in ranked if r["detector"]==item["detector"] and r["analysis_role"]=="TEST"])*80)


if __name__=="__main__":
    started=time.perf_counter()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(EngineTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    path=Path(__file__).parent
    report=dict(schema="GW_CPU_ENGINEERING_VALIDATION_V1",tests_run=result.testsRun,
                failures=len(result.failures),errors=len(result.errors),successful=result.wasSuccessful(),
                wall_seconds=time.perf_counter()-started,synthetic_only=True,real_GW_observations=0,
                new_F2_evaluations=0,network_requests=0,user_Windows_runtime_tested=False,
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest().upper()
                               for p in (path/"CPU_FEATURES.py",path/"ANALYZE_TABLE.py",Path(__file__))})
    (path/"ENGINEERING_TEST_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    sys.exit(0 if result.wasSuccessful() else 1)
