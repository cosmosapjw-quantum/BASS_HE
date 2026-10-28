# EXFOR11 independent review — preexecution component

**Disposition: the core mathematics and implementation pass static review.** One bounded science campaign is admissible after actual S05 publication and source pinning. Two small wording corrections are required before their respective outputs are sealed. This is the preexecution component of one nonauthor review; actual results, timing, certificates and PNG are still pending.

## Scope and independence

I did not author the new contract, implementation or tests. I read the frozen contract, all new Python sources, the original official EXFOR file, the publication-safe Rice/Arends summary and the inherited Bernstein primitive. I compared literal rows and reviewed proofs and code without importing scientific modules or running science, tests, CAS or plots. The exact inspected file digests are in `PREEXEC_REVIEW.json`. Actual runtime model identity is not observable here and is not asserted.

## Two precise corrections

| ID | Target | Evidence and impact | Minimal repair |
|---|---|---|---|
| REV001 | `scripts/plot_saved.py:35` | The black interval uses outward geometry coefficients and therefore encloses the inner family's range; its endpoints need not be attained. Calling it “inner family range” overstates that result. | Change the caption to “inner family enclosure” before the single plot invocation. |
| REV002 | `CONTRACT.md:62` | Each objective is conditioned on one fixed energy. A common positive factor eta(e) cancels at that energy even if it varies between energies. | State cancellation separately at fixed energy; angle-dependent response or energy-dependent weighting inside an energy-integrated observable does not generally cancel. Correct before the execution pin. |

Neither finding changes the scientific computation. The reviewer has made no implementation or contract edits; repairs belong to the parent scientific authority and designated coding executor.

## Mathematical and implementation findings

The twelve DCS/ERR-S rows match M0475002 exactly. The six M0475003 total-cross-section rows remain separate on a disjoint energy grid. Source bytes are pinned by SHA256, and the parser additionally checks exact literal tables. The model correctly identifies the error boxes as sensitivity windows, nominal angles as record coordinates, reflection-even nonnegative Bernstein coefficients as a sufficient positivity cone, uniform azimuth as declared, and endpoint zero as an extrapolation assumption. The Rice discussion is not promoted to an independently recovered original Arends normalization convention.

The paired Bernstein basis and its normalization are correct, including the undoubled middle basis and removal of the endpoint coefficient. The inherited primitive is in mu and matches the new basis. The separate manufactured-cap control expands in x and supplies a useful independent algebraic check. Cosine evaluation uses the correct phase theta/720. Interval products and outward grid rounding remain conservative.

For nonnegative coefficients, the inner inequalities imply feasibility at the exact nominal cosine, and exact feasibility implies the outer inequalities. A strictly positive lower basis row bounds every coordinate; a positive lower observation excludes the origin. Thus denominators are positive and polytopes compact. Exhaustive exact active-set enumeration includes every vertex; singular systems are skipped without numerical tolerance. The fractional-objective vertex principle follows from denominator-weighted convex combinations. Nonnegative basis integration over inherited inner/outer coincidence sets gives the required ordered geometry coefficients.

The saved certificate reader independently checks all stored inequalities, denominators, inner-to-outer inclusion, geometry ordering and objective witnesses using exact arithmetic. It does not independently certify completeness of the vertex list. Completeness instead rests on the reviewed exhaustive enumeration and known-polytope controls; no second independent optimizer should be claimed. The static enumeration comprises 3,984 candidate inversions, shared over three energy right-hand sides. This count is not a timing measurement.

The wrappers check the exact source/dependency manifest and input hash, bound one contracted science campaign, preserve raw output and record resource use. No execution or published pin was inspected at this phase. Timing, memory, control counts, nonempty/empty outcomes and acceptance values must all be reported from the upcoming actual receipts.

## Requirements for the same review's continuation

Read the actual pinned source identity, primary validation report, saved exact result, resource receipts and raw stdout/stderr; inspect the actual PNG and its input digest. Interpret an empty outer family as incompatibility of this finite family and sensitivity window only. An empty inner family with nonempty outer family does not settle true feasibility. Outer extremizers need not be physically feasible nominal fits; inner witnesses are feasible nominal fits but retain geometry enclosures.

This unit does not close any of the three open physical inputs. Central completion remains 28/88 with HE physical delta zero; global physical completion remains null, L4 false and production NOT_APPROVED. No HARMONIC10 science, tests, CAS, plots or backups were rerun.
