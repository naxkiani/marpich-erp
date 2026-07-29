"""P215-I quantum data intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_data_foundation import validate_qc_data_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_data as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_data_foundation():
    result = validate_qc_data_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-I"
    assert result["adr"] == 455
@pytest.mark.unit
def test_qc_data_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-I"
    assert cat["quantum_data_intelligence_platform_present_required"] is True
    assert cat["quantum_knowledge_graph_platform_present_required"] is True
    assert cat["quantum_data_governance_platform_present_required"] is True
    assert cat["via_p212"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["builds_on_p215_h"] is True
    assert "GET /quantum/data" in mod.data_surface()["routes"]
@pytest.mark.unit
def test_qc_data_acl():
    from contexts.quantum.infrastructure.acl import qc_data_acl as acls
    assert acls.to_data_governance(tenant_id="t1", asset_ref="a1")["via_p212"] is True
    assert acls.to_quantum_security(tenant_id="t1", security_ref="s1")["via_p215_h"] is True
    assert acls.to_knowledge_rag(tenant_id="t1", knowledge_ref="k1")["via_p214_g"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", data_ref="d1")["module_local_quantum_data_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_data():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_data"]["prompt_id"] == "P215-I"; assert svc.data_readiness()["passed"] is True
