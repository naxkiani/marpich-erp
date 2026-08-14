"""P214-E Enterprise Generative AI & LLM foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_genai_foundation import (
    validate_ai_genai_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_genai as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_genai_foundation():
    result = validate_ai_genai_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-E"
    assert result["adr"] == 425
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_genai_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-E"
    assert cat["adr"] == 425
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "cognitive interface" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["llmops"]["stage_count"] >= 9
    assert cat["assistants"]["copilot_count"] >= 8
    assert cat["enterprise_generative_ai_platform_present_required"] is True
    assert cat["prompt_intelligence_platform_present_required"] is True
    assert cat["rag_platform_present_required"] is True
    assert cat["vector_intelligence_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["rag_platform"]["via_p212"] is True
    assert cat["rag_platform"]["via_p213_l"] is True
    assert cat["deployment"]["via_p213_o"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["rag_platform"]["pipeline_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_generative_ai_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-D" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/genai" in mod.genai_surface()["routes"]
    assert "GET /ai/genai/rag" in mod.genai_surface()["routes"]
    assert "GET /ai/genai/assistants" in mod.genai_surface()["routes"]


@pytest.mark.unit
def test_ai_genai_acl():
    from contexts.ai.infrastructure.acl import ai_genai_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", graph_ref="g1")[
        "via_p213_l"
    ] is True
    assert acls.to_ops_deploy(tenant_id="t1", release_ref="r1")[
        "via_p213_o"
    ] is True
    assert acls.to_foundation(tenant_id="t1", profile_ref="pf1")[
        "via_p214_a"
    ] is True
    assert acls.to_domain(tenant_id="t1", context_ref="c1")[
        "via_p214_c"
    ] is True
    assert acls.to_mlops(tenant_id="t1", registry_ref="reg1")[
        "via_p214_d"
    ] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", secret_ref="s1")[
        "model_signing"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_genai():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_genai"]["prompt_id"] == "P214-E"
    assert catalog["platform_genai"]["adr"] == 425
    assert catalog["platform_genai"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_genai"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_genai()
    assert summary["prompt_id"] == "P214-E"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-D" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["llmops_stage_count"] >= 9
    assert summary["copilot_count"] >= 8
    assert summary["rag_pipeline_count"] >= 8
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.genai_readiness()["passed"] is True
    assert svc.genai_rag()["via_p212"] is True
    assert svc.genai_rag()["via_p213_l"] is True
    assert svc.genai_foundation_registry()["present_required"] is True
    assert svc.genai_assistants()["present_required"] is True
