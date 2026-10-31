"""Source-conditional D+D in-flight reaction opacity on frozen NRL FastD trajectory.

Nuclear cross section SSOT: Bosch & Hale (1992), Nuclear Fusion 32, 611,
1993 erratum Nucl Fusion 33, 1919; independently transcribed in MIT Magnetic
Fusion Energy Formulary (2014), section 9.7, Table cross section parameters.
This is R-matrix fitted physical cross section, NOT newly measured rows.

Stopping input: BASS_HE PR139 NRL 2023 plasma energy-moment narrow-beam characteristic,
nonrelativistic, fully ionized H/He FLRW; D/H scenario acropolis v1.3.1 obs.pdg2024.
D+D background cold at rest; E_cm = K_lab/2. Not a full fast nuclear network.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
import numpy as np
from scipy import constants as c
from numpy.polynomial.legendre import leggauss
from fastd import plasma, losses, terminal, MEV_J, MD, NOMINAL_SOURCE_DAUGHTERS

D_H = 2.547e-5  # ACROPOLIS v1.3.1 acropolis/obs.py pdg2024
D_H_SIGMA = 0.029e-5  # ACROPOLIS PDG2023/2024 observation; not a nuclear/transport error
BG_SQRT_KEV = 31.3970
# Bosch-Hale MIT-MFE 2014 tabulation: S(E)[keV mb] 5th-order numerator, zero denominator B1..B4
COEFF = {
    'dd_nhe3': (5.3701e4,3.3027e2,-1.2706e-1,2.9327e-5,-2.5151e-9),
    'dd_pt':   (5.5576e4,2.1054e2,-3.2638e-2,1.4987e-6,1.8181e-10),
}
# Source B-H validity CM energy keV (inclusive endpoints for in-domain use)
DOMAINS = {'dd_nhe3':(0.5,4900.), 'dd_pt':(0.5,5000.)}
MASS_MEV={'D':1875.61294257, 'p':938.27208816,'n':939.56542052,
          'T':2808.92113298, 'He3':2808.39160743}
Q_MEV={'dd_nhe3':2*MASS_MEV['D']-MASS_MEV['n']-MASS_MEV['He3'],
       'dd_pt':2*MASS_MEV['D']-MASS_MEV['p']-MASS_MEV['T']}
BIRTHS_MEV=[0.1,0.3,1.,3.,8.]
REDSHIFTS=[1.e4,3.e4,1.e5,3.e5,1.e6]


def sigma_bh_mb(ecm_keV:float,channel:str)->float:
    if channel not in COEFF: raise ValueError('unknown D-D nuclear channel')
    lo,hi=DOMAINS[channel]
    if not (math.isfinite(ecm_keV) and lo<=ecm_keV<=hi):
        raise ValueError('CM energy outside Bosch-Hale published fit domain')
    A=COEFF[channel]
    S=A[0]+ecm_keV*(A[1]+ecm_keV*(A[2]+ecm_keV*(A[3]+ecm_keV*A[4])))
    sigma=S/ecm_keV*math.exp(-BG_SQRT_KEV/math.sqrt(ecm_keV))
    if not math.isfinite(sigma) or sigma<0:raise ValueError('negative or invalid nuclear fit')
    return sigma


def stopping(K:float,p,mode='debye'):
    lr=losses(K,p,mode)
    if lr['total']<=0 or not math.isfinite(lr['total']):
        raise ValueError('stopping moment does not define positive characteristic loss')
    return lr['total']


def _kernel(K:float,p,dh:float,channel:str,log_mode='debye'):
    """d optical depth per MeV of *decrease* in K (MeV^-1)."""
    if not dh>0: raise ValueError('positive D/H required')
    Ecm_keV=500.*K  # equal-mass cold deuteron target, nonrel CM energy
    sig_m2=sigma_bh_mb(Ecm_keV,channel)*1e-31
    v=math.sqrt(2*K*MEV_J/MD)
    nD=p.n_p_m3*dh
    return nD*sig_m2*v/stopping(K,p,log_mode)


def integrate(K0:float,p,order:int=160,dh:float=D_H,log_mode='debye'):
    lo=terminal(p)
    if K0<=lo:raise ValueError('must start above NRL terminal characteristic energy')
    if K0>8.0 or lo<0.001:raise ValueError('source-bounded K0 is >8MeV or low endpoint outside BH fit')
    if not 0<dh<1:raise ValueError('invalid D/H')
    x,w=leggauss(order)
    a,b=math.log(lo),math.log(K0)
    k=np.exp((a+b)/2+(b-a)/2*x)
    dK=(b-a)/2*w*k
    dtn=np.array([_kernel(float(ki),p,dh,'dd_nhe3',log_mode) for ki in k])
    dtp=np.array([_kernel(float(ki),p,dh,'dd_pt',log_mode) for ki in k])
    nu_n=float(np.dot(dtn,dK));nu_p=float(np.dot(dtp,dK));nut=nu_n+nu_p
    # Probabilities: branch fractions integrated along a dilute nuclear optical depth.
    # Numerically stable; discrepancy from exact collision-point survival selection O(tau^2).
    probability=-math.expm1(-nut)
    pn=probability*nu_n/nut if nut>0 else 0.
    pp=probability*nu_p/nut if nut>0 else 0.
    mean_kn=float(np.dot(k*dtn,dK)/nu_n) if nu_n>0 else float('nan')
    mean_kp=float(np.dot(k*dtp,dK)/nu_p) if nu_p>0 else float('nan')
    # Q is stored as *nuclear binding energy release* not heat; no deposited-energy closure.
    return {'z':p.z,'K0_MeV':K0,'K_terminal_MeV':lo,'D_over_H':dh,'D_over_H_sigma':D_H_SIGMA,
            'tau_dd_nhe3':nu_n,'tau_dd_pt':nu_p,'tau_total_DD':nut,
            'P_nhe3':pn,'P_pt':pp,'P_any_BH_DD_fusion':probability,'P_no_BH_DD_fusion':math.exp(-nut),
            'P_sum_residual':probability+math.exp(-nut)-1,
            'K_lab_mean_nhe3_MeV':mean_kn,'K_lab_mean_pt_MeV':mean_kp,
            'Q_nhe3_MeV':Q_MEV['dd_nhe3'],'Q_pt_MeV':Q_MEV['dd_pt'],
            'expected_binding_release_MeV':pn*Q_MEV['dd_nhe3']+pp*Q_MEV['dd_pt'],
            'expected_unstopped_K_at_reaction_MeV':pn*mean_kn+pp*mean_kp,
            'B_H_domain_CM_KEV': '0.5-4900_nhe3__0.5-5000_pT',
            'n_D_m3':p.n_p_m3*dh,'source_scope':'PUBLISHED_BOSCH_HALE_X_NRL_MOMENT_CHARACTERISTIC',
            'nuclear_fit_extrapolation':False,'secondary_deposition':'NOT_COMPUTED'}


def channel_secondary(row:dict,channel:str):
    if channel not in COEFF:raise ValueError('bad channel')
    pch=row['P_nhe3'] if channel=='dd_nhe3' else row['P_pt']
    meanK=row['K_lab_mean_nhe3_MeV'] if channel=='dd_nhe3' else row['K_lab_mean_pt_MeV']
    a,b=('n','He3') if channel=='dd_nhe3' else ('p','T')
    Ecm=meanK/2
    available=Ecm+Q_MEV[channel]
    # non-rel two-body CM kinetic energy split; cannot derive lab angle distribution from total sigma
    ka=available*MASS_MEV[b]/(MASS_MEV[a]+MASS_MEV[b]);kb=available-ka
    return {'z':row['z'],'K0_MeV':row['K0_MeV'],'channel':channel,'P_first_inflight_reaction':pch,
            'mean_reaction_Klab_MeV':meanK,'mean_reaction_Ecm_MeV':Ecm,'Q_MeV':Q_MEV[channel],
            'first_product':a,'second_product':b,
            'mean_first_product_CM_K_MeV':ka,'mean_second_product_CM_K_MeV':kb,
            'mean_total_product_CM_K_MeV':ka+kb,'source':'BOSCH_HALE_1992_1993_ERRATUM_MIT_FORMULARY',
            'stopping_model':'PR139_NRL2023', 'product_lab_distribution':'NOT_MEASURED_OR_DERIVED',
            'product_heat':'NOT_COMPUTED'}


def profile(K0:float,p,points:int=129,dh:float=D_H):
    end=terminal(p)
    if K0>end and K0<=8:
        grid=np.geomspace(K0,end,points)
    else:raise ValueError('source-bounded k range invalid')
    out=[]
    for K in grid:
        x={'z':p.z,'K0_MeV':K0,'K_MeV':float(K),'Ecm_keV':float(K)*500,'D_over_H':dh,
           'sigma_nhe3_mb':sigma_bh_mb(500*float(K),'dd_nhe3'),
           'sigma_pt_mb':sigma_bh_mb(500*float(K),'dd_pt')}
        x['dtaudK_nhe3_perMeV']=_kernel(float(K),p,dh,'dd_nhe3')
        x['dtaudK_pt_perMeV']=_kernel(float(K),p,dh,'dd_pt')
        x['nuclear_Q_nhe3_MeV']=Q_MEV['dd_nhe3'];x['nuclear_Q_pt_MeV']=Q_MEV['dd_pt']
        out.append(x)
    return out
