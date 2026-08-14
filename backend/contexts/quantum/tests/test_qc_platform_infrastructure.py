"""P215-D quantum infrastructure foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_infrastructure_foundation import validate_qc_infrastructure_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_infrastructure as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_infrastructure_foundation():
    result = validate_qc_infrastructure_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-D"
    assert result["adr"] == 450
@pytest.mark.unit
def test_qc_infrastructure_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-D"
    assert cat["quantum_infrastructure_platform_present_required"] is True
    assert cat["quantum_cloud_architecture_present_required"] is True
    assert cat["hardware_abstraction_layer_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["builds_on_p215_a"] is True
    assert cat["builds_on_p215_c"] is True
    assert "GET /quantum/infrastructure" in mod.infrastructure_surface()["routes"]
@pytest.mark.unit
def test_qc_infrastructure_acl():
    from contexts.quantum.infrastructure.acl import qc_infrastructure_acl as acls
    assert acls.to_domain(tenant_id="t1", domain_ref="d1")["via_p215_c"] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", trust_ref="p209")["via_p209"] is True
    assert acls.to_cyber_security(tenant_id="t1", cyber_ref="p210")["via_p210"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", infra_ref="i1")["module_local_quantum_infrastructure_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_infrastructure():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_infrastructure"]["prompt_id"] == "P215-D"; assert svc.infrastructure_readiness()["passed"] is True
