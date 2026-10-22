# HE34: Lorentz pressure-relaxation functional and HE33 Node closure

This bounded sandbox increment follows HE33 at
`bb1259b21c7b83b0376a5f7fcbb0c6321918ec90` and its science pin
`1d7dab57becc5829f0282b88a7516360ccad718a`.
The invoked PhysMath skill is1.3.0; HE33's historical workflow1.0.0 receipts retain
their original meaning. Selected work is R4–R7/C3–C8 plus the requested compact
delivery. No full historical campaign is replayed.

The HE33 E0 module-loading check passed17/17 groups under Node24.19.0 in0.273s.
Exact existing core/check SHA256 values match the science handoff. The new HE34
verification passed11 groups, including C99 compilation and five analytic versus
quadrature power-law controls. Internal test+compile time was0.181s; this is not a
speedup benchmark and excludes Python/SciPy import startup.

`src/lorentz_l2.py` provides angular l=2 projection and source-domain-aware velocity
integration. `src/lorentz_power.c` implements the analytic all-speed power-law
functional using C99/libm only. Inputs are SI. `THEORY.md` derives the weighting,
explains the8/5 constant-cross-section ratio to event frequency, and states the
instantaneous Grad projection boundary. The numerical rates in the controls use
manufactured cross sections; no calibrated primordial transport rates are claimed.

Run only if an affected new host/source dependency needs verification:

```bash
python research/he34_lorentz_transport_20261022/checks/check_transport.py
```

The checker needs Python3, SciPy and GCC, has a15s compile timeout, imports only
this new unit, and writes `evidence/TRANSPORT_VALIDATION.json`. It does not call
HE32, external compute or NCP. Existing HE33 E0 is already complete; its immutable
source remains in the ancestor rather than being copied here.

The next scientific work is source-calibrated sigma_2 and finite-mass/exchange
moments, then B2 reactive source moments and B3 closure. Full B1 is still partial.
The root orchestration owns publication/backup receipts and the new-thread handoff.
