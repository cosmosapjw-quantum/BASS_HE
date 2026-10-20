"""Focused controller tests: fake children only, no HE29/native integration."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('controller', HERE / 'src/continue_missing_references.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
WATCHDOG = HERE / 'tests/vendor/execution.py'
spec2 = importlib.util.spec_from_file_location('original_watchdog', WATCHDOG)
ex = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(ex)


def rows():
    return {'global_errors': [], 'complete': False, 'cases': [
        {'key': c.key(*j), 'status': 'ABSENT', 'files': {}, 'admitted': False,
         'cohort_id': None} for j in c.JOBS]}


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'references'; self.root.mkdir()
        self.out = Path(self.tmp.name) / 'controller'; self.out.mkdir()
    def tearDown(self):
        self.tmp.cleanup()

    def test_original_watchdog_pin(self):
        self.assertEqual(c.digest(WATCHDOG), c.EXECUTION_SHA)

    def test_any_occupied_path_is_preserved(self):
        r = rows(); (self.root / r['cases'][0]['key']).mkdir()
        (self.root / (r['cases'][1]['key'] + '_process')).write_text('malformed')
        (self.root / r['cases'][2]['key']).symlink_to(self.root / 'nonexistent')
        p = c.build_plan(self.root, r, {})
        self.assertEqual(p['never_started'], [c.key(4,1024)])
        self.assertTrue(all(x['action']=='PRESERVE_OCCUPIED_HOLD' for x in p['cases'][:3]))

    def test_cohort_mismatch_blocks_dispatch(self):
        r = rows(); r['cases'][0].update(cohort_id='a', cohort_identity={'runtime':'old'}, admitted=True)
        (self.root / c.key(2,512)).mkdir()
        p = c.build_plan(self.root, r, {'runtime':'new'})
        self.assertFalse(p['execution_allowed'])
        with self.assertRaisesRegex(ValueError,'COHORT'):
            c.dispatch_absent(self.root,p,run_process=lambda *a: self.fail('must not launch'),
                command_for=None,case_wall_s=1,classify=None,write_json=None,out=self.out)

    def test_original_shorter_budget_cannot_be_reset(self):
        d={'jobs':[list(x) for x in c.JOBS], 'concurrency':1, 'stop_on_first_failure':True,
           'integration_rtol':1e-10,'integration_atol_scaled':1e-12,'per_case_wall_s':17}
        (self.root/'DESIGN.json').write_text(json.dumps(d))
        read=lambda p:json.loads(p.read_text())
        self.assertEqual(c.original_budget(self.root,read)[0],17)
        self.assertEqual(c.original_budget(self.root,read,12)[0],12)
        for wrong in [18,3600,0,float('nan')]:
            with self.assertRaises(ValueError):c.original_budget(self.root,read,wrong)

    def test_completed_and_partial_cases_never_dispatched(self):
        r=rows()
        for i in (0,1): (self.root/r['cases'][i]['key']).mkdir()
        r['cases'][0].update(admitted=True,status='COMPLETE_VALID',cohort_id='a',cohort_identity={})
        r['cases'][1]['status']='METHOD_ONLY'
        p=c.build_plan(self.root,r,{})
        seen=[]
        def run(argv,dst,timeout):
            seen.append(argv[0]);dst.mkdir();(self.root/argv[0]).mkdir()
            return {'returncode':0,'timed_out':False,'wall_s':0}
        def classify():
            x=rows()
            for row in x['cases']:row['admitted']=row['key'] in seen
            return x
        c.dispatch_absent(self.root,p,run_process=run,command_for=lambda r,n:[c.key(r,n)],
            case_wall_s=2,classify=classify,write_json=ex.atomic_json,out=self.out)
        self.assertEqual(seen,[c.key(8,512),c.key(4,1024)])

    def test_fake_child_failure_stops_at_first(self):
        p=c.build_plan(self.root,rows(),{})
        records=c.dispatch_absent(self.root,p,
            run_process=lambda a,d,t:c.run_process_group(a,d,t,execution=ex),
            command_for=lambda r,n:[sys.executable,'-c','raise SystemExit(7)'],
            case_wall_s=2,classify=rows,write_json=ex.atomic_json,out=self.out)
        self.assertEqual(len(records),1)
        self.assertEqual(records[0]['process']['returncode'],7)
        self.assertTrue((self.root/(c.key(2,512)+'_process/RECEIPT.json')).is_file())

    def test_original_watchdog_times_out_fake_child(self):
        p=c.build_plan(self.root,rows(),{})
        records=c.dispatch_absent(self.root,p,
            run_process=lambda a,d,t:c.run_process_group(a,d,t,execution=ex),
            command_for=lambda r,n:[sys.executable,'-c','import time; time.sleep(10)'],
            case_wall_s=.08,classify=rows,write_json=ex.atomic_json,out=self.out)
        self.assertEqual(len(records),1);self.assertTrue(records[0]['process']['timed_out'])
        self.assertLess(records[0]['process']['wall_s'],4)

    def test_timeout_kills_descendant_after_leader_exits(self):
        pidfile=Path(self.tmp.name)/'descendant.pid'
        script='''import os,signal,time,sys
pid=os.fork()
if pid==0:
 signal.signal(signal.SIGTERM,signal.SIG_IGN)
 with open(sys.argv[1],'w') as f:f.write(str(os.getpid()));f.flush();os.fsync(f.fileno())
 while True:time.sleep(1)
while True:time.sleep(1)
'''
        descendant=None
        try:
            info=c.run_process_group([sys.executable,'-c',script,str(pidfile)],
                                     self.root/'descendant_process',.25,execution=ex)
            self.assertTrue(info['timed_out'])
            self.assertTrue(info['timeout_residual_group_sigkill_sent'])
            descendant=int(pidfile.read_text())
            deadline=time.monotonic()+2
            while time.monotonic()<deadline:
                stat=Path(f'/proc/{descendant}/stat')
                if not stat.exists() or stat.read_text().split(') ',1)[1].split()[0]=='Z':break
                time.sleep(.01)
            else:self.fail('TERM-resistant descendant survived timeout cleanup')
        finally:
            if pidfile.exists():
                descendant=int(pidfile.read_text())
                try:os.kill(descendant,9)
                except ProcessLookupError:pass

    def test_new_occupancy_between_plan_and_dispatch_stops(self):
        p=c.build_plan(self.root,rows(),{})
        (self.root/(c.key(2,512)+'_process')).mkdir()
        records=c.dispatch_absent(self.root,p,run_process=lambda *a:self.fail('must not run'),
            command_for=None,case_wall_s=1,classify=None,write_json=None,out=self.out)
        self.assertEqual(records,[{'case':c.key(2,512),'status':'BECAME_OCCUPIED_HOLD'}])

    def test_same_campaign_lock_excludes_second_controller(self):
        with c.campaign_lock(self.root):
            with self.assertRaises(BlockingIOError):
                with c.campaign_lock(self.root):pass

    def test_visible_original_campaign_found_without_killing(self):
        proc=Path(self.tmp.name)/'proc';proc.mkdir();p=proc/'424242';p.mkdir()
        (p/'cmdline').write_bytes(b'python\0/old/source/reference_runner.py\0campaign\0--out\0'+str(self.root).encode()+b'\0')
        found=c.active_original_runners('/new/source/reference_runner.py',self.root,proc)
        self.assertEqual(found,[{'pid':424242,'output':str(self.root)}])

    def test_source_drift_rejected_before_import(self):
        p=Path(self.tmp.name)/'bad.py';p.write_text('raise RuntimeError("must not import")')
        with self.assertRaisesRegex(ValueError,'SOURCE_IDENTITY'):c.require_hash(p,c.RUNNER_SHA)


if __name__=='__main__':unittest.main()
