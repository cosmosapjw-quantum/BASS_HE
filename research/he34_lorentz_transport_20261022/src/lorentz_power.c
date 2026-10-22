/* HE34 B1A C99 analytic Lorentz/Grad power-law functional, SI, libm only.
 * No species data or finite-mass mixture closure is embedded.
 * sigma2(v)=sigma_ref*(v/speed_ref)^exponent on all positive speeds.
 * status 0=success, 1=invalid input, 2=unrepresentable positive result.
 */
#include <math.h>
#include <float.h>

int he34_lorentz_power_rate(double n, double m, double T, double sigma,
                           double vref, double r, double *out) {
    const double kb = 1.380649e-23;
    if (!out || !isfinite(n) || n < 0 || !isfinite(m) || m <= 0 ||
        !isfinite(T) || T <= 0 || !isfinite(sigma) || sigma < 0 ||
        !isfinite(vref) || vref <= 0 || !isfinite(r) || r <= -8) return 1;
    if (n == 0 || sigma == 0) { *out = 0; return 0; }
    double lv = 0.5*(log(2*kb)+log(T)-log(m));
    double lr = log(n)+log(sigma)+lv+r*(lv-log(vref))+lgamma(4+r/2)-lgamma(3.5);
    double v = exp(lr);
    if (!isfinite(v) || v == 0) return 2;
    *out = v;
    return 0;
}
