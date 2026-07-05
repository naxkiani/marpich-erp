"""Enterprise journal engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.journal_engine import (
    get_journal_type_rules,
    list_journal_types,
    validate_batch_entry,
    validate_rollback_allowed,
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
        json={"email": "journal@kernel.dev", "password": "SecurePass123!", "display_name": "Journal Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "journal@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_hospital(slug: str) -> dict[str, str]:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    codes = {
        "ar": (await svc.resolve_account_code(slug, "patient_receivables")).unwrap(),
        "rev": (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap(),
        "cash": (await svc.resolve_account_code(slug, "cash")).unwrap(),
        "expense": (await svc.resolve_account_code(slug, "clinical_staff")).unwrap(),
    }
    return codes


def test_all_journal_types_registered():
    types = {t["journal_type"] for t in list_journal_types()}
    expected = {
        "general", "cash", "bank", "purchase", "sales", "inventory",
        "payroll", "tax", "adjustment", "opening", "closing", "reversing",
        "recurring", "foreign_currency", "intercompany",
    }
    assert expected == types


def test_cash_journal_requires_approval():
    rules = get_journal_type_rules("cash")
    assert rules.approval_workflow_required is True
    assert rules.digital_signature_required is True
    assert rules.automatic_posting_allowed is False


def test_payroll_blocks_batch():
    ok, reason = validate_batch_entry("payroll")
    assert ok is False
    assert "batch_not_allowed" in reason


def test_opening_blocks_rollback():
    ok, reason = validate_rollback_allowed("opening")
    assert ok is False


@pytest.mark.asyncio
async def test_journal_types_api(client):
    headers = await _auth_headers(client, "journal-types-api")
    resp = await client.get("/api/v1/financial-kernel/journals/types", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 15

    rules = await client.get(
        "/api/v1/financial-kernel/journals/types/cash/rules",
        headers=headers,
    )
    assert rules.status_code == 200
    assert rules.json()["data"]["digital_signature_required"] is True


@pytest.mark.asyncio
async def test_typed_general_journal_auto_posts(client):
    slug = "journal-general"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    resp = await client.post(
        "/api/v1/financial-kernel/journals/typed",
        headers=headers,
        json={
            "journal_type": "general",
            "source_context": "hospital",
            "source_document_id": "svc-001",
            "currency": "USD",
            "lines": [
                {"account_code": ctx["ar"], "debit": 100, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 100},
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["status"] == "posted"
    assert data["journal_type"] == "general"
    assert data["is_locked"] is True
    assert "journal_type_rules" in data


@pytest.mark.asyncio
async def test_cash_journal_draft_with_approval(client):
    slug = "journal-cash"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    resp = await client.post(
        "/api/v1/financial-kernel/journals/typed",
        headers=headers,
        json={
            "journal_type": "cash",
            "source_context": "treasury",
            "source_document_id": "petty-001",
            "currency": "USD",
            "lines": [
                {"account_code": ctx["expense"], "debit": 50, "credit": 0},
                {"account_code": ctx["cash"], "debit": 0, "credit": 50},
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["status"] == "draft"
    assert data["journal_type"] == "cash"


@pytest.mark.asyncio
async def test_batch_posting(client):
    slug = "journal-batch"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    resp = await client.post(
        "/api/v1/financial-kernel/journals/batch",
        headers=headers,
        json={
            "entries": [
                {
                    "journal_type": "general",
                    "source_context": "hospital",
                    "source_document_id": "batch-a",
                    "currency": "USD",
                    "lines": [
                        {"account_code": ctx["ar"], "debit": 10, "credit": 0},
                        {"account_code": ctx["rev"], "debit": 0, "credit": 10},
                    ],
                },
                {
                    "journal_type": "general",
                    "source_context": "hospital",
                    "source_document_id": "batch-b",
                    "currency": "USD",
                    "lines": [
                        {"account_code": ctx["ar"], "debit": 20, "credit": 0},
                        {"account_code": ctx["rev"], "debit": 0, "credit": 20},
                    ],
                },
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["posted_count"] == 2
    assert data["batch_id"]
    assert all(j["batch_id"] == data["batch_id"] for j in data["journals"])


@pytest.mark.asyncio
async def test_sign_and_ai_review(client):
    slug = "journal-sign"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    draft = await client.post(
        "/api/v1/financial-kernel/journals/typed",
        headers=headers,
        json={
            "journal_type": "cash",
            "source_context": "treasury",
            "source_document_id": "sign-001",
            "currency": "USD",
            "lines": [
                {"account_code": ctx["expense"], "debit": 25, "credit": 0},
                {"account_code": ctx["cash"], "debit": 0, "credit": 25},
            ],
        },
    )
    journal_id = draft.json()["data"]["id"]

    review = await client.post(
        f"/api/v1/financial-kernel/journals/{journal_id}/ai-review",
        headers=headers,
    )
    assert review.status_code == 200
    assert review.json()["data"]["ai_review"]["review_type"] == "journal_ai_review"

    signed = await client.post(
        f"/api/v1/financial-kernel/journals/{journal_id}/sign",
        headers=headers,
        json={"signer_id": "finance-clerk-1"},
    )
    assert signed.status_code == 200
    assert signed.json()["data"]["digital_signature"]["signer_id"] == "finance-clerk-1"


@pytest.mark.asyncio
async def test_journal_versioning(client):
    slug = "journal-version"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    draft = await client.post(
        "/api/v1/financial-kernel/journals/typed",
        headers=headers,
        json={
            "journal_type": "general",
            "source_context": "hospital",
            "source_document_id": "ver-001",
            "currency": "USD",
            "require_approval": True,
            "lines": [
                {"account_code": ctx["ar"], "debit": 30, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 30},
            ],
        },
    )
    journal_id = draft.json()["data"]["id"]

    v2 = await client.post(
        f"/api/v1/financial-kernel/journals/{journal_id}/versions",
        headers=headers,
        json={
            "lines": [
                {"account_code": ctx["ar"], "debit": 35, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 35},
            ],
        },
    )
    assert v2.status_code == 201
    assert v2.json()["data"]["version"] == 2
    assert v2.json()["data"]["parent_version_id"] == journal_id

    versions = await client.get(
        f"/api/v1/financial-kernel/journals/{journal_id}/versions",
        headers=headers,
    )
    assert versions.status_code == 200
    assert len(versions.json()["data"]) >= 2
