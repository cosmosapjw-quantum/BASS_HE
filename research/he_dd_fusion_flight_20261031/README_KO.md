# BASS_HE PR140 | Bosch–Hale D+D in-flight Green response in post-BBN plasma

**Status**: EXPLORATORY, SOURCE-CONDITIONAL, **NOT** a new measurement or production cosmological rate.

**Immutable parent**: cosmosapjw-quantum/BASS_HE Draft PR #139, HEAD `7fa301e661e339e489ee447a6244892ea52cc3c2`. PR139 original `src/fastd.py` file SHA-256 `e450e9cfb58abd834f10dd0ef79f12547cdb78e40ea685dd128fb4526f6e2979`. No edits to that file. Canonical DAG Central 28/88, HE Physical 14/18, delta 0; no merge, no force push, production HOLD.

## What is scientifically new

PR139 produced Coulomb stopping characteristics and energy-independent target columns. This unit inserts a **published energy-dependent R-matrix D+D fusion cross-section** into the stopping characteristic to compute two specific in-flight reaction probabilities, neutron/He3 and proton/tritium output yields and Q-release energy bookkeeping. The results are conditional *per injected fast deuteron*, not cosmic reaction rate or heat.

Source-authority chain: Bosch & Hale, *Nuclear Fusion* **32** (1992), 611–631, DOI `10.1088/0029-5515/32/4/I07` plus erratum *Nuclear Fusion* **33** (1993), 1919, DOI `10.1088/0029-5515/33/12/513`. Formula and exact parameter transcription checked against Hartwig & Podpaly, *MIT Magnetic Fusion Energy Formulary* (Feb 2014), section 9.7; original R-matrix fit valid for **D(d,n)He3 0.5≤Ecm≤4900 keV** and **D(d,p)T 0.5≤Ecm≤5000 keV**. The two cross-sections are NOT new experiments. PR139 energy stopping uses A. Beresnyak (ed.), *2023 NRL Plasma Formulary* p.31 and its original parent code; model is conditional narrow-beam use of an ensemble energy-moment formula.

D abundance is `D/H = (2.547 ± 0.029) × 10^-5` from the actual user-provided ACROPOLIS v1.3.1 `acropolis/obs.py` PDG2024 observation proxy. The uncertainty band applies solely to abundance normalization, not to Bosch–Hale uncertainty, NRL stopping, anisotropy or photoproduction. Input D target stationary; D thermal-velocity convolution NOT performed. H/He plasma is fully ionized and homogeneous at `T=T_CMB(z)`.

**Computational formula** for nonrel D on stationary D target:

`E_cm,keV=500*K_lab,MeV`, `sigma_j(E)=S_j(E)/E*exp(-31.397/sqrt(E)) [mb]`, `S_j(E)=A1+E(A2+E(A3+E(A4+EA5))) [keV mb]`, **B1-B4=0** for the two D+D channels. `S_Coulomb(K,z)=sum_b -dot K_b > 0` with b=e,p,He++; the nuclear *optical depth* is `tau_j=integral[Kterminal,K0] n_D sigma_j(K/2) v_D(K) / S_Coulomb(K,z) dK`. `P_DD,total=-expm1(-(tau_n+tau_p))`, `P_j=(tau_j/tau_total)*P_DD,total`; the final ratio approximation differs from exact survival-weighted branching by `O(tau_total^2)`. No non-D+D nuclear channels included in survival.

Only `K0={0.1,0.3,1,3,8} MeV` are run, at `z={1e4,3e4,1e5,3e5,1e6}`, and Kterminal inherited from PR139 `max(1 keV,30 kBT)`. Above `K0=8MeV` no B-H fit extrapolation is permitted. Four PR129 Asbury source-conditional nominal D births ~77–147 MeV are linked **only** through an explicit `P_DD given D reaches 8MeV` kernel, with upper-energy survival unknown and not silently set to one.

For each channel Q computed from published nuclear rest masses: 3.26885719 MeV for n+He3 and 4.03266400 MeV for p+T. Output CM kinetic energy partition follows two-body mass ratio from `Q+Ecm`; lab energy-angle distribution and **secondary heat** are not calculated. Nuclear Q-release is an additional *binding-energy* budget, not energy deposited from initial fast D.

## Results

25 integrated conditions +50 channel output rows +80 source-fit samples +3225 resolved stopping/nuclear profiles +25 model sensitivity rows +20 PR129 high-energy-source linkage rows = **3425 derived physical model rows**, zero new experimental observations. 4 PNG +4 SVG original science figures. Representative z=1e5, initial K=1MeV: P(D+D→n+He3)=9.28358210e-11, P(D+D→p+T)=7.57350896e-11, P(any of these two)=1.68570911e-10, mean event K_lab=0.707/0.702MeV respectively. Expected nuclear Q release=6.08881210e-10 MeV per fast D, **not heat**. At K0=8MeV and z=1e5, P_any_DD=1.292332949e-8, conditional on actually reaching the fitted energy interval.

Numerical: 160 vs 320 logarithmic Gauss–Legendre quadrature maximum relative difference recorded in SCIENTIFIC_SUMMARY.json; fixed Coulomb log20 vs screened PR139 drag separately tabulated (physics-sensitivity, not quadrature error). Wolfram independently checks the B-H 3/10/500 keV coefficients, nuclear Q; MIT tabulated values match. CSV audit does not import main code and checks counts, conditional labels, positivity, branch normalization and outgoing CM energy ledger.

## No-go gate deliberately NOT claimed

The result is **NOT** `R_event`, `heat_rate`, `kappa`, complete charged-particle nuclear survival, or final nuclear abundance history. No D+p breakup, D+He4 reaction, fast neutron/triton slowing, nuclear energy deposition, stochastic Fokker–Planck stopping distribution, or high-E (>8MeV) in-flight fusion is implemented. BASS-native MeV gamma source absent, but model response can proceed without unpublished experimental data or author contact. `PRODUCTION=HOLD; NO_MERGE=true; NO_FORCE_PUSH=true; AUTO_NEXT_NODE=false`.

## Reproduce

From the ZIP restore, the sibling frozen parent PR139 `research/he_dd_fastd_nrl_20261031/src/fastd.py` is present with its original SHA-256. Install `numpy scipy matplotlib` and run:

```bash
cd research/he_dd_fusion_flight_20261031
bash REPRODUCE.sh
python -O -m unittest discover -s tests -v # ensure PYTHONPATH includes both src paths
python verify_manifest.py
```

For the optimized test, export parent and current `src/` to PYTHONPATH exactly as in `REPRODUCE.sh`. Original parent PR139 / user ACROPOLIS source ZIP identities and Git HEAD are recorded in `notes/SOURCE_PROVENANCE.json`. Independent auditor and user can regenerate from the clean archive. GitHub PR should add only new research subtree; frozen parent file in ZIP is for standalone reproduction, not re-added to Git.
