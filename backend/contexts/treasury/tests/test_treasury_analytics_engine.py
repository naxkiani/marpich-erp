"""Treasury Analytics tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_treasury_analytics_service,
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
    get_treasury_analytics_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "ana@treasury.dev", "password": "SecurePass123!", "display_name": "Ana Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "ana@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    await get_treasury_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})


@pytest.mark.asyncio
async def test_analytics_catalog(client):
    slug = "anacat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/analytics/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "cash_flow_analysis" in caps
    assert "liquidity_trends" in caps
    assert "treasury_kpis" in caps
    assert "bank_balance_analysis" in caps
    assert "forecast_accuracy" in caps
    assert "investment_performance" in caps
    assert "funding_analysis" in caps
    assert "currency_exposure" in caps
    assert "working_capital_kpis" in caps
    assert "executive_dashboard" in caps
    assert "cfo_dashboard" in caps
    assert "ai_treasury_assistant" in caps
    assert "liquidity_optimization" in caps
    assert "funding_strategy" in caps
    assert "cash_concentration" in caps
    assert "operational_efficiency" in caps
    assert len(caps) == 16


@pytest.mark.asyncio
async def test_analytics_dashboard_and_kpis(client):
    slug = "anadash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/treasury/analytics/dashboard", headers=headers)
    assert dash.status_code == 200
    assert "summary" in dash.json()["data"]
    assert dash.json()["data"]["summary"]["capability_count"] == 16

    kpis = await client.get("/api/v1/treasury/analytics/kpis", headers=headers)
    assert kpis.status_code == 200
    assert "kpis" in kpis.json()["data"]
    assert "total_cash" in kpis.json()["data"]["kpis"]


@pytest.mark.asyncio
async def test_cash_flow_and_liquidity_trends(client):
    slug = "anaflow"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    cash_flow = await client.get("/api/v1/treasury/analytics/cash-flow", headers=headers)
    assert cash_flow.status_code == 200
    assert "net_cash_flow_30d" in cash_flow.json()["data"]

    trends = await client.get("/api/v1/treasury/analytics/liquidity-trends", headers=headers)
    assert trends.status_code == 200
    assert "trend_direction" in trends.json()["data"]


@pytest.mark.asyncio
async def test_executive_and_cfo_dashboards(client):
    slug = "anaboards"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    exec_dash = await client.get("/api/v1/treasury/analytics/executive", headers=headers)
    assert exec_dash.status_code == 200
    assert exec_dash.json()["data"]["audience"] == "executive"
    assert "headline" in exec_dash.json()["data"]

    cfo_dash = await client.get("/api/v1/treasury/analytics/cfo", headers=headers)
    assert cfo_dash.status_code == 200
    assert cfo_dash.json()["data"]["audience"] == "cfo"
    assert "treasury_kpis" in cfo_dash.json()["data"]
    assert "bank_balance_analysis" in cfo_dash.json()["data"]


@pytest.mark.asyncio
async def test_bank_balances_and_working_capital(client):
    slug = "anabank"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    bank = await client.get("/api/v1/treasury/analytics/bank-balances", headers=headers)
    assert bank.status_code == 200
    assert "by_bank" in bank.json()["data"]

    wc = await client.get("/api/v1/treasury/analytics/working-capital", headers=headers)
    assert wc.status_code == 200
    assert "working_capital" in wc.json()["data"]


@pytest.mark.asyncio
async def test_funding_currency_forecast_investment(client):
    slug = "anafund"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    funding = await client.get("/api/v1/treasury/analytics/funding", headers=headers)
    assert funding.status_code == 200
    assert "funding_needs" in funding.json()["data"]

    fx = await client.get("/api/v1/treasury/analytics/currency-exposure", headers=headers)
    assert fx.status_code == 200
    assert "positions" in fx.json()["data"]

    forecast = await client.get("/api/v1/treasury/analytics/forecast-accuracy", headers=headers)
    assert forecast.status_code == 200
    assert "avg_forecast_accuracy_pct" in forecast.json()["data"]

    inv = await client.get("/api/v1/treasury/analytics/investment-performance", headers=headers)
    assert inv.status_code == 200
    assert "total_current_value" in inv.json()["data"]


@pytest.mark.asyncio
async def test_recommendations_and_ai_assistant(client):
    slug = "anaai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    recs = await client.get("/api/v1/treasury/analytics/recommendations", headers=headers)
    assert recs.status_code == 200
    data = recs.json()["data"]
    assert "recommendations" in data
    assert "liquidity_optimization" in data
    assert "funding_strategy" in data
    assert "cash_concentration" in data
    assert "operational_efficiency" in data
    assert data["autonomous_execution"] is False

    ai = await client.post("/api/v1/treasury/analytics/ai/assistant", headers=headers)
    assert ai.status_code == 200
    ai_data = ai.json()["data"]
    assert ai_data["assistant"] == "treasury_ai"
    assert "insights" in ai_data
    assert "top_recommendations" in ai_data
    assert ai_data["autonomous_execution"] is False
