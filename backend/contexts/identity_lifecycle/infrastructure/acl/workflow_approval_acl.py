"""ACL — Workflow process outcomes → registration approve/reject."""
from __future__ import annotations

import logging

from contexts.identity_lifecycle.infrastructure.adapters.workflow_approval_adapter import (
    REGISTRATION_APPROVAL_KEY,
)

logger = logging.getLogger(__name__)


async def handle_workflow_process_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "workflow.process.completed":
        return
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    definition_key = str(payload.get("definition_key") or "")
    if definition_key != REGISTRATION_APPROVAL_KEY:
        return
    instance_id = str(payload.get("instance_id") or "")
    status = str(payload.get("status") or "")
    tenant_id = str(envelope.get("tenant_id") or "")
    if not instance_id or not tenant_id:
        return

    from contexts.workflow.container import get_workflow_service

    instance_result = await get_workflow_service().get_instance(tenant_id, instance_id)
    if not instance_result.succeeded:
        logger.warning("workflow_acl_instance_missing instance=%s", instance_id)
        return
    context = (instance_result.unwrap().get("instance") or {}).get("context") or {}
    registration_ref = str(context.get("registration_ref") or "")
    if not registration_ref:
        return

    from contexts.identity_lifecycle.container import get_registration_onboarding_service

    svc = get_registration_onboarding_service()
    corr = str(envelope.get("correlation_id") or "")
    if status == "rejected":
        await svc.reject_registration(
            tenant_id,
            registration_ref,
            reason="workflow_rejected",
            correlation_id=corr,
            actor_id="workflow",
        )
        return
    if status in {"completed", "approved"}:
        await svc.approve_registration(
            tenant_id,
            registration_ref,
            correlation_id=corr,
            actor_id="workflow",
            force=True,
        )
