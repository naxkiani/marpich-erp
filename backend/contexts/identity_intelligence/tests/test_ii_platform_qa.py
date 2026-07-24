"""P207-O QA, Governance & DoD foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_qa_foundation import (
    validate_ii_qa_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_qa as qa,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_qa_foundation():
    result = validate_ii_qa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-O"
    assert result["adr"] == 330
    assert result["sor"] == "identity_intelligence"
    assert result["certification_complete"] is True
    assert result["p207_series_complete"] is True
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_qa_catalog():
    cat = qa.catalog()
    assert cat["prompt_id"] == "P207-O"
    assert cat["adr"] == 330
    assert cat["sor"] == "identity_intelligence"
    assert cat["certification_complete"] is True
    assert cat["p207_series_complete"] is True
    assert cat["definition_of_done"]["p207_completion_gate"] is True
    assert "testing_manual_only" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/qa" in qa.qa_surface()["routes"]
    assert (
        "GET /identity-intelligence/qa/readiness"
        in qa.qa_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qa():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_qa"]["prompt_id"] == "P207-O"
    assert catalog["platform_qa"]["adr"] == 330
    assert catalog["platform_qa"]["certification_complete"] is True
    assert catalog["platform_qa"]["p207_series_complete"] is True
    assert catalog["delegation"]["manual_only_testing"] is False

    summary = svc.platform_qa()
    assert summary["prompt_id"] == "P207-O"
    assert len(summary["builds_on"]) == 14
    assert summary["definition_of_done"]["count"] == 7
    assert summary["p207_series_complete"] is True
