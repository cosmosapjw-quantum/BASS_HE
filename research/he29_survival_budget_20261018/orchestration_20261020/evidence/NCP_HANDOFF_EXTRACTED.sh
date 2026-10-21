: "${HE29_CTRL_REPO:?published controller checkout required}"
: "${HE29_ANALYSIS_REPO:?09929 analysis checkout required}"
HE29_REL=research/he29_survival_budget_20261018
export HE29_CTRL_ROOT="$HE29_CTRL_REPO/$HE29_REL/orchestration_20261020"
export HE29_ANALYSIS_ROOT="$HE29_ANALYSIS_REPO/$HE29_REL"
HE29_THIRD_PATCH="$HE29_CTRL_ROOT/ncp/USE_BOUNDED_CONTROLLER_20261020.patch"
printf '%s  %s\n' a93632cfaa2ce2f81b5dfe49694862e7b6d48bd81cbf9aa4ceedf5e2d8607f4f "$HE29_THIRD_PATCH" | sha256sum -c -
printf '%s  %s\n' 11d0ad0125f40a2890dac82e5103f13d17e6066f41440eabb06c7a8b1f319bc2 "$HE29_REL/ncp/BOOTSTRAP_REFERENCES.sh" | sha256sum -c -
git apply --check "$HE29_THIRD_PATCH"
git apply "$HE29_THIRD_PATCH"
printf '%s  %s\n' 90d36ef7098caa0d6dfa5453ab306a2fc3143be4658a486b434a227dba895234 "$HE29_REL/ncp/BOOTSTRAP_REFERENCES.sh" | sha256sum -c -

set -euo pipefail
: "${HE29_BASELINE_REPO:?existing original baseline checkout required}"
: "${HE29_EXISTING_WORK:?existing campaign work root required}"
: "${HE29_CTRL_REPO:?published controller checkout required}"
: "${HE29_ANALYSIS_REPO:?09929 analysis checkout required}"
HE29_REL=research/he29_survival_budget_20261018
HE29_CTRL_REL="$HE29_REL/orchestration_20261020"
HE29_PY="${HE29_EXISTING_PYTHON:-$HE29_EXISTING_WORK/venv/bin/python}"
HE29_BIN="$HE29_EXISTING_WORK/build/he29_owner_server"
HE29_RECEIPT="$HE29_EXISTING_WORK/build/RECEIPT.json"
[[ -x "$HE29_PY" && -x "$HE29_BIN" && -f "$HE29_RECEIPT" ]]
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
export OMP_DYNAMIC=FALSE OMP_PLACES=cores OMP_PROC_BIND=close
HE29_PLAN_OUT="$(mktemp -d "${TMPDIR:-/tmp}/he29-plan-parent.XXXXXXXX")/plan"
"$HE29_PY" "$HE29_CTRL_REPO/$HE29_CTRL_REL/src/continue_missing_references.py" \
  --baseline-root "$HE29_BASELINE_REPO/$HE29_REL" \
  --analysis-root "$HE29_ANALYSIS_REPO/$HE29_REL" \
  --root "$HE29_EXISTING_WORK/references" \
  --binary "$HE29_BIN" --receipt "$HE29_RECEIPT" --out "$HE29_PLAN_OUT"

HE29_CONT_OUT="$(mktemp -d "${TMPDIR:-/tmp}/he29-continue-parent.XXXXXXXX")/run"
HE29_CONT_RC=0
"$HE29_PY" "$HE29_CTRL_REPO/$HE29_CTRL_REL/src/continue_missing_references.py" \
  --baseline-root "$HE29_BASELINE_REPO/$HE29_REL" \
  --analysis-root "$HE29_ANALYSIS_REPO/$HE29_REL" \
  --root "$HE29_EXISTING_WORK/references" \
  --binary "$HE29_BIN" --receipt "$HE29_RECEIPT" \
  --out "$HE29_CONT_OUT" --execute || HE29_CONT_RC=$?
printf '%s\n' "$HE29_CONT_RC" > "${HE29_CONT_OUT}_EXIT_CODE.txt"
