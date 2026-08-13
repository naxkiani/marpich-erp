"""P217-Y biotechnology bio trust foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_trust_foundation import validate_bio_trust_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_trust as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_trust_foundation():
    result = validate_bio_trust_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-Y"
    assert result["adr"] == 523
@pytest.mark.unit
def test_bio_trust_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-Y"
    assert cat["fabric"] == "meos_final_bio_trust_intelligence_fabric"
    assert cat["bio_evolution_gate"] == "P217-X"
    assert cat["architecture"]["layer_count"] == 6
    assert cat["bio_intelligence_alignment"]["capability_count"] == 4
    assert cat["bio_ethics_civilization"]["pillar_count"] == 4
    assert cat["future_biological_trust"]["component_count"] == 4
    assert cat["trust_agents"]["agent_count"] == 6
    assert cat["never_replace_p217_x_bio_evolution"] is True
    assert cat["never_replace_compliance_platform"] is True
    assert cat["never_skip_human_trust_oversight"] is True
    assert cat["never_unvalidated_trust_policy_release"] is True
    assert cat["never_skip_bio_intelligence_alignment_controls"] is True
    assert cat["never_skip_bio_ethics_civilization_controls"] is True
    assert cat["never_skip_trust_transparency_requirements"] is True
    assert cat["foundation_for_p217_z"] is True
    assert "GET /biotechnology/bio-trust" in mod.bio_trust_surface()["routes"]
    assert "sovereign trust controls" in cat["bio_trust_vision"]
@pytest.mark.unit
def test_bio_trust_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_trust_acl as acls
    assert acls.to_biotechnology_bio_evolution(tenant_id="t1", evolution_ref="e1")["never_replace_p217_x_bio_evolution"] is True
    assert acls.to_biotechnology_bio_gi(tenant_id="t1", bio_gi_ref="g1")["bio_gi_cognition_via_p217v_acl_only"] is True
    assert acls.to_biotechnology_bio_civilization(tenant_id="t1", civilization_ref="c1")["via_p217_w"] is True
    assert acls.to_biotechnology_bio_security(tenant_id="t1", security_ref="s1")["security_via_p217s_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_trust_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_unvalidated_trust_policy_release"] is True
    assert acls.to_compliance(tenant_id="t1", compliance_ref="cp1")["never_replace_compliance_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_trust():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_trust"]["prompt_id"] == "P217-Y"
    assert svc.bio_trust_readiness()["passed"] is True
