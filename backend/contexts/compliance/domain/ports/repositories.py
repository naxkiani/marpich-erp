"""Compliance repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.compliance.domain.aggregates.compliance_control import ComplianceControl
from contexts.compliance.domain.aggregates.compliance_report import ComplianceReport
from contexts.compliance.domain.aggregates.compliance_violation import ComplianceViolation
from shared.domain.value_objects.unique_id import UniqueId


class IComplianceControlRepository(ABC):
    @abstractmethod
    async def save(self, control: ComplianceControl) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, *, domain: str | None = None) -> list[ComplianceControl]: ...

    @abstractmethod
    async def exists(self, tenant_id: str, control_id: str) -> bool: ...


class IComplianceViolationRepository(ABC):
    @abstractmethod
    async def save(self, violation: ComplianceViolation) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, violation_id: UniqueId) -> ComplianceViolation | None: ...

    @abstractmethod
    async def query(
        self,
        tenant_id: str,
        *,
        domain: str | None = None,
        status: str | None = None,
        severity: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ComplianceViolation]: ...

    @abstractmethod
    async def count_open(self, tenant_id: str) -> int: ...

    @abstractmethod
    async def count_by_domain(self, tenant_id: str) -> dict[str, int]: ...


class IComplianceReportRepository(ABC):
    @abstractmethod
    async def save(self, report: ComplianceReport) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, report_id: UniqueId) -> ComplianceReport | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, limit: int = 20) -> list[ComplianceReport]: ...
