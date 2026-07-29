"""P214-Q Autonomous AI Ecosystem / Digital Workforce foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aiworkforce_foundation import (
    validate_ai_aiworkforce_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aiworkforce as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aiworkforce_foundation():
    result = validate_ai_aiworkforce_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-Q"
    assert result["adr"] == 437
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aiworkforce_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-Q"
    assert cat["adr"] == 437
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "self-improving intelligent enterprise operating system" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_autonomous_ai_ecosystem_present_required"] is True
    assert cat["ai_digital_workforce_present_required"] is True
    assert cat["multi_agent_platform_present_required"] is True
    assert cat["ai_organization_model_present_required"] is True
    assert cat["autonomous_workflow_platform_present_required"] is True
    assert cat["governed_by_p214_p"] is True
    assert cat["ecosystem"]["via_p214_f"] is True
    assert cat["learning"]["via_p214_o"] is True
    assert cat["decision_autonomy"]["via_p214_p"] is True
    assert cat["memory"]["via_p214_g"] is True
    assert cat["evolution"]["via_p214_j"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "enterprise_autonomous_ai_ecosystem_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-P" in cat["builds_on"]
    assert "P214-F" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aiworkforce" in mod.aiworkforce_surface()["routes"]
    assert "GET /ai/aiworkforce/learning" in mod.aiworkforce_surface()["routes"]
    assert "GET /ai/aiworkforce/decisions" in mod.aiworkforce_surface()["routes"]


@pytest.mark.unit
def test_ai_aiworkforce_acl():
    from contexts.ai.infrastructure.acl import ai_aiworkforce_acl as acls

    assert acls.to_agents(tenant_id="t1", agent_ref="a1")["via_p214_f"] is True
    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_aiops(tenant_id="t1", ops_ref="o1")["via_p214_j"] is True
    assert acls.to_modelintel(tenant_id="t1", model_ref="m1")["via_p214_l"] is True
    assert acls.to_aiinteg(tenant_id="t1", integration_ref="i1")["via_p214_m"] is True
    assert acls.to_aiinfra(tenant_id="t1", infra_ref="n1")["via_p214_n"] is True
    assert acls.to_aiqa(tenant_id="t1", qa_ref="q1")["via_p214_o"] is True
    assert acls.to_aitrust(tenant_id="t1", trust_ref="tr1")["via_p214_p"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", workforce_ref="wf1")["module_local_ai_workforce_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aiworkforce():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aiworkforce"]["prompt_id"] == "P214-Q"
    assert catalog["platform_aiworkforce"]["adr"] == 437
    assert catalog["platform_aiworkforce"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aiworkforce"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aiworkforce()
    assert summary["prompt_id"] == "P214-Q"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-P" in summary["builds_on"]
    assert "P214-F" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aiworkforce_readiness()["passed"] is True
    assert svc.aiworkforce_ecosystem()["via_p214_f"] is True
    assert svc.aiworkforce_learning()["via_p214_o"] is True
    assert svc.aiworkforce_decisions()["via_p214_p"] is True
    assert svc.aiworkforce_memory()["via_p214_g"] is True
    assert svc.aiworkforce_digital_twin()["present_required"] is True
