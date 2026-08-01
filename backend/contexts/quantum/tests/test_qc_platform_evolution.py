"""P215-U quantum autonomous evolution / self-healing foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_evolution_foundation import validate_qc_evolution_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_evolution as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_evolution_foundation():
    result = validate_qc_evolution_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-U"
    assert result["adr"] == 466
@pytest.mark.unit
def test_qc_evolution_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-U"
    assert cat["fabric"] == "meos_quantum_autonomous_evolution_fabric"
    assert cat["os_gate"] == "P215-T"
    assert cat["trust_gate"] == "P215-K"
    assert cat["quantum_autonomous_intelligence_platform_present_required"] is True
    assert cat["self_healing_ecosystem_present_required"] is True
    assert cat["autonomous_agents_present_required"] is True
    assert cat["evolution_intelligence_present_required"] is True
    assert cat["singularity_readiness_framework_present_required"] is True
    assert cat["self_optimization_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_t"] is True
    assert cat["never_replace_p215_k"] is True
    assert cat["ungated_autonomous_actions_forbidden"] is True
    assert cat["via_p214_z"] is True
    assert "GET /quantum/evolution" in mod.evolution_surface()["routes"]
@pytest.mark.unit
def test_qc_evolution_acl():
    from contexts.quantum.infrastructure.acl import qc_evolution_acl as acls
    assert acls.to_quantum_os(tenant_id="t1", os_ref="os1")["never_replace_p215_t"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["ungated_autonomous_actions_forbidden"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_aiops(tenant_id="t1", aiops_ref="a1")["via_p214_j"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
    assert acls.to_quantum_research(tenant_id="t1", research_ref="r1")["via_p215_q"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_evolution():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_evolution"]["prompt_id"] == "P215-U"; assert svc.evolution_readiness()["passed"] is True
