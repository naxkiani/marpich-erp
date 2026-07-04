"""Enterprise Currency Engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_kernel_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "fx@kernel.dev", "password": "SecurePass123!", "display_name": "FX Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "fx@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict[str, str]:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    ar = (await svc.resolve_account_code(slug, "patient_receivables")).unwrap()
    rev = (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap()
    return {"ar": ar, "rev": rev}


@pytest.mark.asyncio
async def test_currency_config_on_provision():
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": "fx-prov", "payload": {"industry_pack": "retail"}}
    )
    config = (await svc.get_currency_config("fx-prov")).unwrap()
    assert config["base_currency"] == "USD"
    assert "EUR" in config["enabled_currencies"]


@pytest.mark.asyncio
async def test_convert_with_resolved_rate(client):
    slug = "fx-convert"
    headers = await _auth_headers(client, slug)
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "retail"}}
    )
    resp = await client.post(
        "/api/v1/financial-kernel/currency/convert",
        headers=headers,
        json={"amount": "100", "from_currency": "USD", "to_currency": "EUR"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["rate"] == 0.92
    assert float(data["converted_amount"]) == 92.0


@pytest.mark.asyncio
async def test_manual_rate_override(client):
    slug = "fx-manual"
    headers = await _auth_headers(client, slug)
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "retail"}}
    )
    await client.post(
        "/api/v1/financial-kernel/currency/rates/manual",
        headers=headers,
        json={"from_currency": "USD", "to_currency": "EUR", "rate": 0.95},
    )
    resp = await client.post(
        "/api/v1/financial-kernel/currency/convert",
        headers=headers,
        json={"amount": "100", "from_currency": "USD", "to_currency": "EUR", "rate_type": "manual"},
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["rate"] == 0.95


@pytest.mark.asyncio
async def test_fetch_exchange_api_rates(client):
    slug = "fx-fetch"
    headers = await _auth_headers(client, slug)
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "retail"}}
    )
    resp = await client.post(
        "/api/v1/financial-kernel/currency/rates/fetch",
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["imported"] >= 1


@pytest.mark.asyncio
async def test_exchange_rate_history(client):
    slug = "fx-history"
    headers = await _auth_headers(client, slug)
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "retail"}}
    )
    await client.post(
        "/api/v1/financial-kernel/currency/rates/fetch",
        headers=headers,
    )
    history = await client.get(
        "/api/v1/financial-kernel/currency/rates/history",
        headers=headers,
        params={"from_currency": "USD", "to_currency": "EUR"},
    )
    assert history.status_code == 200
    assert len(history.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_journal_stores_rate_snapshot(client):
    slug = "fx-snapshot"
    ctx = await _provision(slug)
    headers = await _auth_headers(client, slug)

    post = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "fx-enc-1",
            "currency": "EUR",
            "base_currency": "USD",
            "lines": [
                {"account_code": ctx["ar"], "debit": 100, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 100},
            ],
        },
    )
    assert post.status_code == 201
    journal = post.json()["data"]
    assert journal["rate_snapshot_id"]
    assert journal["reporting_currency"] == "USD"
    assert journal["lines"][0]["rate_snapshot_id"] == journal["rate_snapshot_id"]

    snapshots = await client.get(
        "/api/v1/financial-kernel/currency/snapshots",
        headers=headers,
    )
    assert snapshots.status_code == 200
    assert any(s["journal_id"] == journal["id"] for s in snapshots.json()["data"])


@pytest.mark.asyncio
async def test_revaluation_and_gain_loss(client):
    slug = "fx-reval"
    headers = await _auth_headers(client, slug)
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "retail"}}
    )
    reval = await client.post(
        "/api/v1/financial-kernel/currency/revaluation",
        headers=headers,
        json={
            "balances": [
                {"currency": "EUR", "foreign_balance": 1000, "base_balance": 920},
            ],
        },
    )
    assert reval.status_code == 201
    assert "net_gain_loss" in reval.json()["data"]

    report = await client.get(
        "/api/v1/financial-kernel/currency/gain-loss",
        headers=headers,
    )
    assert report.status_code == 200
    assert report.json()["data"]["revaluation_count"] >= 1
