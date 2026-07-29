"""P211-H Data Security access governance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_access_foundation import (
    validate_ds_access_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_access as access,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_access_foundation():
    result = validate_ds_access_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-H"
    assert result["adr"] == 383
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_access_catalog():
    cat = access.catalog()
    assert cat["prompt_id"] == "P211-H"
    assert cat["adr"] == 383
    assert cat["permissions_visible_required"] is True
    assert cat["ownership_defined_required"] is True
    assert cat["access_reviews_not_manual_only_required"] is True
    assert cat["risk_evaluation_present_required"] is True
    assert cat["ai_access_managed_required"] is True
    assert cat["least_privilege_enforceable_required"] is True
    assert cat["authorization_decisions_auditable_required"] is True
    assert cat["architecture"]["layer_count"] >= 7
    assert cat["entitlements"]["scope_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 17
    assert "data_permissions_are_invisible" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/access" in access.access_surface()["routes"]
    assert "GET /data-security/access/readiness" in access.access_surface()["routes"]


@pytest.mark.unit
def test_ds_access_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_access_acl as acls,
    )

    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["module_local_pdp_forbidden"] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["least_privilege_enforceable_required"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_access_managed_required"
    ] is True
    assert acls.to_workflow_review(tenant_id="t1", review_ref="r1")[
        "access_reviews_not_manual_only_required"
    ] is True
    assert acls.to_dlp(tenant_id="t1", policy_ref="d1")[
        "via_p211_g_dlp"
    ] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "ownership_defined_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_access():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_access"]["prompt_id"] == "P211-H"
    assert catalog["platform_access"]["adr"] == 383
    summary = svc.platform_access()
    assert summary["prompt_id"] == "P211-H"
    assert "P211-G" in summary["builds_on"]
    assert summary["scope_count"] >= 8
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
