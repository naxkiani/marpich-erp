"""Feature flag system tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.feature_flags.container import get_feature_flag_evaluator, get_feature_flag_service, reset_feature_flag_service
from contexts.feature_flags.infrastructure.persistence.memory_store import FeatureFlagMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    FeatureFlagMemoryStore.reset()
    InProcessEventBus.reset()
    reset_feature_flag_service()
    get_feature_flag_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@flags.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@flags.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_seed_flags_on_provision():
    await get_feature_flag_service().handle_tenant_provisioned(
        {"tenant_id": "hosp", "payload": {"industry_pack": "hospital"}}
    )
    flags = await get_feature_flag_service().list_flags("hosp")
    keys = {f["key"] for f in flags.unwrap()}
    assert "saved_listings" in keys
    assert "advanced_analytics" in keys


@pytest.mark.asyncio
async def test_evaluate_industry_override():
    await get_feature_flag_service().handle_tenant_provisioned(
        {"tenant_id": "uni", "payload": {"industry_pack": "university"}}
    )
    result = await get_feature_flag_evaluator().evaluate(
        tenant_id="uni",
        keys=["advanced_analytics"],
        context={"industry_pack": "university"},
    )
    assert result["advanced_analytics"].enabled is True


@pytest.mark.asyncio
async def test_canary_rollout_and_emergency_disable(client):
    slug = "flags-canary"
    await get_feature_flag_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    headers = await _auth_headers(client, slug)

    rollout = await client.post(
        "/api/v1/feature-flags/saved_listings/rollout",
        headers=headers,
        json={"percentage": 0, "stage": "canary"},
    )
    assert rollout.status_code == 200

    evaluate = await client.post(
        "/api/v1/feature-flags/evaluate",
        headers=headers,
        json={"flags": ["saved_listings"], "context": {"user_id": "u1"}},
    )
    assert evaluate.json()["data"]["saved_listings"]["enabled"] is False

    emergency = await client.post(
        "/api/v1/feature-flags/advanced_analytics/emergency-disable",
        headers=headers,
        json={"reason": "Regression in analytics pipeline"},
    )
    assert emergency.status_code == 200
    assert emergency.json()["data"]["emergency_disabled"] is True


@pytest.mark.asyncio
async def test_ab_test_and_dashboard(client):
    slug = "flags-ab"
    headers = await _auth_headers(client, slug)

    created = await client.post(
        "/api/v1/feature-flags",
        headers=headers,
        json={"key": "checkout_v2", "name": "Checkout V2", "default_enabled": True},
    )
    assert created.status_code == 201

    ab = await client.post(
        "/api/v1/feature-flags/checkout_v2/ab-test",
        headers=headers,
        json={"variants": [{"id": "control", "weight": 50}, {"id": "treatment", "weight": 50}]},
    )
    assert ab.status_code == 200

    evaluate = await client.post(
        "/api/v1/feature-flags/evaluate",
        headers=headers,
        json={"flags": ["checkout_v2"], "context": {"user_id": "stable-user-1"}},
    )
    data = evaluate.json()["data"]["checkout_v2"]
    assert data["enabled"] is True
    assert data["variant_id"] in ("control", "treatment")

    dashboard = await client.get("/api/v1/feature-flags/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["ab_tests_running"] >= 1
