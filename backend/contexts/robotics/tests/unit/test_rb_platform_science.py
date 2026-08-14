"""P216-V robotics science / autonomous laboratory foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_science_foundation import validate_rb_science_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_science as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_science_foundation():
    result = validate_rb_science_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-V"
    assert result["adr"] == 494
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_science_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-V"
    assert cat["fabric"] == "meos_scientific_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["defense_gate"] == "P216-U"
    assert cat["healthcare_gate"] == "P216-I"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["science_robotics_platform_present_required"] is True
    assert cat["autonomous_laboratory_platform_present_required"] is True
    assert cat["ai_scientist_platform_present_required"] is True
    assert cat["human_scientific_oversight_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 12
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_p216_u_defense"] is True
    assert cat["reproducibility_by_design_required"] is True
    assert cat["human_scientific_oversight_required"] is True
    assert cat["explainable_ai_required"] is True
    assert cat["foundation_for_p216_w"] is True
    assert "GET /robotics/science" in mod.science_surface()["routes"]
    assert "MEOS Scientific Intelligence Platform SHALL unify" in cat["science_vision"]
@pytest.mark.unit
def test_rb_science_acl():
    from contexts.robotics.infrastructure.acl import rb_science_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_defense(tenant_id="t1", defense_ref="d1")["never_replace_p216_u_defense"] is True
    assert acls.to_robotics_healthcare(tenant_id="t1", healthcare_ref="h1")["never_replace_p216_i_healthcare"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_lims(tenant_id="t1", lims_ref="l1")["via_lims_api"] is True
    assert acls.to_scientific_database(tenant_id="t1", database_ref="db1")["via_scientific_db_api"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["reproducibility_by_design_required"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["research_ethics_governance_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["human_scientific_oversight_required"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_science():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_science"]["prompt_id"] == "P216-V"
    assert svc.science_readiness()["passed"] is True
