"""P215-Y quantum ultimate trust / alignment / ethics foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_ultimate_trust_foundation import validate_qc_ultimate_trust_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_ultimate_trust as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_ultimate_trust_foundation():
    result = validate_qc_ultimate_trust_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-Y"
    assert result["adr"] == 470
@pytest.mark.unit
def test_qc_ultimate_trust_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-Y"
    assert cat["fabric"] == "meos_quantum_trust_civilization_fabric"
    assert cat["future_gate"] == "P215-X"
    assert cat["civilization_gate"] == "P215-W"
    assert cat["qgi_gate"] == "P215-V"
    assert cat["evolution_gate"] == "P215-U"
    assert cat["os_gate"] == "P215-T"
    assert cat["trust_gate"] == "P215-K"
    assert cat["ultimate_quantum_governance_platform_present_required"] is True
    assert cat["intelligence_alignment_framework_present_required"] is True
    assert cat["quantum_ethics_civilization_layer_present_required"] is True
    assert cat["trust_architecture_platform_present_required"] is True
    assert cat["responsible_intelligence_framework_present_required"] is True
    assert cat["autonomous_governance_assurance_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_k"] is True
    assert cat["ungoverned_intelligence_misalignment_forbidden"] is True
    assert cat["opaque_ethics_decisions_forbidden"] is True
    assert cat["via_p214_z"] is True
    assert "GET /quantum/ultimate-trust" in mod.ultimate_trust_surface()["routes"]
@pytest.mark.unit
def test_qc_ultimate_trust_acl():
    from contexts.quantum.infrastructure.acl import qc_ultimate_trust_acl as acls
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["never_replace_p215_k"] is True
    assert acls.to_quantum_future(tenant_id="t1", future_ref="f1")["never_replace_p215_x"] is True
    assert acls.to_quantum_qgi(tenant_id="t1", qgi_ref="q1")["never_replace_p215_v"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["ungoverned_intelligence_misalignment_forbidden"] is True
    assert acls.to_ethics(tenant_id="t1", ethics_ref="e1")["opaque_ethics_decisions_forbidden"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ultimate_trust():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_ultimate_trust"]["prompt_id"] == "P215-Y"; assert svc.ultimate_trust_readiness()["passed"] is True
