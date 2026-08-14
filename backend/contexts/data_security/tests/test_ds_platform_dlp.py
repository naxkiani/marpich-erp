"""P211-G Data Security DLP foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_dlp_foundation import (
    validate_ds_dlp_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_dlp as dlp,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_dlp_foundation():
    result = validate_ds_dlp_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-G"
    assert result["adr"] == 382
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_dlp_catalog():
    cat = dlp.catalog()
    assert cat["prompt_id"] == "P211-G"
    assert cat["adr"] == 382
    assert cat["sensitive_data_identifiable_required"] is True
    assert cat["data_movement_monitored_required"] is True
    assert cat["policies_enforceable_required"] is True
    assert cat["ai_leakage_managed_required"] is True
    assert cat["insider_risk_visible_required"] is True
    assert cat["violations_investigable_required"] is True
    assert cat["automated_response_available_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["channels"]["channel_count"] >= 5
    assert cat["cursor_outputs"]["count"] >= 18
    assert "sensitive_data_cannot_be_identified" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/dlp" in dlp.dlp_surface()["routes"]
    assert "GET /data-security/dlp/readiness" in dlp.dlp_surface()["routes"]


@pytest.mark.unit
def test_ds_dlp_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_dlp_acl as acls,
    )

    assert acls.to_classification(tenant_id="t1", asset_ref="a1")[
        "sensitive_data_identifiable_required"
    ] is True
    assert acls.to_dspm(tenant_id="t1", posture_ref="p1")[
        "via_p211_f_dspm"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_leakage_managed_required"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="pol1")[
        "policies_enforceable_required"
    ] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "insider_risk_visible_required"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="s1")[
        "automated_response_available_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_dlp():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_dlp"]["prompt_id"] == "P211-G"
    assert catalog["platform_dlp"]["adr"] == 382
    summary = svc.platform_dlp()
    assert summary["prompt_id"] == "P211-G"
    assert "P211-F" in summary["builds_on"]
    assert summary["channel_count"] >= 5
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
