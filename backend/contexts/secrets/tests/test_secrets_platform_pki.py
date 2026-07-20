"""P209-D Secrets PKI foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_pki_foundation import (
    validate_secrets_pki_foundation,
)
from contexts.secrets.domain.services import secrets_platform_pki as pki

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_pki_foundation():
    result = validate_secrets_pki_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-D"
    assert result["adr"] == 349
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_pki_catalog():
    cat = pki.catalog()
    assert cat["prompt_id"] == "P209-D"
    assert cat["adr"] == 349
    assert cat["sor"] == "secrets"
    assert cat["root_ca_keys_protected_required"] is True
    assert cat["certificates_auto_managed_required"] is True
    assert cat["certificate_lifecycle_complete_required"] is True
    assert cat["revocation_mechanisms_required"] is True
    assert cat["trust_chain_validation_required"] is True
    assert cat["certificate_ownership_known_required"] is True
    assert cat["audit_evidence_required"] is True
    assert cat["lifecycle"]["stage_count"] >= 12
    assert cat["cqrs"]["event_count"] >= 12
    assert "root_ca_keys_not_protected" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/pki" in pki.pki_surface()["routes"]
    assert "GET /secrets/pki/readiness" in pki.pki_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_pki():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_pki"]["prompt_id"] == "P209-D"
    assert catalog["platform_pki"]["adr"] == 349
    assert catalog["platform_pki"]["root_ca_keys_protected_required"] is True
    assert catalog["platform_pki"]["revocation_mechanisms_required"] is True

    summary = svc.platform_pki()
    assert summary["prompt_id"] == "P209-D"
    assert summary["builds_on"] == ["P209", "P209-A", "P209-B", "P209-C"]
    assert summary["forbidden_sibling_bc"] == "pki_platform"
    assert summary["root_ca"]["hsm_required"] is True
    assert summary["revocation"]["ocsp"] is True
    assert summary["cursor_outputs"]["count"] == 20
