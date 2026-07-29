"""P210-L Cyber Security Ops fabric foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_ops_foundation import (
    validate_cs_ops_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_ops as ops

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_ops_foundation():
    result = validate_cs_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-L"
    assert result["adr"] == 372
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_ops_catalog():
    cat = ops.catalog()
    assert cat["prompt_id"] == "P210-L"
    assert cat["adr"] == 372
    assert cat["events_immutable_required"] is True
    assert cat["cqrs_separation_complete_required"] is True
    assert cat["services_loosely_coupled_required"] is True
    assert cat["cqrs_events"]["event_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "services_tightly_coupled" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/ops" in ops.ops_surface()["routes"]
    assert "GET /cyber-security/ops/readiness" in ops.ops_surface()["routes"]


@pytest.mark.unit
def test_cs_ops_acl():
    from contexts.cyber_security.infrastructure.acl import cs_ops_acl as acls

    assert acls.to_event_bus(tenant_id="t1", event_ref="e1")[
        "events_immutable_required"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "apis_security_controls_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", stream_ref="s1")[
        "ai_integration_possible_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ops():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ops"]["prompt_id"] == "P210-L"
    assert catalog["platform_ops"]["adr"] == 372
    summary = svc.platform_ops()
    assert summary["prompt_id"] == "P210-L"
    assert "P210-K" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
