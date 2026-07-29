"""P215-H quantum security/trust foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_security_foundation import validate_qc_security_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_security as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_security_foundation():
    result = validate_qc_security_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-H"
    assert result["adr"] == 454
    assert result["pqc_remains_secrets"] is True
@pytest.mark.unit
def test_qc_security_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-H"
    assert cat["quantum_security_platform_present_required"] is True
    assert cat["post_quantum_cryptography_platform_present_required"] is True
    assert cat["quantum_trust_architecture_present_required"] is True
    assert cat["pqc_remains_secrets"] is True
    assert cat["pqc_platform"]["pqc_sor"] == "secrets"
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert "GET /quantum/security" in mod.security_surface()["routes"]
@pytest.mark.unit
def test_qc_security_acl():
    from contexts.quantum.infrastructure.acl import qc_security_acl as acls
    assert acls.to_cryptographic_trust(tenant_id="t1", trust_ref="p209")["via_p209"] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", trust_ref="p209")["pqc_remains_secrets"] is True
    assert acls.to_cyber_security(tenant_id="t1", cyber_ref="p210")["via_p210"] is True
    assert acls.to_identity_intelligence(tenant_id="t1", identity_ref="p207")["via_p207"] is True
    assert acls.to_authorization_intelligence(tenant_id="t1", authz_ref="p208")["via_p208"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", security_ref="s1")["module_local_quantum_security_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_security():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_security"]["prompt_id"] == "P215-H"; assert catalog["platform_security"]["pqc_remains_secrets"] is True; assert svc.security_readiness()["passed"] is True
