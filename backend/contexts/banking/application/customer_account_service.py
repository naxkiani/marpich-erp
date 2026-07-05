"""Banking Customer and Account application service."""
from __future__ import annotations

from contexts.banking.domain.aggregates.customer_account_engine import (
    AccountStatus,
    AccountType,
    ApprovalStatus,
    BankingAccount,
    BankingAccountAudit,
    BankingAccountProduct,
    BankingCustomer,
    BankingCustomerKYC,
    CustomerType,
    DEFAULT_GL_MAP,
    KycStatus,
    RiskRating,
)
from contexts.banking.domain.events.integration_events import (
    BankingAccountOpenedIntegration,
    BankingAccountStatusChangedIntegration,
    BankingCustomerCreatedIntegration,
    BankingKycVerifiedIntegration,
)
from contexts.banking.domain.ports.customer_account_repositories import (
    IAccountAuditRepository,
    IAccountProductRepository,
    IAccountRepository,
    ICustomerRepository,
    IKycRepository,
)
from contexts.banking.domain.services.customer_account_engine import (
    build_customer_account_dashboard,
    check_minimum_balance,
    check_overdraft,
    list_account_status_workflow,
    list_customer_account_catalog,
    requires_approval_for_customer,
)
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingCustomerAccountApplicationService:
    def __init__(
        self,
        customers: ICustomerRepository,
        kyc_records: IKycRepository,
        products: IAccountProductRepository,
        accounts: IAccountRepository,
        audits: IAccountAuditRepository,
        kernel: IFinancialKernel,
        policy: IPolicyEvaluator,
    ) -> None:
        self._customers = customers
        self._kyc = kyc_records
        self._products = products
        self._accounts = accounts
        self._audits = audits
        self._kernel = kernel
        self._policy = policy

    async def _audit(
        self,
        *,
        tenant_id: str,
        account_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> None:
        entry = BankingAccountAudit.create(
            tenant_id=tenant_id,
            account_id=account_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )
        await self._audits.save(entry)

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_customer_account_catalog())

    async def list_status_workflow(self) -> Result[list[dict]]:
        return Result.ok(list_account_status_workflow())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        customers = await self._customers.list_by_tenant(tenant_id)
        accounts = await self._accounts.list_by_tenant(tenant_id)
        products = await self._products.list_by_tenant(tenant_id)
        return Result.ok(
            build_customer_account_dashboard(
                customers=[c.to_dict() for c in customers],
                accounts=[a.to_dict() for a in accounts],
                products=[p.to_dict() for p in products],
            )
        )

    async def create_customer(
        self,
        *,
        tenant_id: str,
        customer_type: str,
        display_name: str,
        legal_name: str,
        email: str,
        phone: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        registration_number: str | None = None,
        tax_id: str | None = None,
        risk_rating: str = RiskRating.LOW.value,
        auto_submit: bool = False,
    ) -> Result[dict]:
        try:
            CustomerType(customer_type)
            RiskRating(risk_rating)
        except ValueError:
            return Result.fail("banking.errors.invalid_customer_type_or_risk")

        existing = await self._customers.find_by_email(tenant_id, email)
        if existing:
            return Result.fail("banking.errors.customer_email_exists")

        customer = BankingCustomer.create(
            tenant_id=tenant_id,
            customer_type=customer_type,
            display_name=display_name,
            legal_name=legal_name,
            email=email,
            phone=phone,
            organization_id=organization_id,
            branch_id=branch_id,
            registration_number=registration_number,
            tax_id=tax_id,
        )
        customer.update_risk_rating(risk_rating)
        if auto_submit or requires_approval_for_customer(
            risk_rating=risk_rating, customer_type=customer_type
        ):
            customer.submit_for_approval()
        await self._customers.save(customer)

        await publish_integration_event(
            BankingCustomerCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"customer-{customer.id}",
                customer_id=str(customer.id),
                customer_type=customer.customer_type,
                display_name=customer.display_name,
                kyc_status=customer.kyc_status,
                risk_rating=customer.risk_rating,
            )
        )
        return Result.ok(customer.to_dict())

    async def list_customers(self, tenant_id: str) -> Result[list[dict]]:
        customers = await self._customers.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in customers])

    async def get_customer(self, customer_id: str) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer:
            return Result.fail("banking.errors.customer_not_found")
        return Result.ok(customer.to_dict())

    async def submit_customer_approval(self, customer_id: str) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer:
            return Result.fail("banking.errors.customer_not_found")
        try:
            customer.submit_for_approval()
        except ValueError:
            return Result.fail("banking.errors.cannot_submit_customer")
        await self._customers.save(customer)
        return Result.ok(customer.to_dict())

    async def approve_customer(self, customer_id: str) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer:
            return Result.fail("banking.errors.customer_not_found")
        try:
            customer.approve()
        except ValueError:
            return Result.fail("banking.errors.not_pending_customer_approval")
        await self._customers.save(customer)
        return Result.ok(customer.to_dict())

    async def reject_customer(self, customer_id: str) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer:
            return Result.fail("banking.errors.customer_not_found")
        try:
            customer.reject()
        except ValueError:
            return Result.fail("banking.errors.not_pending_customer_approval")
        await self._customers.save(customer)
        return Result.ok(customer.to_dict())

    async def update_customer_kyc_status(self, customer_id: str, status: str) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer:
            return Result.fail("banking.errors.customer_not_found")
        try:
            customer.update_kyc_status(status)
        except ValueError:
            return Result.fail("banking.errors.invalid_kyc_status")
        await self._customers.save(customer)
        return Result.ok(customer.to_dict())

    async def update_customer_risk_rating(self, customer_id: str, rating: str) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer:
            return Result.fail("banking.errors.customer_not_found")
        try:
            customer.update_risk_rating(rating)
        except ValueError:
            return Result.fail("banking.errors.invalid_risk_rating")
        await self._customers.save(customer)
        return Result.ok(customer.to_dict())

    async def create_kyc(
        self,
        *,
        tenant_id: str,
        customer_id: str,
        tier: str,
        document_type: str,
        document_ref: str,
        notes: str = "",
    ) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer or customer.tenant_id != tenant_id:
            return Result.fail("banking.errors.customer_not_found")

        kyc = BankingCustomerKYC.create(
            tenant_id=tenant_id,
            customer_id=customer_id,
            tier=tier,
            document_type=document_type,
            document_ref=document_ref,
            notes=notes,
        )
        await self._kyc.save(kyc)
        customer.update_kyc_status(KycStatus.IN_REVIEW.value)
        await self._customers.save(customer)
        return Result.ok(kyc.to_dict())

    async def verify_kyc(self, *, kyc_id: str, verified_by: str) -> Result[dict]:
        kyc = await self._kyc.find_by_id(kyc_id)
        if not kyc:
            return Result.fail("banking.errors.kyc_not_found")

        kyc.verify(verified_by=verified_by)
        await self._kyc.save(kyc)

        customer = await self._customers.find_by_id(kyc.customer_id)
        if customer:
            customer.update_kyc_status(KycStatus.VERIFIED.value)
            await self._customers.save(customer)

        await publish_integration_event(
            BankingKycVerifiedIntegration(
                tenant_id=TenantId.create(kyc.tenant_id),
                correlation_id=f"kyc-{kyc.id}",
                customer_id=kyc.customer_id,
                kyc_id=str(kyc.id),
                tier=kyc.tier,
            )
        )
        return Result.ok(kyc.to_dict())

    async def list_kyc(self, customer_id: str) -> Result[list[dict]]:
        records = await self._kyc.list_by_customer(customer_id)
        return Result.ok([k.to_dict() for k in records])

    async def create_product(
        self,
        *,
        tenant_id: str,
        product_code: str,
        name: str,
        account_type: str,
        currency: str = "USD",
        interest_rate_annual: float = 0.0,
        minimum_balance: float = 0.0,
        overdraft_limit: float = 0.0,
        overdraft_enabled: bool = False,
    ) -> Result[dict]:
        try:
            AccountType(account_type)
        except ValueError:
            return Result.fail("banking.errors.invalid_account_type")

        existing = await self._products.find_by_code(tenant_id, product_code)
        if existing:
            return Result.fail("banking.errors.product_code_exists")

        product = BankingAccountProduct.create(
            tenant_id=tenant_id,
            product_code=product_code,
            name=name,
            account_type=account_type,
            currency=currency,
            interest_rate_annual=interest_rate_annual,
            minimum_balance=minimum_balance,
            overdraft_limit=overdraft_limit,
            overdraft_enabled=overdraft_enabled,
        )
        await self._products.save(product)
        return Result.ok(product.to_dict())

    async def list_products(self, tenant_id: str) -> Result[list[dict]]:
        products = await self._products.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in products])

    async def open_account(
        self,
        *,
        tenant_id: str,
        customer_id: str,
        product_code: str,
        organization_id: str | None = None,
        branch_id: str | None = None,
        is_joint: bool = False,
        joint_holders: list[str] | None = None,
        opening_balance: float = 0.0,
        currency: str | None = None,
    ) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer or customer.tenant_id != tenant_id:
            return Result.fail("banking.errors.customer_not_found")

        if customer.kyc_status != KycStatus.VERIFIED.value:
            return Result.fail("banking.errors.kyc_not_verified")

        if customer.approval_status != ApprovalStatus.APPROVED.value:
            return Result.fail("banking.errors.customer_not_approved")

        product = await self._products.find_by_code(tenant_id, product_code)
        if not product or not product.is_active:
            return Result.fail("banking.errors.product_not_found")

        acct_currency = (currency or product.currency).upper()
        requires_approval = (
            requires_approval_for_customer(
                risk_rating=customer.risk_rating,
                customer_type=customer.customer_type,
            )
            or product.account_type == AccountType.LOAN.value
            or opening_balance >= 10000
        )

        account_number = self._accounts.next_account_number(tenant_id)

        gl_account_code = await self._resolve_gl_code(tenant_id, product.account_type)

        account = BankingAccount.create(
            tenant_id=tenant_id,
            customer_id=customer_id,
            account_number=account_number,
            account_type=product.account_type,
            product_code=product.product_code,
            currency=acct_currency,
            organization_id=organization_id or customer.organization_id,
            branch_id=branch_id or customer.branch_id,
            is_joint=is_joint or product.account_type == AccountType.JOINT.value,
            joint_holders=joint_holders,
            interest_rate_annual=product.interest_rate_annual,
            minimum_balance=product.minimum_balance,
            overdraft_limit=product.overdraft_limit,
            overdraft_enabled=product.overdraft_enabled,
            gl_account_code=gl_account_code,
            opening_balance=opening_balance,
            requires_approval=requires_approval,
        )
        await self._accounts.save(account)
        await self._audit(
            tenant_id=tenant_id,
            account_id=str(account.id),
            action="account.opened",
            detail=f"status={account.status}",
        )

        if not requires_approval:
            link_result = await self._link_and_activate_account(account, actor_id=None)
            if not link_result.succeeded:
                return Result.fail(link_result.error or "banking.errors.kernel_link_failed")
            account = link_result.unwrap()

        return Result.ok(account.to_dict())

    async def list_accounts(self, tenant_id: str) -> Result[list[dict]]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in accounts])

    async def get_account(self, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")
        return Result.ok(account.to_dict())

    async def approve_account(
        self, *, account_id: str, actor_id: str | None = None
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")

        if account.approval_status == ApprovalStatus.APPROVED.value and account.kernel_linked:
            return Result.ok(account.to_dict())

        result = await self._link_and_activate_account(account, actor_id=actor_id)
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def _link_and_activate_account(
        self, account: BankingAccount, *, actor_id: str | None
    ) -> Result[BankingAccount]:
        kernel_key = account.kernel_account_key or "customer_deposits"
        gl_code = await self._resolve_gl_code(account.tenant_id, account.account_type, kernel_key)
        if not gl_code:
            return Result.fail("banking.errors.kernel_gl_account_not_found")

        if account.approval_status == ApprovalStatus.PENDING.value:
            try:
                account.approve_opening()
            except ValueError:
                return Result.fail("banking.errors.not_pending_account_approval")

        journal_id: str | None = None
        if account.balance > 0:
            try:
                post_result = await self._kernel.execute_posting(
                    tenant_id=account.tenant_id,
                    rule_id="bank_deposit",
                    source_context="banking",
                    source_document_id=str(account.id),
                    amount=account.balance,
                    currency=account.currency,
                    correlation_id=f"banking-account-{account.id}",
                    idempotency_key=f"posting:bank_deposit:open:{account.id}",
                    description=f"Opening balance — account {account.account_number}",
                    account_mappings={"debit": gl_code},
                )
                journal_id = post_result.journal_id
            except ValueError:
                pass

        account.link_kernel(
            gl_account_code=gl_code,
            journal_id=journal_id,
            subledger_ref=f"banking:{account.id}",
        )
        await self._accounts.save(account)
        await self._audit(
            tenant_id=account.tenant_id,
            account_id=str(account.id),
            action="account.approved",
            actor_id=actor_id,
            detail=f"kernel_linked=true gl={gl_code}",
        )

        await publish_integration_event(
            BankingAccountOpenedIntegration(
                tenant_id=TenantId.create(account.tenant_id),
                correlation_id=f"account-{account.id}",
                account_id=str(account.id),
                customer_id=account.customer_id,
                account_type=account.account_type,
                account_number=account.account_number,
                currency=account.currency,
                gl_account_code=gl_code,
                kernel_linked=True,
            )
        )
        return Result.ok(account)

    async def reject_account(self, account_id: str, *, actor_id: str | None = None) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")
        try:
            account.reject_opening()
        except ValueError:
            return Result.fail("banking.errors.not_pending_account_approval")
        await self._accounts.save(account)
        await self._audit(
            tenant_id=account.tenant_id,
            account_id=str(account.id),
            action="account.rejected",
            actor_id=actor_id,
        )
        return Result.ok(account.to_dict())

    async def transition_account_status(
        self,
        *,
        account_id: str,
        new_status: str,
        actor_id: str | None = None,
        reason: str = "",
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")
        if not account.kernel_linked and new_status == AccountStatus.ACTIVE.value:
            return Result.fail("banking.errors.account_not_kernel_linked")

        previous = account.status
        try:
            account.transition_status(new_status)
        except ValueError:
            return Result.fail("banking.errors.invalid_status_transition")

        await self._accounts.save(account)
        await self._audit(
            tenant_id=account.tenant_id,
            account_id=str(account.id),
            action=f"status.{new_status}",
            actor_id=actor_id,
            detail=reason,
        )
        await publish_integration_event(
            BankingAccountStatusChangedIntegration(
                tenant_id=TenantId.create(account.tenant_id),
                correlation_id=f"account-status-{account.id}",
                account_id=str(account.id),
                previous_status=previous,
                new_status=new_status,
                actor_id=actor_id,
            )
        )
        return Result.ok(account.to_dict())

    async def evaluate_minimum_balance(self, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")

        local = check_minimum_balance(balance=account.balance, minimum_balance=account.minimum_balance)
        policy = await self._policy.evaluate(
            tenant_id=account.tenant_id,
            domain="banking",
            policy_key="retail.account.minimum_balance",
            facts={
                "balance": account.balance,
                "minimum_balance": account.minimum_balance,
                "account_type": account.account_type,
                "currency": account.currency,
            },
            organization_id=account.organization_id,
        )
        return Result.ok({**local, "policy": policy.to_dict()})

    async def evaluate_overdraft(self, account_id: str, amount: float) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")

        local = check_overdraft(
            balance=account.balance,
            amount=amount,
            overdraft_enabled=account.overdraft_enabled,
            overdraft_limit=account.overdraft_limit,
        )
        policy = await self._policy.evaluate(
            tenant_id=account.tenant_id,
            domain="banking",
            policy_key="retail.overdraft.limit",
            facts={
                "balance": account.balance,
                "amount": amount,
                "overdraft_limit": account.overdraft_limit,
                "overdraft_enabled": account.overdraft_enabled,
                "account_type": account.account_type,
            },
            organization_id=account.organization_id,
        )
        return Result.ok({**local, "policy": policy.to_dict()})

    async def get_account_audit_trail(self, account_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_account(account_id)
        return Result.ok([e.to_dict() for e in entries])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._products.list_by_tenant(tenant_id):
            return

        defaults: list[dict] = [
            {
                "product_code": "SAV-STD",
                "name": "Standard Savings",
                "account_type": AccountType.SAVINGS.value,
                "currency": "USD",
                "interest_rate_annual": 2.5,
                "minimum_balance": 100.0,
            },
            {
                "product_code": "CUR-STD",
                "name": "Standard Current",
                "account_type": AccountType.CURRENT.value,
                "currency": "USD",
                "minimum_balance": 500.0,
                "overdraft_limit": 1000.0,
                "overdraft_enabled": True,
            },
            {
                "product_code": "FD-12M",
                "name": "Fixed Deposit 12M",
                "account_type": AccountType.FIXED_DEPOSIT.value,
                "currency": "USD",
                "interest_rate_annual": 5.0,
                "minimum_balance": 1000.0,
            },
            {
                "product_code": "LOAN-PER",
                "name": "Personal Loan",
                "account_type": AccountType.LOAN.value,
                "currency": "USD",
                "interest_rate_annual": 8.0,
            },
            {
                "product_code": "VIRT-POOL",
                "name": "Virtual Collection",
                "account_type": AccountType.VIRTUAL.value,
                "currency": "USD",
            },
            {
                "product_code": "JOINT-STD",
                "name": "Joint Savings",
                "account_type": AccountType.JOINT.value,
                "currency": "USD",
                "interest_rate_annual": 2.0,
                "minimum_balance": 100.0,
            },
        ]
        for spec in defaults:
            product = BankingAccountProduct.create(tenant_id=tenant_id, **spec)
            await self._products.save(product)

    async def _resolve_gl_code(
        self, tenant_id: str, account_type: str, kernel_key: str | None = None
    ) -> str | None:
        key = kernel_key or DEFAULT_GL_MAP.get(account_type, "customer_deposits")
        accounts = await self._kernel.list_accounts(tenant_id=tenant_id)
        for acct in accounts:
            if acct.get("account_key") == key:
                return acct.get("code") or acct.get("account_code")
        for acct in accounts:
            code = acct.get("code") or acct.get("account_code", "")
            if key.replace("_", "") in code.lower().replace("_", ""):
                return code
        return None
