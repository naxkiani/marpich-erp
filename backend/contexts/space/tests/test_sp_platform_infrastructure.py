"""P218-D space infrastructure foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_infrastructure_foundation import validate_sp_infrastructure_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_infrastructure as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_infrastructure_foundation():
    result = validate_sp_infrastructure_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-D"
    assert result["adr"] == 530
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_infrastructure_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-D"
    assert cat["fabric"] == "meos_space_intelligence_infrastructure_fabric"
    assert cat["foundation_gate"] == "P218"
    assert cat["mission_gate"] == "P218-A"
    assert cat["strategy_gate"] == "P218-B"
    assert cat["domain_gate"] == "P218-C"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["space_infrastructure_architecture_present_required"] is True
    assert cat["ground_segment_platform_present_required"] is True
    assert cat["mission_control_platform_present_required"] is True
    assert cat["space_cloud_platform_present_required"] is True
    assert cat["infrastructure_digital_twin_present_required"] is True
    assert cat["infrastructure_layers"]["layer_count"] == 5
    assert cat["ground_segment"]["component_count"] == 9
    assert cat["space_cloud"]["component_count"] == 6
    assert cat["data_infrastructure"]["domain_count"] == 4
    assert cat["storage_architecture"]["type_count"] == 4
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_foundation"] is True
    assert cat["never_replace_p218_c_domain"] is True
    assert cat["module_local_observability_store_forbidden"] is True
    assert cat["never_direct_ground_station_bypass_of_integration_platform"] is True
    assert cat["foundation_for_p218_e"] is True
    assert "GET /space/infrastructure" in mod.infrastructure_surface()["routes"]
    assert "secure, resilient, autonomous" in cat["infra_mission"]
@pytest.mark.unit
def test_sp_infrastructure_acl():
    from contexts.space.infrastructure.acl import sp_infrastructure_acl as acls
    assert acls.to_space_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p218_foundation"] is True
    assert acls.to_space_mission(tenant_id="t1", mission_ref="m1")["never_replace_p218_a_mission"] is True
    assert acls.to_space_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p218_b_strategy"] is True
    assert acls.to_space_domain(tenant_id="t1", domain_ref="d1")["never_replace_p218_c_domain"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_observability_platform(tenant_id="t1", observability_ref="o1")["module_local_observability_store_forbidden"] is True
    assert acls.to_integration_platform(tenant_id="t1", integration_ref="i1")["never_direct_ground_station_bypass_of_integration_platform"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_infrastructure():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_infrastructure"]["prompt_id"] == "P218-D"
    assert svc.infrastructure_readiness()["passed"] is True
