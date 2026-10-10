#!/usr/bin/env python3
"""Record bounded independent-control subprocess executions without retries."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time


def stamp():
    return datetime.now(timezone.utc).isoformat()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--record-dir', type=Path, required=True)
    p.add_argument('--timeout', type=float, default=30)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command[:1] == ['--'] else a.command
    if not command:
        raise SystemExit('missing command')
    a.record_dir.mkdir(parents=True, exist_ok=False)
    sources = []
    for arg in command:
        path = Path(arg)
        if path.is_file():
            sources.append({'path': str(path.resolve()), 'bytes': path.stat().st_size,
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    start = {'schema': 'bass-he-e13c5-control-execution-v1', 'started_utc': stamp(),
             'command': command, 'cwd': os.getcwd(), 'python': platform.python_version(),
             'source_identity': sources, 'timeout_seconds': a.timeout,
             'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (a.record_dir/'START.json').write_text(json.dumps(start, indent=2)+'\n')
    before = time.perf_counter()
    try:
        with (a.record_dir/'stdout.txt').open('wb') as stdout, (a.record_dir/'stderr.txt').open('wb') as stderr:
            child = subprocess.run(command, stdout=stdout, stderr=stderr,
                                   timeout=a.timeout, check=False)
        exit_code = child.returncode
        status = 'COMPLETED'
    except subprocess.TimeoutExpired:
        exit_code = 124
        status = 'TIMEOUT'
    final = dict(start, finished_utc=stamp(), elapsed_seconds=time.perf_counter()-before,
                 actual_exit_code=exit_code, process_status=status,
                 child_ru_maxrss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (a.record_dir/'FINISH.json').write_text(json.dumps(final, indent=2)+'\n')
    print(json.dumps(final))
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
