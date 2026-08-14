"""P210-E Cyber Security SIEM foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_siem_foundation import (
    validate_cs_siem_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_siem as siem

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_siem_foundation():
    result = validate_cs_siem_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-E"
    assert result["adr"] == 367
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_siem_catalog():
    cat = siem.catalog()
    assert cat["prompt_id"] == "P210-E"
    assert cat["adr"] == 367
    assert cat["event_normalization_complete_required"] is True
    assert cat["multi_domain_correlation_required"] is True
    assert cat["storage_immutable_required"] is True
    assert cat["horizontal_scale_required"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["telemetry_collection"]["source_count"] >= 20
    assert cat["cursor_outputs"]["count"] >= 20
    assert "event_normalization_incomplete" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/siem" in siem.siem_surface()["routes"]
    assert "GET /cyber-security/siem/readiness" in siem.siem_surface()["routes"]


@pytest.mark.unit
def test_cs_siem_acl():
    from contexts.cyber_security.infrastructure.acl import cs_siem_acl as acls

    assert acls.to_soc(tenant_id="t1", alert_ref="a1")["via_p210_d_soc"] is True
    assert acls.to_soar_playbook(tenant_id="t1", playbook_ref="pb1")[
        "via_p210_f_soar"
    ] is True
    assert acls.to_xdr(tenant_id="t1", signal_ref="x1")["via_p210_g_xdr"] is True
    assert acls.to_ai_intelligence(tenant_id="t1", intelligence_ref="i1")[
        "ai_intelligence_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_siem():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_siem"]["prompt_id"] == "P210-E"
    assert catalog["platform_siem"]["adr"] == 367
    summary = svc.platform_siem()
    assert summary["prompt_id"] == "P210-E"
    assert "P210-G" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
