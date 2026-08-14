#!/usr/bin/env bash
# Wave 05 autonomy gate proof — unit deny-by-default + docs present.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== docs =="
test -f "$ROOT/docs/meos/execution/MEOS_WAVE05_AUTONOMY_GATE.md"

echo "== unit gate =="
cd "$ROOT/backend"
if [[ -x .venv/bin/pytest ]]; then
  PYTEST=.venv/bin/pytest
else
  PYTEST=pytest
fi
PERSISTENCE_BACKEND=memory "$PYTEST" -q shared/tests/test_autonomy_gate.py --maxfail=2

echo "PASS: Wave 05 autonomy gate (deny-by-default) verified"
