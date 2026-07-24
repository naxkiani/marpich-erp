"""P209-O Secrets Testing / Governance / Security Validation / DoD tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_qa_foundation import (
    validate_secrets_qa_foundation,
)
from contexts.secrets.domain.services import secrets_platform_qa as qa

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_qa_foundation():
    result = validate_secrets_qa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-O"
    assert result["adr"] == 360
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_qa_catalog():
    cat = qa.catalog()
    assert cat["prompt_id"] == "P209-O"
    assert cat["adr"] == 360
    assert cat["sor"] == "secrets"
    assert cat["security_testing_complete_required"] is True
    assert cat["compliance_evidence_available_required"] is True
    assert cat["cryptographic_controls_validated_required"] is True
    assert cat["production_readiness_defined_required"] is True
    assert cat["governance_ownership_present_required"] is True
    assert cat["audit_trails_complete_required"] is True
    assert cat["security_failures_block_deployment_required"] is True
    assert cat["cqrs"]["event_count"] >= 14
    assert "security_testing_incomplete" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/qa" in qa.qa_surface()["routes"]
    assert "GET /secrets/qa/readiness" in qa.qa_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qa():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_qa"]["prompt_id"] == "P209-O"
    assert catalog["platform_qa"]["adr"] == 360
    assert catalog["platform_qa"]["security_testing_complete_required"] is True
    assert catalog["platform_qa"][
        "security_failures_block_deployment_required"
    ] is True

    summary = svc.platform_qa()
    assert summary["prompt_id"] == "P209-O"
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
        "P209-N",
    ]
    assert "qa_platform" in summary["forbidden_sibling_bc"]
    assert summary["definition_of_done"]["enterprise_dod"] is True
    assert summary["devsecops_validation"][
        "security_failures_block_deployment"
    ] is True
    assert summary["cursor_outputs"]["count"] == 20
