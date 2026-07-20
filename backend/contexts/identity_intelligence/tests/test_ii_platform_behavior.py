"""P207-H Behavioral Identity Analytics foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_behavior_foundation import (
    validate_ii_behavior_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_behavior as behavior,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_behavior_foundation():
    result = validate_ii_behavior_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-H"
    assert result["adr"] == 323
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_behavior_catalog():
    cat = behavior.catalog()
    assert cat["prompt_id"] == "P207-H"
    assert cat["adr"] == 323
    assert cat["sor"] == "identity_intelligence"
    assert cat["capabilities"]["not_rule_only_analysis"] is True
    assert cat["baseline"]["not_absent"] is True
    assert cat["behavioral_risk"]["via_p207g"] is True
    assert "behavioral_analysis_rule_only" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert (
        "GET /identity-intelligence/behavior" in behavior.behavior_surface()["routes"]
    )
    assert (
        "GET /identity-intelligence/behavior/readiness"
        in behavior.behavior_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_behavior():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_behavior"]["prompt_id"] == "P207-H"
    assert catalog["platform_behavior"]["adr"] == 323
    assert catalog["platform_behavior"]["not_rule_only"] is True
    assert catalog["platform_behavior"]["learning_required"] is True
    assert catalog["delegation"]["rule_only_behavior"] is False

    summary = svc.platform_behavior()
    assert summary["prompt_id"] == "P207-H"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-B",
        "P207-C",
        "P207-D",
        "P207-E",
        "P207-F",
        "P207-G",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
