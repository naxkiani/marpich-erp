"""Architecture tests — dependency graph enforcement."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from shared.kernel.dependency_graph import analyze_codebase

BACKEND_ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = Path(__file__).resolve().parent / "dependency_baseline.json"


def test_dependency_graph_no_new_violations() -> None:
    violations = analyze_codebase(BACKEND_ROOT)
    current = {v.key() for v in violations}
    baseline = set(json.loads(BASELINE_PATH.read_text(encoding="utf-8")))
    new = current - baseline
    assert not new, "New dependency violations:\n" + "\n".join(sorted(new))


def test_dependency_graph_baseline_matches_reality() -> None:
    violations = analyze_codebase(BACKEND_ROOT)
    current = {v.key() for v in violations}
    baseline = set(json.loads(BASELINE_PATH.read_text(encoding="utf-8")))
    stale = baseline - current
    assert not stale, (
        "Baseline has stale entries (violations fixed) — run "
        "scripts/check-dependency-graph.py --update-baseline:\n"
        + "\n".join(sorted(stale))
    )


@pytest.mark.parametrize(
    "kind",
    [
        "circular",
        "shared_imports_context",
        "business_imports_business",
        "core_imports_business",
    ],
)
def test_zero_tolerance_violation_kinds(kind: str) -> None:
    violations = analyze_codebase(BACKEND_ROOT)
    hits = [v for v in violations if v.kind.value == kind]
    assert not hits, "\n".join(f"{v.source_file}:{v.lineno} {v.message}" for v in hits)
