import math
import pytest

from bass_he.model_gates import (
    source_headon_rmin_a0, rotation_access_ratio,
    semiclassical_action_probability, paper_eq52_probability,
    source_coupling_regime, critical_energy_for_matching_radius_eVu,
)


def test_source_headon_rmin_recovers_published_100_evu_anchors_and_inverse_energy_scaling():
    assert source_headon_rmin_a0(100.0,'H') == pytest.approx(0.65)
    assert source_headon_rmin_a0(100.0,'D') == pytest.approx(0.40)
    assert source_headon_rmin_a0(100.0,'T') == pytest.approx(0.30)
    assert source_headon_rmin_a0(500.0,'H') == pytest.approx(0.13)
    assert source_headon_rmin_a0(50.0,'H') == pytest.approx(1.30)


def test_rotation_access_ratio_is_diagnostic_not_boolean_gate():
    assert rotation_access_ratio(100.0,'H',1) == pytest.approx(0.65/(7/12))
    assert rotation_access_ratio(500.0,'H',1) == pytest.approx(0.13/(7/12))


def test_source_coupling_regime_uses_published_boundaries_without_inventing_precision():
    assert source_coupling_regime(1000.0) == 'RADIAL_DOMINANT_ABOVE_500_EVU_SOURCE_DISCUSSION'
    assert source_coupling_regime(500.0) == 'ROTATIONAL_RISING_40_TO_500_EVU_SOURCE_DISCUSSION'
    assert source_coupling_regime(100.0) == 'ROTATIONAL_RISING_40_TO_500_EVU_SOURCE_DISCUSSION'
    assert source_coupling_regime(30.0) == 'BELOW_40_EVU_RADIAL_REGAINS_SOURCE_DISCUSSION'


def test_action_probability_carries_factor_two_from_amplitude_modulus_square():
    delta=0.37; v=0.21
    p52=paper_eq52_probability(delta,v)
    p_action=semiclassical_action_probability(delta,v)
    assert p_action == pytest.approx(p52*p52, rel=2e-15)
    assert p_action == pytest.approx(math.exp(-2*delta/v))


def test_model_gate_inputs_are_strict():
    with pytest.raises(ValueError): source_headon_rmin_a0(0,'H')
    with pytest.raises(ValueError): source_headon_rmin_a0(100,'X')
    with pytest.raises(ValueError): rotation_access_ratio(100,'H',0)
    with pytest.raises(ValueError): semiclassical_action_probability(-1,1)
    with pytest.raises(ValueError): paper_eq52_probability(1,0)


def test_upper_shell_absorbing_diagnostic_exposes_bound_separated_correlation():
    from bass_he.model_gates import upper_shell_absorbing_diagnostics
    rows={x['branch']:x for x in upper_shell_absorbing_diagnostics(3)}
    assert rows['Q23']['absorbing_upper_shell'] is True
    assert rows['Q23']['separated_center'] == 'Z2'
    assert rows['Q23']['separated_n'] == 2
    assert rows['Q12']['absorbing_upper_shell'] is False
    assert rows['Q12']['separated_center'] == 'Z1'
    assert rows['Q12']['separated_n'] == 1


def test_source_anchor_implies_energy_threshold_for_inherited_matching_radius():
    assert critical_energy_for_matching_radius_eVu('H',1) == pytest.approx(111.42857142857143)
    assert critical_energy_for_matching_radius_eVu('D',1) == pytest.approx(68.57142857142857)
    assert critical_energy_for_matching_radius_eVu('T',1) == pytest.approx(51.42857142857143)
    assert critical_energy_for_matching_radius_eVu('H',2) == pytest.approx(33.91304347826087)
