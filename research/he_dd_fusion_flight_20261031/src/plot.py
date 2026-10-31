import csv,pathlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams["svg.hashsalt"] = "BASS_HE_PR140_20261031"
R=pathlib.Path(__file__).resolve().parents[1];D=R/'data';F=R/'figures';F.mkdir(exist_ok=True)
def rows(name):
    with (D/name).open() as f:return list(csv.DictReader(f))
a=rows('FASTD_DD_REACTION_GREEN_25.csv')
styles={'figsize':(7,4.5),'dpi':150}
for mode,metric,label,name in [('branches','P_nhe3','P[D(d,n)He3] / fast D','DD_FUSION_NEUTRON_YIELD'),
                               ('all','P_any_BH_DD_fusion','Total D+D reaction probability / fast D','DD_FUSION_TOTAL_PROBABILITY'),
                               ('Q','expected_binding_release_MeV','Expected nuclear binding release [MeV/fast D]','DD_FUSION_BINDING_Q_BUDGET')]:
    fig,ax=plt.subplots(**styles)
    for z in [1e4,1e5,1e6]:
        x=sorted([r for r in a if float(r['z'])==z],key=lambda r:float(r['K0_MeV']))
        ax.plot([float(r['K0_MeV']) for r in x],[float(r[metric]) for r in x],marker='o',label='z='+format(z,'.0e'))
    ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Fast deuteron birth K [MeV]');ax.set_ylabel(label)
    ax.legend();ax.grid(True,which='both',alpha=.25)
    fig.tight_layout();fig.savefig(F/(name+'.png'),metadata={'Software':'PR140_BASS_HE'},dpi=150)
    fig.savefig(F/(name+'.svg'),metadata={'Date':'2026-10-31'},format='svg');plt.close(fig)
# Relevant reaction probabilities on fixed z after nonthermal Coulomb stopping
fig,ax=plt.subplots(**styles);s=sorted((r for r in a if float(r['z'])==1e5),key=lambda r:float(r['K0_MeV']))
for metric,label in [('P_nhe3','n + He3'),('P_pt','p + T')]:
    ax.plot([float(r['K0_MeV']) for r in s],[float(r[metric]) for r in s],marker='o',label=label)
ax.set(xlabel='Fast deuteron birth kinetic energy [MeV]',ylabel='Conditional in-flight probability',yscale='log',xscale='log')
ax.grid(True,which='both',alpha=.25);ax.legend();fig.tight_layout();fig.savefig(F/'DD_CHANNEL_BRANCHES.png',dpi=150,metadata={'Software':'PR140_BASS_HE'});fig.savefig(F/'DD_CHANNEL_BRANCHES.svg',metadata={'Date':'2026-10-31'});plt.close(fig)
print('PLOTS: 4 PNG and 4 SVG')
