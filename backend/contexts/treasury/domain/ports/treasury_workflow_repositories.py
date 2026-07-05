"""Treasury Workflow repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.treasury_workflow_engine import (
    TreasuryWorkflowAudit,
    TreasuryWorkflowDefinition,
    TreasuryWorkflowLimit,
    TreasuryWorkflowRequest,
)


class IWorkflowDefinitionRepository(Protocol):
    async def save(self, definition: TreasuryWorkflowDefinition) -> None: ...

    async def find_by_id(self, definition_id: str) -> TreasuryWorkflowDefinition | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowDefinition]: ...


class IWorkflowLimitRepository(Protocol):
    async def save(self, limit: TreasuryWorkflowLimit) -> None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowLimit]: ...


class IWorkflowRequestRepository(Protocol):
    async def save(self, request: TreasuryWorkflowRequest) -> None: ...

    async def find_by_id(self, request_id: str) -> TreasuryWorkflowRequest | None: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowRequest]: ...


class IWorkflowAuditRepository(Protocol):
    async def save(self, entry: TreasuryWorkflowAudit) -> None: ...

    async def list_by_request(self, request_id: str) -> list[TreasuryWorkflowAudit]: ...

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryWorkflowAudit]: ...
