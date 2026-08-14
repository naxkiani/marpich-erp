"""P210-J Cyber Security AI Ops foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_ai_ops_foundation import (
    validate_cs_ai_ops_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_ai_ops as ai_ops

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_ai_ops_foundation():
    result = validate_cs_ai_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-J"
    assert result["adr"] == 370
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_ai_ops_catalog():
    cat = ai_ops.catalog()
    assert cat["prompt_id"] == "P210-J"
    assert cat["adr"] == 370
    assert cat["ai_decisions_explainable_required"] is True
    assert cat["human_oversight_required"] is True
    assert cat["model_lifecycle_management_required"] is True
    assert cat["module_local_llm_sdk_forbidden"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["agents"]["agent_count"] >= 15
    assert cat["cursor_outputs"]["count"] >= 20
    assert "ai_decisions_not_explainable" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/ai-ops" in ai_ops.ai_ops_surface()["routes"]
    assert (
        "GET /cyber-security/ai-ops/readiness" in ai_ops.ai_ops_surface()["routes"]
    )


@pytest.mark.unit
def test_cs_ai_ops_acl():
    from contexts.cyber_security.infrastructure.acl import cs_ai_ops_acl as acls

    assert acls.to_enterprise_ai(tenant_id="t1", inference_ref="i1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_workflow_oversight(tenant_id="t1", gate_ref="g1")[
        "human_oversight_required"
    ] is True
    assert acls.to_model_lifecycle(tenant_id="t1", model_ref="m1")[
        "model_lifecycle_management_required"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", graph_ref="kg1")[
        "connected_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ai_ops():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ai_ops"]["prompt_id"] == "P210-J"
    assert catalog["platform_ai_ops"]["adr"] == 370
    summary = svc.platform_ai_ops()
    assert summary["prompt_id"] == "P210-J"
    assert "P210-I" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
