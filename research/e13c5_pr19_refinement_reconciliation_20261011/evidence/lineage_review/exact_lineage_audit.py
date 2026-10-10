#!/usr/bin/env python3
"""Independent, bounded exact audit of saved lineage integration evidence.

No candidate, interval helper, reduction implementation, or physical solver is
imported. All interval endpoint arithmetic below uses stdlib Fraction.
"""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUTS = {
    'prior': 'inputs/pr19_lineage/first2/RESULTS.json',
    'pilot': 'inputs/pr19_lineage/pilot/RESULTS.json',
    'controls': 'inputs/PATH_CONTROLS.json',
    'current': 'evidence/N512_P60.json',
    'reduction': 'evidence/lineage_control/output_v2/RESULTS.json',
}
paths = {name: ROOT / path for name, path in INPUTS.items()}
data = {name: json.loads(path.read_text()) for name, path in paths.items()}
checks = []


def interval(value):
    if isinstance(value, dict):
        return Fraction(value['lo']), Fraction(value['hi'])
    return value


def contains(outer, inner):
    a, b = interval(outer)
    c, d = interval(inner)
    return a <= c <= d <= b


def plus(*values):
    return (sum((interval(v)[0] for v in values), Fraction(0)),
            sum((interval(v)[1] for v in values), Fraction(0)))


def times(value, positive):
    assert positive > 0
    a, b = interval(value)
    return a * positive, b * positive


def check(name, condition):
    checks.append({'check': name, 'pass': bool(condition)})


def encoded(value):
    return {'lo_exact': str(value[0]), 'hi_exact': str(value[1])}


prior = {(p['mode'], p['node']): p for p in data['prior']['paths']}
current = {(p['track']['mode'], p['track']['node']): p
           for p in data['current']['tracks']}
rows = {tuple(c['key']): c['row'] for c in data['controls']['controls']}
hybrid = data['reduction']['hybrid']
terms = {(p['mode'], p['node']): p for p in hybrid['path_terms']}
replacement_keys = {('OFF', 0), ('OFF', 700)}
check('keys/current_exactly_OFF0_OFF700', set(current) == replacement_keys)
check('keys/all_twelve_preserved', set(terms) == set(prior) and len(terms) == 12)
check('keys/exactly_two_replacement_tags',
      {k for k, v in terms.items() if v['provenance'] == 'CURRENT_N512_REPLACEMENT'}
      == replacement_keys)
check('modes/no_cross_mode_sum', hybrid['cross_mode_total'] is None
      and hybrid['mode_mixing'] is False)

carry_evidence = []
old700 = prior[('OFF', 700)]['segments']
pilot700 = data['pilot']['segments']
for i, (old, pilot) in enumerate(zip(old700, pilot700, strict=True)):
    check(f'reuse/{i}/same_key', old['key'] == pilot['key'])
    check(f'reuse/{i}/incoming_exact_equal', interval(old['Ia']) == interval(pilot['Ia']))
    f0 = Fraction.from_float(float(rows[tuple(old['key'])]['f0']))
    expected = ((Fraction(0), Fraction(0)) if i == 0 else
                tuple(v - f0 for v in interval(old700[i - 1]['Pend'])))
    check(f'reuse/{i}/original_incoming_contains_exact_carry', contains(pilot['Ia'], expected))
    check(f'reuse/{i}/absolute_endpoint_payload_identical', old['Pend'] == pilot['Pend'])
    carry_evidence.append({'key': old['key'], 'exact_carry': encoded(expected),
                           'saved_original_incoming': pilot['Ia'],
                           'endpoint_equal': interval(old['Ia']) == interval(pilot['Ia']),
                           'contains_exact_carry': contains(pilot['Ia'], expected)})

labels = tuple(data['prior']['selected_subset_weighted_reductions']['OFF'])
moment_labels = tuple(k for k in labels if k not in ('P_final', 'anchor'))
for key, term in terms.items():
    old = prior[key]
    weight = interval(old['weight'])
    check(f'weight/{key}/positive_exact_point', weight[0] == weight[1] and weight[0] > 0)
    check(f'weight/{key}/preserved', term['weight'] == old['weight'])
    check(f'capture/{key}/segments_preserved',
          term['preserved_captured_segments'] == [s['captured'] for s in old['segments']])
    check(f'capture/{key}/node_reductions_preserved',
          term['preserved_captured_segment_to_node_reductions'] ==
          [s['captured_segment_to_node_reduction'] for s in old['segments']])
    if key not in replacement_keys:
        check(f'unchanged/{key}/weighted_term_payload',
              term['weighted_reduction'] == old['weighted_reduction'])
        continue
    track = current[key]
    for s in track['segments']:
        captured_weight = Fraction.from_float(float(rows[tuple(s['key'])]['weight']))
        check(f'weight/{tuple(s["key"])}/same_captured_binary64', captured_weight == weight[0])
    absolute = {k: track['true_moment_enclosures'][k] for k in moment_labels}
    absolute['P_final'] = track['final_photon']['true_absolute_interval']
    absolute['anchor'] = track['summed_true_anchor_eV']
    for label in labels:
        check(f'replacement/{key}/{label}/exact_weighted_absolute',
              interval(term['weighted_reduction'][label]) == times(absolute[label], weight[0]))

off = hybrid['selected_subset_weighted_reductions']['OFF']
width_ratios = {}
for label in labels:
    expected = plus(*(terms[('OFF', node)]['weighted_reduction'][label]
                      for node in (0, 700, 1620, 2344)))
    check(f'OFF_sum/{label}/direct_exact_four_terms', interval(off[label]) == expected)
    old = interval(data['prior']['selected_subset_weighted_reductions']['OFF'][label])
    check(f'OFF_sum/{label}/nested_in_prior', contains(old, expected))
    if expected[1] != expected[0]:
        width_ratios[label] = str((old[1] - old[0]) / (expected[1] - expected[0]))
for mode in ('KF', 'GM'):
    check(f'{mode}/published_aggregate_payload_unchanged',
          hybrid['selected_subset_weighted_reductions'][mode] ==
          data['prior']['selected_subset_weighted_reductions'][mode])

epsilon = Fraction.from_float(1.602176634e-12)
bridges = hybrid['captured_node_bridges']
check('node_bridges/exact_four_keys',
      {(b['mode'], b['node'], b['step']) for b in bridges} ==
      {(mode, node, step) for mode, node in replacement_keys for step in (1, 2)})
for bridge in bridges:
    key = (bridge['mode'], bridge['node'])
    idx = (0,) if bridge['step'] == 1 else (1, 2)
    last = idx[-1]
    retained = prior[key]['segments'][last]['captured_segment_to_node_reduction']
    correction = bridge['correction_relative_to_captured_node']
    track = current[key]
    check(f'bridge/{key}/{bridge["step"]}/native_baseline_preserved',
          bridge['preserved_captured_segment_to_node_reduction'] == retained)
    for label in moment_labels:
        expected = plus(*(track['segments'][i]['outputs'][label]['true_minus_captured_interval']
                          for i in idx), retained[label])
        check(f'bridge/{key}/{bridge["step"]}/{label}/exact',
              interval(correction[label]) == expected)
    for output, native_key, label, conversion in (
            ('P1', 'P', 'P_endpoint', Fraction(1)),
            ('P1_energy_eV', 'U_erg', 'U_endpoint_eV', 1 / epsilon)):
        expected = plus(track['segments'][last]['outputs'][output]['true_minus_captured_interval'],
                        times(retained[native_key], conversion))
        check(f'bridge/{key}/{bridge["step"]}/{label}/exact_single_conversion',
              interval(correction[label]) == expected)

result = {
    'reviewer': '/root/e13c5_independent_review',
    'audit': 'independent saved-endpoint PR19 carry and direct positive-weight reduction audit',
    'finished_utc': datetime.now(timezone.utc).isoformat(),
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'inputs': {name: {'path': INPUTS[name], 'bytes': path.stat().st_size,
                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
               for name, path in paths.items()},
    'arithmetic': 'stdlib Fraction; captured constants lifted using Fraction.from_float(float(csv_string))',
    'candidate_imports': False, 'coefficient_or_exponential_evaluations': 0,
    'new_native_gas_or_continuous_solves': 0,
    'check_count': len(checks), 'failed_count': sum(not c['pass'] for c in checks),
    'status': 'PASS' if all(c['pass'] for c in checks) else 'FAIL',
    'checks': checks, 'reuse_exact_carry': carry_evidence,
    'OFF_prior_over_hybrid_width_exact': width_ratios,
    'exclusions': ['no fresh validity review of the other ten constituent physical paths',
                   'no full first2, missing-complement, global native-reduction, gas or production claim'],
}
target = HERE / 'EXACT_LINEAGE_RESULTS.json'
with target.open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({k: result[k] for k in ('status', 'check_count', 'failed_count', 'source_sha256')}))
sys.exit(0 if result['status'] == 'PASS' else 1)
