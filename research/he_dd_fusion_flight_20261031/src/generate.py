"""Generate source-conditional FastD + D fusion physical data; keep parent PR139 frozen."""
import csv,json,sys,pathlib,math
import numpy as np
from fastd_fusion import *
from fastd import plasma, terminal, NOMINAL_SOURCE_DAUGHTERS
ROOT=pathlib.Path(__file__).resolve().parents[1];D=ROOT/'data';D.mkdir(exist_ok=True)

def save(name,rows):
    if not rows:raise ValueError('no output rows '+name)
    with (D/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    print(name,len(rows))

cases=[];events=[];profile_rows=[];checks=[];source_links=[];sigs=[]
# Calculated published fit grid within both source-valid CM windows, no new measured points.
for ecm in np.geomspace(1.,4000.,40):
    for channel in ['dd_nhe3','dd_pt']:
        sigs.append({'E_cm_keV':float(ecm),'K_lab_equiv_MeV':float(ecm)/500.,
                     'reaction':channel,'sigma_millibarn':sigma_bh_mb(float(ecm),channel),
                     'source_type':'PUBLISHED_RMATRIX_FIT_BOSCH_HALE_NOT_NEW_EXPERIMENT'})
for z in REDSHIFTS:
    p=plasma(z)
    for K0 in BIRTHS_MEV:
        r=integrate(K0,p,160)
        r320=integrate(K0,p,320)
        r_fixed=integrate(K0,p,160,log_mode='fixed20')
        max_rel=max(abs(r[k]-r320[k])/max(abs(r320[k]),1e-200) for k in
                    ['tau_dd_nhe3','tau_dd_pt','K_lab_mean_nhe3_MeV','K_lab_mean_pt_MeV'])
        # ACS input-source sensitivity is not nuclear S-factor or plasma-model uncertainty.
        r_low=integrate(K0,p,160,D_H-D_H_SIGMA)
        r_high=integrate(K0,p,160,D_H+D_H_SIGMA)
        check=dict(z=z,K0_MeV=K0,max_160_320_rel=max_rel,
            P_any_low_DH=r_low['P_any_BH_DD_fusion'],P_any_high_DH=r_high['P_any_BH_DD_fusion'],
            P_any_fixed_ln20=r_fixed['P_any_BH_DD_fusion'],
            P_fixed_ln20_over_dynamic=r_fixed['P_any_BH_DD_fusion']/r['P_any_BH_DD_fusion'],
            nuclear_fit_error_budget='UNKNOWN_NOT_ZERO',
            plasma_log_model_error_budget='SEPARATE_MODEL_SENSITIVITY')
        cases.append(r); checks.append(check)
        for channel in ['dd_nhe3','dd_pt']:events.append(channel_secondary(r,channel))
        profile_rows.extend(profile(K0,p,129))
    # Original PR129 high-energy nominal D birth records are OUTSIDE published B-H cross section range.
    # Only sub-8 MeV path probability conditioned on the D ion reaching 8MeV is supported.
    bounded=next(r for r in cases if r['z']==z and r['K0_MeV']==8.)
    for birth in NOMINAL_SOURCE_DAUGHTERS:
        source_links.append({'z':z,'source_birth_Knom_MeV':birth,'source':'PR129_ASBURY1965_SOURCE_CONDITIONAL_2BODY_KINEMATICS',
           'B_H_nuclear_fit_valid_from_Klab_MeV':0.001,
           'B_H_nuclear_fit_valid_to_Klab_MeV':8.,
           'P_dd_nhe3_if_survives_to8_MeV':bounded['P_nhe3'],
           'P_dd_pt_if_survives_to8_MeV':bounded['P_pt'],
           'P_any_if_survives_to8_MeV':bounded['P_any_BH_DD_fusion'],
           'P_survive_high_energy_to8_MeV':'UNKNOWN_NOT_1',
           'K_above8_nuclear_reaction':'OUTSIDE_FIT_DOMAIN_NOT_CALCULATED',
           'Q_secondaries_as_heat':'NOT_COMPUTED'})

save('BOSCH_HALE_DD_FIT_80.csv',sigs)
save('FASTD_DD_REACTION_GREEN_25.csv',cases)
save('FASTD_DD_REACTION_CHANNELS_50.csv',events)
save('FASTD_DD_REACTION_PROFILE_3225.csv',profile_rows)
save('FASTD_DD_VALIDATION_25.csv',checks)
save('FASTD_SOURCE_DAUGHTER_WINDOW_LINK_20.csv',source_links)
assert sum(map(len,[sigs,cases,events,profile_rows,checks,source_links])) == 3425
ref=next(r for r in cases if r['z']==1e5 and r['K0_MeV']==1.)
summary={'project':'cosmosapjw-quantum/BASS_HE','unit':'FASTD_BOSCH_HALE_DD_FUSION_INFLIGHT_PR140',
         'parent_pr':139,'parent_head':'7fa301e661e339e489ee447a6244892ea52cc3c2',
         'new_conditional_rows':3425,'new_measured_rows':0,
         'input_source_acropolis_DH':{'value':D_H,'sigma':D_H_SIGMA,'identity':'ACROPOLIS_1.3.1_obs.pdg2024'},
         'cross_section_source':'Bosch_Hale_1992_Nuclear_Fusion_32_611_plus_1993_erratum',
         'cross_section_transcription_check':'MIT_Magnetic_Fusion_Energy_Formulary_2014_sec9.7',
         'nuclear_reactions':['D(d,n)He3','D(d,p)T'],
         'plasma_source':'BASS_HE_PR139_NRL2023_FASTD_NARROW_BEAM',
         'data_counts':{'fusion_fit':len(sigs),'integrated':len(cases),'channel_products':len(events),
                        'resolved_profile':len(profile_rows),'validation':len(checks),'source_connection':len(source_links)},
         'validation':{'max_160_320_rel':max(x['max_160_320_rel'] for x in checks),
                       'max_P_normalization_residual':max(abs(x['P_sum_residual']) for x in cases),
                       'max_secondary_cm_energy_residual':max(abs(x['mean_total_product_CM_K_MeV']-(x['mean_reaction_Ecm_MeV']+x['Q_MeV'])) for x in events)},
         'reference':ref,
         'limits':['source-conditioned cold D target D/H observational input','NRL ensemble moment characteristic, not stochastic ion FP',
            'published B-H cross section valid only Ecm 0.5-4900keV /0.5-5000keV',
            'deuterons born >8MeV have unknown survival to the B-H domain',
            'all expected binding energy Q is NOT deposited thermal heat',
            'nuclear branching is perturbatively dilute; parent stopping unaffected to O(P)',
            'no cosmological high-energy gamma emission; no R_event, heat_rate, kappa'],
         'DAG':{'central':'28/88','he_physical':'14/18','delta':0},
         'production':'HOLD'}
(D/'SCIENTIFIC_SUMMARY.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print('MAIN '+json.dumps({'rows':summary['new_conditional_rows'],'reference':ref,'validation':summary['validation']},indent=2))
