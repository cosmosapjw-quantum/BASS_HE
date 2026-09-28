"""Runtime source/environment admission and binding."""
import hashlib, os, platform, subprocess, sys
from pathlib import Path
from .contracts import ExecutionBinding
from .backend import THREAD_POLICY

def binding(repo:Path):
    import numpy, scipy, threadpoolctl
    src=repo/'src'; hashes={str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(src.rglob('*.py'))}
    hashes['scripts/replay_dr11e.py']=hashlib.sha256((repo/'scripts/replay_dr11e.py').read_bytes()).hexdigest()
    git=lambda arg:subprocess.check_output(['git','rev-parse',arg],cwd=repo,text=True).strip()
    plan='4e775fdb61e72fd75f956fe0a83064e37e0522da'
    if git(plan+'^{tree}')!='6cd022714a4c3579ce1b2b68ac27f69968c0782d':raise RuntimeError('plan tree mismatch')
    if subprocess.run(['git','merge-base','--is-ancestor',plan,'HEAD'],cwd=repo).returncode!=0:raise RuntimeError('checkout is not derived from approved plan commit')
    cpuinfo=Path('/proc/cpuinfo').read_text() if Path('/proc/cpuinfo').exists() else ''
    flags=next((line.partition(':')[2].strip() for line in cpuinfo.splitlines() if line.startswith(('flags','Features'))),'UNKNOWN')
    blas=[{k:pool.get(k) for k in ('internal_api','version','filepath','threading_layer')} for pool in threadpoolctl.threadpool_info()]
    return ExecutionBinding(git('HEAD'),git('HEAD^{tree}'),hashlib.sha256(str(sorted(hashes.items())).encode()).hexdigest(),sys.version,{'numpy':numpy.__version__,'scipy':scipy.__version__,'threadpoolctl':threadpoolctl.__version__,'blas':blas,'hashes':hashes},platform.platform()+' '+platform.processor()+' flags_sha256='+hashlib.sha256(flags.encode()).hexdigest(),THREAD_POLICY)
