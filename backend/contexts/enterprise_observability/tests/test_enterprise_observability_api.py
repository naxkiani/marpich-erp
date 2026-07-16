"""Enterprise Observability — integration smoke tests."""
import pytest

from contexts.enterprise_observability.domain.aggregates.enterprise_observability_platform import ObservabilityCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="obs-smoke",
        email="obs-smoke@enterprise.dev",
        display_name="OBS Smoke",
    )
    resp = await integration_client.get("/api/v1/enterprise-observability/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert ObservabilityCapability.DISTRIBUTED_TRACING.value in caps
    assert ObservabilityCapability.INCIDENT_MANAGEMENT.value in caps
    assert len(caps) == 14


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_and_operational_dashboard(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="obs-dash",
        email="obs-dash@enterprise.dev",
        display_name="OBS Dash",
    )
    seed = await integration_client.post("/api/v1/enterprise-observability/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["metrics"] >= 10

    dashboard = await integration_client.get("/api/v1/enterprise-observability/operational-dashboard", headers=headers)
    assert dashboard.status_code == 200
    dash = dashboard.json()["data"]
    assert dash["dashboard_id"] == "platform.system-health"
    assert dash["summary"]["metrics_captured"] >= 10

    graph = await integration_client.get("/api/v1/enterprise-observability/service-dependency-graph", headers=headers)
    assert graph.status_code == 200
    assert graph.json()["data"]["total_services"] >= 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_monitoring_endpoints(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="obs-mon",
        email="obs-mon@enterprise.dev",
        display_name="OBS Mon",
    )
    await integration_client.post("/api/v1/enterprise-observability/seed", headers=headers)

    for path in (
        "/api/v1/enterprise-observability/traces",
        "/api/v1/enterprise-observability/logs",
        "/api/v1/enterprise-observability/metrics",
        "/api/v1/enterprise-observability/health-checks",
        "/api/v1/enterprise-observability/business-kpis",
        "/api/v1/enterprise-observability/events",
        "/api/v1/enterprise-observability/queues",
        "/api/v1/enterprise-observability/api-monitoring",
        "/api/v1/enterprise-observability/workflows",
        "/api/v1/enterprise-observability/ai-monitoring",
        "/api/v1/enterprise-observability/alerts",
    ):
        resp = await integration_client.get(path, headers=headers)
        assert resp.status_code == 200, path


@pytest.mark.integration
@pytest.mark.asyncio
async def test_incident_lifecycle(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="obs-inc",
        email="obs-inc@enterprise.dev",
        display_name="OBS Inc",
    )
    create = await integration_client.post(
        "/api/v1/enterprise-observability/incidents",
        headers=headers,
        json={
            "title": "High queue lag",
            "severity": "critical",
            "source_signal": "queue",
            "summary": "Outbox lag exceeded threshold",
        },
    )
    assert create.status_code == 200
    incident_ref = create.json()["data"]["incident_ref"]

    resolve = await integration_client.post(
        f"/api/v1/enterprise-observability/incidents/{incident_ref}/resolve",
        headers=headers,
        json={"resolution_summary": "Scaled outbox workers"},
    )
    assert resolve.status_code == 200
    assert resolve.json()["data"]["status"] == "resolved"
