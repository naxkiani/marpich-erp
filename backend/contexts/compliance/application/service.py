"""Compliance application service."""
from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from contexts.compliance.application.constants.default_controls import (
    COMPLIANCE_DOMAINS,
    DEFAULT_CONTROLS,
    INDUSTRY_PACK_DOMAINS,
)
from contexts.compliance.domain.aggregates.compliance_control import ComplianceControl
from contexts.compliance.domain.aggregates.compliance_report import ComplianceReport
from contexts.compliance.domain.aggregates.compliance_violation import ComplianceViolation, ViolationStatus
from contexts.compliance.domain.events.integration_events import (
    AlertTriggeredIntegration,
    ReportGeneratedIntegration,
    ViolationDetectedIntegration,
)
from contexts.compliance.domain.ports.repositories import (
    IComplianceControlRepository,
    IComplianceReportRepository,
    IComplianceViolationRepository,
)
from contexts.compliance.infrastructure.acl.violation_mapper import match_violation
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ComplianceApplicationService:
    def __init__(
        self,
        controls: IComplianceControlRepository,
        violations: IComplianceViolationRepository,
        reports: IComplianceReportRepository,
    ) -> None:
        self._controls = controls
        self._violations = violations
        self._reports = reports
        self._access_denied_counts: dict[str, int] = defaultdict(int)
        self._failed_login_counts: dict[str, int] = defaultdict(int)

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        industry_pack = (envelope.get("payload") or {}).get("industry_pack", "")
        domains = INDUSTRY_PACK_DOMAINS.get(str(industry_pack).lower(), ())
        domain_set = set(domains) if domains else {c[0] for c in DEFAULT_CONTROLS}
        for domain, control_id, name, severity in DEFAULT_CONTROLS:
            if domain not in domain_set:
                continue
            if await self._controls.exists(tenant_id, control_id):
                continue
            control = ComplianceControl.register(
                tenant_id=tenant_id,
                domain=domain,
                control_id=control_id,
                name=name,
                severity=severity,
            )
            await self._controls.save(control)

    async def handle_integration_event(self, envelope: dict) -> None:
        event_name = envelope.get("event_name", "")
        tenant_id = envelope.get("tenant_id", "")
        if not tenant_id:
            return

        if event_name == "authorization.access.denied":
            self._access_denied_counts[tenant_id] += 1
            if self._access_denied_counts[tenant_id] >= 5:
                await self._record_violation(
                    tenant_id=tenant_id,
                    domain="security_compliance",
                    control_id="SEC-002",
                    severity="medium",
                    title="Access denial spike detected",
                    source_event=event_name,
                    correlation_id=envelope.get("correlation_id"),
                    payload={"count": self._access_denied_counts[tenant_id]},
                )
            return

        if event_name == "identity.login.failed":
            self._failed_login_counts[tenant_id] += 1
            if self._failed_login_counts[tenant_id] >= 3:
                await self._record_violation(
                    tenant_id=tenant_id,
                    domain="security_compliance",
                    control_id="SEC-001",
                    severity="high",
                    title="Excessive failed login attempts",
                    source_event=event_name,
                    correlation_id=envelope.get("correlation_id"),
                    payload={"count": self._failed_login_counts[tenant_id]},
                )
            return

        rule = match_violation(envelope)
        if not rule:
            return
        await self._record_violation(
            tenant_id=tenant_id,
            domain=rule["domain"],
            control_id=rule["control_id"],
            severity=rule["severity"],
            title=rule["title"],
            source_event=event_name,
            correlation_id=envelope.get("correlation_id"),
            payload=envelope.get("payload") or {},
        )

    async def _record_violation(
        self,
        *,
        tenant_id: str,
        domain: str,
        control_id: str,
        severity: str,
        title: str,
        source_event: str | None,
        correlation_id: str | None,
        payload: dict,
    ) -> ComplianceViolation:
        violation = ComplianceViolation.detect(
            tenant_id=tenant_id,
            domain=domain,
            control_id=control_id,
            severity=severity,
            title=title,
            description=f"Control {control_id} breached",
            source_event=source_event,
            correlation_id=correlation_id,
            payload=payload,
        )
        await self._violations.save(violation)
        corr = correlation_id or f"compliance-{violation.id}"
        await publish_integration_event(
            ViolationDetectedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                violation_id=str(violation.id),
                domain=domain,
                control_id=control_id,
                severity=severity,
                title=title,
            )
        )
        if severity in ("critical", "high"):
            await publish_integration_event(
                AlertTriggeredIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=corr,
                    violation_id=str(violation.id),
                    domain=domain,
                    severity=severity,
                )
            )
        return violation

    async def list_domains(self) -> Result[list[dict]]:
        return Result.ok([{"id": d[0], "name": d[1]} for d in COMPLIANCE_DOMAINS])

    async def list_controls(self, tenant_id: str, *, domain: str | None = None) -> Result[list[dict]]:
        controls = await self._controls.list_by_tenant(tenant_id, domain=domain)
        return Result.ok([c.to_dict() for c in controls])

    async def query_violations(
        self,
        tenant_id: str,
        *,
        domain: str | None = None,
        status: str | None = None,
        severity: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Result[dict]:
        items = await self._violations.query(
            tenant_id,
            domain=domain,
            status=status,
            severity=severity,
            limit=limit,
            offset=offset,
        )
        return Result.ok(
            {
                "items": [v.to_dict() for v in items],
                "total": len(items),
                "open": await self._violations.count_open(tenant_id),
            }
        )

    async def get_violation(self, tenant_id: str, violation_id: str) -> Result[dict]:
        violation = await self._violations.find_by_id(tenant_id, UniqueId.from_string(violation_id))
        if not violation:
            return Result.fail("compliance.errors.violation_not_found")
        return Result.ok(violation.to_dict())

    async def resolve_violation(
        self, tenant_id: str, violation_id: str, *, actor_id: str | None, notes: str
    ) -> Result[dict]:
        violation = await self._violations.find_by_id(tenant_id, UniqueId.from_string(violation_id))
        if not violation:
            return Result.fail("compliance.errors.violation_not_found")
        violation.resolve(actor_id=actor_id, notes=notes)
        await self._violations.save(violation)
        return Result.ok(violation.to_dict())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        controls = await self._controls.list_by_tenant(tenant_id)
        open_count = await self._violations.count_open(tenant_id)
        by_domain = await self._violations.count_by_domain(tenant_id)
        recent = await self._violations.query(tenant_id, limit=10)
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        critical_24h = sum(
            1
            for v in recent
            if v.severity.value == "critical" and v.detected_at >= cutoff and v.status == ViolationStatus.OPEN
        )
        total_controls = len(controls) or 1
        passing = max(0, total_controls - min(open_count, total_controls))
        score = round((passing / total_controls) * 100, 1)
        domain_status = {
            d[0]: {"open_violations": by_domain.get(d[0], 0), "status": "pass" if by_domain.get(d[0], 0) == 0 else "fail"}
            for d in COMPLIANCE_DOMAINS
        }
        return Result.ok(
            {
                "compliance_score": score,
                "open_violations": open_count,
                "critical_alerts_24h": critical_24h,
                "controls_total": len(controls),
                "controls_passing": passing,
                "violations_by_domain": by_domain,
                "domain_status": domain_status,
                "recent_violations": [v.to_dict() for v in recent],
            }
        )

    async def get_alerts(self, tenant_id: str) -> Result[dict]:
        open_violations = await self._violations.query(
            tenant_id, status=ViolationStatus.OPEN.value, severity="critical", limit=50
        )
        high = await self._violations.query(
            tenant_id, status=ViolationStatus.OPEN.value, severity="high", limit=50
        )
        return Result.ok(
            {
                "critical": [v.to_dict() for v in open_violations],
                "high": [v.to_dict() for v in high],
                "total_active": len(open_violations) + len(high),
            }
        )

    async def get_retention_status(self, tenant_id: str) -> Result[dict]:
        open_retention = await self._violations.query(
            tenant_id, domain="retention_policies", status="open", limit=10
        )
        return Result.ok(
            {
                "audit_retention": {"status": "compliant", "note": "Monitor via audit.retention.applied events"},
                "document_retention": {"status": "compliant", "note": "Monitor via documents.retention.applied"},
                "legal_holds": {"active": 0},
                "open_retention_violations": [v.to_dict() for v in open_retention],
            }
        )

    async def create_report(
        self,
        *,
        tenant_id: str,
        report_type: str,
        domain: str | None,
        export_format: str,
        filters: dict,
        requested_by: str | None,
        correlation_id: str,
    ) -> Result[dict]:
        report = ComplianceReport.create(
            tenant_id=tenant_id,
            report_type=report_type,
            domain=domain,
            export_format=export_format,
            filters=filters,
            requested_by=requested_by,
        )
        violations = await self._violations.query(tenant_id, domain=domain, limit=500)
        controls = await self._controls.list_by_tenant(tenant_id, domain=domain)
        dashboard = (await self.get_dashboard(tenant_id)).unwrap()
        data = {
            "report_type": report_type,
            "domain": domain,
            "generated_at": datetime.now(UTC).isoformat(),
            "compliance_score": dashboard["compliance_score"],
            "controls": [c.to_dict() for c in controls],
            "violations": [v.to_dict() for v in violations],
            "filters": filters,
        }
        report.complete(data)
        await self._reports.save(report)
        await publish_integration_event(
            ReportGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                report_id=str(report.id),
                report_type=report_type,
            )
        )
        return Result.ok(report.to_dict())

    async def get_report(self, tenant_id: str, report_id: str) -> Result[dict]:
        report = await self._reports.find_by_id(tenant_id, UniqueId.from_string(report_id))
        if not report:
            return Result.fail("compliance.errors.report_not_found")
        return Result.ok(report.to_dict())

    async def list_reports(self, tenant_id: str) -> Result[list[dict]]:
        reports = await self._reports.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in reports])
