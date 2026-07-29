"""P214-V AGI cognitive-core foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_agi_foundation import validate_ai_agi_foundation
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_agi as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_agi_foundation():
    result = validate_ai_agi_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-V"
    assert result["adr"] == 442
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-003"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_agi_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-V"
    assert cat["adr"] == 442
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "cognitive enterprise intelligence platform" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_agi_platform_present_required"] is True
    assert cat["cognitive_intelligence_core_present_required"] is True
    assert cat["universal_reasoning_engine_present_required"] is True
    assert cat["deepens_p214_u_cognitive_core"] is True
    assert cat["coordinated_by_p214_t"] is True
    assert cat["agi_core"]["via_p214_t"] is True
    assert cat["agi_core"]["via_p214_u"] is True
    assert cat["memory"]["via_p214_g"] is True
    assert cat["strategic_intelligence"]["via_p213"] is True
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 9
    assert cat["cursor_outputs"]["count"] >= 20
    assert "enterprise_agi_platform_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-U" in cat["builds_on"]
    assert "P214-T" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/agi" in mod.agi_surface()["routes"]
    assert "GET /ai/agi/core" in mod.agi_surface()["routes"]
    assert "GET /ai/agi/strategic-intelligence" in mod.agi_surface()["routes"]


@pytest.mark.unit
def test_ai_agi_acl():
    from contexts.ai.infrastructure.acl import ai_agi_acl as acls

    assert acls.to_knowledge(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_aiworkforce(tenant_id="t1", workforce_ref="wf1")["via_p214_q"] is True
    assert acls.to_aios(tenant_id="t1", control_ref="cp1")["via_p214_t"] is True
    assert acls.to_aigov(tenant_id="t1", guardian_ref="gv1")["via_p214_u"] is True
    assert acls.to_decision_intelligence(tenant_id="t1", decision_ref="d1")["via_p213"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", agi_ref="a1")["module_local_agi_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_agi():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_agi"]["prompt_id"] == "P214-V"
    assert catalog["platform_agi"]["adr"] == 442
    assert catalog["platform_agi"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_agi"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_agi()
    assert summary["prompt_id"] == "P214-V"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-U" in summary["builds_on"]
    assert "P214-T" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 9
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.agi_readiness()["passed"] is True
    assert svc.agi_core()["via_p214_t"] is True
    assert svc.agi_core()["via_p214_u"] is True
    assert svc.agi_memory()["via_p214_g"] is True
    assert svc.agi_digital_twin()["present_required"] is True
