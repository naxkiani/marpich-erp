"""P209-A Secrets Strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_strategy_foundation import (
    validate_secrets_strategy_foundation,
)
from contexts.secrets.domain.services import secrets_platform_strategy as strat

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_strategy_foundation():
    result = validate_secrets_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-A"
    assert result["adr"] == 346
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_strategy_catalog():
    cat = strat.catalog()
    assert cat["prompt_id"] == "P209-A"
    assert cat["adr"] == 346
    assert cat["sor"] == "secrets"
    assert cat["secrets_outside_governed_stores_forbidden"] is True
    assert cat["keys_exportable_without_policy_forbidden"] is True
    assert cat["manual_certificate_management_forbidden"] is True
    assert cat["root_ca_security_inadequate_forbidden"] is True
    assert cat["hsm_integration_required"] is True
    assert cat["cryptographic_lifecycle_complete_required"] is True
    assert cat["cryptographic_operations_audit_required"] is True
    assert cat["primary_domains"]["count"] >= 12
    assert cat["cqrs"]["event_count"] >= 12
    assert (
        "secrets_stored_outside_governed_stores"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/strategy" in strat.strategy_surface()["routes"]
    assert (
        "GET /secrets/strategy/readiness" in strat.strategy_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P209-A"
    assert catalog["platform_strategy"]["adr"] == 346
    assert catalog["platform_strategy"][
        "secrets_outside_governed_stores_forbidden"
    ] is True
    assert catalog["delegation"]["secrets_outside_governed_stores"] is False
    assert catalog["delegation"]["keys_exportable_without_policy"] is False

    summary = svc.platform_strategy()
    assert summary["prompt_id"] == "P209-A"
    assert summary["builds_on"] == ["P209"]
    assert summary["cursor_outputs"]["count"] == 20
    assert summary["hsm"]["required"] is True
    assert "vault" in summary["forbidden_sibling_bc"]
