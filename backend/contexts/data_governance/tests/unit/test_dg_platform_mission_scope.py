"""P212-B Data Governance mission/vision/scope foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_mission_foundation import (
    validate_dg_mission_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_mission_scope as mscope,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_mission_foundation():
    result = validate_dg_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-B"
    assert result["adr"] == 393
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_mission_catalog():
    cat = mscope.catalog()
    assert cat["prompt_id"] == "P212-B"
    assert cat["adr"] == 393
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["mission_defined_required"] is True
    assert cat["vision_defined_required"] is True
    assert cat["enterprise_scope_defined_required"] is True
    assert cat["strategic_objectives_present_required"] is True
    assert cat["operating_model_present_required"] is True
    assert cat["maturity_model_present_required"] is True
    assert cat["ai_governance_direction_present_required"] is True
    assert cat["meos_integration_alignment_present_required"] is True
    assert cat["domain_boundaries_clear_required"] is True
    assert cat["enterprise_governance_standard_compliant_required"] is True
    assert cat["strategic_objectives"]["count"] >= 6
    assert cat["maturity_model"]["level_count"] >= 5
    assert cat["cursor_outputs"]["count"] >= 15
    assert "mission_is_undefined" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/mission" in mscope.mission_surface()["routes"]
    assert (
        "GET /data-governance/mission/readiness"
        in mscope.mission_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_mission_acl():
    from contexts.data_governance.infrastructure.acl import (
        dg_mission_acl as acls,
    )

    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "encryption_out_of_scope"
    ] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["via_p208"] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")["via_p209"] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="sig1")[
        "via_p210"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_governance_direction_present_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission_scope():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_scope"]["prompt_id"] == "P212-B"
    assert catalog["platform_mission_scope"]["adr"] == 393
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_mission()
    assert summary["prompt_id"] == "P212-B"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-A" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.mission_readiness()["passed"] is True
