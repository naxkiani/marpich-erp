"""Enterprise subledger platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.subledger_engine import (
    SUBLEDGER_CATALOG,
    build_subledger_idempotency_key,
    compute_subledger_balance,
    reconcile_balances,
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
        json={"email": "sub@kernel.dev", "password": "SecurePass123!", "display_name": "Subledger Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "sub@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def test_subledger_catalog_has_all_types():
    assert len(SUBLEDGER_CATALOG) == 12
    types = set(SUBLEDGER_CATALOG.keys())
    assert "accounts_receivable" in types
    assert "accounts_payable" in types
    assert "patients" in types
    assert "currency_exchange" in types


def test_idempotency_key_and_balance_helpers():
    key = build_subledger_idempotency_key("accounts_receivable", "INV-001")
    assert key == "subledger:accounts_receivable:INV-001"
    check = reconcile_balances(subledger_balance=100.0, gl_control_balance=100.0)
    assert check["balanced"] is True


@pytest.mark.asyncio
async def test_provision_creates_all_subledgers():
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": "sub-prov", "payload": {"industry_pack": "hospital"}}
    )
    subledgers = (await svc.list_subledgers("sub-prov")).unwrap()
    assert len(subledgers) == 12


@pytest.mark.asyncio
async def test_ar_post_auto_gl_and_idempotent(client):
    slug = "sub-ar"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )

    post = await client.post(
        "/api/v1/financial-kernel/subledgers/entries",
        headers=headers,
        json={
            "subledger_type": "patients",
            "source_document_id": "ENC-1001",
            "amount": 250.0,
            "entry_date": "2025-06-01",
            "reference": "ENC-1001",
            "counterparty": "Patient Smith",
        },
    )
    assert post.status_code == 201
    data = post.json()["data"]
    assert data["entry"]["status"] == "posted"
    assert data["journal"] is not None
    assert data["idempotent"] is False

    dup = await client.post(
        "/api/v1/financial-kernel/subledgers/entries",
        headers=headers,
        json={
            "subledger_type": "patients",
            "source_document_id": "ENC-1001",
            "amount": 250.0,
            "entry_date": "2025-06-01",
        },
    )
    assert dup.status_code == 201
    assert dup.json()["data"]["idempotent"] is True


@pytest.mark.asyncio
async def test_ap_inventory_payroll_posting(client):
    slug = "sub-multi"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    await client.post(
        "/api/v1/financial-kernel/coa/templates/apply",
        headers=headers,
        json={"template_key": "coa.enterprise", "template_type": "industry", "merge": True},
    )

    for sub_type, doc_id, amount in [
        ("accounts_payable", "PO-500", 1200.0),
        ("inventory", "GRN-200", 800.0),
        ("payroll", "PAY-JUN", 5000.0),
    ]:
        resp = await client.post(
            "/api/v1/financial-kernel/subledgers/entries",
            headers=headers,
            json={
                "subledger_type": sub_type,
                "source_document_id": doc_id,
                "amount": amount,
                "entry_date": "2025-06-15",
            },
        )
        assert resp.status_code == 201, f"{sub_type} failed: {resp.text}"
        assert resp.json()["data"]["journal"] is not None


@pytest.mark.asyncio
async def test_subledger_reconciliation(client):
    slug = "sub-recon"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    patients = (await svc.get_subledger_by_type(slug, "patients")).unwrap()

    await client.post(
        "/api/v1/financial-kernel/subledgers/entries",
        headers=headers,
        json={
            "subledger_type": "patients",
            "source_document_id": "ENC-2001",
            "amount": 500.0,
            "entry_date": "2025-06-20",
        },
    )

    recon = await client.post(
        f"/api/v1/financial-kernel/subledgers/{patients['id']}/reconcile",
        headers=headers,
        json={"reconciliation_date": "2025-06-30"},
    )
    assert recon.status_code == 201
    data = recon.json()["data"]
    assert "variance" in data
    assert "matched_pairs" in data
    assert data["control_account_code"]


@pytest.mark.asyncio
async def test_reverse_subledger_entry(client):
    slug = "sub-rev"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )

    post = await client.post(
        "/api/v1/financial-kernel/subledgers/entries",
        headers=headers,
        json={
            "subledger_type": "patients",
            "source_document_id": "ENC-3001",
            "amount": 100.0,
            "entry_date": "2025-07-01",
        },
    )
    entry_id = post.json()["data"]["entry"]["id"]

    reverse = await client.post(
        f"/api/v1/financial-kernel/subledgers/entries/{entry_id}/reverse",
        headers=headers,
    )
    assert reverse.status_code == 200
    assert reverse.json()["data"]["original_entry"]["status"] == "reversed"


@pytest.mark.asyncio
async def test_catalog_and_list_endpoints(client):
    headers = await _auth_headers(client, "sub-api")
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": "sub-api", "payload": {"industry_pack": "retail"}}
    )

    catalog = await client.get(
        "/api/v1/financial-kernel/subledgers/catalog", headers=headers
    )
    assert catalog.status_code == 200
    assert len(catalog.json()["data"]) == 12

    listing = await client.get(
        "/api/v1/financial-kernel/subledgers", headers=headers
    )
    assert listing.status_code == 200
    assert len(listing.json()["data"]) == 12

    ar = await client.get(
        "/api/v1/financial-kernel/subledgers/types/accounts_receivable",
        headers=headers,
    )
    assert ar.status_code == 200
    assert ar.json()["data"]["posting_rule_id"] == "sales"
