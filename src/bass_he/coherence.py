"""Minimal coherence diagnostics for an isolated symmetric double passage.

These helpers do not upgrade the scoped Eq. (50) Markov transport into a
coherent multi-channel solver. They only quantify what is lost when one
crossing with single-pass probability p is traversed twice and the relative
phase is discarded. The phase argument absorbs dynamical and Stokes contributions.
"""
from __future__ import annotations
import math


def _p(x: float) -> float:
    p=float(x)
    if not math.isfinite(p) or not (0.0 <= p <= 1.0):
        raise ValueError("probability must be finite and in [0,1]")
    return p


def markov_double_pass_probability(p: float) -> float:
    """Off-diagonal population after two identical incoherent passages."""
    p=_p(p)
    return 2.0*p*(1.0-p)


def coherent_double_pass_probability(p: float, phase: float) -> float:
    """Two-path coherent envelope, 4 p(1-p) sin^2(total phase)."""
    p=_p(p);phi=float(phase)
    if not math.isfinite(phi):
        raise ValueError("phase must be finite")
    return 4.0*p*(1.0-p)*math.sin(phi)**2


def phase_averaged_double_pass_probability(p: float) -> float:
    """Uniform total-phase average of the coherent double-passage formula."""
    return markov_double_pass_probability(p)


def coherent_double_pass_envelope(p: float) -> tuple[float,float]:
    """Minimum/maximum coherent double-passage probability over phase."""
    p=_p(p)
    return 0.0,4.0*p*(1.0-p)


def phase_uncertainty_report(p: float) -> dict:
    """Bounded isolated-crossing phase-ignorance diagnostic.

    For a nontrivial passage the coherent probability ranges from zero to twice
    the phase-averaged/Markov result. The relative half-width about that mean is
    therefore unity. This statement must not be promoted to a five-branch
    network uncertainty without coherent S matrices and inter-branch phases.
    """
    p=_p(p);mean=markov_double_pass_probability(p);lo,hi=coherent_double_pass_envelope(p)
    rel=0.0 if mean==0.0 else (hi-lo)/(2.0*mean)
    return {
        "single_pass_probability":p,
        "markov_double_pass":mean,
        "phase_average":mean,
        "coherent_min":lo,
        "coherent_max":hi,
        "relative_half_width_about_markov":rel,
        "scope":"ISOLATED_SYMMETRIC_DOUBLE_PASS_ONLY_NOT_FULL_EQ50_NETWORK",
    }



def adiabatic_topological_phase() -> float:
    """Square-root hidden-crossing topological phase in the v->0 limit.

    Janev, Pop-Jordanov & Solov'ev (J. Phys. B 30, L353, 1997) give gamma=pi/2
    for a square-root branching point in the adiabatic limit.
    """
    return math.pi/2.0


def hidden_crossing_two_pass_probability(p: float, dynamical_phase: float, topological_phase: float | None = None) -> float:
    """Source-aligned two-pass hidden-crossing interference probability.

    P=4 p(1-p) cos^2(chi+gamma), with gamma=pi/2 by default in the
    adiabatic limit. This is still an isolated two-state formula, not the
    complete multi-branch ARSENY evolution matrix.
    """
    p=_p(p);chi=float(dynamical_phase)
    gamma=adiabatic_topological_phase() if topological_phase is None else float(topological_phase)
    if not math.isfinite(chi) or not math.isfinite(gamma):
        raise ValueError("phases must be finite")
    return 4.0*p*(1.0-p)*math.cos(chi+gamma)**2



def janev1997_eq15_probability(p12: float, p23: float, p_s: float,
                               p_rot: float, chi1: float, chi2: float,
                               *, gamma: float=math.pi/2) -> float:
    """Janev-Pop-Jordanov-Solov'ev 1997 Eq. (15).

    This is the inverse-reaction two-path 1s-sigma/2p-sigma channel formula:
      p12(1-p12)(1-p23) |exp[i(chi1+gamma)]
        +(1-p_s)sqrt(1-p_rot)exp[i(chi2-gamma)]|^2.

    The function reproduces the published coherent topology but does not
    construct chi1/chi2.  Complete reaction-path phase authority remains the
    separate DR10B gate.
    """
    p12=_p(p12);p23=_p(p23);p_s=_p(p_s);p_rot=_p(p_rot)
    c1=float(chi1);c2=float(chi2);g=float(gamma)
    if not all(math.isfinite(x) for x in (c1,c2,g)):
        raise ValueError("phases must be finite")
    a1=complex(math.cos(c1+g),math.sin(c1+g))
    amp=(1.0-p_s)*math.sqrt(1.0-p_rot)
    a2=amp*complex(math.cos(c2-g),math.sin(c2-g))
    return p12*(1.0-p12)*(1.0-p23)*abs(a1+a2)**2


def janev1997_eq15_phase_average(p12: float, p23: float,
                                  p_s: float, p_rot: float) -> float:
    """Uniform relative-phase average of Janev et al. 1997 Eq. (15).

    The exact average is
      p12(1-p12)(1-p23) [1+(1-p_s)^2(1-p_rot)].
    """
    p12=_p(p12);p23=_p(p23);p_s=_p(p_s);p_rot=_p(p_rot)
    return p12*(1.0-p12)*(1.0-p23)*(1.0+(1.0-p_s)**2*(1.0-p_rot))



def janev1997_eq13_phase_average_nmax3_projection(
    p23: float, p12: float, p_s23: float, p_rot2: float
) -> float:
    """Uniform-phase average of 1997 Eq. (13) under an explicit Nmax=3 projection.

    Higher N=4 couplings from 3d-sigma (Q 3d->4f, S 3d->4d and the associated
    higher-shell rotational loss) are frozen to zero transition probability.
    This is a diagnostic projection of the published formula, not the full
    Janev-1997 forward-channel result.
    """
    p23=_p(p23);p12=_p(p12);p_s23=_p(p_s23);p_rot2=_p(p_rot2)
    surviving_inner=(1.0-p12)*(1.0-p_s23)*math.sqrt(1.0-p_rot2)
    first_path=p12+surviving_inner
    return p23*(1.0-p23)*(1.0+first_path*first_path)


def janev1997_eq14_2ppi_probability(
    p23: float, p12: float, p_s23: float, p_pi3dpi: float, p_rot2: float
) -> float:
    """Janev et al. 1997 Eq. (14) for the 2p-pi final channel."""
    p23=_p(p23);p12=_p(p12);p_s23=_p(p_s23);p_pi3dpi=_p(p_pi3dpi);p_rot2=_p(p_rot2)
    return (1.0-p23)*(1.0-p12)*(1.0-p_s23)*(1.0-p_pi3dpi)*p_rot2
