"""P210-A Cyber Security strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import (
    cs_platform_strategy as strat,
)
from contexts.cyber_security.application.cs_strategy_foundation import (
    validate_cs_strategy_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_strategy_foundation():
    result = validate_cs_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-A"
    assert result["adr"] == 361
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_cs_strategy_catalog():
    cat = strat.catalog()
    assert cat["prompt_id"] == "P210-A"
    assert cat["adr"] == 361
    assert cat["sor"] == "cyber_security"
    assert cat["zero_trust_required"] is True
    assert cat["enterprise_soc_required"] is True
    assert cat["ai_security_required"] is True
    assert cat["threat_intelligence_isolated_forbidden"] is True
    assert cat["incident_response_manual_only_forbidden"] is True
    assert cat["capability_domains"]["count"] >= 20
    assert cat["cqrs"]["event_count"] >= 12
    assert "security_architecture_not_zero_trust" in cat["quality_gates"][
        "reject_if"
    ]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/strategy" in strat.strategy_surface()["routes"]
    assert (
        "GET /cyber-security/strategy/readiness"
        in strat.strategy_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P210-A"
    assert catalog["platform_strategy"]["adr"] == 361
    assert catalog["platform_strategy"]["zero_trust_required"] is True
    assert catalog["platform_strategy"]["enterprise_soc_required"] is True

    summary = svc.platform_strategy()
    assert summary["prompt_id"] == "P210-A"
    assert summary["builds_on"] == [
        "ADR-021",
        "ADR-158",
        "ADR-179",
        "ADR-345",
    ]
    assert "P210-G" in summary["follow_up_modules"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"


@pytest.mark.unit
def test_cs_strategy_acl():
    from contexts.cyber_security.infrastructure.acl import cs_strategy_acl as acls

    assert acls.to_security_incident(tenant_id="t1", detection_ref="d1")[
        "ir_lifecycle_owned_by_security_incident"
    ] is True
    assert acls.to_integration_connector(tenant_id="t1", connector_ref="c1")[
        "vendor_sdk_embed_forbidden"
    ] is True
    assert acls.to_workflow_automation(tenant_id="t1", playbook_ref="pb1")[
        "manual_only_forbidden"
    ] is True
    assert acls.to_ai_security(tenant_id="t1", surface_ref="s1")[
        "ai_security_required"
    ] is True
