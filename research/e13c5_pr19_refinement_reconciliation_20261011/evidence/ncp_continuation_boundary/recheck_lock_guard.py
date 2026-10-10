#!/usr/bin/env python3
"""NO_SCIENCE: relevant controls after root's lock-file guard correction."""
from pathlib import Path
import hashlib, importlib.util
W=Path('/workspace/scratch/7fd51143e473/e13c5_ncp_continuation_boundary_work')
P=Path('/workspace/scratch/7fd51143e473/BASS_HE_E13C5_INCOMING_ANCHOR_ENCLOSURE_20261011_v1')
assert hashlib.sha256((P/'code/ncp_continue.py').read_bytes()).hexdigest()=='38957cb24f58b5d36dd4823ce7e642c708f0f4cae725ac2377d3f824b2b41626'
assert hashlib.sha256((P/'CONTINUATION_LOCK.json').read_bytes()).hexdigest()=='a1ccb4f352a7bd12d97419b09dc41bc2782332ae01c4a7b8173f3cdd3bcdbef7'
spec=importlib.util.spec_from_file_location('original_boundary_controls',W/'run_synthetic_boundaries.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.W=W/'repair_01'
m.CASES=[c for c in m.CASES if c[0] in ('verify_only','fresh_success','lock_metadata_tamper_during')]
raise SystemExit(m.main())

