"""P207-M AI Security & Governance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_ai_gov_foundation import (
    validate_ii_ai_gov_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_ai_gov as ai_gov,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_ai_gov_foundation():
    result = validate_ii_ai_gov_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-M"
    assert result["adr"] == 328
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_ai_gov_catalog():
    cat = ai_gov.catalog()
    assert cat["prompt_id"] == "P207-M"
    assert cat["adr"] == 328
    assert cat["sor"] == "identity_intelligence"
    assert cat["platform_ai_gov_peer"] == "ai_governance"
    assert cat["ai_governance_required"] is True
    assert cat["explainable_required"] is True
    assert cat["capabilities"]["does_not_own_platform_ai_gov_sor"] is True
    assert "ai_operates_without_governance" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/ai-gov" in ai_gov.ai_gov_surface()["routes"]
    assert (
        "GET /identity-intelligence/ai-gov/readiness"
        in ai_gov.ai_gov_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ai_gov():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ai_gov"]["prompt_id"] == "P207-M"
    assert catalog["platform_ai_gov"]["adr"] == 328
    assert catalog["platform_ai_gov"]["ai_governance_required"] is True
    assert catalog["platform_ai_gov"]["explainable_required"] is True
    assert catalog["delegation"]["ungoverned_ai"] is False

    summary = svc.platform_ai_gov()
    assert summary["prompt_id"] == "P207-M"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-D",
        "P207-E",
        "P207-F",
        "P207-G",
        "P207-H",
        "P207-I",
        "P207-J",
        "P207-K",
        "P207-L",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
    assert summary["autonomous_action_governance"]["level_count"] == 5
