#!/usr/bin/env python3
"""Run the reviewed two-track host parity job, then exact PR19 reconciliation.

Default is verify-only. --execute authorizes exactly one bounded physics
invocation and one sequential exact saved-output reduction on its fresh result.
This runner never publishes, merges, retries, or expands the selected paths.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def safe_file(package, relative):
    path = (package / relative).resolve()
    if not path.is_relative_to(package) or not path.is_file():
        raise ValueError('missing or invalid package file: ' + relative)
    return path


def check_lock(package, lock):
    rows = []
    for entry in lock['files']:
        path = safe_file(package, entry['path'])
        actual = sha(path)
        passed = actual == entry['sha256'] and path.stat().st_size == entry['bytes']
        rows.append({'path': entry['path'], 'sha256': actual, 'pass': passed})
        if not passed:
            raise ValueError('continuation lock mismatch: ' + entry['path'])
    return rows


def run_child(command, label, out, timeout, env):
    record = {'label': label, 'command': command, 'started_utc': now(),
              'timeout_seconds': timeout, 'memory_limit_bytes': 1073741824,
              'actual_exit': None, 'status': 'RUNNING'}
    write(out / (label + '_RUN.json'), record)
    def limits():
        resource.setrlimit(resource.RLIMIT_AS, (1073741824, 1073741824))
    start = time.perf_counter()
    try:
        with (out / (label + '_stdout.txt')).open('x') as stdout, \
             (out / (label + '_stderr.txt')).open('x') as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                       env=env, start_new_session=True, preexec_fn=limits)
            try:
                record['actual_exit'] = process.wait(timeout=timeout)
                record['status'] = 'EXITED'
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                record['status'] = 'TIMEOUT'
                raise RuntimeError(label + ' timeout; preserve first failure, no retry')
            finally:
                stdout.flush(); stderr.flush()
                os.fsync(stdout.fileno()); os.fsync(stderr.fileno())
        if record['actual_exit'] != 0:
            raise RuntimeError(label + ' exited nonzero; see preserved raw evidence')
        return record
    finally:
        record.update(finished_utc=now(), wall_seconds=time.perf_counter() - start)
        write(out / (label + '_RUN.json'), record)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    package = args.package.resolve()
    out = args.out.absolute()
    out.mkdir(parents=True, exist_ok=False)
    report = {'node': 'NCP_E13C5_PR19_REFINEMENT_PARITY_AND_REDUCTION',
              'started_utc': now(), 'execute_requested': args.execute, 'status': 'INTAKE',
              'actual_new_host_physics_invocations': 0,
              'actual_exact_reduction_invocations': 0,
              'actual_native_runs': 0, 'actual_gas_advances': 0,
              'actual_old_continuous_solves': 0, 'actual_full_first2_runs': 0,
              'physical': 'HOLD', 'production': 'HOLD',
              'receiver_execution_ack': 'SEPARATE', 'host_role': 'EXECUTING_HOST_NOT_PROVIDER_ATTESTED',
              'selected_scope': 'two OFF N512 paths; prior 12-path evidence reduced separately by OFF/KF/GM'}
    write(out / 'NCP_CONTINUATION_RESULT.json', report)
    try:
        lock_path = package / 'CONTINUATION_LOCK.json'
        initial_lock_sha = sha(lock_path)
        lock = read(lock_path)
        before = check_lock(package, lock)
        write(out / 'CONTINUATION_IDENTITY.json', {'lock_sha256': initial_lock_sha, 'files': before})
        if platform.python_implementation() != 'CPython' or sys.version_info[:2] != (3, 12):
            raise RuntimeError('CPython 3.12.x is required; choose installed matching interpreter')
        for variable in ('OMPI_COMM_WORLD_SIZE', 'PMI_SIZE', 'SLURM_NTASKS'):
            if os.environ.get(variable) and int(os.environ[variable]) > 1:
                raise RuntimeError('single-process job required; parallel launcher detected: ' + variable)
        if sha(safe_file(package, lock['baseline_reduction_projection'])) != lock['baseline_reduction_projection_file_sha256']:
            raise ValueError('saved reduction projection identity mismatch')
        env = os.environ.copy()
        for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            env[variable] = '1'
        physics = out / 'physics'
        command = [sys.executable, str(package / 'code/ncp_execute.py'),
                   '--package', str(package), '--out', str(physics)]
        if args.execute:
            command.append('--execute')
        report['status'] = 'PHYSICS_HOST_STAGE'
        write(out / 'NCP_CONTINUATION_RESULT.json', report)
        run_child(command, 'PHYSICS_HOST', out, 205, env)
        first = read(physics / 'NCP_RESULT.json')
        report['actual_new_host_physics_invocations'] = first['new_host_scientific_runs']
        if not args.execute:
            if first['status'] != 'VERIFY_ONLY_PASS' or first['new_host_scientific_runs'] != 0:
                raise RuntimeError('verify-only stage did not remain verify-only')
            report.update(status='VERIFY_ONLY_READY', scientific_execution='NOT_RUN',
                          exact_reduction_execution='NOT_RUN', new_result_accuracy='NOT_EVALUATED')
        else:
            parity = read(physics / 'PARITY.json')
            if not (first['status'] == 'PASS_SCOPED_HOST_PARITY'
                    and first['scientific_execution'] == 'ACTUALLY_EXECUTED'
                    and first['new_host_scientific_runs'] == 1
                    and parity['fresh_output_compared'] is True
                    and parity['fresh_as_run_source_matches_execution_lock'] is True
                    and parity['bitwise_numerical_json_parity'] is True
                    and parity['actual_numerical_sha256'] == lock['baseline_physics_numerical_sha256']):
                raise RuntimeError('fresh physics execution/identity/parity gate failed')
            fresh = physics / 'RESULTS.json'
            fresh_sha = sha(fresh)
            reduction = out / 'reduction'
            command = [sys.executable, str(package / 'code/lineage_reduction.py'),
                       '--prior', str(package / 'inputs/pr19_lineage/first2/RESULTS.json'),
                       '--prior-start', str(package / 'inputs/pr19_lineage/first2/START.json'),
                       '--prior-code', str(package / 'inputs/pr19_lineage/first2/cover.py'),
                       '--pilot', str(package / 'inputs/pr19_lineage/pilot/RESULTS.json'),
                       '--controls', str(package / 'inputs/PATH_CONTROLS.json'),
                       '--current', str(fresh), '--out', str(reduction)]
            report.update(status='EXACT_REDUCTION_STAGE', actual_exact_reduction_invocations=1,
                          fresh_physics_result_sha256=fresh_sha)
            write(out / 'NCP_CONTINUATION_RESULT.json', report)
            run_child(command, 'EXACT_REDUCTION', out, 60, env)
            result = read(reduction / 'RESULTS.json')
            identity = read(reduction / 'NUMERICAL_IDENTITY.json')
            projection_path = reduction / 'NUMERICAL_PROJECTION.json'
            projection_sha = sha(projection_path)
            required_source = next(e['sha256'] for e in lock['files'] if e['path'] == 'code/lineage_reduction.py')
            if not (result['status'] == 'PASS_SCOPED_POSTPROCESSING' and result['failed_count'] == 0
                    and result['disjoint_count'] == 0
                    and result['source_sha256'] == required_source
                    and result['input_identities']['current']['sha256'] == fresh_sha
                    and sha(fresh) == fresh_sha
                    and projection_sha == identity['sha256']
                    and projection_sha == lock['baseline_reduction_projection_file_sha256']
                    and result['new_coefficient_evaluations'] == 0
                    and result['new_native_or_gas_or_continuous_solves'] == 0):
                raise RuntimeError('exact reduction result/identity/projection gate failed')
            report.update(status='PASS_SCOPED_HOST_PARITY_AND_REDUCTION',
                          scientific_execution='ACTUALLY_EXECUTED_ON_RECORDED_HOST',
                          exact_reduction_execution='ACTUALLY_EXECUTED_ON_FRESH_PHYSICS_RESULT',
                          fresh_reduction_projection_sha256=projection_sha,
                          new_result_accuracy='SCOPED_PARITY_AND_EXACT_REDUCTION_PASS')
        after = check_lock(package, lock)
        if sha(lock_path) != initial_lock_sha:
            raise RuntimeError('continuation lock metadata changed during run')
        if before != after:
            raise RuntimeError('locked package changed during run')
        report['source_unchanged_during_run'] = True
    except Exception as error:
        report.update(status='FAILED', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        first_result = out / 'physics/NCP_RESULT.json'
        if first_result.is_file():
            report['actual_new_host_physics_invocations'] = read(first_result).get('new_host_scientific_runs', 0)
        report['finished_utc'] = now()
        write(out / 'NCP_CONTINUATION_RESULT.json', report)
        files = [{'path': str(path.relative_to(out)), 'bytes': path.stat().st_size, 'sha256': sha(path)}
                 for path in sorted(out.rglob('*')) if path.is_file() and path.name != 'RETURN_MANIFEST.json']
        write(out / 'RETURN_MANIFEST.json', {'files': files, 'excludes': ['RETURN_MANIFEST.json']})
        print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
