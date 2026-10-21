# HE29 HPC64 packed canary return

고정 execution code `802a32361288bf5aa0e0d1f63c912768f1a1d407`에서 준비된 m8/GL4/q0,r4/table512 packed canary 1건을 실행했다. 결과는 `CANARY_COMPLETED_SCOPED`; 4개 admitted Radau+DOP853 reference는 그대로 재사용했고 새 reference/transport/test replay는 없었다.

## 측정

- Native call/point records: 182,280; solver thread 1.
- Bridge compile: 104.119s, Cargo/Rust cargo 1.94.1 (29ea6fb6a 2026-03-24), bridge SHA `28d637a9011ad0e23c087659cd07574cfb0ddc55511380c4c807165aee3123eb`.
- Source table: 48 worker 프로세스 실행, 8,721 row, 2.791s, full SHA `919ca6f42028bffc37cb208916ee5a9927356eb99344fe467f9b98e30e9fddcd`.
- Canary: 717.331s; packed solve/checkpoint 710.211s; close + gzip readback 2.197s.
- gzip point records written/durable/verified 182,280/182,280/182,280; complete gzip readback PASS.
- Photon number 3.85117548322e-08/H; energy 9.54604763559e-07 eV/H; binding 4.92540665614e-05 eV/H.
- Number/energy/species defects: 1.31e-20/H, 1.06e-17 eV/H, max 7.03e-20. Positivity PASS.
- Saved Radau/DOP853 comparison max fraction 7.96e-20; max temperature 1.12e-13 K.

The five pre-existing Codex/Codex-session process identities were left alive and exempted only with an external, exact PID/start-tick/cmdline-SHA allowlist after the user's explicit idle confirmation. The process shim and original observation are preserved. No physics, solver thread count, numeric tolerances, or source code changed. No new process identity is exempt.

This is a single finite canary; continuum convergence, global temperature bounds, full EoR, whole Grackle equivalence, and Bianchi/CMB remain HOLD. The canonical `MAKE_RETURN.py` archive is embedded with its receipt; see DELIVERY/DAG for identities and backup status.
