"""P215-S quantum resilience / cyber defense / zero trust foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_resilience_foundation import validate_qc_resilience_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_resilience as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_resilience_foundation():
    result = validate_qc_resilience_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-S"
    assert result["adr"] == 464
@pytest.mark.unit
def test_qc_resilience_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-S"
    assert cat["fabric"] == "meos_quantum_cyber_trust_fabric"
    assert cat["security_gate"] == "P215-H"
    assert cat["quantum_security_platform_present_required"] is True
    assert cat["post_quantum_cyber_defense_present_required"] is True
    assert cat["quantum_identity_fabric_present_required"] is True
    assert cat["quantum_zero_trust_present_required"] is True
    assert cat["threat_intelligence_present_required"] is True
    assert cat["security_operations_present_required"] is True
    assert cat["resilience_intelligence_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_h"] is True
    assert cat["never_local_pqc_store"] is True
    assert cat["pqc_remains_secrets"] is True
    assert cat["via_p209_secrets"] is True
    assert cat["via_policy_engine"] is True
    assert "GET /quantum/resilience" in mod.resilience_surface()["routes"]
@pytest.mark.unit
def test_qc_resilience_acl():
    from contexts.quantum.infrastructure.acl import qc_resilience_acl as acls
    assert acls.to_quantum_security(tenant_id="t1", security_ref="s1")["never_replace_p215_h"] is True
    assert acls.to_secrets_pqc(tenant_id="t1", secret_ref="k1")["never_local_pqc_store"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["module_local_pdp_forbidden"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["via_p200_b"] is True
    assert acls.to_aiops(tenant_id="t1", aiops_ref="a1")["via_p214_j"] is True
    assert acls.to_quantum_strategy(tenant_id="t1", strategy_ref="st1")["via_p215_r"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_resilience():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_resilience"]["prompt_id"] == "P215-S"; assert catalog["platform_resilience"]["pqc_remains_secrets"] is True; assert svc.resilience_readiness()["passed"] is True
