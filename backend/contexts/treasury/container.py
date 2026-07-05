"""Treasury DI."""
from __future__ import annotations

from contexts.treasury.application.bank_account_service import BankAccountApplicationService
from contexts.treasury.application.cash_management_service import CashManagementApplicationService
from contexts.treasury.application.bank_reconciliation_service import BankReconciliationApplicationService
from contexts.treasury.application.cash_reconciliation_service import CashReconciliationApplicationService
from contexts.treasury.application.investment_service import InvestmentApplicationService
from contexts.treasury.application.treasury_workflow_service import TreasuryWorkflowApplicationService
from contexts.treasury.application.treasury_security_service import TreasurySecurityApplicationService
from contexts.treasury.application.treasury_analytics_service import TreasuryAnalyticsApplicationService
from contexts.treasury.application.multi_currency_service import MultiCurrencyApplicationService
from contexts.treasury.application.risk_service import RiskApplicationService
from contexts.treasury.application.cash_forecast_service import CashForecastApplicationService
from contexts.treasury.application.liquidity_service import LiquidityApplicationService
from contexts.treasury.application.service import TreasuryApplicationService
from contexts.treasury.application.treasury_transaction_service import TreasuryTransactionApplicationService
from contexts.treasury.infrastructure.persistence.treasury_transaction_memory_store import (
    InMemoryTreasuryTransactionRepository,
)
from contexts.treasury.infrastructure.persistence.bank_account_memory_store import (
    InMemoryBankAccountDocumentRepository,
    InMemoryBankAccountRepository,
    InMemoryBankBranchRepository,
    InMemoryBankRepository,
    InMemorySignatoryRepository,
)
from contexts.treasury.infrastructure.persistence.cash_management_memory_store import (
    InMemoryCashClosingRepository,
    InMemoryCashCountRepository,
    InMemoryCashLocationRepository,
    InMemoryCashReconciliationRepository,
    InMemoryCashTransactionRepository,
    InMemoryCashVerificationRepository,
)
from contexts.treasury.infrastructure.persistence.bank_reconciliation_memory_store import (
    InMemoryBankStatementImportRepository,
    InMemoryEnterpriseBankReconciliationRepository,
    InMemoryReconciliationAuditRepository,
)
from contexts.treasury.infrastructure.persistence.cash_reconciliation_memory_store import (
    InMemoryCashReconciliationAuditRepository,
    InMemoryCashReconciliationRunRepository,
)
from contexts.treasury.infrastructure.persistence.investment_memory_store import (
    InMemoryInvestmentRepository,
    InMemoryInvestmentTransactionRepository,
)
from contexts.treasury.infrastructure.persistence.treasury_security_memory_store import (
    InMemoryAccessRuleRepository,
    InMemoryApprovalMatrixRepository,
    InMemorySecurityAuditRepository,
    InMemorySecurityLockRepository,
    InMemorySecurityOperationRepository,
    InMemorySecurityPolicyRepository,
    InMemoryTransactionLimitRepository,
)
from contexts.treasury.infrastructure.persistence.treasury_workflow_memory_store import (
    InMemoryWorkflowAuditRepository,
    InMemoryWorkflowDefinitionRepository,
    InMemoryWorkflowLimitRepository,
    InMemoryWorkflowRequestRepository,
)
from contexts.treasury.infrastructure.persistence.multi_currency_memory_store import (
    InMemoryExchangeRateRepository,
    InMemoryFxTransactionRepository,
)
from contexts.treasury.infrastructure.persistence.risk_memory_store import (
    InMemoryRiskAlertRepository,
    InMemoryRiskLimitRepository,
    InMemoryStressTestRepository,
)
from contexts.treasury.infrastructure.persistence.cash_forecast_memory_store import (
    InMemoryCashForecastPlanRepository,
    InMemoryForecastSimulationRepository,
)
from contexts.treasury.infrastructure.persistence.liquidity_memory_store import (
    InMemoryCashPoolRepository,
    InMemoryFundingNeedRepository,
    InMemoryLiquiditySnapshotRepository,
)
from contexts.treasury.infrastructure.persistence.memory_store import (
    InMemoryBankReconciliationRepository,
    InMemoryCashForecastRepository,
    InMemoryTreasuryAccountRepository,
    InMemoryTreasuryTransferRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: TreasuryApplicationService | None = None
_bank_account_service: BankAccountApplicationService | None = None
_cash_management_service: CashManagementApplicationService | None = None
_transaction_service: TreasuryTransactionApplicationService | None = None
_liquidity_service: LiquidityApplicationService | None = None
_cash_forecast_service: CashForecastApplicationService | None = None
_bank_reconciliation_service: BankReconciliationApplicationService | None = None
_cash_reconciliation_service: CashReconciliationApplicationService | None = None
_investment_service: InvestmentApplicationService | None = None
_risk_service: RiskApplicationService | None = None
_multi_currency_service: MultiCurrencyApplicationService | None = None
_treasury_workflow_service: TreasuryWorkflowApplicationService | None = None
_treasury_security_service: TreasurySecurityApplicationService | None = None
_treasury_analytics_service: TreasuryAnalyticsApplicationService | None = None
_registered = False
_cash_registered = False
_liquidity_registered = False
_forecast_registered = False
_investment_registered = False
_risk_registered = False
_fx_registered = False
_workflow_registered = False
_security_registered = False
_analytics_registered = False


def get_treasury_service() -> TreasuryApplicationService:
    global _service, _registered
    if _service is None:
        _service = TreasuryApplicationService(
            accounts=InMemoryTreasuryAccountRepository(),
            transfers=InMemoryTreasuryTransferRepository(),
            reconciliations=InMemoryBankReconciliationRepository(),
            forecasts=InMemoryCashForecastRepository(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def get_bank_account_service() -> BankAccountApplicationService:
    global _bank_account_service
    if _bank_account_service is None:
        get_treasury_service()
        _bank_account_service = BankAccountApplicationService(
            banks=InMemoryBankRepository(),
            branches=InMemoryBankBranchRepository(),
            accounts=InMemoryBankAccountRepository(),
            signatories=InMemorySignatoryRepository(),
            documents=InMemoryBankAccountDocumentRepository(),
        )
    return _bank_account_service


def get_cash_management_service() -> CashManagementApplicationService:
    global _cash_management_service, _cash_registered
    if _cash_management_service is None:
        get_treasury_service()
        _cash_management_service = CashManagementApplicationService(
            locations=InMemoryCashLocationRepository(),
            transactions=InMemoryCashTransactionRepository(),
            counts=InMemoryCashCountRepository(),
            verifications=InMemoryCashVerificationRepository(),
            closings=InMemoryCashClosingRepository(),
            reconciliations=InMemoryCashReconciliationRepository(),
            forecasts=InMemoryCashForecastRepository(),
        )
    if not _cash_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _cash_management_service.handle_tenant_provisioned,
        )
        _cash_registered = True
    return _cash_management_service


def get_treasury_transaction_service() -> TreasuryTransactionApplicationService:
    global _transaction_service
    if _transaction_service is None:
        treasury = get_treasury_service()
        _transaction_service = TreasuryTransactionApplicationService(
            transactions=InMemoryTreasuryTransactionRepository(),
            accounts=treasury._accounts,
        )
    return _transaction_service


def get_liquidity_service() -> LiquidityApplicationService:
    global _liquidity_service, _liquidity_registered
    if _liquidity_service is None:
        treasury = get_treasury_service()
        _liquidity_service = LiquidityApplicationService(
            accounts=treasury._accounts,
            forecasts=treasury._forecasts,
            pools=InMemoryCashPoolRepository(),
            snapshots=InMemoryLiquiditySnapshotRepository(),
            funding_needs=InMemoryFundingNeedRepository(),
        )
    if not _liquidity_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _liquidity_service.handle_tenant_provisioned,
        )
        _liquidity_registered = True
    return _liquidity_service


def get_cash_forecast_service() -> CashForecastApplicationService:
    global _cash_forecast_service, _forecast_registered
    if _cash_forecast_service is None:
        treasury = get_treasury_service()
        _cash_forecast_service = CashForecastApplicationService(
            accounts=treasury._accounts,
            plans=InMemoryCashForecastPlanRepository(),
            simulations=InMemoryForecastSimulationRepository(),
        )
    if not _forecast_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _cash_forecast_service.handle_tenant_provisioned,
        )
        _forecast_registered = True
    return _cash_forecast_service


def get_bank_reconciliation_service() -> BankReconciliationApplicationService:
    global _bank_reconciliation_service
    if _bank_reconciliation_service is None:
        treasury = get_treasury_service()
        _bank_reconciliation_service = BankReconciliationApplicationService(
            accounts=treasury._accounts,
            transfers=treasury._transfers,
            statements=InMemoryBankStatementImportRepository(),
            reconciliations=InMemoryEnterpriseBankReconciliationRepository(),
            audits=InMemoryReconciliationAuditRepository(),
        )
    return _bank_reconciliation_service


def get_cash_reconciliation_service() -> CashReconciliationApplicationService:
    global _cash_reconciliation_service
    if _cash_reconciliation_service is None:
        cash_mgmt = get_cash_management_service()
        _cash_reconciliation_service = CashReconciliationApplicationService(
            locations=cash_mgmt._locations,
            runs=InMemoryCashReconciliationRunRepository(),
            audits=InMemoryCashReconciliationAuditRepository(),
        )
    return _cash_reconciliation_service


def get_investment_service() -> InvestmentApplicationService:
    global _investment_service, _investment_registered
    if _investment_service is None:
        treasury = get_treasury_service()
        _investment_service = InvestmentApplicationService(
            accounts=treasury._accounts,
            investments=InMemoryInvestmentRepository(),
            transactions=InMemoryInvestmentTransactionRepository(),
        )
    if not _investment_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _investment_service.handle_tenant_provisioned,
        )
        _investment_registered = True
    return _investment_service


def get_risk_service() -> RiskApplicationService:
    global _risk_service, _risk_registered
    if _risk_service is None:
        treasury = get_treasury_service()
        liquidity = get_liquidity_service()
        investment = get_investment_service()
        _risk_service = RiskApplicationService(
            accounts=treasury._accounts,
            investments=investment._investments,
            funding_needs=liquidity._funding_needs,
            limits=InMemoryRiskLimitRepository(),
            alerts=InMemoryRiskAlertRepository(),
            stress_tests=InMemoryStressTestRepository(),
        )
    if not _risk_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _risk_service.handle_tenant_provisioned,
        )
        _risk_registered = True
    return _risk_service


def get_multi_currency_service() -> MultiCurrencyApplicationService:
    global _multi_currency_service, _fx_registered
    if _multi_currency_service is None:
        treasury = get_treasury_service()
        investment = get_investment_service()
        _multi_currency_service = MultiCurrencyApplicationService(
            accounts=treasury._accounts,
            investments=investment._investments,
            rates=InMemoryExchangeRateRepository(),
            transactions=InMemoryFxTransactionRepository(),
        )
    if not _fx_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _multi_currency_service.handle_tenant_provisioned,
        )
        _fx_registered = True
    return _multi_currency_service


def get_treasury_workflow_service() -> TreasuryWorkflowApplicationService:
    global _treasury_workflow_service, _workflow_registered
    if _treasury_workflow_service is None:
        _treasury_workflow_service = TreasuryWorkflowApplicationService(
            definitions=InMemoryWorkflowDefinitionRepository(),
            limits=InMemoryWorkflowLimitRepository(),
            requests=InMemoryWorkflowRequestRepository(),
            audits=InMemoryWorkflowAuditRepository(),
        )
    if not _workflow_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _treasury_workflow_service.handle_tenant_provisioned,
        )
        _workflow_registered = True
    return _treasury_workflow_service


def get_treasury_security_service() -> TreasurySecurityApplicationService:
    global _treasury_security_service, _security_registered
    if _treasury_security_service is None:
        _treasury_security_service = TreasurySecurityApplicationService(
            policies=InMemorySecurityPolicyRepository(),
            limits=InMemoryTransactionLimitRepository(),
            matrix=InMemoryApprovalMatrixRepository(),
            access_rules=InMemoryAccessRuleRepository(),
            locks=InMemorySecurityLockRepository(),
            operations=InMemorySecurityOperationRepository(),
            audits=InMemorySecurityAuditRepository(),
        )
    if not _security_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _treasury_security_service.handle_tenant_provisioned,
        )
        _security_registered = True
    return _treasury_security_service


def get_treasury_analytics_service() -> TreasuryAnalyticsApplicationService:
    global _treasury_analytics_service, _analytics_registered
    if _treasury_analytics_service is None:
        treasury = get_treasury_service()
        liquidity = get_liquidity_service()
        forecast = get_cash_forecast_service()
        investment = get_investment_service()
        fx = get_multi_currency_service()
        risk = get_risk_service()
        _treasury_analytics_service = TreasuryAnalyticsApplicationService(
            accounts=treasury._accounts,
            forecasts=treasury._forecasts,
            forecast_plans=forecast._plans,
            pools=liquidity._pools,
            funding_needs=liquidity._funding_needs,
            investments=investment._investments,
            rates=fx._rates,
            fx_transactions=fx._transactions,
            alerts=risk._alerts,
        )
    if not _analytics_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _treasury_analytics_service.handle_tenant_provisioned,
        )
        _analytics_registered = True
    return _treasury_analytics_service


def reset_treasury_service() -> None:
    global _service, _bank_account_service, _cash_management_service, _transaction_service, _liquidity_service, _cash_forecast_service, _bank_reconciliation_service, _cash_reconciliation_service, _investment_service, _risk_service, _multi_currency_service, _treasury_workflow_service, _treasury_security_service, _treasury_analytics_service, _registered, _cash_registered, _liquidity_registered, _forecast_registered, _investment_registered, _risk_registered, _fx_registered, _workflow_registered, _security_registered, _analytics_registered
    _service = None
    _bank_account_service = None
    _cash_management_service = None
    _transaction_service = None
    _liquidity_service = None
    _cash_forecast_service = None
    _bank_reconciliation_service = None
    _cash_reconciliation_service = None
    _investment_service = None
    _risk_service = None
    _multi_currency_service = None
    _treasury_workflow_service = None
    _treasury_security_service = None
    _treasury_analytics_service = None
    _registered = False
    _cash_registered = False
    _liquidity_registered = False
    _forecast_registered = False
    _investment_registered = False
    _risk_registered = False
    _fx_registered = False
    _workflow_registered = False
    _security_registered = False
    _analytics_registered = False
    InMemoryTreasuryAccountRepository.reset()
    InMemoryTreasuryTransferRepository.reset()
    InMemoryBankReconciliationRepository.reset()
    InMemoryCashForecastRepository.reset()
    InMemoryBankRepository.reset()
    InMemoryBankBranchRepository.reset()
    InMemoryBankAccountRepository.reset()
    InMemorySignatoryRepository.reset()
    InMemoryBankAccountDocumentRepository.reset()
    InMemoryCashLocationRepository.reset()
    InMemoryCashTransactionRepository.reset()
    InMemoryCashCountRepository.reset()
    InMemoryCashVerificationRepository.reset()
    InMemoryCashClosingRepository.reset()
    InMemoryCashReconciliationRepository.reset()
    InMemoryTreasuryTransactionRepository.reset()
    InMemoryCashPoolRepository.reset()
    InMemoryLiquiditySnapshotRepository.reset()
    InMemoryFundingNeedRepository.reset()
    InMemoryCashForecastPlanRepository.reset()
    InMemoryForecastSimulationRepository.reset()
    InMemoryBankStatementImportRepository.reset()
    InMemoryEnterpriseBankReconciliationRepository.reset()
    InMemoryReconciliationAuditRepository.reset()
    InMemoryCashReconciliationRunRepository.reset()
    InMemoryCashReconciliationAuditRepository.reset()
    InMemoryInvestmentRepository.reset()
    InMemoryInvestmentTransactionRepository.reset()
    InMemoryRiskLimitRepository.reset()
    InMemoryRiskAlertRepository.reset()
    InMemoryStressTestRepository.reset()
    InMemoryExchangeRateRepository.reset()
    InMemoryFxTransactionRepository.reset()
    InMemoryWorkflowDefinitionRepository.reset()
    InMemoryWorkflowLimitRepository.reset()
    InMemoryWorkflowRequestRepository.reset()
    InMemoryWorkflowAuditRepository.reset()
    InMemorySecurityPolicyRepository.reset()
    InMemoryTransactionLimitRepository.reset()
    InMemoryApprovalMatrixRepository.reset()
    InMemoryAccessRuleRepository.reset()
    InMemorySecurityLockRepository.reset()
    InMemorySecurityOperationRepository.reset()
    InMemorySecurityAuditRepository.reset()
