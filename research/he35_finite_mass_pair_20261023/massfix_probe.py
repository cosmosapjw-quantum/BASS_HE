import numpy as np
from pair import sources
s=sources(1e20,1,1,1,1,np.eye(3),np.eye(3),[1,0,0],[0,0,0])
assert np.max(abs(s['forceA']-[-1,0,0]))<=5e-13
energy=float(np.trace(s['rawA']+s['rawB']));norm=max(np.linalg.norm(s['rawA']),np.linalg.norm(s['rawB']))
assert abs(energy)/norm<=5e-13
sw=sources(1,1e20,1,1,1,np.eye(3),np.eye(3),[0,0,0],[1,0,0])
assert np.max(abs(sw['forceB']-s['forceA']))<=5e-13
with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
 try:
  sources(1,1,1,1,1,np.eye(3),np.eye(3),[1e308,0,0],[0,0,0])
  raise AssertionError('nonfinite source accepted')
 except ValueError:pass
print({'forceA':s['forceA'].tolist(),'raw_energy_trace':energy,'normalized_energy_residual':abs(energy)/norm,'nonfinite_rejected':True})
