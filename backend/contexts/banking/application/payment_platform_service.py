"""Banking Payment Platform application service."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.payment_platform_engine import (
    FraudStatus,
    PaymentAuditEntry,
    PaymentBatch,
    PaymentBeneficiary,
    PaymentFraudCheck,
    PaymentTransfer,
    PaymentWorkflowRequest,
    StandingOrder,
    TransferStatus,
    TransferType,
)
from contexts.banking.domain.events.payment_integration_events import (
    BankingPaymentFraudFlaggedIntegration,
    BankingTransactionPostedIntegration,
    BankingTransferPostedIntegration,
)
from contexts.banking.domain.ports.customer_account_repositories import IAccountRepository
from contexts.banking.domain.ports.payment_platform_repositories import (
    IPaymentAuditRepository,
    IPaymentBatchRepository,
    IPaymentBeneficiaryRepository,
    IPaymentFraudRepository,
    IPaymentTransferRepository,
    IPaymentWorkflowRepository,
    IStandingOrderRepository,
)
from contexts.banking.domain.services.payment_platform_engine import (
    REAL_TIME_TYPES,
    build_payment_dashboard,
    check_transfer_limits,
    list_payment_catalog,
    list_payment_policy_keys,
    map_transfer_channel,
    resolve_approval_levels,
    run_fraud_check,
)
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingPaymentPlatformApplicationService:
    def __init__(
        self,
        beneficiaries: IPaymentBeneficiaryRepository,
        transfers: IPaymentTransferRepository,
        batches: IPaymentBatchRepository,
        standing_orders: IStandingOrderRepository,
        workflows: IPaymentWorkflowRepository,
        fraud_checks: IPaymentFraudRepository,
        audits: IPaymentAuditRepository,
        accounts: IAccountRepository,
        kernel: IFinancialKernel,
        policy: IPolicyEvaluator,
    ) -> None:
        self._beneficiaries = beneficiaries
        self._transfers = transfers
        self._batches = batches
        self._standing_orders = standing_orders
        self._workflows = workflows
        self._fraud_checks = fraud_checks
        self._audits = audits
        self._accounts = accounts
        self._kernel = kernel
        self._policy = policy

    async def _audit(
        self, *, tenant_id: str, transfer_id: str, action: str, actor_id: str | None = None, detail: str = ""
    ) -> None:
        await self._audits.save(
            PaymentAuditEntry.create(
                tenant_id=tenant_id, transfer_id=transfer_id, action=action, actor_id=actor_id, detail=detail
            )
        )

    async def _resolve_gl_code(self, tenant_id: str, account_key: str) -> str | None:
        accounts = await self._kernel.list_accounts(tenant_id=tenant_id)
        for acct in accounts:
            if acct.get("account_key") == account_key:
                return acct.get("code") or acct.get("account_code")
        return None

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_payment_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_payment_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        transfers = await self._transfers.list_by_tenant(tenant_id)
        batches = await self._batches.list_by_tenant(tenant_id)
        orders = await self._standing_orders.list_by_tenant(tenant_id)
        fraud = await self._fraud_checks.list_by_tenant(tenant_id)
        return Result.ok(
            build_payment_dashboard(
                transfers=[t.to_dict() for t in transfers],
                batches=[b.to_dict() for b in batches],
                standing_orders=[o.to_dict() for o in orders],
                fraud_checks=[f.to_dict() for f in fraud],
            )
        )

    async def add_beneficiary(
        self,
        *,
        tenant_id: str,
        customer_id: str,
        name: str,
        account_number: str,
        bank_code: str = "",
        branch_code: str = "",
        currency: str = "USD",
        beneficiary_type: str = "external",
    ) -> Result[dict]:
        ref = self._beneficiaries.next_beneficiary_ref(tenant_id)
        beneficiary = PaymentBeneficiary.create(
            tenant_id=tenant_id,
            customer_id=customer_id,
            beneficiary_ref=ref,
            name=name,
            account_number=account_number,
            bank_code=bank_code,
            branch_code=branch_code,
            currency=currency,
            beneficiary_type=beneficiary_type,
        )
        await self._beneficiaries.save(beneficiary)
        return Result.ok(beneficiary.to_dict())

    async def create_transfer(
        self,
        *,
        tenant_id: str,
        transfer_type: str,
        source_account_id: str,
        amount: float,
        destination_account_id: str | None = None,
        beneficiary_id: str | None = None,
        channel: str | None = None,
        branch_id: str = "",
        destination_branch_id: str = "",
        scheduled_at: datetime | None = None,
        qr_payload: str = "",
        merchant_ref: str = "",
        bill_ref: str = "",
        government_ref: str = "",
        salary_ref: str = "",
        narrative: str = "",
        batch_id: str | None = None,
        standing_order_id: str | None = None,
    ) -> Result[dict]:
        source = await self._accounts.find_by_id(source_account_id)
        if not source or source.tenant_id != tenant_id:
            return Result.fail("banking.errors.account_not_found")
        if not source.kernel_linked:
            return Result.fail("banking.errors.account_not_kernel_linked")

        if destination_account_id:
            dest = await self._accounts.find_by_id(destination_account_id)
            if not dest or dest.tenant_id != tenant_id:
                return Result.fail("banking.errors.destination_account_not_found")

        if beneficiary_id:
            ben = await self._beneficiaries.find_by_id(beneficiary_id)
            if not ben or ben.tenant_id != tenant_id:
                return Result.fail("banking.errors.beneficiary_not_found")

        ref = self._transfers.next_transfer_ref(tenant_id)
        transfer = PaymentTransfer.create(
            tenant_id=tenant_id,
            transfer_ref=ref,
            transfer_type=transfer_type,
            source_account_id=source_account_id,
            customer_id=source.customer_id,
            amount=amount,
            currency=source.currency,
            destination_account_id=destination_account_id,
            beneficiary_id=beneficiary_id,
            channel=channel or map_transfer_channel(transfer_type),
            branch_id=branch_id or source.branch_id,
            destination_branch_id=destination_branch_id,
            scheduled_at=scheduled_at,
            qr_payload=qr_payload,
            merchant_ref=merchant_ref,
            bill_ref=bill_ref,
            government_ref=government_ref,
            salary_ref=salary_ref,
            narrative=narrative,
            batch_id=batch_id,
            standing_order_id=standing_order_id,
        )
        await self._transfers.save(transfer)
        await self._audit(tenant_id=tenant_id, transfer_id=str(transfer.id), action="transfer.created")
        return Result.ok(transfer.to_dict())

    async def submit_transfer(self, *, transfer_id: str) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("banking.errors.transfer_not_found")

        limit_ok, limit_err = await self._check_limits(transfer)
        if not limit_ok:
            return Result.fail(limit_err or "banking.errors.transfer_limit_exceeded")

        fraud_result = await self._run_fraud(transfer)
        transfer.set_fraud(status=fraud_result["status"], score=fraud_result["risk_score"])
        if fraud_result["status"] == FraudStatus.BLOCKED.value:
            transfer.fail("fraud_blocked")
            await self._transfers.save(transfer)
            return Result.fail("banking.errors.transfer_fraud_blocked")

        try:
            transfer.submit()
        except ValueError:
            return Result.fail("banking.errors.not_draft_transfer")

        approval_policy = await self._policy.evaluate(
            tenant_id=transfer.tenant_id,
            domain="bank",
            policy_key="payment.approval.required_level",
            facts={"transfer_type": transfer.transfer_type, "amount": transfer.amount},
        )
        levels = int(
            approval_policy.parameters.get(
                "required_levels",
                resolve_approval_levels(transfer_type=transfer.transfer_type, amount=transfer.amount),
            )
        )
        workflow = PaymentWorkflowRequest.create(
            tenant_id=transfer.tenant_id,
            transfer_id=transfer_id,
            request_type="transfer_approval",
            required_levels=levels,
        )
        await self._workflows.save(workflow)
        await self._transfers.save(transfer)
        await self._audit(tenant_id=transfer.tenant_id, transfer_id=transfer_id, action="transfer.submitted")
        return Result.ok({**transfer.to_dict(), "workflow": workflow.to_dict(), "fraud": fraud_result})

    async def approve_transfer(self, *, transfer_id: str, approver_id: str) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("banking.errors.transfer_not_found")

        workflows = await self._workflows.list_by_transfer(transfer_id)
        pending = next((w for w in workflows if w.status == "pending"), None)
        if pending:
            pending.approve(approver_id=approver_id)
            await self._workflows.save(pending)
            if pending.status != "approved":
                return Result.ok({**transfer.to_dict(), "workflow": pending.to_dict()})

        try:
            transfer.approve()
        except ValueError:
            return Result.fail("banking.errors.not_pending_transfer")
        await self._transfers.save(transfer)
        await self._audit(
            tenant_id=transfer.tenant_id,
            transfer_id=transfer_id,
            action="transfer.approved",
            actor_id=approver_id,
        )
        return Result.ok(transfer.to_dict())

    async def schedule_transfer(self, *, transfer_id: str, scheduled_at: datetime) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("banking.errors.transfer_not_found")
        transfer.scheduled_at = scheduled_at
        try:
            transfer.schedule()
        except ValueError:
            return Result.fail("banking.errors.cannot_schedule_transfer")
        await self._transfers.save(transfer)
        await self._audit(tenant_id=transfer.tenant_id, transfer_id=transfer_id, action="transfer.scheduled")
        return Result.ok(transfer.to_dict())

    async def execute_transfer(self, *, transfer_id: str, approver_id: str = "system") -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("banking.errors.transfer_not_found")

        if transfer.fraud_status == FraudStatus.BLOCKED.value:
            return Result.fail("banking.errors.transfer_fraud_blocked")

        if transfer.status == TransferStatus.DRAFT.value:
            submit = await self.submit_transfer(transfer_id=transfer_id)
            if not submit.succeeded:
                return submit
            transfer = await self._transfers.find_by_id(transfer_id)
            assert transfer

        if transfer.status == TransferStatus.PENDING_APPROVAL.value:
            approve = await self.approve_transfer(transfer_id=transfer_id, approver_id=approver_id)
            if not approve.succeeded:
                return approve
            transfer = await self._transfers.find_by_id(transfer_id)
            assert transfer

        if transfer.status == TransferStatus.SCHEDULED.value:
            if transfer.scheduled_at and transfer.scheduled_at > datetime.now(UTC):
                return Result.fail("banking.errors.transfer_not_due")

        limit_ok, limit_err = await self._check_limits(transfer)
        if not limit_ok:
            return Result.fail(limit_err or "banking.errors.transfer_limit_exceeded")

        source = await self._accounts.find_by_id(transfer.source_account_id)
        if not source:
            return Result.fail("banking.errors.account_not_found")

        try:
            transfer.start_processing()
        except ValueError:
            return Result.fail("banking.errors.cannot_execute_transfer")

        try:
            source.debit(transfer.amount)
        except ValueError:
            transfer.fail("insufficient_balance")
            await self._transfers.save(transfer)
            return Result.fail("banking.errors.insufficient_balance")

        dest = None
        if transfer.destination_account_id:
            dest = await self._accounts.find_by_id(transfer.destination_account_id)
            if dest:
                dest.credit(transfer.amount)

        source_gl = source.gl_account_code or await self._resolve_gl_code(transfer.tenant_id, "customer_deposits")
        dest_gl = None
        if dest:
            dest_gl = dest.gl_account_code or await self._resolve_gl_code(transfer.tenant_id, "customer_deposits")
        elif transfer.transfer_type == TransferType.BANK_TO_BANK.value:
            dest_gl = await self._resolve_gl_code(transfer.tenant_id, "cash_reserves")

        journal_id = await self._post_gl(
            tenant_id=transfer.tenant_id,
            transfer_id=str(transfer.id),
            transfer_ref=transfer.transfer_ref,
            amount=transfer.amount,
            currency=transfer.currency,
            source_gl=source_gl,
            dest_gl=dest_gl or source_gl,
        )

        transfer.complete(journal_id=journal_id)
        await self._transfers.save(transfer)
        await self._accounts.save(source)
        if dest:
            await self._accounts.save(dest)

        await publish_integration_event(
            BankingTransferPostedIntegration(
                tenant_id=TenantId.create(transfer.tenant_id),
                correlation_id=f"transfer-{transfer.id}",
                transfer_id=str(transfer.id),
                transfer_ref=transfer.transfer_ref,
                transfer_type=transfer.transfer_type,
                source_account_id=transfer.source_account_id,
                destination_account_id=transfer.destination_account_id,
                amount=transfer.amount,
                currency=transfer.currency,
                source_gl_code=source_gl,
                destination_gl_code=dest_gl,
            )
        )
        await publish_integration_event(
            BankingTransactionPostedIntegration(
                tenant_id=TenantId.create(transfer.tenant_id),
                correlation_id=f"txn-{transfer.id}",
                transfer_id=str(transfer.id),
                transfer_ref=transfer.transfer_ref,
                transfer_type=transfer.transfer_type,
                amount=transfer.amount,
                currency=transfer.currency,
                channel=transfer.channel,
            )
        )
        await self._audit(
            tenant_id=transfer.tenant_id,
            transfer_id=transfer_id,
            action="transfer.executed",
            actor_id=approver_id,
            detail=transfer.transfer_ref,
        )
        return Result.ok(transfer.to_dict())

    async def create_bulk_transfer(
        self,
        *,
        tenant_id: str,
        source_account_id: str,
        transfer_type: str,
        items: list[dict],
    ) -> Result[dict]:
        source = await self._accounts.find_by_id(source_account_id)
        if not source or source.tenant_id != tenant_id:
            return Result.fail("banking.errors.account_not_found")

        batch_ref = self._batches.next_batch_ref(tenant_id)
        batch = PaymentBatch.create(
            tenant_id=tenant_id,
            batch_ref=batch_ref,
            transfer_type=transfer_type,
            source_account_id=source_account_id,
            customer_id=source.customer_id,
            currency=source.currency,
        )
        created: list[dict] = []
        for item in items:
            result = await self.create_transfer(
                tenant_id=tenant_id,
                transfer_type=transfer_type,
                source_account_id=source_account_id,
                amount=float(item["amount"]),
                destination_account_id=item.get("destination_account_id"),
                beneficiary_id=item.get("beneficiary_id"),
                batch_id=str(batch.id),
                salary_ref=item.get("salary_ref", ""),
                bill_ref=item.get("bill_ref", ""),
                government_ref=item.get("government_ref", ""),
                narrative=item.get("narrative", ""),
            )
            if result.succeeded:
                batch.add_item(float(item["amount"]))
                created.append(result.unwrap())

        await self._batches.save(batch)
        return Result.ok({"batch": batch.to_dict(), "transfers": created})

    async def create_standing_order(
        self,
        *,
        tenant_id: str,
        source_account_id: str,
        transfer_type: str,
        amount: float,
        frequency: str,
        destination_account_id: str | None = None,
        beneficiary_id: str | None = None,
    ) -> Result[dict]:
        source = await self._accounts.find_by_id(source_account_id)
        if not source or source.tenant_id != tenant_id:
            return Result.fail("banking.errors.account_not_found")

        order_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="payment.standing_order.rules",
            facts={"frequency": frequency, "amount": amount},
        )
        if order_policy.outcome == "deny":
            return Result.fail("banking.errors.standing_order_not_allowed")

        next_run = datetime.now(UTC) + timedelta(days=30 if frequency == "monthly" else 7)
        ref = self._standing_orders.next_order_ref(tenant_id)
        order = StandingOrder.create(
            tenant_id=tenant_id,
            order_ref=ref,
            customer_id=source.customer_id,
            source_account_id=source_account_id,
            transfer_type=transfer_type,
            amount=amount,
            currency=source.currency,
            frequency=frequency,
            next_run_at=next_run,
            destination_account_id=destination_account_id,
            beneficiary_id=beneficiary_id,
        )
        await self._standing_orders.save(order)
        return Result.ok(order.to_dict())

    async def run_fraud_check(self, *, transfer_id: str) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("banking.errors.transfer_not_found")
        result = await self._run_fraud(transfer)
        transfer.set_fraud(status=result["status"], score=result["risk_score"])
        await self._transfers.save(transfer)
        return Result.ok(result)

    async def list_transfers(self, tenant_id: str) -> Result[list[dict]]:
        transfers = await self._transfers.list_by_tenant(tenant_id)
        return Result.ok([t.to_dict() for t in transfers])

    async def get_transfer(self, transfer_id: str) -> Result[dict]:
        transfer = await self._transfers.find_by_id(transfer_id)
        if not transfer:
            return Result.fail("banking.errors.transfer_not_found")
        workflows = await self._workflows.list_by_transfer(transfer_id)
        fraud = await self._fraud_checks.find_by_transfer(transfer_id)
        audits = await self._audits.list_by_transfer(transfer_id)
        return Result.ok(
            {
                **transfer.to_dict(),
                "workflows": [w.to_dict() for w in workflows],
                "fraud_check": fraud.to_dict() if fraud else None,
                "audit_trail": [a.to_dict() for a in audits],
            }
        )

    async def get_audit_trail(self, transfer_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_transfer(transfer_id)
        return Result.ok([e.to_dict() for e in entries])

    async def _check_limits(self, transfer: PaymentTransfer) -> tuple[bool, str | None]:
        daily_policy = await self._policy.evaluate(
            tenant_id=transfer.tenant_id,
            domain="bank",
            policy_key="payment.transfer.daily_limit",
            facts={"customer_id": transfer.customer_id, "amount": transfer.amount},
        )
        single_policy = await self._policy.evaluate(
            tenant_id=transfer.tenant_id,
            domain="bank",
            policy_key="payment.transfer.single_limit",
            facts={"amount": transfer.amount, "transfer_type": transfer.transfer_type},
        )
        daily_limit = float(daily_policy.parameters.get("max_amount", 0))
        single_limit = float(single_policy.parameters.get("max_amount", 0))
        daily_total = await self._transfers.daily_total_by_account(
            transfer.tenant_id, transfer.source_account_id
        )
        return check_transfer_limits(
            amount=transfer.amount,
            daily_total=daily_total,
            daily_limit=daily_limit,
            single_limit=single_limit,
            policy_outcome=daily_policy.outcome,
        )

    async def _run_fraud(self, transfer: PaymentTransfer) -> dict:
        fraud_policy = await self._policy.evaluate(
            tenant_id=transfer.tenant_id,
            domain="bank",
            policy_key="payment.fraud.threshold",
            facts={"amount": transfer.amount, "transfer_type": transfer.transfer_type},
        )
        velocity = await self._transfers.velocity_count(transfer.tenant_id, transfer.customer_id)
        result = run_fraud_check(
            amount=transfer.amount,
            transfer_type=transfer.transfer_type,
            channel=transfer.channel,
            velocity_count=velocity,
            policy_thresholds=fraud_policy.parameters,
        )
        check = PaymentFraudCheck.create(
            tenant_id=transfer.tenant_id,
            transfer_id=str(transfer.id),
            risk_score=result["risk_score"],
            status=result["status"],
            factors=result["factors"],
        )
        await self._fraud_checks.save(check)
        if result["status"] in {FraudStatus.BLOCKED.value, FraudStatus.REVIEW.value}:
            await publish_integration_event(
                BankingPaymentFraudFlaggedIntegration(
                    tenant_id=TenantId.create(transfer.tenant_id),
                    correlation_id=f"fraud-{check.id}",
                    transfer_id=str(transfer.id),
                    fraud_check_id=str(check.id),
                    risk_score=result["risk_score"],
                    status=result["status"],
                )
            )
        return result

    async def _post_gl(
        self,
        *,
        tenant_id: str,
        transfer_id: str,
        transfer_ref: str,
        amount: float,
        currency: str,
        source_gl: str | None,
        dest_gl: str | None,
    ) -> str | None:
        debit_code = source_gl or await self._resolve_gl_code(tenant_id, "customer_deposits")
        credit_code = dest_gl or await self._resolve_gl_code(tenant_id, "customer_deposits")
        if not debit_code or not credit_code:
            return None
        try:
            result = await self._kernel.execute_posting(
                tenant_id=tenant_id,
                rule_id="bank_transfer",
                source_context="banking",
                source_document_id=transfer_id,
                amount=amount,
                currency=currency,
                correlation_id=f"posting:bank_transfer:{transfer_ref}",
                idempotency_key=f"posting:bank_transfer:{transfer_ref}",
                description=f"Bank transfer {transfer_ref}",
                account_mappings={"debit": debit_code, "credit": credit_code},
            )
            return result.journal_id
        except ValueError:
            return None

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        pass
