"""P219-T civilization intelligence governance platform foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_intel_gov_foundation import (
    validate_civ_intel_gov_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_intel_gov as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_intel_gov_foundation():
    result = validate_civ_intel_gov_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-T"
    assert result["adr"] == 573
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_intel_gov_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-T"
    assert cat["fabric"] == "meos_civilization_os_civilization_governance_alignment_intelligence_framework"
    assert cat["foundation_gate"] == "P219"
    assert cat["mission_gate"] == "P219-A"
    assert cat["strategy_gate"] == "P219-B"
    assert cat["domain_gate"] == "P219-C"
    assert cat["planetary_gate"] == "P219-D"
    assert cat["ai_os_gate"] == "P219-E"
    assert cat["simulation_gate"] == "P219-F"
    assert cat["resources_gate"] == "P219-G"
    assert cat["economy_gate"] == "P219-H"
    assert cat["knowledge_gate"] == "P219-I"
    assert cat["human_gate"] == "P219-J"
    assert cat["governance_gate"] == "P219-K"
    assert cat["innovation_gate"] == "P219-L"
    assert cat["security_gate"] == "P219-M"
    assert cat["sustainability_gate"] == "P219-N"
    assert cat["prosperity_gate"] == "P219-O"
    assert cat["collaboration_gate"] == "P219-P"
    assert cat["consciousness_gate"] == "P219-Q"
    assert cat["evolution_gate"] == "P219-R"
    assert cat["futures_gate"] == "P219-S"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["architecture"]["maturity_stage_count"] == 6
    assert cat["architecture"]["layer_count"] == 6
    assert cat["architecture"]["governance_domain_count"] == 10
    assert cat["architecture"]["intelligence_governance_domain_count"] == 10
    assert cat["architecture"]["alignment_dimension_count"] == 9
    assert cat["architecture"]["policy_lifecycle_step_count"] == 7
    assert cat["architecture"]["policy_domain_count"] == 9
    assert cat["architecture"]["trust_domain_count"] == 6
    assert cat["architecture"]["compliance_domain_count"] == 5
    assert cat["architecture"]["decision_lifecycle_step_count"] == 8
    assert cat["agents"]["agent_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 11
    assert cat["knowledge_graph"]["relationship_count"] == 8
    assert cat["digital_twin"]["twin_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 4
    assert cat["aggregates"]["aggregate_count"] == 5
    assert cat["events"]["core_event_count"] == 12
    assert cat["cqrs"]["command_count"] == 6
    assert cat["cqrs"]["query_count"] == 6
    assert cat["microservices"]["service_count"] == 10
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_p219_k_governance"] is True
    assert cat["never_replace_p219_s_futures"] is True
    assert cat["never_replace_policy_engine"] is True
    assert cat["never_ungated_governance_decision_execution"] is True
    assert cat["never_opaque_unexplainable_governance_decisions"] is True
    assert cat["never_bypass_human_supervision_governance"] is True
    assert cat["never_bypass_human_accountability"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p219_u"] is True
    assert "GET /civilization/intelligence-governance" in mod.intel_gov_surface()["routes"]
    assert "aligning strategy, policy, execution and decision-making" in cat["primary_capability"]


@pytest.mark.unit
def test_civ_intel_gov_acl():
    from contexts.civilization.infrastructure.acl import civ_intel_gov_acl as acls

    assert acls.to_civilization_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p219_foundation"] is True
    assert acls.to_civilization_ai_os(tenant_id="t1", aios_ref="a1")["never_replace_p219_e_ai_os"] is True
    assert acls.to_civilization_simulation(tenant_id="t1", simulation_ref="s1")["never_replace_p219_f_simulation"] is True
    assert acls.to_civilization_governance(tenant_id="t1", governance_ref="g1")["never_replace_p219_k_governance"] is True
    assert acls.to_civilization_futures(tenant_id="t1", futures_ref="f1")["never_replace_p219_s_futures"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_bypass_human_accountability"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_replace_policy_engine"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_governance_decision_execution"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_replace_audit"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["never_replace_ai_platform"] is True
    assert acls.to_enterprise_civilization(tenant_id="t1", intel_gov_ref="g1")["never_bypass_human_accountability"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_intel_gov():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_intel_gov"]["prompt_id"] == "P219-T"
    assert catalog["platform_intel_gov"]["foundation_for_p219_u"] is True
    assert svc.intel_gov_readiness()["passed"] is True
