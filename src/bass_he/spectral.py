"""Holomorphic CF derivatives and nontrivial branch-point certification.

The matching indices select continued-fraction charts, not different equations.
Duplicate spectral roots are therefore NOT branch-point evidence.
Coulomb charges, R, p and energies use the legacy paper's atomic-unit convention.
"""
from __future__ import annotations
import numpy as np
from arseny_reimpl.term_complex import continue_complex_from_real, solve_complex_term


def _coefficients(s, p, lam, R, m, Z1, Z2, radial):
    """Three coefficients and analytic derivatives ordered p, lambda, R."""
    if radial:
        a=(Z1+Z2)*R; sig=a/(2*p)-m-1
        ds=np.array([-a/(2*p*p),0,(Z1+Z2)/(2*p)],complex)
        A=(s+1)*(s+m+1)
        B=2*s*(s+2*p-sig)-(m+sig)*(m+1)-2*p*sig+lam
        C=(s-1-sig)*(s-1-m-sig)
        dA=np.zeros(3,complex)
        dB=(-2*s-m-1-2*p)*ds+np.array([4*s-2*sig,1,0],complex)
        dC=-(2*s-2-m-2*sig)*ds
    else:
        b=(Z2-Z1)*R; fac=(s+2*m+1)/(2*(s+m)+3)
        A=fac*(b-2*p*(s+m+1)); B=(s+m)*(s+m+1)-lam
        fac2=0 if s==0 else s/(2*(s+m)-1)
        C=fac2*(b+2*p*(s+m))
        dA=np.array([-2*fac*(s+m+1),0,fac*(Z2-Z1)],complex)
        dB=np.array([0,-1,0],complex)
        dC=np.array([2*fac2*(s+m),0,fac2*(Z2-Z1)],complex)
    return complex(A),complex(B),complex(C),dA,dB,dC


def _subtract_product(B, dB, A, dA, C, dC, den, dden):
    if abs(den)<1e-270: raise FloatingPointError('CF chart pole')
    ac=A*C
    return B-ac/den, dB-(dA*C+A*dC)/den+ac*dden/(den*den)


def _cf(n0, p, lam, R, m, Z1, Z2, radial, depth):
    # Coefficients are built once, avoiding repeated coefficient work in each chart.
    cs=[_coefficients(s,p,lam,R,m,Z1,Z2,radial) for s in range(depth+1)]
    low=cs[0][1]; dl=cs[0][4]
    for s in range(1,n0+1):
        Aprev=cs[s-1][0]; dAprev=cs[s-1][3]
        A,B,C,dA,dB,dC=cs[s]
        low,dl=_subtract_product(B,dB,Aprev,dAprev,C,dC,low,dl)
    high=cs[depth][1]; dh=cs[depth][4]
    for s in range(depth-1,n0,-1):
        A,B,C,dA,dB,dC=cs[s]; Cn=cs[s+1][2]; dCn=cs[s+1][5]
        high,dh=_subtract_product(B,dB,A,dA,Cn,dCn,high,dh)
    A=cs[n0][0];dA=cs[n0][3];Cn=cs[n0+1][2];dCn=cs[n0+1][5]
    return _subtract_product(low,dl,A,dA,Cn,dCn,high,dh)


def spectral_system(state,R,p,lam,*,Z1=1.,Z2=2.,depth=96):
    N,l,m=state
    if not(1<=N and 0<=m<=l<N) or depth<=max(N-l-1,l-m)+4:
        raise ValueError('invalid state or continued-fraction depth')
    if Z1==Z2: raise NotImplementedError('asymmetric recurrence only')
    if not all(np.isfinite(x) for x in [p,lam,R,Z1,Z2]) or abs(p)==0 or abs(R)==0:
        raise ValueError('finite nonzero p and R required')
    r,dr=_cf(N-l-1,complex(p),complex(lam),complex(R),m,Z1,Z2,True,depth)
    a,da=_cf(l-m,complex(p),complex(lam),complex(R),m,Z1,Z2,False,depth)
    return np.array([r,a]),np.array([dr,da])


def spectral_certificate(state,R,p,lam,*,depth=96,Z1=1.,Z2=2.,rank_tol=1e-7):
    F,J=spectral_system(state,R,p,lam,depth=depth,Z1=Z1,Z2=Z2)
    u,s,vh=np.linalg.svd(J[:,:2]); ratio=float(s[-1]/s[0]); res=float(max(abs(F)))
    # A fold also needs nonzero left-null projections on F_R and F_zz[v,v].
    direction=vh.conj().T[:,-1]; left=u[:,-1].conj()
    h=2e-4; z=np.array([p,lam],complex)
    fp=spectral_system(state,R,*(z+h*direction),depth=depth,Z1=Z1,Z2=Z2)[0]
    fm=spectral_system(state,R,*(z-h*direction),depth=depth,Z1=Z1,Z2=Z2)[0]
    curvature=left@((fp-2*F+fm)/(h*h)); trans=left@J[:,2]
    return dict(residual=res,sigma_min_over_max=ratio,
                singular=bool(res<1e-8 and ratio<rank_tol),
                transversality=complex(trans),curvature=complex(curvature),
                simple_fold=bool(res<1e-8 and ratio<rank_tol and abs(trans)>1e-7 and abs(curvature)>1e-7))


def find_exceptional_point(state_a,state_b,R_seed,*,depth=96,Z1=1.,Z2=2.,tol=2e-11):
    if state_a[2]!=state_b[2]: raise ValueError('different m cannot coalesce in this model')
    # Nearby independently continued sheets give a seed, never a certificate.
    Rs=complex(R_seed); near=complex(Rs.real,.9*Rs.imag)
    a=continue_complex_from_real(state_a,near,depth=depth,tol=1e-10,Z1=Z1,Z2=Z2)
    b=continue_complex_from_real(state_b,near,depth=depth,tol=1e-10,Z1=Z1,Z2=Z2)
    z=np.array([(a.p+b.p)/2,(a.separation_lambda+b.separation_lambda)/2,Rs],complex)
    F,J=spectral_system(state_a,z[2],z[0],z[1],depth=depth,Z1=Z1,Z2=Z2)
    scale=np.array([max(1,abs(F[0])),max(1,abs(F[1])),max(1,np.linalg.norm(J[:,:2])**2)])
    def fun(x):
        f,j=spectral_system(state_a,x[2],x[0],x[1],depth=depth,Z1=Z1,Z2=Z2)
        return np.array([f[0],f[1],np.linalg.det(j[:,:2])])/scale
    for it in range(35):
        f=fun(z)
        if max(abs(f))<tol:break
        jac=np.empty((3,3),complex)
        for k in range(3):
            h=2e-6*max(1,abs(z[k])); e=np.zeros(3,complex);e[k]=h
            jac[:,k]=(fun(z+e)-fun(z-e))/(2*h)
        dz=np.linalg.solve(jac,-f)
        for n in range(24):
            candidate=z+2.**(-n)*dz
            try:fn=fun(candidate)
            except (ValueError,FloatingPointError):continue
            if max(abs(fn))<max(abs(f)):z=candidate;break
        else:raise RuntimeError('discriminant Newton failed to improve')
    else:raise RuntimeError('discriminant Newton iteration budget exhausted')
    cert=spectral_certificate(state_a,z[2],z[0],z[1],depth=depth,Z1=Z1,Z2=Z2)
    if not cert['simple_fold']:raise RuntimeError(f'branch candidate not a simple fold: {cert}')
    return dict(state_a=tuple(state_a),state_b=tuple(state_b),R=z[2],p=z[0],lam=z[1],
                depth=int(depth),Z1=Z1,Z2=Z2,certificate=cert,iterations=it+1,
                status='SPECTRAL_SIMPLE_FOLD_NOT_YET_MONODROMY_CHECKED')


def monodromy(ep,*,radius=.01,steps=96):
    """One loop must swap and two loops restore distinct local sheets."""
    if radius<=0 or steps<24:raise ValueError('positive radius and >=24 steps required')
    state=ep['state_a']; center=ep['R'];depth=ep['depth'];Z1=ep['Z1'];Z2=ep['Z2']
    zc=np.array([ep['p'],ep['lam']],complex)
    _,J=spectral_system(state,center,*zc,depth=depth,Z1=Z1,Z2=Z2)
    u,s,vh=np.linalg.svd(J[:,:2]); null=vh.conj().T[:,-1];left=u[:,-1].conj()
    h=2e-4
    F=spectral_system(state,center,*zc,depth=depth,Z1=Z1,Z2=Z2)[0]
    fp=spectral_system(state,center,*(zc+h*null),depth=depth,Z1=Z1,Z2=Z2)[0]
    fm=spectral_system(state,center,*(zc-h*null),depth=depth,Z1=Z1,Z2=Z2)[0]
    curvature=left@((fp-2*F+fm)/h**2);trans=left@J[:,2]
    amp=np.sqrt(-2*trans*radius/curvature)
    def solve(R,z):
        p=solve_complex_term(state,R,p0=z[0],lam0=z[1],depth=depth,tol=2e-12,Z1=Z1,Z2=Z2)
        return np.array([p.p,p.separation_lambda])
    za=solve(center+radius,zc+amp*null);zb=solve(center+radius,zc-amp*null)
    a0=za.copy();b0=zb.copy();gap0=float(np.linalg.norm(a0-b0));mingap=gap0
    if gap0<1e-6:raise RuntimeError('monodromy starts on duplicate sheets')
    swap=None
    for k in range(1,2*steps+1):
        R=center+radius*np.exp(2j*np.pi*k/steps)
        za=solve(R,za);zb=solve(R,zb)
        mingap=min(mingap,float(np.linalg.norm(za-zb)))
        if k==steps:swap=float(max(np.linalg.norm(za-b0),np.linalg.norm(zb-a0))/gap0)
    ret=float(max(np.linalg.norm(za-a0),np.linalg.norm(zb-b0))/gap0)
    return dict(one_loop_swap_relative_error=swap,two_loop_return_relative_error=ret,
                minimum_distinct_sheet_gap=mingap,radius=radius,steps_per_loop=steps,
                passed=bool(swap<2e-6 and ret<2e-6 and mingap>1e-6))
