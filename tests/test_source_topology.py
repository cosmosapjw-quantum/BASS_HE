import math
import numpy as np
import pytest

from bass_he.coherence import (
    janev1997_eq15_probability,
    janev1997_eq15_phase_average,
)
from bass_he.transport import apply_eq50
from arseny_reimpl.eq50_scoped import ordered_scoped_branches, branch_state_indices
from arseny_reimpl.state_index import state_index


def _current_sparse_channel(p12,p23,p_s,p_rot,p_other,p_m1,back):
    branches=ordered_scoped_branches()
    pmap={'Q12':p12,'Q23':p23,'S23':p_s,'Qother':p_other,'Qm1':p_m1}
    probs=np.array([[pmap[b.name] for b in branches]],float)
    events=[]
    for b in branches:
        i,j=branch_state_indices(b)
        events.append((i-1,j-1,b.state_b[0]==3))
    dim=state_index(3,2,2)
    prot=np.eye(dim,dtype=float)
    sig=state_index(2,1,0)-1
    pi=state_index(2,1,1)-1
    # Only the sigma input column enters the published Eq.(15) channel.
    # The reverse pi column is left arbitrary but column-stochastic.
    prot[sig,sig]=1-p_rot
    prot[pi,sig]=p_rot
    prot[sig,pi]=back
    prot[pi,pi]=1-back
    initial=np.eye(dim)[:,[sig]]
    out=apply_eq50(probs,events,prot[None,:,:],initial)
    final_1ssigma=state_index(1,0,0)-1
    return float(out[0,final_1ssigma,0])


def test_janev1997_eq15_uniform_phase_average_is_analytic():
    x,w=np.polynomial.legendre.leggauss(64)
    phases=(x+1)*math.pi
    for p12,p23,p_s,p_rot in ((.2,.3,.4,.5),(.91,.02,.15,.73),(.01,.8,.95,.1)):
        vals=np.array([
            janev1997_eq15_probability(p12,p23,p_s,p_rot,phi,0.0)
            for phi in phases
        ])
        avg=float(np.dot(w,vals)/2)
        assert avg == pytest.approx(
            janev1997_eq15_phase_average(p12,p23,p_s,p_rot),
            rel=3e-14,abs=3e-14)


def test_current_sparse_eq50_matches_source_phase_average_for_generic_probabilities():
    rng=np.random.default_rng(20260927)
    for _ in range(256):
        p12,p23,p_s,p_rot,p_other,p_m1,back=rng.random(7)
        got=_current_sparse_channel(p12,p23,p_s,p_rot,p_other,p_m1,back)
        want=janev1997_eq15_phase_average(p12,p23,p_s,p_rot)
        assert got == pytest.approx(want,rel=5e-14,abs=5e-14)


def test_source_channel_is_independent_of_qother_qm1_and_reverse_pi_column():
    fixed=(.37,.29,.41,.63)
    reference=_current_sparse_channel(*fixed,.11,.17,.23)
    for p_other,p_m1,back in ((0,0,0),(1,1,1),(.8,.1,.9),(.2,.9,.05)):
        got=_current_sparse_channel(*fixed,p_other,p_m1,back)
        assert got == pytest.approx(reference,abs=2e-15)


def test_janev1997_eq15_probability_validation_is_strict():
    with pytest.raises(ValueError): janev1997_eq15_probability(-.1,.2,.3,.4,0,0)
    with pytest.raises(ValueError): janev1997_eq15_probability(.1,.2,.3,.4,float('nan'),0)



def _current_forward_outputs(p12,p23,p_s,p_rot,p_other,p_m1,back,*,q23_absorbing=True):
    branches=ordered_scoped_branches()
    pmap={'Q12':p12,'Q23':p23,'S23':p_s,'Qother':p_other,'Qm1':p_m1}
    probs=np.array([[pmap[b.name] for b in branches]],float)
    events=[]
    for b in branches:
        i,j=branch_state_indices(b)
        sink=(b.state_b[0]==3)
        if b.name=='Q23' and not q23_absorbing:
            sink=False
        events.append((i-1,j-1,sink))
    dim=state_index(3,2,2)
    prot=np.eye(dim,dtype=float)
    sig=state_index(2,1,0)-1
    pi=state_index(2,1,1)-1
    prot[sig,sig]=1-p_rot
    prot[pi,sig]=p_rot
    prot[sig,pi]=back
    prot[pi,pi]=1-back
    initial=np.eye(dim)[:,[sig]]
    out=apply_eq50(probs,events,prot[None,:,:],initial)[0,:,0]
    return out


def test_janev1997_eq14_matches_current_sparse_forward_channel():
    from bass_he.coherence import janev1997_eq14_2ppi_probability
    rng=np.random.default_rng(20260928)
    j2ppi=state_index(2,1,1)-1
    for _ in range(256):
        p12,p23,p_s,p_rot,p_other,p_m1,back=rng.random(7)
        out=_current_forward_outputs(p12,p23,p_s,p_rot,p_other,p_m1,back)
        want=janev1997_eq14_2ppi_probability(p23,p12,p_s,p_m1,p_rot)
        assert out[j2ppi] == pytest.approx(want,rel=5e-14,abs=5e-14)


def test_eq13_absorbing_mismatch_has_exact_two_term_decomposition():
    from bass_he.coherence import janev1997_eq13_phase_average_nmax3_projection
    rng=np.random.default_rng(20260929)
    j3dsigma=state_index(3,2,0)-1
    for _ in range(256):
        p12,p23,p_s,p_rot,p_other,p_m1,back=rng.random(7)
        out=_current_forward_outputs(p12,p23,p_s,p_rot,p_other,p_m1,back)
        src=janev1997_eq13_phase_average_nmax3_projection(p23,p12,p_s,p_rot)
        s=math.sqrt(1-p_rot)
        lost_same_phase=2*p23*(1-p23)*p12*(1-p12)*(1-p_s)*s
        absorbing_bias=p23*p23
        assert out[j3dsigma]-src == pytest.approx(
            absorbing_bias-lost_same_phase,rel=8e-14,abs=8e-14)


def test_reversible_q23_isolates_missing_same_phase_cross_term():
    from bass_he.coherence import janev1997_eq13_phase_average_nmax3_projection
    rng=np.random.default_rng(20260930)
    j3dsigma=state_index(3,2,0)-1
    for _ in range(128):
        p12,p23,p_s,p_rot,p_other,p_m1,back=rng.random(7)
        out=_current_forward_outputs(
            p12,p23,p_s,p_rot,p_other,p_m1,back,q23_absorbing=False)
        src=janev1997_eq13_phase_average_nmax3_projection(p23,p12,p_s,p_rot)
        lost=2*p23*(1-p23)*p12*(1-p12)*(1-p_s)*math.sqrt(1-p_rot)
        assert out[j3dsigma]-src == pytest.approx(-lost,rel=8e-14,abs=8e-14)
