"""P210-C Cyber Security domain architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_domain_foundation import (
    validate_cs_domain_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_domain as pdom

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_domain_foundation():
    result = validate_cs_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-C"
    assert result["adr"] == 363
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_domain_catalog():
    cat = pdom.catalog()
    assert cat["prompt_id"] == "P210-C"
    assert cat["adr"] == 363
    assert cat["bounded_contexts"]["count"] >= 10
    assert cat["aggregates"]["count"] >= 10
    assert cat["knowledge_graph"]["integrated"] is True
    assert cat["anti_corruption_layers"]["present"] is True
    assert cat["cursor_outputs"]["count"] >= 20
    assert "bounded_contexts_overlap" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/domain" in pdom.domain_surface()["routes"]
    assert "GET /cyber-security/domain/readiness" in pdom.domain_surface()["routes"]


@pytest.mark.unit
def test_cs_domain_acl():
    from contexts.cyber_security.infrastructure.acl import cs_domain_acl as acls

    assert acls.to_security_incident(tenant_id="t1", detection_ref="d1")[
        "ir_lifecycle_owned_by_security_incident"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "does_not_own_kg_sor"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "does_not_own_twin_sor"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P210-C"
    assert catalog["platform_domain"]["adr"] == 363
    summary = svc.platform_domain()
    assert summary["prompt_id"] == "P210-C"
    assert summary["builds_on"] == ["P210-A", "P210-B", "ADR-361", "ADR-362"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
