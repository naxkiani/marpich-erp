"""P217-U biotechnology bio autonomous foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_autonomous_foundation import validate_bio_autonomous_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_autonomous as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_autonomous_foundation():
    result = validate_bio_autonomous_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-U"
    assert result["adr"] == 520
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_autonomous_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-U"
    assert cat["fabric"] == "meos_bio_autonomous_intelligence_fabric"
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
    assert cat["bio_security_gate"] == "P217-S"
    assert cat["bio_future_gate"] == "P217-T"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_autonomous_platform_present_required"] is True
    assert cat["autonomous_biology_present_required"] is True
    assert cat["bio_ai_autonomy_present_required"] is True
    assert cat["self_optimizing_ecosystem_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["bio_ai_autonomy_engine"]["capability_count"] == 4
    assert cat["autonomous_biology_os"]["capability_count"] == 4
    assert cat["self_optimizing_ecosystem"]["closed_loop_step_count"] == 6
    assert cat["autonomous_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_t_bio_future"] is True
    assert cat["never_replace_p217_s_bio_security"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["autonomous_twins_via_p217g_acl_only"] is True
    assert cat["future_evolution_via_p217t_acl_only"] is True
    assert cat["autonomous_safety_via_p217s_acl_only"] is True
    assert cat["robotics_via_p216z_acl_only"] is True
    assert cat["quantum_optimization_via_p215z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_skip_human_autonomy_oversight"] is True
    assert cat["never_unsupervised_autonomous_bio_action"] is True
    assert cat["never_skip_responsible_bio_autonomy_controls"] is True
    assert cat["never_opaque_autonomous_decisions"] is True
    assert cat["foundation_for_p217_v"] is True
    assert "GET /biotechnology/bio-autonomous" in mod.bio_autonomous_surface()["routes"]
    assert "self-improving" in cat["bio_autonomous_vision"]
@pytest.mark.unit
def test_bio_autonomous_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_autonomous_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_bio_future(tenant_id="t1", future_ref="fu1")["never_replace_p217_t_bio_future"] is True
    assert acls.to_biotechnology_bio_security(tenant_id="t1", security_ref="s1")["autonomous_safety_via_p217s_acl_only"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="sim1")["autonomous_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="q1")["quantum_optimization_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["robotics_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_autonomy_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_unsupervised_autonomous_bio_action"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_responsible_bio_autonomy_controls"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_opaque_autonomous_decisions"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_autonomous():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_autonomous"]["prompt_id"] == "P217-U"
    assert svc.bio_autonomous_readiness()["passed"] is True
