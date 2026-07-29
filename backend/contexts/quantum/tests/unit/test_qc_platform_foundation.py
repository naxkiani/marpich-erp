"""P215-A quantum foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_foundation_foundation import validate_qc_foundation_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_foundation as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_foundation_foundation():
    result = validate_qc_foundation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-A"
    assert result["adr"] == 447
    assert result["sor"] == "quantum"
    assert result["capability"] == "CAP-PLT-QC-001"
    assert result["forbidden_sibling_present"] is False
@pytest.mark.unit
def test_qc_foundation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-A"
    assert cat["enterprise_quantum_computing_foundation_present_required"] is True
    assert cat["quantum_ai"]["via_p214_v"] is True
    assert cat["governed_by_p215_k"] is True
    assert cat["microservices"]["service_count"] >= 10
    assert "GET /quantum/foundation" in mod.foundation_surface()["routes"]
@pytest.mark.unit
def test_qc_foundation_acl():
    from contexts.quantum.infrastructure.acl import qc_foundation_acl as acls
    assert acls.to_master_intelligence(tenant_id="t1", master_ref="m1")["via_p214_z"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["via_p215_k"] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")["pqc_remains_secrets"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", foundation_ref="f1")["module_local_quantum_foundation_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_foundation():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_foundation"]["prompt_id"] == "P215-A"; assert svc.foundation_readiness()["passed"] is True
