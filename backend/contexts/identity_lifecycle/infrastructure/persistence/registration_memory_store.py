"""In-memory registration store (P201-A)."""
from __future__ import annotations

from contexts.identity_lifecycle.domain.aggregates.registration_onboarding import (
    IdentityRegistration,
)
from contexts.identity_lifecycle.domain.ports.registration_repositories import (
    IIdentityRegistrationRepository,
)


class InMemoryRegistrationStore:
    registrations: dict[str, IdentityRegistration] = {}
    counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.registrations.clear()
        cls.counter.clear()


class InMemoryIdentityRegistrationRepository(IIdentityRegistrationRepository):
    async def save(self, registration: IdentityRegistration) -> None:
        InMemoryRegistrationStore.registrations[registration.registration_ref] = registration

    async def find_by_ref(
        self, tenant_id: str, registration_ref: str
    ) -> IdentityRegistration | None:
        reg = InMemoryRegistrationStore.registrations.get(registration_ref)
        if reg and reg.tenant_id == tenant_id:
            return reg
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[IdentityRegistration]:
        return [
            r
            for r in InMemoryRegistrationStore.registrations.values()
            if r.tenant_id == tenant_id
        ]

    def next_registration_ref(self, tenant_id: str) -> str:
        n = InMemoryRegistrationStore.counter.get(tenant_id, 0) + 1
        InMemoryRegistrationStore.counter[tenant_id] = n
        return f"reg-{tenant_id}-{n:04d}"
