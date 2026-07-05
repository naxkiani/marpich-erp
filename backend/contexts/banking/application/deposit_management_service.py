"""Deposit Management application service."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.deposit_management_engine import (
    DepositAuditEntry,
    DepositCertificate,
    DepositInterestAccrual,
    DepositProfile,
    DepositStatement,
    DepositStatus,
    DepositTransaction,
    DepositType,
    DepositWorkflowRequest,
    ProfitDistributionRule,
    TransactionStatus,
    TransactionType,
)
from contexts.banking.domain.events.deposit_integration_events import (
    BankingDepositMaturedIntegration,
    BankingDepositPostedIntegration,
    BankingInterestAccruedIntegration,
    BankingWithdrawalPostedIntegration,
)
from contexts.banking.domain.ports.customer_account_repositories import IAccountRepository
from contexts.banking.domain.ports.deposit_management_repositories import (
    IDepositAccrualRepository,
    IDepositAuditRepository,
    IDepositCertificateRepository,
    IDepositProfileRepository,
    IDepositStatementRepository,
    IDepositTransactionRepository,
    IDepositWorkflowRepository,
    IProfitRuleRepository,
)
from contexts.banking.domain.services.deposit_management_engine import (
    build_deposit_dashboard,
    build_statement_lines,
    calculate_daily_interest,
    calculate_early_withdrawal_penalty,
    list_deposit_catalog,
    list_deposit_policy_keys,
    resolve_approval_levels,
)
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingDepositManagementApplicationService:
    def __init__(
        self,
        deposits: IDepositProfileRepository,
        transactions: IDepositTransactionRepository,
        accruals: IDepositAccrualRepository,
        certificates: IDepositCertificateRepository,
        statements: IDepositStatementRepository,
        workflows: IDepositWorkflowRepository,
        audits: IDepositAuditRepository,
        profit_rules: IProfitRuleRepository,
        accounts: IAccountRepository,
        kernel: IFinancialKernel,
        policy: IPolicyEvaluator,
    ) -> None:
        self._deposits = deposits
        self._transactions = transactions
        self._accruals = accruals
        self._certificates = certificates
        self._statements = statements
        self._workflows = workflows
        self._audits = audits
        self._profit_rules = profit_rules
        self._accounts = accounts
        self._kernel = kernel
        self._policy = policy

    async def _audit(
        self, *, tenant_id: str, deposit_id: str, action: str, actor_id: str | None = None, detail: str = ""
    ) -> None:
        await self._audits.save(
            DepositAuditEntry.create(
                tenant_id=tenant_id, deposit_id=deposit_id, action=action, actor_id=actor_id, detail=detail
            )
        )

    async def _resolve_account_key(self, tenant_id: str, account_key: str) -> str | None:
        accounts = await self._kernel.list_accounts(tenant_id=tenant_id)
        for acct in accounts:
            if acct.get("account_key") == account_key:
                return acct.get("code") or acct.get("account_code")
        return None

    async def _resolve_gl_code(self, tenant_id: str) -> str | None:
        accounts = await self._kernel.list_accounts(tenant_id=tenant_id)
        for acct in accounts:
            if acct.get("account_key") == "customer_deposits":
                return acct.get("code") or acct.get("account_code")
        for acct in accounts:
            code = acct.get("code") or acct.get("account_code", "")
            if "deposit" in code.lower():
                return code
        return None

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_deposit_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_deposit_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        deposits = await self._deposits.list_by_tenant(tenant_id)
        transactions = await self._transactions.list_by_tenant(tenant_id)
        accruals = await self._accruals.list_by_tenant(tenant_id)
        certs = await self._certificates.list_by_tenant(tenant_id)
        return Result.ok(
            build_deposit_dashboard(
                deposits=[d.to_dict() for d in deposits],
                transactions=[t.to_dict() for t in transactions],
                accruals=[a.to_dict() for a in accruals],
                certificates=[c.to_dict() for c in certs],
            )
        )

    async def create_profit_rule(
        self,
        *,
        tenant_id: str,
        rule_code: str,
        name: str,
        deposit_type: str,
        method: str = "interest",
        rate_annual: float = 0.0,
        profit_share_pct: float = 0.0,
    ) -> Result[dict]:
        existing = await self._profit_rules.find_by_code(tenant_id, rule_code)
        if existing:
            return Result.fail("banking.errors.profit_rule_exists")
        rule = ProfitDistributionRule.create(
            tenant_id=tenant_id,
            rule_code=rule_code,
            name=name,
            deposit_type=deposit_type,
            method=method,
            rate_annual=rate_annual,
            profit_share_pct=profit_share_pct,
        )
        await self._profit_rules.save(rule)
        return Result.ok(rule.to_dict())

    async def list_profit_rules(self, tenant_id: str) -> Result[list[dict]]:
        rules = await self._profit_rules.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in rules])

    async def open_deposit(
        self,
        *,
        tenant_id: str,
        account_id: str,
        deposit_type: str,
        principal: float = 0.0,
        interest_rate_annual: float | None = None,
        profit_rule_id: str | None = None,
        tenure_months: int | None = None,
        auto_renew: bool = False,
        recurring_amount: float = 0.0,
        recurring_day: int = 1,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("banking.errors.account_not_found")
        if not account.kernel_linked:
            return Result.fail("banking.errors.account_not_kernel_linked")
        if await self._deposits.find_by_account(account_id):
            return Result.fail("banking.errors.deposit_already_exists")

        rate_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="deposit.interest.rate",
            facts={"deposit_type": deposit_type, "principal": principal, "currency": account.currency},
        )
        rate = interest_rate_annual
        if rate is None:
            rate = float(rate_policy.parameters.get("rate_annual", account.interest_rate_annual))

        gl_code = account.gl_account_code or await self._resolve_gl_code(tenant_id)
        requires_approval = principal >= 10000 or deposit_type == DepositType.TERM.value

        deposit = DepositProfile.create(
            tenant_id=tenant_id,
            account_id=account_id,
            customer_id=account.customer_id,
            deposit_type=deposit_type,
            currency=account.currency,
            principal=principal,
            interest_rate_annual=rate,
            profit_rule_id=profit_rule_id,
            tenure_months=tenure_months,
            auto_renew=auto_renew,
            recurring_amount=recurring_amount,
            recurring_day=recurring_day,
            gl_account_code=gl_code,
            requires_approval=requires_approval,
        )
        await self._deposits.save(deposit)
        await self._audit(
            tenant_id=tenant_id,
            deposit_id=str(deposit.id),
            action="deposit.opened",
            detail=f"type={deposit_type}",
        )
        return Result.ok(deposit.to_dict())

    async def approve_deposit(self, *, deposit_id: str, approver_id: str) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit:
            return Result.fail("banking.errors.deposit_not_found")
        try:
            deposit.approve_opening()
        except ValueError:
            return Result.fail("banking.errors.not_pending_deposit_approval")
        await self._deposits.save(deposit)
        await self._audit(
            tenant_id=deposit.tenant_id,
            deposit_id=deposit_id,
            action="deposit.approved",
            actor_id=approver_id,
        )
        return Result.ok(deposit.to_dict())

    async def list_deposits(self, tenant_id: str) -> Result[list[dict]]:
        deposits = await self._deposits.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in deposits])

    async def get_deposit(self, deposit_id: str) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit:
            return Result.fail("banking.errors.deposit_not_found")
        txns = await self._transactions.list_by_deposit(deposit_id)
        accruals = await self._accruals.list_by_deposit(deposit_id)
        certs = await self._certificates.list_by_deposit(deposit_id)
        stmts = await self._statements.list_by_deposit(deposit_id)
        workflows = await self._workflows.list_by_deposit(deposit_id)
        return Result.ok(
            {
                **deposit.to_dict(),
                "transactions": [t.to_dict() for t in txns],
                "accruals": [a.to_dict() for a in accruals],
                "certificates": [c.to_dict() for c in certs],
                "statements": [s.to_dict() for s in stmts],
                "workflows": [w.to_dict() for w in workflows],
            }
        )

    async def create_deposit_transaction(
        self,
        *,
        tenant_id: str,
        deposit_id: str,
        transaction_type: str,
        amount: float,
        actor_id: str | None = None,
    ) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit or deposit.tenant_id != tenant_id:
            return Result.fail("banking.errors.deposit_not_found")
        if deposit.status != DepositStatus.ACTIVE.value:
            return Result.fail("banking.errors.deposit_not_active")

        penalty = 0.0
        if transaction_type == TransactionType.WITHDRAWAL.value:
            if deposit.deposit_type == DepositType.TERM.value:
                penalty_policy = await self._policy.evaluate(
                    tenant_id=tenant_id,
                    domain="bank",
                    policy_key="deposit.early_withdrawal.penalty",
                    facts={
                        "deposit_type": deposit.deposit_type,
                        "amount": amount,
                        "tenure_months": deposit.tenure_months,
                        "days_to_maturity": _days_to_maturity(deposit.maturity_date),
                    },
                )
                penalty_pct = float(penalty_policy.parameters.get("penalty_pct", 1.0))
                penalty = calculate_early_withdrawal_penalty(
                    amount=amount, penalty_pct=penalty_pct, policy_outcome=penalty_policy.outcome
                )

        ref = self._transactions.next_transaction_ref(tenant_id)
        auto_approve = amount < 5000 and transaction_type == TransactionType.DEPOSIT.value
        txn = DepositTransaction.create(
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            account_id=deposit.account_id,
            transaction_ref=ref,
            transaction_type=transaction_type,
            amount=amount,
            currency=deposit.currency,
            penalty_amount=penalty,
            auto_approve=auto_approve,
        )
        await self._transactions.save(txn)

        if not auto_approve:
            levels = resolve_approval_levels(transaction_type=transaction_type, amount=amount)
            approval_policy = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain="bank",
                policy_key="deposit.approval.required_level",
                facts={"transaction_type": transaction_type, "amount": amount},
            )
            levels = int(approval_policy.parameters.get("required_levels", levels))
            workflow = DepositWorkflowRequest.create(
                tenant_id=tenant_id,
                deposit_id=deposit_id,
                transaction_id=str(txn.id),
                request_type=f"{transaction_type}_approval",
                required_levels=levels,
            )
            await self._workflows.save(workflow)

        await self._audit(
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            action=f"transaction.{transaction_type}.created",
            actor_id=actor_id,
            detail=f"ref={ref} amount={amount}",
        )

        if auto_approve:
            return await self.approve_transaction(transaction_id=str(txn.id), approver_id=actor_id or "system")

        return Result.ok(txn.to_dict())

    async def approve_transaction(
        self, *, transaction_id: str, approver_id: str
    ) -> Result[dict]:
        txn = await self._transactions.find_by_id(transaction_id)
        if not txn:
            return Result.fail("banking.errors.deposit_transaction_not_found")

        workflows = await self._workflows.list_by_deposit(txn.deposit_id)
        pending_wf = next(
            (w for w in workflows if w.transaction_id == transaction_id and w.status == "pending"), None
        )
        if pending_wf:
            pending_wf.approve(approver_id=approver_id)
            await self._workflows.save(pending_wf)
            if pending_wf.status != "approved":
                return Result.ok({**txn.to_dict(), "workflow": pending_wf.to_dict()})

        if txn.status == TransactionStatus.PENDING.value:
            try:
                txn.approve(approved_by=approver_id)
            except ValueError:
                return Result.fail("banking.errors.transaction_not_pending")
        elif txn.status != TransactionStatus.APPROVED.value:
            return Result.fail("banking.errors.transaction_not_pending")

        deposit = await self._deposits.find_by_id(txn.deposit_id)
        if not deposit:
            return Result.fail("banking.errors.deposit_not_found")

        account = await self._accounts.find_by_id(txn.account_id)
        if not account:
            return Result.fail("banking.errors.account_not_found")

        journal_id: str | None = None
        try:
            if txn.transaction_type == TransactionType.DEPOSIT.value:
                account.credit(txn.amount)
                deposit.principal = round(deposit.principal + txn.amount, 2)
                journal_id = await self._post_gl(
                    tenant_id=txn.tenant_id,
                    rule_id="bank_deposit",
                    source_document_id=str(txn.id),
                    amount=txn.amount,
                    currency=txn.currency,
                    gl_code=deposit.gl_account_code,
                    idempotency_key=f"posting:bank_deposit:{txn.transaction_ref}",
                    description=f"Deposit {txn.transaction_ref}",
                )
                await publish_integration_event(
                    BankingDepositPostedIntegration(
                        tenant_id=TenantId.create(txn.tenant_id),
                        correlation_id=f"deposit-txn-{txn.id}",
                        account_id=txn.account_id,
                        deposit_id=txn.deposit_id,
                        transaction_id=str(txn.id),
                        transaction_ref=txn.transaction_ref,
                        amount=txn.amount,
                        currency=txn.currency,
                        gl_account_code=deposit.gl_account_code,
                        account_number=account.account_number,
                    )
                )
            elif txn.transaction_type == TransactionType.WITHDRAWAL.value:
                account.debit(txn.net_amount)
                deposit.principal = round(max(0, deposit.principal - txn.net_amount), 2)
                journal_id = await self._post_gl(
                    tenant_id=txn.tenant_id,
                    rule_id="bank_withdrawal",
                    source_document_id=str(txn.id),
                    amount=txn.net_amount,
                    currency=txn.currency,
                    gl_code=deposit.gl_account_code,
                    idempotency_key=f"posting:bank_withdrawal:{txn.transaction_ref}",
                    description=f"Withdrawal {txn.transaction_ref}",
                )
                await publish_integration_event(
                    BankingWithdrawalPostedIntegration(
                        tenant_id=TenantId.create(txn.tenant_id),
                        correlation_id=f"withdrawal-txn-{txn.id}",
                        account_id=txn.account_id,
                        deposit_id=txn.deposit_id,
                        transaction_id=str(txn.id),
                        transaction_ref=txn.transaction_ref,
                        amount=txn.net_amount,
                        currency=txn.currency,
                        gl_account_code=deposit.gl_account_code,
                        penalty_amount=txn.penalty_amount,
                    )
                )
            elif txn.transaction_type == TransactionType.INTEREST_CREDIT.value:
                account.credit(txn.amount)
                deposit.post_interest(txn.amount)
                journal_id = await self._post_gl(
                    tenant_id=txn.tenant_id,
                    rule_id="interest_accrual",
                    source_document_id=str(txn.id),
                    amount=txn.amount,
                    currency=txn.currency,
                    gl_code=deposit.gl_account_code,
                    idempotency_key=f"posting:interest_accrual:{txn.transaction_ref}",
                    description=f"Interest credit {txn.transaction_ref}",
                )
        except ValueError as exc:
            return Result.fail(f"banking.errors.{exc.args[0]}")

        txn.mark_posted(journal_id=journal_id)
        await self._transactions.save(txn)
        await self._accounts.save(account)
        await self._deposits.save(deposit)
        await self._audit(
            tenant_id=txn.tenant_id,
            deposit_id=txn.deposit_id,
            action="transaction.posted",
            actor_id=approver_id,
            detail=txn.transaction_ref,
        )
        return Result.ok(txn.to_dict())

    async def _post_gl(
        self,
        *,
        tenant_id: str,
        rule_id: str,
        source_document_id: str,
        amount: float,
        currency: str,
        gl_code: str | None,
        idempotency_key: str,
        description: str,
    ) -> str | None:
        mappings: dict[str, str] = {}
        if rule_id == "bank_deposit":
            debit_code = await self._resolve_account_key(tenant_id, "cash_reserves")
            credit_code = gl_code or await self._resolve_account_key(tenant_id, "customer_deposits")
            if debit_code and credit_code:
                mappings = {"debit": debit_code, "credit": credit_code}
        elif rule_id == "bank_withdrawal":
            debit_code = await self._resolve_account_key(tenant_id, "cash_reserves")
            credit_code = gl_code or await self._resolve_account_key(tenant_id, "customer_deposits")
            if debit_code and credit_code:
                mappings = {"debit": debit_code, "credit": credit_code}
        elif rule_id == "interest_accrual":
            debit_code = await self._resolve_account_key(tenant_id, "interest_expense")
            credit_code = await self._resolve_account_key(tenant_id, "interest_income")
            if debit_code and credit_code:
                mappings = {"debit": debit_code, "credit": credit_code}
        elif gl_code:
            if rule_id == "bank_deposit":
                mappings = {"debit": gl_code}
            elif rule_id == "bank_withdrawal":
                mappings = {"credit": gl_code}
            elif rule_id == "interest_accrual":
                mappings = {"credit": gl_code}
        try:
            result = await self._kernel.execute_posting(
                tenant_id=tenant_id,
                rule_id=rule_id,
                source_context="banking",
                source_document_id=source_document_id,
                amount=amount,
                currency=currency,
                correlation_id=idempotency_key,
                idempotency_key=idempotency_key,
                description=description,
                account_mappings=mappings or None,
            )
            return result.journal_id
        except ValueError:
            return None

    async def accrue_interest(
        self, *, tenant_id: str, deposit_id: str, days: int = 1
    ) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit or deposit.tenant_id != tenant_id:
            return Result.fail("banking.errors.deposit_not_found")
        if deposit.status != DepositStatus.ACTIVE.value:
            return Result.fail("banking.errors.deposit_not_active")

        amount = calculate_daily_interest(
            principal=deposit.principal, rate_annual=deposit.interest_rate_annual, days=days
        )
        if amount <= 0:
            return Result.fail("banking.errors.no_interest_to_accrue")

        ref = self._accruals.next_accrual_ref(tenant_id)
        now = datetime.now(UTC)
        accrual = DepositInterestAccrual.create(
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            accrual_ref=ref,
            period_start=now - timedelta(days=days),
            period_end=now,
            principal_base=deposit.principal,
            rate_annual=deposit.interest_rate_annual,
            accrued_amount=amount,
        )
        deposit.add_accrual(amount)
        await self._accruals.save(accrual)
        await self._deposits.save(deposit)

        await publish_integration_event(
            BankingInterestAccruedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"interest-accrual-{accrual.id}",
                deposit_id=deposit_id,
                accrual_id=str(accrual.id),
                accrual_ref=ref,
                accrued_amount=amount,
                currency=deposit.currency,
                gl_account_code=deposit.gl_account_code,
            )
        )
        await self._audit(
            tenant_id=tenant_id, deposit_id=deposit_id, action="interest.accrued", detail=f"amount={amount}"
        )
        return Result.ok({**accrual.to_dict(), "deposit": deposit.to_dict()})

    async def post_accrued_interest(
        self, *, tenant_id: str, deposit_id: str, approver_id: str = "system"
    ) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit or deposit.tenant_id != tenant_id:
            return Result.fail("banking.errors.deposit_not_found")
        if deposit.accrued_interest <= 0:
            return Result.fail("banking.errors.no_accrued_interest")

        amount = deposit.accrued_interest
        ref = self._transactions.next_transaction_ref(tenant_id)
        txn = DepositTransaction.create(
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            account_id=deposit.account_id,
            transaction_ref=ref,
            transaction_type=TransactionType.INTEREST_CREDIT.value,
            amount=amount,
            currency=deposit.currency,
            auto_approve=True,
        )
        await self._transactions.save(txn)

        accruals = await self._accruals.list_by_deposit(deposit_id)
        for a in accruals:
            if a.status == "accrued":
                a.mark_posted()
                await self._accruals.save(a)

        result = await self.approve_transaction(transaction_id=str(txn.id), approver_id=approver_id)
        return result

    async def process_maturity(self, *, deposit_id: str) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit:
            return Result.fail("banking.errors.deposit_not_found")
        if deposit.deposit_type != DepositType.TERM.value:
            return Result.fail("banking.errors.not_term_deposit")

        try:
            deposit.mark_matured()
        except ValueError:
            return Result.fail("banking.errors.cannot_mature")

        await self._deposits.save(deposit)
        await publish_integration_event(
            BankingDepositMaturedIntegration(
                tenant_id=TenantId.create(deposit.tenant_id),
                correlation_id=f"deposit-matured-{deposit_id}",
                deposit_id=deposit_id,
                account_id=deposit.account_id,
                principal=deposit.principal,
                auto_renew=deposit.auto_renew,
            )
        )
        await self._audit(
            tenant_id=deposit.tenant_id, deposit_id=deposit_id, action="deposit.matured", detail=""
        )

        if deposit.auto_renew and deposit.tenure_months:
            return await self.renew_deposit(
                deposit_id=deposit_id, tenure_months=deposit.tenure_months
            )
        return Result.ok(deposit.to_dict())

    async def renew_deposit(
        self, *, deposit_id: str, tenure_months: int, interest_rate_annual: float | None = None
    ) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit:
            return Result.fail("banking.errors.deposit_not_found")
        try:
            deposit.renew(tenure_months=tenure_months, interest_rate_annual=interest_rate_annual)
        except ValueError:
            return Result.fail("banking.errors.cannot_renew")
        await self._deposits.save(deposit)
        await self._audit(
            tenant_id=deposit.tenant_id,
            deposit_id=deposit_id,
            action="deposit.renewed",
            detail=f"tenure={tenure_months}",
        )
        return Result.ok(deposit.to_dict())

    async def issue_certificate(self, *, tenant_id: str, deposit_id: str) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit or deposit.tenant_id != tenant_id:
            return Result.fail("banking.errors.deposit_not_found")
        if deposit.status not in {DepositStatus.ACTIVE.value, DepositStatus.MATURED.value}:
            return Result.fail("banking.errors.deposit_not_active")

        cert_num = self._certificates.next_certificate_number(tenant_id)
        cert = DepositCertificate.create(
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            certificate_number=cert_num,
            issue_date=datetime.now(UTC),
            maturity_date=deposit.maturity_date,
            principal=deposit.principal,
            rate_annual=deposit.interest_rate_annual,
            currency=deposit.currency,
        )
        await self._certificates.save(cert)
        await self._audit(
            tenant_id=tenant_id, deposit_id=deposit_id, action="certificate.issued", detail=cert_num
        )
        return Result.ok(cert.to_dict())

    async def generate_statement(
        self, *, tenant_id: str, deposit_id: str, period_days: int = 30
    ) -> Result[dict]:
        deposit = await self._deposits.find_by_id(deposit_id)
        if not deposit or deposit.tenant_id != tenant_id:
            return Result.fail("banking.errors.deposit_not_found")

        period_end = datetime.now(UTC)
        period_start = period_end - timedelta(days=period_days)
        txns = await self._transactions.list_by_deposit(deposit_id)
        lines, credits, debits, interest = build_statement_lines(
            transactions=[t.to_dict() for t in txns],
            period_start=period_start,
            period_end=period_end,
        )
        opening = round(deposit.principal - credits + debits, 2)
        ref = self._statements.next_statement_ref(tenant_id)
        statement = DepositStatement.create(
            tenant_id=tenant_id,
            deposit_id=deposit_id,
            statement_ref=ref,
            period_start=period_start,
            period_end=period_end,
            opening_balance=opening,
            closing_balance=deposit.principal,
            total_credits=credits,
            total_debits=debits,
            interest_earned=interest,
            line_items=lines,
        )
        await self._statements.save(statement)
        await self._audit(
            tenant_id=tenant_id, deposit_id=deposit_id, action="statement.generated", detail=ref
        )
        return Result.ok(statement.to_dict())

    async def get_audit_trail(self, deposit_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_deposit(deposit_id)
        return Result.ok([e.to_dict() for e in entries])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._profit_rules.list_by_tenant(tenant_id):
            return
        defaults = [
            ("INT-SAV", "Savings Interest", DepositType.SAVINGS.value, "interest", 2.5, 0.0),
            ("INT-TERM", "Term Deposit Interest", DepositType.TERM.value, "interest", 5.0, 0.0),
            ("PROFIT-SAV", "Savings Profit Share", DepositType.SAVINGS.value, "profit_sharing", 0.0, 3.0),
        ]
        for code, name, dtype, method, rate, profit in defaults:
            rule = ProfitDistributionRule.create(
                tenant_id=tenant_id,
                rule_code=code,
                name=name,
                deposit_type=dtype,
                method=method,
                rate_annual=rate,
                profit_share_pct=profit,
            )
            await self._profit_rules.save(rule)


def _days_to_maturity(maturity_date: datetime | None) -> int:
    if not maturity_date:
        return 9999
    if maturity_date.tzinfo is None:
        maturity_date = maturity_date.replace(tzinfo=UTC)
    return max(0, (maturity_date - datetime.now(UTC)).days)
