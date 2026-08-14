"""P0 architecture — deferred contexts must not register live routers."""
from __future__ import annotations

from core.presentation.api.startup_registry import (
    DEFERRED_CONTEXT_IDS,
    ROUTER_SPECS,
    ALL_SERVICE_SPECS,
    CORE_SERVICE_SPECS,
    filter_available_specs,
    _context_id_from_module,
)


def test_deferred_packages_are_not_available():
    for ctx in ("mfa", "currency_exchange", "reporting", "fraud_detection"):
        assert ctx in DEFERRED_CONTEXT_IDS


def test_filter_available_specs_excludes_deferred_routers():
    specs = [
        ("contexts.crm.presentation.router", "router"),
        ("contexts.mfa.presentation.router", "mfa_router"),
        ("contexts.currency_exchange.presentation.fx_rate_router", "fx_rate_router"),
    ]
    available = filter_available_specs(specs, kind="router")
    paths = {m for m, _ in available}
    # Assert only deferred exclusion — non-deferred specs may or may not resolve in unit env
    assert "contexts.mfa.presentation.router" not in paths
    assert "contexts.currency_exchange.presentation.fx_rate_router" not in paths
    for module_path in paths:
        cid = _context_id_from_module(module_path)
        assert cid is None or cid not in DEFERRED_CONTEXT_IDS


def test_no_deferred_context_survives_filter_on_full_router_list():
    available = filter_available_specs(ROUTER_SPECS, kind="router")
    deferred_hits = [
        m
        for m, _ in available
        if (cid := _context_id_from_module(m)) and cid in DEFERRED_CONTEXT_IDS
    ]
    assert deferred_hits == []


def test_no_deferred_context_in_core_service_warmup_filter():
    available = filter_available_specs(CORE_SERVICE_SPECS + ALL_SERVICE_SPECS, kind="service")
    deferred_hits = [
        m
        for m, _ in available
        if (cid := _context_id_from_module(m)) and cid in DEFERRED_CONTEXT_IDS
    ]
    assert deferred_hits == []
