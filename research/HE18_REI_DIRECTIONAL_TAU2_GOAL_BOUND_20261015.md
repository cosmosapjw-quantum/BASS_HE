# BASS_HE → rei_bianchi: conditional directional Thomson quadrupole error budget
2026-10-15 KST. This note is a **downstream cold AXBI reuse receipt**, not a warm HE18 FT03/HM12 source-ODE certificate.

**Canonical new code and computed source-bound evidence:** [rei_bianchi directional transfer and sensitivity module](https://github.com/cosmosapjw-quantum/rei_bianchi/tree/research/bass-he-optical-depth-transfer-20261015/research/bass_he16_transfer_20261015/directional_tau_20261015), commit `5dd89558c290b272716c785094283d3a8d5ca1c8`.

The original five 200001-row cold-source histories have shared source-epoch SHA256 `d7676b9309ac9b084499bbf599e803baecd661c80765489be45839ef5a7cf185`. The BASS_HE HE18 16-cell warm certificate has different helium, thermal and photon-stock conventions. **No warm numerical tau or closure is identified with cold AXBI.**

For a non-tilted normal-comoving observer at the common prefix endpoint (mean zbar~10.2693), the exact Bianchi I directional relative-redshift formula used was
[
1+z_{m dir}=rac{a_o}{a_e}
sqrt{(1-mu_o^2)e^{2(b_e-b_o)}+mu_o^2e^{-4(b_e-b_o)}}.
]
This is a relative redshift to the high-z normal observer, not our present CMB observer.

New **derived conditional goal-functional inequality** with true source errors (sup|delta b|leqepsilon_b), (sup|delta x_{m HII}|,sup|delta x_{m HeII}|,sup|delta x_{m HeIII}|leqepsilon_x) and frozen exact (a(t),t(a),n_H(t)):
[
|delta O_{	au_2}|leq C_bepsilon_b+C_xepsilon_x.
]
The proof uses (|partial_{Delta b}ln F|leq2), log-redshift inverse slope (m=1-2sup|db/dln a|>0), (|delta u_e|leq4epsilon_b/m), and (	frac52int_{-1}^{1}|P_2|dmu=10/(3sqrt3)). The original numerical source-ODE error is **NOT certified**.

At (|q|=.005,z_{m rel}=.75), the actual stored-source odd quadrupole is (O_{	au_2}=-2.5931564384664	imes10^{-6}). Measured conditional sensitivities: (C_b=0.0975613971785774, C_x=0.2870530863320277). A **sufficient bound if only one error source is present** for its contribution to be ≤10% is (epsilon_bleq2.65797	imes10^{-6}) or (epsilon_xleq9.03372	imes10^{-7}). If both error sources coexist, obey their summed budget.

Ubuntu verification: original parent+directional regression tests **52/52 PASS**; injected real-history perturbations at 1e-6 for b and for species satisfy the conditional bound. Five source histories satisfy (n_Ha^3) to maximum relative deviation (3.33	imes10^{-16}). Five-case chunked (16384) slope-extremum implementation and full-array NumPy longdouble reference agree; interleaved 5-run medians **0.08494s vs 0.17557s** (~2.07x faster) with reduced scratch. This is postprocessing, not native Rust solver optimization.

The full updated source/figures/JSON and both original numerical caches are **double backed up** in user Ubuntu `~/archives/BASS_HE_REI_TRANSFER_20261015_1445KST/` and Dropbox `BASS_DERIVATION_DOSSIERS_20260912/HE18_REI_TRANSFER_20261015/`. Delivery receipt includes SHA256 IDs and unchanged live solver HEAD.

**Next science gate:** independent native convergence of b(t), ionization fractions and clocks for a small ZERO/±0.005 common-prefix experiment and goal-oriented error propagation to tau_0/tau_2. No inference of physical shear detection or present-day CMB polarization is admitted.

Physics reference: Fleury, Pitrou & Uzan, *Light propagation in a homogeneous and anisotropic universe*, Phys. Rev. D 91, 043511 (2015), [DOI](https://doi.org/10.1103/PhysRevD.91.043511). Atomic model comparison: Friedrich et al., MNRAS 421, 2232 (2012), [C2-Ray H/He](https://academic.oup.com/mnras/article/421/3/2232/1077406).
