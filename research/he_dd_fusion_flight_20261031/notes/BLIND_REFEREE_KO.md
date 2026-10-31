# Self-blind R06/C09 | One bounded adversarial pass

- **BLOCK NOW corrected:** Generic `P_survival` and `P_any` could falsely imply total nuclear survival. Renamed to `P_no_BH_DD_fusion` and `P_any_BH_DD_fusion`; data and tests regenerated. No global survival claim.
- **SOURCE DOMAIN protected:** Asbury-source reconstructed 77–147 MeV D cannot use Bosch-Hale D+D fit with Ecm up to 4.9/5.0 MeV. Implement explicit `K0>8 MeV` error; 20 source-link records contain only conditional *after entry to 8 MeV* probability. High-energy nuclear survival explicitly unknown.
- **MODEL NORMALIZATION:** D/H is observation proxy ACROPOLIS obs.pdg2024, not new measurement or cosmological model-sourced injection, with observed ±0.029e-5 propagated separately; not an uncertainty on stopping or S factor.
- **KINEMATICS:** Zero-temperature target approximates D+D Ecm=Klab/2. At high z, target Maxwellian may affect low-energy cross section, labelled future physics. Q-values checked from nuclear masses; output CM kinetic energy split not an assumed lab angular distribution. No secondary thermal heat claim.
- **STOCHASTIC STATUS:** NRL `ν_ε` is ensemble energy-moment, not exact single trajectory. Conditional characteristic narrow-beam approximation; full FP straggling and energy diffusion are absent. The source-conditional response cannot be production R_event or heat.
- **INDEPENDENCE:** Internal code checks and saved-CSV audit are separate implementations but the same author; Mathematica/Wolfram independently checked B-H cross section at 3,10,500 keV plus Q masses. Actual different-author R06/C09 NOT_RUN. New tests normal/optimized and parent regression required, with logs.
- **NULL SAFE:** `kappa=null; R_event=null; heat_rate=null; L4=false; PRODUCTION=HOLD; NO_MERGE=true` remain fixed. No implied astrophysical D/H abundance changes from these single-beam probabilities.

Verdict: accepted **source-conditional DD-in-flight micro response** after all targeted tests; global physical closure and canonical DAG increase 0.
