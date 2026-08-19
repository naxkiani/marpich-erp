"""P355 server-side entitlement — no fake customers or payments."""
from datetime import UTC, datetime, timedelta

from contexts.feature_flags.application.product_entitlement import (
    resolve_edition_features,
    transition_allowed,
    validate_license,
)


def test_community_features_without_license():
    result = validate_license(tenant_id="t-a", feature_id="module.crm", license=None)
    assert result["status"] == "ENABLED"
    assert result["edition"] == "community"


def test_paid_feature_without_license_is_not_entitled():
    result = validate_license(tenant_id="t-a", feature_id="ai.platform", license=None)
    assert result["status"] == "NOT_ENTITLED"
    assert result["invalid_state"] == "BLOCKED"


def test_tenant_mismatch_blocked():
    license_doc = {
        "tenant_id": "t-a",
        "edition": "professional",
        "subscription_state": "ACTIVE",
        "application_version": "0.1.0",
        "schema_version": "055",
    }
    result = validate_license(tenant_id="t-b", feature_id="module.accounting", license=license_doc)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "tenant_mismatch"


def test_expired_license():
    license_doc = {
        "tenant_id": "t-a",
        "edition": "professional",
        "subscription_state": "ACTIVE",
        "application_version": "0.1.0",
        "schema_version": "055",
        "expires_at": (datetime.now(UTC) - timedelta(days=1)).isoformat(),
    }
    result = validate_license(tenant_id="t-a", feature_id="module.accounting", license=license_doc)
    assert result["status"] == "EXPIRED"
    assert result["invalid_state"] == "BLOCKED"


def test_trial_professional_accounting():
    license_doc = {
        "tenant_id": "t-a",
        "edition": "professional",
        "subscription_state": "TRIAL",
        "application_version": "0.1.0",
        "schema_version": "055",
    }
    result = validate_license(tenant_id="t-a", feature_id="module.accounting", license=license_doc)
    assert result["status"] == "TRIAL"


def test_edition_includes_lower_tiers():
    assert "module.crm" in resolve_edition_features("enterprise")
    assert "ai.platform" in resolve_edition_features("enterprise")
    assert "ai.platform" not in resolve_edition_features("community")


def test_subscription_transitions_explicit():
    assert transition_allowed("TRIAL", "ACTIVE") is True
    assert transition_allowed("EXPIRED", "ACTIVE") is False


def test_incompatible_schema_blocked():
    license_doc = {
        "tenant_id": "t-a",
        "edition": "community",
        "subscription_state": "NONE",
        "application_version": "0.1.0",
        "schema_version": "999",
    }
    result = validate_license(tenant_id="t-a", feature_id="module.crm", license=license_doc)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "version_not_allowed"
