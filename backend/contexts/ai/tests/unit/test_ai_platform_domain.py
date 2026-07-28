"""P214-C Enterprise AI domain architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_domain_foundation import (
    validate_ai_domain_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_domain as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_domain_foundation():
    result = validate_ai_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-C"
    assert result["adr"] == 423
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_domain_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-C"
    assert cat["adr"] == 423
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "governed enterprise domains" in cat["principle"]
    assert cat["domain_map"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["domain_map"]["supporting_count"] >= 11
    assert cat["bounded_contexts"]["context_count"] >= 8
    assert cat["complete_ai_domain_model_present_required"] is True
    assert cat["aggregates_defined_required"] is True
    assert cat["domain_events_present_required"] is True
    assert cat["microservice_mapping_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["events"]["core_event_count"] >= 9
    assert cat["microservice_mapping"]["service_count"] >= 9
    assert cat["knowledge_domain"]["via_p213_l"] is True
    assert cat["data_domain"]["via_p212"] is True
    assert cat["security_domain"]["via_p207"] is True
    assert cat["cursor_outputs"]["count"] >= 16
    assert (
        "complete_ai_domain_model_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-B" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/domain" in mod.domain_surface()["routes"]
    assert "GET /ai/domain/bounded-contexts" in mod.domain_surface()["routes"]
    assert "GET /ai/domain/microservices" in mod.domain_surface()["routes"]


@pytest.mark.unit
def test_ai_domain_acl():
    from contexts.ai.infrastructure.acl import ai_domain_acl as acls

    assert acls.to_foundation(tenant_id="t1", profile_ref="p1")[
        "via_p214_a"
    ] is True
    assert acls.to_mission(tenant_id="t1", mission_ref="m1")[
        "via_p214_b"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")["via_p213_l"] is True
    assert acls.to_data_governance(tenant_id="t1", product_ref="d1")[
        "via_p212"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", control_ref="c1")[
        "via_p210"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_analytics(tenant_id="t1", insight_ref="i1")[
        "via_p213"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P214-C"
    assert catalog["platform_domain"]["adr"] == 423
    assert catalog["platform_domain"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_domain"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_domain()
    assert summary["prompt_id"] == "P214-C"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-B" in summary["builds_on"]
    assert summary["supporting_count"] >= 11
    assert summary["context_count"] >= 8
    assert summary["microservice_count"] >= 9
    assert summary["event_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.domain_readiness()["passed"] is True
    assert svc.domain_bounded_contexts()["context_count"] >= 8
    assert svc.domain_knowledge()["via_p213_l"] is True
    assert svc.domain_microservices()["service_count"] >= 9
