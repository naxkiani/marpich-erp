"""P214-W civilization-layer foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aicivilization_foundation import (
    validate_ai_aicivilization_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aicivilization as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aicivilization_foundation():
    result = validate_ai_aicivilization_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-W"
    assert result["adr"] == 443
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-004"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aicivilization_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-W"
    assert cat["adr"] == 443
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "living collective intelligence ecosystem" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_civilization_layer_present_required"] is True
    assert cat["collective_intelligence_network_present_required"] is True
    assert cat["knowledge_civilization_platform_present_required"] is True
    assert cat["deepens_p214_v_collective_ecosystem"] is True
    assert cat["guarded_by_p214_u"] is True
    assert cat["coordinated_by_p214_t"] is True
    assert cat["collective_decision"]["via_p213"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert "enterprise_ai_civilization_layer_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-V" in cat["builds_on"]
    assert "P214-U" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aiciv" in mod.aiciv_surface()["routes"]
    assert "GET /ai/aiciv/network" in mod.aiciv_surface()["routes"]
    assert "GET /ai/aiciv/distributed-intelligence" in mod.aiciv_surface()["routes"]


@pytest.mark.unit
def test_ai_aicivilization_acl():
    from contexts.ai.infrastructure.acl import ai_aicivilization_acl as acls

    assert acls.to_aiworkforce(tenant_id="t1", workforce_ref="wf1")["via_p214_q"] is True
    assert acls.to_airesearch(tenant_id="t1", research_ref="rs1")["via_p214_s"] is True
    assert acls.to_aios(tenant_id="t1", control_ref="cp1")["via_p214_t"] is True
    assert acls.to_aigov(tenant_id="t1", guardian_ref="gv1")["via_p214_u"] is True
    assert acls.to_agi(tenant_id="t1", agi_ref="a1")["via_p214_v"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", civilization_ref="c1")["module_local_civilization_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aicivilization():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aicivilization"]["prompt_id"] == "P214-W"
    assert catalog["platform_aicivilization"]["adr"] == 443
    assert catalog["platform_aicivilization"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aicivilization"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aicivilization()
    assert summary["prompt_id"] == "P214-W"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-V" in summary["builds_on"]
    assert "P214-U" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aiciv_readiness()["passed"] is True
    assert svc.aiciv_collective_network()["present_required"] is True
    assert svc.aiciv_collective_decision()["via_p213"] is True
    assert svc.aiciv_knowledge_graph()["via_p214_g"] is True
    assert svc.aiciv_digital_twin()["present_required"] is True
