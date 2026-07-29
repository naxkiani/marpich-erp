"""P215-J quantum network/internet foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_network_foundation import validate_qc_network_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_network as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_network_foundation():
    result = validate_qc_network_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-J"
    assert result["adr"] == 456
@pytest.mark.unit
def test_qc_network_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-J"
    assert cat["quantum_internet_platform_present_required"] is True
    assert cat["quantum_network_fabric_present_required"] is True
    assert cat["quantum_communication_platform_present_required"] is True
    assert cat["quantum_node_federation_present_required"] is True
    assert cat["quantum_network_control_plane_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["builds_on_p215_i"] is True
    assert "GET /quantum/network" in mod.network_surface()["routes"]
@pytest.mark.unit
def test_qc_network_acl():
    from contexts.quantum.infrastructure.acl import qc_network_acl as acls
    assert acls.to_infrastructure(tenant_id="t1", infra_ref="i1")["via_p215_d"] is True
    assert acls.to_quantum_security(tenant_id="t1", security_ref="s1")["via_p215_h"] is True
    assert acls.to_quantum_data(tenant_id="t1", data_ref="d1")["via_p215_i"] is True
    assert acls.to_aiops(tenant_id="t1", aiops_ref="a1")["via_p214_j"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", network_ref="n1")["module_local_quantum_network_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_network():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_network"]["prompt_id"] == "P215-J"; assert svc.network_readiness()["passed"] is True
