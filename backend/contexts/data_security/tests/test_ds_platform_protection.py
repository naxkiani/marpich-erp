"""P211-J Data Security protection foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_protection_foundation import (
    validate_ds_protection_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_protection as prot,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_protection_foundation():
    result = validate_ds_protection_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-J"
    assert result["adr"] == 385
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_protection_catalog():
    cat = prot.catalog()
    assert cat["prompt_id"] == "P211-J"
    assert cat["adr"] == 385
    assert cat["sensitive_data_protected_required"] is True
    assert cat["encryption_policies_defined_required"] is True
    assert cat["token_lifecycle_present_required"] is True
    assert cat["key_integration_available_required"] is True
    assert cat["protection_decisions_auditable_required"] is True
    assert cat["privacy_controls_complete_required"] is True
    assert cat["keys_remain_p209_secrets"] is True
    assert cat["key_integration"]["kms_owner"] == "secrets"
    assert cat["architecture"]["layer_count"] >= 7
    assert cat["domain"]["context_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 16
    assert "sensitive_data_can_exist_unprotected" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/protection" in prot.protection_surface()["routes"]
    assert (
        "GET /data-security/protection/readiness"
        in prot.protection_surface()["routes"]
    )


@pytest.mark.unit
def test_ds_protection_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_protection_acl as acls,
    )

    assert acls.to_secrets(tenant_id="t1", key_ref="k1")[
        "module_local_kms_forbidden"
    ] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")["kms_owner"] == "secrets"
    assert acls.to_classification(tenant_id="t1", asset_ref="a1")[
        "encryption_policies_defined_required"
    ] is True
    assert acls.to_privacy(tenant_id="t1", control_ref="c1")[
        "privacy_controls_complete_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="decrypt"
    )["protection_decisions_auditable_required"] is True
    assert acls.to_workflow(tenant_id="t1", approval_ref="ap1")[
        "token_lifecycle_present_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_protection():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_protection"]["prompt_id"] == "P211-J"
    assert catalog["platform_protection"]["adr"] == 385
    summary = svc.platform_protection()
    assert summary["prompt_id"] == "P211-J"
    assert "P211-I" in summary["builds_on"]
    assert summary["keys_remain_p209_secrets"] is True
    assert summary["context_count"] >= 7
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
