"""Source-locked He4(gamma,d)d experimental data atlas (EXFOR).

Physics priority: genuine author-table, figure-digitized, energy-bin, and E2
multipole-resolved cross-section data. Not a stochastic event rate, 330 MeV
measured total, or deposited heat. All tabulated arithmetic is exact Fraction.
"""
from __future__ import annotations
import csv, hashlib, json, re, subprocess, sys
from pathlib import Path
from fractions import Fraction as F

EXPECTED={
 'M0011': {'blob':'20804471fb7584e07ab979ecad6a3e96cba0c6a2', 'sha256':'8d45af5ca4f0df3c000a5cf672cd84e2e8512b65b52b03a912c5080d2bf5d9b2', 'bytes':2508},
 'M0826': {'blob':'95010842754215e98eea8d99eff5f3de0799c666', 'sha256':'05ea65eaa1a7245f19fd47aa14e91bef3d706fe2a55c6d70a512808ee4e9284c', 'bytes':2396},
 'M0034': {'blob':'7bf684ee6f924c4a87d651a747bee08de1b8ae2d', 'sha256':'d1dbfa9e8899d91fa7c3993be6e22fd9d2aad0438084f09faf2906922eb3bd93', 'bytes':6262},
 'M0475': {'blob':'c49433293921dbb012d7f1b0387745732a598efa', 'sha256':'b2c1c52931e813dd63fb0e98edfc90088bc2eca497fd9142277e748f0935a82f', 'bytes':3349}}
M=F('3727.3794118')
m=F('1875.61294500')
Q=2*m-M
THRESHOLD=((2*m)**2-M**2)/(2*M)
SELECT={
 'M0011002':('TOTAL','AUTHOR_TABLE',14,'SIG'),
 'M0011003':('E2','AUTHOR_TABLE',7,'EP'),
 'M0826002':('TOTAL_BIN','TABLE_BIN',4,'SIG'),
 'M0826003':('DA_BIN','FIGURE_DIGITIZED_BIN',9,'DA'),
 'M0034005':('TOTAL','FIGURE_DIGITIZED',14,'SIG'),
 'M0034006':('E2','FIGURE_DIGITIZED',9,'EP'),
 'M0475002':('DA','AUTHOR_TABLE',12,'DA'),
 'M0475003':('TOTAL','AUTHOR_TABLE',6,'SIG'),
}
UNITS={
 'M0011002':['MEV','MICRO-B','MICRO-B'],
 'M0011003':['MEV','MICRO-B','MICRO-B'],
 'M0826002':['MEV','MEV','MICRO-B','MICRO-B'],
 'M0826003':['ADEG','ADEG','MU-B/SR','MU-B/SR'],
 'M0034005':['MEV','MICRO-B','MICRO-B'],
 'M0034006':['MEV','MICRO-B','MICRO-B'],
 'M0475002':['MEV','ADEG','NB/SR','NB/SR'],
 'M0475003':['MEV','NB','NB'],
}
HEADER={
 'M0011002':['EN','DATA','ERR-S'],
 'M0011003':['EN','DATA','ERR-S'],
 'M0826002':['EN-MIN','EN-MAX','DATA','ERR-S'],
 'M0826003':['ANG-CM-MIN','ANG-CM-MAX','DATA-CM','ERR-S'],
 'M0034005':['EN','DATA','ERR-S'],
 'M0034006':['EN','DATA','ERR-S'],
 'M0475002':['EN','ANG-CM','DATA-CM','ERR-S'],
 'M0475003':['EN','DATA','ERR-S'],
}

def fmt(x:F)->str: return f'{x.numerator}/{x.denominator}'
def dec(x:F)->str: return f'{float(x):.12g}'

def load_exact(source_dir:Path)->tuple[dict[str,str],dict]:
    raw={}; manifest={}
    for name,spec in EXPECTED.items():
        p=source_dir/f'{name}.x4'; b=p.read_bytes()
        h=hashlib.sha256(b).hexdigest()
        g=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if (len(b),h,g)!=(spec['bytes'],spec['sha256'],spec['blob']):
            raise ValueError(f'raw-source drift in {name}: {len(b)} {h} {g}')
        raw[name]=b.decode('ascii');manifest[name]={**spec,'path':f'sources/{name}.x4'}
    return raw,manifest

def parse_block_lines(lines:list[str], name:str)->list[dict]:
    blocks={}
    i=0
    while i<len(lines):
        if lines[i].startswith('SUBENT'):
            tokens=lines[i].split();current=tokens[1]; start=i
            i+=1
            while i<len(lines) and not lines[i].startswith('ENDSUBENT'):i+=1
            blocks[current]=lines[start:i+1]
        i+=1
    return blocks

def parse_sources(raw:dict)->dict[str,dict]:
    result={}
    for entry,txt in raw.items():
        blocks=parse_block_lines(txt.splitlines(),entry)
        for subent,block in blocks.items():
            if subent not in SELECT:continue
            category,status,nrows,rxn=SELECT[subent]
            key=next((line for line in block if line.startswith('REACTION')),None)
            if key is None or not key.count('2-HE-4(G,D)1-H-2') or not key.count(',,' if rxn!='EP' else ',EP,'):
                raise ValueError(f'wrong reaction for {subent}: {key}')
            # Pin the marker to the exact source. Curve digitizations and author tables differ.
            status_line=next((line for line in block if line.startswith('STATUS')),None)
            if status=='AUTHOR_TABLE' and '(TABLE)' not in status_line:
                raise ValueError(f'status mismatch for {subent}: {status_line}')
            if status.startswith('FIGURE') and '(CURVE' not in status_line:
                raise ValueError(f'curve mismatch {subent}')
            if rxn=='EP':
                cm='\n'.join(block)
                if 'POLAR\nNO-DIM\n' not in cm:raise ValueError('Missing EP multipolarity declaration')
                if not re.search(r'POLAR\nNO-DIM\n\s*2\.',cm):raise ValueError('EP multipolarity != E2')
            k=next((j for j,l in enumerate(block) if l.startswith('DATA ')),None)
            if k is None:raise ValueError('missing DATA in selected row')
            h=block[k].split()
            if int(h[1])!=len(HEADER[subent]) or int(h[2])!=nrows:raise ValueError('wrong EXFOR schema/count')
            if block[k+1].split()!=HEADER[subent] or block[k+2].split()!=UNITS[subent]:
                raise ValueError(f'wrong header/units in {subent}')
            rows=[]
            for line in block[k+3:k+3+nrows]:
                v=line.split()
                if len(v)!=len(HEADER[subent]):raise ValueError('missing raw data')
                row={key:F(raw) for key,raw in zip(HEADER[subent],v)}
                rows.append(row)
            common={}
            ck=next((j for j,l in enumerate(block) if l.startswith('COMMON')),None)
            if ck is not None:
                heads=block[ck+1].split();units=block[ck+2].split(); vals=block[ck+3].split()
                if len(heads)!=len(vals):raise ValueError('COMMON grain mismatch')
                common=dict(zip(heads,map(F,vals)))
            if subent=='M0826003' and (common!={'EN-MIN':F(30),'EN-MAX':F(50)}):
                raise ValueError('Energy window mismatch for DA')
            result[subent]={'entry':entry,'kind':category,'status':status,'rows':rows,'common':common,
                            'units':UNITS[subent],'data_headings':HEADER[subent], 'reaction':key.strip(),
                            'source_status':status_line.strip()}
    if set(result)!=set(SELECT):raise ValueError('missing/extra source subentries')
    return result

def make_dataset(parsed:dict,manifest:dict)->dict:
    products={};marginal={'M0011_AUTHOR_TOTAL_E2_SAME_ENERGY':[],
                            'M0034_CURVE_TOTAL_E2_EXACT_MATCH':[],
                            'M0011_M0034_NEAR_ENERGY_DIAGNOSTIC':[]}
    for key,block in parsed.items():
        items=[]
        for r in block['rows']:
            row={k:fmt(v) for k,v in r.items()}
            if 'EN' in r:
                energy=r['EN'];pair=energy-Q
                if energy<THRESHOLD:raise ValueError('below threshold measured source')
                data=r.get('DATA',r.get('DATA-CM'));err=r['ERR-S']
                assert data is not None
                row.update({'E_minus_Q_MeV':fmt(pair),
                            'sigma_times_pairK_source_unit_MeV':fmt(data*pair),
                            'stat_ERR_S_times_pairK_source_unit_MeV':fmt(err*pair)})
            else:
                if 'EN-MIN' in r: Emin,Emax=r['EN-MIN'],r['EN-MAX']
                else: Emin,Emax=block['common']['EN-MIN'],block['common']['EN-MAX']
                if Emin<THRESHOLD or Emin>=Emax:raise ValueError('invalid energy window')
                data=r.get('DATA',r.get('DATA-CM'))
                row.update({'E_minus_Q_support_MeV':[fmt(Emin-Q),fmt(Emax-Q)],
                            'sigma_times_pairK_conditional_support_source_unit_MeV':
                                [fmt(data*(Emin-Q)),fmt(data*(Emax-Q))],
                            'support_assumption':'same nonnegative energy-window response weight; NOT a measured central value'})
            items.append(row)
        products[key]={k:v for k,v in block.items() if k not in {'rows','common'}}
        products[key]['common']={k:fmt(v) for k,v in block['common'].items()}
        products[key]['observations']=items
    # E2/total same source and EXACT same E, no interpolation, nominal ratios only.
    for e2_sub,tot_sub,out in [('M0011003','M0011002','M0011_AUTHOR_TOTAL_E2_SAME_ENERGY'),
                               ('M0034006','M0034005','M0034_CURVE_TOTAL_E2_EXACT_MATCH')]:
        tot={x['EN']:x for x in parsed[tot_sub]['rows']}
        for x in parsed[e2_sub]['rows']:
            if x['EN'] not in tot:continue
            t=tot[x['EN']];frac=x['DATA']/t['DATA'];res=t['DATA']-x['DATA']
            marginal[out].append({'E_MeV':fmt(x['EN']),'total_sigma_microbarn':fmt(t['DATA']),
                'E2_sigma_microbarn':fmt(x['DATA']),'E2_fraction_nominal':fmt(frac),
                'nonE2_remainder_nominal_microbarn':fmt(res),
                'E2_share_joint_uncertainty':'UNKNOWN_COVARIANCE: do not treat ERR-S independent',
                'reported_E2_observable':'EXFOR EP,SIG with POLAR=2 (electric quadrupole); not beam polarisation'})
    # Pair-by-order only for source-lineage comparison; not physical cross energy matching.
    t1=parsed['M0011002']['rows'];t2=parsed['M0034005']['rows']
    for a,b in zip(t1,t2):
        marginal['M0011_M0034_NEAR_ENERGY_DIAGNOSTIC'].append({
            'M0011_E_MeV':fmt(a['EN']), 'M0034_E_MeV':fmt(b['EN']),
            'delta_E_MeV':fmt(b['EN']-a['EN']),
            'M0011_SIG_microbarn':fmt(a['DATA']), 'M0034_SIG_microbarn':fmt(b['DATA']),
            'meaning':'near-energy/origin comparison ONLY, NOT matched same-energy independent data'})
    return {'schema':'BASS_HE_EXFOR_MULTISOURCE_LOW_ENERGY_V1','owner':'cosmosapjw-quantum/BASS_HE',
       'source_revisions':{'exfor_master':'939a14d7bba1ddce51975cb5e8711ce96b3b0871'},
       'sources':manifest,'frozen_mass_energy_MeV':{'M_alpha':fmt(M),'m_D':fmt(m),'Q':fmt(Q),
                                                  'gamma_threshold':fmt(THRESHOLD)},
       'dataset':products,'derived_nominal_multipole':marginal,
       'row_totals':{k:len(v['observations']) for k,v in products.items()},
       'data_status':{'M0011':'AUTHOR_TABLE','M0034':'DIGITIZED_CURVE_NOT_INDEPENDENT_WITHOUT_SOURCE_AUDIT',
         'M0826':'ENERGY_BIN_AND_ANGLE_BIN','M0475':'EXISTING_HIGH_E_EXFOR',
         'E2_EP':'electric_quadrupole_multipole_POLAR_2_NOT_PHOTON_BEAM_POLARIZATION',
         'photoabsorption_SIG':'SOURCE_REPORTED_COUNTS_NOT_CALIBRATED_EXCLUSIVE_EVENT',
         '330_total':'NO_MEASURED_TOTAL',
         'ERR_S':'statistical only, cross-observable covariance unknown',
         'M0826_ERR_SYS':'photon beam intensity not higher than 5%; correlate within same experiment unknown',
         'L4':False,'physical_activation':False,'kappa':None,'R_event':None,'heat_rate':None,
         'D_fast_pool':None,'production':'HOLD'}}

def run(source_dir:Path,out_dir:Path):
    raw,manifest=load_exact(source_dir)
    blocks=parse_sources(raw)
    o=make_dataset(blocks,manifest)
    out_dir.mkdir(parents=True,exist_ok=True)
    (out_dir/'EXFOR_MULTI_SOURCE_ATLAS.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
    with (out_dir/'M0011_E2_SAME_ENERGY.csv').open('w',newline='') as f:
        rows=o['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY']
        w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
    with (out_dir/'M0011_M0034_ORIGIN_DIAGNOSTIC.csv').open('w',newline='') as f:
        rows=o['derived_nominal_multipole']['M0011_M0034_NEAR_ENERGY_DIAGNOSTIC']
        w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
    return o

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    o=run(root/'sources',root/'results')
    print('EXFOR SOURCE-LOCK PASS',len(o['sources']),'entries',sum(o['row_totals'].values()),'physical rows',o['row_totals'])
    for z in o['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY']:
        print('E2',dec(F(z['E_MeV'])),dec(F(z['E2_fraction_nominal'])))
