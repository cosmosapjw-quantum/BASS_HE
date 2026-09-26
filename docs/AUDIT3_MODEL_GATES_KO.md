# AUDIT3 — DR8V surrogate stress, DR9A trajectory gate, DR9B exponent/channel audit

## DR8V surrogate adversarial validation

The local-cubic surrogate in u=rho^2 was challenged against exact geometry at 30 endpoint-near points (0.90, 0.95, 0.98, 0.99, 0.995, 0.999 of each branch support) and 70 new child nodes from the only refined GK7 interval. All 100 exact solves succeeded. Maximum endpoint-near relative Delta error was 7.1816e-6; maximum refinement-node error was 4.0069e-5 (S23). Both are below the runtime gate 2e-4. This is held-out numerical validation, not a global interpolation bound.

## DR9A trajectory-domain gate

Stolterfoht et al. (Phys. Rev. A 81, 052704, 2010) state that realistic classical internuclear trajectories are crucial for the low-energy rotational/isotope effect and that straight-line trajectories cannot reproduce that effect. Their head-on estimates at 100 eV/u are Rmin≈0.65, 0.40, 0.30 a0 for H, D, T.

For the inherited clean-room S_lsigma matching radius, the diagnostic equality Rmin=Rmatch occurs at approximately:
- l=1: H 111.43, D 68.57, T 51.43 eV/u;
- l=2: H 33.91, D 20.87, T 15.65 eV/u.

These are not physical validity thresholds because Rmatch is a clean-room matching convention. At 0.5 keV/u the source puts the system near the transition to radial dominance, so the trajectory-model gate remains open. At 5 keV/u straight-line motion is more plausible, but not independently validated. No production extension below 0.5 keV/u is authorized without a trajectory-aware model or benchmark.

## DR9B factor-of-two and upper-shell semantics

CPC 2023 prints Eq.(52) as p=exp(-Delta/v) for an elementary transition, while Eq.(55) calls exp(-2Delta/v) the Q-series single-pass transition probability. Eq.(56) defines Delta from the imaginary part of a complex action. If the same Delta normalization is used, an amplitude exp[i(S_R+i Delta)/v] has probability |A|^2=exp(-2Delta/v). Thus factor-2 has the standard amplitude-to-probability interpretation, while source normalization remains unresolved.

A fresh Nmax=3 shell-level comparison adds independent evidence. Against Appendix-A shell cross sections, factor-2 gives multiplicative RMS discrepancy about 1.41 across dominant n=2,3 shell points, versus 4.60 for factor-1. Across all six shell points including the tiny n=1 channel, the factors are about 1.98 and 64.0. Total capture model/source ratios are 0.554 and 1.219 for factor-2 at 0.5 and 5 keV/u, versus 5.947 and 2.996 for factor-1.

This strongly favors factor-2 as the theory/benchmark research lane, but does not authorize silently rewriting Eq.(52) or changing a production default. Appendix A also prints CX(n=3)=ionization at Nmax=3 at both test energies, and CORDIR shows an upper united-atom shell can correlate to a lower bound separated-atom shell. The upper-shell population is therefore a source truncation surrogate, not an independently additive physical ionization channel.

## Gates

- DR8V surrogate endpoint/refinement validation: PASS as held-out numerical evidence.
- DR9A trajectory adequacy at 0.5 keV/u: OPEN / transition-boundary regime.
- DR9A 5 keV/u: straight-line more plausible, not independently validated.
- DR9B exponent: factor-2 theory-and-author-benchmark favored; source normalization remains OPEN.
- Nmax upper-shell physical channel partition: OPEN.
- Physical production cross section / BASS CT2 promotion: CLOSED_NOT_STARTED.
