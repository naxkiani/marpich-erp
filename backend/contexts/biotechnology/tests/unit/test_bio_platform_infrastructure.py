"""P217-D biotechnology infrastructure foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_infrastructure_foundation import validate_bio_infrastructure_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_infrastructure as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_infrastructure_foundation():
    result = validate_bio_infrastructure_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-D"
    assert result["adr"] == 503
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_infrastructure_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-D"
    assert cat["fabric"] == "meos_bio_intelligence_infrastructure_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_infrastructure_architecture_present_required"] is True
    assert cat["scientific_computing_platform_present_required"] is True
    assert cat["bio_cloud_architecture_present_required"] is True
    assert cat["ai_compute_foundation_present_required"] is True
    assert cat["infrastructure_layers"]["layer_count"] == 5
    assert cat["scientific_computing"]["component_count"] == 3
    assert cat["bio_cloud"]["component_count"] == 4
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_p217_foundation"] is True
    assert cat["never_replace_p217_c_domain"] is True
    assert cat["module_local_observability_store_forbidden"] is True
    assert cat["never_direct_lab_hardware_bypass_of_integration_platform"] is True
    assert cat["foundation_for_p217_e"] is True
    assert "GET /biotechnology/infrastructure" in mod.infrastructure_surface()["routes"]
    assert "scientific-grade infrastructure foundation" in cat["infra_mission"]
@pytest.mark.unit
def test_bio_infrastructure_acl():
    from contexts.biotechnology.infrastructure.acl import bio_infrastructure_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_mission(tenant_id="t1", mission_ref="m1")["never_replace_p217_a_mission"] is True
    assert acls.to_biotechnology_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p217_b_strategy"] is True
    assert acls.to_biotechnology_domain(tenant_id="t1", domain_ref="d1")["never_replace_p217_c_domain"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_observability(tenant_id="t1", observability_ref="o1")["module_local_observability_store_forbidden"] is True
    assert acls.to_integration(tenant_id="t1", connector_ref="c1")["never_direct_lab_hardware_bypass_of_integration_platform"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_bio_safety_strategy_forbidden"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_infrastructure():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_infrastructure"]["prompt_id"] == "P217-D"
    assert svc.infrastructure_readiness()["passed"] is True
