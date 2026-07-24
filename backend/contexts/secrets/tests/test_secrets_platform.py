"""P209 Secrets Cryptographic Trust foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_foundation import (
    validate_secrets_foundation,
)
from contexts.secrets.domain.services import secrets_platform as plat

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_foundation():
    result = validate_secrets_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209"
    assert result["adr"] == 345
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True
    assert result["registry"] is True
    assert result["startup"] is True


@pytest.mark.unit
def test_secrets_catalog():
    cat = plat.catalog()
    assert cat["prompt_id"] == "P209"
    assert cat["adr"] == 345
    assert cat["sor"] == "secrets"
    assert cat["plaintext_secrets_forbidden"] is True
    assert cat["ungoverned_keys_forbidden"] is True
    assert cat["manual_certificate_management_forbidden"] is True
    assert cat["hsm_integration_required"] is True
    assert cat["cryptographic_agility_required"] is True
    assert cat["verifiable_workload_identity_required"] is True
    assert cat["auditable_trust_required"] is True
    assert cat["pam_orchestrates_refs_only"] is True
    assert cat["domains"]["count"] >= 12
    assert cat["cqrs"]["event_count"] >= 12
    assert "secrets_stored_in_plaintext" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets" in plat.secrets_surface()["routes"]
    assert "GET /secrets/readiness" in plat.secrets_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_crypto_trust():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_crypto_trust"]["prompt_id"] == "P209"
    assert catalog["platform_crypto_trust"]["adr"] == 345
    assert catalog["platform_crypto_trust"]["plaintext_secrets_forbidden"] is True
    assert catalog["delegation"]["plaintext_secrets"] is False
    assert catalog["delegation"]["pam_holds_ciphertext"] is False

    summary = svc.platform_crypto_trust()
    assert summary["prompt_id"] == "P209"
    assert summary["sor"] == "secrets"
    assert summary["cursor_outputs"]["count"] == 20
    assert summary["hsm"]["required"] is True
    assert "vault" in summary["forbidden_sibling_bc"]
