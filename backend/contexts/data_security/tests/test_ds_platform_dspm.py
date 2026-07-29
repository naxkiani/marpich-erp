"""P211-F Data Security DSPM foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_dspm_foundation import (
    validate_ds_dspm_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_dspm as dspm,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_dspm_foundation():
    result = validate_ds_dspm_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-F"
    assert result["adr"] == 381
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_dspm_catalog():
    cat = dspm.catalog()
    assert cat["prompt_id"] == "P211-F"
    assert cat["adr"] == 381
    assert cat["data_assets_known_required"] is True
    assert cat["security_posture_measurable_required"] is True
    assert cat["exposure_risks_visible_required"] is True
    assert cat["findings_owned_required"] is True
    assert cat["remediation_not_manual_only_required"] is True
    assert cat["continuous_assessment_available_required"] is True
    assert cat["architecture"]["layer_count"] >= 7
    assert cat["architecture"]["scope_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 14
    assert "data_assets_are_unknown" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/dspm" in dspm.dspm_surface()["routes"]
    assert "GET /data-security/dspm/readiness" in dspm.dspm_surface()["routes"]


@pytest.mark.unit
def test_ds_dspm_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_dspm_acl as acls,
    )

    assert acls.to_discovery(tenant_id="t1", asset_ref="a1")[
        "data_assets_known_required"
    ] is True
    assert acls.to_classification(tenant_id="t1", asset_ref="a1")[
        "via_p211_e_classification"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "security_posture_measurable_required"
    ] is True
    assert acls.to_workflow_remediation(tenant_id="t1", remediation_ref="r1")[
        "remediation_not_manual_only_required"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="s1")[
        "continuous_assessment_available_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_dspm():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_dspm"]["prompt_id"] == "P211-F"
    assert catalog["platform_dspm"]["adr"] == 381
    summary = svc.platform_dspm()
    assert summary["prompt_id"] == "P211-F"
    assert "P211-E" in summary["builds_on"]
    assert summary["scope_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
