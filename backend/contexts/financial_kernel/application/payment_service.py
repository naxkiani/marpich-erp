"""Enterprise Payment Platform application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.payment import (
    InstallmentPlan,
    Payment,
    PaymentKind,
    PaymentMethod,
    PaymentStatus,
)
from contexts.financial_kernel.domain.aggregates.payment_reconciliation import PaymentReconciliation
from contexts.financial_kernel.domain.events.integration_events import (
    PaymentAllocatedIntegration,
    PaymentChargebackIntegration,
    PaymentReconciledIntegration,
    PaymentRefundedIntegration,
    PaymentSettledIntegration,
)
from contexts.financial_kernel.domain.ports.payment_repositories import (
    IInstallmentPlanRepository,
    IPaymentReconciliationRepository,
    IPaymentRepository,
)
from contexts.financial_kernel.domain.services.payment_engine import (
    auto_allocate,
    build_installment_schedule,
    match_payments_to_bank,
    validate_split_amounts,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class PaymentApplicationService:
    def __init__(
        self,
        payments: IPaymentRepository,
        installments: IInstallmentPlanRepository,
        reconciliations: IPaymentReconciliationRepository,
    ) -> None:
        self._payments = payments
        self._installments = installments
        self._reconciliations = reconciliations

    async def create_payment(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        payment_method: str,
        amount: float,
        currency: str,
        reference: str,
        payment_kind: str = PaymentKind.STANDARD.value,
        paid_amount: float | None = None,
        allocations: list[dict] | None = None,
        payer_id: str | None = None,
        auto_allocate_open_items: list[dict] | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._payments.find_by_idempotency(tenant_id, idempotency_key)
        if existing:
            return Result.ok(existing.to_dict())
        try:
            PaymentMethod(payment_method)
            PaymentKind(payment_kind)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_payment_method")

        final_allocations = allocations
        effective_paid = paid_amount if paid_amount is not None else amount
        if auto_allocate_open_items and not allocations:
            final_allocations = auto_allocate(effective_paid, auto_allocate_open_items)

        payment = Payment.create(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            payment_method=payment_method,
            payment_kind=payment_kind,
            total_amount=amount,
            currency=currency,
            reference=reference,
            paid_amount=paid_amount,
            allocations=final_allocations,
            payer_id=payer_id,
        )
        if final_allocations:
            payment.apply_allocation(final_allocations)
        await self._payments.save(payment)

        if payment.status == PaymentStatus.SETTLED:
            await self._emit_settled(payment, correlation_id)
        if final_allocations:
            await self._emit_allocated(payment, correlation_id)
        return Result.ok(payment.to_dict())

    async def create_split_payment(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        payment_method: str,
        total_amount: float,
        currency: str,
        reference: str,
        splits: list[dict],
        correlation_id: str = "",
    ) -> Result[dict]:
        ok, reason = validate_split_amounts(splits, total_amount)
        if not ok:
            return Result.fail(f"financial_kernel.errors.payment.{reason}")

        parent = Payment.create(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            payment_method=payment_method,
            payment_kind=PaymentKind.SPLIT.value,
            total_amount=total_amount,
            currency=currency,
            reference=reference,
            paid_amount=0,
        )
        parent.status = PaymentStatus.PENDING
        parent.remaining_amount = total_amount
        parent.settled_at = None
        await self._payments.save(parent)

        children = []
        for i, split in enumerate(splits):
            child = Payment.create(
                tenant_id=tenant_id,
                source_context=source_context,
                source_document_id=f"{source_document_id}:split:{i+1}",
                idempotency_key=f"{idempotency_key}:split:{i+1}",
                payment_method=split.get("payment_method", payment_method),
                payment_kind=PaymentKind.SPLIT.value,
                total_amount=float(split["amount"]),
                currency=currency,
                reference=f"{reference}-S{i+1}",
                paid_amount=float(split["amount"]),
                allocations=split.get("allocations"),
                parent_payment_id=str(parent.id),
            )
            await self._payments.save(child)
            children.append(child.to_dict())
            parent.paid_amount = round(parent.paid_amount + child.paid_amount, 2)
            parent.remaining_amount = round(parent.total_amount - parent.paid_amount, 2)

        if parent.remaining_amount <= 0:
            from datetime import UTC, datetime
            parent.status = PaymentStatus.SETTLED
            parent.settled_at = datetime.now(UTC)
            await self._emit_settled(parent, correlation_id)
        else:
            parent.status = PaymentStatus.PARTIAL
        await self._payments.save(parent)

        return Result.ok({**parent.to_dict(), "splits": children})

    async def record_partial_payment(
        self,
        *,
        payment_id: str,
        amount: float,
        correlation_id: str = "",
    ) -> Result[dict]:
        payment = await self._payments.find_by_id(payment_id)
        if not payment:
            return Result.fail("financial_kernel.errors.payment_not_found")
        try:
            payment.record_partial(amount)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_partial_amount")
        payment.payment_kind = PaymentKind.PARTIAL.value
        await self._payments.save(payment)
        if payment.status == PaymentStatus.SETTLED:
            await self._emit_settled(payment, correlation_id)
        return Result.ok(payment.to_dict())

    async def create_advance_payment(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        payment_method: str,
        amount: float,
        currency: str,
        reference: str,
        payer_id: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        return await self.create_payment(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            payment_method=payment_method,
            amount=amount,
            currency=currency,
            reference=reference,
            payment_kind=PaymentKind.ADVANCE.value,
            payer_id=payer_id,
            correlation_id=correlation_id,
        )

    async def create_installment_plan(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        payment_method: str,
        total_amount: float,
        currency: str,
        reference: str,
        installment_count: int,
        due_dates: list[str],
        idempotency_key: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        schedule = build_installment_schedule(total_amount, installment_count, due_dates)
        parent_result = await self.create_payment(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            payment_method=payment_method,
            amount=total_amount,
            currency=currency,
            reference=reference,
            payment_kind=PaymentKind.INSTALLMENT.value,
            paid_amount=0,
            correlation_id=correlation_id,
        )
        if not parent_result.succeeded:
            return parent_result
        parent = await self._payments.find_by_id(parent_result.unwrap()["id"])
        assert parent is not None
        plan = InstallmentPlan.create(
            tenant_id=tenant_id,
            parent_payment_id=str(parent.id),
            source_context=source_context,
            source_document_id=source_document_id,
            currency=currency,
            total_amount=total_amount,
            installments=schedule,
        )
        await self._installments.save(plan)
        return Result.ok({**parent.to_dict(), "installment_plan": plan.to_dict()})

    async def allocate_payment(
        self,
        *,
        payment_id: str,
        allocations: list[dict] | None = None,
        open_items: list[dict] | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        payment = await self._payments.find_by_id(payment_id)
        if not payment:
            return Result.fail("financial_kernel.errors.payment_not_found")
        final = allocations or (auto_allocate(payment.paid_amount, open_items or []) if open_items else [])
        if not final:
            return Result.fail("financial_kernel.errors.no_allocations")
        payment.apply_allocation(final)
        await self._payments.save(payment)
        await self._emit_allocated(payment, correlation_id)
        return Result.ok(payment.to_dict())

    async def settle_payment(self, payment_id: str, correlation_id: str = "") -> Result[dict]:
        payment = await self._payments.find_by_id(payment_id)
        if not payment:
            return Result.fail("financial_kernel.errors.payment_not_found")
        try:
            payment.settle()
        except ValueError:
            return Result.fail("financial_kernel.errors.payment_not_fully_paid")
        await self._payments.save(payment)
        await self._emit_settled(payment, correlation_id)
        return Result.ok(payment.to_dict())

    async def refund_payment(
        self, payment_id: str, amount: float, correlation_id: str = ""
    ) -> Result[dict]:
        payment = await self._payments.find_by_id(payment_id)
        if not payment:
            return Result.fail("financial_kernel.errors.payment_not_found")
        try:
            payment.refund(amount)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_refund_amount")
        await self._payments.save(payment)
        await publish_integration_event(
            PaymentRefundedIntegration(
                tenant_id=TenantId.create(payment.tenant_id),
                correlation_id=correlation_id,
                payment_id=str(payment.id),
                refund_amount=amount,
                remaining_paid=payment.paid_amount,
            )
        )
        return Result.ok(payment.to_dict())

    async def chargeback_payment(
        self, payment_id: str, amount: float, correlation_id: str = ""
    ) -> Result[dict]:
        payment = await self._payments.find_by_id(payment_id)
        if not payment:
            return Result.fail("financial_kernel.errors.payment_not_found")
        try:
            payment.chargeback(amount)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_chargeback_amount")
        await self._payments.save(payment)
        await publish_integration_event(
            PaymentChargebackIntegration(
                tenant_id=TenantId.create(payment.tenant_id),
                correlation_id=correlation_id,
                payment_id=str(payment.id),
                chargeback_amount=amount,
            )
        )
        return Result.ok(payment.to_dict())

    async def match_payments(
        self, *, tenant_id: str, bank_items: list[dict]
    ) -> Result[dict]:
        payments = await self._payments.list_by_tenant(tenant_id)
        pay_items = [
            {
                "payment_id": str(p.id),
                "reference": p.reference,
                "amount": p.paid_amount,
                "status": p.status,
            }
            for p in payments
            if p.status in (PaymentStatus.SETTLED, PaymentStatus.ALLOCATED, PaymentStatus.PARTIAL)
        ]
        return Result.ok(match_payments_to_bank(pay_items, bank_items))

    async def create_reconciliation(
        self,
        *,
        tenant_id: str,
        reconciliation_date: str,
        payment_items: list[dict],
        bank_items: list[dict],
        bank_reference: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        record = PaymentReconciliation.create(
            tenant_id=tenant_id,
            reconciliation_date=reconciliation_date,
            payment_items=payment_items,
            bank_items=bank_items,
            bank_reference=bank_reference,
        )
        await self._reconciliations.save(record)
        await publish_integration_event(
            PaymentReconciledIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                reconciliation_id=str(record.id),
                status=record.status,
                matched_amount=record.matched_amount,
                variance=record.variance,
            )
        )
        return Result.ok(record.to_dict())

    async def list_payments(self, tenant_id: str) -> Result[list[dict]]:
        payments = await self._payments.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in sorted(payments, key=lambda x: x.created_at, reverse=True)])

    async def get_payment(self, payment_id: str) -> Result[dict]:
        payment = await self._payments.find_by_id(payment_id)
        if not payment:
            return Result.fail("financial_kernel.errors.payment_not_found")
        children = await self._payments.list_children(payment_id)
        data = payment.to_dict()
        if children:
            data["splits"] = [c.to_dict() for c in children]
        return Result.ok(data)

    async def list_reconciliations(self, tenant_id: str) -> Result[list[dict]]:
        records = await self._reconciliations.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in records])

    async def _emit_settled(self, payment: Payment, correlation_id: str) -> None:
        await publish_integration_event(
            PaymentSettledIntegration(
                tenant_id=TenantId.create(payment.tenant_id),
                correlation_id=correlation_id or f"pay-{payment.id}",
                payment_id=str(payment.id),
                amount=payment.paid_amount,
                currency=payment.currency,
                payment_method=payment.payment_method,
                payment_source_context=payment.source_context,
                source_document_id=payment.source_document_id,
            )
        )

    async def _emit_allocated(self, payment: Payment, correlation_id: str) -> None:
        await publish_integration_event(
            PaymentAllocatedIntegration(
                tenant_id=TenantId.create(payment.tenant_id),
                correlation_id=correlation_id or f"alloc-{payment.id}",
                payment_id=str(payment.id),
                allocation_count=len(payment.allocations),
                allocated_amount=round(sum(a.get("amount", 0) for a in payment.allocations), 2),
            )
        )
