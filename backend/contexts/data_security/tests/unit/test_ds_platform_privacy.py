"""P211-I Data Security privacy intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_privacy_foundation import (
    validate_ds_privacy_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_privacy as privacy,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_privacy_foundation():
    result = validate_ds_privacy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-I"
    assert result["adr"] == 384
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_privacy_catalog():
    cat = privacy.catalog()
    assert cat["prompt_id"] == "P211-I"
    assert cat["adr"] == 384
    assert cat["personal_data_discoverable_required"] is True
    assert cat["consent_trackable_required"] is True
    assert cat["privacy_risks_measurable_required"] is True
    assert cat["processing_visible_required"] is True
    assert cat["regulatory_obligations_mapped_required"] is True
    assert cat["ai_privacy_risks_managed_required"] is True
    assert cat["consent_ledger_remains_consent"] is True
    assert cat["consent"]["ledger_owner"] == "consent"
    assert cat["architecture"]["layer_count"] >= 7
    assert cat["domain"]["context_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 16
    assert "personal_data_cannot_be_discovered" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/privacy" in privacy.privacy_surface()["routes"]
    assert "GET /data-security/privacy/readiness" in privacy.privacy_surface()["routes"]


@pytest.mark.unit
def test_ds_privacy_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_privacy_acl as acls,
    )

    assert acls.to_consent(tenant_id="t1", consent_ref="c1")[
        "absorb_consent_ledger_forbidden"
    ] is True
    assert acls.to_consent(tenant_id="t1", consent_ref="c1")[
        "ledger_owner"
    ] == "consent"
    assert acls.to_discovery(tenant_id="t1", asset_ref="a1")[
        "personal_data_discoverable_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_privacy_risks_managed_required"
    ] is True
    assert acls.to_compliance(tenant_id="t1", obligation_ref="o1")[
        "regulatory_obligations_mapped_required"
    ] is True
    assert acls.to_access(tenant_id="t1", entitlement_ref="e1")[
        "via_p211_h_access"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_privacy():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_privacy"]["prompt_id"] == "P211-I"
    assert catalog["platform_privacy"]["adr"] == 384
    summary = svc.platform_privacy()
    assert summary["prompt_id"] == "P211-I"
    assert "P211-H" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["consent_ledger_remains_consent"] is True
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
