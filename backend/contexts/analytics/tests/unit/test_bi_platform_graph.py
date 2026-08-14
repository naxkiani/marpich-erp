"""P213-L BI decision knowledge graph foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_graph_foundation import (
    validate_bi_graph_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_graph as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_graph_foundation():
    result = validate_bi_graph_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-L"
    assert result["adr"] == 416
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_graph_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-L"
    assert cat["adr"] == 416
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "governed, connected" in cat["principle"]
    assert cat["enterprise_decision_knowledge_graph_present_required"] is True
    assert cat["enterprise_decision_ontology_present_required"] is True
    assert cat["enterprise_decision_memory_present_required"] is True
    assert cat["graph_analytics_present_required"] is True
    assert cat["ai_reasoning_present_required"] is True
    assert cat["decision_lineage_present_required"] is True
    assert cat["knowledge_graph_federation_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_decision_knowledge_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "DecisionKnowledgeGraphAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["graph_model"]["entity_type_count"] >= 21
    assert cat["graph_analytics"]["capability_count"] >= 9
    assert cat["ai_native"]["agent_count"] >= 6
    assert cat["events"]["core_event_count"] >= 6
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "knowledge_graph_federation_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213-K" in cat["builds_on"]
    assert "P212-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/graph" in mod.graph_surface()["routes"]
    assert "GET /analytics/graph/lineage" in mod.graph_surface()["routes"]


@pytest.mark.unit
def test_bi_graph_acl():
    from contexts.analytics.infrastructure.acl import bi_graph_acl as acls

    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p212_j"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_semantic(tenant_id="t1", metric_ref="m1")[
        "via_p213_g"
    ] is True
    assert acls.to_predictive(tenant_id="t1", forecast_ref="f1")[
        "via_p213_j"
    ] is True
    assert acls.to_prescriptive(tenant_id="t1", recommendation_ref="r1")[
        "via_p213_k"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["node_level_security"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "policy_driven_graph_governance"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_graph():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_graph"]["prompt_id"] == "P213-L"
    assert catalog["platform_graph"]["adr"] == 416
    assert catalog["sor"] == "analytics"
    summary = svc.platform_graph()
    assert summary["prompt_id"] == "P213-L"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-K" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["entity_type_count"] >= 21
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.graph_readiness()["passed"] is True
    assert svc.graph_ai()["agent_count"] >= 6
    assert svc.graph_federation()["via_p212_j"] is True
