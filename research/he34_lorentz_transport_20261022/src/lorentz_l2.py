"""HE34/B1A: Lorentz-limit Grad pressure-relaxation functional, SI units.

This is an instantaneous projected rate for a specified small quadrupole.
It is not a finite-mass multispecies collision closure. SciPy supplies quadrature.
"""
import math
import warnings
from scipy.integrate import quad, IntegrationWarning
from scipy.special import gammainc, gammaincc

KB = 1.380649e-23
GAMMA_7_2 = math.gamma(3.5)


def _nonnegative(name, value):
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError(name + " must be finite and nonnegative")
    return value


def _positive(name, value):
    value = _nonnegative(name, value)
    if value == 0:
        raise ValueError(name + " must be positive")
    return value


def _integral(fun, a, b, rtol):
    if not (math.isfinite(rtol) and 1e-13 <= rtol <= 1e-3):
        raise ValueError("rtol must lie in [1e-13,1e-3]")
    with warnings.catch_warnings():
        warnings.simplefilter("error", IntegrationWarning)
        return quad(fun, a, b, epsabs=0.0, epsrel=rtol, limit=200)


def angular_sigma2(dsigma_domega, rtol=1e-10):
    """Return sigma_2 [m^2] and QUADPACK error estimate, axial elastic kernel.

    Callback takes mu=cos(scattering angle), returns d sigma/d Omega [m^2/sr].
    Forward delta distributions and unscreened divergent kernels need another API.
    """
    def integrand(mu):
        return 3 * math.pi * (1 - mu * mu) * _nonnegative(
            "differential cross section", dsigma_domega(mu))
    value, error = _integral(integrand, -1.0, 1.0, rtol)
    return {"sigma2_m2": value, "quadrature_error_m2": error}


def power_law_rate(n_target, mass, temperature, sigma_ref, speed_ref, exponent):
    """Analytic full-domain rate for sigma_2(v)=sigma_ref*(v/speed_ref)^exponent.

    This law is a manufactured or explicitly adopted model on 0<v<infinity.
    Convergence requires exponent>-8. Return s^-1; positive underflow is explicit.
    """
    n = _nonnegative("n_target", n_target)
    m = _positive("mass", mass)
    t = _positive("temperature", temperature)
    s = _nonnegative("sigma_ref", sigma_ref)
    v0 = _positive("speed_ref", speed_ref)
    r = float(exponent)
    if not math.isfinite(r) or r <= -8:
        raise ValueError("exponent must be finite and greater than -8")
    if n == 0 or s == 0:
        return 0.0
    log_vt = 0.5 * (math.log(2 * KB) + math.log(t) - math.log(m))
    log_rate = (math.log(n) + math.log(s) + log_vt +
                r * (log_vt - math.log(v0)) +
                math.lgamma(4 + r / 2) - math.lgamma(3.5))
    value = math.exp(log_rate)
    if not math.isfinite(value) or value == 0:
        raise OverflowError("positive rate outside representable binary64 range")
    return value


def grad_rate(n_target, mass, temperature, sigma2, speed_domain=(0.0, math.inf),
              global_sigma2_upper_bound=None, rtol=1e-10):
    """Integrate only the stated speed domain. Never extrapolate a data callback.

    A finite domain returns a partial rate, not a full rate. Optional *assumed*
    global cross-section upper bound yields an omitted-domain upper bound.
    Quadrature error is an estimate, not a certified enclosure.
    """
    n = _nonnegative("n_target", n_target)
    m = _positive("mass", mass)
    t = _positive("temperature", temperature)
    lo = _nonnegative("domain lower speed", speed_domain[0])
    hi = float(speed_domain[1])
    if math.isnan(hi) or hi <= lo:
        raise ValueError("domain upper speed must exceed lower speed")
    bound = None if global_sigma2_upper_bound is None else _nonnegative(
        "global_sigma2_upper_bound", global_sigma2_upper_bound)
    vt = math.sqrt(2 * KB * t / m)
    if not math.isfinite(vt) or vt == 0:
        raise ValueError("thermal speed not representable")
    xlo, xhi = (lo / vt) ** 2, (hi / vt) ** 2
    if not math.isfinite(xlo) or (math.isfinite(hi) and not math.isfinite(xhi)):
        raise ValueError("scaled domain not representable")
    calls = 0
    def integrand(x):
        nonlocal calls
        v = vt * math.sqrt(x)
        if not lo <= v <= hi:
            raise ValueError("quadrature requested speed outside source domain")
        s = _nonnegative("sigma2", sigma2(v))
        calls += 1
        if bound is not None and s > bound:
            raise ValueError("sample violates assumed global sigma2 bound")
        return x ** 3 * math.exp(-x) * s
    value, error = _integral(integrand, xlo, xhi, rtol)
    factor = n * vt / GAMMA_7_2
    full = lo == 0 and math.isinf(hi)
    missing_weight = 6 * (float(gammainc(4, xlo)) + float(gammaincc(4, xhi)))
    partial = factor * value
    if not math.isfinite(partial):
        raise OverflowError("rate overflow")
    return {"status": "FULL_DOMAIN_MODEL" if full else "PARTIAL_DOMAIN",
            "partial_rate_s_inv": partial,
            "full_rate_s_inv": partial if full else None,
            "quadrature_error_s_inv": factor * error,
            "outside_rate_upper_bound_s_inv": None if bound is None else factor * bound * missing_weight,
            "bound_status": None if bound is None else "ASSUMED_GLOBAL_SIGMA2_BOUND",
            "callback_evaluations": calls,
            "thermal_speed_m_s": vt}
