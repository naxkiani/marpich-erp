"""Ports for cross-tenant delegation / partner / external stores (P200-B8)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.identity_federation.domain.aggregates.cross_tenant_platform import (
    DelegationAgreement,
    ExternalIdentity,
    PartnerAccess,
)


class IDelegationRepository(ABC):
    @abstractmethod
    async def save(self, agreement: DelegationAgreement) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[DelegationAgreement]: ...

    @abstractmethod
    def next_ref(self, tenant_id: str) -> str: ...


class IPartnerAccessRepository(ABC):
    @abstractmethod
    async def save(self, partner: PartnerAccess) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[PartnerAccess]: ...

    @abstractmethod
    def next_ref(self, tenant_id: str) -> str: ...


class IExternalIdentityRepository(ABC):
    @abstractmethod
    async def save(self, identity: ExternalIdentity) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[ExternalIdentity]: ...

    @abstractmethod
    def next_ref(self, tenant_id: str) -> str: ...
