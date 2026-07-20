"""P209-C Secrets Domain Architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_domain_foundation import (
    validate_secrets_domain_foundation,
)
from contexts.secrets.domain.services import secrets_platform_domain as pdom

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_domain_foundation():
    result = validate_secrets_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-C"
    assert result["adr"] == 348
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_domain_catalog():
    cat = pdom.catalog()
    assert cat["prompt_id"] == "P209-C"
    assert cat["adr"] == 348
    assert cat["sor"] == "secrets"
    assert cat["domain_boundaries_clear_required"] is True
    assert cat["pki_kms_separation_required"] is True
    assert cat["secrets_managed_required"] is True
    assert cat["trust_relationships_modeled_required"] is True
    assert cat["domain_events_required"] is True
    assert cat["bounded_contexts"]["count"] >= 7
    assert cat["events"]["count"] >= 21
    assert "domain_boundaries_unclear" in cat["quality_gates"]["reject_if"]
    assert (
        "pki_and_kms_responsibilities_mixed"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/domain" in pdom.domain_surface()["routes"]
    assert "GET /secrets/domain/readiness" in pdom.domain_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P209-C"
    assert catalog["platform_domain"]["adr"] == 348
    assert catalog["platform_domain"]["pki_kms_separation_required"] is True
    assert catalog["platform_domain"]["secrets_managed_required"] is True

    summary = svc.platform_domain()
    assert summary["prompt_id"] == "P209-C"
    assert summary["builds_on"] == ["P209", "P209-A", "P209-B"]
    assert summary["bounded_contexts"]["logical_only"] is True
    assert summary["pki_kms_separation"]["separated"] is True
    assert summary["microservices"]["deployable_today"] == "secrets"
    assert "vault" in summary["forbidden_sibling_bc"]
