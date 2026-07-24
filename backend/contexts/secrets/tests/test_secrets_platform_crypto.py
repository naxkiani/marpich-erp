"""P209-I Secrets Cryptography Services foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_crypto_foundation import (
    validate_secrets_crypto_foundation,
)
from contexts.secrets.domain.services import secrets_platform_crypto as crypto

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_crypto_foundation():
    result = validate_secrets_crypto_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-I"
    assert result["adr"] == 354
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_crypto_catalog():
    cat = crypto.catalog()
    assert cat["prompt_id"] == "P209-I"
    assert cat["adr"] == 354
    assert cat["sor"] == "secrets"
    assert cat["unmanaged_cryptography_forbidden"] is True
    assert cat["encryption_governance_required"] is True
    assert cat["keys_exposed_forbidden"] is True
    assert cat["algorithms_controlled_required"] is True
    assert cat["signatures_verifiable_required"] is True
    assert cat["crypto_operations_audited_required"] is True
    assert cat["cqrs"]["event_count"] >= 12
    assert (
        "applications_implement_unmanaged_cryptography"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/crypto" in crypto.crypto_surface()["routes"]
    assert "GET /secrets/crypto/readiness" in crypto.crypto_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_crypto():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_crypto"]["prompt_id"] == "P209-I"
    assert catalog["platform_crypto"]["adr"] == 354
    assert catalog["platform_crypto"]["unmanaged_cryptography_forbidden"] is True
    assert catalog["platform_crypto"]["keys_exposed_forbidden"] is True

    summary = svc.platform_crypto()
    assert summary["prompt_id"] == "P209-I"
    assert summary["builds_on"] == [
        "P209",
        "P209-A",
        "P209-B",
        "P209-C",
        "P209-D",
        "P209-E",
        "P209-F",
        "P209-G",
        "P209-H",
    ]
    assert "encryption_platform" in summary["forbidden_sibling_bc"]
    assert summary["eaas"]["enabled"] is True
    assert summary["signatures"]["verifiable"] is True
    assert summary["cursor_outputs"]["count"] == 20
