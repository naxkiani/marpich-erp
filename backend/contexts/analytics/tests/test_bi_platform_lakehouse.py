"""P213-F BI lakehouse foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_lakehouse_foundation import (
    validate_bi_lakehouse_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_lakehouse as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_lakehouse_foundation():
    result = validate_bi_lakehouse_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-F"
    assert result["adr"] == 410
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_lakehouse_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-F"
    assert cat["adr"] == 410
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "decision intelligence converge" in cat["principle"]
    assert cat["enterprise_lakehouse_architecture_present_required"] is True
    assert cat["ai_data_foundation_present_required"] is True
    assert cat["data_mesh_alignment_present_required"] is True
    assert cat["storage_architecture_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_lakehouse_intelligence_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "LakehousePlatformAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["architecture"]["layers"]["layer_count"] >= 4
    assert cat["ai_native"]["agent_count"] >= 5
    assert cat["events"]["core_event_count"] >= 5
    assert cat["microservices"]["service_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 19
    assert "ai_data_foundation_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P213-E" in cat["builds_on"]
    assert "P212-G" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/lakehouse" in mod.lakehouse_surface()["routes"]
    assert "GET /analytics/lakehouse/ai" in mod.lakehouse_surface()["routes"]


@pytest.mark.unit
def test_bi_lakehouse_acl():
    from contexts.analytics.infrastructure.acl import bi_lakehouse_acl as acls

    assert acls.to_data_mesh(tenant_id="t1", product_ref="p1")[
        "via_p212_f"
    ] is True
    assert acls.to_marketplace(tenant_id="t1", listing_ref="l1")[
        "via_p212_g"
    ] is True
    assert acls.to_ai_readiness(tenant_id="t1", dataset_ref="d1")[
        "via_p212_k"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p212_j"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_warehouse(tenant_id="t1", warehouse_ref="w1")[
        "via_p213_e"
    ] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", key_ref="k1")[
        "tokenization"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_lakehouse():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_lakehouse"]["prompt_id"] == "P213-F"
    assert catalog["platform_lakehouse"]["adr"] == 410
    assert catalog["sor"] == "analytics"
    summary = svc.platform_lakehouse()
    assert summary["prompt_id"] == "P213-F"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-E" in summary["builds_on"]
    assert summary["context_count"] >= 5
    assert summary["medallion_layer_count"] >= 4
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.lakehouse_readiness()["passed"] is True
    assert svc.lakehouse_ai()["agent_count"] >= 5
    assert svc.lakehouse_data_products()["via_p212_f"] is True
