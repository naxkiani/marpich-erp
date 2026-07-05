"""Multi-Currency Treasury tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_investment_service,
    get_multi_currency_service,
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
    get_multi_currency_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "fx@treasury.dev", "password": "SecurePass123!", "display_name": "FX Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "fx@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict:
    treasury = get_treasury_service()
    investment = get_investment_service()
    fx = get_multi_currency_service()
    await treasury.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await investment.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await fx.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    accounts = (await treasury.list_accounts(slug)).unwrap()
    return {a["code"]: a for a in accounts}


@pytest.mark.asyncio
async def test_multi_currency_catalog(client):
    slug = "fxcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/multi-currency/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "currency_positions" in caps
    assert "currency_conversion" in caps
    assert "exchange_gain" in caps
    assert "exchange_loss" in caps
    assert "revaluation" in caps
    assert "cross_currency_transfer" in caps
    assert "central_bank" in caps
    assert "market" in caps
    assert "manual" in caps
    assert "historical" in caps
    assert "fx_reports" in caps
    assert "ai_fx_recommendations" in caps
    assert len(caps) == 12


@pytest.mark.asyncio
async def test_seed_rates_and_positions(client):
    slug = "fxseed"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    rates = await client.get("/api/v1/treasury/multi-currency/rates", headers=headers)
    assert rates.status_code == 200
    assert len(rates.json()["data"]) >= 15

    market = await client.get(
        "/api/v1/treasury/multi-currency/rates?rate_type=market", headers=headers
    )
    assert market.status_code == 200
    assert all(r["rate_type"] == "market" for r in market.json()["data"])

    positions = await client.get("/api/v1/treasury/multi-currency/positions", headers=headers)
    assert positions.status_code == 200
    pos = positions.json()["data"]
    currencies = {p["currency"] for p in pos["positions"]}
    assert "USD" in currencies
    assert "EUR" in currencies
    assert "GBP" in currencies


@pytest.mark.asyncio
async def test_currency_conversion(client):
    slug = "fxconv"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    conv = await client.post(
        "/api/v1/treasury/multi-currency/convert",
        headers=headers,
        json={"from_currency": "USD", "to_currency": "EUR", "amount": 1000},
    )
    assert conv.status_code == 201
    data = conv.json()["data"]
    assert data["transaction_type"] == "conversion"
    assert data["from_amount"] == 1000
    assert data["to_amount"] > 0


@pytest.mark.asyncio
async def test_cross_currency_transfer(client):
    slug = "fxxfer"
    headers = await _auth_headers(client, slug)
    accts = await _provision(slug)
    usd = accts["OPERATING-BANK"]
    eur = accts["EUR-OPERATING"]

    xfer = await client.post(
        "/api/v1/treasury/multi-currency/transfers",
        headers=headers,
        json={
            "from_account_id": usd["id"],
            "to_account_id": eur["id"],
            "amount": 5000,
        },
    )
    assert xfer.status_code == 201
    data = xfer.json()["data"]
    assert data["transaction_type"] == "cross_currency_transfer"
    assert data["from_currency"] == "USD"
    assert data["to_currency"] == "EUR"


@pytest.mark.asyncio
async def test_revaluation_exchange_gain_loss(client):
    slug = "fxreval"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    reval = await client.post(
        "/api/v1/treasury/multi-currency/revaluations",
        headers=headers,
        json={"currency": "EUR", "new_rate": 0.85},
    )
    assert reval.status_code == 201
    result = reval.json()["data"]
    assert "gain_loss" in result
    assert result["transaction"]["transaction_type"] in {"revaluation", "exchange_gain", "exchange_loss"}


@pytest.mark.asyncio
async def test_manual_rate_and_fx_report(client):
    slug = "fxreport"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    manual = await client.post(
        "/api/v1/treasury/multi-currency/rates",
        headers=headers,
        json={"quote_currency": "CHF", "rate": 0.88, "rate_type": "manual", "source": "treasury_desk"},
    )
    assert manual.status_code == 201
    assert manual.json()["data"]["rate_type"] == "manual"

    report = await client.get("/api/v1/treasury/multi-currency/report", headers=headers)
    assert report.status_code == 200
    rpt = report.json()["data"]
    assert "summary" in rpt
    assert "positions" in rpt
    assert rpt["summary"]["total_positions"] >= 3


@pytest.mark.asyncio
async def test_fx_dashboard(client):
    slug = "fxdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/treasury/multi-currency/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert "summary" in data
    assert "positions" in data
    assert "market_rates" in data


@pytest.mark.asyncio
async def test_ai_fx_recommendations(client):
    slug = "fxai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    ai = await client.post("/api/v1/treasury/multi-currency/ai/recommendations", headers=headers)
    assert ai.status_code == 200
    data = ai.json()["data"]
    assert "recommendations" in data
    assert data["autonomous_execution"] is False
