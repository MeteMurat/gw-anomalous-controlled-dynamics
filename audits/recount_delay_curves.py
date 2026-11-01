"""Recount saved delay curves, without strain access or another signal analysis.

Python 3.11+, standard library only. Read either the original parent source
bundle or the compact ZIP of exact saved curve bytes. No cut is fitted.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, statistics, zipfile
from collections import defaultdict
from pathlib import Path

CONTAINER = 'ZIP_86DE2654513F10A37E470188'
ARCHIVE_SHA256 = '37FA0890E3A1966A2A2E034F0B3F3E4A548B54E0E3DA680F9014FF7429258ED1'
CUTS = {'O4a': 1.2127042400481731, 'O4b': 1.2033275141068391}
COMPACT_INDEX_SHA256 = '399C8F89BD18BDD3B4909F42D8FC1919A56F6C3EE97571286CE8D85EF7E262C3'

def source_records(args):
    """Yield exactly identified original member bytes from either container."""
    if args.evidence_zip:
        with zipfile.ZipFile(args.evidence_zip) as archive:
            index_bytes = archive.read('EVIDENCE_INDEX.json')
            assert hashlib.sha256(index_bytes).hexdigest().upper() == COMPACT_INDEX_SHA256
            index = json.loads(index_bytes)
            assert index['parent_archive_sha256'] == ARCHIVE_SHA256
            assert index['original_container_key'] == CONTAINER
            assert len(index['records']) == 216
            expected = {'EVIDENCE_INDEX.json'} | {m['member'] for m in index['records']} | {
                m['member'] for m in index['supporting_original_members']}
            assert set(archive.namelist()) == expected
            for member in index['supporting_original_members']:
                body = archive.read(member['member'])
                assert len(body) == member['bytes']
                assert hashlib.sha256(body).hexdigest().upper() == member['sha256']
            for member in index['records']:
                body = archive.read(member['member'])
                assert len(body) == member['bytes']
                assert hashlib.sha256(body).hexdigest().upper() == member['sha256']
                yield member, body
        return
    digest = hashlib.sha256()
    with args.archive.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    assert digest.hexdigest().upper() == ARCHIVE_SHA256
    with zipfile.ZipFile(args.archive) as archive:
        catalog = json.loads(archive.read('archive/ARCHIVE_CATALOG.json'))
        packs = {}
        members = [m for m in catalog['members'] if m['container_key'] == CONTAINER
                   and m['member'].count('/') == 1
                   and m['member'].split('/')[0] in ('BASELINES', 'P2', 'P3')
                   and m['member'].endswith('.json')
                   and not m['member'].endswith('.receipt.json')]
        assert len(members) == 216
        for member in sorted(members, key=lambda m: m['member']):
            obj = catalog['objects'][member['sha256']]
            if member['object'] in archive.namelist():
                body = archive.read(member['object'])
            else:
                pack_path = obj['storage_pack']
                if pack_path not in packs:
                    packs[pack_path] = zipfile.ZipFile(io.BytesIO(archive.read(pack_path)))
                body = packs[pack_path].read(obj['storage_entry'])
            assert hashlib.sha256(body).hexdigest().upper() == member['sha256']
            yield member, body

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive', type=Path, nargs='?')
    ap.add_argument('--evidence-zip', type=Path,
                    help='Compact ZIP of exact original saved curve bytes, no parent ZIP needed')
    ap.add_argument('--out', type=Path, default=Path('delay_failure_recount'))
    args = ap.parse_args()
    if (args.archive is None) == (args.evidence_zip is None):
        ap.error('Specify exactly one of archive or --evidence-zip')
    rows, identities, groups = [], [], defaultdict(list)
    for member, body in source_records(args):
        value = json.loads(body)
        assert value['exact_old_receipts_replayed'] is True
        assert value['thresholds_refit'] is False
        pair_scores = {k: v['segment_max_abs_rho'][-1]
                       for k, v in value['coherence']['per_pair'].items()}
        maximum = max(pair_scores.values())
        winners = [k for k, v in pair_scores.items() if v == maximum]
        assert len(winners) == 1
        winner = winners[0]
        pairs = value['diagnostic']['per_pair']
        for pair_name, pair in pairs.items():
            cap = value['coherence']['per_pair'][pair_name]['max_integer_lag_samples']
            for method in ('raw_correlation', 'envelope_power_correlation'):
                curve = pair[method]
                assert curve['status'] == 'DEFINED'
                lags, coefficients = curve['lag_samples'], curve['signed_normalized_correlation']
                assert len(lags) == len(coefficients) == 2867
                peak = max(abs(x) for x in coefficients)
                maximizers = [lag for lag, coefficient in zip(lags, coefficients)
                              if abs(coefficient) == peak]
                assert peak == curve['broad_abs_max']
                assert maximizers == curve['exact_broad_maximizer_lag_samples']
                intersects = any(abs(lag) <= cap for lag in maximizers)
                assert intersects == curve['exact_broad_peak_set_intersects_physical_cap']
        kind = value['header']['kind']
        variant = value.get('variant') or {}
        control = variant.get('control', 'unmodified')
        if kind == 'BASELINES':
            group = 'Unmodified noise'
        elif kind == 'P2':
            group = 'Packets, ' + {'original': 'original', 'time_reversed': 'reversed',
                                  'incoherent': 'extra delay'}[control]
        else:
            short = variant.get('source_id') == 'ROCKET_T1'
            group = ('10-ms rocket, ' if short else 'Other sources, ') + (
                'original' if control == 'original' else 'extra delay')
        winning = pairs[winner]
        raw = winning['raw_correlation']
        envelope = winning['envelope_power_correlation']
        row = dict(member=member['member'], group=group,
                   topology=value['header']['topology'], noise_id=value['header']['noise_id'],
                   winning_pair=winner, source_id=variant.get('source_id'),
                   family=variant.get('family'),
                   above_cut=value['scores']['COHERENCE'] > CUTS[value['header']['topology']],
                   raw_outside=not raw['exact_broad_peak_set_intersects_physical_cap'],
                   envelope_outside=not envelope['exact_broad_peak_set_intersects_physical_cap'],
                   raw_cap_to_broad_ratio=raw['max_physical_to_broad_abs_ratio'],
                   all_raw_pairs_outside=all(not p['raw_correlation']['exact_broad_peak_set_intersects_physical_cap'] for p in pairs.values()),
                   all_envelope_pairs_outside=all(not p['envelope_power_correlation']['exact_broad_peak_set_intersects_physical_cap'] for p in pairs.values()))
        rows.append(row)
        groups[group].append(row)
        identities.append({'member': member['member'], 'sha256': member['sha256']})
    table = {group: dict(n=len(items), above_cut=sum(r['above_cut'] for r in items),
                        raw_outside=sum(r['raw_outside'] for r in items),
                        envelope_outside=sum(r['envelope_outside'] for r in items),
                        ratio_min=min(r['raw_cap_to_broad_ratio'] for r in items),
                        ratio_max=max(r['raw_cap_to_broad_ratio'] for r in items),
                        ratio_median=statistics.median(r['raw_cap_to_broad_ratio'] for r in items))
             for group, items in groups.items()}
    assert {g: (v['n'],v['above_cut'],v['raw_outside'],v['envelope_outside']) for g,v in table.items()} == {
        'Unmodified noise': (24,4,21,17), 'Packets, original': (48,48,4,9),
        'Packets, reversed': (48,48,3,10), 'Packets, extra delay': (48,38,48,48),
        '10-ms rocket, original': (4,4,0,0), '10-ms rocket, extra delay': (4,1,4,4),
        'Other sources, original': (20,5,15,15), 'Other sources, extra delay': (20,5,15,15)}
    delayed = groups['Packets, extra delay']
    assert sum(r['all_raw_pairs_outside'] for r in delayed) == 48
    assert sum(r['all_envelope_pairs_outside'] for r in delayed) == 47
    args.out.mkdir(parents=True, exist_ok=True)
    report = dict(schema='GW_DELAY_FAILURE_SAVED_CURVE_RECOUNT_V1', status='PASS',
                  scope='Saved-curve recount, not new strain or inference', archive_sha256=ARCHIVE_SHA256,
                  records=216, pairs=432, curves=864, thresholds_changed=False,
                  global_false_alarm_probability=False, table=table,
                  all_delayed_raw_pairs_outside=48, all_delayed_envelope_pairs_outside=47,
                  input_identities=identities)
    (args.out/'DELAY_FAILURE_RECOUNT.json').write_text(json.dumps(report, indent=2)+'\n')
    with (args.out/'DELAY_FAILURE_RECORDS.csv').open('w', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({k:v for k,v in report.items() if k!='input_identities'}, indent=2))

if __name__ == '__main__':
    main()
