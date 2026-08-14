#!/usr/bin/env python3
"""P3 — report missing ROUTER/SERVICE modules vs grandfathered baseline.

Exit 1 when current missing set grows beyond
backend/tests/architecture/missing_router_packages_baseline.json.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from core.presentation.api.startup_registry import (  # noqa: E402
    ALL_SERVICE_SPECS,
    CORE_SERVICE_SPECS,
    ROUTER_SPECS,
)

BASELINE = BACKEND / "tests" / "architecture" / "missing_router_packages_baseline.json"


def _resolves(module_path: str) -> bool:
    try:
        return importlib.util.find_spec(module_path) is not None
    except (ModuleNotFoundError, ValueError, AttributeError):
        return False


def _missing(specs: list[tuple[str, str]]) -> set[str]:
    return {m for m, _ in specs if not _resolves(m)}


def main() -> int:
    data = json.loads(BASELINE.read_text(encoding="utf-8"))
    base_r = set(data["missing_router_modules"])
    base_s = set(data["missing_service_modules"])
    cur_r = _missing(ROUTER_SPECS)
    cur_s = _missing(CORE_SERVICE_SPECS + ALL_SERVICE_SPECS)
    new_r = sorted(cur_r - base_r)
    new_s = sorted(cur_s - base_s)
    stale_r = sorted(m for m in base_r if _resolves(m))
    stale_s = sorted(m for m in base_s if _resolves(m))

    print(f"missing routers: {len(cur_r)} (baseline {len(base_r)})")
    print(f"missing services: {len(cur_s)} (baseline {len(base_s)})")
    rc = 0
    if new_r:
        rc = 1
        print("NEW missing routers:")
        for m in new_r:
            print(f"  - {m}")
    if new_s:
        rc = 1
        print("NEW missing services:")
        for m in new_s:
            print(f"  - {m}")
    if stale_r or stale_s:
        rc = 1
        print("STALE baseline entries (now resolve — shrink baseline):")
        for m in stale_r + stale_s:
            print(f"  - {m}")
    if rc == 0:
        print("P3 OK — no new missing router/service packages")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
