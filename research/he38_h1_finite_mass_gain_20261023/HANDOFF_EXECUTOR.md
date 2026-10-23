# HE38 executor / restoration handoff

Workflow1.0.0 / approval0.2. Repo cosmosapjw-quantum/BASS_HE; branch research/he38-h1-finite-mass-gain-20261023; PR91. Unit research/he38_h1_finite_mass_gain_20261023.

Restore the unit from its pinned Git publication and final archive in delivery/FINAL_ACK.json. Verify that archive's SHA256 before extracting. Keep unrelated working-tree changes. Read README,RESULTS_KO,DAG,NEXT_DAG,RUN_RECORD and the science manifest first.

From the restored repository run only the saved-evidence verifier:

```bash
python research/he38_h1_finite_mass_gain_20261023/verify_saved.py --require-delivery
```

This imports only the standard library and checks hashes, saved outcomes,129CSVrows,stage snapshots and providerACKs. It launches no science. Add --archives --archive-root /actual/archive/directory only when the20newstagearchives andfinalarchive are present locally.

Scientific STF consumers use wrapper.J or species.total_J_Pa_s; nested event_tensor_source.J is legacy trace-projection audit. All physical/energy/frame/domain contracts stay fixed. The original controls and diagnostic are complete and must not be rerun merely for restoration.

The portable independent oracle entry in evidence/raw_controls/portable/launch.py accepts explicit --implementation-root, --output-root, --attempt and refuses an existing attempt. It is PREPARED_NOT_SCIENCE_EXECUTED; use it only for a new justified affected validation after a changed dependency. Preserve the executed originals and their receipts. The diagnostic script also accepts restored paths. Avoid historical /tmp/he38_implementation hard paths in fresh execution.

Executor scope is restoration,execution of a specifically authored new plan, and minimal evidenced boundary fixes. Do not invent physics, alter thresholds/masses/census, normalize away defects, install heavy runtimes without a measured need, merge branches, or overwrite old attempts. Report actual command/exit/time/RSS/input-output identities. If interrupted, resume the recorded delivery job rather than repeating scientific work.
