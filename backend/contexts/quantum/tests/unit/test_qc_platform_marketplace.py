"""P215-P quantum marketplace / economy / innovation foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_marketplace_foundation import validate_qc_marketplace_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_marketplace as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_marketplace_foundation():
    result = validate_qc_marketplace_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-P"
    assert result["adr"] == 461
@pytest.mark.unit
def test_qc_marketplace_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-P"
    assert cat["fabric"] == "meos_quantum_economy_intelligence_fabric"
    assert cat["quantum_marketplace_platform_present_required"] is True
    assert cat["capability_exchange_platform_present_required"] is True
    assert cat["quantum_service_economy_present_required"] is True
    assert cat["algorithm_marketplace_present_required"] is True
    assert cat["application_marketplace_present_required"] is True
    assert cat["innovation_ecosystem_present_required"] is True
    assert cat["economic_intelligence_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["aggregates"]["aggregate_count"] >= 8
    assert cat["via_plugin_platform"] is True
    assert cat["via_financial_kernel"] is True
    assert cat["governed_by_p215_k"] is True
    assert "GET /quantum/marketplace" in mod.marketplace_surface()["routes"]
@pytest.mark.unit
def test_qc_marketplace_acl():
    from contexts.quantum.infrastructure.acl import qc_marketplace_acl as acls
    assert acls.to_quantum_integration(tenant_id="t1", integration_ref="m1")["via_p215_m"] is True
    assert acls.to_quantum_quality(tenant_id="t1", quality_ref="q1")["via_p215_o"] is True
    assert acls.to_plugin_platform(tenant_id="t1", plugin_ref="p1")["module_local_plugin_marketplace_forbidden"] is True
    assert acls.to_financial_kernel(tenant_id="t1", invoice_ref="i1")["module_local_payment_processor_forbidden"] is True
    assert acls.to_decision_intelligence(tenant_id="t1", decision_ref="d1")["via_p213"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", marketplace_ref="mp1")["ungated_capability_publish_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_marketplace():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_marketplace"]["prompt_id"] == "P215-P"; assert svc.marketplace_readiness()["passed"] is True
