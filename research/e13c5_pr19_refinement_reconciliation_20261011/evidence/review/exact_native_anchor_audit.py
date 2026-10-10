#!/usr/bin/env python3
"""Independent reviewer: exact rational audit of SAVED N512 native/anchor data.

No candidate modules, Decimal arithmetic, coefficients, or ODE solves are used.
The residual risk is bookkeeping: tiny anchor terms are far below broad global
ledger widths, so a zero-containing ledger alone cannot detect their omission.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
checks = []


def point(x):
    return (F(x), F(x))


def box(x):
    return (F(x['lo']), F(x['hi']))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[1], -x[0])


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    corners = [a * b for a in x for b in y]
    return (min(corners), max(corners))


def enclosed(saved, expr):
    s = box(saved)
    return s[0] <= expr[0] and expr[1] <= s[1]


def check(name, condition):
    checks.append({'id': name, 'pass': bool(condition)})


def lift(x):
    return F.from_float(float(x))


inputs = json.loads((ROOT / 'inputs/PATH_CONTROLS.json').read_text())
raw = json.loads((ROOT / 'evidence/N512_P60.json').read_text())
by_key = {tuple(x['key']): x for x in inputs['controls']}
eps = F.from_float(1.602176634e-12)

for track in raw['tracks']:
    tag = 'node_' + str(track['track']['node'])
    for row in track['segments']:
        key = tuple(row['key'])
        prefix = '/'.join(map(str, key))
        cap = by_key[key]['row']
        n = point(lift(cap['n']))
        true_capture_u = point(lift(cap['u']) / eps)
        ec = box(row['endpoint_energy_eV'])
        saved_cap = row['captured']
        check(prefix + '/exact_native_photon', enclosed(saved_cap['P1'], n))
        check(prefix + '/exact_native_energy_erg_to_eV', enclosed(saved_cap['P1_energy_eV'], true_capture_u))
        check(prefix + '/native_energy_stock_gap_nonzero',
              not (box(row['native_energy_stock_minus_Eh_n_eV'])[0] <= 0 <= box(row['native_energy_stock_minus_Eh_n_eV'])[1]))
        check(prefix + '/native_stock_gap_included', enclosed(row['native_energy_stock_minus_Eh_n_eV'], sub(box(saved_cap['P1_energy_eV']), mul(ec, n))))
        repr_u = row['representation_exactfrozen_minus_captured']['P1_energy_eV']
        check(prefix + '/full_native_energy_representation', enclosed(repr_u, sub(box(row['frozen']['P1_energy_eV']), box(saved_cap['P1_energy_eV']))))
        out = row['outputs']['P1_energy_eV']
        combined = add(box(row['firstvariation_with_candidate_incoming']['P1_energy_eV']), box(repr_u))
        check(prefix + '/represented_firstvariation_inclusion', enclosed(out['centered_firstvariation_plus_representation_interval'], combined))
        center, rad = F(out['candidate']), F(out['radius'])
        numerical = max(abs(combined[0] - center), abs(combined[1] - center))
        analytic = F(row['remainder']['total_before_numerical_upper']['P1_energy_eV'])
        check(prefix + '/full_radius_includes_representation_rounding', rad >= numerical + analytic)
        check(prefix + '/true_correction_interval', enclosed(out['true_minus_captured_interval'], (center - rad, center + rad)))
        check(prefix + '/true_absolute_energy_interval', enclosed(out['true_absolute_interval'], add(box(saved_cap['P1_energy_eV']), box(out['true_minus_captured_interval']))))
        incoming = row['incoming']
        S_min = abs(F(incoming['center'])) + F(incoming['radius']) + box(row['local']['bounds']['B_r'])[1]
        check(prefix + '/S_bound_includes_incoming', F(row['remainder']['S_upper']) >= S_min)
        for name in ('P1', 'A_total', 'B_total_eV', 'P1_energy_eV'):
            g = box(row['gains'][name])
            minimum = max(abs(g[0]), abs(g[1])) * F(incoming['radius'])
            check(prefix + '/incoming_gain/' + name, F(row['remainder']['incoming_upper'][name]) >= minimum)
    for j, seam in enumerate(track['seams']):
        prefix = tag + '/seam_' + str(j)
        left, right = track['segments'][j:j+2]
        next_cap = by_key[tuple(right['key'])]['row']
        check(prefix + '/signed_deltaE', enclosed(seam['DeltaE_eV'], sub(point(lift(next_cap['e0'])), box(left['endpoint_energy_eV']))))
        delta = box(seam['DeltaE_eV'])
        corr = box(left['outputs']['P1']['true_minus_captured_interval'])
        n = box(left['captured']['P1'])
        check(prefix + '/full_signed_correction_product', enclosed(seam['correction_anchor_relative_to_captured_photon_eV'], mul(delta, corr)))
        check(prefix + '/native_anchor_product', enclosed(seam['native_photon_anchor_eV'], mul(delta, n)))
        check(prefix + '/true_anchor_product', enclosed(seam['true_anchor_eV'], mul(delta, add(n, corr))))
        check(prefix + '/incoming_carry_not_reset', right['incoming'] == seam['next_incoming'])
        check(prefix + '/outgoing_radius_carried', F(right['incoming']['radius']) >= F(left['outputs']['P1']['radius']))
    for j, row in enumerate(track['segments']):
        prior = track['segments'][j-1]['cumulative_moment_corrections'] if j else None
        for name in ('B_total_eV', 'H_total_eV', 'Z_eV', 'QE_eV'):
            prev = F(prior[name]['radius']) if prior else F(0)
            now = F(row['cumulative_moment_corrections'][name]['radius'])
            local = F(row['outputs'][name]['radius'])
            check(tag + '/cumulative_' + str(j) + '/' + name, now >= prev + local)
    anchors = point(0)
    for seam in track['seams']:
        anchors = add(anchors, box(seam['true_anchor_eV']))
    check(tag + '/anchor_sum', enclosed(track['summed_true_anchor_eV'], anchors))
    terms = track['true_moment_enclosures']
    final = track['final_energy_stock_eV']['true_absolute_interval']
    energy = box(final)
    first_cap = by_key[tuple(track['segments'][0]['key'])]['row']
    energy = sub(energy, point(lift(first_cap['e0']) * lift(first_cap['f0'])))
    for name, sign in [('B_total_eV', 1), ('Z_eV', 1), ('QE_eV', -1)]:
        energy = add(energy, box(terms[name]) if sign == 1 else neg(box(terms[name])))
    energy = sub(energy, box(track['summed_true_anchor_eV']))
    saved_ledger = track['global_ledger_enclosures']['energy_eV_with_anchor_subtracted']
    check(tag + '/global_anchor_subtracted_ledger_formula', enclosed(saved_ledger, energy))
    check(tag + '/global_energy_contains_zero', box(saved_ledger)[0] <= 0 <= box(saved_ledger)[1])

result = {'schema': 'e13c5-independent-exact-native-anchor-audit-v1',
          'role': 'INDEPENDENT_DECISION_REVIEWER',
          'arithmetic': 'fractions.Fraction; exact stored decimal rationals and exact binary64 input lift',
          'scope': 'saved N512/P60 only: native energy stock, incoming radii, anchor products and cumulative/global energy bookkeeping',
          'candidate_imports': 0, 'coefficient_evaluations': 0, 'continuous_solves': 0, 'native_runs': 0,
          'checks': checks, 'passed': sum(x['pass'] for x in checks), 'failed': sum(not x['pass'] for x in checks),
          'input_sha256': {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in
                           ['inputs/PATH_CONTROLS.json', 'evidence/N512_P60.json']}}
out = Path(sys.argv[1])
with out.open('x') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps({k: result[k] for k in ['passed', 'failed', 'candidate_imports', 'coefficient_evaluations']}))
raise SystemExit(0 if result['failed'] == 0 else 1)
