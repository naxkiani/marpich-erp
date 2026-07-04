"""In-memory compliance repositories."""
from __future__ import annotations

from contexts.compliance.domain.aggregates.compliance_control import ComplianceControl
from contexts.compliance.domain.aggregates.compliance_report import ComplianceReport
from contexts.compliance.domain.aggregates.compliance_violation import ComplianceViolation, ViolationStatus
from contexts.compliance.domain.ports.repositories import (
    IComplianceControlRepository,
    IComplianceReportRepository,
    IComplianceViolationRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class ComplianceMemoryStore:
    controls: list[ComplianceControl] = []
    violations: list[ComplianceViolation] = []
    reports: dict[str, ComplianceReport] = {}

    @classmethod
    def reset(cls) -> None:
        cls.controls.clear()
        cls.violations.clear()
        cls.reports.clear()


class InMemoryComplianceControlRepository(IComplianceControlRepository):
    async def save(self, control: ComplianceControl) -> None:
        ComplianceMemoryStore.controls = [
            c
            for c in ComplianceMemoryStore.controls
            if not (c.tenant_id == control.tenant_id and c.control_id == control.control_id)
        ]
        ComplianceMemoryStore.controls.append(control)

    async def list_by_tenant(self, tenant_id: str, *, domain: str | None = None) -> list[ComplianceControl]:
        items = [c for c in ComplianceMemoryStore.controls if c.tenant_id == tenant_id]
        if domain:
            items = [c for c in items if c.domain == domain]
        return sorted(items, key=lambda c: (c.domain, c.control_id))

    async def exists(self, tenant_id: str, control_id: str) -> bool:
        return any(c.tenant_id == tenant_id and c.control_id == control_id for c in ComplianceMemoryStore.controls)


class InMemoryComplianceViolationRepository(IComplianceViolationRepository):
    async def save(self, violation: ComplianceViolation) -> None:
        ComplianceMemoryStore.violations = [
            v for v in ComplianceMemoryStore.violations if str(v.id) != str(violation.id)
        ]
        ComplianceMemoryStore.violations.append(violation)

    async def find_by_id(self, tenant_id: str, violation_id: UniqueId) -> ComplianceViolation | None:
        for v in ComplianceMemoryStore.violations:
            if v.tenant_id == tenant_id and str(v.id) == str(violation_id):
                return v
        return None

    async def query(
        self,
        tenant_id: str,
        *,
        domain: str | None = None,
        status: str | None = None,
        severity: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ComplianceViolation]:
        items = [v for v in ComplianceMemoryStore.violations if v.tenant_id == tenant_id]
        if domain:
            items = [v for v in items if v.domain == domain]
        if status:
            items = [v for v in items if v.status.value == status]
        if severity:
            items = [v for v in items if v.severity.value == severity]
        items.sort(key=lambda v: v.detected_at, reverse=True)
        return items[offset : offset + limit]

    async def count_open(self, tenant_id: str) -> int:
        return sum(
            1 for v in ComplianceMemoryStore.violations if v.tenant_id == tenant_id and v.status == ViolationStatus.OPEN
        )

    async def count_by_domain(self, tenant_id: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for v in ComplianceMemoryStore.violations:
            if v.tenant_id == tenant_id and v.status == ViolationStatus.OPEN:
                counts[v.domain] = counts.get(v.domain, 0) + 1
        return counts


class InMemoryComplianceReportRepository(IComplianceReportRepository):
    async def save(self, report: ComplianceReport) -> None:
        ComplianceMemoryStore.reports[str(report.id)] = report

    async def find_by_id(self, tenant_id: str, report_id: UniqueId) -> ComplianceReport | None:
        report = ComplianceMemoryStore.reports.get(str(report_id))
        if report and report.tenant_id == tenant_id:
            return report
        return None

    async def list_by_tenant(self, tenant_id: str, limit: int = 20) -> list[ComplianceReport]:
        items = [r for r in ComplianceMemoryStore.reports.values() if r.tenant_id == tenant_id]
        items.sort(key=lambda r: r.created_at, reverse=True)
        return items[:limit]
