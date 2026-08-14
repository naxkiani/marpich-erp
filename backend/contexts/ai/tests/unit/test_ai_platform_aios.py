"""P214-T AI Operating System / Control Plane foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aios_foundation import (
    validate_ai_aios_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aios as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aios_foundation():
    result = validate_ai_aios_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-T"
    assert result["adr"] == 440
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aios_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-T"
    assert cat["adr"] == 440
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "manages, coordinates, governs and evolves all AI capabilities across MEOS" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_operating_system_present_required"] is True
    assert cat["ai_control_plane_present_required"] is True
    assert cat["autonomous_orchestration_present_required"] is True
    assert cat["ai_command_center_present_required"] is True
    assert cat["deepens_p214_s_control_plane"] is True
    assert cat["governed_by_p214_p"] is True
    assert cat["orchestration"]["via_p214_q"] is True
    assert cat["policy_control"]["via_p214_p"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert "enterprise_ai_operating_system_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-S" in cat["builds_on"]
    assert "P214-P" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aios" in mod.aios_surface()["routes"]
    assert "GET /ai/aios/control-plane" in mod.aios_surface()["routes"]
    assert "GET /ai/aios/command-center" in mod.aios_surface()["routes"]


@pytest.mark.unit
def test_ai_aios_acl():
    from contexts.ai.infrastructure.acl import ai_aios_acl as acls

    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_aiops(tenant_id="t1", ops_ref="o1")["via_p214_j"] is True
    assert acls.to_aitrust(tenant_id="t1", trust_ref="tr1")["via_p214_p"] is True
    assert acls.to_aiworkforce(tenant_id="t1", workforce_ref="wf1")["via_p214_q"] is True
    assert acls.to_aimarket(tenant_id="t1", market_ref="mk1")["via_p214_r"] is True
    assert acls.to_airesearch(tenant_id="t1", research_ref="rs1")["via_p214_s"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", os_ref="os1")["module_local_aios_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aios():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aios"]["prompt_id"] == "P214-T"
    assert catalog["platform_aios"]["adr"] == 440
    assert catalog["platform_aios"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aios"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aios()
    assert summary["prompt_id"] == "P214-T"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-S" in summary["builds_on"]
    assert "P214-P" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aios_readiness()["passed"] is True
    assert svc.aios_orchestration()["via_p214_q"] is True
    assert svc.aios_policy_control()["via_p214_p"] is True
    assert svc.aios_knowledge_graph()["via_p214_g"] is True
    assert svc.aios_digital_twin()["present_required"] is True
