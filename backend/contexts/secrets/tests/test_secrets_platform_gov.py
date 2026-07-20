"""P209-M Secrets AI Security / Governance / Compliance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_gov_foundation import (
    validate_secrets_gov_foundation,
)
from contexts.secrets.domain.services import secrets_platform_gov as gov

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_gov_foundation():
    result = validate_secrets_gov_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-M"
    assert result["adr"] == 358
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_gov_catalog():
    cat = gov.catalog()
    assert cat["prompt_id"] == "P209-M"
    assert cat["adr"] == 358
    assert cat["sor"] == "secrets"
    assert cat["ai_decisions_explainable_required"] is True
    assert cat["crypto_policies_managed_required"] is True
    assert cat["compliance_evidence_automated_required"] is True
    assert cat["risks_measurable_required"] is True
    assert cat["governance_ownership_defined_required"] is True
    assert cat["audit_trails_complete_required"] is True
    assert cat["remediation_automatable_required"] is True
    assert cat["cqrs"]["event_count"] >= 14
    assert "ai_security_decisions_not_explainable" in cat["quality_gates"][
        "reject_if"
    ]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/gov" in gov.gov_surface()["routes"]
    assert "GET /secrets/gov/readiness" in gov.gov_surface()["routes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_gov():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_gov"]["prompt_id"] == "P209-M"
    assert catalog["platform_gov"]["adr"] == 358
    assert catalog["platform_gov"]["ai_decisions_explainable_required"] is True
    assert catalog["platform_gov"]["crypto_policies_managed_required"] is True

    summary = svc.platform_gov()
    assert summary["prompt_id"] == "P209-M"
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
    ]
    assert "governance_platform" in summary["forbidden_sibling_bc"]
    assert summary["compliance_automation"]["evidence_automated"] is True
    assert summary["responsible_ai"]["explainability"] is True
    assert summary["cursor_outputs"]["count"] == 20
