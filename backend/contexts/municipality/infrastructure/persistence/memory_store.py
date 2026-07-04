"""Municipality in-memory repositories."""
from __future__ import annotations

from contexts.municipality.domain.aggregates.permit import Permit
from contexts.municipality.domain.aggregates.service_request import ServiceRequest, ServiceRequestStatus
from contexts.municipality.domain.aggregates.utility_account import UtilityAccount
from contexts.municipality.domain.ports.repositories import (
    IPermitRepository,
    IServiceRequestRepository,
    IUtilityAccountRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class MunicipalityMemoryStore:
    permits: dict[str, Permit] = {}
    service_requests: dict[str, ServiceRequest] = {}
    utility_accounts: dict[str, UtilityAccount] = {}

    @classmethod
    def reset(cls) -> None:
        cls.permits.clear()
        cls.service_requests.clear()
        cls.utility_accounts.clear()


class InMemoryPermitRepository(IPermitRepository):
    async def save(self, permit: Permit) -> None:
        MunicipalityMemoryStore.permits[str(permit.id)] = permit

    async def find_by_id(self, tenant_id: str, permit_id: UniqueId) -> Permit | None:
        p = MunicipalityMemoryStore.permits.get(str(permit_id))
        return p if p and p.tenant_id == tenant_id else None

    async def list_permits(self, tenant_id: str) -> list[Permit]:
        return [p for p in MunicipalityMemoryStore.permits.values() if p.tenant_id == tenant_id]


class InMemoryServiceRequestRepository(IServiceRequestRepository):
    async def save(self, request: ServiceRequest) -> None:
        MunicipalityMemoryStore.service_requests[str(request.id)] = request

    async def find_by_id(self, tenant_id: str, request_id: UniqueId) -> ServiceRequest | None:
        r = MunicipalityMemoryStore.service_requests.get(str(request_id))
        return r if r and r.tenant_id == tenant_id else None

    async def list_open(self, tenant_id: str) -> list[ServiceRequest]:
        return [
            r
            for r in MunicipalityMemoryStore.service_requests.values()
            if r.tenant_id == tenant_id and r.status != ServiceRequestStatus.CLOSED
        ]


class InMemoryUtilityAccountRepository(IUtilityAccountRepository):
    async def save(self, account: UtilityAccount) -> None:
        MunicipalityMemoryStore.utility_accounts[str(account.id)] = account

    async def find_by_id(self, tenant_id: str, account_id: UniqueId) -> UtilityAccount | None:
        a = MunicipalityMemoryStore.utility_accounts.get(str(account_id))
        return a if a and a.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, account_number: str) -> UtilityAccount | None:
        for a in MunicipalityMemoryStore.utility_accounts.values():
            if a.tenant_id == tenant_id and a.account_number == account_number.upper():
                return a
        return None
