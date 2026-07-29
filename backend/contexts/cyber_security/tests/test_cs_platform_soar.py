"""P210-F Cyber Security SOAR foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_soar_foundation import (
    validate_cs_soar_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_soar as soar

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_soar_foundation():
    result = validate_cs_soar_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-F"
    assert result["adr"] == 365
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_soar_catalog():
    cat = soar.catalog()
    assert cat["prompt_id"] == "P210-F"
    assert cat["adr"] == 365
    assert cat["playbooks_versioned_required"] is True
    assert cat["human_approval_required"] is True
    assert cat["rollback_capability_required"] is True
    assert cat["connectors_tightly_coupled_forbidden"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["playbook_engine"]["category_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "playbooks_cannot_be_versioned" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/soar" in soar.soar_surface()["routes"]
    assert "GET /cyber-security/soar/readiness" in soar.soar_surface()["routes"]


@pytest.mark.unit
def test_cs_soar_acl():
    from contexts.cyber_security.infrastructure.acl import cs_soar_acl as acls

    assert acls.to_workflow_approval(tenant_id="t1", gate_ref="g1")[
        "via_workflow"
    ] is True
    assert acls.to_integration_connector(tenant_id="t1", connector_ref="c1")[
        "tightly_coupled_forbidden"
    ] is True
    assert acls.to_ai_explainable(tenant_id="t1", advisory_ref="a1")[
        "explainable_required"
    ] is True
    assert acls.to_evidence(tenant_id="t1", evidence_ref="e1")[
        "preservation_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_soar():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_soar"]["prompt_id"] == "P210-F"
    assert catalog["platform_soar"]["adr"] == 365
    summary = svc.platform_soar()
    assert summary["prompt_id"] == "P210-F"
    assert "P210-D" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
