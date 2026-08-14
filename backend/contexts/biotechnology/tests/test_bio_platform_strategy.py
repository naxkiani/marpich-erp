"""P217-B biotechnology strategic architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_strategy_foundation import validate_bio_strategy_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_strategy as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_strategy_foundation():
    result = validate_bio_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-B"
    assert result["adr"] == 501
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_strategy_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-B"
    assert cat["fabric"] == "meos_biotechnology_strategic_architecture_framework"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["biotechnology_strategic_architecture_present_required"] is True
    assert cat["capability_model_present_required"] is True
    assert cat["operating_framework_present_required"] is True
    assert cat["platform_model_present_required"] is True
    assert cat["service_model_present_required"] is True
    assert cat["maturity_model_present_required"] is True
    assert cat["transformation_roadmap_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["architecture_layers"]["layer_count"] == 5
    assert cat["capability_model"]["group_count"] == 6
    assert cat["service_model"]["service_count"] == 16
    assert cat["maturity_model"]["level_count"] == 5
    assert cat["never_replace_p217_foundation"] is True
    assert cat["never_replace_p217_a_mission"] is True
    assert cat["opaque_bio_safety_strategy_forbidden"] is True
    assert cat["foundation_for_p217_c"] is True
    assert "GET /biotechnology/strategy" in mod.strategy_surface()["routes"]
    assert "MEOS Biotechnology Architecture SHALL" in cat["architecture_vision"]
@pytest.mark.unit
def test_bio_strategy_acl():
    from contexts.biotechnology.infrastructure.acl import bio_strategy_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_mission(tenant_id="t1", mission_ref="m1")["never_replace_p217_a_mission"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["genomic_privacy_strategy_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_bio_safety_strategy_forbidden"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P217-B"
    assert svc.strategy_readiness()["passed"] is True
