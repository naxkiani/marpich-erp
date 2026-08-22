#!/usr/bin/env bash
# Capture local git/build identity for MEOS release governance.
# Never claims DEPLOYED, CERTIFIED, or PRODUCTION_RELEASE.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${MEOS_RELEASE_EVIDENCE_OUT:-$ROOT/docs/meos/execution/.last_release_evidence.json}"

cd "$ROOT"
SHA="$(git rev-parse HEAD 2>/dev/null || echo NOT_AVAILABLE)"
SHORT="$(git rev-parse --short HEAD 2>/dev/null || echo NOT_AVAILABLE)"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo NOT_AVAILABLE)"
DIRTY_COUNT="$(git status --porcelain=v1 2>/dev/null | wc -l | tr -d ' ')"
DESCRIBE="$(git describe --tags --always --dirty 2>/dev/null || echo NOT_AVAILABLE)"
WHEN="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

export MEOS_EV_SHA="$SHA"
export MEOS_EV_SHORT="$SHORT"
export MEOS_EV_BRANCH="$BRANCH"
export MEOS_EV_DIRTY_COUNT="$DIRTY_COUNT"
export MEOS_EV_DESCRIBE="$DESCRIBE"
export MEOS_EV_WHEN="$WHEN"
export MEOS_EV_OUT="$OUT"

python3 <<'PY'
import json
import os
from pathlib import Path

dirty_count = int(os.environ["MEOS_EV_DIRTY_COUNT"])
dirty = dirty_count > 0
sha = os.environ["MEOS_EV_SHA"]
immutable = (not dirty) and sha not in {"", "NOT_AVAILABLE"}
path = Path(os.environ["MEOS_EV_OUT"])
path.parent.mkdir(parents=True, exist_ok=True)
doc = {
    "generated_at": os.environ["MEOS_EV_WHEN"],
    "release_id": "REL-EVIDENCE-LOCAL",
    "git_sha": sha,
    "git_sha_short": os.environ["MEOS_EV_SHORT"],
    "git_describe": os.environ["MEOS_EV_DESCRIBE"],
    "branch": os.environ["MEOS_EV_BRANCH"],
    "working_tree_dirty": dirty,
    "dirty_path_count": dirty_count,
    "immutable_sha": immutable,
    "environment": "LOCAL",
    "test_status": "NOT_DECLARED_BY_THIS_SCRIPT",
    "security_status": "TRUST_CRITICAL",
    "certification_status": "NOT_CERTIFIED",
    "deployment_status": "NOT_DEPLOYED",
    "rollback_status": "NOT_EXERCISED",
    "production_release": False,
    "notes": (
        "Evidence capture only. Dirty tree cannot be an immutable production "
        "artifact (G25). Production cluster BLOCKED (G26)."
    ),
}
path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print(path)
print(
    f"immutable_sha={doc['immutable_sha']} dirty={doc['working_tree_dirty']} "
    f"sha={doc['git_sha_short']}"
)
PY
