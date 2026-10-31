# Source to derivation to computational form | BASS_HE PR140

**Context.** Metric (-,+,+,+), FLRW tetrad local background, physical kinetic energy K in MeV. c, ħ, k_B retained in PR139 source. In a homogeneous, fully ionized primordial plasma with constant local T=T0(1+z), n_D=(D/H) n_H, and source D/H from ACROPOLIS v1.3.1 PDG2024 observational baseline, the in-flight reaction optical depth for channel j as a D slows from K0 to Kt is

\[ \tau_j = \int_{K_t}^{K_0} \frac{n_D(z)\,\sigma_j(E_{\rm cm}(K))\,v_D(K)}{\sum_{b=e,p,\alpha} S_b(K,z)}\,dK,\quad S_b=-\left(\frac{dK}{dt}\right)_b>0.\]

Nonrel stationary D target: Ecm=K/2 and v=sqrt(2K/mD). The NRL 2023 test-particle energy-moment slowdown (PR139 code) is a **characteristic approximation**, not a per-particle deterministic FP trajectory. This is why these outputs are conditional Green responses.

Bosch/Hale parameterization for D(d,n)He3 and D(d,p)T:

\[ \sigma_j(E) = \frac{A_{1j}+E[A_{2j}+E(A_{3j}+E(A_{4j}+EA_{5j}))]}{E}\exp\left(-\frac{B_G}{\sqrt{E}}\right)\;{\rm mb},\quad E\ [\mathrm{keV}],\ B_G=31.3970\sqrt{\mathrm{keV}}.\]

Numerator units implicit in the published B-H parametrization, not SI-based. All b-denominator coefficients zero for the two D+D reactions. Confirmed source at MIT Magnetic Fusion Energy Formulary §9.7. The published validity `0.5≤Ecm≤4900 or 5000 keV` enforces **K_lab≤8 MeV** in this study, with zero extrapolation. For each prescribed K0 and z we compute both tau with 160/320 node quadrature, probability from `-expm1(-tau_total)` and channel weights. This is exact total probability for the integrated *two-channel* opacity; allocating to channels via integral tau fractions incurs O(tau²) because survival correlates with energy-dependent branching. All tau<~few×10^-8 and the correction is less than 10^-15 absolute.

Energy and particle bookkeeping:

* D+D → n+He3 (Q=3.26885719 MeV) and D+D → p+T (Q=4.03266400 MeV) conserve baryon number 4 and charge 2. The outgoing two-body center-of-mass kinetic energy for a collision at lab K is K/2+Q. For final product masses m_a,m_b, K*_a=(K/2+Q)m_b/(m_a+m_b), K*_b=(K/2+Q)m_a/(m_a+m_b). No angular scattering distribution is assumed for lab ejectile kinetic energies.
* Expected Q release `∑P_j Q_j` comes from nuclear binding, not from the incident gamma and not a measured thermal deposition. Residual kinetic energy of reacting fast D `∑P_j〈K〉_j` is also separately reported. The target's binding-energy contribution is not lost in the projectile Coulomb energy account.
* The conditional P(no D+D fusion) is **not** survival against D+p breakup, D+He4 reactions, or any other nuclear channel. 

Dimensional checks: n_D[m^-3] σ[m²] v[m/s] = [1/s]; S=[MeV/s]; dK=[MeV], so τ dimensionless. Q and kinetic outputs in MeV. Limits: D/H→0 implies τ→0; K0↓Kt implies τ→0; increasing K0 adds positive hazards (within B-H domains), and `P_j≥0`, `∑P_j+exp(-τ)=1`.

**Source limitations**: observational D/H uncertainty is small but does not cover cross-section fit errors, nuclear screening, plasma-density variations, thermal target Doppler spread, or NRL model closure. At z=10^6, kBT≈0.235 keV, so near Kt≈7.046 keV finite target temperature may be non-negligible; no Maxwellian convolution has been applied. CEA1966 is neutral gas and not substituted for Coulomb ionized-plasma stopping. Four nominal Asbury D fast births >77 MeV are outside B-H fit; only conditional **post-entry** K≤8MeV kernel is reused.

Science outcome is a physically sourced small-probability secondary production *per fast D*, not R_event or net heat rate. Main next physics: source-owned deuteron–proton breakup and deuteron–alpha reactions above 8MeV, plus kinetic transport/thermalization of neutrons/He3/T/protons, while preserving 17-channel photon cascade and original BASS gamma-source distinction.
