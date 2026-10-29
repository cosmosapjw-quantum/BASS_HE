"""Diagnostic plots of measured EXFOR points, NOT interpolants or joint CIs."""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(root):return json.loads((root/'results/EXFOR_MULTI_SOURCE_ATLAS.json').read_text())
def f(x):return float(F(x))

def plot(root):
    ds=read(root);sources=ds['dataset']; out=root/'figures';out.mkdir(exist_ok=True)
    fig,ax=plt.subplots(figsize=(9.4,5.3))
    entries=[('M0011002','1978 Arkatov table SIG',1),('M0034005','1980 Arkatov digitized SIG',1),('M0475003','1976 Arends table SIG',.001)]
    for key,name,scale in entries:
        t=sources[key]['observations']; E=[f(x['EN']) for x in t];y=[f(x['DATA'])*scale for x in t];err=[f(x['ERR-S'])*scale for x in t]
        ax.errorbar(E,y,yerr=err,fmt='o',capsize=2,linestyle='none',label=name)
    # For EXFOR binned quantities, render horizontal bins with central point for DISPLAY only.
    bins=sources['M0826002']['observations']
    xx=[(f(x['EN-MIN'])+f(x['EN-MAX']))/2 for x in bins]
    dx=[(f(x['EN-MAX'])-f(x['EN-MIN']))/2 for x in bins]
    ax.errorbar(xx,[f(x['DATA']) for x in bins],xerr=dx,yerr=[f(x['ERR-S']) for x in bins],fmt='s',capsize=3,linestyle='none',label='1972 Arkatov group: EN bins, centers display only')
    ax.set_yscale('log');ax.set(xlabel='Gamma energy (MeV; horizontal bin whiskers denote intervals)',ylabel='Source-reported SIG (microbarn; high-E nb converted)',title='4He(gamma,d)d actual EXFOR measurements: source lineage separated')
    ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'01_original_SIG_source_points.png',dpi=190);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8.2,4.8))
    t=ds['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY']
    ax.plot([f(x['E_MeV']) for x in t],[f(x['E2_fraction_nominal']) for x in t], 'o',label='1978 table at exact paired E values')
    ax.set(xlabel='Actual measured photon energy (MeV)',ylabel='Reported E2 multipole / total (nominal; no joint CI)',title='Source-reported electric quadrupole fraction (EP,POLAR=2)')
    ax.set_ylim(0,1.05);ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'02_M0011_E2_reported_fraction.png',dpi=190);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8.5,4.9))
    for key,name in [('M0011002','1978 total: author table'),('M0034005','1980 total: curve-digitized'),('M0011003','1978 E2: author table'),('M0034006','1980 E2: curve-digitized')]:
        z=sources[key]['observations'];ax.errorbar([f(v['EN']) for v in z],[f(v['DATA']) for v in z],yerr=[f(v['ERR-S']) for v in z],fmt='o',linestyle='none',capsize=2,label=name)
    ax.set(xlabel='Reported photon energy (MeV)',ylabel='SIG or EP,SIG (microbarn)',title='Provenance contrast: 1978 author tables vs 1980 digitized curves')
    ax.grid(alpha=.2);ax.legend(fontsize=7);fig.tight_layout();fig.savefig(out/'03_total_E2_source_lineage.png',dpi=190);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8.1,4.6))
    z=sources['M0826003']['observations']
    for x in z:
        l,u=f(x['ANG-CM-MIN']),f(x['ANG-CM-MAX']);v=f(x['DATA-CM']);e=f(x['ERR-S']);
        ax.plot([l,u],[v,v],linewidth=2)
        ax.errorbar([(l+u)/2],[v],xerr=[(u-l)/2],yerr=[e],fmt='o',capsize=2)
    ax.set(xlabel='CM angular range (deg; source reports bins)',ylabel='Source-reported DA (microbarn/sr)',title='1972 30–50 MeV photon-window angular data, NOT point-angle DA')
    ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'04_M0826_angular_bins.png',dpi=190);plt.close(fig)
    return sorted(p.name for p in out.glob('*.png'))
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    print(plot(root))
