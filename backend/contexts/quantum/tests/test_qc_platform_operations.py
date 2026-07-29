"""P215-N quantum operations / AIOps / self-healing foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_operations_foundation import validate_qc_operations_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_operations as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_operations_foundation():
    result = validate_qc_operations_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-N"
    assert result["adr"] == 459
@pytest.mark.unit
def test_qc_operations_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-N"
    assert cat["fabric"] == "meos_quantum_autonomous_operations_fabric"
    assert cat["quantum_operations_platform_present_required"] is True
    assert cat["quantum_aiops_platform_present_required"] is True
    assert cat["self_healing_infrastructure_present_required"] is True
    assert cat["observability_intelligence_present_required"] is True
    assert cat["incident_automation_present_required"] is True
    assert cat["autonomous_management_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["observability_platform"]["module_local_metrics_store_forbidden"] is True
    assert cat["via_p214_j"] is True
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/operations" in mod.operations_surface()["routes"]
@pytest.mark.unit
def test_qc_operations_acl():
    from contexts.quantum.infrastructure.acl import qc_operations_acl as acls
    assert acls.to_infrastructure(tenant_id="t1", infra_ref="i1")["via_p215_d"] is True
    assert acls.to_aiops(tenant_id="t1", aiops_ref="a1")["via_p214_j"] is True
    assert acls.to_qai(tenant_id="t1", qai_ref="q1")["via_p215_f"] is True
    assert acls.to_quantum_twin(tenant_id="t1", twin_ref="tw1")["via_p215_l"] is True
    assert acls.to_quantum_integration(tenant_id="t1", integration_ref="m1")["via_p215_m"] is True
    assert acls.to_observability_platform(tenant_id="t1", telemetry_ref="t1")["module_local_metrics_store_forbidden"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", operations_ref="o1")["module_local_quantum_operations_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_operations():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_operations"]["prompt_id"] == "P215-N"; assert svc.operations_readiness()["passed"] is True
