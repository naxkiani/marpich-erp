"""P215-O quantum testing / validation / certification foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_quality_foundation import validate_qc_quality_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_quality as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_quality_foundation():
    result = validate_qc_quality_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-O"
    assert result["adr"] == 460
@pytest.mark.unit
def test_qc_quality_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-O"
    assert cat["fabric"] == "meos_quantum_quality_intelligence_fabric"
    assert cat["quantum_testing_platform_present_required"] is True
    assert cat["quantum_validation_platform_present_required"] is True
    assert cat["quantum_benchmarking_platform_present_required"] is True
    assert cat["quantum_qa_platform_present_required"] is True
    assert cat["quantum_certification_platform_present_required"] is True
    assert cat["quality_intelligence_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["certification_platform"]["module_local_certification_authority_forbidden"] is True
    assert cat["via_p214_o"] is True
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/testing" in mod.testing_surface()["routes"]
@pytest.mark.unit
def test_qc_quality_acl():
    from contexts.quantum.infrastructure.acl import qc_quality_acl as acls
    assert acls.to_software(tenant_id="t1", software_ref="s1")["via_p215_e"] is True
    assert acls.to_ai_testing(tenant_id="t1", aiqa_ref="a1")["via_p214_o"] is True
    assert acls.to_quantum_operations(tenant_id="t1", operations_ref="o1")["via_p215_n"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["via_p215_k"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["via_workflow"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", quality_ref="q1")["module_local_certification_authority_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_quality():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_quality"]["prompt_id"] == "P215-O"; assert svc.testing_readiness()["passed"] is True
