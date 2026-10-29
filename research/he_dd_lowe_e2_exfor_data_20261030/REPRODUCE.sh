#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 src/build_source_atlas.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m compileall -q src tests
g++ -std=c++20 -O2 -Wall -Wextra -Werror -pedantic tests/independent_cpp_source.cpp -o /tmp/bass_he_exfor_lowE_independent
/tmp/bass_he_exfor_lowE_independent sources
python3 src/plot_sources.py
