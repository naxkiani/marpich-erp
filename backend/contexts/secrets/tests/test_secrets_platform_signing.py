"""P209-J Secrets Signing / Supply Chain foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_signing_foundation import (
    validate_secrets_signing_foundation,
)
from contexts.secrets.domain.services import secrets_platform_signing as signing

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_signing_foundation():
    result = validate_secrets_signing_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-J"
    assert result["adr"] == 355
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_signing_catalog():
    cat = signing.catalog()
    assert cat["prompt_id"] == "P209-J"
    assert cat["adr"] == 355
    assert cat["sor"] == "secrets"
    assert cat["unsigned_artifacts_forbidden"] is True
    assert cat["signing_keys_managed_required"] is True
    assert cat["supply_chain_provenance_required"] is True
    assert cat["sbom_verification_required"] is True
    assert cat["deployment_trust_validatable_required"] is True
    assert cat["artifact_ownership_known_required"] is True
    assert cat["signature_operations_audited_required"] is True
    assert cat["cqrs"]["event_count"] >= 12
    assert (
        "software_artifacts_are_unsigned" in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/signing" in signing.signing_surface()["routes"]
    assert (
        "GET /secrets/signing/readiness" in signing.signing_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_signing():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_signing"]["prompt_id"] == "P209-J"
    assert catalog["platform_signing"]["adr"] == 355
    assert catalog["platform_signing"]["unsigned_artifacts_forbidden"] is True
    assert catalog["platform_signing"]["sbom_verification_required"] is True

    summary = svc.platform_signing()
    assert summary["prompt_id"] == "P209-J"
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
        "P209-I",
    ]
    assert "code_signing_platform" in summary["forbidden_sibling_bc"]
    assert summary["sbom"]["verification_required"] is True
    assert summary["attestation"]["slsa"] is True
    assert summary["cursor_outputs"]["count"] == 20
