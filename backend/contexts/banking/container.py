"""Banking DI — Customer Account + KYC + Deposit + Loan + Interest + Payments + Settlement + Branch + Security + Analytics."""
from __future__ import annotations

from contexts.banking.application.customer_account_service import (
    BankingCustomerAccountApplicationService,
)
from contexts.banking.application.deposit_management_service import (
    BankingDepositManagementApplicationService,
)
from contexts.banking.application.kyc_platform_service import (
    BankingKycPlatformApplicationService,
)
from contexts.banking.application.payment_platform_service import (
    BankingPaymentPlatformApplicationService,
)
from contexts.banking.application.branch_banking_service import (
    BankingBranchPlatformApplicationService,
)
from contexts.banking.application.banking_analytics_service import (
    BankingAnalyticsPlatformApplicationService,
)
from contexts.banking.application.banking_security_service import (
    BankingSecurityPlatformApplicationService,
)
from contexts.banking.application.settlement_engine_service import (
    BankingSettlementEngineApplicationService,
)
from contexts.banking.application.interest_calculation_service import (
    BankingInterestCalculationApplicationService,
)
from contexts.banking.application.loan_management_service import (
    BankingLoanManagementApplicationService,
)
from contexts.banking.infrastructure.persistence.customer_account_memory_store import (
    InMemoryAccountAuditRepository,
    InMemoryAccountProductRepository,
    InMemoryAccountRepository,
    InMemoryCustomerRepository,
    InMemoryKycRepository,
)
from contexts.banking.infrastructure.persistence.postgres_store import (
    PostgresAccountProductRepository,
    PostgresAccountRepository,
    PostgresCustomerRepository,
    PostgresDepositAccrualRepository,
    PostgresDepositProfileRepository,
    PostgresDepositTransactionRepository,
    PostgresLoanCollateralRepository,
    PostgresLoanCreditRiskRepository,
    PostgresLoanGuarantorRepository,
    PostgresLoanInstallmentRepository,
    PostgresLoanProfileRepository,
    PostgresLoanTransactionRepository,
    PostgresPaymentTransferRepository,
    PostgresProfitRuleRepository,
)
from contexts.banking.infrastructure.persistence.deposit_management_memory_store import (
    InMemoryDepositAccrualRepository,
    InMemoryDepositAuditRepository,
    InMemoryDepositCertificateRepository,
    InMemoryDepositProfileRepository,
    InMemoryDepositStatementRepository,
    InMemoryDepositTransactionRepository,
    InMemoryDepositWorkflowRepository,
    InMemoryProfitRuleRepository,
)
from contexts.banking.infrastructure.persistence.kyc_platform_memory_store import (
    InMemoryKycAddressRepository,
    InMemoryKycAuditRepository,
    InMemoryKycBiometricRepository,
    InMemoryKycCaseRepository,
    InMemoryKycDocumentRepository,
    InMemoryKycReviewRepository,
    InMemoryKycScreeningRepository,
    InMemoryKycWorkflowRepository,
)
from contexts.banking.infrastructure.persistence.payment_platform_memory_store import (
    InMemoryPaymentAuditRepository,
    InMemoryPaymentBatchRepository,
    InMemoryPaymentBeneficiaryRepository,
    InMemoryPaymentFraudRepository,
    InMemoryPaymentTransferRepository,
    InMemoryPaymentWorkflowRepository,
    InMemoryStandingOrderRepository,
)
from contexts.banking.infrastructure.persistence.banking_analytics_memory_store import (
    InMemoryBankingAnalyticsJobRepository,
)
from contexts.banking.infrastructure.persistence.banking_security_memory_store import (
    InMemoryEmergencyFreezeRepository,
    InMemoryLimitUsageRepository,
    InMemorySecurityApprovalRepository,
    InMemorySecurityAuditRepository,
    InMemorySecurityDeviceRepository,
    InMemorySecuritySessionRepository,
    InMemoryTransactionMonitorRepository,
)
from contexts.banking.infrastructure.persistence.branch_banking_memory_store import (
    InMemoryBranchAuditRepository,
    InMemoryBranchCashLimitRepository,
    InMemoryBranchDaySessionRepository,
    InMemoryBranchEmployeeAssignmentRepository,
    InMemoryBranchExtensionRepository,
    InMemoryBranchKPIRepository,
    InMemoryBranchOfficeRepository,
    InMemoryBranchVaultMovementRepository,
    InMemoryBranchVaultRepository,
)
from contexts.banking.infrastructure.persistence.settlement_engine_memory_store import (
    InMemoryReconciliationMatchRepository,
    InMemoryReconciliationRunRepository,
    InMemorySettlementAdjustmentRepository,
    InMemorySettlementAuditRepository,
    InMemorySettlementBatchRepository,
    InMemorySettlementDifferenceRepository,
    InMemorySettlementExceptionRepository,
    InMemorySettlementItemRepository,
    InMemorySettlementReportRepository,
)
from contexts.banking.infrastructure.persistence.interest_calculation_memory_store import (
    InMemoryInterestCalculationAuditRepository,
    InMemoryInterestRateChangeRepository,
    InMemoryInterestRateProfileRepository,
)
from contexts.banking.infrastructure.persistence.loan_management_memory_store import (
    InMemoryLoanAuditRepository,
    InMemoryLoanCollateralRepository,
    InMemoryLoanCreditRiskRepository,
    InMemoryLoanGuarantorRepository,
    InMemoryLoanInstallmentRepository,
    InMemoryLoanProfileRepository,
    InMemoryLoanTransactionRepository,
    InMemoryLoanWorkflowRepository,
)
from contexts.financial_kernel.container import get_financial_kernel
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_customer_repo = None
_account_repo = None
_product_repo = None
_transfer_repo = None
_deposit_repo = None
_deposit_tx_repo = None
_deposit_accrual_repo = None
_profit_rule_repo = None
_loan_repo = None
_loan_tx_repo = None
_loan_installment_repo = None
_loan_collateral_repo = None
_loan_guarantor_repo = None
_loan_credit_risk_repo = None

_service: BankingCustomerAccountApplicationService | None = None
_kyc_service: BankingKycPlatformApplicationService | None = None
_deposit_service: BankingDepositManagementApplicationService | None = None
_loan_service: BankingLoanManagementApplicationService | None = None
_interest_service: BankingInterestCalculationApplicationService | None = None
_payment_service: BankingPaymentPlatformApplicationService | None = None
_settlement_service: BankingSettlementEngineApplicationService | None = None
_branch_service: BankingBranchPlatformApplicationService | None = None
_security_service: BankingSecurityPlatformApplicationService | None = None
_analytics_service: BankingAnalyticsPlatformApplicationService | None = None
_registered = False
_kyc_registered = False
_deposit_registered = False
_loan_registered = False
_interest_registered = False
_payment_registered = False
_settlement_registered = False
_branch_registered = False
_security_registered = False
_analytics_registered = False


def _ensure_money_path_repos() -> None:
    global _customer_repo, _account_repo, _product_repo, _transfer_repo
    if _customer_repo is not None:
        return
    if use_postgres():
        _customer_repo = PostgresCustomerRepository()
        _account_repo = PostgresAccountRepository()
        _product_repo = PostgresAccountProductRepository()
        _transfer_repo = PostgresPaymentTransferRepository()
    else:
        _customer_repo = InMemoryCustomerRepository()
        _account_repo = InMemoryAccountRepository()
        _product_repo = InMemoryAccountProductRepository()
        _transfer_repo = InMemoryPaymentTransferRepository()


def _ensure_deposit_loan_repos() -> None:
    global _deposit_repo, _deposit_tx_repo, _deposit_accrual_repo, _profit_rule_repo
    global _loan_repo, _loan_tx_repo, _loan_installment_repo
    global _loan_collateral_repo, _loan_guarantor_repo, _loan_credit_risk_repo
    if _deposit_repo is not None:
        return
    if use_postgres():
        _deposit_repo = PostgresDepositProfileRepository()
        _deposit_tx_repo = PostgresDepositTransactionRepository()
        _deposit_accrual_repo = PostgresDepositAccrualRepository()
        _profit_rule_repo = PostgresProfitRuleRepository()
        _loan_repo = PostgresLoanProfileRepository()
        _loan_tx_repo = PostgresLoanTransactionRepository()
        _loan_installment_repo = PostgresLoanInstallmentRepository()
        _loan_collateral_repo = PostgresLoanCollateralRepository()
        _loan_guarantor_repo = PostgresLoanGuarantorRepository()
        _loan_credit_risk_repo = PostgresLoanCreditRiskRepository()
    else:
        _deposit_repo = InMemoryDepositProfileRepository()
        _deposit_tx_repo = InMemoryDepositTransactionRepository()
        _deposit_accrual_repo = InMemoryDepositAccrualRepository()
        _profit_rule_repo = InMemoryProfitRuleRepository()
        _loan_repo = InMemoryLoanProfileRepository()
        _loan_tx_repo = InMemoryLoanTransactionRepository()
        _loan_installment_repo = InMemoryLoanInstallmentRepository()
        _loan_collateral_repo = InMemoryLoanCollateralRepository()
        _loan_guarantor_repo = InMemoryLoanGuarantorRepository()
        _loan_credit_risk_repo = InMemoryLoanCreditRiskRepository()


def get_banking_customer_account_service() -> BankingCustomerAccountApplicationService:
    global _service, _registered
    _ensure_money_path_repos()
    if _service is None:
        _service = BankingCustomerAccountApplicationService(
            customers=_customer_repo,
            kyc_records=InMemoryKycRepository(),
            products=_product_repo,
            accounts=_account_repo,
            audits=InMemoryAccountAuditRepository(),
            kernel=get_financial_kernel(),
            policy=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def get_banking_kyc_platform_service() -> BankingKycPlatformApplicationService:
    global _kyc_service, _kyc_registered
    if _kyc_service is None:
        get_banking_customer_account_service()
        _kyc_service = BankingKycPlatformApplicationService(
            cases=InMemoryKycCaseRepository(),
            documents=InMemoryKycDocumentRepository(),
            addresses=InMemoryKycAddressRepository(),
            screenings=InMemoryKycScreeningRepository(),
            reviews=InMemoryKycReviewRepository(),
            workflows=InMemoryKycWorkflowRepository(),
            biometrics=InMemoryKycBiometricRepository(),
            audits=InMemoryKycAuditRepository(),
            customers=_customer_repo,
            policy=get_policy_evaluator(),
        )
    if not _kyc_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _kyc_service.handle_tenant_provisioned,
        )
        _kyc_registered = True
    return _kyc_service


def get_banking_deposit_management_service() -> BankingDepositManagementApplicationService:
    global _deposit_service, _deposit_registered
    if _deposit_service is None:
        get_banking_customer_account_service()
        _ensure_deposit_loan_repos()
        _deposit_service = BankingDepositManagementApplicationService(
            deposits=_deposit_repo,
            transactions=_deposit_tx_repo,
            accruals=_deposit_accrual_repo,
            certificates=InMemoryDepositCertificateRepository(),
            statements=InMemoryDepositStatementRepository(),
            workflows=InMemoryDepositWorkflowRepository(),
            audits=InMemoryDepositAuditRepository(),
            profit_rules=_profit_rule_repo,
            accounts=_account_repo,
            kernel=get_financial_kernel(),
            policy=get_policy_evaluator(),
        )
    if not _deposit_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _deposit_service.handle_tenant_provisioned,
        )
        _deposit_registered = True
    return _deposit_service


def get_banking_loan_management_service() -> BankingLoanManagementApplicationService:
    global _loan_service, _loan_registered
    if _loan_service is None:
        get_banking_customer_account_service()
        _ensure_deposit_loan_repos()
        _loan_service = BankingLoanManagementApplicationService(
            loans=_loan_repo,
            collaterals=_loan_collateral_repo,
            guarantors=_loan_guarantor_repo,
            installments=_loan_installment_repo,
            transactions=_loan_tx_repo,
            risk_analyses=_loan_credit_risk_repo,
            workflows=InMemoryLoanWorkflowRepository(),
            audits=InMemoryLoanAuditRepository(),
            accounts=_account_repo,
            customers=_customer_repo,
            kernel=get_financial_kernel(),
            policy=get_policy_evaluator(),
        )
    if not _loan_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _loan_service.handle_tenant_provisioned,
        )
        _loan_registered = True
    return _loan_service


def get_banking_interest_calculation_service() -> BankingInterestCalculationApplicationService:
    global _interest_service, _interest_registered
    if _interest_service is None:
        _interest_service = BankingInterestCalculationApplicationService(
            profiles=InMemoryInterestRateProfileRepository(),
            rate_changes=InMemoryInterestRateChangeRepository(),
            audits=InMemoryInterestCalculationAuditRepository(),
            policy=get_policy_evaluator(),
        )
    if not _interest_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _interest_service.handle_tenant_provisioned,
        )
        _interest_registered = True
    return _interest_service


def get_banking_payment_platform_service() -> BankingPaymentPlatformApplicationService:
    global _payment_service, _payment_registered
    if _payment_service is None:
        get_banking_customer_account_service()
        _payment_service = BankingPaymentPlatformApplicationService(
            beneficiaries=InMemoryPaymentBeneficiaryRepository(),
            transfers=_transfer_repo,
            batches=InMemoryPaymentBatchRepository(),
            standing_orders=InMemoryStandingOrderRepository(),
            workflows=InMemoryPaymentWorkflowRepository(),
            fraud_checks=InMemoryPaymentFraudRepository(),
            audits=InMemoryPaymentAuditRepository(),
            accounts=_account_repo,
            kernel=get_financial_kernel(),
            policy=get_policy_evaluator(),
        )
    if not _payment_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _payment_service.handle_tenant_provisioned,
        )
        _payment_registered = True
    return _payment_service


def get_banking_settlement_engine_service() -> BankingSettlementEngineApplicationService:
    global _settlement_service, _settlement_registered
    if _settlement_service is None:
        get_banking_payment_platform_service()
        _settlement_service = BankingSettlementEngineApplicationService(
            batches=InMemorySettlementBatchRepository(),
            items=InMemorySettlementItemRepository(),
            reconciliations=InMemoryReconciliationRunRepository(),
            matches=InMemoryReconciliationMatchRepository(),
            exceptions=InMemorySettlementExceptionRepository(),
            differences=InMemorySettlementDifferenceRepository(),
            adjustments=InMemorySettlementAdjustmentRepository(),
            audits=InMemorySettlementAuditRepository(),
            reports=InMemorySettlementReportRepository(),
            transfers=_transfer_repo,
            kernel=get_financial_kernel(),
            policy=get_policy_evaluator(),
        )
    if not _settlement_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _settlement_service.handle_tenant_provisioned,
        )
        _settlement_registered = True
    return _settlement_service


def get_banking_branch_platform_service() -> BankingBranchPlatformApplicationService:
    global _branch_service, _branch_registered
    if _branch_service is None:
        _branch_service = BankingBranchPlatformApplicationService(
            offices=InMemoryBranchOfficeRepository(),
            extensions=InMemoryBranchExtensionRepository(),
            sessions=InMemoryBranchDaySessionRepository(),
            vaults=InMemoryBranchVaultRepository(),
            vault_movements=InMemoryBranchVaultMovementRepository(),
            cash_limits=InMemoryBranchCashLimitRepository(),
            assignments=InMemoryBranchEmployeeAssignmentRepository(),
            kpis=InMemoryBranchKPIRepository(),
            audits=InMemoryBranchAuditRepository(),
            policy=get_policy_evaluator(),
        )
    if not _branch_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _branch_service.handle_tenant_provisioned,
        )
        _branch_registered = True
    return _branch_service


def get_banking_security_platform_service() -> BankingSecurityPlatformApplicationService:
    global _security_service, _security_registered
    if _security_service is None:
        _security_service = BankingSecurityPlatformApplicationService(
            approvals=InMemorySecurityApprovalRepository(),
            devices=InMemorySecurityDeviceRepository(),
            sessions=InMemorySecuritySessionRepository(),
            alerts=InMemoryTransactionMonitorRepository(),
            freezes=InMemoryEmergencyFreezeRepository(),
            audits=InMemorySecurityAuditRepository(),
            limit_usage=InMemoryLimitUsageRepository(),
            policy=get_policy_evaluator(),
        )
    if not _security_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _security_service.handle_tenant_provisioned,
        )
        _security_registered = True
    return _security_service


def get_banking_analytics_platform_service() -> BankingAnalyticsPlatformApplicationService:
    global _analytics_service, _analytics_registered
    if _analytics_service is None:
        get_banking_customer_account_service()
        _ensure_deposit_loan_repos()
        _analytics_service = BankingAnalyticsPlatformApplicationService(
            jobs=InMemoryBankingAnalyticsJobRepository(),
            customers=_customer_repo,
            accounts=_account_repo,
            deposits=_deposit_repo,
            deposit_transactions=_deposit_tx_repo,
            interest_accruals=_deposit_accrual_repo,
            loans=_loan_repo,
            installments=_loan_installment_repo,
            loan_transactions=_loan_tx_repo,
            credit_risks=_loan_credit_risk_repo,
            transfers=_transfer_repo,
            fraud_checks=InMemoryPaymentFraudRepository(),
            branch_offices=InMemoryBranchOfficeRepository(),
            branch_kpis=InMemoryBranchKPIRepository(),
            security_alerts=InMemoryTransactionMonitorRepository(),
            policy=get_policy_evaluator(),
        )
    if not _analytics_registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _analytics_service.handle_tenant_provisioned,
        )
        _analytics_registered = True
    return _analytics_service


def reset_banking_customer_account_service() -> None:
    global _service, _kyc_service, _deposit_service, _loan_service, _interest_service, _payment_service, _settlement_service, _branch_service, _security_service, _analytics_service
    global _registered, _kyc_registered, _deposit_registered, _loan_registered, _interest_registered, _payment_registered, _settlement_registered, _branch_registered, _security_registered, _analytics_registered
    global _customer_repo, _account_repo, _product_repo, _transfer_repo
    global _deposit_repo, _deposit_tx_repo, _deposit_accrual_repo, _profit_rule_repo
    global _loan_repo, _loan_tx_repo, _loan_installment_repo
    global _loan_collateral_repo, _loan_guarantor_repo, _loan_credit_risk_repo
    _service = None
    _kyc_service = None
    _deposit_service = None
    _loan_service = None
    _interest_service = None
    _payment_service = None
    _settlement_service = None
    _branch_service = None
    _security_service = None
    _analytics_service = None
    _registered = False
    _kyc_registered = False
    _deposit_registered = False
    _loan_registered = False
    _interest_registered = False
    _payment_registered = False
    _settlement_registered = False
    _branch_registered = False
    _security_registered = False
    _analytics_registered = False
    _customer_repo = None
    _account_repo = None
    _product_repo = None
    _transfer_repo = None
    _deposit_repo = None
    _deposit_tx_repo = None
    _deposit_accrual_repo = None
    _profit_rule_repo = None
    _loan_repo = None
    _loan_tx_repo = None
    _loan_installment_repo = None
    _loan_collateral_repo = None
    _loan_guarantor_repo = None
    _loan_credit_risk_repo = None
    InMemoryCustomerRepository.reset()
    InMemoryKycRepository.reset()
    InMemoryAccountProductRepository.reset()
    InMemoryAccountRepository.reset()
    InMemoryAccountAuditRepository.reset()
    PostgresAccountRepository.reset_counters()
    PostgresPaymentTransferRepository.reset_counters()
    PostgresDepositTransactionRepository.reset_counters()
    PostgresDepositAccrualRepository.reset_counters()
    PostgresLoanProfileRepository.reset_counters()
    PostgresLoanTransactionRepository.reset_counters()
    InMemoryPaymentTransferRepository.reset()
    InMemoryKycCaseRepository.reset()
    InMemoryKycDocumentRepository.reset()
    InMemoryKycAddressRepository.reset()
    InMemoryKycScreeningRepository.reset()
    InMemoryKycReviewRepository.reset()
    InMemoryKycWorkflowRepository.reset()
    InMemoryKycBiometricRepository.reset()
    InMemoryKycAuditRepository.reset()
    InMemoryDepositProfileRepository.reset()
    InMemoryDepositTransactionRepository.reset()
    InMemoryDepositAccrualRepository.reset()
    InMemoryDepositCertificateRepository.reset()
    InMemoryDepositStatementRepository.reset()
    InMemoryDepositWorkflowRepository.reset()
    InMemoryDepositAuditRepository.reset()
    InMemoryProfitRuleRepository.reset()
    InMemoryLoanProfileRepository.reset()
    InMemoryLoanCollateralRepository.reset()
    InMemoryLoanGuarantorRepository.reset()
    InMemoryLoanInstallmentRepository.reset()
    InMemoryLoanTransactionRepository.reset()
    InMemoryLoanCreditRiskRepository.reset()
    InMemoryLoanWorkflowRepository.reset()
    InMemoryLoanAuditRepository.reset()
    InMemoryInterestRateProfileRepository.reset()
    InMemoryInterestRateChangeRepository.reset()
    InMemoryInterestCalculationAuditRepository.reset()
    InMemoryPaymentBeneficiaryRepository.reset()
    InMemoryPaymentTransferRepository.reset()
    InMemoryPaymentBatchRepository.reset()
    InMemoryStandingOrderRepository.reset()
    InMemoryPaymentWorkflowRepository.reset()
    InMemoryPaymentFraudRepository.reset()
    InMemoryPaymentAuditRepository.reset()
    InMemorySettlementBatchRepository.reset()
    InMemorySettlementItemRepository.reset()
    InMemoryReconciliationRunRepository.reset()
    InMemoryReconciliationMatchRepository.reset()
    InMemorySettlementExceptionRepository.reset()
    InMemorySettlementDifferenceRepository.reset()
    InMemorySettlementAdjustmentRepository.reset()
    InMemorySettlementAuditRepository.reset()
    InMemorySettlementReportRepository.reset()
    InMemoryBranchOfficeRepository.reset()
    InMemoryBranchExtensionRepository.reset()
    InMemoryBranchDaySessionRepository.reset()
    InMemoryBranchVaultRepository.reset()
    InMemoryBranchVaultMovementRepository.reset()
    InMemoryBranchCashLimitRepository.reset()
    InMemoryBranchEmployeeAssignmentRepository.reset()
    InMemoryBranchKPIRepository.reset()
    InMemoryBranchAuditRepository.reset()
    InMemorySecurityApprovalRepository.reset()
    InMemorySecurityDeviceRepository.reset()
    InMemorySecuritySessionRepository.reset()
    InMemoryTransactionMonitorRepository.reset()
    InMemoryEmergencyFreezeRepository.reset()
    InMemorySecurityAuditRepository.reset()
    InMemoryLimitUsageRepository.reset()
    InMemoryBankingAnalyticsJobRepository.reset()
