"""Enterprise Liquidity Engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_liquidity_service,
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
    get_liquidity_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "liq@treasury.dev", "password": "SecurePass123!", "display_name": "Liq Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "liq@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    await get_treasury_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await get_liquidity_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await get_treasury_service().create_forecast(
        tenant_id=slug,
        name="Q3 Forecast",
        period_start="2025-07-01",
        period_end="2025-09-30",
        scenario="base",
        currency="USD",
        opening_balance=55000,
        projected_lines=[
            {"date": "2025-07-15", "label": "Payroll", "outflow": 12000},
            {"date": "2025-07-20", "label": "Collections", "inflow": 18000},
            {"date": "2025-08-01", "label": "Rent", "outflow": 5000},
        ],
    )


@pytest.mark.asyncio
async def test_liquidity_catalog(client):
    slug = "liqcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/liquidity/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "cash_position" in caps
    assert "rolling_forecast" in caps
    assert "ai_liquidity_prediction" in caps
    assert "optimization_recommendations" in caps
    assert len(caps) == 12


@pytest.mark.asyncio
async def test_cash_position_and_periods(client):
    slug = "liqpos"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    pos = await client.get("/api/v1/treasury/liquidity/cash-position", headers=headers)
    assert pos.status_code == 200
    assert pos.json()["data"]["total_balance"] > 0

    daily = await client.get("/api/v1/treasury/liquidity/daily?days=14", headers=headers)
    assert daily.status_code == 200
    assert len(daily.json()["data"]["lines"]) == 14

    weekly = await client.get("/api/v1/treasury/liquidity/weekly?weeks=8", headers=headers)
    assert weekly.status_code == 200
    assert len(weekly.json()["data"]["lines"]) == 8

    monthly = await client.get("/api/v1/treasury/liquidity/monthly?months=6", headers=headers)
    assert monthly.status_code == 200
    assert len(monthly.json()["data"]["lines"]) == 6


@pytest.mark.asyncio
async def test_rolling_forecast_gap_working_capital(client):
    slug = "liqroll"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    rolling = await client.get("/api/v1/treasury/liquidity/rolling-forecast", headers=headers)
    assert rolling.status_code == 200
    assert rolling.json()["data"]["horizon_weeks"] == 13

    gap = await client.get("/api/v1/treasury/liquidity/gap", headers=headers)
    assert gap.status_code == 200
    assert "liquidity_gap" in gap.json()["data"]

    wc = await client.get("/api/v1/treasury/liquidity/working-capital", headers=headers)
    assert wc.status_code == 200
    assert "working_capital" in wc.json()["data"]


@pytest.mark.asyncio
async def test_cash_pools_and_funding_needs(client):
    slug = "liqpool"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    pools = await client.get("/api/v1/treasury/liquidity/pools", headers=headers)
    assert pools.status_code == 200
    assert pools.json()["data"]["pool_count"] >= 1

    need = await client.post(
        "/api/v1/treasury/liquidity/funding-needs",
        headers=headers,
        json={
            "label": "Payroll coverage",
            "required_amount": 15000,
            "available_amount": 10000,
            "due_date": "2025-07-15",
        },
    )
    assert need.status_code == 201
    assert need.json()["data"]["gap_amount"] == 5000

    funding = await client.get("/api/v1/treasury/liquidity/funding-needs", headers=headers)
    assert funding.status_code == 200
    assert funding.json()["data"]["total_funding_gap"] >= 5000


@pytest.mark.asyncio
async def test_liquidity_dashboard(client):
    slug = "liqdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/treasury/liquidity/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert "cash_position" in data
    assert "daily_liquidity" in data
    assert "weekly_liquidity" in data
    assert "monthly_liquidity" in data
    assert "rolling_forecast" in data
    assert "working_capital" in data
    assert data["summary"]["cash_position"] > 0


@pytest.mark.asyncio
async def test_ai_prediction_and_optimization(client):
    slug = "liqai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    predict = await client.post(
        "/api/v1/treasury/liquidity/ai/predict",
        headers=headers,
        json={"horizon_days": 30},
    )
    assert predict.status_code == 200
    pred = predict.json()["data"]
    assert "predictions" in pred
    assert pred["autonomous_execution"] is False
    assert "explanation" in pred

    opt = await client.get("/api/v1/treasury/liquidity/ai/optimization", headers=headers)
    assert opt.status_code == 200
    recs = opt.json()["data"]
    assert recs["explainable"] is True
    assert recs["autonomous_execution"] is False
    assert "recommendations" in recs
