"""P213-M BI AI native foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_ai_foundation import (
    validate_bi_ai_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_ai as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_ai_foundation():
    result = validate_bi_ai_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-M"
    assert result["adr"] == 417
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_ai_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-M"
    assert cat["adr"] == 417
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "AI reasoning" in cat["principle"]
    assert cat["ai_native_analytics_platform_present_required"] is True
    assert cat["autonomous_decision_intelligence_present_required"] is True
    assert cat["enterprise_ai_agent_platform_present_required"] is True
    assert cat["multi_agent_collaboration_present_required"] is True
    assert cat["executive_ai_copilot_present_required"] is True
    assert cat["ai_governance_platform_present_required"] is True
    assert cat["via_enterprise_ai_only"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_autonomous_decision_intelligence"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "AutonomousDecisionAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["agents"]["agent_count"] >= 16
    assert cat["autonomy"]["level_count"] >= 5
    assert cat["reasoning"]["mode_count"] >= 11
    assert cat["events"]["core_event_count"] >= 9
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "executive_ai_copilot_is_missing" in cat["quality_gates"]["reject_if"]
    )
    assert "P213-L" in cat["builds_on"]
    assert "P212-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/ai" in mod.ai_surface()["routes"]
    assert "GET /analytics/ai/copilot" in mod.ai_surface()["routes"]


@pytest.mark.unit
def test_bi_ai_acl():
    from contexts.analytics.infrastructure.acl import bi_ai_acl as acls

    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p213_l"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_predictive(tenant_id="t1", forecast_ref="f1")[
        "via_p213_j"
    ] is True
    assert acls.to_prescriptive(tenant_id="t1", recommendation_ref="r1")[
        "via_p213_k"
    ] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", trust_ref="t1")[
        "via_p209"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", asset_ref="a1")[
        "via_p210"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="approve"
    )["human_approval_policies"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ai():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ai"]["prompt_id"] == "P213-M"
    assert catalog["platform_ai"]["adr"] == 417
    assert catalog["sor"] == "analytics"
    summary = svc.platform_ai()
    assert summary["prompt_id"] == "P213-M"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-L" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["agent_count"] >= 16
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.ai_readiness()["passed"] is True
    assert svc.ai_agents()["module_local_llm_sdk_forbidden"] is True
    assert svc.ai_autonomy()["level_count"] >= 5
