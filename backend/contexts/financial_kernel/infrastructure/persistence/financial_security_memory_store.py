"""In-memory Financial Security persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_security import (
    MakerCheckerRequest,
    PeriodCloseRequest,
    SecurityAuditRecord,
    SecurityPolicy,
    TransactionLock,
)
from contexts.financial_kernel.domain.ports.financial_security_repositories import (
    IMakerCheckerRepository,
    IPeriodCloseRequestRepository,
    ISecurityAuditRepository,
    ISecurityPolicyRepository,
    ITransactionLockRepository,
)


class InMemorySecurityAuditRepository(ISecurityAuditRepository):
    _records: dict[str, SecurityAuditRecord] = {}
    _chain: dict[str, list[str]] = {}

    @classmethod
    def reset(cls) -> None:
        cls._records = {}
        cls._chain = {}

    async def save(self, record: SecurityAuditRecord) -> None:
        self._records[str(record.id)] = record
        self._chain.setdefault(record.tenant_id, []).append(record.tamper_hash)

    async def list_by_tenant(self, tenant_id: str) -> list[SecurityAuditRecord]:
        return [r for r in self._records.values() if r.tenant_id == tenant_id]

    async def list_by_resource(
        self, tenant_id: str, resource_type: str, resource_id: str
    ) -> list[SecurityAuditRecord]:
        return [
            r
            for r in self._records.values()
            if r.tenant_id == tenant_id
            and r.resource_type == resource_type
            and r.resource_id == resource_id
        ]

    async def last_tamper_hash(self, tenant_id: str) -> str | None:
        chain = self._chain.get(tenant_id, [])
        return chain[-1] if chain else None


class InMemorySecurityPolicyRepository(ISecurityPolicyRepository):
    _policies: dict[str, SecurityPolicy] = {}

    @classmethod
    def reset(cls) -> None:
        cls._policies = {}

    async def save(self, policy: SecurityPolicy) -> None:
        self._policies[str(policy.id)] = policy

    async def find_by_id(self, policy_id: str) -> SecurityPolicy | None:
        return self._policies.get(policy_id)

    async def list_by_tenant(self, tenant_id: str) -> list[SecurityPolicy]:
        return [p for p in self._policies.values() if p.tenant_id == tenant_id]

    async def find_for_resource(self, tenant_id: str, resource_type: str) -> list[SecurityPolicy]:
        return [
            p
            for p in self._policies.values()
            if p.tenant_id == tenant_id and p.resource_type == resource_type and p.is_active
        ]


class InMemoryMakerCheckerRepository(IMakerCheckerRepository):
    _requests: dict[str, MakerCheckerRequest] = {}

    @classmethod
    def reset(cls) -> None:
        cls._requests = {}

    async def save(self, request: MakerCheckerRequest) -> None:
        self._requests[str(request.id)] = request
        self._requests[f"idemp:{request.tenant_id}:{request.idempotency_key}"] = request

    async def find_by_id(self, request_id: str) -> MakerCheckerRequest | None:
        r = self._requests.get(request_id)
        return r if isinstance(r, MakerCheckerRequest) else None

    async def find_by_idempotency(self, tenant_id: str, key: str) -> MakerCheckerRequest | None:
        r = self._requests.get(f"idemp:{tenant_id}:{key}")
        return r if isinstance(r, MakerCheckerRequest) else None

    async def list_by_tenant(self, tenant_id: str) -> list[MakerCheckerRequest]:
        seen: set[str] = set()
        result = []
        for r in self._requests.values():
            if isinstance(r, MakerCheckerRequest) and r.tenant_id == tenant_id and str(r.id) not in seen:
                seen.add(str(r.id))
                result.append(r)
        return result


class InMemoryTransactionLockRepository(ITransactionLockRepository):
    _locks: dict[str, TransactionLock] = {}

    @classmethod
    def reset(cls) -> None:
        cls._locks = {}

    async def save(self, lock: TransactionLock) -> None:
        self._locks[str(lock.id)] = lock
        if lock.is_active:
            self._locks[f"active:{lock.tenant_id}:{lock.resource_type}:{lock.resource_id}"] = lock

    async def find_active(
        self, tenant_id: str, resource_type: str, resource_id: str
    ) -> TransactionLock | None:
        lock = self._locks.get(f"active:{tenant_id}:{resource_type}:{resource_id}")
        if isinstance(lock, TransactionLock) and lock.is_active:
            return lock
        return None

    async def find_by_id(self, lock_id: str) -> TransactionLock | None:
        lock = self._locks.get(lock_id)
        return lock if isinstance(lock, TransactionLock) else None

    async def list_active(self, tenant_id: str) -> list[TransactionLock]:
        seen: set[str] = set()
        return [
            l
            for l in self._locks.values()
            if isinstance(l, TransactionLock)
            and l.tenant_id == tenant_id
            and l.is_active
            and str(l.id) not in seen
            and (seen.add(str(l.id)) or True)
        ]


class InMemoryPeriodCloseRequestRepository(IPeriodCloseRequestRepository):
    _requests: dict[str, PeriodCloseRequest] = {}

    @classmethod
    def reset(cls) -> None:
        cls._requests = {}

    async def save(self, request: PeriodCloseRequest) -> None:
        self._requests[str(request.id)] = request

    async def find_by_id(self, request_id: str) -> PeriodCloseRequest | None:
        return self._requests.get(request_id)

    async def list_by_tenant(self, tenant_id: str) -> list[PeriodCloseRequest]:
        return [r for r in self._requests.values() if r.tenant_id == tenant_id]
