"""P217-I biotechnology precision medicine foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_precision_medicine_foundation import validate_precision_medicine_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_precision_medicine as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_precision_medicine_foundation():
    result = validate_precision_medicine_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-I"
    assert result["adr"] == 508
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_precision_medicine_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-I"
    assert cat["fabric"] == "meos_precision_health_intelligence_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["infrastructure_gate"] == "P217-D"
    assert cat["bio_ai_gate"] == "P217-E"
    assert cat["synthetic_gate"] == "P217-F"
    assert cat["simulation_gate"] == "P217-G"
    assert cat["digital_health_gate"] == "P217-H"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["precision_medicine_platform_present_required"] is True
    assert cat["genomics_ai_present_required"] is True
    assert cat["omics_intelligence_present_required"] is True
    assert cat["molecular_medicine_present_required"] is True
    assert cat["personalized_therapy_present_required"] is True
    assert cat["architecture"]["layer_count"] == 5
    assert cat["genomics_ai"]["component_count"] == 4
    assert cat["omics"]["domain_count"] == 5
    assert cat["personalized_therapy"]["capability_count"] == 5
    assert cat["precision_agents"]["agent_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_h_digital_health"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["precision_twins_via_p217g_p217h_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_autonomous_clinical_action_without_physician"] is True
    assert cat["never_unconsented_genomic_processing"] is True
    assert cat["foundation_for_p217_j"] is True
    assert "GET /biotechnology/precision-medicine" in mod.precision_medicine_surface()["routes"]
    assert "individualized, predictive" in cat["precision_vision"]
@pytest.mark.unit
def test_precision_medicine_acl():
    from contexts.biotechnology.infrastructure.acl import bio_precision_medicine_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_digital_health(tenant_id="t1", digital_health_ref="d1")["never_replace_p217_h_digital_health"] is True
    assert acls.to_biotechnology_digital_health(tenant_id="t1", digital_health_ref="d1")["precision_twins_via_p217g_p217h_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_unconsented_genomic_processing"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_autonomous_clinical_action_without_physician"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_precision_medicine():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_precision_medicine"]["prompt_id"] == "P217-I"
    assert svc.precision_medicine_readiness()["passed"] is True
