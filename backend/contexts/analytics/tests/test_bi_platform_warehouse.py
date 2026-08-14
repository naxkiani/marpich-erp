"""P213-E BI warehouse foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_warehouse_foundation import (
    validate_bi_warehouse_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_warehouse as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_warehouse_foundation():
    result = validate_bi_warehouse_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-E"
    assert result["adr"] == 409
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_warehouse_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-E"
    assert cat["adr"] == 409
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "historical intelligence memory" in cat["principle"]
    assert cat["enterprise_data_warehouse_architecture_present_required"] is True
    assert cat["dimensional_modeling_present_required"] is True
    assert cat["semantic_layer_present_required"] is True
    assert cat["ai_readiness_alignment_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_analytical_data_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "AnalyticalDataAssetAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["architecture"]["layers"]["layer_count"] >= 6
    assert cat["subject_areas"]["area_count"] >= 10
    assert cat["events"]["core_event_count"] >= 5
    assert cat["microservices"]["service_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 20
    assert "dimensional_modeling_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P213-D" in cat["builds_on"]
    assert "P212-O" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/warehouse" in mod.warehouse_surface()["routes"]
    assert (
        "GET /analytics/warehouse/semantic-layer"
        in mod.warehouse_surface()["routes"]
    )


@pytest.mark.unit
def test_bi_warehouse_acl():
    from contexts.analytics.infrastructure.acl import bi_warehouse_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_data_quality(tenant_id="t1", quality_ref="q1")[
        "via_p212_e"
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
    assert acls.to_cryptographic_trust(tenant_id="t1", key_ref="k1")[
        "via_p209"
    ] is True
    assert acls.to_reporting(tenant_id="t1", report_ref="r1")[
        "via_p213_d"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_warehouse():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_warehouse"]["prompt_id"] == "P213-E"
    assert catalog["platform_warehouse"]["adr"] == 409
    assert catalog["sor"] == "analytics"
    summary = svc.platform_warehouse()
    assert summary["prompt_id"] == "P213-E"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-D" in summary["builds_on"]
    assert summary["context_count"] >= 5
    assert summary["subject_area_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.warehouse_readiness()["passed"] is True
    assert svc.warehouse_subject_areas()["area_count"] >= 10
    assert svc.warehouse_ai_foundation()["via_p212_k"] is True
