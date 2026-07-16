"""P5.3 — Messenger E2EE client ciphertext + real/simulated LiveKit AccessToken."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient
from jose import jwt

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.messenger.container import get_messenger_service, reset_messenger_service
from contexts.messenger.infrastructure.persistence.memory_store import MessengerMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.connectors.adapters.livekit_adapter import LiveKitAdapter
from shared.connectors.builtins import register_builtin_connectors
from shared.connectors.registry import reset_connector_registry
from shared.infrastructure.messaging.event_fabric import EventFabric
from shared.infrastructure.settings import settings


@pytest.fixture(autouse=True)
def reset_all(monkeypatch):
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    MessengerMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_connector_registry()
    register_builtin_connectors()
    reset_platform_service()
    reset_messenger_service()
    get_messenger_service()
    # Ensure sandbox mode for API tests (no real secrets)
    monkeypatch.setattr(settings, "livekit_api_key", "")
    monkeypatch.setattr(settings, "livekit_api_secret", "")
    monkeypatch.setattr(settings, "livekit_url", "")
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str, email: str) -> dict[str, str]:
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Messenger Co", "slug": tenant, "industry_pack": "university"},
    )
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Chat Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {login.json()['data']['access_token']}",
    }


@pytest.mark.asyncio
async def test_e2ee_rejects_plaintext_and_accepts_ciphertext(client):
    headers = await _admin(client, "p53-e2ee", "e2ee@marpich.dev")
    opened = await client.post(
        "/api/v1/messenger/conversations",
        json={"title": "Secure", "member_ids": ["peer-1"], "e2ee_enabled": True},
        headers=headers,
    )
    assert opened.status_code == 201, opened.text
    cid = opened.json()["data"]["id"]

    rejected = await client.post(
        f"/api/v1/messenger/conversations/{cid}/messages",
        json={"body": "secret in clear"},
        headers=headers,
    )
    assert rejected.status_code == 400
    assert "ciphertext_required" in rejected.json()["detail"]

    sent = await client.post(
        f"/api/v1/messenger/conversations/{cid}/messages",
        json={
            "ciphertext": "v1:base64ciphertextblob",
            "ciphertext_type": "application/x-marpich-e2ee",
        },
        headers=headers,
    )
    assert sent.status_code == 201, sent.text
    msg = sent.json()["data"]
    assert msg["body"] == ""
    assert msg["ciphertext"] == "v1:base64ciphertextblob"
    assert msg["ciphertext_type"] == "application/x-marpich-e2ee"


@pytest.mark.asyncio
async def test_livekit_token_route_and_simulated_prefix(client):
    headers = await _admin(client, "p53-lk", "lk@marpich.dev")
    opened = await client.post(
        "/api/v1/messenger/conversations",
        json={
            "title": "AV room",
            "member_ids": ["peer-1"],
            "e2ee_enabled": False,
            "issue_livekit_token": True,
        },
        headers=headers,
    )
    assert opened.status_code == 201, opened.text
    data = opened.json()["data"]
    assert data["livekit_token"].startswith("lk_")
    assert data["livekit_simulated"] is True
    cid = data["id"]

    refresh = await client.post(
        f"/api/v1/messenger/conversations/{cid}/livekit-token",
        headers=headers,
    )
    assert refresh.status_code == 200, refresh.text
    token_data = refresh.json()["data"]
    assert token_data["token"].startswith("lk_")
    assert token_data["simulated"] is True
    assert token_data["room_name"]


@pytest.mark.asyncio
async def test_livekit_adapter_mints_real_jwt_when_secrets_present():
    adapter = LiveKitAdapter()
    result = await adapter.execute(
        operation="create_room_token",
        payload={"room_name": "room-a", "identity": "user-1"},
        config={
            "api_key": "APItestkey",
            "api_secret": "secret-for-hs256-signing-tests",
            "url": "wss://demo.livekit.cloud",
            "ttl_seconds": 600,
        },
        secret="",
        idempotency_key="t1",
    )
    assert result.succeeded
    payload = result.unwrap()["result"]
    assert payload["simulated"] is False
    assert not payload["token"].startswith("lk_")
    claims = jwt.get_unverified_claims(payload["token"])
    assert claims["iss"] == "APItestkey"
    assert claims["sub"] == "user-1"
    assert claims["video"]["room"] == "room-a"
    assert claims["video"]["roomJoin"] is True
    # Verify signature
    decoded = jwt.decode(
        payload["token"],
        "secret-for-hs256-signing-tests",
        algorithms=["HS256"],
        options={"verify_aud": False},
    )
    assert decoded["sub"] == "user-1"


@pytest.mark.asyncio
async def test_plaintext_ok_when_e2ee_disabled(client):
    headers = await _admin(client, "p53-plain", "plain@marpich.dev")
    opened = await client.post(
        "/api/v1/messenger/conversations",
        json={"title": "Open chat", "member_ids": ["peer-1"], "e2ee_enabled": False},
        headers=headers,
    )
    cid = opened.json()["data"]["id"]
    sent = await client.post(
        f"/api/v1/messenger/conversations/{cid}/messages",
        json={"body": "hello"},
        headers=headers,
    )
    assert sent.status_code == 201, sent.text
    assert sent.json()["data"]["body"] == "hello"
    assert sent.json()["data"]["ciphertext"] is None
