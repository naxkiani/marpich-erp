"""P207-I Self-Healing Identity Fabric foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_healing_foundation import (
    validate_ii_healing_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_healing as healing,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_healing_foundation():
    result = validate_ii_healing_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-I"
    assert result["adr"] == 324
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_healing_catalog():
    cat = healing.catalog()
    assert cat["prompt_id"] == "P207-I"
    assert cat["adr"] == 324
    assert cat["sor"] == "identity_intelligence"
    assert cat["capabilities"]["not_manual_only"] is True
    assert cat["remediation"]["not_ungoverned"] is True
    assert cat["digital_twin"]["not_absent"] is True
    assert "recovery_fully_manual" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/healing" in healing.healing_surface()["routes"]
    assert (
        "GET /identity-intelligence/healing/readiness"
        in healing.healing_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_healing():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_healing"]["prompt_id"] == "P207-I"
    assert catalog["platform_healing"]["adr"] == 324
    assert catalog["platform_healing"]["not_fully_manual"] is True
    assert catalog["platform_healing"]["twin_simulation_required"] is True
    assert catalog["delegation"]["fully_manual_healing"] is False

    summary = svc.platform_healing()
    assert summary["prompt_id"] == "P207-I"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-B",
        "P207-C",
        "P207-D",
        "P207-E",
        "P207-F",
        "P207-G",
        "P207-H",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
