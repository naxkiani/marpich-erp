"""ACL — activation/provisioning envelopes → credential orchestration."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def handle_activation_requested(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "identity_lifecycle.activation.requested":
        return
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    registration_ref = str(payload.get("registration_ref") or "")
    tenant_id = str(envelope.get("tenant_id") or "")
    if not registration_ref or not tenant_id:
        return
    from contexts.identity_lifecycle.container import get_registration_onboarding_service

    result = await get_registration_onboarding_service().orchestrate_credentials(
        tenant_id,
        registration_ref,
        correlation_id=str(envelope.get("correlation_id") or ""),
    )
    if not result.succeeded:
        logger.warning(
            "credential_acl_failed tenant=%s ref=%s error=%s",
            tenant_id,
            registration_ref,
            result.error,
        )


async def handle_provisioning_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "identity_lifecycle.provisioning.completed":
        return
    # Credentials are orchestrated on activation.requested (after provision completes).
    return
