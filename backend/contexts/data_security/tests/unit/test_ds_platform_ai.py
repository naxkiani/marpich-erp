"""P211-L Data Security AI autonomous protection foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_ai_foundation import (
    validate_ds_ai_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_ai as ai,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_ai_foundation():
    result = validate_ds_ai_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-L"
    assert result["adr"] == 387
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_ai_catalog():
    cat = ai.catalog()
    assert cat["prompt_id"] == "P211-L"
    assert cat["adr"] == 387
    assert cat["ai_decisions_explainable_required"] is True
    assert cat["autonomous_actions_controlled_required"] is True
    assert cat["data_risks_predictable_required"] is True
    assert cat["learning_loop_present_required"] is True
    assert cat["ai_security_governance_present_required"] is True
    assert cat["human_oversight_possible_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["agents"]["agent_count"] >= 6
    assert cat["cursor_outputs"]["count"] >= 16
    assert "ai_decisions_are_not_explainable" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/ai-data" in ai.ai_surface()["routes"]
    assert "GET /data-security/ai-data/readiness" in ai.ai_surface()["routes"]


@pytest.mark.unit
def test_ds_ai_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_ai_acl as acls,
    )

    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_decisions_explainable_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_workflow_oversight(tenant_id="t1", action_ref="a1")[
        "human_oversight_possible_required"
    ] is True
    assert acls.to_workflow_oversight(tenant_id="t1", action_ref="a1")[
        "autonomous_actions_controlled_required"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")[
        "ai_security_governance_present_required"
    ] is True
    assert acls.to_intelligence(tenant_id="t1", graph_ref="g1")[
        "learning_loop_present_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ai():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ai"]["prompt_id"] == "P211-L"
    assert catalog["platform_ai"]["adr"] == 387
    summary = svc.platform_ai()
    assert summary["prompt_id"] == "P211-L"
    assert "P211-K" in summary["builds_on"]
    assert summary["agent_count"] >= 6
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
