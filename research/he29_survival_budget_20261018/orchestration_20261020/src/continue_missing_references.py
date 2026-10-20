"""Run only never-started HE29 cases in an existing original campaign.

The physical runner and admission are reused. A local watchdog correction
also kills residual group members after the leader exits during timeout.
Any occupied case/process path is preserved, including malformed/partial data.
Default is read-only planning; --execute enables absent-case dispatch only.
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

JOBS = ((2, 512), (4, 512), (8, 512), (4, 1024))
RUNNER_SHA = 'dabb4968e5247815b8d19c31d792187bad497b23bf2028ce2539613ed527ff7e'
EXECUTION_SHA = '876e43d76f0773a8d2c38e262902442c614a68334561f5e2a78024c659edb1c4'
CLASSIFIER_SHA = 'b1c7ece60f5c2e9c86ca50f006aeaca3cc04f7ff418467f3a96f72fb27f7f9f3'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def require_hash(path, expected):
    if not Path(path).is_file() or Path(path).is_symlink() or digest(path) != expected:
        raise ValueError('HE29_CONTROLLER_SOURCE_IDENTITY: ' + str(path))


def key(r, nodes):
    return f'm8_r{r}_table{nodes}'


def occupied(root, name):
    return any(p.exists() or p.is_symlink()
               for p in (Path(root) / name, Path(root) / (name + '_process')))


def run_process_group(argv, destination, timeout_s, *, execution):
    """Original process/evidence contract with descendant timeout cleanup.

    Waiting for the session leader does not reap or stop its descendants.
    Always signal the remaining group with KILL after a timeout, even when
    the leader already exited in response to TERM. No old process is targeted.
    """
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise ValueError('HE29_TIMEOUT_DOMAIN')
    dst = Path(destination); dst.mkdir(parents=True, exist_ok=False)
    execution.atomic_json(dst / 'COMMAND.json', {'argv': list(map(str, argv)), 'timeout_s': timeout_s})
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    env.update(OMP_DYNAMIC='FALSE', OMP_PLACES='cores', OMP_PROC_BIND='close')
    start = time.monotonic(); timed_out = False; killed_group = False
    with (dst / 'stdout.log').open('xb') as stdout, (dst / 'stderr.log').open('xb') as stderr:
        p = subprocess.Popen(list(map(str, argv)), stdout=stdout, stderr=stderr,
                             start_new_session=True, env=env)
        try:
            try:
                code = p.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    p.wait(timeout=3.)
                except subprocess.TimeoutExpired:
                    pass
                # The leader may already be reaped, while a native descendant
                # is still alive in the original process group.
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                    killed_group = True
                except ProcessLookupError:
                    pass
                code = p.wait()
        except BaseException:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()
            raise
        stdout.flush(); stderr.flush(); os.fsync(stdout.fileno()); os.fsync(stderr.fileno())
    receipt = {'returncode': code, 'timed_out': timed_out, 'wall_s': time.monotonic() - start,
               'stdout_sha256': execution.digest(dst / 'stdout.log'),
               'stderr_sha256': execution.digest(dst / 'stderr.log'),
               'watchdog': 'he29.missing_controller.group_cleanup.v1',
               'timeout_residual_group_sigkill_sent': killed_group,
               'cleanup_scope': 'created POSIX process group; descendants escaping the group are outside this mechanism'}
    execution.atomic_json(dst / 'RECEIPT.json', receipt)
    return receipt


def original_budget(root, read_json, requested=None):
    design = read_json(Path(root) / 'DESIGN.json')
    if design.get('jobs') != [list(x) for x in JOBS]:
        raise ValueError('HE29_ORIGINAL_CAMPAIGN_JOBS_REQUIRED')
    if (design.get('concurrency') != 1 or design.get('stop_on_first_failure') is not True
            or design.get('integration_rtol') != 1e-10
            or design.get('integration_atol_scaled') != 1e-12):
        raise ValueError('HE29_ORIGINAL_CAMPAIGN_CONTRACT_CHANGED')
    limit = design.get('per_case_wall_s')
    if type(limit) not in (int, float) or not math.isfinite(limit) or not 0 < limit <= 3600:
        raise ValueError('HE29_ORIGINAL_CASE_BUDGET_INVALID')
    if requested is not None:
        if not math.isfinite(requested) or not 0 < requested <= limit:
            raise ValueError('HE29_CASE_BUDGET_CANNOT_INCREASE')
        limit = requested
    return float(limit), design


def build_plan(root, classification, expected_cohort):
    if classification.get('global_errors'):
        raise ValueError('HE29_EXISTING_TRUST_OR_BINARY_FAILURE')
    cases = classification.get('cases', [])
    if [x.get('key') for x in cases] != [key(*x) for x in JOBS]:
        raise ValueError('HE29_CLASSIFICATION_CASE_SET')
    rows = []
    cohort_conflicts = []
    for row in cases:
        name = row['key']
        present = occupied(root, name)
        if row.get('cohort_id') is not None and row.get('cohort_identity') != expected_cohort:
            cohort_conflicts.append(name)
        if present:
            action = 'REUSE_ADMITTED' if row.get('admitted') else 'PRESERVE_OCCUPIED_HOLD'
        elif row.get('status') == 'ABSENT' and not row.get('files'):
            action = 'RUN_NEVER_STARTED'
        else:
            action = 'CLASSIFICATION_FILESYSTEM_CONFLICT_HOLD'
        rows.append({'case': name, 'action': action, 'observed_status': row.get('status'),
                     'admitted': bool(row.get('admitted')), 'occupied': present})
    return {'cases': rows, 'cohort_conflicts': cohort_conflicts,
            'execution_allowed': not cohort_conflicts and not any(
                x['action'] == 'CLASSIFICATION_FILESYSTEM_CONFLICT_HOLD' for x in rows),
            'never_started': [x['case'] for x in rows if x['action'] == 'RUN_NEVER_STARTED'],
            'preserved': [x['case'] for x in rows if x['occupied']],
            'budget_semantics': 'Original per-case budget only for absent case AND process paths; no occupied case is retried. No aggregate campaign deadline is reset.'}


def active_original_runners(runner, root, proc_root=Path('/proc')):
    """Observe visible Linux processes; do not send signals to old processes."""
    if not proc_root.is_dir():
        raise RuntimeError('HE29_PROCESS_OBSERVATION_REQUIRES_LINUX_PROC')
    runner, root = str(Path(runner).resolve()), Path(root).resolve()
    matches, denied = [], []
    for p in proc_root.iterdir():
        if not p.name.isdigit() or int(p.name) == os.getpid():
            continue
        try:
            args = (p / 'cmdline').read_bytes().decode(errors='replace').split('\0')
        except FileNotFoundError:
            continue
        except PermissionError:
            denied.append(int(p.name)); continue
        if (not any(Path(x).name == 'reference_runner.py' for x in args if x)
                or not any(x in args for x in ('case', 'campaign')) or '--out' not in args):
            continue
        try:
            output = Path(args[args.index('--out') + 1])
            if not output.is_absolute():
                output = (p / 'cwd').resolve(strict=True) / output
            output = output.resolve()
        except (IndexError, FileNotFoundError):
            continue
        if output == root or root in output.parents:
            matches.append({'pid': int(p.name), 'output': str(output)})
    if denied:
        raise RuntimeError('HE29_PROCESS_VISIBILITY_INCOMPLETE: ' + str(denied))
    return matches


@contextlib.contextmanager
def campaign_lock(root):
    path = Path(root) / '.he29_missing_controller.lock'
    if path.is_symlink():
        raise ValueError('HE29_CONTROLLER_LOCK_SYMLINK')
    with path.open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def dispatch_absent(root, plan, *, run_process, command_for, case_wall_s, classify, write_json, out):
    """Small orchestration seam: production supplies pinned original functions."""
    if not plan['execution_allowed']:
        raise ValueError('HE29_COHORT_OR_SNAPSHOT_CONFLICT')
    records = []
    for r, nodes in JOBS:
        name = key(r, nodes)
        if name not in plan['never_started']:
            continue
        # Recheck immediately before the original watchdog reserves its process dir.
        if occupied(root, name):
            records.append({'case': name, 'status': 'BECAME_OCCUPIED_HOLD'})
            break
        info = run_process(command_for(r, nodes), Path(root) / (name + '_process'), case_wall_s)
        records.append({'case': name, 'process': info})
        snapshot = classify()
        write_json(Path(out) / (name + '_CLASSIFICATION.json'), snapshot)
        result = next(x for x in snapshot['cases'] if x['key'] == name)
        if info['returncode'] != 0 or info['timed_out'] or not result.get('admitted'):
            break
    return records


def load_production(baseline, analysis):
    baseline, analysis = Path(baseline).resolve(), Path(analysis).resolve()
    execution = baseline.parent / 'he28_strip_refinement_20261018/src/execution.py'
    runner = baseline / 'src/reference_runner.py'
    classifier = analysis / 'continuation_20261020T0557Z/src/partial_returns.py'
    require_hash(execution, EXECUTION_SHA); require_hash(runner, RUNNER_SHA)
    require_hash(classifier, CLASSIFIER_SHA)
    sys.path[:0] = [str(baseline / 'src'), str(classifier.parent)]
    pr = importlib.import_module('partial_returns')
    for relative, sha in pr.SCIENCE_SOURCES.items():
        require_hash(baseline / relative, sha)
    require_hash(analysis / 'src/reference_contract.py', pr.SCIENCE_SOURCES['src/reference_contract.py'])
    # partial_returns prepends its own source root; runner must use baseline DATA.
    sys.path.insert(0, str(baseline / 'src'))
    rr = importlib.import_module('reference_runner')
    ex = importlib.import_module('execution')
    if Path(ex.__file__).resolve() != execution or Path(rr.__file__).resolve() != runner:
        raise ValueError('HE29_IMPORTED_WATCHDOG_PATH')
    return rr, pr, ex, runner


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline-root', required=True, help='Original1569 HE29 source with both published overlays and verified DATA')
    ap.add_argument('--analysis-root', required=True, help='HE29 source at09929b0 or byte-identical successor containing classifier')
    ap.add_argument('--root', required=True, help='Existing original references/ directory; its DESIGN is immutable')
    ap.add_argument('--binary', required=True); ap.add_argument('--receipt', required=True)
    ap.add_argument('--out', required=True, help='New controller evidence directory')
    ap.add_argument('--case-wall-s', type=float)
    ap.add_argument('--execute', action='store_true')
    args = ap.parse_args(argv)
    root, out = Path(args.root).resolve(), Path(args.out).resolve()
    if not root.is_dir():
        ap.error('existing original references root required')
    if out == root or root in out.parents:
        ap.error('controller output must be outside original references root')
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    ex = None
    try:
        rr, pr, ex, runner = load_production(args.baseline_root, args.analysis_root)
        limit, design = original_budget(root, pr.read_json, args.case_wall_s)
        state = rr.check_sources(args.binary, args.receipt)
        expected = {k: state[k] for k in pr.COHORT_FIELDS}
        expected['runtime'] = {k: state['runtime'][k] for k in ('python', 'numpy', 'scipy')}
        classify = lambda: pr.classify_campaign(root, binary=args.binary, data_root=args.baseline_root)
        before = classify()
        plan = build_plan(root, before, expected)
        processes = active_original_runners(runner, root)
        ex.atomic_json(out / 'BEFORE.json', before)
        ex.atomic_json(out / 'PLAN.json', {**plan, 'case_wall_s': limit,
            'original_design_sha256': digest(root / 'DESIGN.json'), 'visible_active_original_runners': processes,
            'baseline_root': str(Path(args.baseline_root).resolve()), 'analysis_root': str(Path(args.analysis_root).resolve()),
            'binary_sha256': state['binary_sha256'], 'source_files': state['source_files'],
            'mode': 'execute' if args.execute else 'plan', 'native_calls_in_planning': 0})
        if not args.execute:
            return 0 if plan['execution_allowed'] and not processes else 1
        if processes:
            raise RuntimeError('HE29_EXISTING_ORIGINAL_PROCESS_ACTIVE')
        with campaign_lock(root):
            # A second controller may have finished between initial intake and lock.
            plan = build_plan(root, classify(), expected)
            if active_original_runners(runner, root):
                raise RuntimeError('HE29_EXISTING_ORIGINAL_PROCESS_ACTIVE')
            def command_for(r, nodes):
                return [sys.executable, str(runner), 'case', '--out', str(root / key(r, nodes)),
                        '--binary', str(Path(args.binary).resolve()), '--receipt', str(Path(args.receipt).resolve()),
                        '--strips', str(r), '--table-nodes', str(nodes)]
            records = dispatch_absent(root, plan,
                                     run_process=lambda argv, dst, timeout: run_process_group(argv, dst, timeout, execution=ex),
                                     command_for=command_for,
                                     case_wall_s=limit, classify=classify, write_json=ex.atomic_json, out=out)
        after = classify()
        ex.atomic_json(out / 'AFTER.json', after)
        ex.atomic_json(out / 'SUMMARY.json', {'schema': 'he29.missing_controller.v1', 'records': records,
            'started_cases': len([x for x in records if 'process' in x]), 'complete': after['complete'],
            'admitted_pairs': after['admitted_pairs'], 'case_wall_s': limit,
            'wall_s': time.monotonic() - started, 'old_cases_replayed': 0,
            'old_design_and_summary_rewritten': False, 'original_campaign': str(root),
            'physical_claim': 'Same finite HE29 reference admission only',
            'watchdog_grace': 'SIGTERM wait up to3s then residual-group SIGKILL even if leader exited; case_wall_s is wait budget, not a hard total-wall certificate'})
        return 0 if after['complete'] else 1
    except BaseException as exc:
        failure = {'error': repr(exc), 'wall_s': time.monotonic() - started,
            'old_cases_replayed': 0, 'remaining_action': 'Inspect retained records; occupied cases are not automatically retried'}
        if ex is not None:
            ex.atomic_json(out / 'FAILURE.json', failure)
        else:
            # Source import failures still have a create-only record; no imported
            # code from an unverified source is used to create this record.
            with (out / 'FAILURE.json').open('x') as f:
                json.dump(failure, f, indent=2, allow_nan=False)
                f.write('\n'); f.flush(); os.fsync(f.fileno())
        raise


if __name__ == '__main__':
    raise SystemExit(main())
