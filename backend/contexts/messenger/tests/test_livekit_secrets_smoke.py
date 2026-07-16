"""Optional LiveKit secrets smoke — skips when LIVEKIT_* secrets are absent.

Simulated `lk_` tokens already cover messaging. Run with real secrets when A/V is needed:
  LIVEKIT_API_KEY=… LIVEKIT_API_SECRET=… .venv/bin/pytest \\
    contexts/messenger/tests/test_livekit_secrets_smoke.py -q
"""
from __future__ import annotations

import os

import pytest
from jose import jwt

from shared.connectors.adapters.livekit_adapter import LiveKitAdapter


def _secrets_present() -> bool:
    return bool(
        (os.environ.get("LIVEKIT_API_KEY") or "").strip()
        and (os.environ.get("LIVEKIT_API_SECRET") or "").strip()
    )


pytestmark = pytest.mark.skipif(
    not _secrets_present(),
    reason="LIVEKIT_API_KEY + LIVEKIT_API_SECRET not set (simulated mode OK for messaging)",
)


@pytest.mark.asyncio
async def test_livekit_env_secrets_mint_verifiable_jwt():
    api_key = os.environ["LIVEKIT_API_KEY"].strip()
    api_secret = os.environ["LIVEKIT_API_SECRET"].strip()
    url = (os.environ.get("LIVEKIT_URL") or "").strip()

    adapter = LiveKitAdapter()
    probe = await adapter.test_connection(
        config={"api_key": api_key, "api_secret": api_secret, "url": url or None},
        secret=api_secret,
    )
    assert probe.succeeded
    assert probe.unwrap()["simulated"] is False

    minted = await adapter.execute(
        operation="create_room_token",
        payload={"room_name": "pytest-smoke-room", "identity": "pytest-smoke"},
        config={
            "api_key": api_key,
            "api_secret": api_secret,
            "url": url or None,
            "ttl_seconds": 300,
        },
        secret=api_secret,
        idempotency_key="pytest-livekit-smoke",
    )
    assert minted.succeeded
    result = minted.unwrap()["result"]
    assert result["simulated"] is False
    token = result["token"]
    assert not token.startswith("lk_")

    claims = jwt.decode(
        token,
        api_secret,
        algorithms=["HS256"],
        options={"verify_aud": False},
    )
    assert claims["iss"] == api_key
    assert claims["sub"] == "pytest-smoke"
    assert claims["video"]["room"] == "pytest-smoke-room"
