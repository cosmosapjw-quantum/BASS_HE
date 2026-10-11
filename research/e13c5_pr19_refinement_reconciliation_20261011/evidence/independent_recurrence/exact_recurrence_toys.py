#!/usr/bin/env python3
"""Exact Fraction controls for incoming, representation, and signed anchors.

No production modules, floating-point evaluation, numerical ODE solver, or
Decimal arithmetic is used.  exp(-k log 2) is represented algebraically as 2^-k.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys


def point(x):
    x = F(x)
    return (x, x)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[1], -a[0])


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    products = [x * y for x in a for y in b]
    return (min(products), max(products))


def centered(c, r):
    assert r >= 0
    return (c - r, c + r)


def contains(a, b):
    return a[0] <= b[0] and b[1] <= a[1]


def pack(x):
    if isinstance(x, F):
        return f'{x.numerator}/{x.denominator}'
    if isinstance(x, (list, tuple)):
        return [pack(v) for v in x]
    if isinstance(x, dict):
        return {k: pack(v) for k, v in x.items()}
    return x


class Checks:
    def __init__(self):
        self.rows = []

    def check(self, test_id, condition, **evidence):
        self.rows.append({'TestID': test_id,
                          'status': 'PASS' if bool(condition) else 'FAIL',
                          'evidence': pack(evidence)})


def homogeneous_gains(E0, k, species, chi):
    """h=ln2, total opacity k>0, species rates sum to k, source=0."""
    assert sum(species) == k and k > 0
    damp = F(1, 2**k)
    Eh = E0 / 2
    j0 = (1 - damp) / k
    je = E0 * (1 - F(1, 2**(k+1))) / (k+1)
    A = [l * j0 for l in species]
    B = [l * je for l in species]
    H = [b - x * a for b, x, a in zip(B, chi, A)]
    return {'P1': damp, 'A_total': sum(A), 'B_total': sum(B),
            'H_total': sum(H), 'Z': je,
            **{f'A{i}': a for i, a in enumerate(A)},
            **{f'B{i}': b for i, b in enumerate(B)},
            **{f'H{i}': h for i, h in enumerate(H)}}, Eh


def run():
    checks = Checks()
    E0 = F(12)
    k = 2
    chi = [F(2), F(4)]
    gain, Eh = homogeneous_gains(E0, k, [F(1, 2), F(3, 2)], chi)
    checks.check('GAIN-NUMBER-IDENTITY', gain['P1'] + gain['A_total'] == 1,
                 gains=gain)
    checks.check('GAIN-ENERGY-IDENTITY',
                 Eh * gain['P1'] + gain['B_total'] + gain['Z'] == E0)
    checks.check('GAIN-HEAT-IDENTITY',
                 gain['H_total'] == gain['B_total'] -
                 sum(chi[i] * gain[f'A{i}'] for i in range(2)))
    checks.check('GAIN-PHOTON-COUNT-DIFFER', gain['P1'] == F(1, 4)
                 and gain['A_total'] == F(3, 4),
                 photon=gain['P1'], total_count=gain['A_total'])

    c, r = F(1, 8), F(1, 32)
    for name, g in gain.items():
        true_image = mul(point(g), centered(c, r))
        advertised = centered(g * c, abs(g) * r)
        checks.check('INCOMING-' + name, advertised == true_image,
                     interval=advertised, center=g*c, radius=abs(g)*r)
    true_count = gain['A_total'] * (c + r)
    wrong_count = centered(gain['A_total'] * c, gain['P1'] * r)
    checks.check('REJECT-ENDPOINT-GAIN-FOR-COUNT',
                 not contains(wrong_count, point(true_count)),
                 wrong_interval=wrong_count, exact_endpoint=true_count)
    checks.check('REJECT-DROPPED-INCOMING-UNCERTAINTY',
                 not contains(point(gain['P1'] * c),
                              point(gain['P1'] * (c+r))))

    representation = F(-1, 128)
    old_baseline = F(3, 4)
    first_variation = F(1, 64)
    native_baseline = old_baseline - representation
    # With negative representation, omission moves the interval upward.  Select
    # the exact lower incoming endpoint so this wrong sign/omission is decisive.
    exact_truth = old_baseline + first_variation + gain['P1'] * (c-r)
    candidate = gain['P1'] * c + first_variation + representation
    corrected_interval = add(point(native_baseline), centered(candidate, gain['P1']*r))
    checks.check('SIGNED-REPRESENTATION-INCLUSION', contains(corrected_interval, point(exact_truth)),
                 true=exact_truth, interval=corrected_interval,
                 representation_exact_minus_native=representation)
    omitted = add(point(native_baseline), centered(candidate-representation, gain['P1']*r))
    checks.check('REJECT-OMITTED-REPRESENTATION',
                 not contains(omitted, point(exact_truth)))
    flipped = add(point(native_baseline), centered(candidate-2*representation, gain['P1']*r))
    checks.check('REJECT-REVERSED-REPRESENTATION',
                 not contains(flipped, point(exact_truth)))

    anchor_cases = [
        ('negative_delta_positive_photon', (F(-3), F(-2)), (F(1), F(3))),
        ('negative_delta_signed_correction', (F(-3), F(-2)), (F(-1, 8), F(1, 4))),
        ('positive_delta_negative_correction', (F(2), F(4)), (F(-1), F(-1, 4))),
        ('crossing_delta_signed_correction', (F(-2), F(1)), (F(-3), F(2))),
    ]
    for name, delta, photon in anchor_cases:
        products = [d*p for d in delta for p in photon]
        hull = mul(delta, photon)
        checks.check('ANCHOR-HULL-' + name,
                     hull == (min(products), max(products)), products=products, hull=hull)
        for i, product in enumerate(products):
            checks.check(f'ANCHOR-CORNER-{name}-{i}', contains(hull, point(product)), exact=product)
    dneg, pcorr = F(-3), F(1, 4)
    checks.check('REJECT-UNSIGNED-ANCHOR',
                 not contains(point(abs(dneg)*pcorr), point(dneg*pcorr)),
                 signed=dneg*pcorr, incorrect=abs(dneg)*pcorr)

    # Three exact constant-coefficient segments; anchors have both signs.
    # Native values intentionally include signed representation and stock defects.
    energies = [F(12), F(5), F(3)]
    native_P0 = F(1)
    true_P0 = native_P0 + c
    true_interval = centered(true_P0, r)
    c_in, r_in = c, r
    initial_true_stock = energies[0] * true_P0
    cumulative_true = {'A_total': F(0), 'B_total': F(0), 'Z': F(0)}
    cumulative_native = dict(cumulative_true)
    cumulative_correction = dict(cumulative_true)
    cumulative_radius = dict(cumulative_true)
    cumulative_jump = F(0)
    record = []
    initial_native_stock = energies[0] * native_P0 + F(1, 64)
    previous_true = None
    previous_Eh = None
    previous_native_P1 = None
    for index, energy in enumerate(energies):
        g, endpoint_energy = homogeneous_gains(energy, 2, [F(1,2), F(3,2)], [F(1,4), F(1,2)])
        stitch = F(0) if index == 0 else (F(1, 512) if index == 1 else F(-1, 1024))
        if index:
            native_P0 = previous_native_P1 - stitch
            c_in += stitch
            true_P0 = previous_true
            delta = energy - previous_Eh
            jump = delta * true_P0
            cumulative_jump += jump
            checks.check(f'PATH-ANCHOR-SIGN-{index}',
                         (jump < 0) if index == 1 else (jump > 0),
                         delta=delta, true_photon=true_P0, exact_jump=jump)
            checks.check(f'PATH-STITCH-CANDIDATE-{index}',
                         native_P0 + c_in == true_P0,
                         captured_stitch=stitch, incoming_center=c_in)
        frozen_P1 = g['P1'] * native_P0
        repP = F((-1)**index, 128*(index+1))
        native_P1 = frozen_P1 - repP
        true_P1 = g['P1'] * true_P0
        true_interval = mul(point(g['P1']), true_interval)
        c_out = g['P1'] * c_in + repP
        r_out = abs(g['P1']) * r_in
        interval_P1 = add(point(native_P1), centered(c_out, r_out))
        checks.check(f'PATH-PHOTON-{index}', interval_P1 == true_interval
                     and contains(interval_P1, point(true_P1)),
                     native=native_P1, correction=c_out, radius=r_out, interval=interval_P1)
        local_true = {}
        local_native = {}
        local_corrected = {}
        for j, name in enumerate(cumulative_true):
            exact_moment = g[name] * true_P0
            rep = F((-1)**(index+j), 256*(index+1)*(j+1))
            native_moment = g[name] * native_P0 - rep
            correction = g[name] * c_in + rep
            radius = abs(g[name]) * r_in
            checks.check(f'PATH-MOMENT-{index}-{name}',
                         native_moment + correction == exact_moment)
            local_true[name] = exact_moment
            local_native[name] = native_moment
            local_corrected[name] = correction
            cumulative_true[name] += exact_moment
            cumulative_native[name] += native_moment
            cumulative_correction[name] += correction
            cumulative_radius[name] += radius
            checks.check(f'PATH-CUMULATIVE-{index}-{name}',
                         cumulative_native[name] + cumulative_correction[name] == cumulative_true[name]
                         and cumulative_radius[name] > 0,
                         true=cumulative_true[name], native=cumulative_native[name],
                         correction=cumulative_correction[name], radius=cumulative_radius[name])
        native_U0 = energy * native_P0 + F(1, 64*(index+1))
        native_U1 = endpoint_energy * native_P1 - F(1, 256*(index+1))
        stockR0 = energy * native_P0 - native_U0
        stockR1 = endpoint_energy * native_P1 - native_U1
        correction_U0 = energy*c_in + stockR0
        correction_U1 = endpoint_energy*c_out + stockR1
        native_residual = native_U1-native_U0+local_native['B_total']+local_native['Z']
        corrected_residual = native_residual+correction_U1-correction_U0+local_corrected['B_total']+local_corrected['Z']
        checks.check(f'PATH-NATIVE-STOCK-ENERGY-{index}', corrected_residual == 0,
                     native_residual=native_residual, stock_residual_initial=stockR0,
                     stock_residual_final=stockR1)
        omitted_stock = native_residual + endpoint_energy*c_out - energy*c_in + local_corrected['B_total'] + local_corrected['Z']
        checks.check(f'REJECT-OMITTED-NATIVE-STOCK-{index}', omitted_stock != 0,
                     incorrect_residual=omitted_stock)
        record.append({'index':index,'true_P1':true_P1,'native_P1':native_P1,
                       'candidate':c_out,'radius':r_out,'native_stock_final':native_U1})
        c_in, r_in = c_out, r_out
        previous_true, previous_Eh, previous_native_P1 = true_P1, endpoint_energy, native_P1

    final_true_stock = previous_Eh * previous_true
    path_energy_residual = final_true_stock-initial_true_stock+cumulative_true['B_total']+cumulative_true['Z']-cumulative_jump
    checks.check('PATH-THREE-SEGMENT-NUMBER', previous_true-(F(1)+c)+cumulative_true['A_total'] == 0)
    checks.check('PATH-THREE-SEGMENT-ENERGY-WITH-ANCHORS', path_energy_residual == 0,
                 initial_stock=initial_true_stock, final_stock=final_true_stock,
                 moments=cumulative_true, signed_jump_sum=cumulative_jump)
    checks.check('REJECT-PATH-WITHOUT-ANCHORS',
                 final_true_stock-initial_true_stock+cumulative_true['B_total']+cumulative_true['Z'] != 0)
    checks.check('REJECT-CUMULATIVE-RESET',
                 cumulative_true['A_total'] != local_true['A_total'])

    failed = [row['TestID'] for row in checks.rows if row['status'] != 'PASS']
    return {'schema': 'bass-he-e13c5-independent-rational-toys-v1',
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'command_argv': sys.argv,
            'python': platform.python_version(),
            'arithmetic': 'Fraction exact rational; no Decimal and no imported production code',
            'status': 'PASS' if not failed else 'FAIL',
            'check_count': len(checks.rows), 'failures': failed,
            'checks': checks.rows, 'three_segment_records': pack(record),
            'claims': ['implementation-verified exact toy algebra',
                       'derived constant-opacity and signed-anchor identities'],
            'limits': ['Synthetic controls are not new physical solves.',
                       'No saved continuous reference is certified.',
                       'This contributor is not the final independent decision reviewer.']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit('fresh output path required')
    result = run()
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'check_count', 'failures', 'source_sha256']}))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
