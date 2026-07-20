"""P207-D Autonomous Identity Operations foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_autonomous_foundation import (
    validate_ii_autonomous_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_autonomous as auto,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_autonomous_foundation():
    result = validate_ii_autonomous_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-D"
    assert result["adr"] == 319
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_autonomous_catalog():
    cat = auto.catalog()
    assert cat["prompt_id"] == "P207-D"
    assert cat["adr"] == 319
    assert cat["sor"] == "identity_intelligence"
    assert cat["capabilities"]["not_ungoverned"] is True
    assert cat["self_healing"]["not_missing"] is True
    assert cat["ai_governance"]["not_absent_oversight"] is True
    assert "automation_without_governance" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/autonomous" in auto.autonomous_surface()["routes"]
    assert (
        "GET /identity-intelligence/autonomous/readiness"
        in auto.autonomous_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_autonomous():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_autonomous"]["prompt_id"] == "P207-D"
    assert catalog["platform_autonomous"]["adr"] == 319
    assert catalog["platform_autonomous"]["automation_governance_required"] is True
    assert catalog["delegation"]["ungoverned_automation"] is False

    summary = svc.platform_autonomous()
    assert summary["prompt_id"] == "P207-D"
    assert summary["builds_on"] == ["P207-A", "P207-B", "P207-C"]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
