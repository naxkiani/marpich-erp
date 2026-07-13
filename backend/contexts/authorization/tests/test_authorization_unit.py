"""Authorization PDP — unit tests."""
import pytest

from contexts.authorization.domain.aggregates.authorization_platform import AuthorizationCapability
from contexts.authorization.domain.services import authorization_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_eight_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert AuthorizationCapability.RBAC_EVALUATION.value in caps
    assert AuthorizationCapability.PBAC_EVALUATION.value in caps
    assert len(caps) == 8


@pytest.mark.unit
def test_resolve_permission_code_from_resource_uri():
    code = engine.resolve_permission_code(
        permission_code=None,
        resource="marpich://banking/accounts/acc-1",
        action="transfer.initiate",
    )
    assert code == "banking.accounts.transfer.initiate"


@pytest.mark.unit
def test_evaluate_rbac_admin_wildcard():
    allowed, reasons = engine.evaluate_rbac(permissions=["*"], required="banking.accounts.read")
    assert allowed is True
    assert reasons[0].startswith("rbac.permission")


@pytest.mark.unit
def test_evaluate_access_denies_missing_rbac():
    result = engine.evaluate_access(
        profile={"rbac_enabled": True, "abac_enabled": False, "pbac_enabled": False},
        permissions=["identity.users.read"],
        abac_policies=[],
        permission_code="banking.accounts.read",
        resource="marpich://banking/accounts/x",
        action="read",
        facts={},
    )
    assert result["decision"] == "deny"
    assert "rbac.missing" in result["reason_codes"][0]


@pytest.mark.unit
def test_abac_deny_outside_business_hours():
    policies = [{
        "policy_ref": "POL-1",
        "effect": "deny",
        "permission_pattern": "banking.*",
        "conditions": [{"attribute": "hour_utc", "operator": "lt", "value": 8}],
        "active": True,
        "priority": 10,
    }]
    effect, reasons, _ = engine.evaluate_abac(
        policies=policies,
        permission_code="banking.accounts.read",
        facts={"hour_utc": 3},
    )
    assert effect == "deny"
    assert reasons[0].startswith("abac.deny")
