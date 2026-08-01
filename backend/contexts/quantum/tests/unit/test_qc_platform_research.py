"""P215-Q quantum research / innovation lab / discovery foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_research_foundation import validate_qc_research_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_research as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_research_foundation():
    result = validate_qc_research_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-Q"
    assert result["adr"] == 462
@pytest.mark.unit
def test_qc_research_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-Q"
    assert cat["fabric"] == "meos_quantum_discovery_intelligence_fabric"
    assert cat["quantum_research_platform_present_required"] is True
    assert cat["quantum_innovation_lab_present_required"] is True
    assert cat["scientific_collaboration_platform_present_required"] is True
    assert cat["discovery_intelligence_present_required"] is True
    assert cat["ai_assisted_research_present_required"] is True
    assert cat["experiment_management_present_required"] is True
    assert cat["future_technology_radar_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["via_p214_g"] is True
    assert cat["via_document_exchange"] is True
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/research" in mod.research_surface()["routes"]
@pytest.mark.unit
def test_qc_research_acl():
    from contexts.quantum.infrastructure.acl import qc_research_acl as acls
    assert acls.to_scientific(tenant_id="t1", scientific_ref="s1")["via_p215_g"] is True
    assert acls.to_knowledge_rag(tenant_id="t1", rag_ref="r1")["via_p214_g"] is True
    assert acls.to_document_exchange(tenant_id="t1", document_id="d1")["module_local_publication_blob_forbidden"] is True
    assert acls.to_quantum_marketplace(tenant_id="t1", marketplace_ref="m1")["via_p215_p"] is True
    assert acls.to_qai(tenant_id="t1", qai_ref="q1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["ungated_dual_use_research_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_research():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_research"]["prompt_id"] == "P215-Q"; assert svc.research_readiness()["passed"] is True
