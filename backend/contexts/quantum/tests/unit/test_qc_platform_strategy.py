"""P215-R quantum strategy / compliance / risk / executive foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_strategy_foundation import validate_qc_strategy_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_strategy as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_strategy_foundation():
    result = validate_qc_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-R"
    assert result["adr"] == 463
@pytest.mark.unit
def test_qc_strategy_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-R"
    assert cat["fabric"] == "meos_quantum_executive_intelligence_fabric"
    assert cat["trust_gate"] == "P215-K"
    assert cat["quantum_governance_platform_present_required"] is True
    assert cat["quantum_strategy_platform_present_required"] is True
    assert cat["quantum_compliance_intelligence_present_required"] is True
    assert cat["quantum_risk_intelligence_present_required"] is True
    assert cat["quantum_executive_intelligence_present_required"] is True
    assert cat["quantum_policy_management_present_required"] is True
    assert cat["quantum_trust_framework_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_p215_k"] is True
    assert cat["via_policy_engine"] is True
    assert cat["via_p213"] is True
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/strategy" in mod.strategy_surface()["routes"]
@pytest.mark.unit
def test_qc_strategy_acl():
    from contexts.quantum.infrastructure.acl import qc_strategy_acl as acls
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="g1")["never_replace_p215_k"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["module_local_pdp_forbidden"] is True
    assert acls.to_decision_intelligence(tenant_id="t1", decision_ref="d1")["module_local_metrics_store_forbidden"] is True
    assert acls.to_quantum_research(tenant_id="t1", research_ref="r1")["via_p215_q"] is True
    assert acls.to_quantum_quality(tenant_id="t1", quality_ref="q1")["via_p215_o"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["via_audit"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_strategy"]["prompt_id"] == "P215-R"; assert svc.strategy_readiness()["passed"] is True
