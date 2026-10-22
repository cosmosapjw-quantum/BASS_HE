"""One bounded verification pass for HE34 B1A; no historical IVP invocation."""
import ctypes
import hashlib
import json
import math
import pathlib
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from scipy.integrate import quad
from scipy.special import gammainc

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lorentz_l2 import angular_sigma2, grad_rate, power_law_rate, KB


def main():
    start = time.perf_counter()
    groups = []
    sigma, n, mass, temp = 2.3e-20, 4.2e6, 9.1093837139e-31, 20000.0
    vt = math.sqrt(2 * KB * temp / mass)
    def near(a, b, tol=3e-10):
        assert math.isclose(a, b, rel_tol=tol, abs_tol=0), (a, b)
    def add(name, **details):
        groups.append({"name": name, "status": "PASS", **details})
    a = angular_sigma2(lambda mu: sigma/(4*math.pi))
    near(a["sigma2_m2"], sigma)
    add("isotropic_angular_l2", **a)
    a = angular_sigma2(lambda mu: sigma/(4*math.pi)*(1+0.5*(3*mu*mu-1)/2))
    near(a["sigma2_m2"], sigma*0.9)
    add("same_total_cross_section_different_l2", sigma2_over_total=a["sigma2_m2"]/sigma)
    rows = []
    for r in [-2.0, -1.0, 0.0, 2.0, 4.0]:
        numerical = grad_rate(n, mass, temp, lambda v: sigma*(v/vt)**r)
        analytic = power_law_rate(n, mass, temp, sigma, vt, r)
        near(numerical["full_rate_s_inv"], analytic)
        rows.append({"exponent": r, "rate_s_inv": analytic,
                     "relative_difference": abs(numerical["full_rate_s_inv"]/analytic-1),
                     "callback_evaluations": numerical["callback_evaluations"]})
    add("speed_integrals_vs_gamma_family", rows=rows)
    constant = power_law_rate(n, mass, temp, sigma, vt, 0)
    near(constant/(n*sigma*2*vt/math.sqrt(math.pi)), 8/5)
    add("event_rate_is_not_pressure_rate", ratio=constant/(n*sigma*2*vt/math.sqrt(math.pi)))
    near(power_law_rate(n, mass, temp, sigma, vt, -1), n*sigma*vt)
    near(power_law_rate(3*n, mass, temp, sigma, vt, 0), 3*constant)
    add("inverse_speed_exact_constant_frequency_and_density_scaling")
    calls = []
    def limited(v):
        assert .5*vt <= v <= 3*vt
        calls.append(v)
        return sigma
    p = grad_rate(n, mass, temp, limited, (.5*vt, 3*vt), sigma)
    fraction = gammainc(4, 9)-gammainc(4, .25)
    near(p["partial_rate_s_inv"], constant*fraction)
    near(p["partial_rate_s_inv"]+p["outside_rate_upper_bound_s_inv"], constant)
    assert p["full_rate_s_inv"] is None and p["status"] == "PARTIAL_DOMAIN"
    add("finite_source_domain_and_explicit_tail_bound", **p, sampled_min=min(calls), sampled_max=max(calls))
    assert grad_rate(n,mass,temp,limited,(.5*vt,3*vt))["outside_rate_upper_bound_s_inv"] is None
    add("missing_tail_is_unknown_without_assumed_bound")
    invalid = [lambda: power_law_rate(n,mass,temp,sigma,vt,-8),
               lambda: power_law_rate(n,0,temp,sigma,vt,0),
               lambda: grad_rate(n,mass,temp,lambda v:-sigma),
               lambda: angular_sigma2(lambda mu:-sigma),
               lambda: grad_rate(n,mass,temp,lambda v:sigma,(1,0)),
               lambda: grad_rate(n,mass,temp,lambda v:sigma,(0,math.inf),sigma/2)]
    for f in invalid:
        try: f()
        except ValueError: pass
        else: raise AssertionError("invalid input accepted")
    add("invalid_inputs_rejected", count=len(invalid))
    assert power_law_rate(0,mass,temp,sigma,vt,0) == 0
    assert power_law_rate(n,mass,temp,0,vt,0) == 0
    add("zero_density_and_zero_cross_section")
    # The initial Grad radial profile changes when collision frequency depends on speed.
    exact_q = quad(lambda x:x**2.5*math.exp(-x-math.sqrt(x)),0,math.inf,
                   epsabs=0,epsrel=1e-11)[0]/math.gamma(3.5)
    single_exp = math.exp(-math.gamma(4)/math.gamma(3.5))
    assert exact_q > single_exp
    add("projected_initial_rate_is_not_exact_finite_time_closure",
        normalized_time=1, exact_lorentz_q_ratio=exact_q,
        frozen_grad_exponential_q_ratio=single_exp, difference=exact_q-single_exp)
    cc = subprocess.run(["gcc","--version"],capture_output=True,text=True,check=True).stdout.splitlines()[0]
    with tempfile.TemporaryDirectory() as td:
        lib = pathlib.Path(td)/"libhe34.so"
        cmd=["gcc","-std=c99","-O2","-Wall","-Wextra","-Werror","-pedantic",
             "-fPIC","-shared",str(ROOT/"src/lorentz_power.c"),"-lm","-o",str(lib)]
        build=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=15)
        fn=ctypes.CDLL(str(lib)).he34_lorentz_power_rate
        fn.argtypes=[ctypes.c_double]*6+[ctypes.POINTER(ctypes.c_double)]
        fn.restype=ctypes.c_int
        errors=[]
        for r in [-7.5,-2,-1,0,2,4,10]:
            out=ctypes.c_double()
            assert fn(n,mass,temp,sigma,vt,r,ctypes.byref(out))==0
            ref=power_law_rate(n,mass,temp,sigma,vt,r)
            near(out.value,ref,2e-14)
            errors.append(abs(out.value/ref-1))
        out=ctypes.c_double(123)
        assert fn(n,mass,temp,sigma,vt,-8,ctypes.byref(out))==1 and out.value==123
        assert fn(1e-300,mass,temp,1e-300,vt,0,ctypes.byref(out))==2
        add("C99_libm_analytic_kernel", compiler=cc, max_python_relative_difference=max(errors),
            build_exit=build.returncode, stderr=build.stderr, cases=7)
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ROOT/"src/lorentz_l2.py",ROOT/"src/lorentz_power.c",pathlib.Path(__file__)]}
    receipt={"schema":"he34.lorentz_grad.controls.v1","status":"PASS_SCOPED",
             "observed_utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),
             "groups":len(groups),"passed":len(groups),"failed":0,"tests":groups,"source_hashes":hashes,
             "wall_seconds":time.perf_counter()-start,"physical_rate_table_rows_adopted":0,
             "new_cosmological_ivps":0,"scope":"manufactured Lorentz/Grad transport controls and analytic C kernel"}
    (ROOT/"evidence/TRANSPORT_VALIDATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__ == "__main__":
    main()
