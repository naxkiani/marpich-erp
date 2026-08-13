"""P216-U robotics defense / strategic intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_defense_foundation import validate_rb_defense_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_defense as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_defense_foundation():
    result = validate_rb_defense_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-U"
    assert result["adr"] == 493
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_defense_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-U"
    assert cat["fabric"] == "meos_defense_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["government_gate"] == "P216-T"
    assert cat["public_safety_gate"] == "P216-L"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["military_robotics_platform_present_required"] is True
    assert cat["strategic_intelligence_platform_present_required"] is True
    assert cat["autonomous_system_governance_present_required"] is True
    assert cat["human_oversight_architecture_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 11
    assert cat["events"]["core_event_count"] == 6
    assert cat["never_replace_p216_t_government"] is True
    assert cat["never_duplicate_public_safety_core_logic"] is True
    assert cat["human_authorization_control_required"] is True
    assert cat["explainable_ai_required"] is True
    assert cat["ungated_physical_autonomy_strategy_forbidden"] is True
    assert cat["foundation_for_p216_v"] is True
    assert "GET /robotics/defense" in mod.defense_surface()["routes"]
    assert "MEOS Defense Intelligence Platform SHALL unify" in cat["defense_vision"]
@pytest.mark.unit
def test_rb_defense_acl():
    from contexts.robotics.infrastructure.acl import rb_defense_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_government(tenant_id="t1", government_ref="g1")["never_replace_p216_t_government"] is True
    assert acls.to_robotics_public_safety(tenant_id="t1", public_safety_ref="ps1")["never_duplicate_public_safety_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["responsible_ai_governance_required"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["human_authorization_control_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["human_authorization_control_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_cybersecurity(tenant_id="t1", cyber_ref="c1")["via_cyber_api"] is True
    assert acls.to_emergency_management(tenant_id="t1", emergency_ref="e1")["never_duplicate_public_safety_core_logic"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_defense():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_defense"]["prompt_id"] == "P216-U"
    assert svc.defense_readiness()["passed"] is True
