import subprocess,ctypes,json,hashlib,time
from pathlib import Path
import numpy as np
from pair import matrices,sources
start=time.time()
assert all(np.count_nonzero(v)==0 for v in matrices(1e308,1e308,1e308,1e308,0))
assert all(np.count_nonzero(v)==0 for v in sources(1e308,1e308,1e308,1e308,0,np.eye(3),np.eye(3)).values())
subprocess.run(['gcc','-std=c99','-O2','-Wall','-Wextra','-Werror','-fPIC','-shared','pair.c','-lm','-o','pair.so'],check=True)
f=ctypes.CDLL(str(Path('pair.so').resolve())).he35_pair;f.argtypes=[ctypes.c_double]*5+[ctypes.POINTER(ctypes.c_double)]*3
arr=[np.ones(4),np.ones(4),np.ones(2)];assert f(1e308,1e308,1e308,1e308,0,*[a.ctypes.data_as(ctypes.POINTER(ctypes.c_double)) for a in arr])==0;assert all(np.count_nonzero(a)==0 for a in arr)
Path('zero_receipt.json').write_text(json.dumps({'status':'pass_scoped','command':'python3 zero_probe.py','wall_seconds':time.time()-start,'scope':'early zero-kappa branch; previous nonzero scientific suite unchanged','source_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['pair.py','pair.c','zero_probe.py']}},indent=2)+'\n');print('zero-kappa extreme-input probe passed')
