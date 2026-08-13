"""P201-A3 ports — credential lifecycle orchestration (no crypto in EILMP)."""
from __future__ import annotations

from typing import Protocol


class ICredentialLifecyclePort(Protocol):
    async def require_password_change(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict: ...

    async def request_mfa_enrollment(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict: ...

    async def revoke_passkeys(
        self, *, tenant_id: str, user_id: str, correlation_id: str
    ) -> dict: ...

    async def get_credential_status(self, *, tenant_id: str, user_id: str) -> dict: ...
