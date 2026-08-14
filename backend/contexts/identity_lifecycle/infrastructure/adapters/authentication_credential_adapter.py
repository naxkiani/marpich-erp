"""Credential lifecycle adapter → Authentication SoR (WebAuthn passkeys only)."""
from __future__ import annotations

from contexts.authentication.container import get_authentication_service


class AuthenticationCredentialAdapter:
    async def revoke_passkeys(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict:
        auth = get_authentication_service()
        listed = await auth.list_passkeys(tenant_id, user_id)
        if not listed.succeeded:
            # No passkeys / feature off — treat as empty revoke set.
            return {
                "user_id": user_id,
                "revoked": [],
                "count": 0,
                "correlation_id": correlation_id,
            }
        revoked: list[str] = []
        for item in listed.unwrap():
            ref = str(item.get("credential_ref") or item.get("ref") or "")
            if not ref:
                continue
            result = await auth.revoke_passkey(tenant_id, user_id, ref)
            if result.succeeded:
                revoked.append(ref)
        return {
            "user_id": user_id,
            "revoked": revoked,
            "count": len(revoked),
            "correlation_id": correlation_id,
        }
