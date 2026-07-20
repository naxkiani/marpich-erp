"""P209-N Secrets Deploy / DevSecOps / K8s / Observability foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_deploy_foundation import (
    validate_secrets_deploy_foundation,
)
from contexts.secrets.domain.services import secrets_platform_deploy as deploy

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_deploy_foundation():
    result = validate_secrets_deploy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-N"
    assert result["adr"] == 359
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_deploy_catalog():
    cat = deploy.catalog()
    assert cat["prompt_id"] == "P209-N"
    assert cat["adr"] == 359
    assert cat["sor"] == "secrets"
    assert cat["deployment_automated_required"] is True
    assert cat["kubernetes_security_complete_required"] is True
    assert cat["observability_present_required"] is True
    assert cat["cicd_security_validation_required"] is True
    assert cat["scaling_strategy_defined_required"] is True
    assert cat["disaster_recovery_available_required"] is True
    assert cat["infrastructure_changes_managed_required"] is True
    assert cat["cqrs"]["event_count"] >= 16
    assert "deployment_is_manual" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/deploy" in deploy.deploy_surface()["routes"]
    assert "GET /secrets/deploy/readiness" in deploy.deploy_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_deploy():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_deploy"]["prompt_id"] == "P209-N"
    assert catalog["platform_deploy"]["adr"] == 359
    assert catalog["platform_deploy"]["deployment_automated_required"] is True
    assert catalog["platform_deploy"]["observability_present_required"] is True

    summary = svc.platform_deploy()
    assert summary["prompt_id"] == "P209-N"
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
        "P209-L",
        "P209-M",
    ]
    assert "deploy_platform" in summary["forbidden_sibling_bc"]
    assert summary["kubernetes"]["security_complete"] is True
    assert summary["disaster_recovery"]["available"] is True
    assert summary["cursor_outputs"]["count"] == 20
