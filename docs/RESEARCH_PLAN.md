# Audit-led DR8 reconstruction and analytical optimization

Goal: replace false branch certification and inefficient repeated work, preserving the published approximation scope.
Authority: CPC 286 (2023) 108662, attached 2010 END paper, legacy DR7 archive SHA efcc252fcf0bfc8ed8d4a36949c0d1ee859835bd356c3fb5a0b317a1dd6625b8.
User-approved sequence: adversarial audit -> mathematical/physical alternatives -> derived optimizations -> code -> new tests -> pilot -> Git publication.

## Recovery
DR8 directory contains only README.md and README_KO.md, both still describe DR7. No DR8 executable payload or completed numerical result is present. Do not inherit transcript-only execution.
Seven returned archives: transport/manifests checked; these do not prove physical correctness.

## New bounded work units
- A1: formulate explicit branch degeneracy witness; downgrade prior coalescence certificate, preserve baseline.
- A2: prove rotating-frame gauge removal, sparse column action, identity-tail subtraction, and energy-independent geometry reuse. Compare alternatives in RESEARCH_REPORT.
- C1 `src/bass_he/spectral.py`: analytic continued-fraction derivatives; F=0 and det(dF/d(p,lambda))=0 root; monodromy diagnostic.
- C2 `src/bass_he/rotation.py`: gauge-regularized polynomial Hamiltonian, fourth-order unitary Magnus, parity subblocks, batched energies/rho, no singular rho=0 path.
- C3 `src/bass_he/transport.py`: sparse Eq50 initial-column propagation, explicit exponent lanes, disjoint sink vs bound-channel reporting, finite off-diagonal Eq54 only.
- C4 `src/bass_he/geometry.py`: reference-seeded geometry and contour error/branch diagnostics; reuse geometry across energies, process-level parallelism with per-job durable JSON receipts.
- V1: failing tests first; post-fix counterexample rejection, analytic Jacobian checks, monodromy, gauge equivalence, dense/sparse identity, batching/scalar equality and probability bounds.
- V2: limited post-upgrade pilot and timing; no old DR8 full run, no unrelated already-passed test loops.
- P1: clean repository commit and non-force push. Repository is public and initially empty; exclude raw private runtime paths, attached PDFs, tokens and binary caches.

## Stop and claims
No continuum/thermal/production closure. Any ambiguous sheet or failed numerical budget is explicitly rejected. No imputation of missing scientific results. Push requires successful actual remote acknowledgement, not merely push permission in metadata.
