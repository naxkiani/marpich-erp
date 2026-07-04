"""Financial Kernel tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel, get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.infrastructure.persistence.memory_store import (
    InMemoryChartOfAccountRepository,
    InMemoryDimensionRepository,
    InMemoryFiscalPeriodRepository,
    InMemoryJournalRepository,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app
from shared.application.ports.financial_kernel import JournalLine
from shared.infrastructure.messaging.event_bus import InProcessEventBus


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
        json={"email": "cfo@kernel.dev", "password": "SecurePass123!", "display_name": "CFO"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "cfo@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_seed_healthcare_coa_on_provision():
    await get_financial_kernel_service().handle_tenant_provisioned(
        {"tenant_id": "hosp-fk", "payload": {"industry_pack": "hospital"}}
    )
    svc = get_financial_kernel_service()
    ar_code = (await svc.resolve_account_code("hosp-fk", "patient_receivables")).unwrap()
    rev_code = (await svc.resolve_account_code("hosp-fk", "patient_service_revenue")).unwrap()
    assert ar_code == "1200"
    assert rev_code == "4100"
    tree = (await svc.get_account_tree("hosp-fk")).unwrap()
    assert any(n["account_key"] == "assets" for n in tree)
    centers = (await svc.list_cost_centers("hosp-fk")).unwrap()
    assert any(c["code"] == "ER" for c in centers)


@pytest.mark.asyncio
async def test_post_journal_via_api(client):
    slug = "fk-journal"
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    ar_code = (await svc.resolve_account_code(slug, "patient_receivables")).unwrap()
    rev_code = (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap()
    headers = await _auth_headers(client, slug)

    post = await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "enc-001",
            "currency": "USD",
            "lines": [
                {"account_code": ar_code, "debit": 500.0, "credit": 0},
                {"account_code": rev_code, "debit": 0, "credit": 500.0},
            ],
        },
    )
    assert post.status_code == 201
    assert post.json()["data"]["total_debits"] == 500.0


@pytest.mark.asyncio
async def test_kernel_port_and_trial_balance():
    slug = "fk-port"
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "pos"}}
    )
    cash_code = (await svc.resolve_account_code(slug, "pos_cash")).unwrap()
    rev_code = (await svc.resolve_account_code(slug, "sales_revenue")).unwrap()
    kernel = get_financial_kernel()
    result = await kernel.post_journal(
        tenant_id=slug,
        source_context="pos",
        source_document_id="sale-99",
        lines=[
            JournalLine(account_code=cash_code, debit="100", credit="0"),
            JournalLine(account_code=rev_code, debit="0", credit="100"),
        ],
        currency="USD",
        correlation_id="corr-1",
    )
    assert result.status == "posted"
    tb = await kernel.get_trial_balance(tenant_id=slug)
    assert any(line.account_code == rev_code for line in tb)
