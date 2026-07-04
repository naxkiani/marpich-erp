"""In-memory Financial Kernel persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.budget import Budget, RecurringJournal
from contexts.financial_kernel.domain.aggregates.chart_of_account import ChartOfAccount
from contexts.financial_kernel.domain.aggregates.currency import (
    CurrencyRevaluation,
    ExchangeRate,
    ExchangeRateSnapshot,
    TenantCurrencySettings,
)
from contexts.financial_kernel.domain.aggregates.dimensions import CostCenter, ProfitCenter
from contexts.financial_kernel.domain.aggregates.fiscal_period import FiscalPeriod, FiscalYear
from contexts.financial_kernel.domain.aggregates.journal import Journal
from contexts.financial_kernel.domain.ports.repositories import (
    IBudgetRepository,
    IChartOfAccountRepository,
    IDimensionRepository,
    IFiscalPeriodRepository,
    IFiscalYearRepository,
    IJournalRepository,
    IRecurringJournalRepository,
)


class InMemoryChartOfAccountRepository(IChartOfAccountRepository):
    _accounts: dict[str, ChartOfAccount] = {}

    @classmethod
    def reset(cls) -> None:
        cls._accounts = {}

    def _key(self, tenant_id: str, code: str) -> str:
        return f"{tenant_id}:{code}"

    async def save(self, account: ChartOfAccount) -> None:
        self._accounts[self._key(account.tenant_id, account.code)] = account

    async def list_by_tenant(self, tenant_id: str) -> list[ChartOfAccount]:
        return [a for k, a in self._accounts.items() if k.startswith(f"{tenant_id}:")]

    async def find_by_id(self, account_id: str) -> ChartOfAccount | None:
        for account in self._accounts.values():
            if str(account.id) == account_id:
                return account
        return None

    async def find_by_code(self, tenant_id: str, code: str) -> ChartOfAccount | None:
        return self._accounts.get(self._key(tenant_id, code))

    async def find_by_key(self, tenant_id: str, account_key: str) -> ChartOfAccount | None:
        for account in self._accounts.values():
            if account.tenant_id == tenant_id and account.account_key == account_key:
                return account
        return None

    async def list_children(self, tenant_id: str, parent_account_id: str) -> list[ChartOfAccount]:
        return [
            a
            for a in self._accounts.values()
            if a.tenant_id == tenant_id and a.parent_account_id == parent_account_id
        ]


class InMemoryJournalRepository(IJournalRepository):
    _journals: dict[str, Journal] = {}

    @classmethod
    def reset(cls) -> None:
        cls._journals = {}

    async def save(self, journal: Journal) -> None:
        self._journals[str(journal.id)] = journal
        self._journals[f"idemp:{journal.tenant_id}:{journal.idempotency_key}"] = journal

    async def find_by_id(self, journal_id: str) -> Journal | None:
        j = self._journals.get(journal_id)
        return j if isinstance(j, Journal) else None

    async def find_by_idempotency(self, tenant_id: str, key: str) -> Journal | None:
        j = self._journals.get(f"idemp:{tenant_id}:{key}")
        return j if isinstance(j, Journal) else None

    async def list_by_tenant(self, tenant_id: str) -> list[Journal]:
        seen: set[str] = set()
        result = []
        for j in self._journals.values():
            if isinstance(j, Journal) and j.tenant_id == tenant_id and str(j.id) not in seen:
                seen.add(str(j.id))
                result.append(j)
        return result


class InMemoryFiscalYearRepository(IFiscalYearRepository):
    _years: dict[str, FiscalYear] = {}

    @classmethod
    def reset(cls) -> None:
        cls._years = {}

    async def save(self, year: FiscalYear) -> None:
        self._years[str(year.id)] = year

    async def list_by_tenant(self, tenant_id: str) -> list[FiscalYear]:
        return [y for y in self._years.values() if y.tenant_id == tenant_id]

    async def find_by_id(self, year_id: str) -> FiscalYear | None:
        return self._years.get(year_id)


class InMemoryFiscalPeriodRepository(IFiscalPeriodRepository):
    _periods: dict[str, FiscalPeriod] = {}

    @classmethod
    def reset(cls) -> None:
        cls._periods = {}

    async def save(self, period: FiscalPeriod) -> None:
        self._periods[str(period.id)] = period

    async def find_open(
        self, tenant_id: str, organization_id: str | None = None
    ) -> FiscalPeriod | None:
        for period in self._periods.values():
            if period.tenant_id == tenant_id and period.status == "open":
                if organization_id is None or period.organization_id == organization_id:
                    return period
        return None

    async def find_by_id(self, period_id: str) -> FiscalPeriod | None:
        return self._periods.get(period_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FiscalPeriod]:
        return [p for p in self._periods.values() if p.tenant_id == tenant_id]


class InMemoryDimensionRepository(IDimensionRepository):
    _cost: dict[str, CostCenter] = {}
    _profit: dict[str, ProfitCenter] = {}

    @classmethod
    def reset(cls) -> None:
        cls._cost = {}
        cls._profit = {}

    async def save_cost_center(self, center: CostCenter) -> None:
        self._cost[f"{center.tenant_id}:{center.code}"] = center

    async def save_profit_center(self, center: ProfitCenter) -> None:
        self._profit[f"{center.tenant_id}:{center.code}"] = center

    async def list_cost_centers(self, tenant_id: str) -> list[CostCenter]:
        return [c for k, c in self._cost.items() if k.startswith(f"{tenant_id}:")]

    async def list_profit_centers(self, tenant_id: str) -> list[ProfitCenter]:
        return [c for k, c in self._profit.items() if k.startswith(f"{tenant_id}:")]


class InMemoryBudgetRepository(IBudgetRepository):
    _budgets: dict[str, Budget] = {}

    @classmethod
    def reset(cls) -> None:
        cls._budgets = {}

    async def save(self, budget: Budget) -> None:
        self._budgets[str(budget.id)] = budget

    async def find_match(
        self, tenant_id: str, period_id: str, account_code: str, cost_center: str | None
    ) -> Budget | None:
        for b in self._budgets.values():
            if (
                b.tenant_id == tenant_id
                and b.period_id == period_id
                and b.account_code == account_code
                and b.cost_center == cost_center
            ):
                return b
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[Budget]:
        return [b for b in self._budgets.values() if b.tenant_id == tenant_id]


class InMemoryRecurringJournalRepository(IRecurringJournalRepository):
    _templates: dict[str, RecurringJournal] = {}

    @classmethod
    def reset(cls) -> None:
        cls._templates = {}

    async def save(self, template: RecurringJournal) -> None:
        self._templates[str(template.id)] = template

    async def find_by_id(self, template_id: str) -> RecurringJournal | None:
        return self._templates.get(template_id)

    async def list_by_tenant(self, tenant_id: str) -> list[RecurringJournal]:
        return [t for t in self._templates.values() if t.tenant_id == tenant_id]


class InMemoryCurrencySettingsRepository:
    _settings: dict[str, TenantCurrencySettings] = {}

    @classmethod
    def reset(cls) -> None:
        cls._settings = {}

    async def save(self, settings: TenantCurrencySettings) -> None:
        self._settings[settings.tenant_id] = settings

    async def find_by_tenant(self, tenant_id: str) -> TenantCurrencySettings | None:
        return self._settings.get(tenant_id)


class InMemoryExchangeRateRepository:
    _rates: dict[str, ExchangeRate] = {}

    @classmethod
    def reset(cls) -> None:
        cls._rates = {}

    async def save(self, rate: ExchangeRate) -> None:
        self._rates[str(rate.id)] = rate

    async def list_by_tenant(self, tenant_id: str) -> list[ExchangeRate]:
        return [r for r in self._rates.values() if r.tenant_id == tenant_id]

    async def list_history(
        self,
        tenant_id: str,
        *,
        from_currency: str | None = None,
        to_currency: str | None = None,
        rate_type: str | None = None,
    ) -> list[ExchangeRate]:
        rows = await self.list_by_tenant(tenant_id)
        if from_currency:
            rows = [r for r in rows if r.from_currency == from_currency.upper()]
        if to_currency:
            rows = [r for r in rows if r.to_currency == to_currency.upper()]
        if rate_type:
            rows = [r for r in rows if r.rate_type == rate_type]
        return sorted(rows, key=lambda r: (r.effective_date, r.created_at), reverse=True)


class InMemoryExchangeRateSnapshotRepository:
    _snapshots: dict[str, ExchangeRateSnapshot] = {}

    @classmethod
    def reset(cls) -> None:
        cls._snapshots = {}

    async def save(self, snapshot: ExchangeRateSnapshot) -> None:
        self._snapshots[str(snapshot.id)] = snapshot
        if snapshot.journal_id:
            self._snapshots[f"journal:{snapshot.journal_id}"] = snapshot

    async def find_by_id(self, snapshot_id: str) -> ExchangeRateSnapshot | None:
        snap = self._snapshots.get(snapshot_id)
        return snap if isinstance(snap, ExchangeRateSnapshot) else None

    async def list_by_tenant(self, tenant_id: str) -> list[ExchangeRateSnapshot]:
        return [
            s
            for k, s in self._snapshots.items()
            if isinstance(s, ExchangeRateSnapshot) and s.tenant_id == tenant_id
        ]

    async def find_by_journal(self, journal_id: str) -> ExchangeRateSnapshot | None:
        snap = self._snapshots.get(f"journal:{journal_id}")
        return snap if isinstance(snap, ExchangeRateSnapshot) else None


class InMemoryCurrencyRevaluationRepository:
    _runs: dict[str, CurrencyRevaluation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._runs = {}

    async def save(self, revaluation: CurrencyRevaluation) -> None:
        self._runs[str(revaluation.id)] = revaluation

    async def find_by_id(self, revaluation_id: str) -> CurrencyRevaluation | None:
        return self._runs.get(revaluation_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CurrencyRevaluation]:
        return [r for r in self._runs.values() if r.tenant_id == tenant_id]
