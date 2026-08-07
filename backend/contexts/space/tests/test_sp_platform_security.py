"""P218-P security intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_security_foundation import validate_sp_security_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_security as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_security_foundation():
    result = validate_sp_security_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-P"
    assert result["adr"] == 542
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_security_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-P"
    assert cat["fabric"] == "meos_space_security_intelligence_fabric"
    assert cat["logistics_gate"] == "P218-O"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["cybersecurity"]["domain_count"] == 8
    assert cat["satellite_security"]["capability_count"] == 7
    assert cat["security_ai"]["model_count"] == 5
    assert cat["autonomy"]["agent_count"] == 7
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_o_logistics"] is True
    assert cat["never_ungated_autonomous_security_response"] is True
    assert cat["never_skip_command_authentication"] is True
    assert cat["never_skip_satellite_identity_verification"] is True
    assert cat["never_opaque_unexplainable_security_decisions"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_q"] is True
    assert "GET /space/security" in mod.security_surface()["routes"]
    assert "intelligent security ecosystem capable of detecting" in cat["security_mission"]


@pytest.mark.unit
def test_sp_security_acl():
    from contexts.space.infrastructure.acl import sp_security_acl as acls

    assert acls.to_logistics(tenant_id="t1", logistics_ref="l1")["never_replace_p218_o_logistics"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_autonomous_security_response"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_command_authentication"] is True
    assert acls.to_satellite(tenant_id="t1", satellite_ref="s1")["never_skip_satellite_identity_verification"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", security_ref="sec1")["module_local_security_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_security():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_security"]["prompt_id"] == "P218-P"
    assert svc.security_readiness()["passed"] is True
