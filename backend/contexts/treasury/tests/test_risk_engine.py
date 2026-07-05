"""Enterprise Treasury Risk Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_investment_service,
    get_risk_service,
    get_treasury_service,
    reset_treasury_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_treasury_service()
    get_investment_service()
    get_risk_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "risk@treasury.dev", "password": "SecurePass123!", "display_name": "Risk Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "risk@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    treasury = get_treasury_service()
    investment = get_investment_service()
    risk = get_risk_service()
    await treasury.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await investment.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await risk.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})


@pytest.mark.asyncio
async def test_risk_catalog(client):
    slug = "riskcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/risk/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "liquidity_risk" in caps
    assert "interest_rate_risk" in caps
    assert "foreign_exchange_risk" in caps
    assert "counterparty_risk" in caps
    assert "operational_risk" in caps
    assert "limit_management" in caps
    assert "exposure_monitoring" in caps
    assert "stress_testing" in caps
    assert "risk_alerts" in caps
    assert "risk_dashboard" in caps
    assert "ai_risk_scoring" in caps
    assert len(caps) == 11


@pytest.mark.asyncio
async def test_seed_risk_limits(client):
    slug = "riskseed"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    limits = await client.get("/api/v1/treasury/risk/limits", headers=headers)
    assert limits.status_code == 200
    types = {l["risk_type"] for l in limits.json()["data"]}
    assert "liquidity_risk" in types
    assert "interest_rate_risk" in types
    assert "foreign_exchange_risk" in types
    assert "counterparty_risk" in types
    assert "operational_risk" in types
    assert len(limits.json()["data"]) == 5


@pytest.mark.asyncio
async def test_exposure_monitoring_and_dashboard(client):
    slug = "riskdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    exposures = await client.get("/api/v1/treasury/risk/exposures", headers=headers)
    assert exposures.status_code == 200
    data = exposures.json()["data"]
    assert "liquidity_risk" in data["exposures"]
    assert "interest_rate_risk" in data["exposures"]
    assert "foreign_exchange_risk" in data["exposures"]

    dash = await client.get("/api/v1/treasury/risk/dashboard", headers=headers)
    assert dash.status_code == 200
    d = dash.json()["data"]
    assert "summary" in d
    assert "exposures" in d
    assert "composite_risk_score" in d["summary"] or "risk_level" in d["summary"]


@pytest.mark.asyncio
async def test_limit_breach_generates_alert(client):
    slug = "riskalert"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    limits = await client.get("/api/v1/treasury/risk/limits", headers=headers)
    liq_limit = next(l for l in limits.json()["data"] if l["risk_type"] == "liquidity_risk")

    update = await client.patch(
        f"/api/v1/treasury/risk/limits/{liq_limit['id']}",
        headers=headers,
        json={"threshold_value": 99},
    )
    assert update.status_code == 200

    alerts = await client.get("/api/v1/treasury/risk/alerts", headers=headers)
    assert alerts.status_code == 200
    open_alerts = [a for a in alerts.json()["data"] if a["status"] == "open"]
    assert len(open_alerts) >= 1
    assert open_alerts[0]["risk_type"] == "liquidity_risk"


@pytest.mark.asyncio
async def test_stress_testing(client):
    slug = "riskstress"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    scenarios = await client.get("/api/v1/treasury/risk/scenarios", headers=headers)
    assert scenarios.status_code == 200
    assert len(scenarios.json()["data"]) == 5

    run = await client.post(
        "/api/v1/treasury/risk/stress-tests",
        headers=headers,
        json={"scenario": "liquidity_shock"},
    )
    assert run.status_code == 201
    result = run.json()["data"]
    assert result["scenario"] == "liquidity_shock"
    assert "results" in result
    assert "impact_score" in result

    history = await client.get("/api/v1/treasury/risk/stress-tests", headers=headers)
    assert history.status_code == 200
    assert len(history.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_alert_acknowledge_and_resolve(client):
    slug = "riskresolve"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    limits = await client.get("/api/v1/treasury/risk/limits", headers=headers)
    liq_limit = next(l for l in limits.json()["data"] if l["risk_type"] == "counterparty_risk")
    await client.patch(
        f"/api/v1/treasury/risk/limits/{liq_limit['id']}",
        headers=headers,
        json={"threshold_value": 1},
    )

    alerts = await client.get("/api/v1/treasury/risk/alerts", headers=headers)
    alert_id = alerts.json()["data"][0]["id"]

    ack = await client.post(
        f"/api/v1/treasury/risk/alerts/{alert_id}/acknowledge",
        headers=headers,
    )
    assert ack.status_code == 200
    assert ack.json()["data"]["status"] == "acknowledged"

    resolve = await client.post(
        f"/api/v1/treasury/risk/alerts/{alert_id}/resolve",
        headers=headers,
    )
    assert resolve.status_code == 200
    assert resolve.json()["data"]["status"] == "resolved"


@pytest.mark.asyncio
async def test_create_custom_limit(client):
    slug = "risklimit"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/risk/limits",
        headers=headers,
        json={
            "risk_type": "operational_risk",
            "name": "Custom Ops Limit",
            "threshold_value": 5,
            "threshold_unit": "count",
        },
    )
    assert create.status_code == 201
    assert create.json()["data"]["name"] == "Custom Ops Limit"


@pytest.mark.asyncio
async def test_ai_risk_scoring(client):
    slug = "riskai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    ai = await client.post("/api/v1/treasury/risk/ai/scoring", headers=headers)
    assert ai.status_code == 200
    data = ai.json()["data"]
    assert "composite_score" in data
    assert "recommendations" in data
    assert data["autonomous_execution"] is False
    assert all(r.get("autonomous_execution") is False for r in data["recommendations"])
