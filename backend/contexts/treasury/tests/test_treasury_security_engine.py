"""Treasury Security tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_treasury_security_service,
    reset_treasury_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_treasury_security_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _grant_admin_role(tenant: str, email: str) -> None:
    from contexts.identity.container import get_identity_service

    svc = get_identity_service()
    user = await svc._users.find_by_email(tenant, email)
    admin_role = await svc._roles.find_by_code(tenant, "admin")
    if user and admin_role and str(admin_role.id) not in user.role_ids:
        user.role_ids.append(str(admin_role.id))
        await svc._users.save(user)


async def _auth_headers(
    client: AsyncClient,
    tenant: str,
    email: str = "sec@treasury.dev",
    *,
    grant_admin: bool = False,
) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Sec User"},
        headers={"X-Tenant-ID": tenant},
    )
    if grant_admin:
        await _grant_admin_role(tenant, email)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    await get_treasury_security_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


@pytest.mark.asyncio
async def test_security_catalog(client):
    slug = "seccat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/security/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "maker_checker" in caps
    assert "four_eyes" in caps
    assert "segregation_of_duties" in caps
    assert "transaction_limits" in caps
    assert "approval_matrix" in caps
    assert "digital_signature" in caps
    assert "role_based_access" in caps
    assert "attribute_based_access" in caps
    assert "device_verification" in caps
    assert "risk_based_authentication" in caps
    assert "transaction_locking" in caps
    assert "emergency_freeze" in caps
    assert "security_policies" in caps
    assert "audit_trail" in caps
    assert len(caps) == 14


@pytest.mark.asyncio
async def test_seed_policies_limits_matrix(client):
    slug = "secseed"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    policies = await client.get("/api/v1/treasury/security/policies", headers=headers)
    assert policies.status_code == 200
    assert len(policies.json()["data"]) == 7

    limits = await client.get("/api/v1/treasury/security/limits", headers=headers)
    assert limits.status_code == 200
    assert len(limits.json()["data"]) == 4

    matrix = await client.get("/api/v1/treasury/security/matrix", headers=headers)
    assert matrix.status_code == 200
    assert len(matrix.json()["data"]) == 6


@pytest.mark.asyncio
async def test_security_policies_view(client):
    slug = "secpol"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    view = await client.get("/api/v1/treasury/security/policies/view", headers=headers)
    assert view.status_code == 200
    data = view.json()["data"]
    assert data["policy_count"] == 7
    assert "policy_types" in data
    assert "by_policy_type" in data


@pytest.mark.asyncio
async def test_maker_checker_four_eyes_flow(client):
    slug = "secmc"
    maker_headers = await _auth_headers(client, slug, "maker@treasury.dev")
    checker1_headers = await _auth_headers(
        client, slug, "checker1@treasury.dev", grant_admin=True
    )
    checker2_headers = await _auth_headers(
        client, slug, "checker2@treasury.dev", grant_admin=True
    )
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/security/operations",
        headers=maker_headers,
        json={
            "operation_type": "transfer",
            "subject_ref": "xfer-sec-001",
            "amount": 5000,
            "currency": "USD",
            "roles": ["treasury_officer"],
            "device_verified": True,
            "risk_score": 10,
        },
    )
    assert create.status_code == 201
    op_id = create.json()["data"]["id"]

    submit = await client.post(
        f"/api/v1/treasury/security/operations/{op_id}/submit",
        headers=maker_headers,
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "pending_checker"

    approve1 = await client.post(
        f"/api/v1/treasury/security/operations/{op_id}/approve",
        headers=checker1_headers,
        json={"with_signature": True},
    )
    assert approve1.status_code == 200
    assert approve1.json()["data"]["status"] == "pending_checker"

    approve2 = await client.post(
        f"/api/v1/treasury/security/operations/{op_id}/approve",
        headers=checker2_headers,
        json={"with_signature": True},
    )
    assert approve2.status_code == 200
    assert approve2.json()["data"]["status"] == "approved"
    assert len(approve2.json()["data"]["digital_signatures"]) == 2


@pytest.mark.asyncio
async def test_maker_cannot_be_checker(client):
    slug = "secmaker"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    create = await client.post(
        "/api/v1/treasury/security/operations",
        headers=headers,
        json={
            "operation_type": "payment",
            "subject_ref": "pay-001",
            "amount": 1000,
            "roles": ["treasury_officer"],
            "device_verified": True,
        },
    )
    op_id = create.json()["data"]["id"]
    await client.post(f"/api/v1/treasury/security/operations/{op_id}/submit", headers=headers)

    approve = await client.post(
        f"/api/v1/treasury/security/operations/{op_id}/approve",
        headers=headers,
        json={"with_signature": True},
    )
    assert approve.status_code == 400


@pytest.mark.asyncio
async def test_emergency_freeze_and_lock(client):
    slug = "secfreeze"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    freeze = await client.post(
        "/api/v1/treasury/security/freeze",
        headers=headers,
        json={"reason": "Suspected fraud activity"},
    )
    assert freeze.status_code == 201
    lock_id = freeze.json()["data"]["id"]

    eval_resp = await client.post(
        "/api/v1/treasury/security/evaluate",
        headers=headers,
        json={
            "maker_id": "user-1",
            "roles": ["treasury_officer"],
            "operation_type": "transfer",
            "amount": 1000,
            "device_verified": True,
        },
    )
    assert eval_resp.status_code == 200
    assert eval_resp.json()["data"]["allowed"] is False
    assert eval_resp.json()["data"]["reason"] == "emergency_freeze_active"

    release = await client.post(
        f"/api/v1/treasury/security/freeze/{lock_id}/release",
        headers=headers,
    )
    assert release.status_code == 200

    lock = await client.post(
        "/api/v1/treasury/security/locks",
        headers=headers,
        json={
            "subject_ref": "txn-locked-001",
            "subject_type": "transfer",
            "reason": "Pending investigation",
        },
    )
    assert lock.status_code == 201

    check = await client.get(
        "/api/v1/treasury/security/check-lock/txn-locked-001",
        headers=headers,
    )
    assert check.status_code == 200
    assert check.json()["data"]["locked"] is True


@pytest.mark.asyncio
async def test_access_evaluation_and_audit(client):
    slug = "secaudit"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    denied = await client.post(
        "/api/v1/treasury/security/evaluate",
        headers=headers,
        json={
            "maker_id": "user-1",
            "roles": [],
            "operation_type": "transfer",
            "amount": 1000,
        },
    )
    assert denied.status_code == 200
    assert denied.json()["data"]["allowed"] is False

    allowed = await client.post(
        "/api/v1/treasury/security/evaluate",
        headers=headers,
        json={
            "maker_id": "user-1",
            "roles": ["treasury_officer"],
            "operation_type": "transfer",
            "amount": 5000,
            "device_verified": True,
            "risk_score": 20,
        },
    )
    assert allowed.status_code == 200
    assert allowed.json()["data"]["allowed"] is True

    audit = await client.get("/api/v1/treasury/security/audit", headers=headers)
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "access_evaluated" in actions


@pytest.mark.asyncio
async def test_security_dashboard(client):
    slug = "secdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/treasury/security/dashboard", headers=headers)
    assert dash.status_code == 200
    summary = dash.json()["data"]["summary"]
    assert summary["active_policies"] == 7
    assert summary["transaction_limits"] == 4
    assert summary["approval_matrix_entries"] == 6
