"""P210-B Cyber Security mission/vision/scope foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_mission_foundation import (
    validate_cs_mission_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import (
    cs_platform_mission_scope as mscope,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_mission_foundation():
    result = validate_cs_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-B"
    assert result["adr"] == 362
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_mission_catalog():
    cat = mscope.catalog()
    assert cat["prompt_id"] == "P210-B"
    assert cat["adr"] == 362
    assert cat["mission_measurable_required"] is True
    assert cat["vision_enterprise_scale_required"] is True
    assert cat["enterprise_scope"]["count"] >= 20
    assert cat["security_domains"]["count"] >= 15
    assert cat["cursor_outputs"]["count"] >= 20
    assert "mission_not_measurable" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/mission" in mscope.mission_surface()["routes"]
    assert "GET /cyber-security/mission/readiness" in mscope.mission_surface()["routes"]


@pytest.mark.unit
def test_cs_mission_acl():
    from contexts.cyber_security.infrastructure.acl import cs_mission_acl as acls

    assert acls.to_security_incident(tenant_id="t1", mission_ref="m1")[
        "ir_lifecycle_owned_by_security_incident"
    ] is True
    assert acls.to_ai_platform(tenant_id="t1", surface_ref="s1")[
        "ai_security_required"
    ] is True
    assert acls.to_strategy_plane(tenant_id="t1")["via_p210_a_strategy"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission_scope():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_scope"]["prompt_id"] == "P210-B"
    assert catalog["platform_mission_scope"]["adr"] == 362
    summary = svc.platform_mission_scope()
    assert summary["prompt_id"] == "P210-B"
    assert summary["builds_on"] == ["P210-A", "ADR-361"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
