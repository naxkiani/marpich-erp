"""P216-Q robotics education / smart campus foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_education_foundation import validate_rb_education_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_education as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_education_foundation():
    result = validate_rb_education_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-Q"
    assert result["adr"] == 489
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_education_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-Q"
    assert cat["fabric"] == "meos_education_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["hospitality_gate"] == "P216-P"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["education_robotics_platform_present_required"] is True
    assert cat["ai_learning_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 14
    assert cat["never_replace_p216_p_hospitality"] is True
    assert cat["never_duplicate_sis_lms_core_logic"] is True
    assert cat["accessibility_by_design_required"] is True
    assert cat["foundation_for_p216_r"] is True
    assert "GET /robotics/education" in mod.education_surface()["routes"]
    assert "MEOS Education Intelligence Platform SHALL unify" in cat["education_vision"]
@pytest.mark.unit
def test_rb_education_acl():
    from contexts.robotics.infrastructure.acl import rb_education_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_hospitality(tenant_id="t1", hospitality_ref="h1")["never_replace_p216_p_hospitality"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_sis(tenant_id="t1", sis_ref="sis1")["never_duplicate_sis_lms_core_logic"] is True
    assert acls.to_lms(tenant_id="t1", lms_ref="lms1")["never_duplicate_sis_lms_core_logic"] is True
    assert acls.to_library(tenant_id="t1", library_ref="lib1")["never_duplicate_sis_lms_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["accessibility_by_design_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_education():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_education"]["prompt_id"] == "P216-Q"
    assert svc.education_readiness()["passed"] is True
