"""P207-G Predictive Identity Risk Intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_risk_foundation import (
    validate_ii_risk_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_risk as risk,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_risk_foundation():
    result = validate_ii_risk_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-G"
    assert result["adr"] == 322
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_risk_catalog():
    cat = risk.catalog()
    assert cat["prompt_id"] == "P207-G"
    assert cat["adr"] == 322
    assert cat["sor"] == "identity_intelligence"
    assert cat["capabilities"]["not_static"] is True
    assert cat["prediction"]["not_absent"] is True
    assert cat["trust_engine"]["not_undefined"] is True
    assert "risk_static_only" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/risk" in risk.risk_surface()["routes"]
    assert (
        "GET /identity-intelligence/risk/readiness"
        in risk.risk_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_risk():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_risk"]["prompt_id"] == "P207-G"
    assert catalog["platform_risk"]["adr"] == 322
    assert catalog["platform_risk"]["not_static_only"] is True
    assert catalog["platform_risk"]["prediction_required"] is True
    assert catalog["delegation"]["static_only_risk"] is False

    summary = svc.platform_risk()
    assert summary["prompt_id"] == "P207-G"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-B",
        "P207-C",
        "P207-D",
        "P207-E",
        "P207-F",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
