"""Enterprise Treasury application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_reconciliation import BankReconciliation
from contexts.treasury.domain.aggregates.cash_forecast import CashForecast, ForecastScenario
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount, TreasuryAccountType
from contexts.treasury.domain.aggregates.treasury_transfer import (
    PaymentInstrument,
    TransferStatus,
    TreasuryTransfer,
)
from contexts.treasury.domain.events.integration_events import (
    TreasuryLiquidityUpdatedIntegration,
    TreasuryTransferApprovalRequestedIntegration,
    TreasuryTransferExecutedIntegration,
)
from contexts.treasury.domain.ports.repositories import (
    IBankReconciliationRepository,
    ICashForecastRepository,
    ITreasuryAccountRepository,
    ITreasuryTransferRepository,
)
from contexts.treasury.domain.services.treasury_engine import build_dashboard, compute_liquidity
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class TreasuryApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        transfers: ITreasuryTransferRepository,
        reconciliations: IBankReconciliationRepository,
        forecasts: ICashForecastRepository,
    ) -> None:
        self._accounts = accounts
        self._transfers = transfers
        self._reconciliations = reconciliations
        self._forecasts = forecasts

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._accounts.list_by_tenant(tenant_id):
            return
        defaults = [
            ("MAIN-CASH", "Main Cash", TreasuryAccountType.CASH, 5000.0),
            ("OPERATING-BANK", "Operating Bank Account", TreasuryAccountType.BANK, 50000.0),
            ("PETTY-001", "Office Petty Cash", TreasuryAccountType.PETTY_CASH, 500.0),
            ("VAULT-01", "Main Vault", TreasuryAccountType.VAULT, 10000.0),
            ("SAFE-01", "Office Safe", TreasuryAccountType.SAFE, 2000.0),
        ]
        for code, name, atype, balance in defaults:
            account = TreasuryAccount.create(
                tenant_id=tenant_id,
                code=code,
                name=name,
                account_type=atype.value,
                currency="USD",
                bank_name="Default Bank" if atype == TreasuryAccountType.BANK else None,
            )
            account.balance = balance
            await self._accounts.save(account)
        await self._emit_liquidity(tenant_id, f"seed-{tenant_id}")

    async def create_account(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        account_type: str,
        currency: str = "USD",
        bank_name: str | None = None,
        account_number: str | None = None,
        opening_balance: float = 0.0,
    ) -> Result[dict]:
        if await self._accounts.find_by_code(tenant_id, code):
            return Result.fail("treasury.errors.account_exists")
        try:
            TreasuryAccountType(account_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_account_type")
        account = TreasuryAccount.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            account_type=account_type,
            currency=currency,
            bank_name=bank_name,
            account_number=account_number,
        )
        account.balance = round(opening_balance, 2)
        await self._accounts.save(account)
        await self._emit_liquidity(tenant_id, f"account-{account.id}")
        return Result.ok(account.to_dict())

    async def list_accounts(self, tenant_id: str) -> Result[list[dict]]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in sorted(accounts, key=lambda x: x.code)])

    async def get_account(self, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("treasury.errors.account_not_found")
        return Result.ok(account.to_dict())

    async def create_transfer(
        self,
        *,
        tenant_id: str,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        currency: str,
        instrument: str,
        reference: str,
        description: str | None = None,
        cheque_number: str | None = None,
        require_approval: bool = True,
    ) -> Result[dict]:
        try:
            PaymentInstrument(instrument)
        except ValueError:
            return Result.fail("treasury.errors.invalid_instrument")
        if instrument == PaymentInstrument.CHEQUE.value and not cheque_number:
            return Result.fail("treasury.errors.cheque_number_required")
        from_acc = await self._accounts.find_by_id(from_account_id)
        to_acc = await self._accounts.find_by_id(to_account_id)
        if not from_acc or not to_acc or from_acc.tenant_id != tenant_id:
            return Result.fail("treasury.errors.account_not_found")
        if from_acc.currency != currency or to_acc.currency != currency:
            return Result.fail("treasury.errors.currency_mismatch")
        transfer = TreasuryTransfer.create_draft(
            tenant_id=tenant_id,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            currency=currency,
            instrument=instrument,
            reference=reference,
            description=description,
            cheque_number=cheque_number,
            require_approval=require_approval,
        )
        await self._transfers.save(transfer)
        if not require_approval:
            return await self._execute_transfer(transfer, f"auto-{transfer.id}")
        return Result.ok(transfer.to_dict())

    async def submit_transfer(self, transfer_id: str, correlation_id: str) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("treasury.errors.transfer_not_found")
        transfer.submit_for_approval()
        await self._transfers.save(transfer)
        await publish_integration_event(
            TreasuryTransferApprovalRequestedIntegration(
                tenant_id=TenantId.create(transfer.tenant_id),
                correlation_id=correlation_id,
                transfer_id=str(transfer.id),
                amount=transfer.amount,
                instrument=transfer.instrument,
            )
        )
        return Result.ok(transfer.to_dict())

    async def approve_transfer(
        self, transfer_id: str, correlation_id: str, workflow_instance_id: str | None = None
    ) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("treasury.errors.transfer_not_found")
        transfer.approve(workflow_instance_id=workflow_instance_id)
        await self._transfers.save(transfer)
        return await self._execute_transfer(transfer, correlation_id)

    async def reject_transfer(self, transfer_id: str) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("treasury.errors.transfer_not_found")
        transfer.reject()
        await self._transfers.save(transfer)
        return Result.ok(transfer.to_dict())

    async def list_transfers(self, tenant_id: str) -> Result[list[dict]]:
        transfers = await self._transfers.list_by_tenant(tenant_id)
        return Result.ok([t.to_dict() for t in sorted(transfers, key=lambda x: x.created_at, reverse=True)])

    async def create_reconciliation(
        self,
        *,
        tenant_id: str,
        treasury_account_id: str,
        statement_date: str,
        statement_balance: float,
        statement_items: list[dict],
        book_items: list[dict] | None = None,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(treasury_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.account_not_found")
        book = book_items or []
        if not book:
            transfers = await self._transfers.list_by_tenant(tenant_id)
            book = [
                {
                    "reference": t.reference,
                    "amount": t.amount,
                    "date": t.executed_at.isoformat() if t.executed_at else "",
                    "type": "transfer",
                }
                for t in transfers
                if t.status == TransferStatus.EXECUTED
                and t.from_account_id == treasury_account_id
            ]
        recon = BankReconciliation.create(
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            statement_date=statement_date,
            statement_balance=statement_balance,
            book_balance=account.balance,
            statement_items=statement_items,
            book_items=book,
        )
        await self._reconciliations.save(recon)
        return Result.ok(recon.to_dict())

    async def list_reconciliations(self, tenant_id: str) -> Result[list[dict]]:
        records = await self._reconciliations.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in records])

    async def create_forecast(
        self,
        *,
        tenant_id: str,
        name: str,
        period_start: str,
        period_end: str,
        scenario: str = ForecastScenario.BASE.value,
        currency: str = "USD",
        opening_balance: float | None = None,
        projected_lines: list[dict],
    ) -> Result[dict]:
        try:
            ForecastScenario(scenario)
        except ValueError:
            return Result.fail("treasury.errors.invalid_scenario")
        if opening_balance is None:
            accounts = await self._accounts.list_by_tenant(tenant_id)
            opening_balance = round(
                sum(a.balance for a in accounts if a.is_active and a.currency == currency), 2
            )
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
        accounts = await self._accounts.list_by_tenant(tenant_id)
        transfers = await self._transfers.list_by_tenant(tenant_id)
        forecasts = await self._forecasts.list_by_tenant(tenant_id)
        reconciliations = await self._reconciliations.list_by_tenant(tenant_id)
        liquidity = compute_liquidity(accounts)
        pending = [
            t.to_dict()
            for t in transfers
            if t.status in (TransferStatus.DRAFT, TransferStatus.PENDING_APPROVAL)
        ]
        return Result.ok(
            build_dashboard(
                accounts=accounts,
                pending_transfers=pending,
                forecasts=[f.to_dict() for f in forecasts],
                reconciliations=[r.to_dict() for r in reconciliations],
                liquidity=liquidity,
            )
        )

    async def get_liquidity_analysis(self, tenant_id: str) -> Result[dict]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok(compute_liquidity(accounts))

    async def _execute_transfer(self, transfer: TreasuryTransfer, correlation_id: str) -> Result[dict]:
        from_acc = await self._accounts.find_by_id(transfer.from_account_id)
        to_acc = await self._accounts.find_by_id(transfer.to_account_id)
        if not from_acc or not to_acc:
            return Result.fail("treasury.errors.account_not_found")
        try:
            from_acc.debit(transfer.amount)
            to_acc.credit(transfer.amount)
        except ValueError:
            return Result.fail("treasury.errors.insufficient_balance")
        transfer.mark_executed()
        await self._accounts.save(from_acc)
        await self._accounts.save(to_acc)
        await self._transfers.save(transfer)
        await publish_integration_event(
            TreasuryTransferExecutedIntegration(
                tenant_id=TenantId.create(transfer.tenant_id),
                correlation_id=correlation_id,
                transfer_id=str(transfer.id),
                from_account_id=transfer.from_account_id,
                to_account_id=transfer.to_account_id,
                from_account_type=from_acc.account_type,
                to_account_type=to_acc.account_type,
                amount=transfer.amount,
                currency=transfer.currency,
                instrument=transfer.instrument,
            )
        )
        await self._emit_liquidity(transfer.tenant_id, correlation_id)
        return Result.ok(transfer.to_dict())

    async def _emit_liquidity(self, tenant_id: str, correlation_id: str) -> None:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        liquidity = compute_liquidity(accounts)
        await publish_integration_event(
            TreasuryLiquidityUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                total_balance=liquidity["total_balance"],
                liquid_balance=liquidity["liquid_balance"],
                liquidity_ratio=liquidity["liquidity_ratio"],
            )
        )
