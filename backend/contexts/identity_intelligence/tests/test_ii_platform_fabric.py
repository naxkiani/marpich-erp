"""P207-L distributed fabric foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_fabric_foundation import (
    validate_ii_fabric_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_fabric as fabric,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_fabric_foundation():
    result = validate_ii_fabric_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-L"
    assert result["adr"] == 327
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_fabric_catalog():
    cat = fabric.catalog()
    assert cat["prompt_id"] == "P207-L"
    assert cat["adr"] == 327
    assert cat["sor"] == "identity_intelligence"
    assert cat["shared_database_forbidden"] is True
    assert cat["secure_api_required"] is True
    assert cat["capabilities"]["event_store_required"] is True
    assert cat["capabilities"]["ai_integration_connected_required"] is True
    assert "services_share_databases" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness_assessment"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/fabric" in fabric.fabric_surface()["routes"]
    assert (
        "GET /identity-intelligence/fabric/readiness"
        in fabric.fabric_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_fabric():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_fabric"]["prompt_id"] == "P207-L"
    assert catalog["platform_fabric"]["adr"] == 327
    assert catalog["platform_fabric"]["shared_database_forbidden"] is True
    assert catalog["platform_fabric"]["secure_api_required"] is True
    assert catalog["delegation"]["shared_service_database"] is False

    summary = svc.platform_fabric()
    assert summary["prompt_id"] == "P207-L"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-C",
        "P207-D",
        "P207-E",
        "P207-F",
        "P207-G",
        "P207-H",
        "P207-I",
        "P207-J",
        "P207-K",
    ]
    assert summary["microservice_architecture"]["deployable_today"] == "identity_intelligence"
    assert summary["command_catalog"]["count"] >= 16
    assert summary["event_catalog"]["count"] >= 17
