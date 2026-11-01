#!/usr/bin/env python3
"""Bounded reproduction of archived GW results, tables and display figures.

The default run never downloads strain, trains a model, changes historical
state, or executes arbitrary archived scripts. See docs/REPRODUCTION_LEVELS.md.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys

SCHEMA = "GW_ARCHIVED_RESULT_REPRODUCTION_V1"


class ReproductionError(RuntimeError):
    pass


def read_json(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        return json.load(stream)


def write_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                     allow_nan=False)+"\n", encoding="utf-8")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def repo_file(root, relative):
    """Reject escaping paths and symlink aliases before opening inputs."""
    root = Path(root).resolve()
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ReproductionError("UNSAFE_REPOSITORY_PATH: "+str(relative))
    path = root/candidate
    if not path.resolve().is_relative_to(root):
        raise ReproductionError("PATH_OUTSIDE_REPOSITORY: "+str(relative))
    if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
        raise ReproductionError("SYMLINK_INPUT: "+str(relative))
    return path


def verify_manifest(root, relative="SHA256_MANIFEST.json"):
    path = repo_file(root, relative)
    if not path.is_file():
        raise ReproductionError("REQUIRED_MANIFEST_MISSING: "+relative)
    manifest = read_json(path)
    members = manifest.get("members")
    if not isinstance(members, dict) or not members:
        raise ReproductionError("MANIFEST_MEMBERS_REQUIRED")
    checked = []
    for name, value in sorted(members.items()):
        item = repo_file(root, name)
        expected = value.get("sha256") if isinstance(value, dict) else value
        if not isinstance(expected, str) or len(expected) != 64:
            raise ReproductionError("INVALID_MEMBER_DIGEST: "+name)
        if not item.is_file():
            raise ReproductionError("MANIFEST_INPUT_MISSING: "+name)
        if isinstance(value, dict) and "bytes" in value and item.stat().st_size != value["bytes"]:
            raise ReproductionError("MEMBER_SIZE_MISMATCH: "+name)
        actual = sha256(item)
        if actual != expected.upper():
            raise ReproductionError("MEMBER_SHA256_MISMATCH: "+name)
        checked.append(name)
    return {"status":"VERIFIED", "manifest":relative,
            "manifest_sha256":sha256(path), "verified_files":len(checked)}


def flatten(value, prefix=""):
    if isinstance(value, dict):
        for key in sorted(value):
            yield from flatten(value[key], prefix+"."+key if prefix else key)
    else:
        yield prefix, value


def experiment_map(ledger):
    experiments = ledger.get("completed_experiment_details")
    if not isinstance(experiments, list) or not experiments:
        raise ReproductionError("COMPLETED_EXPERIMENT_LEDGER_REQUIRED")
    mapping = {x["id"]:x for x in experiments}
    if len(mapping) != len(experiments):
        raise ReproductionError("DUPLICATE_EXPERIMENT_ID")
    return mapping


def reproduce_tables(ledger, out, source_path, source_sha):
    """Transcribe every retained metric with its scope and evidence source."""
    experiments = experiment_map(ledger)
    rows = []
    for identifier, item in experiments.items():
        for family in ("counts", "outcomes"):
            for metric, value in flatten(item.get(family, {})):
                rows.append({"experiment_id":identifier, "experiment_title":item.get("title", ""),
                             "metric":family+"."+metric,
                             "value_json":json.dumps(value, ensure_ascii=False, allow_nan=False),
                             "reported_primary_source":item.get("reported_primary_source", ""),
                             "evidence_level":item.get("manuscript_evidence_level", ""),
                             "verification_level":item.get("current_verification", ""),
                             "scope_limits":" | ".join(item.get("limits", [])),
                             "ledger_path":source_path, "ledger_sha256":source_sha})
    path = out/"scientific_results.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    write_json(out/"scientific_results.json", {
        "schema":"GW_RETAINED_SCIENTIFIC_RESULT_TABLE_V1",
        "status":"REGENERATED_FROM_FROZEN_LEDGER", "new_raw_strain_replays":0,
        "source":{"path":source_path, "sha256":source_sha},
        "rows":rows, "experiments":list(experiments),
        "limits":"Counts and original evidence tiers are retained; this is not independent raw-data reprocessing."})
    return {"asset":"scientific_results.csv/json", "status":"reproduced_from_retained_numeric_evidence",
            "rows":len(rows), "experiments":len(experiments), "source_sha256":source_sha}


def recompute_conditional_ranks(ledger, out):
    """Recompute the declared finite Monte-Carlo ranks, not a new null."""
    experiments = experiment_map(ledger)
    rows = []
    if "OBS192" in experiments:
        item = experiments["OBS192"]
        rows.append(("OBS192", "conditional_p", item["counts"]["exceedances"],
                     item["counts"]["transforms"], item["outcomes"]["conditional_p"]))
    if "TIMELINE29" in experiments:
        item = experiments["TIMELINE29"]
        for prefix in ("single", "pair"):
            rows.append(("TIMELINE29", prefix+"_p", item["outcomes"][prefix+"_exceedances"],
                         item["counts"]["conditional_transforms"], item["outcomes"][prefix+"_p"]))
    results = []
    for experiment, endpoint, exceed, draws, expected in rows:
        if type(exceed) is not int or type(draws) is not int or not 0 <= exceed <= draws:
            raise ReproductionError("INVALID_CONDITIONAL_RANK_COUNTS: "+experiment)
        value = (exceed+1)/(draws+1)
        if not math.isclose(value, expected, rel_tol=0., abs_tol=2e-15):
            raise ReproductionError("REPORTED_RANK_MISMATCH: "+experiment+"/"+endpoint)
        results.append({"experiment":experiment, "endpoint":endpoint, "exceedances":exceed,
                        "transformations":draws, "recomputed_value":value,
                        "reported_value":expected, "status":"ARITHMETIC_REPRODUCED"})
    write_json(out/"conditional_rank_arithmetic.json", {
        "schema":"GW_CONDITIONAL_RANK_ARITHMETIC_REPLAY_V1", "endpoints":results,
        "formula":"(1+exceedances)/(1+transformations)",
        "independent_null_observations_added":0,
        "scope":"Original conditional working-null interpretation retained; no search-wide false-alarm calibration is added."})
    return {"asset":"conditional_rank_arithmetic.json", "status":"reproduced_arithmetic",
            "endpoints":len(results)}


def _plot_modules():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise ReproductionError("PLOTTING_DEPENDENCY_MISSING: use an existing environment with matplotlib/numpy or --tables-only") from exc
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10,
                         "axes.spines.top":False, "axes.spines.right":False})
    return plt, np


def _count_bars(ax, labels, numerators, denominators, colors):
    if len(labels) != len(numerators) or len(labels) != len(denominators):
        raise ReproductionError("PLOT_COUNT_SHAPE")
    if any(type(a) is not int or type(n) is not int or n <= 0 or not 0 <= a <= n
           for a,n in zip(numerators, denominators)):
        raise ReproductionError("PLOT_COUNT_RANGE")
    bars = ax.bar(labels, [a/n for a,n in zip(numerators, denominators)], color=colors)
    for bar,a,n in zip(bars,numerators,denominators):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+.025, f"{a}/{n}", ha="center", fontsize=9)
    ax.set_ylim(0,1.16); ax.grid(axis="y",alpha=.2); ax.set_axisbelow(True)


def reproduce_summary_plots(ledger, out, source_sha):
    """New display summaries of retained counts; no pooled performance claim."""
    plt, _ = _plot_modules()
    experiments = experiment_map(ledger)
    spec = (("PILOT240","primary_originals",("F4_exceedances","energy_exceedances"),("Learned","Energy")),
            ("COH_DEV80","originals",("COH_above","energy_above"),("Correlation","Energy")),
            ("FRESH6","originals",("COH_above","energy_above"),("Correlation","Energy")),
            ("P2","originals",("COH_original_above","energy_original_above"),("Correlation","Energy")))
    present = [s for s in spec if s[0] in experiments]
    outputs = []
    if present:
        fig, axes = plt.subplots(1,len(present),figsize=(3.25*len(present),4.2),squeeze=False)
        for ax,(identifier,denom,keys,labels) in zip(axes[0],present):
            item = experiments[identifier];n = item["counts"][denom]
            _count_bars(ax,list(labels),[item["outcomes"][k] for k in keys],[n,n],["#2166ac","#c26927"])
            ax.set_title({"PILOT240":"Learned-score pilot", "COH_DEV80":"Correlation development",
                          "FRESH6":"New-source validation", "P2":"Structured packets"}[identifier])
            ax.tick_params(axis="x",labelrotation=15)
        axes[0,0].set_ylabel("Ordinary threshold-exceedance fraction")
        fig.suptitle("Retained injection responses: separate finite experiments",fontsize=13)
        fig.text(.03,.025,"Thresholds, cohorts and shared-context designs differ between panels. No matched-FAR superiority or independent-binomial intervals.",fontsize=8)
        fig.tight_layout(rect=(0,.09,1,.9))
        for extension in ("png","pdf"):
            fig.savefig(out/("retained_injection_responses."+extension),dpi=180)
        plt.close(fig)
        outputs.append({"asset":"retained_injection_responses.png/pdf", "status":"reproduced_from_retained_counts",
                        "experiment_ids":[s[0] for s in present],"ledger_sha256":source_sha})
    if "FRESH6" in experiments and "P2" in experiments and "P4" in experiments:
        fig, axes = plt.subplots(1,3,figsize=(12.5,4.5))
        p2 = experiments["P2"];n = p2["counts"]["originals"]
        _count_bars(axes[0],["Original","Reversed","Extra delay"],
                    [p2["outcomes"][k] for k in ("COH_original_above","COH_reversed_above","COH_extra_delay_above")],
                    [n,p2["counts"]["reversed"],p2["counts"]["extra_delay"]],["#2166ac","#668aad","#9d3935"])
        axes[0].set_title("Structured-packet correlation acceptance")
        fresh = experiments["FRESH6"]["outcomes"]
        noise = [fresh["noise_O4a"],fresh["noise_O4b"]]
        _count_bars(axes[1],["O4a COH","O4a E","O4b COH","O4b E"],
                    [noise[0]["COH"],noise[0]["energy"],noise[1]["COH"],noise[1]["energy"]],
                    [noise[0]["n"]]*2+[noise[1]["n"]]*2,["#2166ac","#c26927"]*2)
        axes[1].set_title("Fresh-source noise exceedances")
        p4 = experiments["P4"]["outcomes"]
        fractions = [str(p4[k]).split("/") for k in ("original_P2_old_winner_raw_outside","delayed_P2_old_winner_raw_outside")]
        _count_bars(axes[2],["Original","Extra delay"],[int(x[0]) for x in fractions],
                    [int(x[1]) for x in fractions],["#2166ac","#9d3935"])
        axes[2].set_title("Winning raw peak outside physical lag")
        axes[0].set_ylabel("Finite-panel fraction")
        for ax in axes:ax.tick_params(axis="x",labelrotation=15)
        fig.text(.03,.025,"Shared injections and reused contexts are retained. Fresh6 noise-guard failure remains binding; broad-lag diagnosis is not a validated new veto.",fontsize=8)
        fig.tight_layout(rect=(0,.09,1,1))
        for extension in ("png","pdf"):
            fig.savefig(out/("retained_noise_and_timing_controls."+extension),dpi=180)
        plt.close(fig)
        outputs.append({"asset":"retained_noise_and_timing_controls.png/pdf", "status":"reproduced_from_retained_counts",
                        "experiment_ids":["FRESH6","P2","P4"],"ledger_sha256":source_sha})
    return outputs


def reproduce_p2_counts(source, out):
    """Portable redraw of the archived P2 count plot, without old builder side effects."""
    plt, np = _plot_modules()
    counts = read_json(source)
    groups = {g["control"]:g for g in counts["controls"]}
    controls = ("original","time_reversed","incoherent")
    labels = ("Original signal","Time reversed","Extra detector delays")
    denominators = [groups[c]["n"] for c in controls]
    if len(set(denominators)) != 1 or denominators[0] <= 0:
        raise ReproductionError("P2_EQUAL_CONTROL_DENOMINATORS_REQUIRED")
    n = denominators[0]; x = np.arange(len(controls))
    fig, axes = plt.subplots(1,2,figsize=(12,4.9),sharey=True)
    colors = {"COHERENCE":"#2166ac","ENERGY":"#c26927"}
    for ax,key,title in zip(axes,("above","upward"),
                            ("A  Fixed-cut threshold exceedances","B  Upward crossings from matched baselines")):
        for j,method in enumerate(("COHERENCE","ENERGY")):
            values = [groups[c]["methods"][method][key] for c in controls]
            if any(type(v) is not int or not 0 <= v <= n for v in values):
                raise ReproductionError("P2_COUNT_RANGE")
            bars = ax.bar(x+(j-.5)*.34,values,width=.32,color=colors[method],label=method,zorder=3)
            for bar,value in zip(bars,values):
                ax.text(bar.get_x()+bar.get_width()/2,value+n/60,f"{value}/{n}",ha="center",fontsize=10)
        ax.set_xticks(x,labels,rotation=12,ha="right");ax.set_ylim(0,n*1.125)
        ax.set_title(title,loc="left",fontsize=10.5,pad=12);ax.grid(axis="y",alpha=.22);ax.set_axisbelow(True)
    axes[0].set_ylabel(f"Variant count ({n} per control)")
    axes[0].legend(frameon=False,loc="upper left",bbox_to_anchor=(0,-.28),ncol=2)
    fig.suptitle("P2: short structured transients - sensitivity and control acceptance",fontsize=13,y=.97)
    figure_counts = counts["counts"]
    fig.text(.06,.025,f"Exploratory reuse of {figure_counts['injection_contexts']} noise contexts and "
             f"{figure_counts['source_blocks']} opened source blocks; frozen cuts; no FAR matching.\n"
             "Count-based redraw from archived result records; no independent-trial intervals or new raw-strain replay.",fontsize=8.5)
    fig.subplots_adjust(top=.82,bottom=.32,wspace=.12,left=.065,right=.99)
    path = out/"P2_DUYARLILIK_VE_KONTROLLER.png"
    fig.savefig(path,dpi=180);fig.savefig(path.with_suffix(".pdf"));plt.close(fig)
    return path


def reproduce_saved_lag_curves(root, recipe, out):
    """Redraw signed saved P4 curves and verify their archived peak values."""
    plt, np = _plot_modules()
    pair = recipe.get("pair", "H1_L1")
    paths = [repo_file(root, recipe[k]) for k in ("baseline_path","original_path","delayed_path")]
    records = [read_json(p) for p in paths]
    noise_ids = {record.get("header",{}).get("noise_id") for record in records}
    block_ids = {record.get("header",{}).get("block_id") for record in records}
    if None in noise_ids or len(noise_ids)!=1 or None in block_ids or len(block_ids)!=1:
        raise ReproductionError("SAVED_CURVES_DO_NOT_SHARE_NOISE_CONTEXT")
    fig, axes = plt.subplots(3,2,figsize=(10.7,8.0),sharex=True)
    rows = ("Unmodified noise","Physically projected original","Extra-delay copy")
    diagnostic_rows = []
    for axes_row,label,record,path in zip(axes,rows,records,paths):
        diagnostic = record["diagnostic"]; fs = diagnostic["rate_hz"]
        pair_record = diagnostic["per_pair"][pair]
        cap_ms = pair_record["physical_cap_samples"]/fs*1000
        for ax,key,column in zip(axes_row,("raw_correlation","envelope_power_correlation"),
                                  ("Raw whitened strain","Centered envelope power")):
            values = pair_record[key]
            lag = np.asarray(values["lag_samples"],dtype=np.float64)
            signed = np.asarray(values["signed_normalized_correlation"],dtype=np.float64)
            if lag.ndim != 1 or signed.shape != lag.shape or not np.isfinite(signed).all() or not np.isfinite(lag).all():
                raise ReproductionError("INVALID_SAVED_LAG_CURVE")
            maximum = float(np.max(np.abs(signed)))
            physical = float(np.max(np.abs(signed[np.abs(lag)<=pair_record["physical_cap_samples"]])))
            if not math.isclose(maximum,values["broad_abs_max"],rel_tol=1e-13,abs_tol=1e-15):
                raise ReproductionError("ARCHIVED_BROAD_LAG_MAXIMUM_MISMATCH")
            if not math.isclose(physical,values["physical_abs_max"],rel_tol=1e-13,abs_tol=1e-15):
                raise ReproductionError("ARCHIVED_PHYSICAL_LAG_MAXIMUM_MISMATCH")
            ax.plot(lag/fs*1000,np.abs(signed),color="#2166ac",linewidth=.85)
            ax.axvspan(-cap_ms,cap_ms,color="#8cb995",alpha=.25,label="Physical lag interval")
            declared = (record.get("declared_pair_source_delays_s") or {}).get(pair)
            if declared is not None:
                ax.axvline(declared*1000,color="#b93450",linewidth=.9,linestyle="--")
            ax.set_title(label+" / "+column,fontsize=9,loc="left")
            ax.set_ylabel("Absolute normalized correlation");ax.grid(alpha=.15)
            diagnostic_rows.append({"input":str(path.relative_to(root)),"input_sha256":sha256(path),
                                    "pair":pair,"channel":key,"broad_abs_max":maximum,"physical_abs_max":physical})
    for ax in axes[-1]:ax.set_xlabel("Signed detector-pair lag [ms]")
    fig.suptitle(recipe.get("title","Saved broad-lag timing diagnosis"),fontsize=12)
    fig.text(.04,.014,"Verified archived curve arrays; no raw-strain replay, fitted veto, common-sky reconstruction or new physical validation.",fontsize=8)
    fig.tight_layout(rect=(0,.04,1,.96))
    stem=recipe.get("output_stem","P4_SAVED_LAG_CURVES")
    if Path(stem).name != stem:raise ReproductionError("UNSAFE_FIGURE_OUTPUT_STEM")
    for extension in ("png","pdf"):fig.savefig(out/(stem+"."+extension),dpi=180)
    plt.close(fig)
    write_json(out/(stem+"_ARITHMETIC.json"),{"schema":"GW_SAVED_LAG_CURVE_REPLAY_V1","rows":diagnostic_rows})
    return stem+".png/pdf"


def reproduce_timeline(root, recipe, out):
    """Recompute saved-matrix endpoints and redraw the observation timeline."""
    plt, np = _plot_modules()
    matrix_path=repo_file(root,recipe["matrix_path"]);result_path=repo_file(root,recipe["result_path"])
    result=read_json(result_path)
    with np.load(matrix_path,allow_pickle=False) as data:
        scores=data["f4_consensus"].copy();times=data["target_gps"].copy()
        topology=data["topology"].astype(str);pairs=data["eligible_pairs_0based"].copy()
    if scores.ndim != 2 or scores.size>10_000_000 or scores.shape[1]!=len(times) or len(times)!=len(topology):
        raise ReproductionError("TIMELINE_MATRIX_SHAPE")
    if not np.isfinite(scores).all() or not np.isfinite(times).all() or scores.shape[0]<2:
        raise ReproductionError("NONFINITE_TIMELINE_MATRIX")
    if pairs.ndim!=2 or pairs.shape[1]!=2 or pairs.dtype.kind not in 'iu' or pairs.min()<0 or pairs.max()>=len(times):
        raise ReproductionError("TIMELINE_PAIR_INDEX")
    endpoints={"P":scores.max(axis=1),"C":np.minimum(scores[:,pairs[:,0]],scores[:,pairs[:,1]]).max(axis=1)}
    arithmetic=[]
    for key,values in endpoints.items():
        actual=float(values[0]);exceed=int(np.count_nonzero(values[1:]>=values[0]));p=(1+exceed)/scores.shape[0]
        declared=result["tests"][key]
        if actual!=declared["observed_statistic"] or exceed!=declared["null_exceedances_including_ties"]:
            raise ReproductionError("SAVED_MATRIX_ENDPOINT_MISMATCH: "+key)
        if not math.isclose(p,declared["p_conditional"],rel_tol=0.,abs_tol=2e-15):
            raise ReproductionError("SAVED_MATRIX_RANK_MISMATCH: "+key)
        arithmetic.append({"endpoint":key,"observed_statistic":actual,"exceedances":exceed,
                           "conditional_p":p,"original_transform_count":scores.shape[0]-1})
    if result["observed_windows"]!=scores.shape[1] or result["eligible_pairs"]!=len(pairs):
        raise ReproductionError("TIMELINE_REPORTED_EXPOSURE_MISMATCH")
    fig,axes=plt.subplots(2,2,figsize=(8.3,5.8));observed=scores[0]
    runs=sorted(set(topology.tolist()))
    if len(runs)!=2:raise ReproductionError("TIMELINE_TWO_RUN_DISPLAY_REQUIRED")
    for ax,run,color in zip(axes[0],runs,("#216a9b","#28775d")):
        ix=np.flatnonzero(topology==run);t0=times[ix].min();days=(times[ix]-t0)/86400
        ax.scatter(days,observed[ix],s=13,color=color,alpha=.8)
        best=int(ix[np.argmax(observed[ix])])
        ax.scatter([(times[best]-t0)/86400],[observed[best]],s=55,facecolors="none",edgecolors="#b93450")
        ax.set_title(f"{run}: {len(ix)} separated four-second targets",loc="left",fontsize=9)
        ax.set_xlabel(f"Days from GPS {t0:.0f}");ax.set_ylabel("Frozen learned-ranking score");ax.grid(axis="y",alpha=.18)
    for ax,key in zip(axes[1],("P","C")):
        values=endpoints[key];declared=result["tests"][key]
        ax.hist(values[1:],bins=32,color="#c2cedd",edgecolor="white");ax.axvline(values[0],color="#b93450")
        ax.set_title("Largest single-window score" if key=="P" else "Largest adjacent-pair minimum",loc="left",fontsize=9)
        ax.set_xlabel(f"{key}: observed {values[0]:.3f}");ax.set_ylabel("Conditional transformations")
        ax.text(.97,.93,f"p_cond={declared['p_conditional']:.3f}\np_adj={declared['p_bonferroni_two_statistics']:.3f}",
                transform=ax.transAxes,ha="right",va="top",fontsize=9)
    fig.tight_layout(pad=1.1,h_pad=2,w_pad=2)
    stem="GW_TIMELINE_EXPLORATORY_EN"
    for extension in ("png","pdf"):fig.savefig(out/(stem+"."+extension),dpi=200,bbox_inches="tight")
    plt.close(fig)
    write_json(out/"saved_matrix_endpoint_replay.json",{
        "schema":"GW_SAVED_SCORE_MATRIX_REPLAY_V1","source_matrix_sha256":sha256(matrix_path),
        "source_result_sha256":sha256(result_path),"endpoints":arithmetic,
        "new_raw_strain_or_neural_inference":0,"scope":"Same archived within-source conditional transformations; no independent search exposure added."})
    return stem+".png/pdf"


def reproduce_source_series(root, recipe, out):
    """Display explicitly generated frozen-model source series; no detector data."""
    plt, np = _plot_modules()
    series=repo_file(root,recipe["series_path"]);metadata_path=repo_file(root,recipe["metadata_path"])
    metadata=read_json(metadata_path)
    with np.load(series,allow_pickle=False) as values:
        rocket_times=values["rocket_times_s"].copy();rocket=values["rocket_hplus"].copy()
        pair_times=values["pair_times_s"].copy();pairs=values["pair_hplus"].copy()
    labels=metadata["labels"]
    if rocket.shape!=(3,len(rocket_times)) or pairs.shape!=(3,len(pair_times)) or len(labels)!=6:
        raise ReproductionError("PHYSICAL_SOURCE_SERIES_SHAPE")
    if any(not np.isfinite(v).all() for v in (rocket_times,rocket,pair_times,pairs)):
        raise ReproductionError("NONFINITE_PHYSICAL_SOURCE_SERIES")
    if not metadata.get("source_model_sha256") or len(metadata.get("source_parameters",[]))!=6:
        raise ReproductionError("PHYSICAL_SOURCE_PROVENANCE_REQUIRED")
    fig,axes=plt.subplots(1,2,figsize=(10.5,4.8))
    for times,signals,names,ax,scale,title in (
        (rocket_times,rocket,labels[:3],axes[0],1e-20,"Newtonian rocket-exhaust memory"),
        (pair_times,pairs,labels[3:],axes[1],1e-23,"Newtonian compact-pair proxy")):
        for vector,name in zip(signals,names):ax.plot(times,vector/scale,label=name,linewidth=1.0)
        ax.set_title(title,loc="left",fontsize=10);ax.set_xlabel("Source time [s]")
        ax.set_ylabel(f"Source h+ / {scale:.0e}");ax.grid(alpha=.2);ax.legend(frameon=False,fontsize=8)
    axes[0].axvline(64,color="gray",linestyle="--",linewidth=.8)
    axes[0].axvline(68,color="gray",linestyle="--",linewidth=.8)
    fig.text(.045,.02,"Source-only frozen-equation series at declared parameters; not a detector-response replay, source identification or physical population bound.",fontsize=8)
    fig.tight_layout(rect=(0,.07,1,1))
    for extension in ("png","pdf"):fig.savefig(out/("PHYSICAL_SOURCE_MODELS."+extension),dpi=180)
    plt.close(fig)
    write_json(out/"PHYSICAL_SOURCE_SERIES_PROVENANCE.json",{
        "schema":"GW_PHYSICAL_SOURCE_DISPLAY_REPLAY_V1","series_sha256":sha256(series),
        "metadata_sha256":sha256(metadata_path),"source_model_sha256":metadata["source_model_sha256"],
        "source_parameters":metadata["source_parameters"],"new_detector_strain_calculations":0,
        "scope":"Display of source-only series generated from the frozen equations; no sensitivity or source-origin measurement added."})
    return "PHYSICAL_SOURCE_MODELS.png/pdf"


def figure_coverage(root, out, index_relative, make_plots):
    """Accept only declared narrow adapters; never execute an index's commands."""
    index_path = repo_file(root,index_relative)
    if not index_path.is_file():
        return [{"asset":index_relative,"status":"unavailable","reason":"required figure coverage index missing"}]
    index = read_json(index_path)
    entries = index.get("figures",[])
    if isinstance(entries,dict):entries = [dict(v,figure_id=k) for k,v in entries.items()]
    results=[]
    for item in entries:
        name = item.get("manuscript_path",item.get("figure_id",item.get("name","unnamed")))
        relative = item.get("repository_path",item.get("retained_path"))
        if not relative:
            results.append({"asset":name,"status":"unavailable","reason":"no repository-relative retained asset path"});continue
        path=repo_file(root,relative)
        if not path.is_file():
            results.append({"asset":name,"status":"unavailable","reason":"retained image missing","expected_path":relative});continue
        actual=sha256(path); expected=item.get("sha256")
        if expected and actual != expected.upper():
            raise ReproductionError("FIGURE_SHA256_MISMATCH: "+relative)
        result={"asset":name,"retained_path":relative,"sha256":actual,"status":"retained_only",
                "level":"Verified original display product; not recomputed from raw strain.",
                "source_archive":item.get("source_archive"),"limits":item.get("limits",[])}
        recipe=item.get("portable_recipe") or {}
        if make_plots and recipe.get("kind")=="p2_archived_counts_v1":
            source=repo_file(root,recipe["counts_path"])
            if not source.is_file():
                result.update(status="unavailable",reason="declared P2 count input missing")
            else:
                expected_input=recipe.get("counts_sha256")
                if expected_input and sha256(source)!=expected_input.upper():
                    raise ReproductionError("FIGURE_RECIPE_INPUT_SHA256_MISMATCH")
                generated=reproduce_p2_counts(source,out)
                result.update(status="reproduced_from_archived_counts",generated_path=str(generated.relative_to(out)),
                              numeric_input_path=recipe["counts_path"],numeric_input_sha256=sha256(source),
                              bitwise_image_equivalence_claimed=False)
        elif make_plots and recipe.get("kind")=="p4_saved_lag_curves_v1":
            generated=reproduce_saved_lag_curves(root,recipe,out)
            result.update(status="reproduced_from_saved_curve_arrays",generated_path=generated,bitwise_image_equivalence_claimed=False)
        elif make_plots and recipe.get("kind")=="timeline_saved_score_matrix_v1":
            generated=reproduce_timeline(root,recipe,out)
            result.update(status="reproduced_from_saved_score_matrix",generated_path=generated,bitwise_image_equivalence_claimed=False)
        elif make_plots and recipe.get("kind")=="physical_source_series_v1":
            generated=reproduce_source_series(root,recipe,out)
            result.update(status="reproduced_from_frozen_model_source_series",generated_path=generated,bitwise_image_equivalence_claimed=False)
        results.append(result)
    return results


def run(root, out, tables_only=False, cpu_tests=False):
    root=Path(root).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    report={"schema":SCHEMA,"status":"STARTED","python":platform.python_version(),
            "scope":"Archived-result arithmetic, tables and figures; not a complete raw-strain/model replay.",
            "raw_strain_downloads":0,"model_training_runs":0,"new_full_search_trials":0,
            "completed_4096_physical_survey_claimed":False,"assets":[],"limitations":[
                "The presence of archived source code does not replace unavailable frozen model weights or original raw caches.",
                "Historical terminal-summary measurements retain their original evidence level.",
                "Regenerated figures describe shared contexts and declared cuts; they do not add independent observations."]}
    try:
        report["integrity"]=verify_manifest(root)
        ledger_relative="evidence/GW_PROJECT_EVIDENCE_LEDGER.json"
        ledger_path=repo_file(root,ledger_relative)
        ledger=read_json(ledger_path);ledger_sha=sha256(ledger_path)
        report["assets"].append(reproduce_tables(ledger,out,ledger_relative,ledger_sha))
        report["assets"].append(recompute_conditional_ranks(ledger,out))
        if not tables_only:report["assets"].extend(reproduce_summary_plots(ledger,out,ledger_sha))
        report["assets"].extend(figure_coverage(root,out,"evidence/FIGURE_AND_RESULT_INDEX.json",not tables_only))
        if cpu_tests:
            locations=("src/cpu_screen/TEST_ENGINE.py","src/cpu_features/TEST_ENGINE.py","engine/TEST_ENGINE.py")
            test=next((repo_file(root,p) for p in locations if repo_file(root,p).is_file()),None)
            if test is None:raise ReproductionError("CPU_ENGINE_TEST_SOURCE_MISSING")
            # Import through unittest rather than running the archived __main__:
            # that __main__ writes its report beside the input source files.
            environment=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
            process=subprocess.run([sys.executable,"-B","-m","unittest","-v",test.stem],
                                   cwd=test.parent,capture_output=True,text=True,timeout=120,env=environment)
            (out/"cpu_engine_tests.txt").write_text(process.stdout+process.stderr,encoding="utf-8")
            report["cpu_engineering_tests"]={"exit_code":process.returncode,"synthetic_only":True}
            if process.returncode:raise ReproductionError("CPU_ENGINE_SYNTHETIC_TEST_FAILURE")
        missing=[a for a in report["assets"] if a["status"]=="unavailable"]
        report["status"]="INCOMPLETE_DISPLAY_ASSETS" if missing else "BOUNDED_ARCHIVED_RESULT_REPRODUCTION_COMPLETE"
        report["full_raw_reproduction_status"]="NOT_ESTABLISHED_BY_THIS_RUN"
        report["missing_required_display_assets"]=len(missing)
        report["exit_code"]=3 if missing else 0
    except (ReproductionError,KeyError,TypeError,ValueError,OSError,subprocess.SubprocessError) as exc:
        report.update(status="REPRODUCTION_ERROR",error_type=type(exc).__name__,reason=str(exc),exit_code=2)
    write_json(out/"REPRODUCTION_REPORT.json",report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument("--out",type=Path,default=None)
    parser.add_argument("--tables-only",action="store_true",help="Regenerate tables/arithmetic without plotting imports")
    parser.add_argument("--cpu-tests",action="store_true",help="Also run the optional synthetic CPU engineering suite")
    args=parser.parse_args();out=args.out or args.root/"reproduced"
    report=run(args.root,out,args.tables_only,args.cpu_tests)
    print(json.dumps({k:report.get(k) for k in ("status","exit_code","missing_required_display_assets","reason")},ensure_ascii=False))
    print("REPRODUCTION_REPORT: "+str(Path(out).resolve()/"REPRODUCTION_REPORT.json"))
    return report["exit_code"]


if __name__=="__main__":
    raise SystemExit(main())
