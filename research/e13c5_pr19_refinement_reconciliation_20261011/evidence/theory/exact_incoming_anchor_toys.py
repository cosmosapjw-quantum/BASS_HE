#!/usr/bin/env python3
"""Exact E13C5 controls: Fraction coefficients and formal T=exp(-1).

No imports from the candidate, no binary floating-point exp, no physical solve.
The only transcendental sign facts use an independently derived rational
Taylor enclosure for exp(1), then invert it to enclose T.
"""
from fractions import Fraction as F
import argparse
import json
import math
from pathlib import Path


class R:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError('reversed rational interval')

    def __add__(self, other):
        other = other if isinstance(other, R) else R(other)
        return R(self.lo + other.lo, self.hi + other.hi)
    __radd__ = __add__

    def __neg__(self):
        return R(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -(other if isinstance(other, R) else R(other))

    def __mul__(self, other):
        other = other if isinstance(other, R) else R(other)
        ends = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return R(min(ends), max(ends))
    __rmul__ = __mul__

    def json(self):
        return {'lo': str(self.lo), 'hi': str(self.hi)}


class P:
    """Polynomial in T with exact rational coefficients, low powers first."""
    def __init__(self, coefficients=0):
        if isinstance(coefficients, P):
            self.c = coefficients.c
            return
        if not isinstance(coefficients, (tuple, list)):
            coefficients = [coefficients]
        c = [F(x) for x in coefficients]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c = tuple(c)

    def __add__(self, other):
        other = P(other)
        n = max(len(self.c), len(other.c))
        return P([(self.c[i] if i < len(self.c) else 0) +
                  (other.c[i] if i < len(other.c) else 0) for i in range(n)])
    __radd__ = __add__

    def __neg__(self):
        return P([-x for x in self.c])

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        other = P(other)
        c = [F(0)] * (len(self.c) + len(other.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                c[i + j] += a * b
        return P(c)
    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return P([x / F(scalar) for x in self.c])

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError('nonnegative integer formal power required')
        result = P(1)
        for _ in range(n):
            result *= self
        return result

    def __eq__(self, other):
        return self.c == P(other).c

    def interval(self):
        result = R(0)
        for coefficient in reversed(self.c):
            result = result * T_RANGE + coefficient
        return result

    def json(self):
        return {'basis': 'T^k; T=exp(-1)', 'coefficients': [str(x) for x in self.c]}


T = P([0, 1])
e_lower = sum((F(1, math.factorial(k)) for k in range(13)), F(0))
# Terms after k=12 start at 1/13!, and later ratios <= 1/14.
e_upper = e_lower + F(1, math.factorial(13)) / (1 - F(1, 14))
T_RANGE = R(1 / e_upper, 1 / e_lower)
CHECKS = []


def equal(name, actual, expected=0):
    actual, expected = P(actual), P(expected)
    CHECKS.append({'id': name, 'passed': actual == expected,
                   'relation': 'exact formal polynomial equality',
                   'difference': (actual - expected).json()})


def positive(name, value):
    value = P(value)
    bounds = value.interval()
    CHECKS.append({'id': name, 'passed': bounds.lo > 0,
                   'relation': 'strict positivity via rational Taylor enclosure',
                   'expression': value.json(), 'enclosure': bounds.json()})


def nonzero(name, value):
    value = P(value)
    bounds = value.interval()
    CHECKS.append({'id': name, 'passed': bounds.lo > 0 or bounds.hi < 0,
                   'relation': 'nonzero via rational Taylor enclosure',
                   'expression': value.json(), 'enclosure': bounds.json()})


def predicate(name, passed, **evidence):
    CHECKS.append({'id': name, 'passed': bool(passed), **evidence})


def J(rate):
    return P(1) if rate == 0 else (1 - T ** rate) / rate


def flow(initial, source, total_rate, species_rates, energy0, chi):
    """Exact constant-coefficient solution over h=1, E=energy0*exp(-u)."""
    initial = P(initial)
    if total_rate == 0:
        stock = initial + source
        integral = initial + F(source, 2)
        # integral u*exp(-u) = 1 - 2T
        energy_integral = energy0 * (initial * J(1) + source * (1 - 2 * T))
    else:
        stock = initial * (T ** total_rate) + source * J(total_rate)
        integral = initial * J(total_rate) + F(source, total_rate) * (1 - J(total_rate))
        energy_integral = energy0 * (initial * J(total_rate + 1) +
            F(source, total_rate) * (J(1) - J(total_rate + 1)))
    count = [rate * integral for rate in species_rates]
    absorbed = [rate * energy_integral for rate in species_rates]
    heat = [b - threshold * a for a, b, threshold in zip(count, absorbed, chi)]
    return {'P': stock, 'A': count, 'B': absorbed, 'H': heat,
            'Z': energy_integral, 'QN': P(source), 'QE': source * energy0 * J(1),
            'E': energy0 * T, 'U': energy0 * T * stock}


def incoming_tests():
    initial = F(1, 2)
    center, eta = F(1, 7), F(1, 8)
    lambdas, chi = [F(1, 3), F(2, 3)], [F(1), F(2)]
    frozen = flow(initial, F(1, 3), 1, lambdas, 12, chi)
    centered = flow(initial + center, F(1, 3), 1, lambdas, 12, chi)
    actual = flow(initial + center + eta, F(1, 3), 1, lambdas, 12, chi)
    gp, gz = T, 12 * J(2)
    ga = [rate * J(1) for rate in lambdas]
    gb = [rate * gz for rate in lambdas]
    gh = [b - threshold * a for a, b, threshold in zip(ga, gb, chi)]
    gains = {'P': gp, 'Z': gz, 'QN': P(0), 'QE': P(0), 'U': 12 * T * gp}
    equal('INCOMING_GAIN_NUMBER_LEDGER', gp + sum(ga), 1)
    equal('INCOMING_GAIN_ENERGY_LEDGER', 12 * T * gp + sum(gb) + gz, 12)
    for label, gain in gains.items():
        equal('INCOMING_CENTER_' + label, centered[label] - frozen[label], gain * center)
        equal('INCOMING_UNCERTAINTY_' + label, actual[label] - centered[label], gain * eta)
    for label, gg in [('A', ga), ('B', gb), ('H', gh)]:
        for i, gain in enumerate(gg):
            equal(f'INCOMING_CENTER_{label}_{i}', centered[label][i] - frozen[label][i], gain * center)
            equal(f'INCOMING_UNCERTAINTY_{label}_{i}', actual[label][i] - centered[label][i], gain * eta)
            positive(f'POSITIVE_GAIN_{label}_{i}', gain)
    rp = actual['P'] - centered['P']
    ra = sum(actual['A']) - sum(centered['A'])
    equal('NONZERO_INCOMING_REMAINDER_NUMBER_LEDGER', rp + ra, eta)
    equal('NONZERO_INCOMING_REMAINDER_ENERGY_LEDGER',
          actual['U'] - centered['U'] + sum(actual['B']) - sum(centered['B']) +
          actual['Z'] - centered['Z'], 12 * eta)
    equal('CORRECT_TOTAL_COUNT_BOUND_IS_EXACT', ra, eta * (1 - T))
    positive('REJECT_REUSING_PHOTON_BOUND_FOR_TOTAL_COUNT', ra - eta * T)
    equal('UNCERTAINTY_PERSISTS_WHEN_BR_AND_DL_ZERO', rp, eta * T)
    positive('ZERO_REMAINDER_WITH_ZERO_INCOMING_BUT_NONZERO_ETA_IS_WRONG', rp)
    previous_moment_error = F(1, 16)
    current_moment_error = eta * sum(gh)
    correct = previous_moment_error + current_moment_error
    wrong_damped = T * previous_moment_error + current_moment_error
    positive('REJECT_DAMPING_PREVIOUS_CUMULATIVE_MOMENT_ERROR', correct - wrong_damped)


def composition_tests():
    f01, source1, c, eta = F(1, 2), F(1, 3), F(1, 7), F(1, 8)
    incoming = c + eta
    chi = [F(1, 4), F(1, 2)]
    lf1, lf2 = [F(1, 3), F(2, 3)], [F(3, 2), F(1, 2)]
    frozen1 = flow(f01, source1, 1, lf1, 12, chi)
    true1 = flow(f01 + incoming, source1, 1, lf1, 12, chi)
    n1, n2 = F(2, 5), F(3, 50)
    rho1 = frozen1['P'] - n1
    e1 = true1['P'] - frozen1['P']
    ecenter1, eradius1 = c * T, eta * T
    for transfer_offset in [F(0), F(1, 100)]:
        tag = 'CONTIGUOUS' if transfer_offset == 0 else 'NONZERO_CAPTURE_TRANSFER'
        f02 = n1 + transfer_offset
        kappa = n1 - f02
        ein2 = e1 + rho1 + kappa
        equal(tag + '_CARRIED_INCOMING_IDENTITY', ein2, true1['P'] - f02)
        candidate2 = ecenter1 + rho1 + kappa
        equal(tag + '_CARRIED_RADIUS_NOT_RESET', ein2 - candidate2, eradius1)
        true2 = flow(true1['P'], 0, 2, lf2, 6, chi)
        frozen2 = flow(f02, 0, 2, lf2, 6, chi)
        equal(tag + '_SECOND_SEGMENT_CONTINUITY', true2['P'] - frozen2['P'], (T ** 2) * ein2)
        rho2 = frozen2['P'] - n2
        equal(tag + '_NATIVE_ENDPOINT_CORRECTION', true2['P'] - n2, (T ** 2) * ein2 + rho2)
        equal(tag + '_TWO_SEGMENT_INCOMING_UNCERTAINTY',
              true2['P'] - n2 - ((T ** 2) * candidate2 + rho2), eta * (T ** 3))
        nonzero(tag + '_REJECT_OMITTING_REPRESENTATION_SEAM', (T ** 2) * rho1)
        nonzero(tag + '_REJECT_RESETTING_INCOMING', (T ** 2) * ein2)
        if transfer_offset:
            nonzero(tag + '_REJECT_OMITTING_KAPPA', (T ** 2) * kappa)
    for next_e0, tag in [(F(6), 'POSITIVE'), (F(3), 'NEGATIVE')]:
        true2 = flow(true1['P'], 0, 2, lf2, next_e0, chi)
        delta_e = next_e0 - true1['E']
        anchor = delta_e * true1['P']
        ledger_no_anchor = true2['U'] - 12 * (f01 + incoming) + sum(true1['B']) + sum(true2['B']) + true1['Z'] + true2['Z'] - true1['QE'] - true2['QE']
        equal(tag + '_GLOBAL_ENERGY_LEDGER_MINUS_ANCHOR', ledger_no_anchor - anchor)
        equal(tag + '_OMITTED_ANCHOR_RESIDUAL', ledger_no_anchor, anchor)
        positive(tag + '_ANCHOR_EXPECTED_SIGN', anchor if next_e0 == 6 else -anchor)
        equal(tag + '_NATIVE_ANCHOR_CORRECTION', anchor - delta_e * n1, delta_e * (e1 + rho1))
        nonzero(tag + '_REJECT_NATIVE_ANCHOR_USING_EXACT_FROZEN_CORRECTION_ONLY', delta_e * rho1)
        equal(tag + '_ANCHOR_CARRIES_INCOMING_UNCERTAINTY',
              delta_e * (e1 + rho1) - delta_e * (ecenter1 + rho1), delta_e * eradius1)
    ucap = F(9, 5)
    rho_u = frozen1['U'] - ucap
    equal('NATIVE_ENERGY_STOCK_FULL_REPRESENTATION_IDENTITY',
          true1['U'] - ucap, true1['E'] * e1 + rho_u)
    equal('NATIVE_ENERGY_STOCK_REPRESENTATION_DECOMPOSITION',
          rho_u, true1['E'] * rho1 + true1['E'] * n1 - ucap)
    nonzero('REJECT_ONLY_E_TIMES_PHOTON_REPRESENTATION', rho_u - true1['E'] * rho1)
    acap = [F(1, 25), F(2, 25)]
    bcap = [F(1, 5), F(2, 5)]
    zcap, qncap, qecap = F(1, 3), F(1, 3), F(3)
    residual_n = P(n1 - f01 + sum(acap) - qncap)
    residual_e = P(ucap - 12 * f01 + sum(bcap) + zcap - qecap)
    correction_n = true1['P'] - n1 - incoming + sum(a - ac for a, ac in zip(true1['A'], acap)) - (true1['QN'] - qncap)
    correction_e = true1['U'] - ucap - 12 * incoming + sum(b - bc for b, bc in zip(true1['B'], bcap)) + true1['Z'] - zcap - (true1['QE'] - qecap)
    equal('NATIVE_LOCAL_NUMBER_CORRECTION_LEDGER_HAS_CAPTURED_RESIDUAL', correction_n, -residual_n)
    equal('NATIVE_LOCAL_ENERGY_CORRECTION_LEDGER_HAS_CAPTURED_RESIDUAL', correction_e, -residual_e)
    nonzero('NATIVE_CAPTURED_NUMBER_RESIDUAL_NOT_FORCED_TO_ZERO', residual_n)
    nonzero('NATIVE_CAPTURED_ENERGY_RESIDUAL_NOT_FORCED_TO_ZERO', residual_e)


def cancellation_incoming_tests():
    # F=1, qf=q=1, L=Lambda=1, ea=1/8. Then e=ea*exp(-u),
    # while delta_lambda1=+u/4 and delta_lambda2=-u/4.
    # The photon firstvariation is exact; species moments have a linear-in-ea
    # coefficient-variation product that must remain in the remainder.
    incoming, epsilon = F(1, 8), F(1, 4)
    a1 = incoming * epsilon * (1 - 2 * T)
    a2 = -a1
    b1 = 12 * incoming * epsilon * (1 - 3 * T ** 2) / 4
    b2 = -b1
    h1, h2 = b1 - a1, b2 - 2 * a2
    equal('DL_ZERO_NONZERO_INCOMING_TOTAL_COUNT_REMAINDER_CANCELS', a1 + a2)
    equal('DL_ZERO_NONZERO_INCOMING_TOTAL_ABSORBED_REMAINDER_CANCELS', b1 + b2)
    equal('DL_ZERO_NONZERO_INCOMING_TOTAL_HEAT_REMAINDER_SURVIVES', h1 + h2, a1)
    positive('REJECT_PHOTON_EXACT_IMPLIES_SPECIES_EXACT', a1)
    positive('REJECT_PHOTON_EXACT_IMPLIES_TOTAL_HEAT_EXACT', h1 + h2)
    equal('FIXED_O1_INCOMING_REMAINDER_LINEAR_IN_VARIATION', 2 * a1,
          incoming * (2 * epsilon) * (1 - 2 * T))


def product_uncertainty_tests():
    center, eta, eta_d = F(2, 5), F(1, 8), F(1, 16)
    for dcenter, tag in [(F(1, 3), 'POSITIVE'), (F(-1, 3), 'NEGATIVE'), (F(0), 'ZERO_CENTER')]:
        d_range, e_range = R(dcenter - eta_d, dcenter + eta_d), R(center - eta, center + eta)
        product = d_range * e_range
        bound = abs(dcenter) * eta + center * eta_d + eta_d * eta
        nominal = dcenter * center
        for i, (d, e) in enumerate([(d, e) for d in (d_range.lo, d_range.hi) for e in (e_range.lo, e_range.hi)]):
            exact = d * e
            predicate(f'{tag}_ANCHOR_PRODUCT_CORNER_{i}', product.lo <= exact <= product.hi and abs(exact - nominal) <= bound,
                      relation='exact rational inclusion and complete product error bound',
                      value=str(exact), product_enclosure=product.json(), bound=str(bound))
        sign = -1 if dcenter < 0 else 1
        worst = (dcenter + sign * eta_d) * (center + eta)
        bound_without_cross = abs(dcenter) * eta + center * eta_d
        predicate(tag + '_REJECT_OMITTING_ANCHOR_PRODUCT_CROSS_TERM',
                  abs(worst - nominal) > bound_without_cross,
                  relation='strict exact rational counterexample',
                  actual_error=str(abs(worst - nominal)), incomplete_bound=str(bound_without_cross),
                  omitted_cross_term=str(eta_d * eta))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    incoming_tests()
    composition_tests()
    cancellation_incoming_tests()
    product_uncertainty_tests()
    failures = [row for row in CHECKS if not row['passed']]
    result = {'schema': 'bass-he-e13c5-exact-incoming-anchor-toys-v1',
              'arithmetic': 'fractions.Fraction polynomial coefficients; formal T=exp(-1); rational Taylor-tail sign enclosure',
              'independence': 'No candidate imports; no Decimal or binary floating-point transcendental evaluation; inherited physical coefficient model not executed',
              'scope': 'Exact discriminating controls for incoming uncertainty, cumulative moments, representation seams, native ledgers and energy anchors',
              'T_enclosure': T_RANGE.json(),
              'checks': CHECKS, 'check_count': len(CHECKS), 'failures': failures,
              'status': 'PASS_SCOPED_EXACT_TOYS' if not failures else 'FAIL',
              'physical': 'HOLD', 'production': 'HOLD'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'check_count': len(CHECKS), 'fail_count': len(failures), 'status': result['status']}), flush=True)
    return 2 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
