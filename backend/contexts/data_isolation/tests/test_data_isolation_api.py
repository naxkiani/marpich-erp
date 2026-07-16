"""Data isolation — integration smoke tests."""
import pytest

from contexts.data_isolation.domain.aggregates.data_isolation_platform import IsolationCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="iso-smoke",
        email="iso-smoke@enterprise.dev",
        display_name="Isolation Smoke",
    )
    resp = await integration_client.get("/api/v1/data-isolation/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert IsolationCapability.PRINCIPAL_REGISTRY.value in caps
    assert len(caps) == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_sync_and_verify_principals(integration_client):
    tenant = "iso-flow"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="iso-flow@enterprise.dev",
        display_name="Isolation Flow",
    )
    seed = await integration_client.post("/api/v1/data-isolation/seed", headers=headers)
    assert seed.status_code == 200
    assert seed.json()["data"]["seeded"] is True

    sync = await integration_client.post("/api/v1/data-isolation/principals/sync", headers=headers)
    assert sync.status_code == 200
    assert sync.json()["data"]["created"] >= 1

    principals = await integration_client.get("/api/v1/data-isolation/principals", headers=headers)
    assert principals.status_code == 200
    assert len(principals.json()["data"]) >= 1

    partitions = await integration_client.get("/api/v1/data-isolation/partitions", headers=headers)
    assert partitions.status_code == 200
    assert partitions.json()["data"]["principals_total"] >= 1

    verify = await integration_client.post("/api/v1/data-isolation/verify", headers=headers)
    assert verify.status_code == 200
    assert verify.json()["data"]["passed"] is True

    dashboard = await integration_client.get("/api/v1/data-isolation/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["summary"]["principals"] >= 1
