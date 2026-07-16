#!/usr/bin/env python3
"""LiveKit secrets smoke — Integration connector only (no messenger domain).

Usage:
  cd backend && .venv/bin/python scripts/smoke_livekit_secrets.py

Exit codes:
  0  — OK (simulated mode when secrets absent, or real JWT verified)
  1  — secrets present but mint/verify failed
  2  — usage / unexpected error

Env (from settings / process):
  LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL (optional), LIVEKIT_TOKEN_TTL_SECONDS

Never prints secret values. Simulated tokens already cover messaging without A/V.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Allow running from repo root or backend/
_BACKEND = Path(__file__).resolve().parents[1]
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))


async def _run() -> int:
    from jose import jwt

    from shared.connectors.adapters.livekit_adapter import LiveKitAdapter
    from shared.infrastructure.settings import settings

    api_key = (settings.livekit_api_key or "").strip()
    api_secret = (settings.livekit_api_secret or "").strip()
    url = (settings.livekit_url or "").strip()
    ttl = int(settings.livekit_token_ttl_seconds or 3600)

    adapter = LiveKitAdapter()
    probe = await adapter.test_connection(
        config={"api_key": api_key or None, "api_secret": api_secret or None, "url": url or None},
        secret=api_secret,
    )
    if not probe.succeeded:
        print(f"FAIL test_connection: {probe.error}", file=sys.stderr)
        return 1

    meta = probe.unwrap()
    if meta.get("simulated"):
        print(
            "OK LiveKit smoke — simulated mode "
            "(LIVEKIT_API_KEY + LIVEKIT_API_SECRET not set). "
            "Messaging tokens work; set secrets only when you need real A/V."
        )
        return 0

    key_hint = f"{api_key[:4]}…" if len(api_key) >= 4 else "(short)"
    print(f"Secrets detected — minting AccessToken (api_key={key_hint}, url={'set' if url else 'unset'})")

    minted = await adapter.execute(
        operation="create_room_token",
        payload={
            "room_name": "marpich-smoke-room",
            "identity": "smoke-probe",
            "can_publish": True,
            "can_subscribe": True,
        },
        config={
            "api_key": api_key,
            "api_secret": api_secret,
            "url": url or None,
            "ttl_seconds": min(ttl, 600),
        },
        secret=api_secret,
        idempotency_key="livekit-secrets-smoke",
    )
    if not minted.succeeded:
        print(f"FAIL create_room_token: {minted.error}", file=sys.stderr)
        return 1

    result = minted.unwrap()["result"]
    if result.get("simulated"):
        print("FAIL expected real JWT but adapter returned simulated=true", file=sys.stderr)
        return 1

    token = str(result.get("token") or "")
    if not token or token.startswith("lk_"):
        print("FAIL token missing or still simulated prefix", file=sys.stderr)
        return 1

    try:
        claims = jwt.decode(
            token,
            api_secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
    except Exception as exc:  # noqa: BLE001 — smoke reports any verify failure
        print(f"FAIL JWT verify: {exc}", file=sys.stderr)
        return 1

    if claims.get("iss") != api_key:
        print(f"FAIL iss mismatch: got {claims.get('iss')!r}", file=sys.stderr)
        return 1
    if claims.get("sub") != "smoke-probe":
        print(f"FAIL sub mismatch: got {claims.get('sub')!r}", file=sys.stderr)
        return 1
    video = claims.get("video") if isinstance(claims.get("video"), dict) else {}
    if video.get("room") != "marpich-smoke-room" or not video.get("roomJoin"):
        print(f"FAIL video grants: {video!r}", file=sys.stderr)
        return 1

    print(
        "OK LiveKit secrets smoke — real AccessToken mint + HS256 verify passed. "
        "Room join still requires a LiveKit client against LIVEKIT_URL."
    )
    return 0


def main() -> None:
    try:
        raise SystemExit(asyncio.run(_run()))
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL unexpected: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
