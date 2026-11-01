# Reproduction scope

The release distinguishes four operations. They are not interchangeable.

| Level | What is available | What a successful replay establishes |
| --- | --- | --- |
| Archive integrity | SHA-256 and byte counts for released members | The archived inputs match the declared release. |
| Retained-result reproduction | Experiment ledger, source result summaries and declared arithmetic | Tables, finite counts and conditional-rank arithmetic reproduce the retained evidence. Historical summary-only measurements retain that evidence tier. |
| Figure redraw | A declared numeric input and an explicit narrow plot adapter | The numerical display is regenerated from those inputs. Rendering differences across library/font versions are possible; pixel equality is not claimed. |
| Raw/model replay | Original strain, quality selections, all frozen model weights and the relevant original executable environment | Only an actually executed replay with these inputs can establish numerical pipeline equivalence or a new search result. The default runner does not establish this level. |

## One command

Use an existing Python environment with the packages in
`requirements-reproduction.txt`, then run:

```text
python reproduce.py
```

On Windows, double-click `BASLAT.cmd`, or use:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\REPRODUCE.ps1 -PythonExe 'E:\GW_TECHNOSIGNATURE\_runtime\T0_F2_R2_CPU_TORCH_2_6_0_PY311\Scripts\python.exe'
```

The PowerShell wrapper writes results and a return ZIP to the Desktop. It
does not change power settings, install packages, download strain, train a
model, or alter any historical scientific state. `GW_PYTHON` can select an
existing interpreter. A Python executable alone does not guarantee that its
environment includes the optional plotting packages.

For arithmetic and tables without plotting imports:

```text
python reproduce.py --tables-only
```

The optional `--cpu-tests` flag runs the separate synthetic engineering
suite if it is included at one of the declared source paths. It does not
create real observations or constitute a laptop throughput benchmark.

## Inputs and outputs

The supervisor verifies `SHA256_MANIFEST.json` before opening science data.
Its `members` mapping uses repository-relative paths with SHA-256 and byte
counts. Inputs that escape the repository or use symlinks are rejected.

`evidence/GW_PROJECT_EVIDENCE_LEDGER.json` supplies every retained result
metric. `scientific_results.csv` and `.json` include experiment IDs,
denominators, source descriptions, evidence levels and interpretation
limits. `conditional_rank_arithmetic.json` checks the originally declared
`(1+exceedances)/(1+transformations)` calculations; it creates no new null
data. The newly generated response/control summary figures explicitly keep
the cohorts separate and display their original denominators.

`evidence/FIGURE_AND_RESULT_INDEX.json` enumerates manuscript display
assets. Each entry should supply `repository_path`, the retained asset
`sha256`, and source provenance. It may additionally declare a supported
`portable_recipe`. The runner does not execute arbitrary commands or
archived builders from this index. The currently supported recipe is
`p2_archived_counts_v1`, with `counts_path` and optional `counts_sha256`.
The additional narrow recipes are `p4_saved_lag_curves_v1` (three matching
noise/original/delayed JSON records, a detector pair, and output stem),
`timeline_saved_score_matrix_v1` (the original score matrix and result JSON),
and `physical_source_series_v1` (the frozen-equation source series plus its
parameters and model-source digest). Saved lag maxima and saved-matrix
endpoint counts are recomputed and checked against their archived values.
The physical-source plot describes an equation-level series, rather than a
new detector-noise response. Other original figures remain verified,
retained products until a vetted adapter and the exact required numeric
inputs are present.

`REPRODUCTION_REPORT.json` records a status for each table and figure:
reproduced arithmetic/count display, retained only, or unavailable.
Retained-only assets are not mislabeled as recomputed. A required display
asset that is missing returns exit code 3. Corrupt/missing manifest inputs,
invalid counts or calculation mismatches return exit code 2. Exit code 0
means the declared bounded archived-result operation completed; it does
not certify full raw/model reproducibility, an anomaly detection, a global
false-alarm probability, or completion of a new 4096-record survey.

The default output directory is `reproduced/`; exclude it from the release
manifest and version control. Raw strain acquisition, model retraining and
archived repair launchers require their own explicit procedure and input
availability. Never execute every archived PowerShell script as a batch.

## Received original neural artifacts

The original three fitted checkpoints and exact bounded-training item schedule
are now included and SHA256-verified. This closes their file-availability gap.
The schedule identifies 640 training and 320 internal-development branch items
and includes expected preprocessing-array digests. The arrays themselves and
production ledger are not supplied. No model or training execution is implied
by a successful archive-integrity check. Static tensor/metadata checks and any
optional native strict-load/synthetic smoke results are reported separately;
original real-input embedding parity remains an additional replay requirement.

The four scientific completion units remain separate: legacy full searches
3/4096, H1 conditional units 10/4096, the previously completed foreground
conditional transformations 4096/4096, and the newly executed CPU record survey4096/4096audited supports (4020valid feature records;76quality rejections;0input rejections). This new survey is an actual separate experiment; recovery of old files itself does not change any historical counter.


## Actual random-record survey replay

`experiments/random4096_20261030/REPLAY_SAVED_RESULTS.py` reads the unchanged frozen FRAME roles and the4096SHA-bound receipts, then recomputes their TRAIN-only scoring and descriptive TEST ranking. It verifies the declared numerical profile and never repartitions only the quality-passing subset. It performs no raw access or neural inference. The old `ANALYZE_TABLE.py` generic role allocator remains archived source; it is not the final frozen-frame replay entry point.

Raw-source replay uses the separate package worker and requires existing NumPy/SciPy/h5py plus publisher-verified HDF5 acquisition. The host run used CPython3.12, NumPy2.3.5, SciPy1.17.0 and h5py3.16.0 with single-thread numerical controls; this is distinct from the historical Windows neural runtime. Published record timing separates locally ready input computation from source acquisition and does not promise a Windows wall-time benchmark.

The144planned secondary variants and eight planned candidate reviews are separately accounted, including ineligible or unavailable inputs. No hardware-injection-free, technological-origin, population-rate or calibrated global-significance claim follows from completion.


### Redraw the four new survey figures

```bash
python experiments/random4096_20261030/evidence/paper/EXPORT_SURVEY_FIGURES.py --campaign experiments/random4096_20261030/results --out reproduced/random4096_figures
```

This uses released measured tables and secondary-response counts with an already available Matplotlib environment. It performs no strain acquisition, neural inference or threshold selection.
