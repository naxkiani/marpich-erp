"""P207-F Identity Digital Twin Platform foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_twin_foundation import (
    validate_ii_twin_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_twins as twins,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_twin_foundation():
    result = validate_ii_twin_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-F"
    assert result["adr"] == 321
    assert result["sor"] == "identity_intelligence"
    assert result["twin_storage_peer"] == "identity_digital_twin"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_twin_catalog():
    cat = twins.catalog()
    assert cat["prompt_id"] == "P207-F"
    assert cat["adr"] == 321
    assert cat["sor"] == "identity_intelligence"
    assert cat["twin_storage_peer"] == "identity_digital_twin"
    assert cat["capabilities"]["not_data_copy"] is True
    assert cat["simulation"]["not_missing"] is True
    assert cat["impact_analysis"]["not_unavailable"] is True
    assert "twin_only_data_copy" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/twins" in twins.twins_surface()["routes"]
    assert (
        "GET /identity-intelligence/twins/readiness"
        in twins.twins_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_twins():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_twins"]["prompt_id"] == "P207-F"
    assert catalog["platform_twins"]["adr"] == 321
    assert catalog["platform_twins"]["not_data_copy_only"] is True
    assert catalog["platform_twins"]["twin_storage_peer"] == "identity_digital_twin"
    assert catalog["delegation"]["twin_sor_duplication"] is False
    assert catalog["delegation"]["twin_data_copy_only"] is False

    summary = svc.platform_twins()
    assert summary["prompt_id"] == "P207-F"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-B",
        "P207-C",
        "P207-D",
        "P207-E",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
