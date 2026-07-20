"""P207-K Knowledge Graph Intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_graph_foundation import (
    validate_ii_graph_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_graph as graph,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_graph_foundation():
    result = validate_ii_graph_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-K"
    assert result["adr"] == 326
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_graph_catalog():
    cat = graph.catalog()
    assert cat["prompt_id"] == "P207-K"
    assert cat["adr"] == 326
    assert cat["sor"] == "identity_intelligence"
    assert cat["graph_storage_peer"] == "directory"
    assert cat["not_data_only"] is True
    assert cat["reasoning_required"] is True
    assert cat["capabilities"]["does_not_own_graph_sor"] is True
    assert "graph_only_data_without_reasoning" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/graph" in graph.graph_surface()["routes"]
    assert (
        "GET /identity-intelligence/graph/readiness"
        in graph.graph_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_graph():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_graph"]["prompt_id"] == "P207-K"
    assert catalog["platform_graph"]["adr"] == 326
    assert catalog["platform_graph"]["not_data_only"] is True
    assert catalog["platform_graph"]["reasoning_required"] is True
    assert catalog["platform_graph"]["graph_storage_peer"] == "directory"
    assert catalog["delegation"]["graph_data_only"] is False

    summary = svc.platform_graph()
    assert summary["prompt_id"] == "P207-K"
    assert summary["builds_on"] == [
        "P207-A",
        "P207-B",
        "P207-C",
        "P207-E",
        "P207-F",
        "P207-G",
        "P207-H",
        "P207-J",
    ]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
    assert summary["graph_storage_peer"] == "directory"
