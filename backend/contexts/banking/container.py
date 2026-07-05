"""Banking DI — Customer Account + KYC Platform + Deposit Management + Loan Platform."""
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

_customer_repo = InMemoryCustomerRepository()
_account_repo = InMemoryAccountRepository()

_service: BankingCustomerAccountApplicationService | None = None
_kyc_service: BankingKycPlatformApplicationService | None = None
_deposit_service: BankingDepositManagementApplicationService | None = None
_loan_service: BankingLoanManagementApplicationService | None = None
_registered = False
_kyc_registered = False
_deposit_registered = False
_loan_registered = False


def get_banking_customer_account_service() -> BankingCustomerAccountApplicationService:
    global _service, _registered
    if _service is None:
        _service = BankingCustomerAccountApplicationService(
            customers=_customer_repo,
            kyc_records=InMemoryKycRepository(),
            products=InMemoryAccountProductRepository(),
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
        _deposit_service = BankingDepositManagementApplicationService(
            deposits=InMemoryDepositProfileRepository(),
            transactions=InMemoryDepositTransactionRepository(),
            accruals=InMemoryDepositAccrualRepository(),
            certificates=InMemoryDepositCertificateRepository(),
            statements=InMemoryDepositStatementRepository(),
            workflows=InMemoryDepositWorkflowRepository(),
            audits=InMemoryDepositAuditRepository(),
            profit_rules=InMemoryProfitRuleRepository(),
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
        _loan_service = BankingLoanManagementApplicationService(
            loans=InMemoryLoanProfileRepository(),
            collaterals=InMemoryLoanCollateralRepository(),
            guarantors=InMemoryLoanGuarantorRepository(),
            installments=InMemoryLoanInstallmentRepository(),
            transactions=InMemoryLoanTransactionRepository(),
            risk_analyses=InMemoryLoanCreditRiskRepository(),
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


def reset_banking_customer_account_service() -> None:
    global _service, _kyc_service, _deposit_service, _loan_service
    global _registered, _kyc_registered, _deposit_registered, _loan_registered
    _service = None
    _kyc_service = None
    _deposit_service = None
    _loan_service = None
    _registered = False
    _kyc_registered = False
    _deposit_registered = False
    _loan_registered = False
    InMemoryCustomerRepository.reset()
    InMemoryKycRepository.reset()
    InMemoryAccountProductRepository.reset()
    InMemoryAccountRepository.reset()
    InMemoryAccountAuditRepository.reset()
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
