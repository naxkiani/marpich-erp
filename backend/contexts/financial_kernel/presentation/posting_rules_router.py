"""Enterprise Posting Rule Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    ExecutePostingRequest,
    PreviewPostingRuleRequest,
    RuleBuilderRequest,
    UpdatePostingRuleRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

posting_rules_router = APIRouter(
    prefix="/financial-kernel/posting-rules", tags=["Posting Rule Engine"]
)


def _serialize_slots(slots: dict | None) -> dict | None:
    if slots is None:
        return None
    return {name: slot.model_dump() for name, slot in slots.items()}


def _serialize_templates(templates: list | None) -> list[dict] | None:
    if templates is None:
        return None
    return [t.model_dump() for t in templates]


@posting_rules_router.get("")
async def list_posting_rules(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.posting_rules.read"))],
):
    return {"data": (await get_financial_kernel_service().list_enterprise_posting_rules(tenant_id)).unwrap()}


@posting_rules_router.get("/{rule_id}")
async def get_posting_rule(
    rule_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.posting_rules.read"))],
):
    result = await get_financial_kernel_service().get_enterprise_posting_rule(tenant_id, rule_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@posting_rules_router.post("/builder", status_code=status.HTTP_201_CREATED)
async def create_posting_rule(
    body: RuleBuilderRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.posting_rules.write"))],
):
    result = await get_financial_kernel_service().build_posting_rule(
        tenant_id=tenant_id,
        rule_id=body.rule_id,
        label=body.label,
        module=body.module,
        journal_type=body.journal_type,
        pattern=body.pattern,
        account_slots=_serialize_slots(body.account_slots) or {},
        line_templates=_serialize_templates(body.line_templates) or [],
        approval_required=body.approval_required,
        tax_amount_field=body.tax_amount_field,
        tax_account_slot=body.tax_account_slot,
        dimensions=body.dimensions,
        description=body.description,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@posting_rules_router.put("/{rule_id}")
async def update_posting_rule(
    rule_id: str,
    body: UpdatePostingRuleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.posting_rules.write"))],
):
    result = await get_financial_kernel_service().update_posting_rule(
        tenant_id=tenant_id,
        rule_id=rule_id,
        label=body.label,
        account_slots=_serialize_slots(body.account_slots),
        line_templates=_serialize_templates(body.line_templates),
        approval_required=body.approval_required,
        description=body.description,
        is_active=body.is_active,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@posting_rules_router.post("/preview")
async def preview_posting_rule(
    body: PreviewPostingRuleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.posting_rules.read"))],
):
    result = await get_financial_kernel_service().preview_posting_rule_execution(
        tenant_id=tenant_id,
        rule_id=body.rule_id,
        amount=body.amount,
        account_mappings=body.account_mappings,
        lines=[line.model_dump() for line in body.lines] if body.lines else None,
        description=body.description,
        dimensions=body.dimensions,
        tax_amount=body.tax_amount,
        use_default_accounts=body.use_default_accounts,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@posting_rules_router.post("/execute", status_code=status.HTTP_201_CREATED)
async def execute_posting(
    body: ExecutePostingRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.posting_rules.execute"))],
):
    result = await get_financial_kernel_service().execute_posting(
        tenant_id=tenant_id,
        rule_id=body.rule_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        currency=body.currency,
        correlation_id=correlation_id,
        amount=body.amount,
        account_mappings=body.account_mappings,
        lines=[line.model_dump() for line in body.lines] if body.lines else None,
        description=body.description,
        dimensions=body.dimensions,
        tax_amount=body.tax_amount,
        idempotency_key=body.idempotency_key,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        use_default_accounts=body.use_default_accounts,
        require_approval=body.require_approval,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
