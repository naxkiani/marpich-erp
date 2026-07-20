"""P209-B Secrets Mission / Vision / Scope foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.secrets.container import get_secrets_service, reset_secrets_service
from contexts.secrets.domain.services.secrets_mission_foundation import (
    validate_secrets_mission_foundation,
)
from contexts.secrets.domain.services import (
    secrets_platform_mission_scope as mscope,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_secrets_service()
    yield
    reset_secrets_service()


@pytest.mark.unit
def test_secrets_mission_foundation():
    result = validate_secrets_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P209-B"
    assert result["adr"] == 347
    assert result["sor"] == "secrets"
    assert result["forbidden_sibling_present"] is False
    assert result["catalog"] is True
    assert result["aggregates"] is True
    assert result["acl"] is True
    assert result["router"] is True


@pytest.mark.unit
def test_secrets_mission_catalog():
    cat = mscope.catalog()
    assert cat["prompt_id"] == "P209-B"
    assert cat["adr"] == 347
    assert cat["sor"] == "secrets"
    assert cat["mission_vision_required"] is True
    assert cat["enterprise_scope_required"] is True
    assert cat["boundaries_clear_required"] is True
    assert cat["does_not_own_business_authorization"] is True
    assert cat["does_not_replace_peer_sors"] is True
    assert cat["strategic_objectives"]["count"] == 5
    assert cat["evolution_roadmap"]["count"] == 7
    assert cat["cursor_outputs"]["count"] == 15
    assert "mission_vision_absent" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /secrets/mission" in mscope.mission_surface()["routes"]
    assert (
        "GET /secrets/mission/readiness" in mscope.mission_surface()["routes"]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission_scope():
    svc = get_secrets_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_scope"]["prompt_id"] == "P209-B"
    assert catalog["platform_mission_scope"]["adr"] == 347
    assert catalog["platform_mission_scope"]["mission_vision_required"] is True
    assert catalog["delegation"]["owns_business_authorization"] is False
    assert catalog["delegation"]["replaces_peer_sors"] is False

    summary = svc.platform_mission_scope()
    assert summary["prompt_id"] == "P209-B"
    assert summary["builds_on"] == ["P209", "P209-A"]
    assert summary["boundaries"]["does_not_own_count"] == 5
    assert summary["meos_integrations"]["count"] == 8
    assert "vault" in summary["forbidden_sibling_bc"]
