"""Authorization PDP — integration smoke tests."""
import pytest

from contexts.authorization.domain.aggregates.authorization_platform import AuthorizationCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="authz-smoke",
        email="authz-smoke@enterprise.dev",
        display_name="Authorization Smoke",
    )
    resp = await integration_client.get("/api/v1/authorization/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert AuthorizationCapability.RBAC_EVALUATION.value in caps
    assert len(caps) == 8


@pytest.mark.integration
@pytest.mark.asyncio
async def test_check_allow_and_deny(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="authz-check",
        email="authz-check@enterprise.dev",
        display_name="Authorization Check",
    )
    await integration_client.post("/api/v1/authorization/seed", headers=headers)

    allow = await integration_client.post(
        "/api/v1/authorization/check",
        headers=headers,
        json={
            "resource": "marpich://identity/users/me",
            "action": "read",
            "permission_code": "identity.users.read",
            "context": {"device_trust": "high"},
        },
    )
    assert allow.status_code == 200
    assert allow.json()["data"]["decision"] == "allow"

    deny = await integration_client.post(
        "/api/v1/authorization/check",
        headers=headers,
        json={
            "resource": "marpich://banking/accounts/acc-1",
            "action": "transfer.initiate",
            "context": {"hour_utc": 3, "device_trust": "low"},
        },
    )
    assert deny.status_code == 200
    assert deny.json()["data"]["decision"] == "deny"

    decisions = await integration_client.get("/api/v1/authorization/decisions", headers=headers)
    assert decisions.status_code == 200
    assert len(decisions.json()["data"]) >= 2

    simulate = await integration_client.post(
        "/api/v1/authorization/simulate",
        headers=headers,
        json={
            "permission_code": "identity.users.read",
            "context": {},
        },
    )
    assert simulate.status_code == 200
    assert simulate.json()["data"]["simulated"] is True
