"""Enterprise Payment Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_payment_service
from contexts.financial_kernel.presentation.payment_schemas import (
    AllocatePaymentRequest,
    ChargebackRequest,
    CreateInstallmentRequest,
    CreatePaymentReconciliationRequest,
    CreatePaymentRequest,
    CreateSplitPaymentRequest,
    MatchPaymentsRequest,
    PartialPaymentRequest,
    RefundRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

payments_router = APIRouter(prefix="/financial-kernel/payments", tags=["Payment Platform"])


@payments_router.post("", status_code=status.HTTP_201_CREATED)
async def create_payment(
    body: CreatePaymentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}"
    result = await get_payment_service().create_payment(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        idempotency_key=key,
        payment_method=body.payment_method,
        amount=body.amount,
        currency=body.currency,
        reference=body.reference,
        paid_amount=body.paid_amount,
        allocations=[a.model_dump() for a in body.allocations] if body.allocations else None,
        payer_id=body.payer_id,
        auto_allocate_open_items=[i.model_dump() for i in body.open_items] if body.open_items else None,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/split", status_code=status.HTTP_201_CREATED)
async def create_split_payment(
    body: CreateSplitPaymentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}:split"
    result = await get_payment_service().create_split_payment(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        idempotency_key=key,
        payment_method=body.payment_method,
        total_amount=body.total_amount,
        currency=body.currency,
        reference=body.reference,
        splits=[s.model_dump() for s in body.splits],
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/advance", status_code=status.HTTP_201_CREATED)
async def create_advance_payment(
    body: CreatePaymentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}:advance"
    result = await get_payment_service().create_advance_payment(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        idempotency_key=key,
        payment_method=body.payment_method,
        amount=body.amount,
        currency=body.currency,
        reference=body.reference,
        payer_id=body.payer_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/installments", status_code=status.HTTP_201_CREATED)
async def create_installment_plan(
    body: CreateInstallmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}:install"
    result = await get_payment_service().create_installment_plan(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        payment_method=body.payment_method,
        total_amount=body.total_amount,
        currency=body.currency,
        reference=body.reference,
        installment_count=body.installment_count,
        due_dates=body.due_dates,
        idempotency_key=key,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.get("")
async def list_payments(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.read"))],
):
    return {"data": (await get_payment_service().list_payments(tenant_id)).unwrap()}


@payments_router.get("/reconciliation/list")
async def list_payment_reconciliations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.read"))],
):
    return {"data": (await get_payment_service().list_reconciliations(tenant_id)).unwrap()}


@payments_router.get("/{payment_id}")
async def get_payment(
    payment_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.read"))],
):
    result = await get_payment_service().get_payment(payment_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@payments_router.post("/{payment_id}/partial")
async def record_partial_payment(
    payment_id: str,
    body: PartialPaymentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    result = await get_payment_service().record_partial_payment(
        payment_id=payment_id, amount=body.amount, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/{payment_id}/allocate")
async def allocate_payment(
    payment_id: str,
    body: AllocatePaymentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    result = await get_payment_service().allocate_payment(
        payment_id=payment_id,
        allocations=[a.model_dump() for a in body.allocations] if body.allocations else None,
        open_items=[i.model_dump() for i in body.open_items] if body.open_items else None,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/{payment_id}/settle")
async def settle_payment(
    payment_id: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    result = await get_payment_service().settle_payment(payment_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: str,
    body: RefundRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    result = await get_payment_service().refund_payment(
        payment_id=payment_id, amount=body.amount, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/{payment_id}/chargeback")
async def chargeback_payment(
    payment_id: str,
    body: ChargebackRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.write"))],
):
    result = await get_payment_service().chargeback_payment(
        payment_id=payment_id, amount=body.amount, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@payments_router.post("/matching")
async def match_payments(
    body: MatchPaymentsRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.read"))],
):
    return {
        "data": (
            await get_payment_service().match_payments(
                tenant_id=tenant_id,
                bank_items=[b.model_dump() for b in body.bank_items],
            )
        ).unwrap()
    }


@payments_router.post("/reconciliation", status_code=status.HTTP_201_CREATED)
async def create_payment_reconciliation(
    body: CreatePaymentReconciliationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.payments.reconcile"))],
):
    result = await get_payment_service().create_reconciliation(
        tenant_id=tenant_id,
        reconciliation_date=body.reconciliation_date,
        payment_items=[p.model_dump() for p in body.payment_items],
        bank_items=[b.model_dump() for b in body.bank_items],
        bank_reference=body.bank_reference,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
