"""P214-R AI Ecosystem Marketplace / Capability Exchange foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aimarket_foundation import (
    validate_ai_aimarket_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aimarket as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aimarket_foundation():
    result = validate_ai_aimarket_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-R"
    assert result["adr"] == 438
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aimarket_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-R"
    assert cat["adr"] == 438
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "discoverable, governed and reusable enterprise intelligence assets" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_marketplace_present_required"] is True
    assert cat["ai_capability_registry_present_required"] is True
    assert cat["ai_model_exchange_present_required"] is True
    assert cat["ai_plugin_marketplace_present_required"] is True
    assert cat["plugin_marketplace_via_platform_required"] is True
    assert cat["models"]["via_p214_l"] is True
    assert cat["agents"]["via_p214_f"] is True
    assert cat["agents"]["via_p214_q"] is True
    assert cat["services"]["via_p214_m"] is True
    assert cat["plugins"]["via_plugin_platform"] is True
    assert cat["trust_rating"]["via_p214_p"] is True
    assert cat["trust_rating"]["via_p214_o"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "enterprise_ai_marketplace_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P214-Q" in cat["builds_on"]
    assert "P214-P" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aimarket" in mod.aimarket_surface()["routes"]
    assert "GET /ai/aimarket/plugins" in mod.aimarket_surface()["routes"]
    assert "GET /ai/aimarket/economy" in mod.aimarket_surface()["routes"]


@pytest.mark.unit
def test_ai_aimarket_acl():
    from contexts.ai.infrastructure.acl import ai_aimarket_acl as acls

    assert acls.to_agents(tenant_id="t1", agent_ref="a1")["via_p214_f"] is True
    assert acls.to_modelintel(tenant_id="t1", model_ref="m1")["via_p214_l"] is True
    assert acls.to_aiinteg(tenant_id="t1", integration_ref="i1")["via_p214_m"] is True
    assert acls.to_aiqa(tenant_id="t1", qa_ref="q1")["via_p214_o"] is True
    assert acls.to_aitrust(tenant_id="t1", trust_ref="tr1")["via_p214_p"] is True
    assert acls.to_aiworkforce(tenant_id="t1", workforce_ref="wf1")["via_p214_q"] is True
    assert acls.to_plugin_platform(tenant_id="t1", plugin_ref="pl1")["via_plugin_platform"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", market_ref="mk1")["module_local_ai_marketplace_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aimarket():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aimarket"]["prompt_id"] == "P214-R"
    assert catalog["platform_aimarket"]["adr"] == 438
    assert catalog["platform_aimarket"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aimarket"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aimarket()
    assert summary["prompt_id"] == "P214-R"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-Q" in summary["builds_on"]
    assert "P214-P" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aimarket_readiness()["passed"] is True
    assert svc.aimarket_models()["via_p214_l"] is True
    assert svc.aimarket_agents()["via_p214_f"] is True
    assert svc.aimarket_plugins()["via_plugin_platform"] is True
    assert svc.aimarket_trust_rating()["via_p214_p"] is True
    assert svc.aimarket_digital_twin()["present_required"] is True
