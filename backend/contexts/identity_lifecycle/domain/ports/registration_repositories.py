"""Registration repository ports (P201-A)."""
from __future__ import annotations

from typing import Protocol

from contexts.identity_lifecycle.domain.aggregates.registration_onboarding import (
    IdentityRegistration,
)


class IIdentityRegistrationRepository(Protocol):
    async def save(self, registration: IdentityRegistration) -> None: ...

    async def find_by_ref(
        self, tenant_id: str, registration_ref: str
    ) -> IdentityRegistration | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[IdentityRegistration]: ...

    def next_registration_ref(self, tenant_id: str) -> str: ...
