"""P215-W quantum civilization / collective intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_civilization_foundation import validate_qc_civilization_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_civilization as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_civilization_foundation():
    result = validate_qc_civilization_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-W"
    assert result["adr"] == 468
@pytest.mark.unit
def test_qc_civilization_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-W"
    assert cat["fabric"] == "meos_quantum_civilization_intelligence_fabric"
    assert cat["qgi_gate"] == "P215-V"
    assert cat["evolution_gate"] == "P215-U"
    assert cat["os_gate"] == "P215-T"
    assert cat["trust_gate"] == "P215-K"
    assert cat["quantum_civilization_intelligence_layer_present_required"] is True
    assert cat["collective_intelligence_network_present_required"] is True
    assert cat["global_cognitive_ecosystem_present_required"] is True
    assert cat["knowledge_civilization_platform_present_required"] is True
    assert cat["multi_agent_intelligence_society_present_required"] is True
    assert cat["collective_decision_intelligence_present_required"] is True
    assert cat["future_intelligence_evolution_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_v"] is True
    assert cat["ungoverned_cross_tenant_intelligence_federation_forbidden"] is True
    assert cat["opaque_collective_decisions_forbidden"] is True
    assert cat["via_p213"] is True
    assert "GET /quantum/civilization" in mod.civilization_surface()["routes"]
@pytest.mark.unit
def test_qc_civilization_acl():
    from contexts.quantum.infrastructure.acl import qc_civilization_acl as acls
    assert acls.to_quantum_qgi(tenant_id="t1", qgi_ref="q1")["never_replace_p215_v"] is True
    assert acls.to_quantum_evolution(tenant_id="t1", evolution_ref="e1")["never_replace_p215_u"] is True
    assert acls.to_decision_intelligence(tenant_id="t1", decision_ref="d1")["opaque_collective_decisions_forbidden"] is True
    assert acls.to_federation(tenant_id="t1", federation_ref="f1")["ungoverned_cross_tenant_intelligence_federation_forbidden"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["via_p215_k"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_civilization():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_civilization"]["prompt_id"] == "P215-W"; assert svc.civilization_readiness()["passed"] is True
