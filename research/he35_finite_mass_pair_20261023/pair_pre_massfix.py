"""Exact homogeneous isotropic Maxwell binary moments; SI, proper seconds.
κ is supplied in m³/s. No rate data or closure fit is included.
PSD roundoff: eigenvalues >= -64 eps * spectral scale are accepted, never clipped.
"""
import numpy as np

def matrices(mA,mB,nA,nB,kappa):
    z=np.array([mA,mB,nA,nB,kappa],float)
    if not np.isfinite(z).all() or min(z[:4])<=0 or kappa<0:
        raise ValueError('finite positive masses/densities and nonnegative kappa required')
    if kappa == 0: return np.zeros((2,2)),np.zeros((2,2)),np.zeros(2)
    # Ratios avoid overflow in the mass sum.
    scale=max(mA,mB); a=(mA/scale)/(mA/scale+mB/scale); b=(mB/scale)/(mA/scale+mB/scale)
    thermal=2*a*b*kappa*np.array([[-nB,nA],[nB,-nA]])
    stf=kappa*np.array([[-nB*b*(2*a+b),nA*a*b],[nB*a*b,-nA*a*(2*b+a)]])
    # Stable nonnegative roots of -STF: determinant / fast root for slow.
    x=nB*b*(2*a+b); y=nA*a*(2*b+a)
    fast=.5*(x+y+np.hypot(x-y,2*a*b*np.sqrt(nA)*np.sqrt(nB)))
    det=2*nA*nB*a*b # exact simplified determinant
    slow=det/fast if fast else 0.
    rates=kappa*np.array([slow,fast])
    if not all(np.isfinite(v).all() for v in (thermal,stf,rates)):
        raise ValueError('unrepresentable output')
    return thermal,stf,rates

def pressure(P):
    P=np.asarray(P,float)
    if P.shape!=(3,3) or not np.isfinite(P).all(): raise ValueError('finite 3x3 tensor required')
    scale=np.max(np.abs(P))
    tol=64*np.finfo(float).eps*scale
    if np.max(np.abs(P-P.T))>tol or np.linalg.eigvalsh(P).min() < -tol:
        raise ValueError('symmetric PSD tensor required')
    return P

def sources(mA,mB,nA,nB,kappa,PA,PB,uA=None,uB=None):
    matrices(mA,mB,nA,nB,kappa)
    PA,PB=pressure(PA),pressure(PB)
    uA=np.zeros(3) if uA is None else np.asarray(uA,float)
    uB=np.zeros(3) if uB is None else np.asarray(uB,float)
    if uA.shape!=(3,) or uB.shape!=(3,) or not np.isfinite([uA,uB]).all(): raise ValueError('finite velocities required')
    if kappa == 0:
        return {key:np.zeros((3,3) if key.startswith(("raw","central")) else 3) for key in ("rawA","rawB","forceA","forceB","centralA","centralB")}
    scale=max(mA,mB); a=(mA/scale)/(mA/scale+mB/scale); b=1-a
    SA=PA/(mA*nA)+np.outer(uA,uA); SB=PB/(mB*nB)+np.outer(uB,uB)
    X=np.outer(uA,uB)+np.outer(uB,uA); G=SA+SB-X
    H=2*a*SA-2*b*SB+(b-a)*X; D=np.trace(G)*np.eye(3)/3-G
    RA=mA*nA*nB*kappa*(-b*H+b*b*D)
    RB=mB*nA*nB*kappa*(a*H+a*a*D)
    FA=-(mA*b)*nA*nB*kappa*(uA-uB); FB=-FA
    CA=RA-np.outer(uA,FA)-np.outer(FA,uA)
    CB=RB-np.outer(uB,FB)-np.outer(FB,uB)
    return dict(rawA=RA,rawB=RB,forceA=FA,forceB=FB,centralA=CA,centralB=CB)
