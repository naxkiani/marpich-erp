"""Banking Security Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_security_platform_service,
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
    get_banking_security_platform_service()
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
        json={"email": "sec@bank.dev", "password": "SecurePass123!", "display_name": "Sec Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "sec@bank.dev", "password": "SecurePass123!"},
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
    await get_banking_security_platform_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


@pytest.mark.asyncio
async def test_security_catalog(client):
    slug = "seccat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/security/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "role_based_access" in caps
    assert "maker_checker" in caps
    assert "four_eyes_principle" in caps
    assert "immutable_audit_trail" in caps
    assert "policy_driven_approval" in caps


@pytest.mark.asyncio
async def test_maker_checker_four_eyes_flow(client):
    slug = "secmc"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    submit = await client.post(
        "/api/v1/banking/security/approvals",
        headers=headers,
        json={
            "action_type": "transfer",
            "resource_id": "txn-001",
            "maker_id": "maker-1",
            "payload": {"amount": 150000},
            "required_approvals": 2,
        },
    )
    assert submit.status_code == 201
    req_id = submit.json()["data"]["id"]
    assert submit.json()["data"]["digital_signature"] is not None

    first = await client.post(
        f"/api/v1/banking/security/approvals/{req_id}/approve",
        headers=headers,
        json={"approver_id": "checker-1"},
    )
    assert first.status_code == 200
    assert first.json()["data"]["status"] == "pending"

    second = await client.post(
        f"/api/v1/banking/security/approvals/{req_id}/approve",
        headers=headers,
        json={"approver_id": "checker-2"},
    )
    assert second.status_code == 200
    assert second.json()["data"]["status"] == "approved"


@pytest.mark.asyncio
async def test_limits_velocity_and_risk(client):
    slug = "seclim"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    limits = await client.post(
        "/api/v1/banking/security/limits/check",
        headers=headers,
        json={"user_id": "user-1", "amount": 5000.0},
    )
    assert limits.status_code == 200
    assert limits.json()["data"]["allowed"] is True

    risk = await client.post(
        "/api/v1/banking/security/risk/assess",
        headers=headers,
        json={"user_id": "user-1", "amount": 1000.0, "device_trusted": True},
    )
    assert risk.status_code == 200
    assert risk.json()["data"]["level"] == "allow"


@pytest.mark.asyncio
async def test_device_session_monitoring(client):
    slug = "secdev"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    device = await client.post(
        "/api/v1/banking/security/devices/register",
        headers=headers,
        json={"user_id": "user-1", "device_fingerprint": "fp-abc-123"},
    )
    assert device.status_code == 201

    verified = await client.post(
        "/api/v1/banking/security/devices/verify",
        headers=headers,
        json={"user_id": "user-1", "device_fingerprint": "fp-abc-123"},
    )
    assert verified.status_code == 200
    assert verified.json()["data"]["trusted"] is True

    session = await client.post(
        "/api/v1/banking/security/sessions/register",
        headers=headers,
        json={"user_id": "user-1", "device_id": verified.json()["data"]["id"], "ip_address": "10.0.0.1"},
    )
    assert session.status_code == 201
    session_id = session.json()["data"]["id"]

    heartbeat = await client.post(
        f"/api/v1/banking/security/sessions/{session_id}/heartbeat",
        headers=headers,
        json={"risk_score": 85.0},
    )
    assert heartbeat.status_code == 200


@pytest.mark.asyncio
async def test_authorize_encrypt_freeze_audit(client):
    slug = "secauth"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    auth = await client.post(
        "/api/v1/banking/security/authorize",
        headers=headers,
        json={
            "user_id": "maker-1",
            "roles": ["admin"],
            "action_type": "transfer",
            "resource_id": "txn-100",
            "amount": 500.0,
        },
    )
    assert auth.status_code == 200
    assert auth.json()["data"]["authorized"] is True

    enc = await client.post(
        "/api/v1/banking/security/encrypt",
        headers=headers,
        json={"payload": {"account": "12345", "balance": 1000}},
    )
    assert enc.status_code == 200
    assert "encrypted" in enc.json()["data"]

    sig = await client.post(
        "/api/v1/banking/security/sign",
        headers=headers,
        json={"resource_id": "txn-100", "payload": {"amount": 500}, "signer_id": "maker-1"},
    )
    assert sig.status_code == 200
    assert "signature" in sig.json()["data"]

    freeze = await client.post(
        "/api/v1/banking/security/freeze",
        headers=headers,
        json={"activated_by": "admin-1", "reason": "fraud_investigation"},
    )
    assert freeze.status_code == 201

    blocked = await client.post(
        "/api/v1/banking/security/authorize",
        headers=headers,
        json={
            "user_id": "maker-1",
            "roles": ["admin"],
            "action_type": "transfer",
            "resource_id": "txn-101",
            "amount": 100.0,
        },
    )
    assert blocked.status_code == 400

    release = await client.post(
        "/api/v1/banking/security/freeze/release",
        headers=headers,
        json={"released_by": "admin-1"},
    )
    assert release.status_code == 200

    audit = await client.get("/api/v1/banking/security/audit", headers=headers)
    assert audit.status_code == 200
    assert len(audit.json()["data"]) >= 1

    verify = await client.get("/api/v1/banking/security/audit/verify", headers=headers)
    assert verify.status_code == 200
    assert verify.json()["data"]["valid"] is True

    dash = await client.get("/api/v1/banking/security/dashboard", headers=headers)
    assert dash.status_code == 200
    assert "audit_entries" in dash.json()["data"]
