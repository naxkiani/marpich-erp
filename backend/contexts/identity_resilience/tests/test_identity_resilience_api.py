"""Identity resilience — integration smoke tests."""
from datetime import UTC, datetime, timedelta

import pytest

from contexts.identity_resilience.domain.aggregates.identity_resilience_platform import ResilienceCapability
from contexts.identity_resilience.infrastructure.persistence.identity_resilience_memory_store import (
    InMemoryIdentityResilienceStore,
)
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="res-smoke",
        email="res-smoke@enterprise.dev",
        display_name="Resilience Smoke",
    )
    resp = await integration_client.get("/api/v1/identity-resilience/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert ResilienceCapability.LEADER_ELECTION.value in caps
    assert len(caps) == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_deploy_workers_and_failover(integration_client):
    tenant = "res-failover"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="res-failover@enterprise.dev",
        display_name="Resilience Failover",
    )
    seed = await integration_client.post("/api/v1/identity-resilience/seed", headers=headers)
    assert seed.status_code == 200

    regions = await integration_client.get("/api/v1/identity-resilience/regions", headers=headers)
    assert regions.status_code == 200
    region_list = regions.json()["data"]
    assert len(region_list) >= 2
    primary = next(r for r in region_list if r["is_primary"])
    standby = next(r for r in region_list if not r["is_primary"])

    leader = await integration_client.post(
        "/api/v1/identity-resilience/workers",
        headers=headers,
        json={"worker_type": "directory_sync", "region_id": primary["region_id"], "role": "leader"},
    )
    assert leader.status_code == 200
    leader_ref = leader.json()["data"]["worker_ref"]

    standby_worker = await integration_client.post(
        "/api/v1/identity-resilience/workers",
        headers=headers,
        json={"worker_type": "directory_sync", "region_id": standby["region_id"], "role": "standby"},
    )
    assert standby_worker.status_code == 200

    failover = await integration_client.post(
        "/api/v1/identity-resilience/failover",
        headers=headers,
        json={"worker_type": "directory_sync", "reason": "manual_failover"},
    )
    assert failover.status_code == 200
    data = failover.json()["data"]
    assert data["new_leader"]["role"] == "leader"
    assert data["new_leader"]["region_id"] == standby["region_id"]

    failovers = await integration_client.get("/api/v1/identity-resilience/failovers", headers=headers)
    assert failovers.status_code == 200
    assert len(failovers.json()["data"]) >= 1

    dashboard = await integration_client.get("/api/v1/identity-resilience/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["summary"]["workers"] >= 2


@pytest.mark.integration
@pytest.mark.asyncio
async def test_replication_health_and_directory_sync_ha(integration_client):
    tenant = "res-sync"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="res-sync@enterprise.dev",
        display_name="Resilience Sync",
    )
    await integration_client.post("/api/v1/identity-resilience/seed", headers=headers)

    regions = await integration_client.get("/api/v1/identity-resilience/regions", headers=headers)
    primary = next(r for r in regions.json()["data"] if r["is_primary"])

    deploy = await integration_client.post(
        "/api/v1/identity-resilience/workers",
        headers=headers,
        json={"worker_type": "directory_sync", "region_id": primary["region_id"], "role": "leader"},
    )
    assert deploy.status_code == 200

    replication = await integration_client.get("/api/v1/identity-resilience/replication", headers=headers)
    assert replication.status_code == 200
    assert len(replication.json()["data"]["regions"]) >= 2

    sync = await integration_client.post("/api/v1/identity-resilience/workers/directory-sync/run", headers=headers)
    assert sync.status_code == 200
    assert sync.json()["data"]["delegated"] is True
