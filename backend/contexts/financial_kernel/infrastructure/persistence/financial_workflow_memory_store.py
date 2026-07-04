"""In-memory Financial Workflow persistence."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.financial_kernel.domain.aggregates.financial_workflow import (
    FinancialWorkflow,
    FinancialWorkflowStatus,
)
from contexts.financial_kernel.domain.ports.financial_workflow_repositories import (
    IFinancialWorkflowRepository,
)


class InMemoryFinancialWorkflowRepository(IFinancialWorkflowRepository):
    _workflows: dict[str, FinancialWorkflow] = {}

    @classmethod
    def reset(cls) -> None:
        cls._workflows = {}

    async def save(self, workflow: FinancialWorkflow) -> None:
        self._workflows[str(workflow.id)] = workflow
        self._workflows[f"idemp:{workflow.tenant_id}:{workflow.idempotency_key}"] = workflow

    async def find_by_id(self, workflow_id: str) -> FinancialWorkflow | None:
        w = self._workflows.get(workflow_id)
        return w if isinstance(w, FinancialWorkflow) else None

    async def find_by_idempotency(self, tenant_id: str, key: str) -> FinancialWorkflow | None:
        w = self._workflows.get(f"idemp:{tenant_id}:{key}")
        return w if isinstance(w, FinancialWorkflow) else None

    async def list_by_tenant(self, tenant_id: str) -> list[FinancialWorkflow]:
        seen: set[str] = set()
        result = []
        for w in self._workflows.values():
            if isinstance(w, FinancialWorkflow) and w.tenant_id == tenant_id and str(w.id) not in seen:
                seen.add(str(w.id))
                result.append(w)
        return result

    async def list_by_type(self, tenant_id: str, workflow_type: str) -> list[FinancialWorkflow]:
        return [w for w in await self.list_by_tenant(tenant_id) if w.workflow_type == workflow_type]

    async def list_pending_sla_breached(self, tenant_id: str) -> list[FinancialWorkflow]:
        now = datetime.now(UTC)
        return [
            w
            for w in await self.list_by_tenant(tenant_id)
            if w.is_sla_breached(now)
            and w.status
            in (FinancialWorkflowStatus.PENDING, FinancialWorkflowStatus.IN_PROGRESS)
        ]
