"""In-memory Treasury Security repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_security_engine import (
    TreasuryAccessRule,
    TreasuryApprovalMatrix,
    TreasurySecurityAudit,
    TreasurySecurityLock,
    TreasurySecurityOperation,
    TreasurySecurityPolicy,
    TreasuryTransactionLimit,
)


class InMemorySecurityPolicyRepository:
    _store: dict[str, TreasurySecurityPolicy] = {}

    async def save(self, policy: TreasurySecurityPolicy) -> None:
        self._store[str(policy.id)] = policy

    async def find_by_id(self, policy_id: str) -> TreasurySecurityPolicy | None:
        return self._store.get(policy_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityPolicy]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryTransactionLimitRepository:
    _store: dict[str, TreasuryTransactionLimit] = {}

    async def save(self, limit: TreasuryTransactionLimit) -> None:
        self._store[str(limit.id)] = limit

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryTransactionLimit]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryApprovalMatrixRepository:
    _store: dict[str, TreasuryApprovalMatrix] = {}

    async def save(self, entry: TreasuryApprovalMatrix) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryApprovalMatrix]:
        return [m for m in self._store.values() if m.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryAccessRuleRepository:
    _store: dict[str, TreasuryAccessRule] = {}

    async def save(self, rule: TreasuryAccessRule) -> None:
        self._store[str(rule.id)] = rule

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryAccessRule]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemorySecurityLockRepository:
    _store: dict[str, TreasurySecurityLock] = {}

    async def save(self, lock: TreasurySecurityLock) -> None:
        self._store[str(lock.id)] = lock

    async def find_by_id(self, lock_id: str) -> TreasurySecurityLock | None:
        return self._store.get(lock_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityLock]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemorySecurityOperationRepository:
    _store: dict[str, TreasurySecurityOperation] = {}

    async def save(self, operation: TreasurySecurityOperation) -> None:
        self._store[str(operation.id)] = operation

    async def find_by_id(self, operation_id: str) -> TreasurySecurityOperation | None:
        return self._store.get(operation_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityOperation]:
        return [o for o in self._store.values() if o.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemorySecurityAuditRepository:
    _store: dict[str, TreasurySecurityAudit] = {}

    async def save(self, entry: TreasurySecurityAudit) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityAudit]:
        return sorted(
            [e for e in self._store.values() if e.tenant_id == tenant_id],
            key=lambda e: e.occurred_at,
            reverse=True,
        )

    async def list_by_subject(self, subject_ref: str) -> list[TreasurySecurityAudit]:
        return [e for e in self._store.values() if e.subject_ref == subject_ref]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
