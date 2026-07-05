"""Enterprise Cash Management tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import get_cash_management_service, reset_treasury_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_cash_management_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "cash@treasury.dev", "password": "SecurePass123!", "display_name": "Cash Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "cash@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict[str, dict]:
    svc = get_cash_management_service()
    await svc.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    locs = (await svc.list_locations(slug)).unwrap()
    return {l["location_type"]: l for l in locs}


@pytest.mark.asyncio
async def test_cash_management_catalog(client):
    slug = "cashcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/cash-management/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "cash_registers" in caps
    assert "cash_counting" in caps
    assert "enterprise_cash_dashboard" in caps
    assert len(caps) >= 18


@pytest.mark.asyncio
async def test_seed_seven_location_types(client):
    slug = "cashseed"
    locs = await _provision(slug)
    types = set(locs.keys())
    assert "cash_register" in types
    assert "petty_cash" in types
    assert "main_cash_office" in types
    assert "vault" in types
    assert "safe" in types
    assert "branch_cash" in types
    assert "department_cash" in types


@pytest.mark.asyncio
async def test_cash_transactions(client):
    slug = "cashtxn"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    register = locs["cash_register"]
    petty = locs["petty_cash"]

    deposit = await client.post(
        "/api/v1/treasury/cash-management/transactions",
        headers=headers,
        json={
            "location_id": register["id"],
            "transaction_type": "deposit",
            "amount": 200,
            "reference": "DEP-001",
        },
    )
    assert deposit.status_code == 201

    transfer = await client.post(
        "/api/v1/treasury/cash-management/transactions",
        headers=headers,
        json={
            "location_id": register["id"],
            "transaction_type": "transfer",
            "amount": 100,
            "reference": "XFR-001",
            "counterpart_location_id": petty["id"],
        },
    )
    assert transfer.status_code == 201

    withdrawal = await client.post(
        "/api/v1/treasury/cash-management/transactions",
        headers=headers,
        json={
            "location_id": petty["id"],
            "transaction_type": "withdrawal",
            "amount": 50,
            "reference": "WDL-001",
        },
    )
    assert withdrawal.status_code == 201


@pytest.mark.asyncio
async def test_count_verify_close_reconcile(client):
    slug = "cashctrl"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    vault = locs["vault"]

    count = await client.post(
        "/api/v1/treasury/cash-management/counts",
        headers=headers,
        json={"location_id": vault["id"], "counted_amount": vault["balance"]},
    )
    assert count.status_code == 201
    count_id = count.json()["data"]["id"]

    verify = await client.post(
        f"/api/v1/treasury/cash-management/counts/{count_id}/verify",
        headers=headers,
        json={"approved": True},
    )
    assert verify.status_code == 200
    assert verify.json()["data"]["count"]["status"] == "verified"

    open_close = await client.post(
        "/api/v1/treasury/cash-management/closings",
        headers=headers,
        json={"location_id": vault["id"]},
    )
    assert open_close.status_code == 201
    closing_id = open_close.json()["data"]["id"]

    close = await client.post(
        f"/api/v1/treasury/cash-management/closings/{closing_id}/close",
        headers=headers,
        json={"counted_amount": vault["balance"]},
    )
    assert close.status_code == 200
    assert close.json()["data"]["status"] == "closed"

    recon = await client.post(
        "/api/v1/treasury/cash-management/reconciliations",
        headers=headers,
        json={
            "location_id": vault["id"],
            "period_start": "2025-07-01",
            "period_end": "2025-07-31",
            "counted_balance": vault["balance"],
        },
    )
    assert recon.status_code == 201
    assert recon.json()["data"]["status"] == "reconciled"


@pytest.mark.asyncio
async def test_cash_forecast_and_dashboard(client):
    slug = "cashdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    forecast = await client.post(
        "/api/v1/treasury/cash-management/forecasts",
        headers=headers,
        json={
            "name": "July Cash Forecast",
            "period_start": "2025-07-01",
            "period_end": "2025-07-31",
            "scenario": "base",
            "opening_balance": 40000,
            "projected_lines": [
                {"date": "2025-07-15", "label": "Payroll", "outflow": 8000},
                {"date": "2025-07-20", "label": "Collections", "inflow": 12000},
            ],
        },
    )
    assert forecast.status_code == 201

    dash = await client.get("/api/v1/treasury/cash-management/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert data["summary"]["location_count"] == 7
    assert data["summary"]["total_cash_balance"] > 0
    assert "balances_by_location_type" in data
    assert "forecasts" in data


@pytest.mark.asyncio
async def test_all_transaction_types(client):
    slug = "cashall"
    headers = await _auth_headers(client, slug)
    locs = await _provision(slug)
    loc = locs["main_cash_office"]

    for ttype in ("deposit", "receipt", "payment", "withdrawal"):
        resp = await client.post(
            "/api/v1/treasury/cash-management/transactions",
            headers=headers,
            json={
                "location_id": loc["id"],
                "transaction_type": ttype,
                "amount": 10,
                "reference": f"{ttype.upper()}-1",
            },
        )
        assert resp.status_code == 201, ttype

    adj = await client.post(
        "/api/v1/treasury/cash-management/transactions",
        headers=headers,
        json={
            "location_id": loc["id"],
            "transaction_type": "adjustment",
            "amount": 5,
            "reference": "ADJ-1",
        },
    )
    assert adj.status_code == 201
