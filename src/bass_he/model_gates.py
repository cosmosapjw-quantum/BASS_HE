"""Source-derived diagnostics for physical/model gates.

These helpers do not modify the collision dynamics. They expose bounded
diagnostics used by the AUDIT3 research loop.
"""
from __future__ import annotations
import math
from arseny_reimpl.rotational import s_sigma_boundary

_RMIN_100_EVU_A0 = {"H": 0.65, "D": 0.40, "T": 0.30}


def source_headon_rmin_a0(energy_eV_per_amu: float, isotope: str = "H") -> float:
    """Source-anchored head-on closest-approach diagnostic in a0.

    Stolterfoht et al. quote Rmin~0.65,0.40,0.30 a0 for H,D,T at
    100 eV/u. Their Eq.(3) gives inverse-energy scaling for a fixed isotope.
    This is not a realistic trajectory integrator.
    """
    E=float(energy_eV_per_amu)
    if not math.isfinite(E) or E <= 0:
        raise ValueError("positive finite energy required")
    try:
        r100=_RMIN_100_EVU_A0[str(isotope)]
    except KeyError as exc:
        raise ValueError("isotope must be H, D, or T") from exc
    return r100*100.0/E


def rotation_access_ratio(energy_eV_per_amu: float, isotope: str, l: int) -> float:
    """Rmin(source diagnostic) / inherited clean-room S_l0 matching radius."""
    if not isinstance(l,int) or l < 1:
        raise ValueError("l must be an integer >=1")
    return source_headon_rmin_a0(energy_eV_per_amu,isotope)/s_sigma_boundary(l)


def critical_energy_for_matching_radius_eVu(isotope: str, l: int) -> float:
    """Energy where source-anchored head-on Rmin equals inherited S_l0 radius.

    This is a diagnostic threshold only, not a trajectory validity theorem.
    """
    if not isinstance(l,int) or l < 1:
        raise ValueError("l must be an integer >=1")
    try:
        r100=_RMIN_100_EVU_A0[str(isotope)]
    except KeyError as exc:
        raise ValueError("isotope must be H, D, or T") from exc
    return 100.0*r100/s_sigma_boundary(l)


def source_coupling_regime(energy_eV_per_amu: float) -> str:
    """Encode only qualitative energy boundaries stated in Stolterfoht 2010."""
    E=float(energy_eV_per_amu)
    if not math.isfinite(E) or E <= 0:
        raise ValueError("positive finite energy required")
    if E > 500.0:
        return "RADIAL_DOMINANT_ABOVE_500_EVU_SOURCE_DISCUSSION"
    if E >= 40.0:
        return "ROTATIONAL_RISING_40_TO_500_EVU_SOURCE_DISCUSSION"
    return "BELOW_40_EVU_RADIAL_REGAINS_SOURCE_DISCUSSION"


def paper_eq52_probability(delta: float, velocity: float) -> float:
    """Literal printed Eq.(52) compatibility lane: exp(-Delta/v)."""
    d=float(delta);v=float(velocity)
    if not math.isfinite(d) or d < 0 or not math.isfinite(v) or v <= 0:
        raise ValueError("require finite delta>=0 and velocity>0")
    return math.exp(-d/v)


def semiclassical_action_probability(delta: float, velocity: float) -> float:
    """Probability from |exp(i S/v)|^2 when Im(S)=Delta>=0."""
    d=float(delta);v=float(velocity)
    if not math.isfinite(d) or d < 0 or not math.isfinite(v) or v <= 0:
        raise ValueError("require finite delta>=0 and velocity>0")
    return math.exp(-2.0*d/v)


def upper_shell_absorbing_diagnostics(Nmax: int = 3) -> list[dict]:
    """Expose truncation-sink semantics beside separated-atom labels."""
    if not isinstance(Nmax,int) or Nmax < 1:
        raise ValueError("Nmax must be a positive integer")
    from arseny_reimpl.eq50_scoped import ordered_scoped_branches
    from arseny_reimpl.correlation import cordir_heh
    rows=[]
    for b in ordered_scoped_branches():
        sep=cordir_heh(*b.state_b)
        rows.append({
            "branch":b.name,"state_b":b.state_b,
            "absorbing_upper_shell":bool(b.state_b[0] == Nmax),
            "separated_center":sep.center,"separated_Z":sep.Z,"separated_n":sep.n,
            "separated_n1":sep.n1,"separated_n2":sep.n2,"separated_m":sep.m,
            "claim":"SOURCE_TRUNCATION_DIAGNOSTIC_NOT_DISJOINT_PHYSICAL_CHANNEL_ASSIGNMENT",
        })
    return rows
