"""P207-C Identity Intelligence Domain Architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_domain_foundation import (
    validate_ii_domain_foundation,
)
from contexts.identity_intelligence.domain.services import ii_platform_domain as pdom

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_domain_foundation():
    result = validate_ii_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-C"
    assert result["adr"] == 318
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_domain_catalog():
    cat = pdom.catalog()
    assert cat["prompt_id"] == "P207-C"
    assert cat["adr"] == 318
    assert cat["sor"] == "identity_intelligence"
    assert cat["ddd"]["boundaries_clear"] is True
    assert cat["ddd"]["not_anemic"] is True
    assert cat["cqrs"]["cqrs_ready"] is True
    assert cat["purpose"]["transforms_into"] == (
        "actionable_enterprise_identity_intelligence"
    )
    assert "ddd_boundaries_unclear" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/domain" in pdom.domain_surface()["routes"]
    assert (
        "GET /identity-intelligence/domain/readiness"
        in pdom.domain_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P207-C"
    assert catalog["platform_domain"]["adr"] == 318
    assert catalog["platform_domain"]["ddd_boundaries_clear"] is True

    summary = svc.platform_domain()
    assert summary["prompt_id"] == "P207-C"
    assert summary["builds_on"] == ["P207-A", "P207-B"]
    assert summary["ddd"]["aggregate_count"] >= 12
