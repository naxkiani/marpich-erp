"""P217 biotechnology / bio intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_foundation_foundation import validate_bio_foundation_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_foundation as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_foundation_foundation():
    result = validate_bio_foundation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217"
    assert result["adr"] == 499
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_foundation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217"
    assert cat["fabric"] == "meos_bio_intelligence_fabric"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["biotechnology_platform_present_required"] is True
    assert cat["synthetic_biology_platform_present_required"] is True
    assert cat["bio_ai_intelligence_engine_present_required"] is True
    assert cat["bio_ethics_governance_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_hospital_emr"] is True
    assert cat["never_replace_laboratory_lims"] is True
    assert cat["never_replace_robotics_supreme"] is True
    assert cat["genomic_privacy_required"] is True
    assert cat["ethical_bioengineering_required"] is True
    assert cat["opaque_bio_safety_decisions_forbidden"] is True
    assert cat["foundation_for_p217_a"] is True
    assert "GET /biotechnology/foundation" in mod.foundation_surface()["routes"]
    assert "MEOS Bio Intelligence Platform SHALL unify" in cat["bio_vision"]
@pytest.mark.unit
def test_bio_foundation_acl():
    from contexts.biotechnology.infrastructure.acl import bio_foundation_acl as acls
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_robotics_supreme"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="p1")["never_replace_pharmacy"] is True
    assert acls.to_integration(tenant_id="t1", connector_ref="c1")["research_via_integration_platform_only"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["genomic_privacy_required"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ethical_bioengineering_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_bio_safety_decisions_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_foundation():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_foundation"]["prompt_id"] == "P217"
    assert svc.foundation_readiness()["passed"] is True
