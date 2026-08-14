"""P216-T robotics government / digital government foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_government_foundation import validate_rb_government_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_government as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_government_foundation():
    result = validate_rb_government_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-T"
    assert result["adr"] == 492
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_government_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-T"
    assert cat["fabric"] == "meos_government_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["finance_gate"] == "P216-R"
    assert cat["public_safety_gate"] == "P216-L"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["government_robotics_platform_present_required"] is True
    assert cat["autonomous_public_services_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 12
    assert cat["never_replace_p216_r_finance"] is True
    assert cat["never_duplicate_government_core_logic"] is True
    assert cat["never_duplicate_municipality_core_logic"] is True
    assert cat["human_governance_oversight_required"] is True
    assert cat["explainable_ai_required"] is True
    assert cat["p216_s_legal_planned"] is True
    assert cat["foundation_for_p216_u"] is True
    assert "GET /robotics/government" in mod.government_surface()["routes"]
    assert "MEOS Government Intelligence Platform SHALL unify" in cat["government_vision"]
@pytest.mark.unit
def test_rb_government_acl():
    from contexts.robotics.infrastructure.acl import rb_government_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_finance(tenant_id="t1", finance_ref="f1")["never_replace_p216_r_finance"] is True
    assert acls.to_robotics_public_safety(tenant_id="t1", public_safety_ref="ps1")["never_replace_p216_l_public_safety"] is True
    assert acls.to_government(tenant_id="t1", government_ref="g1")["never_duplicate_government_core_logic"] is True
    assert acls.to_municipality(tenant_id="t1", municipality_ref="m1")["never_duplicate_municipality_core_logic"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_replace_identity_platform"] is True
    assert acls.to_national_identity(tenant_id="t1", national_id_ref="n1")["never_replace_identity_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["explainable_ai_required"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["human_governance_oversight_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_government():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_government"]["prompt_id"] == "P216-T"
    assert svc.government_readiness()["passed"] is True
