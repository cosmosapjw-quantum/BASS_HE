#!/usr/bin/env python3
"""E13C5 PR19 compatibility and exact positive-weight refinement reduction.

No candidate imports, interval-Decimal implementation, exp, or ODE evaluation.
All serialized finite decimal endpoints are interpreted as exact Fractions.
The conditional hybrid is rebuilt per mode from ten old and two new path terms.
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

SP=('HI','HeI','HeII')
MODES=('OFF','KF','GM')
NODES=(0,700,1620,2344)
ORDER=((1,0),(2,0),(2,1))
EPS=F.from_float(1.602176634e-12)
LABELS=('Z_eV','QN','QE_eV')+tuple(p+'_'+s+('_eV' if p!='A' else '') for s in SP for p in ('A','B','H'))
PRIOR_SHA='418dcac9280947abc227c69f9178c0163bbdb00fa34bff1f9e34ab9eea35ece4'
PRIOR_CODE_SHA='aaae27a0d053d42ce6727593df676352697dd042486aa448d1e9104b16f979f6'
PILOT_SHA='75648e29291c3c364c2d8a0c859710d95074f1c12c5d910c61a4856465034b96'
HELPER_SHAS={'local_enclosure.py':'fade8983b7db8974c479ac4473424b7d572e8f7a0f09c042669fb3c40c32e370',
             'directed_interval.py':'ce4a44b11d1c0a3a5c52861033fa817a587bca9a5b852fab48329213b9a732e5'}


def box(x):
    if isinstance(x,dict):return (F(x['lo']),F(x['hi']))
    if isinstance(x,tuple):return x
    return (F(x),F(x))
def add(a,b):
    a,b=box(a),box(b);return (a[0]+b[0],a[1]+b[1])
def neg(a):
    a=box(a);return (-a[1],-a[0])
def sub(a,b):return add(a,neg(b))
def scale(a,k):
    a=box(a);v=(a[0]*k,a[1]*k);return(min(v),max(v))
def total(xs):
    v=box(0)
    for x in xs:v=add(v,x)
    return v
def includes(a,b):
    a,b=box(a),box(b);return a[0]<=b[0] and b[1]<=a[1]
def overlaps(a,b):
    a,b=box(a),box(b);return max(a[0],b[0])<=min(a[1],b[1])
def width(a):
    a=box(a);return a[1]-a[0]
def lift(x):return F.from_float(float(x))
def identity(p):
    raw=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def digest_object(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def decimal_exact(x):
    """Exact finite decimal rendering, otherwise a/b. No Decimal backend."""
    x=F(x)
    if x==0:return '0'
    d=x.denominator;a=b=0
    while d%2==0:a+=1;d//=2
    while d%5==0:b+=1;d//=5
    if d!=1:return str(x)
    n=max(a,b);digits=str(abs(x.numerator)*2**(n-a)*5**(n-b))
    if n:
        digits=digits.zfill(n+1);digits=digits[:-n]+'.'+digits[-n:]
        digits=digits.rstrip('0').rstrip('.')
    return ('-' if x<0 else '')+digits
def encode(x):
    if isinstance(x,F):return decimal_exact(x)
    if isinstance(x,tuple) and len(x)==2 and all(isinstance(v,F) for v in x):
        return {'lo':decimal_exact(x[0]),'hi':decimal_exact(x[1])}
    if isinstance(x,list):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x


class Audit:
    def __init__(self):self.checks=[];self.comparisons=[]
    def check(self,name,condition,**detail):
        self.checks.append({'TestID':name,'status':'PASS' if condition else 'FAIL',
                            **({'failure_evidence':encode(detail)} if not condition else {})})
    def comparison(self,name,old,new,semantics,run):
        old,new=box(old),box(new);ow,nw=width(old),width(new)
        ok=overlaps(old,new)
        self.check('COMPAT/'+run+'/'+name,ok,old=old,new=new)
        self.comparisons.append({'id':name,'current_run':run,'semantics':semantics,
            'prior':encode(old),'current':encode(new),'overlap':ok,
            'prior_contains_current':includes(old,new),'current_contains_prior':includes(new,old),
            'prior_width':decimal_exact(ow),'current_width':decimal_exact(nw),
            'prior_over_current_width_exact':str(ow/nw) if nw else None,
            'width_ratio_status':'DEFINED' if nw else ('BOTH_ZERO' if not ow else 'CURRENT_ZERO')})
    def failed(self):return [r for r in self.checks if r['status']=='FAIL']


def only_suffix(hashes,suffix):
    values=[v for k,v in hashes.items() if k.endswith(suffix)]
    if len(values)!=1:raise ValueError('unique recorded identity missing for '+suffix)
    return values[0]


def synthetic(audit):
    # Distinct weights make label swaps detectable in exact arithmetic.
    values={('OFF',0):F(2),('OFF',700):F(5),('KF',0):F(11),('KF',700):F(17)}
    weights={0:F(2),700:F(3)}
    off=sum(weights[n]*values[('OFF',n)] for n in (0,700))
    kf=sum(weights[n]*values[('KF',n)] for n in (0,700))
    audit.check('TOY/weighted_OFF_exact',off==19)
    audit.check('TOY/reject_dropped_weights',sum(values[('OFF',n)] for n in (0,700))!=off)
    audit.check('TOY/reject_swapped_nodes',weights[0]*values[('OFF',700)]+weights[700]*values[('OFF',0)]!=off)
    audit.check('TOY/reject_mode_mixing',off+kf!=off and off+kf!=kf)
    frozen,captured,old_correction=F(10),F(12),F(3)
    rho=frozen-captured;new_native_correction=old_correction+rho
    audit.check('TOY/representation_correct_mapping',captured+new_native_correction==frozen+old_correction==13)
    audit.check('TOY/reject_representation_confusion',captured+old_correction!=frozen+old_correction)
    old_terms=[(F(1),F(3)),(F(5),F(7))];new_term=(F(2),F(5,2))
    direct=add(new_term,old_terms[1])
    subtractive=add(sub(total(old_terms),old_terms[0]),new_term)
    audit.check('TOY/direct_hybrid_exact',direct==(F(7),F(19,2)))
    audit.check('TOY/reject_interval_subtraction_as_same_width',width(subtractive)>width(direct))
    return {'weighted_OFF':str(off),'weighted_KF':str(kf),'mode_mixed_invalid':str(off+kf),
            'native_correction':str(new_native_correction),'true_absolute':str(frozen+old_correction),
            'direct_hybrid':encode(direct),'subtractive_interval':encode(subtractive)}


def bind(a,prior,start,current,controls,ids,run):
    a.check('IDENTITY/'+run+'/current_controls_hash',
            current['identity']['source_sha256_before_run']['inputs/PATH_CONTROLS.json']==ids['controls']['sha256'])
    a.check('IDENTITY/'+run+'/current_resolution',current['identity']['subdivisions']==(512 if run=='N512_P60' else 128)
            and current['identity']['precision_digits']==60)
    a.check('IDENTITY/'+run+'/prior_resolution',start['N']==128 and start['precision']==60)
    hashes=start['hashes']
    for name,digest in HELPER_SHAS.items():
        a.check('IDENTITY/'+run+'/'+name,
            only_suffix(hashes,'/code/'+name)==digest==current['identity']['source_sha256_before_run']['code/'+name])
    for local,suffix in [('inputs/captured/OFF_SEGMENTS.csv','/capture/OFF/SEGMENTS.csv'),
                         ('inputs/captured/OFF_STAGES.csv','/inputs/OFF_STAGES.csv')]:
        a.check('IDENTITY/'+run+'/'+local,controls['source_files'][local]['sha256']==only_suffix(hashes,suffix))
    expected=[(m,n) for m in MODES for n in NODES]
    actual=[(p['mode'],p['node']) for p in prior['paths']]
    a.check('IDENTITY/'+run+'/prior12keys',actual==expected and len(set(actual))==12)
    a.check('IDENTITY/'+run+'/current2keys',[(p['track']['mode'],p['track']['node']) for p in current['tracks']]==[('OFF',0),('OFF',700)])
    a.check('IDENTITY/'+run+'/no_new_physical_run',current['identity']['native_runs']==current['identity']['gas_advances']==current['identity']['old_continuous_solves']==0)
    for track in current['tracks']:
        key=('OFF',track['track']['node']);old=next(p for p in prior['paths'] if (p['mode'],p['node'])==key)
        cc=[c for c in controls['controls'] if c['key'][2]==key[1]]
        expected_keys=[['OFF',s,key[1],j] for s,j in ORDER]
        a.check('IDENTITY/'+run+f'/OFF{key[1]}/segments',
                [s['key'] for s in old['segments']]==[s['key'] for s in track['segments']]==[c['key'] for c in cc]==expected_keys)
        weight=box(old['weight'])
        a.check('IDENTITY/'+run+f'/OFF{key[1]}/positive_exact_weight',weight[0]==weight[1]>0
                and all(lift(c['row']['weight'])==weight[0] for c in cc))
        for j,(s,c) in enumerate(zip(old['segments'],cc)):
            prefix='IDENTITY/'+run+f'/OFF{key[1]}/segment{j}'
            a.check(prefix+'/event',s['mask']==c['mask'] and s['source_on']==c['source_on']
                    and s['anchored']==bool(float(c['row']['anchored'])))
            true_native_p=lift(c['row']['n'])
            a.check(prefix+'/captured_P_by_old_Pend_DP',includes(sub(s['Pend'],s['DP']),true_native_p))
            expected_ia=box(0) if j==0 else sub(old['segments'][j-1]['Pend'],lift(c['row']['f0']))
            a.check(prefix+'/old_incoming_contains_exact_recursion',includes(s['Ia'],expected_ia),
                    saved=box(s['Ia']),exact=expected_ia)
            for label in LABELS:
                a.check(prefix+'/captured_baseline_overlap/'+label,overlaps(s['captured'][label],track['segments'][j]['captured'][label]))


def check_pilot(a,prior,pilot,controls,start,ids):
    a.check('REUSE/pilot_hash',ids['pilot']['sha256']==PILOT_SHA==only_suffix(start['hashes'],'/E13C5_OFF700_THREE_SEGMENT_INCOMING_ANCHOR_PILOT/RESULTS.json'))
    old=next(p for p in prior['paths'] if p['mode']=='OFF' and p['node']==700)
    rows=[c for c in controls['controls'] if c['key'][2]==700]
    a.check('REUSE/three_pilot_keys',[s['key'] for s in pilot['segments']]==[s['key'] for s in old['segments']])
    result=[]
    for j,(s,p,c) in enumerate(zip(old['segments'],pilot['segments'],rows)):
        a.check(f'REUSE/{j}/Ia_exact_endpoints_equal',box(s['Ia'])==box(p['Ia']))
        a.check(f'REUSE/{j}/Pend_exact_endpoints_equal',box(s['Pend'])==box(p['Pend']))
        expected=box(0) if j==0 else sub(old['segments'][j-1]['Pend'],lift(c['row']['f0']))
        a.check(f'REUSE/{j}/original_pilot_Ia_contains_exact_recurrence',includes(p['Ia'],expected),
                original_pilot=box(p['Ia']),exact_recurrence=expected)
        for field,newfield in [('DP','DP'),('g','g'),('J','J'),('remainder','remainder'),
                               ('frozen','frozen'),('captured','captured'),('continuous_minus_frozen','corrected')]:
            # These are replayed serialized objects. Equal JSON is a stronger
            # byte-semantic equality than overlap for these reused records.
            a.check(f'REUSE/{j}/unchanged_{field}',s[field]==p[newfield])
        result.append({'key':s['key'],'incoming_cover':s['Ia'],'incoming_original_pilot':p['Ia'],
                       'exact_recurred_incoming':encode(expected),
                       'original_pilot_contains_recurred':includes(p['Ia'],expected),
                       'endpoint_equal':box(s['Pend'])==box(p['Pend'])})
    return result


def compare(a,prior,current,controls,run):
    for track in current['tracks']:
        node=track['track']['node'];old=next(p for p in prior['paths'] if p['mode']=='OFF' and p['node']==node)
        weight=box(old['weight'])[0]
        for j,(s,t) in enumerate(zip(old['segments'],track['segments'])):
            prefix=f'OFF{node}/segment{j}'
            a.comparison(prefix+'/P_absolute',s['Pend'],t['outputs']['P1']['true_absolute_interval'],'absolute photon',run)
            a.comparison(prefix+'/P_native_correction',s['DP'],t['outputs']['P1']['true_minus_captured_interval'],'continuous minus captured photon',run)
            a.comparison(prefix+'/incoming',s['Ia'],t['incoming']['interval'],'continuous minus captured incoming photon',run)
            old_Ucorr=scale(s['energy_endpoint_minus_captured_erg'],1/EPS)
            a.comparison(prefix+'/U_native_correction_eV',old_Ucorr,t['outputs']['P1_energy_eV']['true_minus_captured_interval'],'continuous energy stock minus captured u/epsilon',run)
            for label in LABELS:
                rho=s['frozen_minus_captured'][label]
                old_correction=add(s['continuous_minus_frozen'][label],rho)
                old_absolute=add(s['frozen'][label],s['continuous_minus_frozen'][label])
                a.comparison(prefix+'/native_correction/'+label,old_correction,t['outputs'][label]['true_minus_captured_interval'],'continuous minus captured segment moment',run)
                a.comparison(prefix+'/absolute/'+label,old_absolute,t['outputs'][label]['true_absolute_interval'],'absolute segment moment',run)
                a.comparison(prefix+'/representation/'+label,rho,t['representation_exactfrozen_minus_captured'][label],'exact frozen minus captured segment moment',run)
            if j<2:
                a.comparison(prefix+'/anchor',s['anchor_to_next'],track['seams'][j]['true_anchor_eV'],'signed true energy anchor',run)
        for label in LABELS:
            a.comparison(f'OFF{node}/cumulative_native_correction/'+label,old['cumulative_correction'][label],
                         track['cumulative_moment_corrections'][label]['interval'],'continuous minus exact real sum of captured segment moments',run)
            a.comparison(f'OFF{node}/weighted_absolute/'+label,old['weighted_reduction'][label],
                         scale(track['true_moment_enclosures'][label],weight),'positive captured weight times absolute cumulative moment',run)
        a.comparison(f'OFF{node}/weighted_P_final',old['weighted_reduction']['P_final'],
                     scale(track['final_photon']['true_absolute_interval'],weight),'positive captured weight times final photon',run)
        a.comparison(f'OFF{node}/weighted_anchor',old['weighted_reduction']['anchor'],
                     scale(track['summed_true_anchor_eV'],weight),'positive captured weight times true anchor sum',run)
        # Prior's total heat is sum of species; current also has a direct bound.
        for pre in ('A','B','H'):
            suf='' if pre=='A' else '_eV'
            prior_total=total(old['cumulative_correction'][pre+'_'+sp+suf] for sp in SP)
            a.comparison(f'OFF{node}/cumulative_native_correction/{pre}_total{suf}',prior_total,
                         track['cumulative_moment_corrections'][pre+'_total'+suf]['interval'],
                         'same exact total; prior species sum versus current dedicated total enclosure',run)


def old_term_checks(a,prior):
    for p in prior['paths']:
        name=f"{p['mode']}/{p['node']}";w=box(p['weight'])
        a.check('REDUCTION_OLD/'+name+'/positive_point_weight',w[0]==w[1]>0)
        for label in LABELS:
            exact=scale(total(add(s['frozen'][label],s['continuous_minus_frozen'][label]) for s in p['segments']),w[0])
            a.check('REDUCTION_OLD/'+name+'/'+label,includes(p['weighted_reduction'][label],exact),
                    saved=box(p['weighted_reduction'][label]),exact=exact)
        a.check('REDUCTION_OLD/'+name+'/P_final',includes(p['weighted_reduction']['P_final'],scale(p['segments'][-1]['Pend'],w[0])))
        a.check('REDUCTION_OLD/'+name+'/anchor',includes(p['weighted_reduction']['anchor'],scale(total(s['anchor_to_next'] for s in p['segments']),w[0])))
    for mode in MODES:
        paths=[p for p in prior['paths'] if p['mode']==mode]
        a.check('REDUCTION_OLD/'+mode+'/four_nodes',[p['node'] for p in paths]==list(NODES))
        for label in (*LABELS,'P_final','anchor'):
            exact=total(p['weighted_reduction'][label] for p in paths)
            a.check('REDUCTION_OLD/'+mode+'/sum/'+label,
                    includes(prior['selected_subset_weighted_reductions'][mode][label],exact))


def hybrid(a,prior,current):
    current_by={('OFF',t['track']['node']):t for t in current['tracks']}
    terms=[];node_bridges=[]
    for old in prior['paths']:
        key=(old['mode'],old['node']);w=box(old['weight'])[0]
        if key in current_by:
            track=current_by[key]
            values={label:scale(track['true_moment_enclosures'][label],w) for label in LABELS}
            values['P_final']=scale(track['final_photon']['true_absolute_interval'],w)
            values['anchor']=scale(track['summed_true_anchor_eV'],w)
            item={'mode':key[0],'node':key[1],'provenance':'CURRENT_N512_REPLACEMENT',
                  'weight':old['weight'],'weighted_reduction':encode(values),
                  'prior_weighted_reduction':old['weighted_reduction'],
                  'preserved_captured_segments':[s['captured'] for s in old['segments']],
                  'preserved_captured_segment_to_node_reductions':[s['captured_segment_to_node_reduction'] for s in old['segments']]}
            for step,indexes,last in [(1,[0],0),(2,[1,2],2)]:
                reduction=old['segments'][last]['captured_segment_to_node_reduction']
                corrected={label:add(total(track['segments'][j]['outputs'][label]['true_minus_captured_interval'] for j in indexes),reduction[label]) for label in LABELS}
                corrected['P_endpoint']=add(track['segments'][last]['outputs']['P1']['true_minus_captured_interval'],reduction['P'])
                corrected['U_endpoint_eV']=add(track['segments'][last]['outputs']['P1_energy_eV']['true_minus_captured_interval'],scale(reduction['U_erg'],1/EPS))
                node_bridges.append({'mode':key[0],'node':key[1],'step':step,
                    'segment_keys':[track['segments'][j]['key'] for j in indexes],
                    'preserved_captured_segment_to_node_reduction':reduction,
                    'correction_relative_to_captured_node':encode(corrected),
                    'meaning':'current continuous-minus-captured-segments plus unchanged captured-segments-minus-captured-node; endpoint U_erg reduced and converted exactly once',
                    'does_not_certify':'native full weighted aggregate reduction or a node with any different gas/mask/source/anchor inputs'})
        else:
            item={'mode':key[0],'node':key[1],'provenance':'UNCHANGED_PRIOR_N128',
                  'weight':old['weight'],'weighted_reduction':old['weighted_reduction'],
                  'preserved_captured_segments':[s['captured'] for s in old['segments']],
                  'preserved_captured_segment_to_node_reductions':[s['captured_segment_to_node_reduction'] for s in old['segments']]}
            a.check(f"HYBRID/unchanged/{key[0]}/{key[1]}",item['weighted_reduction']==old['weighted_reduction'])
        terms.append(item)
    a.check('HYBRID/exactly_two_replacements',sum(t['provenance']=='CURRENT_N512_REPLACEMENT' for t in terms)==2)
    a.check('HYBRID/exactly_ten_preserved',sum(t['provenance']=='UNCHANGED_PRIOR_N128' for t in terms)==10)
    exact_sums={};published={};metrics=[]
    for mode in MODES:
        selected=[t for t in terms if t['mode']==mode]
        a.check('HYBRID/'+mode+'/same_four_nodes',[p['node'] for p in selected]==list(NODES))
        exact_sums[mode]={label:encode(total(t['weighted_reduction'][label] for t in selected)) for label in (*LABELS,'P_final','anchor')}
        # Retain published KF/GM interval bytes; expose exact rational sums too.
        published[mode]=exact_sums[mode] if mode=='OFF' else prior['selected_subset_weighted_reductions'][mode]
        if mode!='OFF':a.check('HYBRID/'+mode+'/aggregate_unchanged',published[mode]==prior['selected_subset_weighted_reductions'][mode])
        for label in (*LABELS,'P_final','anchor'):
            a.check('HYBRID/'+mode+'/aggregate_contains_exact_terms/'+label,includes(published[mode][label],exact_sums[mode][label]))
            old=box(prior['selected_subset_weighted_reductions'][mode][label]);new=box(published[mode][label]);ow,nw=width(old),width(new)
            a.check('HYBRID/'+mode+'/old_overlap/'+label,overlaps(old,new))
            metrics.append({'mode':mode,'quantity':label,'prior_width':decimal_exact(ow),'hybrid_width':decimal_exact(nw),
                'prior_over_hybrid_width_exact':str(ow/nw) if nw else None,
                'width_ratio_status':'DEFINED' if nw else ('BOTH_ZERO' if not ow else 'HYBRID_ZERO'),
                'prior_contains_hybrid':includes(old,new),'hybrid_contains_prior':includes(new,old)})
    # Optional total A/B/H outputs remain sums within each mode only.
    totals={}
    for mode in MODES:
        totals[mode]={p+'_total'+('' if p=='A' else '_eV'):encode(total(published[mode][p+'_'+sp+('' if p=='A' else '_eV')] for sp in SP)) for p in ('A','B','H')}
    return {'method':'direct exact positive-weight sum of 10 unchanged prior path terms and 2 current N512 terms, grouped by alternative mode',
            'path_terms':terms,'exact_fraction_term_sums_by_mode':exact_sums,
            'selected_subset_weighted_reductions':published,'species_totals_by_mode':totals,
            'width_diagnostics':metrics,'captured_node_bridges':node_bridges,
            'mode_mixing':False,'cross_mode_total':None,
            'claims':'conditional selected-subset reduction of reviewed constituent enclosures; no new path solve, native aggregate reduction or full-first2 admission'}


def numerical_projection(result):
    """Host-independent N512 postprocessing payload for a fresh NCP producer.

    Raw fresh producer-file identity is verified by the outer execution runner;
    its numerical outputs occur throughout compatibility and hybrid records.
    Optional N128 diagnostic checks/results do not alter this projection.
    """
    checks=[x for x in result['checks'] if '/N128_P60/' not in x['TestID']]
    comparisons=[x for x in result['compatibility_comparisons'] if x['current_run']=='N512_P60']
    return {'schema':'bass-he-e13c5-pr19-reconciliation-numerical-projection-v1',
        'node':result['node'],'status':result['status'],
        'source_sha256':result['source_sha256'],'prior_commit':result['prior_commit'],
        'stable_input_identities':{k:{'sha256':v['sha256'],'bytes':v['bytes']} for k,v in result['inputs'].items() if k not in ('current','diagnostic')},
        'current_numerical_contract':result['current_numerical_contract'],
        'checks':checks,'check_count':len(checks),
        'compatibility_comparisons':comparisons,'comparison_count':len(comparisons),
        'original_pilot_reuse_incoming':result['original_pilot_reuse_incoming'],
        'exact_toy':result['exact_toy'],'hybrid':result['hybrid'],
        'semantic_mapping':result['semantic_mapping'],
        'arithmetic':result['arithmetic'],'independence':result['independence'],
        'new_coefficient_evaluations':result['new_coefficient_evaluations'],
        'new_native_or_gas_or_continuous_solves':result['new_native_or_gas_or_continuous_solves'],
        'holds':result['holds']}


def main():
    parser=argparse.ArgumentParser()
    for arg in ('prior','prior-start','pilot','current','controls','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    parser.add_argument('--prior-code',type=Path)
    parser.add_argument('--diagnostic',type=Path)
    args=parser.parse_args()
    if args.out.exists():raise SystemExit('fresh output path required')
    if args.prior_code is None:args.prior_code=args.prior.parent/'cover.py'
    paths={k:getattr(args,k) for k in ('prior','prior_start','prior_code','pilot','current','controls')}
    if args.diagnostic:paths['diagnostic']=args.diagnostic
    ids={k:identity(v) for k,v in paths.items()}
    data={k:json.loads(p.read_text()) for k,p in paths.items() if k!='prior_code'}
    a=Audit();toy=synthetic(a)
    a.check('IDENTITY/prior_result_pin',ids['prior']['sha256']==PRIOR_SHA)
    a.check('IDENTITY/prior_code_pin',ids['prior_code']['sha256']==PRIOR_CODE_SHA)
    reuse=check_pilot(a,data['prior'],data['pilot'],data['controls'],data['prior_start'],ids)
    bind(a,data['prior'],data['prior_start'],data['current'],data['controls'],ids,'N512_P60')
    compare(a,data['prior'],data['current'],data['controls'],'N512_P60')
    if args.diagnostic:
        bind(a,data['prior'],data['prior_start'],data['diagnostic'],data['controls'],ids,'N128_P60')
        compare(a,data['prior'],data['diagnostic'],data['controls'],'N128_P60')
    old_term_checks(a,data['prior'])
    hybrid_result=None
    if not a.failed():hybrid_result=hybrid(a,data['prior'],data['current'])
    failed=a.failed();comparisons=a.comparisons
    result={'schema':'bass-he-e13c5-pr19-refinement-reconciliation-v1',
        'node':'HE_E13C5_PR19_REFINEMENT_RECONCILIATION01',
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS_SCOPED_POSTPROCESSING' if not failed and hybrid_result else 'FAIL',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':platform.python_version(),'command_argv':sys.argv,'inputs':ids,
        'current_numerical_contract':{k:data['current']['identity'][k] for k in ('subdivisions','precision_digits','source_sha256_before_run')},
        'prior_commit':'e25039b3a53031ce37800cebefb51200aa5a63a2',
        'checks':a.checks,'check_count':len(a.checks),'failed_count':len(failed),
        'failure_ids':[r['TestID'] for r in failed],
        'compatibility_comparisons':comparisons,
        'comparison_count':len(comparisons),'disjoint_count':sum(not r['overlap'] for r in comparisons),
        'original_pilot_reuse_incoming':reuse,'exact_toy':toy,'hybrid':hybrid_result,
        'arithmetic':'stdlib Fraction exact rational; no Decimal/exp/solver/candidate imports',
        'new_coefficient_evaluations':0,'new_native_or_gas_or_continuous_solves':0,
        'semantic_mapping':{
          'Pend':'current outputs.P1.true_absolute_interval',
          'DP':'current outputs.P1.true_minus_captured_interval',
          'old_continuous_minus_frozen_plus_old_frozen_minus_captured':'current outputs.X.true_minus_captured_interval',
          'old_frozen_plus_old_continuous_minus_frozen':'current outputs.X.true_absolute_interval',
          'old_cumulative_correction':'current cumulative_moment_corrections.X.interval',
          'old_energy_endpoint_minus_captured_erg_divided_by_epsilon':'current outputs.P1_energy_eV.true_minus_captured_interval',
          'old_weighted_reduction':'captured positive weight times current absolute cumulative moments, final photon, signed true anchor sum'},
        'independence':'Independent representation/reduction arithmetic; shared captured inputs and unchanged E13C4 coefficient/interval helpers; prior/local enclosure validity remains conditional on constituent reviews. Overlap is consistency, not independent validation of the same physical model.',
        'holds':['full_first2','physical','production','new_gas_evolution','actual_atomic_photon_heat_recoil','receiver_adoption','automatic_E13C6'],
        'actual_host_execution':'This command performs saved-output postprocessing only; external caller records runtime provenance.'}
    projection=numerical_projection(result)
    projection_sha=digest_object(projection)
    result['numerical_projection_sha256']=projection_sha
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'RESULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    (args.out/'NUMERICAL_PROJECTION.json').write_text(json.dumps(projection,sort_keys=True,separators=(',',':'))+'\n')
    (args.out/'NUMERICAL_IDENTITY.json').write_text(json.dumps({'numerical_projection_sha256':projection_sha,
       'definition':'sha256 of numerical_projection(result) canonical JSON sorted keys and compact separators, excluding trailing newline',
       'included':'all substantive N512 compatibility, hybrid, representation, reuse and control data',
       'excluded':'N128 optional diagnostics and associated checks; timing/host/argv/paths/current raw producer file hash',
       'current_producer_identity_obligation':'outer runner must independently check fresh producer identity and numerical parity'},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','check_count','failed_count','failure_ids','comparison_count','disjoint_count','source_sha256')}))
    return 0 if result['status']=='PASS_SCOPED_POSTPROCESSING' else 1


if __name__=='__main__':raise SystemExit(main())
