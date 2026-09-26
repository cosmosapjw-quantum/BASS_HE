# AUDIT6 — DR10C source-topology identity

## Source formula

Janev, Pop-Jordanov & Solov'ev, J. Phys. B 30, L353-L360 (1997), Eq. (15), give the coherent 1s-sigma/2p-sigma inverse-reaction channel probability

P = p12(1-p12)(1-p23)
    | exp[i(chi1+gamma)]
      +(1-pS) sqrt(1-p_rot) exp[i(chi2-gamma)] |^2.

Uniform averaging over the relative phase removes the cross term and gives

Pbar = p12(1-p12)(1-p23)
       [1+(1-pS)^2(1-p_rot)].

This averaging statement does not require constructing chi1 or chi2.

## Exact comparison with current sparse Eq. (50)

The current Nmax=3 event order is S23, Qother, Q12, Qm1, Q23 on recession and the reverse order on approach, with P_rot in the middle. Starting in the united-atom 2p-sigma state and reading the final 1s-sigma population, exact symbolic multiplication gives

P(j1 <- j3)
 = p12(1-p12)(1-p23)
   [1+(1-pS)^2(1-p_rot)].

The expression contains neither Qother nor Qm1. Wolfram simplifies the difference from the phase-averaged 1997 Eq. (15) to exactly zero. An independent 10,000-point random stress gives maximum absolute difference 1.11e-16 and exactly zero sensitivity to Qother/Qm1 variations.

Therefore the current stochastic topology is not merely a generic Markov guess for this one source channel: it exactly reproduces the uniform-phase average of the published coherent two-path topology.

## Scope

Closed:
- source Eq. (15) coherent algebra: implemented;
- phase-average algebra: implemented;
- current sparse Eq. (50) topology for this final 1s-sigma channel: exact source-phase-average identity;
- irrelevance of Qother/Qm1 for this channel: exact.

Open:
- chi1/chi2 complete path construction;
- finite-phase differential probability;
- source-equivalent identities for the forward 3d-sigma/2p-pi channels of Eqs. (13)-(14);
- full five-branch coherent network;
- physical production cross section and production CT2.

The result validates topology under phase averaging, not phase erasure at arbitrary velocity.
