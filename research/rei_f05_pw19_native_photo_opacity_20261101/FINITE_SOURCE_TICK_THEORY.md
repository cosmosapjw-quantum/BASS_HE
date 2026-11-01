# R1–R5: source-clock-matched frozen H/He photon survival, not a new IGM IVP

2026-11-01 | BASS_HE original REI IGM | Continuation of one bounded PR148 original-source opacity unit.

**Motivation and question.** PR148 obtained a large PW19 hard-band transmission difference (0.82777 against 0.367879 for grey) after **one local mean free path**, an arbitrary diagnostic length. The original F05 first proposed interval [160,161] has a real **proper clock step** from original REC191 source; quantify if that hypothetical time length `L=c Δt` actually makes this grey closure problematic. This is material for prioritizing genuine original REI 26-event photon/thermal RUX03/04 acceptance, rather than repeatedly exploring unphysical mean-free-path attenuation examples.

**Source identity and exact clock.** Immutable original REC191 source-inclusive ZIP SHA256 `3f6772f54822274bf6228dac1ec629a9d0b0cde9d2a0adbaa08d59a1ac352d0e` contains `research/rec_rei_f05_native_thomson_medium_20261101/results/SCIENCE_RESULT.json` and original 17 first-interval forcing nodes. It gives `original_proper_tick_s="4.87184874916821289E+9"`, source `z_mid=5.95`, original source tick160/131072 **accepted**, proposed tick161 **NOT ACCEPTED**. The timestep from this original source is not the span of a cosmological photon geodesic. The corresponding physical length `L=c Δt` means only the distance a light ray would travel in a *fixed homogeneous local material* during one **hypothetical** step. It does **not** imply local cells have size L or remain homogeneous over this distance.

**Microphysics and actual original material.** Reuse exact PR148 original 46,080-cell `REIADP1` H/He accepted tick160 population interval / proper volume, original Taira-PW19 spectral positive photon weights and Verner HI/HeI/HeII fit, the three threshold resolved donor bands. Keep all source input hashes, original 14 ledgers, source F05 G3 effectively no hard photons, original P19 homogeneous UVB distinct from local causal source.

For each original cell j and donor band g, define `X_g(E)=κ_j(E)=Σ_s n_{sj}^proper σ_s(E) ≥ 0`, source photon-number probability measure `w_g(E)≥0,∫w_g dlnE=1`, `μ_{gj}=E_w[X_g(E)]=κ_g(j)`, `V_{gj}=Var_w[X_g(E)]≥0`. Let `L=cΔt`, `τ_{gj}=μ_{gj}L`. Exact **constant-frozen-cell** survival for this imposed background is `T_{gj}(L)=E_w[exp(-L X_g(E))]`. Grey survival at the same instantaneous opacity is `Tgrey=exp(-τ)`.

### Exact theorem: finite-step grey bias upper envelope
Since exp(-x) is convex, `0 ≤ T-Tgrey`. Moreover for nonnegative κ and L,
`0 ≤ T-Tgrey ≤ (L²/2) Var_w[κ] = (τ²/2) CV²`, where `CV²=Var_w[κ]/μ²`.

Proof: Taylor's theorem for `f(x)=exp(-Lx)` about μ,
`f(x)≤f(μ)+f'(μ)(x-μ)+(L²/2)(x-μ)²`
because `0≤f''(x)=L² exp(-Lx)≤L²` for x≥0. Integrate w; the linear mean-zero term cancels. Jensen yields the lower bound. True spectral **absorption fraction** `1-T` is at most the grey one `1-Tgrey` for frozen positive material and photon-number weighting; grey overestimates absorption.

The **source-clock bound** `B_g(j)=0.5 τ_g(j)^2 CV²_g(j)` can be evaluated on all original 46,080 cells without inserting any invented photon birth history. Its source-volume-weighted mean is an upper bound on the volume-weighted mean absolute transmission bias under **uniform imposed PW19 photon density**, not a conservative observable CMB LoS bound or total thermal-energy error. Cell-specific spectral `T` is directly quadrature evaluated at source-density/opacity quantile representative native cells as a model falsification witness.

### Meaning and stop conditions
Compare B_g with `10^-6` and `10^-4` only as **science-scale descriptors**, NOT original REI 2e-4 adaptive numerical gate, which concerns a different quantity and original 26-event local discrete map. Never interpret `L=cΔt` as actual spatial cell size, direction-specific photon ray or native source; the local W_node volumes do not define paths. No new photon radiation packets, nuclear source emissivity, H/He chemistry update, proper relativistic Bianchi transport or official tick161.

One bounded output: 3-band × true 46k-cell source-clock τ and Jensen upper bound summaries + 9 actual source-cell spectral transmission samples, same-author independent frequency re-integration and source hash tests. After this, **STOP** adjacent PW19 spectral/opacity atlases, return to actual REI original Rust source-clock + causal photon owner and F05 V2 admission. All stages preserve REI central **28/88**, working **33/88**, physical fast **4/7**, BASS_HE physical **14/18**, canonical delta **0**, production HOLD, no merge/force/tolerance changes.

Primary literature: Pawlik & Schaye 2011 doi:10.1111/j.1365-2966.2010.18032.x photon conserving multi-frequency transfer; Friedrich et al. 2012 doi:10.1111/j.1365-2966.2012.20449.x coupled H/He and OTS; Puchwein et al. 2019 doi:10.1093/mnras/stz222 context for equivalent effective vs local source.
