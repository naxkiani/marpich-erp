"""P213-P BI qa foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.analytics.application.bi_qa_foundation import validate_bi_qa_foundation
from contexts.analytics.container import get_analytics_service, reset_analytics_service
from contexts.analytics.domain.services import bi_platform_qa as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_qa_foundation():
    result = validate_bi_qa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-P"
    assert result["adr"] == 420


@pytest.mark.unit
def test_bi_qa_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-P"
    assert cat["adr"] == 420
    assert cat["sor"] == "analytics"
    assert cat["architecture"]["capability_count"] >= 5
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qa():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_qa"]["prompt_id"] == "P213-P"
    assert catalog["platform_qa"]["adr"] == 420
    assert getattr(svc, "qa_readiness")()["passed"] is True
