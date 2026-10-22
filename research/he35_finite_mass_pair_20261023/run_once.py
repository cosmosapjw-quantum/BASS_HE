import subprocess,time,json,hashlib,platform
from pathlib import Path
start=time.time();cmd=['python3','test_pair.py'];r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
Path('stdout.txt').write_text(r.stdout);Path('stderr.txt').write_text(r.stderr)
Path('execution_receipt.json').write_text(json.dumps({'command':cmd,'cwd':str(Path.cwd()),'exit_code':r.returncode,'wall_seconds':time.time()-start,'timeout_seconds':30,'platform':platform.platform(),'source_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['pair.py','pair.c','pair.h','test_pair.py','run_once.py']}},indent=2)+'\n');print(r.stdout,r.stderr);raise SystemExit(r.returncode)
