"""Enterprise Bank Reconciliation tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_bank_reconciliation_service,
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
    get_bank_reconciliation_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "recon@treasury.dev", "password": "SecurePass123!", "display_name": "Recon"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "recon@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> dict[str, dict]:
    await get_treasury_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    accounts = (await get_treasury_service().list_accounts(slug)).unwrap()
    return {a["code"]: a for a in accounts}


@pytest.mark.asyncio
async def test_reconciliation_catalog(client):
    slug = "reconcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/bank-reconciliation/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "automatic_matching" in caps
    assert "bank_api_integration" in caps
    assert "ai_matching_suggestions" in caps
    assert "reconciliation_audit" in caps
    assert len(caps) == 11


@pytest.mark.asyncio
async def test_statement_import_and_auto_match(client):
    slug = "reconauto"
    headers = await _auth_headers(client, slug)
    accts = await _provision(slug)
    bank = accts["OPERATING-BANK"]

    stmt = await client.post(
        "/api/v1/treasury/bank-reconciliation/statements/import",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "source": "file_import",
            "statement_date": "2025-06-30",
            "statement_balance": bank["balance"],
            "items": [{"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"}],
        },
    )
    assert stmt.status_code == 201

    recon = await client.post(
        "/api/v1/treasury/bank-reconciliation",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "reconciliation_date": "2025-06-30",
            "statement_balance": bank["balance"],
            "statement_items": [{"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"}],
            "book_items": [{"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"}],
        },
    )
    assert recon.status_code == 201
    data = recon.json()["data"]
    assert len(data["matched_pairs"]) == 1
    assert data["matched_pairs"][0]["match_type"] == "automatic"


@pytest.mark.asyncio
async def test_bank_api_import(client):
    slug = "reconapi"
    headers = await _auth_headers(client, slug)
    accts = await _provision(slug)
    bank = accts["OPERATING-BANK"]

    resp = await client.post(
        "/api/v1/treasury/bank-reconciliation/statements/bank-api",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "statement_date": "2025-07-01",
            "api_payload": {
                "balance": 50000,
                "transactions": [
                    {"reference": "API-TXN-1", "amount": 500, "date": "2025-07-01"},
                ],
            },
        },
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["source"] == "bank_api"


@pytest.mark.asyncio
async def test_exceptions_outstanding_ai(client):
    slug = "reconexc"
    headers = await _auth_headers(client, slug)
    accts = await _provision(slug)
    bank = accts["OPERATING-BANK"]

    recon = await client.post(
        "/api/v1/treasury/bank-reconciliation",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "reconciliation_date": "2025-06-30",
            "statement_balance": bank["balance"] + 500,
            "statement_items": [
                {"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"},
                {"reference": "UNK-001", "amount": 500, "date": "2025-06-20"},
            ],
            "book_items": [{"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"}],
        },
    )
    assert recon.status_code == 201
    recon_id = recon.json()["data"]["id"]

    exceptions = await client.get(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/exceptions", headers=headers
    )
    assert exceptions.status_code == 200
    assert len(exceptions.json()["data"]) >= 1

    outstanding = await client.get(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/outstanding", headers=headers
    )
    assert outstanding.status_code == 200
    assert len(outstanding.json()["data"]) >= 1

    ai = await client.get(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/ai-suggestions", headers=headers
    )
    assert ai.status_code == 200
    assert len(ai.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_manual_match_and_workflow(client):
    slug = "reconwf"
    headers = await _auth_headers(client, slug)
    accts = await _provision(slug)
    bank = accts["OPERATING-BANK"]

    recon = await client.post(
        "/api/v1/treasury/bank-reconciliation",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "reconciliation_date": "2025-06-30",
            "statement_balance": bank["balance"],
            "statement_items": [{"reference": "MAN-001", "amount": 750, "date": "2025-06-18"}],
            "book_items": [{"reference": "BOOK-001", "amount": 760, "date": "2025-06-19"}],
        },
    )
    assert recon.status_code == 201
    recon_id = recon.json()["data"]["id"]
    stmt_item = recon.json()["data"]["unmatched_statement"][0]
    book_item = recon.json()["data"]["unmatched_book"][0]

    match = await client.post(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/match",
        headers=headers,
        json={"statement_item": stmt_item, "book_item": book_item},
    )
    assert match.status_code == 200
    assert len(match.json()["data"]["matched_pairs"]) == 1
    assert match.json()["data"]["matched_pairs"][0]["match_type"] == "manual"

    submit = await client.post(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/submit", headers=headers
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/approve", headers=headers
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "approved"


@pytest.mark.asyncio
async def test_report_audit_dashboard(client):
    slug = "reconrep"
    headers = await _auth_headers(client, slug)
    accts = await _provision(slug)
    bank = accts["OPERATING-BANK"]

    recon = await client.post(
        "/api/v1/treasury/bank-reconciliation",
        headers=headers,
        json={
            "treasury_account_id": bank["id"],
            "reconciliation_date": "2025-06-30",
            "statement_balance": bank["balance"],
            "statement_items": [{"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"}],
            "book_items": [{"reference": "DEP-001", "amount": 1000, "date": "2025-06-15"}],
        },
    )
    recon_id = recon.json()["data"]["id"]

    report = await client.get(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/report", headers=headers
    )
    assert report.status_code == 200
    assert "match_rate" in report.json()["data"]

    audit = await client.get(
        f"/api/v1/treasury/bank-reconciliation/{recon_id}/audit", headers=headers
    )
    assert audit.status_code == 200
    assert len(audit.json()["data"]) >= 1

    dash = await client.get("/api/v1/treasury/bank-reconciliation/dashboard", headers=headers)
    assert dash.status_code == 200
    assert dash.json()["data"]["summary"]["reconciliation_count"] >= 1
