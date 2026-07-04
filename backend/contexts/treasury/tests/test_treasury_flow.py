"""Enterprise Treasury tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import get_treasury_service, reset_treasury_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_treasury_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "cfo@treasury.dev", "password": "SecurePass123!", "display_name": "CFO"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "cfo@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict:
    svc = get_treasury_service()
    await svc.handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    accounts = (await svc.list_accounts(slug)).unwrap()
    by_type = {a["account_type"]: a for a in accounts}
    return by_type


@pytest.mark.asyncio
async def test_seed_accounts_on_provision():
    accounts = await _provision("treasury-seed")
    types = {a["account_type"] for a in accounts.values()}
    assert "cash" in types
    assert "bank" in types
    assert "petty_cash" in types
    assert "vault" in types
    assert "safe" in types


@pytest.mark.asyncio
async def test_treasury_dashboard(client):
    slug = "treasury-dash"
    await _provision(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/dashboard", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["summary"]["account_count"] == 5
    assert data["summary"]["total_balance"] > 0
    assert "liquidity_analysis" in data


@pytest.mark.asyncio
async def test_transfer_approval_workflow(client):
    slug = "treasury-transfer"
    accounts = await _provision(slug)
    headers = await _auth_headers(client, slug)
    bank = accounts["bank"]
    cash = accounts["cash"]

    draft = await client.post(
        "/api/v1/treasury/transfers",
        headers=headers,
        json={
            "from_account_id": bank["id"],
            "to_account_id": cash["id"],
            "amount": 1000,
            "currency": "USD",
            "instrument": "electronic_transfer",
            "reference": "TRF-001",
        },
    )
    assert draft.status_code == 201
    transfer_id = draft.json()["data"]["id"]
    assert draft.json()["data"]["status"] == "draft"

    submit = await client.post(
        f"/api/v1/treasury/transfers/{transfer_id}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/treasury/transfers/{transfer_id}/approve",
        headers=headers,
        json={},
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "executed"


@pytest.mark.asyncio
async def test_cheque_transfer(client):
    slug = "treasury-cheque"
    accounts = await _provision(slug)
    headers = await _auth_headers(client, slug)
    bank = accounts["bank"]
    petty = accounts["petty_cash"]

    resp = await client.post(
        "/api/v1/treasury/transfers",
        headers=headers,
        json={
            "from_account_id": bank["id"],
            "to_account_id": petty["id"],
            "amount": 200,
            "currency": "USD",
            "instrument": "cheque",
            "reference": "CHQ-100",
            "cheque_number": "10042",
            "require_approval": False,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["status"] == "executed"
    assert resp.json()["data"]["instrument"] == "cheque"


@pytest.mark.asyncio
async def test_mobile_money_and_digital_wallet(client):
    slug = "treasury-mobile"
    accounts = await _provision(slug)
    headers = await _auth_headers(client, slug)
    cash = accounts["cash"]
    petty = accounts["petty_cash"]

    for instrument in ("mobile_money", "digital_wallet"):
        resp = await client.post(
            "/api/v1/treasury/transfers",
            headers=headers,
            json={
                "from_account_id": cash["id"],
                "to_account_id": petty["id"],
                "amount": 50,
                "currency": "USD",
                "instrument": instrument,
                "reference": f"{instrument.upper()}-001",
                "require_approval": False,
            },
        )
        assert resp.status_code == 201
        assert resp.json()["data"]["instrument"] == instrument


@pytest.mark.asyncio
async def test_bank_reconciliation(client):
    slug = "treasury-recon"
    accounts = await _provision(slug)
    headers = await _auth_headers(client, slug)
    bank = accounts["bank"]

    resp = await client.post(
        "/api/v1/treasury/reconciliations",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "statement_date": "2025-06-30",
            "statement_balance": bank["balance"],
            "statement_items": [
                {"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"},
            ],
            "book_items": [
                {"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"},
            ],
        },
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["status"] == "reconciled"


@pytest.mark.asyncio
async def test_cash_flow_forecast(client):
    slug = "treasury-forecast"
    await _provision(slug)
    headers = await _auth_headers(client, slug)

    resp = await client.post(
        "/api/v1/treasury/forecasts",
        headers=headers,
        json={
            "name": "Q3 Cash Forecast",
            "period_start": "2025-07-01",
            "period_end": "2025-09-30",
            "scenario": "base",
            "projected_lines": [
                {"date": "2025-07-15", "label": "Payroll", "outflow": 15000},
                {"date": "2025-08-01", "label": "Customer receipts", "inflow": 25000},
                {"date": "2025-09-01", "label": "Rent", "outflow": 5000},
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert len(data["lines"]) == 3
    assert data["total_inflow"] == 25000
    assert data["total_outflow"] == 20000


@pytest.mark.asyncio
async def test_liquidity_analysis(client):
    slug = "treasury-liquidity"
    await _provision(slug)
    headers = await _auth_headers(client, slug)

    resp = await client.get("/api/v1/treasury/liquidity", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "liquidity_ratio" in data
    assert "restricted_balance" in data
    assert data["by_account_type"]["vault"] > 0
