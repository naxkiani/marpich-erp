"""In-memory Treasury Workflow repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_workflow_engine import (
    TreasuryWorkflowAudit,
    TreasuryWorkflowDefinition,
    TreasuryWorkflowLimit,
    TreasuryWorkflowRequest,
)


class InMemoryWorkflowDefinitionRepository:
    _store: dict[str, TreasuryWorkflowDefinition] = {}

    async def save(self, definition: TreasuryWorkflowDefinition) -> None:
        self._store[str(definition.id)] = definition

    async def find_by_id(self, definition_id: str) -> TreasuryWorkflowDefinition | None:
        return self._store.get(definition_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowDefinition]:
        return [d for d in self._store.values() if d.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryWorkflowLimitRepository:
    _store: dict[str, TreasuryWorkflowLimit] = {}

    async def save(self, limit: TreasuryWorkflowLimit) -> None:
        self._store[str(limit.id)] = limit

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowLimit]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryWorkflowRequestRepository:
    _store: dict[str, TreasuryWorkflowRequest] = {}

    async def save(self, request: TreasuryWorkflowRequest) -> None:
        self._store[str(request.id)] = request

    async def find_by_id(self, request_id: str) -> TreasuryWorkflowRequest | None:
        return self._store.get(request_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowRequest]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryWorkflowAuditRepository:
    _store: dict[str, TreasuryWorkflowAudit] = {}

    async def save(self, entry: TreasuryWorkflowAudit) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_request(self, request_id: str) -> list[TreasuryWorkflowAudit]:
        return [e for e in self._store.values() if e.request_id == request_id]

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowAudit]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
