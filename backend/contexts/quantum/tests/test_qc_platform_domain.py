"""P215-C quantum domain architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_domain_foundation import validate_qc_domain_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_domain as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_domain_foundation():
    result = validate_qc_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-C"
    assert result["adr"] == 449
@pytest.mark.unit
def test_qc_domain_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-C"
    assert cat["quantum_domain_model_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 8
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["builds_on_p215_a"] is True
    assert cat["builds_on_p215_b"] is True
    assert "GET /quantum/domain" in mod.domain_surface()["routes"]
@pytest.mark.unit
def test_qc_domain_acl():
    from contexts.quantum.infrastructure.acl import qc_domain_acl as acls
    assert acls.to_mission(tenant_id="t1", mission_ref="m1")["via_p215_b"] is True
    assert acls.to_agi(tenant_id="t1", agi_ref="a1")["via_p214_v"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", domain_ref="d1")["module_local_quantum_domain_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_domain"]["prompt_id"] == "P215-C"; assert svc.domain_readiness()["passed"] is True
