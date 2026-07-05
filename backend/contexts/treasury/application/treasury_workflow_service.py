"""Treasury Workflow application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_workflow_engine import (
    TreasuryWorkflowAudit,
    TreasuryWorkflowDefinition,
    TreasuryWorkflowLimit,
    TreasuryWorkflowRequest,
    WorkflowType,
)
from contexts.treasury.domain.events.integration_events import (
    BankAccountApprovalRequestedIntegration,
    TreasuryTransactionApprovalRequestedIntegration,
    TreasuryTransferApprovalRequestedIntegration,
)
from contexts.treasury.domain.ports.treasury_workflow_repositories import (
    IWorkflowAuditRepository,
    IWorkflowDefinitionRepository,
    IWorkflowLimitRepository,
    IWorkflowRequestRepository,
)
from contexts.treasury.domain.services.treasury_workflow_engine import (
    APPROVAL_EVENT_MAP,
    build_workflow_dashboard,
    build_workflow_designer_view,
    build_workflow_steps,
    generate_digital_signature_hash,
    list_workflow_catalog,
    list_workflow_states,
    monitor_sla,
    resolve_required_levels,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class TreasuryWorkflowApplicationService:
    def __init__(
        self,
        definitions: IWorkflowDefinitionRepository,
        limits: IWorkflowLimitRepository,
        requests: IWorkflowRequestRepository,
        audits: IWorkflowAuditRepository,
    ) -> None:
        self._definitions = definitions
        self._limits = limits
        self._requests = requests
        self._audits = audits

    async def _audit(
        self,
        *,
        tenant_id: str,
        request_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> None:
        entry = TreasuryWorkflowAudit.create(
            tenant_id=tenant_id,
            request_id=request_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )
        await self._audits.save(entry)

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_workflow_catalog())

    async def list_workflow(self) -> Result[list[dict]]:
        return Result.ok(list_workflow_states())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        requests = await self._requests.list_by_tenant(tenant_id)
        definitions = await self._definitions.list_by_tenant(tenant_id)
        limits = await self._limits.list_by_tenant(tenant_id)
        sorted_reqs = sorted(requests, key=lambda r: r.created_at, reverse=True)
        return Result.ok(
            build_workflow_dashboard(
                requests=[r.to_dict() for r in sorted_reqs],
                definitions=[d.to_dict() for d in definitions],
                limits=[l.to_dict() for l in limits],
            )
        )

    async def get_designer(self, tenant_id: str) -> Result[dict]:
        definitions = await self._definitions.list_by_tenant(tenant_id)
        return Result.ok(
            build_workflow_designer_view(definitions=[d.to_dict() for d in definitions])
        )

    async def list_definitions(self, tenant_id: str) -> Result[list[dict]]:
        defs = await self._definitions.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in defs])

    async def create_definition(
        self,
        *,
        tenant_id: str,
        name: str,
        workflow_type: str,
        approval_mode: str,
        steps: list[dict],
        sla_hours: int = 48,
        description: str = "",
    ) -> Result[dict]:
        try:
            WorkflowType(workflow_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_workflow_type")

        definition = TreasuryWorkflowDefinition.create(
            tenant_id=tenant_id,
            name=name,
            workflow_type=workflow_type,
            approval_mode=approval_mode,
            steps=steps,
            sla_hours=sla_hours,
            description=description,
        )
        await self._definitions.save(definition)
        return Result.ok(definition.to_dict())

    async def list_limits(self, tenant_id: str) -> Result[list[dict]]:
        limits = await self._limits.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in limits])

    async def create_limit(
        self,
        *,
        tenant_id: str,
        workflow_type: str,
        name: str,
        max_amount: float,
        currency: str = "USD",
        approval_levels: int = 1,
    ) -> Result[dict]:
        try:
            WorkflowType(workflow_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_workflow_type")

        limit = TreasuryWorkflowLimit.create(
            tenant_id=tenant_id,
            workflow_type=workflow_type,
            name=name,
            max_amount=max_amount,
            currency=currency,
            approval_levels=approval_levels,
        )
        await self._limits.save(limit)
        return Result.ok(limit.to_dict())

    async def create_request(
        self,
        *,
        tenant_id: str,
        workflow_type: str,
        amount: float,
        currency: str,
        subject_ref: str,
        subject_type: str,
        requester_id: str,
        title: str,
        description: str = "",
        definition_id: str | None = None,
    ) -> Result[dict]:
        try:
            WorkflowType(workflow_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_workflow_type")

        definitions = await self._definitions.list_by_tenant(tenant_id)
        definition = None
        if definition_id:
            definition = await self._definitions.find_by_id(definition_id)
        else:
            definition = next(
                (d for d in definitions if d.workflow_type == workflow_type and d.is_active),
                None,
            )

        limits = await self._limits.list_by_tenant(tenant_id)
        required_levels = resolve_required_levels(
            amount, [l.to_dict() for l in limits], workflow_type
        )

        if definition:
            approval_mode = definition.approval_mode
            steps = definition.steps or build_workflow_steps(
                approval_mode=approval_mode, required_levels=required_levels
            )
            sla_hours = definition.sla_hours
            def_id = str(definition.id)
        else:
            approval_mode = "sequential"
            steps = build_workflow_steps(
                approval_mode=approval_mode, required_levels=max(required_levels, 1)
            )
            sla_hours = 48
            def_id = ""

        request = TreasuryWorkflowRequest.create(
            tenant_id=tenant_id,
            workflow_type=workflow_type,
            definition_id=def_id,
            approval_mode=approval_mode,
            amount=amount,
            currency=currency,
            subject_ref=subject_ref,
            subject_type=subject_type,
            requester_id=requester_id,
            title=title,
            description=description,
            steps=steps,
            sla_hours=sla_hours,
        )
        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=str(request.id),
            action="created",
            actor_id=requester_id,
            detail=f"{workflow_type} request created",
        )
        return Result.ok(request.to_dict())

    async def submit_request(
        self, request_id: str, *, tenant_id: str, actor_id: str
    ) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("treasury.errors.workflow_request_not_found")

        sla_hours = 48
        if request.definition_id:
            definition = await self._definitions.find_by_id(request.definition_id)
            if definition:
                sla_hours = definition.sla_hours

        try:
            request.submit(sla_hours=sla_hours)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=request_id,
            action="submitted",
            actor_id=actor_id,
        )
        await self._publish_approval_event(request)
        return Result.ok(request.to_dict())

    async def approve_step(
        self,
        request_id: str,
        *,
        tenant_id: str,
        step_id: str,
        approver_id: str,
        comment: str = "",
        with_signature: bool = True,
    ) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("treasury.errors.workflow_request_not_found")

        signature_hash = None
        if with_signature:
            signature_hash = generate_digital_signature_hash(
                request_id=request_id, step_id=step_id, approver_id=approver_id
            )

        try:
            request.approve_step(
                step_id=step_id,
                approver_id=approver_id,
                signature_hash=signature_hash,
                comment=comment,
            )
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=request_id,
            action="approved",
            actor_id=approver_id,
            detail=f"Step {step_id} approved",
        )
        return Result.ok(request.to_dict())

    async def reject_request(
        self,
        request_id: str,
        *,
        tenant_id: str,
        approver_id: str,
        comment: str = "",
    ) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("treasury.errors.workflow_request_not_found")

        try:
            request.reject(approver_id=approver_id, comment=comment)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=request_id,
            action="rejected",
            actor_id=approver_id,
            detail=comment,
        )
        return Result.ok(request.to_dict())

    async def delegate_step(
        self,
        request_id: str,
        *,
        tenant_id: str,
        step_id: str,
        from_user: str,
        to_user: str,
        reason: str = "",
    ) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("treasury.errors.workflow_request_not_found")

        try:
            request.delegate(step_id=step_id, from_user=from_user, to_user=to_user, reason=reason)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=request_id,
            action="delegated",
            actor_id=from_user,
            detail=f"Delegated to {to_user}: {reason}",
        )
        return Result.ok(request.to_dict())

    async def escalate_request(
        self,
        request_id: str,
        *,
        tenant_id: str,
        escalated_to: str,
        actor_id: str,
        reason: str = "sla_breach",
    ) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("treasury.errors.workflow_request_not_found")

        try:
            request.escalate(escalated_to=escalated_to, reason=reason)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=request_id,
            action="escalated",
            actor_id=actor_id,
            detail=f"Escalated to {escalated_to}: {reason}",
        )
        return Result.ok(request.to_dict())

    async def execute_request(
        self, request_id: str, *, tenant_id: str, actor_id: str
    ) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("treasury.errors.workflow_request_not_found")

        try:
            request.execute()
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._requests.save(request)
        await self._audit(
            tenant_id=tenant_id,
            request_id=request_id,
            action="executed",
            actor_id=actor_id,
        )
        return Result.ok(request.to_dict())

    async def list_requests(self, tenant_id: str) -> Result[list[dict]]:
        requests = await self._requests.list_by_tenant(tenant_id)
        return Result.ok(
            [r.to_dict() for r in sorted(requests, key=lambda x: x.created_at, reverse=True)]
        )

    async def get_request(self, request_id: str) -> Result[dict]:
        request = await self._requests.find_by_id(request_id)
        if not request:
            return Result.fail("treasury.errors.workflow_request_not_found")
        return Result.ok(request.to_dict())

    async def get_audit_trail(self, request_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_request(request_id)
        return Result.ok([e.to_dict() for e in entries])

    async def get_sla_monitoring(self, tenant_id: str) -> Result[dict]:
        requests = await self._requests.list_by_tenant(tenant_id)
        return Result.ok(monitor_sla(requests=[r.to_dict() for r in requests]))

    async def _publish_approval_event(self, request: TreasuryWorkflowRequest) -> None:
        event_name = APPROVAL_EVENT_MAP.get(request.workflow_type)
        if not event_name:
            return

        tenant = TenantId.create(request.tenant_id)
        correlation_id = f"workflow-{request.id}"

        if event_name == "treasury.transfer.approval.requested":
            await publish_integration_event(
                TreasuryTransferApprovalRequestedIntegration(
                    tenant_id=tenant,
                    correlation_id=correlation_id,
                    transfer_id=request.subject_ref,
                    amount=request.amount,
                    instrument=request.workflow_type,
                )
            )
        elif event_name == "treasury.bank_account.approval.requested":
            await publish_integration_event(
                BankAccountApprovalRequestedIntegration(
                    tenant_id=tenant,
                    correlation_id=correlation_id,
                    bank_account_id=request.subject_ref,
                    code=request.title,
                    account_type=request.subject_type,
                )
            )
        elif event_name == "treasury.transaction.approval.requested":
            await publish_integration_event(
                TreasuryTransactionApprovalRequestedIntegration(
                    tenant_id=tenant,
                    correlation_id=correlation_id,
                    transaction_id=request.subject_ref,
                    transaction_type=request.workflow_type,
                    amount=request.amount,
                    currency=request.currency,
                    required_approval_levels=len(request.steps),
                )
            )

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._definitions.list_by_tenant(tenant_id):
            return

        defaults = [
            (WorkflowType.TRANSFER_APPROVAL.value, "Standard Transfer Approval", "sequential", 24),
            (WorkflowType.PAYMENT_APPROVAL.value, "Payment Approval", "sequential", 24),
            (WorkflowType.FUND_REQUEST.value, "Fund Request", "sequential", 48),
            (WorkflowType.CASH_REQUEST.value, "Cash Request", "sequential", 24),
            (WorkflowType.CASH_TRANSFER.value, "Cash Transfer", "sequential", 24),
            (WorkflowType.INVESTMENT_APPROVAL.value, "Investment Approval", "parallel", 72),
            (WorkflowType.BANK_ACCOUNT_APPROVAL.value, "Bank Account Approval", "sequential", 48),
        ]

        for wtype, name, mode, sla in defaults:
            levels = 2 if wtype == WorkflowType.INVESTMENT_APPROVAL.value else 1
            steps = build_workflow_steps(approval_mode=mode, required_levels=levels)
            definition = TreasuryWorkflowDefinition.create(
                tenant_id=tenant_id,
                name=name,
                workflow_type=wtype,
                approval_mode=mode,
                steps=steps,
                sla_hours=sla,
            )
            await self._definitions.save(definition)

        limit_defaults = [
            (WorkflowType.TRANSFER_APPROVAL.value, "Transfer Tier 1", 10000, 1),
            (WorkflowType.TRANSFER_APPROVAL.value, "Transfer Tier 2", 50000, 2),
            (WorkflowType.TRANSFER_APPROVAL.value, "Transfer Tier 3", 999999999, 3),
            (WorkflowType.PAYMENT_APPROVAL.value, "Payment Tier 1", 25000, 1),
            (WorkflowType.INVESTMENT_APPROVAL.value, "Investment Tier 1", 100000, 2),
        ]
        for wtype, name, max_amt, levels in limit_defaults:
            limit = TreasuryWorkflowLimit.create(
                tenant_id=tenant_id,
                workflow_type=wtype,
                name=name,
                max_amount=max_amt,
                approval_levels=levels,
            )
            await self._limits.save(limit)
