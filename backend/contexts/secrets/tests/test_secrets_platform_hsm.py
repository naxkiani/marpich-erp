"""P209-K Secrets HSM / AI Crypto / PQC foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_hsm_foundation import (
    validate_secrets_hsm_foundation,
)
from contexts.secrets.domain.services import secrets_platform_hsm as hsm

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_hsm_foundation():
    result = validate_secrets_hsm_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-K"
    assert result["adr"] == 356
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_hsm_catalog():
    cat = hsm.catalog()
    assert cat["prompt_id"] == "P209-K"
    assert cat["adr"] == 356
    assert cat["sor"] == "secrets"
    assert cat["cryptographic_agility_required"] is True
    assert cat["hsm_protection_required"] is True
    assert cat["ai_crypto_decisions_auditable_required"] is True
    assert cat["confidential_attestation_required"] is True
    assert cat["pqc_migration_strategy_required"] is True
    assert cat["hardware_trust_validated_required"] is True
    assert cat["cryptographic_risks_measurable_required"] is True
    assert cat["cqrs"]["event_count"] >= 12
    assert "hsm_protection_is_absent" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/hsm" in hsm.hsm_surface()["routes"]
    assert "GET /secrets/hsm/readiness" in hsm.hsm_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_hsm():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_hsm"]["prompt_id"] == "P209-K"
    assert catalog["platform_hsm"]["adr"] == 356
    assert catalog["platform_hsm"]["hsm_protection_required"] is True
    assert catalog["platform_hsm"]["pqc_migration_strategy_required"] is True

    summary = svc.platform_hsm()
    assert summary["prompt_id"] == "P209-K"
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
        "P209-J",
    ]
    assert "hsm_platform" in summary["forbidden_sibling_bc"]
    assert summary["hsm"]["fips_140_3"] is True
    assert summary["pqc"]["migration_strategy_defined"] is True
    assert summary["cursor_outputs"]["count"] == 20
