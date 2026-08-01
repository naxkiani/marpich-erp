"""P216-K robotics construction / smart infrastructure foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_construction_foundation import validate_rb_construction_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_construction as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_construction_foundation():
    result = validate_rb_construction_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-K"
    assert result["adr"] == 483
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_construction_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-K"
    assert cat["fabric"] == "meos_construction_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["healthcare_gate"] == "P216-I"
    assert cat["mobility_gate"] == "P216-H"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["construction_robotics_platform_present_required"] is True
    assert cat["smart_infrastructure_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 16
    assert cat["never_replace_p216_i_healthcare"] is True
    assert cat["never_direct_bim_gis_scada_bypass"] is True
    assert cat["foundation_for_p216_l"] is True
    assert "GET /robotics/construction" in mod.construction_surface()["routes"]
    assert "MEOS Construction Intelligence Platform SHALL unify" in cat["construction_vision"]
@pytest.mark.unit
def test_rb_construction_acl():
    from contexts.robotics.infrastructure.acl import rb_construction_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_healthcare(tenant_id="t1", healthcare_ref="h1")["never_replace_p216_i_healthcare"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["never_direct_bim_gis_scada_bypass"] is True
    assert acls.to_construction_peer(tenant_id="t1", construction_ref="c1")["never_duplicate_construction_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_construction():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_construction"]["prompt_id"] == "P216-K"
    assert svc.construction_readiness()["passed"] is True
