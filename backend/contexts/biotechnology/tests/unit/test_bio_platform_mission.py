"""P217-A biotechnology mission / vision / strategy foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_mission_foundation import validate_bio_mission_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_mission as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_mission_foundation():
    result = validate_bio_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-A"
    assert result["adr"] == 500
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_mission_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-A"
    assert cat["fabric"] == "meos_bio_intelligence_strategic_framework"
    assert cat["foundation_gate"] == "P217"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["biotechnology_mission_framework_present_required"] is True
    assert cat["biotechnology_vision_framework_present_required"] is True
    assert cat["strategic_biotechnology_scope_present_required"] is True
    assert cat["bio_capability_framework_present_required"] is True
    assert cat["value_streams_framework_present_required"] is True
    assert cat["maturity_model_present_required"] is True
    assert cat["governance_framework_present_required"] is True
    assert cat["meos_integration_strategy_present_required"] is True
    assert cat["future_evolution_roadmap_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["objectives"]["objective_count"] >= 7
    assert cat["purposes"]["purpose_count"] >= 5
    assert cat["bio_domains"]["domain_count"] >= 6
    assert cat["never_replace_p217_foundation"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["opaque_bio_safety_strategy_forbidden"] is True
    assert cat["foundation_for_p217_b"] is True
    assert "GET /biotechnology/mission" in mod.mission_surface()["routes"]
    assert "enterprise biological intelligence ecosystem" in cat["mission_statement"]
@pytest.mark.unit
def test_bio_mission_acl():
    from contexts.biotechnology.infrastructure.acl import bio_mission_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["genomic_privacy_strategy_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_bio_safety_strategy_forbidden"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission"]["prompt_id"] == "P217-A"
    assert svc.mission_readiness()["passed"] is True
