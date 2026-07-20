"""P207-J AI Governance & Access Optimization foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_access_gov_foundation import (
    validate_ii_access_gov_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_access_gov as access_gov,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_access_gov_foundation():
    result = validate_ii_access_gov_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-J"
    assert result["adr"] == 325
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_access_gov_catalog():
    cat = access_gov.catalog()
    assert cat["prompt_id"] == "P207-J"
    assert cat["adr"] == 325
    assert cat["sor"] == "identity_intelligence"
    assert cat["capabilities"]["not_periodic"] is True
    assert cat["certification"]["not_periodic_only"] is True
    assert cat["risk_integration"]["via_p207g"] is True
    assert "governance_periodic_only" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert (
        "GET /identity-intelligence/access-gov"
        in access_gov.access_gov_surface()["routes"]
    )
    assert (
        "GET /identity-intelligence/access-gov/readiness"
        in access_gov.access_gov_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_access_gov():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_access_gov"]["prompt_id"] == "P207-J"
    assert catalog["platform_access_gov"]["adr"] == 325
    assert catalog["platform_access_gov"]["not_periodic_only"] is True
    assert catalog["platform_access_gov"]["continuous_governance"] is True
    assert catalog["delegation"]["periodic_only_governance"] is False

    summary = svc.platform_access_gov()
    assert summary["prompt_id"] == "P207-J"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-B",
        "P207-C",
        "P207-E",
        "P207-F",
        "P207-G",
        "P207-H",
        "P207-I",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
