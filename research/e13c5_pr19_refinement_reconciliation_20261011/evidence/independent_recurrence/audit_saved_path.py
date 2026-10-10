#!/usr/bin/env python3
"""Independent Fraction arithmetic audit of saved E13C5 path output.

The audit imports no candidate or interval-production code.  It certifies its
exact arithmetic comparisons of serialized endpoints, conditional on those
endpoints enclosing the local functions/integrals they claim to enclose.
No reference solver is run and no true reference solution is assumed.
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

SPECIES = ('HI', 'HeI', 'HeII')
CHI = tuple(F.from_float(x) for x in (13.598434599702, 24.587389011, 54.41776))
EV_ERG = F.from_float(1.602176634e-12)


def iv(x):
    if isinstance(x, dict):
        return (F(x['lo']), F(x['hi']))
    if isinstance(x, tuple):
        return x
    return (F(x), F(x))


def add(a, b):
    a, b = iv(a), iv(b)
    return (a[0]+b[0], a[1]+b[1])


def neg(a):
    a = iv(a)
    return (-a[1], -a[0])


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    a, b = iv(a), iv(b)
    corners = [x*y for x in a for y in b]
    return (min(corners), max(corners))


def scale(a, x):
    return mul(a, iv(x))


def divide_positive(a, x):
    assert x > 0
    a = iv(a)
    return (a[0]/x, a[1]/x)


def total(xs):
    out = iv(0)
    for x in xs:
        out = add(out, x)
    return out


def around(c, r):
    c, r = F(c), F(r)
    assert r >= 0
    return (c-r, c+r)


def contains(a, b):
    a, b = iv(a), iv(b)
    return a[0] <= b[0] and b[1] <= a[1]


def overlap(a, b):
    a, b = iv(a), iv(b)
    return max(a[0], b[0]) <= min(a[1], b[1])


def magnitude(a):
    a = iv(a)
    return max(abs(a[0]), abs(a[1]))


def cap(x):
    # Independent spelling of the contract CSV -> binary64 -> exact rational.
    return F.from_float(float(x))


def pack(x):
    if isinstance(x, F):
        return f'{x.numerator}/{x.denominator}'
    if isinstance(x, (tuple, list)):
        return [pack(v) for v in x]
    if isinstance(x, dict):
        return {k:pack(v) for k,v in x.items()}
    return x


class Checks:
    def __init__(self):
        self.rows = []

    def test(self, name, condition, **on_failure):
        row = {'TestID': name, 'status': 'PASS' if bool(condition) else 'FAIL'}
        if not condition:
            row['failure_evidence'] = pack(on_failure)
        self.rows.append(row)

    def enclosing(self, name, saved, required):
        self.test(name, contains(saved, required), saved=iv(saved), required=iv(required))

    def zero(self, name, box):
        self.enclosing(name, box, 0)


def capture_outputs(row):
    out = {'P1':cap(row['n']), 'P1_energy_eV':cap(row['u'])/EV_ERG,
           'Z_eV':cap(row['red'])/EV_ERG, 'QN':cap(row['qn']),
           'QE_eV':cap(row['qe'])/EV_ERG}
    for name, chi in zip(SPECIES, CHI):
        out['A_'+name] = cap(row['A_'+name])
        out['B_'+name+'_eV'] = cap(row['B_'+name])/EV_ERG
        out['H_'+name+'_eV'] = out['B_'+name+'_eV'] - chi*out['A_'+name]
    for prefix in ('A','B','H'):
        suffix = '' if prefix == 'A' else '_eV'
        out[prefix+'_total'+suffix] = sum(out[prefix+'_'+sp+suffix] for sp in SPECIES)
    return out


def recursive_intervals(checks, value, path):
    if isinstance(value, dict):
        if set(value) == {'lo','hi'}:
            box = iv(value)
            checks.test('ORDER/'+path, box[0] <= box[1], interval=box)
        else:
            for k, v in value.items():
                recursive_intervals(checks,v,path+'/'+k)
    elif isinstance(value,list):
        for i,v in enumerate(value):
            recursive_intervals(checks,v,path+'/'+str(i))


def audit_segment(checks, segment, control, prefix):
    row = control['row']
    incoming = segment['incoming']
    center, radius = F(incoming['center']), F(incoming['radius'])
    checks.test(prefix+'/incoming_radius_nonnegative', radius >= 0)
    checks.enclosing(prefix+'/incoming_center_radius', incoming['interval'], around(center,radius))
    captured = segment['captured']
    exact_captured = capture_outputs(row)
    for name, x in exact_captured.items():
        checks.enclosing(prefix+'/captured_exact_conversion/'+name,captured[name],x)
    E0, Eh = cap(row['e0']), iv(segment['endpoint_energy_eV'])
    f0, q, h = cap(row['f0']), cap(row['q']), cap(row['h'])
    lam = tuple(cap(row['lambda_'+sp]) for sp in SPECIES)
    L = sum(lam)
    gains = segment['gains']
    checks.enclosing(prefix+'/initial_energy_lift', segment['initial_energy_eV'], E0)
    checks.enclosing(prefix+'/frozen_Lh_lift', segment['frozen_Lh'], L*h)
    checks.test(prefix+'/captured_time_width', cap(row['a'])+h == cap(row['b']))
    checks.test(prefix+'/zero_outflow', cap(row['outn']) == cap(row['oute']) == 0)
    W = iv(gains['P1'])
    checks.test(prefix+'/photon_gain_damped', 0 <= W[0] <= W[1] <= 1)
    checks.zero(prefix+'/homogeneous_number_gain_identity', sub(add(W,gains['A_total']),1))
    checks.zero(prefix+'/homogeneous_energy_gain_identity',
                sub(total([mul(Eh,W),gains['B_total_eV'],gains['Z_eV']]),E0))
    checks.test(prefix+'/source_incoming_gains_zero',
                iv(gains['QN']) == iv(0) and iv(gains['QE_eV']) == iv(0))
    # Alternative algebraic coefficient formulas from conservation kernels.
    # Their overlapping enclosures are a consistency check, not an exp proof.
    J0 = divide_positive(sub(1,W),L)
    KE = divide_positive(sub(E0,mul(Eh,W)),L+1)
    independent_gain = {'P1':W,'Z_eV':KE,'QN':iv(0),'QE_eV':iv(0)}
    for sp, l, chi in zip(SPECIES,lam,CHI):
        independent_gain['A_'+sp] = scale(J0,l)
        independent_gain['B_'+sp+'_eV'] = scale(KE,l)
        independent_gain['H_'+sp+'_eV'] = scale(sub(KE,scale(J0,chi)),l)
    for pre in ('A','B','H'):
        suf = '' if pre == 'A' else '_eV'
        independent_gain[pre+'_total'+suf] = total(independent_gain[pre+'_'+sp+suf] for sp in SPECIES)
    independent_gain['P1_energy_eV'] = mul(Eh,W)
    for name, expected in independent_gain.items():
        checks.test(prefix+'/independent_gain_identity/'+name,
                    overlap(expected,gains[name]), derived=expected, saved=iv(gains[name]))
    for sp,chi in zip(SPECIES,CHI):
        checks.zero(prefix+'/gain_heat/'+sp,
                    add(sub(gains['H_'+sp+'_eV'],gains['B_'+sp+'_eV']),scale(gains['A_'+sp],chi)))
    checks.test(prefix+'/own_totalcount_gain_is_not_photon_gain',
                not overlap(gains['A_total'],gains['P1']))

    local = segment['local']
    first = segment['firstvariation_with_candidate_incoming']
    frozen = segment['frozen']
    representation = segment['representation_exactfrozen_minus_captured']
    rem = segment['remainder']
    bounds = local['bounds']
    expected_S = abs(center)+radius+iv(bounds['B_r'])[1]
    checks.test(prefix+'/S_includes_abs_incoming_and_radius',F(rem['S_upper']) >= expected_S,
                saved=F(rem['S_upper']),required=expected_S)
    HH, HE = iv(bounds['H_h'])[1], iv(bounds['H_E'])[1]
    expected_T = {'P1':HH, 'Z_eV':HE,'QN':F(0),'QE_eV':F(0),
                  'A_total':HH,
                  'B_total_eV':min(iv(bounds['effective_B_total'])[1],Eh[1]*HH+HE),
                  'H_total_eV':min(iv(bounds['effective_H_total'])[1],iv(bounds['triangle_H_total'])[1]),
                  'P1_energy_eV':Eh[1]*HH}
    for pre in ('A','B','H'):
        for sp in SPECIES:
            suf = '' if pre == 'A' else '_eV'
            expected_T[pre+'_'+sp+suf] = min(iv(bounds['effective_'+pre+'_'+sp])[1],
                                           iv(bounds['triangle_'+pre+'_'+sp])[1])
    for name, minimum in expected_T.items():
        T = F(rem['T_upper'][name])
        inc = F(rem['incoming_upper'][name])
        nonlinear = F(rem['nonlinear_upper'][name])
        total_bound = F(rem['total_before_numerical_upper'][name])
        checks.test(prefix+'/nonlinear_kernel/'+name, T >= minimum >= 0,saved=T,required=minimum)
        checks.test(prefix+'/incoming_gain_radius/'+name,
                    inc >= magnitude(gains[name])*radius,
                    saved=inc,required=magnitude(gains[name])*radius)
        checks.test(prefix+'/nonlinear_S_T/'+name,
                    nonlinear >= F(rem['S_upper'])*T,
                    saved=nonlinear,required=F(rem['S_upper'])*T)
        checks.test(prefix+'/remainder_sum/'+name,total_bound >= inc+nonlinear,
                    saved=total_bound,required=inc+nonlinear)

    for name, out in segment['outputs'].items():
        checks.enclosing(prefix+'/firstvariation_incoming/'+name, first[name],
                         add(local['signed'][name],scale(gains[name],center)))
        checks.enclosing(prefix+'/representation_signed/'+name,representation[name],
                         sub(frozen[name],captured[name]))
        represented = out['centered_firstvariation_plus_representation_interval']
        checks.enclosing(prefix+'/represented_firstvariation/'+name, represented,
                         add(first[name],representation[name]))
        candidate, final_radius = F(out['candidate']),F(out['radius'])
        numerical = F(out['numerical_and_representation_radius'])
        checks.test(prefix+'/numerical_representation_radius/'+name,
                    numerical >= magnitude(sub(represented,candidate)),
                    saved=numerical,required=magnitude(sub(represented,candidate)))
        checks.test(prefix+'/full_radius/'+name,
                    final_radius >= numerical+F(rem['total_before_numerical_upper'][name]),
                    saved=final_radius,required=numerical+F(rem['total_before_numerical_upper'][name]))
        checks.enclosing(prefix+'/correction_center_radius/'+name,
                         out['true_minus_captured_interval'],around(candidate,final_radius))
        checks.enclosing(prefix+'/native_absolute_output/'+name,out['true_absolute_interval'],
                         add(captured[name],out['true_minus_captured_interval']))
        checks.enclosing(prefix+'/true_model_conditional_inclusion/'+name,out['true_absolute_interval'],
                         add(captured[name],add(represented,around(0,F(rem['total_before_numerical_upper'][name])))))

    native_stock = segment['native_energy_stock_minus_Eh_n_eV']
    checks.enclosing(prefix+'/native_stock_residual', native_stock,
                     sub(captured['P1_energy_eV'],mul(Eh,captured['P1'])))
    checks.zero(prefix+'/representation_energy_stock_identity',
                add(sub(representation['P1_energy_eV'],mul(Eh,representation['P1'])),native_stock))
    ledgers = segment['ledger_enclosures']
    computed = {'frozen_number':sub(add(sub(frozen['P1'],f0),frozen['A_total']),frozen['QN']),
                'frozen_energy_eV':sub(total([frozen['P1_energy_eV'],-E0*f0,frozen['B_total_eV'],frozen['Z_eV']]),frozen['QE_eV']),
                'firstvariation_number':sub(add(sub(first['P1'],center),first['A_total']),first['QN']),
                'firstvariation_energy_eV':sub(total([first['P1_energy_eV'],-E0*center,first['B_total_eV'],first['Z_eV']]),first['QE_eV'])}
    for sp,chi in zip(SPECIES,CHI):
        computed['firstvariation_heat_'+sp] = add(sub(first['H_'+sp+'_eV'],first['B_'+sp+'_eV']),scale(first['A_'+sp],chi))
    for name, expected in computed.items():
        checks.enclosing(prefix+'/ledger_arithmetic/'+name,ledgers[name],expected)
        checks.zero(prefix+'/ledger_zero/'+name,expected)
    return exact_captured


def audit_track(checks, track, controls, prefix):
    segments, seams = track['segments'],track['seams']
    checks.test(prefix+'/three_segments_two_seams', len(segments)==3 and len(seams)==2)
    cumulative_centers = {name:F(0) for name in track['cumulative_moment_corrections']}
    cumulative_radius = dict(cumulative_centers)
    exact_cap_sum = dict(cumulative_centers)
    previous_cap_boxes = {name:iv(0) for name in cumulative_centers}
    previous_cumulative = {name:{'candidate':'0','radius':'0'} for name in cumulative_centers}
    previous_segment = None
    for j,(segment,control) in enumerate(zip(segments,controls)):
        sp = prefix+f'/segment{j}'
        checks.test(sp+'/key',segment['key']==control['key'])
        if j == 0:
            checks.test(sp+'/exact_initial_zero',F(segment['incoming']['center'])==F(segment['incoming']['radius'])==0)
        else:
            incoming=segment['incoming']; previous=seams[j-1]['next_incoming']
            checks.test(sp+'/incoming_transport_exact_serialization',incoming==previous)
            checks.test(sp+'/incoming_not_reset',F(incoming['radius'])>0 and F(incoming['center'])!=0)
        cap_values = audit_segment(checks,segment,control,sp)
        for name in cumulative_centers:
            out = segment['outputs'][name]
            now = segment['cumulative_moment_corrections'][name]
            c,r = F(now['candidate']),F(now['radius'])
            raw_center = F(previous_cumulative[name]['candidate'])+F(out['candidate'])
            minimum_radius=F(previous_cumulative[name]['radius'])+F(out['radius'])+abs(raw_center-c)
            checks.test(sp+'/cumulative_radius/'+name,r>=minimum_radius,saved=r,required=minimum_radius)
            checks.enclosing(sp+'/cumulative_interval/'+name,now['interval'],around(c,r))
            cumulative_centers[name] += F(out['candidate'])
            cumulative_radius[name] += F(out['radius'])
            checks.enclosing(sp+'/cumulative_all_prior_terms/'+name,now['interval'],
                             around(cumulative_centers[name],cumulative_radius[name]))
            exact_cap_sum[name] += cap_values[name]
            cap_box=segment['cumulative_captured_moments'][name]
            checks.enclosing(sp+'/cumulative_native_exact_sum/'+name,cap_box,exact_cap_sum[name])
            checks.enclosing(sp+'/cumulative_native_interval_add/'+name,cap_box,
                             add(previous_cap_boxes[name],segment['captured'][name]))
            previous_cap_boxes[name]=iv(cap_box)
            previous_cumulative[name]=now
        previous_segment=segment
    for j,seam in enumerate(seams):
        a,b=segments[j],segments[j+1]
        ar,br=controls[j]['row'],controls[j+1]['row']
        sp=prefix+f'/seam{j}'
        dE,corr=iv(seam['DeltaE_eV']),iv(seam['incoming_correction_to_anchor'])
        checks.enclosing(sp+'/signed_energy_delta',dE,sub(cap(br['e0']),a['endpoint_energy_eV']))
        checks.test(sp+'/correction_is_previous_output',seam['incoming_correction_to_anchor']==a['outputs']['P1']['true_minus_captured_interval'])
        products=[x*y for x in dE for y in corr]
        checks.test(sp+'/four_anchor_products_present',len(seam['anchor_endpoint_products'])==4)
        for k,(product,saved) in enumerate(zip(products,seam['anchor_endpoint_products'])):
            checks.enclosing(sp+f'/corner_product{k}',saved,product)
        hull=(min(products),max(products))
        checks.enclosing(sp+'/full_signed_correction_anchor',seam['correction_anchor_relative_to_captured_photon_eV'],hull)
        checks.enclosing(sp+'/native_anchor',seam['native_photon_anchor_eV'],mul(dE,a['captured']['P1']))
        true_box=mul(dE,add(a['captured']['P1'],corr))
        checks.enclosing(sp+'/true_anchor',seam['true_anchor_eV'],true_box)
        checks.enclosing(sp+'/anchor_split',seam['true_anchor_split_enclosure'],
                         add(seam['native_photon_anchor_eV'],seam['correction_anchor_relative_to_captured_photon_eV']))
        checks.enclosing(sp+'/split_covers_true_product',seam['true_anchor_split_enclosure'],true_box)
        gap=cap(ar['n'])-cap(br['f0'])
        checks.enclosing(sp+'/photon_stitch_exact',seam['captured_photon_stitch_residual'],gap)
        next_in=seam['next_incoming']; c_next,r_next=F(next_in['center']),F(next_in['radius'])
        previous=a['outputs']['P1']
        raw=F(previous['candidate'])+gap
        checks.test(sp+'/next_radius_preserves_stitch_rounding',
                    r_next>=F(previous['radius'])+abs(raw-c_next))
        checks.enclosing(sp+'/incoming_preserved',next_in['interval'],
                         add(previous['true_minus_captured_interval'],gap))
        checks.test(sp+'/captured_time_node_identity',cap(ar['b'])==cap(br['a'])
                    and ar['node']==br['node'] and cap(ar['eta'])==cap(br['eta'])
                    and cap(ar['weight'])==cap(br['weight']))
    anchor_sum=total(s['true_anchor_eV'] for s in seams)
    checks.enclosing(prefix+'/anchor_sum',track['summed_true_anchor_eV'],anchor_sum)
    checks.test(prefix+'/final_photon_identity',track['final_photon']==segments[-1]['outputs']['P1'])
    checks.test(prefix+'/final_energy_identity',track['final_energy_stock_eV']==segments[-1]['outputs']['P1_energy_eV'])
    true_moments=track['true_moment_enclosures']
    for name in cumulative_centers:
        checks.test(prefix+'/cumulative_snapshot/'+name,
                    track['cumulative_moment_corrections'][name]==segments[-1]['cumulative_moment_corrections'][name])
        checks.enclosing(prefix+'/final_true_moment/'+name,true_moments[name],
                         add(track['cumulative_captured_moments'][name],track['cumulative_moment_corrections'][name]['interval']))
    P0,E0=cap(controls[0]['row']['f0']),cap(controls[0]['row']['e0'])
    ledgers={'number':sub(add(sub(track['final_photon']['true_absolute_interval'],P0),true_moments['A_total']),true_moments['QN']),
             'energy_eV_with_anchor_subtracted':sub(sub(total([track['final_energy_stock_eV']['true_absolute_interval'],-E0*P0,true_moments['B_total_eV'],true_moments['Z_eV']]),true_moments['QE_eV']),track['summed_true_anchor_eV'])}
    for sp,chi in zip(SPECIES,CHI):
        ledgers['heat_'+sp]=add(sub(true_moments['H_'+sp+'_eV'],true_moments['B_'+sp+'_eV']),scale(true_moments['A_'+sp],chi))
    for name,box in ledgers.items():
        checks.enclosing(prefix+'/global_ledger_arithmetic/'+name,track['global_ledger_enclosures'][name],box)
        checks.zero(prefix+'/global_ledger_zero/'+name,box)
    for pre in ('A','B','H'):
        suf='' if pre=='A' else '_eV'
        checks.zero(prefix+'/global_species_total/'+pre,
                    sub(true_moments[pre+'_total'+suf],total(true_moments[pre+'_'+s+suf] for s in SPECIES)))


def identity(path):
    data=path.read_bytes()
    return {'path':str(path.resolve()),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def run(source_path,input_path):
    data=json.loads(source_path.read_text())
    inputs=json.loads(input_path.read_text())
    checks=Checks()
    checks.test('TOP/two_tracks',len(data['tracks'])==2)
    checks.test('TOP/protected_hold',data['physical']==data['production']=='HOLD')
    checks.test('TOP/no_other_solve',data['identity']['native_runs']==data['identity']['gas_advances']==data['identity']['old_continuous_solves']==0)
    recursive_intervals(checks,data,'results')
    for i,track in enumerate(data['tracks']):
        controls=inputs['controls'][i*3:(i+1)*3]
        audit_track(checks,track,controls,f"track{track['track']['node']}")
    failures=[r for r in checks.rows if r['status']!='PASS']
    return {'schema':'bass-he-e13c5-independent-saved-fraction-audit-v1',
            'created_utc':datetime.now(timezone.utc).isoformat(),
            'status':'PASS_SCOPED_ARITHMETIC' if not failures else 'FAIL',
            'check_count':len(checks.rows),'failed_count':len(failures),
            'checks':checks.rows,
            'arithmetic':'Fraction exact rational from Decimal strings; own interval algebra',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs':[identity(source_path),identity(input_path)],
            'python':platform.python_version(),'command_argv':sys.argv,
            'independence':{'production_module_imports':[],
                'shared_inputs':'The six captured controls and saved local gain/integral/remainder interval endpoints.',
                'production_source_read':'path_enclosure.py read for schema/semantics; not imported or executed.',
                'backend':'Python Fraction; no Decimal interval operations, exp, logarithm or physical solver.',
                'not_independent_of':'Physical coefficient model, inherited constants, input captures, local C4 interval certificate.'},
            'claim_ceiling':'Exact arithmetic audit of incoming, representation, signed anchor, cumulative and ledger bookkeeping conditional on the saved local enclosures; not an independent enclosure of the continuous reference, not final decision review.',
            'failure_ids':[r['TestID'] for r in failures]}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results',type=Path,required=True)
    p.add_argument('--inputs',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():
        raise SystemExit('fresh output path required')
    result=run(a.results,a.inputs)
    a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('status','check_count','failed_count','failure_ids','source_sha256')}))
    return 0 if result['failed_count']==0 else 1


if __name__=='__main__':
    raise SystemExit(main())
