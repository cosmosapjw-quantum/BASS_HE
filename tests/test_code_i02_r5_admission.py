"""CODE-I02 R5 admission attacks and exact cache identity controls."""
import copy
import json
import math

import numpy as np
import pytest

from bass_he import spectral
from bass_he.sturm_geometry import contour_geometry


SEED = 1.2125718090356707 + 1.363814370435508j


@pytest.fixture(scope="module")
def ep():
    return spectral.find_exceptional_point((1, 0, 0), (2, 1, 0), SEED, depth=64)


def _before_anchor(monkeypatch, candidate):
    def reached(*args, **kwargs):
        pytest.fail("invalid certificate reached first anchor")

    monkeypatch.setattr("bass_he.sturm_geometry.bound_pair", reached)
    with pytest.raises(ValueError):
        contour_geometry(candidate, 0.0, panels=8)


@pytest.mark.parametrize("value", [float("nan"), -float("inf"), -0.001, "nan", "0.0"])
def test_matching_error_must_be_strict_finite_nonnegative(ep, monkeypatch, value):
    candidate = copy.deepcopy(ep)
    candidate["pair_membership"]["max_scaled_matching_error"] = value
    _before_anchor(monkeypatch, candidate)


@pytest.mark.parametrize("field,value", [
    ("state_a", [True, 0, 0]), ("state_a", [1.0, 0, 0]),
    ("depth", 64.0),
])
def test_stored_binding_keeps_json_type_identity(ep, monkeypatch, field, value):
    candidate = copy.deepcopy(ep)
    candidate["pair_membership"]["binding"][field] = value
    _before_anchor(monkeypatch, candidate)


@pytest.mark.parametrize("value", ["False", "0", 1, np.bool_(True)])
def test_passed_must_be_python_bool(ep, monkeypatch, value):
    candidate = copy.deepcopy(ep)
    candidate["pair_membership"]["passed"] = value
    _before_anchor(monkeypatch, candidate)


@pytest.mark.parametrize("value", ["False", 1, np.bool_(True)])
def test_stored_simple_fold_is_strict(ep, monkeypatch, value):
    candidate = copy.deepcopy(ep)
    candidate["certificate"]["simple_fold"] = value
    _before_anchor(monkeypatch, candidate)


@pytest.mark.parametrize("field", ["tolerance", "probe_scale"])
def test_policy_scalars_reject_numeric_strings(ep, monkeypatch, field):
    candidate = copy.deepcopy(ep)
    candidate["pair_membership"][field] = str(candidate["pair_membership"][field])
    _before_anchor(monkeypatch, candidate)


@pytest.mark.parametrize("field", ["tolerance", "probe_scale"])
def test_rehashed_caller_policy_cannot_relax_verifier_policy(ep, monkeypatch, field):
    candidate = copy.deepcopy(ep)
    cert = candidate["pair_membership"]
    cert[field] *= 2
    cert["binding"][field + "_float64_hex"] = float(cert[field]).hex()
    cert["binding_sha256"] = spectral._binding_sha256(cert["binding"])
    _before_anchor(monkeypatch, candidate)


def test_caller_cannot_inject_alternate_policy_cache(ep):
    candidate = copy.deepcopy(ep)
    cert = candidate["pair_membership"]
    cert["tolerance"] *= 2
    cert["binding"]["tolerance_float64_hex"] = float(cert["tolerance"]).hex()
    cert["binding_sha256"] = spectral._binding_sha256(cert["binding"])
    injected = spectral._SemanticAdmissionCache(tolerance=cert["tolerance"])
    with pytest.raises((TypeError, ValueError)):
        spectral.validate_pair_membership_certificate(candidate, cache=injected)


def test_fabricated_wrong_pair_fails_fresh_semantics(ep, monkeypatch):
    candidate = copy.deepcopy(ep)
    candidate["state_b"] = (3, 2, 0)
    cert = candidate["pair_membership"]
    cert["binding"] = spectral._pair_membership_binding(
        candidate["state_a"], candidate["state_b"], candidate["R"],
        candidate["p"], candidate["lam"], depth=candidate["depth"],
        Z1=candidate["Z1"], Z2=candidate["Z2"],
        tolerance=cert["tolerance"], probe_scale=cert["probe_scale"])
    cert["binding_sha256"] = spectral._binding_sha256(cert["binding"])
    cert["passed"] = True
    cert["max_scaled_matching_error"] = 0.0
    _before_anchor(monkeypatch, candidate)


def test_constructor_json_roundtrip_numpy_endpoint_and_reversed_permutation(ep):
    candidates = [ep, copy.deepcopy(ep), copy.deepcopy(ep)]
    candidates[1]["state_a"] = tuple(np.int64(x) for x in ep["state_a"])
    candidates[1]["depth"] = np.int64(ep["depth"])
    candidates[2]["pair_membership"]["permutation"].reverse()
    for candidate in candidates:
        assert spectral.validate_pair_membership_certificate(candidate)["passed"] is True
    # JSON-compatible complex representation follows the repository serializer.
    from bass_he.geometry import jsonable, unjsonable
    roundtrip = unjsonable(json.loads(json.dumps(jsonable(ep))))
    assert spectral.validate_pair_membership_certificate(roundtrip)["passed"] is True


def test_exact_cache_identity_distinguishes_nested_python_aliases(ep):
    cache = spectral._SemanticAdmissionCache()
    base = copy.deepcopy(ep)
    keys = []
    for state in [(1, 0, 0), (1.0, 0, 0), (True, 0, 0)]:
        candidate = copy.deepcopy(base)
        candidate["state_a"] = state
        try:
            keys.append(cache.key(candidate))
        except ValueError:
            keys.append(None)
    assert keys[0] is not None
    assert keys[1] != keys[0] and keys[2] != keys[0]


def test_extended_precision_scalar_cannot_alias_float64_cache_key(ep):
    cache = spectral._SemanticAdmissionCache()
    candidate = copy.deepcopy(ep)
    candidate["Z1"] = np.longdouble(1) + np.finfo(np.longdouble).eps
    with pytest.raises(ValueError):
        cache.key(candidate)


def test_exact_integer_charges_remain_constructor_compatible_and_cache_distinct(ep):
    integer_charges = spectral.find_exceptional_point(
        (1, 0, 0), (2, 1, 0), SEED, depth=64, Z1=1, Z2=2)
    assert spectral.validate_pair_membership_certificate(integer_charges)["passed"] is True
    cache = spectral._SemanticAdmissionCache()
    assert cache.key(integer_charges) != cache.key(ep)


@pytest.mark.parametrize("field", ["R", "p", "lam", "Z1", "Z2"])
def test_one_ulp_endpoint_changes_cache_key(ep, field):
    cache = spectral._SemanticAdmissionCache()
    candidate = copy.deepcopy(ep)
    original = candidate[field]
    if isinstance(original, complex):
        candidate[field] = complex(np.nextafter(original.real, math.inf), original.imag)
    else:
        candidate[field] = np.nextafter(original, math.inf)
    assert cache.key(candidate) != cache.key(ep)


def test_state_depth_policy_and_revision_change_cache_key(ep):
    cache = spectral._SemanticAdmissionCache()
    base = cache.key(ep)
    for field, value in [("state_b", (3, 2, 0)), ("depth", 65)]:
        candidate = copy.deepcopy(ep)
        candidate[field] = value
        assert cache.key(candidate) != base
    assert spectral._SemanticAdmissionCache(probe_scale=2e-4).key(ep) != base
    assert spectral._SemanticAdmissionCache(verifier_revision="test-new-revision").key(ep) != base


def test_exact_endpoint_revalidates_once_and_stale_caller_digest_is_irrelevant(ep, monkeypatch):
    cache = spectral._SemanticAdmissionCache()
    calls = {"fold": 0, "pair": 0}
    fold = spectral.spectral_certificate
    pair = spectral._pair_membership_certificate

    def counted_fold(*args, **kwargs):
        calls["fold"] += 1
        return fold(*args, **kwargs)

    def counted_pair(*args, **kwargs):
        calls["pair"] += 1
        return pair(*args, **kwargs)

    monkeypatch.setattr(spectral, "spectral_certificate", counted_fold)
    monkeypatch.setattr(spectral, "_pair_membership_certificate", counted_pair)
    cache.revalidate(ep)
    cache.revalidate(copy.deepcopy(ep))
    assert calls == {"fold": 1, "pair": 1}
    candidate = copy.deepcopy(ep)
    candidate["R"] = complex(np.nextafter(candidate["R"].real, math.inf), candidate["R"].imag)
    candidate["pair_membership"]["binding_sha256"] = ep["pair_membership"]["binding_sha256"]
    assert cache.key(candidate) != cache.key(ep)
    cache.revalidate(candidate)
    assert calls == {"fold": 2, "pair": 2}
    with pytest.raises(ValueError):
        spectral.validate_pair_membership_certificate(candidate)


def test_recorded_error_must_equal_fresh_error(ep, monkeypatch):
    candidate = copy.deepcopy(ep)
    candidate["pair_membership"]["max_scaled_matching_error"] = 0.0
    _before_anchor(monkeypatch, candidate)


def test_non_authoritative_diagnostics_do_not_change_admission(ep):
    candidate = copy.deepcopy(ep)
    candidate["pair_membership"]["probe_radius"] = "diagnostic-only"
    candidate["pair_membership"]["scaled_distance_matrix"] = None
    assert spectral.validate_pair_membership_certificate(candidate)["passed"] is True
