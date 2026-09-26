# AUDIT4 — DR10 coherent-vs-stochastic transport gate

## 1. Isolated double passage

For a single two-state crossing with one-pass probability p, two incoherent population updates give P_M = 2 p (1-p).

A coherent two-path treatment can be written, after absorbing dynamical and Stokes contributions into a total phase Phi, as P_coh(Phi) = 4 p (1-p) sin^2(Phi).

Uniform phase averaging gives exactly 2 p (1-p), so the Markov result is the phase average for this isolated symmetric double-passage problem. The coherent envelope is [0, 4 p(1-p)], twice the Markov mean at its maximum. For any nontrivial p, the phase-ignorance half-width about the Markov mean is therefore 100% of that mean.

Wolfram checks the phase average and the two-pass stochastic matrix identity. Unit tests independently lock both formulas.

## 2. Why this does not close the full Eq. (50) network

The CPC 2023 Eq. (50)-(52) assembly multiplies probability matrices and therefore carries no complex phase. Stolterfoht et al. 2010 explicitly describe the impact-parameter oscillations in He2+ + H as Stückelberg interference produced by coherent contributions from two localized transition regions. Thus the current probability transport is a phase-erased model, not a coherent prediction.

The isolated two-pass phase-average equivalence cannot simply be promoted to the five-branch network with P_rot: multiple paths can recombine, branch phases are correlated, and the rotational block mixes channels. A coherent extension would need amplitude-level crossing matrices with Stokes phases, dynamical phase integrals between events, a phase convention through the rotational block, and a physical treatment of the upper-shell absorbing sink. Alternatively, retaining the Markov model as physics requires an explicit random-phase/decoherence authority.

## 3. Numerical stress at Appendix-A B=0

Using the factor-2 single-pass lane favored by DR9B: at 5 keV/u the Q23 branch has p≈0.2400, so the isolated double-pass Markov value is 0.3648 while the coherent envelope is 0–0.7297. At 0.5 keV/u Q23 has p≈0.01097, giving Markov 0.02170 and coherent envelope 0–0.04341. These are branch-level stress values only; they are not full cross-section error bars.

## 4. Gate

- isolated double-pass Markov = uniform phase average: CLOSED;
- full Eq. (50) coherence equivalence: OPEN;
- random-phase/decoherence authority: OPEN;
- coherent multi-branch transport: NOT IMPLEMENTED;
- physical production cross section / production CT2: CLOSED.
