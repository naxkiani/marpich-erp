"""P212-G Data Governance marketplace foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_marketplace_foundation import (
    validate_dg_marketplace_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_marketplace as mkt,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_marketplace_foundation():
    result = validate_dg_marketplace_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-G"
    assert result["adr"] == 400
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_marketplace_catalog():
    cat = mkt.catalog()
    assert cat["prompt_id"] == "P212-G"
    assert cat["adr"] == 400
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["marketplace_architecture_complete_required"] is True
    assert cat["data_catalog_architecture_present_required"] is True
    assert cat["data_discovery_architecture_present_required"] is True
    assert cat["data_product_consumption_model_present_required"] is True
    assert cat["data_access_governance_present_required"] is True
    assert cat["ai_recommendation_intelligence_present_required"] is True
    assert cat["data_mesh_alignment_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["zero_trust_alignment_present_required"] is True
    assert cat["enterprise_scalability_present_required"] is True
    assert cat["marketplace_architecture"]["bc_count"] >= 6
    assert cat["data_catalog"]["capability_count"] >= 4
    assert cat["discovery"]["capability_count"] >= 5
    assert cat["access_governance"]["step_count"] >= 7
    assert cat["microservices"]["service_count"] >= 7
    assert cat["cqrs"]["event_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 18
    assert (
        "enterprise_data_marketplace_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/marketplace" in mkt.marketplace_surface()["routes"]
    assert (
        "GET /data-governance/marketplace/readiness"
        in mkt.marketplace_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_marketplace_acl():
    from contexts.data_governance.infrastructure.acl import (
        dg_marketplace_acl as acls,
    )

    assert acls.to_ownership(tenant_id="t1", owner_ref="o1")[
        "via_p212_d"
    ] is True
    assert acls.to_quality(tenant_id="t1", product_ref="p1")[
        "via_p212_e"
    ] is True
    assert acls.to_mesh(tenant_id="t1", product_ref="p1")[
        "via_p212_f"
    ] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_recommendation_intelligence_present_required"
    ] is True
    assert acls.to_enterprise_search(tenant_id="t1", query_ref="q1")[
        "via_enterprise_search"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="request_access"
    )["via_p208"] is True
    assert acls.to_workflow(tenant_id="t1", request_ref="r1")[
        "via_workflow"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_marketplace():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_marketplace"]["prompt_id"] == "P212-G"
    assert catalog["platform_marketplace"]["adr"] == 400
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_marketplace()
    assert summary["prompt_id"] == "P212-G"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-F" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.marketplace_readiness()["passed"] is True
