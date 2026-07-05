"""Enterprise Cash Reconciliation application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_reconciliation_engine import (
    CashReconciliationAudit,
    CashReconciliationRun,
    ClosingType,
)
from contexts.treasury.domain.events.integration_events import TreasuryAIAnalysisCompletedIntegration
from contexts.treasury.domain.ports.cash_management_repositories import ICashLocationRepository
from contexts.treasury.domain.ports.cash_reconciliation_repositories import (
    ICashReconciliationAuditRepository,
    ICashReconciliationRunRepository,
)
from contexts.treasury.domain.services.cash_reconciliation_engine import (
    build_cash_reconciliation_dashboard,
    build_discrepancy_report,
    detect_ai_anomalies,
    list_cash_reconciliation_catalog,
    list_workflow_states,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class CashReconciliationApplicationService:
    def __init__(
        self,
        locations: ICashLocationRepository,
        runs: ICashReconciliationRunRepository,
        audits: ICashReconciliationAuditRepository,
    ) -> None:
        self._locations = locations
        self._runs = runs
        self._audits = audits

    async def _audit(
        self,
        *,
        tenant_id: str,
        reconciliation_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> None:
        entry = CashReconciliationAudit.create(
            tenant_id=tenant_id,
            reconciliation_id=reconciliation_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )
        await self._audits.save(entry)

    async def _get_location(self, tenant_id: str, location_id: str):
        loc = await self._locations.find_by_id(location_id)
        if not loc or loc.tenant_id != tenant_id:
            return None
        return loc

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_cash_reconciliation_catalog())

    async def list_workflow(self) -> Result[list[dict]]:
        return Result.ok(list_workflow_states())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        runs = await self._runs.list_by_tenant(tenant_id)
        sorted_runs = sorted(runs, key=lambda r: r.created_at, reverse=True)
        return Result.ok(
            build_cash_reconciliation_dashboard(runs=[r.to_dict() for r in sorted_runs])
        )

    async def perform_cash_count(
        self,
        *,
        tenant_id: str,
        location_id: str,
        counted_amount: float,
        closing_type: str = ClosingType.CASH_CLOSING.value,
        counted_by: str | None = None,
        notes: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        loc = await self._get_location(tenant_id, location_id)
        if not loc:
            return Result.fail("treasury.errors.cash_location_not_found")
        try:
            ClosingType(closing_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_closing_type")

        prior = await self._runs.list_by_location(location_id)
        historical = [r.variance for r in prior[-10:]]

        variance = round(counted_amount - loc.balance, 2)
        report = build_discrepancy_report(
            location_id=location_id,
            location_name=loc.name,
            closing_type=closing_type,
            system_balance=loc.balance,
            counted_amount=counted_amount,
            variance=variance,
            variance_type="balanced" if abs(variance) < 0.01 else ("cash_over" if variance > 0 else "cash_short"),
            currency=loc.currency,
            branch_id=loc.branch_id,
        )
        anomalies = detect_ai_anomalies(
            system_balance=loc.balance,
            counted_amount=counted_amount,
            variance=variance,
            historical_variances=historical,
            closing_type=closing_type,
        )

        run = CashReconciliationRun.create(
            tenant_id=tenant_id,
            location_id=location_id,
            closing_type=closing_type,
            system_balance=loc.balance,
            counted_amount=counted_amount,
            currency=loc.currency,
            branch_id=loc.branch_id,
            counted_by=counted_by,
            notes=notes,
            ai_anomalies=anomalies,
            discrepancy_report=report,
        )
        await self._runs.save(run)
        await self._audit(
            tenant_id=tenant_id,
            reconciliation_id=str(run.id),
            action="cash_count",
            actor_id=counted_by,
            detail=f"Counted {counted_amount}, variance {variance}",
        )

        if anomalies and any(a.get("priority") in ("high", "medium") for a in anomalies):
            await publish_integration_event(
                TreasuryAIAnalysisCompletedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id or f"cash-recon-ai-{run.id}",
                    capability="ai_anomaly_detection",
                    result_summary=f"{len(anomalies)} anomalies detected",
                )
            )
        return Result.ok(run.to_dict())

    async def verify_count(
        self, run_id: str, *, tenant_id: str, verified_by: str
    ) -> Result[dict]:
        run = await self._runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        try:
            run.verify(verified_by)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._runs.save(run)
        await self._audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="cash_verification",
            actor_id=verified_by,
            detail="Count verified",
        )
        return Result.ok(run.to_dict())

    async def approve_variance(
        self, run_id: str, *, tenant_id: str, manager_id: str
    ) -> Result[dict]:
        run = await self._runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        if not run.requires_manager_approval:
            return Result.fail("treasury.errors.no_variance_approval_needed")
        try:
            run.approve(manager_id)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._runs.save(run)
        await self._audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="manager_approved",
            actor_id=manager_id,
            detail=f"Variance {run.variance} approved",
        )
        return Result.ok(run.to_dict())

    async def reject_variance(
        self,
        run_id: str,
        *,
        tenant_id: str,
        manager_id: str,
        reason: str = "",
    ) -> Result[dict]:
        run = await self._runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        try:
            run.reject(manager_id, reason=reason)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._runs.save(run)
        await self._audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="manager_rejected",
            actor_id=manager_id,
            detail=reason or "Variance rejected",
        )
        return Result.ok(run.to_dict())

    async def close_reconciliation(
        self, run_id: str, *, tenant_id: str, actor_id: str | None = None
    ) -> Result[dict]:
        run = await self._runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        try:
            run.close()
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        loc = await self._get_location(tenant_id, run.location_id)
        if loc:
            loc.balance = run.counted_amount
            await self._locations.save(loc)

        await self._runs.save(run)
        await self._audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action=f"{run.closing_type}_closed",
            actor_id=actor_id,
            detail=f"Closed with balance {run.counted_amount}",
        )
        return Result.ok(run.to_dict())

    async def perform_branch_closing(
        self,
        *,
        tenant_id: str,
        branch_id: str,
        location_counts: list[dict],
        closed_by: str | None = None,
    ) -> Result[list[dict]]:
        results = []
        for item in location_counts:
            result = await self.perform_cash_count(
                tenant_id=tenant_id,
                location_id=item["location_id"],
                counted_amount=item["counted_amount"],
                closing_type=ClosingType.BRANCH_CLOSING.value,
                counted_by=closed_by,
                notes=item.get("notes"),
            )
            if not result.succeeded:
                return Result.fail(result.error)
            results.append(result.unwrap())
        return Result.ok(results)

    async def get_discrepancy_report(self, run_id: str) -> Result[dict]:
        run = await self._runs.find_by_id(run_id)
        if not run:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        return Result.ok(run.discrepancy_report)

    async def get_ai_anomalies(self, run_id: str) -> Result[list[dict]]:
        run = await self._runs.find_by_id(run_id)
        if not run:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        return Result.ok(run.ai_anomalies)

    async def list_runs(self, tenant_id: str, location_id: str | None = None) -> Result[list[dict]]:
        if location_id:
            runs = await self._runs.list_by_location(location_id)
        else:
            runs = await self._runs.list_by_tenant(tenant_id)
        return Result.ok(
            [r.to_dict() for r in sorted(runs, key=lambda x: x.created_at, reverse=True)]
        )

    async def get_run(self, run_id: str) -> Result[dict]:
        run = await self._runs.find_by_id(run_id)
        if not run:
            return Result.fail("treasury.errors.cash_reconciliation_not_found")
        return Result.ok(run.to_dict())

    async def get_audit_trail(self, run_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_reconciliation(run_id)
        return Result.ok([e.to_dict() for e in entries])
