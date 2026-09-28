#!/usr/bin/env python3
"""Local durable cloud replay entrypoint; service invokes the same CLI."""
import argparse, json, os, sys
from pathlib import Path
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','NUMBA_NUM_THREADS'):os.environ[key]='1'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bass_he.cloud.runtime import binding
from bass_he.cloud.store import ResultStore
from bass_he.cloud.controller import Controller
from bass_he.cloud.export import export_checkpoint
from bass_he.cloud.resources import inventory,worker_limit

ROOT=Path(__file__).resolve().parents[1]
def admit_storage(out,profile):
    mode=profile.get('storage_mode')
    if mode=='mounted_host':
        if not out.resolve().is_relative_to('/srv/bass-he/runs'):raise ValueError('run directory outside mounted data volume')
        if not profile.get('worker_rss_p95_bytes'):raise ValueError('measured worker RSS required')
        host=inventory(Path('/srv/bass-he'))
        if not host.data_mount:raise RuntimeError('BLOCKED_DATA_MOUNT')
        worker_limit(profile,host,1,profile['worker_rss_p95_bytes'])
        return lambda ready:worker_limit(profile,inventory(Path('/srv/bass-he')),ready,profile['worker_rss_p95_bytes'])
    if mode=='local_sandbox':
        if not out.resolve().is_relative_to('/tmp'):raise ValueError('local sandbox output must be under /tmp')
        return lambda ready:min(2,profile['workers'],ready)
    raise ValueError('unknown storage mode')
def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('preflight')
    p=sub.add_parser('run');p.add_argument('--profile',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=1)
    for name in ('resume','status','export'):
        p=sub.add_parser(name);p.add_argument('--out',type=Path,required=True)
        if name=='resume':p.add_argument('--retry-failed',action='store_true')
    args=ap.parse_args();bind=binding(ROOT)
    if args.command=='preflight':
        print(json.dumps({'status':'PASS','source_commit':bind.source_commit,'source_tree':bind.source_tree,'binding':bind.identity(),'accelerator':'ACCELERATOR_PAYLOAD_UNAVAILABLE'},sort_keys=True));return 0
    out=args.out
    if args.command=='run':
        profile=json.loads(args.profile.read_text())
        if profile.get('artifact_kind')=='DESIGN_TARGET_NOT_EXECUTABLE_RUNNER_CONFIG':raise ValueError('design profile is not a runtime profile')
        if profile.get('backend')!='python' or profile.get('source_commit')!=bind.source_commit:raise ValueError('runtime profile binding mismatch')
        if profile.get('storage_mode') not in ('local_sandbox','mounted_host'):raise ValueError('explicit storage_mode required')
        if args.workers<1 or args.workers>32:raise ValueError('initial worker cap is 32')
        runtime_profile={'source_commit':bind.source_commit,'backend':'python','workers':args.workers,'storage_mode':profile['storage_mode'],'worker_rss_p95_bytes':profile.get('worker_rss_p95_bytes')}
    else:runtime_profile=json.loads((out/'RUN_PROFILE.json').read_text())
    cap=admit_storage(out,runtime_profile)
    if args.command=='run':
        out.mkdir(parents=True,exist_ok=True)
        pf=out/'RUN_PROFILE.json'
        with pf.open('xb') as f:
            f.write((json.dumps(runtime_profile,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
        fd=os.open(out,os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
    profile=runtime_profile
    store=ResultStore(out,bind)
    try:
        if args.command=='status':
            rec=store.reconcile();print(json.dumps(rec.__dict__,sort_keys=True));return 0
        if args.command=='export':
            receipt=export_checkpoint(store,out/'exports');print(json.dumps(receipt.__dict__,sort_keys=True));return 0
        result=Controller(store,profile['workers'],worker_cap=cap,retry_failed=getattr(args,'retry_failed',False)).run()
        print(json.dumps(result.__dict__,sort_keys=True));return 0 if result.status=='PASS' else 1
    finally:store.close()
if __name__=='__main__':raise SystemExit(main())
