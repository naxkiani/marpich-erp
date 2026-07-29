"""P214-U Autonomous AI Governance guardian-layer foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aigovernance_foundation import (
    validate_ai_aigovernance_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aigovernance as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aigovernance_foundation():
    result = validate_ai_aigovernance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-U"
    assert result["adr"] == 441
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-002"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aigovernance_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-U"
    assert cat["adr"] == 441
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "safely manage, govern and evolve increasingly autonomous intelligence systems" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["autonomous_ai_governance_present_required"] is True
    assert cat["self_healing_intelligence_present_required"] is True
    assert cat["ai_alignment_platform_present_required"] is True
    assert cat["deepens_p214_t_guardian_layer"] is True
    assert cat["governed_by_p214_p"] is True
    assert cat["autonomous_governance"]["via_p214_p"] is True
    assert cat["autonomous_governance"]["via_p214_t"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert "autonomous_ai_governance_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-T" in cat["builds_on"]
    assert "P214-P" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aigov" in mod.aigov_surface()["routes"]
    assert "GET /ai/aigov/autonomous-governance" in mod.aigov_surface()["routes"]
    assert "GET /ai/aigov/agi-readiness" in mod.aigov_surface()["routes"]


@pytest.mark.unit
def test_ai_aigovernance_acl():
    from contexts.ai.infrastructure.acl import ai_aigovernance_acl as acls

    assert acls.to_aitrust(tenant_id="t1", trust_ref="tr1")["via_p214_p"] is True
    assert acls.to_aios(tenant_id="t1", control_ref="cp1")["via_p214_t"] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_aiworkforce(tenant_id="t1", workforce_ref="wf1")["via_p214_q"] is True
    assert acls.to_airesearch(tenant_id="t1", research_ref="rs1")["via_p214_s"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", guardian_ref="g1")["module_local_guardian_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aigovernance():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aigovernance"]["prompt_id"] == "P214-U"
    assert catalog["platform_aigovernance"]["adr"] == 441
    assert catalog["platform_aigovernance"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aigovernance"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aigovernance()
    assert summary["prompt_id"] == "P214-U"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-T" in summary["builds_on"]
    assert "P214-P" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aigov_readiness()["passed"] is True
    assert svc.aigov_autonomous_governance()["via_p214_t"] is True
    assert svc.aigov_autonomous_governance()["via_p214_p"] is True
    assert svc.aigov_knowledge_graph()["via_p214_g"] is True
    assert svc.aigov_digital_twin()["present_required"] is True
