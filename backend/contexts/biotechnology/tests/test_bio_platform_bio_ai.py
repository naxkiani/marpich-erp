"""P217-E biotechnology Bio-AI foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_ai_foundation import validate_bio_ai_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_ai as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_ai_foundation():
    result = validate_bio_ai_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-E"
    assert result["adr"] == 504
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_ai_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-E"
    assert cat["fabric"] == "meos_bio_ai_intelligence_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["infrastructure_gate"] == "P217-D"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_ai_platform_present_required"] is True
    assert cat["foundation_models_present_required"] is True
    assert cat["ai_biology_engine_present_required"] is True
    assert cat["computational_life_intelligence_core_present_required"] is True
    assert cat["architecture"]["layer_count"] == 5
    assert cat["foundation_models"]["model_count"] == 5
    assert cat["scientific_agents"]["agent_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_d_infrastructure"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_opaque_unexplainable_decisions"] is True
    assert cat["foundation_for_p217_f"] is True
    assert "GET /biotechnology/bio-ai" in mod.bio_ai_surface()["routes"]
    assert "intelligence-driven ecosystem" in cat["bio_ai_vision"]
@pytest.mark.unit
def test_bio_ai_acl():
    from contexts.biotechnology.infrastructure.acl import bio_ai_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_infrastructure(tenant_id="t1", infra_ref="i1")["never_replace_p217_d_infrastructure"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_bio_safety_strategy_forbidden"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_ai():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_ai"]["prompt_id"] == "P217-E"
    assert svc.bio_ai_readiness()["passed"] is True
