"""P215-X quantum future / post-QGI / singularity evolution foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_future_foundation import validate_qc_future_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_future as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_future_foundation():
    result = validate_qc_future_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-X"
    assert result["adr"] == 469
@pytest.mark.unit
def test_qc_future_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-X"
    assert cat["fabric"] == "meos_ultimate_intelligence_evolution_fabric"
    assert cat["civilization_gate"] == "P215-W"
    assert cat["qgi_gate"] == "P215-V"
    assert cat["evolution_gate"] == "P215-U"
    assert cat["os_gate"] == "P215-T"
    assert cat["trust_gate"] == "P215-K"
    assert cat["future_quantum_architecture_platform_present_required"] is True
    assert cat["post_qgi_evolution_framework_present_required"] is True
    assert cat["singularity_evolution_engine_present_required"] is True
    assert cat["intelligence_expansion_platform_present_required"] is True
    assert cat["future_scenario_simulator_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_w"] is True
    assert cat["ungoverned_singularity_acceleration_forbidden"] is True
    assert cat["via_p214_z"] is True
    assert "GET /quantum/future" in mod.future_surface()["routes"]
@pytest.mark.unit
def test_qc_future_acl():
    from contexts.quantum.infrastructure.acl import qc_future_acl as acls
    assert acls.to_quantum_civilization(tenant_id="t1", civilization_ref="c1")["never_replace_p215_w"] is True
    assert acls.to_quantum_qgi(tenant_id="t1", qgi_ref="q1")["never_replace_p215_v"] is True
    assert acls.to_quantum_evolution(tenant_id="t1", evolution_ref="e1")["never_replace_p215_u"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungoverned_singularity_acceleration_forbidden"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["via_p215_k"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_future():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_future"]["prompt_id"] == "P215-X"; assert svc.future_readiness()["passed"] is True
