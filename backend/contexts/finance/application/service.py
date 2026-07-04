"""Finance application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.finance.application.commands.record_journal_from_accounting import (
    RecordJournalFromAccountingCommand,
)
from contexts.finance.application.ports.accounting_events import IAccountingEventAdapter
from contexts.finance.application.services.chart_seeder import build_default_accounts
from contexts.finance.domain.aggregates.account import Account, AccountType
from contexts.finance.domain.aggregates.fiscal_period import FiscalPeriod
from contexts.finance.domain.aggregates.journal_entry import JournalEntry
from contexts.finance.domain.events.integration_events import JournalRecordedIntegration
from contexts.finance.domain.ports.repositories import (
    IAccountRepository,
    IFiscalPeriodRepository,
    IJournalEntryRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleFinanceAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "finance", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class FinanceApplicationService:
    def __init__(
        self,
        accounts: IAccountRepository,
        periods: IFiscalPeriodRepository,
        journals: IJournalEntryRepository,
        accounting_events: IAccountingEventAdapter,
        audit: ConsoleFinanceAudit | None = None,
    ) -> None:
        self._accounts = accounts
        self._periods = periods
        self._journals = journals
        self._accounting_events = accounting_events
        self._audit = audit or ConsoleFinanceAudit()

    async def ensure_chart_of_accounts(self, tenant_id: str) -> None:
        existing = await self._accounts.list_accounts(tenant_id)
        if existing:
            return
        for account in build_default_accounts(tenant_id):
            await self._accounts.save(account)

    async def _ensure_default_open_period(self, tenant_id: str) -> None:
        if not await self._periods.find_open_period(tenant_id):
            period = FiscalPeriod.open_period(
                tenant_id=tenant_id,
                name="Default Period",
                start_date="2025-01-01",
                end_date="2025-12-31",
            )
            await self._periods.save(period)

    async def handle_accounting_journal_posted(self, envelope: dict) -> None:
        command = await self._accounting_events.parse_journal_posted(envelope)
        await self.record_journal_from_accounting(command)

    async def record_journal_from_accounting(
        self, command: RecordJournalFromAccountingCommand
    ) -> Result[dict]:
        await self.ensure_chart_of_accounts(command.tenant_id)

        existing = await self._journals.find_by_external_journal(
            command.tenant_id, command.external_journal_id
        )
        if existing:
            return Result.ok(existing.to_dict())

        open_period = await self._periods.find_open_period(command.tenant_id)
        if not open_period:
            await self._ensure_default_open_period(command.tenant_id)
            open_period = await self._periods.find_open_period(command.tenant_id)
        if not open_period:
            return Result.fail("finance.errors.no_open_period")

        entry = JournalEntry.from_accounting_event(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            external_journal_id=command.external_journal_id,
            source_type=command.source_type,
            source_id=command.source_id,
            currency=command.currency,
            lines=command.lines,
        )

        for line in command.lines:
            code = line.get("account_code", "")
            account = await self._accounts.find_by_code(command.tenant_id, code)
            if not account:
                return Result.fail(f"finance.errors.unknown_account:{code}")
            debit = float(line.get("debit", 0.0))
            credit = float(line.get("credit", 0.0))
            if debit:
                account.apply_debit(debit)
            if credit:
                account.apply_credit(credit)
            await self._accounts.save(account)

        await self._journals.save(entry)

        event = JournalRecordedIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            journal_entry_id=entry.id,
            source_type=entry.source_type,
            source_id=entry.source_id,
        )
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="finance.journal.recorded",
            resource_type="journal_entry",
            resource_id=str(entry.id),
            payload={"source_type": entry.source_type, "source_id": entry.source_id},
        )
        return Result.ok(entry.to_dict())

    async def open_fiscal_period(
        self,
        *,
        tenant_id: str,
        name: str,
        start_date: str,
        end_date: str,
        correlation_id: str,
    ) -> Result[dict]:
        await self.ensure_chart_of_accounts(tenant_id)
        open_period = await self._periods.find_open_period(tenant_id)
        if open_period:
            return Result.fail("finance.errors.period_already_open")

        period = FiscalPeriod.open_period(
            tenant_id=tenant_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
        )
        await self._periods.save(period)

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="finance.period.opened",
            resource_type="fiscal_period",
            resource_id=str(period.id),
        )
        return Result.ok(period.to_dict())

    async def close_fiscal_period(
        self, tenant_id: str, period_id: str, correlation_id: str
    ) -> Result[dict]:
        period = await self._periods.find_by_id(tenant_id, UniqueId.from_string(period_id))
        if not period:
            return Result.fail("finance.errors.period_not_found")

        event = period.close(correlation_id)
        await self._periods.save(period)
        await publish_integration_event(event)

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="finance.period.closed",
            resource_type="fiscal_period",
            resource_id=str(period.id),
        )
        return Result.ok(period.to_dict())

    async def create_account(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        account_type: str,
        correlation_id: str,
    ) -> Result[dict]:
        await self.ensure_chart_of_accounts(tenant_id)
        existing = await self._accounts.find_by_code(tenant_id, code)
        if existing:
            return Result.fail("finance.errors.account_exists")

        try:
            acct_type = AccountType(account_type)
        except ValueError:
            return Result.fail("finance.errors.invalid_account_type")

        account = Account.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            account_type=acct_type,
        )
        await self._accounts.save(account)

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="finance.account.created",
            resource_type="account",
            resource_id=str(account.id),
        )
        return Result.ok(account.to_dict())

    async def list_accounts(self, tenant_id: str) -> Result[list[dict]]:
        await self.ensure_chart_of_accounts(tenant_id)
        accounts = await self._accounts.list_accounts(tenant_id)
        return Result.ok([a.to_dict() for a in sorted(accounts, key=lambda a: a.code)])

    async def list_periods(self, tenant_id: str) -> Result[list[dict]]:
        periods = await self._periods.list_periods(tenant_id)
        return Result.ok([p.to_dict() for p in periods])

    async def list_journal_entries(self, tenant_id: str) -> Result[list[dict]]:
        entries = await self._journals.list_entries(tenant_id)
        return Result.ok([e.to_dict() for e in entries])

    async def find_journal_by_source(
        self, tenant_id: str, source_type: str, source_id: str
    ) -> Result[dict]:
        entry = await self._journals.find_by_source(tenant_id, source_type, source_id)
        if not entry:
            return Result.fail("finance.errors.journal_not_found")
        return Result.ok(entry.to_dict())

    async def trial_balance(self, tenant_id: str) -> Result[dict]:
        await self.ensure_chart_of_accounts(tenant_id)
        accounts = await self._accounts.list_accounts(tenant_id)
        rows = [a.to_dict() for a in sorted(accounts, key=lambda a: a.code)]
        total_debits = sum(
            a.balance for a in accounts if a.account_type in (AccountType.ASSET, AccountType.EXPENSE)
        )
        total_credits = sum(
            a.balance
            for a in accounts
            if a.account_type in (AccountType.LIABILITY, AccountType.EQUITY, AccountType.REVENUE)
        )
        return Result.ok(
            {
                "accounts": rows,
                "total_debits": round(total_debits, 2),
                "total_credits": round(total_credits, 2),
            }
        )
