# Structured transients in public gravitational-wave data

Reproducibility companion for the study of timing specificity and conditional
amplitude limits by Murat Metehan Türkoğlu.

## Scientific content

The study separates response to injected strain, transfer to held-out noise,
physical inter-detector timing, and conditional amplitude inference. A fixed
restricted-delay, maximum-pair correlation statistic can accept deliberately
over-delayed structured packets. A simple broad-peak timing veto also rejects
some physically projected controls. A separate linear calculation sets a
received-strain endpoint for one prescribed phase-coded transient under an
independent uniform source-phase model.

These results do not identify artificial origin, establish global discovery
significance, or demonstrate superiority at matched false-alarm rates.

## Code and complete inputs

Readable scientific source snapshots are in `analysis/`, `audits/`, and
`legacy_source/`. Complete executable layouts, retained inputs, neural model
weights and historical results are included in the versioned full release asset.
Download that asset from this repository's **Releases** page and extract it.
See `REPRODUCTION.md` before executing any historical launcher.

The visible snapshots are kept byte-exact for source review. Several scripts
expect the layout and hash-pinned inputs from their complete bundle; moving one
script alone does not make it an independent executable package.

## Different completion units

- Selected-record survey: 4096 audited H1 records, 4020 valid and 76 rejected by
  the specified quality rules. These are not claimed as 4096 independent network
  null trials.
- Historical independent full-search background: three completed realizations
  out of the original 4096 planned. The later cheap survey does not change this.
- Fixed-packet experiment: twelve retained raw H1 contexts and 109440 linear
  variant-equivalent evaluations on shared noise, not independent observations.
- Conditional received-H1-strain endpoint: approximately
  2.3393053703e-23 Hz^(-1/2), with at least 90% coverage over the specified
  independent uniform source phase. This is not a fixed-phase, source-rate,
  distance, or all-sky exclusion.

## Reproducibility scope

The fixed-packet calculation was repeated from the twelve raw inputs on native
Windows with all six checks passing. The 4020-row variance envelope is a
different, much weaker construction from retained variances, not another raw
matched-template scan of 4020 arrays.

Three original trained neural checkpoints are recovered and included. Their
architecture, preprocessing, training schedule and selection are documented.
Complete historical raw-input/training replay remains unperformed because some
original compact training inputs and production metadata were not recovered.
The new packet and retained-evidence audits do not use neural weights.

## Publication and provenance

Use the current manuscript supplied at the top level of the versioned release.
Manuscripts inside the immutable historical bundles are archived earlier
versions, not the current publication text. Hashes, original filenames and
operational ledgers belong to these reproducibility records, not the paper's
physics narrative. No new license grant is asserted; pre-existing third-party
notices and source identities are retained.

## Manuscript corrections

The complete code, original model weights and numerical inputs are retained in
release v1.0.0. The v1.0.1 manuscript-only patch repairs internal cross-references
without changing any numerical result, threshold, equation or figure. The latest
source is `manuscript/manuscript.md`. Later manuscript corrections reuse the
complete v1.0.0 archive rather than replacing it.
