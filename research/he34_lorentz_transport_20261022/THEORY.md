# HE34 B1A: a computable pressure-relaxation functional

This unit supplies the first restricted transport input for the HE33 pressure
equation. It selects the elastic Lorentz limit: stationary, effectively infinite
mass scattering targets of number density n_t, projectile mass m, an isotropic
Maxwellian reference at T>0, and a small traceless quadrupole perturbation. Target
recoil, target thermal motion, inelastic events, electromagnetic acceleration and
species exchange are outside this derivation. SI units are retained.

## Angular operator

Let v denote speed, omega its direction, mu=omega dot omega', and
D(v,mu)=d sigma/d Omega >=0. The elastic rotationally invariant collision operator is

    C[f](v,omega)=n_t v integral D(v,omega dot omega')
                                  [f(v,omega')-f(v,omega)] d omega'.

Rotational invariance diagonalizes this angular convolution in spherical
harmonics. Aligning omega with the polar axis and integrating over azimuth gives

    C[f_lm Y_lm]=-n_t v sigma_l(v) f_lm Y_lm,
    sigma_l(v)=2 pi integral[-1,1] [1-P_l(mu)] D(v,mu) d mu.

The pressure STF moment contains only l=2. Consequently

    sigma_2(v)=(3/2) integral sin(theta)^2 d sigma
              =3 pi integral[-1,1](1-mu^2)D(v,mu)d mu.                 (1)

The positive weight proves sigma_2>=0 for a nonnegative differential cross
section. It also shows why total or l=1 momentum-transfer cross sections cannot
generally replace sigma_2. For example D=sigma_0[1+a P_2(mu)]/(4 pi), with
-1<=a<=2, has unchanged total and l=1 cross sections but
sigma_2=sigma_0(1-a/5). Pure reversal does not change a quadratic velocity moment.
The implementation integrates regular functions; distributional angular kernels
and divergent unscreened Coulomb kernels require a separate representation.

## Velocity moment and its precise closure level

Take the tangent to a positive anisotropic Gaussian at an isotropic Maxwellian:
delta f is proportional to f_M(v) v_<i v_j> A_ij, with A symmetric traceless.
This is a linear response statement; the truncated polynomial correction is not
asserted to be a positive distribution at every speed for finite amplitude.
Since the pressure moment supplies another v^2 and d^3v supplies v^2 dv,

    nu_pi,Grad = n_t integral[0,infinity] v^7 exp(-v^2/v_T^2) sigma_2(v) dv
                     / integral[0,infinity] v^6 exp(-v^2/v_T^2) dv,
    v_T=sqrt(2 k_B T/m).

With x=v^2/v_T^2 this becomes the implemented expression

    nu_pi,Grad = n_t v_T/Gamma(7/2)
                integral[0,infinity] x^3 exp(-x) sigma_2(v_T sqrt(x)) dx. (2)

Its dimension is s^-1. For sigma_2(v)=sigma_ref (v/v_ref)^r on all positive
speeds, convergence at the origin requires r>-8, and

    nu_pi,Grad = n_t v_T sigma_ref (v_T/v_ref)^r
                Gamma(4+r/2)/Gamma(7/2).                             (3)

The C99 libm kernel evaluates (3) in logarithms. For a constant isotropic cross
section it gives 16 n_t sigma_ref v_T/(5 sqrt(pi)). The Maxwellian event rate
is 2 n_t sigma_ref v_T/sqrt(pi); their ratio is 8/5. This factor follows from
the pressure-moment weighting, not a rate fit. Root orchestration separately
checked the Gamma integral and ratio using the live Wolfram evaluator.

Equation (2) is an instantaneous projected rate. Under collisions alone, each
speed's quadrupole decays with its own n_t v sigma_2(v). Even a small initial Grad
perturbation therefore generally leaves its initial radial shape. The exact
pressure ratio is a weighted superposition of exponentials. At constant sigma_2,
with n_t sigma_2 v_T t=1, the new quadrature gives 0.18437048354567437,
whereas freezing the initial projected rate gives 0.16440758378370465.
Jensen's inequality predicts this ordering for the positive normalized radial
weight. Only a speed-independent collision eigenvalue, for example sigma_2~1/v,
makes this simple exponential exact for this pure angular-scattering problem.
No general impossibility theorem is claimed; this explicit control identifies
the additional closure assumption required by a one-rate model.

## Source domains and uncertainty

The callback returns sigma_2 in m^2 and declares its speed interval. A finite
interval produces a PARTIAL_DOMAIN contribution, with full_rate_s_inv=null.
No out-of-domain evaluation or extrapolation is performed. If an independently
justified global upper bound sigma_max is supplied, the omitted contribution is
bounded above by

    n_t v_T sigma_max/Gamma(7/2) * 6
        * [P(4,x_lo)+Q(4,x_hi)],                                    (4)

where P,Q are regularized incomplete Gamma functions. This is conditional on the
global bound; the code checks sampled in-domain values but cannot validate an
unseen physical tail. QUADPACK error estimates remain numerical estimates, not
rigorous interval enclosures. A missing bound remains unknown explicitly.

## Reuse and next physical dependency

HE33 source/check bytes are unchanged. Its E0 Node host compatibility gate now
passes separately. HE34 code is a callable functional and an analytic C kernel,
with manufactured controls and no adopted empirical species-rate rows. Turning
it into an electron-neutral transport input requires an angular source or an
independently sourced sigma_2 table with units, temperature/energy domain and
uncertainty. Finite-mass neutral/ion collisions and Coulomb energy exchange require
the species-resolved B1 matrix; reactive Q,J,R_part remain B2. B3 chooses the
closure before B4 uses one saved HE32 background. No completed HE32 trajectory
has been regenerated and no new cosmological IVP was run.

## Source use

The university kinetic-theory notes cited in SOURCES.json supply the differential
cross-section collision operator and linearization context. The l=2 projection,
radial weighting, Gamma formula and domain bound above are derived here. The
SciSpace-discovered Winkler et al. paper is a relevant follow-up on Lorentz-plasma
harmonic and tensor representations; only its metadata/abstract were inspected,
so no unseen equation is attributed to it. Existing HE33 equations define the
pressure convention and prohibit substituting event rates for transport rates.
