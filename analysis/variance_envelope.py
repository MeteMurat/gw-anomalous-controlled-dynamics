#!/usr/bin/env python3
"""Read-only all4020 raw-variance envelope under a separately certified packet bound.

Python3.11+ standard library only. Does not access raw strain or change any old
campaign file. Formula constants are read from the earlier immutable protocol.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import math
from pathlib import Path
import time
import zipfile

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = '7DD8A9F34EC791C74482B6F33716CB47A569A47E2223F30B8C9530E99CBCAFF1'
RELEASE_SHA = '37FA0890E3A1966A2A2E034F0B3F3E4A548B54E0E3DA680F9014FF7429258ED1'
RESULTS_MEMBER = 'experiments/random4096_20261030/results/RESULTS.jsonl'
FRAME_MEMBER = 'experiments/random4096_20261030/package/data/FRAME.json'
MANIFEST_MEMBER = 'SHA256_MANIFEST.json'

def sha(data):
    return hashlib.sha256(data).hexdigest().upper()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def quantile(values, probability):
    """Linear interpolation at p*(n-1), equivalent to the usual type7 quantile."""
    v = sorted(values)
    require(bool(v), 'EMPTY_QUANTILE')
    position = probability * (len(v) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    return v[lower] + (position - lower) * (v[upper] - v[lower])

def describe(rows, column):
    values = [r[column] for r in rows]
    return {
        'records': len(rows), 'minimum': min(values), 'median': quantile(values, 0.5),
        'maximum': max(values), 'quantile_definition': 'Linear p*(n-1), type7',
        'quantiles': {str(p): quantile(values, p) for p in (0.05, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99)},
    }

def run(release, output):
    started = time.perf_counter()
    output.mkdir(parents=True, exist_ok=True)
    protocol_bytes = (HERE/'PROTOCOL_FROZEN.json').read_bytes()
    require(sha(protocol_bytes) == PROTOCOL_SHA, 'FROZEN_PROTOCOL_CHANGED')
    protocol = json.loads(protocol_bytes)
    require((protocol['Gdt_min_lower_bound'], protocol['full_h_gram_upper_bound'],
             protocol['kappa_lower_bound'], protocol['alpha_phase_fraction'])
            == (0.14, 0.142, 0.99, 0.1), 'FIXED_FORMULA_CONSTANTS')
    with release.open('rb') as stream:
        release_hash = hashlib.file_digest(stream, 'sha256').hexdigest().upper()
    require(release_hash == RELEASE_SHA, 'RELEASE_IDENTITY_MISMATCH')
    with zipfile.ZipFile(release) as archive:
        manifest_bytes = archive.read(MANIFEST_MEMBER)
        manifest = json.loads(manifest_bytes)
        input_bytes = {n: archive.read(n) for n in (RESULTS_MEMBER, FRAME_MEMBER)}
    input_proofs = {}
    for name, data in input_bytes.items():
        expected = manifest['members'][name]
        require(len(data) == expected['bytes'] and sha(data) == expected['sha256'], 'INPUT_MANIFEST_MISMATCH:'+name)
        input_proofs[name] = {'sha256': sha(data), 'bytes': len(data), 'manifest_matched': True}
    frame = json.loads(input_bytes[FRAME_MEMBER])
    frame_by_id = {r['record_id']: r for r in frame['records']}
    require(len(frame_by_id) == len(frame['records']) == 4096, 'FRAME_ALLOCATION')
    receipts = [json.loads(line) for line in input_bytes[RESULTS_MEMBER].splitlines() if line.strip()]
    require(len(receipts) == 4096, 'RECEIPT_COUNT')
    seen = set()
    status_counts = Counter()
    rows = []
    for receipt in receipts:
        rid = receipt['record_id']
        require(rid not in seen and rid in frame_by_id, 'DUPLICATE_OR_UNKNOWN_RECORD')
        seen.add(rid)
        pin = receipt['receipt_sha256']
        unsigned = {k: v for k, v in receipt.items() if k != 'receipt_sha256'}
        require(sha(canonical(unsigned).encode('utf-8')) == pin, 'RECEIPT_SELF_HASH:'+rid)
        selected = frame_by_id[rid]
        require(receipt['record'] == selected, 'FROZEN_RECORD_METADATA:'+rid)
        status_counts[receipt['status']] += 1
        if receipt['status'] != 'FEATURES_VALID':
            require(receipt['status'] == 'QUALITY_REJECTED', 'UNEXPECTED_TERMINAL_STATUS')
            continue
        require(receipt.get('synthetic_fixture_label') is None, 'SYNTHETIC_RECEIPT')
        require(receipt['source_evidence']['publisher_md5_verified'] is True, 'SOURCE_MD5_GATE')
        require(receipt['quality']['eligible'] is True, 'QUALITY_ELIGIBILITY')
        require(selected['detector'] == 'H1' and selected['role'] in ('TRAIN', 'CALIBRATION', 'TEST'), 'ROLE_OR_DETECTOR')
        require(selected['support_stop'] - selected['support_start'] == 68.0
                and selected['target_gps'] - selected['support_start'] == 64.0, 'SUPPORT_GEOMETRY')
        variance = receipt['diagnostics']['raw_target_power']
        reference_variance = receipt['diagnostics']['raw_reference_power']
        require(isinstance(variance, (int, float)) and math.isfinite(variance) and variance > 0, 'RAW_TARGET_VARIANCE')
        require(isinstance(reference_variance, (int, float)) and math.isfinite(reference_variance) and reference_variance > 0, 'RAW_REFERENCE_VARIANCE')
        m_ceiling = math.sqrt(4.0 * variance / protocol['Gdt_min_lower_bound'])
        h90_ceiling = m_ceiling * math.sqrt(protocol['full_h_gram_upper_bound']) / (
            protocol['kappa_lower_bound'] * math.sin(protocol['alpha_phase_fraction'] * math.pi))
        require(math.isfinite(m_ceiling) and math.isfinite(h90_ceiling), 'NONFINITE_ENVELOPE')
        rows.append({
            'record_id': rid, 'run': selected['run'], 'detector': selected['detector'],
            'target_gps': selected['target_gps'], 'support_start_gps': selected['support_start'],
            'support_stop_gps': selected['support_stop'], 'frozen_role': selected['role'],
            'source_time_group': selected['source_time_group'],
            'raw_target_demeaned_variance': variance,
            'raw_reference_demeaned_variance': reference_variance,
            'raw_target_demeaned_hrss_norm': math.sqrt(4.0 * variance),
            'M_coefficient_ceiling': m_ceiling,
            'h90_ceiling_if_template_proof_valid': h90_ceiling,
            'receipt_sha256': pin,
        })
    require(dict(status_counts) == {'FEATURES_VALID': 4020, 'QUALITY_REJECTED': 76}, 'TERMINAL_COUNTS')
    require(dict(Counter(r['frozen_role'] for r in rows)) == {'TRAIN': 2384, 'CALIBRATION': 786, 'TEST': 850}, 'ROLE_COUNTS')
    require(dict(Counter(r['run'] for r in rows)) == {'O4a': 2016, 'O4b': 2004}, 'RUN_COUNTS')
    rows.sort(key=lambda r: r['record_id'])
    csv_path = output/'ALL4020_VARIANCE_ENVELOPE.csv'
    with csv_path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format(v, '.17g') if isinstance(v, float) else v for k, v in row.items()})
    largest = sorted(rows, key=lambda r: (-r['raw_target_demeaned_variance'], r['record_id']))[:10]
    all_descriptions = {
        column: describe(rows, column)
        for column in ('raw_target_demeaned_variance', 'raw_target_demeaned_hrss_norm',
                       'M_coefficient_ceiling', 'h90_ceiling_if_template_proof_valid')
    }
    summary = {
        'schema': 'GW_PHASE_PACKET_ALL4020_VARIANCE_ENVELOPE_V1',
        'status': 'COMPUTED_PENDING_TEMPLATE_BOUND_CERTIFICATION',
        'template_bound_certification_status': 'PENDING_SEPARATE_PROOF_REVIEW',
        'protocol_sha256': PROTOCOL_SHA, 'protocol_frozen_utc': protocol['frozen_utc'],
        'computed_utc': datetime.now(timezone.utc).isoformat(),
        'release_sha256': release_hash, 'source_manifest_sha256': sha(manifest_bytes),
        'source_input_proofs': input_proofs,
        'input_receipts': len(receipts), 'audited_valid_supports': len(rows),
        'quality_rejected_supports_excluded': 76,
        'run_counts': dict(Counter(r['run'] for r in rows)),
        'frozen_role_counts': dict(Counter(r['frozen_role'] for r in rows)),
        'source_time_groups': len({r['source_time_group'] for r in rows}),
        'global_summary': all_descriptions,
        'by_run': {run: {'frozen_role_counts': dict(Counter(r['frozen_role'] for r in rows if r['run'] == run)),
                         'envelope': describe([r for r in rows if r['run'] == run], 'h90_ceiling_if_template_proof_valid'),
                         'raw_variance': describe([r for r in rows if r['run'] == run], 'raw_target_demeaned_variance')}
                   for run in ('O4a', 'O4b')},
        'global_maximum_record': largest[0], 'largest_raw_variance_records': largest,
        'all4020_csv_sha256': sha(csv_path.read_bytes()),
        'runtime_seconds': time.perf_counter() - started,
        'formula': {'M_ceiling': protocol['M_ceiling_formula'], 'h90_ceiling': protocol['h90_ceiling_formula'],
                    'Gdt_min_lower_bound': 0.14, 'full_h_gram_upper_bound': 0.142,
                    'kappa_lower_bound': 0.99, 'alpha_phase_fraction': 0.1},
        'interpretation': [
            'Formula evaluated under the separately checked fixed-template/phase-response assumptions; not certified by the variance summary alone.',
            'A conservative common upper envelope is the maximum across the4020validselected4ssupports, including all original TRAIN/CAL/TEST roles as annotations.',
            'The template is the declared256Hz four-Gaussian(+,-,-,+)packet, de-meaned quadratures, arrival offset restricted to±0.25s.',
            'All previously opened data are exploratory; this does not establish discovery significance or a global false-alarm probability.',
            'No independence claim, event-rate bound, physical-distance exclusion, transmitter proof or generic technosignature exclusion.',
            'The76quality-rejected supports and unobserved time are outside this envelope.',
        ],
        'raw_strain_arrays_accessed': 0, 'network_requests': 0, 'new_neural_inference_calls': 0,
        'original_release_modified': False, 'primary12experiment_modified': False,
    }
    (output/'SUMMARY_PENDING_PROOF.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-zip', type=Path, default=HERE.parent/'recovered_gw_20261101/techosignatures/GW_TUM_KOD_SEKIL_HESAP_20261030.zip')
    parser.add_argument('--out', type=Path, default=HERE/'results')
    args = parser.parse_args()
    result = run(args.release_zip.resolve(), args.out.resolve())
    print(json.dumps({k: result[k] for k in ('status', 'audited_valid_supports', 'run_counts', 'frozen_role_counts', 'global_maximum_record', 'runtime_seconds')}, ensure_ascii=False))

if __name__ == '__main__':
    main()
