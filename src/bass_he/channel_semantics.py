"""Source-output channel-semantics diagnostics for the Nmax truncation.

The CPC paper simultaneously:
  * defines ionization as upper-shell population in the finite united-atom basis,
  * correlates those same united states to bound separated-atom states, and
  * exports shell-resolved capture and ionization numbers.

This module makes that overlap explicit. It does not change Eq. (50) dynamics
and it does not manufacture a disjoint physical channel partition.
"""
from __future__ import annotations

from arseny_reimpl.correlation import cordir_heh
from arseny_reimpl.eq50_scoped import ordered_scoped_branches
from arseny_reimpl.state_index import state_index


def upper_shell_correlation_rows(Nmax: int=3) -> list[dict]:
    if not isinstance(Nmax,int) or Nmax < 1:
        raise ValueError("Nmax must be a positive integer")
    rows=[]
    N=Nmax
    for l in range(N):
        for m in range(l+1):
            s=cordir_heh(N,l,m)
            rows.append({
                "j":state_index(N,l,m),
                "united":(N,l,m),
                "separated_center":s.center,
                "separated_Z":s.Z,
                "separated_n":s.n,
                "separated_n1":s.n1,
                "separated_n2":s.n2,
                "separated_m":s.m,
                "is_bound_correlation":True,
                "separated_n_equals_Nmax":bool(s.n==Nmax),
                "source_upper_shell_truncation_member":True,
            })
    return rows


def branch_destination_semantics(Nmax: int=3) -> list[dict]:
    """Compare united-Nmax membership with separated-shell correlation.

    separated_n_equals_Nmax is an Appendix-A output diagnostic, not an
    inferred replacement for the author internal CR_SECTION branch rule.
    """
    out=[]
    for b in ordered_scoped_branches():
        s=cordir_heh(*b.state_b)
        out.append({
            "branch":b.name,
            "state_b":b.state_b,
            "j_b":state_index(*b.state_b),
            "united_Nmax_member":bool(b.state_b[0]==Nmax),
            "separated_center":s.center,
            "separated_n":s.n,
            "separated_n_equals_Nmax":bool(s.n==Nmax),
            "internal_absorbing_rule_authority":"UNRESOLVED_FROM_PUBLISHED_OUTPUT_ALONE",
        })
    return out


def appendix_a_nmax3_alias_oracle() -> dict:
    """Literal Appendix-A shell/ionization equalities in cm^2."""
    rows={
        0.5:{"capture_n3":0.3285e-17,"ionization":0.3285e-17},
        5.0:{"capture_n3":0.7708e-16,"ionization":0.7708e-16},
    }
    return {
        "rows":rows,
        "exact_equalities":all(x["capture_n3"]==x["ionization"] for x in rows.values()),
        "interpretation":"SOURCE_EXPORT_ALIAS_OR_TRUNCATION_BOOKKEEPING__NOT_TWO_DISJOINT_PHYSICAL_OBSERVABLES",
    }


def require_disjoint_physical_labels(*,uses_upper_shell_as_sink: bool,
                                     also_exports_bound_correlations: bool) -> None:
    """Reject a claim that overlapping labels form a disjoint physical partition."""
    if uses_upper_shell_as_sink and also_exports_bound_correlations:
        raise ValueError(
            "upper-shell sink and bound separated correlations overlap; "
            "a disjoint physical channel partition requires additional authority"
        )

