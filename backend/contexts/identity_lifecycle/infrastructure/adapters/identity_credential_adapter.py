"""Credential lifecycle adapter → Identity SoR (password must-change + MFA status)."""
from __future__ import annotations

from contexts.identity.container import get_identity_service
from contexts.identity_lifecycle.domain.ports.credentials import ICredentialLifecyclePort


class IdentityCredentialAdapter(ICredentialLifecyclePort):
    async def require_password_change(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict:
        identity = get_identity_service()
        cred = await identity.get_user_credential(tenant_id, user_id)
        if not cred.succeeded:
            raise ValueError(cred.error or "identity.errors.user_not_found")
        data = cred.unwrap()
        result = await identity.update_password_hash(
            tenant_id=tenant_id,
            user_id=user_id,
            password_hash=str(data["password_hash"]),
            hash_algorithm=str(data.get("password_hash_algorithm") or "argon2"),
            must_change_password=True,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            raise ValueError(result.error or "identity.errors.password_update_failed")
        return {"user_id": user_id, "password_must_change": True, "action": "require_password_change"}

    async def request_mfa_enrollment(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict:
        cred = await get_identity_service().get_user_credential(tenant_id, user_id)
        if not cred.succeeded:
            raise ValueError(cred.error or "identity.errors.user_not_found")
        data = cred.unwrap()
        return {
            "user_id": user_id,
            "mfa_enabled": bool(data.get("mfa_enabled")),
            "enrollment_required": not bool(data.get("mfa_enabled")),
            "action": "request_mfa_enrollment",
            "correlation_id": correlation_id,
        }

    async def revoke_passkeys(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict:
        # Passkey crypto owned by authentication — see AuthenticationCredentialAdapter.
        return {
            "user_id": user_id,
            "delegated_to": "authentication",
            "action": "revoke_passkeys",
            "correlation_id": correlation_id,
        }

    async def get_credential_status(self, *, tenant_id: str, user_id: str) -> dict:
        cred = await get_identity_service().get_user_credential(tenant_id, user_id)
        if not cred.succeeded:
            raise ValueError(cred.error or "identity.errors.user_not_found")
        data = cred.unwrap()
        return {
            "user_id": user_id,
            "password_must_change": bool(data.get("password_must_change")),
            "mfa_enabled": bool(data.get("mfa_enabled")),
            "status": data.get("status"),
        }
