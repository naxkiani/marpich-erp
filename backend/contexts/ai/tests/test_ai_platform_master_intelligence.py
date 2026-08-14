"""P214-Z master-intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.ai.application.ai_master_intelligence_foundation import validate_ai_master_intelligence_foundation
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_master_intelligence as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service(); yield; reset_ai_service()
@pytest.mark.unit
def test_ai_master_intelligence_foundation():
    result = validate_ai_master_intelligence_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P214-Z"
    assert result["adr"] == 446
@pytest.mark.unit
def test_ai_master_intelligence_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-Z"
    assert cat["enterprise_ai_master_intelligence_architecture_present_required"] is True
    assert cat["supreme_control_plane"]["via_p214_t"] is True
    assert cat["enterprise_brain"]["via_p214_v"] is True
    assert cat["federates_p214_a_through_y"] is True
    assert "GET /ai/master-intelligence" in mod.master_intelligence_surface()["routes"]
@pytest.mark.unit
def test_ai_master_intelligence_acl():
    from contexts.ai.infrastructure.acl import ai_master_intelligence_acl as acls
    assert acls.to_ultimate_governance(tenant_id="t1", trust_ref="y1")["via_p214_y"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", master_ref="m1")["module_local_master_intelligence_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_master_intelligence():
    svc = get_ai_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_master_intelligence"]["prompt_id"] == "P214-Z"; assert svc.master_intelligence_readiness()["passed"] is True
