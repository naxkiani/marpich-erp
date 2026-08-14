"""P210-H Cyber Security Threat Intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_intel_foundation import (
    validate_cs_intel_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_intel as intel

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_intel_foundation():
    result = validate_cs_intel_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-H"
    assert result["adr"] == 368
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_intel_catalog():
    cat = intel.catalog()
    assert cat["prompt_id"] == "P210-H"
    assert cat["adr"] == 368
    assert cat["threat_hunting_proactive_required"] is True
    assert cat["knowledge_graph_integration_required"] is True
    assert cat["intelligence_sharing_standards_required"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["sources"]["source_count"] >= 15
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "threat_intelligence_cannot_be_validated"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/intel" in intel.intel_surface()["routes"]
    assert "GET /cyber-security/intel/readiness" in intel.intel_surface()["routes"]


@pytest.mark.unit
def test_cs_intel_acl():
    from contexts.cyber_security.infrastructure.acl import cs_intel_acl as acls

    assert acls.to_siem(tenant_id="t1", detection_ref="d1")[
        "detection_engineering_connected"
    ] is True
    assert acls.to_ai_explainable(tenant_id="t1", advisory_ref="a1")[
        "explainable_required"
    ] is True
    assert acls.to_stix_taxii(tenant_id="t1", channel_ref="c1")[
        "stix_taxii"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", graph_ref="g1")[
        "integration_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_intel():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_intel"]["prompt_id"] == "P210-H"
    assert catalog["platform_intel"]["adr"] == 368
    summary = svc.platform_intel()
    assert summary["prompt_id"] == "P210-H"
    assert "P210-E" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
