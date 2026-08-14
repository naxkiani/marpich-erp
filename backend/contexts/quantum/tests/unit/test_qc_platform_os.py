"""P215-T quantum OS / control plane / intelligence core foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_os_foundation import validate_qc_os_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_os as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_os_foundation():
    result = validate_qc_os_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-T"
    assert result["adr"] == 465
@pytest.mark.unit
def test_qc_os_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-T"
    assert cat["fabric"] == "meos_quantum_intelligence_operating_fabric"
    assert cat["trust_gate"] == "P215-K"
    assert cat["security_gate"] == "P215-H"
    assert cat["quantum_operating_system_present_required"] is True
    assert cat["quantum_control_plane_present_required"] is True
    assert cat["autonomous_governance_present_required"] is True
    assert cat["quantum_intelligence_core_present_required"] is True
    assert cat["resource_orchestration_present_required"] is True
    assert cat["policy_engine_present_required"] is True
    assert cat["agent_management_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_core_platform"] is True
    assert cat["never_replace_p215_k"] is True
    assert cat["never_replace_p215_h"] is True
    assert cat["via_policy_engine"] is True
    assert cat["via_p214_z"] is True
    assert "GET /quantum/os" in mod.os_surface()["routes"]
@pytest.mark.unit
def test_qc_os_acl():
    from contexts.quantum.infrastructure.acl import qc_os_acl as acls
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["never_replace_p215_k"] is True
    assert acls.to_quantum_security(tenant_id="t1", security_ref="s1")["never_replace_p215_h"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["module_local_pdp_forbidden"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_infrastructure(tenant_id="t1", infra_ref="i1")["via_p215_d"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_os():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_os"]["prompt_id"] == "P215-T"; assert svc.os_readiness()["passed"] is True
