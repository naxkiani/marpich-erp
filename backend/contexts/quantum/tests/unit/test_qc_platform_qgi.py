"""P215-V quantum QGI / cognitive enterprise foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_qgi_foundation import validate_qc_qgi_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_qgi as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_qgi_foundation():
    result = validate_qc_qgi_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-V"
    assert result["adr"] == 467
@pytest.mark.unit
def test_qc_qgi_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-V"
    assert cat["fabric"] == "meos_quantum_cognitive_intelligence_fabric"
    assert cat["evolution_gate"] == "P215-U"
    assert cat["os_gate"] == "P215-T"
    assert cat["trust_gate"] == "P215-K"
    assert cat["quantum_general_intelligence_platform_present_required"] is True
    assert cat["cognitive_enterprise_brain_present_required"] is True
    assert cat["advanced_reasoning_engine_present_required"] is True
    assert cat["knowledge_understanding_layer_present_required"] is True
    assert cat["cognitive_agent_network_present_required"] is True
    assert cat["enterprise_memory_platform_present_required"] is True
    assert cat["intelligence_evolution_framework_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_u"] is True
    assert cat["never_replace_p215_t"] is True
    assert cat["ungated_agi_class_actions_forbidden"] is True
    assert cat["opaque_unexplainable_decisions_forbidden"] is True
    assert cat["via_p214_z"] is True
    assert "GET /quantum/qgi" in mod.qgi_surface()["routes"]
@pytest.mark.unit
def test_qc_qgi_acl():
    from contexts.quantum.infrastructure.acl import qc_qgi_acl as acls
    assert acls.to_quantum_evolution(tenant_id="t1", evolution_ref="e1")["never_replace_p215_u"] is True
    assert acls.to_quantum_os(tenant_id="t1", os_ref="os1")["never_replace_p215_t"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_decision_intelligence(tenant_id="t1", decision_ref="d1")["opaque_unexplainable_decisions_forbidden"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["ungated_agi_class_actions_forbidden"] is True
    assert acls.to_knowledge_rag(tenant_id="t1", rag_ref="r1")["via_p214_g"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qgi():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_qgi"]["prompt_id"] == "P215-V"; assert svc.qgi_readiness()["passed"] is True
