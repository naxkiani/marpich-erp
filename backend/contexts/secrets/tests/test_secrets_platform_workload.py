"""P209-H Secrets Workload Identity foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_workload_foundation import (
    validate_secrets_workload_foundation,
)
from contexts.secrets.domain.services import secrets_platform_workload as wl

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_workload_foundation():
    result = validate_secrets_workload_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-H"
    assert result["adr"] == 353
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_workload_catalog():
    cat = wl.catalog()
    assert cat["prompt_id"] == "P209-H"
    assert cat["adr"] == 353
    assert cat["sor"] == "secrets"
    assert cat["cryptographic_workload_identity_required"] is True
    assert cat["static_credentials_forbidden"] is True
    assert cat["mtls_enforceable_required"] is True
    assert cat["certificate_rotation_automatic_required"] is True
    assert cat["trust_domains_defined_required"] is True
    assert cat["workload_identity_ownership_known_required"] is True
    assert cat["service_communication_audited_required"] is True
    assert cat["lifecycle"]["stage_count"] >= 9
    assert cat["cqrs"]["event_count"] >= 12
    assert (
        "workloads_lack_cryptographic_identity"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/workload" in wl.workload_surface()["routes"]
    assert "GET /secrets/workload/readiness" in wl.workload_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_workload():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_workload"]["prompt_id"] == "P209-H"
    assert catalog["platform_workload"]["adr"] == 353
    assert (
        catalog["platform_workload"][
            "cryptographic_workload_identity_required"
        ]
        is True
    )
    assert catalog["platform_workload"]["mtls_enforceable_required"] is True

    summary = svc.platform_workload()
    assert summary["prompt_id"] == "P209-H"
    assert summary["builds_on"] == [
        "P209",
        "P209-A",
        "P209-B",
        "P209-C",
        "P209-D",
        "P209-E",
        "P209-F",
        "P209-G",
    ]
    assert "spiffe_platform" in summary["forbidden_sibling_bc"]
    assert summary["mtls"]["enforceable"] is True
    assert summary["spiffe"]["svid"] is True
    assert summary["cursor_outputs"]["count"] == 20
