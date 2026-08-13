"""P217-S biotechnology bio security foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_security_foundation import validate_bio_security_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_security as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_security_foundation():
    result = validate_bio_security_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-S"
    assert result["adr"] == 518
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_security_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-S"
    assert cat["fabric"] == "meos_bio_security_intelligence_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["infrastructure_gate"] == "P217-D"
    assert cat["bio_ai_gate"] == "P217-E"
    assert cat["synthetic_gate"] == "P217-F"
    assert cat["simulation_gate"] == "P217-G"
    assert cat["digital_health_gate"] == "P217-H"
    assert cat["precision_medicine_gate"] == "P217-I"
    assert cat["clinical_research_gate"] == "P217-J"
    assert cat["drug_discovery_gate"] == "P217-K"
    assert cat["bio_manufacturing_gate"] == "P217-L"
    assert cat["bio_supply_chain_gate"] == "P217-M"
    assert cat["bio_regulatory_gate"] == "P217-N"
    assert cat["bio_sustainability_gate"] == "P217-O"
    assert cat["bio_marketplace_gate"] == "P217-P"
    assert cat["bio_innovation_gate"] == "P217-Q"
    assert cat["bio_investment_gate"] == "P217-R"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_security_platform_present_required"] is True
    assert cat["bio_cybersecurity_present_required"] is True
    assert cat["biological_risk_intelligence_present_required"] is True
    assert cat["threat_intelligence_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["bio_cybersecurity"]["domain_count"] == 4
    assert cat["biological_risk"]["engine_count"] == 3
    assert cat["threat_intelligence"]["source_count"] == 5
    assert cat["security_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_r_bio_investment"] is True
    assert cat["never_replace_identity_platform"] is True
    assert cat["never_replace_audit_platform"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["security_twins_via_p217g_acl_only"] is True
    assert cat["compliance_intelligence_via_p217n_acl_only"] is True
    assert cat["environmental_security_via_p217o_acl_only"] is True
    assert cat["commerce_security_via_p217p_acl_only"] is True
    assert cat["research_protection_via_p217q_acl_only"] is True
    assert cat["financial_security_via_p217r_acl_only"] is True
    assert cat["robotics_via_p216z_acl_only"] is True
    assert cat["quantum_optimization_via_p215z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_skip_human_security_oversight"] is True
    assert cat["never_autonomous_defense_without_approval"] is True
    assert cat["never_skip_zero_trust_controls"] is True
    assert cat["foundation_for_p217_t"] is True
    assert "GET /biotechnology/bio-security" in mod.bio_security_surface()["routes"]
    assert "continuously adaptive security intelligence" in cat["bio_security_vision"]
@pytest.mark.unit
def test_bio_security_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_security_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_bio_investment(tenant_id="t1", investment_ref="i1")["never_replace_p217_r_bio_investment"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="id1")["never_replace_identity_platform"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_replace_audit_platform"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["security_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="q1")["quantum_optimization_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["robotics_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_security_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_autonomous_defense_without_approval"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_zero_trust_controls"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_security():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_security"]["prompt_id"] == "P217-S"
    assert svc.bio_security_readiness()["passed"] is True
