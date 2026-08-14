"""P214-G Enterprise AI Knowledge / RAG / Cognitive foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_knowledge_foundation import (
    validate_ai_knowledge_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_knowledge as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_knowledge_foundation():
    result = validate_ai_knowledge_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-G"
    assert result["adr"] == 427
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_knowledge_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-G"
    assert cat["adr"] == 427
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "trusted cognitive foundation" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["rag_platform"]["pipeline_count"] >= 11
    assert cat["enterprise_ai_knowledge_platform_present_required"] is True
    assert cat["rag_platform_present_required"] is True
    assert cat["vector_intelligence_platform_present_required"] is True
    assert cat["ai_memory_platform_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["governance"]["via_p212"] is True
    assert cat["semantic"]["via_p213_l"] is True
    assert cat["rag_platform"]["via_p214_e"] is True
    assert cat["memory"]["via_p214_f"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_knowledge_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-F" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/knowledge" in mod.knowledge_surface()["routes"]
    assert "GET /ai/knowledge/rag" in mod.knowledge_surface()["routes"]
    assert "GET /ai/knowledge/graph-rag" in mod.knowledge_surface()["routes"]


@pytest.mark.unit
def test_ai_knowledge_acl():
    from contexts.ai.infrastructure.acl import ai_knowledge_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", graph_ref="g1")[
        "via_p213_l"
    ] is True
    assert acls.to_genai(tenant_id="t1", model_ref="m1")[
        "via_p214_e"
    ] is True
    assert acls.to_agents(tenant_id="t1", agent_ref="a1")[
        "via_p214_f"
    ] is True
    assert acls.to_documents(tenant_id="t1", document_ref="d1")[
        "via_documents"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", knowledge_ref="k1")[
        "module_local_vector_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_knowledge():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_knowledge"]["prompt_id"] == "P214-G"
    assert catalog["platform_knowledge"]["adr"] == 427
    assert catalog["platform_knowledge"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_knowledge"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_knowledge()
    assert summary["prompt_id"] == "P214-G"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-F" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["rag_pipeline_count"] >= 11
    assert summary["lifecycle_stage_count"] >= 8
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.knowledge_readiness()["passed"] is True
    assert svc.knowledge_rag()["via_p214_e"] is True
    assert svc.knowledge_governance()["via_p212"] is True
    assert svc.knowledge_memory()["via_p214_f"] is True
    assert svc.knowledge_vectors()["present_required"] is True
