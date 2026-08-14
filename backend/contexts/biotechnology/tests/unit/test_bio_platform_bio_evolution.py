"""P217-X biotechnology ultimate bio evolution foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_evolution_foundation import validate_bio_evolution_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_evolution as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_evolution_foundation():
    result = validate_bio_evolution_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-X"
    assert result["adr"] == 522
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_evolution_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-X"
    assert cat["fabric"] == "meos_ultimate_bio_evolution_fabric"
    assert cat["bio_gi_gate"] == "P217-V"
    assert cat["bio_civilization_gate"] == "P217-W"
    assert cat["architecture"]["layer_count"] == 6
    assert cat["post_biological_intelligence"]["capability_count"] == 3
    assert cat["human_bio_ai_convergence"]["capability_count"] == 3
    assert cat["bio_singularity_framework"]["component_count"] == 3
    assert cat["evolution_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_v_bio_gi"] is True
    assert cat["never_replace_p217_w_bio_civilization"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["evolution_twins_via_p217g_acl_only"] is True
    assert cat["bio_gi_cognition_via_p217v_acl_only"] is True
    assert cat["civilization_intelligence_via_p217w_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_skip_human_singularity_oversight"] is True
    assert cat["never_unvalidated_singularity_scenario_release"] is True
    assert cat["never_skip_responsible_evolution_governance"] is True
    assert cat["never_skip_convergence_safety_controls"] is True
    assert cat["never_skip_human_benefit_first_principle"] is True
    assert cat["foundation_for_p217_y"] is True
    assert "GET /biotechnology/bio-evolution" in mod.bio_evolution_surface()["routes"]
    assert "responsibly advancing future biological evolution" in cat["bio_evolution_vision"]
@pytest.mark.unit
def test_bio_evolution_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_evolution_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_bio_gi(tenant_id="t1", bio_gi_ref="g1")["never_replace_p217_v_bio_gi"] is True
    assert acls.to_biotechnology_bio_civilization(tenant_id="t1", civilization_ref="c1")["civilization_intelligence_via_p217w_acl_only"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="sim1")["evolution_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_singularity_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_unvalidated_singularity_scenario_release"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_convergence_safety_controls"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_benefit_first_principle"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_evolution():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_evolution"]["prompt_id"] == "P217-X"
    assert svc.bio_evolution_readiness()["passed"] is True
