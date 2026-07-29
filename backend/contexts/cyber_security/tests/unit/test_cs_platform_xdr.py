"""P210-G Cyber Security XDR/EDR/NDR foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_xdr_foundation import (
    validate_cs_xdr_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_xdr as xdr

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_xdr_foundation():
    result = validate_cs_xdr_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-G"
    assert result["adr"] == 366
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_xdr_catalog():
    cat = xdr.catalog()
    assert cat["prompt_id"] == "P210-G"
    assert cat["adr"] == 366
    assert cat["endpoint_telemetry_complete_required"] is True
    assert cat["xdr_correlation_unified_required"] is True
    assert cat["agent_integrity_verifiable_required"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["edr"]["capability_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "endpoint_telemetry_incomplete" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/xdr" in xdr.xdr_surface()["routes"]
    assert "GET /cyber-security/xdr/readiness" in xdr.xdr_surface()["routes"]


@pytest.mark.unit
def test_cs_xdr_acl():
    from contexts.cyber_security.infrastructure.acl import cs_xdr_acl as acls

    assert acls.to_soar_playbook(tenant_id="t1", playbook_ref="pb1")[
        "via_p210_f_soar"
    ] is True
    assert acls.to_workflow_approval(tenant_id="t1", gate_ref="g1")[
        "response_safeguards_required"
    ] is True
    assert acls.to_ai_analytics(tenant_id="t1", analytics_ref="a1")[
        "ai_analytics_required"
    ] is True
    assert acls.to_secrets_agent_integrity(tenant_id="t1", agent_ref="ag1")[
        "agent_integrity_verifiable_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_xdr():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_xdr"]["prompt_id"] == "P210-G"
    assert catalog["platform_xdr"]["adr"] == 366
    summary = svc.platform_xdr()
    assert summary["prompt_id"] == "P210-G"
    assert "P210-F" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
