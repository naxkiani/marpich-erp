"""P207-B Identity Intelligence Mission / Vision / Scope foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_intelligence.container import (
    get_identity_intelligence_service,
    reset_identity_intelligence_service,
)
from contexts.identity_intelligence.domain.services.ii_mission_foundation import (
    validate_ii_mission_foundation,
)
from contexts.identity_intelligence.domain.services import (
    ii_platform_mission_scope as mscope,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_intelligence_service()
    yield
    reset_identity_intelligence_service()


@pytest.mark.unit
def test_ii_mission_foundation():
    result = validate_ii_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P207-B"
    assert result["adr"] == 317
    assert result["sor"] == "identity_intelligence"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_ii_mission_catalog():
    cat = mscope.catalog()
    assert cat["prompt_id"] == "P207-B"
    assert cat["adr"] == 317
    assert cat["sor"] == "identity_intelligence"
    assert cat["mission"]["not_absent"] is True
    assert cat["vision"]["not_absent"] is True
    assert cat["enterprise_scope"]["not_replacing_peers"] is True
    assert cat["strategic_objectives"]["category_count"] == 4
    assert "mission_vision_absent" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /identity-intelligence/mission" in mscope.mission_surface()["routes"]
    assert (
        "GET /identity-intelligence/mission/readiness"
        in mscope.mission_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_identity_intelligence_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_scope"]["prompt_id"] == "P207-B"
    assert catalog["platform_mission_scope"]["adr"] == 317
    assert catalog["platform_mission_scope"]["does_not_replace_peers"] is True
    assert catalog["delegation"]["replaces_peer_sors"] is False

    summary = svc.platform_mission_scope()
    assert summary["prompt_id"] == "P207-B"
    assert summary["builds_on"] == ["P207-A"]
    assert summary["meos_placement"]["intelligence_layer"] is True
