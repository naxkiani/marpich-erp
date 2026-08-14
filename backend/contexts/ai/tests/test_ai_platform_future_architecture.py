"""P214-X future-architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.ai.application.ai_future_architecture_foundation import validate_ai_future_architecture_foundation
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_future_architecture as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service(); yield; reset_ai_service()
@pytest.mark.unit
def test_ai_future_architecture_foundation():
    result = validate_ai_future_architecture_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P214-X"
    assert result["adr"] == 444
@pytest.mark.unit
def test_ai_future_architecture_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-X"
    assert cat["future_ai_architecture_present_required"] is True
    assert cat["superintelligence_governance"]["via_p214_u"] is True
    assert cat["knowledge_graph"]["via_p214_g"] is True
    assert "GET /ai/future-arch" in mod.future_arch_surface()["routes"]
@pytest.mark.unit
def test_ai_future_architecture_acl():
    from contexts.ai.infrastructure.acl import ai_future_architecture_acl as acls
    assert acls.to_aiciv(tenant_id="t1", civilization_ref="c1")["via_p214_w"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", future_ref="f1")["module_local_future_arch_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_future_architecture():
    svc = get_ai_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_future_architecture"]["prompt_id"] == "P214-X"; assert svc.future_arch_readiness()["passed"] is True
