"""Enterprise Cash Management application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_forecast import CashForecast, ForecastScenario
from contexts.treasury.domain.aggregates.cash_management import (
    CashClosing,
    CashCount,
    CashLocation,
    CashReconciliation,
    CashTransaction,
    CashTransactionType,
    CashVerification,
)
from contexts.treasury.domain.events.integration_events import TreasuryTransferExecutedIntegration
from contexts.treasury.domain.ports.cash_management_repositories import (
    ICashClosingRepository,
    ICashCountRepository,
    ICashLocationRepository,
    ICashReconciliationRepository,
    ICashTransactionRepository,
    ICashVerificationRepository,
)
from contexts.treasury.domain.ports.repositories import ICashForecastRepository
from contexts.treasury.domain.services.cash_management_engine import (
    assert_location_type,
    assert_transaction_type,
    build_cash_dashboard,
    list_cash_management_catalog,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class CashManagementApplicationService:
    def __init__(
        self,
        locations: ICashLocationRepository,
        transactions: ICashTransactionRepository,
        counts: ICashCountRepository,
        verifications: ICashVerificationRepository,
        closings: ICashClosingRepository,
        reconciliations: ICashReconciliationRepository,
        forecasts: ICashForecastRepository,
    ) -> None:
        self._locations = locations
        self._transactions = transactions
        self._counts = counts
        self._verifications = verifications
        self._closings = closings
        self._reconciliations = reconciliations
        self._forecasts = forecasts

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_cash_management_catalog())

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._locations.list_by_tenant(tenant_id):
            return
        defaults = [
            ("REG-01", "Front Register", "cash_register", 500.0),
            ("PETTY-HQ", "HQ Petty Cash", "petty_cash", 300.0),
            ("MCO-01", "Main Cash Office", "main_cash_office", 10000.0),
            ("VAULT-01", "Main Vault", "vault", 25000.0),
            ("SAFE-01", "Office Safe", "safe", 2000.0),
            ("BR-CASH-01", "Branch Cash", "branch_cash", 1500.0),
            ("DEPT-FIN", "Finance Dept Cash", "department_cash", 800.0),
        ]
        for code, name, loc_type, balance in defaults:
            loc = CashLocation.create(
                tenant_id=tenant_id,
                code=code,
                name=name,
                location_type=loc_type,
                opening_balance=balance,
            )
            await self._locations.save(loc)

    async def create_location(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        location_type: str,
        currency: str = "USD",
        organization_id: str | None = None,
        branch_id: str | None = None,
        department_id: str | None = None,
        opening_balance: float = 0.0,
        gl_account_code: str | None = None,
    ) -> Result[dict]:
        if await self._locations.find_by_code(tenant_id, code):
            return Result.fail("treasury.errors.cash_location_exists")
        try:
            assert_location_type(location_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_cash_location_type")
        loc = CashLocation.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            location_type=location_type,
            currency=currency,
            organization_id=organization_id,
            branch_id=branch_id,
            department_id=department_id,
            opening_balance=opening_balance,
            gl_account_code=gl_account_code,
        )
        await self._locations.save(loc)
        return Result.ok(loc.to_dict())

    async def list_locations(
        self, tenant_id: str, organization_id: str | None = None
    ) -> Result[list[dict]]:
        locs = await self._locations.list_by_tenant(tenant_id, organization_id)
        return Result.ok([l.to_dict() for l in sorted(locs, key=lambda x: x.code)])

    async def get_location(self, tenant_id: str, location_id: str) -> Result[dict]:
        loc = await self._locations.find_by_id(location_id)
        if not loc or loc.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_location_not_found")
        return Result.ok(loc.to_dict())

    async def _get_location(self, tenant_id: str, location_id: str) -> CashLocation | None:
        loc = await self._locations.find_by_id(location_id)
        if not loc or loc.tenant_id != tenant_id:
            return None
        return loc

    async def record_transaction(
        self,
        *,
        tenant_id: str,
        location_id: str,
        transaction_type: str,
        amount: float,
        reference: str,
        created_by: str | None = None,
        description: str | None = None,
        counterpart_location_id: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        try:
            assert_transaction_type(transaction_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_cash_transaction_type")

        loc = await self._get_location(tenant_id, location_id)
        if not loc:
            return Result.fail("treasury.errors.cash_location_not_found")
        if loc.status != "active":
            return Result.fail("treasury.errors.cash_location_inactive")

        direction = "in"
        if transaction_type in (
            CashTransactionType.WITHDRAWAL.value,
            CashTransactionType.PAYMENT.value,
            CashTransactionType.TRANSFER.value,
        ):
            direction = "out"

        if transaction_type == CashTransactionType.TRANSFER.value:
            if not counterpart_location_id:
                return Result.fail("treasury.errors.counterpart_required")
            counterpart = await self._get_location(tenant_id, counterpart_location_id)
            if not counterpart:
                return Result.fail("treasury.errors.counterpart_not_found")
            try:
                loc.debit(amount)
                counterpart.credit(amount)
            except ValueError:
                return Result.fail("treasury.errors.insufficient_balance")
            await self._locations.save(loc)
            await self._locations.save(counterpart)
            await publish_integration_event(
                TreasuryTransferExecutedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    transfer_id=f"cash-{reference}",
                    from_account_id=location_id,
                    to_account_id=counterpart_location_id,
                    from_account_type=loc.location_type,
                    to_account_type=counterpart.location_type,
                    amount=amount,
                    currency=loc.currency,
                    instrument="cash",
                )
            )
        elif transaction_type == CashTransactionType.DEPOSIT.value:
            loc.credit(amount)
            await self._locations.save(loc)
        elif transaction_type == CashTransactionType.RECEIPT.value:
            loc.credit(amount)
            await self._locations.save(loc)
        elif transaction_type in (
            CashTransactionType.WITHDRAWAL.value,
            CashTransactionType.PAYMENT.value,
        ):
            try:
                loc.debit(amount)
            except ValueError:
                return Result.fail("treasury.errors.insufficient_balance")
            await self._locations.save(loc)
        elif transaction_type == CashTransactionType.ADJUSTMENT.value:
            if amount >= 0:
                loc.credit(amount)
            else:
                try:
                    loc.debit(abs(amount))
                except ValueError:
                    return Result.fail("treasury.errors.insufficient_balance")
            await self._locations.save(loc)
            direction = "adjustment"

        txn = CashTransaction.record(
            tenant_id=tenant_id,
            location_id=location_id,
            transaction_type=transaction_type,
            amount=amount,
            currency=loc.currency,
            reference=reference,
            direction=direction,
            organization_id=loc.organization_id,
            description=description,
            counterpart_location_id=counterpart_location_id,
            created_by=created_by,
        )
        await self._transactions.save(txn)
        return Result.ok(txn.to_dict())

    async def list_transactions(self, tenant_id: str, location_id: str | None = None) -> Result[list[dict]]:
        if location_id:
            txns = await self._transactions.list_by_location(location_id)
        else:
            txns = await self._transactions.list_by_tenant(tenant_id)
        return Result.ok([t.to_dict() for t in txns])

    async def create_count(
        self,
        *,
        tenant_id: str,
        location_id: str,
        counted_amount: float,
        counted_by: str,
        notes: str | None = None,
    ) -> Result[dict]:
        loc = await self._get_location(tenant_id, location_id)
        if not loc:
            return Result.fail("treasury.errors.cash_location_not_found")
        count = CashCount.create(
            tenant_id=tenant_id,
            location_id=location_id,
            system_balance=loc.balance,
            counted_amount=counted_amount,
            currency=loc.currency,
            counted_by=counted_by,
            notes=notes,
        )
        await self._counts.save(count)
        return Result.ok(count.to_dict())

    async def verify_count(
        self,
        *,
        tenant_id: str,
        count_id: str,
        verified_by: str,
        approved: bool,
        notes: str | None = None,
    ) -> Result[dict]:
        count = await self._counts.find_by_id(count_id)
        if not count or count.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_count_not_found")
        if approved:
            count.verify()
        else:
            count.reject()
        await self._counts.save(count)
        verification = CashVerification.record(
            tenant_id=tenant_id,
            cash_count_id=count_id,
            verified_by=verified_by,
            approved=approved,
            notes=notes,
        )
        await self._verifications.save(verification)
        return Result.ok({"count": count.to_dict(), "verification": verification.to_dict()})

    async def list_counts(self, tenant_id: str, location_id: str | None = None) -> Result[list[dict]]:
        if location_id:
            counts = await self._counts.list_by_location(location_id)
        else:
            counts = await self._counts.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in counts])

    async def open_closing(
        self, *, tenant_id: str, location_id: str, closed_by: str
    ) -> Result[dict]:
        loc = await self._get_location(tenant_id, location_id)
        if not loc:
            return Result.fail("treasury.errors.cash_location_not_found")
        open_sessions = await self._closings.list_open_by_location(location_id)
        if open_sessions:
            return Result.fail("treasury.errors.closing_session_open")
        closing = CashClosing.open_session(
            tenant_id=tenant_id,
            location_id=location_id,
            opening_balance=loc.balance,
            currency=loc.currency,
            closed_by=closed_by,
        )
        await self._closings.save(closing)
        return Result.ok(closing.to_dict())

    async def close_session(
        self,
        *,
        tenant_id: str,
        closing_id: str,
        counted_amount: float,
    ) -> Result[dict]:
        closing = await self._closings.find_by_id(closing_id)
        if not closing or closing.tenant_id != tenant_id:
            return Result.fail("treasury.errors.cash_closing_not_found")
        loc = await self._get_location(tenant_id, closing.location_id)
        if not loc:
            return Result.fail("treasury.errors.cash_location_not_found")
        try:
            closing.close(counted_amount=counted_amount, closing_balance=loc.balance)
        except ValueError:
            return Result.fail("treasury.errors.closing_session_not_open")
        await self._closings.save(closing)
        return Result.ok(closing.to_dict())

    async def list_closings(self, tenant_id: str) -> Result[list[dict]]:
        closings = await self._closings.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in closings])

    async def reconcile_cash(
        self,
        *,
        tenant_id: str,
        location_id: str,
        period_start: str,
        period_end: str,
        counted_balance: float,
        reconciled_by: str | None = None,
    ) -> Result[dict]:
        loc = await self._get_location(tenant_id, location_id)
        if not loc:
            return Result.fail("treasury.errors.cash_location_not_found")
        recon = CashReconciliation.create(
            tenant_id=tenant_id,
            location_id=location_id,
            period_start=period_start,
            period_end=period_end,
            book_balance=loc.balance,
            counted_balance=counted_balance,
            currency=loc.currency,
            reconciled_by=reconciled_by,
        )
        await self._reconciliations.save(recon)
        return Result.ok(recon.to_dict())

    async def list_reconciliations(self, tenant_id: str) -> Result[list[dict]]:
        recons = await self._reconciliations.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in recons])

    async def create_forecast(
        self,
        *,
        tenant_id: str,
        name: str,
        period_start: str,
        period_end: str,
        scenario: str,
        currency: str,
        opening_balance: float,
        projected_lines: list[dict],
    ) -> Result[dict]:
        try:
            ForecastScenario(scenario)
        except ValueError:
            return Result.fail("treasury.errors.invalid_forecast_scenario")
        forecast = CashForecast.create(
            tenant_id=tenant_id,
            name=name,
            period_start=period_start,
            period_end=period_end,
            scenario=scenario,
            currency=currency,
            opening_balance=opening_balance,
            projected_lines=projected_lines,
        )
        await self._forecasts.save(forecast)
        return Result.ok(forecast.to_dict())

    async def list_forecasts(self, tenant_id: str) -> Result[list[dict]]:
        forecasts = await self._forecasts.list_by_tenant(tenant_id)
        return Result.ok([f.to_dict() for f in forecasts])

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        locations = [l.to_dict() for l in await self._locations.list_by_tenant(tenant_id)]
        transactions = [t.to_dict() for t in await self._transactions.list_by_tenant(tenant_id)]
        counts = [c.to_dict() for c in await self._counts.list_by_tenant(tenant_id)]
        closings = [c.to_dict() for c in await self._closings.list_by_tenant(tenant_id)]
        reconciliations = [r.to_dict() for r in await self._reconciliations.list_by_tenant(tenant_id)]
        forecasts = [f.to_dict() for f in await self._forecasts.list_by_tenant(tenant_id)]
        return Result.ok(
            build_cash_dashboard(
                locations=locations,
                transactions=transactions,
                counts=counts,
                closings=closings,
                reconciliations=reconciliations,
                forecasts=forecasts,
            )
        )
