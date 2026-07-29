"""P214-F Enterprise AI Agent & Autonomous Intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_agents_foundation import (
    validate_ai_agents_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_agents as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_agents_foundation():
    result = validate_ai_agents_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-F"
    assert result["adr"] == 426
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_agents_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-F"
    assert cat["adr"] == 426
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "digital workers" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 8
    assert cat["lifecycle"]["stage_count"] >= 10
    assert cat["enterprise_ai_agent_platform_present_required"] is True
    assert cat["agent_identity_present_required"] is True
    assert cat["agent_memory_present_required"] is True
    assert cat["agent_reasoning_present_required"] is True
    assert cat["multi_agent_architecture_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["identity"]["via_p207"] is True
    assert cat["memory"]["via_p214_e"] is True
    assert cat["knowledge"]["via_p212"] is True
    assert cat["deployment"]["via_p213_o"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_agent_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-E" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/agents" in mod.agents_surface()["routes"]
    assert "GET /ai/agents/memory" in mod.agents_surface()["routes"]
    assert "GET /ai/agents/multi-agent" in mod.agents_surface()["routes"]


@pytest.mark.unit
def test_ai_agents_acl():
    from contexts.ai.infrastructure.acl import ai_agents_acl as acls

    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="p1", action="tool.invoke"
    )["via_p208"] is True
    assert acls.to_knowledge_graph(tenant_id="t1", graph_ref="g1")[
        "via_p213_l"
    ] is True
    assert acls.to_genai(tenant_id="t1", model_ref="m1")[
        "via_p214_e"
    ] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")[
        "via_workflow_engine"
    ] is True
    assert acls.to_data_governance(tenant_id="t1", product_ref="d1")[
        "via_p212"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", agent_ref="a1")[
        "module_local_agent_runtime_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_agents():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_agents"]["prompt_id"] == "P214-F"
    assert catalog["platform_agents"]["adr"] == 426
    assert catalog["platform_agents"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_agents"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_agents()
    assert summary["prompt_id"] == "P214-F"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-E" in summary["builds_on"]
    assert summary["context_count"] >= 8
    assert summary["lifecycle_stage_count"] >= 10
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.agents_readiness()["passed"] is True
    assert svc.agents_identity()["via_p207"] is True
    assert svc.agents_memory()["via_p214_e"] is True
    assert svc.agents_multi_agent()["present_required"] is True
    assert svc.agents_digital_twin()["present_required"] is True
