"""Financial Kernel DI."""
from __future__ import annotations

from contexts.financial_kernel.application.financial_ai_service import FinancialAIApplicationService
from contexts.financial_kernel.application.financial_security_service import FinancialSecurityApplicationService
from contexts.financial_kernel.application.financial_workflow_service import FinancialWorkflowApplicationService
from contexts.financial_kernel.application.cost_center_service import CostCenterApplicationService
from contexts.financial_kernel.application.financial_document_service import FinancialDocumentApplicationService
from contexts.financial_kernel.application.payment_service import PaymentApplicationService
from contexts.financial_kernel.application.service import FinancialKernelApplicationService
from contexts.financial_kernel.infrastructure.adapters.exchange_rate_provider import (
    CentralBankRateProvider,
    StubExchangeRateProvider,
)
from contexts.financial_kernel.infrastructure.adapters.kernel_client import FinancialKernelClient
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
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: FinancialKernelApplicationService | None = None
_payment_service: PaymentApplicationService | None = None
_financial_document_service: FinancialDocumentApplicationService | None = None
_cost_center_service: CostCenterApplicationService | None = None
_financial_workflow_service: FinancialWorkflowApplicationService | None = None
_financial_security_service: FinancialSecurityApplicationService | None = None
_financial_ai_service: FinancialAIApplicationService | None = None
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
        )
        _kernel = FinancialKernelClient(_service)
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


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


def get_financial_kernel() -> IFinancialKernel:
    get_financial_kernel_service()
    assert _kernel is not None
    return _kernel


def reset_financial_kernel_service() -> None:
    global _service, _payment_service, _financial_document_service, _cost_center_service, _financial_workflow_service, _financial_security_service, _financial_ai_service, _kernel, _registered
    _service = None
    _payment_service = None
    _financial_document_service = None
    _cost_center_service = None
    _financial_workflow_service = None
    _financial_security_service = None
    _financial_ai_service = None
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
