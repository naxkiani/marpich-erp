"""In-memory financial validation repositories."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_validation import (
    ValidationAuditLog,
    ValidationRun,
)
from contexts.financial_kernel.domain.ports.financial_validation_repositories import (
    IValidationAuditRepository,
    IValidationRunRepository,
)


class InMemoryValidationRunRepository(IValidationRunRepository):
    _runs: dict[str, ValidationRun] = {}

    @classmethod
    def reset(cls) -> None:
        cls._runs = {}

    async def save(self, run: ValidationRun) -> None:
        self._runs[str(run.id)] = run

    async def find_by_id(self, run_id: str) -> ValidationRun | None:
        return self._runs.get(run_id)

    async def list_by_tenant(self, tenant_id: str) -> list[ValidationRun]:
        items = [r for r in self._runs.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)


class InMemoryValidationAuditRepository(IValidationAuditRepository):
    _entries: list[ValidationAuditLog] = []

    @classmethod
    def reset(cls) -> None:
        cls._entries = []

    async def save(self, entry: ValidationAuditLog) -> None:
        self._entries.append(entry)

    async def list_by_validation_run(self, validation_run_id: str) -> list[ValidationAuditLog]:
        return [e for e in self._entries if e.validation_run_id == validation_run_id]
