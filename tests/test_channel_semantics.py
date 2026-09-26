import pytest

from bass_he.channel_semantics import (
    upper_shell_correlation_rows,
    branch_destination_semantics,
    appendix_a_nmax3_alias_oracle,
    require_disjoint_physical_labels,
)


def test_nmax3_united_upper_shell_correlates_entirely_to_bound_separated_states():
    rows=upper_shell_correlation_rows(3)
    assert len(rows)==6
    assert all(r["is_bound_correlation"] for r in rows)
    assert all(r["separated_center"]=="Z2" for r in rows)
    assert sorted(r["separated_n"] for r in rows)==[2,3,3,3,3,3]


def test_q23_destination_is_united_upper_shell_but_separated_n2():
    rows={r["branch"]:r for r in branch_destination_semantics(3)}
    q23=rows["Q23"]
    assert q23["united_Nmax_member"] is True
    assert q23["separated_n"]==2
    assert q23["separated_n_equals_Nmax"] is False
    for name in ("S23","Qother","Qm1"):
        assert rows[name]["united_Nmax_member"] is True
        assert rows[name]["separated_n"]==3
        assert rows[name]["separated_n_equals_Nmax"] is True


def test_appendix_a_reports_n3_capture_equal_to_ionization_at_both_energies():
    o=appendix_a_nmax3_alias_oracle()
    assert o["exact_equalities"] is True
    assert o["rows"][0.5]["capture_n3"]==o["rows"][0.5]["ionization"]
    assert o["rows"][5.0]["capture_n3"]==o["rows"][5.0]["ionization"]


def test_overlapping_source_labels_cannot_be_promoted_as_disjoint_physical_channels():
    with pytest.raises(ValueError,match="overlap"):
        require_disjoint_physical_labels(
            uses_upper_shell_as_sink=True,
            also_exports_bound_correlations=True,
        )
    require_disjoint_physical_labels(
        uses_upper_shell_as_sink=False,
        also_exports_bound_correlations=True,
    )

