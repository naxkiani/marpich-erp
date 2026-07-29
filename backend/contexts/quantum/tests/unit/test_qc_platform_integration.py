"""P215-M quantum integration / gateway / mesh foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_integration_foundation import validate_qc_integration_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_integration as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_integration_foundation():
    result = validate_qc_integration_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-M"
    assert result["adr"] == 458
@pytest.mark.unit
def test_qc_integration_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-M"
    assert cat["fabric"] == "meos_quantum_integration_intelligence_fabric"
    assert cat["quantum_integration_platform_present_required"] is True
    assert cat["quantum_api_gateway_present_required"] is True
    assert cat["quantum_service_mesh_present_required"] is True
    assert cat["hybrid_intelligence_bridge_present_required"] is True
    assert cat["event_integration_backbone_present_required"] is True
    assert cat["capability_federation_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["api_gateway"]["module_local_gateway_forbidden"] is True
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/integration" in mod.integration_surface()["routes"]
@pytest.mark.unit
def test_qc_integration_acl():
    from contexts.quantum.infrastructure.acl import qc_integration_acl as acls
    assert acls.to_algorithms(tenant_id="t1", algorithm_ref="a1")["via_p215_e"] is True
    assert acls.to_qai(tenant_id="t1", qai_ref="q1")["via_p215_f"] is True
    assert acls.to_quantum_security(tenant_id="t1", security_ref="s1")["via_p215_h"] is True
    assert acls.to_quantum_twin(tenant_id="t1", twin_ref="tw1")["via_p215_l"] is True
    assert acls.to_platform_api_gateway(tenant_id="t1", route_ref="r1")["via_platform_api_gateway"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["via_integration_platform"] is True
    assert acls.to_event_fabric(tenant_id="t1", event_ref="e1")["via_event_fabric"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", integration_ref="i1")["module_local_quantum_integration_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_integration():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_integration"]["prompt_id"] == "P215-M"; assert svc.integration_readiness()["passed"] is True
