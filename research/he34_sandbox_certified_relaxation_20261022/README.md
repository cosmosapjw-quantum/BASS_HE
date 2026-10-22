# HE34-SCR: sandbox certified relaxation and neutral H/He transport

**workflow1.0.0 / approval0.2.** PR88 continues HE33. HE32's 30/30 completed campaign and HE33's source/evidence are reused. This unit is distinct from the parallel HE34 Lorentz-transport PR87.

## Checkpoint S1 — executed, 17/20 stages complete

On one pinned saved HE32 background (s07_m03_r03, 201 nodes), the new prescribed-rate mechanical controls accepted chi=1000,10000 and rejected chi=10,100 against the fixed 1e-6 ratio/log-pressure continuum bounds. At chi=1000 the observed ratio error is 6.8409e-7 and its proved bound is 6.8689e-7. A separate numerical convergence/budget gate passed. No outward-rounded floating-point certificate is claimed.

The exact neutral-H1/He4 first-Sonine viscosity reduction agrees with the independently assembled 2x2 solve to 6.4653e-16 relative at all 201 saved epochs. Its hydrodynamic matching diagnostic chi_neutral falls from 1.6671e4 to 1.5527e-3. It is not used as the prescribed mechanical chi and does not close the all-gas transport problem.

Measured median times in this host/workload: certified mechanical calculation 73.505 ms versus interval-segmented Radau 785.762 ms (10.69 ratio; five variable-duration trials); vector rational transport 0.244831 ms versus batched matrix 0.315845 ms (1.290 ratio). Full raw timings and qualifications are preserved.

## Scope and evidence

- [CONTRACT.json](CONTRACT.json): assumptions, fixed tolerances, original-goal gap.
- [DAG.json](DAG.json): per-stage evidence, checkpoint, backup and next stages.
- [theory/EQUATION_CODE_MAP.md](theory/EQUATION_CODE_MAP.md): source/equation/code contracts and numerical boundaries.
- [results/MECHANICAL_CONTROLS.json](results/MECHANICAL_CONTROLS.json), [results/NEUTRAL_TRANSPORT.json](results/NEUTRAL_TRANSPORT.json): actual new results.
- [evidence/MECHANICAL_EXECUTION.json](evidence/MECHANICAL_EXECUTION.json), [evidence/TRANSPORT_VALIDATION.json](evidence/TRANSPORT_VALIDATION.json): commands, environment, stdout/stderr and exit status.

The current mechanics is source-free Q=j=0 with prescribed constant chi. The neutral result assumes common T=20000 K and HE32's A*m_u mass convention. Calibrated baryonic stress, reactive tensor/energy moments, evolving temperature and radiation, extra species and metric feedback remain explicit dependencies. Existing matter stress is nonbaryonic; HE32 gas pi_b remains zero.

Old HE32 IVP/render/benchmark replay: **0/0/0**. New full cosmological IVPs: **0**. Eleven new mechanical reference histories (four controls, one refinement, one baseline accuracy run, five timing runs) used 2200 short source-interval solves. Prototype executions and their serialization failure are accounted separately.

Current next step: independent output/figure review and final R10/C10 closeout with both handoffs. Publication/backup acknowledgements are under delivery/. This checkpoint does not claim those remaining stages complete.
