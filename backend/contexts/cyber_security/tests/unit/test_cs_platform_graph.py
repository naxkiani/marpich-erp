"""P210-K Cyber Security Knowledge Graph foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_graph_foundation import (
    validate_cs_graph_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_graph as graph

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_graph_foundation():
    result = validate_cs_graph_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-K"
    assert result["adr"] == 371
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_graph_catalog():
    cat = graph.catalog()
    assert cat["prompt_id"] == "P210-K"
    assert cat["adr"] == 371
    assert cat["semantic_relationships_required"] is True
    assert cat["attack_paths_calculable_required"] is True
    assert cat["digital_twins_living_required"] is True
    assert cat["simulation_capability_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "security_entities_lack_semantic_relationships"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/graph" in graph.graph_surface()["routes"]
    assert "GET /cyber-security/graph/readiness" in graph.graph_surface()["routes"]


@pytest.mark.unit
def test_cs_graph_acl():
    from contexts.cyber_security.infrastructure.acl import cs_graph_acl as acls

    assert acls.to_enterprise_ai(tenant_id="t1", reasoning_ref="r1")[
        "ai_reasoning_available_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="p1", action="read"
    )["graph_governance_required"] is True
    assert acls.to_ai_ops(tenant_id="t1", agent_ref="a1")[
        "via_p210_j_ai_ops"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_graph():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_graph"]["prompt_id"] == "P210-K"
    assert catalog["platform_graph"]["adr"] == 371
    summary = svc.platform_graph()
    assert summary["prompt_id"] == "P210-K"
    assert "P210-J" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
