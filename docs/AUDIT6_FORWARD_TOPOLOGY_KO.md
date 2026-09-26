# AUDIT6 follow-up — Janev 1997 forward-channel topology

## Eq. (14): 2p-pi channel

Janev et al. 1997 Eq. (14) is

P_2p-pi = (1-p23)(1-p12)(1-pS)(1-p_pi3dpi) p_rot.

The current sparse Eq. (50) final 2p-pi population is symbolically identical. Qother and the reverse pi->sigma rotational column do not enter this matrix element. A 10,000-point independent numerical stress gives max absolute difference 1.11e-16.

This forward channel therefore has direct source-topology support without invoking an unknown coherent phase.

## Eq. (13): 3d-sigma channel

To compare with the Nmax=3 scoped model, higher N=4 transitions in the published Eq. (13) are explicitly frozen to zero transition probability. Define

s = sqrt(1-p_rot),
B = (1-p12)(1-pS)s.

The uniform-phase average of that Nmax=3 source projection is

P_src = p23(1-p23) [1 + (p12+B)^2].

If Q23 is made reversible in an otherwise stochastic Markov assembly,

P_revM = p23(1-p23) [1 + p12^2 + B^2].

The exact difference is

P_revM - P_src = -2 p23(1-p23) p12(1-p12)(1-pS)s.

Thus stochastic population propagation loses a coherent cross term between two subpaths that carry the *same* source phase chi1. Uniform averaging between chi1 and chi2 does not remove this term.

The actual current Nmax=3 implementation treats the upper-shell Q23 destination as absorbing. Its final 3d-sigma/sink population is

P_current = P_revM + p23^2,

and therefore

P_current - P_src
 = p23^2
   - 2 p23(1-p23)p12(1-p12)(1-pS)s.

Wolfram verifies these identities exactly. A 10,000-point random stress gives max residual 2.22e-16.

## Interpretation

The source comparison is channel-selective:

- Eq. (15) inverse sigma channel: exact phase-averaged topology match.
- Eq. (14) forward 2p-pi channel: exact topology match.
- Eq. (13) forward 3d-sigma channel: mismatch with two separately identified causes:
  1. missing same-phase intra-contour coherence in a pure probability propagation;
  2. Nmax=3 absorbing-sink semantics adding p23^2.

This is stronger than a generic warning about coherence. It identifies the exact algebraic place where the scoped stochastic model ceases to reproduce the published coherent topology.

No attempt is made to call the Nmax sink a physical 3d-sigma cross section.
