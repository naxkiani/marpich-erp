"""Enterprise Investment Management tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_investment_service,
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
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "invest@treasury.dev", "password": "SecurePass123!", "display_name": "Invest Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "invest@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict[str, dict]:
    treasury = get_treasury_service()
    investments = get_investment_service()
    await treasury.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await investments.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    accounts = (await treasury.list_accounts(slug)).unwrap()
    invs = (await investments.list_investments(slug)).unwrap()
    return {"accounts": {a["code"]: a for a in accounts}, "investments": invs}


@pytest.mark.asyncio
async def test_investment_catalog(client):
    slug = "investcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/investments/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "fixed_deposit" in caps
    assert "bonds" in caps
    assert "government_securities" in caps
    assert "mutual_funds" in caps
    assert "investment_portfolio" in caps
    assert "investment_income" in caps
    assert "interest_accrual" in caps
    assert "maturity_tracking" in caps
    assert "risk_rating" in caps
    assert "portfolio_performance" in caps
    assert "investment_dashboard" in caps
    assert "ai_investment_analysis" in caps
    assert len(caps) == 12


@pytest.mark.asyncio
async def test_seed_investments_all_types(client):
    slug = "investseed"
    data = await _provision(slug)
    types = {i["investment_type"] for i in data["investments"]}
    assert "fixed_deposit" in types
    assert "bonds" in types
    assert "government_securities" in types
    assert "mutual_funds" in types
    assert len(data["investments"]) == 4


@pytest.mark.asyncio
async def test_create_investment_and_dashboard(client):
    slug = "investdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/investments",
        headers=headers,
        json={
            "portfolio_name": "Liquidity Reserve",
            "investment_type": "fixed_deposit",
            "name": "12-Month FD",
            "instrument_code": "FD-12M-NEW",
            "principal_amount": 50000,
            "currency": "USD",
            "interest_rate": 5.0,
            "purchase_date": "2025-07-01",
            "maturity_date": "2026-07-01",
        },
    )
    assert create.status_code == 201

    dash = await client.get("/api/v1/treasury/investments/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert data["summary"]["total_investments"] >= 5
    assert "performance" in data
    assert "maturity_tracking" in data
    assert "risk_ratings" in data


@pytest.mark.asyncio
async def test_interest_accrual_and_income(client):
    slug = "investinc"
    headers = await _auth_headers(client, slug)
    data = await _provision(slug)
    fd = next(i for i in data["investments"] if i["investment_type"] == "fixed_deposit")
    inv_id = fd["id"]

    accrue = await client.post(
        f"/api/v1/treasury/investments/{inv_id}/accrue-interest",
        headers=headers,
        json={"days": 30},
    )
    assert accrue.status_code == 200
    assert accrue.json()["data"]["accrual_amount"] > 0

    income = await client.post(
        f"/api/v1/treasury/investments/{inv_id}/record-income",
        headers=headers,
        json={"amount": 100},
    )
    assert income.status_code == 200
    assert income.json()["data"]["investment"]["total_income"] == 100

    txns = await client.get(f"/api/v1/treasury/investments/{inv_id}/income", headers=headers)
    assert txns.status_code == 200
    assert len(txns.json()["data"]) >= 2


@pytest.mark.asyncio
async def test_maturity_tracking_and_performance(client):
    slug = "investmat"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    maturities = await client.get("/api/v1/treasury/investments/maturities", headers=headers)
    assert maturities.status_code == 200
    mat = maturities.json()["data"]
    assert "upcoming_maturities" in mat
    assert "overdue_maturities" in mat

    perf = await client.get("/api/v1/treasury/investments/performance", headers=headers)
    assert perf.status_code == 200
    p = perf.json()["data"]
    assert p["total_principal"] > 0
    assert "portfolios" in p
    assert len(p["portfolios"]) >= 2


@pytest.mark.asyncio
async def test_risk_ratings_and_portfolios(client):
    slug = "investrisk"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    risk = await client.get("/api/v1/treasury/investments/risk-ratings", headers=headers)
    assert risk.status_code == 200
    assert "portfolio_risk_rating" in risk.json()["data"]
    assert "by_rating" in risk.json()["data"]

    portfolios = await client.get("/api/v1/treasury/investments/portfolios", headers=headers)
    assert portfolios.status_code == 200
    names = {p["portfolio_name"] for p in portfolios.json()["data"]}
    assert "Core Treasury Portfolio" in names


@pytest.mark.asyncio
async def test_mature_investment(client):
    slug = "investmature"
    headers = await _auth_headers(client, slug)
    data = await _provision(slug)
    tbill = next(i for i in data["investments"] if i["instrument_code"] == "T-BILL-91")

    mature = await client.post(
        f"/api/v1/treasury/investments/{tbill['id']}/mature",
        headers=headers,
        json={},
    )
    assert mature.status_code == 200
    result = mature.json()["data"]
    assert result["investment"]["status"] == "matured"
    assert result["maturity_proceeds"] >= tbill["principal_amount"]


@pytest.mark.asyncio
async def test_ai_investment_analysis(client):
    slug = "investai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    ai = await client.post("/api/v1/treasury/investments/ai/analysis", headers=headers)
    assert ai.status_code == 200
    data = ai.json()["data"]
    assert "recommendations" in data
    assert len(data["recommendations"]) >= 1
    assert data["autonomous_execution"] is False
    assert all(r.get("autonomous_execution") is False for r in data["recommendations"])
