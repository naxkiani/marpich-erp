"""P214-B Enterprise AI mission/vision/scope foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_mission_foundation import (
    validate_ai_mission_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_mission_scope as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_mission_foundation():
    result = validate_ai_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-B"
    assert result["adr"] == 422
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_mission_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-B"
    assert cat["adr"] == 422
    assert cat["fabric"] == mod.FABRIC
    assert "continuously learning operating system" in cat["mission"]["statement"]
    assert "intelligence layer that continuously learns" in cat["vision"]["statement"]
    assert cat["mission_defined_required"] is True
    assert cat["vision_defined_required"] is True
    assert cat["ai_capability_map_present_required"] is True
    assert cat["ai_maturity_model_present_required"] is True
    assert cat["ai_governance_strategy_defined_required"] is True
    assert cat["responsible_ai_strategy_defined_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["strategic_objectives"]["count"] >= 10
    assert cat["capability_map"]["domain_count"] >= 6
    assert cat["maturity_model"]["level_count"] >= 6
    assert cat["transformation_roadmap"]["phase_count"] >= 5
    assert cat["knowledge_strategy"]["via_p213_l"] is True
    assert cat["security_strategy"]["via_p210"] is True
    assert cat["cursor_outputs"]["count"] >= 18
    assert "mission_is_undefined" in cat["quality_gates"]["reject_if"]
    assert "P214-A" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/mission" in mod.mission_surface()["routes"]
    assert "GET /ai/mission/maturity" in mod.mission_surface()["routes"]
    assert "GET /ai/mission/roadmap" in mod.mission_surface()["routes"]


@pytest.mark.unit
def test_ai_mission_acl():
    from contexts.ai.infrastructure.acl import ai_mission_acl as acls

    assert acls.to_foundation(tenant_id="t1", profile_ref="p1")[
        "via_p214_a"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")["via_p213_l"] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")["via_p212_l"] is True
    assert acls.to_cyber_security(tenant_id="t1", control_ref="c1")[
        "via_p210"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_autonomous_di(tenant_id="t1", decision_ref="d1")[
        "via_p213_m"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission"]["prompt_id"] == "P214-B"
    assert catalog["platform_mission"]["adr"] == 422
    assert catalog["platform_mission"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_mission()
    assert summary["prompt_id"] == "P214-B"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-A" in summary["builds_on"]
    assert summary["objective_count"] >= 10
    assert summary["capability_domain_count"] >= 6
    assert summary["maturity_level_count"] >= 6
    assert summary["roadmap_phase_count"] >= 5
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.mission_readiness()["passed"] is True
    assert svc.mission_maturity()["level_count"] >= 6
    assert svc.mission_security()["via_p210"] is True
    assert svc.mission_knowledge()["via_p213_l"] is True
