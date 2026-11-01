#!/usr/bin/env python3
"""Reproduce the4020 variance envelopes from compact authenticated receipts.

Python3.11+ standard library only. The393MB historical ZIP is not needed.
This reads stored variances and source/frame identities, never raw strain.
The original BUILD_ENVELOPE.py and its pending output remain unchanged.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import time

import BUILD_ENVELOPE as frozen

HERE = Path(__file__).resolve().parent
CERTIFICATE_SHA = 'AE63236692CAC8B8D2A94B14D71D4CE76C48C869726D9D79749EAE917781E1FA'
FINAL_SUMMARY_SHA = '2981B703D7D1196703A0AC7919E3F97B20F6D9F9C50A825E8815882118628D9F'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def run(inputs, output):
    started = time.perf_counter()
    require(output.resolve() not in ((HERE/'results').resolve(), inputs.resolve(), HERE.resolve()), 'USE_SEPARATE_REPLAY_OUTPUT')
    protocol_bytes = (HERE/'PROTOCOL_FROZEN.json').read_bytes()
    require(frozen.sha(protocol_bytes) == frozen.PROTOCOL_SHA, 'FROZEN_PROTOCOL_HASH')
    protocol = json.loads(protocol_bytes)
    cert_bytes = (HERE/'proof/RAW_VARIANCE_CERTIFICATION.json').read_bytes()
    require(frozen.sha(cert_bytes) == CERTIFICATE_SHA, 'CERTIFICATE_HASH')
    cert = json.loads(cert_bytes)
    require(cert['status'] == 'PASS_SEPARATE_DEMEANED_TARGET_TEMPLATE_BOUND', 'CERTIFICATE_STATUS')
    require(cert['code_sha256'] == frozen.sha((HERE/'BUILD_ENVELOPE.py').read_bytes()), 'FROZEN_IMPLEMENTATION_HASH')
    pending_bytes = (HERE/'results/SUMMARY_PENDING_PROOF.json').read_bytes()
    require(frozen.sha(pending_bytes) == cert['summary_input_sha256'], 'PENDING_SUMMARY_HASH')
    pending = json.loads(pending_bytes)
    final_bytes = (HERE/'results/SUMMARY.json').read_bytes()
    require(frozen.sha(final_bytes) == FINAL_SUMMARY_SHA, 'FINAL_SUMMARY_HASH')
    final = json.loads(final_bytes)
    require(final['status'] == 'COMPLETE_CONSERVATIVE_VARIANCE_ENVELOPE', 'FINAL_STATUS')
    require(pending['protocol_sha256'] == cert['protocol_sha256'] == frozen.PROTOCOL_SHA, 'PROTOCOL_BINDING')
    expected_csv = (HERE/'results/ALL4020_VARIANCE_ENVELOPE.csv').read_bytes()
    require(frozen.sha(expected_csv) == cert['all4020_csv_sha256'] == pending['all4020_csv_sha256'], 'FROZEN_CSV_HASH')
    source_bytes = {}
    for member in (frozen.RESULTS_MEMBER, frozen.FRAME_MEMBER):
        local_name = member.rsplit('/', 1)[-1]
        data = (inputs/local_name).read_bytes()
        pin = pending['source_input_proofs'][member]
        require(len(data) == pin['bytes'] and frozen.sha(data) == pin['sha256'], 'COMPACT_INPUT_HASH:'+local_name)
        source_bytes[member] = data
    frame = json.loads(source_bytes[frozen.FRAME_MEMBER])
    frame_by_id = {r['record_id']: r for r in frame['records']}
    require(len(frame_by_id) == len(frame['records']) == 4096, 'FRAME_ALLOCATION')
    receipts = [json.loads(line) for line in source_bytes[frozen.RESULTS_MEMBER].splitlines() if line.strip()]
    require(len(receipts) == 4096, 'RECEIPT_COUNT')
    rows, seen = [], set()
    status_counts = Counter()
    for receipt in receipts:
        rid = receipt['record_id']
        require(rid not in seen and rid in frame_by_id, 'DUPLICATE_OR_UNKNOWN_RECORD')
        seen.add(rid)
        pin = receipt['receipt_sha256']
        unsigned = {k: v for k, v in receipt.items() if k != 'receipt_sha256'}
        require(frozen.sha(frozen.canonical(unsigned).encode('utf-8')) == pin, 'RECEIPT_SELF_HASH:'+rid)
        selected = frame_by_id[rid]
        require(receipt['record'] == selected, 'FROZEN_RECORD_METADATA:'+rid)
        status_counts[receipt['status']] += 1
        if receipt['status'] != 'FEATURES_VALID':
            require(receipt['status'] == 'QUALITY_REJECTED', 'TERMINAL_STATUS')
            continue
        require(receipt['source_evidence']['publisher_md5_verified'] is True, 'PUBLISHER_SOURCE_GATE')
        require(receipt['quality']['eligible'] is True, 'QUALITY_GATE')
        require(receipt.get('synthetic_fixture_label') is None, 'SYNTHETIC_RECORD')
        variance = receipt['diagnostics']['raw_target_power']
        ref_variance = receipt['diagnostics']['raw_reference_power']
        require(math.isfinite(variance) and variance > 0 and math.isfinite(ref_variance) and ref_variance > 0, 'RAW_VARIANCE')
        m = math.sqrt(4.0 * variance / protocol['Gdt_min_lower_bound'])
        h90 = m * math.sqrt(protocol['full_h_gram_upper_bound']) / (
            protocol['kappa_lower_bound'] * math.sin(protocol['alpha_phase_fraction'] * math.pi))
        rows.append({
            'record_id': rid, 'run': selected['run'], 'detector': selected['detector'],
            'target_gps': selected['target_gps'], 'support_start_gps': selected['support_start'],
            'support_stop_gps': selected['support_stop'], 'frozen_role': selected['role'],
            'source_time_group': selected['source_time_group'],
            'raw_target_demeaned_variance': variance,
            'raw_reference_demeaned_variance': ref_variance,
            'raw_target_demeaned_hrss_norm': math.sqrt(4.0 * variance),
            'M_coefficient_ceiling': m, 'h90_ceiling_if_template_proof_valid': h90,
            'receipt_sha256': pin,
        })
    require(dict(status_counts) == {'FEATURES_VALID': 4020, 'QUALITY_REJECTED': 76}, 'TERMINAL_COUNTS')
    require(dict(Counter(r['run'] for r in rows)) == {'O4a': 2016, 'O4b': 2004}, 'RUN_COUNTS')
    require(dict(Counter(r['frozen_role'] for r in rows)) == {'TRAIN': 2384, 'CALIBRATION': 786, 'TEST': 850}, 'FROZEN_ROLE_COUNTS')
    rows.sort(key=lambda r: r['record_id'])
    output.mkdir(parents=True, exist_ok=True)
    path = output/'ALL4020_VARIANCE_ENVELOPE.csv'
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader()
        for row in rows:
            writer.writerow({k: format(v, '.17g') if isinstance(v, float) else v for k, v in row.items()})
    require(path.read_bytes() == expected_csv, 'RECOMPUTED_CSV_NOT_BYTE_IDENTICAL')
    descriptions = {column: frozen.describe(rows, column) for column in final['global_summary']}
    require(descriptions == final['global_summary'], 'GLOBAL_SUMMARY_MISMATCH')
    report = {
        'schema': 'GW_PACKET_VARIANCE_COMPACT_REPLAY_V1', 'status': 'PASS_COMPACT_REPLAY',
        'valid_records_recomputed': len(rows), 'input_receipts_checked': len(receipts),
        'all_receipt_self_hashes_and_frame_bindings_checked': True,
        'all4020_csv_byte_identical': True, 'all4020_csv_sha256': frozen.sha(expected_csv),
        'global_summary_exact': True, 'global_summary': descriptions,
        'original_release_sha256_recorded': final['release_sha256'],
        'original393MB_release_reverified_by_this_compact_run': False,
        'compact_inputs_match_certificate_pinned_release_members': True,
        'certificate_sha256': CERTIFICATE_SHA, 'protocol_sha256': frozen.PROTOCOL_SHA,
        'runtime_seconds': time.perf_counter() - started,
        'raw_strain_arrays_accessed': 0, 'network_requests': 0, 'new_neural_inference_calls': 0,
        'scope': final['interpretation'],
    }
    (output/'COMPACT_REPLAY_REPORT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=HERE/'inputs')
    parser.add_argument('--out', type=Path, default=HERE/'reproduced_compact')
    args = parser.parse_args()
    report = run(args.inputs.resolve(), args.out.resolve())
    print(json.dumps({k: report[k] for k in ('status', 'valid_records_recomputed', 'all4020_csv_byte_identical', 'global_summary_exact', 'runtime_seconds')}))

if __name__ == '__main__':
    main()
