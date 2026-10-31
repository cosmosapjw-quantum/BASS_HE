from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parent
manifest=json.loads((R/'MANIFEST_SHA256.json').read_text())
for name,digest in manifest.items():
    path=R/name
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        print('FAIL',name);sys.exit(1)
print('MANIFEST_SHA256_PASS',len(manifest),'/',len(manifest))
P=R.parent/'he_dd_fastd_nrl_20261031'/'src'/'fastd.py'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='e450e9cfb58abd834f10dd0ef79f12547cdb78e40ea685dd128fb4526f6e2979'
print('IMMUTABLE_PR139_FASTD_SHA_PASS')
