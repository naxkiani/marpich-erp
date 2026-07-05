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
from contexts.financial_kernel.domain.aggregates.account_hierarchy import (
    AccountTree,
    AccountTreeVersion,
    TreeChangeType,
    TreeType,
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
from contexts.financial_kernel.domain.aggregates.fiscal_calendar import (
    CloseActionType,
    CloseLevel,
    CloseRequestStatus,
    FiscalCalendar,
    FiscalCalendarAuditLog,
    FiscalCloseRequest,
)
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
from contexts.financial_kernel.domain.services.account_type_engine import (
    get_posting_rule,
    list_account_types,
    resolve_account_type,
    validate_account_type_assignment,
)
from contexts.financial_kernel.domain.services.coa_engine import (
    CATEGORY_ROOTS,
    build_enriched_tree,
    validate_account_fields,
)
from contexts.financial_kernel.domain.services.account_hierarchy_engine import (
    apply_account_updates,
    build_hierarchy_tree,
    build_version_snapshot,
    compute_move_updates,
    compute_tree_stats,
    detect_duplicates,
    export_bulk_rows,
    filter_accounts_for_tree,
    generate_ai_tree_optimization,
    generate_visual_account_tree as build_visual_account_tree,
    resolve_parent_from_import_row,
    search_tree_accounts,
    validate_bulk_import_rows,
    validate_tree_integrity,
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
from contexts.financial_kernel.domain.services.double_entry_posting_engine import (
    JournalEntryType,
    SingleEntryInput,
    apply_posting_rule,
    build_adjusting_entry,
    build_audit_trail_entry,
    build_closing_entry,
    build_intercompany_entry,
    build_opening_balance_entry,
    build_rollback_plan,
    classify_journal_entry_type,
    expand_single_entry_to_double,
    list_posting_rules,
)
from contexts.financial_kernel.domain.services.double_entry_validation_engine import (
    PostingValidationContext,
)
from contexts.financial_kernel.domain.services.posting_rule_engine import (
    RuleBuilderInput,
    PostingExecutionContext,
    build_lines_from_rule,
    build_rule_from_builder,
    get_platform_rule,
    get_rule_detail,
    list_all_posting_rules,
    list_platform_posting_rules,
    preview_posting_rule,
    resolve_default_account_mappings,
    resolve_rule,
    validate_rule_builder_input,
)
from contexts.financial_kernel.domain.aggregates.posting_rules import PostingPattern
from contexts.financial_kernel.domain.aggregates.subledger import (
    Subledger,
    SubledgerEntry,
    SubledgerReconciliation,
)
from contexts.financial_kernel.domain.services.fiscal_calendar_engine import (
    build_closing_assistant,
    create_adjustment_period as build_adjustment_period,
    generate_ai_closing_checklist,
    generate_monthly_periods,
    get_close_rule,
    quarter_period_numbers,
    validate_close_transition,
)
from contexts.financial_kernel.domain.ports.fiscal_calendar_repositories import (
    IFiscalCalendarAuditRepository,
    IFiscalCalendarRepository,
    IFiscalCloseRequestRepository,
)
from contexts.financial_kernel.domain.services.coa_tree_service import (
    build_account_tree,
    validate_parent_assignment,
)
from contexts.financial_kernel.domain.ports.account_hierarchy_repositories import (
    IAccountTreeRepository,
    IAccountTreeVersionRepository,
)
from contexts.financial_kernel.domain.aggregates.financial_dimension import (
    DimensionAuditLog,
    DimensionValue,
)
from contexts.financial_kernel.domain.ports.financial_dimension_repositories import (
    IDimensionAuditRepository,
    IDimensionValueRepository,
)
from contexts.financial_kernel.domain.aggregates.financial_validation import (
    ValidationAuditLog,
    ValidationRun,
)
from contexts.financial_kernel.domain.ports.financial_validation_repositories import (
    IValidationAuditRepository,
    IValidationRunRepository,
)
from contexts.financial_kernel.domain.aggregates.reconciliation import (
    ApprovalAction,
    ReconciliationAuditLog,
    ReconciliationRun,
)
from contexts.financial_kernel.domain.ports.reconciliation_repositories import (
    IReconciliationAuditRepository,
    IReconciliationRunRepository,
)
from contexts.financial_kernel.domain.ports.subledger_repositories import (
    ISubledgerEntryRepository,
    ISubledgerReconciliationRepository,
    ISubledgerRepository,
)
from contexts.financial_kernel.domain.services.financial_validation_engine import (
    FinancialValidationContext,
    list_validation_catalog,
    reject_if_invalid,
    run_full_validation,
)
from contexts.financial_kernel.domain.services.financial_dimension_engine import (
    build_dimension_lookup,
    enrich_journal_lines,
    get_dimension_definition,
    list_dimension_catalog,
    merge_header_dimensions,
    normalize_dimension_type,
    summarize_line_dimensions,
    validate_line_dimensions,
)
from contexts.financial_kernel.domain.services.reconciliation_engine import (
    automatic_match_items,
    build_difference_analysis,
    build_exception_queue,
    build_reconciliation_report,
    generate_ai_suggestions,
    get_reconciliation_definition,
    list_reconciliation_catalog,
    sum_item_amounts,
    validate_approval_action,
)
from contexts.financial_kernel.domain.ports.posting_rule_repositories import IPostingRuleRepository
from contexts.financial_kernel.domain.services.subledger_engine import (
    SUBLEDGER_CATALOG,
    build_gl_items_from_journals,
    build_reconciliation_items,
    build_subledger_account_mappings,
    build_subledger_from_catalog,
    build_subledger_idempotency_key,
    compute_subledger_balance,
    get_subledger_definition,
    list_subledger_catalog,
    reconcile_balances,
    resolve_entry_side,
    update_subledger_stats,
    validate_no_duplicate_entry,
)
from contexts.financial_kernel.domain.services.journal_engine import (
    apply_type_posting_defaults,
    build_batch_id,
    enrich_journal_dict,
    get_journal_type_rules,
    list_journal_types,
    resolve_journal_type,
    review_journal_with_ai,
    sign_journal_entry,
    validate_batch_entry,
    validate_journal_modifiable,
    validate_rollback_allowed,
    validate_signature_required,
    validate_versioning_enabled,
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
        posting_rules: IPostingRuleRepository | None = None,
        calendars: IFiscalCalendarRepository | None = None,
        calendar_audits: IFiscalCalendarAuditRepository | None = None,
        close_requests: IFiscalCloseRequestRepository | None = None,
        account_trees: IAccountTreeRepository | None = None,
        tree_versions: IAccountTreeVersionRepository | None = None,
        subledgers: ISubledgerRepository | None = None,
        subledger_entries: ISubledgerEntryRepository | None = None,
        subledger_reconciliations: ISubledgerReconciliationRepository | None = None,
        reconciliation_runs: IReconciliationRunRepository | None = None,
        reconciliation_audits: IReconciliationAuditRepository | None = None,
        dimension_values: IDimensionValueRepository | None = None,
        dimension_audits: IDimensionAuditRepository | None = None,
        validation_runs: IValidationRunRepository | None = None,
        validation_audits: IValidationAuditRepository | None = None,
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
        self._posting_rules = posting_rules
        self._calendars = calendars
        self._calendar_audits = calendar_audits
        self._close_requests = close_requests
        self._account_trees = account_trees
        self._tree_versions = tree_versions
        self._subledgers = subledgers
        self._subledger_entries = subledger_entries
        self._subledger_reconciliations = subledger_reconciliations
        self._reconciliation_runs = reconciliation_runs
        self._reconciliation_audits = reconciliation_audits
        self._dimension_values = dimension_values
        self._dimension_audits = dimension_audits
        self._validation_runs = validation_runs
        self._validation_audits = validation_audits

    async def _provision_subledgers(self, tenant_id: str) -> None:
        if not self._subledgers:
            return
        for subledger_type in SUBLEDGER_CATALOG:
            existing = await self._subledgers.find_by_type(tenant_id, subledger_type)
            if existing:
                continue
            subledger = build_subledger_from_catalog(tenant_id, subledger_type)
            await self._subledgers.save(subledger)

    async def _ensure_default_account_tree(self, tenant_id: str, *, template_key: str | None = None) -> str | None:
        if not self._account_trees:
            return None
        existing = await self._account_trees.find_default(tenant_id)
        if existing:
            return str(existing.id)
        tree = AccountTree.create(
            tenant_id=tenant_id,
            name="Primary Chart of Accounts",
            description="Default account hierarchy",
            tree_type=TreeType.PRIMARY.value,
            template_key=template_key,
            template_type="industry" if template_key else None,
            is_default=True,
        )
        await self._account_trees.save(tree)
        return str(tree.id)

    async def _tree_accounts(self, tenant_id: str, tree_id: str) -> list[ChartOfAccount]:
        scoped = await self._accounts.list_by_tree(tenant_id, tree_id)
        if scoped:
            return scoped
        all_accounts = await self._accounts.list_by_tenant(tenant_id)
        return filter_accounts_for_tree(all_accounts, tree_id)

    async def _refresh_tree_stats(self, tree: AccountTree) -> None:
        accounts = await self._tree_accounts(tree.tenant_id, str(tree.id))
        stats = compute_tree_stats(accounts)
        tree.account_count = stats["account_count"]
        tree.max_depth = stats["max_depth"]
        await self._account_trees.save(tree)

    async def _record_tree_version(
        self,
        *,
        tenant_id: str,
        tree: AccountTree,
        change_type: str,
        actor_id: str = "system",
        change_summary: str = "",
    ) -> AccountTreeVersion | None:
        if not self._tree_versions:
            return None
        accounts = await self._tree_accounts(tenant_id, str(tree.id))
        snapshot = build_version_snapshot(accounts)
        stats = compute_tree_stats(accounts)
        version_number = tree.bump_version()
        version = AccountTreeVersion.create(
            tenant_id=tenant_id,
            tree_id=str(tree.id),
            version_number=version_number,
            snapshot=snapshot,
            change_type=change_type,
            change_summary=change_summary,
            actor_id=actor_id,
            account_count=stats["account_count"],
            max_depth=stats["max_depth"],
        )
        await self._tree_versions.save(version)
        tree.account_count = stats["account_count"]
        tree.max_depth = stats["max_depth"]
        await self._account_trees.save(tree)
        return version

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        industry_pack = (envelope.get("payload") or {}).get("industry_pack", "retail")
        if await self._accounts.list_by_tenant(tenant_id):
            return
        template_key = INDUSTRY_PACK_TO_COA.get(industry_pack, "coa.retail")
        tree_id = await self._ensure_default_account_tree(tenant_id, template_key=template_key)
        for account in build_accounts(tenant_id, template_key):
            if tree_id:
                account.tree_id = tree_id
            await self._accounts.save(account)
        if tree_id and self._account_trees:
            tree = await self._account_trees.find_by_id(tree_id)
            if tree:
                await self._refresh_tree_stats(tree)
                await self._record_tree_version(
                    tenant_id=tenant_id,
                    tree=tree,
                    change_type=TreeChangeType.TEMPLATE_APPLY.value,
                    change_summary=f"Provisioned from {template_key}",
                )
        for code, name in INDUSTRY_COST_CENTERS.get(industry_pack, []):
            await self._dimensions.save_cost_center(
                CostCenter.create(tenant_id=tenant_id, code=code, name=name)
            )
        await self._provision_subledgers(tenant_id)
        calendar_id = None
        if self._calendars:
            calendar = FiscalCalendar.create(
                tenant_id=tenant_id,
                organization_id=None,
                name="Default Fiscal Calendar",
                is_default=True,
            )
            await self._calendars.save(calendar)
            calendar_id = str(calendar.id)
        year = FiscalYear.create(
            tenant_id=tenant_id,
            organization_id=None,
            name="FY2025",
            start_date="2025-01-01",
            end_date="2025-12-31",
            calendar_id=calendar_id,
        )
        await self._years.save(year)
        if not await self._periods.find_open(tenant_id):
            await self._periods.save(
                FiscalPeriod.open_period(
                    tenant_id=tenant_id,
                    organization_id=None,
                    branch_id=None,
                    fiscal_year_id=str(year.id),
                    calendar_id=calendar_id,
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
        currency: str | None = None,
        is_control_account: bool = False,
        reconciliation_required: bool = False,
        tax_code: str | None = None,
        budget_code: str | None = None,
        effective_date: str | None = None,
    ) -> Result[dict]:
        if await self._accounts.find_by_code(tenant_id, code):
            return Result.fail("financial_kernel.errors.account_exists")
        if account_key and await self._accounts.find_by_key(tenant_id, account_key):
            return Result.fail("financial_kernel.errors.account_key_exists")
        try:
            category = _resolve_account_category(account_category, account_type)
            resolved_type = resolve_account_type(
                account_type=account_type,
                account_category=category.value,
            )
        except (ValueError, KeyError):
            return Result.fail("financial_kernel.errors.invalid_account_type")

        ok_type, type_reason = validate_account_type_assignment(
            account_type=resolved_type,
            account_category=category.value,
            is_posting=is_posting,
        )
        if not ok_type:
            return Result.fail(f"financial_kernel.errors.account.{type_reason}")

        parent = None
        level = 0
        tree_path = account_key or code
        if parent_account_id:
            parent = await self._accounts.find_by_id(parent_account_id)
            if not parent or parent.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.parent_not_found")
            level = parent.level + 1
            tree_path = f"{parent.tree_path}/{account_key or code}"

        ok, reason = validate_account_fields(
            code=code,
            name=name,
            account_category=category.value,
            is_posting=is_posting,
            parent=parent,
        )
        if not ok:
            return Result.fail(f"financial_kernel.errors.account.{reason}")

        account = ChartOfAccount.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            account_category=category,
            account_type=resolved_type,
            account_key=account_key,
            parent_account_id=parent_account_id,
            level=level,
            tree_path=tree_path,
            account_group=account_group,
            is_posting=is_posting,
            template_source=TemplateSource.TENANT,
            currency=currency,
            is_control_account=is_control_account,
            reconciliation_required=reconciliation_required,
            tax_code=tax_code,
            budget_code=budget_code,
            effective_date=effective_date,
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
        return Result.ok(build_enriched_tree(accounts))

    async def list_account_categories(self) -> Result[list[dict]]:
        return Result.ok(CATEGORY_ROOTS)

    async def list_enterprise_account_types(self) -> Result[list[dict]]:
        return Result.ok(list_account_types())

    async def get_account_type_posting_rules(self, account_type: str) -> Result[dict]:
        try:
            rule = get_posting_rule(account_type)
        except KeyError:
            return Result.fail("financial_kernel.errors.unknown_account_type")
        return Result.ok(
            {
                "account_type": rule.account_type,
                "category": rule.category,
                "normal_balance": rule.normal_balance,
                "gl_posting_allowed": rule.gl_posting_allowed,
                "is_contra": rule.is_contra,
                "is_control_account": rule.is_control_account,
                "reconciliation_required": rule.reconciliation_required,
                "requires_subledger": rule.requires_subledger,
                "budget_tracked": rule.budget_tracked,
                "tax_related": rule.tax_related,
                "description": rule.description,
            }
        )

    async def list_enterprise_journal_types(self) -> Result[list[dict]]:
        return Result.ok(list_journal_types())

    async def get_journal_type_rules(self, journal_type: str) -> Result[dict]:
        try:
            rules = get_journal_type_rules(journal_type)
        except KeyError:
            return Result.fail("financial_kernel.errors.unknown_journal_type")
        return Result.ok(
            {
                "journal_type": rules.journal_type,
                "label": rules.label,
                "journal_entry_type": rules.journal_entry_type,
                "approval_workflow_required": rules.approval_workflow_required,
                "digital_signature_required": rules.digital_signature_required,
                "ai_review_enabled": rules.ai_review_enabled,
                "automatic_posting_allowed": rules.automatic_posting_allowed,
                "batch_posting_allowed": rules.batch_posting_allowed,
                "rollback_allowed": rules.rollback_allowed,
                "lock_on_post": rules.lock_on_post,
                "versioning_enabled": rules.versioning_enabled,
                "default_posting_mode": rules.default_posting_mode,
                "description": rules.description,
            }
        )

    async def _tenant_posting_rules(self, tenant_id: str) -> list:
        if not self._posting_rules:
            return []
        return await self._posting_rules.list_by_tenant(tenant_id)

    async def list_enterprise_posting_rules(self, tenant_id: str) -> Result[list[dict]]:
        tenant_rules = await self._tenant_posting_rules(tenant_id)
        legacy = [{"rule_id": r["id"], "label": r["description"], "module": "legacy", "is_platform": True, **r} for r in list_posting_rules()]
        platform = list_platform_posting_rules()
        custom = [r.to_dict() for r in tenant_rules if r.is_active]
        seen = {r["rule_id"] for r in platform}
        merged = platform + [r for r in legacy if r["rule_id"] not in seen] + custom
        return Result.ok(merged)

    async def get_enterprise_posting_rule(self, tenant_id: str, rule_id: str) -> Result[dict]:
        try:
            rule = resolve_rule(rule_id, tenant_rules=await self._tenant_posting_rules(tenant_id))
        except KeyError:
            return Result.fail("financial_kernel.errors.unknown_posting_rule")
        return Result.ok(get_rule_detail(rule))

    async def preview_posting_rule_execution(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        amount: float | None = None,
        account_mappings: dict[str, str] | None = None,
        lines: list[dict] | None = None,
        description: str = "",
        dimensions: dict[str, str] | None = None,
        tax_amount: float | None = None,
        use_default_accounts: bool = True,
    ) -> Result[dict]:
        try:
            rule = resolve_rule(rule_id, tenant_rules=await self._tenant_posting_rules(tenant_id))
        except KeyError:
            return Result.fail("financial_kernel.errors.unknown_posting_rule")
        mappings = dict(account_mappings or {})
        if use_default_accounts:
            mappings = await self._resolve_account_mappings(tenant_id, rule, mappings)
        context = PostingExecutionContext(
            amount=amount or 0,
            account_mappings=mappings,
            description=description,
            dimensions=dimensions,
            tax_amount=tax_amount,
            lines=lines,
        )
        return Result.ok(preview_posting_rule(rule, context))

    async def execute_posting(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        source_context: str,
        source_document_id: str,
        currency: str,
        correlation_id: str,
        amount: float | None = None,
        account_mappings: dict[str, str] | None = None,
        lines: list[dict] | None = None,
        description: str = "",
        dimensions: dict[str, str] | None = None,
        tax_amount: float | None = None,
        idempotency_key: str | None = None,
        organization_id: str | None = None,
        branch_id: str | None = None,
        base_currency: str = "USD",
        exchange_rate: float = 1.0,
        use_default_accounts: bool = True,
        require_approval: bool | None = None,
    ) -> Result[dict]:
        """Canonical posting entry — business modules must use this, not _post directly."""
        try:
            rule = resolve_rule(rule_id, tenant_rules=await self._tenant_posting_rules(tenant_id))
        except KeyError:
            return Result.fail("financial_kernel.errors.unknown_posting_rule")

        mappings = dict(account_mappings or {})
        if use_default_accounts and rule.pattern != PostingPattern.EXPLICIT_LINES.value:
            mappings = await self._resolve_account_mappings(tenant_id, rule, mappings)

        context = PostingExecutionContext(
            amount=amount or 0,
            account_mappings=mappings,
            description=description,
            dimensions=dimensions,
            tax_amount=tax_amount,
            lines=lines,
        )
        try:
            built_lines = build_lines_from_rule(rule, context)
        except ValueError as exc:
            return Result.fail(f"financial_kernel.errors.posting.{exc}")

        approval = require_approval if require_approval is not None else rule.approval_required
        return await self.post_typed_journal(
            tenant_id=tenant_id,
            journal_type=rule.journal_type,
            source_context=source_context,
            source_document_id=source_document_id,
            lines=built_lines,
            currency=currency,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key or f"posting:{rule_id}:{source_document_id}",
            organization_id=organization_id,
            branch_id=branch_id,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            require_approval=approval,
        )

    async def build_posting_rule(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        label: str,
        module: str,
        journal_type: str = "general",
        pattern: str = PostingPattern.DEBIT_CREDIT.value,
        account_slots: dict | None = None,
        line_templates: list[dict] | None = None,
        approval_required: bool = False,
        tax_amount_field: str | None = None,
        tax_account_slot: str | None = None,
        dimensions: list[str] | None = None,
        description: str = "",
    ) -> Result[dict]:
        if not self._posting_rules:
            return Result.fail("financial_kernel.errors.posting_rules_not_configured")
        existing = await self._posting_rules.find_by_rule_id(tenant_id, rule_id)
        if existing:
            return Result.fail("financial_kernel.errors.posting_rule_exists")
        builder = RuleBuilderInput(
            rule_id=rule_id,
            label=label,
            module=module,
            journal_type=journal_type,
            pattern=pattern,
            account_slots=account_slots,
            line_templates=line_templates,
            approval_required=approval_required,
            tax_amount_field=tax_amount_field,
            tax_account_slot=tax_account_slot,
            dimensions=dimensions,
            description=description,
        )
        try:
            rule = build_rule_from_builder(tenant_id, builder)
        except ValueError as exc:
            return Result.fail(f"financial_kernel.errors.posting.{exc}")
        await self._posting_rules.save(rule)
        return Result.ok(rule.to_dict())

    async def update_posting_rule(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        label: str | None = None,
        account_slots: dict | None = None,
        line_templates: list[dict] | None = None,
        approval_required: bool | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Result[dict]:
        if not self._posting_rules:
            return Result.fail("financial_kernel.errors.posting_rules_not_configured")
        rule = await self._posting_rules.find_by_rule_id(tenant_id, rule_id)
        if not rule:
            return Result.fail("financial_kernel.errors.unknown_posting_rule")
        if account_slots is not None or line_templates is not None:
            builder = RuleBuilderInput(
                rule_id=rule_id,
                label=label or rule.label,
                module=rule.module,
                journal_type=rule.journal_type,
                pattern=rule.pattern,
                account_slots=account_slots or rule.account_slots,
                line_templates=line_templates or rule.line_templates,
                approval_required=approval_required if approval_required is not None else rule.approval_required,
                description=description or rule.description,
            )
            ok, reason = validate_rule_builder_input(builder)
            if not ok:
                return Result.fail(f"financial_kernel.errors.posting.{reason}")
        rule.update(
            label=label,
            account_slots=account_slots,
            line_templates=line_templates,
            approval_required=approval_required,
            description=description,
            is_active=is_active,
        )
        await self._posting_rules.save(rule)
        return Result.ok(rule.to_dict())

    async def _resolve_account_mappings(
        self,
        tenant_id: str,
        rule: PostingRuleDefinition,
        mappings: dict[str, str],
    ) -> dict[str, str]:
        key_resolver: dict[str, str] = {}
        for account in await self._accounts.list_by_tenant(tenant_id):
            if account.account_key:
                key_resolver[account.account_key] = account.code
        resolved = dict(mappings)
        for slot, code in resolve_default_account_mappings(rule, account_key_resolver=key_resolver).items():
            resolved.setdefault(slot, code)
        return resolved

    async def post_typed_journal(
        self,
        *,
        tenant_id: str,
        journal_type: str,
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
        require_approval: bool | None = None,
        batch_id: str | None = None,
    ) -> Result[dict]:
        resolved_type = resolve_journal_type(journal_type)
        defaults = apply_type_posting_defaults(resolved_type, require_approval=require_approval)
        posting_mode = (
            PostingMode.MANUAL
            if defaults["require_approval"]
            else defaults["posting_mode"]
        )
        entry_type = (
            None
            if defaults["journal_entry_type"] == JournalEntryType.STANDARD.value
            else defaults["journal_entry_type"]
        )
        result = await self._post(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            posting_mode=posting_mode,
            organization_id=organization_id,
            branch_id=branch_id,
            require_approval=defaults["require_approval"],
            journal_entry_type=entry_type,
            journal_type=resolved_type,
            batch_id=batch_id,
            lock_on_post=defaults["lock_on_post"],
        )
        if not result.succeeded:
            return result
        rules = get_journal_type_rules(resolved_type)
        return Result.ok(enrich_journal_dict(result.unwrap(), rules))

    async def batch_post_journals(
        self,
        *,
        tenant_id: str,
        entries: list[dict],
        correlation_id: str,
        batch_id: str | None = None,
    ) -> Result[dict]:
        resolved_batch_id = batch_id or build_batch_id()
        results: list[dict] = []
        errors: list[dict] = []
        for index, entry in enumerate(entries):
            journal_type = resolve_journal_type(entry.get("journal_type"))
            ok, reason = validate_batch_entry(journal_type)
            if not ok:
                errors.append({"index": index, "error": reason})
                continue
            result = await self.post_typed_journal(
                tenant_id=tenant_id,
                journal_type=journal_type,
                source_context=entry["source_context"],
                source_document_id=entry["source_document_id"],
                lines=entry["lines"],
                currency=entry.get("currency", "USD"),
                correlation_id=correlation_id,
                idempotency_key=entry.get("idempotency_key"),
                organization_id=entry.get("organization_id"),
                branch_id=entry.get("branch_id"),
                base_currency=entry.get("base_currency", "USD"),
                exchange_rate=entry.get("exchange_rate", 1.0),
                require_approval=entry.get("require_approval"),
                batch_id=resolved_batch_id,
            )
            if result.succeeded:
                results.append(result.unwrap())
            else:
                errors.append({"index": index, "error": result.error})
        return Result.ok(
            {
                "batch_id": resolved_batch_id,
                "posted_count": len(results),
                "error_count": len(errors),
                "journals": results,
                "errors": errors,
            }
        )

    async def lock_journal(self, journal_id: str) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        journal.lock()
        await self._journals.save(journal)
        return Result.ok(journal.to_dict())

    async def sign_journal(
        self, journal_id: str, signer_id: str, correlation_id: str
    ) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        ok, reason = validate_journal_modifiable(
            status=journal.status, is_locked=journal.is_locked
        )
        if not ok and journal.status != JournalStatus.PENDING_APPROVAL.value:
            return Result.fail(f"financial_kernel.errors.journal.{reason}")
        signature = sign_journal_entry(
            journal_id=journal_id,
            journal_type=journal.journal_type,
            signer_id=signer_id,
        )
        journal.attach_signature(signature)
        await self._journals.save(journal)
        return Result.ok(journal.to_dict())

    async def ai_review_journal(self, journal_id: str) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        rules = get_journal_type_rules(journal.journal_type)
        if not rules.ai_review_enabled:
            return Result.fail("financial_kernel.errors.ai_review_not_enabled")
        review = review_journal_with_ai(journal=journal.to_dict())
        journal.attach_ai_review(review)
        await self._journals.save(journal)
        return Result.ok(journal.to_dict())

    async def create_journal_version(
        self,
        *,
        journal_id: str,
        lines: list[dict],
        correlation_id: str,
    ) -> Result[dict]:
        original = await self._journals.find_by_id(journal_id)
        if not original:
            return Result.fail("financial_kernel.errors.journal_not_found")
        ok, reason = validate_journal_modifiable(
            status=original.status, is_locked=original.is_locked
        )
        if not ok:
            return Result.fail(f"financial_kernel.errors.journal.{reason}")
        ok, reason = validate_versioning_enabled(original.journal_type)
        if not ok:
            return Result.fail(f"financial_kernel.errors.journal.{reason}")
        ok, reason = validate_journal_lines(lines)
        if not ok:
            return Result.fail(f"financial_kernel.errors.journal.{reason}")
        version = Journal.create_draft(
            tenant_id=original.tenant_id,
            organization_id=original.organization_id,
            branch_id=original.branch_id,
            fiscal_year_id=original.fiscal_year_id,
            period_id=original.period_id,
            source_context=original.source_context,
            source_document_id=f"{original.source_document_id}-v{original.version + 1}",
            idempotency_key=f"version:{journal_id}:{original.version + 1}",
            currency=original.currency,
            base_currency=original.base_currency,
            exchange_rate=original.exchange_rate,
            lines=lines,
            posting_mode=PostingMode.MANUAL,
            correlation_id=correlation_id,
            journal_entry_type=original.journal_entry_type,
            journal_type=original.journal_type,
            version=original.version + 1,
            parent_version_id=str(original.id),
        )
        await self._journals.save(version)
        return Result.ok(version.to_dict())

    async def list_journal_versions(self, journal_id: str) -> Result[list[dict]]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        root_id = journal.parent_version_id or str(journal.id)
        all_journals = await self._journals.list_by_tenant(journal.tenant_id)
        versions = [
            j.to_dict()
            for j in all_journals
            if str(j.id) == root_id
            or j.parent_version_id == root_id
            or (j.parent_version_id and j.parent_version_id == str(journal.id))
            or str(j.id) == journal_id
        ]
        versions.sort(key=lambda v: v["version"])
        return Result.ok(versions)

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
                "tree": build_enriched_tree(accounts),
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

    async def _record_calendar_audit(
        self,
        *,
        tenant_id: str,
        action: str,
        actor_id: str,
        calendar_id: str | None = None,
        period_id: str | None = None,
        fiscal_year_id: str | None = None,
        before_state: dict | None = None,
        after_state: dict | None = None,
        correlation_id: str = "",
    ) -> None:
        if not self._calendar_audits:
            return
        entry = FiscalCalendarAuditLog.record(
            tenant_id=tenant_id,
            action=action,
            actor_id=actor_id,
            calendar_id=calendar_id,
            period_id=period_id,
            fiscal_year_id=fiscal_year_id,
            before_state=before_state,
            after_state=after_state,
            correlation_id=correlation_id,
        )
        await self._calendar_audits.save(entry)

    async def create_fiscal_calendar(
        self,
        *,
        tenant_id: str,
        name: str,
        organization_id: str | None = None,
        description: str = "",
        fiscal_year_start_month: int = 1,
        is_default: bool = False,
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._calendars:
            return Result.fail("financial_kernel.errors.fiscal_calendar_not_configured")
        if is_default:
            existing = await self._calendars.find_default(tenant_id, organization_id)
            if existing:
                existing.is_default = False
                await self._calendars.save(existing)
        calendar = FiscalCalendar.create(
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name,
            description=description,
            fiscal_year_start_month=fiscal_year_start_month,
            is_default=is_default,
        )
        await self._calendars.save(calendar)
        await self._record_calendar_audit(
            tenant_id=tenant_id,
            action="fiscal_calendar.created",
            actor_id=actor_id,
            calendar_id=str(calendar.id),
            after_state=calendar.to_dict(),
        )
        return Result.ok(calendar.to_dict())

    async def list_fiscal_calendars(self, tenant_id: str) -> Result[list[dict]]:
        if not self._calendars:
            return Result.fail("financial_kernel.errors.fiscal_calendar_not_configured")
        calendars = await self._calendars.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in calendars])

    async def get_fiscal_calendar(self, calendar_id: str) -> Result[dict]:
        if not self._calendars:
            return Result.fail("financial_kernel.errors.fiscal_calendar_not_configured")
        calendar = await self._calendars.find_by_id(calendar_id)
        if not calendar:
            return Result.fail("financial_kernel.errors.calendar_not_found")
        return Result.ok(calendar.to_dict())

    async def create_calendar_fiscal_year(
        self,
        *,
        tenant_id: str,
        calendar_id: str,
        name: str,
        start_date: str,
        end_date: str,
        organization_id: str | None = None,
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._calendars:
            return Result.fail("financial_kernel.errors.fiscal_calendar_not_configured")
        calendar = await self._calendars.find_by_id(calendar_id)
        if not calendar or calendar.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.calendar_not_found")
        year = FiscalYear.create(
            tenant_id=tenant_id,
            organization_id=organization_id or calendar.organization_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            calendar_id=calendar_id,
        )
        await self._years.save(year)
        await self._record_calendar_audit(
            tenant_id=tenant_id,
            action="fiscal_year.created",
            actor_id=actor_id,
            calendar_id=calendar_id,
            fiscal_year_id=str(year.id),
            after_state=year.to_dict(),
        )
        return Result.ok(year.to_dict())

    async def generate_calendar_periods(
        self,
        *,
        tenant_id: str,
        fiscal_year_id: str,
        actor_id: str = "system",
    ) -> Result[list[dict]]:
        year = await self._years.find_by_id(fiscal_year_id)
        if not year or year.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.fiscal_year_not_found")
        existing = await self._periods.list_by_fiscal_year(tenant_id, fiscal_year_id)
        if existing:
            return Result.ok([p.to_dict() for p in existing])
        periods = generate_monthly_periods(
            tenant_id=tenant_id,
            organization_id=year.organization_id,
            branch_id=None,
            fiscal_year=year,
            calendar_id=year.calendar_id,
        )
        for period in periods:
            await self._periods.save(period)
        await self._record_calendar_audit(
            tenant_id=tenant_id,
            action="fiscal_periods.generated",
            actor_id=actor_id,
            calendar_id=year.calendar_id,
            fiscal_year_id=fiscal_year_id,
            after_state={"period_count": len(periods)},
        )
        return Result.ok([p.to_dict() for p in periods])

    async def create_adjustment_period(
        self,
        *,
        tenant_id: str,
        fiscal_year_id: str,
        actor_id: str = "system",
    ) -> Result[dict]:
        year = await self._years.find_by_id(fiscal_year_id)
        if not year or year.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.fiscal_year_not_found")
        period = build_adjustment_period(
            tenant_id=tenant_id,
            organization_id=year.organization_id,
            branch_id=None,
            fiscal_year=year,
            calendar_id=year.calendar_id,
        )
        await self._periods.save(period)
        await self._record_calendar_audit(
            tenant_id=tenant_id,
            action="adjustment_period.created",
            actor_id=actor_id,
            fiscal_year_id=fiscal_year_id,
            period_id=str(period.id),
            after_state=period.to_dict(),
        )
        return Result.ok(period.to_dict())

    async def request_period_close_action(
        self,
        *,
        tenant_id: str,
        period_id: str,
        action_type: str,
        requester_id: str,
        reason: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        if not self._close_requests:
            return Result.fail("financial_kernel.errors.fiscal_calendar_not_configured")
        period = await self._periods.find_by_id(period_id)
        if not period or period.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.period_not_found")
        ok, err = validate_close_transition(current_status=period.status, action_type=action_type)
        if not ok:
            return Result.fail(f"financial_kernel.errors.{err}")
        rule = get_close_rule(action_type)
        request = FiscalCloseRequest.request(
            tenant_id=tenant_id,
            action_type=action_type,
            close_level=rule.get("close_level", CloseLevel.MONTHLY.value),
            requester_id=requester_id,
            period_id=period_id,
            fiscal_year_id=period.fiscal_year_id,
            calendar_id=period.calendar_id,
            reason=reason,
            correlation_id=correlation_id,
        )
        await self._close_requests.save(request)
        await self._record_calendar_audit(
            tenant_id=tenant_id,
            action=f"close.{action_type}.requested",
            actor_id=requester_id,
            period_id=period_id,
            correlation_id=correlation_id,
            after_state=request.to_dict(),
        )
        return Result.ok(request.to_dict())

    async def approve_period_close_action(
        self,
        *,
        tenant_id: str,
        request_id: str,
        approver_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        if not self._close_requests:
            return Result.fail("financial_kernel.errors.fiscal_calendar_not_configured")
        request = await self._close_requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.request_not_found")
        before = request.to_dict()
        try:
            request.approve(approver_id)
        except ValueError as exc:
            return Result.fail(f"financial_kernel.errors.{exc.args[0]}")
        if request.status == CloseRequestStatus.APPROVED.value:
            await self._apply_close_request(request)
        await self._close_requests.save(request)
        await self._record_calendar_audit(
            tenant_id=tenant_id,
            action=f"close.{request.action_type}.approved",
            actor_id=approver_id,
            period_id=request.period_id,
            correlation_id=correlation_id,
            before_state=before,
            after_state=request.to_dict(),
        )
        return Result.ok(request.to_dict())

    async def _apply_close_request(self, request: FiscalCloseRequest) -> None:
        rule = get_close_rule(request.action_type)
        if request.action_type == CloseActionType.YEAR_CLOSE.value and request.fiscal_year_id:
            year = await self._years.find_by_id(request.fiscal_year_id)
            if year:
                year.close_year()
                await self._years.save(year)
            for period in await self._periods.list_by_fiscal_year(request.tenant_id, request.fiscal_year_id):
                if period.status == "open":
                    period.hard_close(close_level=CloseLevel.YEAR.value)
                    await self._periods.save(period)
            return
        if request.action_type == CloseActionType.QUARTER_CLOSE.value and request.period_id:
            period = await self._periods.find_by_id(request.period_id)
            if not period:
                return
            nums = quarter_period_numbers(period.period_number)
            for p in await self._periods.list_by_fiscal_year(request.tenant_id, period.fiscal_year_id):
                if p.period_number in nums and p.status == "open":
                    p.soft_close(close_level=CloseLevel.QUARTER.value)
                    await self._periods.save(p)
            return
        if not request.period_id:
            return
        period = await self._periods.find_by_id(request.period_id)
        if not period:
            return
        before = period.to_dict()
        if request.action_type == CloseActionType.REOPEN.value:
            period.reopen()
        elif request.action_type == CloseActionType.HARD_CLOSE.value:
            period.hard_close(close_level=rule.get("close_level", CloseLevel.YEAR.value))
        elif request.action_type in (
            CloseActionType.SOFT_CLOSE.value,
            CloseActionType.MONTHLY_CLOSE.value,
        ):
            period.soft_close(close_level=rule.get("close_level", CloseLevel.MONTHLY.value))
        await self._periods.save(period)

    async def lock_fiscal_period(self, period_id: str, actor_id: str = "system") -> Result[dict]:
        period = await self._periods.find_by_id(period_id)
        if not period:
            return Result.fail("financial_kernel.errors.period_not_found")
        period.apply_financial_lock()
        await self._periods.save(period)
        await self._record_calendar_audit(
            tenant_id=period.tenant_id,
            action="period.financial_lock",
            actor_id=actor_id,
            period_id=period_id,
            after_state=period.to_dict(),
        )
        return Result.ok(period.to_dict())

    async def unlock_fiscal_period(self, period_id: str, actor_id: str = "system") -> Result[dict]:
        period = await self._periods.find_by_id(period_id)
        if not period:
            return Result.fail("financial_kernel.errors.period_not_found")
        period.release_financial_lock()
        await self._periods.save(period)
        await self._record_calendar_audit(
            tenant_id=period.tenant_id,
            action="period.financial_unlock",
            actor_id=actor_id,
            period_id=period_id,
            after_state=period.to_dict(),
        )
        return Result.ok(period.to_dict())

    async def list_fiscal_calendar_audit_log(
        self, tenant_id: str, *, limit: int = 100
    ) -> Result[list[dict]]:
        if not self._calendar_audits:
            return Result.ok([])
        entries = await self._calendar_audits.list_by_tenant(tenant_id, limit=limit)
        return Result.ok([e.to_dict() for e in entries])

    async def get_closing_assistant(self, tenant_id: str, period_id: str) -> Result[dict]:
        period = await self._periods.find_by_id(period_id)
        if not period or period.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.period_not_found")
        journals = await self._journals.list_by_tenant(tenant_id)
        period_journals = [j for j in journals if j.period_id == period_id]
        unposted = [j for j in period_journals if j.status in ("draft", "pending_approval")]
        trial = (await self.get_trial_balance(tenant_id)).unwrap()
        return Result.ok(
            build_closing_assistant(
                period=period.to_dict(),
                trial_balance=trial,
                journal_count=len(period_journals),
                unposted_count=len(unposted),
            )
        )

    async def get_ai_closing_checklist(self, tenant_id: str, period_id: str) -> Result[dict]:
        period = await self._periods.find_by_id(period_id)
        if not period or period.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.period_not_found")
        journals = await self._journals.list_by_tenant(tenant_id)
        period_journals = [j.to_dict() for j in journals if j.period_id == period_id]
        unposted = [j for j in period_journals if j.get("status") in ("draft", "pending_approval")]
        trial = (await self.get_trial_balance(tenant_id)).unwrap()
        return Result.ok(
            generate_ai_closing_checklist(
                period=period.to_dict(),
                trial_balance=trial,
                journals=period_journals,
                unposted_count=len(unposted),
            )
        )

    async def create_account_tree(
        self,
        *,
        tenant_id: str,
        name: str,
        description: str = "",
        tree_type: str = TreeType.PRIMARY.value,
        template_key: str | None = None,
        template_type: str | None = None,
        country_code: str | None = None,
        is_default: bool = False,
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        if is_default:
            existing = await self._account_trees.find_default(tenant_id)
            if existing:
                existing.is_default = False
                await self._account_trees.save(existing)
        tree = AccountTree.create(
            tenant_id=tenant_id,
            name=name,
            description=description,
            tree_type=tree_type,
            template_key=template_key,
            template_type=template_type,
            country_code=country_code,
            is_default=is_default,
        )
        await self._account_trees.save(tree)
        await self._record_tree_version(
            tenant_id=tenant_id,
            tree=tree,
            change_type=TreeChangeType.CREATE.value,
            actor_id=actor_id,
            change_summary=f"Created tree {name}",
        )
        return Result.ok(tree.to_dict())

    async def list_account_trees(self, tenant_id: str) -> Result[list[dict]]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        trees = await self._account_trees.list_by_tenant(tenant_id)
        return Result.ok([t.to_dict() for t in trees])

    async def get_account_tree_meta(self, tenant_id: str, tree_id: str) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        await self._refresh_tree_stats(tree)
        integrity = validate_tree_integrity(await self._tree_accounts(tenant_id, tree_id))
        return Result.ok({**tree.to_dict(), "integrity": integrity})

    async def get_hierarchy_structure(self, tenant_id: str, tree_id: str) -> Result[list[dict]]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        accounts = await self._tree_accounts(tenant_id, tree_id)
        return Result.ok(build_hierarchy_tree(accounts))

    async def move_account_in_tree(
        self,
        *,
        tenant_id: str,
        tree_id: str,
        account_id: str,
        new_parent_id: str | None,
        position: int | None = None,
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.account_not_found")
        new_parent = None
        if new_parent_id:
            new_parent = await self._accounts.find_by_id(new_parent_id)
            if not new_parent or new_parent.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.parent_not_found")
        all_accounts = await self._tree_accounts(tenant_id, tree_id)
        ok, reason, updates = compute_move_updates(
            account=account,
            new_parent=new_parent,
            all_accounts=all_accounts,
            position=position,
        )
        if not ok:
            return Result.fail(f"financial_kernel.errors.parent.{reason}")
        by_id = {str(a.id): a for a in all_accounts}
        for update in updates:
            target = by_id.get(update["account_id"]) or await self._accounts.find_by_id(update["account_id"])
            if target:
                apply_account_updates(target, update)
                if not target.tree_id:
                    target.tree_id = tree_id
                await self._accounts.save(target)
        version = await self._record_tree_version(
            tenant_id=tenant_id,
            tree=tree,
            change_type=TreeChangeType.MOVE.value,
            actor_id=actor_id,
            change_summary=f"Moved account {account.code}",
        )
        moved = await self._accounts.find_by_id(account_id)
        return Result.ok(
            {
                "account": moved.to_dict() if moved else {},
                "updates_applied": len(updates),
                "version": version.to_dict() if version else None,
            }
        )

    async def create_tree_version_snapshot(
        self,
        *,
        tenant_id: str,
        tree_id: str,
        actor_id: str = "system",
        change_summary: str = "Manual snapshot",
    ) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        version = await self._record_tree_version(
            tenant_id=tenant_id,
            tree=tree,
            change_type=TreeChangeType.MANUAL_SNAPSHOT.value,
            actor_id=actor_id,
            change_summary=change_summary,
        )
        if not version:
            return Result.fail("financial_kernel.errors.version_not_recorded")
        return Result.ok(version.to_dict())

    async def list_tree_versions(self, tenant_id: str, tree_id: str) -> Result[list[dict]]:
        if not self._tree_versions:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id) if self._account_trees else None
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        versions = await self._tree_versions.list_by_tree(tree_id)
        return Result.ok([v.to_dict() for v in versions])

    async def get_tree_version(self, tenant_id: str, version_id: str) -> Result[dict]:
        if not self._tree_versions:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        version = await self._tree_versions.find_by_id(version_id)
        if not version or version.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.version_not_found")
        return Result.ok(version.to_dict())

    async def search_hierarchy_accounts(
        self,
        tenant_id: str,
        tree_id: str,
        *,
        query: str = "",
        account_category: str | None = None,
        account_type: str | None = None,
        is_posting: bool | None = None,
        level: int | None = None,
        parent_account_id: str | None = None,
    ) -> Result[list[dict]]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        accounts = await self._tree_accounts(tenant_id, tree_id)
        return Result.ok(
            search_tree_accounts(
                accounts,
                query=query,
                account_category=account_category,
                account_type=account_type,
                is_posting=is_posting,
                level=level,
                parent_account_id=parent_account_id,
            )
        )

    async def validate_account_hierarchy(self, tenant_id: str, tree_id: str) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        accounts = await self._tree_accounts(tenant_id, tree_id)
        integrity = validate_tree_integrity(accounts)
        duplicates = detect_duplicates(accounts)
        return Result.ok(
            {
                "tree_id": tree_id,
                "integrity": integrity,
                "duplicates": duplicates,
                "valid": integrity["valid"] and not duplicates,
            }
        )

    async def bulk_import_hierarchy_accounts(
        self,
        *,
        tenant_id: str,
        tree_id: str,
        rows: list[dict],
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        existing = await self._tree_accounts(tenant_id, tree_id)
        validation = validate_bulk_import_rows(rows, existing)
        if not validation["valid"]:
            return Result.fail("financial_kernel.errors.import_validation_failed")
        code_to_id = {a.code: str(a.id) for a in existing}
        batch_code_to_id: dict[str, str] = {}
        created: list[dict] = []
        sorted_rows = sorted(rows, key=lambda r: r.get("level", r.get("parent_code") is None and 0 or 99))
        for row in sorted_rows:
            code = str(row["code"]).strip()
            name = str(row["name"]).strip()
            category = row.get("account_category", "asset")
            account_type = row.get("account_type")
            try:
                resolved_category = _resolve_account_category(category, account_type)
                resolved_type = resolve_account_type(
                    account_type=account_type,
                    account_category=resolved_category.value,
                )
            except (ValueError, KeyError):
                return Result.fail(f"financial_kernel.errors.invalid_account_type:{code}")
            parent_id = resolve_parent_from_import_row(
                row, code_to_id=code_to_id, batch_code_to_id=batch_code_to_id
            )
            parent = await self._accounts.find_by_id(parent_id) if parent_id else None
            level = parent.level + 1 if parent else 0
            segment = row.get("account_key") or code
            tree_path = segment if not parent else f"{parent.tree_path}/{segment}"
            account = ChartOfAccount.create(
                tenant_id=tenant_id,
                code=code,
                name=name,
                account_category=resolved_category,
                account_type=resolved_type,
                account_key=row.get("account_key"),
                parent_account_id=parent_id,
                tree_id=tree_id,
                level=level,
                tree_path=tree_path,
                is_posting=row.get("is_posting", True),
                display_order=row.get("display_order", 0),
                template_source=TemplateSource.TENANT,
            )
            if parent:
                ok, reason = validate_parent_assignment(account, parent, existing + [account])
                if not ok:
                    return Result.fail(f"financial_kernel.errors.parent.{reason}")
            await self._accounts.save(account)
            batch_code_to_id[code] = str(account.id)
            code_to_id[code] = str(account.id)
            existing.append(account)
            created.append(account.to_dict())
        version = await self._record_tree_version(
            tenant_id=tenant_id,
            tree=tree,
            change_type=TreeChangeType.IMPORT.value,
            actor_id=actor_id,
            change_summary=f"Bulk import {len(created)} accounts",
        )
        return Result.ok(
            {
                "imported_count": len(created),
                "accounts": created,
                "version": version.to_dict() if version else None,
            }
        )

    async def bulk_export_hierarchy_accounts(self, tenant_id: str, tree_id: str) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        accounts = await self._tree_accounts(tenant_id, tree_id)
        rows = export_bulk_rows(accounts)
        return Result.ok(
            {
                "tree_id": tree_id,
                "tree_name": tree.name,
                "row_count": len(rows),
                "rows": rows,
            }
        )

    async def apply_template_to_tree(
        self,
        *,
        tenant_id: str,
        tree_id: str,
        template_key: str,
        template_type: str = "industry",
        code_overrides: dict[str, str] | None = None,
        code_prefix: str = "",
        country_code: str | None = None,
        merge: bool = False,
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        tree_accounts = await self._tree_accounts(tenant_id, tree_id)
        if not merge and tree_accounts:
            return Result.fail("financial_kernel.errors.tree_already_has_accounts")
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
            account.tree_id = tree_id
            await self._accounts.save(account)
        tree.template_key = template_key
        tree.template_type = template_type
        if country_code:
            tree.country_code = country_code
        await self._account_trees.save(tree)
        version = await self._record_tree_version(
            tenant_id=tenant_id,
            tree=tree,
            change_type=TreeChangeType.TEMPLATE_APPLY.value,
            actor_id=actor_id,
            change_summary=f"Applied template {template_key}",
        )
        refreshed_accounts = await self._tree_accounts(tenant_id, tree_id)
        return Result.ok(
            {
                "template_key": template_key,
                "template_type": template_type,
                "account_count": len(accounts),
                "tree": build_hierarchy_tree(refreshed_accounts),
                "version": version.to_dict() if version else None,
            }
        )

    async def ai_optimize_account_tree(self, tenant_id: str, tree_id: str) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        accounts = await self._tree_accounts(tenant_id, tree_id)
        return Result.ok(generate_ai_tree_optimization(accounts, tree_name=tree.name))

    async def generate_visual_account_tree(self, tenant_id: str, tree_id: str) -> Result[dict]:
        if not self._account_trees:
            return Result.fail("financial_kernel.errors.account_hierarchy_not_configured")
        tree = await self._account_trees.find_by_id(tree_id)
        if not tree or tree.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.tree_not_found")
        accounts = await self._tree_accounts(tenant_id, tree_id)
        roots = build_hierarchy_tree(accounts)
        visual = build_visual_account_tree(roots)
        return Result.ok({**visual, "tree_id": tree_id, "tree_name": tree.name})

    async def list_subledger_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_subledger_catalog())

    async def list_subledgers(self, tenant_id: str) -> Result[list[dict]]:
        if not self._subledgers:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledgers = await self._subledgers.list_by_tenant(tenant_id)
        if not subledgers:
            await self._provision_subledgers(tenant_id)
            subledgers = await self._subledgers.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in subledgers])

    async def get_subledger(self, tenant_id: str, subledger_id: str) -> Result[dict]:
        if not self._subledgers:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledger = await self._subledgers.find_by_id(subledger_id)
        if not subledger or subledger.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.subledger_not_found")
        if self._subledger_entries:
            entries = await self._subledger_entries.list_by_subledger(subledger_id)
            update_subledger_stats(subledger, entries)
            await self._subledgers.save(subledger)
        return Result.ok(subledger.to_dict())

    async def get_subledger_by_type(self, tenant_id: str, subledger_type: str) -> Result[dict]:
        if not self._subledgers:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledger = await self._subledgers.find_by_type(tenant_id, subledger_type)
        if not subledger:
            await self._provision_subledgers(tenant_id)
            subledger = await self._subledgers.find_by_type(tenant_id, subledger_type)
        if not subledger:
            return Result.fail("financial_kernel.errors.subledger_not_found")
        return Result.ok(subledger.to_dict())

    async def post_subledger_entry(
        self,
        *,
        tenant_id: str,
        subledger_type: str,
        source_document_id: str,
        amount: float,
        entry_date: str,
        currency: str = "USD",
        reference: str = "",
        counterparty: str | None = None,
        description: str = "",
        dimensions: dict | None = None,
        account_mappings: dict | None = None,
        idempotency_key: str | None = None,
        correlation_id: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        tax_amount: float | None = None,
    ) -> Result[dict]:
        if not self._subledgers or not self._subledger_entries:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledger = await self._subledgers.find_by_type(tenant_id, subledger_type)
        if not subledger:
            await self._provision_subledgers(tenant_id)
            subledger = await self._subledgers.find_by_type(tenant_id, subledger_type)
        if not subledger or not subledger.is_active:
            return Result.fail("financial_kernel.errors.subledger_not_found")

        key = idempotency_key or build_subledger_idempotency_key(
            subledger_type, source_document_id
        )
        existing = await self._subledger_entries.find_by_idempotency(tenant_id, key)
        ok, reason = validate_no_duplicate_entry(existing)
        if not ok:
            if existing and existing.journal_id:
                journal = await self._journals.find_by_id(existing.journal_id)
                return Result.ok(
                    {
                        "entry": existing.to_dict(),
                        "journal": journal.to_dict() if journal else None,
                        "idempotent": True,
                    }
                )
            return Result.fail(f"financial_kernel.errors.subledger.{reason}")

        entry = SubledgerEntry.create(
            tenant_id=tenant_id,
            subledger_id=str(subledger.id),
            subledger_type=subledger_type,
            source_context=subledger.source_context,
            source_document_id=source_document_id,
            idempotency_key=key,
            amount=amount,
            entry_date=entry_date,
            currency=currency,
            reference=reference,
            counterparty=counterparty,
            description=description,
            dimensions=dimensions,
            account_mappings=account_mappings or {},
            posting_rule_id=subledger.posting_rule_id,
            side=resolve_entry_side(subledger_type),
        )
        await self._subledger_entries.save(entry)

        journal_result: Result[dict] | None = None
        if subledger.auto_post_to_gl:
            try:
                rule = resolve_rule(
                    subledger.posting_rule_id,
                    tenant_rules=await self._tenant_posting_rules(tenant_id),
                )
            except KeyError:
                return Result.fail("financial_kernel.errors.unknown_posting_rule")
            tenant_accounts = await self._accounts.list_by_tenant(tenant_id)
            mappings = build_subledger_account_mappings(
                rule.account_slots,
                tenant_accounts,
                provided=account_mappings,
            )
            context = PostingExecutionContext(
                amount=amount,
                account_mappings=mappings,
                description=description or f"{subledger.name} entry",
                dimensions=dimensions,
                tax_amount=tax_amount,
            )
            try:
                built_lines = build_lines_from_rule(rule, context)
            except ValueError as exc:
                return Result.fail(f"financial_kernel.errors.posting.{exc}")
            journal_result = await self.post_typed_journal(
                tenant_id=tenant_id,
                journal_type=subledger.journal_type,
                source_context=subledger.source_context,
                source_document_id=source_document_id,
                lines=built_lines,
                currency=currency,
                correlation_id=correlation_id,
                idempotency_key=key,
                organization_id=organization_id,
                branch_id=branch_id,
                require_approval=False,
            )
            if not journal_result.succeeded:
                return journal_result
            journal = journal_result.unwrap()
            entry.mark_posted(journal.get("id", ""))
            await self._subledger_entries.save(entry)

        entries = await self._subledger_entries.list_by_subledger(str(subledger.id))
        update_subledger_stats(subledger, entries)
        await self._subledgers.save(subledger)

        return Result.ok(
            {
                "entry": entry.to_dict(),
                "journal": journal_result.unwrap() if journal_result else None,
                "idempotent": False,
            }
        )

    async def get_subledger_entry(self, tenant_id: str, entry_id: str) -> Result[dict]:
        if not self._subledger_entries:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        entry = await self._subledger_entries.find_by_id(entry_id)
        if not entry or entry.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.subledger_entry_not_found")
        return Result.ok(entry.to_dict())

    async def list_subledger_entries(
        self, tenant_id: str, subledger_id: str
    ) -> Result[list[dict]]:
        if not self._subledger_entries:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledger = await self._subledgers.find_by_id(subledger_id) if self._subledgers else None
        if not subledger or subledger.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.subledger_not_found")
        entries = await self._subledger_entries.list_by_subledger(subledger_id)
        return Result.ok([e.to_dict() for e in entries])

    async def reverse_subledger_entry(
        self,
        *,
        tenant_id: str,
        entry_id: str,
        correlation_id: str,
        reason: str = "",
    ) -> Result[dict]:
        if not self._subledger_entries:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        entry = await self._subledger_entries.find_by_id(entry_id)
        if not entry or entry.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.subledger_entry_not_found")
        if not entry.journal_id:
            return Result.fail("financial_kernel.errors.subledger.not_posted")
        reverse_key = build_subledger_idempotency_key(
            entry.subledger_type, entry.source_document_id, suffix="reversal"
        )
        existing_reverse = await self._subledger_entries.find_by_idempotency(
            tenant_id, reverse_key
        )
        if existing_reverse:
            return Result.ok({"entry": existing_reverse.to_dict(), "idempotent": True})

        reversal = await self.reverse_journal(
            journal_id=entry.journal_id,
            correlation_id=correlation_id,
        )
        if not reversal.succeeded:
            return reversal
        entry.mark_reversed()
        await self._subledger_entries.save(entry)
        subledger = await self._subledgers.find_by_id(entry.subledger_id) if self._subledgers else None
        if subledger:
            entries = await self._subledger_entries.list_by_subledger(str(subledger.id))
            update_subledger_stats(subledger, entries)
            await self._subledgers.save(subledger)
        return Result.ok(
            {
                "original_entry": entry.to_dict(),
                "reversal_journal": reversal.unwrap(),
                "idempotent": False,
            }
        )

    async def run_subledger_reconciliation(
        self,
        *,
        tenant_id: str,
        subledger_id: str,
        reconciliation_date: str,
        period_id: str | None = None,
    ) -> Result[dict]:
        if not self._subledgers or not self._subledger_reconciliations:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledger = await self._subledgers.find_by_id(subledger_id)
        if not subledger or subledger.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.subledger_not_found")

        entries = (
            await self._subledger_entries.list_by_subledger(subledger_id)
            if self._subledger_entries
            else []
        )
        subledger_balance = compute_subledger_balance(
            entries, normal_balance=subledger.normal_balance
        )
        control_account = await self._accounts.find_by_key(
            tenant_id, subledger.control_account_key
        )
        if not control_account:
            return Result.fail(
                f"financial_kernel.errors.control_account_not_found:{subledger.control_account_key}"
            )
        gl_control_balance = control_account.balance
        subledger_items = build_reconciliation_items(entries)

        journal_dicts: list[dict] = []
        for entry in entries:
            if not entry.journal_id:
                continue
            journal = await self._journals.find_by_id(entry.journal_id)
            if journal:
                journal_dicts.append(journal.to_dict())
        gl_items = build_gl_items_from_journals(journal_dicts, control_account.code)

        reconciliation = SubledgerReconciliation.create(
            tenant_id=tenant_id,
            subledger_id=subledger_id,
            subledger_type=subledger.subledger_type,
            reconciliation_date=reconciliation_date,
            subledger_balance=subledger_balance,
            gl_control_balance=gl_control_balance,
            subledger_items=subledger_items,
            gl_items=gl_items,
            control_account_code=control_account.code,
            period_id=period_id,
        )
        await self._subledger_reconciliations.save(reconciliation)
        balance_check = reconcile_balances(
            subledger_balance=subledger_balance,
            gl_control_balance=gl_control_balance,
        )
        return Result.ok({**reconciliation.to_dict(), "balance_check": balance_check})

    async def get_subledger_reconciliation(
        self, tenant_id: str, reconciliation_id: str
    ) -> Result[dict]:
        if not self._subledger_reconciliations:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        reconciliation = await self._subledger_reconciliations.find_by_id(reconciliation_id)
        if not reconciliation or reconciliation.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        return Result.ok(reconciliation.to_dict())

    async def list_subledger_reconciliations(
        self, tenant_id: str, subledger_id: str
    ) -> Result[list[dict]]:
        if not self._subledger_reconciliations:
            return Result.fail("financial_kernel.errors.subledger_not_configured")
        subledger = await self._subledgers.find_by_id(subledger_id) if self._subledgers else None
        if not subledger or subledger.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.subledger_not_found")
        items = await self._subledger_reconciliations.list_by_subledger(subledger_id)
        return Result.ok([r.to_dict() for r in items])

    async def list_reconciliation_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_reconciliation_catalog())

    async def create_reconciliation_run(
        self,
        *,
        tenant_id: str,
        reconciliation_type: str,
        reconciliation_date: str,
        reference_id: str | None,
        reference_label: str,
        left_items: list[dict],
        right_items: list[dict],
        period_id: str | None = None,
        actor_id: str = "system",
        auto_match: bool = True,
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        try:
            definition = get_reconciliation_definition(reconciliation_type)
        except KeyError as exc:
            return Result.fail(str(exc))

        left_total = sum_item_amounts(left_items)
        right_total = sum_item_amounts(right_items)
        matched: list[dict] = []
        unmatched_left = list(left_items)
        unmatched_right = list(right_items)
        if auto_match:
            matched, unmatched_left, unmatched_right = automatic_match_items(
                left_items, right_items
            )

        difference_analysis = build_difference_analysis(
            left_total=left_total,
            right_total=right_total,
            matched_pairs=matched,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
        )
        variance = difference_analysis["variance"]
        exceptions = build_exception_queue(
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
            variance=variance,
        )
        ai_suggestions = generate_ai_suggestions(
            reconciliation_type=reconciliation_type,
            difference_analysis=difference_analysis,
            exceptions=exceptions,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
        )
        run = ReconciliationRun.create(
            tenant_id=tenant_id,
            reconciliation_type=reconciliation_type,
            reference_id=reference_id,
            reference_label=reference_label,
            reconciliation_date=reconciliation_date,
            left_label=definition["left_label"],
            right_label=definition["right_label"],
            left_items=left_items,
            right_items=right_items,
            matched_pairs=matched,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
            left_total=left_total,
            right_total=right_total,
            period_id=period_id,
            difference_analysis=difference_analysis,
            ai_suggestions=ai_suggestions,
            exceptions=exceptions,
        )
        report_summary = build_reconciliation_report(
            reconciliation_type=reconciliation_type,
            reference_label=reference_label,
            reconciliation_date=reconciliation_date,
            difference_analysis=difference_analysis,
            matched_pairs=matched,
            exceptions=exceptions,
            status=run.status,
        )
        run.report_summary = report_summary
        await self._reconciliation_runs.save(run)
        await self._record_reconciliation_audit(
            tenant_id=tenant_id,
            reconciliation_id=str(run.id),
            action="created",
            actor_id=actor_id,
            after_state=run.to_dict(),
            notes=f"type={reconciliation_type}",
        )
        return Result.ok(run.to_dict())

    async def get_reconciliation_run(
        self, tenant_id: str, run_id: str
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        return Result.ok(run.to_dict())

    async def list_reconciliation_runs(
        self,
        tenant_id: str,
        *,
        reconciliation_type: str | None = None,
    ) -> Result[list[dict]]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        if reconciliation_type:
            items = await self._reconciliation_runs.list_by_type(
                tenant_id, reconciliation_type
            )
        else:
            items = await self._reconciliation_runs.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in items])

    async def run_automatic_match(
        self, tenant_id: str, run_id: str, *, actor_id: str = "system"
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        before = run.to_dict()
        matched, unmatched_left, unmatched_right = automatic_match_items(
            run.left_items, run.right_items
        )
        run.matched_pairs = matched
        run.unmatched_left = unmatched_left
        run.unmatched_right = unmatched_right
        run.difference_analysis = build_difference_analysis(
            left_total=run.left_total,
            right_total=run.right_total,
            matched_pairs=matched,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
        )
        run.variance = run.difference_analysis["variance"]
        run.exceptions = build_exception_queue(
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
            variance=run.variance,
        )
        run.ai_suggestions = generate_ai_suggestions(
            reconciliation_type=run.reconciliation_type,
            difference_analysis=run.difference_analysis,
            exceptions=run.exceptions,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
        )
        run._refresh_status()
        run.report_summary = build_reconciliation_report(
            reconciliation_type=run.reconciliation_type,
            reference_label=run.reference_label,
            reconciliation_date=run.reconciliation_date,
            difference_analysis=run.difference_analysis,
            matched_pairs=matched,
            exceptions=run.exceptions,
            status=run.status,
        )
        await self._reconciliation_runs.save(run)
        await self._record_reconciliation_audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="auto_match",
            actor_id=actor_id,
            before_state=before,
            after_state=run.to_dict(),
        )
        return Result.ok(run.to_dict())

    async def apply_reconciliation_manual_match(
        self,
        *,
        tenant_id: str,
        run_id: str,
        left_item: dict,
        right_item: dict,
        actor_id: str,
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        before = run.to_dict()
        run.apply_manual_match(
            left_item=left_item, right_item=right_item, actor_id=actor_id
        )
        run.difference_analysis = build_difference_analysis(
            left_total=run.left_total,
            right_total=run.right_total,
            matched_pairs=run.matched_pairs,
            unmatched_left=run.unmatched_left,
            unmatched_right=run.unmatched_right,
        )
        run.exceptions = build_exception_queue(
            unmatched_left=run.unmatched_left,
            unmatched_right=run.unmatched_right,
            variance=run.variance,
        )
        run.ai_suggestions = generate_ai_suggestions(
            reconciliation_type=run.reconciliation_type,
            difference_analysis=run.difference_analysis,
            exceptions=run.exceptions,
            unmatched_left=run.unmatched_left,
            unmatched_right=run.unmatched_right,
        )
        run.report_summary = build_reconciliation_report(
            reconciliation_type=run.reconciliation_type,
            reference_label=run.reference_label,
            reconciliation_date=run.reconciliation_date,
            difference_analysis=run.difference_analysis,
            matched_pairs=run.matched_pairs,
            exceptions=run.exceptions,
            status=run.status,
        )
        await self._reconciliation_runs.save(run)
        await self._record_reconciliation_audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="manual_match",
            actor_id=actor_id,
            before_state=before,
            after_state=run.to_dict(),
        )
        return Result.ok(run.to_dict())

    async def get_reconciliation_exceptions(
        self, tenant_id: str, run_id: str
    ) -> Result[list[dict]]:
        result = await self.get_reconciliation_run(tenant_id, run_id)
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap()["exceptions"])

    async def get_reconciliation_ai_suggestions(
        self, tenant_id: str, run_id: str
    ) -> Result[list[dict]]:
        result = await self.get_reconciliation_run(tenant_id, run_id)
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap()["ai_suggestions"])

    async def get_reconciliation_difference_analysis(
        self, tenant_id: str, run_id: str
    ) -> Result[dict]:
        result = await self.get_reconciliation_run(tenant_id, run_id)
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap()["difference_analysis"])

    async def get_reconciliation_report(
        self, tenant_id: str, run_id: str
    ) -> Result[dict]:
        result = await self.get_reconciliation_run(tenant_id, run_id)
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap()["report_summary"])

    async def submit_reconciliation_for_approval(
        self, tenant_id: str, run_id: str, *, actor_id: str
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        ok, reason = validate_approval_action(
            current_status=run.status, action=ApprovalAction.SUBMIT.value
        )
        if not ok:
            return Result.fail(f"financial_kernel.errors.reconciliation_approval:{reason}")
        before = run.to_dict()
        run.submit_for_approval(actor_id=actor_id)
        await self._reconciliation_runs.save(run)
        await self._record_reconciliation_audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="submit",
            actor_id=actor_id,
            before_state=before,
            after_state=run.to_dict(),
        )
        return Result.ok(run.to_dict())

    async def approve_reconciliation(
        self, tenant_id: str, run_id: str, *, actor_id: str
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        ok, reason = validate_approval_action(
            current_status=run.status, action=ApprovalAction.APPROVE.value
        )
        if not ok:
            return Result.fail(f"financial_kernel.errors.reconciliation_approval:{reason}")
        before = run.to_dict()
        run.approve(actor_id=actor_id)
        await self._reconciliation_runs.save(run)
        await self._record_reconciliation_audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="approve",
            actor_id=actor_id,
            before_state=before,
            after_state=run.to_dict(),
        )
        return Result.ok(run.to_dict())

    async def reject_reconciliation(
        self,
        tenant_id: str,
        run_id: str,
        *,
        actor_id: str,
        reason: str = "",
    ) -> Result[dict]:
        if not self._reconciliation_runs:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        ok, err = validate_approval_action(
            current_status=run.status, action=ApprovalAction.REJECT.value
        )
        if not ok:
            return Result.fail(f"financial_kernel.errors.reconciliation_approval:{err}")
        before = run.to_dict()
        run.reject(actor_id=actor_id, reason=reason)
        await self._reconciliation_runs.save(run)
        await self._record_reconciliation_audit(
            tenant_id=tenant_id,
            reconciliation_id=run_id,
            action="reject",
            actor_id=actor_id,
            before_state=before,
            after_state=run.to_dict(),
            notes=reason,
        )
        return Result.ok(run.to_dict())

    async def list_reconciliation_audit_history(
        self, tenant_id: str, run_id: str
    ) -> Result[list[dict]]:
        if not self._reconciliation_audits:
            return Result.fail("financial_kernel.errors.reconciliation_not_configured")
        run = await self._reconciliation_runs.find_by_id(run_id) if self._reconciliation_runs else None
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.reconciliation_not_found")
        entries = await self._reconciliation_audits.list_by_reconciliation(run_id)
        return Result.ok([e.to_dict() for e in entries])

    async def _record_reconciliation_audit(
        self,
        *,
        tenant_id: str,
        reconciliation_id: str,
        action: str,
        actor_id: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
        notes: str = "",
    ) -> None:
        if not self._reconciliation_audits:
            return
        entry = ReconciliationAuditLog.record(
            tenant_id=tenant_id,
            reconciliation_id=reconciliation_id,
            action=action,
            actor_id=actor_id,
            before_state=before_state,
            after_state=after_state,
            notes=notes,
        )
        await self._reconciliation_audits.save(entry)

    async def list_dimension_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_dimension_catalog())

    async def create_dimension_value(
        self,
        *,
        tenant_id: str,
        dimension_type: str,
        code: str,
        name: str,
        parent_id: str | None = None,
        metadata: dict | None = None,
        actor_id: str = "system",
    ) -> Result[dict]:
        if not self._dimension_values:
            return Result.fail("financial_kernel.errors.dimensions_not_configured")
        dim_type = normalize_dimension_type(dimension_type)
        try:
            get_dimension_definition(dim_type)
        except KeyError as exc:
            return Result.fail(str(exc))
        existing = await self._dimension_values.find_by_code(tenant_id, dim_type, code)
        if existing:
            return Result.fail("financial_kernel.errors.dimension_code_exists")
        value = DimensionValue.create(
            tenant_id=tenant_id,
            dimension_type=dim_type,
            code=code,
            name=name,
            parent_id=parent_id,
            metadata=metadata,
        )
        await self._dimension_values.save(value)
        await self._record_dimension_audit(
            tenant_id=tenant_id,
            dimension_value_id=str(value.id),
            action="created",
            actor_id=actor_id,
            after_state=value.to_dict(),
        )
        return Result.ok(value.to_dict())

    async def get_dimension_value(
        self, tenant_id: str, value_id: str
    ) -> Result[dict]:
        if not self._dimension_values:
            return Result.fail("financial_kernel.errors.dimensions_not_configured")
        value = await self._dimension_values.find_by_id(value_id)
        if not value or value.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.dimension_not_found")
        return Result.ok(value.to_dict())

    async def list_dimension_values(
        self,
        tenant_id: str,
        *,
        dimension_type: str | None = None,
    ) -> Result[list[dict]]:
        if not self._dimension_values:
            return Result.fail("financial_kernel.errors.dimensions_not_configured")
        if dimension_type:
            dim_type = normalize_dimension_type(dimension_type)
            items = await self._dimension_values.list_by_type(tenant_id, dim_type)
        else:
            items = await self._dimension_values.list_by_tenant(tenant_id)
        return Result.ok([v.to_dict() for v in items])

    async def deactivate_dimension_value(
        self, tenant_id: str, value_id: str, *, actor_id: str = "system"
    ) -> Result[dict]:
        if not self._dimension_values:
            return Result.fail("financial_kernel.errors.dimensions_not_configured")
        value = await self._dimension_values.find_by_id(value_id)
        if not value or value.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.dimension_not_found")
        before = value.to_dict()
        value.deactivate()
        await self._dimension_values.save(value)
        await self._record_dimension_audit(
            tenant_id=tenant_id,
            dimension_value_id=value_id,
            action="deactivated",
            actor_id=actor_id,
            before_state=before,
            after_state=value.to_dict(),
        )
        return Result.ok(value.to_dict())

    async def validate_journal_dimensions(
        self, tenant_id: str, lines: list[dict]
    ) -> Result[dict]:
        enriched = enrich_journal_lines(lines)
        if not self._dimension_values:
            return Result.ok(
                {
                    "valid": True,
                    "issues": [],
                    "summary": summarize_line_dimensions(enriched),
                }
            )
        values = await self._dimension_values.list_by_tenant(tenant_id)
        lookup = build_dimension_lookup([v.to_dict() for v in values])
        valid, issues = validate_line_dimensions(enriched, lookup=lookup)
        return Result.ok(
            {
                "valid": valid,
                "issues": issues,
                "summary": summarize_line_dimensions(enriched),
            }
        )

    async def _validate_journal_dimensions_for_post(
        self, tenant_id: str, lines: list[dict]
    ) -> Result[None]:
        if not self._dimension_values:
            return Result.ok(None)
        values = await self._dimension_values.list_by_tenant(tenant_id)
        if not values:
            return Result.ok(None)
        lookup = build_dimension_lookup([v.to_dict() for v in values])
        valid, issues = validate_line_dimensions(lines, lookup=lookup)
        if not valid:
            first = issues[0]
            return Result.fail(
                f"financial_kernel.errors.dimension.{first['error']}:"
                f"{first['dimension_type']}:{first['code']}"
            )
        return Result.ok(None)

    async def list_dimension_audit_history(
        self, tenant_id: str, value_id: str
    ) -> Result[list[dict]]:
        if not self._dimension_audits:
            return Result.fail("financial_kernel.errors.dimensions_not_configured")
        value = await self._dimension_values.find_by_id(value_id) if self._dimension_values else None
        if not value or value.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.dimension_not_found")
        entries = await self._dimension_audits.list_by_dimension_value(value_id)
        return Result.ok([e.to_dict() for e in entries])

    async def _record_dimension_audit(
        self,
        *,
        tenant_id: str,
        dimension_value_id: str,
        action: str,
        actor_id: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
        notes: str = "",
    ) -> None:
        if not self._dimension_audits:
            return
        entry = DimensionAuditLog.record(
            tenant_id=tenant_id,
            dimension_value_id=dimension_value_id,
            action=action,
            actor_id=actor_id,
            before_state=before_state,
            after_state=after_state,
            notes=notes,
        )
        await self._dimension_audits.save(entry)

    async def list_validation_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_validation_catalog())

    async def validate_transaction(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        lines: list[dict],
        currency: str = "USD",
        base_currency: str = "USD",
        exchange_rate: float = 1.0,
        period_id: str | None = None,
        idempotency_key: str | None = None,
        posting_mode: str = "automatic",
        requires_approval: bool = False,
        journal_entry_type: str = "standard",
        user_permissions: list[str] | None = None,
        actor_id: str = "system",
        persist: bool = True,
    ) -> Result[dict]:
        enriched = enrich_journal_lines(lines)
        key = idempotency_key or f"{source_context}:{source_document_id}"
        existing = await self._journals.find_by_idempotency(tenant_id, key)
        ctx = await self._build_financial_validation_context(
            tenant_id=tenant_id,
            lines=enriched,
            period_id=period_id,
            journal_entry_type=journal_entry_type,
            requires_approval=requires_approval,
            resource_key=key,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            idempotency_key=key,
            duplicate_exists=existing is not None,
            posting_mode=posting_mode,
            user_permissions=user_permissions,
        )
        report = run_full_validation(enriched, context=ctx)
        payload = {
            "report": report,
            "rejected": not report.get("can_post"),
            "source_context": source_context,
            "source_document_id": source_document_id,
        }
        if persist and self._validation_runs:
            run = ValidationRun.create(
                tenant_id=tenant_id,
                source_context=source_context,
                source_document_id=source_document_id,
                report=report,
                lines=enriched,
                idempotency_key=key,
                actor_id=actor_id,
            )
            await self._validation_runs.save(run)
            await self._record_validation_audit(
                tenant_id=tenant_id,
                validation_run_id=str(run.id),
                action="validated",
                actor_id=actor_id,
                report_summary=report.get("summary", {}),
            )
            payload["validation_run_id"] = str(run.id)
        return Result.ok(payload)

    async def get_validation_run(self, tenant_id: str, run_id: str) -> Result[dict]:
        if not self._validation_runs:
            return Result.fail("financial_kernel.errors.validation_not_configured")
        run = await self._validation_runs.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.validation_not_found")
        return Result.ok(run.to_dict())

    async def list_validation_runs(self, tenant_id: str) -> Result[list[dict]]:
        if not self._validation_runs:
            return Result.fail("financial_kernel.errors.validation_not_configured")
        items = await self._validation_runs.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in items])

    async def list_validation_audit_history(
        self, tenant_id: str, run_id: str
    ) -> Result[list[dict]]:
        if not self._validation_audits:
            return Result.fail("financial_kernel.errors.validation_not_configured")
        run = await self._validation_runs.find_by_id(run_id) if self._validation_runs else None
        if not run or run.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.validation_not_found")
        entries = await self._validation_audits.list_by_validation_run(run_id)
        return Result.ok([e.to_dict() for e in entries])

    async def _build_financial_validation_context(
        self,
        *,
        tenant_id: str,
        lines: list[dict],
        period_id: str | None = None,
        journal_entry_type: str = "standard",
        requires_approval: bool = False,
        resource_key: str | None = None,
        currency: str = "USD",
        base_currency: str = "USD",
        exchange_rate: float = 1.0,
        idempotency_key: str | None = None,
        duplicate_exists: bool = False,
        posting_mode: str = "automatic",
        user_permissions: list[str] | None = None,
        journal_status: str | None = None,
    ) -> FinancialValidationContext:
        base_ctx = await self._build_validation_context(
            tenant_id=tenant_id,
            period_id=period_id,
            journal_entry_type=journal_entry_type,
            requires_approval=requires_approval,
            resource_key=resource_key,
        )
        accounts = await self._accounts.list_by_tenant(tenant_id)
        account_active = {a.code: a.is_active for a in accounts}
        account_status = {a.code: a.status for a in accounts}
        dimension_lookup = None
        if self._dimension_values:
            values = await self._dimension_values.list_by_tenant(tenant_id)
            if values:
                dimension_lookup = build_dimension_lookup([v.to_dict() for v in values])
        budget_checks = await self._build_budget_checks(tenant_id, period_id, lines)
        return FinancialValidationContext(
            tenant_id=tenant_id,
            period_status=base_ctx.period_status,
            fiscal_year_status=base_ctx.fiscal_year_status,
            account_postable=base_ctx.account_postable,
            account_active=account_active,
            account_status=account_status,
            account_categories=base_ctx.account_categories,
            locked_resources=base_ctx.locked_resources,
            resource_key=base_ctx.resource_key,
            journal_entry_type=journal_entry_type,
            requires_approval=requires_approval,
            journal_status=journal_status,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            user_permissions=user_permissions,
            posting_mode=posting_mode,
            idempotency_key=idempotency_key,
            duplicate_exists=duplicate_exists,
            dimension_lookup=dimension_lookup,
            budget_checks=budget_checks,
        )

    async def _build_budget_checks(
        self, tenant_id: str, period_id: str | None, lines: list[dict]
    ) -> list[dict]:
        if not period_id:
            return []
        accounts = await self._accounts.list_by_tenant(tenant_id)
        categories = {a.code: a.account_category.value for a in accounts}
        checks: list[dict] = []
        for line in lines:
            code = line.get("account_code", "")
            if categories.get(code) != "expense":
                continue
            account = await self._accounts.find_by_code(tenant_id, code)
            if account:
                rule = get_posting_rule(account.account_type)
                if not rule.budget_tracked:
                    continue
            cost_center = line.get("cost_center")
            budget = await self._budgets.find_match(
                tenant_id, period_id, code, cost_center
            )
            if budget:
                checks.append(
                    {
                        "account_code": code,
                        "cost_center": cost_center,
                        "remaining": budget.remaining,
                    }
                )
        return checks

    async def _record_validation_audit(
        self,
        *,
        tenant_id: str,
        validation_run_id: str,
        action: str,
        actor_id: str,
        report_summary: dict,
        notes: str = "",
    ) -> None:
        if not self._validation_audits:
            return
        entry = ValidationAuditLog.record(
            tenant_id=tenant_id,
            validation_run_id=validation_run_id,
            action=action,
            actor_id=actor_id,
            report_summary=report_summary,
            notes=notes,
        )
        await self._validation_audits.save(entry)

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
        return await self.execute_posting(
            tenant_id=tenant_id,
            rule_id="general_manual",
            source_context=source_context,
            source_document_id=source_document_id,
            currency=currency,
            correlation_id=correlation_id,
            lines=lines,
            idempotency_key=idempotency_key,
            organization_id=organization_id,
            branch_id=branch_id,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            use_default_accounts=False,
            require_approval=False,
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

    async def approve_journal(
        self,
        journal_id: str,
        correlation_id: str,
        *,
        actor_id: str = "system",
        audit_meta: dict | None = None,
    ) -> Result[dict]:
        journal = await self._journals.find_by_id(journal_id)
        if not journal:
            return Result.fail("financial_kernel.errors.journal_not_found")
        rules = get_journal_type_rules(journal.journal_type)
        sig_ok, sig_reason = validate_signature_required(
            journal_type=journal.journal_type,
            has_signature=journal.digital_signature is not None,
        )
        if rules.digital_signature_required and not sig_ok:
            return Result.fail(f"financial_kernel.errors.journal.{sig_reason}")
        budget_ok = await self._validate_and_consume_budget(journal)
        if not budget_ok.succeeded:
            return budget_ok
        journal.approve_and_post(lock_on_post=rules.lock_on_post)
        await self._apply_balances(journal)
        await self._journals.save(journal)
        await self._emit_posted(journal, correlation_id)
        await self._audit_journal(
            action="approved",
            journal_dict=journal.to_dict(),
            correlation_id=correlation_id,
            actor_id=actor_id,
            audit_meta=audit_meta,
        )
        await self._audit_journal(
            action="posted",
            journal_dict=journal.to_dict(),
            correlation_id=correlation_id,
            actor_id=actor_id,
            audit_meta=audit_meta,
        )
        await publish_integration_event(
            JournalApprovedIntegration(
                tenant_id=TenantId.create(journal.tenant_id),
                correlation_id=correlation_id,
                journal_id=journal_id,
            )
        )
        return Result.ok(journal.to_dict())

    async def reverse_journal(
        self,
        journal_id: str,
        correlation_id: str,
        *,
        actor_id: str = "system",
        audit_meta: dict | None = None,
    ) -> Result[dict]:
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
            journal_type="reversing",
        )
        if not result.succeeded:
            return result
        reversal = await self._journals.find_by_id(result.unwrap()["id"])
        assert reversal is not None
        original.mark_reversed(str(reversal.id))
        await self._journals.save(original)
        await self._audit_journal(
            action="reversed",
            journal_dict=original.to_dict(),
            correlation_id=correlation_id,
            actor_id=actor_id,
            audit_meta=audit_meta,
            before_state={"status": "posted"},
            after_state={"status": "reversed", "reversal_journal_id": str(reversal.id)},
        )
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

    async def preview_posting(
        self,
        *,
        tenant_id: str,
        lines: list[dict],
        currency: str = "USD",
        base_currency: str = "USD",
        journal_entry_type: str = JournalEntryType.STANDARD.value,
        period_id: str | None = None,
        requires_approval: bool = False,
    ) -> Result[dict]:
        enriched = enrich_journal_lines(lines)
        ctx = await self._build_financial_validation_context(
            tenant_id=tenant_id,
            lines=enriched,
            period_id=period_id,
            journal_entry_type=journal_entry_type,
            requires_approval=requires_approval,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=1.0,
            posting_mode="manual" if requires_approval else "automatic",
        )
        report = run_full_validation(enriched, context=ctx)
        total_debit = sum(float(l.get("debit", 0)) for l in enriched)
        total_credit = sum(float(l.get("credit", 0)) for l in enriched)
        return Result.ok(
            {
                "validation": report,
                "can_post": report.get("can_post"),
                "preview": {
                    "lines": enriched,
                    "currency": currency,
                    "base_currency": base_currency,
                    "total_debit": total_debit,
                    "total_credit": total_credit,
                    "is_balanced": total_debit == total_credit,
                    "is_compound": len(enriched) > 2,
                    "journal_entry_type": journal_entry_type,
                    "requires_approval": requires_approval,
                },
            }
        )

    async def post_single_entry(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        amount: float,
        primary_account_code: str,
        offset_account_code: str,
        side: str,
        currency: str,
        correlation_id: str,
        description: str = "",
        organization_id: str | None = None,
        branch_id: str | None = None,
        cost_center: str | None = None,
        profit_center: str | None = None,
        idempotency_key: str | None = None,
        require_approval: bool = False,
    ) -> Result[dict]:
        try:
            lines = expand_single_entry_to_double(
                SingleEntryInput(
                    amount=amount,
                    primary_account_code=primary_account_code,
                    offset_account_code=offset_account_code,
                    side=side,
                    description=description,
                    cost_center=cost_center,
                    profit_center=profit_center,
                )
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        return await self._post(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key or f"single:{source_document_id}",
            posting_mode=PostingMode.MANUAL if require_approval else PostingMode.AUTOMATIC,
            organization_id=organization_id,
            branch_id=branch_id,
            require_approval=require_approval,
            journal_entry_type=JournalEntryType.SINGLE_ENTRY.value,
        )

    async def post_adjusting_entry(
        self,
        *,
        tenant_id: str,
        source_document_id: str,
        debit_account: str,
        credit_account: str,
        amount: float,
        currency: str,
        correlation_id: str,
        description: str = "Adjusting entry",
        organization_id: str | None = None,
        require_approval: bool = True,
    ) -> Result[dict]:
        lines = build_adjusting_entry(
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            description=description,
        )
        return await self._post(
            tenant_id=tenant_id,
            source_context="financial_kernel",
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=f"adjusting:{source_document_id}",
            posting_mode=PostingMode.MANUAL,
            organization_id=organization_id,
            require_approval=require_approval,
            journal_entry_type=JournalEntryType.ADJUSTING.value,
        )

    async def post_closing_entry(
        self,
        *,
        tenant_id: str,
        source_document_id: str,
        retained_earnings_account: str,
        income_summary_account: str,
        revenue_closes: list[dict],
        expense_closes: list[dict],
        currency: str,
        correlation_id: str,
        organization_id: str | None = None,
    ) -> Result[dict]:
        lines = build_closing_entry(
            retained_earnings_account=retained_earnings_account,
            income_summary_account=income_summary_account,
            revenue_closes=revenue_closes,
            expense_closes=expense_closes,
        )
        if not lines:
            return Result.fail("financial_kernel.errors.closing_no_lines")
        return await self._post(
            tenant_id=tenant_id,
            source_context="financial_kernel",
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=f"closing:{source_document_id}",
            posting_mode=PostingMode.AUTOMATIC,
            organization_id=organization_id,
            journal_entry_type=JournalEntryType.CLOSING.value,
        )

    async def post_opening_balance(
        self,
        *,
        tenant_id: str,
        source_document_id: str,
        balances: list[dict],
        currency: str,
        correlation_id: str,
        organization_id: str | None = None,
        require_approval: bool = True,
    ) -> Result[dict]:
        lines = build_opening_balance_entry(balances)
        return await self._post(
            tenant_id=tenant_id,
            source_context="financial_kernel",
            source_document_id=source_document_id,
            lines=lines,
            currency=currency,
            base_currency=currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=f"opening:{source_document_id}",
            posting_mode=PostingMode.MANUAL if require_approval else PostingMode.AUTOMATIC,
            organization_id=organization_id,
            require_approval=require_approval,
            journal_entry_type=JournalEntryType.OPENING_BALANCE.value,
        )

    async def post_intercompany_entry(
        self,
        *,
        tenant_id: str,
        source_document_id: str,
        originating_org_id: str,
        counterparty_org_id: str,
        amount: float,
        due_from_account: str,
        due_to_account: str,
        expense_account: str,
        revenue_account: str,
        currency: str,
        correlation_id: str,
        description: str = "Intercompany entry",
    ) -> Result[dict]:
        org_a_lines, org_b_lines, pair_id = build_intercompany_entry(
            originating_org_id=originating_org_id,
            counterparty_org_id=counterparty_org_id,
            amount=amount,
            due_from_account=due_from_account,
            due_to_account=due_to_account,
            expense_account=expense_account,
            revenue_account=revenue_account,
            description=description,
        )
        result_a = await self._post(
            tenant_id=tenant_id,
            source_context="financial_kernel",
            source_document_id=f"{source_document_id}-org-a",
            lines=org_a_lines,
            currency=currency,
            base_currency=currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=f"intercompany:{pair_id}:a",
            posting_mode=PostingMode.AUTOMATIC,
            organization_id=originating_org_id,
            journal_entry_type=JournalEntryType.INTERCOMPANY.value,
        )
        if not result_a.succeeded:
            return result_a
        result_b = await self._post(
            tenant_id=tenant_id,
            source_context="financial_kernel",
            source_document_id=f"{source_document_id}-org-b",
            lines=org_b_lines,
            currency=currency,
            base_currency=currency,
            exchange_rate=1.0,
            correlation_id=correlation_id,
            idempotency_key=f"intercompany:{pair_id}:b",
            posting_mode=PostingMode.AUTOMATIC,
            organization_id=counterparty_org_id,
            journal_entry_type=JournalEntryType.INTERCOMPANY.value,
        )
        if not result_b.succeeded:
            return result_b
        return Result.ok({
            "intercompany_pair_id": pair_id,
            "originating_journal": result_a.unwrap(),
            "counterparty_journal": result_b.unwrap(),
        })

    async def rollback_journal(
        self, journal_id: str, correlation_id: str, *, reason: str = "rollback"
    ) -> Result[dict]:
        original = await self._journals.find_by_id(journal_id)
        if not original:
            return Result.fail("financial_kernel.errors.journal_not_found")
        if original.status != JournalStatus.POSTED:
            return Result.fail("financial_kernel.errors.only_posted_reversible")
        rb_ok, rb_reason = validate_rollback_allowed(original.journal_type)
        if not rb_ok:
            return Result.fail(f"financial_kernel.errors.journal.{rb_reason}")
        plan = build_rollback_plan(original.lines, reason=reason)
        result = await self._post(
            tenant_id=original.tenant_id,
            source_context="financial_kernel",
            source_document_id=f"rollback-{journal_id}",
            lines=plan["reversal_lines"],
            currency=original.currency,
            base_currency=original.base_currency,
            exchange_rate=original.exchange_rate,
            correlation_id=correlation_id,
            idempotency_key=f"rollback:{journal_id}",
            posting_mode=PostingMode.REVERSING,
            organization_id=original.organization_id,
            branch_id=original.branch_id,
            period_id=original.period_id,
            fiscal_year_id=original.fiscal_year_id,
            reverses_journal_id=journal_id,
            journal_entry_type=JournalEntryType.REVERSING.value,
            journal_type="reversing",
        )
        if not result.succeeded:
            return result
        reversal = await self._journals.find_by_id(result.unwrap()["id"])
        assert reversal is not None
        original.mark_reversed(str(reversal.id))
        await self._journals.save(original)
        data = reversal.to_dict()
        data["rollback"] = build_audit_trail_entry(
            action="rollback",
            journal_id=journal_id,
            actor_id=None,
            correlation_id=correlation_id,
            details={"reason": reason, "reversal_journal_id": str(reversal.id)},
        )
        return Result.ok(data)

    async def list_posting_rules_catalog(self) -> Result[list[dict]]:
        legacy = list_posting_rules()
        platform = list_platform_posting_rules()
        seen = {r["rule_id"] for r in platform}
        merged: list[dict] = []
        for rule in platform:
            merged.append({"id": rule["rule_id"], **rule})
        for r in legacy:
            if r["id"] not in seen:
                merged.append(
                    {
                        "id": r["id"],
                        "rule_id": r["id"],
                        "label": r.get("description", r["id"]),
                        "module": "legacy",
                        **r,
                    }
                )
        return Result.ok(merged)

    async def post_with_rule(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        source_context: str,
        source_document_id: str,
        amount: float,
        debit_account: str,
        credit_account: str,
        currency: str,
        correlation_id: str,
        description: str = "",
    ) -> Result[dict]:
        return await self.execute_posting(
            tenant_id=tenant_id,
            rule_id=rule_id,
            source_context=source_context,
            source_document_id=source_document_id,
            amount=amount,
            account_mappings={"debit": debit_account, "credit": credit_account},
            currency=currency,
            correlation_id=correlation_id,
            description=description,
            use_default_accounts=False,
        )

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
            journal_type="recurring",
            journal_entry_type=JournalEntryType.RECURRING.value,
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
        journal_entry_type: str | None = None,
        journal_type: str = "general",
        batch_id: str | None = None,
        lock_on_post: bool | None = None,
        actor_id: str = "system",
        audit_meta: dict | None = None,
    ) -> Result[dict]:
        key = idempotency_key or f"{source_context}:{source_document_id}"
        existing = await self._journals.find_by_idempotency(tenant_id, key)
        if existing:
            return Result.ok(existing.to_dict())

        resolved_type = resolve_journal_type(journal_type)
        type_defaults = apply_type_posting_defaults(
            resolved_type,
            require_approval=require_approval,
            posting_mode=posting_mode,
            journal_entry_type=journal_entry_type,
        )
        require_approval = type_defaults["require_approval"]
        posting_mode = type_defaults["posting_mode"]
        resolved_lock = (
            lock_on_post if lock_on_post is not None else type_defaults["lock_on_post"]
        )

        resolved_period_id = period_id
        period = None
        if period_id:
            period = await self._periods.find_by_id(period_id)
        else:
            period = await self._periods.find_open(tenant_id, organization_id)
            if not period and organization_id:
                period = await self._periods.find_open(tenant_id, None)
            if period:
                resolved_period_id = str(period.id)

        if not period and not period_id:
            return Result.fail("financial_kernel.errors.no_open_period")

        lines = merge_header_dimensions(
            lines,
            organization_id=organization_id,
            branch_id=branch_id,
        )

        if journal_entry_type:
            entry_type = journal_entry_type
        elif type_defaults["journal_entry_type"] != JournalEntryType.STANDARD.value:
            entry_type = type_defaults["journal_entry_type"]
        else:
            entry_type = classify_journal_entry_type(lines)

        settings = await self._ensure_currency_settings(tenant_id)
        txn_currency = currency.upper()
        resolved_base = (base_currency or settings.base_currency).upper()

        fin_ctx = await self._build_financial_validation_context(
            tenant_id=tenant_id,
            lines=lines,
            period_id=resolved_period_id,
            journal_entry_type=entry_type,
            requires_approval=require_approval,
            resource_key=f"{source_context}:{source_document_id}",
            currency=txn_currency,
            base_currency=resolved_base,
            exchange_rate=exchange_rate,
            idempotency_key=key,
            duplicate_exists=False,
            posting_mode=posting_mode,
            user_permissions=None,
        )
        report = run_full_validation(lines, context=fin_ctx)
        ok, err = reject_if_invalid(report)
        if not ok:
            return Result.fail(err)

        for line in lines:
            account = await self._accounts.find_by_code(tenant_id, line["account_code"])
            if not account:
                return Result.fail(f"financial_kernel.errors.unknown_account:{line['account_code']}")

        reporting_currency = settings.reporting_currency
        base_currency = resolved_base

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
            journal_entry_type=entry_type,
            journal_type=resolved_type,
            batch_id=batch_id,
        )
        snapshot.journal_id = str(journal.id)
        await self._rate_snapshots.save(snapshot)

        if require_approval:
            await self._journals.save(journal)
            rules = get_journal_type_rules(resolved_type)
            journal_data = enrich_journal_dict(journal.to_dict(), rules)
            await self._audit_journal(
                action="created",
                journal_dict=journal_data,
                correlation_id=correlation_id,
                actor_id=actor_id,
                audit_meta=audit_meta,
            )
            return Result.ok(journal_data)

        budget_ok = await self._validate_and_consume_budget(journal)
        if not budget_ok.succeeded:
            return budget_ok

        journal.mark_posted(lock_on_post=resolved_lock)
        await self._apply_balances(journal)
        await self._journals.save(journal)
        await self._emit_posted(journal, correlation_id)
        rules = get_journal_type_rules(resolved_type)
        journal_data = enrich_journal_dict(journal.to_dict(), rules)
        audit_action = "reversed" if posting_mode == PostingMode.REVERSING else "posted"
        await self._audit_journal(
            action=audit_action,
            journal_dict=journal_data,
            correlation_id=correlation_id,
            actor_id=actor_id,
            audit_meta=audit_meta,
        )
        return Result.ok(journal_data)

    async def _audit_journal(
        self,
        *,
        action: str,
        journal_dict: dict,
        correlation_id: str,
        actor_id: str = "system",
        audit_meta: dict | None = None,
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> None:
        from contexts.financial_kernel.container import get_financial_audit_service

        meta = audit_meta or {}
        await get_financial_audit_service().record(
            tenant_id=journal_dict["tenant_id"],
            resource_type="journal",
            resource_id=journal_dict["id"],
            action=action,
            actor_id=actor_id,
            correlation_id=correlation_id,
            organization_id=journal_dict.get("organization_id"),
            ip_address=meta.get("ip_address"),
            device=meta.get("device"),
            reason=meta.get("reason", ""),
            before_state=before_state,
            after_state=after_state or journal_dict,
        )

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
            account = await self._accounts.find_by_code(journal.tenant_id, code)
            if account:
                rule = get_posting_rule(account.account_type)
                if not rule.budget_tracked:
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

    async def _build_validation_context(
        self,
        *,
        tenant_id: str,
        period_id: str | None = None,
        journal_entry_type: str = JournalEntryType.STANDARD.value,
        requires_approval: bool = False,
        resource_key: str | None = None,
    ) -> PostingValidationContext:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        account_postable = {
            a.code: a.accepts_gl_posting() for a in accounts
        }
        account_categories = {
            a.code: a.account_category.value if a.account_category else ""
            for a in accounts
        }
        period_status = None
        fiscal_year_status = None
        if period_id:
            period = await self._periods.find_by_id(period_id)
            if period:
                period_status = period.status
                year = await self._years.find_by_id(str(period.fiscal_year_id))
                if year:
                    fiscal_year_status = year.status
        return PostingValidationContext(
            tenant_id=tenant_id,
            period_status=period_status,
            fiscal_year_status=fiscal_year_status,
            account_postable=account_postable,
            account_categories=account_categories,
            journal_entry_type=journal_entry_type,
            requires_approval=requires_approval,
            resource_key=resource_key,
        )

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
        from contexts.financial_kernel.domain.services.account_type_engine import (
            resolve_category_from_type,
        )

        return resolve_category_from_type(account_type)
    raise ValueError("account_category or account_type required")
