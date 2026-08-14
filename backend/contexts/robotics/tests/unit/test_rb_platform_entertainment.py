"""P216-X robotics entertainment / creative intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_entertainment_foundation import validate_rb_entertainment_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_entertainment as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_entertainment_foundation():
    result = validate_rb_entertainment_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-X"
    assert result["adr"] == 496
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_entertainment_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-X"
    assert cat["fabric"] == "meos_creative_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["personal_gate"] == "P216-W"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["entertainment_robotics_platform_present_required"] is True
    assert cat["creative_ai_platform_present_required"] is True
    assert cat["creative_governance_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_p216_w_personal"] is True
    assert cat["never_replace_identity_platform"] is True
    assert cat["creative_rights_governance_required"] is True
    assert cat["human_ai_creative_collaboration_required"] is True
    assert cat["audience_privacy_required"] is True
    assert cat["foundation_for_p216_y"] is True
    assert "GET /robotics/entertainment" in mod.entertainment_surface()["routes"]
    assert "MEOS Creative Intelligence Platform SHALL unify" in cat["creative_vision"]
@pytest.mark.unit
def test_rb_entertainment_acl():
    from contexts.robotics.infrastructure.acl import rb_entertainment_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_personal(tenant_id="t1", personal_ref="p1")["never_replace_p216_w_personal"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_replace_identity_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_gaming(tenant_id="t1", gaming_ref="g1")["via_gaming_api"] is True
    assert acls.to_streaming(tenant_id="t1", streaming_ref="s1")["via_streaming_api"] is True
    assert acls.to_metaverse(tenant_id="t1", metaverse_ref="mv1")["via_metaverse_api"] is True
    assert acls.to_creative_software(tenant_id="t1", creative_software_ref="cs1")["via_creative_software_api"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["creative_rights_governance_required"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["audience_privacy_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["human_ai_creative_collaboration_required"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_entertainment():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_entertainment"]["prompt_id"] == "P216-X"
    assert svc.entertainment_readiness()["passed"] is True
