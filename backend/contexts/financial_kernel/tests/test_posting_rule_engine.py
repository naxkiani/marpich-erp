"""Enterprise posting rule engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_kernel,
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.financial_kernel.domain.services.posting_rule_engine import (
    list_platform_posting_rules,
    resolve_rule,
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
        json={"email": "posting@kernel.dev", "password": "SecurePass123!", "display_name": "Posting Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "posting@kernel.dev", "password": "SecurePass123!"},
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
    }


def test_platform_posting_rules_count():
    rules = list_platform_posting_rules()
    ids = {r["rule_id"] for r in rules}
    assert "purchase" in ids
    assert "hospital_billing" in ids
    assert "university_tuition" in ids
    assert len(ids) >= 14


def test_resolve_legacy_posting_rule():
    rule = resolve_rule("expense_payment")
    assert rule.rule_id == "expense_payment"
    assert rule.module == "legacy"


@pytest.mark.asyncio
async def test_posting_rules_api(client):
    headers = await _auth_headers(client, "posting-api")
    resp = await client.get("/api/v1/financial-kernel/posting-rules", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert any(r["rule_id"] == "purchase" for r in data)


@pytest.mark.asyncio
async def test_hospital_billing_execute_posting(client):
    slug = "posting-hospital"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    preview = await client.post(
        "/api/v1/financial-kernel/posting-rules/preview",
        headers=headers,
        json={
            "rule_id": "hospital_billing",
            "amount": 250,
            "account_mappings": {"debit": ctx["ar"], "credit": ctx["rev"]},
            "use_default_accounts": False,
        },
    )
    assert preview.status_code == 200
    assert preview.json()["data"]["is_balanced"] is True

    execute = await client.post(
        "/api/v1/financial-kernel/posting-rules/execute",
        headers=headers,
        json={
            "rule_id": "hospital_billing",
            "source_context": "hospital",
            "source_document_id": "enc-post-001",
            "amount": 250,
            "account_mappings": {"debit": ctx["ar"], "credit": ctx["rev"]},
            "use_default_accounts": False,
            "require_approval": False,
        },
    )
    assert execute.status_code == 201
    data = execute.json()["data"]
    assert data["journal_type"] == "sales"
    assert data["status"] == "posted"


@pytest.mark.asyncio
async def test_rule_builder_custom_rule(client):
    slug = "posting-builder"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    create = await client.post(
        "/api/v1/financial-kernel/posting-rules/builder",
        headers=headers,
        json={
            "rule_id": "custom_donation",
            "label": "Donation Receipt",
            "module": "fundraising",
            "journal_type": "general",
            "account_slots": {
                "debit": {"label": "Cash", "role": "asset"},
                "credit": {"label": "Donation revenue", "role": "revenue"},
            },
            "line_templates": [
                {"side": "debit", "account_slot": "debit"},
                {"side": "credit", "account_slot": "credit"},
            ],
        },
    )
    assert create.status_code == 201

    execute = await client.post(
        "/api/v1/financial-kernel/posting-rules/execute",
        headers=headers,
        json={
            "rule_id": "custom_donation",
            "source_context": "fundraising",
            "source_document_id": "don-001",
            "amount": 100,
            "account_mappings": {"debit": ctx["cash"], "credit": ctx["rev"]},
            "use_default_accounts": False,
            "require_approval": False,
        },
    )
    assert execute.status_code == 201
    assert execute.json()["data"]["status"] == "posted"


@pytest.mark.asyncio
async def test_kernel_port_execute_posting():
    slug = "posting-port"
    ctx = await _provision_hospital(slug)
    kernel = get_financial_kernel()

    result = await kernel.execute_posting(
        tenant_id=slug,
        rule_id="hospital_billing",
        source_context="hospital",
        source_document_id="port-001",
        currency="USD",
        correlation_id="test-corr",
        amount=150,
        account_mappings={"debit": ctx["ar"], "credit": ctx["rev"]},
    )
    assert result.journal_id
    assert result.status == "draft"
