"""Identity risk — integration smoke tests."""
import pytest

from contexts.identity_risk.domain.aggregates.identity_risk_platform import IdentityRiskCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="risk-smoke",
        email="risk-smoke@enterprise.dev",
        display_name="Risk Smoke",
    )
    resp = await integration_client.get("/api/v1/identity-risk/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert IdentityRiskCapability.ANOMALY_DETECTION.value in caps
    assert len(caps) == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_evaluate_authentication_and_directory_risk(integration_client):
    tenant = "risk-flow"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="risk-flow@enterprise.dev",
        display_name="Risk Flow",
    )
    await integration_client.post("/api/v1/identity-risk/seed", headers=headers)

    auth_eval = await integration_client.post(
        "/api/v1/identity-risk/evaluate",
        headers=headers,
        json={
            "event_type": "authentication",
            "payload": {
                "user_id": "user-123",
                "auth_method": "saml",
                "is_new_user": True,
            },
        },
    )
    assert auth_eval.status_code == 200
    auth_score = auth_eval.json()["data"]
    assert auth_score["score"] >= 35
    assert auth_score["explainable"] is True

    sync_eval = await integration_client.post(
        "/api/v1/identity-risk/evaluate",
        headers=headers,
        json={
            "event_type": "directory_sync",
            "payload": {
                "users_synced": 100,
                "users_created": 25,
                "source_type": "ldap",
            },
        },
    )
    assert sync_eval.status_code == 200
    sync_score = sync_eval.json()["data"]
    assert sync_score["score"] >= 50
    assert sync_score["risk_level"] in {"medium", "high", "critical"}

    scores = await integration_client.get("/api/v1/identity-risk/scores", headers=headers)
    assert scores.status_code == 200
    assert len(scores.json()["data"]) >= 2

    alerts = await integration_client.get("/api/v1/identity-risk/alerts", headers=headers)
    assert alerts.status_code == 200
    assert len(alerts.json()["data"]) >= 1

    dashboard = await integration_client.get("/api/v1/identity-risk/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["summary"]["risk_scores"] >= 2


@pytest.mark.integration
@pytest.mark.asyncio
async def test_event_driven_scim_risk_scoring(integration_client):
    from shared.infrastructure.messaging.event_bus import publish_integration_event
    from shared.domain.value_objects.tenant_id import TenantId
    from contexts.directory.domain.events.directory_integration_events import ScimUserProvisionedIntegration

    tenant = "risk-scim"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="risk-scim@enterprise.dev",
        display_name="Risk SCIM",
    )
    await integration_client.post("/api/v1/identity-risk/seed", headers=headers)

    await publish_integration_event(
        ScimUserProvisionedIntegration(
            tenant_id=TenantId(tenant),
            correlation_id="risk-scim-corr",
            user_id="scim-user-001",
            email="provisioned@enterprise.dev",
            provider_ref="scim-risk-scim-0001",
        )
    )

    scores = await integration_client.get("/api/v1/identity-risk/scores", headers=headers)
    assert scores.status_code == 200
    assert len(scores.json()["data"]) >= 1
