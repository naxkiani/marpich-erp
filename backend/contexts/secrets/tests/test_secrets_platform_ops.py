"""P209-L Secrets CQRS / Events / APIs / Microservices foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_ops_foundation import (
    validate_secrets_ops_foundation,
)
from contexts.secrets.domain.services import secrets_platform_ops as ops

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_ops_foundation():
    result = validate_secrets_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-L"
    assert result["adr"] == 357
    assert result["sor"] == "secrets"
    assert result["series_status"] == "complete"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_ops_catalog():
    cat = ops.catalog()
    assert cat["prompt_id"] == "P209-L"
    assert cat["adr"] == 357
    assert cat["sor"] == "secrets"
    assert cat["no_shared_databases_required"] is True
    assert cat["events_present_required"] is True
    assert cat["api_security_required"] is True
    assert cat["crypto_operations_auditable_required"] is True
    assert cat["microservice_ownership_clear_required"] is True
    assert cat["observability_complete_required"] is True
    assert cat["deployment_scalable_required"] is True
    assert cat["series_closeout"] is True
    assert cat["cqrs"]["event_count"] >= 26
    assert cat["cqrs"]["command_count"] >= 18
    assert "services_share_databases" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/ops" in ops.ops_surface()["routes"]
    assert "GET /secrets/ops/readiness" in ops.ops_surface()["routes"]
    assert len(cat["microservice_map"]["logical_services"]) == 12


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ops():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ops"]["prompt_id"] == "P209-L"
    assert catalog["platform_ops"]["adr"] == 357
    assert catalog["platform_ops"]["no_shared_databases_required"] is True
    assert catalog["platform_ops"]["events_present_required"] is True

    summary = svc.platform_ops()
    assert summary["prompt_id"] == "P209-L"
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
        "P209-K",
    ]
    assert "ops_platform" in summary["forbidden_sibling_bc"]
    assert summary["data_architecture"]["no_shared_databases"] is True
    assert summary["observability"]["complete"] is True
    assert summary["cursor_outputs"]["count"] == 20
    assert summary["series_closeout"] is True
