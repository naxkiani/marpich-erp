"""Treasury Security repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.treasury_security_engine import (
    TreasuryAccessRule,
    TreasuryApprovalMatrix,
    TreasurySecurityAudit,
    TreasurySecurityLock,
    TreasurySecurityOperation,
    TreasurySecurityPolicy,
    TreasuryTransactionLimit,
)


class ISecurityPolicyRepository(Protocol):
    async def save(self, policy: TreasurySecurityPolicy) -> None: ...

    async def find_by_id(self, policy_id: str) -> TreasurySecurityPolicy | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityPolicy]: ...


class ITransactionLimitRepository(Protocol):
    async def save(self, limit: TreasuryTransactionLimit) -> None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryTransactionLimit]: ...


class IApprovalMatrixRepository(Protocol):
    async def save(self, entry: TreasuryApprovalMatrix) -> None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryApprovalMatrix]: ...


class IAccessRuleRepository(Protocol):
    async def save(self, rule: TreasuryAccessRule) -> None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryAccessRule]: ...


class ISecurityLockRepository(Protocol):
    async def save(self, lock: TreasurySecurityLock) -> None: ...

    async def find_by_id(self, lock_id: str) -> TreasurySecurityLock | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityLock]: ...


class ISecurityOperationRepository(Protocol):
    async def save(self, operation: TreasurySecurityOperation) -> None: ...

    async def find_by_id(self, operation_id: str) -> TreasurySecurityOperation | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityOperation]: ...


class ISecurityAuditRepository(Protocol):
    async def save(self, entry: TreasurySecurityAudit) -> None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasurySecurityAudit]: ...

    async def list_by_subject(self, subject_ref: str) -> list[TreasurySecurityAudit]: ...
