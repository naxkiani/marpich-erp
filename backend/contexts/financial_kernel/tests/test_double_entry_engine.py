"""Enterprise Double Entry Accounting Engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.double_entry_posting_engine import (
    build_closing_entry,
    expand_single_entry_to_double,
    SingleEntryInput,
)
from contexts.financial_kernel.domain.services.double_entry_validation_engine import (
    run_posting_validation,
    validate_double_entry_balance,
)
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
        json={"email": "de@kernel.dev", "password": "SecurePass123!", "display_name": "DE Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "de@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_hospital(slug: str) -> dict[str, str]:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    return {
        "ar": (await svc.resolve_account_code(slug, "patient_receivables")).unwrap(),
        "rev": (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap(),
        "cash": (await svc.resolve_account_code(slug, "cash")).unwrap(),
        "expense": (await svc.resolve_account_code(slug, "clinical_staff")).unwrap(),
    }


def test_validation_rejects_unbalanced():
    lines = [
        {"account_code": "1000", "debit": 100, "credit": 0},
        {"account_code": "4000", "debit": 0, "credit": 50},
    ]
    result = validate_double_entry_balance(lines)
    assert not result.valid
    assert result.issues[0].code == "unbalanced"
    assert result.balance_delta == 50


def test_single_entry_expands_to_balanced_double():
    lines = expand_single_entry_to_double(
        SingleEntryInput(
            amount=500,
            primary_account_code="6000",
            offset_account_code="1000",
            side="debit",
            description="Expense payment",
        )
    )
    result = validate_double_entry_balance(lines)
    assert result.valid
    assert result.total_debit == 500
    assert result.total_credit == 500


def test_closing_entry_balances():
    lines = build_closing_entry(
        retained_earnings_account="3000",
        income_summary_account="3999",
        revenue_closes=[{"account_code": "4000", "balance": 1000}],
        expense_closes=[{"account_code": "6000", "balance": 400}],
    )
    result = validate_double_entry_balance(lines)
    assert result.valid
    assert result.is_compound


@pytest.mark.asyncio
async def test_posting_preview_balanced(client):
    slug = "depreview"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/posting/preview",
        headers=headers,
        json={
            "lines": [
                {"account_code": ctx["ar"], "debit": 300, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 300},
            ],
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["can_post"] is True
    assert data["preview"]["is_balanced"] is True


@pytest.mark.asyncio
async def test_posting_preview_rejects_unbalanced(client):
    slug = "deunbal"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/posting/preview",
        headers=headers,
        json={
            "lines": [
                {"account_code": ctx["ar"], "debit": 300, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 100},
            ],
        },
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["can_post"] is False
    assert any(i["code"] == "unbalanced" for i in data["validation"]["issues"])


@pytest.mark.asyncio
async def test_single_entry_ui_posting(client):
    slug = "desingle"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/journals/single-entry",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "exp-001",
            "amount": 150,
            "primary_account_code": ctx["expense"],
            "offset_account_code": ctx["cash"],
            "side": "debit",
            "description": "Clinical expense",
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["status"] == "posted"
    assert data["journal_entry_type"] == "single_entry"
    assert data["total_debits"] == 150
    assert data["total_credits"] == 150


@pytest.mark.asyncio
async def test_compound_journal_posting(client):
    slug = "decompound"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "compound-1",
            "lines": [
                {"account_code": ctx["cash"], "debit": 100, "credit": 0},
                {"account_code": ctx["ar"], "debit": 50, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 150},
            ],
        },
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["journal_entry_type"] == "compound"


@pytest.mark.asyncio
async def test_adjusting_entry(client):
    slug = "deadjust"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    draft = await client.post(
        "/api/v1/financial-kernel/ledger/journals/adjusting",
        headers=headers,
        json={
            "source_document_id": "adj-001",
            "debit_account": ctx["expense"],
            "credit_account": ctx["cash"],
            "amount": 75,
        },
    )
    assert draft.status_code == 201
    assert draft.json()["data"]["journal_entry_type"] == "adjusting"
    assert draft.json()["data"]["status"] == "draft"


@pytest.mark.asyncio
async def test_opening_balance(client):
    slug = "deopen"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/journals/opening-balance",
        headers=headers,
        json={
            "source_document_id": "ob-2025",
            "balances": [
                {"account_code": ctx["cash"], "debit": 10000, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 10000},
            ],
            "require_approval": False,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["journal_entry_type"] == "opening_balance"


@pytest.mark.asyncio
async def test_intercompany_entry(client):
    slug = "deinter"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/journals/intercompany",
        headers=headers,
        json={
            "source_document_id": "ic-001",
            "originating_org_id": "org-a",
            "counterparty_org_id": "org-b",
            "amount": 200,
            "due_from_account": ctx["ar"],
            "due_to_account": ctx["cash"],
            "expense_account": ctx["expense"],
            "revenue_account": ctx["rev"],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["intercompany_pair_id"]
    assert data["originating_journal"]["journal_entry_type"] == "intercompany"
    assert data["counterparty_journal"]["journal_entry_type"] == "intercompany"


@pytest.mark.asyncio
async def test_rollback_journal(client):
    slug = "deroll"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    posted = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "rb-001",
            "lines": [
                {"account_code": ctx["ar"], "debit": 80, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 80},
            ],
        },
    )
    journal_id = posted.json()["data"]["id"]
    rollback = await client.post(
        f"/api/v1/financial-kernel/ledger/journals/{journal_id}/rollback",
        headers=headers,
        json={"reason": "data_correction"},
    )
    assert rollback.status_code == 201
    assert rollback.json()["data"]["rollback"]["action"] == "rollback"


@pytest.mark.asyncio
async def test_posting_rules_catalog(client):
    slug = "derules"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/financial-kernel/ledger/posting-rules", headers=headers)
    assert resp.status_code == 200
    rules = {r["id"] for r in resp.json()["data"]}
    assert "expense_payment" in rules
    assert "revenue_receipt" in rules


@pytest.mark.asyncio
async def test_unbalanced_journal_rejected(client):
    slug = "dereject"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/ledger/journals/automatic",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "bad-001",
            "lines": [
                {"account_code": ctx["ar"], "debit": 100, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 50},
            ],
        },
    )
    assert resp.status_code == 400
    assert "unbalanced" in resp.json()["detail"]
