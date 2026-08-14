"""P215-G quantum optimization/scientific intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_optimization_foundation import validate_qc_optimization_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_optimization as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_optimization_foundation():
    result = validate_qc_optimization_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-G"
    assert result["adr"] == 453
@pytest.mark.unit
def test_qc_optimization_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-G"
    assert cat["quantum_optimization_platform_present_required"] is True
    assert cat["simulation_intelligence_platform_present_required"] is True
    assert cat["discovery_intelligence_platform_present_required"] is True
    assert cat["decision_optimization_engine_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["aggregates"]["aggregate_count"] >= 6
    assert cat["builds_on_p215_f"] is True
    assert "GET /quantum/optimization" in mod.optimization_surface()["routes"]
@pytest.mark.unit
def test_qc_optimization_acl():
    from contexts.quantum.infrastructure.acl import qc_optimization_acl as acls
    assert acls.to_qai(tenant_id="t1", qai_ref="q1")["via_p215_f"] is True
    assert acls.to_knowledge_rag(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_decision_intelligence(tenant_id="t1", decision_ref="d1")["via_p213"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", optimization_ref="o1")["module_local_quantum_optimization_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_optimization():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_optimization"]["prompt_id"] == "P215-G"; assert svc.optimization_readiness()["passed"] is True
