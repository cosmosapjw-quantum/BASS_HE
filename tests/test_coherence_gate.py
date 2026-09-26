import math
import numpy as np
import pytest

from bass_he.coherence import (
    markov_double_pass_probability,
    coherent_double_pass_probability,
    phase_averaged_double_pass_probability,
    coherent_double_pass_envelope,
    phase_uncertainty_report,
)


def test_markov_double_pass_matches_two_population_matrices():
    for p in (0.0, 1e-6, 0.1, 0.5, 0.9, 1.0):
        M=np.array([[1-p,p],[p,1-p]],float)
        got=(M@M)[1,0]
        assert got == pytest.approx(markov_double_pass_probability(p),abs=1e-15)


def test_coherent_double_pass_has_expected_envelope():
    p=0.24
    lo,hi=coherent_double_pass_envelope(p)
    assert lo == 0.0
    assert hi == pytest.approx(4*p*(1-p))
    assert coherent_double_pass_probability(p,0.0) == pytest.approx(lo)
    assert coherent_double_pass_probability(p,math.pi/2) == pytest.approx(hi)


def test_uniform_phase_average_equals_markov_double_pass():
    for p in (1e-7,0.01,0.24,0.5,0.91):
        assert phase_averaged_double_pass_probability(p) == pytest.approx(
            markov_double_pass_probability(p),rel=2e-15,abs=2e-15)


def test_phase_uncertainty_is_order_unity_relative_to_markov_mean():
    r=phase_uncertainty_report(0.24)
    assert r['phase_average'] == pytest.approx(r['markov_double_pass'])
    assert r['coherent_min'] == 0.0
    assert r['coherent_max'] == pytest.approx(2*r['markov_double_pass'])
    assert r['relative_half_width_about_markov'] == pytest.approx(1.0)


def test_probability_validation_is_strict():
    with pytest.raises(ValueError): markov_double_pass_probability(-1e-3)
    with pytest.raises(ValueError): coherent_double_pass_probability(1.001,0.2)
    with pytest.raises(ValueError): coherent_double_pass_probability(0.5,float('nan'))
