"""P217-C biotechnology DDD domain architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_domain_foundation import validate_bio_domain_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_domain as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_domain_foundation():
    result = validate_bio_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-C"
    assert result["adr"] == 502
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_domain_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-C"
    assert cat["fabric"] == "meos_biotechnology_domain_architecture_framework"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["biotechnology_core_domain_present_required"] is True
    assert cat["bounded_context_map_present_required"] is True
    assert cat["aggregates_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["aggregates"]["aggregate_count"] == 7
    assert cat["domain_services"]["service_count"] == 14
    assert cat["repositories"]["repository_count"] == 7
    assert cat["microservices"]["service_count"] == 7
    assert cat["events"]["core_event_count"] == 9
    assert cat["never_replace_p217_foundation"] is True
    assert cat["never_replace_p217_a_mission"] is True
    assert cat["never_replace_p217_b_strategy"] is True
    assert cat["never_cross_context_aggregate_mutation"] is True
    assert cat["foundation_for_p217_d"] is True
    assert "GET /biotechnology/domain" in mod.domain_surface()["routes"]
    assert "intelligent biological discovery" in cat["primary_capability"]
@pytest.mark.unit
def test_bio_domain_acl():
    from contexts.biotechnology.infrastructure.acl import bio_domain_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_mission(tenant_id="t1", mission_ref="m1")["never_replace_p217_a_mission"] is True
    assert acls.to_biotechnology_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p217_b_strategy"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["genomic_privacy_strategy_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_bio_safety_strategy_forbidden"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
    assert acls.to_enterprise_biotechnology(tenant_id="t1", domain_ref="d1")["never_cross_context_aggregate_mutation"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P217-C"
    assert svc.domain_readiness()["passed"] is True
