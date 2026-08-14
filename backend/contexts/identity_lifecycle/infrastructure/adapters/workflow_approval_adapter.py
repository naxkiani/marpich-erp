"""Workflow approval adapter — starts platform Workflow for registration approvals."""
from __future__ import annotations

from contexts.identity_lifecycle.domain.ports.provisioning import IWorkflowApprovalPort
from contexts.workflow.container import get_workflow_service

REGISTRATION_APPROVAL_KEY = "identity_lifecycle.registration.approval"


class WorkflowApprovalAdapter(IWorkflowApprovalPort):
    async def ensure_registration_approval_definition(self, tenant_id: str) -> None:
        wf = get_workflow_service()
        existing = await wf.list_definitions(tenant_id)
        keys = {d["key"] for d in (existing.unwrap() if existing.succeeded else [])}
        if REGISTRATION_APPROVAL_KEY in keys:
            return
        await wf.deploy_definition(
            tenant_id=tenant_id,
            key=REGISTRATION_APPROVAL_KEY,
            name="Identity registration approval",
            steps=[{"key": "registration_review", "name": "Review registration"}],
        )

    async def start_registration_approval(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        registration_ref: str,
        started_by: str,
        assignee_id: str | None = None,
    ) -> dict:
        await self.ensure_registration_approval_definition(tenant_id)
        result = await get_workflow_service().start_instance(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            definition_key=REGISTRATION_APPROVAL_KEY,
            context={
                "registration_ref": registration_ref,
                "source_context": "identity_lifecycle",
            },
            assignees={"registration_review": assignee_id or started_by, "*": assignee_id or started_by},
            started_by=started_by,
        )
        if not result.succeeded:
            raise ValueError(result.error or "workflow.errors.start_failed")
        return result.unwrap()
