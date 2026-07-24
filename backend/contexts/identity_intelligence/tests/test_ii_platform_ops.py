"""P207-N DevSecOps & Observability foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_ops_foundation import (
    validate_ii_ops_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_ops as ops,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_ops_foundation():
    result = validate_ii_ops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-N"
    assert result["adr"] == 329
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_ops_catalog():
    cat = ops.catalog()
    assert cat["prompt_id"] == "P207-N"
    assert cat["adr"] == 329
    assert cat["sor"] == "identity_intelligence"
    assert cat["automated_deployment_required"] is True
    assert cat["capabilities"]["not_manual_deployment"] is True
    assert cat["high_availability"]["availability_target"] == "99.99%"
    assert "deployment_manual" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/ops" in ops.ops_surface()["routes"]
    assert (
        "GET /identity-intelligence/ops/readiness"
        in ops.ops_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ops():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ops"]["prompt_id"] == "P207-N"
    assert catalog["platform_ops"]["adr"] == 329
    assert catalog["platform_ops"]["automated_deployment_required"] is True
    assert catalog["platform_ops"]["observability_complete_required"] is True
    assert catalog["delegation"]["manual_deployment"] is False

    summary = svc.platform_ops()
    assert summary["prompt_id"] == "P207-N"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-D",
        "P207-E",
        "P207-F",
        "P207-G",
        "P207-H",
        "P207-I",
        "P207-J",
        "P207-K",
        "P207-L",
        "P207-M",
    ]
    assert summary["kubernetes_platform"]["namespace_count"] == 7
    assert summary["disaster_recovery"]["rpo"] == "15m"
