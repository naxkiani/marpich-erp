"""Financial Kernel DI."""
from __future__ import annotations

from contexts.financial_kernel.application.financial_ai_service import FinancialAIApplicationService
from contexts.financial_kernel.application.gl_ai_service import GLAIApplicationService
from contexts.financial_kernel.application.financial_consolidation_service import (
    FinancialConsolidationApplicationService,
)
from contexts.financial_kernel.application.financial_statements_service import (
    FinancialStatementsPlatformApplicationService,
)
from contexts.financial_kernel.application.treasury_posting_bridge import TreasuryPostingBridge
from contexts.financial_kernel.application.banking_posting_bridge import BankingPostingBridge
from contexts.financial_kernel.application.exchange_posting_bridge import ExchangePostingBridge
from contexts.financial_kernel.application.pos_posting_bridge import PosPostingBridge
from contexts.financial_kernel.application.financial_audit_service import FinancialAuditApplicationService
from contexts.financial_kernel.application.financial_security_service import FinancialSecurityApplicationService
from contexts.financial_kernel.application.financial_workflow_service import FinancialWorkflowApplicationService
from contexts.financial_kernel.application.cost_center_service import CostCenterApplicationService
from contexts.financial_kernel.application.financial_document_service import FinancialDocumentApplicationService
from contexts.financial_kernel.application.payment_workflow_service import PaymentWorkflowApplicationService
from contexts.financial_kernel.application.procurement_workflow_service import ProcurementWorkflowApplicationService
from contexts.financial_kernel.application.budget_workflow_service import BudgetWorkflowApplicationService
from contexts.financial_kernel.application.treasury_workflow_service import TreasuryWorkflowApplicationService
from contexts.financial_kernel.application.tax_workflow_service import TaxWorkflowApplicationService
from contexts.financial_kernel.application.payment_service import PaymentApplicationService
from contexts.financial_kernel.application.service import FinancialKernelApplicationService
from contexts.financial_kernel.infrastructure.adapters.exchange_rate_provider import (
    CentralBankRateProvider,
    StubExchangeRateProvider,
)
from contexts.financial_kernel.infrastructure.adapters.kernel_client import FinancialKernelClient
from contexts.financial_kernel.infrastructure.persistence.financial_audit_memory_store import (
    InMemoryFinancialAuditRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_validation_memory_store import (
    InMemoryValidationAuditRepository,
    InMemoryValidationRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_dimension_memory_store import (
    InMemoryDimensionAuditRepository,
    InMemoryDimensionValueRepository,
)
from contexts.financial_kernel.infrastructure.persistence.reconciliation_memory_store import (
    InMemoryReconciliationAuditRepository,
    InMemoryReconciliationRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.subledger_memory_store import (
    InMemorySubledgerEntryRepository,
    InMemorySubledgerReconciliationRepository,
    InMemorySubledgerRepository,
)
from contexts.financial_kernel.infrastructure.persistence.account_hierarchy_memory_store import (
    InMemoryAccountTreeRepository,
    InMemoryAccountTreeVersionRepository,
)
from contexts.financial_kernel.infrastructure.persistence.fiscal_calendar_memory_store import (
    InMemoryFiscalCalendarAuditRepository,
    InMemoryFiscalCalendarRepository,
    InMemoryFiscalCloseRequestRepository,
)
from contexts.financial_kernel.infrastructure.persistence.memory_store import (
    InMemoryBudgetRepository,
    InMemoryChartOfAccountRepository,
    InMemoryCurrencyRevaluationRepository,
    InMemoryCurrencySettingsRepository,
    InMemoryDimensionRepository,
    InMemoryExchangeRateRepository,
    InMemoryExchangeRateSnapshotRepository,
    InMemoryFiscalPeriodRepository,
    InMemoryFiscalYearRepository,
    InMemoryJournalRepository,
    InMemoryRecurringJournalRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_ai_memory_store import (
    InMemoryFinancialAIChatRepository,
    InMemoryFinancialAIJobRepository,
)
from contexts.financial_kernel.infrastructure.persistence.gl_ai_memory_store import (
    InMemoryGLAIJobRepository,
)
from contexts.financial_kernel.infrastructure.persistence.payment_workflow_memory_store import (
    InMemoryPaymentWorkflowConfigRepository,
    InMemoryPaymentWorkflowRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.procurement_workflow_memory_store import (
    InMemoryProcurementWorkflowConfigRepository,
    InMemoryProcurementWorkflowRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.budget_workflow_memory_store import (
    InMemoryBudgetWorkflowConfigRepository,
    InMemoryBudgetWorkflowRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.treasury_workflow_memory_store import (
    InMemoryTreasuryWorkflowConfigRepository,
    InMemoryTreasuryWorkflowRunRepository,
    InMemoryTreasuryWorkflowTemplateRepository,
)
from contexts.financial_kernel.infrastructure.persistence.tax_workflow_memory_store import (
    InMemoryTaxWorkflowConfigRepository,
    InMemoryTaxWorkflowRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_consolidation_memory_store import (
    InMemoryConsolidationAuditRepository,
    InMemoryConsolidationGroupRepository,
    InMemoryConsolidationRuleRepository,
    InMemoryConsolidationRunRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_statements_memory_store import (
    InMemoryFinancialStatementRunRepository,
    InMemoryFinancialStatementTemplateRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_security_memory_store import (
    InMemoryMakerCheckerRepository,
    InMemoryPeriodCloseRequestRepository,
    InMemorySecurityAuditRepository,
    InMemorySecurityPolicyRepository,
    InMemoryTransactionLockRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_workflow_memory_store import (
    InMemoryFinancialWorkflowRepository,
)
from contexts.financial_kernel.infrastructure.persistence.cost_center_memory_store import (
    InMemoryCenterAllocationRepository,
    InMemoryEnterpriseCostCenterRepository,
    InMemoryEnterpriseProfitCenterRepository,
)
from contexts.financial_kernel.infrastructure.persistence.financial_document_memory_store import (
    InMemoryFinancialDocumentRepository,
    InMemoryFinancialDocumentVersionRepository,
)
from contexts.financial_kernel.infrastructure.persistence.payment_memory_store import (
    InMemoryInstallmentPlanRepository,
    InMemoryPaymentReconciliationRepository,
    InMemoryPaymentRepository,
)
from contexts.financial_kernel.infrastructure.persistence.posting_rule_memory_store import (
    InMemoryPostingRuleRepository,
)
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: FinancialKernelApplicationService | None = None
_payment_service: PaymentApplicationService | None = None
_financial_document_service: FinancialDocumentApplicationService | None = None
_cost_center_service: CostCenterApplicationService | None = None
_financial_workflow_service: FinancialWorkflowApplicationService | None = None
_financial_audit_service: FinancialAuditApplicationService | None = None
_financial_security_service: FinancialSecurityApplicationService | None = None
_financial_ai_service: FinancialAIApplicationService | None = None
_gl_ai_service: GLAIApplicationService | None = None
_financial_statements_service: FinancialStatementsPlatformApplicationService | None = None
_financial_consolidation_service: FinancialConsolidationApplicationService | None = None
_payment_workflow_service: PaymentWorkflowApplicationService | None = None
_procurement_workflow_service: ProcurementWorkflowApplicationService | None = None
_budget_workflow_service: BudgetWorkflowApplicationService | None = None
_treasury_workflow_service: TreasuryWorkflowApplicationService | None = None
_tax_workflow_service: TaxWorkflowApplicationService | None = None
_treasury_bridge: TreasuryPostingBridge | None = None
_banking_bridge: BankingPostingBridge | None = None
_exchange_bridge: ExchangePostingBridge | None = None
_pos_bridge: PosPostingBridge | None = None
_kernel: FinancialKernelClient | None = None
_registered = False


def get_financial_kernel_service() -> FinancialKernelApplicationService:
    global _service, _kernel, _registered
    if _service is None:
        _service = FinancialKernelApplicationService(
            accounts=InMemoryChartOfAccountRepository(),
            journals=InMemoryJournalRepository(),
            periods=InMemoryFiscalPeriodRepository(),
            years=InMemoryFiscalYearRepository(),
            dimensions=InMemoryDimensionRepository(),
            budgets=InMemoryBudgetRepository(),
            recurring=InMemoryRecurringJournalRepository(),
            currency_settings=InMemoryCurrencySettingsRepository(),
            exchange_rates=InMemoryExchangeRateRepository(),
            rate_snapshots=InMemoryExchangeRateSnapshotRepository(),
            revaluations=InMemoryCurrencyRevaluationRepository(),
            rate_provider=StubExchangeRateProvider(),
            central_bank_provider=CentralBankRateProvider(),
            posting_rules=InMemoryPostingRuleRepository(),
            calendars=InMemoryFiscalCalendarRepository(),
            calendar_audits=InMemoryFiscalCalendarAuditRepository(),
            close_requests=InMemoryFiscalCloseRequestRepository(),
            account_trees=InMemoryAccountTreeRepository(),
            tree_versions=InMemoryAccountTreeVersionRepository(),
            subledgers=InMemorySubledgerRepository(),
            subledger_entries=InMemorySubledgerEntryRepository(),
            subledger_reconciliations=InMemorySubledgerReconciliationRepository(),
            reconciliation_runs=InMemoryReconciliationRunRepository(),
            reconciliation_audits=InMemoryReconciliationAuditRepository(),
            dimension_values=InMemoryDimensionValueRepository(),
            dimension_audits=InMemoryDimensionAuditRepository(),
            validation_runs=InMemoryValidationRunRepository(),
            validation_audits=InMemoryValidationAuditRepository(),
        )
        _kernel = FinancialKernelClient(_service)
    if not _registered:
        _treasury_bridge = TreasuryPostingBridge(_service)
        _banking_bridge = BankingPostingBridge(_service)
        _exchange_bridge = ExchangePostingBridge(_service)
        _pos_bridge = PosPostingBridge(_service)
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        InProcessEventBus.subscribe(
            "treasury.transfer.executed",
            _treasury_bridge.handle_transfer_executed,
        )
        InProcessEventBus.subscribe(
            "treasury.transaction.executed",
            _treasury_bridge.handle_transaction_executed,
        )
        InProcessEventBus.subscribe(
            "banking.account.opened",
            _banking_bridge.handle_account_opened,
        )
        InProcessEventBus.subscribe(
            "banking.deposit.posted",
            _banking_bridge.handle_deposit_posted,
        )
        InProcessEventBus.subscribe(
            "banking.withdrawal.posted",
            _banking_bridge.handle_withdrawal_posted,
        )
        InProcessEventBus.subscribe(
            "banking.interest.accrued",
            _banking_bridge.handle_interest_accrued,
        )
        InProcessEventBus.subscribe(
            "banking.loan.disbursed",
            _banking_bridge.handle_loan_disbursed,
        )
        InProcessEventBus.subscribe(
            "banking.loan.repayment.posted",
            _banking_bridge.handle_loan_repayment_posted,
        )
        InProcessEventBus.subscribe(
            "banking.transfer.posted",
            _banking_bridge.handle_transfer_posted,
        )
        InProcessEventBus.subscribe(
            "banking.settlement.posted",
            _banking_bridge.handle_settlement_posted,
        )
        InProcessEventBus.subscribe(
            "currency_exchange.deal.settled",
            _exchange_bridge.handle_deal_settled,
        )
        InProcessEventBus.subscribe(
            "currency_exchange.fee.charged",
            _exchange_bridge.handle_fee_charged,
        )
        InProcessEventBus.subscribe(
            "currency_exchange.deal.reversed",
            _exchange_bridge.handle_deal_reversed,
        )
        InProcessEventBus.subscribe(
            "currency_exchange.remittance.settled",
            _exchange_bridge.handle_remittance_settled,
        )
        InProcessEventBus.subscribe(
            "pos.sale.completed",
            _pos_bridge.handle_sale_completed,
        )
        _registered = True
    return _service


def get_treasury_posting_bridge() -> TreasuryPostingBridge:
    get_financial_kernel_service()
    assert _treasury_bridge is not None
    return _treasury_bridge


def get_payment_service() -> PaymentApplicationService:
    global _payment_service
    if _payment_service is None:
        _payment_service = PaymentApplicationService(
            payments=InMemoryPaymentRepository(),
            installments=InMemoryInstallmentPlanRepository(),
            reconciliations=InMemoryPaymentReconciliationRepository(),
        )
    return _payment_service


def get_financial_document_service() -> FinancialDocumentApplicationService:
    global _financial_document_service
    if _financial_document_service is None:
        _financial_document_service = FinancialDocumentApplicationService(
            documents=InMemoryFinancialDocumentRepository(),
            versions=InMemoryFinancialDocumentVersionRepository(),
        )
    return _financial_document_service


def get_cost_center_service() -> CostCenterApplicationService:
    global _cost_center_service
    if _cost_center_service is None:
        get_financial_kernel_service()
        _cost_center_service = CostCenterApplicationService(
            cost_centers=InMemoryEnterpriseCostCenterRepository(),
            profit_centers=InMemoryEnterpriseProfitCenterRepository(),
            allocations=InMemoryCenterAllocationRepository(),
            journals=InMemoryJournalRepository(),
            accounts=InMemoryChartOfAccountRepository(),
        )
    return _cost_center_service


def get_financial_workflow_service() -> FinancialWorkflowApplicationService:
    global _financial_workflow_service
    if _financial_workflow_service is None:
        _financial_workflow_service = FinancialWorkflowApplicationService(
            workflows=InMemoryFinancialWorkflowRepository(),
        )
    return _financial_workflow_service


def get_financial_audit_service() -> FinancialAuditApplicationService:
    global _financial_audit_service
    if _financial_audit_service is None:
        _financial_audit_service = FinancialAuditApplicationService(
            audits=InMemoryFinancialAuditRepository(),
        )
    return _financial_audit_service


def get_financial_security_service() -> FinancialSecurityApplicationService:
    global _financial_security_service
    if _financial_security_service is None:
        get_financial_kernel_service()
        _financial_security_service = FinancialSecurityApplicationService(
            audits=InMemorySecurityAuditRepository(),
            policies=InMemorySecurityPolicyRepository(),
            maker_checker=InMemoryMakerCheckerRepository(),
            locks=InMemoryTransactionLockRepository(),
            period_closes=InMemoryPeriodCloseRequestRepository(),
            periods=InMemoryFiscalPeriodRepository(),
            years=InMemoryFiscalYearRepository(),
        )
    return _financial_security_service


def get_financial_ai_service() -> FinancialAIApplicationService:
    global _financial_ai_service
    if _financial_ai_service is None:
        get_financial_kernel_service()
        get_payment_service()
        _financial_ai_service = FinancialAIApplicationService(
            jobs=InMemoryFinancialAIJobRepository(),
            chats=InMemoryFinancialAIChatRepository(),
            journals=InMemoryJournalRepository(),
            accounts=InMemoryChartOfAccountRepository(),
            budgets=InMemoryBudgetRepository(),
            payments=InMemoryPaymentRepository(),
        )
    return _financial_ai_service


def get_gl_ai_service() -> GLAIApplicationService:
    global _gl_ai_service
    if _gl_ai_service is None:
        get_financial_kernel_service()
        _gl_ai_service = GLAIApplicationService(
            jobs=InMemoryGLAIJobRepository(),
            journals=InMemoryJournalRepository(),
            accounts=InMemoryChartOfAccountRepository(),
            budgets=InMemoryBudgetRepository(),
        )
    return _gl_ai_service


def get_financial_statements_platform_service() -> FinancialStatementsPlatformApplicationService:
    global _financial_statements_service
    if _financial_statements_service is None:
        from contexts.policy.container import get_policy_evaluator

        get_financial_kernel_service()
        _financial_statements_service = FinancialStatementsPlatformApplicationService(
            templates=InMemoryFinancialStatementTemplateRepository(),
            runs=InMemoryFinancialStatementRunRepository(),
            policy=get_policy_evaluator(),
        )
    return _financial_statements_service


def get_financial_consolidation_service() -> FinancialConsolidationApplicationService:
    global _financial_consolidation_service
    if _financial_consolidation_service is None:
        from contexts.policy.container import get_policy_evaluator

        get_financial_kernel_service()
        _financial_consolidation_service = FinancialConsolidationApplicationService(
            groups=InMemoryConsolidationGroupRepository(),
            rules=InMemoryConsolidationRuleRepository(),
            runs=InMemoryConsolidationRunRepository(),
            audits=InMemoryConsolidationAuditRepository(),
            policy=get_policy_evaluator(),
        )
    return _financial_consolidation_service


def get_payment_workflow_service() -> PaymentWorkflowApplicationService:
    global _payment_workflow_service
    if _payment_workflow_service is None:
        from contexts.policy.container import get_policy_evaluator

        _payment_workflow_service = PaymentWorkflowApplicationService(
            configs=InMemoryPaymentWorkflowConfigRepository(),
            runs=InMemoryPaymentWorkflowRunRepository(),
            kernel=get_financial_kernel_service(),
            policy=get_policy_evaluator(),
        )
    return _payment_workflow_service


def get_procurement_workflow_service() -> ProcurementWorkflowApplicationService:
    global _procurement_workflow_service
    if _procurement_workflow_service is None:
        from contexts.policy.container import get_policy_evaluator

        _procurement_workflow_service = ProcurementWorkflowApplicationService(
            configs=InMemoryProcurementWorkflowConfigRepository(),
            runs=InMemoryProcurementWorkflowRunRepository(),
            kernel=get_financial_kernel_service(),
            policy=get_policy_evaluator(),
        )
    return _procurement_workflow_service


def get_budget_workflow_service() -> BudgetWorkflowApplicationService:
    global _budget_workflow_service
    if _budget_workflow_service is None:
        from contexts.policy.container import get_policy_evaluator

        _budget_workflow_service = BudgetWorkflowApplicationService(
            configs=InMemoryBudgetWorkflowConfigRepository(),
            runs=InMemoryBudgetWorkflowRunRepository(),
            policy=get_policy_evaluator(),
        )
    return _budget_workflow_service


def get_treasury_workflow_service() -> TreasuryWorkflowApplicationService:
    global _treasury_workflow_service
    if _treasury_workflow_service is None:
        from contexts.policy.container import get_policy_evaluator

        _treasury_workflow_service = TreasuryWorkflowApplicationService(
            templates=InMemoryTreasuryWorkflowTemplateRepository(),
            configs=InMemoryTreasuryWorkflowConfigRepository(),
            runs=InMemoryTreasuryWorkflowRunRepository(),
            policy=get_policy_evaluator(),
        )
    return _treasury_workflow_service


def get_tax_workflow_service() -> TaxWorkflowApplicationService:
    global _tax_workflow_service
    if _tax_workflow_service is None:
        from contexts.policy.container import get_policy_evaluator

        _tax_workflow_service = TaxWorkflowApplicationService(
            configs=InMemoryTaxWorkflowConfigRepository(),
            runs=InMemoryTaxWorkflowRunRepository(),
            policy=get_policy_evaluator(),
        )
    return _tax_workflow_service


def get_financial_kernel() -> IFinancialKernel:
    get_financial_kernel_service()
    assert _kernel is not None
    return _kernel


def reset_financial_kernel_service() -> None:
    global _service, _payment_service, _financial_document_service, _cost_center_service, _financial_workflow_service, _financial_security_service, _financial_audit_service, _financial_ai_service, _gl_ai_service, _financial_statements_service, _financial_consolidation_service, _payment_workflow_service, _procurement_workflow_service, _budget_workflow_service, _treasury_workflow_service, _tax_workflow_service, _treasury_bridge, _banking_bridge, _exchange_bridge, _pos_bridge, _kernel, _registered
    _service = None
    _payment_service = None
    _financial_document_service = None
    _cost_center_service = None
    _financial_workflow_service = None
    _financial_security_service = None
    _financial_audit_service = None
    _financial_ai_service = None
    _gl_ai_service = None
    _financial_statements_service = None
    _financial_consolidation_service = None
    _payment_workflow_service = None
    _procurement_workflow_service = None
    _budget_workflow_service = None
    _treasury_workflow_service = None
    _tax_workflow_service = None
    _treasury_bridge = None
    _banking_bridge = None
    _exchange_bridge = None
    _pos_bridge = None
    _kernel = None
    _registered = False
    InMemoryChartOfAccountRepository.reset()
    InMemoryJournalRepository.reset()
    InMemoryFiscalPeriodRepository.reset()
    InMemoryFiscalYearRepository.reset()
    InMemoryDimensionRepository.reset()
    InMemoryBudgetRepository.reset()
    InMemoryRecurringJournalRepository.reset()
    InMemoryCurrencySettingsRepository.reset()
    InMemoryExchangeRateRepository.reset()
    InMemoryExchangeRateSnapshotRepository.reset()
    InMemoryCurrencyRevaluationRepository.reset()
    InMemoryPaymentRepository.reset()
    InMemoryInstallmentPlanRepository.reset()
    InMemoryPaymentReconciliationRepository.reset()
    InMemoryFinancialDocumentRepository.reset()
    InMemoryFinancialDocumentVersionRepository.reset()
    InMemoryEnterpriseCostCenterRepository.reset()
    InMemoryEnterpriseProfitCenterRepository.reset()
    InMemoryCenterAllocationRepository.reset()
    InMemoryFinancialWorkflowRepository.reset()
    InMemorySecurityAuditRepository.reset()
    InMemorySecurityPolicyRepository.reset()
    InMemoryMakerCheckerRepository.reset()
    InMemoryTransactionLockRepository.reset()
    InMemoryPeriodCloseRequestRepository.reset()
    InMemoryFinancialAIJobRepository.reset()
    InMemoryFinancialAIChatRepository.reset()
    InMemoryGLAIJobRepository.reset()
    InMemoryPostingRuleRepository.reset()
    InMemoryFiscalCalendarRepository.reset()
    InMemoryFiscalCalendarAuditRepository.reset()
    InMemoryFiscalCloseRequestRepository.reset()
    InMemoryAccountTreeRepository.reset()
    InMemoryAccountTreeVersionRepository.reset()
    InMemorySubledgerRepository.reset()
    InMemorySubledgerEntryRepository.reset()
    InMemorySubledgerReconciliationRepository.reset()
    InMemoryReconciliationRunRepository.reset()
    InMemoryReconciliationAuditRepository.reset()
    InMemoryDimensionValueRepository.reset()
    InMemoryDimensionAuditRepository.reset()
    InMemoryValidationRunRepository.reset()
    InMemoryValidationAuditRepository.reset()
    InMemoryFinancialAuditRepository.reset()
    InMemoryFinancialStatementTemplateRepository.reset()
    InMemoryFinancialStatementRunRepository.reset()
    InMemoryConsolidationGroupRepository.reset()
    InMemoryConsolidationRuleRepository.reset()
    InMemoryConsolidationRunRepository.reset()
    InMemoryConsolidationAuditRepository.reset()
    InMemoryPaymentWorkflowConfigRepository.reset()
    InMemoryPaymentWorkflowRunRepository.reset()
    InMemoryProcurementWorkflowConfigRepository.reset()
    InMemoryProcurementWorkflowRunRepository.reset()
    InMemoryBudgetWorkflowConfigRepository.reset()
    InMemoryBudgetWorkflowRunRepository.reset()
    InMemoryTreasuryWorkflowTemplateRepository.reset()
    InMemoryTreasuryWorkflowConfigRepository.reset()
    InMemoryTreasuryWorkflowRunRepository.reset()
    InMemoryTaxWorkflowConfigRepository.reset()
    InMemoryTaxWorkflowRunRepository.reset()
