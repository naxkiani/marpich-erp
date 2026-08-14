"""P216-R robotics financial / autonomous banking foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_finance_foundation import validate_rb_finance_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_finance as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_finance_foundation():
    result = validate_rb_finance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-R"
    assert result["adr"] == 490
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_finance_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-R"
    assert cat["fabric"] == "meos_financial_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["education_gate"] == "P216-Q"
    assert cat["logistics_gate"] == "P216-G"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["financial_robotics_platform_present_required"] is True
    assert cat["autonomous_banking_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 13
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p216_q_education"] is True
    assert cat["never_replace_financial_kernel"] is True
    assert cat["never_direct_payment_bypass"] is True
    assert cat["never_duplicate_core_banking_logic"] is True
    assert cat["explainable_financial_ai_required"] is True
    assert cat["foundation_for_p216_s"] is True
    assert "GET /robotics/finance" in mod.finance_surface()["routes"]
    assert "MEOS Financial Intelligence Platform SHALL unify" in cat["finance_vision"]
@pytest.mark.unit
def test_rb_finance_acl():
    from contexts.robotics.infrastructure.acl import rb_finance_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_education(tenant_id="t1", education_ref="e1")["never_replace_p216_q_education"] is True
    assert acls.to_financial_kernel(tenant_id="t1", kernel_ref="k1")["never_replace_financial_kernel"] is True
    assert acls.to_core_banking(tenant_id="t1", banking_ref="b1")["never_duplicate_core_banking_logic"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["never_direct_payment_bypass"] is True
    assert acls.to_payment_network(tenant_id="t1", payment_ref="p1")["never_direct_payment_bypass"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["explainable_financial_ai_required"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["regulatory_compliance_by_design_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_finance():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_finance"]["prompt_id"] == "P216-R"
    assert svc.finance_readiness()["passed"] is True
