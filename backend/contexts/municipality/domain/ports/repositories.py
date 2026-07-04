"""Municipality repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.municipality.domain.aggregates.permit import Permit
from contexts.municipality.domain.aggregates.service_request import ServiceRequest
from contexts.municipality.domain.aggregates.utility_account import UtilityAccount
from shared.domain.value_objects.unique_id import UniqueId


class IPermitRepository(ABC):
    @abstractmethod
    async def save(self, permit: Permit) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, permit_id: UniqueId) -> Permit | None: ...

    @abstractmethod
    async def list_permits(self, tenant_id: str) -> list[Permit]: ...


class IServiceRequestRepository(ABC):
    @abstractmethod
    async def save(self, request: ServiceRequest) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, request_id: UniqueId) -> ServiceRequest | None: ...

    @abstractmethod
    async def list_open(self, tenant_id: str) -> list[ServiceRequest]: ...


class IUtilityAccountRepository(ABC):
    @abstractmethod
    async def save(self, account: UtilityAccount) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, account_id: UniqueId) -> UtilityAccount | None: ...

    @abstractmethod
    async def find_by_number(self, tenant_id: str, account_number: str) -> UtilityAccount | None: ...
