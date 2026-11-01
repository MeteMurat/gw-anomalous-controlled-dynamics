# Reproduction guide

Download and extract the complete versioned release asset. It contains three
immutable bundles and the current publication manuscript.

## 1. Original code, models and retained results

Extract `bundles/legacy_complete.zip` into a fresh directory. It includes all
three original neural checkpoints, original source modules, historical compact
evidence, source catalog and reproduction-level documentation. Consult its
README before running `reproduce.py`: saved-table reproduction is different
from a new raw-strain experiment, neural inference or complete training replay.

## 2. Fixed phase-coded packet, actual raw replay

Extract `bundles/fixed_packet_complete.zip`. The complete directory contains
twelve raw 68-second H1 inputs, frozen protocol, proofs and coefficients. Run
the supplied `REPRODUCE_PACKET.py` with its documented `--out` argument using
preinstalled Python 3.11+ and NumPy. This repeats the numerical packet experiment;
it performs no network transfer, installation or model training. Its Windows
wrapper uses the existing frozen runtime. Check the included README for the
full command and the distinction between opening saved results and running a
raw-input replay.

## 3. Three compact retained-evidence audits

Extract `bundles/comparison_and_phase_audits.zip`, then use its `BASLAT.cmd` or:

```bash
python RUN_ALL_AUDITS.py --out a_new_output_directory
```

The output directory must not already exist. This checks exact stored delay
curves, paired score comparisons, and the phase endpoint's assumption tradeoff.
No new strain or neural computation is performed. Necessary evidence is bundled
so the old 393-MB archive is not required for these three compact checks.

The selected-record survey, injection variants, conditional transformations and
independent full-search realizations have distinct denominators. Reproducing a
stored result never increases any observational completion count.

## Source review

`CODE_CATALOG.json` pins the visible source snapshots to their original bytes.
Their original relative layouts and input hashes remain inside the bundles.
`RELEASE_CONTENTS.json` pins each complete bundle. Do not edit hash-pinned
inputs merely to make a check pass. Dependencies are listed within each bundle;
no launcher in this repository installs packages automatically.
