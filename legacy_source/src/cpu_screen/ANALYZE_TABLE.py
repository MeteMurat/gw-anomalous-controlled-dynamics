"""Source-held-out exploratory ranking of a completed CPU feature table.

One JSON object per input line is required. This module does not acquire data,
change the sampling frame, count neural trials, or produce discovery p-values.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy import signal
from CPU_FEATURES import FEATURE_NAMES

SPLIT_SALT = "GW_CPU_FEATURE_SOURCE_SPLIT_V1_20261030"
MIN_TRAIN_RECORDS, MIN_TRAIN_GROUPS = 32, 2
MAX_CANDIDATES = 8


def _hash(value):
    return hashlib.sha256((SPLIT_SALT+"|"+value).encode("utf-8")).hexdigest()


def validate_rows(rows):
    if not rows:
        raise ValueError("NONEMPTY_FEATURE_TABLE_REQUIRED")
    ids, detector_targets, source_meta = set(), set(), {}
    for r in rows:
        for k in ("record_id", "run", "detector", "source_id"):
            if not isinstance(r.get(k), str) or not r[k]:
                raise ValueError("MISSING_STRING:"+k)
        if r["record_id"] in ids:
            raise ValueError("DUPLICATE_RECORD_ID")
        ids.add(r["record_id"])
        for k in ("gps", "source_start_gps", "source_stop_gps"):
            if isinstance(r.get(k), bool) or not isinstance(r.get(k), (int, float)) or not math.isfinite(r[k]):
                raise ValueError("NONFINITE_TIME:"+k)
        a, b, g = r["source_start_gps"], r["source_stop_gps"], r["gps"]
        if not a <= g-64 < g+4 <= b:
            raise ValueError("FULL68S_NOT_IN_SOURCE")
        identity = (r["run"], r["detector"], g)
        if identity in detector_targets:
            raise ValueError("DETECTOR_GPS_REUSED")
        detector_targets.add(identity)
        skey = (r["run"], r["detector"], r["source_id"])
        if source_meta.setdefault(skey, (a, b)) != (a, b):
            raise ValueError("SOURCE_METADATA_INCONSISTENT")
        values = r.get("features")
        if not isinstance(values, dict) or set(FEATURE_NAMES)-set(values):
            raise ValueError("FEATURE_SCHEMA_MISSING")
        if not all(isinstance(values[k], (int, float)) and not isinstance(values[k], bool)
                   and math.isfinite(values[k]) for k in FEATURE_NAMES):
            raise ValueError("NONFINITE_FEATURE_TABLE")
    # Supports may touch, but must not overlap within one detector/run.
    by_stream = defaultdict(list)
    for r in rows:
        by_stream[r["run"], r["detector"]].append((r["gps"]-64, r["gps"]+4))
    for intervals in by_stream.values():
        intervals.sort()
        if any(b[0] < a[1] for a, b in zip(intervals, intervals[1:])):
            raise ValueError("OVERLAPPING_DETECTOR_SUPPORTS")


def grouped_roles(rows):
    """Assign whole connected source-time intervals, never individual windows.

    Overlapping source intervals within a run are merged across ALL detectors,
    including aliases with different source names. Connected components are
    deterministic and conservative: transitive overlaps remain together.
    Components are hashed, then allocated 60%/20%/remainder to train/cal/test.
    With >=3 components each role receives at least one. This is an analysis
    role split, not a probability sample and not proof of independence.
    """
    validate_rows(rows)
    by_run = defaultdict(list)
    for index, r in enumerate(rows):
        by_run[r["run"]].append((r["source_start_gps"], r["source_stop_gps"], index))
    groups, row_group = {}, {}
    for run, intervals in sorted(by_run.items()):
        intervals.sort()
        members, left, right = [], None, None
        def flush():
            if not members:
                return
            key = run+"|"+format(left, ".17g")+"|"+format(right, ".17g")
            group = "SRC_TIME_"+_hash(key)[:24]
            groups[group] = {"run": run, "start_gps": left, "stop_gps": right,
                             "records": len(members)}
            for j in members:
                row_group[j] = group
        for a, b, j in intervals:
            if right is not None and a >= right:
                flush(); members, left, right = [], None, None
            if left is None:
                left, right = a, b
            else:
                right = max(right, b)
            members.append(j)
        flush()
    assigned = {}
    # Split within run to avoid a run appearing solely in one global role.
    for run in sorted(by_run):
        keys = sorted((g for g in groups if groups[g]["run"] == run), key=_hash)
        n = len(keys)
        if n < 3:
            for g in keys:
                assigned[g] = "UNSPLIT_TOO_FEW_SOURCE_GROUPS"
            continue
        nt = max(1, min(n-2, int(math.floor(.6*n))))
        nc = max(1, min(n-nt-1, int(math.floor(.2*n))))
        for k, g in enumerate(keys):
            assigned[g] = "TRAIN" if k < nt else "CALIBRATION" if k < nt+nc else "TEST"
    return [{**r, "source_time_group": row_group[i], "analysis_role": assigned[row_group[i]]}
            for i, r in enumerate(rows)], groups


def _fit_reference(rows):
    a = np.asarray([[r["features"][k] for k in FEATURE_NAMES] for r in rows], dtype=np.float64)
    med = np.median(a, axis=0)
    mad = np.median(np.abs(a-med), axis=0)*1.482602218505602
    # Fixed fallback; degenerate dimensions are reported and omitted, rather
    # than assigned an arbitrarily tiny scale that manufactures huge scores.
    iqr = (np.quantile(a, .75, axis=0)-np.quantile(a, .25, axis=0))/1.348979500392164
    scale = np.where(mad > 0., mad, iqr)
    active = np.isfinite(scale) & (scale > 0.)
    return med, scale, active


def rank_rows(rows):
    ranked, groups = grouped_roles(rows)
    strata = defaultdict(list)
    for r in ranked:
        strata[r["run"], r["detector"]].append(r)
    models = {}
    for (run, detector), subset in sorted(strata.items()):
        key = run+"/"+detector
        train = [r for r in subset if r["analysis_role"] == "TRAIN"]
        n_groups = len({r["source_time_group"] for r in train})
        model = {"train_records": len(train), "train_source_time_groups": n_groups,
                 "minimum_train_records": MIN_TRAIN_RECORDS, "minimum_train_groups": MIN_TRAIN_GROUPS}
        models[key] = model
        if len(train) < MIN_TRAIN_RECORDS or n_groups < MIN_TRAIN_GROUPS:
            model["status"] = "INSUFFICIENT_HELD_OUT_REFERENCE"
            for r in subset:
                r.update(anomaly_score=None, score_status=model["status"])
            continue
        med, scale, active = _fit_reference(train)
        model.update(status="EXPLORATORY_REFERENCE_FITTED", active_features=[k for k,v in zip(FEATURE_NAMES,active) if v],
                     omitted_degenerate_features=[k for k,v in zip(FEATURE_NAMES,active) if not v],
                     location={k:float(v) for k,v in zip(FEATURE_NAMES,med)},
                     scale={k:(float(v) if ok else None) for k,v,ok in zip(FEATURE_NAMES,scale,active)})
        if not np.any(active):
            model["status"] = "ALL_REFERENCE_FEATURES_DEGENERATE"
        for r in subset:
            if not np.any(active):
                r.update(anomaly_score=None, score_status=model["status"]); continue
            v = np.asarray([r["features"][k] for k in FEATURE_NAMES])
            z = np.abs((v[active]-med[active])/scale[active])
            k = int(np.argmax(z))
            r.update(anomaly_score=float(z[k]), score_status="EXPLORATORY_RANK_ONLY",
                     score_driving_feature=np.asarray(FEATURE_NAMES)[active][k].item())
        calibration = [r["anomaly_score"] for r in subset
                       if r["analysis_role"] == "CALIBRATION" and r["anomaly_score"] is not None]
        model["calibration_records"] = len(calibration)
        model["calibration_source_time_groups"] = len({r["source_time_group"] for r in subset
                                                        if r["analysis_role"] == "CALIBRATION"})
        model["calibration_descriptive_quantiles"] = ({str(q):float(np.quantile(calibration,q,method="higher"))
                                                       for q in (.5,.95,.99)} if calibration else {})
    candidates = sorted((r for r in ranked if r["analysis_role"] == "TEST" and r["anomaly_score"] is not None),
                        key=lambda r:(-r["anomaly_score"],r["record_id"]))[:MAX_CANDIDATES]
    scored_test = sum(r["analysis_role"] == "TEST" and r["anomaly_score"] is not None for r in ranked)
    unscored_test = sum(r["analysis_role"] == "TEST" and r["anomaly_score"] is None for r in ranked)
    status = ("TABLE_ANALYZED_NO_ELIGIBLE_TEST_RANKS" if not scored_test else
              "EXPLORATORY_RANKING_PARTIAL_REFERENCE" if unscored_test else "EXPLORATORY_RANKING_COMPLETE")
    report = {
        "schema":"GW_CPU_TABLE_EXPLORATORY_ANALYSIS_V1", "status":status,
        "unique_input_records":len(rows), "source_time_groups":len(groups), "group_definitions":groups,
        "scored_test_records":scored_test, "unscored_test_records":unscored_test,
        "role_records":dict(Counter(r["analysis_role"] for r in ranked)), "models":models,
        "candidate_limit":MAX_CANDIDATES, "candidate_record_ids":[r["record_id"] for r in candidates],
        "discovery_p_value":None, "independent_observation_count":None,
        "counter_semantics":"Unique supplied completed feature records only; no legacy trial count modification.",
        "interpretation":"Source-held-out candidate ranking; neither significance nor artificial-origin inference.",
        "selection_frame_and_inclusion_probabilities_validated_here":False,
        "historical_source_roles_validated_here":False,
        "morphological_maximum_time_permutation_performed":False,
        "limits":["Reference/sample role splitting does not establish exchangeability or independence.",
                  "Source intervals must be genuine physical identities, not artificial per-window labels.",
                  "Historical source-role exclusions require an external verified source manifest before this split.",
                  "Top-eight ranking is a bounded review budget, not an eight-event detection claim.",
                  "Missing source strata or insufficient training references are reported without substitution."]}
    return ranked, report


def descriptive_periodicity(rows, feature):
    """Coarse fixed-grid Lomb-Scargle on actual TEST GPS values, without FAP.

    Scans 4096 linearly spaced frequencies from 2/span to 1/160 Hz. This is a
    prespecified descriptive coarse scan, not an exhaustive period search;
    there is no universally applicable Nyquist frequency for irregular data.
    The explicit upper limit comes from the proposed 80-s sampling design.
    """
    if feature not in FEATURE_NAMES:
        raise ValueError("UNKNOWN_PERIODICITY_FEATURE")
    output = []
    by_stratum = defaultdict(list)
    for r in rows:
        if r["analysis_role"] == "TEST":
            by_stratum[r["run"],r["detector"]].append(r)
    for (run, detector), subset in sorted(by_stratum.items()):
        subset = sorted(subset,key=lambda r:r["gps"])
        t = np.asarray([r["gps"] for r in subset],dtype=np.float64)
        y = np.asarray([r["features"][feature] for r in subset],dtype=np.float64)
        span = float(t[-1]-t[0]) if len(t)>1 else 0.
        record = {"run":run,"detector":detector,"feature":feature,"records":len(t),"span_seconds":span,
                  "p_value":None,"status":"INSUFFICIENT_PERIOD_SCAN_DOMAIN"}
        if len(t) >= 20 and span > 320. and np.var(y)>0.:
            t -= t[0]
            frequencies = np.linspace(2./span,1./160.,4096)
            powers = signal.lombscargle(t,y,2*np.pi*frequencies,precenter=False,
                                        normalize=True,floating_mean=True)
            j = int(np.argmax(powers))
            # The sampling-window spectrum exposes aliases; it is not a null.
            spectral_window = np.asarray([np.abs(np.mean(np.exp(2j*np.pi*f*t)))**2 for f in frequencies])
            record.update(status="DESCRIPTIVE_COARSE_GPS_SCAN_ONLY",frequency_grid_hz=[float(frequencies[0]),float(frequencies[-1])],
                          frequency_bins=len(frequencies),peak_frequency_hz=float(frequencies[j]),
                          peak_period_seconds=float(1./frequencies[j]),peak_normalized_power=float(powers[j]),
                          window_power_at_peak=float(spectral_window[j]),
                          window_maximum_power=float(np.max(spectral_window)),
                          gaps_concatenated=False, independent_samples_assumed=False)
        output.append(record)
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_jsonl",type=Path)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--periodicity-feature",choices=FEATURE_NAMES)
    args=parser.parse_args()
    raw=args.input_jsonl.read_bytes()
    rows=[json.loads(line) for line in raw.decode("utf-8-sig").splitlines() if line.strip()]
    ranked,report=rank_rows(rows)
    report["input_sha256"]=hashlib.sha256(raw).hexdigest().upper()
    if args.periodicity_feature:
        report["descriptive_periodicity"]=descriptive_periodicity(ranked,args.periodicity_feature)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"ANALYSIS.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    (args.out/"RANKED_RECORDS.jsonl").write_text("".join(json.dumps(r,sort_keys=True,allow_nan=False)+"\n" for r in ranked),encoding="utf-8")
    with (args.out/"CANDIDATES.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["record_id","run","detector","gps","source_id","source_time_group","analysis_role","anomaly_score","score_driving_feature"]
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader()
        for r in ranked:
            if r["record_id"] in report["candidate_record_ids"]:
                w.writerow(r)
    print(json.dumps({"status":report["status"],"unique_records":len(rows),"candidates":len(report["candidate_record_ids"]),"discovery_p_value":None}))


if __name__=="__main__":
    main()
