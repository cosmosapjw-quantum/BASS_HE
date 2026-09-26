# AUDIT7 — DR11A Nmax channel-semantics audit

## Primary-source facts

CPC 2023 section 2.7 states that the finite adiabatic basis is truncated at N=Nmax and that the ionization channel is identified with population of the upper shell; transitions down from that shell are closed.

Appendix A simultaneously prints the CORDIR map. At Nmax=3 every united N=3 state correlates to a bound Z2 separated state:
- (3,0,0) -> He+ n=3
- (3,1,0) -> He+ n=3
- (3,2,0) -> He+ n=2
- (3,1,1) -> He+ n=3
- (3,2,1) -> He+ n=3
- (3,2,2) -> He+ n=3

Thus the united upper-shell truncation label and the bound separated-atom labels overlap by construction.

Appendix A then prints exactly:
- E=0.5 keV/u: CX(n=3)=0.3285e-17 cm^2 and ionization=0.3285e-17 cm^2;
- E=5 keV/u: CX(n=3)=0.7708e-16 cm^2 and ionization=0.7708e-16 cm^2.

These outputs are therefore not independent measurements or a disjoint physical partition.

## Q23 semantic tension

Q23 ends at united (3,2,0), but CORDIR maps that state to separated He+ n=2. The published output alone therefore does not establish whether the internal CPC-2023 Q23 event used a blanket united-Nmax absorbing rule or a more selective channel convention before export. Janev-1997 treats 3d-sigma as a bound reversible channel, while the CPC-2023 prose describes upper-shell absorption broadly.

The correct audit state is INTERNAL_Q23_ABSORBING_SEMANTICS_OPEN. We do not rewrite the transport rule from output labels alone.

## Archived q2 structural diagnostic

The old fixed-order q2 run is not production-converged, but it is useful as a structural counterexample. In the factor-2 lane:
- 0.5 keV/u: mapped separated-n=3 area = 0.0952689842 a0^2; sum of all united N=3 output populations = 1.2633512363 a0^2; ratio = 13.2609.
- 5 keV/u: mapped separated-n=3 area = 2.4715281602 a0^2; all united N=3 = 59.9879167111 a0^2; ratio = 24.2716.

So identifying all united Nmax output population with the exported physical ionization cross section is incompatible with the Appendix-A export pattern.

## Claim gate

Closed:
- upper-shell/bound-correlation overlap: source-established;
- Appendix-A n=3 capture == ionization alias at two test energies: source-established;
- Q23 destination separated n=2 mapping: source-established;
- current reaction_loss_area must not be relabeled physical ionization.

Open:
- exact internal 2023 CR_SECTION rule selecting which upper-shell contributions feed the printed ionization number;
- physical disjoint partition of capture/excitation/continuum;
- whether Q23 should be reversible in a source-faithful reimplementation;
- production CT2.
