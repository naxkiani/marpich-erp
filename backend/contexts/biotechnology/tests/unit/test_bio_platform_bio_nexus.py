"""P217-Z biotechnology bio nexus foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_nexus_foundation import validate_bio_nexus_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_nexus as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_nexus_foundation():
    result = validate_bio_nexus_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-Z"
    assert result["adr"] == 525
@pytest.mark.unit
def test_bio_nexus_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-Z"
    assert cat["fabric"] == "meos_final_bio_intelligence_architecture"
    assert cat["bio_trust_gate"] == "P217-Y"
    assert cat["architecture"]["layer_count"] == 6
    assert cat["bio_supreme_control_plane"]["domain_count"] == 4
    assert cat["autonomous_biological_nexus"]["capability_count"] == 4
    assert cat["bio_civilization_intelligence_core"]["capability_count"] == 4
    assert cat["supreme_agents"]["agent_count"] == 6
    assert cat["never_replace_p217_y_bio_trust"] is True
    assert cat["never_skip_human_supreme_oversight"] is True
    assert cat["never_skip_bio_supreme_control_plane_controls"] is True
    assert cat["never_skip_autonomous_nexus_safety_controls"] is True
    assert cat["never_skip_civilization_core_governance"] is True
    assert cat["never_unvalidated_nexus_capability_release"] is True
    assert cat["series_closure_for_p217"] is True
    assert cat["foundation_for_p218"] is True
    assert "GET /biotechnology/bio-nexus" in mod.bio_nexus_surface()["routes"]
    assert "biological intelligence operating framework" in cat["bio_nexus_vision"]
@pytest.mark.unit
def test_bio_nexus_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_nexus_acl as acls
    assert acls.to_biotechnology_bio_trust(tenant_id="t1", trust_ref="y1")["trust_via_p217y_acl_only"] is True
    assert acls.to_biotechnology_bio_evolution(tenant_id="t1", evolution_ref="x1")["evolution_via_p217x_acl_only"] is True
    assert acls.to_biotechnology_bio_civilization(tenant_id="t1", civilization_ref="w1")["via_p217_w"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_supreme_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_unvalidated_nexus_capability_release"] is True
    assert acls.to_compliance(tenant_id="t1", compliance_ref="cp1")["never_replace_compliance_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_nexus():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_nexus"]["prompt_id"] == "P217-Z"
    assert svc.bio_nexus_readiness()["passed"] is True
