"""Enterprise Financial Workflow application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_workflow import (
    FinancialWorkflow,
    FinancialWorkflowType,
)
from contexts.financial_kernel.domain.events.integration_events import (
    FinancialWorkflowApprovedIntegration,
    FinancialWorkflowEscalatedIntegration,
    FinancialWorkflowRejectedIntegration,
    FinancialWorkflowSignedIntegration,
    FinancialWorkflowStartedIntegration,
)
from contexts.financial_kernel.domain.ports.financial_workflow_repositories import (
    IFinancialWorkflowRepository,
)
from contexts.financial_kernel.domain.services.financial_workflow_engine import (
    compute_sla_deadline,
    default_sla_hours,
    escalation_target,
    generate_ai_recommendation,
    sign_workflow,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class FinancialWorkflowApplicationService:
    def __init__(self, workflows: IFinancialWorkflowRepository) -> None:
        self._workflows = workflows

    async def start_workflow(
        self,
        *,
        tenant_id: str,
        workflow_type: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        assignee_id: str,
        started_by: str,
        amount: float | None = None,
        currency: str = "USD",
        sla_hours: int | None = None,
        metadata: dict | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._workflows.find_by_idempotency(tenant_id, idempotency_key)
        if existing:
            return Result.ok(existing.to_dict())

        try:
            FinancialWorkflowType(workflow_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_workflow_type")

        hours = sla_hours if sla_hours is not None else default_sla_hours(workflow_type)
        ai_rec = generate_ai_recommendation(
            workflow_type=workflow_type,
            amount=amount,
            currency=currency,
            metadata=metadata or {},
        )

        workflow = FinancialWorkflow.start(
            tenant_id=tenant_id,
            workflow_type=workflow_type,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            assignee_id=assignee_id,
            sla_hours=hours,
            sla_deadline=compute_sla_deadline(hours),
            started_by=started_by,
            amount=amount,
            currency=currency,
            metadata=metadata,
            ai_recommendation=ai_rec,
        )
        await self._workflows.save(workflow)

        await publish_integration_event(
            FinancialWorkflowStartedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                workflow_id=str(workflow.id),
                workflow_type=workflow_type,
                fin_wf_source_context=source_context,
                source_document_id=source_document_id,
                assignee_id=assignee_id,
                sla_hours=hours,
            )
        )
        return Result.ok(workflow.to_dict())

    async def get_workflow(self, tenant_id: str, workflow_id: str) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")
        return Result.ok(workflow.to_dict())

    async def list_workflows(
        self,
        tenant_id: str,
        workflow_type: str | None = None,
    ) -> Result[list[dict]]:
        if workflow_type:
            try:
                FinancialWorkflowType(workflow_type)
            except ValueError:
                return Result.fail("financial_kernel.errors.invalid_workflow_type")
            items = await self._workflows.list_by_type(tenant_id, workflow_type)
        else:
            items = await self._workflows.list_by_tenant(tenant_id)
        return Result.ok([w.to_dict() for w in items])

    async def list_workflow_types(self) -> Result[list[dict]]:
        return Result.ok(
            [
                {
                    "type": t.value,
                    "sla_hours_default": default_sla_hours(t.value),
                    "capabilities": [
                        "sla",
                        "escalation",
                        "ai_recommendation",
                        "audit",
                        "history",
                        "digital_signature",
                    ],
                }
                for t in FinancialWorkflowType
            ]
        )

    async def approve_workflow(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        actor_id: str,
        comment: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")
        try:
            workflow.approve(actor_id, comment)
        except ValueError:
            return Result.fail("financial_kernel.errors.workflow_terminal")
        await self._workflows.save(workflow)

        await publish_integration_event(
            FinancialWorkflowApprovedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                workflow_id=str(workflow.id),
                workflow_type=workflow.workflow_type,
                approved_by=actor_id,
            )
        )
        return Result.ok(workflow.to_dict())

    async def reject_workflow(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        actor_id: str,
        comment: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")
        try:
            workflow.reject(actor_id, comment)
        except ValueError:
            return Result.fail("financial_kernel.errors.workflow_terminal")
        await self._workflows.save(workflow)

        await publish_integration_event(
            FinancialWorkflowRejectedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                workflow_id=str(workflow.id),
                workflow_type=workflow.workflow_type,
                rejected_by=actor_id,
            )
        )
        return Result.ok(workflow.to_dict())

    async def escalate_workflow(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        actor_id: str,
        escalated_to: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")

        target = escalated_to or escalation_target(workflow.workflow_type, workflow.metadata)
        try:
            workflow.escalate(actor_id, target)
        except ValueError:
            return Result.fail("financial_kernel.errors.workflow_terminal")
        await self._workflows.save(workflow)

        await publish_integration_event(
            FinancialWorkflowEscalatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                workflow_id=str(workflow.id),
                workflow_type=workflow.workflow_type,
                escalated_to=target,
            )
        )
        return Result.ok(workflow.to_dict())

    async def auto_escalate_sla_breached(self, tenant_id: str, correlation_id: str = "") -> Result[list[dict]]:
        breached = await self._workflows.list_pending_sla_breached(tenant_id)
        results = []
        for workflow in breached:
            target = escalation_target(workflow.workflow_type, workflow.metadata)
            workflow.escalate("system", target)
            await self._workflows.save(workflow)
            await publish_integration_event(
                FinancialWorkflowEscalatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    workflow_id=str(workflow.id),
                    workflow_type=workflow.workflow_type,
                    escalated_to=target,
                )
            )
            results.append(workflow.to_dict())
        return Result.ok(results)

    async def get_ai_recommendation(self, tenant_id: str, workflow_id: str) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")

        if not workflow.ai_recommendation:
            rec = generate_ai_recommendation(
                workflow_type=workflow.workflow_type,
                amount=workflow.amount,
                currency=workflow.currency,
                metadata=workflow.metadata,
            )
            workflow.set_ai_recommendation(rec)
            await self._workflows.save(workflow)
        return Result.ok(workflow.ai_recommendation or {})

    async def get_history(self, tenant_id: str, workflow_id: str) -> Result[list[dict]]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")
        return Result.ok([h.to_dict() for h in workflow.history])

    async def sign_workflow(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        signer_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")

        signature = sign_workflow(
            workflow_id=str(workflow.id),
            workflow_type=workflow.workflow_type,
            signer_id=signer_id,
        )
        try:
            workflow.sign(signature, signer_id)
        except ValueError:
            return Result.fail("financial_kernel.errors.not_approved")
        await self._workflows.save(workflow)

        await publish_integration_event(
            FinancialWorkflowSignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                workflow_id=str(workflow.id),
                workflow_type=workflow.workflow_type,
                signer_id=signer_id,
            )
        )
        return Result.ok(workflow.to_dict())

    async def complete_workflow(
        self,
        *,
        tenant_id: str,
        workflow_id: str,
        actor_id: str,
    ) -> Result[dict]:
        workflow = await self._workflows.find_by_id(workflow_id)
        if not workflow or workflow.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.workflow_not_found")
        try:
            workflow.complete(actor_id)
        except ValueError:
            return Result.fail("financial_kernel.errors.not_ready_to_complete")
        await self._workflows.save(workflow)
        return Result.ok(workflow.to_dict())
