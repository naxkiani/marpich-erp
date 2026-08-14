"""P215-L quantum digital twin / reality modeling foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_twin_foundation import validate_qc_twin_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_twin as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_twin_foundation():
    result = validate_qc_twin_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-L"
    assert result["adr"] == 457
@pytest.mark.unit
def test_qc_twin_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-L"
    assert cat["fabric"] == "meos_quantum_reality_intelligence_fabric"
    assert cat["quantum_digital_twin_platform_present_required"] is True
    assert cat["quantum_simulation_intelligence_present_required"] is True
    assert cat["quantum_reality_modeling_present_required"] is True
    assert cat["predictive_intelligence_present_required"] is True
    assert cat["scenario_simulation_present_required"] is True
    assert cat["evolution_intelligence_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/twin" in mod.twin_surface()["routes"]
@pytest.mark.unit
def test_qc_twin_acl():
    from contexts.quantum.infrastructure.acl import qc_twin_acl as acls
    assert acls.to_infrastructure(tenant_id="t1", infra_ref="i1")["via_p215_d"] is True
    assert acls.to_qai(tenant_id="t1", qai_ref="q1")["via_p215_f"] is True
    assert acls.to_optimization(tenant_id="t1", optimization_ref="o1")["via_p215_g"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["via_p215_k"] is True
    assert acls.to_aiops(tenant_id="t1", aiops_ref="a1")["via_p214_j"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", twin_ref="tw1")["module_local_quantum_twin_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_twin():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_twin"]["prompt_id"] == "P215-L"; assert svc.twin_readiness()["passed"] is True
