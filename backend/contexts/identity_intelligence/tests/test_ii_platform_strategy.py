"""P207-A Identity Intelligence strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_platform_foundation import (
    validate_ii_strategy_foundation,
)
from contexts.identity_intelligence.domain.services import ii_platform_strategy as strat

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_strategy_foundation():
    result = validate_ii_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-A"
    assert result["adr"] == 316
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["principles"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True
    assert result["registry"] is True


@pytest.mark.unit
def test_ii_catalog():
    cat = strat.catalog()
    assert cat["prompt_id"] == "P207-A"
    assert cat["adr"] == 316
    assert cat["sor"] == "identity_intelligence"
    assert cat["chatbot_only_forbidden"] is True
    assert cat["digital_twin"]["not_absent"] is True
    assert cat["knowledge_graph"]["not_missing"] is True
    assert cat["predictive_risk"]["not_unmeasurable"] is True
    assert cat["autonomous_operations"]["not_ungoverned"] is True
    assert cat["ai_agents"]["not_chatbot_only"] is True
    assert "ai_only_chatbot" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/strategy" in strat.strategy_surface()["routes"]
    assert (
        "GET /identity-intelligence/strategy/readiness"
        in strat.strategy_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ii():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_identity_intelligence"]["prompt_id"] == "P207-A"
    assert catalog["platform_identity_intelligence"]["adr"] == 316
    assert catalog["platform_identity_intelligence"]["chatbot_only_forbidden"] is True
    assert catalog["delegation"]["embeds_llm"] is False
    assert catalog["delegation"]["chatbot_only"] is False

    summary = svc.platform_identity_intelligence()
    assert summary["prompt_id"] == "P207-A"
    assert summary["forbidden_sibling_bc"] == "ai_identity_ops"
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
    assert summary["builds_on"] == [
        "P201",
        "P202",
        "P203",
        "P204",
        "P205",
        "identity_digital_twin",
    ]
