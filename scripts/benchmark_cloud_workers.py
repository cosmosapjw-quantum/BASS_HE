#!/usr/bin/env python3
"""Authorized host-only fresh PERF sweep; no science cache reuse."""
import argparse,json,os,sys
from pathlib import Path
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','NUMBA_NUM_THREADS'):os.environ[key]='1'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bass_he.cloud.benchmark import benchmark,PerfWorkload
from bass_he.cloud.contracts import CaseSpec
from bass_he.cloud.resources import inventory,worker_limit
from bass_he.cloud.runtime import binding

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--profile',type=Path,required=True);ap.add_argument('--cases',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seed',type=int,default=20260928);ap.add_argument('--budget-seconds',type=int,default=900)
    a=ap.parse_args();profile=json.loads(a.profile.read_text());b=binding(Path(__file__).resolve().parents[1]);host=inventory(Path('/srv/bass-he'))
    if profile.get('storage_mode')!='mounted_host' or profile.get('source_commit')!=b.source_commit or profile.get('backend')!='python':raise RuntimeError('host runtime profile mismatch')
    if not a.out.resolve().is_relative_to('/srv/bass-he/runs') or not host.data_mount:raise RuntimeError('BLOCKED_DATA_MOUNT')
    cases=[CaseSpec(**item) for item in json.loads(a.cases.read_text())]
    if not cases or any(s.science_fields['source']!=b.source_commit+':'+b.source_tree or s.science_fields['backend']!='python' for s in cases):raise ValueError('PERF case source/backend mismatch')
    max_workers=worker_limit(profile,host,len(cases),profile['worker_rss_p95_bytes'])
    if max_workers<1:raise RuntimeError('no eligible host workers')
    class LimitedHost:usable_cpus=max_workers
    workload=PerfWorkload(cases,b,a.out/'PERF')
    report=benchmark(profile,LimitedHost(),workload,a.budget_seconds,a.seed)
    a.out.mkdir(parents=True,exist_ok=True)
    result={'status':report.status,'selected':report.selected,'observations':report.observations,'seed':report.seed,'binding':b.identity(),'namespace':'PERF_NOT_SCIENCE'}
    dest=a.out/'WORKER_SWEEP.json'
    with dest.open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps({'status':report.status,'selected':report.selected,'arms':len(report.observations)}))
    return 0 if report.status=='COMPLETE' else 2
if __name__=='__main__':raise SystemExit(main())
