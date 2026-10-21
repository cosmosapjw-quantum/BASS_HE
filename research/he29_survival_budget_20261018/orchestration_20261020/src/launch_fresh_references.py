"""Fresh-only HE29 launcher for the additive bootstrap watchdog overlay.

This creates the original immutable DESIGN and delegates every case to the
same absent-only controller. Existing roots are always rejected.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
import continue_missing_references as controller


def create_design(root, limit, write_json):
    if not math.isfinite(limit) or not 0 < limit <= 3600:
        raise ValueError('HE29_ORIGINAL_CASE_BUDGET_INVALID')
    root = Path(root)
    root.mkdir(parents=True, exist_ok=False)
    write_json(root / 'DESIGN.json', {
        'jobs': [list(j) for j in controller.JOBS], 'integration_rtol': 1e-10,
        'integration_atol_scaled': 1e-12, 'per_case_wall_s': limit,
        'concurrency': 1, 'stop_on_first_failure': True,
        'reason': 'same-r/same-table error separation; no repeats of completed transport'})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ('baseline-root', 'analysis-root', 'root', 'binary', 'receipt', 'out'):
        ap.add_argument('--' + key, required=True)
    ap.add_argument('--case-wall-s', type=float, default=3600.)
    args = ap.parse_args(argv)
    root, out = Path(args.root).resolve(), Path(args.out).resolve()
    if root.exists() or root.is_symlink() or out.exists() or out.is_symlink():
        ap.error('fresh references and controller evidence paths must both be absent')
    if out == root or root in out.parents:
        ap.error('controller evidence must be outside references')
    rr, _, ex, runner = controller.load_production(args.baseline_root, args.analysis_root)
    rr.check_sources(args.binary, args.receipt)
    if controller.active_original_runners(runner, root):
        raise RuntimeError('HE29_EXISTING_ORIGINAL_PROCESS_ACTIVE')
    create_design(root, args.case_wall_s, ex.atomic_json)
    return controller.main([
        '--baseline-root', args.baseline_root, '--analysis-root', args.analysis_root,
        '--root', str(root), '--binary', args.binary, '--receipt', args.receipt,
        '--out', str(out), '--execute'])


if __name__ == '__main__':
    raise SystemExit(main())
