"""Enterprise Integration Studio — integration smoke tests."""
import pytest

from contexts.enterprise_integration_studio.domain.aggregates.enterprise_integration_studio_platform import StudioCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="eis-smoke",
        email="eis-smoke@enterprise.dev",
        display_name="Integration Studio Smoke",
    )
    resp = await integration_client.get("/api/v1/enterprise-integration-studio/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert StudioCapability.VISUAL_API_BUILDER.value in caps
    assert len(caps) == 14


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_dashboard_portals_and_lifecycle(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="eis-dash",
        email="eis-dash@enterprise.dev",
        display_name="Integration Studio Dash",
    )
    seed = await integration_client.post("/api/v1/enterprise-integration-studio/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["projects"] == 2
    assert body["artifacts"] == 6

    dashboard = await integration_client.get("/api/v1/enterprise-integration-studio/dashboard", headers=headers)
    assert dashboard.status_code == 200
    dash = dashboard.json()["data"]
    assert dash["summary"]["artifacts"] == 6

    portal = await integration_client.get("/api/v1/enterprise-integration-studio/developer-portal", headers=headers)
    assert portal.status_code == 200
    assert portal.json()["data"]["title"] == "Marpich Integration Developer Portal"

    citizen = await integration_client.get("/api/v1/enterprise-integration-studio/citizen-workspace", headers=headers)
    assert citizen.status_code == 200
    assert citizen.json()["data"]["no_code"] is True

    artifacts = await integration_client.get("/api/v1/enterprise-integration-studio/artifacts", headers=headers)
    artifact_ref = artifacts.json()["data"][0]["artifact_ref"]

    test = await integration_client.post(
        f"/api/v1/enterprise-integration-studio/artifacts/{artifact_ref}/test",
        headers=headers,
        json={"use_mock": True},
    )
    assert test.status_code == 200
    assert test.json()["data"]["result"]["status"] == "passed"

    publish = await integration_client.post(
        f"/api/v1/enterprise-integration-studio/artifacts/{artifact_ref}/publish",
        headers=headers,
    )
    assert publish.status_code == 200

    deploy = await integration_client.post(
        f"/api/v1/enterprise-integration-studio/artifacts/{artifact_ref}/deploy",
        headers=headers,
        json={"environment": "sandbox"},
    )
    assert deploy.status_code == 200
    assert deploy.json()["data"]["status"] == "live"

    marketplace = await integration_client.get("/api/v1/enterprise-integration-studio/marketplace", headers=headers)
    assert marketplace.status_code == 200
    assert len(marketplace.json()["data"]) == 3
