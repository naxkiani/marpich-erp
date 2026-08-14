"""P215-E quantum algorithms foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_algorithms_foundation import validate_qc_algorithms_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_algorithms as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_algorithms_foundation():
    result = validate_qc_algorithms_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-E"
    assert result["adr"] == 451
@pytest.mark.unit
def test_qc_algorithms_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-E"
    assert cat["quantum_algorithm_platform_present_required"] is True
    assert cat["quantum_software_platform_present_required"] is True
    assert cat["circuit_intelligence_engine_present_required"] is True
    assert cat["quantum_marketplace_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["builds_on_p215_d"] is True
    assert "GET /quantum/algorithms" in mod.algorithms_surface()["routes"]
@pytest.mark.unit
def test_qc_algorithms_acl():
    from contexts.quantum.infrastructure.acl import qc_algorithms_acl as acls
    assert acls.to_infrastructure(tenant_id="t1", infra_ref="i1")["via_p215_d"] is True
    assert acls.to_agent_platform(tenant_id="t1", agent_ref="a1")["via_p214_f"] is True
    assert acls.to_agi(tenant_id="t1", agi_ref="g1")["via_p214_v"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", algorithm_ref="alg1")["module_local_quantum_algorithms_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_algorithms():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_algorithms"]["prompt_id"] == "P215-E"; assert svc.algorithms_readiness()["passed"] is True
