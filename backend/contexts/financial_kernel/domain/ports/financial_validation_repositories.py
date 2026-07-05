"""Financial validation repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.financial_kernel.domain.aggregates.financial_validation import (
    ValidationAuditLog,
    ValidationRun,
)


class IValidationRunRepository(Protocol):
    async def save(self, run: ValidationRun) -> None: ...
    async def find_by_id(self, run_id: str) -> ValidationRun | None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[ValidationRun]: ...


class IValidationAuditRepository(Protocol):
    async def save(self, entry: ValidationAuditLog) -> None: ...
    async def list_by_validation_run(self, validation_run_id: str) -> list[ValidationAuditLog]: ...
