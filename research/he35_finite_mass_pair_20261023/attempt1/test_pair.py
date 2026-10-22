import ctypes,json,subprocess
from pathlib import Path
import numpy as np
from pair import matrices,sources
checks={}
def check(name,x,y,scale=None):
 x=np.asarray(x);y=np.asarray(y);e=float(np.max(np.abs(x-y))/(scale or max(np.max(np.abs(x)),np.max(np.abs(y)),1e-290)));checks[name]=e;assert e<=5e-13,(name,e)
rng=np.random.default_rng(3535)
for i in range(8):
 ma,mb,na,nb,k=2.,7.,3.,5.,.13
 va=rng.normal(size=(5,3))+[2,1,-1];vb=rng.normal(size=(7,3))+[-1,0,2]
 wa=rng.random(5);wa/=sum(wa);wb=rng.random(7);wb/=sum(wb)
 ua=wa@va;ub=wb@vb
 pa=ma*na*np.einsum('i,ij,ik->jk',wa,va-ua,va-ua);pb=mb*nb*np.einsum('i,ij,ik->jk',wb,vb-ub,vb-ub)
 s=sources(ma,mb,na,nb,k,pa,pb,ua,ub)
 ra=np.zeros((3,3));rb=ra.copy();fa=np.zeros(3)
 # Exact degree-two outgoing spherical quadrature using six axis directions.
 for v,p in zip(va,wa):
  for w,q in zip(vb,wb):
   V=(ma*v+mb*w)/(ma+mb);g=np.linalg.norm(v-w)
   for d in np.concatenate((np.eye(3),-np.eye(3))):
    vp=V+mb/(ma+mb)*g*d;wp=V-ma/(ma+mb)*g*d;wt=p*q*na*nb*k/6
    ra+=wt*ma*(np.outer(vp,vp)-np.outer(v,v));rb+=wt*mb*(np.outer(wp,wp)-np.outer(w,w));fa+=wt*ma*(vp-v)
 for key,z in [('rawA',ra),('rawB',rb),('forceA',fa)]:check(f'oracle_{i}_{key}',s[key],z)
 norm=max(np.linalg.norm(ra),np.linalg.norm(rb));check(f'energy_{i}',np.trace(s['rawA']+s['rawB']),0,norm)
 check(f'momentum_{i}',s['forceA'],-s['forceB'])
 check(f'heat_{i}',np.trace(s['centralA']+s['centralB']),ma*mb/(ma+mb)*na*nb*k*np.dot(ua-ub,ua-ub))
 sw=sources(mb,ma,nb,na,k,pb,pa,ub,ua);check(f'swap_{i}',s['centralA'],sw['centralB'])
 z=sources(ma,mb,na,nb,k,pa,pb);t,h,r=matrices(ma,mb,na,nb,k);p=np.array([np.trace(pa),np.trace(pb)])/3
 for j,key in enumerate(['centralA','centralB']):check(f'matrix_{i}_{j}',z[key],(t@p)[j]*np.eye(3)+h[j,0]*(pa-p[0]*np.eye(3))+h[j,1]*(pb-p[1]*np.eye(3)))
check('equal_rates',matrices(2,2,3,3,.2)[2],[.3,.6])
for ratio in [1e-8,.1,1,10,1e8]:
 t,h,r=matrices(1,ratio,3,5,.13);W=np.diag([1/3,1/5]);check('weighted_'+str(ratio),W@h,(W@h).T);assert np.linalg.eigvalsh(W@h).max()<0
 # Eigen solver subtraction loses relative accuracy of the small root; normalize to fast.
 check('eigen_'+str(ratio),r,np.sort(np.linalg.eigvals(-h)),max(r))
check('lorentz',matrices(1,1e15,3,5,.13)[1][0,0],-.65)
s=sources(2,7,3,5,.13,3*np.eye(3),5*np.eye(3));check('equilibrium',s['centralA'],0,1)
s=sources(2,7,3,5,0,np.eye(3),np.eye(3));assert all(np.count_nonzero(x)==0 for x in s.values())
for args in [(-1,2,3,4,.1),(1,2,0,4,.1),(1,2,3,4,-1),(1,2,3,4,float('nan'))]:
 try:matrices(*args);raise AssertionError('invalid accepted')
 except ValueError:pass
for bad in [np.diag([-1,1,1]),np.array([[1,1,0],[0,1,0],[0,0,1]]),np.full((3,3),np.nan)]:
 try:sources(2,7,3,5,.13,bad,np.eye(3));raise AssertionError('invalid accepted')
 except ValueError:pass
subprocess.run(['gcc','-std=c99','-O2','-Wall','-Wextra','-Werror','-fPIC','-shared','pair.c','-lm','-o','pair.so'],check=True)
f=ctypes.CDLL(str(Path('pair.so').resolve())).he35_pair;f.argtypes=[ctypes.c_double]*5+[ctypes.POINTER(ctypes.c_double)]*3
fixtures=[]
for args in [(2,7,3,5,.13),(1,1,3,3,.2),(1e-27,9e-27,1e8,2e7,3e-16),(1,1e15,3,5,.13),(2,7,3,5,0)]:
 arrays=[np.zeros(4),np.zeros(4),np.zeros(2)];ptr=[a.ctypes.data_as(ctypes.POINTER(ctypes.c_double)) for a in arrays];assert f(*args,*ptr)==0
 for j,(a,b) in enumerate(zip(arrays,matrices(*args))):check(f'C_{len(fixtures)}_{j}',a,b.ravel())
 fixtures.append({'input':args,'output':[a.tolist() for a in arrays]})
assert f(-1,2,3,4,.1,*ptr)==1
result={'status':'pass_scoped','checks':checks,'C_fixtures':fixtures,'max_normalized_error':max(checks.values())};Path('results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'pass_scoped','checks':len(checks),'max_error':max(checks.values())}))
