"""P210-D Cyber Security SOC foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_soc_foundation import (
    validate_cs_soc_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_soc as soc

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_soc_foundation():
    result = validate_cs_soc_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-D"
    assert result["adr"] == 364
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_soc_catalog():
    cat = soc.catalog()
    assert cat["prompt_id"] == "P210-D"
    assert cat["adr"] == 364
    assert cat["soc_24x7_required"] is True
    assert cat["alert_correlation_required"] is True
    assert cat["ai_assistance_required"] is True
    assert cat["threat_hunting_required"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["telemetry"]["count"] >= 20
    assert cat["cursor_outputs"]["count"] >= 20
    assert "soc_not_24x7" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/soc" in soc.soc_surface()["routes"]
    assert "GET /cyber-security/soc/readiness" in soc.soc_surface()["routes"]


@pytest.mark.unit
def test_cs_soc_acl():
    from contexts.cyber_security.infrastructure.acl import cs_soc_acl as acls

    assert acls.to_security_incident_handoff(
        tenant_id="t1", alert_ref="a1", severity="high"
    )["ir_lifecycle_owned_by_security_incident"] is True
    assert acls.to_ai_assistance(tenant_id="t1", surface_ref="s1")[
        "ai_assistance_required"
    ] is True
    assert acls.to_workflow_playbook(tenant_id="t1", playbook_ref="pb1")[
        "manual_only_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_soc():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_soc"]["prompt_id"] == "P210-D"
    assert catalog["platform_soc"]["adr"] == 364
    summary = svc.platform_soc()
    assert summary["prompt_id"] == "P210-D"
    assert "P210-C" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
