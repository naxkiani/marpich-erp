"""P218 space intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_foundation_foundation import validate_sp_foundation_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_foundation as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_foundation_foundation():
    result = validate_sp_foundation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218"
    assert result["adr"] == 526
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_foundation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218"
    assert cat["fabric"] == "meos_space_intelligence_fabric"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["space_intelligence_platform_present_required"] is True
    assert cat["space_ai_operating_system_present_required"] is True
    assert cat["orbital_civilization_architecture_present_required"] is True
    assert cat["autonomous_space_operations_platform_present_required"] is True
    assert cat["architecture"]["layer_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["agents"]["agent_count"] == 6
    assert cat["never_replace_biotechnology"] is True
    assert cat["never_replace_robotics_supreme"] is True
    assert cat["never_ungated_autonomous_mission_release"] is True
    assert cat["never_opaque_mission_critical_decisions"] is True
    assert cat["never_skip_human_mission_oversight"] is True
    assert cat["foundation_for_p218_a"] is True
    assert "GET /space/foundation" in mod.foundation_surface()["routes"]
    assert "MEOS Space Intelligence Platform SHALL unify" in cat["space_vision"]
@pytest.mark.unit
def test_sp_foundation_acl():
    from contexts.space.infrastructure.acl import sp_foundation_acl as acls
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_robotics_supreme"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_integration(tenant_id="t1", connector_ref="c1")["telemetry_via_integration_platform_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_autonomous_mission_release"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_mission_oversight"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_space_cybersecurity_controls"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_foundation():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_foundation"]["prompt_id"] == "P218"
    assert svc.foundation_readiness()["passed"] is True
