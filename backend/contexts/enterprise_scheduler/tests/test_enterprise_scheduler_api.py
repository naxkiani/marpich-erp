"""Enterprise Scheduler — integration smoke tests."""
import pytest

from contexts.enterprise_scheduler.domain.aggregates.enterprise_scheduler_platform import SchedulerCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="sch-smoke",
        email="sch-smoke@enterprise.dev",
        display_name="Scheduler Smoke",
    )
    resp = await integration_client.get("/api/v1/enterprise-scheduler/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert SchedulerCapability.CRON_JOBS.value in caps
    assert len(caps) == 12


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_dashboard_and_trigger(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="sch-dash",
        email="sch-dash@enterprise.dev",
        display_name="Scheduler Dash",
    )
    seed = await integration_client.post("/api/v1/enterprise-scheduler/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["jobs"] == 5

    dashboard = await integration_client.get("/api/v1/enterprise-scheduler/dashboard", headers=headers)
    assert dashboard.status_code == 200
    dash = dashboard.json()["data"]
    assert dash["summary"]["jobs_total"] == 5

    jobs = await integration_client.get("/api/v1/enterprise-scheduler/jobs", headers=headers)
    job_ref = jobs.json()["data"][0]["job_ref"]
    trigger = await integration_client.post(f"/api/v1/enterprise-scheduler/jobs/{job_ref}/trigger", headers=headers)
    assert trigger.status_code == 200
    assert trigger.json()["data"]["execution"]["status"] == "succeeded"

    history = await integration_client.get("/api/v1/enterprise-scheduler/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()["data"]) >= 6

    monitoring = await integration_client.get("/api/v1/enterprise-scheduler/monitoring", headers=headers)
    assert monitoring.status_code == 200
    assert monitoring.json()["data"]["jobs_total"] == 5
