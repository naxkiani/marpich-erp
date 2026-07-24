"""P209-F Secrets KMS foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_kms_foundation import (
    validate_secrets_kms_foundation,
)
from contexts.secrets.domain.services import secrets_platform_kms as kms

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_kms_foundation():
    result = validate_secrets_kms_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-F"
    assert result["adr"] == 351
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_kms_catalog():
    cat = kms.catalog()
    assert cat["prompt_id"] == "P209-F"
    assert cat["adr"] == 351
    assert cat["sor"] == "secrets"
    assert cat["keys_stored_without_protection_forbidden"] is True
    assert cat["hsm_capability_required"] is True
    assert cat["key_lifecycle_complete_required"] is True
    assert cat["key_ownership_known_required"] is True
    assert cat["rotation_automatic_required"] is True
    assert cat["key_operations_audited_required"] is True
    assert cat["cryptographic_policies_required"] is True
    assert cat["lifecycle"]["stage_count"] >= 11
    assert cat["cqrs"]["event_count"] >= 12
    assert "keys_stored_without_protection" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/kms" in kms.kms_surface()["routes"]
    assert "GET /secrets/kms/readiness" in kms.kms_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_kms():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_kms"]["prompt_id"] == "P209-F"
    assert catalog["platform_kms"]["adr"] == 351
    assert catalog["platform_kms"]["keys_stored_without_protection_forbidden"] is True
    assert catalog["platform_kms"]["hsm_capability_required"] is True

    summary = svc.platform_kms()
    assert summary["prompt_id"] == "P209-F"
    assert summary["builds_on"] == [
        "P209",
        "P209-A",
        "P209-B",
        "P209-C",
        "P209-D",
        "P209-E",
    ]
    assert summary["forbidden_sibling_bc"] == "kms_platform"
    assert summary["hsm"]["available"] is True
    assert summary["lifecycle"]["automatic_rotation"] is True
    assert summary["cursor_outputs"]["count"] == 20
