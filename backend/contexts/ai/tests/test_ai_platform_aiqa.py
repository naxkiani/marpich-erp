"""P214-O Enterprise AI Testing / Evaluation / QA foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aiqa_foundation import (
    validate_ai_aiqa_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aiqa as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aiqa_foundation():
    result = validate_ai_aiqa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-O"
    assert result["adr"] == 435
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aiqa_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-O"
    assert cat["adr"] == 435
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "continuous intelligent validation" in cat["principle"]
    assert "autonomous improvement" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_testing_platform_present_required"] is True
    assert cat["ai_evaluation_platform_present_required"] is True
    assert cat["ai_safety_testing_present_required"] is True
    assert cat["ai_certification_platform_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["genai_quality"]["via_p214_e"] is True
    assert cat["agent_testing"]["via_p214_f"] is True
    assert cat["safety"]["via_p214_h"] is True
    assert cat["safety"]["via_p214_i"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_testing_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-N" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aiqa" in mod.aiqa_surface()["routes"]
    assert "GET /ai/aiqa/safety" in mod.aiqa_surface()["routes"]
    assert "GET /ai/aiqa/quality-score" in mod.aiqa_surface()["routes"]


@pytest.mark.unit
def test_ai_aiqa_acl():
    from contexts.ai.infrastructure.acl import ai_aiqa_acl as acls

    assert acls.to_mlops(tenant_id="t1", model_ref="m1")[
        "via_p214_d"
    ] is True
    assert acls.to_genai(tenant_id="t1", model_ref="g1")[
        "via_p214_e"
    ] is True
    assert acls.to_agents(tenant_id="t1", agent_ref="a1")[
        "via_p214_f"
    ] is True
    assert acls.to_governance(tenant_id="t1", policy_ref="p1")[
        "via_p214_h"
    ] is True
    assert acls.to_aisec(tenant_id="t1", security_ref="s1")[
        "via_p214_i"
    ] is True
    assert acls.to_aiinfra(tenant_id="t1", infra_ref="i1")[
        "via_p214_n"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", qa_ref="q1")[
        "module_local_ai_qa_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aiqa():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aiqa"]["prompt_id"] == "P214-O"
    assert catalog["platform_aiqa"]["adr"] == 435
    assert catalog["platform_aiqa"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aiqa"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aiqa()
    assert summary["prompt_id"] == "P214-O"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-N" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aiqa_readiness()["passed"] is True
    assert svc.aiqa_genai_quality()["via_p214_e"] is True
    assert svc.aiqa_safety()["via_p214_h"] is True
    assert svc.aiqa_agent_testing()["via_p214_f"] is True
    assert svc.aiqa_quality_score()["present_required"] is True
    assert svc.aiqa_digital_twin()["present_required"] is True
