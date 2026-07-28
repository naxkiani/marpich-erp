"""P213-B Enterprise BI mission foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_mission_foundation import (
    validate_bi_mission_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import (
    bi_platform_mission_scope as mscope,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_mission_foundation():
    result = validate_bi_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-B"
    assert result["adr"] == 395
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_mission_catalog():
    cat = mscope.catalog()
    assert cat["prompt_id"] == "P213-B"
    assert cat["adr"] == 395
    assert cat["sor"] == "analytics"
    assert cat["mission_defined_required"] is True
    assert cat["vision_defined_required"] is True
    assert cat["decision_intelligence_scope_defined_required"] is True
    assert cat["capability_map_present_required"] is True
    assert cat["governance_model_present_required"] is True
    assert cat["ai_strategy_defined_required"] is True
    assert "trusted enterprise data" in cat["mission"]["statement"]
    assert cat["strategic_objectives"]["count"] >= 6
    assert cat["capability_map"]["capability_count"] >= 10
    assert cat["enterprise_scope"]["scope_category_count"] >= 4
    assert cat["operating_model"]["lifecycle_step_count"] >= 8
    assert cat["maturity_model"]["level_count"] >= 6
    assert cat["ai_strategy"]["level_count"] >= 5
    assert cat["enterprise_roadmap"]["phase_count"] >= 5
    assert cat["knowledge_graph_alignment"]["via_p212_j"] is True
    assert cat["digital_twin_alignment"]["via_p212_l"] is True
    assert cat["cursor_outputs"]["count"] >= 15
    assert "mission_is_undefined" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/mission" in mscope.mission_surface()["routes"]


@pytest.mark.unit
def test_bi_mission_acl():
    from contexts.analytics.infrastructure.acl import bi_mission_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")["via_p212_j"] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")["via_p212_l"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "via_enterprise_ai"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read_mission"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_scope"]["prompt_id"] == "P213-B"
    assert catalog["platform_mission_scope"]["adr"] == 395
    assert catalog["sor"] == "analytics"
    summary = svc.platform_mission()
    assert summary["prompt_id"] == "P213-B"
    assert summary["capability"] == "CAP-PLT-BI-001"
    assert "P213-A" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.mission_readiness()["passed"] is True
