"""P209-E Secrets CA / Trust Chain foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_ca_foundation import (
    validate_secrets_ca_foundation,
)
from contexts.secrets.domain.services import secrets_platform_ca as ca

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_ca_foundation():
    result = validate_secrets_ca_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-E"
    assert result["adr"] == 350
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_ca_catalog():
    cat = ca.catalog()
    assert cat["prompt_id"] == "P209-E"
    assert cat["adr"] == 350
    assert cat["sor"] == "secrets"
    assert cat["root_ca_online_unprotected_forbidden"] is True
    assert cat["ca_private_keys_hsm_required"] is True
    assert cat["trust_chain_validation_required"] is True
    assert cat["revocation_available_required"] is True
    assert cat["certificate_ownership_known_required"] is True
    assert cat["ca_governance_defined_required"] is True
    assert cat["audit_trail_complete_required"] is True
    assert cat["hierarchy"]["count"] >= 7
    assert cat["cqrs"]["event_count"] >= 12
    assert "root_ca_online_without_protection" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/ca" in ca.ca_surface()["routes"]
    assert "GET /secrets/ca/readiness" in ca.ca_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ca():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ca"]["prompt_id"] == "P209-E"
    assert catalog["platform_ca"]["adr"] == 350
    assert catalog["platform_ca"]["root_ca_online_unprotected_forbidden"] is True
    assert catalog["platform_ca"]["ca_private_keys_hsm_required"] is True

    summary = svc.platform_ca()
    assert summary["prompt_id"] == "P209-E"
    assert summary["builds_on"] == [
        "P209",
        "P209-A",
        "P209-B",
        "P209-C",
        "P209-D",
    ]
    assert "ca_platform" in summary["forbidden_sibling_bc"]
    assert summary["root_ca"]["hsm_protected"] is True
    assert summary["revocation"]["ocsp"] is True
    assert summary["cursor_outputs"]["count"] == 20
