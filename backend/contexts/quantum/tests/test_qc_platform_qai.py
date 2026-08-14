"""P215-F quantum AI/QML foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_qai_foundation import validate_qc_qai_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_qai as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_qai_foundation():
    result = validate_qc_qai_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-F"
    assert result["adr"] == 452
@pytest.mark.unit
def test_qc_qai_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-F"
    assert cat["quantum_ai_platform_present_required"] is True
    assert cat["quantum_machine_learning_platform_present_required"] is True
    assert cat["quantum_neural_intelligence_present_required"] is True
    assert cat["quantum_ai_agent_foundation_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 8
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["builds_on_p215_e"] is True
    assert "GET /quantum/qai" in mod.qai_surface()["routes"]
@pytest.mark.unit
def test_qc_qai_acl():
    from contexts.quantum.infrastructure.acl import qc_qai_acl as acls
    assert acls.to_algorithms(tenant_id="t1", algorithm_ref="a1")["via_p215_e"] is True
    assert acls.to_model_lifecycle(tenant_id="t1", model_ref="m1")["via_p214_l"] is True
    assert acls.to_agent_platform(tenant_id="t1", agent_ref="ag1")["via_p214_f"] is True
    assert acls.to_data_governance(tenant_id="t1", asset_ref="d1")["via_p212"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", qai_ref="q1")["module_local_quantum_qai_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qai():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_qai"]["prompt_id"] == "P215-F"; assert svc.qai_readiness()["passed"] is True
