#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
P="$(cd "$D/../he_dd_fastd_nrl_20261031" && pwd)"
cd "$D"
export PYTHONPATH="$P/src:$D/src"
export MPLBACKEND=Agg
export SOURCE_DATE_EPOCH=1793404800
python -m compileall -q src tests
python src/generate.py
python src/plot.py
python src/audit_saved_data.py
python -m unittest discover -s tests -v
