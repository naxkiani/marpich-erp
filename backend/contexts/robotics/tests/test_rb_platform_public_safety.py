"""P216-L robotics public safety / civil protection foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_public_safety_foundation import validate_rb_public_safety_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_public_safety as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_public_safety_foundation():
    result = validate_rb_public_safety_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-L"
    assert result["adr"] == 484
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_public_safety_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-L"
    assert cat["fabric"] == "meos_civil_protection_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["construction_gate"] == "P216-K"
    assert cat["healthcare_gate"] == "P216-I"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["public_safety_robotics_platform_present_required"] is True
    assert cat["emergency_response_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 14
    assert cat["never_replace_p216_k_construction"] is True
    assert cat["never_direct_gis_weather_bypass"] is True
    assert cat["never_bypass_notification_platform"] is True
    assert cat["foundation_for_p216_m"] is True
    assert "GET /robotics/public-safety" in mod.public_safety_surface()["routes"]
    assert "MEOS Civil Protection Intelligence Platform SHALL unify" in cat["public_safety_vision"]
@pytest.mark.unit
def test_rb_public_safety_acl():
    from contexts.robotics.infrastructure.acl import rb_public_safety_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_construction(tenant_id="t1", construction_ref="c1")["never_replace_p216_k_construction"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["never_direct_gis_weather_bypass"] is True
    assert acls.to_notification_platform(tenant_id="t1", notification_ref="n1")["never_bypass_notification_platform"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_duplicate_hospital_clinic_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_public_safety():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_public_safety"]["prompt_id"] == "P216-L"
    assert svc.public_safety_readiness()["passed"] is True
