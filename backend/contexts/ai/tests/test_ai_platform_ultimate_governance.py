"""P214-Y ultimate-governance foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.ai.application.ai_ultimate_governance_foundation import validate_ai_ultimate_governance_foundation
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_ultimate_governance as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service(); yield; reset_ai_service()
@pytest.mark.unit
def test_ai_ultimate_governance_foundation():
    result = validate_ai_ultimate_governance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P214-Y"
    assert result["adr"] == 445
@pytest.mark.unit
def test_ai_ultimate_governance_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-Y"
    assert cat["ultimate_ai_governance_present_required"] is True
    assert cat["alignment"]["via_p214_u"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert cat["deepens_p214_x"] is True
    assert "GET /ai/ultimate-governance" in mod.ultimate_governance_surface()["routes"]
@pytest.mark.unit
def test_ai_ultimate_governance_acl():
    from contexts.ai.infrastructure.acl import ai_ultimate_governance_acl as acls
    assert acls.to_aifuture(tenant_id="t1", future_ref="f1")["via_p214_x"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", trust_ref="u1")["module_local_ultimate_governance_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ultimate_governance():
    svc = get_ai_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_ultimate_governance"]["prompt_id"] == "P214-Y"; assert svc.ultimate_governance_readiness()["passed"] is True
