"""Enterprise Loan Platform application service."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.loan_management_engine import (
    LoanAuditEntry,
    LoanCollateral,
    LoanCreditRiskAnalysis,
    LoanGuarantor,
    LoanInstallment,
    LoanProfile,
    LoanStatus,
    LoanTransaction,
    LoanTransactionType,
    LoanWorkflowRequest,
    TransactionStatus,
)
from contexts.banking.domain.events.loan_integration_events import (
    BankingLoanCreditRiskAnalyzedIntegration,
    BankingLoanDisbursedIntegration,
    BankingLoanRepaymentPostedIntegration,
)
from contexts.banking.domain.ports.customer_account_repositories import (
    IAccountRepository,
    ICustomerRepository,
)
from contexts.banking.domain.ports.loan_management_repositories import (
    ILoanAuditRepository,
    ILoanCollateralRepository,
    ILoanCreditRiskRepository,
    ILoanGuarantorRepository,
    ILoanInstallmentRepository,
    ILoanProfileRepository,
    ILoanTransactionRepository,
    ILoanWorkflowRepository,
)
from contexts.banking.domain.services.loan_management_engine import (
    analyze_credit_risk,
    build_amortization_schedule,
    build_loan_dashboard,
    calculate_emi,
    calculate_late_penalty,
    list_loan_catalog,
    list_loan_policy_keys,
    resolve_loan_approval_levels,
)
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingLoanManagementApplicationService:
    def __init__(
        self,
        loans: ILoanProfileRepository,
        collaterals: ILoanCollateralRepository,
        guarantors: ILoanGuarantorRepository,
        installments: ILoanInstallmentRepository,
        transactions: ILoanTransactionRepository,
        risk_analyses: ILoanCreditRiskRepository,
        workflows: ILoanWorkflowRepository,
        audits: ILoanAuditRepository,
        accounts: IAccountRepository,
        customers: ICustomerRepository,
        kernel: IFinancialKernel,
        policy: IPolicyEvaluator,
    ) -> None:
        self._loans = loans
        self._collaterals = collaterals
        self._guarantors = guarantors
        self._installments = installments
        self._transactions = transactions
        self._risk_analyses = risk_analyses
        self._workflows = workflows
        self._audits = audits
        self._accounts = accounts
        self._customers = customers
        self._kernel = kernel
        self._policy = policy

    async def _audit(
        self, *, tenant_id: str, loan_id: str, action: str, actor_id: str | None = None, detail: str = ""
    ) -> None:
        await self._audits.save(
            LoanAuditEntry.create(
                tenant_id=tenant_id, loan_id=loan_id, action=action, actor_id=actor_id, detail=detail
            )
        )

    async def _resolve_account_key(self, tenant_id: str, account_key: str) -> str | None:
        accounts = await self._kernel.list_accounts(tenant_id=tenant_id)
        for acct in accounts:
            if acct.get("account_key") == account_key:
                return acct.get("code") or acct.get("account_code")
        return None

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_loan_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_loan_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        loans = await self._loans.list_by_tenant(tenant_id)
        txns = await self._transactions.list_by_tenant(tenant_id)
        all_installments: list[dict] = []
        for loan in loans:
            insts = await self._installments.list_by_loan(str(loan.id))
            all_installments.extend([i.to_dict() for i in insts])
        risks = await self._risk_analyses.list_by_tenant(tenant_id)
        return Result.ok(
            build_loan_dashboard(
                loans=[l.to_dict() for l in loans],
                transactions=[t.to_dict() for t in txns],
                installments=all_installments,
                risk_analyses=[r.to_dict() for r in risks],
            )
        )

    async def apply_loan(
        self,
        *,
        tenant_id: str,
        account_id: str,
        loan_type: str,
        principal: float,
        tenure_months: int = 12,
        interest_rate_annual: float | None = None,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("banking.errors.account_not_found")
        if not account.kernel_linked:
            return Result.fail("banking.errors.account_not_kernel_linked")
        if await self._loans.find_by_account(account_id):
            return Result.fail("banking.errors.loan_already_exists")

        rate_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="loan.interest.rate",
            facts={"loan_type": loan_type, "principal": principal, "tenure_months": tenure_months},
        )
        rate = interest_rate_annual
        if rate is None:
            rate = float(rate_policy.parameters.get("rate_annual", account.interest_rate_annual or 12.0))

        emi = calculate_emi(principal=principal, rate_annual=rate, tenure_months=tenure_months)
        gl_code = account.gl_account_code or await self._resolve_account_key(tenant_id, "loans_receivable")
        ref = self._loans.next_loan_ref(tenant_id)

        loan = LoanProfile.create(
            tenant_id=tenant_id,
            account_id=account_id,
            customer_id=account.customer_id,
            loan_type=loan_type,
            loan_ref=ref,
            currency=account.currency,
            principal=principal,
            interest_rate_annual=rate,
            tenure_months=tenure_months,
            emi_amount=emi,
            gl_account_code=gl_code,
        )
        await self._loans.save(loan)
        await self._audit(tenant_id=tenant_id, loan_id=str(loan.id), action="loan.applied", detail=f"type={loan_type}")
        return Result.ok(loan.to_dict())

    async def submit_loan(self, *, loan_id: str) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")
        try:
            loan.submit()
        except ValueError:
            return Result.fail("banking.errors.not_draft_loan")

        approval_policy = await self._policy.evaluate(
            tenant_id=loan.tenant_id,
            domain="bank",
            policy_key="loan.approval.required_level",
            facts={"loan_type": loan.loan_type, "amount": loan.principal},
        )
        levels = int(approval_policy.parameters.get("required_levels", resolve_loan_approval_levels(
            loan_type=loan.loan_type, amount=loan.principal
        )))
        workflow = LoanWorkflowRequest.create(
            tenant_id=loan.tenant_id,
            loan_id=loan_id,
            request_type="loan_approval",
            required_levels=levels,
        )
        await self._workflows.save(workflow)
        await self._loans.save(loan)
        await self._audit(tenant_id=loan.tenant_id, loan_id=loan_id, action="loan.submitted")
        return Result.ok({**loan.to_dict(), "workflow": workflow.to_dict()})

    async def approve_loan(self, *, loan_id: str, approver_id: str) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")

        workflows = await self._workflows.list_by_loan(loan_id)
        pending = next((w for w in workflows if w.status == "pending"), None)
        if pending:
            pending.approve(approver_id=approver_id)
            await self._workflows.save(pending)
            if pending.status != "approved":
                return Result.ok({**loan.to_dict(), "workflow": pending.to_dict()})

        try:
            loan.approve()
        except ValueError:
            return Result.fail("banking.errors.not_pending_loan_approval")
        await self._loans.save(loan)
        await self._audit(
            tenant_id=loan.tenant_id, loan_id=loan_id, action="loan.approved", actor_id=approver_id
        )
        return Result.ok(loan.to_dict())

    async def add_collateral(
        self,
        *,
        tenant_id: str,
        loan_id: str,
        collateral_type: str,
        description: str,
        estimated_value: float,
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan or loan.tenant_id != tenant_id:
            return Result.fail("banking.errors.loan_not_found")
        collateral = LoanCollateral.create(
            tenant_id=tenant_id,
            loan_id=loan_id,
            collateral_type=collateral_type,
            description=description,
            estimated_value=estimated_value,
            currency=loan.currency,
        )
        await self._collaterals.save(collateral)
        await self._audit(tenant_id=tenant_id, loan_id=loan_id, action="collateral.added")
        return Result.ok(collateral.to_dict())

    async def add_guarantor(
        self,
        *,
        tenant_id: str,
        loan_id: str,
        guarantor_name: str,
        guarantor_id_ref: str,
        relationship: str = "",
        guaranteed_amount: float = 0.0,
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan or loan.tenant_id != tenant_id:
            return Result.fail("banking.errors.loan_not_found")
        guarantor = LoanGuarantor.create(
            tenant_id=tenant_id,
            loan_id=loan_id,
            guarantor_name=guarantor_name,
            guarantor_id_ref=guarantor_id_ref,
            relationship=relationship,
            guaranteed_amount=guaranteed_amount or loan.principal,
            currency=loan.currency,
        )
        await self._guarantors.save(guarantor)
        await self._audit(tenant_id=tenant_id, loan_id=loan_id, action="guarantor.added")
        return Result.ok(guarantor.to_dict())

    async def analyze_credit_risk(
        self,
        *,
        tenant_id: str,
        loan_id: str,
        monthly_income: float,
        existing_obligations: float = 0.0,
        ai_provider_ref: str | None = None,
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan or loan.tenant_id != tenant_id:
            return Result.fail("banking.errors.loan_not_found")

        collaterals = await self._collaterals.list_by_loan(loan_id)
        collateral_value = sum(c.estimated_value for c in collaterals)

        haircut_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="lending.collateral.haircut",
            facts={"collateral_type": collaterals[0].collateral_type if collaterals else "none", "collateral_value": collateral_value},
        )
        haircut = float(haircut_policy.parameters.get("haircut_pct", 10.0))

        risk_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="loan.credit_risk.threshold",
            facts={"loan_type": loan.loan_type, "amount": loan.principal},
        )
        thresholds = risk_policy.parameters

        customer = await self._customers.find_by_id(loan.customer_id)
        kyc_risk = customer.risk_rating if customer else "low"

        result = analyze_credit_risk(
            loan_amount=loan.principal,
            emi_amount=loan.emi_amount,
            monthly_income=monthly_income,
            existing_obligations=existing_obligations,
            collateral_value=collateral_value,
            haircut_pct=haircut,
            kyc_risk_rating=kyc_risk,
            policy_thresholds=thresholds,
        )

        analysis = LoanCreditRiskAnalysis.create(
            tenant_id=tenant_id,
            loan_id=loan_id,
            risk_score=result["risk_score"],
            risk_grade=result["risk_grade"],
            recommendation=result["recommendation"],
            factors=result["factors"],
            dti_ratio=result["dti_ratio"],
            collateral_coverage_pct=result["collateral_coverage_pct"],
            ai_provider_ref=ai_provider_ref,
        )
        loan.credit_risk_id = str(analysis.id)
        await self._risk_analyses.save(analysis)
        await self._loans.save(loan)
        await publish_integration_event(
            BankingLoanCreditRiskAnalyzedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"loan-risk-{analysis.id}",
                loan_id=loan_id,
                analysis_id=str(analysis.id),
                risk_score=result["risk_score"],
                risk_grade=result["risk_grade"],
                recommendation=result["recommendation"],
            )
        )
        await self._audit(
            tenant_id=tenant_id,
            loan_id=loan_id,
            action="credit_risk.analyzed",
            detail=f"score={result['risk_score']} grade={result['risk_grade']}",
        )
        return Result.ok(analysis.to_dict())

    async def disburse_loan(self, *, loan_id: str, approver_id: str) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")
        try:
            loan.disburse(loan.principal)
        except ValueError:
            return Result.fail("banking.errors.not_approved_loan")

        schedule = build_amortization_schedule(
            principal=loan.principal,
            rate_annual=loan.interest_rate_annual,
            tenure_months=loan.tenure_months,
        )
        for row in schedule:
            inst = LoanInstallment.create(
                tenant_id=loan.tenant_id,
                loan_id=loan_id,
                installment_number=row["installment_number"],
                due_date=datetime.fromisoformat(row["due_date"].replace("Z", "+00:00")),
                principal_due=row["principal_due"],
                interest_due=row["interest_due"],
            )
            await self._installments.save(inst)

        ref = self._transactions.next_transaction_ref(loan.tenant_id)
        txn = LoanTransaction.create(
            tenant_id=loan.tenant_id,
            loan_id=loan_id,
            account_id=loan.account_id,
            transaction_ref=ref,
            transaction_type=LoanTransactionType.DISBURSEMENT.value,
            amount=loan.principal,
            currency=loan.currency,
            auto_approve=True,
        )
        await self._transactions.save(txn)

        account = await self._accounts.find_by_id(loan.account_id)
        if account:
            account.credit(loan.principal)

        journal_id = await self._post_gl(
            tenant_id=loan.tenant_id,
            rule_id="loan_disbursement",
            source_document_id=str(txn.id),
            amount=loan.principal,
            currency=loan.currency,
            gl_code=loan.gl_account_code,
            idempotency_key=f"posting:loan_disbursement:{ref}",
            description=f"Loan disbursement {ref}",
        )
        txn.mark_posted(journal_id=journal_id)
        await self._transactions.save(txn)
        if account:
            await self._accounts.save(account)

        loan.activate()
        await self._loans.save(loan)

        await publish_integration_event(
            BankingLoanDisbursedIntegration(
                tenant_id=TenantId.create(loan.tenant_id),
                correlation_id=f"loan-disburse-{txn.id}",
                account_id=loan.account_id,
                loan_id=loan_id,
                transaction_id=str(txn.id),
                transaction_ref=ref,
                amount=loan.principal,
                currency=loan.currency,
                gl_account_code=loan.gl_account_code,
                account_number=account.account_number if account else "",
            )
        )
        await self._audit(
            tenant_id=loan.tenant_id, loan_id=loan_id, action="loan.disbursed", actor_id=approver_id
        )
        return Result.ok({**loan.to_dict(), "transaction": txn.to_dict()})

    async def pay_installment(
        self,
        *,
        tenant_id: str,
        loan_id: str,
        installment_id: str,
        approver_id: str = "system",
        days_overdue: int = 0,
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan or loan.tenant_id != tenant_id:
            return Result.fail("banking.errors.loan_not_found")
        if loan.status not in {LoanStatus.ACTIVE.value, LoanStatus.RESTRUCTURED.value}:
            return Result.fail("banking.errors.loan_not_active")

        installment = await self._installments.find_by_id(installment_id)
        if not installment or installment.loan_id != loan_id:
            return Result.fail("banking.errors.installment_not_found")
        if installment.status == "paid":
            return Result.fail("banking.errors.installment_already_paid")

        penalty_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="loan.penalty.late_payment",
            facts={"days_overdue": days_overdue, "amount": installment.total_due, "loan_type": loan.loan_type},
        )
        penalty_pct = float(penalty_policy.parameters.get("penalty_pct", 1.0))
        penalty = calculate_late_penalty(
            amount=installment.total_due,
            days_overdue=days_overdue,
            penalty_pct=penalty_pct,
            policy_outcome=penalty_policy.outcome,
        )
        total = round(installment.total_due + penalty, 2)
        ref = self._transactions.next_transaction_ref(tenant_id)
        txn = LoanTransaction.create(
            tenant_id=tenant_id,
            loan_id=loan_id,
            account_id=loan.account_id,
            transaction_ref=ref,
            transaction_type=LoanTransactionType.REPAYMENT.value,
            amount=total,
            currency=loan.currency,
            principal_part=installment.principal_due,
            interest_part=installment.interest_due,
            penalty_amount=penalty,
            auto_approve=True,
        )
        await self._transactions.save(txn)

        account = await self._accounts.find_by_id(loan.account_id)
        if account:
            account.debit(total)

        journal_id = await self._post_gl(
            tenant_id=tenant_id,
            rule_id="loan_repayment",
            source_document_id=str(txn.id),
            amount=total,
            currency=loan.currency,
            gl_code=loan.gl_account_code,
            idempotency_key=f"posting:loan_repayment:{ref}",
            description=f"Loan repayment {ref}",
        )
        txn.mark_posted(journal_id=journal_id)
        await self._transactions.save(txn)

        loan.apply_repayment(
            principal_part=installment.principal_due,
            interest_part=installment.interest_due,
            penalty=penalty,
        )
        installment.mark_paid(penalty=penalty)
        await self._installments.save(installment)
        await self._loans.save(loan)
        if account:
            await self._accounts.save(account)

        await publish_integration_event(
            BankingLoanRepaymentPostedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"loan-repay-{txn.id}",
                account_id=loan.account_id,
                loan_id=loan_id,
                transaction_id=str(txn.id),
                transaction_ref=ref,
                amount=total,
                principal_part=installment.principal_due,
                interest_part=installment.interest_due,
                penalty_amount=penalty,
                currency=loan.currency,
                gl_account_code=loan.gl_account_code,
            )
        )
        await self._audit(
            tenant_id=tenant_id, loan_id=loan_id, action="installment.paid", actor_id=approver_id, detail=ref
        )
        return Result.ok({**txn.to_dict(), "loan": loan.to_dict()})

    async def restructure_loan(
        self,
        *,
        loan_id: str,
        tenure_months: int,
        interest_rate_annual: float | None = None,
        approver_id: str = "system",
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")

        restructure_policy = await self._policy.evaluate(
            tenant_id=loan.tenant_id,
            domain="bank",
            policy_key="loan.restructure.rules",
            facts={"loan_type": loan.loan_type, "outstanding": loan.outstanding_principal},
        )
        if restructure_policy.outcome == "deny":
            return Result.fail("banking.errors.restructure_not_allowed")

        rate = interest_rate_annual or loan.interest_rate_annual
        emi = calculate_emi(
            principal=loan.outstanding_principal, rate_annual=rate, tenure_months=tenure_months
        )
        try:
            loan.restructure(tenure_months=tenure_months, interest_rate_annual=rate, emi_amount=emi)
        except ValueError:
            return Result.fail("banking.errors.cannot_restructure")

        schedule = build_amortization_schedule(
            principal=loan.outstanding_principal,
            rate_annual=rate,
            tenure_months=tenure_months,
        )
        for row in schedule:
            inst = LoanInstallment.create(
                tenant_id=loan.tenant_id,
                loan_id=loan_id,
                installment_number=row["installment_number"],
                due_date=datetime.fromisoformat(row["due_date"].replace("Z", "+00:00")),
                principal_due=row["principal_due"],
                interest_due=row["interest_due"],
            )
            await self._installments.save(inst)

        await self._loans.save(loan)
        await self._audit(
            tenant_id=loan.tenant_id, loan_id=loan_id, action="loan.restructured", actor_id=approver_id
        )
        return Result.ok(loan.to_dict())

    async def settle_loan(
        self, *, loan_id: str, settlement_amount: float, approver_id: str
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")

        discount_policy = await self._policy.evaluate(
            tenant_id=loan.tenant_id,
            domain="bank",
            policy_key="loan.settlement.discount",
            facts={"outstanding": loan.outstanding_principal, "settlement_amount": settlement_amount},
        )
        discount_pct = float(discount_policy.parameters.get("discount_pct", 0.0))

        ref = self._transactions.next_transaction_ref(loan.tenant_id)
        txn = LoanTransaction.create(
            tenant_id=loan.tenant_id,
            loan_id=loan_id,
            account_id=loan.account_id,
            transaction_ref=ref,
            transaction_type=LoanTransactionType.SETTLEMENT.value,
            amount=settlement_amount,
            currency=loan.currency,
            principal_part=loan.outstanding_principal,
            auto_approve=True,
        )
        await self._transactions.save(txn)

        account = await self._accounts.find_by_id(loan.account_id)
        if account:
            account.debit(settlement_amount)

        journal_id = await self._post_gl(
            tenant_id=loan.tenant_id,
            rule_id="loan_repayment",
            source_document_id=str(txn.id),
            amount=settlement_amount,
            currency=loan.currency,
            gl_code=loan.gl_account_code,
            idempotency_key=f"posting:loan_settlement:{ref}",
            description=f"Loan settlement {ref}",
        )
        txn.mark_posted(journal_id=journal_id)
        await self._transactions.save(txn)
        if account:
            await self._accounts.save(account)

        loan.settle(settlement_amount)
        await self._loans.save(loan)
        await self._audit(
            tenant_id=loan.tenant_id,
            loan_id=loan_id,
            action="loan.settled",
            actor_id=approver_id,
            detail=f"discount_pct={discount_pct}",
        )
        return Result.ok({**loan.to_dict(), "transaction": txn.to_dict()})

    async def early_close_loan(
        self, *, loan_id: str, closure_amount: float, approver_id: str
    ) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")

        penalty_policy = await self._policy.evaluate(
            tenant_id=loan.tenant_id,
            domain="bank",
            policy_key="loan.early_closure.penalty",
            facts={"outstanding": loan.outstanding_principal, "closure_amount": closure_amount},
        )
        penalty_pct = float(penalty_policy.parameters.get("penalty_pct", 0.0))
        penalty = round(loan.outstanding_principal * (penalty_pct / 100), 2) if penalty_pct else 0.0
        total = round(closure_amount + penalty, 2)

        ref = self._transactions.next_transaction_ref(loan.tenant_id)
        txn = LoanTransaction.create(
            tenant_id=loan.tenant_id,
            loan_id=loan_id,
            account_id=loan.account_id,
            transaction_ref=ref,
            transaction_type=LoanTransactionType.EARLY_CLOSURE.value,
            amount=total,
            currency=loan.currency,
            principal_part=loan.outstanding_principal,
            penalty_amount=penalty,
            auto_approve=True,
        )
        await self._transactions.save(txn)

        account = await self._accounts.find_by_id(loan.account_id)
        if account:
            account.debit(total)

        journal_id = await self._post_gl(
            tenant_id=loan.tenant_id,
            rule_id="loan_repayment",
            source_document_id=str(txn.id),
            amount=total,
            currency=loan.currency,
            gl_code=loan.gl_account_code,
            idempotency_key=f"posting:loan_early_close:{ref}",
            description=f"Loan early closure {ref}",
        )
        txn.mark_posted(journal_id=journal_id)
        await self._transactions.save(txn)
        if account:
            await self._accounts.save(account)

        loan.early_close()
        await self._loans.save(loan)
        await self._audit(
            tenant_id=loan.tenant_id, loan_id=loan_id, action="loan.early_closed", actor_id=approver_id
        )
        return Result.ok({**loan.to_dict(), "transaction": txn.to_dict()})

    async def list_loans(self, tenant_id: str) -> Result[list[dict]]:
        loans = await self._loans.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in loans])

    async def get_loan(self, loan_id: str) -> Result[dict]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")
        collaterals = await self._collaterals.list_by_loan(loan_id)
        guarantors = await self._guarantors.list_by_loan(loan_id)
        installments = await self._installments.list_by_loan(loan_id)
        txns = await self._transactions.list_by_loan(loan_id)
        risk = await self._risk_analyses.find_by_loan(loan_id)
        workflows = await self._workflows.list_by_loan(loan_id)
        return Result.ok(
            {
                **loan.to_dict(),
                "collaterals": [c.to_dict() for c in collaterals],
                "guarantors": [g.to_dict() for g in guarantors],
                "installments": [i.to_dict() for i in installments],
                "transactions": [t.to_dict() for t in txns],
                "credit_risk": risk.to_dict() if risk else None,
                "workflows": [w.to_dict() for w in workflows],
            }
        )

    async def get_schedule(self, loan_id: str) -> Result[list[dict]]:
        loan = await self._loans.find_by_id(loan_id)
        if not loan:
            return Result.fail("banking.errors.loan_not_found")
        installments = await self._installments.list_by_loan(loan_id)
        return Result.ok([i.to_dict() for i in installments])

    async def get_audit_trail(self, loan_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_loan(loan_id)
        return Result.ok([e.to_dict() for e in entries])

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
        debit_code = await self._resolve_account_key(tenant_id, "loans_receivable")
        credit_code = await self._resolve_account_key(tenant_id, "cash_reserves")
        loan_gl = gl_code or debit_code
        mappings: dict[str, str] = {}
        if rule_id == "loan_disbursement" and loan_gl and credit_code:
            mappings = {"debit": loan_gl, "credit": credit_code}
        elif rule_id == "loan_repayment" and loan_gl and credit_code:
            mappings = {"debit": credit_code, "credit": loan_gl}
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

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        pass
