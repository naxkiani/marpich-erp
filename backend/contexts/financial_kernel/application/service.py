"""Financial Kernel + Enterprise GL application service."""
from __future__ import annotations

from contexts.financial_kernel.application.constants.industry_coa import (
    INDUSTRY_COST_CENTERS,
    INDUSTRY_PACK_TO_COA,
    build_accounts,
    list_country_templates,
    list_industry_templates,
    materialize_template_tree,
)
from contexts.financial_kernel.domain.aggregates.budget import Budget, RecurringJournal
from contexts.financial_kernel.domain.aggregates.chart_of_account import (
    AccountCategory,
    AccountType,
    ChartOfAccount,
    TemplateSource,
)
from contexts.financial_kernel.domain.aggregates.currency import (
    CurrencyRevaluation,
    ExchangeRate,
    RateSource,
    RateType,
    TenantCurrencySettings,
)
from contexts.financial_kernel.domain.aggregates.dimensions import CostCenter
from contexts.financial_kernel.domain.aggregates.fiscal_period import FiscalPeriod, FiscalYear
from contexts.financial_kernel.domain.aggregates.journal import Journal, JournalStatus, PostingMode
from contexts.financial_kernel.domain.events.integration_events import (
    BudgetExceededIntegration,
    CoaSeededIntegration,
    CurrencyRevaluationCompletedIntegration,
    ExchangeRatesUpdatedIntegration,
    JournalApprovalRequestedIntegration,
    JournalApprovedIntegration,
    JournalPostedIntegration,
    JournalReversedIntegration,
    RecurringExecutedIntegration,
)
from contexts.financial_kernel.domain.ports.repositories import (
    IBudgetRepository,
    IChartOfAccountRepository,
    ICurrencyRevaluationRepository,
    ICurrencySettingsRepository,
    IDimensionRepository,
    IExchangeRateRepository,
    IExchangeRateSnapshotRepository,
    IFiscalPeriodRepository,
    IFiscalYearRepository,
    IJournalRepository,
    IRecurringJournalRepository,
)
from contexts.financial_kernel.domain.services.coa_tree_service import (
    build_account_tree,
    validate_parent_assignment,
)
from contexts.financial_kernel.domain.services.currency_engine import (
    build_rate_snapshot,
    compute_revaluation_lines,
    convert_amount,
    resolve_rate_from_list,
)
from contexts.financial_kernel.infrastructure.adapters.exchange_rate_provider import (
    CentralBankRateProvider,
    StubExchangeRateProvider,
)
from contexts.financial_kernel.domain.services.gl_engine import (
    apply_multi_currency,
    build_reversal_lines,
    compute_expense_total,
    validate_journal_lines,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class FinancialKernelApplicationService:
    def __init__(
        self,
        accounts: IChartOfAccountRepository,
        journals: IJournalRepository,
        periods: IFiscalPeriodRepository,
        years: IFiscalYearRepository,
        dimensions: IDimensionRepository,
        budgets: IBudgetRepository,
        recurring: IRecurringJournalRepository,
        currency_settings: ICurrencySettingsRepository,
        exchange_rates: IExchangeRateRepository,
        rate_snapshots: IExchangeRateSnapshotRepository,
        revaluations: ICurrencyRevaluationRepository,
        rate_provider: StubExchangeRateProvider | None = None,
        central_bank_provider: CentralBankRateProvider | None = None,
    ) -> None:
        self._accounts = accounts
        self._journals = journals
        self._periods = periods
        self._years = years
        self._dimensions = dimensions
        self._budgets = budgets
        self._recurring = recurring
        self._currency_settings = currency_settings
        self._exchange_rates = exchange_rates
        self._rate_snapshots = rate_snapshots
        self._revaluations = revaluations
        self._rate_provider = rate_provider or StubExchangeRateProvider()
        self._central_bank_provider = central_bank_provider or CentralBankRateProvider()

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        industry_pack = (envelope.get("payload") or {}).get("industry_pack", "retail")
        if await self._accounts.list_by_tenant(tenant_id):
            return
        template_key = INDUSTRY_PACK_TO_COA.get(industry_pack, "coa.retail")
        for account in build_accounts(tenant_id, template_key):
            await self._accounts.save(account)
        for code, name in INDUSTRY_COST_CENTERS.get(industry_pack, []):
            await self._dimensions.save_cost_center(
                CostCenter.create(tenant_id=tenant_id, code=code, name=name)
            )
        year = FiscalYear.create(
            tenant_id=tenant_id,
            organization_id=None,
            name="FY2025",
            start_date="2025-01-01",
            end_date="2025-12-31",
        )
        await self._years.save(year)
        if not await self._periods.find_open(tenant_id):
            await self._periods.save(
                FiscalPeriod.open_period(
                    tenant_id=tenant_id,
                    organization_id=None,
                    branch_id=None,
                    fiscal_year_id=str(year.id),
                    name="Period 01",
                    start_date="2025-01-01",
                    end_date="2025-12-31",
                )
            )
        await publish_integration_event(
            CoaSeededIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"coa-seed-{tenant_id}",
                industry_pack=industry_pack,
                account_count=len(await self._accounts.list_by_tenant(tenant_id)),
            )
        )
        await self._seed_currency_defaults(tenant_id)

    async def _seed_currency_defaults(self, tenant_id: str) -> None:
        if await self._currency_settings.find_by_tenant(tenant_id):
            return
        settings = TenantCurrencySettings.create_default(tenant_id=tenant_id)
        await self._currency_settings.save(settings)
        for from_c, to_c, rate in [("USD", "EUR", 0.92), ("USD", "GBP", 0.79), ("USD", "IRR", 42000.0)]:
            await self._exchange_rates.save(
                ExchangeRate.create(
                    tenant_id=tenant_id,
                    from_currency=from_c,
                    to_currency=to_c,
                    rate=rate,
                    rate_type=RateType.SPOT.value,
                    rate_source=RateSource.SYSTEM.value,
                )
            )

    async def create_account(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        account_type: str | None = None,
        account_category: str | None = None,
        account_key: str | None = None,
        parent_account_id: str | None = None,
        account_group: str | None = None,
        is_posting: bool = True,
    ) -> Result[dict]:
        if await self._accounts.find_by_code(tenant_id, code):
            return Result.fail("financial_kernel.errors.account_exists")
        if account_key and await self._accounts.find_by_key(tenant_id, account_key):
            return Result.fail("financial_kernel.errors.account_key_exists")
        try:
            category = _resolve_account_category(account_category, account_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_account_type")

        parent = None
        level = 0
        tree_path = account_key or code
        if parent_account_id:
            parent = await self._accounts.find_by_id(parent_account_id)
            if not parent or parent.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.parent_not_found")
            level = parent.level + 1
            tree_path = f"{parent.tree_path}/{account_key or code}"

        account = ChartOfAccount.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            account_category=category,
            account_key=account_key,
            parent_account_id=parent_account_id,
            level=level,
            tree_path=tree_path,
            account_group=account_group,
            is_posting=is_posting,
            template_source=TemplateSource.TENANT,
        )
        if parent:
            all_accounts = await self._accounts.list_by_tenant(tenant_id)
            ok, reason = validate_parent_assignment(account, parent, all_accounts)
            if not ok:
                return Result.fail(f"financial_kernel.errors.parent.{reason}")
        await self._accounts.save(account)
        return Result.ok(account.to_dict())

    async def get_account_tree(self, tenant_id: str) -> Result[list[dict]]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok(build_account_tree(accounts))

    async def get_account(self, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("financial_kernel.errors.account_not_found")
        return Result.ok(account.to_dict())

    async def list_account_children(self, tenant_id: str, parent_account_id: str) -> Result[list[dict]]:
        children = await self._accounts.list_children(tenant_id, parent_account_id)
        return Result.ok([c.to_dict() for c in sorted(children, key=lambda x: x.code)])

    async def list_coa_templates(self) -> Result[dict]:
        return Result.ok(
            {
                "industry": list_industry_templates(),
                "country": list_country_templates(),
            }
        )

    async def apply_coa_template(
        self,
        *,
        tenant_id: str,
        template_key: str,
        template_type: str = "industry",
        code_overrides: dict[str, str] | None = None,
        code_prefix: str = "",
        country_code: str | None = None,
        merge: bool = False,
    ) -> Result[dict]:
        if not merge and await self._accounts.list_by_tenant(tenant_id):
            return Result.fail("financial_kernel.errors.coa_already_seeded")
        try:
            accounts = materialize_template_tree(
                tenant_id=tenant_id,
                template_key=template_key,
                template_type=template_type,
                code_overrides=code_overrides,
                code_prefix=code_prefix,
                country_code=country_code,
            )
        except KeyError:
            return Result.fail("financial_kernel.errors.template_not_found")
        for account in accounts:
            if await self._accounts.find_by_code(tenant_id, account.code):
                return Result.fail(f"financial_kernel.errors.account_exists:{account.code}")
            await self._accounts.save(account)
        return Result.ok(
            {
                "template_key": template_key,
                "template_type": template_type,
                "account_count": len(accounts),
                "tree": build_account_tree(accounts),
            }
        )

    async def resolve_account_code(self, tenant_id: str, account_key: str) -> Result[str]:
        account = await self._accounts.find_by_key(tenant_id, account_key)
        if not account:
            return Result.fail(f"financial_kernel.errors.unknown_account_key:{account_key}")
        return Result.ok(account.code)

    async def list_accounts(self, tenant_id: str) -> Result[list[dict]]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in sorted(accounts, key=lambda x: x.code)])

    async def create_fiscal_year(
        self, *, tenant_id: str, organization_id: str | None, name: str, start_date: str, end_date: str
    ) -> Result[dict]:
        year = FiscalYear.create(
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
        )
        await self._years.save(year)
        return Result.ok(year.to_dict())

    async def list_fiscal_years(self, tenant_id: str) -> Result[list[dict]]:
        years = await self._years.list_by_tenant(tenant_id)
        return Result.ok([y.to_dict() for y in years])

    async def create_period(
        self,
        *,
        tenant_id: str,
        organization_id: str | None,
        branch_id: str | None,
        fiscal_year_id: str,
        name: str,
        start_date: str,
        end_date: str,
    ) -> Result[dict]:
        period = FiscalPeriod.open_period(
            tenant_id=tenant_id,
            organization_id=organization_id,
            branch_id=branch_id,
            fiscal_year_id=fiscal_year_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
        )
        await self._periods.save(period)
        return Result.ok(period.to_dict())

    async def list_periods(self, tenant_id: str) -> Result[list[dict]]:
        periods = await self._periods.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in periods])

    async def list_cost_centers(self, tenant_id: str) -> Result[list[dict]]:
        centers = await self._dimensions.list_cost_centers(tenant_id)
        return Result.ok([c.to_dict() for c in centers])

    async def list_journals(self, tenant_id: str) -> Result[list[dict]]:
        journals = await self._journals.list_by_tenant(tenant_id)
        return Result.ok([j.to_dict() for j in sorted(journals, key=lambda x: x.created_at)])

    async def get_journal(self, journal_id: str) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        return Result.ok(journal.to_dict())

    async def post_journal(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        lines: list[dict],
        currency: str,
        correlation_id: str,
        idempotency_key: str | None = None,
        organization_id: str | None = None,
        branch_id: str | None = None,
        base_currency: str = "USD",
        exchange_rate: float = 1.0,
    ) -> Result[dict]:
        return await self._post(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            posting_mode=PostingMode.AUTOMATIC,
            organization_id=organization_id,
            branch_id=branch_id,
        )

    async def post_manual_journal(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        lines: list[dict],
        currency: str,
        correlation_id: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        base_currency: str = "USD",
        exchange_rate: float = 1.0,
    ) -> Result[dict]:
        return await self._post(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            correlation_id=correlation_id,
            idempotency_key=f"manual:{source_document_id}",
            posting_mode=PostingMode.MANUAL,
            organization_id=organization_id,
            branch_id=branch_id,
            require_approval=True,
        )

    async def submit_journal_for_approval(self, journal_id: str, correlation_id: str) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        journal.submit_for_approval()
        await self._journals.save(journal)
        await publish_integration_event(
            JournalApprovalRequestedIntegration(
                tenant_id=TenantId.create(journal.tenant_id),
                correlation_id=correlation_id,
                journal_id=journal_id,
            )
        )
        return Result.ok(journal.to_dict())

    async def approve_journal(self, journal_id: str, correlation_id: str) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        budget_ok = await self._validate_and_consume_budget(journal)
        if not budget_ok.succeeded:
            return budget_ok
        journal.approve_and_post()
        await self._apply_balances(journal)
        await self._journals.save(journal)
        await self._emit_posted(journal, correlation_id)
        await publish_integration_event(
            JournalApprovedIntegration(
                tenant_id=TenantId.create(journal.tenant_id),
                correlation_id=correlation_id,
                journal_id=journal_id,
            )
        )
        return Result.ok(journal.to_dict())

    async def reverse_journal(self, journal_id: str, correlation_id: str) -> Result[dict]:
        original = await self._journals.find_by_id(journal_id)
        if not original:
            return Result.fail("financial_kernel.errors.journal_not_found")
        if original.status != JournalStatus.POSTED:
            return Result.fail("financial_kernel.errors.only_posted_reversible")
        reversal_lines = build_reversal_lines(original.lines)
        result = await self._post(
            tenant_id=original.tenant_id,
            source_context="financial_kernel",
            source_document_id=f"reversal-{journal_id}",
            lines=reversal_lines,
            currency=original.currency,
            base_currency=original.base_currency,
            exchange_rate=original.exchange_rate,
            correlation_id=correlation_id,
            idempotency_key=f"reversal:{journal_id}",
            posting_mode=PostingMode.REVERSING,
            organization_id=original.organization_id,
            branch_id=original.branch_id,
            period_id=original.period_id,
            fiscal_year_id=original.fiscal_year_id,
            reverses_journal_id=journal_id,
        )
        if not result.succeeded:
            return result
        reversal = await self._journals.find_by_id(result.unwrap()["id"])
        assert reversal is not None
        original.mark_reversed(str(reversal.id))
        await self._journals.save(original)
        await publish_integration_event(
            JournalReversedIntegration(
                tenant_id=TenantId.create(original.tenant_id),
                correlation_id=correlation_id,
                original_journal_id=journal_id,
                reversal_journal_id=str(reversal.id),
            )
        )
        data = reversal.to_dict()
        data["reversed_original_id"] = journal_id
        return Result.ok(data)

    async def create_recurring_journal(
        self,
        *,
        tenant_id: str,
        organization_id: str | None,
        name: str,
        schedule: str,
        currency: str,
        base_currency: str,
        lines: list[dict],
        requires_approval: bool,
    ) -> Result[dict]:
        ok, reason = validate_journal_lines(lines)
        if not ok:
            return Result.fail(f"financial_kernel.errors.journal.{reason}")
        template = RecurringJournal.create(
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name,
            schedule=schedule,
            currency=currency,
            base_currency=base_currency,
            lines=lines,
            requires_approval=requires_approval,
        )
        await self._recurring.save(template)
        return Result.ok(template.to_dict())

    async def list_recurring_journals(self, tenant_id: str) -> Result[list[dict]]:
        templates = await self._recurring.list_by_tenant(tenant_id)
        return Result.ok([t.to_dict() for t in templates])

    async def run_recurring_journal(self, template_id: str, correlation_id: str) -> Result[dict]:
        template = await self._recurring.find_by_id(template_id)
        if not template or not template.is_active:
            return Result.fail("financial_kernel.errors.recurring_not_found")
        mode = PostingMode.MANUAL if template.requires_approval else PostingMode.RECURRING
        result = await self._post(
            tenant_id=template.tenant_id,
            source_context="financial_kernel",
            source_document_id=f"recurring-{template_id}-{template.run_count + 1}",
            lines=template.lines,
            currency=template.currency,
            base_currency=template.base_currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=f"recurring:{template_id}:{template.run_count + 1}",
            posting_mode=mode,
            organization_id=template.organization_id,
            recurring_template_id=template_id,
            require_approval=template.requires_approval,
        )
        if result.succeeded:
            template.record_run()
            await self._recurring.save(template)
            await publish_integration_event(
                RecurringExecutedIntegration(
                    tenant_id=TenantId.create(template.tenant_id),
                    correlation_id=correlation_id,
                    template_id=template_id,
                    journal_id=result.unwrap()["id"],
                )
            )
        return result

    async def create_budget(
        self,
        *,
        tenant_id: str,
        organization_id: str | None,
        period_id: str,
        account_code: str,
        amount: float,
        cost_center: str | None = None,
        currency: str = "USD",
    ) -> Result[dict]:
        budget = Budget.create(
            tenant_id=tenant_id,
            organization_id=organization_id,
            period_id=period_id,
            account_code=account_code,
            amount=amount,
            cost_center=cost_center,
            currency=currency,
        )
        await self._budgets.save(budget)
        return Result.ok(budget.to_dict())

    async def list_budgets(self, tenant_id: str) -> Result[list[dict]]:
        budgets = await self._budgets.list_by_tenant(tenant_id)
        return Result.ok([b.to_dict() for b in budgets])

    async def get_trial_balance(self, tenant_id: str) -> Result[list[dict]]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        rows = []
        for account in sorted(accounts, key=lambda a: a.code):
            if not account.is_posting or not account.account_type:
                continue
            if account.balance >= 0:
                rows.append({
                    "account_code": account.code,
                    "account_name": account.name,
                    "debit_balance": account.balance,
                    "credit_balance": 0.0,
                })
            else:
                rows.append({
                    "account_code": account.code,
                    "account_name": account.name,
                    "debit_balance": 0.0,
                    "credit_balance": abs(account.balance),
                })
        return Result.ok(rows)

    async def convert_currency(
        self,
        *,
        tenant_id: str,
        amount: str,
        from_currency: str,
        to_currency: str,
        rate_type: str | None = None,
        as_of_date: str | None = None,
    ) -> Result[dict]:
        resolved = await self._resolve_rate(
            tenant_id,
            from_currency.strip().upper(),
            to_currency.strip().upper(),
            rate_type=rate_type,
            as_of_date=as_of_date,
        )
        if not resolved.succeeded:
            return resolved
        rate = resolved.unwrap()
        converted = convert_amount(float(amount), rate["rate"])
        return Result.ok({
            "tenant_id": tenant_id,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper(),
            "amount": amount,
            "converted_amount": str(converted),
            "rate": rate["rate"],
            "rate_type": rate["rate_type"],
            "rate_source": rate["rate_source"],
            "effective_date": rate["effective_date"],
        })

    async def get_currency_config(self, tenant_id: str) -> Result[dict]:
        settings = await self._ensure_currency_settings(tenant_id)
        return Result.ok(settings.to_dict())

    async def update_currency_config(
        self,
        *,
        tenant_id: str,
        base_currency: str | None = None,
        reporting_currency: str | None = None,
        auto_update_enabled: bool | None = None,
        auto_update_provider: str | None = None,
    ) -> Result[dict]:
        settings = await self._ensure_currency_settings(tenant_id)
        if base_currency:
            settings.set_base_currency(base_currency)
        if reporting_currency:
            settings.set_reporting_currency(reporting_currency)
        if auto_update_enabled is not None:
            settings.auto_update_enabled = auto_update_enabled
        if auto_update_provider:
            settings.auto_update_provider = auto_update_provider
        await self._currency_settings.save(settings)
        return Result.ok(settings.to_dict())

    async def list_currencies(self, tenant_id: str) -> Result[list[dict]]:
        settings = await self._ensure_currency_settings(tenant_id)
        return Result.ok(
            [{"code": c, "is_base": c == settings.base_currency, "is_reporting": c == settings.reporting_currency}
             for c in settings.enabled_currencies]
        )

    async def add_currency(self, tenant_id: str, code: str) -> Result[dict]:
        settings = await self._ensure_currency_settings(tenant_id)
        settings.add_currency(code)
        await self._currency_settings.save(settings)
        return Result.ok(settings.to_dict())

    async def list_exchange_rates(
        self,
        tenant_id: str,
        *,
        from_currency: str | None = None,
        to_currency: str | None = None,
        rate_type: str | None = None,
    ) -> Result[list[dict]]:
        rates = await self._exchange_rates.list_history(
            tenant_id,
            from_currency=from_currency,
            to_currency=to_currency,
            rate_type=rate_type,
        )
        return Result.ok([r.to_dict() for r in rates])

    async def create_manual_rate(
        self,
        *,
        tenant_id: str,
        from_currency: str,
        to_currency: str,
        rate: float,
        effective_date: str | None = None,
    ) -> Result[dict]:
        entry = ExchangeRate.create(
            tenant_id=tenant_id,
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            rate_type=RateType.MANUAL.value,
            rate_source=RateSource.MANUAL.value,
            effective_date=effective_date,
        )
        await self._exchange_rates.save(entry)
        return Result.ok(entry.to_dict())

    async def import_central_bank_rates(
        self, *, tenant_id: str, central_bank: str = "fed"
    ) -> Result[dict]:
        settings = await self._ensure_currency_settings(tenant_id)
        fetched = await self._central_bank_provider.fetch_rates(
            base_currency=settings.base_currency,
            target_currencies=settings.enabled_currencies,
            central_bank=central_bank,
        )
        saved = []
        for row in fetched:
            entry = ExchangeRate.create(
                tenant_id=tenant_id,
                from_currency=row["from_currency"],
                to_currency=row["to_currency"],
                rate=row["rate"],
                rate_type=row["rate_type"],
                rate_source=row["rate_source"],
                effective_date=row["effective_date"],
                provider=row.get("provider"),
            )
            await self._exchange_rates.save(entry)
            saved.append(entry.to_dict())
        await publish_integration_event(
            ExchangeRatesUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"cb-rates-{tenant_id}",
                source="central_bank",
                rate_count=len(saved),
            )
        )
        return Result.ok({"imported": len(saved), "rates": saved})

    async def fetch_exchange_api_rates(self, *, tenant_id: str) -> Result[dict]:
        settings = await self._ensure_currency_settings(tenant_id)
        if not settings.auto_update_enabled:
            return Result.fail("financial_kernel.errors.auto_update_disabled")
        fetched = await self._rate_provider.fetch_spot_rates(
            base_currency=settings.base_currency,
            target_currencies=settings.enabled_currencies,
            provider=settings.auto_update_provider,
        )
        saved = []
        for row in fetched:
            entry = ExchangeRate.create(
                tenant_id=tenant_id,
                from_currency=row["from_currency"],
                to_currency=row["to_currency"],
                rate=row["rate"],
                rate_type=row["rate_type"],
                rate_source=row["rate_source"],
                effective_date=row["effective_date"],
                provider=row.get("provider"),
            )
            await self._exchange_rates.save(entry)
            saved.append(entry.to_dict())
        await publish_integration_event(
            ExchangeRatesUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"api-rates-{tenant_id}",
                source="exchange_api",
                rate_count=len(saved),
            )
        )
        return Result.ok({"imported": len(saved), "rates": saved})

    async def get_exchange_history(
        self,
        tenant_id: str,
        *,
        from_currency: str | None = None,
        to_currency: str | None = None,
        rate_type: str | None = None,
    ) -> Result[list[dict]]:
        return await self.list_exchange_rates(
            tenant_id,
            from_currency=from_currency,
            to_currency=to_currency,
            rate_type=rate_type,
        )

    async def list_rate_snapshots(self, tenant_id: str) -> Result[list[dict]]:
        snaps = await self._rate_snapshots.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in sorted(snaps, key=lambda x: x.created_at, reverse=True)])

    async def run_revaluation(
        self,
        *,
        tenant_id: str,
        period_id: str | None = None,
        revaluation_date: str | None = None,
        rate_type: str = RateType.SPOT.value,
        balances: list[dict] | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        from datetime import date

        settings = await self._ensure_currency_settings(tenant_id)
        rates_list = await self._exchange_rates.list_by_tenant(tenant_id)
        new_rates: dict[str, float] = {}
        for currency in settings.enabled_currencies:
            if currency == settings.base_currency:
                continue
            resolved = resolve_rate_from_list(
                rates_list,
                from_currency=currency,
                to_currency=settings.base_currency,
                rate_type=rate_type,
                as_of_date=revaluation_date or date.today().isoformat(),
            )
            if not resolved:
                resolved = resolve_rate_from_list(
                    rates_list,
                    from_currency=currency,
                    to_currency=settings.base_currency,
                    as_of_date=revaluation_date or date.today().isoformat(),
                )
            if resolved:
                new_rates[currency] = resolved.rate
        input_balances = balances or []
        lines = compute_revaluation_lines(
            input_balances,
            new_rates=new_rates,
            base_currency=settings.base_currency,
        )
        run = CurrencyRevaluation.create(
            tenant_id=tenant_id,
            period_id=period_id,
            revaluation_date=revaluation_date or date.today().isoformat(),
            base_currency=settings.base_currency,
            reporting_currency=settings.reporting_currency,
            rate_type=rate_type,
            lines=lines,
        )
        await self._revaluations.save(run)
        await publish_integration_event(
            CurrencyRevaluationCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"reval-{run.id}",
                revaluation_id=str(run.id),
                net_gain_loss=run.net_gain_loss,
            )
        )
        return Result.ok(run.to_dict())

    async def list_revaluations(self, tenant_id: str) -> Result[list[dict]]:
        runs = await self._revaluations.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in runs])

    async def get_gain_loss_report(self, tenant_id: str) -> Result[dict]:
        runs = await self._revaluations.list_by_tenant(tenant_id)
        total_gain = round(sum(r.total_gain for r in runs), 2)
        total_loss = round(sum(r.total_loss for r in runs), 2)
        return Result.ok({
            "tenant_id": tenant_id,
            "total_gain": total_gain,
            "total_loss": total_loss,
            "net_gain_loss": round(total_gain - total_loss, 2),
            "revaluation_count": len(runs),
            "runs": [r.to_dict() for r in runs],
        })

    async def _ensure_currency_settings(self, tenant_id: str) -> TenantCurrencySettings:
        settings = await self._currency_settings.find_by_tenant(tenant_id)
        if settings:
            return settings
        settings = TenantCurrencySettings.create_default(tenant_id=tenant_id)
        await self._currency_settings.save(settings)
        return settings

    async def _resolve_rate(
        self,
        tenant_id: str,
        from_currency: str,
        to_currency: str,
        *,
        rate_type: str | None = None,
        as_of_date: str | None = None,
    ) -> Result[dict]:
        if from_currency == to_currency:
            return Result.ok({
                "rate": 1.0,
                "rate_type": RateType.SPOT.value,
                "rate_source": RateSource.SYSTEM.value,
                "effective_date": as_of_date or "",
                "from_currency": from_currency,
                "to_currency": to_currency,
            })
        rates = await self._exchange_rates.list_by_tenant(tenant_id)
        resolved = resolve_rate_from_list(
            rates,
            from_currency=from_currency,
            to_currency=to_currency,
            rate_type=rate_type,
            as_of_date=as_of_date,
        )
        if not resolved:
            return Result.fail(
                f"financial_kernel.errors.rate_not_found:{from_currency}:{to_currency}"
            )
        return Result.ok(resolved.to_dict())

    async def calculate_tax(
        self, *, tenant_id: str, amount: str, tax_code: str, jurisdiction: str
    ) -> Result[dict]:
        rate = divmod(hash(tax_code + jurisdiction) % 20, 100)[0] / 100 + 0.05
        tax_amount = round(float(amount) * rate, 2)
        return Result.ok({
            "tenant_id": tenant_id,
            "amount": amount,
            "tax_code": tax_code,
            "jurisdiction": jurisdiction,
            "tax_rate": rate,
            "tax_amount": str(tax_amount),
        })

    async def _post(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        lines: list[dict],
        currency: str,
        base_currency: str,
        exchange_rate: float,
        correlation_id: str,
        idempotency_key: str | None,
        posting_mode: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        period_id: str | None = None,
        fiscal_year_id: str | None = None,
        recurring_template_id: str | None = None,
        reverses_journal_id: str | None = None,
        require_approval: bool = False,
        rate_type: str | None = None,
    ) -> Result[dict]:
        key = idempotency_key or f"{source_context}:{source_document_id}"
        existing = await self._journals.find_by_idempotency(tenant_id, key)
        if existing:
            return Result.ok(existing.to_dict())

        period = await self._periods.find_open(tenant_id, organization_id)
        if not period and not period_id:
            return Result.fail("financial_kernel.errors.no_open_period")

        ok, reason = validate_journal_lines(lines)
        if not ok:
            return Result.fail(f"financial_kernel.errors.journal.{reason}")

        for line in lines:
            account = await self._accounts.find_by_code(tenant_id, line["account_code"])
            if not account:
                return Result.fail(f"financial_kernel.errors.unknown_account:{line['account_code']}")
            if not account.accepts_gl_posting():
                return Result.fail(
                    f"financial_kernel.errors.non_posting_account:{line['account_code']}"
                )

        settings = await self._ensure_currency_settings(tenant_id)
        txn_currency = currency.upper()
        base_currency = (base_currency or settings.base_currency).upper()
        reporting_currency = settings.reporting_currency

        base_rate_result = await self._resolve_rate(
            tenant_id,
            txn_currency,
            base_currency,
            rate_type=rate_type,
        )
        if not base_rate_result.succeeded and txn_currency != base_currency:
            return base_rate_result
        base_rate_data = base_rate_result.unwrap() if base_rate_result.succeeded else {
            "rate": 1.0,
            "rate_type": RateType.SPOT.value,
            "rate_source": RateSource.SYSTEM.value,
            "effective_date": "",
        }
        if exchange_rate == 1.0 and txn_currency != base_currency:
            exchange_rate = float(base_rate_data["rate"])
        resolved_rate_type = rate_type or base_rate_data.get("rate_type", RateType.SPOT.value)

        reporting_rate_result = await self._resolve_rate(
            tenant_id,
            txn_currency,
            reporting_currency,
            rate_type=resolved_rate_type,
        )
        reporting_rate_data = (
            reporting_rate_result.unwrap()
            if reporting_rate_result.succeeded
            else base_rate_data
        )
        reporting_exchange_rate = float(reporting_rate_data["rate"])

        snapshot = build_rate_snapshot(
            tenant_id=tenant_id,
            transaction_currency=txn_currency,
            base_currency=base_currency,
            reporting_currency=reporting_currency,
            transaction_to_base=ExchangeRate.create(
                tenant_id=tenant_id,
                from_currency=txn_currency,
                to_currency=base_currency,
                rate=exchange_rate,
                rate_type=resolved_rate_type,
                rate_source=base_rate_data.get("rate_source", RateSource.SYSTEM.value),
                effective_date=base_rate_data.get("effective_date") or "",
            )
            if txn_currency != base_currency
            else None,
            transaction_to_reporting=ExchangeRate.create(
                tenant_id=tenant_id,
                from_currency=txn_currency,
                to_currency=reporting_currency,
                rate=reporting_exchange_rate,
                rate_type=resolved_rate_type,
                rate_source=reporting_rate_data.get("rate_source", RateSource.SYSTEM.value),
                effective_date=reporting_rate_data.get("effective_date") or "",
            )
            if txn_currency != reporting_currency
            else None,
            source_context=source_context,
            source_document_id=source_document_id,
        )

        enriched_lines = apply_multi_currency(
            lines,
            currency=txn_currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            reporting_currency=reporting_currency,
            reporting_exchange_rate=reporting_exchange_rate,
            rate_type=resolved_rate_type,
            rate_snapshot_id=str(snapshot.id),
        )
        journal = Journal.create_draft(
            tenant_id=tenant_id,
            organization_id=organization_id,
            branch_id=branch_id,
            fiscal_year_id=fiscal_year_id or (str(period.fiscal_year_id) if period else None),
            period_id=period_id or (str(period.id) if period else None),
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=key,
            currency=txn_currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            lines=enriched_lines,
            posting_mode=posting_mode,
            correlation_id=correlation_id,
            reporting_currency=reporting_currency,
            reporting_exchange_rate=reporting_exchange_rate,
            rate_snapshot_id=str(snapshot.id),
            rate_type=resolved_rate_type,
            recurring_template_id=recurring_template_id,
            reverses_journal_id=reverses_journal_id,
        )
        snapshot.journal_id = str(journal.id)
        await self._rate_snapshots.save(snapshot)

        if require_approval:
            await self._journals.save(journal)
            return Result.ok(journal.to_dict())

        budget_ok = await self._validate_and_consume_budget(journal)
        if not budget_ok.succeeded:
            return budget_ok

        journal.mark_posted()
        await self._apply_balances(journal)
        await self._journals.save(journal)
        await self._emit_posted(journal, correlation_id)
        return Result.ok(journal.to_dict())

    async def _validate_and_consume_budget(self, journal: Journal) -> Result[None]:
        if not journal.period_id:
            return Result.ok(None)
        account_types = {
            a.code: a.account_category.value
            for a in await self._accounts.list_by_tenant(journal.tenant_id)
        }
        for line in journal.lines:
            code = line.get("account_code", "")
            if account_types.get(code) != "expense":
                continue
            cost_center = line.get("cost_center")
            amount = float(line.get("debit", 0))
            budget = await self._budgets.find_match(
                journal.tenant_id, journal.period_id, code, cost_center
            )
            if not budget:
                continue
            if not budget.consume(amount):
                await publish_integration_event(
                    BudgetExceededIntegration(
                        tenant_id=TenantId.create(journal.tenant_id),
                        correlation_id=journal.correlation_id,
                        account_code=code,
                        cost_center=cost_center,
                        requested_amount=amount,
                        remaining=budget.remaining,
                    )
                )
                return Result.fail("financial_kernel.errors.budget_exceeded")
            await self._budgets.save(budget)
        return Result.ok(None)

    async def _apply_balances(self, journal: Journal) -> None:
        for line in journal.lines:
            account = await self._accounts.find_by_code(journal.tenant_id, line["account_code"])
            assert account is not None
            debit = float(line.get("debit", 0))
            credit = float(line.get("credit", 0))
            if debit:
                account.apply_debit(debit)
            if credit:
                account.apply_credit(credit)
            await self._accounts.save(account)

    async def _emit_posted(self, journal: Journal, correlation_id: str) -> None:
        await publish_integration_event(
            JournalPostedIntegration(
                tenant_id=TenantId.create(journal.tenant_id),
                correlation_id=correlation_id,
                journal_id=str(journal.id),
                posting_source_context=journal.source_context,
                source_document_id=journal.source_document_id,
                total_debit=journal.total_debits,
                total_credit=journal.total_credits,
                posting_mode=journal.posting_mode,
            )
        )


def _resolve_account_category(
    account_category: str | None, account_type: str | None
) -> AccountCategory:
    if account_category:
        return AccountCategory(account_category)
    if account_type:
        return AccountCategory(AccountType(account_type).value)
    raise ValueError("account_category or account_type required")
