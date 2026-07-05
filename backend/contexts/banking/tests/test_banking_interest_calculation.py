"""Interest Calculation Engine tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_interest_calculation_service,
    reset_banking_customer_account_service,
)
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from contexts.policy.infrastructure.persistence.memory_store import PolicyMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PolicyMemoryStore.reset()
    reset_financial_kernel_service()
    reset_banking_customer_account_service()
    reset_policy_service()
    get_financial_kernel_service()
    get_banking_customer_account_service()
    get_banking_interest_calculation_service()
    get_policy_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "int@bank.dev", "password": "SecurePass123!", "display_name": "Interest Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "int@bank.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_banking_customer_account_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )
    await get_banking_interest_calculation_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


@pytest.mark.asyncio
async def test_interest_catalog(client):
    slug = "intcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/interest/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "daily" in caps
    assert "monthly" in caps
    assert "annual" in caps
    assert "simple" in caps
    assert "compound" in caps
    assert "profit_sharing" in caps
    assert "grace_period" in caps
    assert "penalty_interest" in caps
    assert "fixed" in caps
    assert "floating" in caps
    assert "promotional" in caps
    assert "historical_rate_changes" in caps
    assert "calculation_audit_history" in caps
    assert "simulation_mode" in caps
    assert "configurable_policies" in caps


@pytest.mark.asyncio
async def test_simple_daily_calculation_with_audit(client):
    slug = "intcalc"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    calc = await client.post(
        "/api/v1/banking/interest/calculate",
        headers=headers,
        json={
            "product_context": "deposit",
            "principal": 100000.0,
            "frequency": "daily",
            "method": "simple",
            "days": 30,
            "source_ref": "DEP-TEST-001",
        },
    )
    assert calc.status_code == 201
    data = calc.json()["data"]
    assert data["interest_amount"] > 0
    assert data["audit"]["mode"] == "production"
    assert data["audit"]["method"] == "simple"
    assert "policy_snapshot" in data["audit"]

    audit = await client.get("/api/v1/banking/interest/audit", headers=headers)
    assert audit.status_code == 200
    assert len(audit.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_compound_monthly_simulation(client):
    slug = "intsim"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    sim = await client.post(
        "/api/v1/banking/interest/simulate",
        headers=headers,
        json={
            "product_context": "loan",
            "principal": 50000.0,
            "frequency": "monthly",
            "method": "compound",
            "periods": 12,
        },
    )
    assert sim.status_code == 201
    data = sim.json()["data"]
    assert data["interest_amount"] > 0
    assert data["audit"]["mode"] == "simulation"


@pytest.mark.asyncio
async def test_floating_rate_profile_and_history(client):
    slug = "intrate"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    profile = await client.post(
        "/api/v1/banking/interest/profiles",
        headers=headers,
        json={
            "product_context": "deposit",
            "rate_type": "floating",
            "rate_annual": 5.0,
            "index_ref": "SOFR",
            "index_rate_annual": 4.0,
            "spread_bps": 150,
        },
    )
    assert profile.status_code == 201
    profile_id = profile.json()["data"]["id"]
    assert profile.json()["data"]["rate_annual"] == 5.5

    change = await client.post(
        f"/api/v1/banking/interest/profiles/{profile_id}/rate-changes",
        headers=headers,
        json={"new_rate_annual": 6.0, "reason": "market adjustment"},
    )
    assert change.status_code == 201

    history = await client.get(
        f"/api/v1/banking/interest/profiles/{profile_id}/rate-history",
        headers=headers,
    )
    assert history.status_code == 200
    assert len(history.json()["data"]) == 1
    assert history.json()["data"][0]["new_rate_annual"] == 6.0


@pytest.mark.asyncio
async def test_penalty_interest_on_overdue(client):
    slug = "intpen"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    calc = await client.post(
        "/api/v1/banking/interest/calculate",
        headers=headers,
        json={
            "product_context": "loan",
            "principal": 20000.0,
            "frequency": "daily",
            "days": 30,
            "days_overdue": 15,
        },
    )
    assert calc.status_code == 201
    data = calc.json()["data"]
    assert data["penalty_interest"] > 0


@pytest.mark.asyncio
async def test_interest_dashboard(client):
    slug = "intdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    await client.post(
        "/api/v1/banking/interest/calculate",
        headers=headers,
        json={
            "product_context": "generic",
            "principal": 10000.0,
            "frequency": "annual",
            "periods": 1,
        },
    )

    dash = await client.get("/api/v1/banking/interest/dashboard", headers=headers)
    assert dash.status_code == 200
    assert dash.json()["data"]["summary"]["calculation_count"] >= 1
