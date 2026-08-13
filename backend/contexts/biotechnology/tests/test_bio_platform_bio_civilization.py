"""P217-W biotechnology bio civilization foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_civilization_foundation import validate_bio_civilization_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_civilization as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_civilization_foundation():
    result = validate_bio_civilization_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-W"
    assert result["adr"] == 524
@pytest.mark.unit
def test_bio_civilization_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-W"
    assert cat["fabric"] == "meos_bio_civilization_intelligence_fabric"
    assert cat["bio_gi_gate"] == "P217-V"
    assert cat["architecture"]["layer_count"] == 6
    assert cat["collective_biological_network"]["capability_count"] == 4
    assert cat["global_bio_cognitive_ecosystem"]["pillar_count"] == 4
    assert cat["human_bio_ai_symbiosis"]["component_count"] == 4
    assert cat["civilization_agents"]["agent_count"] == 6
    assert cat["never_replace_p217_v_bio_gi"] is True
    assert cat["never_ungoverned_cross_tenant_intelligence_federation"] is True
    assert cat["never_opaque_collective_decisions"] is True
    assert cat["never_skip_human_civilization_oversight"] is True
    assert cat["never_skip_collective_bio_ethics_controls"] is True
    assert cat["never_skip_human_bio_ai_symbiosis_controls"] is True
    assert cat["never_unvalidated_civilization_scenario_release"] is True
    assert cat["foundation_for_p217_x"] is True
    assert cat["foundation_for_p217_y"] is True
    assert "GET /biotechnology/bio-civilization" in mod.bio_civilization_surface()["routes"]
    assert "collective civilization network" in cat["bio_civilization_vision"]
@pytest.mark.unit
def test_bio_civilization_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_civilization_acl as acls
    assert acls.to_biotechnology_bio_gi(tenant_id="t1", bio_gi_ref="g1")["bio_gi_cognition_via_p217v_acl_only"] is True
    assert acls.to_biotechnology_bio_security(tenant_id="t1", security_ref="s1")["security_via_p217s_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_civilization_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_opaque_collective_decisions"] is True
    assert acls.to_compliance(tenant_id="t1", compliance_ref="cp1")["never_replace_compliance_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_enterprise_biotechnology(tenant_id="t1", bio_civilization_ref="bc1")["civilization_intelligence_via_p217w_acl_only"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_civilization():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_civilization"]["prompt_id"] == "P217-W"
    assert svc.bio_civilization_readiness()["passed"] is True
