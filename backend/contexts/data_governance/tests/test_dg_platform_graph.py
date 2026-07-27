"""P212-J Data Governance knowledge graph foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_graph_foundation import (
    validate_dg_graph_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_graph as graph,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_graph_foundation():
    result = validate_dg_graph_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-J"
    assert result["adr"] == 402
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_graph_catalog():
    cat = graph.catalog()
    assert cat["prompt_id"] == "P212-J"
    assert cat["adr"] == 402
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["knowledge_graph_architecture_complete_required"] is True
    assert cat["ddd_domain_model_present_required"] is True
    assert cat["ontology_architecture_present_required"] is True
    assert cat["semantic_data_fabric_present_required"] is True
    assert cat["graph_intelligence_engine_present_required"] is True
    assert cat["ai_reasoning_layer_present_required"] is True
    assert cat["data_mesh_integration_present_required"] is True
    assert cat["metadata_integration_present_required"] is True
    assert cat["data_marketplace_integration_present_required"] is True
    assert cat["policy_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["zero_trust_security_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["graph_architecture"]["bc_count"] >= 5
    assert cat["ontology"]["capability_count"] >= 6
    assert cat["semantic_fabric"]["layer_count"] >= 5
    assert cat["graph_intelligence"]["capability_count"] >= 6
    assert cat["node_model"]["category_count"] >= 5
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cqrs"]["event_count"] >= 6
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "enterprise_knowledge_graph_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/graph" in graph.graph_surface()["routes"]
    assert (
        "GET /data-governance/graph/readiness"
        in graph.graph_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_graph_acl():
    from contexts.data_governance.infrastructure.acl import dg_graph_acl as acls

    assert acls.to_ownership(tenant_id="t1", owner_ref="o1")["via_p212_d"] is True
    assert acls.to_quality(tenant_id="t1", asset_ref="a1")["via_p212_e"] is True
    assert acls.to_mesh(tenant_id="t1", product_ref="p1")["via_p212_f"] is True
    assert acls.to_marketplace(tenant_id="t1", product_ref="p1")[
        "via_p212_g"
    ] is True
    assert acls.to_policies(tenant_id="t1", policy_ref="pol1")[
        "via_p212_h"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_reasoning_layer_present_required"
    ] is True
    assert acls.to_enterprise_search(tenant_id="t1", query_ref="q1")[
        "via_enterprise_search"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="query_graph"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_graph():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_graph"]["prompt_id"] == "P212-J"
    assert catalog["platform_graph"]["adr"] == 402
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_graph()
    assert summary["prompt_id"] == "P212-J"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-H" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.graph_readiness()["passed"] is True
