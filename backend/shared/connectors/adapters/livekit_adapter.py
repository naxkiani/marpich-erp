"""LiveKit connector adapter — AccessToken JWT via Integration Platform.

Sandbox (no api_secret): deterministic simulated `lk_` tokens for tests/dev.
Production: real LiveKit Access Token (HS256 JWT with video grants).
Messenger never imports LiveKit SDK — only this connector.
"""
from __future__ import annotations

import hashlib
import hmac
import time

from jose import jwt

from shared.application.result import Result
from shared.connectors.stub_adapter import BaseConnectorAdapter
from shared.infrastructure.settings import settings


def _resolve_credentials(config: dict, secret: str) -> tuple[str, str, str, bool]:
    """Return (api_key, api_secret, url, use_real_jwt)."""
    api_key = str(
        config.get("api_key")
        or getattr(settings, "livekit_api_key", "")
        or ""
    ).strip()
    api_secret = str(
        config.get("api_secret")
        or secret
        or getattr(settings, "livekit_api_secret", "")
        or ""
    ).strip()
    url = str(
        config.get("url")
        or config.get("ws_url")
        or getattr(settings, "livekit_url", "")
        or ""
    ).strip()
    use_real = bool(api_key and api_secret)
    if not api_key:
        api_key = "dev-livekit-key"
    return api_key, api_secret, url, use_real


def _mint_livekit_access_token(
    *,
    api_key: str,
    api_secret: str,
    identity: str,
    room_name: str,
    ttl_seconds: int,
    can_publish: bool = True,
    can_subscribe: bool = True,
) -> tuple[str, int]:
    """Mint a LiveKit Access Token (JWT) compatible with livekit-server."""
    now = int(time.time())
    exp = now + max(60, ttl_seconds)
    claims = {
        "iss": api_key,
        "sub": identity,
        "nbf": now,
        "exp": exp,
        "video": {
            "roomJoin": True,
            "room": room_name,
            "canPublish": can_publish,
            "canSubscribe": can_subscribe,
        },
    }
    token = jwt.encode(claims, api_secret, algorithm="HS256")
    return token, exp


def _mint_simulated_token(
    *,
    api_key: str,
    identity: str,
    room_name: str,
    ttl_seconds: int,
) -> tuple[str, int]:
    exp = int(time.time()) + max(60, ttl_seconds)
    material = f"{room_name}:{identity}:{exp}"
    digest = hmac.new(api_key.encode(), material.encode(), hashlib.sha256).hexdigest()
    return f"lk_{digest}", exp


class LiveKitAdapter(BaseConnectorAdapter):
    def __init__(self) -> None:
        super().__init__(
            "livekit",
            ["create_room_token", "create_room", "test_connection"],
        )

    async def test_connection(self, *, config: dict, secret: str = "") -> Result[dict]:
        api_key, api_secret, url, use_real = _resolve_credentials(config, secret)
        return Result.ok(
            {
                "connector_type": self.connector_type,
                "connected": True,
                "simulated": not use_real,
                "url": url or None,
                "api_key_present": bool(api_key and api_key != "dev-livekit-key"),
                "api_secret_present": bool(api_secret),
            }
        )

    async def execute(
        self,
        *,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        if operation not in self._operations:
            return Result.fail(f"unsupported_operation:{operation}")
        if operation == "test_connection":
            return await self.test_connection(config=config, secret=secret)

        api_key, api_secret, url, use_real = _resolve_credentials(config, secret)
        ttl = int(config.get("ttl_seconds") or getattr(settings, "livekit_token_ttl_seconds", 3600) or 3600)

        if operation == "create_room":
            room = str(payload.get("room_name") or f"room-{int(time.time())}")
            # LiveKit creates rooms on first join; optional RoomService deferred.
            return Result.ok(
                {
                    "connector_type": self.connector_type,
                    "operation": operation,
                    "status": "completed",
                    "idempotency_key": idempotency_key or None,
                    "result": {
                        "room_name": room,
                        "url": url or None,
                        "simulated": not use_real,
                    },
                }
            )

        room_name = str(payload.get("room_name") or "")
        identity = str(payload.get("identity") or "anonymous")
        if not room_name:
            return Result.fail("livekit.errors.room_name_required")
        if not identity.strip():
            return Result.fail("livekit.errors.identity_required")

        if use_real:
            token, exp = _mint_livekit_access_token(
                api_key=api_key,
                api_secret=api_secret,
                identity=identity,
                room_name=room_name,
                ttl_seconds=ttl,
                can_publish=bool(payload.get("can_publish", True)),
                can_subscribe=bool(payload.get("can_subscribe", True)),
            )
        else:
            token, exp = _mint_simulated_token(
                api_key=api_key,
                identity=identity,
                room_name=room_name,
                ttl_seconds=ttl,
            )

        return Result.ok(
            {
                "connector_type": self.connector_type,
                "operation": operation,
                "status": "completed",
                "idempotency_key": idempotency_key or None,
                "result": {
                    "token": token,
                    "room_name": room_name,
                    "identity": identity,
                    "expires_at": exp,
                    "url": url or None,
                    "simulated": not use_real,
                },
            }
        )
