# HE35: finite-mass elastic pair pressure exchange

This additive unit supplies the exact first and second collisional moments of a specified isotropic Maxwell collision model for two finite-mass species. It extends HE34's stationary-heavy-target control to a conservative pair matrix. The parameter is supplied explicitly; no empirical H/He transport coefficient is adopted. The independent HE34 certified-relaxation/neutral-viscosity branch remains unchanged.

## Definition and owner conventions

Use a local orthonormal frame, proper time in seconds, metric signature (-,+,+,+), masses m_A,m_B in kg, fixed positive number densities n_A,n_B in m^-3, and pressure tensors in Pa. The classical nonrelativistic domain requires bulk speed much smaller than c and eigenvalues P_s/(n_s m_s c^2) much smaller than one. Thermal equilibrium is P_s=n_s k_B T I; k_B is retained. Neither hbar nor a radiation bath enters this classical elastic operator. Expansion/shear can be supplied separately by the HE33 mechanical equations. Number sources, binding energy, photons, self collisions and reactive moments are absent from this chosen binary cross-collision operator.

Let a=m_A/(m_A+m_B), b=m_B/(m_A+m_B), mu=m_A m_B/(m_A+m_B), a+b=1. The model is defined by

    g d sigma/dOmega = kappa/(4 pi),     kappa >= 0 [m^3/s].

This is an isotropic pseudo-Maxwell model. At g=0 the finite collision kernel defines the operator directly; a separate 1/g cross section is unnecessary. It is not the differential angular law of a calibrated inverse-fourth-power potential. The integral encounter frequencies are n_B kappa and n_A kappa. In this angular model sigma_1=sigma_2=sigma_tot=kappa/g, but finite-mass pressure eigenvalues still differ from encounter frequency.

For nonnegative independent distributions f_A,f_B with finite second moments, the pair rate per proper volume is n_A n_B kappa. There is no factor 1/2 because A and B are distinguishable populations. Define incoming g=v-w and V=a v+b w. Elastic outgoing velocities are

    v'=V+b |g| omega,      w'=V-a |g| omega,

where omega is uniform on the unit sphere. Consequently <g'>=0 and <g'g'^T>=|g|^2 I/3. These identities exactly integrate all polynomial moments used below; no Grad radial ansatz is needed.

## Direct event derivation and arbitrary drift

Write u_s=<v_s>, S_s=<v_s v_s^T>=P_s/(m_s n_s)+u_s u_s^T and X=u_A u_B^T+u_B u_A^T. Independence gives

    G=<gg^T>=S_A+S_B-X,
    H=<Vg^T+gV^T>=2a S_A-2b S_B+(b-a)X.

Angular averaging the difference of vv^T and ww^T yields the raw second-moment sources

    R_A=m_A n_A n_B kappa [-b H+b^2(tr(G) I/3-G)],
    R_B=m_B n_A n_B kappa [ a H+a^2(tr(G) I/3-G)].        (1)

The momentum sources are F_A=-mu n_A n_B kappa(u_A-u_B), F_B=-F_A. The central pressure sources are

    C_s=R_s-u_s F_s^T-F_s u_s^T.                        (2)

These formulae retain drift heating. Since m_A b=m_B a, the H terms cancel in R_A+R_B; the remaining term is traceless. Hence F_A+F_B=0 and tr(R_A+R_B)/2=0 exactly. Also

    tr(C_A+C_B)/2=mu n_A n_B kappa |u_A-u_B|^2 >= 0,

which equals the loss of bulk kinetic energy. The energy owner is the two-species matter kinetic sector; no opposite photon debit is introduced.

## Common-bulk pressure matrix

For u_A=u_B (choose their common rest frame), set p_s=tr(P_s)/3 and pi_s=P_s-p_s I. Equation (1) gives

    p_A'=-2ab kappa (n_B p_A-n_A p_B),    p_B'=-p_A',    (3)

    [pi_A'] = kappa [-n_B b(2a+b)    n_A ab       ] [pi_A]
    [pi_B']         [ n_B ab        -n_A a(2b+a)] [pi_B]. (4)

Each STF component obeys the same matrix. In HE33 LRS convention pi_s=q_s diag(-1,-1,2), the vector (q_A,q_B) follows (4). Total pair energy is 3(p_A+p_B)/2 and is conserved. Common-temperature isotropic states are fixed points because p_A/n_A=p_B/n_B=k_B T. The thermal difference relaxes at 2ab kappa(n_A+n_B).

Let A=n_B b(2a+b), B=n_A a(2b+a). The positive pressure-relaxation eigenvalues are

    lambda_fast=kappa [A+B+sqrt((A-B)^2+4 n_A n_B a^2 b^2)]/2,
    lambda_slow=2 a b n_A n_B kappa^2/lambda_fast.         (5)

The zero-kappa branch is explicit. The determinant identity is A B-n_A n_B a^2 b^2=2ab n_A n_B. Formula (5) avoids subtracting nearly equal positive roots. Finite floating-point representation is an implementation domain, not a change in the physical model.

## Positivity, dissipation and limits

For W=diag(1/n_A,1/n_B), W L in (4) is symmetric. Its negative diagonal and positive determinant imply negative definiteness when kappa>0 and all masses/densities are positive. Therefore the quadratic STF measure pi_A:pi_A/n_A+pi_B:pi_B/n_B strictly decreases away from zero. This weighted tensor statement does not assert that each species' signed anisotropy decreases monotonically in isolation.

The full common-bulk tensor equation also reads

    C_A=-kappa n_B b(2a+b)P_A+kappa ab n_A P_B
        +kappa(b^2 n_B p_A+ab n_A p_B)I,

with A<->B for C_B. All gain coefficients are nonnegative. Variation of constants and iteration preserve the positive-semidefinite pressure cone from PSD initial tensors. This is a property of the continuous operator, not of an arbitrary explicit finite numerical timestep.

For equal masses and equal n, the STF eigenvalues are n kappa/2 and n kappa. For m_B/m_A -> infinity with stationary cold target and fixed n_B kappa, species A has p_A' -> 0 and pi_A' -> -n_B kappa pi_A, recovering the HE34 speed-independent Lorentz case. Species swap gives the same pair physics. kappa=0 annihilates all sources.

## Sources, verification and scope

Bobylev and Gamba, *Boltzmann equations for mixtures of Maxwell gases: exact solutions and power like tails*, Section 2, pp. 2-4, supplies the Maxwell-mixture collision-kernel convention and elastic mass-dependent kinematics. The primary author-hosted PDF was read at https://www.oden.utexas.edu/media/reports/2005/0542.pdf on 2026-10-22 UTC (2026-10-23 KST). Equations (1)-(5) and the checks above are derived here from angular averaging; no numerical coefficient is imported from that paper.

Sanchez Romero and Garzo, Entropy 25 (2023) 222, DOI 10.3390/e25020222, abstract and Section 2 read at https://pmc.ncbi.nlm.nih.gov/articles/PMC9954823/, provide independent context for exact low-degree Maxwell mixture moments. Their collision-frequency/angular conventions are not silently identified with this kappa.

Validation uses finite incoming velocity measures and six outgoing coordinate-axis directions; that spherical quadrature exactly reproduces zeroth, first and second angular moments independently of (1). It tests tensor sources, momentum/energy, drift heating, species symmetry, equilibrium, eigenvalues and the Lorentz limit, with normalized tolerance 5e-13. A portable C99 scalar implementation is compared with independent reference fixtures. One bounded initial process has a 30-second cap; completed historical suites and cosmological trajectories are not replayed.

This is an exact conditional model result and executable component. Real energy-dependent/angular differential cross sections require new source-qualified collision integrals and may require additional moments/closure. HE33/34 mechanical moments, HE88 neutral Chapman-Enskog viscosity, and this exact pair model are separate contracts. No new impossibility theorem is adopted (NG1-NG7 not applicable). Physical mixture calibration, reactive B2, B3 closure choice and Einstein feedback remain open.
