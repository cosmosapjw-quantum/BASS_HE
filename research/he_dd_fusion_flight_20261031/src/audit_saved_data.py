"""Independent CSV structural/conservation audit; do not import fastd_fusion."""
import pathlib,csv,json,math
D=pathlib.Path(__file__).resolve().parents[1]/'data'
C={'BOSCH_HALE_DD_FIT_80.csv':80,'FASTD_DD_REACTION_GREEN_25.csv':25,
'FASTD_DD_REACTION_CHANNELS_50.csv':50,'FASTD_DD_REACTION_PROFILE_3225.csv':3225,
'FASTD_DD_VALIDATION_25.csv':25,'FASTD_SOURCE_DAUGHTER_WINDOW_LINK_20.csv':20}
allrows={}
for f,n in C.items():
    with (D/f).open() as stream:rs=list(csv.DictReader(stream))
    assert len(rs)==n,(f,len(rs),n)
    allrows[f]=rs
cases=allrows['FASTD_DD_REACTION_GREEN_25.csv']; events=allrows['FASTD_DD_REACTION_CHANNELS_50.csv']
for r in cases:
    t=lambda x:float(r[x]);
    assert 0<=t('P_any_BH_DD_fusion')<=1 and 0<=t('P_pt')<=1 and 0<=t('P_nhe3')<=1
    assert abs(t('P_pt')+t('P_nhe3')-t('P_any_BH_DD_fusion'))<1e-14
    assert abs(t('P_no_BH_DD_fusion')+t('P_any_BH_DD_fusion')-1)<5e-15
    assert abs(t('expected_binding_release_MeV')-(t('P_nhe3')*t('Q_nhe3_MeV')+t('P_pt')*t('Q_pt_MeV')))<1e-15
for r in events:
    t=lambda x:float(r[x])
    assert abs(t('mean_total_product_CM_K_MeV')-(t('mean_reaction_Ecm_MeV')+t('Q_MeV')))<1e-13
for r in allrows['FASTD_SOURCE_DAUGHTER_WINDOW_LINK_20.csv']:
    assert r['P_survive_high_energy_to8_MeV']=='UNKNOWN_NOT_1'
    assert r['K_above8_nuclear_reaction']=='OUTSIDE_FIT_DOMAIN_NOT_CALCULATED'
for r in allrows['FASTD_DD_VALIDATION_25.csv']:
    assert float(r['max_160_320_rel'])<1e-3
print('INDEPENDENT_SAVED_CSV_AUDIT PASS rows',sum(C.values()))
