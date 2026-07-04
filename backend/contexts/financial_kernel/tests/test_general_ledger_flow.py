"""Enterprise General Ledger tests."""
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
        json={"email": "gl@kernel.dev", "password": "SecurePass123!", "display_name": "GL Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "gl@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_hospital(slug: str) -> dict[str, str]:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    periods = (await svc.list_periods(slug)).unwrap()
    codes = {
        "ar": (await svc.resolve_account_code(slug, "patient_receivables")).unwrap(),
        "rev": (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap(),
        "cash": (await svc.resolve_account_code(slug, "cash")).unwrap(),
        "expense": (await svc.resolve_account_code(slug, "clinical_staff")).unwrap(),
    }
    return {"period_id": periods[0]["id"], **codes}


@pytest.mark.asyncio
async def test_immutable_automatic_journal(client):
    slug = "gl-auto"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    post = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "enc-100",
            "currency": "EUR",
            "base_currency": "USD",
            "exchange_rate": 1.1,
            "lines": [
                {"account_code": ctx["ar"], "debit": 200, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 200},
            ],
        },
    )
    assert post.status_code == 201
    data = post.json()["data"]
    assert data["status"] == "posted"
    assert data["is_immutable"] is True
    assert data["immutable_hash"]
    assert data["lines"][0]["base_debit"] == 220.0


@pytest.mark.asyncio
async def test_manual_approval_workflow(client):
    slug = "gl-manual"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    draft = await client.post(
        "/api/v1/financial-kernel/ledger/journals/manual",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "adj-001",
            "lines": [
                {"account_code": ctx["expense"], "debit": 50, "credit": 0},
                {"account_code": ctx["cash"], "debit": 0, "credit": 50},
            ],
        },
    )
    assert draft.status_code == 201
    journal_id = draft.json()["data"]["id"]
    assert draft.json()["data"]["status"] == "draft"

    submit = await client.post(
        f"/api/v1/financial-kernel/ledger/journals/{journal_id}/submit",
        headers=headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_approval"

    approve = await client.post(
        f"/api/v1/financial-kernel/ledger/journals/{journal_id}/approve",
        headers=headers,
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "posted"


@pytest.mark.asyncio
async def test_reverse_only_no_delete(client):
    slug = "gl-reverse"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    post = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "enc-rev",
            "lines": [
                {"account_code": ctx["ar"], "debit": 300, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 300},
            ],
        },
    )
    journal_id = post.json()["data"]["id"]

    reverse = await client.post(
        f"/api/v1/financial-kernel/ledger/journals/{journal_id}/reverse",
        headers=headers,
    )
    assert reverse.status_code == 201
    assert reverse.json()["data"]["posting_mode"] == "reversing"
    assert reverse.json()["data"]["reverses_journal_id"] == journal_id

    original = await client.get(
        f"/api/v1/financial-kernel/ledger/journals/{journal_id}",
        headers=headers,
    )
    assert original.json()["data"]["status"] == "reversed"


@pytest.mark.asyncio
async def test_recurring_journal_and_budget_validation(client):
    slug = "gl-recurring"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    await client.post(
        "/api/v1/financial-kernel/ledger/budgets",
        headers=headers,
        json={
            "period_id": ctx["period_id"],
            "account_code": ctx["expense"],
            "amount": 60.0,
            "cost_center": "ER",
        },
    )

    recurring = await client.post(
        "/api/v1/financial-kernel/ledger/recurring",
        headers=headers,
        json={
            "name": "Monthly Rent",
            "schedule": "monthly",
            "lines": [
                {"account_code": ctx["expense"], "debit": 30, "credit": 0, "cost_center": "ER"},
                {"account_code": ctx["cash"], "debit": 0, "credit": 30},
            ],
        },
    )
    template_id = recurring.json()["data"]["id"]

    run1 = await client.post(
        f"/api/v1/financial-kernel/ledger/recurring/{template_id}/run",
        headers=headers,
    )
    assert run1.status_code == 201

    run2 = await client.post(
        f"/api/v1/financial-kernel/ledger/recurring/{template_id}/run",
        headers=headers,
    )
    assert run2.status_code == 201

    run3 = await client.post(
        f"/api/v1/financial-kernel/ledger/recurring/{template_id}/run",
        headers=headers,
    )
    assert run3.status_code == 400
    assert "budget_exceeded" in run3.json()["detail"]


@pytest.mark.asyncio
async def test_unlimited_accounts(client):
    slug = "gl-accounts"
    await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    for i in range(5):
        resp = await client.post(
            "/api/v1/financial-kernel/ledger/accounts",
            headers=headers,
            json={"code": f"9{i:03d}", "name": f"Custom Account {i}", "account_type": "expense"},
        )
        assert resp.status_code == 201

    accounts = await client.get("/api/v1/financial-kernel/ledger/accounts", headers=headers)
    assert len(accounts.json()["data"]) >= 9
