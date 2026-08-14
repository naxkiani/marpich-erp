"""P3 contract — fail CI when ROUTER/SERVICE specs introduce new missing packages."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from core.presentation.api.startup_registry import (
    ALL_SERVICE_SPECS,
    CORE_SERVICE_SPECS,
    DEFERRED_CONTEXT_IDS,
    EMPTY_INDUSTRY_SCAFFOLD_IDS,
    ROUTER_SPECS,
    _context_id_from_module,
)

_BASELINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "architecture"
    / "missing_router_packages_baseline.json"
)
_CONTEXTS_ROOT = Path(__file__).resolve().parents[2] / "contexts"


def _load_baseline() -> dict:
    return json.loads(_BASELINE_PATH.read_text(encoding="utf-8"))


def _module_resolves(module_path: str) -> bool:
    try:
        return importlib.util.find_spec(module_path) is not None
    except (ModuleNotFoundError, ValueError, AttributeError):
        return False


def _missing_modules(specs: list[tuple[str, str]]) -> list[str]:
    return sorted({m for m, _ in specs if not _module_resolves(m)})


def _missing_context_packages(module_paths: list[str]) -> list[str]:
    missing: set[str] = set()
    for module_path in module_paths:
        ctx = _context_id_from_module(module_path)
        if ctx and not (_CONTEXTS_ROOT / ctx).is_dir():
            missing.add(ctx)
    return sorted(missing)


def test_baseline_file_exists_and_versioned():
    data = _load_baseline()
    assert data.get("version") == 1
    assert isinstance(data.get("missing_router_modules"), list)
    assert isinstance(data.get("missing_service_modules"), list)
    assert isinstance(data.get("missing_context_packages"), list)


def test_no_new_missing_router_modules():
    """Adding a ROUTER_SPEC that cannot resolve is a P3 hard fail unless baseline grows intentionally."""
    baseline = set(_load_baseline()["missing_router_modules"])
    current = set(_missing_modules(ROUTER_SPECS))
    new_missing = sorted(current - baseline)
    assert new_missing == [], (
        "P3: new missing router modules (implement package or update baseline with ADR):\n"
        + "\n".join(f"  - {m}" for m in new_missing)
    )


def test_no_new_missing_service_modules():
    baseline = set(_load_baseline()["missing_service_modules"])
    current = set(_missing_modules(CORE_SERVICE_SPECS + ALL_SERVICE_SPECS))
    new_missing = sorted(current - baseline)
    assert new_missing == [], (
        "P3: new missing service modules (implement package or update baseline with ADR):\n"
        + "\n".join(f"  - {m}" for m in new_missing)
    )


def test_missing_context_packages_must_be_deferred():
    """Package dirs referenced by ROUTER_SPECS that do not exist must stay in DEFERRED_CONTEXT_IDS."""
    missing_pkgs = _missing_context_packages(_missing_modules(ROUTER_SPECS))
    undeferred = sorted(set(missing_pkgs) - set(DEFERRED_CONTEXT_IDS))
    assert undeferred == [], (
        "P3: missing context packages not in DEFERRED_CONTEXT_IDS:\n"
        + "\n".join(f"  - {c}" for c in undeferred)
    )


def test_no_new_missing_context_packages():
    baseline = set(_load_baseline()["missing_context_packages"])
    current = set(_missing_context_packages(_missing_modules(ROUTER_SPECS)))
    new_pkgs = sorted(current - baseline)
    assert new_pkgs == [], (
        "P3: new missing context packages (do not invent ROUTER_SPECS without a package):\n"
        + "\n".join(f"  - {c}" for c in new_pkgs)
    )


def test_baseline_shrinks_when_modules_land():
    """Boy Scout: if a grandfathered module now resolves, shrink the baseline."""
    data = _load_baseline()
    stale_routers = sorted(
        m for m in data["missing_router_modules"] if _module_resolves(m)
    )
    stale_services = sorted(
        m for m in data["missing_service_modules"] if _module_resolves(m)
    )
    assert stale_routers == [], (
        "P3: baseline lists routers that now resolve — remove from "
        "missing_router_packages_baseline.json:\n"
        + "\n".join(f"  - {m}" for m in stale_routers)
    )
    assert stale_services == [], (
        "P3: baseline lists services that now resolve — remove from "
        "missing_router_packages_baseline.json:\n"
        + "\n".join(f"  - {m}" for m in stale_services)
    )


def test_empty_scaffolds_frozen_in_baseline():
    data = _load_baseline()
    assert set(data.get("empty_industry_scaffolds", [])) == set(EMPTY_INDUSTRY_SCAFFOLD_IDS)
