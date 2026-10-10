#!/usr/bin/env python3
"""NO_SCIENCE: synthetic process/identity fixtures for unchanged ncp_continue.py."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, shutil, subprocess, sys, time

W=Path('/workspace/scratch/7fd51143e473/e13c5_ncp_continuation_boundary_work')
P=Path('/workspace/scratch/7fd51143e473/BASS_HE_E13C5_INCOMING_ANCHOR_ENCLOSURE_20261011_v1')
CASES=[
 ('verify_only',False,True,0),
 ('fresh_success',True,True,1),
 ('stale_current_hash',True,False,1),
 ('false_fresh_parity',True,False,0),
 ('failed_physics',True,False,0),
 ('wrong_projection_bytes',True,False,1),
 ('locked_payload_tamper_before',True,False,0),
 ('wrong_producer_hash',True,False,1),
 ('locked_payload_tamper_during',True,False,1),
 ('existing_out_collision',True,False,0),
 ('lock_metadata_tamper_during',True,False,1),
]
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(d,indent=2)+'\n')
MOCK_PHYSICS=r"""#!/usr/bin/env python3
# NO_SCIENCE mock; never imports scientific code.
from pathlib import Path
import argparse,json,os,sys
p=argparse.ArgumentParser();p.add_argument('--package',type=Path);p.add_argument('--out',type=Path);p.add_argument('--execute',action='store_true');a=p.parse_args()
case=os.environ['BASS_HE_CONTINUATION_FIXTURE_CASE']
a.out.mkdir(parents=True,exist_ok=False)
with (a.out.parent/'SYNTHETIC_CHILD_INVOCATIONS.jsonl').open('a') as f:f.write(json.dumps({'NO_SCIENCE':True,'child':'physics_mock','case':case})+'\n')
def w(name,obj):(a.out/name).write_text(json.dumps(obj,sort_keys=True)+'\n')
print('NO_SCIENCE synthetic physics child '+case,flush=True)
if not a.execute:
 w('NCP_RESULT.json',{'NO_SCIENCE':True,'status':'VERIFY_ONLY_PASS','new_host_scientific_runs':0,'scientific_execution':'NOT_RUN'});sys.exit(0)
w('NCP_RESULT.json',{'NO_SCIENCE':True,'status':'FAILED' if case=='failed_physics' else 'PASS_SCOPED_HOST_PARITY','new_host_scientific_runs':1,'scientific_execution':'ACTUALLY_EXECUTED'})
if case=='failed_physics':
 print('NO_SCIENCE intentional mock exit17',file=sys.stderr);sys.exit(17)
lock=json.loads((a.package/'CONTINUATION_LOCK.json').read_text())
w('RESULTS.json',{'NO_SCIENCE':True,'fixture_values':[2,4],'payload':'fresh synthetic result'})
w('PARITY.json',{'NO_SCIENCE':True,'fresh_output_compared':case!='false_fresh_parity','fresh_as_run_source_matches_execution_lock':True,'bitwise_numerical_json_parity':True,'actual_numerical_sha256':lock['baseline_physics_numerical_sha256']})
"""
MOCK_REDUCTION=r"""#!/usr/bin/env python3
# NO_SCIENCE mock; verifies wrapper plumbing only.
from pathlib import Path
import argparse,hashlib,json,os
p=argparse.ArgumentParser()
for k in ['prior','prior-start','prior-code','pilot','controls','current','out']:p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();case=os.environ['BASS_HE_CONTINUATION_FIXTURE_CASE'];package=Path(__file__).resolve().parents[1]
a.out.mkdir(parents=True,exist_ok=False)
with (a.out.parent/'SYNTHETIC_CHILD_INVOCATIONS.jsonl').open('a') as f:f.write(json.dumps({'NO_SCIENCE':True,'child':'reduction_mock','case':case})+'\n')
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def w(name,obj):(a.out/name).write_text(json.dumps(obj,sort_keys=True)+'\n')
lock=json.loads((package/'CONTINUATION_LOCK.json').read_text())
projection=(package/lock['baseline_reduction_projection']).read_bytes()
if case=='wrong_projection_bytes':projection+=b' '
(a.out/'NUMERICAL_PROJECTION.json').write_bytes(projection)
w('NUMERICAL_IDENTITY.json',{'NO_SCIENCE':True,'sha256':sh(a.out/'NUMERICAL_PROJECTION.json')})
w('RESULTS.json',{'NO_SCIENCE':True,'status':'PASS_SCOPED_POSTPROCESSING','failed_count':0,'disjoint_count':0,'source_sha256':'0'*64 if case=='wrong_producer_hash' else sh(Path(__file__)),'input_identities':{'current':{'sha256':'0'*64 if case=='stale_current_hash' else sh(a.current)}},'new_coefficient_evaluations':0,'new_native_or_gas_or_continuous_solves':0})
if case=='locked_payload_tamper_during':
 with (package/'inputs/PATH_CONTROLS.json').open('a') as f:f.write('NO_SCIENCE_TAMPER')
if case=='lock_metadata_tamper_during':
 lock['NO_SCIENCE_MUTATED_DURING_CHILD']=True
 (package/'CONTINUATION_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
print('NO_SCIENCE synthetic reduction child '+case,flush=True)
"""
def main():
 W.mkdir(parents=True,exist_ok=True)
 raw_wrapper=(P/'code/ncp_continue.py').read_bytes();original_sha=hashlib.sha256(raw_wrapper).hexdigest()
 real_lock=json.loads((P/'CONTINUATION_LOCK.json').read_text())
 paths=[e['path'] for e in real_lock['files']]
 assert len(paths)==19 and len(set(paths))==19
 base_projection=real_lock['baseline_reduction_projection']
 contract={'NO_SCIENCE':True,'role':'independent synthetic infrastructure controls, not physics review','started_utc':now(),'source_path':str(P/'code/ncp_continue.py'),'source_sha256':original_sha,'original_source_bytes':len(raw_wrapper),'cases':[dict(name=n,execute=x,expected_success=s,expected_reduction_mock_calls=r) for n,x,s,r in CASES],'real_science_invocations':0,'remote_mutations':0,'write_scope':str(W)}
 write(W/'CONTRACT.json',contract)
 results=[]
 for name,execute,expected_success,expected_reductions in CASES:
  c=W/'cases'/name;c.mkdir(parents=True,exist_ok=False);package=c/'package';package.mkdir()
  for rel in paths:
   dest=package/rel;dest.parent.mkdir(parents=True,exist_ok=True)
   if rel=='code/ncp_continue.py':dest.write_bytes(raw_wrapper)
   elif rel=='code/ncp_execute.py':dest.write_text(MOCK_PHYSICS)
   elif rel=='code/lineage_reduction.py':dest.write_text(MOCK_REDUCTION)
   elif rel==base_projection:dest.write_text('{"NO_SCIENCE":true,"projection":[1,2,3]}\n')
   else:write(dest,{'NO_SCIENCE':True,'fixture_placeholder':rel})
  fixture_lock={'schema':'NO_SCIENCE_SYNTHETIC_CONTINUATION_LOCK','files':[{'path':rel,'bytes':(package/rel).stat().st_size,'sha256':sha(package/rel)} for rel in paths],'baseline_physics_numerical_sha256':hashlib.sha256(b'NO_SCIENCE synthetic numerical projection').hexdigest(),'baseline_reduction_projection':base_projection,'baseline_reduction_projection_file_sha256':sha(package/base_projection),'NO_SCIENCE':True}
  write(package/'CONTINUATION_LOCK.json',fixture_lock)
  start_lock_sha=sha(package/'CONTINUATION_LOCK.json')
  if name=='locked_payload_tamper_before':
   with (package/'inputs/PATH_CONTROLS.json').open('a') as f:f.write('NO_SCIENCE_TAMPER')
  out=c/'out'
  if name=='existing_out_collision':
   out.mkdir();(out/'PRESERVE_EXISTING.txt').write_text('NO_SCIENCE existing output must remain\n')
  cmd=[sys.executable,'-B',str(package/'code/ncp_continue.py'),'--package',str(package),'--out',str(out)]
  if execute:cmd.append('--execute')
  env=os.environ.copy();env['BASS_HE_CONTINUATION_FIXTURE_CASE']=name
  # Do not hide an MPI environment: wrapper must reject one if actually present.
  record={'NO_SCIENCE':True,'case':name,'argv':cmd,'started_utc':now(),'wrapper_sha256_before':sha(package/'code/ncp_continue.py'),'lock_sha256_before':start_lock_sha,'actual_fixture_exit':None}
  write(c/'RUN_START.json',record)
  begin=time.perf_counter()
  with (c/'wrapper_stdout.txt').open('xb') as stdout,(c/'wrapper_stderr.txt').open('xb') as stderr:
   run=subprocess.run(cmd,stdout=stdout,stderr=stderr,env=env,timeout=20)
  record.update(finished_utc=now(),wall_seconds=time.perf_counter()-begin,actual_fixture_exit=run.returncode,wrapper_sha256_after=sha(package/'code/ncp_continue.py'),lock_sha256_after=sha(package/'CONTINUATION_LOCK.json'))
  write(c/'RUN_FINISH.json',record)
  callpath=out/'SYNTHETIC_CHILD_INVOCATIONS.jsonl'
  calls=[json.loads(line) for line in callpath.read_text().splitlines()] if callpath.exists() else []
  nred=sum(x['child']=='reduction_mock' for x in calls)
  result_path=out/'NCP_CONTINUATION_RESULT.json'
  report=json.loads(result_path.read_text()) if result_path.exists() else None
  success=run.returncode==0
  assertions={
   'expected_exit_class':success==expected_success,
   'expected_reduction_mock_call_count':nred==expected_reductions,
   'wrapper_copy_unchanged':record['wrapper_sha256_before']==record['wrapper_sha256_after']==original_sha,
   'mock_calls_labeled_NO_SCIENCE':all(x.get('NO_SCIENCE') is True for x in calls),
   'no_retry':sum(x['child']=='physics_mock' for x in calls)<=1 and nred<=1,
  }
  if name=='verify_only':
   assertions['default_zero_mock_science_count']=report['actual_new_host_physics_invocations']==0 and report['actual_exact_reduction_invocations']==0 and report['status']=='VERIFY_ONLY_READY'
  if name=='existing_out_collision':
   assertions['existing_marker_preserved']=(out/'PRESERVE_EXISTING.txt').read_text()=='NO_SCIENCE existing output must remain\n'
   assertions['no_child_started']=len(calls)==0
  row={'NO_SCIENCE':True,'case':name,'actual_fixture_exit':run.returncode,'wall_seconds':record['wall_seconds'],'expected_success':expected_success,'actual_success':success,'mock_physics_child_calls':sum(x['child']=='physics_mock' for x in calls),'mock_reduction_child_calls':nred,'wrapper_report_status':None if report is None else report['status'],'wrapper_report_error':None if report is None else report.get('error'),'assertions':assertions,'passed':all(assertions.values()),'evidence_dir':str(c)}
  results.append(row)
  print(json.dumps(row),flush=True)
 final={'NO_SCIENCE':True,'status':'PASS_SYNTHETIC_BOUNDARIES' if all(x['passed'] for x in results) else 'FINDING_REQUIRES_OWNER_TRIAGE','source_sha256':original_sha,'finished_utc':now(),'cases':results,'passed_cases':sum(x['passed'] for x in results),'total_cases':len(results),'real_science_invocations':0,'actual_NCP_host_jobs':0,'remote_mutations':0,'original_main_wrapper_unchanged':sha(P/'code/ncp_continue.py')==original_sha,'warning':'Fixture wrapper reports simulate scientific status strings; no scientific child code was copied or executed.'}
 write(W/'RESULTS.json',final)
 manifest=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(W.rglob('*')) if p.is_file() and p.name!='FILE_MANIFEST.json']
 write(W/'FILE_MANIFEST.json',{'NO_SCIENCE':True,'files':manifest,'excludes':['FILE_MANIFEST.json']})
 return 0 if all(x['passed'] for x in results) else 1
if __name__=='__main__':raise SystemExit(main())

