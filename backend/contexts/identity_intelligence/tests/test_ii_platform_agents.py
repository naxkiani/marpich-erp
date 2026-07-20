"""P207-E Identity AI Agent Platform foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_agent_foundation import (
    validate_ii_agent_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_agents as agents,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_agent_foundation():
    result = validate_ii_agent_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-E"
    assert result["adr"] == 320
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_agent_catalog():
    cat = agents.catalog()
    assert cat["prompt_id"] == "P207-E"
    assert cat["adr"] == 320
    assert cat["sor"] == "identity_intelligence"
    assert cat["capabilities"]["not_permissionless"] is True
    assert cat["agent_catalog"]["count"] == 6
    assert cat["tools"]["not_unscoped"] is True
    assert cat["rag"]["not_uncontrolled"] is True
    assert "agents_without_permissions" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/agents" in agents.agents_surface()["routes"]
    assert (
        "GET /identity-intelligence/agents/readiness"
        in agents.agents_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_agents():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_agents"]["prompt_id"] == "P207-E"
    assert catalog["platform_agents"]["adr"] == 320
    assert catalog["platform_agents"]["agent_permissions_required"] is True
    assert catalog["delegation"]["permissionless_agents"] is False

    summary = svc.platform_agents()
    assert summary["prompt_id"] == "P207-E"
    assert summary["builds_on"] == ["P207-A", "P207-B", "P207-C", "P207-D"]
    assert summary["microservices"]["deployable_today"] == "identity_intelligence"
