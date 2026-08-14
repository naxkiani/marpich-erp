"""P2 architecture — blueprint fabrics and empty industry scaffolds stay honest."""
from __future__ import annotations

from pathlib import Path

from core.presentation.api.app_profiles import BLUEPRINT_CONTEXTS, contexts_for_profile
from core.presentation.api.startup_registry import (
    BLUEPRINT_CONTEXT_IDS,
    DEFERRED_CONTEXT_IDS,
    EMPTY_INDUSTRY_SCAFFOLD_IDS,
    ROUTER_SPECS,
    _context_id_from_module,
    filter_available_specs,
)

_CONTEXTS_ROOT = Path(__file__).resolve().parents[2] / "contexts"

# Canonical empty industry scaffolds from completeness audit — do not expand without a Functional slice.
EXPECTED_EMPTY_SCAFFOLDS = frozenset(
    {
        "construction",
        "currency_exchange",
        "government",
        "hotel",
        "islamic_banking",
        "manufacturing",
        "ngo",
        "projects",
        "real_estate",
        "restaurant",
        "school",
        "warehouse",
    }
)

EXPECTED_BLUEPRINTS = frozenset(
    {
        "quantum",
        "robotics",
        "biotechnology",
        "space",
        "civilization",
    }
)


def test_empty_scaffolds_match_audit_and_deferred():
    assert EMPTY_INDUSTRY_SCAFFOLD_IDS == EXPECTED_EMPTY_SCAFFOLDS
    assert EXPECTED_EMPTY_SCAFFOLDS <= DEFERRED_CONTEXT_IDS


def test_empty_scaffolds_have_no_real_python_bodies():
    """Placeholder trees only — expanding empties is a P2 violation."""
    for ctx in sorted(EMPTY_INDUSTRY_SCAFFOLD_IDS):
        root = _CONTEXTS_ROOT / ctx
        assert root.is_dir(), f"missing scaffold dir {ctx}"
        nonempty = []
        for path in root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if len(text) > 80:
                nonempty.append(path.relative_to(_CONTEXTS_ROOT).as_posix())
        assert nonempty == [], f"{ctx} has non-placeholder Python: {nonempty[:5]}"


def test_blueprint_ids_aligned_across_modules():
    assert BLUEPRINT_CONTEXT_IDS == EXPECTED_BLUEPRINTS
    assert BLUEPRINT_CONTEXTS == EXPECTED_BLUEPRINTS


def test_default_filter_excludes_blueprints_and_scaffolds(monkeypatch):
    monkeypatch.setattr(
        "shared.infrastructure.settings.settings.marpich_enable_blueprint_apis",
        False,
        raising=False,
    )
    monkeypatch.setattr(
        "shared.infrastructure.settings.settings.marpich_app_profile",
        "full",
        raising=False,
    )
    available = filter_available_specs(ROUTER_SPECS, kind="router")
    ids = {_context_id_from_module(m) for m, _ in available}
    assert ids.isdisjoint(BLUEPRINT_CONTEXT_IDS)
    assert ids.isdisjoint(EMPTY_INDUSTRY_SCAFFOLD_IDS)


def test_blueprint_profile_includes_blueprint_contexts():
    allowed = contexts_for_profile("blueprint")
    assert allowed is not None
    assert EXPECTED_BLUEPRINTS <= allowed


def test_opt_in_enables_blueprint_router_specs(monkeypatch):
    monkeypatch.setattr(
        "shared.infrastructure.settings.settings.marpich_enable_blueprint_apis",
        True,
        raising=False,
    )
    specs = [
        ("contexts.crm.presentation.router", "router"),
        ("contexts.quantum.presentation.router", "quantum_router"),
        ("contexts.currency_exchange.presentation.fx_rate_router", "fx_rate_router"),
    ]
    available = filter_available_specs(specs, kind="router")
    paths = {m for m, _ in available}
    assert "contexts.quantum.presentation.router" in paths
    assert "contexts.currency_exchange.presentation.fx_rate_router" not in paths
