"""P211-B Data Security mission/vision/scope foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_mission_foundation import (
    validate_ds_mission_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_mission_scope as mscope,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_mission_foundation():
    result = validate_ds_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-B"
    assert result["adr"] == 377
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_mission_catalog():
    cat = mscope.catalog()
    assert cat["prompt_id"] == "P211-B"
    assert cat["adr"] == 377
    assert cat["data_security_scope_defined_required"] is True
    assert cat["ownership_model_required"] is True
    assert cat["privacy_responsibilities_clear_required"] is True
    assert cat["data_protection_principles_present_required"] is True
    assert cat["integration_boundaries_defined_required"] is True
    assert cat["governance_model_complete_required"] is True
    assert cat["strategic_objectives"]["count"] >= 6
    assert cat["enterprise_scope"]["asset_type_count"] >= 20
    assert cat["principles"]["count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 15
    assert "data_security_scope_is_undefined" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/mission" in mscope.mission_surface()["routes"]
    assert "GET /data-security/mission/readiness" in mscope.mission_surface()["routes"]


@pytest.mark.unit
def test_ds_mission_acl():
    from contexts.data_security.infrastructure.acl import ds_mission_acl as acls

    assert acls.to_consent(tenant_id="t1", subject_ref="s1")[
        "privacy_responsibilities_clear_required"
    ] is True
    assert acls.to_governance_board(tenant_id="t1", board_ref="b1")[
        "governance_model_complete_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["zero_trust_data_access"] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="sig1")[
        "via_p210"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission_scope():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_scope"]["prompt_id"] == "P211-B"
    assert catalog["platform_mission_scope"]["adr"] == 377
    summary = svc.platform_mission_scope()
    assert summary["prompt_id"] == "P211-B"
    assert "P211-A" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
