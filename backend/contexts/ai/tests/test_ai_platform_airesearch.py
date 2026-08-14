"""P214-S AI Research / Innovation Lab / Future Evolution foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_airesearch_foundation import (
    validate_ai_airesearch_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_airesearch as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_airesearch_foundation():
    result = validate_ai_airesearch_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-S"
    assert result["adr"] == 439
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_airesearch_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-S"
    assert cat["adr"] == 439
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "continuously evolving intelligent enterprise capable of discovering and creating future AI capabilities" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_research_platform_present_required"] is True
    assert cat["ai_innovation_lab_present_required"] is True
    assert cat["experimentation_platform_present_required"] is True
    assert cat["prototype_factory_present_required"] is True
    assert cat["deepens_p214_r_future_evolution"] is True
    assert cat["governed_by_p214_p"] is True
    assert cat["experimentation"]["via_p214_o"] is True
    assert cat["experimentation"]["via_p214_l"] is True
    assert cat["prototypes"]["via_p214_n"] is True
    assert cat["knowledge"]["via_p214_g"] is True
    assert cat["roadmap"]["via_p214_r"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert "enterprise_ai_research_platform_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-R" in cat["builds_on"]
    assert "P214-P" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/airesearch" in mod.airesearch_surface()["routes"]
    assert "GET /ai/airesearch/experiments" in mod.airesearch_surface()["routes"]
    assert "GET /ai/airesearch/roadmap" in mod.airesearch_surface()["routes"]


@pytest.mark.unit
def test_ai_airesearch_acl():
    from contexts.ai.infrastructure.acl import ai_airesearch_acl as acls

    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_modelintel(tenant_id="t1", model_ref="m1")["via_p214_l"] is True
    assert acls.to_aiinfra(tenant_id="t1", infra_ref="n1")["via_p214_n"] is True
    assert acls.to_aiqa(tenant_id="t1", qa_ref="q1")["via_p214_o"] is True
    assert acls.to_aitrust(tenant_id="t1", trust_ref="tr1")["via_p214_p"] is True
    assert acls.to_aiworkforce(tenant_id="t1", workforce_ref="wf1")["via_p214_q"] is True
    assert acls.to_aimarket(tenant_id="t1", market_ref="mk1")["via_p214_r"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", research_ref="rs1")["module_local_ai_research_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_airesearch():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_airesearch"]["prompt_id"] == "P214-S"
    assert catalog["platform_airesearch"]["adr"] == 439
    assert catalog["platform_airesearch"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_airesearch"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_airesearch()
    assert summary["prompt_id"] == "P214-S"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-R" in summary["builds_on"]
    assert "P214-P" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.airesearch_readiness()["passed"] is True
    assert svc.airesearch_experiments()["via_p214_o"] is True
    assert svc.airesearch_prototypes()["via_p214_n"] is True
    assert svc.airesearch_knowledge()["via_p214_g"] is True
    assert svc.airesearch_roadmap()["via_p214_r"] is True
    assert svc.airesearch_digital_twin()["present_required"] is True
